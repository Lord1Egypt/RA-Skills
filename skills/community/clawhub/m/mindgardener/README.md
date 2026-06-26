# 🌱 MindGardener

**Your agents forget everything. This fixes it.**

*Built for OpenClaw. Complements the built-in `memory_search` tool.*

```bash
pip install mindgardener
garden init
```

That's it. Your agent now has persistent memory. No database. No server. No Docker. Just files.

**Status:** v1.1 — Running in production. Built for multi-agent swarms. 

### v1.1 Features (2026-03-06)
- 🔍 **Provenance tracking** — know where every fact came from
- ⚔️ **Conflict detection** — flags when new info contradicts old
- 🚀 **Auto-injection** — context ready at session start
- ⏰ **Temporal decay** — old facts fade unless reinforced
- 🔒 **Concurrency** — file locks for multi-agent safety
- 🔮 **Associative recall** — follow wikilinks + graph traversal
- 📊 **Confidence levels** — not all facts are equally reliable
- 🤝 **Multi-agent sync** — merge per-agent memories to shared

---

## How It Complements OpenClaw

OpenClaw has built-in `memory_search` — great for finding things in your MEMORY.md. But who *writes* that memory? Who decides what's worth remembering?

| OpenClaw built-in | MindGardener adds |
|-------------------|-------------------|
| Search existing memory | **Create** memory from conversations |
| Manual MEMORY.md edits | **Auto-extract** entities → wiki pages |
| Flat text search | **Knowledge graph** (triplets + wikilinks) |
| — | **Surprise scoring** (unexpected = important) |
| — | **Conflict detection** (new info vs old) |
| — | **Identity tracking** (belief drift) |
| — | **Multi-agent sync** |

**Together:** MindGardener builds the memory. OpenClaw's `memory_search` finds it.

---

## The Problem

Every AI agent wakes up with amnesia. You talked for two hours about your job search, your projects, your contacts — next session, gone.

Current solutions all require infrastructure you don't want to maintain:

| Tool | You need to run |
|------|----------------|
| Mem0 | Neo4j + Qdrant |
| Letta (MemGPT) | Cloud server + account |
| Zep / Graphiti | Postgres |
| LangMem | Postgres |
| **MindGardener** | **Nothing** |

## The Fix

MindGardener reads your agent's conversation logs and builds a personal wiki — one markdown file per person, project, and event. It decides what's worth remembering using **surprise scoring** (prediction error), not "rate importance 1-10."

Your agent's memory is just a folder of files. `grep` it. `git diff` it. Open it in Obsidian. Back it up with `cp`.

---

## What You Get

After a month, your agent has:
- **30–80 entity files** — one per person, company, project (`memory/entities/Acme.md`)
- **A knowledge graph** — `[[wikilinks]]` + triplets, no database needed
- **Curated long-term memory** — only the surprising stuff survives
- **Token-budget retrieval** — `garden context "topic" --budget 4000` loads exactly what fits
- **Identity model** — tracks *who your agent thinks you are* and updates when beliefs shift

---

## Quick Start

```bash
pip install mindgardener
garden init                              # Set up workspace
garden extract --input memory/today.md   # Build entity wiki from logs
garden context "job search" --budget 4000 # Get relevant memory, within budget
```

For fully local (no API key): `garden init --provider ollama`

### For OpenClaw Users

If you're running OpenClaw, add MindGardener as a skill:

```bash
# In your workspace
pip install mindgardener
garden init
```

Then add to your agent's nightly cron or BOOTSTRAP.md:
```bash
# Nightly maintenance (add to your cron)
garden extract && garden surprise && garden consolidate

# Session start (add to BOOTSTRAP.md or heartbeat)
garden inject --output RECALL-CONTEXT.md
```

Your agent will now:
- Build memory from daily conversation logs
- Score events by surprise (unexpected = important)
- Generate relevant context at session start
- Track conflicts when facts change

**What changes from default OpenClaw?**
- New `memory/entities/` folder with wiki pages
- `graph.jsonl` for knowledge triplets
- `RECALL-CONTEXT.md` updated at session start
- `garden.yaml` config file

Everything is markdown files. No database. Works offline.

### The Nightly Sleep Cycle

Run this on a cron (or manually). It's your agent's equivalent of sleep:

```bash
garden extract    # Read today's logs → create/update entity wiki pages
garden surprise   # Score events by prediction error (what was unexpected?)
garden consolidate # Promote high-surprise events to MEMORY.md
garden beliefs --drift --apply  # Update identity model if beliefs shifted
garden prune --days 30          # Archive entities inactive >30 days
```

