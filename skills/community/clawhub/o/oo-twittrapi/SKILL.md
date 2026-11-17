---
name: oo-twittrapi
description: "TwittrAPI (twittrapi.com). Use this skill for ANY TwittrAPI request — searching and reading data. Whenever a task involves TwittrAPI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TwittrAPI"
  author: "OOMOL"
  version: "1.0.2"
  services: ["twittrapi"]
  icon: "https://static.oomol.com/logo/third-party/twittrapi.svg"
---

# TwittrAPI

Operate **TwittrAPI** through your OOMOL-connected account. This skill calls the `twittrapi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TwittrAPI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "twittrapi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "twittrapi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_community_tweets` — List posts shared in an X Community.
- `get_list_tweets` — List recent posts from the members of an X list, newest first.
- `get_trends` — Get the current trending topics on X for a place, identified by its Yahoo WOEID.
- `get_tweet` — Get one X post by ID with its author, media, and engagement counts, without the reply thread.
- `get_tweet_conversation` — Get the conversation around an X post: the posts it replies to, the post itself, then its replies, one page at a time.
- `get_tweet_quotes` — List posts that quote a given X post.
- `get_tweet_retweeters` — List accounts that reposted a given X post.
- `get_user` — Get an X profile by numeric user ID or by handle, including follower and post counts.
- `get_user_followers` — List accounts that follow an X profile.
- `get_user_following` — List accounts that an X profile follows.
- `get_user_tweets` — List posts from an X profile timeline, newest first, without replies. A pinned post comes first.
- `get_user_tweets_and_replies` — List posts and replies from an X profile, newest first.
- `get_users_by_ids` — Get up to 500 X profiles in one call by numeric user ID.
- `search_tweets` — Search X posts with the same query syntax as the X search box, including operators such as from:, lang:, and since:.
- `search_users` — Search X accounts by name, handle, or bio keywords, as on the People tab of X search.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TwittrAPI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TwittrAPI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/twittrapi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TwittrAPI homepage: https://twittrapi.com
- API documentation: https://twittrapi.com/docs
