---
name: paper-ingest-normalizer
description: "Normalize papers, PDFs, URLs, and literature notes into structured research records for project memory and retrieval. Use when: (1) a new paper, PDF, DOI, or article enters the system, (2) literature format is inconsistent, (3) researcher needs standardized extraction, (4) project memory needs clean paper records. Triggered by requests like read this paper, ingest this PDF, normalize this literature, 整理这篇文献, or when raw literature needs to become structured project memory."
---

# Paper Ingest Normalizer

Convert raw literature inputs into standardized records safe for project memory, paper databases, and downstream synthesis pipelines.

## Input

One of the following is required:
- `pdf_path` — local path to PDF file
- `url` — link to paper/article
- `raw_text` — extracted or pasted text
- `metadata_blob` — existing metadata dict

Plus:
- `project_id` — required for any writeback
- `source_type` — one of: `pdf`, `doi`, `url`, `text`, `metadata`
- `optional tags` — list of strings for categorization

## Output Schema

Return a structured object:

```
title: string
authors: string[] | null
year: number | null
source: string          # journal, conference, preprint, etc.
doi_or_url: string | null
project_id: string
paper_type: string      # experimental, theoretical, review, etc.
material_system: string | null   # e.g. "钙钛矿太阳能电池", " graphene FET"
device_type: string | null       # e.g. "FTO/glass", "flexible substrate"
key_variables: string[] | null   # independent variables studied
key_metrics: string[] | null     # measured outcomes (PCE, mobility, etc.)
core_findings: string            # 2-3 sentence neutral summary
claimed_mechanism: string | null
limitations: string | null
normalized_summary: string       # 1-2 paragraph structured summary
uncertain_fields: string[] | null  # fields that could not be verified
writeback_ready: boolean        # true only if key identity fields present
writeback_payload: object        # the record to write into project memory
```

## Rules

1. **Never write into project memory without project_id.** Ask if not provided.
2. **Separate direct observations from claimed interpretations.** Mark inference vs. direct extraction.
3. **Preserve uncertainty.** Use `null` for missing fields; list in `uncertain_fields`.
4. **Do not invent missing bibliographic fields.** Don't hallucinate authors, year, etc.
5. **Do not over-claim.** Keep `core_findings` and `normalized_summary` grounded in what the text actually says.
6. **Never conflate abstract with findings.** The abstract states intentions; findings are what the data supports.
7. If `writeback_ready = false`, list explicitly which fields are missing and why.

## PDF Extraction

For PDFs, use the `summarize` skill or `pdfplumber`/`PyMuPDF` to extract text before processing.

## Workflow

1. **Identify source type** — determine which input field is populated
2. **Extract raw content** — PDF text, URL content, or use provided raw text
3. **Parse bibliographic fields** — title, authors, year, source, DOI
4. **Identify research content** — material system, device type, variables, metrics
5. **Distill findings** — separate what was measured from what was claimed
6. **Assemble writeback_payload** — structured record matching the schema above
7. **Assess completeness** — set `writeback_ready` based on presence of key identity fields

## Failure Handling

If parsing is incomplete:
- Return partial structured output with all successfully extracted fields
- Populate `uncertain_fields` with the list of fields that could not be determined
- Set `writeback_ready = false` when title, authors, or year are missing

## Cross-Reference

For synthesis after normalization, see the `research` skill for paper synthesis workflows.
