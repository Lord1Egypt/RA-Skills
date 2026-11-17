---
name: oo-growsurf
description: "GrowSurf (growsurf.com). Use this skill for ANY GrowSurf request — reading, creating, updating, and deleting data. Whenever a task involves GrowSurf, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "GrowSurf"
  author: "OOMOL"
  version: "1.0.2"
  services: ["growsurf"]
  icon: "https://static.oomol.com/logo/third-party/growsurf.png"
---

# GrowSurf

Operate **GrowSurf** through your OOMOL-connected account. This skill calls the `growsurf` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected GrowSurf. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "growsurf" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "growsurf" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_delayed_referral` — Cancel a pending delayed GrowSurf referral trigger. Returns success false when there is no pending trigger. [destructive]
- `create_participant` — Add a GrowSurf participant; an existing email returns its participant unchanged. In affiliate programs, omitted isAffiliate enrolls an approved affiliate unless a valid referredBy is supplied. Referred signups may earn Lead rewards. [write]
- `delete_participant` — Delete a GrowSurf participant. Pending analytics erasure runs automatically; do not repeat deletion to complete it. [destructive]
- `get_campaign` — Get one GrowSurf program's configuration and totals.
- `get_participant` — Get a GrowSurf participant by ID or email address.
- `get_team` — Get the GrowSurf team bound to your API key and its email verification state.
- `list_campaigns` — List GrowSurf programs belonging to your API key's team. Deleted programs are excluded.
- `list_participants` — List a page of GrowSurf participants. Pass nextId into the next request until null; metadata filters match all supplied values exactly.
- `trigger_referral` — Trigger referral credit for a GrowSurf participant immediately or after a delay managed by GrowSurf. Inspect success and message for the actual outcome. [write]
- `update_participant` — Update a GrowSurf participant. Can suspend or ban affiliates and expire referral credit. Supplied vanityKeys replace existing aliases; omitted fields remain unchanged. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change GrowSurf state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — GrowSurf is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/growsurf
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- GrowSurf homepage: https://growsurf.com/
- API documentation: https://docs.growsurf.com/developer-tools/rest-api
