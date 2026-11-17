---
name: origin-office
description: Native documents (docx/pptx) → verifiable objects — conversion IS the semantic transaction. Zero-dependency parsing of docx chapters/articles/paragraphs/tables (merged cells expanded, checkboxes preserved) and pptx slides/shapes/tables (placeholder types, gridSpan merges). Each structure becomes one object in a Benxiang package; a SHA-256 structure fingerprint is recorded, and `verify` proves the package matches the source file (tampering detected). The industry aims its firepower at scanned PDFs (OCR has physical error); lossless structuring of native electronic documents is what nobody does seriously — Benxiang turns words into verifiable state objects. Use when docx/pptx must become AI-anchorable, verifiable structure, or for document version tracking / clause-level citation. (中文版见 SKILL.md)
version: 1.1.1
slug: origin-office
license: Apache-2.0
displayName: origin-office — Verifiable Structuring of Native Documents
summary: docx/pptx native structure → verifiable objects: chapters/articles/tables/slides stored per-structure, SHA-256 fingerprint, conversion as semantic transaction.
metadata:
  openclaw:
    runtime: node >= 18
    tags: [office, docx, pptx, document, structure, verify]
---

# origin-office · Native Documents as Benxiang Objects

> Hand a red-header official document to an AI and it sees fragments carved up by OCR
> or text-box extraction. Yet the docx plainly says "Chapter 1, Article 50, table Q112,
> merged cells" — **native electronic documents carry structure losslessly**, and the
> industry still treats them like scans to be guessed at.
> This skill imports docx/pptx into a Benxiang package, turning chapters, articles,
> tables, and slides into anchorable, verifiable objects.

## Install

```bash
# The Benxiang protocol repo
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin

# Verify
npm run test:office    # 20 assertions (docx + pptx synthetic fixtures + unified CLI: build/verify/tamper detection)
```

## Usage

```bash
# Unified CLI: docx/pptx → Benxiang package (conversion IS the semantic transaction)
node adapters/office/cli.mjs import file.docx report.origin --name "Report Name"
node adapters/office/cli.mjs import deck.pptx deck.origin

# Inspect structure only, no package
node adapters/office/cli.mjs inspect file.docx

# Verify: recompute the source file hash and compare with the package fingerprint (any edit is detected)
node adapters/office/cli.mjs verify report.origin file.docx && echo consistent

# Legacy usage: docx → markdown (chapter → ##, article → ###, table → GFM pipe table)
node adapters/office/import.mjs file.docx output.md
node adapters/office/import.mjs file.docx --json
```

## Objects produced

- docx: `par:*` (paragraphs, with chapter/article anchors), `tbl:*` (tables, post-merge row/column grid)
- pptx: `sldNN-shp*` (shapes, with placeholder type title/subTitle/body), `sldNN-tbl*` (tables)
- Every package carries fact objects: `fact:structure-hash` (SHA-256 structure fingerprint), `fact:stats`

After the package is built, read it with the Benxiang protocol CLI:

```bash
node compiler/cli.mjs status  report.origin    # package overview
node compiler/cli.mjs why     report.origin par:0003.text   # why is this value what it is
node compiler/cli.mjs history report.origin    # every change
```

## Verifiability (the essential difference from the scanned-PDF route)

| | Scanned-PDF route (MinerU/Docling/LlamaParse) | Benxiang (native docx/pptx) |
|---|---|---|
| Input | Scans/PDF; physical error is a hard floor | Native electronic documents; structure is lossless |
| Tables | OmniDocBench TEDS ≈ 0.78, lower for Chinese | Merged cells expanded via gridSpan/vMerge; every cell anchorable |
| Verifiable | None (output is the final state) | Conversion = transaction; structure fingerprint stored; `verify` re-checks |

## Verification

```bash
npm run test:office    # 20 assertions: docx structure restore 11 + pptx parsing 5 + unified CLI build/fingerprint/tamper 4
```

Real case: the Maritime Safety Administration's 2019 "Rules on Quality Management for Seafarer Training
and Seafarer Management" red-header document → 409 structural objects (6 chapters /
77 articles / 16 tables / 59 checkboxes), verify consistent.

## Related

- Benxiang protocol (benxiang-protocol): persistent object representation + semantic
  transactions + evidence chains.
- xlsx dialect: spreadsheets (formula dependency graph) have a dedicated importer at adapters/xlsx/.

---
