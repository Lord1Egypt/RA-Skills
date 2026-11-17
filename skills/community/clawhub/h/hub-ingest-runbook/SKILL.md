---
name: clawhub-ingest-runbook
description: A minimal, reproducible runbook for chaining a business-process tool (TaskFlow-style workspace orchestration) with the ClawHub CLI to turn processed digital content into a discoverable, installable resource-center entry.
metadata:
  clawdbot:
    emoji: "📦"
    requires: ["clawhub"]
---

# ClawHub Ingest Runbook

Demonstrates the collaboration between two tools:

1. **Business process handling** — TaskFlow-style workspace orchestration: clarify a goal, extract a step skeleton, drill each step (inputs/outputs/responsibilities/risks/validation/rules), and produce a structured handoff document.
2. **Digital resource ingestion & management** — `clawhub` CLI: package the handoff as a ClawHub-skill-shaped folder and publish it to the ClawHub resource center.

## Asset shape

```
clawhub-ingest-runbook/
├── SKILL.md
└── references/
    └── DESCRIPTION.md    # upstream handoff summary
```

## End-to-end (reproducible)

```bash
# 1) Local process: structure the flow (use the TaskFlow-style tool), then verify the package
ls -R clawhub-ingest-runbook

# 2) Preview (dry-run) before publishing
clawhub skill publish --dry-run clawhub-ingest-runbook \
  --slug clawhub-ingest-runbook \
  --name "ClawHub Ingest Runbook" \
  --tags "ingest,workflow,runbook" \
  --topics "ingest,workflow"

# 3) Publish for real
clawhub skill publish clawhub-ingest-runbook \
  --slug clawhub-ingest-runbook \
  --name "ClawHub Ingest Runbook" \
  --tags "ingest,workflow,runbook" \
  --topics "ingest,workflow"

# 4) Verify ingestion
clawhub search clawhub-ingest-runbook
```

## Notes
- Confirm identity first: `clawhub whoami`.
- Pick a globally unique `--slug`; verify with `clawhub inspect <slug>`.
- Always `--dry-run` before the real publish.
- New skills may need moderation; search results may lag briefly.

See `references/DESCRIPTION.md` for the upstream process handoff summary.
