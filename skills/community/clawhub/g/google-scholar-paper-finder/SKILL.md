---
name: google-scholar-paper-finder
description: Use when the user wants to find more relevant academic papers through real-time Google Scholar retrieval with google-scholar-search-mcp, expand search terms from a research topic or seed paper, screen papers by venue quality, or return a ranked literature table with title, authors, year, journal/conference, impact factor, JCR/CAS/CCF/EI/core tags, citations, download/access links, source evidence, and recommendation reasons. Triggers include "Google Scholar 找论文", "google-scholar-search-mcp", "实时搜索论文", "找更多相关论文", "高质量论文筛选", "影响因子", "CCF", "EI", "CSSCI", "北大核心", "文献检索", "参考文献滚雪球", and "返回论文表格".
---

# Google Scholar Paper Finder

Use this Skill to solve two linked problems:

1. Find a broad but controlled pool of relevant papers through real Google Scholar retrieval using `google-scholar-search-mcp`, query expansion, seed papers, citations, and related articles.
2. Keep high-quality papers by scoring venues with local journal/conference quality data and returning a clear table.

## Retrieval Contract

Use real retrieval. Do not invent papers, citation counts, authors, venues, DOI values, abstracts, or download links.

Required retrieval order:

1. Use `google-scholar-search-mcp` for Google Scholar results.
2. Retrieve, dedupe, and keep at least 50 Google Scholar candidates whenever Scholar returns enough usable records.
3. Use cited-by, related-article, seed-author/title, and query-expansion routes inside Google Scholar when the initial results are too narrow.
4. Use local JSON quality data only after retrieval, never as a discovery source.

Fail closed:

- If `google-scholar-search-mcp` is not available, blocked, rate-limited, or returns no usable data, say so explicitly and stop or ask to install/connect it.
- Do not silently replace Google Scholar with PubMed, ordinary Google, generic web search, Crossref, Semantic Scholar, publisher pages, or model memory.
- Publisher pages, DOI pages, PDF pages, or repository pages may verify or provide access links, but they must not be presented as Google Scholar search evidence.

Google Scholar does not support true regular expressions. Generate Scholar-compatible search queries with phrases, `OR`, exclusion terms, and concept combinations. Use regex or keyword patterns only after retrieval to filter titles, snippets, abstracts, and references.

## Workflow

### 1. Clarify The Search Target

Extract or ask for the minimum context needed:

- research topic or question;
- language preference: English, Chinese, or both;
- discipline and methods if known;
- desired years if any;
- whether to prioritize journal papers, conferences, reviews, empirical studies, or methods;
- any seed paper, DOI, title, or author already known.

If the user gives a Chinese topic, generate English academic terms as the default search layer, and keep Chinese terms when Chinese literature is relevant.

### 2. Generate Search Expansion

Break the topic into 2-4 core concepts:

- object/population;
- method/technology;
- context/domain;
- outcome/problem.

For each concept, generate:

- exact phrase terms;
- synonyms and academic variants;
- abbreviations;
- narrower and broader terms;
- likely negative terms to exclude.

Create multiple Google Scholar MCP queries rather than one giant query:

- narrow query for precision;
- broad query for recall;
- review query;
- guideline/consensus query when the discipline uses guidelines;
- highly cited/classic query;
- method query;
- recent-year query;
- seed-paper author/title query when available.

See [search-workflow.md](references/search-workflow.md) for query patterns and MCP-specific rules.

### 3. Retrieve Candidate Papers

Use `google-scholar-search-mcp` to collect candidates. Default target:

- collect 50 deduped Google Scholar papers for normal topic searches;
- collect 80-100 candidates first when the topic is broad, then return the best 50;
- return fewer only when Google Scholar does not provide enough usable results, and say how many were found.

For each candidate, capture as many fields as possible:

- title;
- authors;
- year;
- journal or conference venue;
- citation count;
- Google Scholar URL or Scholar result identifier;
- PDF/download URL if visible;
- DOI or publisher URL if available;
- snippet/abstract if available;
- source database: `Google Scholar`;
- source route: query, cited-by, related-articles, seed-title, seed-author, or term-expansion;
- query string that found the paper.

Do not promise every paper has a free PDF. Use "download/access link" and prefer PDF links when visible; otherwise use publisher, DOI, or Scholar links.

### 4. Expand By Citation Chaining

Use citation chaining before concluding the search is complete:

- use "Cited by" for forward chaining;
- use "Related articles" for lateral expansion;
- search exact titles of high-quality seed papers to recover variants, publisher links, and related clusters;
- search core authors from the best seed papers when the field is small;
- extract recurring terms from titles/snippets and generate second-round queries;
- keep a deduped candidate list.

Stop expanding when 50 deduped candidates are collected, or when new results repeat the same venues/authors/keywords after at least two query rounds.

### 5. Score Quality

Use optional local venue-quality data after retrieval:

- `journal_scores.json`
- `ccf_conferences.json`
- `eiiRankingName.json`
- `chinese_journal_tags.json`

The default quality-data directory is the skill's `data/` folder. Users can also set `SCHOLAR_QUALITY_DATA_DIR` or pass `--data-dir`.

Use `scripts/score_papers.py` whenever the candidate list is available as JSON or CSV. The script enriches papers with impact factor, JCR quartile, CAS zone, CCF rank, EI tag, Chinese core tags, quality score, and recommendation tier. If the quality files are missing, the script must still return a ranked table and mark unmatched venues as `unknown venue`.

Example:

```bash
python3 scripts/score_papers.py candidates.json \
  --markdown papers.md \
  --json enriched.json
```

If no candidate file exists, score manually using the same rules in [quality-scoring.md](references/quality-scoring.md).

### 6. Rank By Relevance And Quality

Never recommend a paper only because the venue is prestigious. Use this hierarchy:

- high relevance + high-quality venue: core must-read;
- high relevance + decent/unknown venue: useful reference;
- weak relevance + high-quality venue: optional background;
- weak relevance + unknown/low-quality venue: remove or mark cautious.

If relevance cannot be verified from title/snippet/abstract, mark it as "needs manual check" instead of pretending confidence.

Default ranking should combine:

- relevance to the user's topic or research question;
- source quality from IF, JCR/CAS, CCF, EI, or Chinese core tags;
- citation count as a secondary authority signal;
- recency when the user asks for current research or clinical guidance.

## Final Output

Return a Markdown table by default. Include:

| Tier | Source | Title | Authors | Year | Venue | IF | Rank/Tags | Citations | Access | Why keep |
|---|---|---|---:|---:|---|---:|---|---:|---|---|

Use these recommendation tiers:

- `Core`: highly relevant and high-quality source.
- `Priority`: relevant and quality source.
- `Reference`: relevant but source quality is modest or unknown.
- `Check`: potentially useful but needs manual verification.
- `Remove`: low relevance or weak evidence.

Also include:

- search queries used;
- tools/sources used, especially whether `google-scholar-search-mcp` succeeded;
- candidate-pool size, dedupe count, and final result count;
- expansion terms discovered;
- inclusion/exclusion notes;
- limitations such as missing abstracts, missing PDFs, or unmatched venues.
