# Movie Advisor — Framework & Guide

## Tool summary

- **Name**: Movie Advisor  
- **Commands**: `recommend`, `search`, `detail`  
- **Typical deps**: `pip install requests tmdbsimple` (if you wire real API calls)

## Analysis dimensions

- Metadata: title, year, genre, runtime, ratings (from APIs or trusted sources)  
- Fit: mood, occasion, “similar to,” age appropriateness  
- Depth: themes, director/style, comparable titles  
- Distribution: **where to watch** on major global streaming services (see below)

## Framework

### Phase 1: Clarify ask
- Genre, era, language, max runtime, “like X,” or “avoid Y”  
- Whether the user cares about **subscription vs rental vs free**

### Phase 2: Shortlist & compare
- Cross-check ratings and basics (TMDb/OMDb or equivalent)  
- Note caveats (director’s cut, sequel order)

### Phase 3: Present & point to watch options
- Clear top picks with one-line rationale each  
- **Streaming**: name platforms that commonly carry such titles, and remind that **availability is regional** — use [JustWatch](https://www.justwatch.com) or each service’s own search when precision matters

## Major global streaming platforms (outside China-centric apps)

Use these as **reference brands** when discussing legal viewing options internationally. Catalogs differ by country and change over time.

| Platform | Notes | Link |
|----------|-------|------|
| Netflix | SVOD originals + licensed library | https://www.netflix.com |
| YouTube (Movies & TV) | Rent/buy; some free with ads | https://www.youtube.com/movies |
| Amazon Prime Video | Often bundled with Prime; optional add-ons | https://www.primevideo.com |
| Disney+ | Disney, Marvel, Star Wars, Pixar, Nat Geo | https://www.disneyplus.com |
| Max | HBO / Warner-heavy catalog (name varies by region) | https://www.max.com |
| Apple TV+ | Apple Originals | https://tv.apple.com |
| Hulu | Strong in US; bundles with Disney+ in some plans | https://www.hulu.com |
| Paramount+ | Paramount, CBS, Showtime (region-dependent) | https://www.paramountplus.com |
| Peacock | NBCUniversal (primarily US) | https://www.peacocktv.com |
| Crunchyroll | Anime & related Asian content worldwide | https://www.crunchyroll.com |

**Tip:** For “where can I stream *this* title in my country?”, [JustWatch](https://www.justwatch.com) aggregates many of the above.

## Scoring rubric (for structured reviews)

| Score | Level | Meaning | Suggested action |
|-------|-------|---------|------------------|
| 5 | ⭐⭐⭐⭐⭐ | Strong match | Top recommendation |
| 4 | ⭐⭐⭐⭐ | Good match | Prioritize |
| 3 | ⭐⭐⭐ | OK | Optional |
| 2 | ⭐⭐ | Weak match | Caveat heavily |
| 1 | ⭐ | Poor match | Avoid or pivot |

## Output template

```markdown
# Movie Advisor analysis

## Top picks
1. …
2. …

## Evidence
| Title | Rating source | Genre | Runtime |
|-------|-----------------|-------|---------|

## Where to watch (verify for user’s region)
- …

## Caveats
- Availability changes; confirm on JustWatch or the provider’s site.
```

## Reference links

- [TMDb API](https://developer.themoviedb.org/docs/getting-started)  
- [OMDb API](https://www.omdbapi.com/)  
- [Daily YouTube digest (OpenClaw)](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-youtube-digest.md)  
- [Public APIs — entertainment](https://github.com/public-apis/public-apis)  
- [Hacker News](https://news.ycombinator.com/item?id=43600632)  
- [Reddit r/MovieSuggestions](https://www.reddit.com/r/MovieSuggestions/comments/106e373yyz/movie_advisor_ai/)  

## Tips

1. Align recommendations with **stated constraints** (time, mood, subtitles).  
2. Separate **critical acclaim** from **personal fit**.  
3. For streaming, prefer naming **platforms + “check locally”** over asserting a single country-specific URL unless you have a live source.  
