---
name: llamaparse
description: Parse, extract, and analyze documents using the LlamaParse API (LlamaCloud). Use when the user asks to parse PDFs, images, spreadsheets, or other documents into markdown/text/structured data, extract tables or charts from documents, do OCR on scans, batch-process a folder of files, or use LlamaParse for any document processing task. Triggers on phrases like "parse this PDF", "extract text from document", "OCR this scan", "convert PDF to markdown", "extract tables", "parse with LlamaParse", "llamaparse", "llama parse".
metadata:
  openclaw:
    requires:
      env:
        - LLAMA_CLOUD_API_KEY
      bins:
        - python3
    primaryEnv: LLAMA_CLOUD_API_KEY
    emoji: "\U0001F4C4"
    homepage: https://cloud.llamaindex.ai
    install:
      - kind: uv
        package: llama-cloud
        bins: []
---

# LlamaParse

Parse documents (PDFs, images, spreadsheets, presentations — 130+ formats) into LLM-ready text, markdown, and structured data using the LlamaParse API.

## Prerequisites

- **Python package:** `llama-cloud>=1.0` (`pip install llama-cloud`)
- **API key:** Set `LLAMA_CLOUD_API_KEY` environment variable. Get one at https://cloud.llamaindex.ai

Verify setup:

```bash
pip install llama-cloud>=1.0
export LLAMA_CLOUD_API_KEY=llx-...
```

## Quick Start

```python
from llama_cloud import AsyncLlamaCloud
import asyncio

async def parse_document(file_path: str):
    client = AsyncLlamaCloud()  # Uses LLAMA_CLOUD_API_KEY env var
    file = await client.files.create(file=file_path, purpose="parse")
    result = await client.parsing.parse(
        file_id=file.id,
        tier="agentic",
        version="latest",
        expand=["markdown", "text"],
    )
    return result

result = asyncio.run(parse_document("document.pdf"))
print(result.markdown.pages[0].markdown)
```

## Core Concepts

### Tiers (required — choose one)

| Tier | Use Case | Cost |
|------|----------|------|
| `agentic_plus` | Maximum accuracy, complex layouts, charts | Highest |
| `agentic` | Advanced parsing with intelligent agents | Medium-high |
| `cost_effective` | Balanced performance and cost | Medium |
| `fast` | Fastest, basic parsing | Lowest |

Always specify both `tier` and `version`. Use `version="latest"` for dev, or a date string like `"2026-01-08"` for production reproducibility.

### Output Views (expand parameter)

Request one or more in the `expand` list:

- **`markdown`** — Structured markdown with headings, lists, tables. Best for RAG/LLM pipelines.
- **`text`** — Clean flattened text per page. Good for search/retrieval.
- **`items`** — Structured tree of page elements (headers, paragraphs, tables, figures) with bounding boxes. Use for layout-aware processing.
- **`metadata`** — Document metadata.
- **`images_content_metadata`** — Image/screenshot metadata with presigned URLs.

Access results: `result.markdown.pages[i].markdown`, `result.text.pages[i].text`, `result.items.pages[i].items`

### Output Options

Control markdown rendering:

```python
output_options={
    "markdown": {
        "tables": {
            "output_tables_as_markdown": True,  # or False for HTML tables
        },
    },
    "images_to_save": ["screenshot"],  # Save page screenshots
}
```

### Processing Options

```python
processing_options={
    "ignore": {"ignore_diagonal_text": True},
    "ocr_parameters": {"languages": ["en"]},  # OCR language hints
    "specialized_chart_parsing": "agentic_plus",  # Extract charts as structured data
}
```

### Custom Prompts (Agentic Parsing Instructions)

Guide the parser like an LLM — useful for extracting specific data or transforming output:

```python
from llama_cloud.types.parsing_create_params import (
    ProcessingOptions, ProcessingOptionsAutoModeConfiguration,
    ProcessingOptionsAutoModeConfigurationParsingConf
)

result = await client.parsing.parse(
    file_id=file.id,
    tier="agentic",
    version="latest",
    expand=["markdown"],
    processing_options=ProcessingOptions(
        auto_mode_configuration=[ProcessingOptionsAutoModeConfiguration(
            parsing_conf=ProcessingOptionsAutoModeConfigurationParsingConf(
                custom_prompt="Extract only prices and totals from this receipt."
            )
        )]
    ),
)
```

## Common Workflows

### Parse a single document

Use `scripts/parse_document.py`:

```bash
python scripts/parse_document.py document.pdf --tier agentic --output markdown,text
```

### Batch parse a folder

Use `scripts/batch_parse.py`:

```bash
python scripts/batch_parse.py ./documents/ --tier agentic --max-concurrent 5
```

### Extract tables from a document

Request `items` in expand, then filter for table items:

```python
for page in result.items.pages:
    for item in page.items:
        if hasattr(item, 'rows'):  # Table item
            print(f"Table on page {page.page_number}: {len(item.rows)} rows")
            # item.csv, item.html, item.md available
```

### Extract chart data

Enable specialized chart parsing, then pull table rows from the chart page:

```python
result = await client.parsing.parse(
    file_id=file.id,
    tier="agentic_plus",
    version="latest",
    processing_options={"specialized_chart_parsing": "agentic_plus"},
    expand=["items"],
)
```

### Download page screenshots

```python
import httpx, re

result = await client.parsing.parse(
    file_id=file.id, tier="agentic", version="latest",
    output_options={"images_to_save": ["screenshot"]},
    expand=["images_content_metadata"],
)

for img in result.images_content_metadata.images:
    if img.presigned_url and re.match(r"^page_\d+\.jpg$", img.filename):
        async with httpx.AsyncClient() as http:
            resp = await http.get(img.presigned_url)
            with open(img.filename, "wb") as f:
                f.write(resp.content)
```

## API Reference

For complete API details, see `references/api-reference.md`.

## External Service & Security

This skill uses the **LlamaParse API** (https://cloud.llamaindex.ai), a cloud document parsing service by LlamaIndex.

- **API key required:** You must set the `LLAMA_CLOUD_API_KEY` environment variable. Get a key at https://cloud.llamaindex.ai.
- **Data sent externally:** Documents are uploaded to the LlamaParse API for server-side parsing. Parsed results are returned to your local machine.
- **No other network calls:** The scripts only communicate with `api.cloud.llamaindex.ai`. Screenshot downloads use presigned URLs from the same service.
- **Scripts are reference utilities:** `scripts/parse_document.py` and `scripts/batch_parse.py` are helper scripts meant to be run manually by the user. They are not executed automatically by the skill.

## Tips

- Request only the `expand` views you need — more views = larger response + higher latency.
- Use `agentic_plus` tier with `specialized_chart_parsing` for documents with charts/graphs.
- For production, pin a specific `version` date instead of `"latest"`.
- Use semaphore-based concurrency for batch parsing to respect rate limits.
- The `items` view provides bounding boxes (`b_box`) for each element — useful for spatial analysis.
