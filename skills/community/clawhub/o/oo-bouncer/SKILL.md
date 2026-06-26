---
name: oo-bouncer
description: "Bouncer (usebouncer.com). Use this skill for ANY Bouncer request — reading, creating, updating, and deleting data. Whenever a task involves Bouncer, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Bouncer"
  author: "OOMOL"
  version: "1.0.1"
  services: ["bouncer"]
  icon: "https://static.oomol.com/logo/third-party/Bouncer.svg"
---

# Bouncer

Operate **Bouncer** through your OOMOL-connected account. This skill calls the `bouncer` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Bouncer. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bouncer" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bouncer" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_batch_request` — Create an async Bouncer batch verification request for multiple email addresses. [write]
- `create_toxicity_list_job` — Create a Bouncer toxicity list job for multiple email addresses. [write]
- `delete_batch_request` — Delete a Bouncer batch verification request and its stored results. [destructive]
- `delete_toxicity_list_job` — Delete a Bouncer toxicity list job and its stored results. [destructive]
- `finish_batch` — Request early completion for a Bouncer batch verification request.
- `get_batch_results` — Download normalized results from a completed Bouncer batch verification request.
- `get_batch_status` — Get the current processing status of a Bouncer batch verification request.
- `get_credits` — Get the current Bouncer credit balance.
- `get_toxicity_list_job_status` — Get the current processing status of a Bouncer toxicity list job.
- `get_toxicity_list_results` — Download normalized results from a completed Bouncer toxicity list job.
- `verify_domain` — Verify one domain with Bouncer and inspect its DNS and catch-all signals.
- `verify_email` — Verify a single email address with Bouncer in real time.
- `verify_emails_batch_sync` — Verify multiple email addresses with Bouncer batch sync in a single request. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Bouncer state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Bouncer is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=bouncer
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Bouncer homepage: https://www.usebouncer.com/
