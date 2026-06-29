---
name: oo-agility
description: "Agility CMS (agilitycms.com). Use this skill for ANY Agility CMS request — searching and reading data. Whenever a task involves Agility CMS, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Agility CMS"
  author: "OOMOL"
  version: "1.0.0"
  services: ["agility"]
  icon: "https://static.oomol.com/logo/third-party/agility.svg"
---

# Agility CMS

Operate **Agility CMS** through your OOMOL-connected account. This skill calls the `agility` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Agility CMS. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "agility" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "agility" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_content_item` — Retrieve an Agility CMS content item by content ID for a locale.
- `get_content_list` — Retrieve an Agility CMS content list by reference name with optional pagination, filtering, sorting, and linked-content expansion.
- `get_flat_sitemap` — Retrieve an Agility CMS flat sitemap keyed by page path for a channel.
- `get_nested_sitemap` — Retrieve an Agility CMS nested sitemap for generating menus or navigation.
- `get_page` — Retrieve an Agility CMS page by page ID for a locale.
- `list_content_models` — List content models for an Agility CMS instance using the Content Fetch API.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Agility CMS state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Agility CMS is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=agility
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Agility CMS homepage: https://agilitycms.com/
