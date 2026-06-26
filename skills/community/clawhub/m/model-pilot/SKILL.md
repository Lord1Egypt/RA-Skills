---
name: model-pilot
description: "Match task complexity to the right model. Quick heuristic check before expensive tasks — recommends cheaper models when quality won't suffer. Fetches live pricing via web_fetch. Use when: (1) starting an expensive task, (2) 'can a cheaper model do this?', (3) 'is this the right model?', (4) comparing model costs. Homepage: https://clawhub.ai/skills/model-pilot"
---

# Model Pilot v2.0

**Install:** `clawhub install model-pilot`

Stop overpaying for intelligence. Match every task to the cheapest model that delivers the quality you need.

## Language

Detect from user's message language. Default: English.

## When to Activate

- User explicitly asks about model choice or cost
- A task is starting that will be expensive (agent judgment — don't analyze trivial tasks)
- User says "save tokens", "cheaper model", "right model?"

**Do NOT activate** for trivial tasks — formatting, greetings, simple lookups.

## Quick Complexity Check

Before an expensive task, ask yourself:

```
1. What is the task? (classify)
2. What model is active?
3. Could a cheaper model handle this equally well?
4. If yes → recommend switch + estimated savings
5. If no → proceed, explain why
```

### Tier Classification

| Tier | Tasks | Model |
|------|-------|-------|
| 🟢 Routine | Formatting, Q&A, reminders, greetings, file ops | Cheapest available |
| 🟡 Intermediate | Email drafting, code review, data analysis, translations | Mid-tier |
| 🔴 Complex | Architecture decisions, creative writing, debugging complex issues | Best available |

**Signal:** Task needs <1000 output tokens + no creativity = Tier 1.

## Live Pricing

Fetch current pricing when user asks about costs:

```
web_fetch https://z.ai/pricing
web_search "openai gpt-4o pricing per token"
```

**Do NOT hardcode prices** — they change frequently. Always fetch live.

## Cost Estimation

Quick formula:
```
Estimated cost = (input_tokens / 1M × input_price) + (output_tokens / 1M × output_price)
```

Show to user:
```
Model: GLM-5-Turbo
  Input: ~5K tokens
  Output: ~2K tokens
  Estimated cost: ~$0.002
  Could use: GLM-4 (~$0.001) — saves ~50%
```

## Quick Commands

| User says | Action |
|-----------|--------|
| "right model?" | Quick complexity check |
| "model cost" | Cost estimate for current task |
| "compare models" | Live pricing comparison |
| "cheaper option" | Find cheaper model for same task |

## Guidelines for Agent

1. **Don't waste tokens analyzing cheap tasks** — check only for expensive ones
2. **Use live pricing** — never hardcode
3. **Be honest about quality** — if cheaper means worse, say so
4. **Keep it quick** — 5 seconds of thinking max
5. **Match user language**

## What This Skill Does NOT Do

- Does NOT switch models automatically — recommends only
- Does NOT persist anything
- Does NOT access credentials
- Does NOT modify any files

## More by TommoT2

- **cross-check** — Auto-detect and verify assumptions in your responses
- **context-brief** — Persistent context survival across sessions
- **setup-doctor** — Diagnose and fix OpenClaw setup issues

Install the full suite:
```bash
clawhub install model-pilot cross-check context-brief setup-doctor
```
