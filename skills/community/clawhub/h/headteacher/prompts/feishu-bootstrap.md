# Feishu Bootstrap

Use this prompt when the selected backend is `feishu_base`.

## Prerequisites

Run:

```bash
python3 tools/setup_doctor.py --backend feishu_base --format markdown
```

Read the reported `agent runtime` and `Feishu access mode` first.

### If access mode is `openclaw_plugin`

- verify whether the official OpenClaw Lark/Feishu plugin `openclaw-lark` is installed
- if missing, guide the user to install that plugin first
- once installed, create the workspace through the plugin's Feishu Base API tools
- use API-level operations to create:
  - the base
  - tables
  - fields
  - relation fields
  - views
- do not require `lark-cli` in this branch

### If access mode is `lark_cli`

If `lark-cli` is missing, guide installation first.

If `lark-cli` is not configured, guide:

```bash
lark-cli config init --new
```

## Bootstrap path

### New workspace

If access mode is `lark_cli`, use:

```bash
python3 tools/feishu_bootstrap.py bootstrap --workspace-name "<class-name>" --format markdown
```

If access mode is `openclaw_plugin`, use the official OpenClaw Feishu plugin's Base APIs to perform the same schema bootstrap based on this repository's schema definition.

### Existing Base provided by user

If access mode is `lark_cli`, inspect first:

```bash
python3 tools/migration_inspector.py feishu --base-token "<base-token>" --format markdown
```

If access mode is `openclaw_plugin`, inspect the existing Base through the plugin's Base APIs first, then classify it before deciding whether to connect or migrate.

Then decide:

- connect existing headteacher base
- or copy-and-refactor a subject-teacher base

## Rules

- do not overwrite an existing Base by default
- classify first, migrate second
- write the local workspace manifest after bootstrap succeeds
- keep the user informed of created tables, views, and local manifest path
- when running in OpenClaw, prefer the official plugin's Feishu Base tools over local shell-based Feishu tooling
