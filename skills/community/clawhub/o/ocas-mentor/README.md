# 🎓 Mentor

Mentor is the system's control plane -- in runtime mode it decomposes goals into task graphs, supervises execution across skills, and dynamically repairs failures through a layered escalation policy from local retry up to full strategy replan. In heartbeat mode it reads journals from every skill, scores OKR performance against baselines, and generates improvement proposals that flow to Forge and Fellow for empirical evaluation and promotion.

---

## Overview

Mentor operates in two modes that share state and telemetry. In runtime mode it acts as an orchestration engine -- decomposing goals into task graphs, supervising execution across skills, and repairing failures through a layered escalation policy from local retry up to full strategy replan. In heartbeat mode it reads journals from every skill, scores OKRs against baselines, generates improvement proposals that go to Forge for building, and routes experiments to Fellow for empirical evaluation. Together these modes form a self-improving control plane. Mentor and Elephas are parallel journal consumers -- neither blocks the other.

Mentor also supports named Workflow Plans -- pre-authored, parameterized task sequences that can be invoked by name with arguments, run on a schedule, or triggered via heartbeat. Plans encode multi-skill workflows (like contact enrichment) so they can be repeated reliably without reconstructing the task graph each time.

## Commands

| Command | Description |
|---|---|
| `mentor.project.create` | Create a project with goal, constraints, and requested output |
| `mentor.project.status` | Current project state, task graph, execution progress |
| `mentor.project.replan` | Trigger strategy-level replan |
| `mentor.task.list` | Tasks with statuses, dependencies, blocking reasons |
| `mentor.heartbeat.light` | Lightweight pass: ingest journals, update aggregates, queue work |
| `mentor.heartbeat.deep` | Deep pass: full scoring, trend analysis, proposals |
| `mentor.variants.list` | Active champion/challenger pairs with evaluation status |
| `mentor.variants.decide` | Emit promotion decision for a variant |
| `mentor.proposals.list` | Pending skill improvement proposals |
| `mentor.proposals.create` | Generate a VariantProposal for a target skill |
| `mentor.status` | Active projects, pending evaluations, self-improvement metrics |
| `mentor.journal` | Write journal for the current run |
| `mentor.update` | Pull latest from GitHub source (preserves journals and data) |
| `mentor.plan.list` | List available workflow plans with version and description |
| `mentor.plan.run` | Execute a named workflow plan with optional arguments |
| `mentor.plan.status` | Current state of a running or recent plan run |
| `mentor.plan.resume` | Continue a paused or failed plan run from the last incomplete step |
| `mentor.plan.history` | Recent plan run summaries |

## Setup

`mentor.init` runs automatically on first invocation and creates all required directories, config.json, and JSONL files. It registers the `mentor:deep` cron job (daily 5am) and the `mentor:light` heartbeat entry. It also copies bundled workflow plans from the skill package to `~/openclaw/data/ocas-mentor/plans/`. No manual setup is required.

## Dependencies

**OCAS Skills**
- [Forge](https://github.com/indigokarasu/forge) -- receives VariantProposal and VariantDecision files via intake directory
- [Fellow](https://github.com/indigokarasu/fellow) -- invoked to run controlled benchmark experiments
- [Elephas](https://github.com/indigokarasu/elephas) -- Chronicle read-only for evaluation context
- [Corvus](https://github.com/indigokarasu/corvus) -- pattern data for anomaly context
- All skills -- reads journals from all skills for evaluation

**External**
- None

## Workflow Plans

Mentor ships with a bundled plan library. Plans are parameterized, reusable workflows that Mentor can run on demand or on a schedule.

| Plan | Description |
|---|---|
| `contact-enrichment` | Enriches a Weave contact by scanning Gmail, running Scout OSINT, and Sift web search |

Run a plan manually:

```
mentor.plan.run contact-enrichment
mentor.plan.run contact-enrichment --arg contact_id=person_abc123
```

Schedule a daily run against a random contact:

```bash
openclaw cron add --name mentor:contact-enrich \
  --schedule "0 3 * * *" \
  --command "mentor.plan.run contact-enrichment" \
  --sessionTarget isolated --lightContext true --wakeMode next-heartbeat \
  --timezone America/Los_Angeles
```

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `mentor:deep` | cron | `0 5 * * *` (daily 5am) | Full OKR scoring, trend analysis, variant proposals |
| `mentor:light` | heartbeat | Every heartbeat pass | Ingest journals, update aggregates, queue work |
| `mentor:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.3.0 -- March 25, 2026
- Added Workflow Plans system: named, parameterized task sequences invokable by name or via cron/heartbeat
- New commands: `mentor.plan.list`, `mentor.plan.run`, `mentor.plan.status`, `mentor.plan.resume`, `mentor.plan.history`
- Bundled contact-enrichment plan (Gmail + Scout + Sift pipeline)
- Init now creates `plans/` and `plan-runs/` directories and copies bundled plans

### v2.3.0 -- March 27, 2026
- Added `mentor.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Run completion with Forge intake integration
- Initialization with cron and heartbeat registration
- Background task definitions

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite

---

*Mentor is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*