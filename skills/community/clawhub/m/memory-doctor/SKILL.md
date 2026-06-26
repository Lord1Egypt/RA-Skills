---
name: memory-doctor
description: Keep an LLM agent's long-term memory healthy — the cure for context rot. Use when a memory store exists and the user wants to check or tidy it ("记忆体检", "整理记忆", "memory health", "memory cleanup", "dedup memory", "fix MEMORY.md index"), or whenever memory has grown long, contradictory, or its index drifted. Runs a read-only health report and safe, reversible repairs. Supports the Claude Code auto-memory format (frontmatter + [[links]] + MEMORY.md) and the mneme format (.mneme cells). Zero dependencies, zero LLM in v0.1.
version: 0.1.2
---

# memory-doctor — keep agent memory healthy

Memory skills *write* memory; almost none *maintain* it. Over time a store grows long,
contradicts itself, sprouts dead links, and its index drifts — the agent then burns tokens
parsing stale history instead of acting. That is **context rot**. This skill governs an
*existing* store; it does not produce memory.

> Producers write, memory-doctor keeps it alive. Complements memory skills, doesn't replace them.
> Source & issues: <https://github.com/casperkwok/memory-doctor>

## When to use
- A memory store exists (a `MEMORY.md` + `*.md` notes, or a `*.mneme` file) and the user wants
  to check or clean it: "记忆体检 / 整理记忆 / memory health / cleanup / dedup / fix the index".
- Memory has clearly grown long, repetitive, or the index no longer matches the files.

## How to run (zero deps, Python ≥ 3.9)
```bash
# read-only — safe anytime; print the health card first
python scripts/curate.py report --dir <memory-dir>

# auto-memory only: preview then apply the index reconciliation (snapshots first)
python scripts/curate.py lint --dir <memory-dir>
python scripts/curate.py lint --dir <memory-dir> --fix

# revert the last write
python scripts/curate.py undo --dir <memory-dir>
```
The format is auto-detected (`*.mneme` present → mneme, else auto-memory); override with
`--format auto-memory|mneme`.

## What the report checks
- **dead links**, **stale** notes, **oversized** files, lexical **duplicate candidates**,
  and a **freshness** score (per-type exponential decay).
- auto-memory: **index drift** (MEMORY.md vs files) and **orphans** (no inbound link, unindexed).
- mneme: **history** cells (superseded/retired/proposed) excluded from active health, and
  **supersede back-link symmetry**; freshness uses each cell's `seen` date.

## What it fixes (v0.1 — deterministic & reversible only)
- **Index reconciliation** (auto-memory): add missing `MEMORY.md` entries, drop dangling ones,
  preserving your hand-written hooks. A full-directory snapshot is taken first; `undo` reverts.
- mneme's spine is *derived*, so there is no index to reconcile — use `report`.

Semantic fixes that need a model — true duplicate **merge**, contradiction **reconcile**,
oversized **compaction** — are *flagged* in v0.1 and *resolved* in v0.2 (no embeddings;
manual-apply, snapshot-backed). Never auto-edit memory content on the user's behalf without
confirmation.

## Safety
Every write snapshots the whole directory to `.memory-doctor/snapshots/<ts>/` and logs to
`.memory-doctor/changelog.md`; `undo` restores it. v0.1 only ever rewrites the index file.

## Optional: a read-only health nudge
`hooks/health_nudge.py` (in the repo) can be wired to a Claude Code `SessionStart` hook to print
a one-line nudge when health drops. It is read-only and never edits anything. Opt-in.
