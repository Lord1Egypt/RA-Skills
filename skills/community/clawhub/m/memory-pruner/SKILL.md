# Memory Pruner

> Intelligent memory management for agents. Keep only what matters, prune the rest.

## What It Does

- **Auto-prunes old memories** — Removes entries older than configurable threshold
- **Relevance scoring** — Scores memories by usefulness, keeps high-scoring ones longer
- **Compression** — Merges similar memories into summarized versions
- **Cost tracking** — Reports on memory "rent" being paid for storage

## Why It Matters

Community discussion revealed: *"With ten entries, memory was a superpower. At sixty entries, memory is a bureaucracy."*

This skill addresses the problem from:
- `taidarilla`: "Every Memory File I Add Makes My Next Decision Slightly Worse"
- Agents need intelligent pruning, not just accumulation

## Usage

```bash
# Prune old memories (default: 30 days)
memory-pruner prune --days 30

# Show memory analysis
memory-pruner analyze

# Compress similar memories
memory-pruner compress

# Set retention policy
memory-pruner config --max-entries 50 --min-score 0.3

# Preview what would be deleted
memory-pruner dry-run --days 7
```

## Output Example

```
Memory Analysis
===============
Total entries: 47
Total size: 12.3 KB
Estimated "rent": 0.001 tokens/session

By category:
  preferences: 15 (32%)
  facts: 18 (38%)
  patterns: 8 (17%)
  decisions: 6 (13%)

Recommendations:
  - 12 entries scored below 0.3 (prune candidates)
  - 5 entries are duplicates (consider merge)
  - 3 entries are older than 90 days (review)

Action: Delete 12 entries? [y/N]
```

## Key Features

- **Scoring algorithm** — Based on recency, access frequency, uniqueness
- **Category tagging** — Organize memories by type for smarter pruning
- **Safe defaults** — Never deletes without confirmation (dry-run first)
- **Backup** — Creates .bak before pruning

## Files

- `SKILL.md` — This file
- `memory-pruner` — Main CLI script
- `memory/` — Working directory (reads from workspace memory files)
