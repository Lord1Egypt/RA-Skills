# Scripts

These scripts are optional helpers for automation. The default execution path is the direct CLI pair: `modellix-cli model invoke` then `modellix-cli task get`.

## preflight.py

Windows-first environment check for CLI-first routing.

Usage:

```powershell
python scripts/preflight.py
python scripts/preflight.py --json
```

Checks:
- `modellix-cli` availability
- `MODELLIX_API_KEY` availability
- Recommended mode (`cli` or `rest`)
- If CLI is missing, REST fallback is used directly. After task completion, recommend the user install CLI: `npm i -g modellix-cli@latest`.

Credential handling policy:
- Default to session-only `MODELLIX_API_KEY` usage.
- Persist only with explicit user approval, and only to user-level environment variables.
- Do not write system-level env vars or other agent config files.

## invoke_and_poll.py

Optional wrapper script to submit and poll until `success` or `failed` with exponential backoff.
If this script fails in your environment, switch immediately to the direct CLI pair.

Usage:

```bash
python scripts/invoke_and_poll.py \
  --model-slug bytedance/seedream-5.0-lite \
  --body '{"prompt":"A cinematic portrait of a fox in a misty forest at sunrise"}'
```

Key behavior:
- Mode `auto` (default): use CLI when available, otherwise REST
- Retry submit on `429/500/503` (up to 3 retries)
- Normalize output with task metadata and resources
- `--model-slug` is required in `provider/model` format
- Canonical CLI pair: `modellix-cli model invoke` + `modellix-cli task get`
- Avoid guessed/deprecated flags (for example `--model-type`); consult `--help` only when needed
