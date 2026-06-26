---
name: nvidia-model-config
description: Add the NVIDIA provider to OpenClaw with SecretRef apiKey (no plaintext in openclaw.json). Documents shell vs systemd gateway env so the key actually resolves. Includes Mixtral, Kimi, Nemotron Super, Nemotron Ultra, and MiniMax M2.5 model entries.
---

# NVIDIA Model Config Skill

## Overview

This skill packages three reusable pieces:

1. **A script** (`scripts/merge_nvidia_config.py`) that inserts the NVIDIA provider block into any `openclaw.json` file and configures `apiKey` as a SecretRef by default.
2. **Model entries** for Mixtral, Moonshot Kimi, Kimi K2.5, Nemotron Super (1M ctx), Llama 3.1 Nemotron Ultra 253B (128K ctx), and MiniMax M2.5 (204.8K ctx) — delete extras or add more from `openclaw models list --provider nvidia --all`.
3. **Instructions** for backups, secrets, and **where** `NVIDIA_API_KEY` must be set so the gateway can resolve it (this is not only `openclaw.json`).

Use the skill whenever you want to replicate the NVIDIA `models.providers.nvidia` entry without guessing which keys or nested objects to copy.

## Quick start

1. Copy or download this skill (e.g., `rsync -av skills/nvidia-model-config /path/to/other/workspace/skills/`).
2. Obtain your NVIDIA API key and **keep it secret** (do not commit it).
3. Run the script from the target workspace:

```bash
python skills/nvidia-model-config/scripts/merge_nvidia_config.py \
  --config openclaw.json --key "YOUR_KEY" --setup-env ~/.config/openclaw/gateway.env --setup-systemd --backup
```

- `--config` defaults to `openclaw.json` in the current directory.
- `--key` provides the API key (alternatively, set `NVIDIA_API_KEY` in your shell).
- `--setup-env` writes the key to a dedicated environment file (e.g., `~/.config/openclaw/gateway.env`).
- `--setup-systemd` creates a systemd user override to load the environment file for the gateway.
- `--backup` saves the original file as `openclaw.json.bak` before overwriting.
- By default, the script writes `models.providers.nvidia.apiKey` as:
  - `{"source":"env","provider":"default","id":"NVIDIA_API_KEY"}`

### Manual Environment Setup

If you prefer not to use `--setup-systemd`, you must set your key in the **runtime environment** where the OpenClaw **gateway** runs.

**Interactive shell / CLI only** (e.g. testing `openclaw` in a terminal):

```bash
export NVIDIA_API_KEY="$YOUR_KEY"
```

**Gateway under systemd (typical on Linux)** — the service does **not** read `~/.bashrc`. Put the key in a file the unit loads, for example:

- File: `~/.config/openclaw/gateway.env` (mode `600`):

```bash
NVIDIA_API_KEY=your_key_here
```

- User unit drop-in `~/.config/systemd/user/openclaw-gateway.service.d/override.conf`:

```ini
[Service]
Environment=NVIDIA_API_KEY=
EnvironmentFile=-/home/YOUR_USER/.config/openclaw/gateway.env
```

The empty `Environment=NVIDIA_API_KEY=` clears any inherited value so `EnvironmentFile` is the single source of truth. Then:

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

You can also keep a personal `~/.config/openclaw/secrets.env` and `source` it from `~/.bashrc` for CLI-only use; that does **not** replace the gateway env above.

If you want to preview the changes before writing, add `--dry-run` and capture the printed JSON.

## What the script does

1. Removes legacy plaintext copies of `NVIDIA_API_KEY` from config (`env.vars.*` and `env.*`) when present.
2. Creates or updates the `models.providers.nvidia` block with bundled NVIDIA models (Nemotron Super 1M ctx, Nemotron Ultra 253B ~128K ctx, MiniMax M2.5 ~204.8K ctx, plus Mixtral/Kimi entries). NVIDIA may return `403` if your key is not entitled to a model; pick a model that matches your account and catalog.
3. Keeps the `api`/`baseUrl` values in sync with NVIDIA’s `integrate.api.nvidia.com` endpoint.
4. Supports an explicit legacy mode when needed:

```bash
NVIDIA_API_KEY="$YOUR_KEY" \
  python skills/nvidia-model-config/scripts/merge_nvidia_config.py \
  --config openclaw.json --inline-key
```

Use `--inline-key` only for short-lived local tests.

## Optional adjustments

- Set default model with `openclaw models set nvidia/<model-id>` (full id is `nvidia/` + provider model id, e.g. `nvidia/nvidia/nemotron-3-super-120b-a12b` when the provider entry id is `nvidia/nemotron-3-super-120b-a12b`).
- If the target install manages agent defaults manually, add fallback entries under `agents.defaults.model.fallbacks` so clients can recover if the primary model fails.
- Double-check other agents’ `models` lists if they need aliases.

## Distribution tips

1. Bundle this skill directory and any instructions or scripts you use into a `.zip`/`.skill` file to share with teammates.
2. In your documentation, point operators to this SKILL so Codex can reload it and the script automatically when they ask to “add NVIDIA models.”
3. Keep real API keys outside of Git. Use environment variables or SecretManagers and rely on the script to merge them at runtime.
