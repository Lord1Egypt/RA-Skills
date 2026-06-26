---
name: oo-strava
description: "Strava (strava.com). Use this skill for ANY Strava request — reading, creating, and updating data. Whenever a task involves Strava, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Strava"
  author: "OOMOL"
  version: "1.0.1"
  services: ["strava"]
  icon: "https://static.oomol.com/logo/third-party/Strava.svg"
---

# Strava

Operate **Strava** through your OOMOL-connected account. This skill calls the `strava` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Strava. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "strava" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "strava" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_activity` — Create a manually entered Strava activity. [write]
- `explore_segments` — Explore eligible Strava segments within a given bounding box.
- `export_route_gpx` — Export the GPX content of a specified Strava route.
- `export_route_tcx` — Export TCX content for a specified Strava route.
- `get_activity` — Get activity details for current Strava athletes by ID.
- `get_activity_streams` — Get streaming data for the specified Strava activity.
- `get_activity_zones` — Gets the training partition results for the specified Strava activity.
- `get_athlete_stats` — Get a summary of statistics for a specified Strava athlete.
- `get_authenticated_athlete` — Get currently licensed Strava athlete profiles.
- `get_club` — Get Strava club details by ID.
- `get_equipment` — Get Strava gear details by ID.
- `get_route` — Get Strava route details by ID.
- `get_route_streams` — Get flow data for a specified Strava route.
- `get_segment` — Get Strava segment details by ID.
- `get_segment_effort` — Get Strava segment performance details by ID.
- `get_segment_effort_streams` — Get streaming data for a specified Strava segment score.
- `get_segment_streams` — Get flow data for a specified Strava segment.
- `get_upload` — Query the status of Strava activity upload tasks. [write]
- `get_zones` — Get the current Strava athlete's training partition.
- `list_activity_comments` — Lists comments for the specified Strava activity.
- `list_activity_kudoers` — List athletes who have liked the specified Strava activity.
- `list_activity_laps` — Lists the segments for a given Strava activity.
- `list_athlete_activities` — Paginated list of current Strava athletes' activities.
- `list_athlete_clubs` — Lists the clubs current Strava athletes belong to.
- `list_athlete_routes` — Paginated list of routes for a given Strava athlete.
- `list_club_activities` — Paginated list of recent activity for a given Strava club.
- `list_club_administrators` — Paginated list of Strava club admins.
- `list_club_members` — Paginated list of Strava club members.
- `list_segment_efforts` — List Strava segment scores by segment ID.
- `list_starred_segments` — Paginated list of current Strava athlete collections.
- `star_segment` — Favorite or unfavorite a specific Strava segment. [write]
- `update_activity` — Update activity information for current Strava athletes. [write]
- `update_athlete` — Update current Strava athlete's weight. [write]
- `upload_activity` — Upload GPX, TCX or FIT files to Strava to generate events. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Strava state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Strava is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=strava
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Strava homepage: https://www.strava.com
