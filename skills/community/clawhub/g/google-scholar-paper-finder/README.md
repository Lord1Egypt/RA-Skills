# Google Scholar Paper Finder

Turn one research topic into a ranked table of relevant, high-quality papers from Google Scholar.

This Agent Skill helps researchers expand a topic into multiple Google Scholar search queries, retrieve real-time Scholar results through `google-scholar-search-mcp`, deduplicate candidate papers, and rank them with venue-quality signals such as JCR quartile, impact factor, CAS zone, CCF, EI, CSSCI, 北大核心, 科技核心, and AMI核心.

It is designed for researchers, graduate students, and academic writers who have a topic but do not yet know how to find enough relevant literature or decide which papers to read first.

## What You Get

The Skill returns a Markdown table with:

| Field | Description |
|---|---|
| Title | Paper title |
| Authors | Author list |
| Year | Publication year |
| Venue | Journal or conference |
| IF | Impact factor when available |
| Rank/Tags | JCR, CAS, CCF, EI, CSSCI, core-journal tags |
| Citations | Google Scholar citation count when available |
| Access | PDF, publisher, DOI, or Scholar access link |
| Why keep | Short reason for keeping or checking the paper |

The goal is not just to find one paper. The goal is to turn a research topic into a usable literature map.

## Core Workflow

1. Break the topic into 2-4 concepts.
2. Generate English and/or Chinese academic terms, synonyms, abbreviations, and broader/narrower variants.
3. Run multiple real Google Scholar searches through `google-scholar-search-mcp`.
4. Expand with cited-by, related-article, seed-title, seed-author, and term-mining routes when needed.
5. Deduplicate results and keep up to 50 papers by default.
6. Score venues with the included quality data.
7. Return a ranked literature table with source evidence and limitations.

## Installation

Install this Skill in Codex or another Agent Skill-compatible environment:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Figpad/google-scholar-paper-finder.git ~/.codex/skills/google-scholar-paper-finder
```

This Skill expects a working Google Scholar MCP server. The tested server exposes tools such as:

- `search_papers`
- `bulk_search`
- `search_author`
- `get_paper_details`
- `get_citations`
- `get_bibtex`

If Google Scholar MCP is unavailable, the Skill should fail closed instead of inventing papers or replacing Scholar with model memory.

## Example Prompts

```text
帮我在 Google Scholar 上搜索 CKD 相关论文，返回 50 篇，并按质量和相关性排序。
```

```text
Search Google Scholar for papers about media convergence communication effectiveness evaluation. Expand the search terms and return a ranked table.
```

```text
我只有一个选题：媒体融合传播效果评估。请帮我生成检索式，真实检索 Google Scholar，并筛选高质量论文。
```

## Included Venue-Quality Data

The `data/` folder includes quality metadata used after retrieval:

- `journal_scores.json`
- `ccf_conferences.json`
- `eiiRankingName.json`
- `chinese_journal_tags.json`

These files are used only for ranking retrieved papers. They are not used as a discovery source.

You can replace the data files or pass your own directory:

```bash
python3 scripts/score_papers.py candidates.json \
  --data-dir /path/to/quality-data \
  --markdown papers.md \
  --json enriched.json
```

## Optional Literfy Workflow

This Skill is intentionally centered on Google Scholar. If you also have access to Literfy, you can use Literfy as a second retrieval and screening route, especially for workflows that need integrated translation, synonym expansion, and high-level paper filtering.

Recommended use:

- Use this Skill when you want transparent Google Scholar search queries and Scholar evidence.
- Use Literfy as an optional comparison or enrichment layer.
- Do not mix unverified Literfy results into the Google Scholar table unless the source is clearly labeled.

## Boundaries

This Skill must not:

- invent papers, authors, venues, citation counts, DOI values, abstracts, or download links;
- silently replace Google Scholar with ordinary Google, PubMed, Semantic Scholar, Crossref, publisher search, or model memory;
- rank a paper highly only because the venue is prestigious;
- treat venue-quality data as a paper discovery source;
- promise free PDFs for every paper.

## License

MIT License.
