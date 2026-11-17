---
name: oo-qqmusic
description: "QQ Music (y.qq.com). Use this skill for ANY QQ Music request — searching and reading data. Whenever a task involves QQ Music, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "QQ Music"
  author: "OOMOL"
  version: "1.0.2"
  services: ["qqmusic"]
  icon: "https://static.oomol.com/logo/third-party/qqmusic.png"
---

# QQ Music

Operate **QQ Music** through your OOMOL-connected account. This skill calls the `qqmusic` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected QQ Music. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "qqmusic" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "qqmusic" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_chart` — Get one page of a chart. Increment page while hasMore is true.
- `get_daily_mix` — Get the daily personalized song recommendations.
- `get_listening_report` — Get personal daily, weekly, or monthly listening statistics. Only the selected time dimension is populated.
- `get_playlist` — Get one page of a playlist. Increment page while hasMore is true.
- `get_radio` — Get songs from the personalized radio.
- `list_ai_playlists` — List AI-recommended playlists. This endpoint does not accept a prompt or create a playlist.
- `list_charts` — List chart groups and chart previews. Use topId to retrieve a chart.
- `search` — Search songs, albums, playlists, music videos, radios, or singers. Increment page while hasMore is true.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change QQ Music state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — QQ Music is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/qqmusic
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- QQ Music homepage: https://y.qq.com/
- API documentation: https://github.com/tencentmusic/qqmusic-skills
