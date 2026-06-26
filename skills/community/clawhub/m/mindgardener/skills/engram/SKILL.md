---
name: engram
description: "Persistent memory layer with knowledge graph and surprise-driven consolidation. Extract entities, build wiki pages, score prediction errors, and recall context — all from markdown files."
homepage: https://github.com/maweding/agent-engram
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"pip":["agent-engram"]}}}
---

# Engram — Agent Memory

Give your agent a brain that persists across sessions. No database, no server — just markdown files.

## Setup

```bash
pip install agent-engram
```

Configure in `engram.yaml` (workspace root):
```yaml
workspace: .
provider: gemini          # or openai, anthropic, ollama, compatible
model: gemini-2.0-flash   # any model your provider supports
```

Set your API key:
```bash
export GEMINI_API_KEY=...   # or OPENAI_API_KEY, ANTHROPIC_API_KEY
```

For local models (zero cost):
```yaml
provider: ollama
model: llama3.2
```

## Daily Workflow

### After each session — extract what happened:
```bash
engram extract                          # Process today's daily log
engram extract --date 2026-02-16        # Process specific date
engram extract --all                    # Process all unprocessed dates
```

This creates entity wiki pages in `memory/entities/` and triplets in `memory/graph.jsonl`.

### Query what you know:
```bash
engram recall "Kadoa"                   # Entity page + graph neighbors
engram recall "peter"                   # Fuzzy match → Peter Steinberger
engram entities                         # List all known entities
```

### What was surprising today?
```bash
engram surprise                         # Prediction error scoring
engram surprise --date 2026-02-16       # Score specific date
```

Output:
```
🔴 [0.8] Repo renamed to openclaw/openclaw
🟡 [0.7] HOT BUG: Session Path Regression
🟢 [0.2] Routine PR work
📉 Learning rate: 0.60
```

### Nightly sleep cycle — consolidate to long-term memory:
```bash
engram consolidate                      # Promote high-surprise events to MEMORY.md
```

### Maintenance:
```bash
engram decay --dry-run                  # Show stale entities
engram decay --execute                  # Archive entities not referenced in 30+ days
engram merge --detect                   # Find duplicate entities
engram merge "steipete" "Peter Steinberger"  # Merge two entities
engram viz                              # Render knowledge graph (Mermaid)
engram stats                            # Memory statistics
```

## How It Works

1. **Extract** — LLM reads daily markdown logs, outputs entities + relationships + events
2. **Surprise** — Two-stage prediction error: predict what should happen → compare with reality → delta = surprise score
3. **Consolidate** — Only high-surprise events promoted to MEMORY.md (the "sleep cycle")
4. **Decay** — Unreferenced entities archived after 30 days. Active ones reinforced.

## Recommended Cron Setup

Run the full sleep cycle nightly:
```bash
# In your agent's cron (e.g., 03:00 daily):
engram extract && engram surprise && engram consolidate && engram decay --execute
```

Or use Clawdbot's cron:
```json
{"name": "engram-nightly", "schedule": {"kind": "cron", "expr": "0 3 * * *"}, "payload": {"kind": "systemEvent", "text": "Run nightly engram cycle: engram extract && engram surprise && engram consolidate"}}
```

## Multi-Agent Setup

Multiple agents can share a knowledge graph:
```bash
# Shared entities directory (symlink from each agent's workspace)
ln -s /shared/memory/entities /agent-a/memory/entities
ln -s /shared/memory/entities /agent-b/memory/entities
```

Each agent writes to the shared graph. Entity pages accumulate knowledge from all agents.

## File Structure

```
memory/
├── 2026-02-17.md           # Daily log (you write this)
├── entities/               # Auto-generated wiki pages
│   ├── Kadoa.md
│   ├── OpenClaw.md
│   └── Peter-Steinberger.md
├── graph.jsonl             # Knowledge graph triplets
├── prediction-errors.jsonl # PE scores history
└── surprise-scores.jsonl   # Surprise history
```

## Tips

- Entity pages are plain markdown — edit them manually if the LLM gets something wrong
- Use `[[wikilinks]]` in your daily logs to help extraction
- `graph.jsonl` is queryable with `jq`: `jq 'select(.object == "Kadoa")' memory/graph.jsonl`
- Git-version your `memory/` directory for full history
