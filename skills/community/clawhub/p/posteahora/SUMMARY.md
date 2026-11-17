# Summary

**PosteAhora CLI** — schedule and publish social media posts across Instagram,
TikTok, YouTube, X (Twitter), Facebook, LinkedIn, Threads, Bluesky, Mastodon,
Discord, Telegram, WordPress, Dev.to, Tumblr, Pinterest and Google Business,
from the command line. A thin, zero-dependency wrapper over the
[PosteAhora](https://posteahora.com) public REST API, built for developers, CI,
and AI agents.

## TL;DR

```bash
npm install -g @posteahora/cli
posteahora auth --key pah_live_xxxx
posteahora accounts
posteahora post "Hello 👋" --to twitter:a1b2 --to instagram:c3d4
```

## What it does

- Publish now, schedule, or draft posts to one or many channels.
- Upload images and video; attach them to posts.
- Manage a content-ideas backlog.
- Read cross-platform analytics.
- `--json` output everywhere for scripting and agents.

## Command cheat sheet

| Command | Purpose |
|---------|---------|
| `posteahora auth --key <pah_…>` | Save & validate an API key |
| `posteahora accounts` | List connected accounts (get IDs) |
| `posteahora post "<text>" --to platform:id` | Publish / schedule / draft |
| `posteahora posts [--status]` | List posts |
| `posteahora ideas add "<title>"` / `ideas list` | Manage ideas |
| `posteahora analytics [--period]` | Performance metrics |
| `posteahora upload <file>` | Upload media → public URL |

## Links

- Website — https://posteahora.com
- Docs — https://posteahora.com/docs
- API reference — https://posteahora.com/docs/api
- CLI (npm) — https://www.npmjs.com/package/@posteahora/cli
- MCP server — https://github.com/posteahora/mcp

## Related docs

[README](README.md) · [QUICK_START](QUICK_START.md) · [FEATURES](FEATURES.md) ·
[PLATFORMS](PLATFORMS.md) · [PUBLISHING](PUBLISHING.md) ·
[SUPPORTED_FILE_TYPES](SUPPORTED_FILE_TYPES.md) · [HOW_TO_RUN](HOW_TO_RUN.md) ·
[examples/](examples/)
