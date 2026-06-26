---
name: MemCore 记忆核心
description: >
  v2.1.0 (WAL+VFM enhanced). Five-tier adaptive memory system with WAL indexing, Working Buffer search, and VFM scoring. 为 OpenClaw 打造的五层自适应记忆检索系统，四层自进化记忆模型（L1轨迹→L2模式→L3世界模型→技能结晶），反馈驱动的价值评分，自动维护与健康诊断。适用场景：(1) 带降级保障的记忆搜索，(2) 带历史故障诊断的健康检查，(3) 每日散会流程自动模式归纳，(4) 生成启动简报替代全量MEMORY.md注入节省92% token，(5) 跨领域模式关联检查防止重复犯错。
  
  Five-tier adaptive memory retrieval, self-evolving four-layer memory model (L1 trace → L2 pattern → L3 world model → Skill crystallization), feedback-driven value scoring, auto-maintenance, and health diagnostics for OpenClaw agents. Use when: (1) Searching memory with fallback guarantees, (2) Running health checks with historical fault diagnosis, (3) Daily 散会流程 with auto pattern induction, (4) Generating startup brief to replace full MEMORY.md injection, (5) Checking cross-domain pattern associations to prevent recurring failures.
---

# MemCore 记忆核心

为 OpenClaw 打造的五层自适应记忆系统，自进化。替代全量 MEMORY.md 注入 — 节省 92% token。

Five-tier adaptive memory system with self-evolution for OpenClaw. Drop-in replacement for full MEMORY.md injection — 92% token savings.

## v2.1.0 (proactive-agent enhanced) ⭐

- **WAL Protocol**: `cmd_index` now parses SESSION-STATE.md as high-priority traces
- **Working Buffer**: SESSION-STATE.md + working-buffer.md searchable in World Model tier
- **VFM Scoring**: 4-dimension trace evaluation (frequency, failure reduction, user burden, self cost)
- **New command**: `python3 scripts/memcore/cli.py vfm` — VFM score analysis

## Quick Commands

```bash
# Startup: generate brief (≤500 tokens, replaces full MEMORY.md)
python3 scripts/memcore/cli.py brief

# Search: 5-tier adaptive fallback
python3 scripts/memcore/cli.py search "<query>" -n 5

# Daily maintenance (index new logs → induce patterns → decay → refresh brief)
python3 scripts/memcore/cli.py run-all

# VFM score analysis
python3 scripts/memcore/cli.py vfm

# Stats overview
python3 scripts/memcore/cli.py stats

# Feedback: log whether retrieved memory was useful
python3 scripts/memcore/cli.py feedback-log <trace_id> used|skipped|good|bad
```

## Startup Integration

On each session start, replace full MEMORY.md loading with:

```
1. Read SOUL.md → USER.md → MEMORY_BRIEF.md (auto-generated) → .anatomy.md → yesterday+today memory
2. MEMORY.md loaded on-demand only via: python3 scripts/memcore/cli.py search "<keywords>"
```

The brief generator picks top 5 active patterns, top 3 recent lessons, and current taskboard items — all under 500 tokens.

## 散会 Integration

Add step 3 to 散会 flow:

```bash
python3 scripts/memcore/cli.py index && \
python3 scripts/memcore/cli.py induce && \
python3 scripts/memcore/cli.py feedback
```

This auto-indexes today's log, induces new patterns, and decays stale traces.

## Health Check Integration

When running daily health checks (09:00), append MemCore diagnostic:

```bash
# Get system stats
python3 scripts/memcore/cli.py stats

# If anomalies found, search historical similar faults
python3 scripts/memcore/cli.py search "<anomaly keywords>" -n 3
```

**Safety rule**: Report only. Never auto-fix. Let human decide.

## Search & Feedback Flow

After every `memory_search` call, log feedback:

```bash
# If the retrieved memory was helpful:
python3 scripts/memcore/cli.py feedback-log <trace_id> used

# If irrelevant:
python3 scripts/memcore/cli.py feedback-log <trace_id> skipped
```

This trains the retrieval system — high-value traces rise, stale ones decay.

## Cron Setup

Two 12-hour maintenance jobs (systemEvent, main session, wakeMode: next-heartbeat):

| Time (CST) | Cron expression | Action |
|-----------|----------------|--------|
| 04:00 | `0 4 * * *` | index + induce + feedback + brief |
| 16:00 | `0 16 * * *` | same |

These are SQLite-only, no model calls, near-zero resource cost.

## Rollback

```bash
cp memcore_backup_<date>/AGENTS.md ~/.openclaw/workspace/
cp memcore_backup_<date>/MEMORY.md ~/.openclaw/workspace/
```

Original MEMORY.md is never modified. All MemCore data lives in separate SQLite files under `~/.openclaw/`.

## Detailed Reference

- **Architecture**: See [references/architecture.md](references/architecture.md) for L1-L4 model, 5-tier retrieval details, file structure, and CLI reference.
- **EXO1 Upgrade**: See [references/upgrade-guide.md](references/upgrade-guide.md) for Syncthing-based deployment to EXO1.
