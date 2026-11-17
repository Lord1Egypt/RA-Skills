---
name: oo-weixin-official-account
description: "WeChat Official Account (mp.weixin.qq.com). Use this skill for ANY WeChat Official Account request — reading, creating, updating, and deleting data. Whenever a task involves WeChat Official Account, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WeChat Official Account"
  author: "OOMOL"
  version: "1.0.2"
  services: ["weixin_official_account"]
  icon: "https://static.oomol.com/logo/third-party/weixin_official_account.svg"
---

# WeChat Official Account

Operate **WeChat Official Account** through your OOMOL-connected account. This skill calls the `weixin_official_account` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WeChat Official Account. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "weixin_official_account" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "weixin_official_account" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_draft` — Create an article draft with 1 to 8 articles. Cover images must be permanent material media_ids. [write]
- `add_material` — Upload a permanent media material. Permanent materials do not expire but count toward the account material quota. Size limits: image 10 MB, voice 2 MB, video 10 MB, thumb 64 KB. Video uploads require title and introduction. [write]
- `add_template` — Add a private template from the template library by its short id and get back the full template_id. Only certified service accounts can use this API. [write]
- `batch_get_draft` — List article drafts in pages of at most 20 items.
- `batch_get_material` — List permanent materials of one type in pages of at most 20 items.
- `batch_get_published` — List successfully published article records in pages of at most 20 items.
- `callback_check` — Check network connectivity between WeChat servers and the callback URL configured for the official account. Fails with errcode 40201 when the account has no callback URL configured.
- `clear_quota` — Reset the monthly API call quota of the connected official account. The account's appId is taken from the credential. Each account can clear its quota at most 10 times per calendar month. [write]
- `delete_draft` — Permanently delete one article draft by media_id. This cannot be undone. [destructive]
- `delete_mass_message` — Delete a mass-sent message by msg_id. articleIdx selects one article inside the message, counting from 1; omit it to delete the whole message. Only messages sent through the API that finished sending can be deleted, and only news and video messages qualify. Deletion invalidates the article content page for everyone; users who already received the message still see its card locally. When several mass sends shared one article, deleting one send invalidates all of them. [destructive]
- `delete_material` — Permanently delete a permanent material by media_id. This cannot be undone. [destructive]
- `delete_publish` — Delete a published article by article_id. index selects one article inside the published message, counting from 1; omit index to delete the whole message. Deleted articles show as unavailable to readers. This cannot be undone. [destructive]
- `delete_template` — Delete one private template by template_id. Only certified service accounts can use this API. This cannot be undone. [destructive]
- `get_all_templates` — List all private templates of the account. Only certified service accounts can use this API.
- `get_api_domain_ip` — Get the WeChat API server IP addresses that the official account servers may call from.
- `get_article_read` — Get the daily read metrics of every published article that was read on the given day. Both dates use YYYY-MM-DD, and WeChat returns data up to yesterday at the latest. The range spans at most 1 day(s) including both ends. Only certified WeChat Official Accounts can use this API.
- `get_article_share` — Get the daily share metrics of every published article that was shared on the given day. Both dates use YYYY-MM-DD, and WeChat returns data up to yesterday at the latest. The range spans at most 1 day(s) including both ends. Only certified WeChat Official Accounts can use this API.
- `get_article_total_detail` — Get the cumulative per-article metrics for everything published in the range. Each article accumulates at most 30 days of data from its publish date. Both dates use YYYY-MM-DD, and WeChat returns data up to yesterday at the latest. The range spans at most 1 day(s) including both ends. Only certified WeChat Official Accounts can use this API.
- `get_biz_summary` — Get the per-day overview metrics aggregated across all content published in the range. Both dates use YYYY-MM-DD, and WeChat returns data up to yesterday at the latest. The range spans at most 30 day(s) including both ends. Only certified WeChat Official Accounts can use this API.
- `get_callback_ip` — Get the WeChat callback server IP addresses. Allowlist them when the official account receives message callbacks.
- `get_draft` — Get the content of one article draft by media_id.
- `get_draft_count` — Get the total number of article drafts of the official account.
- `get_mass_message_status` — Poll the send status of a mass message task by msg_id.
- `get_material` — Get a permanent material by media_id. News materials return their articles and video materials return title, description, and down_url as JSON; image and voice materials are stored in local transit storage.
- `get_material_count` — Get the permanent material counts of the official account, grouped by media type.
- `get_publish_status` — Poll the status of a publish task by publish_id.
- `get_published_article` — Get the content of a published article by article_id.
- `get_temp_media` — Download a temporary media file by media_id. Image, voice, and thumb media are stored in local transit storage; video media returns a video_url instead.
- `get_template_industry` — Get the primary and secondary industry currently set on the account. Only certified service accounts can use this API.
- `get_user_cumulate` — Get the per-day cumulative follower count of the official account. Both dates use YYYY-MM-DD, and WeChat returns data up to yesterday at the latest. The range spans at most 7 day(s) including both ends. Only certified WeChat Official Accounts can use this API.
- `get_user_summary` — Get per-day follower gains and losses of the official account. Both dates use YYYY-MM-DD, and WeChat returns data up to yesterday at the latest. The range spans at most 7 day(s) including both ends. Only certified WeChat Official Accounts can use this API.
- `preview_mass_message` — Preview a mass message to one follower before sending, to check its style and layout. Only certified accounts can use this API. Previewing by WeChat ID (toWxName) is limited to 100 calls per day. [write]
- `publish_draft` — Submit one article draft for publishing. The returned publish_id only means the publish task was accepted; poll get_publish_status for the result. Only certified accounts can publish. [write]
- `send_custom_message` — Send a customer service message to one follower. Only certified accounts can use this API, and the follower must have interacted with the account within the last 48 hours. content is the message-type-specific object documented per msgType. [write]
- `send_mass_message` — Mass-send a message to a list of follower OpenIDs (between 2 and 10000). Only certified accounts can mass-send: certified subscription accounts once per day, certified service accounts 4 times per calendar month. A successful response only means the task was accepted; poll get_mass_message_status for the result. [write]
- `send_mass_message_by_tag` — Mass-send a message to all followers or to one follower tag. Only certified accounts can mass-send: certified subscription accounts once per day, certified service accounts 4 times per calendar month. A successful response only means the task was accepted; poll get_mass_message_status for the result. [write]
- `send_template_message` — Send a template message to one follower. Only certified service accounts can use this API. data maps each template keyword to {value, color?}. [write]
- `set_template_industry` — Set the primary and secondary industry of the account, which decides which template library entries are available. Only certified service accounts can use this API. [write]
- `set_typing_status` — Show or hide the customer service typing indicator for one follower. Only certified accounts can use this API, and the follower must have interacted with the account within the last 48 hours. [write]
- `update_draft` — Replace one article inside a draft. index is zero-based: the first article is 0. [write]
- `upload_article_image` — Upload an image used inside article HTML content and get back its WeChat-hosted URL. Only the returned URL renders inside article content. JPG/PNG only, at most 1 MB. Does not consume the material quota. [write]
- `upload_temp_media` — Upload a temporary media file to the official account. Temporary media expires 3 days after upload. Size limits: image 10 MB, voice 2 MB, video 10 MB, thumb 64 KB. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WeChat Official Account state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WeChat Official Account is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/weixin_official_account
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- WeChat Official Account homepage: https://mp.weixin.qq.com/
- API documentation: https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
