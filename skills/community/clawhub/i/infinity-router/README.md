# infinity-router

Unlimited free AI routing via OpenRouter.
Auto-discover, score, and configure free models with a smart fallback chain — zero downtime, zero cost.

---

## How it works

OpenRouter exposes 30+ free-tier models. Each has a rate limit.
infinity-router treats them as a pool: it picks the best, wires a fallback chain,
and rotates automatically when one goes down.

Models are filtered to chat-only (audio, image, video, and embedding models are excluded),
scored by tool/function-calling support, context length, recency, and provider trust,
then written to your OpenClaw or Claude Code config.

---

## Project structure

```
infinity-router/
├── src/
│   └── infinity_router/
│       ├── __init__.py     package version
│       ├── models.py       model registry — fetch, score, cache, rate-limit state
│       ├── probe.py        HTTP health check, latency measurement, bulk validation
│       ├── targets.py      config writers — OpenClaw, Claude Code
│       ├── cli.py          `infinity-router` CLI
│       └── daemon.py       `infinity-router-daemon` CLI
├── tests/
│   ├── __init__.py
│   └── test_models.py      unit tests (no network required)
├── install.sh              installer (handles Debian/Ubuntu venv restriction)
├── uninstall.sh            uninstaller
├── .env.example
├── pyproject.toml
├── README.md
└── SKILL.md
```

---

## Installation

### Recommended — `install.sh` (works on all Linux/macOS)

The script creates a venv, installs the package into it, then symlinks
the commands to `/usr/local/bin`. This avoids the Debian/Ubuntu
`externally-managed-environment` restriction.

```bash
chmod +x install.sh
./install.sh
```

Two commands become available globally:

```
infinity-router
infinity-router-daemon
```

To uninstall:

```bash
./uninstall.sh
```

---

### Manual — virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

### macOS / Windows (no system restriction)

```bash
pip install -e .
pipx install .    # isolated (recommended for CLI tools)
```

---

## Setup

### Single API key

```bash
# export for current session:
export OPENROUTER_API_KEY="sk-or-v1-..."

# or persist via OpenClaw:
openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
```

### Multiple API keys (recommended — avoids daily free-tier limits)

Comma-separate keys in the same variable. Infinity-Router rotates through them
during validation probes so no single key exhausts its daily quota.

```bash
openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-KEY1,sk-or-v1-KEY2,sk-or-v1-KEY3"
```

For actual inference (OpenClaw gateway), register each key as a separate auth profile
in `~/.openclaw/agents/main/agent/auth-profiles.json`:

```json
{
  "version": 1,
  "profiles": {
    "openrouter:default": {
      "type": "api_key",
      "provider": "openrouter",
      "key": "sk-or-v1-KEY1"
    },
    "openrouter:key2": {
      "type": "api_key",
      "provider": "openrouter",
      "key": "sk-or-v1-KEY2"
    },
    "openrouter:key3": {
      "type": "api_key",
      "provider": "openrouter",
      "key": "sk-or-v1-KEY3"
    }
  }
}
```

> Infinity-Router also reads keys from `auth-profiles.json` automatically,
> so you don't need to duplicate them in `openclaw.json` if they're already there.

---

## Quick start

```bash
infinity-router pick          # auto-configure best model + fallbacks
openclaw gateway restart      # apply config
```

For a safer first run (probes each candidate before writing — slower but avoids stale models):

```bash
infinity-router pick --validate
openclaw gateway restart
```

---

## Commands — `infinity-router`

### `scan` — discover and rank free models

```bash
infinity-router scan
infinity-router scan --limit 30 --refresh
```

```
  #    Model ID                                              Context   Score    Status
  ─────────────────────────────────────────────────────────────────────────────────
  1    meta-llama/llama-3.3-70b-instruct:free               128K      0.821    ● primary
  2    mistralai/mistral-small-3.1-24b-instruct:free        128K      0.714    · fallback
  3    deepseek/deepseek-r1:free                            128K      0.698
  ...
```

| Flag | Description |
|------|-------------|
| `-n / --limit N` | rows to display (default 20) |
| `-r / --refresh` | bypass cache, fetch live |
| `-t / --target` | `openclaw` \| `claude-code` |

---

### `pick` — auto-configure best model + fallbacks

```bash
infinity-router pick
infinity-router pick --validate          # probe each candidate before writing
infinity-router pick --fallbacks-only    # keep current primary, rebuild fallbacks
infinity-router pick --count 10          # 10 fallbacks instead of default 5
infinity-router pick --auth              # also add OpenRouter auth profile
```

`--validate` sends a test request to each candidate model before writing it.
Uses key rotation (1.5 s delay per key) to avoid exhausting the daily free quota.
Caps probing at 12 candidates.

---

### `use` — set a specific model

```bash
infinity-router use deepseek             # partial name match
infinity-router use llama-3.3-70b        # partial name match
infinity-router use qwen3-coder --fallbacks-only
infinity-router use deepseek --validate  # also validate fallbacks
```

---

### `bench` — latency-test top models

```bash
infinity-router bench
infinity-router bench --count 10
```

```
Benchmarking 5 models …

  meta-llama/llama-3.3-70b-instruct:free                     ✓  312 ms
  mistralai/mistral-small-3.1-24b-instruct:free               ✓  489 ms
  deepseek/deepseek-r1:free                                   ✗  rate_limit

  Ranked by latency:
    1.  meta-llama/llama-3.3-70b-instruct:free  —  312 ms
    2.  mistralai/mistral-small-3.1-24b-instruct:free  —  489 ms
```

