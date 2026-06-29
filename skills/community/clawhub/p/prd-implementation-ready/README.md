# PRD Implementation Ready Skills

Agent Skills for turning rough product notes, PRDs, BRDs, and functional specs into implementation-ready product requirements.

This repository contains one skill:

- `prd-implementation-ready`: a rigorous PRD completion and review skill for business flows, object states, page UX, data sources, permissions, exceptions, finance/payment/reconciliation/profit-sharing, formulas, and post-event writebacks.

Former internal name: `prd-rigorous-completion`.

## What This Skill Helps With

Use this skill when a product requirement needs to become clear enough for an engineer or coding agent to implement without asking business questions.

It is strongest for:

- B2B/admin/SaaS workflows
- multi-role and multi-tenant business flows
- finance, payment, reconciliation, invoicing, cost, credit, and profit-sharing flows
- object lifecycle and state-machine design
- page structure, fields, data sources, permissions, and idempotency
- exception handling, rollback, red flush, void, retry, and recovery
- formulas, pricing, settlement, guarantees, caps/floors, and adjustments
- post-event writebacks after payment, audit, refund, callback, sync, or batch completion

It also applies to non-finance products where a controlled resource or value must be tracked end to end, such as inventory, coupons, quotas, permissions, appointments, seats, usage rights, or content visibility.

## Repository Layout

```text
.
├── SKILL.md
└── references/
```

`SKILL.md` contains the core workflow and routes to reference files only when needed. The `references/` directory contains detailed gates for finance operations, data flow, page UX, business consistency, output structure, and review checklists.

## Manual Installation

For Codex:

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\prd-implementation-ready"
```

For Claude Code:

```bash
cp -R . ~/.claude/skills/prd-implementation-ready
```

Then start a new session and ask for help writing, reviewing, or completing a PRD.

## Publishing Notes

This repository is intended for skill hubs and marketplaces. Keep the repository public, non-fork, and unarchived so GitHub-based importers can read `SKILL.md`.

Useful search keywords:

- agent skills
- Claude skills
- Codex skills
- PRD
- product requirements
- implementation-ready specs
- B2B SaaS
- finance reconciliation

## License

MIT-0. See [LICENSE](LICENSE).
