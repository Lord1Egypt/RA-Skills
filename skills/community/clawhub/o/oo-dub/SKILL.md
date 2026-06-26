---
name: oo-dub
description: "Dub (dub.co). Use this skill for ANY Dub request — reading, creating, updating, and deleting data. Whenever a task involves Dub, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Dub"
  author: "OOMOL"
  version: "1.0.2"
  services: ["dub"]
  icon: "https://static.oomol.com/logo/third-party/dub.svg"
---

# Dub

Operate **Dub** through your OOMOL-connected account. This skill calls the `dub` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Dub. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "dub" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "dub" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `count_links` — Retrieve the number of matching links in the authenticated Dub workspace.
- `create_folder` — Create a folder in the authenticated Dub workspace. [write]
- `create_link` — Create a short link in the authenticated Dub workspace. [write]
- `create_tag` — Create a tag in the authenticated Dub workspace. [write]
- `delete_folder` — Delete a folder from the authenticated Dub workspace. [destructive]
- `delete_link` — Delete a short link from the authenticated Dub workspace. [destructive]
- `delete_tag` — Delete a tag from the authenticated Dub workspace. [destructive]
- `list_folders` — List folders in the authenticated Dub workspace.
- `list_links` — List short links in the authenticated Dub workspace.
- `list_tags` — List tags in the authenticated Dub workspace.
- `retrieve_analytics` — Retrieve analytics for a Dub link, domain, or workspace.
- `retrieve_link` — Retrieve a Dub short link by ID or by supported lookup fields.
- `update_folder` — Update a folder in the authenticated Dub workspace. [write]
- `update_link` — Update a short link in the authenticated Dub workspace. [write]
- `update_tag` — Update a tag in the authenticated Dub workspace. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Dub state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Dub is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=dub
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Dub homepage: https://dub.co
