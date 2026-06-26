---
name: llm-cost-optimizer
description: Analyze LLM API usage logs and suggest cost optimizations. Use when you need to reduce LLM spending, compare model costs, find downgrade opportunities, detect caching wins, or compress verbose outputs. Supports OpenAI, Anthropic, Google, DeepSeek, and Meta models.
---

# LLM Cost Optimizer

Analyze LLM API usage patterns and suggest optimizations to reduce costs by 50%+.

## Quick Start

Run the analysis script against a usage log JSON file:

```bash
python3 scripts/analyze.py --input usage_logs/
```

## Input Format

Usage logs are JSON arrays of objects with:
- `timestamp` (ISO 8601)
- `model` (e.g. "gpt-4o", "claude-sonnet-4-20250514")
- `input_tokens` (int)
- `output_tokens` (int)
- `task_type` (optional: "general", "coding", "classification", "extraction", "summary", "creative", "analysis")
- `session_id` (optional)
- `cached` (optional bool)

## Optimization Strategies

1. **Downgrade**: Find simple calls (low output, basic task types) on premium models and suggest cheaper alternatives
2. **Cache**: Detect repeated prompt patterns and recommend prompt caching
3. **Compress**: Find verbose outputs and suggest prompt tuning for conciseness

## Supported Models & Pricing

All pricing is per 1M tokens (input/output). Rates are in the `PRICING` dict in `scripts/analyze.py`.

## Model Tiers

- **Premium**: gpt-4o, claude-sonnet-4, gemini-2.5-pro
- **Mid**: gpt-4.1-mini, claude-haiku-3-5, gemini-2.5-flash, deepseek-v3
- **Budget**: gpt-4.1-nano, deepseek-r1, llama-4-maverick

Downgrade suggestions map premium → mid → budget for simple tasks.