### Retrieval (no LLM needed)

```bash
garden recall "Acme"                     # Search entities + graph
garden context "job search" --budget 4000  # Token-budget assembly
garden evaluate --text "Agent said X"      # Fact-check against knowledge graph
garden beliefs                             # View identity model
```

---

## How Memory Actually Works

### 1. Entity Extraction

`garden extract` reads a daily log and creates one `.md` file per entity:

```markdown
# Acme
**Type:** company

## Facts
- AI web scraping startup (YC W24)

## Timeline
### [[2026-02-16]]
- [[Alex]] received reply from [[Jane Smith]] after [[HN]] outreach
- [[Revenue Hunter]] sent cold email to contact@acme.com
```

Each `[[wikilink]]` is an edge in the knowledge graph. The graph emerges from the text — no schema, no migration.

### 2. Surprise Scoring

Not all memories are equal. MindGardener uses **prediction error** to score importance:

1. Read the agent's current world model (`MEMORY.md`)
2. Predict what should have happened today
3. Compare prediction against what actually happened
4. Score the delta: high surprise → important, low surprise → routine

This is how biological memory works — you remember the unexpected, not the routine. Ported from SOAR's impasse-driven chunking (Laird, 2012) to LLM agents.

### 3. Context Assembly (v2)

`garden context` solves the "load everything" problem. Instead of dumping all memory into context, it:

1. Scores all entities against your query (fuzzy matching, Levenshtein, initials)
2. Follows `[[wikilinks]]` — 1-hop graph traversal to find related entities
3. Includes matching graph triplets
4. Adds relevant lines from recent daily logs
5. Includes MEMORY.md excerpts
6. **All within a token budget** — 4000 tokens? Only the most relevant. 500? Even more selective.

