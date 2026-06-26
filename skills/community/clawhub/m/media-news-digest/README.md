# Media News Digest 🎬

> Automated media & entertainment industry news digest — 29 sources, 3-layer pipeline, one chat message to install.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 💬 Install in One Message

Tell your [OpenClaw](https://openclaw.ai) AI assistant:

> **"Install media-news-digest and send a daily digest to #news-media every morning at 7am"**

That's it. Your bot handles installation, configuration, scheduling, and delivery — all through conversation.

More examples:

> 🗣️ "Set up a weekly Hollywood digest, only box office and awards, deliver to Discord #awards every Monday"

> 🗣️ "Install media-news-digest, add my RSS feeds, and send festival news to email"

> 🗣️ "Give me a media digest right now, focus on streaming news"

Or install via CLI:
```bash
clawhub install media-news-digest
```

## 📊 What You Get

A quality-scored, deduplicated entertainment industry digest built from **29 sources**:

| Layer | Sources | What |
|-------|---------|------|
| 📡 RSS | 16 feeds | THR, Deadline, Variety, IndieWire, The Wrap, Collider, Gold Derby… |
| 🐦 Twitter/X | 11 KOLs | @THR, @DEADLINE, @Variety, @BoxOfficeMojo, @MattBelloni… |
| 🔍 Web Search | 7 topics | Brave Search API with freshness filters |

### Pipeline

```
RSS + Twitter + Web Search
         ↓
   merge-sources.py
         ↓
Quality Scoring → Deduplication → Topic Grouping
         ↓
  Discord / Email output
```

## 🎯 7 Topic Sections

| # | Section | Covers |
|---|---------|--------|
| 🎬 | Production / 制作动态 | New projects, casting, filming updates |
| 💰 | Deals & Business / 行业交易 | M&A, rights, talent deals, restructuring |
| 🎟️ | Box Office / 票房 | NA/global box office, opening weekends |
| 📺 | Streaming / 流媒体 | Netflix, Disney+, Apple TV+, viewership |
| 🏆 | Awards / 颁奖季 | Oscars, Golden Globes, Emmys, campaigns |
| 🎪 | Film Festivals / 电影节 | Cannes, Venice, TIFF, Sundance, Berlin |
| ⭐ | Reviews & Buzz / 影评口碑 | Critical reception, RT/Metacritic scores |

## 📡 RSS Sources (16 enabled)

THR · Deadline · Variety · IndieWire · The Wrap · Collider · Awards Daily · Gold Derby · Screen Rant · Empire · The Playlist · /Film · JoBlo · FirstShowing.net · ComingSoon.net · World of Reel

## 🐦 Twitter/X KOLs (11)

@THR · @DEADLINE · @Variety · @FilmUpdates · @DiscussingFilm · @ScottFeinberg · @kristapley · @BoxOfficeMojo · @GiteshPandya · @MattBelloni · @Borys_Kit

## ⚙️ Configuration

### Default configs in `config/defaults/`:
- `sources.json` — RSS feeds, Twitter handles
- `topics.json` — Report sections with search queries

### User overrides in `workspace/config/`:
- Same `id` → user version wins
- New `id` → appended to defaults

## 🚀 Quick Start

```bash
# Full pipeline
python3 scripts/fetch-rss.py --defaults config/defaults --hours 48 --output /tmp/md-rss.json
python3 scripts/fetch-twitter.py --defaults config/defaults --hours 48 --output /tmp/md-twitter.json
python3 scripts/fetch-web.py --defaults config/defaults --freshness pd --output /tmp/md-web.json
python3 scripts/merge-sources.py --rss /tmp/md-rss.json --twitter /tmp/md-twitter.json --web /tmp/md-web.json --output /tmp/md-merged.json
```

## 📦 Dependencies

```bash
pip install -r requirements.txt
```

All scripts work with **Python 3.8+ standard library only**. `feedparser` optional but recommended.

## 📋 Cron Integration

Reference `references/digest-prompt.md` in OpenClaw cron prompts. See [SKILL.md](SKILL.md) for full documentation.

## License

MIT
