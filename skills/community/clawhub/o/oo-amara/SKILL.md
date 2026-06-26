---
name: oo-amara
description: "Amara (amara.org). Use this skill for ANY Amara request — reading, creating, updating, and deleting data. Whenever a task involves Amara, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Amara"
  author: "OOMOL"
  version: "1.0.1"
  services: ["amara"]
  icon: "https://static.oomol.com/logo/third-party/Amara.svg"
---

# Amara

Operate **Amara** through your OOMOL-connected account. This skill calls the `amara` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Amara. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "amara" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "amara" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_subtitle_note` — Add a subtitle note for a specific video and subtitle language. [write]
- `add_video_url` — Add a new source URL to an existing Amara video. [write]
- `create_subtitle_language` — Create a new subtitle language track for an Amara video. [write]
- `create_subtitles` — Create a new subtitle version for a specific video and language. [write]
- `create_video` — Create a new Amara video from a source URL and title, with optional metadata. [write]
- `delete_video_url` — Delete a source URL from an existing Amara video. [destructive]
- `fetch_subtitles_data` — Fetch subtitle data for a specific video and language in JSON, SRT, or VTT format.
- `get_activity` — Fetch a single Amara activity item by activity ID.
- `get_subtitle_language_details` — Fetch a single subtitle language track for an Amara video.
- `get_team_details` — Fetch a single Amara team by team slug.
- `get_team_languages` — Fetch preferred and blacklisted language codes for a single Amara team.
- `get_user` — Fetch a single Amara user by username or user ID.
- `get_user_activity` — List activity items for a specific Amara user.
- `get_user_data` — Fetch a single Amara user by username, `me`, or user ID.
- `get_video` — Fetch a single Amara video by video ID.
- `get_video_url` — Fetch a single Amara video URL entry by video ID and URL ID.
- `get_video_url_details` — Look up Amara metadata for a public or embeddable video URL.
- `list_activity` — List Amara activity items with optional team, video, language, and date filters.
- `list_available_languages` — List the languages supported by the Amara API.
- `list_languages` — List the languages supported by the Amara API.
- `list_subtitle_actions` — List the subtitle workflow actions available for a specific video and language.
- `list_subtitle_languages` — List all subtitle language tracks for a single Amara video.
- `list_subtitle_notes` — List all subtitle notes for a specific video and subtitle language.
- `list_teams` — List the Amara teams accessible to the current API key with pagination controls.
- `list_video_activity` — List activity items for a single Amara video with pagination controls.
- `list_video_urls` — List all source URLs associated with a single Amara video.
- `list_videos` — List Amara videos with optional filters, sorting, and pagination controls.
- `make_video_url_primary` — Update a video URL entry and mark it as the primary URL when requested.
- `perform_subtitle_action` — Perform a subtitle workflow action such as publish, approve, or reject.
- `send_message` — Send a message to an Amara user or team recipient. [write]
- `update_subtitle_language` — Update subtitle language settings such as completion flags and soft limits. [write]
- `update_video` — Update an existing Amara video's metadata, assignment, or language settings. [write]
- `view_video_details` — Fetch a single Amara video by video ID.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Amara state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Amara is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=amara
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Amara homepage: https://amara.org
