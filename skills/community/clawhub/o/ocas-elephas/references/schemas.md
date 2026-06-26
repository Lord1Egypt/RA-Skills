# Chronicle Schemas

LadybugDB DDL for `chronicle.lbug`. The database auto-initializes on first command via `_ensure_init()`. Run `elephas.init` only for diagnostics or repair.

Check existing tables before running DDL: `CALL show_tables() RETURN *`

## DDL

```cypher
CREATE NODE TABLE Entity (
  id STRING PRIMARY KEY,
  name STRING,
  entity_type STRING,
  aliases STRING,
  identifiers STRING,
  possible_matches STRING,
  merge_history STRING,
  identity_state STRING,
  source_skill STRING,
  record_time STRING
);

CREATE NODE TABLE Place (
  id STRING PRIMARY KEY,
  name STRING,
  place_type STRING,
  coordinates STRING,
  address STRING,
  source_skill STRING,
  record_time STRING
);

CREATE NODE TABLE Concept (
  id STRING PRIMARY KEY,
  name STRING,
  description STRING,
  concept_type STRING,
  event_time STRING,
  source_skill STRING,
  record_time STRING
);

CREATE NODE TABLE Thing (
  id STRING PRIMARY KEY,
  name STRING,
  thing_type STRING,
  metadata STRING,
  source_skill STRING,
  record_time STRING
);

CREATE NODE TABLE Signal (
  id STRING PRIMARY KEY,
  source_skill STRING,
  source_journal_type STRING,
  payload STRING,
  timestamp STRING,
  status STRING
);

CREATE NODE TABLE Candidate (
  id STRING PRIMARY KEY,
  proposed_type STRING,
  proposed_data STRING,
  supporting_signals STRING,
  confidence STRING,
  status STRING,
  created_at STRING,
  resolved_at STRING,
  resolved_reason STRING
);

CREATE NODE TABLE Inference (
  id STRING PRIMARY KEY,
  inference_type STRING,
  confidence STRING,
  supporting_nodes STRING,
  description STRING,
  created_at STRING
);

CREATE REL TABLE Relates (
  FROM Entity TO Entity,
  FROM Entity TO Concept,
  FROM Entity TO Place,
  FROM Entity TO Thing,
  FROM Concept TO Place,
  FROM Concept TO Concept,
  relationship_type STRING,
  evidence_refs STRING,
  confidence STRING,
  event_time STRING,
  record_time STRING,
  valid_from STRING,
  valid_until STRING
);

CREATE REL TABLE Supports (
  FROM Signal TO Candidate
);

CREATE REL TABLE Promotes (
  FROM Candidate TO Entity,
  FROM Candidate TO Place,
  FROM Candidate TO Concept,
  FROM Candidate TO Thing
);

CREATE REL TABLE Infers (
  FROM Inference TO Entity,
  FROM Inference TO Concept,
  FROM Inference TO Place
);
```

Note: LadybugDB indexes primary keys automatically. No secondary index DDL is needed for Chronicle's expected scale (100k–500k nodes).

## Python auto-init implementation

```python
import real_ladybug as lb
from pathlib import Path
import json, uuid
from datetime import datetime, timezone

OCAS_BASE = Path("~/openclaw").expanduser()
DB_PATH = OCAS_BASE / "db/ocas-elephas/chronicle.lbug"
INTAKE = OCAS_BASE / "db/ocas-elephas/intake"
STAGING = OCAS_BASE / "db/ocas-elephas/staging"
JOURNALS = OCAS_BASE / "journals/ocas-elephas"
CONFIG_PATH = OCAS_BASE / "db/ocas-elephas/config.json"

def _open_db(read_only=False):
    """Open connection. Auto-inits schema and directories on first use."""
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

def _ensure_config():
    if not CONFIG_PATH.exists():
        now = datetime.now(timezone.utc).isoformat()
        config = {
            "skill_id": "ocas-elephas",
            "skill_version": "2.0.0",
            "config_version": "1",
            "created_at": now,
            "updated_at": now,
            "consolidation": {
                "immediate_interval_minutes": 15,
                "deep_interval_hours": 24
            },
            "identity": {
                "auto_merge_threshold": 0.90,
                "flag_review_threshold": 0.70
            },
            "inference": {
                "enabled": True,
                "min_supporting_nodes": 3
            },
            "retention": {"days": 0}
        }
        CONFIG_PATH.write_text(json.dumps(config, indent=2))

def _ensure_init(conn):
    """Run DDL only if schema is missing. Idempotent."""
    tables = {row[0] for row in conn.execute("CALL show_tables() RETURN *")}
    if "Entity" not in tables:
        _run_ddl(conn)

def _run_ddl(conn):
    statements = [
        """CREATE NODE TABLE Entity (
            id STRING PRIMARY KEY, name STRING, entity_type STRING,
            aliases STRING, identifiers STRING, possible_matches STRING,
            merge_history STRING, identity_state STRING,
            source_skill STRING, record_time STRING
        )""",
        """CREATE NODE TABLE Place (
            id STRING PRIMARY KEY, name STRING, place_type STRING,
            coordinates STRING, address STRING,
            source_skill STRING, record_time STRING
        )""",
        """CREATE NODE TABLE Concept (
            id STRING PRIMARY KEY, name STRING, description STRING,
            concept_type STRING, event_time STRING,
            source_skill STRING, record_time STRING
        )""",
        """CREATE NODE TABLE Thing (
            id STRING PRIMARY KEY, name STRING, thing_type STRING,
            metadata STRING, source_skill STRING, record_time STRING
        )""",
        """CREATE NODE TABLE Signal (
            id STRING PRIMARY KEY, source_skill STRING,
            source_journal_type STRING, payload STRING,
            timestamp STRING, status STRING
        )""",
        """CREATE NODE TABLE Candidate (
            id STRING PRIMARY KEY, proposed_type STRING, proposed_data STRING,
            supporting_signals STRING, confidence STRING, status STRING,
            created_at STRING, resolved_at STRING, resolved_reason STRING
        )""",
        """CREATE NODE TABLE Inference (
            id STRING PRIMARY KEY, inference_type STRING, confidence STRING,
            supporting_nodes STRING, description STRING, created_at STRING
        )""",
        """CREATE REL TABLE Relates (
            FROM Entity TO Entity,
            FROM Entity TO Concept,
            FROM Entity TO Place,
            FROM Entity TO Thing,
            FROM Concept TO Place,
            FROM Concept TO Concept,
            relationship_type STRING, evidence_refs STRING, confidence STRING,
            event_time STRING, record_time STRING,
            valid_from STRING, valid_until STRING
        )""",
        "CREATE REL TABLE Supports (FROM Signal TO Candidate)",
        """CREATE REL TABLE Promotes (
            FROM Candidate TO Entity,
            FROM Candidate TO Place,
            FROM Candidate TO Concept,
            FROM Candidate TO Thing
        )""",
        """CREATE REL TABLE Infers (
            FROM Inference TO Entity,
            FROM Inference TO Concept,
            FROM Inference TO Place
        )""",
    ]
    for stmt in statements:
        conn.execute(stmt)
```

