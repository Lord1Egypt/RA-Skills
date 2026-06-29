---
name: oo-meet-geek
description: "MeetGeek (meetgeek.ai). Use this skill for ANY MeetGeek request — searching and reading data. Whenever a task involves MeetGeek, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "MeetGeek"
  author: "OOMOL"
  version: "1.0.0"
  services: ["meet_geek"]
  icon: "https://static.oomol.com/logo/third-party/meet_geek.svg"
---

# MeetGeek

Operate **MeetGeek** through your OOMOL-connected account. This skill calls the `meet_geek` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected MeetGeek. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "meet_geek" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "meet_geek" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_highlights` — Get highlights for a MeetGeek meeting, optionally filtered by type.
- `get_insights` — Get KPI and improvement insights for a MeetGeek meeting.
- `get_meeting` — Get details for a MeetGeek meeting.
- `get_summary` — Get the summary and AI insights for a MeetGeek meeting.
- `get_transcript` — Get paginated transcript sentences for a MeetGeek meeting.
- `list_meetings` — List paginated past meetings from MeetGeek.
- `list_team_meetings` — List paginated past meetings for a MeetGeek team.
- `list_teams` — List MeetGeek teams available to the API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change MeetGeek state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — MeetGeek is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=meet_geek
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- MeetGeek homepage: https://meetgeek.ai
