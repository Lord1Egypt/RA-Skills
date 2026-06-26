# -*- coding: utf-8 -*-
import os
import sqlite3
import json
from datetime import datetime


def run(migrations_dir="/migrations", db_path="/var/db/app.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT filename FROM _migrations")
    applied = set(r[0] for r in cur.fetchall())
    conn.close()

    all_migrations = sorted(os.listdir(migrations_dir)) if os.path.isdir(migrations_dir) else []
    pending = [m for m in all_migrations if m not in applied and m.endswith(".sql")]

    validation_errors = []
    for m in all_migrations:
        filepath = os.path.join(migrations_dir, m)
        if not m.endswith(".sql"):
            continue
        with open(filepath) as f:
            sql = f.read()
        try:
            conn = sqlite3.connect(":memory:")
            cur = conn.cursor()
            cur.executescript(sql)
            conn.close()
        except Exception as e:
            validation_errors.append({"migration": m, "error": str(e)})

    return {
        "validation_timestamp": datetime.utcnow().isoformat(),
        "migrations_found": all_migrations,
        "applied_migrations": list(applied),
        "pending_migrations": pending,
        "validation_errors": validation_errors,
        "status": "completed",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
