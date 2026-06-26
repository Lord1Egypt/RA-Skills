---
name: oo-contentful
description: "Contentful (contentful.com). Use this skill for ANY Contentful request — reading, creating, and updating data. Whenever a task involves Contentful, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Contentful"
  author: "OOMOL"
  version: "1.0.1"
  services: ["contentful"]
  icon: "https://static.oomol.com/logo/third-party/Contentful.svg"
---

# Contentful

Operate **Contentful** through your OOMOL-connected account. This skill calls the `contentful` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Contentful. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "contentful" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "contentful" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_entry` — Create a Contentful entry in a specific environment. [write]
- `get_current_user` — Get the authenticated Contentful user profile for the current personal access token.
- `get_entry` — Get a single Contentful entry by identifier.
- `list_content_types` — List Contentful content types available in a specific environment.
- `list_entries` — List Contentful entries with common filtering, pagination, and include options.
- `list_environments` — List Contentful environments inside a specific space.
- `list_spaces` — List Contentful spaces accessible to the current personal access token.
- `update_entry` — Update a Contentful entry using optimistic locking. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Contentful state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Contentful is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=contentful
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Contentful homepage: https://www.contentful.com
