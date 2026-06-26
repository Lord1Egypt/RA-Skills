# 🌅 Vesper

Vesper is the system's daily voice -- it aggregates signals from every other skill and presents what matters as a concise, conversational morning or evening briefing, surfacing concrete outcomes, upcoming decisions, and actionable opportunities without exposing any internal architecture or analysis processes. Its signal filtering is strict: routine background activity, speculative observations, and already-experienced events are excluded, so every briefing earns attention rather than demanding it.

---

## Overview

Vesper aggregates signals from every other skill -- portfolio outcomes from Rally, insight proposals from Corvus, pending commitments from Dispatch, upcoming calendar events -- and assembles them into a concise morning or evening briefing in natural language. Its signal filtering is strict: routine background activity, speculative observations, and already-experienced events are excluded. The result is a briefing that earns attention rather than demanding it, with no internal architecture or system terminology visible to the reader. Vesper also presents pending decision requests with option, benefit, and cost framing -- but never nags about ignored decisions.

## Commands

| Command | Description |
|---|---|
| `vesper.briefing.morning` | Generate morning briefing |
| `vesper.briefing.evening` | Generate evening briefing |
| `vesper.briefing.manual` | On-demand briefing |
| `vesper.decisions.pending` | List unacted decision requests |
| `vesper.config.set` | Update schedule, sections, delivery settings |
| `vesper.status` | Last briefing time, pending decisions, schedule |
| `vesper.journal` | Write journal for the current run |
| `vesper.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`vesper.init` runs automatically on first invocation and creates all required directories, config.json, and JSONL files. It also registers the `vesper:morning` cron job (daily 7am) and `vesper:evening` cron job (daily 6pm) and `vesper:update` (midnight daily, self-update). No manual setup is required.

## Dependencies

**OCAS Skills**
- [Corvus](https://github.com/indigokarasu/corvus) -- sends InsightProposal files via Vesper intake directory
- [Dispatch](https://github.com/indigokarasu/dispatch) -- may deliver briefings on request
- [Rally](https://github.com/indigokarasu/rally) -- portfolio outcome signals for briefing content

**External**
- Calendar and Weather APIs (for briefing content)

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `vesper:morning` | cron | `0 7 * * *` (daily 7am) | Morning briefing generation |
| `vesper:evening` | cron | `0 18 * * *` (daily 6pm) | Evening briefing generation |
| `vesper:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.6.0 -- April 2, 2026
- Structured entity observations in journal payloads (`entities_observed`, `relationships_observed`, `preferences_observed`)
- `user_relevance` tagging on journal observations (`user` for calendar/task entities, `agent_only` for external news context)
- Elephas journal cooperation in skill cooperation section

### v2.3.0 -- March 27, 2026
- Added `vesper.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Daily briefing synthesis with Corvus InsightProposal intake
- Two background cron tasks registered at initialization

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Vesper is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
