# Wiki Entry Skill

Wiki Entry merges compiled transit notes into domain wiki pages, updates source metadata, keeps the central index in sync, and verifies the result before the note is marked as graduated.

This is a workflow skill for OpenClaw operators who maintain a markdown knowledge base with topic pages, source notes, and an index. It is designed for high-trust local workspaces where the agent is allowed to read, write, move, and validate files inside a configured vault.

## Plain Markdown First

Obsidian is optional. Wiki Entry works on ordinary local markdown folders.

If you have compiled `.md` notes in a transit folder and topic `.md` pages in a domain wiki folder, this skill can merge the notes into the right wiki pages, update the index, and move completed source notes into a graduated folder.

At minimum, you need:

- A transit folder containing compiled `.md` notes.
- A domain wiki folder containing topic `.md` pages.
- A graduated folder for completed source notes.
- A central markdown index file such as `_INDEX.md`.
- A local OpenClaw runtime with basic shell tools.

Paths are fully configurable. For safety, normal precheck requires an explicit vault path from OpenClaw config, `OPENCLAW_VAULT`, or `--vault`; it will not treat the current working directory as an implicit vault.

If you want to start from an empty plain folder, run the explicit initializer first:

```bash
bash scripts/wiki_entry_precheck.sh --vault /path/to/your/vault --init
```

Normal workflow runs should use precheck without `--init`, so missing or misconfigured paths fail fast instead of creating a false vault in the wrong directory.

## Background

This skill was built after repeated wiki-entry runs exposed a familiar failure pattern: the agent could write useful wiki content, but metadata often drifted. Source tables missed rows, `sources_count` diverged from the index, links became one-way, and partially completed documents were hard to recover after interruption.

Wiki Entry turns that fragile process into a checkpointed workflow. The agent still performs the semantic merge, but deterministic scripts handle fragile operations: status transitions, section writes, metadata writeback, index updates, backlink synchronization, movement of graduated notes, and final audit.

The design follows four principles:

- Keep the skill self-contained and installable in OpenClaw.
- Use environment variables for local paths, so the same package can run in different vaults.
- Treat QMD as optional recall infrastructure, not a hard runtime dependency.
- Fail closed on metadata and audit errors instead of letting the agent explain them away.

## What It Does

- Scans transit notes for `waiting` and `graduating` states.
- Forces A/B/reject path decisions before writing wiki content.
- Optionally searches local history and contradiction notes when QMD is configured.
- Marks source notes as `graduating` before wiki edits begin.
- Writes wiki sections through deterministic scripts.
- Adds source and evolution rows idempotently.
- Recomputes `sources_count` from the actual source table.
- Updates the central index.
- Synchronizes related-topic backlinks.
- Moves fully graduated transit notes into the graduated directory.
- Runs a final audit for source-table, frontmatter, index, and wikilink consistency.

## Package Layout

```text
wiki-entry/
├── SKILL.md
├── references/
│   ├── error-playbook.md
│   ├── path-decision.md
│   ├── self-check-checklist.md
│   └── workflow.md
└── scripts/
    ├── _shared/index_update.sh
    ├── _shared/query_history.sh
    ├── wiki_entry_audit.sh
    ├── wiki_entry_content_write.sh
    ├── wiki_entry_meta_writeback.sh
    ├── wiki_entry_mv_graduated.sh
    ├── wiki_entry_precheck.sh
    ├── wiki_entry_status_update.sh
    ├── wiki_entry_step_checkpoint.sh
    ├── wiki_entry_task_logger.sh
    ├── wiki_entry_wiki_scan.sh
    └── wiki_entry_xref_sync.sh
```

## OpenClaw Configuration

The skill is self-contained. Configure paths with environment variables in your OpenClaw skill or agent settings:

```json
{
  "skills": {
    "entries": {
      "wiki-entry": {
        "enabled": true,
        "env": {
          "OPENCLAW_VAULT": "/path/to/your/vault",
          "WIKI_ENTRY_TRANSIT_DIR": "/path/to/your/vault/Knowledge/Transit",
          "WIKI_ENTRY_DOMAIN_DIR": "/path/to/your/vault/Knowledge/Domain",
          "WIKI_ENTRY_GRADUATED_DIR": "/path/to/your/vault/Knowledge/Graduated",
          "WIKI_ENTRY_INDEX_FILE": "/path/to/your/vault/Knowledge/_INDEX.md",
          "WIKI_ENTRY_STATE_DIR": "/path/to/your/vault/.openclaw/state"
        }
      }
    }
  }
}
```

## Optional: QMD Local Recall

Wiki Entry can run without QMD. When `WIKI_ENTRY_QMD_ENTRY` and `COMPILE_QMD_ENTRY` are not configured, the bundled `query_history.sh` outputs `RESULT: QMD_SKIPPED` and the workflow continues.

QMD is recommended when you want stronger local recall: prior entry decisions, topic evolution, contradiction checks, and knowledge-base continuity. To enable it, install QMD locally and set:

```json
{
  "skills": {
    "entries": {
      "wiki-entry": {
        "env": {
          "WIKI_ENTRY_QMD_ENTRY": "/path/to/qmd"
        }
      }
    }
  }
}
```

The QMD CLI should support `search`, `get`, `--files`, and `--collection`.

## Defaults

When `OPENCLAW_VAULT` is set, scripts use these default subpaths unless the specific environment variables override them:

- `Knowledge/中转站/`
- `Knowledge/领域/`
- `Knowledge/已入库/`
- `Knowledge/_INDEX.md`
- `.openclaw/state/`

When `OPENCLAW_VAULT` is not set, pass `--vault /path/to/your/vault` to runtime scripts. The skill intentionally does not infer the vault from the shell working directory.

## Safety Model

This skill is intentionally manual-invocation only. It modifies wiki pages, updates index metadata, changes source-note status, and may move files, so it should not be auto-triggered for generic editing or summarization.

The final audit must pass before the operator treats an entry run as complete. If an audit fails, the agent should stop, record a blocked checkpoint, fix the specific issue, and rerun the audit.

## Validation Status

- Bundle contains only text-based files.
- No API keys or credentials are required.
- Runtime dependencies are declared in `SKILL.md`.
- Path configuration is environment-driven.
- `scripts/_shared/query_history.sh` and `scripts/_shared/index_update.sh` are bundled to avoid undeclared external script dependencies.

## Author

Designed and developed by 强哥.
