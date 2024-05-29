import math
from cell import states, cell
import pygame
import drawfn

ACTION_EAST = 0
ACTION_SOUTH = 1
ACTION_WEST = 2
ACTION_NORTH = 3

TRANSITION_SUCCEED = 0.8
TRANSITION_FAIL = 0.2
GAMMA = 0.9
ACTION_REWARD = -0.1
CONVERGENCE = 0.0000001
cur_convergence = 100

def computeQValue(s, action):
    q_value = 0.0
    cell = states[s[1]][s[0]]
    
    # Compute the new state based on the action
    if action == ACTION_SOUTH:
        new_state = (s[0], s[1] + 1)
    elif action == ACTION_WEST:
        new_state = (s[0] - 1, s[1])
    elif action == ACTION_EAST:
        new_state = (s[0] + 1, s[1])
    elif action == ACTION_NORTH:
        new_state = (s[0], s[1] - 1)
    else:
        raise ValueError("Invalid action!")

    if 0 <= new_state[0] < len(states[0]) and 0 <= new_state[1] < len(states):
        q_value = (
            TRANSITION_SUCCEED * (ACTION_REWARD + GAMMA * states[new_state[1]][new_state[0]].state_value) +
            TRANSITION_FAIL * (ACTION_REWARD + GAMMA * cell.state_value)
        )

    return q_value

def valueIteration():
    print('Value Iteration.')
    global cur_convergence
    new_state_values = [[0.0] * len(states[0]) for _ in range(len(states))]
    for j in range(len(states)):
        for i in range(len(states[0])):
            cell = states[j][i]
            blocked_cells = {(1, 1), (3, 0), (3, 1)}
            if (i, j) not in blocked_cells:
                actions = [ACTION_SOUTH, ACTION_WEST, ACTION_EAST, ACTION_NORTH]
                q_values = [computeQValue((i, j), action) for action in actions]
                cell.q_values = q_values
                new_state_values[j][i] = max(q_values)
    max_change = max(abs(states[j][i].state_value - new_state_values[j][i]) for j in range(len(states)) for i in range(len(states[0])))

    for j in range(len(states)):
        for i in range(len(states[0])):
            states[j][i].state_value = new_state_values[j][i]

    cur_convergence = max_change

def policyEvaluation():
    print('Policy Evaluation')
    global cur_convergence
    new_state_values = [[0.0 for _ in range(len(states[0]))] for _ in range(len(states))]
    def is_blocked(i, j):
        return (i, j) in [(1, 1), (3, 0), (3, 1)]
    def updated_values(i, j, action, new_value):
        if not is_blocked(i, j):
            new_state_values[j][i] = new_value
    while(1):
        delta = 0.0
        for j in range(len(states)):
            for i in range(len(states[0])):
                cell = states[j][i]
                if is_blocked(i, j):
                    continue
                old_value = cell.state_value
                action = cell.policy
                new_value = computeQValue((i, j), action)
                updated_values(i, j, action, new_value)
                delta = max(delta, abs(old_value - new_value))
        if delta < CONVERGENCE:
            break
        for j in range(len(states)):
            for i in range(len(states[0])):
                cell = states[j][i]
                if not is_blocked(i, j):
                    cell.state_value = new_state_values[j][i]

def policyImprovement():
    print('Policy Improvement.')

    def is_blocked(i, j):
        return (i, j) in [(1, 1), (3, 0), (3, 1)]

    for j in range(len(states)):
        for i in range(len(states[0])):
            cell = states[j][i]
            if not is_blocked(i, j):
                actions = [ACTION_SOUTH, ACTION_WEST, ACTION_EAST, ACTION_NORTH]
                q_values = [computeQValue((i, j), action) for action in actions]
                best_action_index = q_values.index(max(q_values))
                cell.policy = actions[best_action_index]

################################# Dont modify the code below ###########################
def policyIteration():
    drawfn.check2=True
    drawfn.radio1=False
    drawfn.radio2=True
    policies={}
    for s in states:
        for cell in s:
            policies[cell.location]=cell.policy
    #policies should be a dictionary with states[][].location as it's key and states[][].policy as value
    i=0
    while True:
        i+=1
        oldPolicy=policies.copy()
        policyEvaluation()
        policyImprovement()
        for s in states:
            for cell in s:
                if ((cell.location[0] == 1 and cell.location[1] == 1) or (cell.location[0] == 3 and cell.location[1] == 0) or  (cell.location[0] == 3 and cell.location[1] == 1)):
                    continue
                else:
                    policies[cell.location]=cell.policy

        drawfn.draw()
        pygame.time.delay(200)
        drawfn.screen.fill(pygame.Color(255,255,255),pygame.Rect(300,580,150,20))
        fnt = pygame.font.SysFont("Bahnschrift", 20)
        iterText = fnt.render("Iterations: "+str(i), 1, (0,0,0))
        drawfn.screen.blit(iterText, (300,580))
        pygame.display.update()
        
        if all(oldPolicy[key] == policies[key] for key in policies):
            print('Ideal Policy Obtained.')
            break
  
def onGo(idx):
        # global idx
        if(idx<=100 and cur_convergence>CONVERGENCE):
            valueIteration()
            drawfn.screen.fill(pygame.Color(255,255,255),pygame.Rect(300,580,150,20))
            fnt = pygame.font.SysFont("Bahnschrift", 20)
            iterText = fnt.render("Iterations: "+str(idx), 1, (0,0,0))
            drawfn.screen.blit(iterText, (300,580))
            return True
        else:
            return False
