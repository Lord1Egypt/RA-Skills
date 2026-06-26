---
name: oo-openrouter
description: "OpenRouter (openrouter.ai). Use this skill for ANY OpenRouter request — reading, creating, and updating data. Whenever a task involves OpenRouter, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OpenRouter"
  author: "OOMOL"
  version: "1.0.1"
  services: ["openrouter"]
  icon: "https://static.oomol.com/logo/third-party/Openrouter.svg"
---

# OpenRouter

Operate **OpenRouter** through your OOMOL-connected account. This skill calls the `openrouter` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected OpenRouter. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "openrouter" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "openrouter" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_chat_completion` — Create an OpenRouter chat completion through the OpenAI-compatible `/chat/completions` endpoint. [write]
- `create_coinbase_charge` — Call OpenRouter's deprecated Coinbase charge endpoint for credits purchases. The upstream endpoint is currently deprecated and may return 410 Gone. [write]
- `create_message` — Create an OpenRouter Anthropic-format message through the `/messages` endpoint. [write]
- `get_credits` — Get the authenticated OpenRouter credit balance summary.
- `get_current_key` — Get metadata for the currently authenticated OpenRouter API key.
- `get_generation` — Get request and usage metadata for a specific OpenRouter generation.
- `get_models_count` — Get the total number of OpenRouter models, optionally filtered by output modalities.
- `list_available_models` — List the available OpenRouter models, or return the RSS feed when requested.
- `list_embedding_models` — List the embedding models available through OpenRouter.
- `list_model_endpoints` — List the currently available endpoints for a specific OpenRouter model.
- `list_providers` — List the model providers currently available through OpenRouter.
- `list_user_models` — List models filtered by the current user's OpenRouter routing preferences, privacy settings, and guardrails.
- `list_zdr_endpoints` — Preview the OpenRouter endpoints that remain available under Zero Data Retention.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OpenRouter state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — OpenRouter is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=openrouter
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- OpenRouter homepage: https://openrouter.ai
