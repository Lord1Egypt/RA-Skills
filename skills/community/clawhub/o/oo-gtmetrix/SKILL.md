---
name: oo-gtmetrix
description: "GTmetrix (gtmetrix.com). Use this skill for ANY GTmetrix request — reading, creating, and updating data. Whenever a task involves GTmetrix, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "GTmetrix"
  author: "OOMOL"
  version: "1.0.1"
  services: ["gtmetrix"]
  icon: "https://static.oomol.com/logo/third-party/GTmetrix.svg"
---

# GTmetrix

Operate **GTmetrix** through your OOMOL-connected account. This skill calls the `gtmetrix` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected GTmetrix. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gtmetrix" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gtmetrix" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account_status` — Get the current GTmetrix account status, credits, and plan capabilities.
- `get_browser` — Get a single GTmetrix browser by ID.
- `get_latest_page_report` — Get the latest GTmetrix report associated with a page.
- `get_location` — Get a single GTmetrix test location by ID.
- `get_page` — Get a single GTmetrix page by slug.
- `get_report` — Get a single GTmetrix report by slug.
- `get_simulated_device` — Get a single GTmetrix simulated device by ID.
- `get_test` — Get the current state of a GTmetrix test and detect when it has completed.
- `list_browsers` — List GTmetrix browsers that can be used for tests.
- `list_locations` — List GTmetrix test locations available to the connected account.
- `list_page_reports` — List GTmetrix reports associated with a single page.
- `list_pages` — List GTmetrix pages associated with the connected account.
- `list_simulated_devices` — List GTmetrix simulated devices that can be used for tests.
- `list_tests` — List GTmetrix tests for the connected account.
- `start_test` — Start a new GTmetrix performance test for a URL. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change GTmetrix state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — GTmetrix is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=gtmetrix
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- GTmetrix homepage: https://gtmetrix.com
