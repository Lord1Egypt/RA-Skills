---
name: multimodal-memory
description: "Remember and retrieve visual content from conversations. Use when: (1) user sends an image, photo, chart, diagram, or screenshot and wants it saved/remembered; (2) user asks to capture or remember a website, URL, or web page UI; (3) user asks what you've seen before, wants to recall a past image, or searches visual memories; (4) user sends an image to find similar past content."
metadata: {"clawdbot":{"emoji":"🧠","os":["darwin","linux"],"requires":{"bins":["python3"]}}}
---

# Multimodal Memory

Store and retrieve visual content — user images, charts, diagrams, website UIs — across conversations.

## Important: Image Analysis

**The primary model may not support vision.** Always use `analyze.py` to analyze images — it calls GPT-4o directly via API and does not rely on your own vision capability.

## Storage Location

All data lives in `~/.multimodal-memory/`:
- `images/` — saved copies of captured images
- `metadata.db` — SQLite database (auto-created)
- `memory.md` — human-readable summary (auto-updated)

Read `~/.multimodal-memory/memory.md` at session start for a quick overview.

## Scenarios & Actions

### 1. User Sends an Image / Chart / Diagram

When a user sends an image, OpenClaw saves it locally and provides the file path in the message context (look for a path like `/tmp/...` or `~/.openclaw/...`).

Run `analyze.py` with that path — it calls GPT-4o to analyze and stores the result automatically:

```bash
python {baseDir}/scripts/analyze.py \
  --image-path "/absolute/path/to/image.jpg" \
  --source "image"
```

For charts use `--source "chart"`, for diagrams use `--source "image"`.

**If you cannot find the file path in the message context**, ask the user:
> "请问这张图片保存在哪个路径？或者你可以直接粘贴文件路径给我。"

### 2. User Asks to Capture / Remember a Website

Step 1 — take the screenshot:
```bash
python {baseDir}/scripts/capture_url.py --url "https://example.com"
```
The script prints the saved screenshot path.

Step 2 — analyze and store it:
```bash
python {baseDir}/scripts/analyze.py \
  --image-path "/path/printed/above.png" \
  --source "website" \
  --url "https://example.com"
```

### 3. User Searches by Text

```bash
python {baseDir}/scripts/search.py --query "login screen dark theme"
```

Show results with descriptions and image paths.

### 4. User Sends an Image to Search (find similar memories)

Step 1 — analyze the query image to get its description:
```bash
python {baseDir}/scripts/analyze.py \
  --image-path "/path/to/query/image.jpg" \
  --source "image"
```

Step 2 — the analysis is stored; also search for similar past content using the description keywords:
```bash
python {baseDir}/scripts/search.py --query "key concepts from the analysis output"
```

Step 3 — present matching memories and explain why they're relevant.

### 5. List Recent Memories

```bash
python {baseDir}/scripts/list.py --limit 20
```

## Core Rules

- **Never try to analyze images yourself** — always delegate to `analyze.py`.
- After storing, confirm to user: description + tags saved.
- Image paths must be **absolute**.
- The `--extra-tags` arg accepts comma-separated additional tags.

## One-Time Setup for URL Capture

If `capture_url.py` fails:
```bash
pip install playwright && python -m playwright install chromium
```

## Script Reference

| Script | Purpose | Key args |
|--------|---------|----------|
| `analyze.py` | Analyze image with GPT-4o + store | `--image-path`, `--source`, `--url`, `--extra-tags` |
| `store.py` | Store pre-analyzed result | `--image-path`, `--description`, `--tags`, `--source`, `--url` |
| `search.py` | Text search | `--query`, `[--limit N]` |
| `list.py` | List memories | `[--limit N]` |
| `capture_url.py` | Screenshot a URL | `--url` |
