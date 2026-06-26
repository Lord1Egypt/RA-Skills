---
name: oo-nasa
description: "NASA (nasa.gov). Use this skill for ANY NASA request — searching and reading data. Whenever a task involves NASA, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "NASA"
  author: "OOMOL"
  version: "1.0.1"
  services: ["nasa"]
  icon: "https://static.oomol.com/logo/third-party/Nasa.svg"
---

# NASA

Operate **NASA** through your OOMOL-connected account. This skill calls the `nasa` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected NASA. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "nasa" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "nasa" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `browse_neo` — Browse NASA's near-Earth object catalog with pagination support.
- `get_apod` — Retrieve NASA's Astronomy Picture of the Day metadata for a specific date or the current day.
- `get_donki_cme` — Retrieve DONKI coronal mass ejection events for a date range.
- `get_donki_cme_analysis` — Retrieve DONKI coronal mass ejection analysis entries with optional accuracy and catalog filters.
- `get_donki_gst` — Retrieve DONKI geomagnetic storm events for a date range.
- `get_donki_hss` — Retrieve DONKI high-speed solar wind stream events for a date range.
- `get_donki_ips` — Retrieve DONKI interplanetary shock events with optional location and catalog filters.
- `get_donki_mpc` — Retrieve DONKI magnetopause crossing events for a date range.
- `get_donki_notifications` — Retrieve DONKI space weather notifications with optional type filtering.
- `get_donki_rbe` — Retrieve DONKI radiation belt enhancement events for a date range.
- `get_donki_sep` — Retrieve DONKI solar energetic particle events for a date range.
- `get_donki_solar_flares` — Retrieve DONKI solar flare events for a date range.
- `get_donki_wsa_enlil` — Retrieve DONKI WSA-Enlil simulation runs for a date range.
- `get_epic_aerosol` — Retrieve the most recent EPIC aerosol imagery metadata.
- `get_epic_aerosol_date` — Retrieve EPIC aerosol imagery metadata for a specific date.
- `get_epic_cloud` — Retrieve the most recent EPIC cloud fraction imagery metadata.
- `get_epic_cloud_date` — Retrieve EPIC cloud fraction imagery metadata for a specific date.
- `get_epic_enhanced` — Retrieve the most recent EPIC enhanced color image metadata.
- `get_epic_enhanced_date` — Retrieve EPIC enhanced color image metadata for a specific date.
- `get_epic_natural` — Retrieve the most recent EPIC natural color image metadata.
- `get_epic_natural_date` — Retrieve EPIC natural color image metadata for a specific date.
- `get_neo_lookup` — Lookup a specific NASA near-Earth object by asteroid id.
- `list_epic_aerosol_dates` — List the dates with available EPIC aerosol imagery.
- `list_epic_cloud_dates` — List the dates with available EPIC cloud fraction imagery.
- `list_epic_enhanced_dates` — List the dates with available EPIC enhanced color imagery.
- `list_epic_natural_dates` — List the dates with available EPIC natural color imagery.
- `search_near_earth_objects` — Search NASA near-Earth objects by closest approach date within a maximum 7-day window.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change NASA state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — NASA is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=nasa
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- NASA homepage: https://www.nasa.gov
