# Paper Search (paper-search-mcp)

Multi-source academic paper search and download. Uses the `paper-search-mcp` Python package invoked via MCP stdio. Searches 20+ academic platforms simultaneously.

## Prerequisites

```bash
pip install paper-search-mcp
```

Optional API keys for enhanced rate limits:
- `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_KEY` — Semantic Scholar (improves from 5 to 50 req/sec)
- `PAPER_SEARCH_MCP_CORE_KEY` — CORE (raises rate limits)
- `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL` — Unpaywall (required for DOI lookup)
- `PAPER_SEARCH_MCP_GOOGLE_SCHOLAR_PROXY_URL` — Proxy for Google Scholar (bot detection bypass)

## Actions

### `search`
Search papers across all configured sources (arXiv, PubMed, bioRxiv, medRxiv, Semantic Scholar, Crossref, OpenAlex, etc.).

```bash
python3 scripts/reach.py query paper_search search '{"query": "transformer attention mechanism", "limit": 10}'
```

Params:
- `query` (string, required) — Search terms
- `limit` (int, default: 10) — Max results per source
- `sources` (list, optional) — Specific sources to search (e.g., ["arxiv", "pubmed"])

### `arxiv`
Search arXiv specifically.

```bash
python3 scripts/reach.py query paper_search arxiv '{"query": "large language models", "limit": 5}'
```

Params:
- `query` (string, required)
- `limit` (int, default: 10)

### `pubmed`
Search PubMed specifically.

```bash
python3 scripts/reach.py query paper_search pubmed '{"query": "CRISPR gene therapy", "limit": 5}'
```

Params:
- `query` (string, required)
- `limit` (int, default: 10)

### `download`
Download a paper PDF using fallback chain (publisher OA → repositories → Unpaywall).

```bash
python3 scripts/reach.py query paper_search download '{"doi": "10.48550/arXiv.2301.00001"}'
```

Params:
- `doi` (string) — DOI of the paper, OR
- `url` (string) — Direct URL to paper
- `source` (string, optional) — Preferred source (e.g., "arxiv", "pubmed")

## Supported sources

| Source | Search | Download | Notes |
|--------|--------|----------|-------|
| arXiv | ✅ | ✅ | Open API, reliable |
| PubMed | ✅ | ⚠️ info-only | Biomedical literature |
| bioRxiv/medRxiv | ✅ | ✅ | Preprints |
| Semantic Scholar | ✅ | ✅ OA | Key improves rate limits |
| Crossref | ✅ | ⚠️ metadata | DOI resolution |
| OpenAlex | ✅ | ⚠️ metadata | Broad academic metadata |
| PMC | ✅ | ✅ OA | PubMed Central full-text |
| CORE | ✅ | ✅ record-dependent | Repository aggregator |
| Europe PMC | ✅ | ✅ OA | European biomedical |
| dblp | ✅ | ⚠️ metadata | Computer science |
| Zenodo/HAL | ✅ | ✅ record-dependent | Open repositories |
| Unpaywall | ✅ DOI lookup | — | Requires email env var |

## Use cases

- **Research** — Find academic papers on any topic
- **Literature review** — Search across multiple academic databases simultaneously
- **Paper download** — Get PDFs of open-access papers
- **Citation lookup** — Resolve DOIs and get metadata

## Pitfalls

- **Rate limits vary by source** — arXiv allows 1 req/3sec, Semantic Scholar 5/sec without key, Crossref 50/sec polite pool
- **Google Scholar blocked** — Bot detection active from cloud IPs; set proxy URL if needed
- **Download success varies** — Not all papers are open access. The fallback chain tries multiple sources.
- **MCP server startup** — First call may be slow as the Python module initializes
