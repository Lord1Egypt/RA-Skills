---
name: loci
description: Structured memory system with domains, decay, and links for AI agents. Replaces flat MEMORY.md with a palace of organized, weighted, interconnected memories. Use when: (1) storing important context, decisions, or learnings, (2) recalling prior knowledge before answering, (3) periodic memory maintenance (heartbeat walks), (4) migrating from flat memory files. Based on Method of Loci (memory palace) — forced structure, capacity limits, association links, and natural decay.
---

# loci — Structured Memory for AI Agents

**GitHub:** https://github.com/bayhax/loci | **ClawHub:** `clawhub install loci`

## Quick Start

```bash
LOCI="node <skill_dir>/scripts/loci.mjs"

# Initialize palace (first time only)
$LOCI init

# Store a memory
$LOCI store work "Switched to Claude Opus model per user preference" --tag model --tag preference

# Recall memories
$LOCI recall "what model does the user prefer"

# Walk through palace (do this during heartbeats)
$LOCI walk

# See overview
$LOCI status
```

## Core Concepts

**Domains** — Categories that organize memories (like rooms). Each has a capacity limit.
Default domains: work, knowledge, people, tools, preferences, archive.

**Memories** — Individual pieces of context stored in a domain. Each has:
- Unique ID (e.g. `e3a7f2c1`)
- Content text
- Tags for categorization
- Links to related memories
- Weight that decays over time

**Decay** — Memories lose weight exponentially based on time since last access.
Formula: `weight = base_weight × e^(-decay_rate × days_since_access)`
Default decay rate: 0.05 (half-life ≈ 14 days).

**Links** — Bidirectional connections between related memories across any domain.

## Commands

| Command | Purpose |
|---------|---------|
| `init` | Create new palace (once) |
| `store <domain> <content>` | Add memory. Options: `--tag`, `--link` |
| `recall <query>` | Search. Options: `--domain`, `--top N` |
| `walk` | Traverse all memories, report health |
| `prune` | Remove decayed memories. Options: `--threshold`, `--dry-run` |
| `status` | Overview of all domains |
| `inspect <id>` | View memory details + links |
| `link <id1> <id2>` | Connect two memories |
| `domains` | List/add/remove domains |
| `export` | Export as markdown or JSON. Options: `--format md\|yaml` |

## Integration with Heartbeats

During heartbeat walks, run:

```bash
$LOCI walk --decay 0.05
```

This reports domain health, identifies fading memories, and updates the walk timestamp.
Periodically follow with `$LOCI prune --dry-run` to review candidates for removal.

## When to Store vs. When to Skip

**Store:** Decisions, user preferences, environment quirks, lessons learned, important people/relationships, recurring patterns.

**Skip:** Transient task details, one-off commands, things already in daily memory files.

**Rule of thumb:** If future-you would benefit from knowing this in 2 weeks, store it.

## Palace File

Default location: `~/.openclaw/workspace/loci_palace.json`
Override with `--palace PATH` on any command.
Format: JSON. Zero external dependencies — only requires Node.js (ships with OpenClaw).
