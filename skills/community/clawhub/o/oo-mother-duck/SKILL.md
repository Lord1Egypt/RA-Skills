---
name: oo-mother-duck
description: "MotherDuck (motherduck.com). Use this skill for ANY MotherDuck request — reading, creating, updating, and deleting data. Whenever a task involves MotherDuck, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "MotherDuck"
  author: "OOMOL"
  version: "1.0.0"
  services: ["mother_duck"]
  icon: "https://static.oomol.com/logo/third-party/mother_duck.svg"
---

# MotherDuck

Operate **MotherDuck** through your OOMOL-connected account. This skill calls the `mother_duck` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected MotherDuck. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mother_duck" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mother_duck" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_token` — Create a MotherDuck access token for a user. [write]
- `create_user` — Create a MotherDuck member user in the organization. [write]
- `delete_token` — Invalidate a MotherDuck access token for a user. [destructive]
- `delete_user` — Permanently delete a MotherDuck user and all of their data. [destructive]
- `get_user_duckling_config` — Retrieve MotherDuck Duckling configuration for a user.
- `list_active_accounts` — List active MotherDuck accounts and their active Ducklings in the organization.
- `list_tokens` — List MotherDuck access tokens for a user.
- `set_user_duckling_config` — Set MotherDuck Duckling configuration for a user. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change MotherDuck state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — MotherDuck is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mother_duck
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- MotherDuck homepage: https://motherduck.com
