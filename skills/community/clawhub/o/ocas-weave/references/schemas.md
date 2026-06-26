# Schemas

LadybugDB DDL for `weave.lbug`. The database auto-initializes on first command via `_ensure_init()`. Run `weave.init` only for diagnostics or repair.

Check existing tables before running DDL: `CALL show_tables() RETURN *`

## DDL

```cypher
CREATE NODE TABLE IF NOT EXISTS Person (
  id STRING PRIMARY KEY,
  name STRING,
  name_given STRING,
  name_family STRING,
  email STRING,
  phone STRING,
  location_city STRING,
  location_country STRING,
  occupation STRING,
  org STRING,
  notes STRING,
  google_resource_name STRING,
  clay_id STRING,
  source_type STRING,
  source_ref STRING,
  confidence DOUBLE,
  event_time STRING,
  record_time STRING,
  valid_from STRING,
  valid_until STRING
);

CREATE NODE TABLE IF NOT EXISTS Preference (
  id STRING PRIMARY KEY,
  category STRING,
  value STRING,
  valence STRING,
  confidence DOUBLE,
  source_type STRING,
  source_ref STRING,
  record_time STRING
);

CREATE NODE TABLE IF NOT EXISTS Fact (
  id STRING PRIMARY KEY,
  predicate STRING,
  value STRING,
  confidence DOUBLE,
  source_type STRING,
  source_ref STRING,
  record_time STRING
);

CREATE REL TABLE IF NOT EXISTS Knows (
  FROM Person TO Person,
  rel_type STRING,
  strength DOUBLE,
  since STRING,
  context STRING,
  source_ref STRING,
  confidence DOUBLE,
  record_time STRING
);

CREATE REL TABLE IF NOT EXISTS HasPreference (
  FROM Person TO Preference
);

CREATE REL TABLE IF NOT EXISTS HasFact (
  FROM Person TO Fact
);
```

Note: LadybugDB does not support `CREATE INDEX IF NOT EXISTS` syntax. Primary keys are indexed automatically. No secondary indexes are needed at Weave's expected scale (thousands of nodes).

## Python auto-init implementation

```python
import real_ladybug as lb
from pathlib import Path
import uuid, json
from datetime import datetime, timezone

OCAS_BASE = Path("~/openclaw").expanduser()
DB_PATH = OCAS_BASE / "db/ocas-weave/weave.lbug"
STAGING = OCAS_BASE / "db/ocas-weave/staging"
JOURNALS = OCAS_BASE / "journals/ocas-weave"
CONFIG_PATH = OCAS_BASE / "db/ocas-weave/config.json"

def _open_db(read_only=False):
    """Open connection. Auto-inits schema and directories on first use."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    JOURNALS.mkdir(parents=True, exist_ok=True)
    _ensure_config()
    db = lb.Database(str(DB_PATH), read_only=read_only)
    conn = lb.Connection(db)
    if not read_only:
        _ensure_init(conn)
    return db, conn

def _ensure_config():
    if not CONFIG_PATH.exists():
        now = datetime.now(timezone.utc).isoformat()
        config = {
            "skill_id": "ocas-weave",
            "skill_version": "2.0.0",
            "config_version": "1",
            "created_at": now,
            "updated_at": now,
            "writeback": {"google_contacts": False, "clay": False},
            "last_sync": {"google_contacts": None, "clay": None},
            "retention": {"days": 0}
        }
        CONFIG_PATH.write_text(json.dumps(config, indent=2))

def _ensure_init(conn):
    """Run DDL only if schema is missing. Idempotent."""
    tables = {row[0] for row in conn.execute("CALL show_tables() RETURN *")}
    if "Person" not in tables:
        _run_ddl(conn)

def _run_ddl(conn):
    statements = [
        """CREATE NODE TABLE Person (
            id STRING PRIMARY KEY, name STRING, name_given STRING,
            name_family STRING, email STRING, phone STRING,
            location_city STRING, location_country STRING,
            occupation STRING, org STRING, notes STRING,
            google_resource_name STRING, clay_id STRING,
            source_type STRING, source_ref STRING, confidence DOUBLE,
            event_time STRING, record_time STRING,
            valid_from STRING, valid_until STRING
        )""",
        """CREATE NODE TABLE Preference (
            id STRING PRIMARY KEY, category STRING, value STRING,
            valence STRING, confidence DOUBLE, source_type STRING,
            source_ref STRING, record_time STRING
        )""",
        """CREATE NODE TABLE Fact (
            id STRING PRIMARY KEY, predicate STRING, value STRING,
            confidence DOUBLE, source_type STRING, source_ref STRING,
            record_time STRING
        )""",
        """CREATE REL TABLE Knows (
            FROM Person TO Person,
            rel_type STRING, strength DOUBLE, since STRING,
            context STRING, source_ref STRING, confidence DOUBLE,
            record_time STRING
        )""",
        "CREATE REL TABLE HasPreference (FROM Person TO Preference)",
        "CREATE REL TABLE HasFact (FROM Person TO Fact)",
    ]
    for stmt in statements:
        conn.execute(stmt)
```

