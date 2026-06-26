---
name: modelpool-free
description: "ModelPool (Free) — Free AI model manager for OpenClaw. One command to auto-discover free models, configure multi-key rotation for multiplied free quota, build smart fallback chains, and one-click repair model issues. v1.0.1: Fixed security patterns (removed shell=True, killall, /proc writes). Prepare your OpenRouter API key(s) before install (free at openrouter.ai) and say goodbye to model anxiety forever."
license: MIT
---

# 🎱 ModelPool (Free) — Free AI Model Manager for OpenClaw

**One command. Unlimited free AI. No more rate limits.**

Prepare your OpenRouter API key(s) before install (free at [openrouter.ai](https://openrouter.ai)), then:

```bash
modelpool setup
```

ModelPool will auto-discover the best free models, configure multi-key rotation, and build a smart fallback chain. You'll never hit a rate limit again.

## Commands

| Command | Description |
|---------|-------------|
| `modelpool setup` | **The one command you need** — interactive setup, enter keys, everything auto-configured |
| `modelpool auto` | Auto-reconfigure with existing keys (non-interactive) |
| `modelpool list` | Browse all free models ranked by quality score |
| `modelpool switch <model>` | Manually switch primary model |
| `modelpool status` | Show current config, keys, and fallback chain |
| `modelpool repair` | **One-click fix** — diagnoses and repairs 7 common issues automatically |
| `modelpool keys add <key>` | Add another OpenRouter key (more keys = more quota) |
| `modelpool keys list` | Show all configured keys |
| `modelpool refresh` | Force refresh model cache from API |

## How It Works

### Multi-Key Rotation
Each OpenRouter key has independent rate limits. ModelPool distributes models across keys:
- Key1: Model A, Model C, Model E
- Key2: Model B, Model D, Model F

When Key1 hits rate limit → auto-switch to Key2 → back to Key1 when cooldown ends.

**2 keys = 2x quota. 3 keys = 3x quota. Simple math.**

### Smart Fallback Chain
Models ranked by quality (context window × reasoning × benchmarks). Fallback alternates between keys for maximum uptime:

```
Request → Key1/StepFlash → ✅
Request → Key1/StepFlash → ❌ Rate Limited
         → Key2/StepFlash → ✅ (fresh key!)
         → Key1/Nemotron  → ✅ (different model, same key)
```

### One-Click Repair (`modelpool repair`)
7-step auto-fix:
1. Check Gateway process
2. Test each model API connectivity
3. Fix config (`openclaw doctor`)
4. Clean stuck sessions
5. Rebuild fallback chain (skip dead models)
6. Free memory & clean logs
7. Full restart

## Getting Started

1. Get free API key(s) at [openrouter.ai](https://openrouter.ai) (no credit card needed)
2. Run `modelpool setup`
3. Enter your key(s)
4. Done. Go code.

## Requirements

- OpenClaw installed
- Python 3.8+
- At least 1 OpenRouter API key (free)
