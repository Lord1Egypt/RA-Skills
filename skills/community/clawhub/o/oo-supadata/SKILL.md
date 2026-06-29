---
name: oo-supadata
description: "Supadata (supadata.ai). Use this skill for ANY Supadata request — searching and reading data. Whenever a task involves Supadata, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Supadata"
  author: "OOMOL"
  version: "1.0.2"
  services: ["supadata"]
  icon: "https://static.oomol.com/logo/third-party/supadata.svg"
---

# Supadata

Operate **Supadata** through your OOMOL-connected account. This skill calls the `supadata` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Supadata. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "supadata" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "supadata" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account` — Retrieve Supadata organization, plan, and credit usage details.
- `get_youtube_channel` — Get metadata for a YouTube channel by URL, handle, or ID.
- `get_youtube_playlist` — Get metadata for a YouTube playlist by URL or ID.
- `get_youtube_transcript` — Get a YouTube transcript by video URL or ID.
- `get_youtube_video` — Get metadata for a YouTube video by URL or ID.
- `list_youtube_channel_videos` — List video IDs from a YouTube channel.
- `list_youtube_playlist_videos` — List video IDs from a YouTube playlist.
- `map_web_links` — Extract links found on a website.
- `scrape_web_page` — Extract Markdown content from a web page.
- `search_youtube` — Search YouTube videos, channels, and playlists through Supadata.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Supadata state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Supadata is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=supadata
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Supadata homepage: https://supadata.ai/
