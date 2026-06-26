---
name: project-memory-ledger
description: "Engineering project memory ledger with evidence + rollback (Invariants, Decision Log, Change Log). Use to extend conversations over time, reduce hallucinations, avoid memory pollution, and keep systems stable by recording project rules/decisions/changes with traceability. Supports local-only mode (Markdown) and optional Drive project-doc scaffolding via gws; defaults to project-memory-ledger when no Project is specified."
metadata:
  openclaw:
    requires:
      bins:
        - python3
    recommends:
      bins:
        - gws
---

# Project Memory Ledger

Maintain a durable, low-pollution ledger split into **three books**:
- **Invariants**: hard rules / stable facts
- **Decisions**: tradeoffs and rationale
- **Changes**: what changed + why + evidence + impact + rollback

Backends (configurable) — **simplified semantics**:
- The **ledger is always local Markdown**.
- `backend` only controls where the **project docs/assets** are scaffolded and stored.

Values:
- **local**: create project directory structure locally and store docs as Markdown
- **drive**: create Drive folder structure and store docs as GDoc/GSheet (requires gws auth)

## Key conventions (write these into entries)
### Project tagging (normalized, case-insensitive)
- Allowed `Project` slugs: `hunter-system` | `keyword-engine` | `common`
- `shared` is **disabled**. Cross-project relationships must be expressed via an explicit field:
  - `Interfaces: hunter-system ↔ keyword-engine`

### Default project
If `append` is called without `--project`, the script injects:
- `Project: project-memory-ledger` (configurable by `default_project`)

Use this for improvements/bugs/requirements **about this skill itself**.

## How to run
### 1) Configure (one-time)
Config path (recommended):
- `/root/.openclaw/workspace-nero/config/project_memory_ledger.json`

Minimal fields:
- `backend`: `local` | `drive`
- `default_project`: `project-memory-ledger`
- `local_dir`: `/root/.openclaw/workspace-nero/ledgers`

If `backend` is `drive` or `both`, also set:
- `shared_folder_id`: Drive folder id for `Shared/`

Template:
- `references/default_config.json`

### 2) Init (recommended)
Creates/links Drive docs (drive/both) and ensures local files exist:
```bash
python3 skills/project-memory-ledger/scripts/ledger.py init \
  --config /root/.openclaw/workspace-nero/config/project_memory_ledger.json
```

### 3) Append entries
```bash
python3 skills/project-memory-ledger/scripts/ledger.py append \
  --config /root/.openclaw/workspace-nero/config/project_memory_ledger.json \
  --doc changes \
  --project "Keyword Engine" \
  --text "- **Interfaces**: hunter-system ↔ keyword-engine\n- **Change**: ...\n- **Why**: ...\n- **Evidence**: ...\n- **Rollback**: ...\n"
```

Local mode writes:
- `ledgers/INVARIANTS.md`
- `ledgers/DECISIONS.md`
- `ledgers/CHANGES.md`
- `ledgers/PROJECTS.md` (when registering projects)

### 4) Register a project (project registry)
Use when something is worth upgrading into a maintained engineering project (creates a registry entry and records the decision). In drive/both, it also scaffolds a standard Drive folder structure by default:
```bash
python3 skills/project-memory-ledger/scripts/ledger.py register-project \
  --config /root/.openclaw/workspace-nero/config/project_memory_ledger.json \
  --name "My New Project" \
  --purpose "Why it exists + success criteria" \
  --interfaces "hunter-system ↔ keyword-engine" \
  --notes "optional"
```

### 5) Update PRD (propose-only)
Generate a PRD patch proposal (no auto-apply in v1):
```bash
python3 skills/project-memory-ledger/scripts/ledger.py update-prd \
  --config /root/.openclaw/workspace-nero/config/project_memory_ledger.json \
  --project "Keyword Engine" \
  --mode propose
```
This writes to local `ledgers/PRD_PATCHES.md` (local/both) and prints the proposal.

## Drive access note (optional)
Drive mode is a **pluggable backend** and is optional.

### Drive backend options (not hard-bound)
- **Option 1 (v1 implemented)**: `gws` CLI (must be installed + authenticated)
- **Option 2**: Google API / service account (good for servers / CI)
- **Option 3**: Third-party Drive tooling (user-chosen)

### Recommended practice
If you don’t need humans editing the ledger, prefer **local**. If humans want to participate, keep the ledger local and have the agent generate Drive summaries (propose-only style).

## What to record (assistant-owned scope)
- Drive structure changes (create/move/permissions)
- systemd service/timer changes
- SQLite schema/dedup logic changes (with before/after stats)
- auth/publishing reliability fixes
- output contract changes (doc/sheet rules)

Use templates:
- `references/ledger_templates.md`
