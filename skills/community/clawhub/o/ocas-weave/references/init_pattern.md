# Weave Initialization Pattern

Use this pattern when implementing `_open_db` for Weave. The database auto-initializes on first use — no manual init command is needed.

```python
import real_ladybug as lb
from pathlib import Path

ROOT = Path("~/openclaw").expanduser()
DB_PATH = ROOT / "db/ocas-weave/weave.lbug"
STAGING = ROOT / "db/ocas-weave/staging"
JOURNALS = ROOT / "journals/ocas-weave"

def _open_db(read_only=False):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    db = lb.Database(str(DB_PATH), read_only=read_only)
    conn = lb.Connection(db)
    if not read_only:
        _ensure_init(conn)
    return db, conn

def _ensure_init(conn):
    tables = {row[0] for row in conn.execute("CALL show_tables() RETURN *")}
    if "Person" not in tables:
        _run_ddl(conn)

def _run_ddl(conn):
    # Full DDL from references/schemas.md
    pass  # See references/schemas.md for complete DDL
```

Full schema DDL is in `references/schemas.md`.
