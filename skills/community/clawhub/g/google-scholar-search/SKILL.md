---
name: google-scholar-search
description: Academic paper search using Semantic Scholar API. Free API - no key required. Search research papers, get citations, abstracts, authors, and download PDFs. Use when searching academic literature, finding research papers on specific topics, finding citation counts and paper metadata, getting paper abstracts and author information, or looking for papers from specific years or with minimum citations.
---

# Google Scholar Search

Search academic papers using the free Semantic Scholar API. No API key required.

## Quick Start

Basic search:
```bash
python3 {baseDir}/scripts/search_papers.py "machine learning transformers"
```

Search with filters:
```bash
python3 {baseDir}/scripts/search_papers.py "deep learning" --limit 5 --year 2020-2023 --min-citations 10
```

## Search Options

- `--limit N`: Number of results (default: 10, max: 100)
- `--year YYYY-YYYY`: Filter by year range (e.g., "2020-2023" or "2023")
- `--min-citations N`: Minimum citation count
- `--json`: Output in JSON format for machine processing

## Get Paper Details

Retrieve detailed information about a specific paper:
```bash
python3 {baseDir}/scripts/search_papers.py --details <paper-id>
```

## Returned Data

Each paper includes:
- **title**: Paper title
- **authors**: List of authors with names
- **year**: Publication year
- **venue**: Journal or conference name
- **citationCount**: Number of citations
- **abstract**: Paper abstract
- **url**: Link to Semantic Scholar page
- **openAccessPdf**: Direct PDF link if available
- **paperId**: Unique Semantic Scholar ID (for details lookup)

## Examples

Search for recent AI papers:
```bash
python3 {baseDir}/scripts/search_papers.py "large language models" --year 2022-2024 --limit 10
```

Find highly cited papers on a topic:
```bash
python3 {baseDir}/scripts/search_papers.py "quantum computing" --min-citations 50 --limit 10
```

Get JSON output for integration:
```bash
python3 {baseDir}/scripts/search_papers.py "neural networks" --json --limit 20
```

## Tips

- Use specific keywords for better results
- Filter by year to get recent research
- Use `--min-citations` to find influential papers
- The API is free and requires no authentication
- For complex queries, try multiple related terms
