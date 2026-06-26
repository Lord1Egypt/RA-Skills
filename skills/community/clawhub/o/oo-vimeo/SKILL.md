---
name: oo-vimeo
description: "Vimeo (vimeo.com). Use this skill for ANY Vimeo request — reading, creating, updating, and deleting data. Whenever a task involves Vimeo, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Vimeo"
  author: "OOMOL"
  version: "1.0.1"
  services: ["vimeo"]
  icon: "https://static.oomol.com/logo/third-party/vimeo.svg"
---

# Vimeo

Operate **Vimeo** through your OOMOL-connected account. This skill calls the `vimeo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Vimeo. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "vimeo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "vimeo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_video_tags` — Add one or more tags to a Vimeo video. [write]
- `add_video_to_folder` — Add a Vimeo video to a folder. [write]
- `add_video_to_showcase` — Add a Vimeo video to a showcase. [write]
- `create_folder` — Create a Vimeo folder for the authenticated user or a specified Vimeo user. [write]
- `delete_folder` — Delete a Vimeo folder, optionally deleting the videos inside it. [destructive]
- `delete_video` — Delete a Vimeo video by ID. [destructive]
- `delete_video_tag` — Remove a tag from a Vimeo video. [destructive]
- `download_video_file` — Download one Vimeo video file link and store it in connector transit storage.
- `get_current_user` — Get the authenticated Vimeo user profile.
- `get_folder` — Get metadata for a Vimeo folder.
- `get_showcase` — Get metadata for a specific Vimeo showcase.
- `get_video` — Get metadata for a specific Vimeo video.
- `get_video_download_links` — Get temporary downloadable file links for a Vimeo video when Vimeo exposes them.
- `list_folder_videos` — List videos in a Vimeo folder.
- `list_folders` — List folders that belong to the authenticated user or to a specified Vimeo user.
- `list_showcase_videos` — List videos in a Vimeo showcase.
- `list_showcases` — List showcases that belong to the authenticated user or to a specified Vimeo user.
- `list_user_videos` — List videos uploaded by the authenticated user or by a specified Vimeo user.
- `list_video_tags` — List tags attached to a Vimeo video.
- `remove_video_from_folder` — Remove a Vimeo video from a folder without deleting the video. [destructive]
- `remove_video_from_showcase` — Remove a Vimeo video from a showcase. [destructive]
- `replace_video_from_url` — Add a new version to an existing Vimeo video by asking Vimeo to pull the replacement media from a URL. [write]
- `update_folder` — Update a Vimeo folder name. [write]
- `update_video` — Update basic metadata for a Vimeo video without uploading or replacing media. [write]
- `upload_video_from_url` — Upload a new Vimeo video by asking Vimeo to pull the media from an HTTP or HTTPS URL. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Vimeo state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Vimeo is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=vimeo
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Vimeo homepage: https://vimeo.com
