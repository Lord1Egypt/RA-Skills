---
name: oo-litellm
description: "LiteLLM (litellm.ai). Use this skill for ANY LiteLLM request — searching and reading data. Whenever a task involves LiteLLM, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "LiteLLM"
  author: "OOMOL"
  version: "1.0.2"
  services: ["litellm"]
  icon: "https://static.oomol.com/logo/third-party/litellm.png"
---

# LiteLLM

Operate **LiteLLM** through your OOMOL-connected account. This skill calls the `litellm` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected LiteLLM. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "litellm" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "litellm" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_chat_completion` — Create a chat completion through the LiteLLM proxy's OpenAI-compatible `/v1/chat/completions` endpoint. LiteLLM routes the request to whichever upstream provider serves the model, with its load balancing, fallbacks, and budget checks applied.
- `create_embedding` — Create embeddings through the LiteLLM proxy's OpenAI-compatible `/v1/embeddings` endpoint.
- `create_message` — Create an Anthropic-format message through the LiteLLM proxy's `/v1/messages` endpoint, for any model the proxy serves.
- `get_key_info` — Read the spend, remaining budget, rate limits, and allowed models of the LiteLLM virtual key used by this connection. The proxy master key has no stored record, so this action needs a virtual key.
- `get_model_info` — Read the context window, output limit, per-token pricing, and capabilities LiteLLM reports for each model deployment, so an agent can pick a model before calling it.
- `list_models` — List the model names this LiteLLM key can call.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change LiteLLM state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — LiteLLM is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/litellm
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- LiteLLM homepage: https://www.litellm.ai
- API documentation: https://docs.litellm.ai/docs/proxy/virtual_keys
