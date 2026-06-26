---
name: arxiv-related-papers
description: Search and download related arXiv papers by topic plus date range, or from a seed paper title/id. Use when user asks to crawl related papers, collect arXiv articles, or bulk download PDFs into an arxiv folder with structured filenames.
---

# arXiv Related Papers Downloader

## What this skill does

- Accepts either:
  - `topic + time range`, or
  - `seed paper (arXiv id or title)`
- Finds related papers from arXiv API.
- Downloads PDF files into `arxiv/`.
- Uses filename format: `versionDate-title.pdf`, where `versionDate` is `vN_YYYYMMDD`.

## When to use

Use this skill when the user asks to:

- crawl/search related papers by topic;
- find related papers from one article;
- download arXiv PDFs in batch;
- save with a deterministic naming rule.

## Required user input

The user must provide one of these modes:

1. **Topic mode**
   - `topic`
   - `start date` (`YYYY-MM-DD`)
   - `end date` (`YYYY-MM-DD`)

2. **Seed paper mode**
   - `seed arXiv id` (preferred) or `seed title`
   - optional `start date` / `end date`

Optional:

- `max results` (default: `20`)

## Execution steps

1. Confirm missing parameters with the user.
2. Run the script from workspace root:

```bash
# Topic mode
python ./arxiv-related-papers/scripts/download_arxiv.py \
  --topic "graph neural network" \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --max-results 20

# Seed mode by arXiv id
python ./arxiv-related-papers/scripts/download_arxiv.py \
  --seed-id "2401.12345v1" \
  --max-results 20

# Seed mode by title
python ./arxiv-related-papers/scripts/download_arxiv.py \
  --seed-title "Attention Is All You Need" \
  --start-date 2018-01-01 \
  --end-date 2024-12-31 \
  --max-results 20
```

3. Report back:
   - how many papers were found;
   - how many PDFs were downloaded;
   - the output directory path.

## Output location and naming

- Output dir: `./arxiv/` (auto-created if missing)
- File naming rule:
  - `v1_20240213-Your_Paper_Title.pdf`
  - `v3_20231105-Your_Paper_Title.pdf`

## Notes

- The script only uses Python standard library.
- If a paper has no PDF link or download fails, it is skipped with a warning.
- Existing files are not downloaded again.
