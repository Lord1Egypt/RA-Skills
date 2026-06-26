---
name: paper-cluster-survey-v2-2
description: Extract structured paper records from one or more local PDFs, arXiv links, DOI links, or general paper URLs, then classify the papers and write an academic survey review. Use when the task involves mixed paper sources, URL-first literature collection, PDF-based review drafting, taxonomy building, or producing a formal literature review from a paper set. By default, provide one classification table and one integrated review for the full corpus; only write separate reviews for each category when the user explicitly asks for per-category reviews.
---

# Paper Cluster Survey V2.2

## Overview

Turn raw paper URLs and PDFs into usable review inputs. Extract structured metadata and text evidence first, then classify the papers, produce a classification table, and write a review that follows common academic survey conventions instead of a rigid fill-in-the-blanks template.

## Workflow

### 1. Normalize the source set

- Accept multiple local PDF paths, arXiv URLs, DOI URLs, and general paper URLs.
- Use `scripts/normalize-sources.mjs` when the source set is mixed or should be stored as a reusable manifest.
- Preserve the original source string for traceability.

### 2. Extract paper records before reasoning

- Use `scripts/extract-paper-records.mjs` to turn PDFs and URLs into structured records before classification.
- The extraction pass should gather as much of the following as possible:
  - `title`
  - `authors`
  - `year`
  - `venue`
  - `abstract`
  - `task`
  - `method`
  - `datasets`
  - `metrics`
  - `main_contribution`
  - `limitations`
  - `source`
  - `extraction_notes`
- Treat extracted records as the primary context for classification and survey drafting.
- If important fields are missing, only fall back to direct source reading for the specific missing details.

Read [extraction-pipeline.md](./references/extraction-pipeline.md) when deciding how much to trust the extracted fields and when to re-open the raw source.

### 3. Verify evidence quality

- Do not classify from titles alone when abstract or body text is available.
- Prefer abstract, introduction, and method section.
- Mark uncertain inferences explicitly.
- If the extractor had to fall back to weak methods, keep claims conservative.

### 4. Design the classification scheme

- Produce a classification scheme before writing the review.
- Prefer task-based categories first.
- If tasks are too similar, classify by method family.
- Use application-domain categories only when they best explain the corpus.
- Keep the taxonomy shallow unless the corpus is large.
- Assign one primary category to each paper unless the user explicitly wants multi-label grouping.

Read [taxonomy-guidelines.md](./references/taxonomy-guidelines.md) when the category design is ambiguous.

### 5. Output the classification table

- Always provide one classification table before the review.
- Include:
  - paper
  - year
  - category
  - rationale
  - evidence used
- Keep rationales brief and evidence-based.

### 6. Decide the review shape

Default rule:
- Write one integrated literature review for the entire corpus after the classification table.

Exception:
- If the user explicitly asks for "each category write a survey", "分别写综述", "per-category review", or equivalent, write separate review sections for each category.

### 7. Write the review in academic survey style

The review must read like a normal survey paper, not a bullet summary dump.

- Use a concise academic title.
- Include an abstract when the output is formal enough to justify it.
- Include keywords when they help position the review.
- Use an introduction that explains background, significance, scope, source selection, and the organizing logic of the review.
- Organize the main body by the most defensible basis for the corpus:
  - chronology
  - research themes
  - method families
  - viewpoints or schools
- End with a conclusion or concluding discussion.
- Add future directions, outlook, or open problems when the corpus supports them.
- List references in GB/T 7714 style when bibliographic data is available.

Typical sections in a strong review are:
- title
- abstract
- keywords
- introduction
- themed main sections
- discussion, conclusion, or both
- future directions or open problems when useful
- references

Not every output needs every section. Match the structure to the user's request, the corpus size, and the field while staying recognizably review-like.

Read [review-paper-style.md](./references/review-paper-style.md) when drafting the prose review or choosing section structure.

### 8. Keep the prose review-like

- Prefer connected academic prose over bullet dumps.
- Use tables only to support comparison, not replace the review.
- Do not invent datasets, metrics, or reference details.
- If extracted metadata is incomplete, keep partial references and state what is missing.

## Output Contract

Return results in this order unless the user asks otherwise:
1. Corpus summary
2. Classification scheme
3. Classification table
4. Formal review article
5. References

If the user wants structured output, read [output-schema.md](./references/output-schema.md).

## Bundled Scripts

### `scripts/normalize-sources.mjs`

- Normalize mixed PDF and URL inputs into a JSON manifest.
- Use when the source set is large, mixed, or should be reused.

### `scripts/extract-paper-records.mjs`

- Fetch URLs, resolve likely paper metadata, and extract paper text evidence from URLs or PDFs.
- Prefer this script before asking the model to reason over a large source set.
- Use its output as the main context object for classification and review drafting.

### `scripts/render-formal-review-template.mjs`

- Render a flexible academic-review scaffold from structured paper records.
- Default to one integrated review.
- Use `--per-category` only when the user explicitly asks for separate category reviews.

## Quality Bar

- Run extraction before classification unless the user already gave structured paper records.
- Keep classification and review consistent with extracted evidence.
- Use raw source re-reading only to fill important gaps.
- If the extractor had to rely on weak fallbacks, say so.
