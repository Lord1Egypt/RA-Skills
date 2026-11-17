---
name: oo-7-shifts
description: "7shifts (7shifts.com). Use this skill for ANY 7shifts request — searching and reading data. Whenever a task involves 7shifts, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "7shifts"
  author: "OOMOL"
  version: "1.0.4"
  services: ["7_shifts"]
  icon: "https://static.oomol.com/logo/third-party/7_shifts.png"
---

# 7shifts

Operate **7shifts** through your OOMOL-connected account. This skill calls the `7_shifts` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected 7shifts. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "7_shifts" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "7_shifts" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_company` — Retrieve one 7shifts company by ID.
- `list_companies` — List 7shifts companies available to the access token.
- `list_departments` — List 7shifts departments for a company.
- `list_locations` — List 7shifts locations for a company.
- `list_roles` — List 7shifts roles for a company.
- `list_users` — List 7shifts users for a company.
- `retrieve_identity` — Retrieve the 7shifts identity associated with the access token.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change 7shifts state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — 7shifts is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/7_shifts
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- 7shifts homepage: https://www.7shifts.com/
- API documentation: https://developers.7shifts.com/
