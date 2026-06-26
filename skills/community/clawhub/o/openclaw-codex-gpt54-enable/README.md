# OpenClaw Codex GPT-5.4 Enable Skill

A reusable OpenClaw skill that documents a low-risk, config-layer workflow for enabling `openai-codex/gpt-5.4` without rebuilding OpenClaw.

## What this repository contains

- `SKILL.md` — the actual OpenClaw skill file
- `README.md` — English documentation
- `README.zh-CN.md` — Chinese documentation
- `LICENSE` — MIT license

## Why this skill exists

In some OpenClaw setups, `openai/gpt-5.4` is already available, while `openai-codex/gpt-5.4` is still blocked, missing, or marked as `not allowed`.

This skill turns that troubleshooting experience into a repeatable workflow:

1. Check what models are already visible
2. Patch `~/.openclaw/openclaw.json` instead of rebuilding the app
3. Add the `openai-codex` provider
4. Add the `gpt-5.4` model definition
5. Register alias + fallback entries
6. Verify with `openclaw models list`
7. Confirm the gateway truly accepts the model via `session_status`

## Key idea

Prefer a **configuration-layer patch** over editing packaged app files or recompiling:

- Lower risk
- Easier rollback
- Faster validation
- Better for real-world experimentation

## Typical use case

Use this skill when:

- `openai/gpt-5.4` already exists in OpenClaw
- `openai-codex/gpt-5.4` does not
- You want a reproducible enablement process
- You want to avoid patching the Homebrew-installed app bundle

## Quick flow

```bash
# 1) Inspect current model availability
openclaw models list --plain | grep 'gpt-5.4'

# 2) Back up config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)

# 3) Patch ~/.openclaw/openclaw.json
#    - add models.providers.openai-codex
#    - add model gpt-5.4
#    - add alias GPT54Codex
#    - add fallback openai-codex/gpt-5.4

# 4) Verify registration
openclaw models list --plain | grep 'openai-codex/gpt-5.4'
```

Then validate inside OpenClaw with:

```text
session_status(model='openai-codex/gpt-5.4')
```

## Repository audience

This repo is for:

- OpenClaw power users
- people testing new model routes
- anyone who wants to preserve model-enablement know-how as a skill

## Notes

Field names may differ slightly between OpenClaw versions. Always merge the examples into your real `~/.openclaw/openclaw.json` structure instead of blindly replacing the whole file.

## License

MIT
