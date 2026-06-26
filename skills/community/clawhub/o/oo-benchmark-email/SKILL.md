---
name: oo-benchmark-email
description: "Benchmark Email (benchmarkemail.com). Use this skill for ANY Benchmark Email request — searching and reading data. Whenever a task involves Benchmark Email, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Benchmark Email"
  author: "OOMOL"
  version: "1.0.1"
  services: ["benchmark_email"]
  icon: "https://static.oomol.com/logo/third-party/benchmark_email.svg"
---

# Benchmark Email

Operate **Benchmark Email** through your OOMOL-connected account. This skill calls the `benchmark_email` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Benchmark Email. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "benchmark_email" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "benchmark_email" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account_summary` — Get the current Benchmark Email account summary and image storage plan details.
- `get_contact_details` — Get detailed information for a specific Benchmark Email contact email within a specific list.
- `get_contact_list_summary` — Get summary counts for a Benchmark Email contact list, including active, bounced, pending, and unsubscribed contacts.
- `get_contacts_in_list` — Get paginated contacts from a Benchmark Email list with optional search, filter, and sorting parameters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Benchmark Email state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Benchmark Email is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=benchmark_email
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Benchmark Email homepage: https://www.benchmarkemail.com
