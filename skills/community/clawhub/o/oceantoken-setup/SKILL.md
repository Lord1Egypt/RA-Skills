---
name: oceantoken-setup
description: Configure OceanToken as the model provider for Codex or Claude Code (run the agent itself on OceanToken models and balance), or connect an application's code to the OceanToken API. Use when the user asks to switch Codex or Claude Code to OceanToken, to call OceanToken models from their own app, to set up OCEANTOKEN_API_KEY, or to fix 401 / 403 / budget errors from the OceanToken API. Also for Chinese requests such as 把 Codex／Claude Code 换成 OceanToken、配置 API key、401、403、余额不足.
metadata:
  openclaw:
    homepage: https://oceantoken.ai
    envVars:
      - name: OCEANTOKEN_API_KEY
        required: false
        description: OceanToken API key, only when configuring an app or the agent's own model provider to call the OceanToken API.
---

# Setting up OceanToken as a provider

OceanToken's API is OpenAI-compatible at `https://api.oceantoken.ai/v1`
(chat completions, responses, images, videos, audio, embeddings), and Claude
models also answer the Anthropic Messages API at `https://api.oceantoken.ai`.
Auth is `Authorization: Bearer sk-...`.

Only change configuration when the user asked for this setup. Before writing
any file (agent config, settings, `.env`), show the exact change and get a
yes; never write a key anywhere without that confirmation.

## The key

1. The user creates a key at https://app.oceantoken.ai/ui/?page=api-keys (a
   credit limit per key is a good idea for agents).
2. Store it as an environment variable, never in a repository file:
   `export OCEANTOKEN_API_KEY=sk-...` in the shell profile, or a `.env` that is
   listed in `.gitignore`.
3. Check it: `curl -s https://api.oceantoken.ai/v1/models -H "Authorization: Bearer $OCEANTOKEN_API_KEY" | head -c 300`.

## Codex on OceanToken

Add a provider and a profile to `~/.codex/config.toml` so the user's default
setup stays untouched and OceanToken is one flag away. Pick the model with
`search_models` (type `chat`, capability `tools`); OpenAI GPT-5 family models
are the safe choice for Codex.

```toml
[model_providers.oceantoken]
name = "OceanToken"
base_url = "https://api.oceantoken.ai/v1"
env_key = "OCEANTOKEN_API_KEY"
wire_api = "responses"

[profiles.oceantoken]
model_provider = "oceantoken"
model = "openai/gpt-5.5"
```

Run with `codex --profile oceantoken`, and verify with
`codex exec --profile oceantoken "Reply with the single word OK"`. Show the
user the diff of `config.toml` before saving, and back the file up first.

## Claude Code on OceanToken

Claude Code talks the Anthropic Messages API, which OceanToken serves for its
Claude models. For one project, put this in `.claude/settings.local.json`
(git-ignored); for every project, in `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.oceantoken.ai",
    "ANTHROPIC_AUTH_TOKEN": "<the user's OceanToken key>",
    "ANTHROPIC_MODEL": "anthropic/claude-sonnet-5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "anthropic/claude-haiku-4.5"
  }
}
```

Use model ids exactly as `search_models` returns them. Verify with
`claude -p "Reply with the single word OK"`. Settings files hold the key in
plain text: prefer the project-local file, keep it out of git, and tell the user
where it is.

## An application calling OceanToken

OpenAI SDKs need only the base URL and key:

```python
import os
from openai import OpenAI
client = OpenAI(base_url="https://api.oceantoken.ai/v1", api_key=os.environ["OCEANTOKEN_API_KEY"])
client.chat.completions.create(model="openai/gpt-5-mini", messages=[{"role": "user", "content": "Hi"}])
```

Anthropic SDKs: `Anthropic(base_url="https://api.oceantoken.ai", api_key=...)`
with a Claude model id. Read the key from the environment; never hard-code it.

## Errors

| Status | Meaning | Fix |
|---|---|---|
| 401 | Missing, wrong, expired or deleted key | Check the header; create a new key |
| 403 | Key not allowed that model | Use a model from `GET /v1/models` |
| 400 "budget exceeded" | Balance or the key's credit limit reached | Add credit in the OceanToken console or raise the key limit |
| 404 | Unknown model | Check the id with `search_models` |
| 429 | Rate limited | Back off and retry |
| 5xx | Provider failure (not charged) | Retry once, then switch model |
