# Compile Skill

Compile turns raw markdown notes from an inbox into structured knowledge-transfer documents, then archives the original material with reversible links and checkpointed audit state.

This is a workflow skill for OpenClaw operators who maintain a markdown knowledge base. It is designed for high-trust local workspaces where the agent is allowed to read, write, move, and validate files inside a configured vault.

## Plain Markdown First

Obsidian is optional. Compile works on ordinary local markdown folders.

Put raw `.md` articles into an inbox folder, point OpenClaw to that folder with `COMPILE_INBOX_DIR`, and the skill can generate compiled markdown notes into `COMPILE_TRANSIT_DIR` while archiving the originals into `COMPILE_RAW_DIR`.

At minimum, you need:

- An inbox folder containing raw `.md` files.
- A transit folder for compiled notes.
- A raw-material folder for archived originals.
- A local OpenClaw runtime with basic shell tools.

`COMPILE_INBOX_DIR` must point to an existing inbox. Normal precheck fails fast when the inbox is missing or not configured, so a misconfigured install does not silently create or scan the wrong folder.

`COMPILE_TRANSIT_DIR`, `COMPILE_RAW_DIR`, and `COMPILE_STATE_DIR` may be initialized by the workflow after the inbox has been explicitly configured.

## Background

This skill was built after repeated knowledge-ingestion runs exposed the same failure pattern: an agent could summarize a raw note, but the result was hard to audit, hard to trace back to source material, and easy to drift from the knowledge-base schema.

Compile turns that fragile ad hoc process into a controlled workflow. The central idea is simple: let the agent do the semantic work, but put deterministic scripts around every fragile operation: duplicate detection, frontmatter generation, checkpointing, archiving, backlink repair, and final validation.

The design follows four principles:

- Keep the skill self-contained and installable in OpenClaw.
- Use environment variables for all local paths, so the same package can run in different vaults.
- Treat QMD as optional recall infrastructure, not a hard runtime dependency.
- Fail closed on structure and audit errors instead of letting the agent explain them away.

## What It Does

- Scans an inbox for unprocessed markdown notes.
- Normalizes clipped frontmatter and unsafe filenames.
- Checks duplicates by normalized title and source URL.
- Searches local history when QMD is available.
- Generates standards-compliant compiled frontmatter.
- Guides the agent through a structured compiled note template.
- Archives raw material and assets into a raw-material directory.
- Writes checkpoint state for every workflow step.
- Runs a deterministic final audit before completion.

## Package Layout

```text
compile/
├── SKILL.md
├── references/
│   ├── compile-template.md
│   ├── error-playbook.md
│   ├── frontmatter-spec.md
│   ├── self-check-checklist.md
│   ├── title-rules.md
│   └── workflow.md
└── scripts/
    ├── _shared/query_history.sh
    ├── compile_archive.sh
    ├── compile_check.sh
    ├── compile_clipper_fix.sh
    ├── compile_duplicate_check.sh
    ├── compile_filename_check.sh
    ├── compile_frontmatter_gen.sh
    ├── compile_precheck.sh
    ├── compile_step_checkpoint.sh
    └── compile_task_logger.sh
```

## OpenClaw Configuration

The skill is self-contained. Configure paths with environment variables in your OpenClaw skill or agent settings:

```json
{
  "skills": {
    "entries": {
      "compile": {
        "enabled": true,
        "env": {
          "OPENCLAW_VAULT": "/path/to/your/vault",
          "COMPILE_INBOX_DIR": "/path/to/your/vault/Inbox",
          "COMPILE_TRANSIT_DIR": "/path/to/your/vault/Knowledge/Transit",
          "COMPILE_RAW_DIR": "/path/to/your/vault/Knowledge/Raw",
          "COMPILE_STATE_DIR": "/path/to/your/vault/.openclaw/state"
        }
      }
    }
  }
}
```

## Optional: QMD Local Recall

Compile can run without QMD. When `COMPILE_QMD_ENTRY` is not configured, `query_history.sh` outputs `RESULT: QMD_SKIPPED` and the workflow continues.

QMD is recommended when you want stronger local recall: duplicate awareness, topic reuse, prior conclusion lookup, and knowledge-base continuity. To enable it, install QMD locally and set:

```json
{
  "skills": {
    "entries": {
      "compile": {
        "env": {
          "COMPILE_QMD_ENTRY": "/path/to/qmd"
        }
      }
    }
  }
}
```

The QMD CLI should support `search`, `get`, `--files`, and `--collection`.

## Defaults

`OPENCLAW_VAULT` is optional, but `COMPILE_INBOX_DIR` must be configured explicitly. When `COMPILE_TRANSIT_DIR`, `COMPILE_RAW_DIR`, or `COMPILE_STATE_DIR` are not set, scripts derive them from `OPENCLAW_VAULT`:

- `Knowledge/中转站/`
- `Knowledge/原材料仓库/`
- `.openclaw/state/`

## Safety Model

This skill is intentionally manual-invocation only. It moves source files and writes compiled documents, so it should not be auto-triggered for generic summarization or wiki-entry tasks.

The final audit must pass before the operator treats a compile run as complete. If an audit fails, the agent should stop, record a blocked checkpoint, fix the specific issue, and rerun the audit.

## Validation Status

- Bundle contains only text-based files.
- No API keys or credentials are required.
- Runtime dependencies are declared in `SKILL.md`.
- Path configuration is environment-driven.
- `scripts/_shared/query_history.sh` is bundled to avoid undeclared external script dependencies.

## Author

Designed and developed by 强哥.
