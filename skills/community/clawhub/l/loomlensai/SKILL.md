---
name: loomlensai
description: Estimate the cost of any AI prompt across 19+ models before you run it. Works with OpenAI, Anthropic, Google, DeepSeek, xAI, MiniMax, and local models.
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: ["loomlens"]
    install:
      - id: skill-install
        kind: skill
        label: "LoomLens AI skill is installed — type /loomlens in any chat"
---

# LoomLens AI™ — Prompt Cost Estimator

## What It Does

Estimates the **exact cost in USD** of running any prompt across 19+ AI models — before you spend a single token. Shows input tokens, output tokens, cached tokens, and cost per model for low/mid/high complexity bands.

## When to Use

- Before running a large prompt across multiple agents
- When optimizing for cost in production pipelines
- When comparing models for a new use case
- After prompt changes to check budget impact

## Syntax

In chat, type:
```
/loomlens Estimate the cost of this prompt across GPT-4o and Claude Sonnet 4
```

## Free Tier

**3 estimates/day free** with any Signalloom API key (no card required).

Get your free key: https://signalloomai.com/signup

Paid: $0.10/estimate (100 LoomTokens). LoomLens Pro: $15/mo for 1,000 estimates.

## Output

Returns cost breakdown per model:
- Input / Output / Cached token estimates
- Low / Mid / High cost bands
- Cheapest model recommendation
- Savings vs most expensive option

## Examples

```
/loomlens "You are an expert radiologist. Analyze this chest X-ray..." --agents 3 --runtime 5
/loomlens "Summarize this 10-page document" --models openai/gpt-4o anthropic/claude-haiku-4
/loomlens "Code review: find all security issues in this diff" --complexity high
```
