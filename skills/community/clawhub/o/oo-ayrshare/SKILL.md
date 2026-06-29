---
name: oo-ayrshare
description: "Ayrshare (ayrshare.com). Use this skill for ANY Ayrshare request — reading, creating, updating, and deleting data. Whenever a task involves Ayrshare, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Ayrshare"
  author: "OOMOL"
  version: "1.0.3"
  services: ["ayrshare"]
  icon: "https://static.oomol.com/logo/third-party/ayrshare.png"
---

# Ayrshare

Operate **Ayrshare** through your OOMOL-connected account. This skill calls the `ayrshare` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Ayrshare. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ayrshare" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ayrshare" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_post_length` — Check weighted social post length and platform validity using Ayrshare's post length validator. [write]
- `delete_post` — Delete one or more Ayrshare posts, delete all pending scheduled posts, or mark a post as manually deleted. [destructive]
- `get_post` — Get one Ayrshare post by top-level Ayrshare post ID, including status and per-platform results. [write]
- `get_post_analytics` — Get real-time analytics for an Ayrshare post, optionally limited to selected social platforms. [write]
- `get_user_profile` — Get Ayrshare account or user profile details, including linked social accounts and usage metadata.
- `list_post_history` — List Ayrshare post history with optional filters for date range, status, type, and social platforms. [write]
- `publish_post` — Publish or schedule a social media post through Ayrshare using a JSON-friendly first-pass field set. [write]
- `retry_post` — Retry an Ayrshare post whose previous publish attempt failed, returning the new pending post status. [write]
- `update_post` — Update mutable Ayrshare post metadata such as scheduleDate, approval status, notes, pause state, comments, or YouTube visibility. [write]
- `validate_post` — Validate an Ayrshare post payload before publishing, including platform and media URL checks. [write]
- `verify_media_url` — Verify that a media URL exists and is accessible to Ayrshare.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Ayrshare state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Ayrshare is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=ayrshare
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Ayrshare homepage: https://www.ayrshare.com/
