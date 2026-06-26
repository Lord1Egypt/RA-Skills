# 👁️ Look

Look bridges the physical world and the digital agent -- it takes a user-provided image, infers what the user probably wants done with it, and produces a validated, decision-ready action draft across domains including calendar events, meal macros, places, product comparisons, receipts, documents, and civic reports. It resolves ambiguity through research and option reduction before asking any clarifying questions, and nothing executes without explicit per-draft confirmation.

---

## Overview

Look closes the gap between the physical world and the digital agent stack. A photo of a restaurant flyer becomes a calendar event draft. A meal photo becomes a macro estimate. A storefront becomes a saved place. A receipt becomes an expense entry. Look infers intent from visual evidence, reduces ambiguity through research and option reduction before asking any clarifying questions, and produces one to three decision-ready drafts -- none of which execute without explicit per-draft confirmation. Extracted entities (places, events, products) are emitted as enrichment candidates to Chronicle so discovered knowledge accumulates.

## Commands

| Command | Description |
|---|---|
| `look.ingest.image` | Ingest image(s) with optional EXIF and device pre-parse |
| `look.propose.actions` | Generate ActionDrafts with DecisionRecords |
| `look.execute.action` | Execute a confirmed draft (requires explicit approval) |
| `look.rollback.action` | Attempt rollback for reversible actions |
| `look.status` | Last ingest, pending drafts, items awaiting confirmation |
| `look.config.set` | Update configuration |
| `look.journal` | Write journal for the current run |
| `look.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`look.init` runs automatically on first invocation and creates all required directories, config.json, state.json, and JSONL files. No manual setup is required. It also registers the `look:update` cron job (midnight daily) for automatic self-updates.

## Dependencies

**OCAS Skills**
- [Sift](https://github.com/indigokarasu/sift) -- web research for validation during draft generation
- [Elephas](https://github.com/indigokarasu/elephas) -- receives Signal files for extracted entities after draft generation

**External**
- None

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `look:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.3.0 -- March 27, 2026
- Added `look.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Signal emission to Elephas for extracted entities
- Journal documentation and mandatory confirmation enforcement

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Look is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
