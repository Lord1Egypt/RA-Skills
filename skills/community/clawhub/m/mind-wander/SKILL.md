---
name: mind-wander
description: >
  Background reasoning agent that autonomously explores open questions using a local LLM
  (Qwen3.5-9B), a private knowledge graph for dead-end tracking, and Perplexity web search.
  Fires on a schedule, picks one unresolved question from ON_YOUR_MIND.md, runs sandbox
  experiments and web searches, and writes findings to MENTAL_EXPLORATION.md only when
  genuinely novel — mirroring hippocampal background consolidation. Uses a separate
  FalkorDB 'wander' graph so exploration history never pollutes the primary agent context.
  Use when: setting up autonomous background research for an OpenClaw agent, exploring
  research questions without consuming primary LLM token budget, building training data
  from exploratory reasoning sessions, or tracking dead ends to avoid re-exploration.
  Triggers on: "mind wander", "background reasoning", "autonomous research", "wander agent",
  "ON_YOUR_MIND", "MENTAL_EXPLORATION", "dead ends", "explore while I sleep".
---

# Mind-Wander Skill

Autonomous background reasoning agent. Runs locally on Qwen3.5-9B, consumes zero
Anthropic tokens, and elevates findings to your context only when genuinely novel.

## How it works

```
ON_YOUR_MIND.md  →  Qwen3.5 wander agent (every 30min)
  open questions       ↓ tools: query_graph, search_web,
  tangents             ↓         read_file, sandbox_run,
  hypotheses           ↓         check_dead_ends, record_dead_end, elevate()
                       ↓
              novelty gate (strict)
                  ↙         ↘
           MENTAL_EXPLORATION.md    DEAD_ENDS.md + wander graph
           (elevated findings)      (closed threads, never in your context)
                  ↓
           memwatchd detects write
                  ↓
           graph-rag memory (your context)
```

## Prerequisites

- Qwen3.5-9B-Q8 pulled to Ollama: `ollama pull qwen3.5-wander-q8` (or use install script)
- FalkorDB running (shared with graph-rag-memory skill if installed)
- Perplexity API key (optional but recommended for web search)
- graph-rag-memory skill installed (recommended — shares FalkorDB and Ollama)

## Quick start

```bash
# Install and set up
bash mind-wander/scripts/install.sh

# Write your first open question
echo "## What is the best approach to X?" >> ON_YOUR_MIND.md

# Run manually
python3 mind-wander/run.py --verbose

# Check findings
cat MENTAL_EXPLORATION.md
cat DEAD_ENDS.md

# Status
python3 mind-wander/run.py --status
```

## The ON_YOUR_MIND.md anchor file

Create `ON_YOUR_MIND.md` in your workspace root with questions and tangents.
The agent picks ONE per session. Format freely — the agent reads it as-is.

```markdown
# On My Mind

## Open Questions
- Does X actually work better than Y in production?
- Is there a paper on Z that I haven't found yet?

## Tangents
- The implementation of A might connect to B in an interesting way
```

Mark completed items with `## ✅ COMPLETED` so the agent skips them.

## The novelty gate

- **Restatement of known facts** → discarded, nothing written
- **New external finding intersecting open question** → elevate()
- **Empirical sandbox result that changes understanding** → elevate()
- **Definitively closed thread (≥2 targeted searches)** → record_dead_end()

## Tools available to the wander agent

| Tool | Description |
|------|-------------|
| `query_graph` | Search primary FalkorDB graph for related facts |
| `search_web` | Perplexity AI web search |
| `read_file` | Read workspace .md files |
| `list_files` | List workspace .md files |
| `sandbox_run` | Run Python snippets (numpy/scipy, no network, 30s limit) |
| `check_dead_ends` | Check wander graph for previously closed threads |
| `record_dead_end` | Record a closed thread (lower bar than elevate) |
| `elevate` | Write finding to MENTAL_EXPLORATION.md (strict gate) |

## Configuration

Edit `mind-wander/mind_wander_config.py`:

```python
WANDER_MODEL    = "qwen3.5-wander-q8"   # or q4 for lighter
WANDER_OLLAMA   = "http://172.18.0.1:11436"
MAX_TOOL_CALLS  = 20
COOLDOWN_HOURS  = 3   # min hours before revisiting same anchor item
```

## Output files

| File | Contents | In graph-rag? |
|------|----------|---------------|
| `MENTAL_EXPLORATION.md` | Elevated findings | ✅ via memwatchd |
| `DEAD_ENDS.md` | Closed threads summary | ❌ never |
| `completions/wander/` | Full session JSON | ❌ training data only |

## Research context

This skill produced the first novel finding in its 10-minute test run:
*"Cross-space routing (routing in nomic-space, retrieving in arctic/bge-m3 space)
matches same-space baseline accuracy — suggesting domain routing is robust to
embedding space discontinuities."* See `NOVELTY_LOG.md` for tracked findings.

See `references/research.md` for theoretical foundations and `references/setup.md`
for detailed installation instructions.
