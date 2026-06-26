# MovieMovie

Intelligently search and recommend HD movies that meet both conditions:
1. Movies with downloadable resources (magnet links / torrents)
2. Real-time trending movies on Rotten Tomatoes and Douban


[![ClawHub](https://img.shields.io/badge/ClawHub-moviemovie-blue)](https://clawhub.ai/kunhai1994/moviemovie)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[中文文档](README.zh-CN.md)

## Quick Start

Copy this to OpenClaw or Claude Code:
```
Install this skill: https://github.com/kunhai1994/moviemovie
```

Then just ask:

```
> find Sinners 2025 4K download
> recommend trending movies with downloads
> find Inception 1080p magnet
> recommend sci-fi movies like Blade Runner
```

## Features

| Feature | Basic (zero config) | Enhanced (with API keys) |
|---------|--------------------|-----------------------|
| **Trending + verified downloads** | Rotten Tomatoes + Douban aggregation → torrent verification → only show downloadable | + TMDb trending API |
| Torrent search | apibay + bitsearch + torrentdownload + YTS (3-4 sources) | + TorrentClaw (30+ sources) |
| Magnet links | hash → auto-constructed magnet links | full magnet + quality score (0-100) |
| Quality filtering | 720p / 1080p / 2160p parsed from filename | + HDR / codec / audio verification |
| Size tier Top 3 | Light (1-3GB) / Balanced (3-5GB) / Premium (10-30GB) | same |
| Movie info | WebSearch + LLM knowledge | TMDb structured JSON (multilingual, posters) |
| Subtitle search | SubtitleCat (60+ languages) + SubHD (Chinese) | same |

## Usage Examples

### Direct Search

```
> find Interstellar 4K download
> find Sinners 2025 magnet
> Peaky Blinders Immortal Man download
```

Output: user reviews + Top 3 size tiers with magnet links:

```
💬 Reviews
Critics: "A rip-roaring fusion of masterful visual storytelling
and toe-tapping music..." — RT Critics Consensus
🍅 97% (438 reviews) | 🍿 96% (5,000+ ratings)

⭐⭐⭐⭐⭐ "Honestly one of the best movie going experiences
for me in a long time." — TheGeekySandbox
⭐⭐⭐⭐⭐ "Something about this movie touches the soul in
an unexpected but wonderful way." — Elizabeth

🏆 Recommended Downloads

1. 📱 Light (1.1GB) — mobile / quick download
   Sinners 2025 1080p HDRip HEVC x265
   [1080p x265] seeds: 1614
   magnet:?xt=urn:btih:81FB914A...

2. 🖥️ Premium (18.1GB) — home theater / collection
   Sinners 2025 Hybrid 1080p UHD BluRay DV HDR10 x265
   [2160p BluRay x265 DV] seeds: 17
   magnet:?xt=urn:btih:AC03F6B8...

3. ⚖️ Balanced (4.6GB) — good quality, reasonable size
   Sinners 2025 REPACK 1080p WEBRip x265
   [1080p WEBRip x265] seeds: 29
   magnet:?xt=urn:btih:4DE427E4...
```

### Trending Recommendations

```
> what's trending and downloadable?
> recommend movies I can watch tonight
> any good new movies to download?
```

Output: only movies with confirmed downloads:

```
🎬 8 Trending Movies (all with confirmed downloads)

1. Sinners (2025) — 🍅97% 🍿96% ⭐7.7
   135 torrents | best: 1080p 1.1GB seeds:1614

2. One Battle After Another (2025) — 🍅94% 🍿85% ⭐8.0
   86 torrents | best: 1080p 3.0GB seeds:3470
...

❌ Not available: GOAT (2026) — likely still in theaters
```

### Subtitle Search

```
> find subtitles for Sinners
> find subtitles for Inception
```

### Specific Charts

```
> Rotten Tomatoes certified fresh with downloads
> Netflix trending movies
> Douban trending with downloads
```

## Optional: Configure API Keys for Enhanced Experience

The skill works out of the box with zero configuration. API keys are **optional** — they unlock more sources and structured data.

### TorrentClaw API Key (recommended, free)

Unlocks 30+ torrent sources, quality scoring (0-100), HDR/codec verification, and full magnet links.

1. Visit [torrentclaw.com/register](https://torrentclaw.com/register)
2. Sign up with email
3. Copy your API key from the Dashboard
4. Configure (pick one):

**Easiest way:** Just tell Claude Code / OpenClaw your key and let it save it for you:
```
My TorrentClaw API Key is xxx, please configure it
```

**Manual setup:**
- Claude Code: Add to `.claude/settings.json` or `~/.claude/settings.json`:
  ```json
  { "env": { "TORRENTCLAW_API_KEY": "your-key-here" } }
  ```
- OpenClaw: Settings → Environment Variables → Add `TORRENTCLAW_API_KEY`

### TMDb API Key (optional, free)

Unlocks structured movie data (JSON), multilingual support, trending/discover/recommendations, and poster images.

1. Visit [themoviedb.org/signup](https://www.themoviedb.org/signup)
2. Create an account
3. Go to Settings → API → Request an API Key (choose "Developer")
4. Configure (pick one):

**Easiest:** Tell Claude Code / OpenClaw `My TMDb API Key is xxx, please configure it`

**Manual:** Same as above, variable name is `TMDB_API_KEY`

## Architecture

```
User Input → SKILL.md instructions
   │
   ├── Step 0: status.py (environment check)
   │
   ├── Step 1: Intent parsing (LLM)
   │   ├── Direct search: "find Movie X"
   │   ├── Recommendation: "what's trending?"
   │   └── Chart: "RT certified fresh"
   │
   ├── Step 1.5: Film name standardization
   │   └── WebSearch "[name] [year] movie English title imdb"
   │       ⚠️ NEVER translate directly — always search for exact title
   │
   ├── Step 2: Movie info / Trending lists
   │   ├── Basic: WebFetch Rotten Tomatoes + Douban
   │   └── Enhanced: TMDb API
   │
   ├── Step 3: search_torrents.py (parallel multi-source)
   │   ├── apibay.org ── JSON API, best for new releases
   │   ├── bitsearch.to ── HTML scrape, best catalog depth
   │   ├── torrentdownload.info ── HTML scrape, good all-around
   │   ├── YTS ── JSON API, backup (may be unreachable)
   │   ├── [TorrentClaw] ── 30+ sources (with API key)
   │   └── [LLM fallback] ── WebSearch "movie magnet" (last resort)
   │
   ├── Step 4: Dedupe → filter dead → classify size tiers → Top 3
   │
   ├── Step 4.5: Fetch user reviews (Rotten Tomatoes)
   │   └── Critics consensus + top audience reviews
   │
   ├── Step 5: Subtitle search (runs in parallel with Step 3)
   │   ├── SubtitleCat ── 60+ languages
   │   ├── SubHD ── Chinese subtitles
   │   └── WebSearch fallback
   │
   └── Step 6: Formatted output in user's language
```

## System Requirements

- Python 3.10+ (usually pre-installed)
- Internet access
- **Recommended LLM: Claude** (Anthropic)

No pip packages needed — all scripts use Python standard library only.

### Important: LLM Choice Matters

This skill is designed for and tested with **Claude** (Claude Code / OpenClaw with Claude backend). We strongly recommend using Claude for the best experience.

**Why not ChatGPT?** ChatGPT's content policies are extremely restrictive around torrent/magnet link topics. Even if you tell ChatGPT you're an FBI agent investigating piracy sites, it will likely refuse to cooperate. It tends to decline any request involving torrent searches, magnet link construction, or torrent site scraping — making this skill essentially non-functional.

**Why not Gemini?** Gemini has similar (though slightly less strict) content restrictions. Results may be inconsistent.

**Claude** handles these requests pragmatically, following the skill's instructions to search APIs, construct magnet links, and present results as designed.

## FAQ

**Q: Why does the skill sometimes miss a movie I can find manually?**
A: The most common cause is incorrect film name standardization. The skill uses WebSearch to find the exact English title — if the search returns the wrong title, all torrent searches will fail. Try providing the English title directly.

**Q: Why are some trending movies marked "not available"?**
A: Movies still in theaters usually don't have torrent resources yet. The skill prioritizes the Rotten Tomatoes "streaming/at home" list because those movies are already available online and much more likely to have torrents.

**Q: Do I need API keys?**
A: No. The basic version works with zero configuration using 3 torrent sources + WebFetch for movie data. API keys are optional enhancements — TorrentClaw adds 30+ sources, TMDb adds structured multilingual data.

**Q: Which sites does the script access?**
A: apibay.org, bitsearch.to, torrentdownload.info, yts.mx (torrent search); rottentomatoes.com, movie.douban.com (trending); subtitlecat.com, subhd.tv (subtitles). Does NOT access Cloudflare-protected sites (1337x, TorrentGalaxy).

## License

MIT
