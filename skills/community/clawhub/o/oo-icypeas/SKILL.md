---
name: oo-icypeas
description: "Icypeas (icypeas.com). Use this skill for ANY Icypeas request — reading, creating, and updating data. Whenever a task involves Icypeas, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Icypeas"
  author: "OOMOL"
  version: "1.0.5"
  services: ["icypeas"]
  icon: "https://static.oomol.com/logo/third-party/icypeas.png"
---

# Icypeas

Operate **Icypeas** through your OOMOL-connected account. This skill calls the `icypeas` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Icypeas. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "icypeas" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "icypeas" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_search_item` — Retrieve one Icypeas search item by ID and expose its processing status.
- `get_subscription_information` — Fetch Icypeas subscription details and remaining credit balances by account email.
- `reverse_email_lookup` — Find a LinkedIn profile URL behind one professional email address with Icypeas.
- `submit_domain_scan` — Submit one Icypeas domain scan for role-based email addresses. [write]
- `submit_email_search` — Submit one Icypeas email discovery search for a person and company. [write]
- `submit_email_verification` — Submit one Icypeas email verification request and return the search item handle. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Icypeas state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Icypeas is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/icypeas
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Icypeas homepage: https://www.icypeas.com
- API documentation: https://api-doc.icypeas.com/getting-started
