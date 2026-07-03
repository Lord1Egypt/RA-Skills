---
name: oo-helpscout-docs
description: "Help Scout Docs (helpscout.com). Use this skill for ANY Help Scout Docs request — searching and reading data. Whenever a task involves Help Scout Docs, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Help Scout Docs"
  author: "OOMOL"
  version: "1.0.0"
  services: ["helpscout_docs"]
  icon: "https://static.oomol.com/logo/third-party/helpscout_docs.svg"
---

# Help Scout Docs

Operate **Help Scout Docs** through your OOMOL-connected account. This skill calls the `helpscout_docs` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Help Scout Docs. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "helpscout_docs" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "helpscout_docs" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_article` — Get a Help Scout Docs article by ID or article number.
- `list_articles` — List Help Scout Docs articles in a collection or category.
- `list_categories` — List Help Scout Docs categories in a collection.
- `list_collections` — List Help Scout Docs collections available to the API key.
- `list_sites` — List Help Scout Docs sites available to the API key.
- `search_articles` — Search Help Scout Docs articles by query with optional collection and site filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Help Scout Docs state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Help Scout Docs is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=helpscout_docs
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Help Scout Docs homepage: https://www.helpscout.com
