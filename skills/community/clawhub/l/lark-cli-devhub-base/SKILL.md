---
name: lark-cli-devhub-base
description: Use when designing, provisioning, searching, or writing Feishu/Lark Base records through lark-cli or feishu-cli for a development knowledge hub, including Projects, Areas, Tasks, Bugfixes, Pitfalls, Playbooks, Decisions, Releases, Artifacts, and AI Runs.
metadata:
  requires:
    bins: ["lark-cli", "python3"]
---

# Lark CLI Dev Hub Base

Base is the AI-readable database for Dev Hub. Prefer Base for facts, state, relationships, and search keywords.

Discovery aliases: `feishu-cli base`, `飞书多维表格`, `lark-cli base`, `Lark Base`, `Feishu Base`, `Bitable`.

## Schema

The default schema lives at:

```text
$HOME/.codex/devhub/templates/base-schema.json
```

Provision:

```bash
python3 "$DEVHUB_HOME/bin/devhub.py" provision \
  --schema "$DEVHUB_HOME/templates/base-schema.json" \
  --seed "$DEVHUB_HOME/templates/seed.example.json"
```

## Tables

- `Projects`: repo identity and current focus.
- `Areas`: modules, code paths, risk, and owner.
- `Tasks`: user-facing task state and next actions.
- `Bugfixes`: what broke, why, how it was fixed, and how verified.
- `Pitfalls`: reusable traps and "check this first" guidance.
- `Playbooks`: repeatable diagnosis order and commands.
- `Decisions`: accepted choices, tradeoffs, and review triggers.
- `Releases`: release evidence before main/master push.
- `Artifacts`: Docs, Whiteboards, dashboards, files, and links.
- `AI Runs`: agent work summaries and verification trail.

## Write Rules

- Always include `Project`, `Area`, `AI Summary`, and `Search Keywords` when the fields exist.
- Put long prose in Docs only when useful; keep Base summaries dense and searchable.
- Use stable names in text fields when relation fields are not configured yet.
- Do not store secrets or raw credentials.
- If a write fails, leave an outbox item. Do not create fake receipts.

## Direct CLI Pattern

When using raw `lark-cli base` commands, read the current schema and field list first:

```bash
lark-cli base +table-list --base-token "$BASE_TOKEN" --as user --format json
lark-cli base +field-list --base-token "$BASE_TOKEN" --table-id "$TABLE_ID" --as user --format json
```

Then write records through `devhub.py` when possible so receipts/outbox stay consistent.
