# 🔍 Scout

Scout conducts lawful OSINT research on people, companies, and organizations, assembling provenance-backed briefs where every claim carries a source reference, retrieval timestamp, and direct quote. It works through a tiered source waterfall -- public web first, then rate-limited registries, then paid databases only with explicit permission -- collecting no more than the stated research goal requires.

---

## Overview

Scout makes research provenance a first-class requirement. Every claim in a Scout brief traces to a source with URL, retrieval timestamp, and direct quote -- no unsupported assertions. It works through a tiered source waterfall: public web sources automatically, rate-limited registries if useful, paid OSINT databases only after explicit permission is recorded. Collection is bounded to what the stated research goal actually requires, and private details are suppressed unless explicitly permitted. Confirmed entities and relationships discovered during research are emitted as signal candidates to Chronicle.

## Commands

| Command | Description |
|---|---|
| `scout.research.start` | Begin a new research request with subject and goal |
| `scout.research.expand --tier <1\|2\|3>` | Escalate to a higher source tier |
| `scout.brief.render` | Generate the final markdown brief with findings and sources |
| `scout.brief.render_pdf` | Optional PDF brief generation |
| `scout.status` | Current research state |
| `scout.journal` | Write journal for the current run |
| `scout.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`scout.init` runs automatically on first invocation and creates all required directories, config.json, and JSONL files. No manual setup is required. It also registers the `scout:update` cron job (midnight daily) for automatic self-updates.

## Dependencies

**OCAS Skills**
- [Weave](https://github.com/indigokarasu/weave) -- social graph read-only for identity context
- [Elephas](https://github.com/indigokarasu/elephas) -- receives Signal files for confirmed entities
- [Sift](https://github.com/indigokarasu/sift) -- web searches during research

**External**
- Paid OSINT providers (Tier 3, optional -- requires explicit permission grant before use)

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `scout:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.3.0 -- March 27, 2026
- Added `scout.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Signal emission to Elephas for confirmed entities and relationships
- Journaling as mandatory final step in every research run

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Scout is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
