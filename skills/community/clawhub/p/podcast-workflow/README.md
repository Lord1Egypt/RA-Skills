# podcast-workflow

**Full podcast post-production pipeline for OpenClaw.**

Give your agent a transcript or episode URL. Get back show notes, chapter markers, social media posts, SEO metadata, and a newsletter blurb — all in one shot.

## Install

```bash
clawhub install podcast-workflow
```

## What it produces

| Output | Format | Length |
|--------|--------|--------|
| Show notes | Markdown | 200–400 words |
| Chapter markers | Timestamp list | 4–12 chapters |
| LinkedIn post | Plain text | 150–250 words |
| X/Twitter thread | 5–7 tweets | Numbered |
| Instagram caption | Plain text + hashtags | 100–180 words |
| SEO metadata | Title + description + keywords | — |
| Newsletter blurb | Markdown | 100–150 words |

## How to use

Just paste your transcript or episode URL:

```
/podcast
[paste transcript here]
```

Or with a URL:

```
/podcast
https://youtu.be/your-episode
```

The skill handles the rest — no flags, no options required.

## Requirements

- `curl` (pre-installed on macOS and most Linux systems)
- No API keys required
- Works with any transcript: auto-generated, manual, or AI-produced

## Supported input types

- Raw transcript text (any format)
- YouTube URLs (extracts available transcript)
- Podcast RSS feed URLs
- Plain URLs with transcript/description content

## Why this skill exists

Every podcaster runs the same post-production workflow after recording: write the show notes, generate timestamps, create social posts, fill in the SEO fields, draft the newsletter blurb. It takes 2–4 hours per episode. This skill does it in under 60 seconds.

As of April 2026, no equivalent skill exists on ClawHub.

## License

MIT-0 — use freely, no attribution required.

## Issues and feedback

Open an issue on GitHub or reach out through ClawHub comments.
