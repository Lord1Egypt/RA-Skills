---
name: oo-wakatime
description: "WakaTime (wakatime.com). Use this skill for ANY WakaTime request — searching and reading data. Whenever a task involves WakaTime, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WakaTime"
  author: "OOMOL"
  version: "1.0.1"
  services: ["wakatime"]
  icon: "https://static.oomol.com/logo/third-party/WakaTime.svg"
---

# WakaTime

Operate **WakaTime** through your OOMOL-connected account. This skill calls the `wakatime` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WakaTime. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wakatime" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wakatime" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_all_time_since_today` — Get the total WakaTime coding time logged since the account was created.
- `get_current_user` — Get the currently authenticated WakaTime user.
- `get_stats` — Get WakaTime coding stats for the authenticated user.
- `get_status_bar_today` — Get today's cached WakaTime status bar summary for the authenticated user.
- `get_summaries` — Get WakaTime daily summaries for the authenticated user.
- `list_projects` — List WakaTime projects for the authenticated user.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WakaTime state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WakaTime is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=wakatime
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- WakaTime homepage: https://wakatime.com
