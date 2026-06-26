---
name: pipeworx-crossref
description: Search academic papers by keyword, look up metadata by DOI, and fetch journal info via Crossref
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🔬"
    homepage: https://pipeworx.io/packs/crossref
---

# Crossref Academic Papers

Crossref indexes over 150 million scholarly works. Search papers by keyword, retrieve full metadata for a specific DOI, or look up journal information by ISSN. Essential for literature reviews, citation analysis, and academic research tools.

## Tools

- **`search_works`** — Keyword search across papers, books, and proceedings. Returns title, authors, DOI, publication date, citation count, and journal info.
- **`get_work`** — Detailed metadata for a specific DOI (e.g., `"10.1038/nature12373"`). Includes abstract, references, funders, and license info.
- **`get_journal`** — Journal metadata by ISSN (e.g., `"1476-4687"` for Nature). Returns publisher, subject areas, and coverage dates.

## When to reach for this

- A researcher asks "find me papers on climate change and machine learning"
- Need to verify a citation or look up the full reference for a DOI
- Building a bibliography tool that auto-fills metadata from DOIs
- Analyzing citation counts or publication trends in a field

## Example: searching for CRISPR papers

```bash
curl -s -X POST https://gateway.pipeworx.io/crossref/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_works","arguments":{"query":"CRISPR gene editing therapy","limit":5}}}'
```

## Connect your client

```json
{
  "mcpServers": {
    "pipeworx-crossref": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/crossref/mcp"]
    }
  }
}
```
