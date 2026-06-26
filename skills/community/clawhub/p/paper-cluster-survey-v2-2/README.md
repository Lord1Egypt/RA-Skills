# Paper Cluster Survey

Extract, classify, and review academic papers from PDFs or URLs.

## Overview

Paper Cluster Survey is an OpenClaw skill that transforms raw paper sources (local PDFs, arXiv links, DOI links, or paper URLs) into structured metadata records, classifies them, and produces an academic survey review following common scholarly conventions.

## Features

- **Multi-source support**: Local PDFs, arXiv URLs, DOI links, and general paper URLs
- **Structured extraction**: Extracts title, authors, year, venue, abstract, methods, datasets, and metrics
- **Intelligent classification**: Task-based, method-based, or application-based categorization
- **Academic output**: Generates review articles in standard academic survey format
- **Evidence tracking**: Every classification includes source evidence

## Workflow

1. **Normalize sources** - Convert mixed inputs into a reusable JSON manifest
2. **Extract records** - Pull structured metadata from PDFs and URLs
3. **Verify quality** - Check extraction confidence levels
4. **Design taxonomy** - Create classification scheme based on research tasks or methods
5. **Generate review** - Write academic survey following scholarly conventions

## Usage

### Normalize sources

```bash
node scripts/normalize-sources.mjs --out sources.json paper1.pdf https://arxiv.org/abs/1234.5678
```

### Extract paper records

```bash
node scripts/extract-paper-records.mjs --manifest sources.json --out papers.json
```

### Render formal review

```bash
node scripts/render-formal-review-template.mjs --in papers.json --out review.md
```

For per-category reviews:

```bash
node scripts/render-formal-review-template.mjs --in papers.json --out review.md --per-category
```

## Output Structure

The skill produces:

1. **Corpus summary** - Overview of the paper collection
2. **Classification scheme** - Taxonomy design rationale
3. **Classification table** - Papers with categories and evidence
4. **Formal review** - Academic survey article
5. **References** - GB/T 7714 formatted bibliography

## Extraction Trust Levels

| Level | Source | Fields |
|-------|--------|--------|
| High | PDF text (pdftotext/mutool/pypdf) | Full metadata |
| Medium | HTML metadata tags | Title, abstract, authors |
| Low | Text fallback (strings) | Partial data only |

## Requirements

- Node.js 18+ (ES Modules)
- Optional: `pdftotext`, `mutool`, or `python3 + pypdf` for PDF extraction

## Project Structure

```
paper-cluster-survey-v2-2/
├── agents/
│   └── openai.yaml           # AI Agent configuration
├── references/
│   ├── extraction-pipeline.md
│   ├── output-schema.md
│   ├── review-paper-style.md
│   └── taxonomy-guidelines.md
├── scripts/
│   ├── extract-paper-records.mjs
│   ├── normalize-sources.mjs
│   └── render-formal-review-template.mjs
├── SKILL.md
└── README.md
```

## License

MIT License

## References

See the `references/` directory for detailed guidelines on extraction pipelines, output schemas, review paper style, and taxonomy design.
