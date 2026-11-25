---
name: oo-zoom
description: "Zoom (zoom.com). Use this skill for ANY Zoom request — reading, creating, and updating data. Whenever a task involves Zoom, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zoom"
  author: "OOMOL"
  version: "1.0.8"
  services: ["zoom"]
  icon: "https://static.oomol.com/logo/third-party/zoom.svg"
---

# Zoom

Operate **Zoom** through your OOMOL-connected account. This skill calls the `zoom` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zoom. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zoom" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zoom" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_meeting` — Create a Zoom meeting for a user with the core official scheduling fields and first-pass settings. [write]
- `get_meeting_summary` — Fetch the AI Companion summary of one meeting instance by its UUID. When Zoom answers 403 code 2305 (summary access restricted to IP ranges, summaries shared by email only, or the summary in Trash), the result is available false with a reason instead of an error.
- `get_user` — Fetch one Zoom user by ID or email, or the connected user when userId is omitted.
- `list_meetings` — List scheduled, live, upcoming, or previous meetings for a Zoom user using official pagination.
- `list_user_meeting_summaries` — List a user's AI Companion meeting summaries in a time window, newest first, without their content. Zoom's page token expires 15 minutes after it is issued; an expired token is refused as invalid input.
- `update_meeting` — Update a Zoom meeting by meeting ID with the core official scheduling fields and first-pass settings. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zoom state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zoom is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/zoom
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Zoom homepage: https://www.zoom.com
- API documentation: https://developers.zoom.us/docs/api/meetings/
