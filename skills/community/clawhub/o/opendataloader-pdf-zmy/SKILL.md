---
name: opendataloader-pdf
description: OpenDataLoader PDF — AI-ready PDF parser. Parse PDFs into Markdown/JSON/HTML for RAG pipelines, extract tables with bounding boxes, OCR scanned PDFs, and enrich charts/formulas with AI descriptions. Use when: (1) parsing PDFs for knowledge bases or RAG systems; (2) extracting structured data from medical reports, academic papers, invoices; (3) building AI knowledge bases from PDF documents; (4) converting PDF documents to Markdown/JSON for further processing; (5) any PDF-to-LLM data extraction task.
---

# OpenDataLoader PDF Skill

## Quick Install

```bash
# Basic (CPU, ~20 pages/sec)
pip install -U opendataloader-pdf

# Hybrid mode (AI-enhanced, for complex docs, ~2 pages/sec)
pip install -U "opendataloader-pdf[hybrid]"

# LangChain integration
pip install langchain-opendataloader-pdf
```

**Requirements:** Java 11+ (for hybrid mode), Python 3.10+

---

## Core Usage Patterns

### 1. Parse PDF → Markdown (best for RAG chunking)

```python
from opendataloader_pdf import convert

convert(
    input_path=["file1.pdf", "folder/"],
    output_dir="output/",
    format="markdown"  # clean text, LLM-ready
)
```

### 2. Parse PDF → JSON (with bounding boxes for citations)

```python
convert(
    input_path=["report.pdf"],
    output_dir="output/",
    format="json",           # structured data + coordinates
    image_output="embedded"  # "off" | "embedded" | "external"
)
```

### 3. LangChain + RAG Pipeline

```python
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = OpenDataLoaderPDFLoader(file_path="document.pdf", format="text")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
# → embed → vector store → RAG
```

---

## CLI Commands

```bash
# Basic: single file or folder
opendataloader-pdf file1.pdf file2.pdf folder/

# Complex tables / nested structure (hybrid mode)
opendataloader-pdf --hybrid docling-fast file1.pdf

# Start hybrid backend first, then:
opendataloader-pdf-hybrid --port 5002
# (in another terminal)
opendataloader-pdf --hybrid docling-fast file1.pdf

# OCR for scanned PDFs
opendataloader-pdf-hybrid --port 5002 --force-ocr file1.pdf

# Math formula extraction (LaTeX)
opendataloader-pdf-hybrid --enrich-formula
opendataloader-pdf --hybrid docling-fast --hybrid-mode full file1.pdf

# Chart/image AI description
opendataloader-pdf-hybrid --enrich-picture-description
opendataloader-pdf --hybrid docling-fast --hybrid-mode full file1.pdf

# Security: sanitize prompt injection
opendataloader-pdf file1.pdf --sanitize
```

---

## Output Format Selection Guide

| Document Type | Recommended Format | Mode |
|--------------|-------------------|------|
| Standard digital PDF | `markdown` | Basic |
| Complex/nested tables | `json` | Hybrid |
| Scanned PDFs | any + `--force-ocr` | Hybrid |
| Math formulas | `markdown` + `--enrich-formula` | Hybrid |
| Charts needing description | `markdown` + `--enrich-picture-description` | Hybrid |
| Medical reports (cite-able) | `json` | Hybrid |
| RAG knowledge base | `markdown` | Basic or Hybrid |

---

## Key Reference Files

- [API Reference](references/api-reference.md) — Full Python API, all parameters
- [CLI Reference](references/cli-reference.md) — All CLI flags and hybrid mode
- [Examples](references/examples.md) — RAG pipeline, table extraction, batch processing

---

## Benchmark Results (v2.0)

| Metric | Score |
|--------|-------|
| Overall Accuracy | **0.90** |
| Reading Order | 0.94 |
| Table Accuracy | 0.93 |
| Heading Accuracy | 0.83 |

**License:** Apache 2.0 | GitHub: `opendataloader-project/opendataloader-pdf`
