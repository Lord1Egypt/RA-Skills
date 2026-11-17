# scihub — Academic Paper Access via Sci-Hub Mirrors

## What this source has

Sci-Hub provides free access to ~85 million academic research papers. Each mirror can resolve a DOI, title, or keyword to a direct PDF download URL. This is not an official API — it scrapes the HTML of whichever mirror is currently reachable.

Coverage: virtually all DOI-registered scholarly content including paywalled journal articles, conference papers, and book chapters. No synthesis — raw PDF URLs and metadata only.

## Auth

| | |
|---|---|
| Required | none |
| Env var | — |
| Account URL | — |
| Plan tier | free |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 30 req/min; mirrors are fragile, be gentle |

## Mirror Strategy

Sci-Hub mirrors go down frequently. This source maintains a prioritized mirror list with automatic failover:

**Primary mirrors (prioritized):**
1. `sci-hub.st` — primary (186.2.163.201)  <!-- sanitize-allow: third-party public mirror, not operator infrastructure -->
2. `sci-hub.su`
3. `sci-hub.red`
4. `sci-hub.ren`
5. `sci-hub.ru` — official
6. `sci-hub.box` — fallback (190.115.31.76)  <!-- sanitize-allow: third-party public mirror, not operator infrastructure -->
7. `www.sci-hub.pub` — mirror directory
8. `sci-hub.al`
9. `sci-hub.mk`
10. `sci-hub.ee`

**Mirror selection order:** Try each mirror in order. On first success, cache that mirror for subsequent queries in the same session. If a mirror fails (timeout, 404, or invalid response), mark it bad for 5 minutes and try the next one.

New mirrors can be discovered at `https://www.sci-hub.pub/`.

## Alternative Endpoints

- **sci-bot.ru** (`https://sci-hub.box` via `CITE_READER_URL`) — AI-powered research assistant that proxies through Sci-Hub mirrors. CORS-restricted; use from server-side only.
- **CrossRef** (`https://api.crossref.org`) — not Sci-Hub, but the metadata backbone. Used as fallback: CrossRef resolves title→DOI, then Sci-Hub resolves DOI→PDF.

## Endpoints

```bash
# Search by DOI — returns paper metadata + PDF URL
python3 scripts/reach.py query scihub search_doi '{"doi": "10.1038/nature09492"}'

# Search by title — CrossRef resolves title→DOI, then Sci-Hub resolves DOI→PDF
python3 scripts/reach.py query scihub search_title '{"title": "Attention Is All You Need"}'

# Search by keyword — CrossRef keyword search + Sci-Hub resolution
python3 scripts/reach.py query scihub search_keyword '{"keyword": "transformer attention mechanism", "num_results": 5}'

# Download a PDF directly
python3 scripts/reach.py query scihub download_pdf '{"pdf_url": "https://sci-hub.st/10.1038/nature09492", "output_path": "/tmp/paper.pdf"}'
```

## Response shape

`search_doi` / `search_title` returns:
```json
{
  "doi": "10.1038/nature09492",
  "title": "Paper Title",
  "author": "Author One, Author Two",
  "year": "2023",
  "pdf_url": "https://sci-hub.st/10.1038/nature09492",
  "mirror_used": "sci-hub.st",
  "status": "success"
}
```

`search_keyword` returns a list of the above objects.

`download_pdf` returns:
```json
{
  "status": "success",
  "output_path": "/tmp/paper.pdf",
  "bytes": 245760,
  "mirror_used": "sci-hub.box"
}
```

On failure:
```json
{
  "status": "error",
  "error": "All mirrors failed",
  "doi": "10.1038/nature09492"
}
```

## Worked examples

```bash
# Find a paper by DOI
python3 scripts/reach.py query scihub search_doi '{"doi": "10.1145/3442381.3449852"}'

# Find a paper by approximate title
python3 scripts/reach.py query scihub search_title '{"title": "BERT Pre-training of Deep Bidirectional Transformers"}'

# Search for recent papers on a topic
python3 scripts/reach.py query scihub search_keyword '{"keyword": "mixture of experts language model", "num_results": 10}'

# Download once you have the PDF URL
python3 scripts/reach.py query scihub download_pdf '{"pdf_url": "https://sci-hub.st/10.1145/3442381.3449852", "output_path": "/tmp/bert.pdf"}'
```

## Pitfalls

- **Mirror instability:** Any mirror can go down at any time. Always have fallback mirrors ready.
- **Bot detection:** Sci-Hub may block automated requests. Use residential IP/proxy if needed. Rotate User-Agent.
- **DNS ISP blocking:** Some ISPs block Sci-Hub domains at DNS level. Use DNS-over-HTTPS (Google/Cloudflare) as fallback.
- **PDF validation:** Always verify downloaded content starts with `%PDF` magic bytes — mirrors may return HTML error pages instead.
- **CORS:** Browser-based access to Sci-Hub mirrors is often blocked by CORS. Use server-side (Python) requests only.
- **Rate limiting:** More aggressive than 30/min can trigger blocks. Respect the rate limit.
- **Title search imprecision:** Title search goes through CrossRef first. Vague titles may return wrong paper. Always verify DOI matches intent.
- **No bulk download:** Downloading many papers in sequence mirrors aggressive scraping behavior. Space requests and use sparingly.

## Sci-Hub Ecosystem

For finding working mirrors and alternatives, see:
- `https://www.sci-hub.pub/` — latest mirror list
- `https://sci-bot.ru/` — AI research assistant (uses `sci-hub.box`)
- Anna's Archive — largest open library
- arXiv — open access preprints (already registered as separate source)
- Unpaywall — 20M free scholarly articles (could be added as source)
- CORE — world's largest open access collection
