---
name: oo-leadfeeder
description: "Leadfeeder (leadfeeder.com). Use this skill for ANY Leadfeeder request — searching and reading data. Whenever a task involves Leadfeeder, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Leadfeeder"
  author: "OOMOL"
  version: "1.0.5"
  services: ["leadfeeder"]
  icon: "https://static.oomol.com/logo/third-party/leadfeeder.svg"
---

# Leadfeeder

Operate **Leadfeeder** through your OOMOL-connected account. This skill calls the `leadfeeder` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Leadfeeder. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "leadfeeder" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "leadfeeder" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `enrich_ip` — Enrich one IPv4 or IPv6 address with Leadfeeder company or network intelligence.
- `get_companies` — Fetch detailed Leadfeeder firmographic data for up to 100 company IDs in one request.
- `get_company` — Fetch detailed Leadfeeder firmographic and hierarchy data for one company ID.
- `get_current_user` — Retrieve the Leadfeeder user associated with the connected API key.
- `list_accounts` — List Leadfeeder accounts available to the API key, optionally including credit details for one account.
- `match_companies` — Match one or more company records to Leadfeeder companies and return ranked matches for each input record.
- `search_companies` — Search Leadfeeder company intelligence using company terms, location, industry, size, revenue, ICP, and boolean filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Leadfeeder state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Leadfeeder is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/leadfeeder
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Leadfeeder homepage: https://www.leadfeeder.com
- API documentation: https://docs.leadfeeder.com/api/public/introduction-354545m0
