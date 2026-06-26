# Cross-DB Linking

LadybugDB supports read-only queries against external `.lbug` databases. Weave may query other skill databases for enrichment. Never open another skill's database as READ_WRITE.

## Key constraints

Attached and externally opened databases are READ-ONLY.
Only one ATTACH active at a time. After ATTACH, the active context switches — weave.lbug is inaccessible until DETACH.
Do not ATTACH while a write transaction on weave.lbug is in progress.

## Cypher ATTACH pattern

```cypher
ATTACH '~/openclaw/db/{skill-name}/{skill-name}.lbug' AS {alias} (dbtype lbug)
-- run read-only queries --
DETACH {alias};
```

List attached databases:
```cypher
CALL SHOW_ATTACHED_DATABASES() RETURN *;
```

## Python direct open (preferred for scripts)

Two Database objects pointing to different files never conflict — the lock is per-file.

```python
import real_ladybug as lb
from pathlib import Path

OCAS_BASE = Path("~/openclaw").expanduser()

def query_external_db(skill_name: str, cypher: str, params: dict = None):
    """Open an external lbug READ_ONLY and execute a query. Releases lock immediately."""
    db_path = OCAS_BASE / f"db/{skill_name}/{skill_name.split('-', 1)[-1]}.lbug"
    db = lb.Database(str(db_path), read_only=True)
    conn = lb.Connection(db)
    rows = list(conn.execute(cypher, params or {}))
    del conn, db
    return rows
```

## Known OCAS skill databases

ocas-elephas -- `~/openclaw/db/ocas-elephas/chronicle.lbug` -- entity knowledge graph, maintained by Elephas
ocas-triage -- `~/openclaw/db/ocas-triage/triage.lbug` -- task graph and priority queues
ocas-scout -- `~/openclaw/db/ocas-scout/scout.lbug` -- OSINT research findings

If a skill's path is unknown, check its SKILL.md storage layout section.

## Chronicle enrichment example

Chronicle may store a `weave:person_id` identifier on Entity nodes for people that exist in both systems. To find Chronicle context for a Weave person:

```python
rows = query_external_db(
    "ocas-elephas",
    """
    MATCH (e:Entity)
    WHERE e.type = 'Person' AND lower(e.name) CONTAINS lower($name)
    RETURN e.id, e.name, e.identifiers
    LIMIT 5
    """,
    {"name": person_name}
)
```

Weave reads this for enrichment only. Weave does not write to Chronicle and has no dependency on Chronicle being available.

## What not to do

Never open another skill's database as READ_WRITE.
Never run COPY FROM sourced from an attached database — export to staging CSV first, then import.
Never ATTACH while an uncommitted write transaction is active on weave.lbug.
