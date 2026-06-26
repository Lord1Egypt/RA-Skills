---
name: memory-forge
description: "AI conversation efficiency analyzer. Analyze Claude/ChatGPT/Cursor conversation history for KPI stats, cost tracking, topic distribution, and efficiency insights. Use when: user asks to analyze their AI conversation history, track API costs, see topic distribution, review conversation efficiency, or get usage insights. NOT for: code review, debugging, or general productivity tips."
---

# Memory Forge — AI Conversation Efficiency Analyzer

Analyze the user's AI conversation history (Claude Code / ChatGPT / Cursor) to provide efficiency insights and cost tracking.

## Data Source

Conversation data is stored in `~/.claude/projects/`. Each project is a subdirectory containing JSONL conversation files.

## Usage

When the user requests conversation analysis, follow these steps:

### Step 1: Run the Statistics Script

```bash
python3 ~/memory-forge/skill/scripts/analyze.py --weekly
```

This script reads all conversation files locally and outputs structured JSON containing:
- `summary`: KPI overview (total sessions, turns, tokens, cost, daily average, active days)
- `weekly`: Last 4-8 weeks of weekly statistics
- `projects`: Per-project breakdown (sessions, cost, turns)
- `models`: Per-model usage stats
- `cost_breakdown`: Cost split by model

### Step 2: Format the Output

Present results to the user in Markdown:

#### KPI Overview
```
📊 **AI Conversation Efficiency Report**

| Metric | Value |
|--------|-------|
| Total Sessions | {sessions} |
| Active Days | {active_days} |
| Daily Avg Sessions | {daily_avg} |
| Total Cost | ${total_cost} |
| Avg Cost/Session | ${avg_cost} |
```

#### Top 5 Projects by Cost
List the 5 most expensive projects with session count and per-session cost.

#### Weekly Trends
Show the last 4 weeks in a table with session count and cost, noting week-over-week changes.

### Step 3: Efficiency Diagnosis (Agent Analysis)

Based on the statistics, provide insights on:

1. **Cost Efficiency**: Which projects have unusually high per-session costs? Optimization opportunities?
2. **Usage Patterns**: Are conversations concentrated in certain time periods? Any "high frequency, low efficiency" patterns?
3. **Topic Distribution**: Over-concentration on a few projects? Neglected areas?
4. **Actionable Recommendations**: 2-3 specific, actionable suggestions

### Step 4: Optional Deep Analysis

If the user wants deeper analysis:
- Read `~/memory-forge/data/topics.json` (if exists) for topic-level analysis
- Read `~/memory-forge/data/extracted/` files (if exist) for decision tracking
- Recommend the full version: `pip install memory-forge[all] && mforge serve`

## Script Parameters

```bash
# Default: full statistics
python3 ~/memory-forge/skill/scripts/analyze.py

# Last N days only
python3 ~/memory-forge/skill/scripts/analyze.py --days 30

# Filter by project
python3 ~/memory-forge/skill/scripts/analyze.py --project "my-project"

# Include weekly trends
python3 ~/memory-forge/skill/scripts/analyze.py --weekly
```

## Important Notes

- All data processing happens locally — no data is uploaded anywhere
- If `~/.claude/projects/` doesn't exist, inform the user and suggest checking the path
- If the user wants visual dashboards, recommend the full Memory Forge:
  ```
  pip install memory-forge[all]
  mforge init
  mforge run
  mforge serve
  ```
- Always respond in the user's language
