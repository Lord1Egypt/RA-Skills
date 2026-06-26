---
name: oo-pexels
description: "Pexels (pexels.com). Use this skill for ANY Pexels request — searching and reading data. Whenever a task involves Pexels, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pexels"
  author: "OOMOL"
  version: "1.0.1"
  services: ["pexels"]
  icon: "https://static.oomol.com/logo/third-party/Pexels.svg"
---

# Pexels

Operate **Pexels** through your OOMOL-connected account. This skill calls the `pexels` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pexels. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pexels" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pexels" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `collection_media` — Retrieve the photo and video items inside a Pexels collection, with optional type and sort filters.
- `curated_photos` — Retrieve the current curated photo feed from Pexels with pagination controls.
- `featured_collections` — Retrieve featured Pexels collections with pagination controls.
- `get_photo` — Retrieve the full metadata for a single Pexels photo by photo id.
- `get_video` — Retrieve the full metadata for a single Pexels video by video id.
- `my_collections` — Retrieve collections owned by the authenticated Pexels account.
- `popular_videos` — Retrieve the current popular Pexels videos with pagination and optional dimension or duration filters.
- `search_photos` — Search Pexels photos by keyword with optional orientation, size, color, locale, and pagination filters.
- `search_videos` — Search Pexels videos by keyword with optional orientation, size, and pagination filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pexels state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pexels is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=pexels
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Pexels homepage: https://www.pexels.com
