# PubMed

Search and retrieve biomedical literature from the National Library of Medicine's PubMed database. Over 36 million citations from MEDLINE, life science journals, and online books.

## Capabilities

| Tool | Description |
|------|-------------|
| `search_pubmed` | Search by keyword, author name, or MeSH term. Returns PubMed IDs. |
| `get_summary` | Metadata for one or more articles: title, authors, journal, DOI. |
| `get_abstract` | Full abstract text with section labels (Background, Methods, Results, Conclusions). |

## Typical workflow

1. Search for articles on a topic with `search_pubmed`
2. Get metadata for the top results with `get_summary`
3. Pull the full abstract for the most relevant paper with `get_abstract`

## Example: find CRISPR research

```bash
curl -X POST https://gateway.pipeworx.io/pubmed/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_pubmed","arguments":{"query":"CRISPR cancer therapy","limit":5}}}'
```

## Query syntax tips

PubMed supports field-tagged searches. Some useful patterns:

- `"Smith J"[Author]` -- search by author
- `"COVID-19"[MeSH]` -- search MeSH terms
- `"Nature"[Journal]` -- restrict to a journal
- Combine with AND/OR: `CRISPR AND (cancer OR tumor)`

## Add to your MCP client

```json
{
  "mcpServers": {
    "pubmed": {
      "url": "https://gateway.pipeworx.io/pubmed/mcp"
    }
  }
}
```

No API key required. Powered by NCBI E-utilities.
