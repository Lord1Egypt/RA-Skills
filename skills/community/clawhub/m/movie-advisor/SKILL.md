---
name: movie-advisor
description: Movie and TV recommendation and critique assistant. Suggests films and series from taste, mood, or context; surfaces ratings, cast, runtime, and where to watch on major global streaming platforms. Keywords: movie recommendation, TV show, film review, Netflix, streaming, what to watch.
---

# Movie Advisor — Recommendations & Deeper Takes

## Overview

Helps users pick **movies and TV shows** that fit their preferences, mood, or occasion, and supports **short analytical takes** (themes, tone, comparable titles). Use for weekend picks, group viewing, discovering lesser-known gems, or understanding a title before watching.

**Trigger keywords**: movie recommendation, TV show, film, what to watch, similar to [title], streaming

## Prerequisites

```bash
pip install requests tmdbsimple
```

## Capabilities

1. **Data-backed lookups** — TMDb / OMDb–style workflows for titles, ratings, cast, and metadata (see `references/movie_advisor_guide.md`).
2. **Taste-aware suggestions** — recommendations by genre, mood, “like this title,” or scenario (date night, family, short runtime).
3. **Title briefs** — scores, synopsis, key cast, runtime, and **where to watch** pointers on major **global** streaming services (outside mainland China’s domestic apps).

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `recommend` | Recommend titles | `python3 scripts/skills/movie-advisor/scripts/movie_advisor_tool.py recommend [args]` |
| `search` | Search / filter titles | `python3 scripts/skills/movie-advisor/scripts/movie_advisor_tool.py search [args]` |
| `detail` | Title details | `python3 scripts/skills/movie-advisor/scripts/movie_advisor_tool.py detail [args]` |

## Usage (from repository root)

```bash
python3 scripts/skills/movie-advisor/scripts/movie_advisor_tool.py recommend --like 'Interstellar' --count 5
python3 scripts/skills/movie-advisor/scripts/movie_advisor_tool.py search --year 2026 --sort rating
python3 scripts/skills/movie-advisor/scripts/movie_advisor_tool.py detail --title 'Oppenheimer'
```

## Major global streaming platforms (reference)

When suggesting **where to watch**, prefer well-known **international** services and official hubs. Availability varies by country and title; remind users to check their region.

| Platform | Role | Official site |
|----------|------|---------------|
| **Netflix** | Subscription SVOD; strong originals & licensed catalog | https://www.netflix.com |
| **YouTube** | Rentals/purchases (**YouTube Movies & TV**), free ad-supported titles, creator film channels | https://www.youtube.com/movies |
| **Amazon Prime Video** | Included with Prime in many regions; add-on channels | https://www.primevideo.com |
| **Disney+** | Disney, Pixar, Marvel, Star Wars, Nat Geo | https://www.disneyplus.com |
| **Max** (HBO catalog in many markets) | HBO originals & Warner Bros. library (branding varies by region) | https://www.max.com |
| **Apple TV+** | Apple originals; often bundled with Apple One | https://tv.apple.com |
| **Hulu** | US-focused SVOD (Disney bundle in US) | https://www.hulu.com |
| **Paramount+** | Paramount, CBS, Showtime (where available) | https://www.paramountplus.com |
| **Peacock** | NBCUniversal (US) | https://www.peacocktv.com |
| **Crunchyroll** | Anime & Asian drama (global) | https://www.crunchyroll.com |

**Aggregator (where to watch by country):** [JustWatch](https://www.justwatch.com) — useful to cross-check Netflix / Prime / Apple / etc. for a specific title.

Do **not** invent “available on X” without a source; when unsure, say availability is region-dependent and point to JustWatch or the platform’s own search.

## Output format (for the agent’s report)

```markdown
# Movie Advisor report

**Generated**: YYYY-MM-DD HH:MM

## Key picks
1. [Title — one-line why]
2. …
3. …

## Snapshot
| Title | Score / source | Genre | Runtime |
|-------|----------------|-------|---------|

## Notes
[Themes, tone, or “if you liked X” — grounded in facts you have]

## Where to watch (verify locally)
| Title | Platform hints (region-dependent) |
|-------|-----------------------------------|
```

## References

### APIs & data
- [TMDb API](https://developer.themoviedb.org/docs/getting-started)
- [OMDb API](https://www.omdbapi.com/)
- [Public APIs — entertainment](https://github.com/public-apis/public-apis)

### Patterns & community
- [Daily YouTube digest (OpenClaw use case)](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-youtube-digest.md)
- [Hacker News — recommendation engines](https://news.ycombinator.com/item?id=43600632)
- [Reddit r/MovieSuggestions](https://www.reddit.com/r/MovieSuggestions/comments/106e373yyz/movie_advisor_ai/)

## Notes

- Base scores and metadata on **API or user-provided** data; do not fabricate ratings or availability.
- Mark missing fields as **unavailable** instead of guessing.
- Streaming lineups change often; **region** and **date** matter.
