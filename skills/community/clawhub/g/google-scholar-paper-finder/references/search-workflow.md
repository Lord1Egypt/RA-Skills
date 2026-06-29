# Search Workflow

Use this reference when generating Google Scholar search strategies and running real-time Scholar retrieval through `google-scholar-search-mcp`. The default goal is to collect 50 deduped Google Scholar candidates, then rank them by relevance and quality.

## MCP Requirement

Use `google-scholar-search-mcp` as the Google Scholar retrieval layer. The MCP server is intended for searching Google Scholar papers, authors, citations, and BibTeX records.

Acceptable Google Scholar MCP actions include equivalent tools for:

- paper search;
- bulk paper search;
- advanced paper search;
- author lookup;
- citation tracking / cited-by expansion;
- paper details;
- BibTeX export.

If the connected MCP exposes different tool names, inspect the tool schema and map them to these actions. In the tested `google-scholar-search-mcp`, common tool names include `search_papers`, `bulk_search`, `search_author`, `get_paper_details`, `get_citations`, and `get_bibtex`.

Fail closed:

- If no Google Scholar MCP tool is available, tell the user that real Scholar retrieval cannot be performed in this session.
- If Scholar blocks, rate-limits, or returns captcha/empty data, report that limitation.
- Do not replace Scholar MCP results with PubMed, ordinary Google search results, generic web search, Crossref, Semantic Scholar, or publisher search.
- Do not fill missing fields from memory.

## Default Retrieval Depth

For a normal topic search:

1. Build 5-8 focused Scholar queries.
2. Retrieve about 10-20 results per query, depending on MCP limits and rate limits.
3. Dedupe by normalized title, then by DOI or Scholar cluster ID when available.
4. Keep at least 50 deduped candidates when Google Scholar returns enough usable results.
5. If the topic is broad, collect 80-100 raw candidates first and return the best 50.

Return fewer than 50 only when:

- Google Scholar returns fewer usable records;
- rate limiting or CAPTCHA prevents additional retrieval;
- the user's topic is intentionally narrow;
- the user requests a smaller list.

Always report raw result count, deduped candidate count, and final table count.

## Query Building

Google Scholar supports phrase search and simple operators, not true regex.

Useful patterns:

```text
"exact phrase"
("term A" OR "term B" OR "term C")
"core concept" "domain concept"
"core concept" "method concept" -irrelevant_term
author:"Surname"
allintitle: key phrase
```

Avoid overlong queries. Scholar often works better with several focused MCP searches.

Do not use regex inside Google Scholar. Use regex only after retrieval to filter titles, snippets, and metadata.

## Concept Matrix

Turn a topic into a matrix:

| Concept | Narrow terms | Broad terms | Related terms | Exclude |
|---|---|---|---|---|

Then generate query families:

- `A exact + B exact`
- `A synonyms + B exact`
- `A exact + C domain`
- `method + domain + outcome`
- `review/survey + topic`
- `guideline/consensus + topic`
- `highly cited/classic seed + topic`
- `recent term + topic`

For medical or clinical topics, use Google Scholar-only query families such as:

- `"topic" review`
- `"topic" guideline`
- `"topic" epidemiology`
- `"topic" diagnosis`
- `"topic" management`
- `"topic" treatment`
- `"topic" meta-analysis`

## Snowball Search

Start with 5-20 seed papers, then expand:

- **Forward**: papers that cite the seed papers.
- **Lateral**: related articles and shared-author papers.
- **Term mining**: new keywords from repeated titles, abstracts, and venue names.

Second-round queries should use terms found in good papers, not only the user's initial words.

## Recall And Precision Controls

If results are too few:

- remove one constraint;
- replace exact phrase with broader synonym;
- search only two concepts at a time;
- include abbreviations and older terminology;
- use a review paper as a seed.

If results are too noisy:

- add domain/context terms;
- add method/outcome terms;
- use exact phrases;
- exclude repeated false-positive terms;
- constrain by recent years manually in Scholar.

## Candidate Fields To Capture

Minimum:

- title;
- authors;
- year;
- venue;
- citation count;
- Scholar/access URL.
- source database (`Google Scholar`);
- source route (`query`, `cited-by`, `related-articles`, `seed-title`, `seed-author`, or `term-expansion`);
- source query.

Best effort:

- PDF URL;
- DOI;
- abstract/snippet;
- source route;
- Scholar result ID, cluster ID, or BibTeX if the MCP returns it.

## Ranking

Rank papers by a combined judgment:

- relevance to the user's topic or research question;
- venue authority from local IF/JCR/CAS/CCF/EI/core data;
- citation count as a secondary authority signal;
- recency when current evidence matters;
- document type fit, such as review, guideline, meta-analysis, RCT, empirical study, or methods paper.

Recommended sorting:

- `Core`: high relevance and strong quality.
- `Priority`: good relevance and good quality.
- `Reference`: useful but lower/unknown quality.
- `Check`: plausible but metadata or relevance needs manual verification.
- `Remove`: low relevance or weak evidence.

Do not keep a weakly related paper only because it is published in a famous journal.
