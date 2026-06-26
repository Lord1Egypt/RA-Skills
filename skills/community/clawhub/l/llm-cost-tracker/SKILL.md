---
name: api-cost-tracker
description: Track, analyze, and optimize LLM API spending across providers (OpenAI, Anthropic, Google, DeepSeek, etc.). Use when the user asks about API costs, token usage, billing, budget alerts, cost optimization, or wants to monitor how much their OpenClaw agent is spending. Supports daily/weekly/monthly breakdowns, per-model cost analysis, budget threshold alerts, and cost reduction recommendations.
---

# API Cost Tracker

Monitor and optimize your LLM API spending directly from your agent.

## Quick Start

Run cost analysis:
```bash
python3 scripts/cost_tracker.py --summary
```

## Commands

### Check Current Spend
```bash
python3 scripts/cost_tracker.py --provider openai --period today
python3 scripts/cost_tracker.py --provider anthropic --period week
python3 scripts/cost_tracker.py --all --period month
```

### Set Budget Alert
```bash
python3 scripts/cost_tracker.py --set-budget 100 --period month --alert telegram
```

### Cost Breakdown by Model
```bash
python3 scripts/cost_tracker.py --breakdown model --period week
```

### Optimization Recommendations
```bash
python3 scripts/cost_tracker.py --optimize
```

This analyzes usage patterns and recommends:
- Model downgrades for simple tasks (e.g., use Haiku instead of Opus for classification)
- Caching opportunities (repeated similar prompts)
- Batch processing windows (off-peak pricing where available)
- Context window optimization (trim unnecessary context)

## Supported Providers

| Provider | Method | Setup |
|----------|--------|-------|
| OpenAI | Usage API | `OPENAI_API_KEY` env var |
| Anthropic | Usage API | `ANTHROPIC_API_KEY` env var |
| Google AI | Billing API | `GOOGLE_API_KEY` env var |
| DeepSeek | Usage API | `DEEPSEEK_API_KEY` env var |

## Budget Alerts

Configure in `~/.openclaw/cost-tracker.json`:
```json
{
  "budgets": {
    "daily": 10,
    "weekly": 50,
    "monthly": 200
  },
  "alertChannels": ["telegram", "discord"],
  "alertThresholds": [50, 75, 90, 100]
}
```

Alerts fire at each threshold percentage. At 100%, optionally pause non-critical agent tasks.

## Output Format

Reports generate as markdown tables suitable for any messaging surface:
```
Provider    | Model              | Tokens    | Cost
------------|--------------------|-----------|---------
Anthropic   | claude-opus-4-6   | 2.1M      | $63.00
Anthropic   | claude-sonnet-4-6 | 5.4M      | $16.20
OpenAI      | gpt-4o            | 1.8M      | $9.00
            | TOTAL              |           | $88.20
```

## Advanced: Cost Optimization Patterns

See `references/optimization-guide.md` for detailed strategies on reducing API spend by 30-60% without sacrificing quality.
