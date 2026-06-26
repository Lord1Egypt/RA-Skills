---
name: poetry-daily-art
description: Generate daily Chinese classical poetry art cards — AI-generated landscape painting paired with poem text, delivered to chat. Use when the user asks for poetry illustration, poem art card, daily poem image, 诗词配图, 每日诗歌图片, or when a cron job triggers the daily poetry art task.
---

# Poetry Daily Art

Generate an AI landscape painting inspired by a Chinese classical poem and deliver it as a card with the poem's full text.

## Workflow

1. **Identify today's poem** — Read `data/poem_study_progress.json` to get the latest studied poem title.
2. **Generate image** — Run `scripts/generate_image.sh` (requires `mmx` CLI, MiniMax image model).
3. **Compose caption** — Format:
   ```
   🌅 《<poem_title>》— <author>（<dynasty>）

   <full poem text, preserving original line breaks>

   愿你今天充满诗意与力量 🌸
   ```
4. **Deliver** — Send via `message` tool with `media` (image path) and `caption`.

## Data Sources

- `data/poem_study_progress.json` — Tracks studied poems (name, date). The last entry is today's poem.
- Poem full text — Retrieved from the agent's poetry knowledge or `archive/poem/` directory.

## Script: `scripts/generate_image.sh`

Reads the latest poem title from progress JSON, generates a 9:16 landscape image via `mmx image`, outputs `FOUND:<path>` and `TITLE:<title>`.

### Prerequisites
- `mmx` CLI (MiniMax, `npm install -g mmx-cli`)
- MiniMax API key configured

### Usage
```bash
bash scripts/generate_image.sh
```

Output:
```
今日诗词：卜算子·咏梅
生成图片中...
FOUND:/path/to/image_001.jpg
TITLE:卜算子·咏梅
```

## Cron Integration

Schedule at **07:30 Asia/Hong_Kong** (after the 07:15 poetry study push, so the progress file has today's poem).

Prompt template for cron:
```
执行每日诗词配图任务：
1. 运行 scripts/generate_image.sh
2. 解析 FOUND/TITLE
3. 查找诗词原文（含作者、朝代）
4. 用 message 工具发送图片 + caption 到 Telegram
```

## Style Guide

- Image: Chinese ink wash painting + photography blend, 9:16 portrait, no text in image
- Caption: Clean, poem-first, minimal decoration (one emoji header, one closing line)
- Mood: Match the poem's emotional tone (heroic → dramatic lighting; melancholic → misty dusk; joyful → warm sunrise)
