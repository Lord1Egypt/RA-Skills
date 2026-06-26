# Elephas Initialization Pattern

Use this pattern when implementing `_open_db` for Elephas. The database auto-initializes on first use — no manual init command is needed.

```python
import real_ladybug as lb
from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path("~/openclaw").expanduser()
DB_PATH = ROOT / "db/ocas-elephas/chronicle.lbug"
INTAKE = ROOT / "db/ocas-elephas/intake"
STAGING = ROOT / "db/ocas-elephas/staging"
JOURNALS = ROOT / "journals/ocas-elephas"
CONFIG_PATH = ROOT / "db/ocas-elephas/config.json"

def _open_db(read_only=False):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    INTAKE.mkdir(parents=True, exist_ok=True)
    (INTAKE / "processed").mkdir(parents=True, exist_ok=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    JOURNALS.mkdir(parents=True, exist_ok=True)
    _ensure_config()
    db = lb.Database(str(DB_PATH), read_only=read_only)
    conn = lb.Connection(db)
    if not read_only:
        _ensure_init(conn)
    return db, conn

def _ensure_init(conn):
    tables = {row[0] for row in conn.execute("CALL show_tables() RETURN *")}
    if "Entity" not in tables:
        _run_ddl(conn)

def _run_ddl(conn):
    # Full DDL in references/schemas.md
    pass
```

Full schema DDL is in `references/schemas.md`.
