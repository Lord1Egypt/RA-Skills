---
name: oo-bilibili
description: "Bilibili (bilibili.com). Use this skill for ANY Bilibili request — reading, creating, updating, and deleting data. Whenever a task involves Bilibili, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Bilibili"
  author: "OOMOL"
  version: "1.0.2"
  services: ["bilibili"]
  icon: "https://static.oomol.com/logo/third-party/bilibili.svg"
---

# Bilibili

Operate **Bilibili** through your OOMOL-connected account. This skill calls the `bilibili` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Bilibili. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bilibili" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bilibili" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_anthology` — Create an anthology (文集) that groups articles of the authorized user. [write]
- `delete_anthology` — Delete an anthology of the authorized user. This cannot be undone. [destructive]
- `delete_archive` — Delete one video archive of the authorized user. This cannot be undone. [destructive]
- `delete_articles` — Delete one or more articles of the authorized user. This cannot be undone. [destructive]
- `edit_anthology` — Edit an anthology's name, summary, or cover. Only provided fields change. [write]
- `edit_archive` — Edit descriptive fields of an existing archive (title, partition, cover, description, repost permission). Unchanged fields keep their current values. The video file itself cannot be replaced, and the archive is reviewed again after editing. [write]
- `edit_article` — Edit an existing article. Only provided fields change; the rest keep their current values. The article is reviewed again after editing. The article detail endpoint does not return the comment-section setting, so omitting upClosedReply resets it to the provider default. [write]
- `get_anthology` — Get one anthology with the articles it contains.
- `get_archive` — Get one video archive of the authorized user, including its review state and playback links.
- `get_archive_inc_stats` — Get the authorized user's overall archive increments over the last 30 days: plays, danmaku, comments, favorites, coins, shares, likes, and charges.
- `get_archive_stat` — Get engagement counters of one video archive: plays, danmaku, comments, favorites, coins, shares, likes.
- `get_article` — Get one article of the authorized user, including body HTML, review state, tags, and counters.
- `get_article_card_snippet` — Get the card HTML snippet of a video (BV id) or article (cv id) to embed into article content when submitting or editing an article.
- `get_article_inc_stats` — Get the authorized user's overall article increments over the last 30 days: reads, comments, favorites, likes, shares, coins.
- `get_article_stats` — Get engagement counters of one or more articles: reads, favorites, likes, dislikes, comments, shares, coins.
- `get_user_info` — Get the authorized Bilibili user's public profile (nickname, avatar, openid).
- `get_user_scopes` — List the Bilibili interface permission points (scopes) the authorized user actually granted to this application.
- `get_user_stat` — Get account-level counters of the authorized user: followers, followings, and passed video archives.
- `get_user_union_id` — Get the authorized user's union_id, which is stable across all applications of the same developer. Bilibili must enable this endpoint for your application separately.
- `list_anthologies` — List all anthologies of the authorized user with review state and article counts.
- `list_archive_types` — List Bilibili video partitions (分区). Pick a second-level partition id as the tid of bilibili.upload_video; refresh it periodically because partitions change over time.
- `list_archives` — List the authorized user's video archives with review state, publication time, and playback links.
- `list_article_categories` — List Bilibili article categories. Pick a second-level category id as the categoryId of bilibili.submit_article.
- `list_articles` — List the authorized user's articles with review state and counters, plus the account-level counts by review state.
- `set_anthology_articles` — Replace the article list of an anthology. An article already filed under another anthology is not moved. Pass an empty list to clear the anthology. [write]
- `submit_article` — Submit a new Bilibili article (专栏). Image URLs in the content and covers must come from bilibili.upload_article_image. The article enters review after submission and becomes public once approved. [write]
- `upload_article_image` — Upload an image (jpg/png, up to 5MB) for article content, covers, or banners. The returned Bilibili-hosted URL is what article fields accept. [write]
- `upload_video` — Upload a video file to Bilibili and submit it as a new archive. Files up to 100MB use a single upload; larger files (up to 4GB) are uploaded in 10MB parts. The archive enters review after submission and becomes public once approved. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Bilibili state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Bilibili is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/bilibili
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Bilibili homepage: https://www.bilibili.com
- API documentation: https://bilibili.apifox.cn/doc-885734
