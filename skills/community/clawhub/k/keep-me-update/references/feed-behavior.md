# RSS Feed Behavior Reference

> Known patterns observed across KeepMeUpdate runs. Update as new quirks emerge.

## Consistently Problematic Feeds

| Feed | Symptom | Cause | Impact |
|------|---------|-------|--------|
| r/unixporn | HTTP 429 | Reddit rate limiting | Always fails, ignore |
| Linux Reddit (r/linux) | Occasional HTTP 429 | Reddit rate limiting | Sometimes succeeds, don't pre-discount |
| 爱范儿 (ifanr) | SSL wrong version | Server-side TLS issue | Intermittent, retry helps |

## arXiv cs.AI — Known Delay

arXiv feed frequently returns `count: 0` on the **first fetch of a day** because its RSS updates later than other feeds. On a re-fetch (after `--mark-read` + `--skip-read`) it typically returns 10 articles.

**Signal**: If `total_articles` < 50 and `arxiv_retry: true`, a re-fetch is worthwhile.

## Feed Count Expectations

Healthy run (all feeds populated):
- **60-85 new articles** (skipping already-read ones)
- **24-27 feeds reporting data** out of 28
- arXiv adds +10 when it's populated

## HN --fetch URL Trap

`search_web_stdlib.py --fetch` on HN returns **no URLs** — only titles, domains, and scores. Each story lacks both its original URL and its HN discussion URL. This creates a strong hallucination risk where agents invent `item?id=XXXXXXXX` links.

**Rule**: HN --fetch titles are search clues only. Cross-reference against RSS cache or web_search for verified URLs before inclusion.

## Lobsters / Aggregator Domain Mismatch

Lobsters, Linux Reddit, and similar aggregator feeds return the **original article URL** (e.g., `omgubuntu.co.uk`, `github.com`), not the aggregator's own discussion page. The `source` field must reflect the URL's actual domain, not the aggregator name.

## Date Awareness

- RSS cache files are named `articles_YYYY-MM-DD.json` by UTC fetch time
- **Always use `datetime.now(TZ)` for the output date**, not the cache file name
- Previous runs' cache from "yesterday" may persist — still use current CST date
- User may trigger the skill after midnight CST — the cache name lags behind
