# welib — Free Books and Papers Library

## What this source has

WeLib (welib.org) provides free access to ~43 million books and ~98 million academic papers. It aggregates open-access academic content, textbooks, and research papers into a single searchable index with direct download links.

Coverage: books, academic papers, research articles. Claims 43M books + 98M papers. No login required for search and download.

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
| Rate | unknown; be conservative |

## Cloudflare Protection

⚠️ WeLib is behind Cloudflare bot protection. API calls from server-side may be blocked. If blocked, use the `browser` tool with stealth mode or a residential proxy.

## Endpoints

```bash
# Search for books and papers
python3 scripts/reach.py query welib search '{"q": "quantum physics", "type": "all", "limit": 10}'

# Get item details by ID
python3 scripts/reach.py query welib detail '{"id": "...", "type": "book"}'
```

## Response shape

`search` action returns:
```json
{
  "results": [
    {
      "id": "...",
      "title": "Introduction to Quantum Mechanics",
      "type": "book",
      "authors": ["Author Name"],
      "year": "2020",
      "download_url": "https://.../book.pdf",
      "format": "pdf",
      "size_bytes": 1234567
    }
  ],
  "total": 1500,
  "offset": 0,
  "limit": 10
}
```

## Worked examples

```bash
# Search for books on quantum physics
python3 scripts/reach.py query welib search '{"q": "quantum physics textbook", "type": "book", "limit": 5}'

# Search for papers
python3 scripts/reach.py query welib search '{"q": "attention mechanism neural network", "type": "paper", "limit": 10}'

# Get details for a specific item
python3 scripts/reach.py query welib detail '{"id": "...", "type": "book"}'
```

## Integration with other sources

WeLib complements the academic paper sources:
- `unpaywall` → legal OA copies from repositories/journals
- `scihub` → paywalled papers via mirrors
- `welib` → books + aggregated open-access papers + textbook content
- `arxiv` → preprints only
- `openalex` → scholarly metadata + citation graph

Use WeLib when looking for textbooks, monographs, or a broad sweep of both books and papers on a topic.

## Pitfalls

- **Cloudflare:** May block automated access. Use browser tool or residential proxy if API calls fail.
- **API stability:** WeLib is a smaller operation. API structure may change without notice.
- **No documented rate limits:** Be conservative with request frequency.
- **Mixed quality:** Results may include both high-quality OA papers and lower-quality sources. Verify source quality before citing.
- **Type filtering:** Use `type: book` or `type: paper` to narrow results. Default `type: all` may return mixed content.
