---
name: oo-linux-do
description: "Linux DO (linux.do). Use this skill for ANY Linux DO request — searching and reading data. Whenever a task involves Linux DO, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Linux DO"
  author: "OOMOL"
  version: "1.0.2"
  services: ["linux_do"]
  icon: "https://static.oomol.com/logo/third-party/linux_do.svg"
---

# Linux DO

Operate **Linux DO** through your OOMOL-connected account. This skill calls the `linux_do` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Linux DO needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "linux_do" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "linux_do" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `list_badge_grants` — List recent grants of a Linux DO badge. RSS endpoint: GET https://linux.do/badges/{id}.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_category_tag_topics` — List topics with a tag inside a category. RSS endpoint: GET https://linux.do/tags/c/{slug}/{id}/{tag}.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_category_topics` — List topics in a Linux DO category. RSS endpoint: GET https://linux.do/c/{slug}/{id}.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_group_mentions` — List posts mentioning a Linux DO group. RSS endpoint: GET https://linux.do/g/{name}/mentions.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_group_posts` — List posts by members of a Linux DO group. RSS endpoint: GET https://linux.do/g/{name}/posts.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_hot_topics` — List public hot/trending topics from Linux DO. RSS endpoint: GET https://linux.do/hot.rss. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_latest_posts` — List the latest public posts across Linux DO. RSS endpoint: GET https://linux.do/posts.rss. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_latest_topics` — List the latest public topics from Linux DO. RSS endpoint: GET https://linux.do/latest.rss. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_tag_topics` — List topics with a Linux DO tag. RSS endpoint: GET https://linux.do/tag/{tag}.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_top_topics` — List public top topics from Linux DO for a time period. RSS endpoint: GET https://linux.do/top.rss?period={period} (daily/weekly/monthly/quarterly/yearly/all). On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_topic_posts` — List posts within a Linux DO topic. RSS endpoint: GET https://linux.do/t/{slug}/{id}.rss (slug defaults to "topic"). Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_user_posts` — List posts by a Linux DO user. RSS endpoint: GET https://linux.do/u/{username}/activity.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.
- `list_user_topics` — List topics created by a Linux DO user. RSS endpoint: GET https://linux.do/u/{username}/activity/topics.rss. Returns 404 when the target is private or not accessible anonymously; a 404 does not necessarily mean the resource does not exist. On a 429/rate-limit error, retry later or fetch the endpoint URL directly from a local network.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Linux DO state — confirm the exact payload and effect with the user before running.**
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

- Linux DO homepage: https://linux.do
