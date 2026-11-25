---
name: oo-cloro
description: "Cloro (cloro.dev). Use this skill for ANY Cloro request — reading, creating, updating, and deleting data. Whenever a task involves Cloro, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloro"
  author: "OOMOL"
  version: "1.0.3"
  services: ["cloro"]
  icon: "https://static.oomol.com/logo/third-party/cloro.svg"
---

# Cloro

Operate **Cloro** through your OOMOL-connected account. This skill calls the `cloro` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloro. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloro" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloro" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `clear_queue` — Delete all QUEUED tasks in the organization. Processing, completed and failed tasks are unaffected. [destructive]
- `create_batch_tasks` — Submit up to 500 monitoring tasks. Each task is validated independently upstream; inspect results for partial failures. [write]
- `create_task` — Submit a native asynchronous monitoring task. Use get_task for the result; priority, idempotency and webhooks are supported. [write]
- `get_credits` — Read organization credit balance and billing cycle. Values can be cached for up to 60 seconds.
- `get_queue_status` — Read queued and processing task counts and concurrency usage.
- `get_task` — Read task status and final engine response. Failed task details remain available in response.
- `list_countries` — List supported country codes, optionally filtered by engine.
- `list_states` — List supported US states. Other country codes return an empty list.
- `monitor_aimode` — Retrieve Google AI Mode results synchronously. For long-running or bulk work, use create_task or create_batch_tasks. Sync calls include a credit surcharge; Google product tokens expire after five minutes.
- `monitor_bing_aimode` — Retrieve Bing AI Mode results synchronously. For long-running or bulk work, use create_task or create_batch_tasks. Sync calls include a credit surcharge; Google product tokens expire after five minutes.
- `monitor_chatgpt` — Retrieve ChatGPT results synchronously. For long-running or bulk work, use create_task or create_batch_tasks. Sync calls include a credit surcharge; Google product tokens expire after five minutes.
- `monitor_gemini` — Retrieve Gemini results synchronously. For long-running or bulk work, use create_task or create_batch_tasks. Sync calls include a credit surcharge; Google product tokens expire after five minutes.
- `monitor_google` — Retrieve Google Search results synchronously. For long-running or bulk work, use create_task or create_batch_tasks. Sync calls include a credit surcharge; Google product tokens expire after five minutes.
- `monitor_google_news` — Retrieve Google News results synchronously. For long-running or bulk work, use create_task or create_batch_tasks. Sync calls include a credit surcharge; Google product tokens expire after five minutes.
- `monitor_google_product` — Retrieve Google product details results synchronously. For long-running or bulk work, use create_task or create_batch_tasks. Sync calls include a credit surcharge; Google product tokens expire after five minutes.
- `resolve_google_link` — Resolve a Google redirect link through Cloro without consuming credits.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloro state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloro is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/cloro
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cloro homepage: https://cloro.dev
- API documentation: https://cloro.dev/docs
