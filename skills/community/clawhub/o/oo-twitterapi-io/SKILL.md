---
name: oo-twitterapi-io
description: "TwitterAPI.io (twitterapi.io). Use this skill for ANY TwitterAPI.io request — reading, creating, updating, and deleting data. Whenever a task involves TwitterAPI.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TwitterAPI.io"
  author: "OOMOL"
  version: "1.0.1"
  services: ["twitterapi_io"]
  icon: "https://static.oomol.com/logo/third-party/twitterapi_io.svg"
---

# TwitterAPI.io

Operate **TwitterAPI.io** through your OOMOL-connected account. This skill calls the `twitterapi_io` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TwitterAPI.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "twitterapi_io" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "twitterapi_io" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_monitored_tweet_user` — Add an X user to real-time Tweet monitoring. [write]
- `add_tweet_filter_rule` — Add a Webhook/WebSocket tweet filter rule. [write]
- `advanced_search_tweets` — Run an advanced Twitter search query.
- `batch_get_users` — Retrieve multiple X user profiles by user ID.
- `check_follow_relationship` — Check whether one X user follows or is followed by another user. [write]
- `delete_tweet_filter_rule` — Delete a Webhook/WebSocket tweet filter rule. [destructive]
- `get_account_info` — Retrieve twitterapi.io account credit information for the API key.
- `get_article` — Retrieve an X article by Tweet ID.
- `get_community_info` — Retrieve information about an X Community.
- `get_community_members` — Retrieve members of an X Community.
- `get_community_moderators` — Retrieve moderators of an X Community.
- `get_community_tweets` — Retrieve Tweets from an X Community.
- `get_list_followers` — Retrieve followers of an X List.
- `get_list_members` — Retrieve members of an X List.
- `get_list_timeline` — Retrieve timeline Tweets from an X List.
- `get_list_tweets` — Retrieve Tweets from an X List.
- `get_space` — Retrieve details for an X Space.
- `get_trends` — Retrieve X trends for a WOEID location.
- `get_tweet_quotes` — Retrieve quote Tweets for a Tweet.
- `get_tweet_replies` — Retrieve replies to a Tweet with twitterapi.io V2 sorting.
- `get_tweet_replies_legacy` — Retrieve replies to an original Tweet with the legacy replies endpoint.
- `get_tweet_retweeters` — Retrieve users who retweeted a Tweet.
- `get_tweet_thread_context` — Retrieve the conversation context around a Tweet.
- `get_tweets` — Retrieve Tweets by Tweet IDs.
- `get_user` — Retrieve an X user profile by screen name.
- `get_user_about` — Retrieve the X About profile information for a screen name.
- `get_user_follower_ids` — Retrieve follower IDs for a user by user ID or screen name.
- `get_user_followers` — Retrieve followers for a user by screen name.
- `get_user_followings` — Retrieve users followed by a screen name.
- `get_user_last_tweets` — Retrieve the latest Tweets from a user by user ID or screen name.
- `get_user_mentions` — Retrieve Tweets mentioning a user.
- `get_user_timeline` — Retrieve a user's profile timeline by user ID.
- `get_user_verified_followers` — Retrieve verified followers for a user by user ID.
- `list_monitored_tweet_users` — List X users monitored for real-time Tweets.
- `list_tweet_filter_rules` — List Webhook/WebSocket tweet filter rules configured for the API key.
- `remove_monitored_tweet_user` — Remove an X user from real-time Tweet monitoring. [destructive]
- `search_all_community_tweets` — Search Tweets from all X Communities by keyword.
- `search_users` — Search X users by keyword.
- `update_tweet_filter_rule` — Update a Webhook/WebSocket tweet filter rule. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TwitterAPI.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TwitterAPI.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=twitterapi_io
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- TwitterAPI.io homepage: https://twitterapi.io
