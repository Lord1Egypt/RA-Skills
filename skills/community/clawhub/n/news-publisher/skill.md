# OpenClaw News Publisher

**Multi-platform news publishing automation from Markdown**

## Overview

OpenClaw News Publisher is a CLI-based tool that automates news article distribution across multiple platforms. Write once in Markdown, publish everywhere with a single command.

## Core Capabilities

### 1. Multi-Platform Publishing
- **RSS Feed**: Full implementation with automatic feed generation
- **WeChat Official Account**: Framework ready (API pending)
- **Twitter/X**: Framework ready (OAuth pending)
- **Toutiao (今日头条)**: Placeholder
- **YouTube**: Placeholder
- **Douyin (抖音)**: Placeholder

### 2. Markdown-First Workflow
- Write news in standard Markdown with YAML Front Matter
- Template system for different content types
- Preview before publishing
- Automatic content extraction and formatting

### 3. Publishing Features
- Automatic platform fallback on failures
- Dry-run mode for testing
- Publishing history tracking with JSON records
- Platform-specific formatting (e.g., Twitter 280 char limit)
- Batch publishing to multiple platforms

### 4. Content Management
- Draft system for work-in-progress articles
- Published archive organized by date
- Template-based article creation
- Front Matter metadata support

## Installation

```bash
# Clone repository
git clone https://github.com/ZhenRobotics/openclaw-news-publisher.git
cd openclaw-news-publisher

# Install dependencies
npm install

# Configure platforms
cp .env.example .env
# Edit .env with your credentials

# Verify installation
./agents/news-cli.sh help
```

## Quick Start

### 1. Create News Article

```bash
# Create from template
openclaw-news create "AI Breakthrough in 2026"

# Or use script directly
./scripts/create-news.sh "My News Title" --template tech-news
```

This generates: `news/drafts/ai-breakthrough-TIMESTAMP.md`

### 2. Edit Article

```markdown
---
title: "AI Breakthrough in 2026"
author: "Your Name"
category: "Technology"
tags: ["AI", "Innovation"]
platforms: ["rss", "twitter"]
---

# AI Breakthrough in 2026

Your article content here...
```

### 3. Preview Article

```bash
openclaw-news preview news/drafts/ai-breakthrough-*.md
```

Shows: title, author, word count, content preview

### 4. Publish

```bash
# Publish to all configured platforms
openclaw-news publish news/drafts/ai-breakthrough-*.md

# Publish to specific platforms
openclaw-news publish news/drafts/my-news.md --platforms rss,twitter

# Dry run (preview only, no actual publishing)
openclaw-news publish news/drafts/my-news.md --dry-run
```

### 5. List Published Articles

```bash
openclaw-news list
```

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Create news draft | `openclaw-news create "Title"` |
| `preview` | Preview article | `openclaw-news preview <file>` |
| `publish` | Publish to platforms | `openclaw-news publish <file>` |
| `list` | List published articles | `openclaw-news list` |
| `help` | Show help | `openclaw-news help` |

## Configuration

### Platform Credentials (.env)

```bash
# Platform priority (comma-separated)
PUBLISH_PLATFORMS="rss,wechat,twitter"

# RSS Configuration
RSS_SITE_URL="https://your-site.com"
RSS_FEED_URL="https://your-site.com/feed.xml"

# WeChat
WECHAT_APP_ID="wx..."
WECHAT_APP_SECRET="..."

# Twitter
TWITTER_API_KEY="..."
TWITTER_API_SECRET="..."
TWITTER_ACCESS_TOKEN="..."

# (See .env.example for full configuration)
```

## Article Format

### Front Matter Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `title` | ✅ | Article title | "AI News" |
| `author` | ⬜ | Author name | "John Doe" |
| `category` | ⬜ | Category | "Technology" |
| `tags` | ⬜ | Tag array | `["AI", "Tech"]` |
| `platforms` | ⬜ | Target platforms | `["rss", "twitter"]` |
| `coverImage` | ⬜ | Cover image path | "img/cover.jpg" |
| `draft` | ⬜ | Draft status | `true` or `false` |

