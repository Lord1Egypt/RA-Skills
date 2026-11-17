---
name: oo-youtube
description: "YouTube (youtube.com). Use this skill for ANY YouTube request — reading, creating, updating, and deleting data. Whenever a task involves YouTube, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "YouTube"
  author: "OOMOL"
  version: "1.0.7"
  services: ["youtube"]
  icon: "https://static.oomol.com/logo/third-party/youtube.svg"
---

# YouTube

Operate **YouTube** through your OOMOL-connected account. This skill calls the `youtube` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected YouTube. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "youtube" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "youtube" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_video_to_playlist` — Add a YouTube video to a playlist. [write]
- `create_comment_reply` — Reply to an existing YouTube comment thread. [write]
- `create_playlist` — Create a YouTube playlist owned by the authenticated user. [write]
- `delete_caption` — Delete a YouTube caption track. [destructive]
- `delete_playlist` — Delete a YouTube playlist owned by the authenticated user. [destructive]
- `delete_playlist_item` — Delete an item from a YouTube playlist. [destructive]
- `delete_video` — Delete a YouTube video owned by the authenticated user. [destructive]
- `download_caption` — Download a YouTube caption track and return a temporary transit URL.
- `get_video_rating` — Get the authenticated user's rating for one or more YouTube videos.
- `list_caption_tracks` — List YouTube caption tracks for a video or caption track IDs.
- `list_channels` — List YouTube channel resources by ID, username, handle, or authenticated owner.
- `list_comment_threads` — List top-level YouTube comment threads for a video, channel, or thread IDs.
- `list_comments` — List YouTube comments by parent comment ID or comment IDs.
- `list_i18n_languages` — List YouTube interface languages.
- `list_i18n_regions` — List YouTube content regions.
- `list_playlist_items` — List videos and resources contained in a YouTube playlist.
- `list_playlists` — List YouTube playlists by ID, channel, or authenticated owner.
- `list_video_categories` — List YouTube video categories for a region or category IDs.
- `list_videos` — List YouTube video resources by ID or chart.
- `post_comment` — Post a top-level public comment on a YouTube video. [write]
- `rate_video` — Set or clear the authenticated user's rating for a YouTube video. [destructive]
- `search` — Search YouTube for videos, channels, or playlists.
- `set_thumbnail_from_url` — Upload and set a custom YouTube video thumbnail from an HTTPS image URL. [write]
- `update_caption` — Update a YouTube caption track's metadata. [write]
- `update_playlist` — Update a YouTube playlist's snippet and status metadata. [write]
- `update_playlist_item` — Update a YouTube playlist item's position or note. [write]
- `update_video` — Update a YouTube video's snippet and status metadata. [write]
- `upload_caption_from_url` — Upload a YouTube caption track from an HTTPS caption file URL. [write]
- `upload_video_from_url` — Upload a YouTube video from an HTTPS media URL using the resumable upload API. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change YouTube state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — YouTube is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/youtube
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- YouTube homepage: https://www.youtube.com/
- API documentation: https://developers.google.com/youtube/v3/docs
