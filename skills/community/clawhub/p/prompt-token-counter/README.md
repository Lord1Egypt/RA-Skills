# prompt-token-counter

[中文](README.zh.md)

An **OpenClaw skill** for counting tokens and estimating API costs.

## How It Works

This project provides **local token counting** without API calls:

| Approach | OpenAI | Other models |
|----------|--------|--------------|
| **Method** | tiktoken (exact) | Formula-based approximation |
| **Accuracy** | Exact | ~85–95% typical |

For non-OpenAI models, we use **provider-specific formulas** calibrated from benchmark data. When text contains CJK (Chinese/Japanese/Korean), we **blend the ratio** by CJK character ratio so that Chinese-heavy text gets fewer chars-per-token (more tokens per character).

### Benchmark: Main Models (8927 chars, English/mixed)

| Model | Chars | Tokens | 1 token ≈ chars | Status |
|-------|-------|--------|-----------------|--------|
| anthropic/claude-sonnet-4-6 | 8927 | 2763 | 3.23 | ✓ |
| anthropic/claude-sonnet-4-5 | 8927 | 2763 | 3.23 | ✓ |
| anthropic/claude-opus-4.6 | 8927 | 2763 | 3.23 | ✓ |
| openai/gpt-5.2-codex | 8927 | 2459 | 3.63 | ✓ |
| google/gemini-3.1-pro-preview | 8927 | 2627 | 3.40 | ✓ |
| z-ai/glm-5 | 8927 | 2457 | 3.63 | ✓ |
| volcengine/doubao-seed-2-0-pro | 8927 | 2702 | 3.30 | ✓ |
| moonshot/kimi-k2.5 | 8927 | 2402 | 3.72 | ✓ |
| minimax/MiniMax-M2.5 | 8927 | 2428 | 3.68 | ✓ |
| deepseek-v3.2 | 8927 | 2578 | 3.46 | ✓ |

### Benchmark: Main Models (3050 chars, Chinese-mixed 混杂中文)

| Model | Chars | Tokens | 1 token ≈ chars | Status |
|-------|-------|--------|-----------------|--------|
| anthropic/claude-sonnet-4-6 | 3050 | 1913 | 1.59 | ✓ |
| anthropic/claude-sonnet-4-5 | 3050 | 1913 | 1.59 | ✓ |
| anthropic/claude-opus-4.6 | 3050 | 1913 | 1.59 | ✓ |
| openai/gpt-5.2-codex | 3050 | 1564 | 1.95 | ✓ |
| google/gemini-3.1-pro-preview | 3050 | 1473 | 2.07 | ✓ |
| z-ai/glm-5 | 3050 | 1318 | 2.31 | ✓ |
| volcengine/doubao-seed-2-0-pro | 3050 | 1494 | 2.04 | ✓ |
| moonshot/kimi-k2.5 | 3050 | 1257 | 2.43 | ✓ |
| minimax/MiniMax-M2.5 | 3050 | 1289 | 2.37 | ✓ |
| deepseek-v3.2 | 3050 | 1361 | 2.24 | ✓ |

*Benchmark data from `scripts/examples/benchmark_token_ratio.py` (API mode).*

## What This Skill Does

When loaded, the agent can:

| Capability | Use case |
|------------|----------|
| **Count tokens** | "How many tokens in this prompt?", "Token length of X" |
| **Estimate cost** | "How much for this text on GPT-4?", "API cost for Claude" |
| **Audit OpenClaw workspace** | "How many tokens does my workspace use?", "Which memory/persona/skills consume tokens?" |
| **Compare models** | "Compare token cost across models", "Which model is cheaper?" |

### OpenClaw Token Audit

The skill helps identify token consumption of workspace components:

- **Memory & persona**: AGENTS.md, SOUL.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md, etc.
- **Skills**: Each SKILL.md under `~/.openclaw/skills/` or `workspace/skills/`

Example audit (batch mode, multiple files):
```bash
python -m scripts.cli -m gpt-4o -c AGENTS.md SOUL.md MEMORY.md
```

## When to Trigger

- User asks about token count, prompt length, API cost
- User mentions OpenClaw context size or workspace token usage
- Agent needs to audit token consumption before/after changes

## Copy and send to OpenClaw

**ClawHub (recommended, international)**
```text
Please run clawhub install prompt-token-counter to install this skill, and help me count tokens and estimate API costs.
```

**npm**
```text
Please run npm i prompt-token-counter to install this skill, and help me count tokens and estimate API costs.
```

## Quick Reference

```bash
python -m scripts.cli -m gpt-4 "Hello, world!"
python -m scripts.cli -f input.txt -m claude-3-opus -c
python -m scripts.cli -l   # list 300+ models
```

## Benchmark Script

Run `scripts/examples/benchmark_token_ratio.py` to test token ratios across models:

- **API mode** (default): Uses model API to get exact `prompt_tokens`. Set `API_KEY` and `BASE_URL` in the script.
- **Local mode** (`--local`): Uses this project's TokenCounter (no API). Good for quick comparison.

```bash
python scripts/examples/benchmark_token_ratio.py           # API mode
python scripts/examples/benchmark_token_ratio.py --local   # local approximation
```

MIT