---

### `status` — show current state

```bash
infinity-router status
```

```
Infinity-Router
──────────────────────────────────────────────────
  API key 1     sk-or-v1-…f3a2
  API key 2     sk-or-v1-…ed9f5
  API key 3     sk-or-v1-…6793

  Targets:
    OpenClaw        found  ← active
    Claude Code     not found

  Primary     openrouter/meta-llama/llama-3.3-70b-instruct:free
  Fallbacks (5):
              ↳  openrouter/free
              ↳  mistralai/mistral-small-3.1-24b-instruct:free
              …

  Cache       25 models, updated 1h 12m ago
  Cache TTL   6h   |   RL cooldown 30m
```

---

### `watch` — tail gateway log, auto-rotate on failures

```bash
infinity-router watch
infinity-router watch --verbose                        # print every matched failure line
infinity-router watch --thresh 5 --window 60           # 5 failures in 60s → rotate
infinity-router watch --cooldown 600                   # wait 10 min between rotations
infinity-router watch --notify https://your-webhook    # POST event on rotation
```

Tails `/tmp/openclaw/openclaw-YYYY-MM-DD.log` in real-time.
When failures spike above the threshold, it:
1. Marks the current model as rate-limited
2. Rotates to the next best available model
3. Rebuilds the fallback chain
4. Runs `openclaw gateway restart` automatically

Failure patterns detected:
- `FailoverError` / `Unknown model`
- `model_not_found`
- `No endpoints found` (tool use not supported)
- `free-models-per-day` / `free-models-per-min` (rate limit)

| Flag | Default | Description |
|------|---------|-------------|
| `-w / --window` | 120s | sliding window for counting failures |
| `-n / --thresh` | 3 | failures in window before rotating |
| `-c / --cooldown` | 300s | minimum gap between rotations |
| `--notify URL` | — | webhook to POST rotation events |
| `-v / --verbose` | off | print every matched failure line |
| `-t / --target` | openclaw | config target |

Run as a background service on VPS:

```bash
# Quick background run
nohup infinity-router watch &> ~/.infinity-router/watch.log &

# Or as a systemd unit (recommended)
# Create ~/.config/systemd/user/infinity-router-watch.service
```

---

### `reset` — remove model config

```bash
infinity-router reset
infinity-router reset --clear-rl    # also clear rate-limit records
```

---

## Commands — `infinity-router-daemon`

| Flag | Description |
|------|-------------|
| *(none)* | one-shot check, rotate if needed |
| `--loop / -l` | continuous monitoring (Ctrl-C to stop) |
| `--rotate / -r` | force-rotate to next best model |
| `--status / -s` | show rotation history and cooldowns |
| `--clear-rl` | clear all rate-limit records |
| `--target / -t` | `openclaw` \| `claude-code` |

```bash
infinity-router-daemon --loop     # start the watcher
infinity-router-daemon --status   # check what's been rotated
```

---

## Config targets

| Target | File | Written |
|--------|------|---------|
| `openclaw` *(default)* | `~/.openclaw/openclaw.json` | primary + fallback chain |
| `claude-code` | `~/.claude/settings.json` | primary model only |

```bash
infinity-router pick --target claude-code
```

Only the model keys are touched. Everything else in the config is preserved.

---

## Model scoring

Each model is scored 0.0–1.0 from five weighted criteria:

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Tool/function calling | 35% | required for coding agents — models that fake tool support are excluded |
| Context length | 30% | larger window = bigger codebase support |
| Recency | 20% | newer weights tend to perform better |
| Provider trust | 10% | Meta, Mistral, DeepSeek, NVIDIA, Qwen, Google, etc. |
| Other capabilities | 5% | vision, structured output, etc. |

**Non-chat models are excluded** — audio generation (Lyria), image generation (Imagen, DALL-E),
video, and embedding-only models are filtered out before scoring.

**Gemma models** are excluded from tool support scoring — they claim function calling
in the API but fail at runtime when tools are actually invoked.

`openrouter/free` is always inserted as the first fallback — it is OpenRouter's own
smart router that selects the best available model per request.

---

## API key rotation

When multiple keys are configured, Infinity-Router rotates through them during
`--validate` probing:

- Each probe request uses the next key in the pool
- If a key is rate-limited (429), the next key is tried automatically
- Delay between probes: `1.5s ÷ number_of_keys`
- Max candidates probed per run: 12

This means with 3 keys you can probe 3× as many models before hitting rate limits.

---

## Local state

All state lives under `~/.infinity-router/`:

```
~/.infinity-router/
├── model-cache.json      ranked model list  (6 h TTL)
├── rate-limits.json      per-model cooldown timestamps  (30 min)
└── daemon-state.json     rotation count and metadata
```

---

## Daily maintenance (optional)

Run once a day or when models start failing:

```bash
rm -f ~/.infinity-router/model-cache.json
infinity-router pick
openclaw gateway restart
```

---

## Tests

```bash
pip install pytest
pytest tests/
```

Tests cover scoring and filtering logic only — no network calls required.

---

## Requirements

- Python 3.10+
- `requests` (only dependency)
- Free [OpenRouter](https://openrouter.ai/keys) account

---

## License

MIT
