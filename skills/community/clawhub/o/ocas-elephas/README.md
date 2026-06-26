# 🐘 Elephas

Elephas is the system's long-term memory -- the sole writer to Chronicle, the authoritative knowledge graph where entities, relationships, events, and inferences live permanently once confirmed. It ingests structured signals from every skill's journals, scores candidate facts for confidence, resolves identity across possible duplicates, and promotes what survives into durable Chronicle facts with full provenance.

---

## Overview

Every other skill in the OCAS suite generates signals -- Elephas is what makes those signals permanent. It ingests structured signal files from all skill journals, scores candidate facts for confidence, resolves identity across potential duplicates using a staged merge protocol, and promotes what survives into Chronicle as durable facts with full provenance. As the sole writer to Chronicle, Elephas is the single source of truth for long-term world knowledge in the system. The Chronicle database (LadybugDB, embedded single-file graph) initializes automatically on first use at `~/openclaw/db/ocas-elephas/chronicle.lbug`.

## Commands

| Command | Description |
|---|---|
| `elephas.ingest.journals` | Ingest structured signals from skill journal files and signal intake directory |
| `elephas.consolidate.immediate` | Score candidate confidence, promote above threshold, flag possible matches |
| `elephas.consolidate.deep` | Full identity reconciliation, inference generation, graph cleanup |
| `elephas.identity.resolve` | Attempt to resolve whether two Entity records are the same real-world entity |
| `elephas.identity.merge` | Merge two confirmed-same Entity records (always reversible) |
| `elephas.candidates.list` | List pending candidates by confidence tier and age |
| `elephas.candidates.promote` | Manually promote a candidate to a confirmed Chronicle fact |
| `elephas.candidates.reject` | Reject a candidate with stated reason |
| `elephas.query` | Query Chronicle for entities, relationships, events, or inferences |
| `elephas.init` | Diagnostic and repair: checks schema, creates missing tables, verifies indexes |
| `elephas.status` | Chronicle health: entity counts, pending candidates, last consolidation timestamps |
| `elephas.journal` | Write journal for the current run |
| `elephas.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`elephas.init` runs automatically on first invocation and creates all required directories, config.json, the Chronicle database, and JSONL files. It also registers the `elephas:ingest` and `elephas:deep` cron jobs and `elephas:update` (midnight daily, self-update). No manual setup is required.

## Dependencies

**OCAS Skills**
- All skills -- ingest structured signals from skill journals and signal intake directory
- [Weave](https://github.com/indigokarasu/weave) -- read-only cross-DB queries for social graph enrichment
- [Mentor](https://github.com/indigokarasu/mentor) -- reads Chronicle read-only for evaluation context

**External**
- LadybugDB -- embedded single-file graph database (auto-created at `~/openclaw/db/ocas-elephas/chronicle.lbug`)

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `elephas:ingest` | cron | `*/15 * * * *` (every 15 min) | Ingest journals then immediate consolidation |
| `elephas:deep` | cron | `0 4 * * *` (daily 4am) | Full identity reconciliation, inference, cleanup |
| `elephas:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.3.0 -- March 27, 2026
- Added `elephas.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Automated maintenance with cron registration
- Ingestion pipeline with staged signal promotion
- Deep consolidation pass with identity reconciliation

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Elephas is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
