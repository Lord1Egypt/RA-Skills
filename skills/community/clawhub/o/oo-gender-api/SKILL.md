---
name: oo-gender-api
description: "Gender-API.com (gender-api.com). Use this skill for ANY Gender-API.com request — searching and reading data. Whenever a task involves Gender-API.com, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gender-API.com"
  author: "OOMOL"
  version: "1.0.5"
  services: ["gender_api"]
  icon: "https://static.oomol.com/logo/third-party/gender_api.svg"
---

# Gender-API.com

Operate **Gender-API.com** through your OOMOL-connected account. This skill calls the `gender_api` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gender-API.com. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gender_api" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gender_api" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_country_of_origin` — Get likely country-of-origin and ethnicity metadata for one first name, full name, or email address.
- `get_statistics` — Read remaining credits and recent usage statistics for the connected account.
- `query_gender_by_email_address` — Determine the likely gender for one email address after Gender-API.com extracts a name from it.
- `query_gender_by_first_name` — Determine the likely gender for one first name with optional country, locale, IP, and caller ID hints.
- `query_gender_by_full_name` — Determine the likely gender for one full name while letting Gender-API.com split the name.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gender-API.com state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gender-API.com is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gender_api
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Gender-API.com homepage: https://gender-api.com/
- API documentation: https://gender-api.com/en/api-docs/v2
