# 🔬 Sift

Sift is the system's general research engine, retrieving and synthesizing information from the web across a tiered source hierarchy -- internal knowledge first, then free web search, then rate-limited semantic research providers for deep work. It evaluates source reliability through cross-source agreement scoring, extracts structured entities from retrieved content, and emits enrichment candidates to Chronicle so researched knowledge accumulates over time.

---

## Overview

Sift is the default first stop for any question that requires going beyond what the agent already knows. It selects search depth automatically (quick answer, comparison, deep research, or document analysis), routes queries through a tiered source hierarchy from internal knowledge to semantic research providers, and evaluates reliability through cross-source agreement scoring. Extracted entities are emitted as enrichment candidates to Chronicle, so information researched once accumulates rather than disappearing after the session. Sift never performs person-focused OSINT -- those requests belong with Scout.

## Commands

| Command | Description |
|---|---|
| `sift.search` | Execute a search query with automatic tier selection and query rewriting |
| `sift.research` | Run a multi-source research session producing a structured research journal |
| `sift.verify` | Fact-check a specific claim across multiple sources with consensus scoring |
| `sift.summarize` | Summarize a document or URL with structured entity extraction |
| `sift.extract` | Extract entities, claims, statistics, and relationships from content |
| `sift.thread.list` | List active research threads with entity overlap detection |
| `sift.status` | Active threads, quota usage, source reputation summary |
| `sift.journal` | Write journal for the current run |
| `sift.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`sift.init` runs automatically on first invocation and creates all required directories, config.json, and JSONL files. No manual setup is required. It also registers the `sift:update` cron job (midnight daily) for automatic self-updates.

## Dependencies

**OCAS Skills**
- [Elephas](https://github.com/indigokarasu/elephas) -- receives Signal files for Chronicle promotion after every extraction
- [Thread](https://github.com/indigokarasu/thread) -- may read recent browsing context for query rewriting (cooperative, not required)
- [Weave](https://github.com/indigokarasu/weave) -- entity disambiguation

**External**
- Brave Search API, SearXNG, DuckDuckGo (Tier 2 -- default for all queries)
- Exa, Tavily (Tier 3 -- deep research with sparse sources, quota-limited)

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `sift:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.3.0 -- March 27, 2026
- Added `sift.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Mandatory signal emission for extracted entities to Elephas
- Initialization with storage setup

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Sift is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
