from datetime import datetime

def log_journal(entry):
    with open("../logs/journal.log", "a") as f:
        f.write(f"[{datetime.now()}] {entry}\n")
