---
name: oo-neon-ai-gateway
description: "Neon AI Gateway (neon.com). Use this skill for ANY Neon AI Gateway request — searching and reading data. Whenever a task involves Neon AI Gateway, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Neon AI Gateway"
  author: "OOMOL"
  version: "1.0.0"
  services: ["neon_ai_gateway"]
  icon: "https://static.oomol.com/logo/third-party/neon_ai_gateway.svg"
---

# Neon AI Gateway

Operate **Neon AI Gateway** through your OOMOL-connected account. This skill calls the `neon_ai_gateway` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Neon AI Gateway. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "neon_ai_gateway" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "neon_ai_gateway" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_chat_completion` — Create a chat completion through Neon AI Gateway's OpenAI-compatible `/v1/chat/completions` endpoint. One branch credential reaches Anthropic, OpenAI, Google, and open-weight models.
- `create_embedding` — Create embeddings through Neon AI Gateway's OpenAI-compatible `/v1/embeddings` endpoint.
- `create_message` — Create an Anthropic Messages API message through Neon AI Gateway (`/anthropic/v1/messages`). Use it for prompt caching and extended thinking on Claude models.
- `create_response` — Create a response through Neon AI Gateway's OpenAI Responses API endpoint (`/openai/v1/responses`). Required for `gpt-5-3-codex` and `gpt-5-5-pro`. Image generation needs streaming, which connector actions do not support, because non-streaming responses are capped at 655,360 bytes.
- `evaluate` — Answer yes/no (noul), choice, and score questions about text, JSON, or images with TypeSafe System One decision models through Neon AI Gateway (`/typesafe/v1/systemone`). Returns probabilities instead of generated text.
- `generate_content` — Generate content with a Google Gemini model through Neon AI Gateway's native Gemini endpoint (`/gemini/v1beta/models/{model}:generateContent`). Use it for Gemini-only options such as `thinkingConfig`; the chat completions action also serves Gemini models.
- `list_models` — List the Neon AI Gateway model catalog in an OpenRouter-shaped response. Each entry's `enabled` field says whether this account can call the model now.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Neon AI Gateway state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Neon AI Gateway is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/neon_ai_gateway
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Neon AI Gateway homepage: https://neon.com
- API documentation: https://neon.com/docs/ai-gateway/overview
