# 🧹 Custodian

Custodian detects, classifies, and repairs OpenClaw operational failures autonomously during quiet hours so the user wakes to clean logs, initialized skills, and registered background tasks -- surfacing only what it could not fix.

---

## Overview

Custodian monitors the OpenClaw gateway logs, cron job registry, skill journals, and OCAS data directories for operational failures. It fingerprints errors against a known-issues registry, classifies them into tiers (auto-fix, surface with plan, escalate, or alert-only), and applies safe, non-destructive repairs within a strict safety envelope. It initializes uninitialized skills, registers missing background tasks, and maintains an activity model that optimizes its own scan schedule toward quiet hours. Fixes that recur after repair are automatically promoted to escalation tier. Unknown errors trigger a progressive web search protocol that learns new fix patterns over time.

## Commands

| Command | Description |
|---|---|
| `custodian.init` | Create storage directories, register background tasks, copy bundled plan to Mentor |
| `custodian.scan.light` | Quick scan: tail gateway log, check cron health, retry failed fixes |
| `custodian.scan.deep` | Full sweep: all checks, conformance, activity model, repair pass, report |
| `custodian.verify {fix_id}` | Verify outcome of a specific fix |
| `custodian.repair.auto` | Apply all pending Tier 1 fixes from last scan |
| `custodian.repair.plan` | Generate structured repair plan for Tier 2/3 issues |
| `custodian.issues.list` | List open issues with tier, status, age, recurrence |
| `custodian.issues.resolve {issue_id}` | Mark issue resolved manually |
| `custodian.status` | Current health state |
| `custodian.schedule.show` | Display current and target scan schedule |
| `custodian.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`custodian.init` runs automatically on first invocation and creates all required directories, config.json, and JSONL files. It registers the `custodian:deep` cron job (6-hour cycle), the `custodian:light` heartbeat entry, and the `custodian:update` midnight cron. It also copies the bundled `custodian-repair.plan.md` workflow plan to Mentor's plans directory. No manual setup is required.

## Dependencies

**OCAS Skills**
- [Vesper](https://github.com/indigokarasu/vesper) -- receives InsightProposal alerts after deep scans
- [Mentor](https://github.com/indigokarasu/mentor) -- reads escalation-tagged journals; runs custodian-repair workflow plan
- [Corvus](https://github.com/indigokarasu/corvus) -- optional activity pattern blending for schedule optimization
- [Sift](https://github.com/indigokarasu/sift) -- used by custodian-repair plan for diagnosis research

**External**
- None

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `custodian:light` | heartbeat | every heartbeat cycle | `custodian.scan.light` |
| `custodian:deep` | cron | optimized 6h (initial: `0 1,7,13,19 * * *` PT) | `custodian.scan.deep` |
| `custodian:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v1.0.0 -- March 27, 2026
- Initial release: gateway log scanning, cron health monitoring, skill journal validation
- Tier 1 auto-fix with 11 pre-seeded fingerprints and verification jobs
- Skill conformance checking and automatic initialization
- Activity model with 14-day rolling window and schedule optimization
- Web search protocol with 5-mutation query sequence and learned-issues accumulation
- Fix effectiveness tracking with high-recurrence auto-escalation
- Bundled custodian-repair workflow plan for Mentor
- Vesper integration for escalation alerts

---

*Custodian is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
