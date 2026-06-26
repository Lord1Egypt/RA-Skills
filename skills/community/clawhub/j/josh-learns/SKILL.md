---
name: "MeshMorize"
description: "🧠 Multi-layer memory system: fresh + mesh edges + fuzzy search + auto-summarize + compliance"
---

# MeshMorize 🧠

Multi-layer memory system for LLM agents. Fresh daily layer, mesh graph with edges, auto-logging, fuzzy cross-layer search, auto-summarize, and compliance checks.

## Tools

| Tool | Source |
|------|--------|
| `mem-bridge` | `memory/bridge.py` — rotation, nodes, edges, summarize |
| `auto_log` | `scripts/auto_log` — timestamped logger |
| `memory_search` | `scripts/memory_search` — multi-layer + fuzzy + edges |
| `memcheck` | `scripts/memory_check` — 10-point compliance |

## Edge Types

| Relation | Meaning |
|----------|---------|
| `triggers` | Source causes target to execute |
| `depends_on` | Source requires target |
| `related_to` | Generic connection |
| `part_of` | Source is a component of target |
| `precedes` | Source happens before target |

## Latest Fixes (v3.2.2)

- bridge.py now respects `$OPENCLAW_WORKSPACE` env var
- Edge types documented in help + SKILL.md
- All 12 compliance checks passing

https://github.com/mozz0/MeshMorize
