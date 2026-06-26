---
name: oo-googlephotos
description: "Google Photos (google.com). Use this skill for ANY Google Photos request — reading, creating, updating, and deleting data. Whenever a task involves Google Photos, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Photos"
  author: "OOMOL"
  version: "1.0.1"
  services: ["googlephotos"]
  icon: "https://static.oomol.com/logo/third-party/Google%20Photos.svg"
---

# Google Photos

Operate **Google Photos** through your OOMOL-connected account. This skill calls the `googlephotos` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Photos. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googlephotos" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googlephotos" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_enrichment` — Add an enrichment item to a Google Photos album. [write]
- `batch_add_media_items` — Add existing Google Photos media items to an album. [write]
- `batch_create_media_items` — Batch create Google Photos media items from URLs or base64 payloads. [write]
- `batch_get_media_items` — Fetch multiple Google Photos media items by ID.
- `create_album` — Create a Google Photos album. [write]
- `create_picker_session` — Create a Google Photos Picker session for selecting items from the user's library. [write]
- `delete_picker_session` — Delete a Google Photos Picker session. [destructive]
- `get_album` — Fetch one Google Photos album by ID.
- `get_media_item_download` — Download a Google Photos Library API media item created by this application through connector file transit.
- `get_picked_media_item_download` — Download a picked Google Photos media item through connector file transit using its trusted temporary base URL.
- `get_picker_session` — Get the current state of a Google Photos Picker session.
- `list_albums` — List Google Photos albums visible to the current application connection. If you need the user to choose from their existing Google Photos library, use the Picker actions instead.
- `list_media_items` — List Google Photos Library API media items created by this application.
- `list_picked_media_items` — List media items selected from the user's Google Photos library in a picker session.
- `search_media_items` — Search Google Photos Library API media items created by this application.
- `update_album` — Update a Google Photos album title or cover photo. [write]
- `update_media_item` — Update a Google Photos media item description. [write]
- `upload_media` — Upload one media item into Google Photos from a URL or base64 payload. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Photos state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Photos is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=googlephotos
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Photos homepage: https://www.google.com/photos/about/
