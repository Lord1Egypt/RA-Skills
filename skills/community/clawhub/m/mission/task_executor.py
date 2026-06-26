from logger import log_journal

def execute_tasks(tasks):
    results = []
    for task in tasks:
        result = f"Executing: {task['name']}"
        log_journal(result)
        results.append(result)
    return results
