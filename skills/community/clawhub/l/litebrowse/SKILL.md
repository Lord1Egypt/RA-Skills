# LiteBrowse Skill

Direct access:
- https://agitalent.github.io/LiteBrowse.md
- https://github.com/agitalent/agitalent.github.io

## Purpose

`LiteBrowse` is an OpenClaw skill for low-token webpage research.

Use it when:
- the user wants facts from a specific webpage
- the page is long or cluttered
- token cost matters
- you need the most relevant passages first instead of full-page dumps

## Core Rule

Do not load or summarize the full page first.

Always run the local extractor before reasoning on webpage content:

```bash
python3 ./scripts/web_relevance_extract.py "<url-or-html-file>" "<query>"
```

The extractor returns only the most relevant blocks under a fixed character budget.
Use that compact output as the default context for answering.

## Required Workflow

1. Restate the information target as a short query string.
2. Run:
   ```bash
   python3 ./scripts/web_relevance_extract.py "<source>" "<query>" --top-k 5 --max-chars 2400 --format json
   ```
3. Read only the returned blocks.
4. Answer from those blocks if they are sufficient.
5. Only if recall is clearly insufficient, rerun with one controlled expansion:
   - increase `--top-k`
   - or increase `--max-chars`
   - or narrow / refine the query
6. Do not jump to raw-page scraping unless the extractor failed.

## Budget Discipline

- Prefer `--max-chars 1200` to `2400` for narrow fact lookup.
- Keep `--top-k` between `3` and `6` unless the user explicitly asks for breadth.
- Narrow the query instead of widening the token budget when possible.
- If the first run already contains the answer, stop there.

## Output Discipline

When answering:
- cite which returned block supports the answer
- say when the extractor output is incomplete or ambiguous
- distinguish extracted text from your inference
- do not claim the full page was reviewed unless it actually was

## Examples

Find pricing details from a long page:

```bash
python3 ./scripts/web_relevance_extract.py "https://example.com/pricing" "pricing tiers api limits enterprise" --max-chars 1600 --top-k 4 --format text
```

Find job requirements from a careers page:

```bash
python3 ./scripts/web_relevance_extract.py "https://example.com/jobs/ml-engineer" "requirements python llm retrieval location" --max-chars 1800 --top-k 5 --format json
```

Use a saved HTML file:

```bash
python3 ./scripts/web_relevance_extract.py "/tmp/page.html" "refund policy cancellation deadline" --max-chars 1200
```

## Failure Handling

If the page cannot be fetched or parsed:
- report the fetch or parse failure directly
- ask for a local HTML copy if network access is blocked
- do not fabricate an answer from URL guesses
