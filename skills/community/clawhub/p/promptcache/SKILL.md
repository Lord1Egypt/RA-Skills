---
name: promptcache
description: Estimate the cost savings from caching frequently-used prompts across AI models.
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins: ["promptcache"]
    install:
      - id: skill-install
        kind: skill
        label: "Prompt Cache skill is installed — type /promptcache in any chat"
---

# promptcache — LoomLens Advisor

## What It Does

Estimates the cost savings from caching frequently-used prompts. Compares the cost of re-sending full context every call vs. cached prompt mode across all major models.

## When to Use

- When you run the same system prompt repeatedly
- Before enabling prompt caching on a production pipeline
- When evaluating cost savings from prompt template reuse

## Syntax

```
/promptcache "You are an expert radiologist..." --calls-per-day 50
/promptcache "Summarize this in 3 bullets" --model openai/gpt-4o-mini
```

## Free Tier

**3 analyses/day free** with any Signalloom API key.

Get your free key: https://signalloomai.com/signup
