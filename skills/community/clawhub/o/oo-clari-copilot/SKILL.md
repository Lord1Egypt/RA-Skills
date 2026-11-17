---
name: oo-clari-copilot
description: "Clari Copilot (clari.com). Use this skill for ANY Clari Copilot request — searching and reading data. Whenever a task involves Clari Copilot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Clari Copilot"
  author: "OOMOL"
  version: "1.0.5"
  services: ["clari_copilot"]
  icon: "https://static.oomol.com/logo/third-party/clari_copilot.png"
---

# Clari Copilot

Operate **Clari Copilot** through your OOMOL-connected account. This skill calls the `clari_copilot` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Clari Copilot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "clari_copilot" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "clari_copilot" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_call_details` — Retrieve one Clari Copilot call with transcript, summary, and optional media URLs.
- `list_calls` — List Clari Copilot calls with supported filters, sorting, and pagination.
- `list_scorecards` — List Clari Copilot scorecards with pagination and scorer filters.
- `list_topics` — List Clari Copilot topics, optionally filtered by last modified time.
- `list_users` — List current users in the Clari Copilot workspace.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Clari Copilot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Clari Copilot is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/clari_copilot
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Clari Copilot homepage: https://www.clari.com/products/copilot/
- API documentation: https://api-doc.copilot.clari.com/
