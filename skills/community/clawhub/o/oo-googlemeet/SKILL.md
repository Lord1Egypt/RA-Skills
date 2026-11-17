---
name: oo-googlemeet
description: "Google Meet (workspace.google.com). Use this skill for ANY Google Meet request — reading, creating, and updating data. Whenever a task involves Google Meet, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Meet"
  author: "OOMOL"
  version: "1.0.5"
  services: ["googlemeet"]
  icon: "https://static.oomol.com/logo/third-party/googlemeet.svg"
---

# Google Meet

Operate **Google Meet** through your OOMOL-connected account. This skill calls the `googlemeet` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Meet. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googlemeet" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googlemeet" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_space` — Create a Google Meet space and return its join URL. [write]
- `end_active_conference` — End the active conference currently running in a Google Meet space. [write]
- `get_conference_record` — Retrieve one Google Meet conference record.
- `get_participant` — Retrieve one participant from a Google Meet conference record.
- `get_participant_session` — Retrieve one Google Meet participant session.
- `get_recording` — Retrieve one Google Meet recording.
- `get_smart_note` — Retrieve one Google Meet smart-note artifact.
- `get_space` — Retrieve a Google Meet space by resource name or meeting code.
- `get_transcript` — Retrieve one Google Meet transcript.
- `get_transcript_entry` — Retrieve one speaker segment from a Google Meet transcript.
- `list_conference_records` — List accessible Google Meet conference records with optional filtering and pagination.
- `list_participant_sessions` — List join-to-leave sessions for a Google Meet participant.
- `list_participants` — List participants in a Google Meet conference record.
- `list_recordings` — List recordings generated for a Google Meet conference record.
- `list_smart_notes` — List smart notes generated for a Google Meet conference record.
- `list_transcript_entries` — List speaker segments in a Google Meet transcript.
- `list_transcripts` — List transcripts generated for a Google Meet conference record.
- `update_space` — Update the configuration of a Google Meet space. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Meet state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Meet is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/googlemeet
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Google Meet homepage: https://workspace.google.com/products/meet/
- API documentation: https://developers.google.com/workspace/meet/api/reference/rest/v2
