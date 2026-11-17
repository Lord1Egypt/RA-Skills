---
name: oo-klipfolio
description: "Klipfolio (klipfolio.com). Use this skill for ANY Klipfolio request — searching and reading data. Whenever a task involves Klipfolio, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Klipfolio"
  author: "OOMOL"
  version: "1.0.4"
  services: ["klipfolio"]
  icon: "https://static.oomol.com/logo/third-party/klipfolio.svg"
---

# Klipfolio

Operate **Klipfolio** through your OOMOL-connected account. This skill calls the `klipfolio` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Klipfolio. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "klipfolio" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "klipfolio" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_client` — Get a Klipfolio client asset by ID.
- `get_dashboard` — Get a Klipfolio dashboard asset by ID.
- `get_data_source` — Get a Klipfolio data source asset by ID.
- `get_klip` — Get a Klipfolio Klip asset by ID.
- `list_clients` — List Klipfolio client assets visible to the current API key.
- `list_dashboards` — List Klipfolio dashboard assets visible to the current API key.
- `list_data_sources` — List Klipfolio data source assets visible to the current API key.
- `list_klips` — List Klipfolio Klip assets visible to the current API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Klipfolio state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Klipfolio is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/klipfolio
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Klipfolio homepage: https://www.klipfolio.com
- API documentation: https://apidocs.klipfolio.com/reference
