# IMINI ImageGen Configuration

This skill reads credentials from local environment variables. Do not store real keys inside the skill directory.

## Required Variable

```bash
export IMINI_IMAGE_API_KEY="your_api_key"
```

If you install this skill through OpenClaw or ClawHub, declare the same env there as well so the registry metadata matches runtime behavior.

Example OpenClaw skill config:

```json
{
  "skills": {
    "entries": {
      "imini-imagegen": {
        "enabled": true,
        "env": {
          "IMINI_IMAGE_API_KEY": "your_real_key",
          "IMINI_IMAGE_API_BASE_URL": "https://openapi.imini.ai/imini/router"
        }
      }
    }
  }
}
```

## Optional Variables

```bash
export IMINI_IMAGE_API_BASE_URL="https://openapi.imini.ai/imini/router"
export IMINI_IMAGE_TIMEOUT="300"
export IMINI_IMAGE_POLL_INTERVAL="2"
```

## Recommended Setup

Add the exports to your shell profile:

- `~/.zshrc` for `zsh`
- `~/.bashrc` or `~/.bash_profile` for `bash`

Example:

```bash
export IMINI_IMAGE_API_KEY="your_api_key"
export IMINI_IMAGE_API_BASE_URL="https://openapi.imini.ai/imini/router"
```

Reload the shell after editing:

```bash
source ~/.zshrc
```

## Verify Configuration

Check that the key is present:

```bash
python3 - <<'PY'
import os
print("IMINI_IMAGE_API_KEY set:", bool(os.getenv("IMINI_IMAGE_API_KEY")))
PY
```

Do not print the full key to the terminal.

## Switching Keys

When using different accounts or machines:

- update the local environment variable
- start a new Codex session if needed
- avoid sharing shell files that contain real production keys
