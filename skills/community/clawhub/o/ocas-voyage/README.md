# 🧭 Voyage

Voyage builds complete, constraint-aware travel itineraries -- taking a destination, dates, budget, dietary preferences, and pace, then assembling lodging, dining, and activity recommendations into a logistics-optimized plan that is ready for reservation without auto-booking anything. It never presents uncertain operating hours or availability as confirmed fact, and surfaces cost implications throughout so the plan remains honest about what it actually knows.

---

## Overview

Voyage builds travel itineraries that are actually usable -- respecting constraints around budget, dietary preferences, and pace, optimizing logistics across lodging, dining, and activities, and producing plans that are reservation-ready without auto-booking anything. It surfaces cost implications throughout rather than hiding them until checkout, and it never presents uncertain operating hours or availability as confirmed fact. The result is an honest, actionable itinerary rather than an optimistic suggestion list. Voyage may cooperate with Taste for preference-aware recommendations and Weave for trip companion context.

## Commands

| Command | Description |
|---|---|
| `voyage.plan.trip` | Create a full trip plan from destination, dates, and constraints |
| `voyage.recommend.lodging` | Lodging recommendations based on trip context |
| `voyage.recommend.food` | Restaurant recommendations based on route and preferences |
| `voyage.recommend.activities` | Activity recommendations based on interests and logistics |
| `voyage.optimize.itinerary` | Optimize an existing itinerary for feasibility and logistics |
| `voyage.status` | Current plan state, pending reservations, open decisions |
| `voyage.journal` | Write journal for the current run |
| `voyage.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`voyage.init` runs automatically on first invocation and creates all required directories, config.json, state.json, and JSONL files. No manual setup is required. It also registers the `voyage:update` cron job (midnight daily) for automatic self-updates.

## Dependencies

**OCAS Skills**
- [Sift](https://github.com/indigokarasu/sift) -- venue research and availability information
- [Taste](https://github.com/indigokarasu/taste) -- preference-aware recommendations
- [Weave](https://github.com/indigokarasu/weave) -- trip companion context from social graph

**External**
- None

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `voyage:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.3.0 -- March 27, 2026
- Added `voyage.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Run completion procedures with state persistence
- Journal documentation

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Voyage is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