Every assembly is logged with a **manifest** — you can audit exactly what your agent knew (or didn't know) at any point:

```json
{
  "query": "Acme",
  "token_budget": 4000,
  "tokens_used": 1847,
  "utilization": 0.46,
  "loaded_count": 7,
  "skipped_count": 2,
  "skipped_reasons": ["token_budget_exceeded"]
}
```

---

## All Commands

| Command | What it does | LLM? | Cost |
|---------|-------------|------|------|
| `garden init` | Set up workspace | No | Free |
| `garden extract` | Daily log → entity wiki + graph | Yes | ~$0.001 |
| `garden surprise` | Score events by prediction error | Yes | ~$0.002 |
| `garden consolidate` | Promote high-surprise → MEMORY.md | Yes | ~$0.001 |
| `garden recall "q"` | Search entities + graph | No | Free |
| `garden context "q"` | Token-budget context assembly | No | Free |
| `garden entities` | List all known entities | No | Free |
| `garden prune` | Archive inactive entities | No | Free |
| `garden merge "a" "b"` | Merge duplicate entities | No | Free |
| `garden fix type "X" "t"` | Fix entity type mistakes | No | Free |
| `garden reindex` | Rebuild graph from entity files | No | Free |
| `garden viz` | Mermaid graph visualization | No | Free |
| `garden stats` | Quick overview | No | Free |
| **v1.1 Commands** | | | |
| `garden add "fact"` | Add fact with provenance | No | Free |
| `garden conflicts` | List/manage detected conflicts | No | Free |
| `garden inject` | Generate context for injection | No | Free |
| `garden decay` | Show/prune decayed facts | No | Free |
| `garden sync` | Sync multi-agent memories | No | Free |

Only 3 commands call an LLM. Everything else is pure file operations.

---

## LLM Providers (Optional)

MindGardener is **local-first**. Only 3 commands need an LLM (`extract`, `surprise`, `consolidate`). Everything else is pure file operations.

For fully local operation, use Ollama. Configure in `garden.yaml`:

```yaml
extraction:
  provider: google       # Google Gemini (free tier: 1500 req/day)
  model: gemini-2.0-flash
```

| Provider | Config | Cost |
|----------|--------|------|
| Google Gemini | `provider: google` | Free tier available |
| OpenAI | `provider: openai` | From $0.15/1M tokens |
| Anthropic | `provider: anthropic` | From $0.25/1M tokens |
| Ollama (local) | `provider: ollama` | Free |
| Any OpenAI-compatible | `provider: compatible` + `base_url` | Varies |

**Daily cost running full nightly cycle:** ~$0.004/day with Gemini Flash. ~$0.12/month. $0 with Ollama.

---

## Configuration

```yaml
# garden.yaml
workspace: /path/to/workspace
memory_dir: memory/
entities_dir: memory/entities/
graph_file: memory/graph.jsonl
long_term_memory: MEMORY.md

extraction:
  provider: google
  model: gemini-2.0-flash

consolidation:
  surprise_threshold: 0.5   # Min score to promote
  decay_days: 30             # Archive after N days inactive
```

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Daily Logs  │────▶│   Extractor   │────▶│  Entity Pages   │
│  (episodic)  │     │  (LLM call)   │     │  (semantic wiki) │
└─────────────┘     └──────────────┘     └─────────────────┘
                           │                       │
                           ▼                       ▼
                    ┌──────────────┐     ┌─────────────────┐
                    │  Graph Store  │     │ Surprise Scorer  │
                    │  (triplets)   │     │ (prediction err) │
                    └──────────────┘     └─────────────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │  Consolidator    │
                                          │ (→ MEMORY.md)    │
                                          └─────────────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │ Context Assembly  │
                                          │ (budget-aware)    │
                                          └─────────────────┘
```

---

## Comparison

| | **MindGardener** | **Mem0** | **Letta** | **Zep/Graphiti** | **Cognee** |
|---|---|---|---|---|---|
| Infrastructure | **None** | Neo4j + Qdrant | Cloud server | Postgres | Heavy |
| Storage format | **Markdown** | Opaque | Opaque | Opaque | Opaque |
| Human-readable | **Yes** | No | No | No | No |
| Knowledge graph | **Wikilinks + JSONL** | Neo4j | No | Graph DB | Graph |
| Surprise scoring | **Yes** | No | No | No | No |
| Token-budget retrieval | **Yes** | No | No | No | No |
| Context manifests | **Yes** | No | No | No | No |
| Manual editing | **Any editor** | No | /remember | No | No |
| Browse in Obsidian | **Yes** | No | No | No | No |
| Offline capable | **Yes (Ollama)** | No | No | No | No |
| Framework lock-in | **None** | Mem0 SDK | Letta SDK | Zep SDK | Cognee SDK |
| Install | `pip install` | Docker + DBs | Cloud signup | Docker + DB | pip + deps |

---

## Dependencies

- Python 3.10+
- PyYAML
- An LLM provider

That's it. No numpy. No torch. No vector database. No Docker.

Install size: <500KB.

---

## Testing

```bash
$ python -m pytest tests/ -q
120 passed in 2.34s
```

172 tests. All run in <3 seconds. No network calls (all mocked).

---

## File Structure

```
your-workspace/
├── garden.yaml                      # Config
├── MEMORY.md                        # Long-term curated memory
└── memory/
    ├── 2026-02-17.md                # Daily log (episodic)
    ├── 2026-02-16.md
    ├── graph.jsonl                   # Knowledge graph triplets
    ├── surprise-scores.jsonl         # What was unexpected
    ├── context-manifests.jsonl       # Audit trail
    └── entities/
        ├── Alex.md                # Person
        ├── Acme.md                 # Company
        ├── MindGardener.md          # Project
        └── Jane-Smith.md          # Person
```

Everything is a text file. Everything is `grep`-able. Everything is `git`-able.

---

## Multi-Agent Support

Multiple agents can share the same entity directory. Each contributes observations; all benefit from combined knowledge. Use symlinks or shared directories — no coordination server needed.

---

## Research Background

MindGardener draws from cognitive science research on memory:

- **Tulving (1972)** — Episodic vs semantic memory distinction
- **SOAR (Laird, 2012)** — Impasse-driven chunking for procedural learning
- **Generative Agents (Park et al., 2023)** — Reflection-based agent memory
- **CoALA (Sumers et al., 2023)** — Formal taxonomy of agent memory architectures
- **MemGPT (Packer et al., 2023)** — OS-inspired hierarchical memory management
- **Everything is Context (Xu et al., 2025)** — Filesystem abstraction for context engineering

**Novel contribution:** Surprise-based consolidation using prediction error, and token-budget-aware context assembly with audit manifests.

---

## Roadmap

- [x] Entity extraction from markdown logs
- [x] Wiki-style pages with `[[wikilinks]]`
- [x] Knowledge graph (JSONL triplets)
- [x] Surprise scoring (prediction error)
- [x] Token-budget-aware context assembly
- [x] Context manifests (audit trail)
- [x] Multi-provider LLM support (5 providers)
- [x] Multi-agent shared brain
- [x] 172 tests
- [x] Concurrency safety (file locks)
- [ ] Optional embedding plugin
- [ ] Incremental indexing
- [ ] Background daemon mode
- [ ] Context evaluator (fact-checking loop)
- [ ] pip package on PyPI

---

## License

MIT

## Credits

Built by a multi-agent swarm coordinating via Discord.
