---
name: oo-mixmax
description: "Mixmax (mixmax.com). Use this skill for ANY Mixmax request — reading, creating, and updating data. Whenever a task involves Mixmax, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mixmax"
  author: "OOMOL"
  version: "1.0.4"
  services: ["mixmax"]
  icon: "https://static.oomol.com/logo/third-party/mixmax.svg"
---

# Mixmax

Operate **Mixmax** through your OOMOL-connected account. This skill calls the `mixmax` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mixmax. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mixmax" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mixmax" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_sequence_recipients` — Add recipients to a Mixmax sequence and optionally schedule them or keep them in draft. [write]
- `list_sequence_recipients` — List activated recipients for one Mixmax sequence with offset pagination.
- `list_sequences` — List Mixmax sequences with optional name, folder, expansion, and cursor filters.
- `search_sequence_recipients` — Search Mixmax sequence recipients by query text or exact email addresses, optionally within one sequence.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mixmax state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mixmax is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/mixmax
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Mixmax homepage: https://www.mixmax.com/
- API documentation: https://developer.mixmax.com/reference/getting-started-with-the-api
