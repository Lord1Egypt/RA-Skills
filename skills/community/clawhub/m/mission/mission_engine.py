from logger import log_journal

def create_mission_plan(goal):
    tasks = [
        {"name": f"Break down goal: {goal}", "priority": 1},
        {"name": "Identify highest impact action", "priority": 1},
        {"name": "Execute first action immediately", "priority": 1}
    ]
    log_journal(f"Mission created: {goal}")
    return tasks
