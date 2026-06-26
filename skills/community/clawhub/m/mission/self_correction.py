from logger import log_journal

def evaluate_progress(results):
    lessons = []
    for r in results:
        lessons.append(f"Completed: {r}")
    log_journal("Lessons Learned: " + "; ".join(lessons))
    return lessons
