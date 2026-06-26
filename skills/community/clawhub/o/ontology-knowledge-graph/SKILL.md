---
name: ontology
description: Typed knowledge graph for structured agent memory and composable skills. Create/query/link entities (Person, Project, Task, Event, Document), enforce constraints, auto-sync from memory files, and use as backup memory fallback. Trigger on "remember", "what do I know about", "link X to Y", "show dependencies", entity CRUD, or cross-skill data access.
---

# Ontology 知识图谱

A typed vocabulary + constraint system for representing knowledge as a verifiable graph. Supports entity CRUD, schema validation, automatic sync from memory files, and serves as a backup memory fallback.

## Core Concept

Everything is an **entity** with a **type**, **properties**, and **relations** to other entities. Every mutation is validated against type constraints before committing.

```
Entity: { id, type, properties, relations, created, updated }
Relation: { from_id, relation_type, to_id, properties }
```

## When to Use

| Trigger | Action |
|---------|--------|
| "Remember that..." | Create/update entity |
| "What do I know about X?" | Query graph |
| "Link X to Y" | Create relation |
| "Show all tasks for project Z" | Graph traversal |
| "What depends on X?" | Dependency query |
| Planning multi-step work | Model as graph transformations |
| Skill needs shared state | Read/write ontology objects |
| Main memory extraction fails | **Backup memory fallback** |

## Core Types

```yaml
# Agents & People
Person: { name, email?, phone?, notes?, organization? }
Organization: { name, type?, members[] }

# Work
Project: { name, status, goals[], owner? }
Task: { title, status, due?, priority?, assignee?, blockers[] }
Goal: { description, target_date?, metrics[] }

# Time & Place
Event: { title, start, end?, location?, attendees[], recurrence? }
Location: { name, address?, coordinates? }

# Information
Document: { title, path?, url?, summary? }
Message: { content, sender, recipients[], thread? }
Thread: { subject, participants[], messages[] }
Note: { content, tags[], refs[] }

# Resources
Account: { service, username, credential_ref? }
Device: { name, type, identifiers[] }
Credential: { service, secret_ref }  # Never store secrets directly

# Meta
Action: { type, target, timestamp, outcome? }
Policy: { scope, rule, enforcement }

# Extended types (v2.0+)
Technology: { name, domain?, source? }
Skill: { name, source?, version? }
```

## Storage

Default: `memory/ontology/graph.jsonl`

```jsonl
{"op":"create","entity":{"id":"p_001","type":"Person","properties":{"name":"Alice"}}}
{"op":"create","entity":{"id":"proj_001","type":"Project","properties":{"name":"Website Redesign","status":"active"}}}
{"op":"relate","from":"proj_001","rel":"has_owner","to":"p_001"}
```

Query via scripts or direct file ops. For complex graphs, migrate to SQLite.

### Append-Only Rule

When working with existing ontology data or schema, **append/merge** changes instead of overwriting files. This preserves history and avoids clobbering prior definitions.

## Workflows

### Create Entity

```bash
python scripts/ontology.py create --type Person --props '{"name":"Alice","email":"alice@example.com"}'
```

### Query

```bash
python scripts/ontology.py query --type Task --where '{"status":"open"}'
python scripts/ontology.py get --id task_001
python scripts/ontology.py related --id proj_001 --rel has_task
python scripts/ontology.py list --type Person
```

### Link Entities

```bash
python scripts/ontology.py relate --from proj_001 --rel has_task --to task_001
```

### Validate

```bash
python scripts/ontology.py validate  # Check all constraints
```

### Auto-Sync from Memory Files (v2.0+)

```bash
# Sync entities from daily notes (last 7 days)
python scripts/ontology_sync.py

# Sync last N days
python scripts/ontology_sync.py --days 3

# Dry run (preview only)
python scripts/ontology_sync.py --dry-run

# Check graph status
python scripts/ontology_sync.py --status
```

## Backup Memory Fallback (v2.0+)

When the primary memory system fails to extract accurate results, Ontology serves as a backup memory layer:

**Fallback hierarchy:**
1. `tdai_memory_search` (primary memory)
2. `openclaw-mem0` (auxiliary memory)
3. **Ontology graph** (structured entities + relations)

**Trigger conditions:** Primary memory returns empty results / inaccurate data / user says "results are wrong"

