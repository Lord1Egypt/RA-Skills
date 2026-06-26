# -*- coding: utf-8 -*-
import sqlite3
import os
import json
from datetime import datetime

RECOMMENDATION_PATH = "/root/.schema/recommendation.json"

REDUNDANT_PATTERNS = [
    "_email_",
    "_temp_",
    "_auto_",
    "_idx_",
    "_bak_",
]


def run(db_path="/var/db/app.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    all_indexes = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    conn.close()

    redundant_indexes = []
    for idx in all_indexes:
        for pattern in REDUNDANT_PATTERNS:
            if pattern in idx.lower():
                redundant_indexes.append(idx)
                break

    recommendation = {
        "indexes_to_drop": redundant_indexes,
        "generated_at": datetime.utcnow().isoformat(),
    }
    os.makedirs(os.path.dirname(RECOMMENDATION_PATH), exist_ok=True)
    with open(RECOMMENDATION_PATH, "w") as f:
        json.dump(recommendation, f, indent=2)

    return {
        "analysis_timestamp": datetime.utcnow().isoformat(),
        "tables": tables,
        "total_indexes": len(all_indexes),
        "all_indexes": all_indexes,
        "redundant_indexes": redundant_indexes,
        "recommendation_file": RECOMMENDATION_PATH,
        "status": "completed",
    }


if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else "/var/db/app.db"
    result = run(db_path)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
