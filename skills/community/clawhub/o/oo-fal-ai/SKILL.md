---
name: oo-fal-ai
description: "fal.ai (fal.ai). Use this skill for ANY fal.ai request — reading, creating, and updating data. Whenever a task involves fal.ai, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "fal.ai"
  author: "OOMOL"
  version: "1.0.1"
  services: ["fal_ai"]
  icon: "https://static.oomol.com/logo/third-party/Fal.ai.svg"
---

# fal.ai

Operate **fal.ai** through your OOMOL-connected account. This skill calls the `fal_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected fal.ai. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fal_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fal_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_queue_request` — Request cancellation of a queued or in-progress fal request by model ID and request ID. [write]
- `estimate_pricing` — Estimate total fal model cost using either historical API call quantities or expected billing-unit quantities.
- `get_jwks` — Retrieve the fal JSON Web Key Set used for webhook signature verification.
- `get_models` — Discover fal model endpoints with optional text search, status, category, pagination, endpoint filtering, and response expansion.
- `get_pricing` — Retrieve unit pricing information for one or more fal model endpoints, including billing unit and currency.
- `get_queue_request_result` — Retrieve the stored final result payload for a completed fal queued request.
- `queue_get_status` — Check the status of a queued fal request, with optional log retrieval for in-progress or completed work.
- `queue_get_status_stream` — Consume fal queue status updates as a streamed sequence of SSE events until the server closes the stream.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change fal.ai state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — fal.ai is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=fal_ai
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- fal.ai homepage: https://fal.ai