## CLI usage

```bash
# Open interactive shell
lbug ~/openclaw/db/ocas-weave/weave.lbug

# Check schema
lbug ~/openclaw/db/ocas-weave/weave.lbug -c ":schema"

# Non-interactive query
echo "MATCH (p:Person) RETURN count(p)" | lbug ~/openclaw/db/ocas-weave/weave.lbug

# Read-only shell (safe alongside running process)
lbug ~/openclaw/db/ocas-weave/weave.lbug --readonly

# Show tables
lbug ~/openclaw/db/ocas-weave/weave.lbug -c "CALL show_tables() RETURN *"

# Show warnings after COPY FROM
lbug ~/openclaw/db/ocas-weave/weave.lbug -c "CALL show_warnings() RETURN *"
```

Lock error means another process (CLI, another Python session) has the file open READ_WRITE. Check running processes, close them, retry.

## Person fields

id -- STRING, PRIMARY KEY. UUID. Merge key. Never merge on name alone.
name -- STRING, required. Canonical display name.
name_given / name_family -- STRING. First / last name.
email -- STRING. Primary email.
phone -- STRING. E.164 preferred.
location_city / location_country -- STRING. ISO 3166-1 alpha-2 for country.
occupation / org / notes -- STRING.
google_resource_name -- STRING. Google Contacts foreign key.
clay_id -- STRING. Clay foreign key.
source_type -- STRING, required. direct / inferred / imported / user-stated.
source_ref -- STRING, required. Provenance reference.
confidence -- DOUBLE, required. 0.0–1.0.
event_time -- STRING. ISO 8601. When the real-world observation occurred.
record_time -- STRING, required. ISO 8601. When Weave wrote this record.
valid_from / valid_until -- STRING. ISO 8601. Validity window. valid_until null = currently valid.

Single upsert pattern:
```cypher
MERGE (p:Person {id: $id})
SET p.name = $name,
    p.source_type = $source_type,
    p.source_ref = $source_ref,
    p.confidence = $confidence,
    p.record_time = $record_time
```

Read-back (required after every MERGE or CREATE):
```cypher
MATCH (p:Person {id: $id}) RETURN p.id, p.name
```

## Preference fields

id -- STRING, PRIMARY KEY. UUID per record.
category -- STRING. food / gift / travel / interest / constraint / other.
value -- STRING. Free text.
valence -- STRING. like / dislike / constraint.
confidence -- DOUBLE.
source_type / source_ref / record_time -- STRING, required.

Each preference is a distinct CREATE — never MERGE on value.

## Knows fields

rel_type -- STRING. Ontology standard: knows / friend_of / colleague_of / family_of / introduced_by / spouse_of / reports_to / acquaintance_of.
strength -- DOUBLE. 0.0–1.0.
since -- STRING. ISO 8601 date.
context -- STRING.
source_ref / record_time -- STRING, required.
confidence -- DOUBLE.

## CSV import column map

For `COPY Person FROM 'file.csv' (header=true)`. Column names must match field names exactly.

Required: id (generate UUID if absent), name, source_type (default: imported), source_ref (default: filename), confidence (default: 0.8), record_time (default: now)
Optional: name_given, name_family, email, phone, location_city, location_country, occupation, org, notes, google_resource_name, clay_id, event_time, valid_from, valid_until
