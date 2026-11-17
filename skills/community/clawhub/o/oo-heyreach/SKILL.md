---
name: oo-heyreach
description: "HeyReach (heyreach.io). Use this skill for ANY HeyReach request — reading, creating, and updating data. Whenever a task involves HeyReach, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "HeyReach"
  author: "OOMOL"
  version: "1.0.4"
  services: ["heyreach"]
  icon: "https://static.oomol.com/logo/third-party/heyreach.svg"
---

# HeyReach

Operate **HeyReach** through your OOMOL-connected account. This skill calls the `heyreach` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected HeyReach. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "heyreach" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "heyreach" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_empty_list` — Create an empty HeyReach lead or company list. [write]
- `get_campaign` — Retrieve one HeyReach campaign by ID.
- `get_lead` — Retrieve HeyReach lead details by LinkedIn profile URL.
- `get_lead_tags` — Retrieve tags for a HeyReach lead by LinkedIn profile URL.
- `get_overall_stats` — Retrieve aggregated HeyReach outreach stats for optional account and campaign filters.
- `get_overall_stats_by_campaign` — Retrieve HeyReach outreach stats grouped by campaign.
- `list_campaigns` — List HeyReach campaigns with optional filters and pagination.
- `list_leads` — List leads from a HeyReach list with optional filters and pagination.
- `list_linkedin_accounts` — List HeyReach LinkedIn sender accounts with pagination.
- `list_lists` — List HeyReach lead and company lists with pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change HeyReach state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — HeyReach is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/heyreach
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- HeyReach homepage: https://www.heyreach.io
- API documentation: https://documenter.getpostman.com/view/23808049/2sA2xb5F75
