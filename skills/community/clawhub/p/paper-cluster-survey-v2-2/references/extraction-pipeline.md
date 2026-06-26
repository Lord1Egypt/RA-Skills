# Extraction Pipeline

The bundled extractor is designed to reduce context load before classification and review drafting.

## What the extractor does

- Normalize local paths and URLs into source records
- Fetch HTML pages and capture paper-oriented metadata when present
- Follow likely PDF URLs for direct paper downloads
- Extract text from PDFs using the best available local tool
- Build structured paper records with provenance notes

## Extraction trust levels

Treat fields differently depending on how they were obtained:

- High trust:
  - citation meta tags from the source page
  - PDF text extracted by `pdftotext`, `mutool`, or `python3 + pypdf`
- Medium trust:
  - HTML title and meta description
  - year inferred from citation metadata or DOI landing pages
- Low trust:
  - title or abstract inferred from noisy text fallback
  - PDF text recovered only via `strings`

## When to reopen the raw source

Re-open the raw source when:
- title and abstract are missing or obviously wrong
- classification depends on fine-grained method differences
- the review needs exact datasets, metrics, or limitations
- the extractor reports fallback warnings

## Common extractor outputs

The extractor tries to populate:
- `title`
- `authors`
- `year`
- `venue`
- `abstract`
- `text_excerpt`
- `source`
- `extraction_method`
- `extraction_notes`

Use the notes field as part of quality control. If the extractor had to degrade, say so in the final analysis when it matters.
