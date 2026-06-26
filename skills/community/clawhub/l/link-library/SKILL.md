---
name: link-library
version: "1.0.0"
description: >
  Personal knowledge base that captures web content (articles, tweets/threads, videos, podcasts, images, PDFs)
  and makes it retrievable for future conversations and writing.
  Use when: (1) User shares a URL with ANY interest signal — asking to summarize, commenting positively,
  saying "有意思/不错/interesting/值得看/学到了", or requesting it be saved,
  (2) User asks to find previously saved content ("我之前存的那篇...", "find that article about..."),
  (3) User needs reference material for writing or discussion,
  (4) User shares Twitter/X, WeChat, YouTube, Bilibili, or any web link and engages with it.
  Interest signals that trigger save: "帮我总结一下", "这篇不错", "有意思", "记一下", "留着以后用",
  "这个观点很好", "学到了", "值得保存", "放进知识库", sharing link + any commentary or opinion,
  asking follow-up questions about link content. Do NOT require literal "save"/"bookmark" keywords.
---

# Link Library — Personal Content Knowledge Base

Save web content with full original text, generate summaries and tags, retrieve semantically.

## Core Rules

1. **Always save original full text** — summaries are for retrieval, originals are for re-reading
2. **Detect interest, don't demand commands** — if user engages with a link, offer to save
3. **Twitter/X is first-class** — tweets, threads, and articles are fully supported

## Interest Detection

When user shares a link, evaluate interest signals:

**Auto-save (no confirmation needed):**
- User explicitly says save/bookmark/记一下/放进知识库
- User asks "帮我总结一下" (summarize implies save-worthy)

**Offer to save (ask once):**
- User shares link + positive commentary ("这篇不错", "有意思", "学到了")
- User asks follow-up questions about link content
- User discusses link content substantively

**Don't save:**
- User shares link just for quick reference in conversation
- User says "不用保存" or similar

## Data Location

All entries in `~/.openclaw/workspace-main/library/`:

```
library/
├── articles/     # Web articles, blog posts, WeChat, Zhihu
├── tweets/       # Twitter/X posts and threads
├── videos/       # YouTube, Bilibili
├── podcasts/     # Podcast episodes
├── papers/       # Academic papers, PDFs
├── images/       # Infographics, visual content
└── misc/         # Everything else
```

## Content Types & Fetch Methods

| Type | URL Patterns | Fetch Method | Template |
|------|-------------|--------------|----------|
| article | Generic web, blog, /post/ | `web_fetch` or `curl -s "https://r.jina.ai/URL"` | `article.md` |
| wechat | mp.weixin.qq.com | `cd ~/.agent-reach/tools/wechat-article-for-ai && python3 main.py "URL"` | `article.md` |
| tweet | x.com, twitter.com /status/ | `xreach tweet URL --json` | `tweet.md` |
| thread | x.com, twitter.com (thread) | `xreach thread URL --json` | `tweet.md` |
| video | youtube.com, youtu.be | `yt-dlp --dump-json "URL"` + subtitle extraction | `video.md` |
| bilibili | bilibili.com | `yt-dlp --dump-json "URL"` + subtitle extraction | `video.md` |
| paper | arxiv.org, .pdf links | `web_fetch` or browser | `paper.md` |
| podcast | Podcast platforms | `web_fetch` metadata | `podcast.md` |
| image | Image URLs | Download + describe | `image.md` |

### Twitter/X Fetch Details

```bash
# Single tweet
xreach tweet URL_OR_ID --json

# Full thread
xreach thread URL_OR_ID --json

# User timeline (for context)
xreach tweets @username -n 20 --json
```

Extract from JSON: `full_text`, `user.screen_name`, `created_at`, `entities`, media URLs.
For threads: concatenate all tweets in order as full content.

### Video Subtitle Extraction

```bash
# Download subtitles
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" \
  --convert-subs vtt --skip-download -o "/tmp/%(id)s" "URL"
# Then read the .vtt file as transcript
```

## Entry Structure

Every entry has two parts:

### 1. YAML Frontmatter (structured metadata)
```yaml
title: "..."
source: "..."           # Platform/domain
url: "..."              # Original URL
author: "..."           # Author or @handle
date_published: "..."   # When content was created
date_saved: "..."       # When we saved it
last_updated: "..."     # Last modification
type: article|tweet|video|podcast|paper|image
tags: [tag1, tag2, ...]
status: unread|read|reviewed
priority: low|normal|high
related: []             # Paths to related entries
```

### 2. Markdown Body (content)
```markdown
# {title}

## Summary
2-3 sentence summary.

## Key Points
- Point 1
- Point 2

## Original Content
THE FULL ORIGINAL TEXT — not truncated, not summarized.
This is the authoritative source for re-reading and quoting.

## Quotes
> Notable quotes worth highlighting

## Notes
Personal observations, connections, action items.

## Related
- [[library/tweets/related-tweet]]
- [[library/articles/related-article]]
```

**⚠️ MANDATORY: Always save original full text in "Original Content" section.**
Summaries and key points are for quick retrieval. The original text is for accurate re-reading and quoting. Never skip saving the full content.

## Filename Convention

`<slugified-title>-<YYYY-MM-DD>.md`

Examples:
- `library/articles/yc-why-not-work-and-startup-2026-03-12.md`
- `library/tweets/garry-tan-on-yc-advice-2026-03-13.md`
- `library/videos/how-to-build-agents-2026-03-13.md`

## Save Workflow

1. **Detect URL** — Parse link from user message
2. **Identify type** — Match URL pattern to content type
3. **Check dedup** — `memory_search("URL or title")` to avoid duplicates
4. **Fetch content** — Use appropriate method from table above
5. **Generate metadata** — Title, summary, key points, tags (3-7)
6. **Write entry** — Use template, fill frontmatter + full original text
7. **Confirm** — Tell user: title, tags, and where it's saved

## Search & Retrieval

```python
# Semantic search
memory_search("创业方法论")
memory_search("Garry Tan 的推文")
memory_search("AI agent 视频教程")

# Read specific entry
memory_get("library/tweets/garry-tan-on-yc-2026-03-13.md")
```

When returning search results, show:
- Title + source + date
- Summary (2 lines max)
- Tags
- Offer to show full original text

## Writing Reference Mode

When user asks to write something using saved content:

1. Search library for relevant entries
2. Read full original text of top matches
3. Synthesize insights, cite sources inline
4. Format citations as `[[library/type/entry-name]]`

## Templates

Located in `templates/`:
- `article.md` — Web articles, blog posts, newsletters
- `tweet.md` — Twitter/X posts and threads
- `video.md` — Videos with transcript
- `podcast.md` — Podcast episodes
- `paper.md` — Academic papers
- `image.md` — Visual content

## Best Practices

- **Save originals religiously** — summaries lose nuance
- **Tag consistently** — reuse existing tags, keep vocabulary tight
- **Link related entries** — build a knowledge graph over time
- **Don't over-ask** — if interest is clear, just save and confirm
