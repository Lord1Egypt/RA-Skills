# Configuration

First non-empty value wins.

Security:

- Never add credentials yourself unless the user explicitly asks you to start interactive auth or perform non-interactive credential setup.
- If the user only asks how to add creds, instruct them to run `potaco auth add <provider>` interactively.
- Prefer encrypted stored credentials over `--api-key` or `POTACO_API_KEY`.
- Avoid `--api-key` and `POTACO_API_KEY` unless the user explicitly approves non-interactive setup.
- Never print or copy `~/.potaco/credentials.enc`, `~/.potaco/.salt`, shell history, or secret env vars.

### Provider

1. `--provider` CLI flag
2. `POTACO_PROVIDER` env var
3. `active_provider` from config file (`~/.potaco/config.yaml`)
4. Error if none set

### API key

1. `--api-key` CLI flag
2. `POTACO_API_KEY` env var
3. Credential store (`~/.potaco/credentials.enc`, decrypted)
4. Error if none found

### Model

1. `--model` CLI flag
2. `POTACO_MODEL` env var
3. `active_model` from config file

There is no provider preset model. Use `potaco models` or `potaco config set model <model>`.
Generation capability is assumed available. Edit capability is not auto-detected; configure it per model with `potaco config set model.edit true` or `potaco config set providers.<name>.models.<model>.edit true`.

### Base URL

1. `--base-url` CLI flag
2. `POTACO_BASE_URL` env var
3. `base_url` from the provider config in config file
4. Provider preset default (openai: `https://api.openai.com/v1`, fal: `https://fal.run`, vercel: `https://ai-gateway.vercel.sh/v1`)
5. Empty (custom and non-built-in provider aliases have no usable setup preset; error if not configured)

For `custom` and any non-built-in provider name, the base URL is required during setup, then persisted. Confirm remote custom or alias endpoints are trusted before saving.

### Retries

1. `--retries` CLI flag
2. `POTACO_RETRIES` env var
3. `retries` from provider config in config file
4. Default: 2

### Timeout

1. `--timeout` CLI flag (seconds as integer string, e.g. `120`)
2. `POTACO_TIMEOUT` env var (seconds as integer string)
3. `timeout` from provider config in config file (integer, in seconds)
4. Default: 120

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `POTACO_API_KEY` | Override stored API key; avoid unless explicitly approved |
| `POTACO_PROVIDER` | Override active provider |
| `POTACO_MODEL` | Override active model |
| `POTACO_BASE_URL` | Override API base URL (required for custom and non-built-in provider setup) |
| `POTACO_RETRIES` | Override retry count |
| `POTACO_TIMEOUT` | Override timeout in seconds |
| `POTACO_NON_INTERACTIVE` | Set to `1` to force non-interactive mode for agents and automated terminal execution |

`POTACO_NON_INTERACTIVE=1` equals `--non-interactive` and skips TUI flows and automatic update prompts. It is plain automation support, not a polished scripting API.

## Config File

Located at `~/.potaco/config.yaml`.

### Format (YAML)

```yaml
active_provider: openai
active_model: gpt-image-2
auto_update: true
providers:
  openai:
    model: gpt-image-2
    base_url: https://api.openai.com/v1
    models:
      gpt-image-2:
        edit: true
    retries: 3
    timeout: 120
  fal:
    model: fal-ai/flux/dev
    retries: 2
    timeout: 120
  custom:
    model: my-model
    base_url: https://api.example.com/v1
    retries: 2
    timeout: 120
```

`auto_update` defaults to enabled when omitted. `base_url` is optional for built-in provider names and required for `custom` or non-built-in aliases. `timeout` is integer seconds. `models.<id>.edit` is the user-configured edit capability for that model.

### Config commands

```sh
potaco config show
```

Shows config path, active provider/model, and per-provider model/base URL/retries/timeout.

```sh
potaco config set model gpt-image-2
potaco config set providers.vercel.model openai/gpt-image-2
potaco config set model.edit true
potaco config set providers.openai.models.gpt-image-2.edit true
potaco config set base_url https://api.example.com/v1
potaco config set retries 5
potaco config set timeout 60
potaco config set auto_update false
```

Sets values for the active provider or a named provider. Confirm custom base URLs are trusted before saving because prompts/images may be sent there.

## Credential Storage

- AES-256-GCM, key derived from hostname + username + salt using scrypt.
- Salt: `~/.potaco/.salt`; encrypted keys: `~/.potaco/credentials.enc`.
- Output/logs/dry-run redact credentials as `[REDACTED]`.
- Safest setup: user runs `potaco auth add <provider>` interactively, without `--api-key`.

## File Paths

| File | Purpose |
|------|---------|
| `~/.potaco/config.yaml` | Multi-provider config |
| `~/.potaco/.potaco.json` | Update check cache |
| `~/.potaco/credentials.enc` | Encrypted API keys |
| `~/.potaco/.salt` | Salt for key derivation |
| `~/.potaco/debug.log` | Raw error log (append-only) |

## Debug Log

`UserError` raw errors append to `~/.potaco/debug.log`:

```
2025-01-15T10:30:00Z [api] generate: http 401: invalid api key
```

Categories: `config`, `api`, `image`, `generic`. Use `--verbose` for retry/debug stderr.

## Provider Presets

Presets store only a base URL:

| Provider | Base URL |
|----------|----------|
| openai | `https://api.openai.com/v1` |
| fal | `https://fal.run` |
| vercel | `https://ai-gateway.vercel.sh/v1` |
| custom | (no preset; user-supplied) |

No preset default model exists.