**Query examples:**
```bash
# List all projects
python scripts/ontology.py list --type Project

# Query by type and property
python scripts/ontology.py query --type Organization --where '{"type":"supplier"}'

# Get related entities for a person
python scripts/ontology.py related --id pers_xxx --dir both
```

## Constraints

Define in `memory/ontology/schema.yaml`:

```yaml
types:
  Task:
    required: [title, status]
    status_enum: [open, in_progress, blocked, done]
  
  Event:
    required: [title, start]
    validate: "end >= start if end exists"

  Credential:
    required: [service, secret_ref]
    forbidden_properties: [password, secret, token]  # Force indirection

relations:
  has_owner:
    from_types: [Project, Task]
    to_types: [Person]
    cardinality: many_to_one
  
  blocks:
    from_types: [Task]
    to_types: [Task]
    acyclic: true  # No circular dependencies
```

## Skill Contract

Skills that use ontology should declare:

```yaml
# In SKILL.md frontmatter or header
ontology:
  reads: [Task, Project, Person]
  writes: [Task, Action]
  preconditions:
    - "Task.assignee must exist"
  postconditions:
    - "Created Task has status=open"
```

## Planning as Graph Transformation

Model multi-step plans as a sequence of graph operations:

```
Plan: "Schedule team meeting and create follow-up tasks"

1. CREATE Event { title: "Team Sync", attendees: [p_001, p_002] }
2. RELATE Event -> has_project -> proj_001
3. CREATE Task { title: "Prepare agenda", assignee: p_001 }
4. RELATE Task -> for_event -> event_001
5. CREATE Task { title: "Send summary", assignee: p_001, blockers: [task_001] }
```

Each step is validated before execution. Rollback on constraint violation.

## Integration Patterns

### With Causal Inference

Log ontology mutations as causal actions:

```python
# When creating/updating entities, also log to causal action log
action = {
    "action": "create_entity",
    "domain": "ontology", 
    "context": {"type": "Task", "project": "proj_001"},
    "outcome": "created"
}
```

### Cross-Skill Communication

```python
# Email skill creates commitment
commitment = ontology.create("Commitment", {
    "source_message": msg_id,
    "description": "Send report by Friday",
    "due": "2026-01-31"
})

# Task skill picks it up
tasks = ontology.query("Commitment", {"status": "pending"})
for c in tasks:
    ontology.create("Task", {
        "title": c.description,
        "due": c.due,
        "source": c.id
    })
```

## Cron Auto-Sync Setup

Recommended: Configure an OpenClaw Cron job for daily auto-sync:

```json
{
  "name": "Ontology Daily Sync",
  "schedule": { "kind": "cron", "expr": "0 22 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run ontology sync: python scripts/ontology_sync.py --days 7"
  },
  "sessionTarget": "isolated"
}
```

## Quick Start

```bash
# Initialize ontology storage
mkdir -p memory/ontology
touch memory/ontology/graph.jsonl

# Create schema (optional but recommended)
python scripts/ontology.py schema-append --data '{
  "types": {
    "Task": { "required": ["title", "status"] },
    "Project": { "required": ["name"] },
    "Person": { "required": ["name"] }
  }
}'

# Start using
python scripts/ontology.py create --type Person --props '{"name":"Alice"}'
python scripts/ontology.py list --type Person

# Auto-sync from existing memory files
python scripts/ontology_sync.py --days 30
```

## References

- `references/schema.md` — Full type definitions and constraint patterns
- `references/queries.md` — Query language and traversal examples

## File Structure

```
ontology/
├── SKILL.md              # This file
├── scripts/
│   ├── ontology.py       # Core CLI (create/query/relate/validate)
│   └── ontology_sync.py  # Auto-sync from memory files (v2.0+)
└── references/
    ├── schema.md         # Schema reference
    └── queries.md        # Query patterns
```

## Instruction Scope

Runtime instructions operate on local files (`memory/ontology/graph.jsonl` and `memory/ontology/schema.yaml`) and provide CLI usage for create/query/relate/validate; this is within scope. The skill reads/writes workspace files and will create the `memory/ontology` directory when used. Validation includes property/enum/forbidden checks, relation type/cardinality validation, acyclicity for relations marked `acyclic: true`, and Event `end >= start` checks; other higher-level constraints may still be documentation-only unless implemented in code.
