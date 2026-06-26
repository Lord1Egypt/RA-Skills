---
name: multi-post
description: "Multi-platform content publisher via browser automation. Post text+images to Weibo, Xiaohongshu, Zhihu, Twitter/X, Reddit, V2EX, Douban, LinkedIn, and more — all from one command. Use when user says: 发帖, 发微博, 发小红书, 发朋友圈, 万能发帖, 跨平台发布, multi-post, publish everywhere, post to all platforms."
---

# Multi-Post: 万能跨平台发帖

One content, all platforms. Uses browser automation (OpenClaw `browser` tool with `profile="user"`) to publish through logged-in sessions.

## Prerequisites

- User's Chrome must be running (browser tool with `profile="user"`)
- Target platforms must be **logged in** in Chrome
- For image posts: images must be local files accessible to the browser

## Supported Platforms

| Platform | Text | Images | Notes |
|----------|------|--------|-------|
| **微博 (Weibo)** | ✅ | ✅ | 140 char limit display, 2000 actual |
| **小红书 (Xiaohongshu)** | ✅ | ✅ required | Must have ≥1 image |
| **知乎 (Zhihu)** | ✅ | ✅ | 想法(short) or 文章(long) |
| **Twitter/X** | ✅ | ✅ | 280 char limit, thread for longer |
| **Reddit** | ✅ | ✅ | Needs subreddit + title |
| **V2EX** | ✅ | ❌ | Needs node + title |
| **LinkedIn** | ✅ | ✅ | Professional tone recommended |
| **Douban** | ✅ | ✅ | 广播(status update) |

## Workflow

1. **Receive content** — text + optional images + target platforms
2. **Adapt content** per platform (length limits, tone, hashtags)
3. **Execute sequentially** — one platform at a time via browser automation
4. **Report results** — success/fail per platform with URLs

## Content Adaptation Rules

Read `references/platform-rules.md` for per-platform formatting, character limits, and best practices.

## Execution: Browser Automation Steps

For each platform, follow the specific automation sequence in `references/platform-flows.md`.

### General Pattern

```
1. browser navigate → platform compose page
2. browser snapshot → verify logged in
3. browser act (type) → fill content
4. browser act (upload) → attach images (if any)
5. browser act (click) → publish button
6. browser snapshot → confirm success, capture post URL
```

### Error Handling

- **Not logged in** → skip platform, report to user
- **Content too long** → auto-truncate with "..." + link to full version
- **Upload failed** → retry once, then skip images and post text-only
- **Rate limited** → wait and retry once, then skip
- **CAPTCHA** → skip platform, report to user

## Usage Examples

User: "把这段文案发到微博、小红书、知乎"
→ Adapt content × 3 platforms → browser automate × 3 → report

User: "发推特，附上这张图"
→ Single platform with image → browser automate → report

User: "全平台发布这个产品推广"
→ All logged-in platforms → adapt × N → browser automate × N → report
