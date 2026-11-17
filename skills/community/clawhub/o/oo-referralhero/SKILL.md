---
name: oo-referralhero
description: "ReferralHero (referralhero.com). Use this skill for ANY ReferralHero request — reading, creating, updating, and deleting data. Whenever a task involves ReferralHero, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ReferralHero"
  author: "OOMOL"
  version: "1.0.5"
  services: ["referralhero"]
  icon: "https://static.oomol.com/logo/third-party/referralhero.svg"
---

# ReferralHero

Operate **ReferralHero** through your OOMOL-connected account. This skill calls the `referralhero` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ReferralHero. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "referralhero" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "referralhero" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_subscriber` — Add a subscriber to a ReferralHero campaign using its configured identifier. [write]
- `confirm_referral` — Confirm the third conversion event for a verified ReferralHero subscriber. [write]
- `create_list` — Create a ReferralHero referral campaign with a name and default referral URL. [write]
- `delete_subscriber` — Delete one subscriber from a ReferralHero campaign. [destructive]
- `get_leaderboard` — Get the highest-ranked subscribers in a ReferralHero campaign.
- `get_subscriber` — Retrieve one verified ReferralHero subscriber by ID.
- `list_lists` — List active ReferralHero referral campaigns in the connected account.
- `list_rewards` — List the rewards configured for a ReferralHero campaign.
- `list_subscribers` — List subscribers in a ReferralHero campaign with pagination and optional sorting.
- `track_conversion` — Track the second conversion event for a two-step or three-step referral campaign. [write]
- `update_subscriber` — Update fields on one verified ReferralHero subscriber. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ReferralHero state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ReferralHero is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/referralhero
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- ReferralHero homepage: https://referralhero.com
- API documentation: https://support.referralhero.com/integrate/rest-api
