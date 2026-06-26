---
name: infinity-router
description: Routes AI requests across free OpenRouter models for OpenClaw and Claude Code. Auto-discovers, scores, and configures the best free model with a smart fallback chain. Use when the user mentions free AI, OpenRouter, model switching, rate limits, or wants to reduce AI costs.
---

# infinity-router

## What it does

Configures OpenClaw (or Claude Code) to use free AI models from OpenRouter.
Selects the best tool-capable model as primary, builds a ranked fallback chain so
rate limits cause zero interruption, and leaves the rest of the config untouched.

Only chat models are selected — audio, image, video, and embedding models are
automatically filtered out. Models that claim tool support but fail at runtime
(e.g. Gemma) are excluded from tool scoring.

## Prerequisites

**1. API key(s)**

```bash
# Single key
openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."

# Multiple keys (comma-separated) — recommended to avoid daily free-tier limits
openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-KEY1,sk-or-v1-KEY2,sk-or-v1-KEY3"
```

For OpenClaw inference key rotation, add each key as a separate profile in
`~/.openclaw/agents/main/agent/auth-profiles.json`:

```json
{
  "version": 1,
  "profiles": {
    "openrouter:default": { "type": "api_key", "provider": "openrouter", "key": "sk-or-v1-KEY1" },
    "openrouter:key2":    { "type": "api_key", "provider": "openrouter", "key": "sk-or-v1-KEY2" },
    "openrouter:key3":    { "type": "api_key", "provider": "openrouter", "key": "sk-or-v1-KEY3" }
  }
}
```

> Note: the file is `auth-profiles.json` (with `s`), not `auth-profile.json`.

**2. Install**

On Debian/Ubuntu servers (Python 3.12+), use the provided script:

```bash
cd /path/to/infinity-router
chmod +x install.sh
./install.sh
which infinity-router    # should return /usr/local/bin/infinity-router
```

To uninstall: `./uninstall.sh`

## Standard workflow

```bash
# 1. Configure best model + fallback chain
infinity-router pick

# 2. Apply to the running gateway
openclaw gateway restart
```

For a safer run that validates each model before writing (avoids stale/broken models):

```bash
infinity-router pick --validate
openclaw gateway restart
```

## Command reference

| Command | When to run |
|---------|-------------|
| `infinity-router pick` | Set up best free model + fallbacks (most common) |
| `infinity-router pick --validate` | Probe each candidate before writing — avoids "Unknown model" errors |
| `infinity-router pick -f` | Keep current primary, rebuild fallbacks only |
| `infinity-router pick -c 10` | Use 10 fallbacks instead of default 5 |
| `infinity-router pick --auth` | Also add OpenRouter auth profile to OpenClaw |
| `infinity-router scan` | Browse all available free models |
| `infinity-router scan -n 30` | Show all 30+ models |
| `infinity-router use deepseek` | Set a specific model (partial name OK) |
| `infinity-router use qwen3-coder -f` | Add model to fallbacks only |
| `infinity-router use deepseek --validate` | Set model and validate fallbacks |
| `infinity-router bench` | Latency-test top 5 models |
| `infinity-router bench -c 10` | Test top 10 models |
| `infinity-router status` | Show current config, all API keys, cache age |
| `infinity-router watch` | Tail gateway log, auto-rotate + restart on failures |
| `infinity-router watch --verbose` | Also print every matched failure line |
| `infinity-router watch --notify URL` | POST rotation event to webhook on each rotate |
| `infinity-router reset` | Remove model config from target |
| `infinity-router reset --clear-rl` | Also clear rate-limit cooldown records |

**Always run `openclaw gateway restart` after any command that changes config.**

## Config targets

```bash
infinity-router pick                        # default: openclaw
infinity-router pick --target claude-code   # Claude Code settings.json
```

## What gets written (OpenClaw)

Only these keys in `~/.openclaw/openclaw.json`:

- `agents.defaults.model.primary` — e.g. `openrouter/meta-llama/llama-3.3-70b-instruct:free`
- `agents.defaults.model.fallbacks` — e.g. `["openrouter/free", "mistralai/mistral-small:free", …]`
- `agents.defaults.models` — model allowlist

The first fallback is always `openrouter/free` — OpenRouter's smart router that
auto-picks the best available model for each request.

## Daemon (auto-rotation)

```bash
infinity-router-daemon            # one-shot check
infinity-router-daemon --loop     # continuous monitoring
infinity-router-daemon --rotate   # force rotate now
infinity-router-daemon --status   # rotation history
infinity-router-daemon --clear-rl # reset all cooldowns
```

## Daily maintenance

Run once a day or when models start failing:

```bash
rm -f ~/.infinity-router/model-cache.json
infinity-router pick
openclaw gateway restart
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `infinity-router: command not found` | Run `./install.sh` from the project directory |
| `OPENROUTER_API_KEY not set` | Get a free key at https://openrouter.ai/keys |
| Config not taking effect | `openclaw gateway restart`, then `/new` in Telegram |
| `Unknown model` errors in gateway log | Stale cache — `rm ~/.infinity-router/model-cache.json && infinity-router pick --validate` |
| Agent gives fake/hallucinated responses | Model doesn't support tools — run `infinity-router pick --validate` to get a real tool-capable model |
| All probes return `rate_limit` | Daily free quota exhausted — wait for UTC midnight reset, or add more API keys |
| `HTTP 429: free-models-per-day` | Add more keys comma-separated in `env.OPENROUTER_API_KEY`, or add separate profiles to `auth-profiles.json` |
| `Something went wrong` in Telegram | Run `infinity-router status` to see active model, then `openclaw gateway restart` and `/new` |
