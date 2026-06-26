---
name: opendataloader-pdf
description: Use when parsing PDFs for RAG pipelines, extracting structured data from PDFs, or converting PDFs to Markdown/JSON with bounding boxes for AI processing
attribution: Based on OpenDataLoader PDF (https://github.com/opendataloader-project/opendataloader-pdf), licensed under Apache 2.0
---

> This skill is based on [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf), licensed under Apache License 2.0.

# OpenDataLoader PDF

PDF parser for AI-ready data extraction. Open-source. #1 in benchmarks (0.90 overall accuracy).

## Prerequisites

- **Java 11+** required (run `java -version` to verify)
- Python 3.10+ or Node.js 18+

## Installation

```bash
# Python
pip install -U opendataloader-pdf

# Python with hybrid AI mode (for complex documents)
pip install -U "opendataloader-pdf[hybrid]"

# Node.js
npm install @opendataloader/pdf
```

## Quick Start

### Python

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path=["file1.pdf", "file2.pdf", "folder/"],
    output_dir="output/",
    format="markdown,json"  # Output formats: markdown, json, html
)
```

### Node.js

```typescript
import { convert } from '@opendataloader/pdf';

await convert(['file1.pdf', 'file2.pdf'], {
  outputDir: 'output/',
  format: 'markdown,json'
});
```

### CLI

```bash
# Fast local mode (0.05s/page)
opendataloader-pdf file1.pdf file2.pdf -o output/

# With hybrid AI mode (higher accuracy for complex docs)
opendataloader-pdf --hybrid docling-fast file1.pdf
```

## Mode Selection

| Document Type | Mode | Command |
|---------------|------|---------|
| Standard digital PDF | Fast (default) | `pip install opendataloader-pdf` |
| Complex tables | Hybrid | `pip install "opendataloader-pdf[hybrid]"` + start server |
| Scanned PDFs | Hybrid + OCR | `opendataloader-pdf-hybrid --force-ocr` |
| Multi-language scanned | Hybrid + OCR | `--ocr-lang "zh,en"` |
| Mathematical formulas | Hybrid + formula | `--enrich-formula` |
| Charts needing description | Hybrid + picture | `--enrich-picture-description` |

## Benchmark Comparison

| Engine | Overall | Table | Speed (s/page) |
|--------|---------|-------|----------------|
| **opendataloader [hybrid]** | **0.90** | **0.93** | 0.43 |
| opendataloader (local) | 0.72 | 0.49 | **0.05** |
| docling | 0.86 | 0.89 | 0.73 |
| marker | 0.83 | 0.81 | 53.93 |
| pymupdf4llm | 0.57 | 0.40 | 0.09 |

## Key Features

- **Bounding boxes** for every element (for source citations in RAG)
- **XY-Cut++** reading order for multi-column layouts
- **100% local** - no data sent to cloud
- **AI safety filters** - prompt injection protection
- **Table extraction** - borderless tables via hybrid mode
- **OCR** - 80+ languages via hybrid mode
- **Formula extraction** - LaTeX output

## LangChain Integration

```bash
pip install langchain-opendataloader-pdf
```

```python
from langchain_opendataloader_pdf import OpenDataLoaderPDF

loader = OpenDataLoaderPDF(file_path="document.pdf")
docs = loader.load()
```

## Output Formats

- **markdown**: Structured text with heading hierarchy
- **json**: Element-level with bounding boxes, page numbers, types
- **html**: Rich formatted output

JSON output includes:
- `type`: paragraph, heading, table, image, etc.
- `content`: text content
- `bbox`: `[left, bottom, right, top]` in PDF points
- `page`: page number
- `heading_level`: for headings

## Common Issues

| Issue | Solution |
|-------|----------|
| "java not found" | Install JDK 11+ from adoptium.net |
| Slow repeated calls | Batch files in single call; each spawns JVM |
| Poor table accuracy | Use hybrid mode (`--hybrid docling-fast`) |
| Scanned PDF not extracted | Use hybrid mode with `--force-ocr` |
| Non-English OCR not work | Specify `--ocr-lang "zh,en"` |

## Resources

- [Quick Start](https://opendataloader.org/docs/quick-start-python)
- [Hybrid Mode Guide](https://opendataloader.org/docs/hybrid-mode)
- [JSON Schema](https://opendataloader.org/docs/json-schema)
- [LangChain Integration](https://docs.langchain.com/oss/python/integrations/document_loaders/opendataloader_pdf)