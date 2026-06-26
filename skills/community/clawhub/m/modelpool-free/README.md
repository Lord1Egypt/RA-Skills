# 🎱 ModelPool (Free)

**The smart free AI model manager for OpenClaw that never hits rate limits.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Compatible-green.svg)](https://openrouter.ai)

ModelPool solves the #1 pain point of using free AI models: **rate limits**. By intelligently rotating multiple API keys and auto-switching between quality-ranked free models, you get unlimited free AI coding without interruptions.

---

## ⚡ Quick Start

```bash
pip install modelpool-oc
modelpool setup
```

That's it. Enter your OpenRouter keys (free at [openrouter.ai](https://openrouter.ai)), and ModelPool handles everything else automatically.

---

## 🎯 Why ModelPool?

| Problem | ModelPool Solution |
|---------|---------------------|
| 🚫 Hit rate limits constantly | Multi-key rotation: 2 keys = 2x quota, 3 keys = 3x quota |
| 🤷 Don't know which free models are good | Auto-ranks models by context window, reasoning, ratings |
| ⏱️ Downtime when switching models | Smart fallback chain switches instantly |
| 🔧 Model/API issues break workflow | One-click repair fixes 7 common issues automatically |
| 📋 Manual key management is tedious | Built-in key manager with health checks |

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Commands Reference](#-commands-reference)
- [How It Works](#-how-it-works)
- [Comparison with FreeRide](#-comparison-with-freeride)
- [Requirements](#-requirements)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔑 Multi-Key Rotation *(Unique to ModelPool)*

Add multiple OpenRouter keys (free to register) and ModelPool distributes models across them. Each key has independent rate limits, so **2 keys = 2x free quota**.

```
Key 1: Step 3.5 Flash → Nemotron 120B → GPT-OSS 120B
Key 2: Step 3.5 Flash → Qwen3 Coder  → Hermes 405B
```

### 🔍 Auto-Discovery & Quality Ranking

ModelPool fetches all free models from OpenRouter's API and scores them by:
- Context window size (bigger = better)
- Reasoning capability
- Known quality benchmarks

You always get the **best free models available**, automatically.

### 🔗 Smart Fallback Chain

When one model hits a rate limit, ModelPool instantly switches to the next model on a different key. The chain alternates between keys for maximum uptime:

```
Request → Key1/Model A → ✅ Success
Request → Key1/Model A → ❌ Rate Limited
         → Key2/Model B → ✅ Success (fresh key, fresh quota)
```

### 🔧 One-Click Repair

`modelpool repair` runs 7 automated diagnostic and fix steps:

1. Check Gateway process
2. Test each model API connectivity
3. Fix config with `openclaw doctor`
4. Clean stuck sessions
5. Rebuild fallback chain (skip dead models)
6. Free memory and clean old logs
7. Full Gateway restart

---

## 📦 Installation

### Option A: pip install

```bash
pip install modelpool-oc
```

### Option B: Clone and install

```bash
git clone https://github.com/meilihulee/modelpool.git
cd modelpool
pip install -e .
```

### Option C: Just run the script

```bash
git clone https://github.com/meilihulee/modelpool.git
python modelpool/scripts/freeswitch.py setup
```

---

## 🚀 Usage

### First-Time Setup

```bash
$ modelpool setup

🦞 ModelPool Setup
========================================

  Enter your OpenRouter API Key(s)
  (Get one free at https://openrouter.ai)

  Key 1 (required): sk-or-v1-abc123...
  Key 2 (optional, Enter to skip): sk-or-v1-def456...

  🔑 Validating keys...
    Key 1: ✅ 247 models accessible
    Key 2: ✅ 247 models accessible

  ✅ 2 valid key(s) saved

  🔍 Fetching free models from OpenRouter...
  ✅ Found 28 free models

  ⚙️  Configuring providers...
    ✅ openrouter: step-3.5-flash:free, nemotron-3-super-120b-a12b:free, gpt-oss-120b:free
    ✅ openrouter2: step-3.5-flash:free, qwen3-coder:free, hermes-3-llama-3.1-405b:free

  🔗 Building fallback chain...
    Primary: openrouter/stepfun/step-3.5-flash:free
    Fallbacks: 5

  🔄 Restarting OpenClaw...

========================================
🎉 Done! 28 free models, 2 keys, 2x quota
========================================
```

### Check Status

```bash
$ modelpool status

  🦞 ModelPool Status
  ────────────────────────────────────────
  Keys:      2
  Providers: 2
  Primary:   openrouter/stepfun/step-3.5-flash:free
  Fallbacks: 5
  ────────────────────────────────────────

  Fallback chain:
    1. openrouter2/stepfun/step-3.5-flash:free
    2. openrouter/nvidia/nemotron-3-super-120b-a12b:free
    3. openrouter2/qwen/qwen3-coder:free
    4. openrouter/openai/gpt-oss-120b:free
    5. openrouter2/nousresearch/hermes-3-llama-3.1-405b:free

  Gateway: ✅ running
```

### Browse Free Models

```bash
$ modelpool list

  📋 28 free models available:

  Rank  Score  Model ID                                          Context
  ───── ────── ────────────────────────────────────────────────── ──────────
  1     75     stepfun/step-3.5-flash:free                        256k
  2     75     qwen/qwen3-coder:free                              262k
  3     45     nvidia/nemotron-3-super-120b-a12b:free             262k
  4     45     openai/gpt-oss-120b:free                           131k
  5     45     meta-llama/llama-3.3-70b-instruct:free             128k
  ...
```

### Fix Issues

```bash
$ modelpool repair

🔧 ModelPool Repair v1.0
========================================

📋 [1/7] Diagnostics...
  ✅ Gateway port 18789 listening
  ✅ Config file valid
  ✅ Memory OK: 417MB free
  ✅ Disk OK: 40%

📋 [2/7] Testing model API connectivity...
  ✅ openrouter/stepfun/step-3.5-flash:free
  ✅ openrouter2/qwen/qwen3-coder:free
  ❌ groq/llama-3.3-70b — HTTP 403 (auto-skipped)

📋 [3/7] Fixing config... ✅
📋 [4/7] Cleaning stuck sessions... ✅
📋 [5/7] Rebuilding fallback chain... ✅
📋 [6/7] Cleaning resources... ✅
📋 [7/7] Restarting OpenClaw... ✅

========================================
🎉 Repair complete!
========================================
```

---

## 📖 Commands Reference

| Command | Description |
|---------|-------------|
| `modelpool setup` | **Interactive first-time setup** — the one command you need |
| `modelpool auto` | Auto-reconfigure using existing keys (non-interactive) |
| `modelpool list` | Show all available free models with quality scores |
| `modelpool switch <model>` | Manually switch primary model |
| `modelpool status` | Show current config, keys, and fallback chain |
| `modelpool repair` | One-click diagnose and fix all issues |
| `modelpool keys add <key>` | Add another OpenRouter key |
| `modelpool keys list` | Show all configured keys (masked) |
| `modelpool refresh` | Force refresh model cache from API |

---

## ⚙️ How It Works

### The Rotation Algorithm

1. **Discover**: Fetch all models from OpenRouter, filter free ones (price = $0)
2. **Score**: Rank by context window + reasoning capability + known quality
3. **Distribute**: Spread top models across keys in interleaved pattern
4. **Chain**: Build fallback: Key1/ModelA → Key2/ModelB → Key1/ModelC → ...
5. **Configure**: Write to OpenClaw config, restart gateway

When a request fails (rate limit, timeout, error), OpenClaw's built-in fallback walks down the chain. Since adjacent models use different keys, the next attempt has a fresh rate limit quota.

### Why Interleaved?

```
❌ Bad:  Key1/A → Key1/B → Key1/C → Key2/D → Key2/E → Key2/F
         (Key1 exhausted before Key2 even starts)

✅ Good: Key1/A → Key2/B → Key1/C → Key2/D → Key1/E → Key2/F
         (Load balanced, both keys share the work)
```

---

## 🆚 Comparison with FreeRide

| Feature | ModelPool | FreeRide |
|---------|:----------:|:--------:|
| Auto-discover free models | ✅ | ✅ |
| Quality scoring & ranking | ✅ | ✅ |
| **Multi-key rotation** | ✅ 2x-10x quota | ❌ |
| **One-click repair** | ✅ 7-step auto-fix | ❌ |
| **API connectivity test** | ✅ | ❌ |
| **Dead model auto-skip** | ✅ | ❌ |
| Key management (add/list) | ✅ | ❌ |
| Key validation on input | ✅ | ❌ |
| Config backup before write | ✅ | ❌ |
| Session cleanup | ✅ | ❌ |
| Memory/disk cleanup | ✅ | ❌ |

---

## 📋 Requirements

- **Python** 3.8+
- **OpenClaw** installed ([install guide](https://openclaw.ai))
- **At least 1 OpenRouter API key** — free at [openrouter.ai](https://openrouter.ai)
- No external Python dependencies (stdlib only)

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

### Ideas for contributions:
- Support for additional free API providers (Groq, Together, etc.)
- Web dashboard for monitoring model usage
- Usage analytics and quota tracking
- Automated key health monitoring

---

## 📄 License

MIT — use it however you want.

---

## 🙏 Acknowledgments

- [OpenClaw](https://openclaw.ai) — The AI coding agent that makes this useful
- [OpenRouter](https://openrouter.ai) — Free access to quality AI models
- Inspired by [FreeRide](https://clawhub.ai/Shaivpidadi/free-ride)

---

**⭐ If ModelPool saves you money, give it a star!**
