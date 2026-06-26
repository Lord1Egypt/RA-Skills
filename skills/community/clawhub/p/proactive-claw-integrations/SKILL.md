---
name: Proactive Claw Integrations
description: >
  Optional network and automation helpers for Proactive Claw core:
  GitHub/Notion cross-skill context, team calendar awareness, daemon installer,
  and optional clawhub OAuth bootstrap.

version: 0.1.0

metadata:
  openclaw:
    requires:
      bins: [python3]
      skills: [proactive-claw]
    install:
      - kind: shell
        label: "Install core first. Then enable only the integrations you need."
---

# Proactive Claw Integrations

This add-on contains integrations intentionally split from core for privacy-focused deployments.

## Included scripts

- `scripts/cross_skill.py` (GitHub + Notion context enrichment)
- `scripts/team_awareness.py` (shared team calendar coordination)
- `scripts/install_daemon.sh` (background scheduler installer)
- `scripts/optional/setup_clawhub_oauth.sh` (optional credentials bootstrap)

## Important

- Requires `proactive-claw` core skill already installed.
- These scripts operate on core data under:
  `~/.openclaw/workspace/skills/proactive-claw/`
- Enable each integration explicitly; do not enable what you do not need.
