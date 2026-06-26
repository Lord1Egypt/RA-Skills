---
name: mc-db-discovery
description: Systematic workflow to locate and verify the Mission Control SQLite database when path assumptions fail, and reconcile frontend/backend schema mismatches.
---

- Step 1: When DB file not found at expected path, trace createDb() calls in server code to find the resolvedPath (defaults to ~/.mc/data/mission-control.db).
- Step 2: Verify DB existence with: ls -la ~/.mc/data/mission-control.db
- Step 3: Inspect schema with: sqlite3 ~/.mc/data/mission-control.db ".schema tasks"
- Step 4: Check actual column names (e.g., 'state' vs 'status'); adjust frontend types or backend schema accordingly.
- Step 5: Validate data inserted correctly: sqlite3 ~/.mc/data/mission-control.db "SELECT * FROM tasks ORDER BY timestamp DESC LIMIT 5;"
- Pitfall: The frontend Task interface may use 'status' while the DB uses 'state'; always verify before debugging application logic.
