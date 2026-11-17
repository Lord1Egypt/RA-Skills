---
name: oo-instagram
description: "Instagram (instagram.com). Use this skill for ANY Instagram request — searching and reading data. Whenever a task involves Instagram, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Instagram"
  author: "OOMOL"
  version: "1.0.0"
  services: ["instagram"]
  icon: "https://static.oomol.com/logo/third-party/instagram.png"
---

# Instagram

Operate **Instagram** through your OOMOL-connected account. This skill calls the `instagram` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Instagram. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "instagram" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "instagram" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account_insights` — Retrieve insight metrics for the connected Instagram professional account.
- `get_current_account` — Retrieve the connected Instagram professional account and its profile metadata.
- `get_media` — Retrieve one media object owned by the connected Instagram professional account.
- `get_media_insights` — Retrieve insight metrics for one Instagram media object.
- `list_media` — List media published by the connected Instagram professional account.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Instagram state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Instagram is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=instagram
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Instagram homepage: https://www.instagram.com/
