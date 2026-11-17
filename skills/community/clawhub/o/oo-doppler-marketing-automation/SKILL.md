---
name: oo-doppler-marketing-automation
description: "Doppler Marketing Automation (fromdoppler.com). Use this skill for ANY Doppler Marketing Automation request — reading, creating, updating, and deleting data. Whenever a task involves Doppler Marketing Automation, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Doppler Marketing Automation"
  author: "OOMOL"
  version: "1.0.4"
  services: ["doppler_marketing_automation"]
  icon: "https://static.oomol.com/logo/third-party/doppler_marketing_automation.png"
---

# Doppler Marketing Automation

Operate **Doppler Marketing Automation** through your OOMOL-connected account. This skill calls the `doppler_marketing_automation` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Doppler Marketing Automation. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "doppler_marketing_automation" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "doppler_marketing_automation" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_subscriber_to_list` — Create or update a Doppler subscriber and associate the subscriber with a list. [write]
- `create_list` — Create a Doppler Email Marketing subscriber list. [write]
- `delete_list` — Remove a Doppler Email Marketing list while leaving its contacts in the account. [destructive]
- `get_list` — Retrieve one Doppler Email Marketing subscriber list by ID.
- `get_subscriber` — Retrieve one Doppler Email Marketing subscriber by email address.
- `list_list_subscribers` — List subscribers associated with a Doppler Email Marketing list.
- `list_lists` — List Doppler Email Marketing subscriber lists with optional pagination.
- `list_subscribers` — List subscribers across a Doppler Email Marketing account.
- `remove_subscriber_from_list` — Remove a subscriber from a Doppler list without deleting the subscriber from the account. [destructive]
- `update_list` — Rename a Doppler Email Marketing subscriber list. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Doppler Marketing Automation state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Doppler Marketing Automation is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/doppler_marketing_automation
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Doppler Marketing Automation homepage: https://www.fromdoppler.com/en/
- API documentation: https://restapi.fromdoppler.com/docs/
