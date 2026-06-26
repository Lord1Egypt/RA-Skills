---
name: content-repurposer
description: Repurpose long-form content (blog posts, articles, YouTube transcripts) into multiple formats automatically — Twitter/X threads, LinkedIn posts, email newsletters, Instagram captions, and short-form summaries. Use when converting blog posts to social media, creating multi-platform content from a single source, generating tweet threads from articles, writing newsletters from blog content, or building a content distribution pipeline.
---

# Content Repurposer — One Source → Multiple Platforms

Turn any long-form content into platform-optimized posts for Twitter/X, LinkedIn, email, and more.

## How It Works

1. **Fetch** — Pull content from a URL, file, or paste
2. **Extract** — Identify key points, quotes, stats, and narrative arc
3. **Transform** — Generate platform-specific versions with proper formatting
4. **Output** — Save all versions to files or send directly via APIs

## Quick Start

```bash
# From a URL
node scripts/repurpose.js --url "https://example.com/blog-post" --formats twitter,linkedin,newsletter

# From a local file
node scripts/repurpose.js --file ./my-article.md --formats twitter,linkedin

# From clipboard/stdin
cat article.md | node scripts/repurpose.js --formats all
```

## Supported Output Formats

| Format | Description | Typical Length |
|--------|-------------|----------------|
| `twitter` | Thread of 3-8 tweets with hooks and CTAs | 280 chars/tweet |
| `linkedin` | Professional post with formatting | 500-1,500 chars |
| `newsletter` | Email-ready summary with key takeaways | 300-800 words |
| `instagram` | Caption with hashtags and emoji | 200-400 chars |
| `summary` | TL;DR bullet points | 3-5 bullets |
| `all` | Generate all formats | — |

## Platform-Specific Rules

### Twitter/X Threads
- First tweet = hook (question, bold claim, or surprising stat)
- Each tweet is self-contained but builds on the thread
- Last tweet = CTA (follow, link, retweet ask)
- Use line breaks for readability
- No hashtags in thread (except last tweet)

### LinkedIn Posts
- Opening line = scroll-stopper (no "I'm excited to announce...")
- Use single-line paragraphs with spacing
- Include a personal take or lesson learned
- End with a question to drive comments
- 3-5 relevant hashtags at the bottom

### Email Newsletter
- Subject line options (3 variants)
- Opening hook → key insights → action items → sign-off
- Bold key takeaways for skimmers
- Keep under 800 words

## Configuration

Edit `scripts/config.json`:
- `tone`: professional | casual | provocative | educational
- `audience`: developers | marketers | founders | general
- `includeEmoji`: true/false
- `maxTweets`: 3-12 (default 6)
- `ctaLink`: URL to include in posts

## Scripts

- `scripts/repurpose.js` — Main pipeline
- `scripts/config.json` — Tone, audience, and format settings

## References

- See `references/platform-guides.md` for character limits and best practices per platform
