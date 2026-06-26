---
name: oo-ticketmaster
description: "Ticketmaster (ticketmaster.com). Use this skill for ANY Ticketmaster request — searching and reading data. Whenever a task involves Ticketmaster, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Ticketmaster"
  author: "OOMOL"
  version: "1.0.1"
  services: ["ticketmaster"]
  icon: "https://static.oomol.com/logo/third-party/Ticketmaster.png"
---

# Ticketmaster

Operate **Ticketmaster** through your OOMOL-connected account. This skill calls the `ticketmaster` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Ticketmaster. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ticketmaster" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ticketmaster" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `execute_season_ticketing_command` — Execute a Ticketmaster Season Ticketing command and optionally poll until the command finishes.
- `get_attraction_details` — Get the details for a specific Ticketmaster attraction by ID.
- `get_attractions` — Search Discovery API attractions for artists, teams, performers, and other attraction entities.
- `get_classification_details` — Get the details for a specific Ticketmaster classification by ID.
- `get_classifications` — List Discovery API classifications for segments, genres, and sub-genres.
- `get_event_details` — Get the details for a specific Ticketmaster event by ID.
- `get_event_images` — Get the image set for a specific Ticketmaster event.
- `get_events` — Search Discovery API events with Ticketmaster filters for keyword, location, date, and taxonomy fields.
- `get_genre_details` — Get the details for a specific Ticketmaster genre by ID.
- `get_section_map_image` — Get a section-map image for a Ticketmaster event through the Partner Availability API.
- `get_segment_details` — Get the details for a specific Ticketmaster segment by ID.
- `get_subgenre_details` — Get the details for a specific Ticketmaster sub-genre by ID.
- `get_suggestions` — Get Discovery API search suggestions across events, venues, and attractions.
- `get_venue_details` — Get the details for a specific Ticketmaster venue by ID.
- `get_venues` — Search Discovery API venues by ID, keyword, and location filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Ticketmaster state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Ticketmaster is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=ticketmaster
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Ticketmaster homepage: https://www.ticketmaster.com
