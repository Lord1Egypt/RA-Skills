# Project Memory Ledger (OpenClaw Skill)

AI-ready engineering project ledger for long-term memory + evidence chains (**Invariants / Decisions / Changes**) with traceability and rollback.

**Keywords:** project ledger, engineering ledger, change log, decision log, invariants, traceability, rollback, evidence chain, agent memory, long-term memory, LLM ops, OpenClaw, Google Drive, Markdown

## What it does

### 1) Local-first ledger (always local Markdown)
The ledger is always written to local Markdown files:
- `<workspace>/ledgers/INVARIANTS.md`
- `<workspace>/ledgers/DECISIONS.md`
- `<workspace>/ledgers/CHANGES.md`
- `<workspace>/ledgers/PROJECTS.md`
- `<workspace>/ledgers/PRD_PATCHES.md`

### 2) Project scaffolding (docs location controlled by backend)
`backend` decides where **project docs/assets** live:
- `backend=local`: create local project folders + Markdown docs
- `backend=drive`: create Drive project folders + GDoc/GSheet docs (requires `gws` authenticated)

> This skill does **not** dual-write docs by design (avoids inconsistency). The ledger remains local.

---

## Quick start

### 0) Choose a workspace
“workspace” means your OpenClaw working directory (not necessarily `workspace-nero`).

### 1) Create config
Recommended path:
- `<workspace>/config/project_memory_ledger.json`

Minimal config (local docs):
```json
{
  "language": "en",
  "backend": "local",
  "default_project": "project-memory-ledger",
  "local_dir": "./ledgers",
  "projects_root_dir": "./projects",
  "projects_root_folder_id": ""
}
```

Drive docs config:
```json
{
  "language": "en",
  "backend": "drive",
  "default_project": "project-memory-ledger",
  "local_dir": "./ledgers",
  "projects_root_dir": "./projects",
  "projects_root_folder_id": "<Drive folder id where projects should be created>"
}
```

Template:
- `references/default_config.json`

### 2) Init
```bash
python3 skills/project-memory-ledger/scripts/ledger.py init --config <workspace>/config/project_memory_ledger.json
```

### 3) Append entries
```bash
python3 skills/project-memory-ledger/scripts/ledger.py append \
  --config <workspace>/config/project_memory_ledger.json \
  --doc changes \
  --project "Keyword Engine" \
  --text "- **Interfaces**: hunter-system ↔ keyword-engine\n- **Change**: ...\n- **Why**: ...\n- **Evidence**: ...\n- **Rollback**: ...\n"
```

### 4) Register a project (scaffold)
```bash
python3 skills/project-memory-ledger/scripts/ledger.py register-project \
  --config <workspace>/config/project_memory_ledger.json \
  --name "My New Project" \
  --purpose "Why it exists + success criteria" \
  --interfaces "hunter-system ↔ keyword-engine" \
  --notes "optional"
```

- `backend=local` → creates `<workspace>/projects/My New Project/...` and Markdown docs
- `backend=drive` → creates Drive folders + GDoc/GSheet docs

### 5) Update PRD (propose-only)
```bash
python3 skills/project-memory-ledger/scripts/ledger.py update-prd \
  --config <workspace>/config/project_memory_ledger.json \
  --project "Keyword Engine" \
  --mode propose
```

---

## Conventions

### Project tagging
Project values are case-insensitive and normalized to slugs.

Recommended slugs:
- `hunter-system`
- `keyword-engine`
- `common` (cross-project rules/methods; not global AGENTS/MEMORY)

`shared` is disabled. Cross-project coupling must be explicit:
- `Interfaces: a ↔ b`

### Default project
If you omit `--project`, the script injects:
- `Project: project-memory-ledger`

---

## Drive backend options
Drive mode is optional and pluggable:
- Option 1 (v1 implemented): `gws` CLI (installed + authenticated)
- Option 2: Google API / service account
- Option 3: third-party Drive tooling

If Drive isn’t available, use `backend=local`.
