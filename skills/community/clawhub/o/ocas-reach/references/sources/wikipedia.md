# wikipedia — full-text Wikipedia via MediaWiki API

## What this source has

Every Wikipedia article (English here; other languages by changing `en.wikipedia.org` to `<lang>.wikipedia.org`). Searchable full-text plus structured "extract" plain-text pulls. Article counts ~7M for enwiki as of 2026. Updated continuously — most edits are visible within seconds.

The MediaWiki Action API (`/w/api.php`) is the most expressive surface. The REST-v1 wrapper (`/api/rest_v1/page/summary/{title}`) is faster for one-shot summaries.

Use Wikipedia for: general factual lookups, definitions, biographical / institutional summaries, "what is X" answers. Pair with `wikidata` when you need structured facts (dates, populations, coordinates) instead of prose.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

But the MediaWiki API **does require a meaningful `User-Agent`**. Reach sends `ocas-reach/3.0 (<agent-email>)` automatically.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | ~200 req/sec ceiling for the Action API; treat 10 req/sec as a polite default |

Aggressive callers without a real `User-Agent` get blocked at the load balancer.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Full-text search across page bodies | `srsearch` (query string) |
| `summary` | Single-paragraph plain-text intro | `title` (path-encoded) |
| `extract` | Full intro section as plain text | `titles` |

## Worked examples

```bash
# Search for "claude shannon"
python3 scripts/reach.py query wikipedia search '{"srsearch": "claude shannon", "srlimit": 5}'

# Get a summary of "Claude Shannon"
python3 scripts/reach.py query wikipedia summary '{"title": "Claude Shannon"}'

# Get the lead-section extract
python3 scripts/reach.py query wikipedia extract '{"titles": "Claude Shannon", "explaintext": 1}'
```

## Response shape

- `search`: top-level `query.search` is a list of `{ns, title, pageid, size, wordcount, snippet, timestamp}`. `snippet` contains HTML highlight markers.
- `summary` (REST v1): `{title, extract, extract_html, content_urls, thumbnail, originalimage, coordinates, ...}`. The `extract` field is the most useful single value.
- `extract`: `query.pages[<pageid>].extract` holds the plain-text body. With `exintro: 1` (default in our registry) you get only the lead.

## Pitfalls

- **Disambiguation pages** look like normal pages but the extract describes the disambiguation, not the entity. Check for `(disambiguation)` in the title and re-query with the canonical form.
- **`title` is case-sensitive** for the REST `summary` endpoint; spaces become underscores when path-encoded.
- **Redirects** are followed by default in `summary` but not always in `extract` — pass `redirects: 1`.
- **Snippet HTML** in search results contains `<span class="searchmatch">` — strip if you need plain text.
- **Mobile vs desktop content** — REST summary returns desktop content; that's what you want.

## Source links

- Action API docs: https://www.mediawiki.org/wiki/API:Main_page
- REST API: https://en.wikipedia.org/api/rest_v1/
- User-Agent policy: https://meta.wikimedia.org/wiki/User-Agent_policy
