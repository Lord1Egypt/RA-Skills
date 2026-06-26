---
name: golden-hour
description: Automates the "Golden Hour" Instagram engagement hack. Use this skill when a user wants to set up a bot that watches an Instagram Reel/Post for a specific keyword in the comments (like "BOT" or "GOLDEN") and automatically replies to the comment and sends a DM with a link or message.
---

# Golden Hour Automator

This skill provides the script and instructions needed to run a comment-to-DM automation on Instagram. It is designed to boost engagement in the critical first hour (the "Golden Hour") after a post goes live.

## Prerequisites

The user must have:
1. An Instagram Professional/Business account linked to a Facebook Page.
2. A Long-Lived Instagram Graph API Page Access Token (`IG_ACCESS_TOKEN`).
3. Their Instagram Business Account ID (`IG_ACCOUNT_ID`).

Ensure these are set in the environment or `.env` file before running the script.

## Usage

When a user asks to monitor a post for a keyword and send a DM, run the included `ig_golden_hour.py` script.

```bash
uv run {baseDir}/scripts/ig_golden_hour.py \
    --media_id "12345678901234567" \
    --keyword "bot" \
    --dm_text "Here is the link you requested: https://example.com" \
    --duration 60
```

### Parameters:
- `--media_id`: The ID of the specific Instagram post/Reel to monitor. (You may need to query the Graph API `me/media` endpoint to find this for the user's latest post).
- `--keyword`: The trigger word the script watches for in the comments (case-insensitive).
- `--dm_text`: The exact message to send to the user's DMs.
- `--duration`: How many minutes the script should stay alive and monitor the post (default is 60).

### What the Script Does:
1. Polls the comments of the specified `media_id` every 2 minutes.
2. If it finds the `--keyword`, it sends the `--dm_text` directly to the commenter's inbox using the Meta `me/messages` endpoint.
3. It posts a public reply to the comment ("Just sent you a DM with the link! 🚀") to double the post's comment count and boost algorithmic reach.
4. It sends a success notification back to OpenClaw via the `openclaw message` CLI.