## CLI usage

```bash
# Open interactive shell
lbug ~/openclaw/db/ocas-elephas/chronicle.lbug

# Check schema
lbug ~/openclaw/db/ocas-elephas/chronicle.lbug -c ":schema"

# Non-interactive query
echo "MATCH (e:Entity) RETURN count(e)" | lbug ~/openclaw/db/ocas-elephas/chronicle.lbug

# Read-only shell (safe alongside running process)
lbug ~/openclaw/db/ocas-elephas/chronicle.lbug --readonly

# Show all tables
lbug ~/openclaw/db/ocas-elephas/chronicle.lbug -c "CALL show_tables() RETURN *"

# Check pending candidates
lbug ~/openclaw/db/ocas-elephas/chronicle.lbug -c \
  "MATCH (c:Candidate {status: 'pending'}) RETURN c.id, c.proposed_type, c.confidence ORDER BY c.created_at ASC LIMIT 20"

# Show warnings after COPY FROM
lbug ~/openclaw/db/ocas-elephas/chronicle.lbug -c "CALL show_warnings() RETURN *"
```

Lock error means another process has the file open READ_WRITE. Only Elephas should hold READ_WRITE. Other skills open as READ_ONLY. If locked unexpectedly, identify the offending process, close it, retry.

## Common query patterns

All confirmed Person entities:
```cypher
MATCH (e:Entity {entity_type: 'Person', identity_state: 'distinct'})
RETURN e.id, e.name, e.identifiers
ORDER BY e.name
```

Pending candidates by confidence:
```cypher
MATCH (c:Candidate {status: 'pending'})
RETURN c.id, c.proposed_type, c.confidence, c.created_at
ORDER BY c.confidence DESC, c.created_at ASC
```

All relationships for an entity:
```cypher
MATCH (e:Entity {id: $entity_id})-[r:Relates]->(other)
RETURN r.relationship_type, other.name, r.confidence, r.event_time
```

Entities flagged for identity review:
```cypher
MATCH (e:Entity {identity_state: 'possible_match'})
RETURN e.id, e.name, e.possible_matches, e.identifiers
```

Find Chronicle Entity by skill-namespaced identifier (Weave cross-reference):
```cypher
MATCH (e:Entity)
WHERE e.identifiers CONTAINS $weave_person_id
RETURN e.id, e.name, e.entity_type
LIMIT 5
```

Active signals from a specific skill:
```cypher
MATCH (s:Signal {source_skill: $skill_name, status: 'active'})
RETURN s.id, s.source_journal_type, s.timestamp
ORDER BY s.timestamp ASC
```

## Field notes

Entity.aliases -- JSON array string: `["alias1", "alias2"]`
Entity.identifiers -- JSON array string: `[{"type": "email", "value": "..."}]`
  Allowed types: email, phone, handle, url, domain, employee_id, external_id
  Skill-namespaced: `{"type": "weave:person_id", "value": "uuid"}`
Entity.possible_matches -- JSON array string of Entity ids
Entity.merge_history -- JSON array string: `[{"merged_id":"...","merged_at":"...","merged_by":"ocas-elephas","reason":"..."}]`
Entity.identity_state -- distinct (default) / possible_match / confirmed_same

Concept.concept_type -- Event / Action / Idea
  Event subtypes (use as name prefix): TravelEvent, MeetingEvent, PurchaseEvent, AppointmentEvent, CommunicationEvent

Signal.status -- active (awaiting processing) / consumed (ingested)
Signal.source_journal_type -- Observation / Action / Research

Candidate.confidence -- high / med / low
Candidate.status -- pending / confirmed / rejected / merged

Relates.relationship_type -- use ontology standard types:
  Entity-Entity: knows, friend_of, colleague_of, family_of, introduced_by, spouse_of, reports_to, acquaintance_of
  Entity-Concept: participated_in, organized, attended
  Entity-Place: lives_in, works_at, visited, associated_with
  Entity-Thing: created, owns, uses
  Concept-Place: occurred_at, located_in
  Concept-Concept: related_to, derived_from, part_of
