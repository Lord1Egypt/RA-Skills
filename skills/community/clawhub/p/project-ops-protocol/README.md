# project-ops-protocol

![LGD-powered](https://raw.githubusercontent.com/zhaoxinghua09-cell/lgd-theory/main/assets/badges/powered/lgd-powered-en.svg)
![LGD](https://raw.githubusercontent.com/zhaoxinghua09-cell/lgd-theory/main/assets/badges/lgd-aligned-en.svg)

**A lightweight operating protocol for serious projects that run across multiple AI sessions, agents and one (or more) humans.**

Proven in the field on a long-running multi-session build (100+ documents, 50+ tools, parallel AI sessions) — no lost state, no duplicated work, no collisions.

## What you get

- **Four layers**: Plan (layered battle map + honest watchlist) → Execute (measure first, reuse before rebuild) → Sync (append-only alignment board + milestone heartbeats) → Memory (relay note + handbook-first rules).
- **Seven standard artifacts** with one job each and a write rule (battle map, release ledger, topic ledger, alignment board, relay note, retrospective, handbook).
- **Eight hard rule cards** that prevent the common failure modes (lost context, silent overwrites, duplicated work, secret leakage, publishing too early).
- **LLM-as-judge quality rubric** (5 dimensions, ≥0.80 pass) plus a 30-second self-check for anything that goes public.
- **Day-1 and wrap-up checklists** you can paste into any project.

## Install (as an agent skill)

Copy the `SKILL.md` into your agent's skills directory (e.g. `~/.workbuddy/skills/project-ops-protocol/SKILL.md`, or `.claude/skills/...`), or clone this repo and point your skill loader at the `SKILL.md`.

```bash
git clone https://github.com/zhaoxinghua09-cell/project-ops-protocol
```

## Why it works (credits)

Borrowed, credited and adapted from best practices that are public:

- **Handbook-first / single source of truth** — GitLab's all-remote operating culture.
- **Orchestrator-worker + compressed findings + Memory** — Anthropic's multi-agent research system engineering notes.
- **Judge-gated publishing** — LLM-as-judge evaluation, small-sample early checks.
- **Plain files over heavy memory infra** — Letta's filesystem agents beating specialised memory tools on LoCoMo is a strong hint to start simple.

## License

© 2026 Zhao Xinghua (Steven Zhao) — [CC BY 4.0](LICENSE) · MedXpert × SynomosAI
