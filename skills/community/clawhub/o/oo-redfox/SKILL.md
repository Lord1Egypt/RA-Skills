---
name: oo-redfox
description: "RedFoxHub (redfox.hk). Use this skill for ANY RedFoxHub request — reading, creating, and updating data. Whenever a task involves RedFoxHub, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "RedFoxHub"
  author: "OOMOL"
  version: "1.0.8"
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

- `get_account_balance` — Get the points balance associated with the connected RedFoxHub API key.
- `get_autohome_article` — Get the content and metadata of an Autohome article.
- `get_autohome_video` — Get details of an Autohome video.
- `get_baidu_search` — Get the status and results of a Baidu AI search task.
- `get_baijiahao_article` — Get the content and metadata of a Baijiahao article.
- `get_baijiahao_user` — Get details of a Baijiahao account.
- `get_baijiahao_video` — Get details of a Baijiahao video.
- `get_bilibili_audio` — Extract an audio download URL from a Bilibili video.
- `get_bilibili_transcription` — Get the status and transcript of a Bilibili transcription task.
- `get_bilibili_user` — Get details about a Bilibili account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_bilibili_video_download` — Resolve a Bilibili video URL into downloadable media links.
- `get_bilibili_work` — Get a Bilibili work by its BV ID or URL. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_deepseek_search` — Get the status and results of a DeepSeek AI search task.
- `get_dongchedi_user_works` — List posts published by a Dongchedi account.
- `get_dongchedi_work` — Get details of a Dongchedi post.
- `get_doubao_search` — Get the status and results of a Doubao AI search task.
- `get_douyin_transcription` — Get the status and transcript of a Douyin transcription task.
- `get_douyin_user` — Get details about a Douyin account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_douyin_video_download` — Resolve a Douyin video URL into downloadable media links.
- `get_douyin_work` — Get a Douyin work by its ID or URL. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_douyin_work_broad` — Get a Douyin post from the broad database. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `get_gemini_banana_2_1_generation` — Get the status and output of a Gemini Banana 2.1 generation task.
- `get_gpt_image_2_5_generation` — Get the status and output of a GPT Image 2.5 generation task.
- `get_gpt_image_2_generation` — Get the status and output of a GPT Image 2 generation task.
- `get_instagram_post` — Get an Instagram post by shortcode or URL.
- `get_instagram_user` — Get an Instagram account by username or user ID.
- `get_instagram_video_download` — Resolve an Instagram video URL into downloadable media links.
- `get_kimi_search` — Get the status and results of a Kimi AI search task.
- `get_kuaishou_transcription` — Get the status and transcript of a Kuaishou transcription task.
- `get_kuaishou_video_download` — Resolve a Kuaishou video URL into downloadable media links.
- `get_kuaishou_work` — Get details about a Kuaishou work. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `get_qwen_search` — Get the status and results of a Qwen AI search task.
- `get_seedance_video_generation` — Get the status and output of a Seedance video generation task.
- `get_seedream_lite_generation` — Get the status and output of a Seedream Lite generation task.
- `get_seedream_pro_generation` — Get the status and output of a Seedream Pro generation task.
- `get_tiktok_video_download` — Resolve a TikTok video URL into downloadable media links.
- `get_tiktok_work` — Get a TikTok video by its ID.
- `get_toutiao_work` — Get details about a Toutiao work.
- `get_wechat_account` — Get details about a WeChat Official Account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_wechat_account_broad` — Get a WeChat Official Account from the broad database. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `get_wechat_article` — Get a WeChat Official Account article by its UUID. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_wechat_article_broad` — Get a WeChat Official Account article from the broad database. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `get_wechat_article_by_url` — Get a WeChat Official Account article by its URL.
- `get_wechat_channel_transcription` — Get the status and transcript of a WeChat channel transcription task.
- `get_wechat_channel_video_download` — Resolve a WeChat channel video URL into downloadable media links.
- `get_wechat_channel_work` — Get details about a WeChat Channel work. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `get_wechat_channel_work_by_url` — Get a WeChat Channels post by its shared URL.
- `get_weibo_user` — Get details of a Weibo account.
- `get_weibo_work` — Get details of a Weibo post.
- `get_x_post` — Get an X post by its ID.
- `get_x_user` — Get an X account by username or user ID.
- `get_x_video_download` — Resolve an X video URL into downloadable media links.
- `get_xiaohongshu_comments` — Get the status and collected comments of a Xiaohongshu comment task. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `get_xiaohongshu_transcription` — Get the status and transcript of a Xiaohongshu transcription task.
- `get_xiaohongshu_user` — Get details about a Xiaohongshu account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_xiaohongshu_video_download` — Resolve a Xiaohongshu video URL into downloadable media links.
- `get_xiaohongshu_work` — Get a Xiaohongshu work by its ID or link. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `get_yiche_article` — Get the content and metadata of a Yiche article.
- `get_yiche_video` — Get details of a Yiche video.
- `get_youtube_subtitles` — Get subtitle tracks for a YouTube video.
- `get_youtube_transcript` — Get the transcript of a YouTube video.
- `get_youtube_video` — Get details of a YouTube video.
- `get_youtube_video_download` — Resolve a YouTube video URL into downloadable media links.
- `get_yuanbao_search` — Get the status and results of a Yuanbao AI search task.
- `list_aggregated_hot_topics` — List trending topics aggregated across platforms for a time range.
- `list_api_usage` — List API consumption records associated with the connected RedFoxHub API key.
- `list_autohome_user_works` — List posts published by an Autohome account.
- `list_bilibili_user_works` — List works published by a Bilibili account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `list_douyin_daily_rising_works` — List Douyin posts gaining popularity over a day. Data is updated on a T+1 schedule, not in real time.
- `list_douyin_hot_users` — List ranked Douyin accounts by category. Data is updated on a T+1 schedule, not in real time.
- `list_douyin_hot_works` — List popular Douyin posts by category and date. Data is updated on a T+1 schedule, not in real time.
- `list_douyin_user_works` — List works published by a Douyin account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `list_douyin_user_works_broad` — List posts by a Douyin account in the broad database. Data is updated on a T+1 schedule, not in real time.
- `list_douyin_weekly_rising_works` — List Douyin posts gaining popularity over a week. Data is updated on a T+1 schedule, not in real time.
- `list_instagram_post_comments` — List comments on an Instagram post.
- `list_kuaishou_user_works` — List works published by a Kuaishou account. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `list_platform_hot_topics` — List trending topics on a selected platform for a date range.
- `list_tiktok_comment_replies` — List replies to a TikTok video comment.
- `list_tiktok_topic_works` — List TikTok videos associated with a topic.
- `list_tiktok_user_following` — List accounts followed by a TikTok user.
- `list_tiktok_user_liked_works` — List videos liked by a TikTok user.
- `list_tiktok_user_works` — List videos published by a TikTok account.
- `list_tiktok_work_comments` — List comments on a TikTok video.
- `list_toutiao_user_works` — List works published by a Toutiao account.
- `list_toutiao_work_comments` — List comments on a Toutiao work.
- `list_wechat_account_articles` — List articles published by a WeChat Official Account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `list_wechat_account_articles_broad` — List articles by a WeChat Official Account in the broad database. Data is updated on a T+1 schedule, not in real time.
- `list_wechat_account_rankings` — List WeChat Official Account rankings. Data is updated on a T+1 schedule, not in real time.
- `list_wechat_channel_user_works` — List works published by a WeChat Channel account. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `list_wechat_headline_growth` — List WeChat Official Account headline articles ranked by readership growth.
- `list_wechat_high_read_articles` — List WeChat Official Account articles with high readership. Data is updated on a T+1 schedule, not in real time.
- `list_wechat_original_viral_articles` — List popular original articles from WeChat Official Accounts. Data is updated on a T+1 schedule, not in real time.
- `list_wechat_reading_growth` — List WeChat Official Account articles ranked by readership growth. Data is updated on a T+1 schedule, not in real time.
- `list_weibo_hot_searches` — List trending Weibo search terms.
- `list_x_hot_users` — List popular X accounts by category. Uses the curated database.
- `list_x_post_comments` — List replies to an X post.
- `list_x_user_following` — List accounts followed by an X user.
- `list_x_user_posts` — List posts published by an X account.
- `list_xiaohongshu_breakout_notes` — List Xiaohongshu notes that outperform their authors’ usual engagement. Data is updated on a T+1 schedule, not in real time.
- `list_xiaohongshu_daily_viral_notes` — List popular Xiaohongshu notes for a day. Data is updated on a T+1 schedule, not in real time.
- `list_xiaohongshu_hot_users` — List ranked Xiaohongshu accounts by category. Data is updated on a T+1 schedule, not in real time.
- `list_xiaohongshu_user_works` — List notes published by a Xiaohongshu account. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `list_xiaohongshu_weekly_viral_notes` — List popular Xiaohongshu notes for a week. Data is updated on a T+1 schedule, not in real time.
- `list_yiche_user_works` — List posts published by a Yiche account.
- `list_youtube_video_comments` — List comments on a YouTube video.
- `parse_video` — Resolve a shared video URL into media metadata and download links.
- `search_autohome_works` — Search Autohome posts by keyword.
- `search_baijiahao_users` — Search Baijiahao accounts by keyword.
- `search_baijiahao_works` — Search Baijiahao posts by keyword.
- `search_bilibili_users` — Search Bilibili accounts by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_bilibili_works` — Search Bilibili works by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_dongchedi_users` — Search Dongchedi accounts by keyword.
- `search_dongchedi_works` — Search Dongchedi posts by keyword.
- `search_douyin_ai_creations` — Search Douyin works related to AI creation. Data is updated on a T+1 schedule, not in real time.
- `search_douyin_users` — Search Douyin accounts by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_douyin_users_broad` — Search Douyin accounts by name in the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_douyin_works` — Search Douyin works by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_douyin_works_broad` — Search Douyin posts by keyword in the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_hot_topics` — Search trending topics by keywords, platforms and date range.
- `search_instagram` — Search Instagram by keyword, with pagination.
- `search_kuaishou_users` — Search Kuaishou accounts by name. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_kuaishou_works` — Search Kuaishou works by keyword. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_tiktok_topics` — Search TikTok topics by keyword.
- `search_tiktok_users` — Search TikTok accounts by keyword.
- `search_tiktok_works` — Search TikTok videos by keyword.
- `search_toutiao_users` — Search Toutiao accounts by keyword.
- `search_toutiao_works` — Search Toutiao works by keyword.
- `search_wechat_accounts` — Search WeChat Official Accounts by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_wechat_accounts_broad` — Search WeChat Official Accounts by keyword in the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_wechat_ai_creations` — Search WeChat Official Account articles related to AI creation. Data is updated on a T+1 schedule, not in real time.
- `search_wechat_articles` — Search WeChat Official Account articles by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_wechat_articles_broad` — Search WeChat Official Account articles in the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_wechat_channel_users` — Search WeChat Channel accounts by name. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_wechat_channel_works` — Search WeChat Channel works by keyword. Uses the broad database. Data is updated on a T+1 schedule, not in real time.
- `search_weibo_users` — Search Weibo accounts by keyword.
- `search_weibo_works` — Search Weibo posts by keyword.
- `search_x_posts` — Search X posts by keyword.
- `search_xiaohongshu_ai_creations` — Search Xiaohongshu works related to AI creation. Data is updated on a T+1 schedule, not in real time.
- `search_xiaohongshu_users` — Search Xiaohongshu accounts by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_xiaohongshu_viral_notes` — Search popular Xiaohongshu notes by keyword and date. Data is updated on a T+1 schedule, not in real time.
- `search_xiaohongshu_works` — Search Xiaohongshu notes by keyword. Uses the curated database. Data is updated on a T+1 schedule, not in real time.
- `search_yiche_users` — Search Yiche accounts by keyword.
- `search_yiche_works` — Search Yiche posts by keyword.
- `search_youtube_videos` — Search YouTube videos by keyword.
- `search_zhihu_works` — Search Zhihu content by keyword.
- `submit_baidu_search` — Start an AI search with Baidu and return a task ID. [write]
- `submit_bilibili_transcription` — Start transcribing a Bilibili video and return a task ID. [write]
- `submit_deepseek_search` — Start an AI search with DeepSeek and return a task ID. [write]
- `submit_doubao_search` — Start an AI search with Doubao and return a task ID. [write]
- `submit_douyin_transcription` — Start transcribing a Douyin video and return a task ID. [write]
- `submit_gemini_banana_2_1_generation` — Start a Gemini Banana 2.1 generation task and return its task ID. [write]
- `submit_gpt_image_2_5_generation` — Start a GPT Image 2.5 generation task and return its task ID. [write]
- `submit_gpt_image_2_generation` — Start a GPT Image 2 generation task and return its task ID. [write]
- `submit_kimi_search` — Start an AI search with Kimi and return a task ID. [write]
- `submit_kuaishou_transcription` — Start transcribing a Kuaishou video and return a task ID. [write]
- `submit_qwen_search` — Start an AI search with Qwen and return a task ID. [write]
- `submit_seedance_video_generation` — Start a Seedance video generation task and return its task ID. [write]
- `submit_seedream_lite_generation` — Start a Seedream Lite generation task and return its task ID. [write]
- `submit_seedream_pro_generation` — Start a Seedream Pro generation task and return its task ID. [write]
- `submit_wechat_channel_transcription` — Start transcribing a WeChat channel video and return a task ID. [write]
- `submit_xiaohongshu_comments` — Start collecting comments on a Xiaohongshu note and return a task ID. Uses the broad database. Data is updated on a T+1 schedule, not in real time. [write]
- `submit_xiaohongshu_transcription` — Start transcribing a Xiaohongshu video and return a task ID. [write]
- `submit_yuanbao_search` — Start an AI search with Yuanbao and return a task ID. [write]

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
  https://console.oomol.com/connections/redfox
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- RedFoxHub homepage: https://redfox.hk
- API documentation: https://redfox.hk/story/web/api/doc/platforms
