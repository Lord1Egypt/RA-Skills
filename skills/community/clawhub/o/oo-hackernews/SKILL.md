---
name: oo-hackernews
description: "Hacker News (news.ycombinator.com). Use this skill for ANY Hacker News request — searching and reading data. Whenever a task involves Hacker News, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Hacker News"
  author: "OOMOL"
  version: "1.0.1"
  services: ["hackernews"]
  icon: "https://static.oomol.com/logo/third-party/Hacker%20News.svg"
---

# Hacker News

Operate **Hacker News** through your OOMOL-connected account. This skill calls the `hackernews` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Hacker News needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hackernews" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hackernews" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_ask_stories` — Get the latest Ask HN story IDs from Hacker News.
- `get_best_stories` — Get the best story IDs from Hacker News ranked by score.
- `get_item` — Get a Hacker News item by its numeric ID.
- `get_item_with_id` — Get a Hacker News item with a bounded nested comment tree.
- `get_job_stories` — Get the latest job story IDs from Hacker News.
- `get_latest_posts` — Get the latest Hacker News posts via Algolia search_by_date.
- `get_max_item_id` — Get the current largest Hacker News item ID.
- `get_new_stories` — Get the newest story IDs from Hacker News.
- `get_show_stories` — Get the latest Show HN story IDs from Hacker News.
- `get_top_stories` — Get the top story IDs from Hacker News sorted by front page position.
- `get_updates` — Get recently changed items and user profiles from Hacker News.
- `get_user` — Get a Hacker News user's public profile summary by username.
- `get_user_by_username` — Get a Hacker News user's detailed public profile by username.
- `search_posts` — Search Hacker News posts using Algolia full-text search.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Hacker News state — confirm the exact payload and effect with the user before running.**
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

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Hacker News homepage: https://news.ycombinator.com
