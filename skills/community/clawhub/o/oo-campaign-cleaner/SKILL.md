---
name: oo-campaign-cleaner
description: "Campaign Cleaner (campaigncleaner.com). Use this skill for ANY Campaign Cleaner request — reading, creating, updating, and deleting data. Whenever a task involves Campaign Cleaner, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Campaign Cleaner"
  author: "OOMOL"
  version: "1.0.1"
  services: ["campaign_cleaner"]
  icon: "https://static.oomol.com/logo/third-party/campaign_cleaner.png"
---

# Campaign Cleaner

Operate **Campaign Cleaner** through your OOMOL-connected account. This skill calls the `campaign_cleaner` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Campaign Cleaner. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "campaign_cleaner" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "campaign_cleaner" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_campaign` — Delete one saved Campaign Cleaner campaign by campaign ID. [destructive]
- `get_campaign` — Retrieve the full Campaign Cleaner analysis payload for one saved campaign.
- `get_campaign_pdf_analysis` — Download a Campaign Cleaner PDF analysis report and return it as a transit file.
- `get_campaign_status` — Fetch the current processing status of one submitted Campaign Cleaner campaign.
- `get_credits` — Get the remaining Campaign Cleaner credits available to the current API key.
- `list_campaigns` — List saved Campaign Cleaner campaigns together with their current processing status.
- `send_campaign` — Submit an email campaign HTML payload for Campaign Cleaner analysis and processing. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Campaign Cleaner state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Campaign Cleaner is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=campaign_cleaner
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Campaign Cleaner homepage: https://campaigncleaner.com
