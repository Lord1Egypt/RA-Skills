---
name: oo-neverbounce
description: "NeverBounce (neverbounce.com). Use this skill for ANY NeverBounce request — reading, creating, and updating data. Whenever a task involves NeverBounce, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "NeverBounce"
  author: "OOMOL"
  version: "1.0.1"
  services: ["neverbounce"]
  icon: "https://static.oomol.com/logo/third-party/NeverBounce.svg"
---

# NeverBounce

Operate **NeverBounce** through your OOMOL-connected account. This skill calls the `neverbounce` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected NeverBounce. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "neverbounce" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "neverbounce" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_job` — Create a NeverBounce bulk verification job from a remote file or supplied rows. [write]
- `download_job_results` — Download a NeverBounce bulk job as CSV with optional result filters and extra columns.
- `get_account_info` — Get the current NeverBounce account credit summary and bulk job counters.
- `get_job_results` — Retrieve paginated NeverBounce verification results for a completed bulk job.
- `get_job_status` — Retrieve the current processing status and aggregate counts for a NeverBounce job.
- `parse_job` — Parse a NeverBounce bulk job created without auto_parse enabled.
- `single_check` — Verify a single email address with NeverBounce and return the verification result.
- `start_job` — Start a parsed NeverBounce bulk job. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change NeverBounce state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — NeverBounce is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=neverbounce
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- NeverBounce homepage: https://neverbounce.com