### Example Article

```markdown
---
title: "Breaking: New AI Model Released"
author: "Tech Reporter"
category: "Technology"
tags: ["AI", "Machine Learning"]
platforms: ["rss", "twitter", "wechat"]
coverImage: "images/ai-model.jpg"
draft: false
---

# Breaking: New AI Model Released

## Summary
A revolutionary AI model has been announced...

## Details
The new model demonstrates...

### Key Features
- **Performance**: 50% improvement
- **Efficiency**: Reduced compute costs
- **Applications**: Healthcare, finance

## Conclusion
This breakthrough marks...
```

## Platform-Specific Behavior

### RSS
- Generates RSS 2.0 feed at `public/feed.xml`
- Converts Markdown to HTML automatically
- Includes last 20 articles
- Updates on each publish

### Twitter
- Automatically truncates to 280 characters
- Extracts hashtags from article tags
- Uses summary or first paragraph

### WeChat
- Extracts title, author, content
- Prepares for draft article creation
- (Full API integration pending)

## Use Cases

### 1. News Website
```bash
# Daily news workflow
openclaw-news create "Today's Tech News"
# Edit article...
openclaw-news publish news/drafts/todays-tech-news-*.md --platforms rss
```

### 2. Multi-Platform Content Distribution
```bash
# Write once, publish everywhere
openclaw-news publish article.md --platforms rss,wechat,twitter,toutiao
```

### 3. Content Preview Before Publishing
```bash
# Preview and test
openclaw-news preview article.md
openclaw-news publish article.md --dry-run
openclaw-news publish article.md  # Actual publish
```

## Project Structure

```
openclaw-news-publisher/
├── news/
│   ├── templates/        # Article templates
│   ├── drafts/           # Work in progress
│   └── published/        # Published archive
├── scripts/
│   ├── platforms/        # Platform publishers
│   ├── publish-news.sh   # Main publish script
│   └── create-news.sh    # Create drafts
├── agents/
│   └── news-cli.sh       # CLI entry point
└── public/
    └── feed.xml          # Generated RSS feed
```

## Advanced Features

### Publishing History

Each publish creates a JSON record:

```json
{
  "article_id": "my-news",
  "platform": "rss",
  "status": "success",
  "published_at": "2026-03-10T12:00:00Z",
  "platform_url": "https://example.com/feed.xml",
  "error": null
}
```

Stored in: `news/published/YYYY-MM-DD/article-id.platform.json`

### Automatic Platform Fallback

If a platform fails, publishing continues to next platform:

```
Publishing to: rss        ✅ Success
Publishing to: wechat     ❌ Failed (not configured)
Publishing to: twitter    ✅ Success

Summary: 2 success, 1 failed
```

### Template System

Built-in templates:
- `default.md` - General purpose
- `tech-news.md` - Technology news

Create custom templates in `news/templates/`

## Requirements

- **Node.js**: >=18.0.0
- **Operating System**: Linux, macOS, WSL
- **Dependencies**: None (uses standard system tools)
- **Platform Credentials**: Required for each platform

## Limitations

- WeChat/Twitter APIs require manual implementation
- Toutiao/YouTube are placeholders
- No built-in image hosting
- No scheduling system (yet)

## Roadmap

- [ ] Complete WeChat API integration
- [ ] Implement Twitter OAuth flow
- [ ] Add Toutiao API support
- [ ] Add YouTube Data API
- [ ] Web UI dashboard
- [ ] Scheduling system
- [ ] Analytics tracking

## Support

- **GitHub**: https://github.com/ZhenRobotics/openclaw-news-publisher
- **Issues**: https://github.com/ZhenRobotics/openclaw-news-publisher/issues
- **Documentation**: See `docs/PLATFORMS.md`

## License

MIT License - Free for commercial and personal use

---

**Version**: 1.0.0
**Author**: justin
**Status**: Production Ready (RSS), Beta (WeChat, Twitter)
