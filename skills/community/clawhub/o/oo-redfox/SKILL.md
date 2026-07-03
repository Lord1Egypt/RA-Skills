---
name: oo-redfox
description: "RedFoxHub (redfox.hk). Use this skill for ANY RedFoxHub request — searching and reading data. Whenever a task involves RedFoxHub, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "RedFoxHub"
  author: "OOMOL"
  version: "1.0.1"
  services: ["redfox"]
  icon: "https://static.oomol.com/logo/third-party/redfox.png"
---

# RedFoxHub

Operate **RedFoxHub** through your OOMOL-connected account. This skill calls the `redfox` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected RedFoxHub. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "redfox" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "redfox" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_douyin_user` — Fetch a Douyin account detail payload through RedFoxHub.
- `get_douyin_work` — Fetch a Douyin work detail payload through RedFoxHub by work ID or work URL.
- `get_wechat_account` — Fetch a WeChat Official Account detail payload through RedFoxHub.
- `get_wechat_article` — Fetch a WeChat Official Account article payload through RedFoxHub.
- `get_wechat_article_by_url` — Fetch WeChat Official Account article data through RedFoxHub by article URL.
- `get_xiaohongshu_user` — Fetch a Xiaohongshu account detail payload through RedFoxHub.
- `get_xiaohongshu_work` — Fetch a Xiaohongshu work detail payload through RedFoxHub by work ID or link.
- `list_douyin_user_works` — List works published by a Douyin account through RedFoxHub.
- `list_wechat_account_articles` — List articles published by a WeChat Official Account through RedFoxHub.
- `search_douyin_ai_creations` — Search Douyin AI creation data through RedFoxHub.
- `search_douyin_users` — Search Douyin accounts through RedFoxHub and return the upstream result payload.
- `search_douyin_works` — Search Douyin works through RedFoxHub and return the upstream result payload.
- `search_tiktok_users` — Search TikTok accounts through RedFoxHub.
- `search_wechat_accounts` — Search WeChat Official Accounts through RedFoxHub and return the upstream payload.
- `search_wechat_ai_creations` — Search WeChat Official Account AI creation data through RedFoxHub.
- `search_wechat_articles` — Search WeChat Official Account articles through RedFoxHub and return the upstream payload.
- `search_xiaohongshu_ai_creations` — Search Xiaohongshu AI creation data through RedFoxHub.
- `search_xiaohongshu_users` — Search Xiaohongshu accounts through RedFoxHub and return the upstream result payload.
- `search_xiaohongshu_works` — Search Xiaohongshu works through RedFoxHub and return the upstream result payload.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change RedFoxHub state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — RedFoxHub is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=redfox
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- RedFoxHub homepage: https://redfox.hk
