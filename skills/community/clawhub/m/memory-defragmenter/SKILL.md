---
name: memory-defragmenter
description: "Defragment and optimize agent memory files by cleaning duplicates, merging similar entries, archiving stale content, and ensuring proper tiering. Use when: (1) memory files feel cluttered or bloated; (2) before or after context optimization; (3) weekly memory maintenance; (4) when explicitly asked to clean, defragment, or optimize memory."
---

# Memory Defragmenter

Clean, merge, and optimize memory files to keep them lean and effective.

## Purpose

Memory files grow over time and become:
- Bloated with duplicates
- Stale with outdated info
- Scattered across tiers
- Inconsistent in format

This skill defragments them.

## When to Run

| Trigger | Action |
|---------|--------|
| Weekly maintenance | Full defragment |
| Before context optimization | Clean first |
| After many sessions | Remove stale entries |
| Explicit request | Clean specified files |

## Defragmentation Workflow

### Step 1: Analyze Memory State

```bash
python3 scripts/analyze_memory.py
```

Reports:
- Files analyzed and sizes
- Duplicate detection
- Stale entry detection (30+ days old)
- Tier distribution
- Formatting consistency

### Step 2: Generate Defragmentation Plan

```bash
python3 scripts/defragment.py --plan
```

Creates `defragment-plan.md` with:
- Entries to merge
- Entries to archive
- Entries to delete
- Entries to promote/demote

### Step 3: Review Plan

Read the plan and approve/modify before execution.

### Step 4: Execute Defragmentation

```bash
python3 scripts/defragment.py --execute
```

Backs up original files first, then:
- Merges duplicate entries
- Archives stale content to `archive/`
- Promotes hot entries to HOT tier
- Demotes cold entries to archive
- Normalizes formatting

### Step 5: Verify

```bash
python3 scripts/verify_memory.py
```

Checks:
- All files readable
- No broken links
- Consistent formatting
- Tier limits respected

## Memory Tiers Reference

| Tier | Location | Max Size | Age Policy |
|------|----------|----------|------------|
| HOT | `memory.md`, `~/self-improving/memory.md` | ≤100 lines each | Review monthly |
| WARM | `memory/*.md`, `~/self-improving/domains/` | ≤200 lines each | Review quarterly |
| COLD | `archive/` | Unlimited | Archive at 90 days |

## Safety Rules

1. **Always backup before executing**
2. **Review plan before applying**
3. **Never delete - only archive**
4. **Keep originals for 24h after**
5. **Verify after every defragment**

## Files

- `scripts/analyze_memory.py` — Analyze memory state
- `scripts/defragment.py` — Plan and execute cleanup
- `scripts/verify_memory.py` — Verify integrity
- `references/rules.md` — Defragmentation rules and patterns
