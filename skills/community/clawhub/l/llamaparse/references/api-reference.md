# LlamaParse API Reference

## Client Initialization

```python
from llama_cloud import AsyncLlamaCloud, LlamaCloud

# Async client (recommended)
client = AsyncLlamaCloud(api_key="llx-...")  # or uses LLAMA_CLOUD_API_KEY env var

# Sync client
client = LlamaCloud(api_key="llx-...")
```

## File Upload

```python
file = await client.files.create(
    file="path/to/document.pdf",   # Local file path
    purpose="parse",               # Required: "parse"
    external_file_id="my-id",      # Optional: your own ID for tracking
)
# Returns: file.id (used in parsing)
```

## Parsing

```python
result = await client.parsing.parse(
    file_id=file.id,               # Required
    tier="agentic",                # Required: agentic_plus | agentic | cost_effective | fast
    version="latest",              # Required: "latest" or date like "2026-01-08"
    expand=[...],                  # List of output views to include
    input_options={},              # File-type-specific options (html, spreadsheet, etc.)
    output_options={},             # Control output structure and markdown styling
    processing_options={},         # Control document processing behavior
)
```

### Tiers

| Tier | Description |
|------|-------------|
| `agentic_plus` | State-of-the-art models, maximum accuracy |
| `agentic` | Advanced parsing with intelligent agents |
| `cost_effective` | Balanced performance/cost with efficient models |
| `fast` | Fastest tier, basic parsing |

### Expand Options

| Value | Description | Access Pattern |
|-------|-------------|----------------|
| `markdown` | Structured markdown | `result.markdown.pages[i].markdown` |
| `text` | Clean flattened text | `result.text.pages[i].text` |
| `items` | Structured element tree | `result.items.pages[i].items` |
| `metadata` | Document metadata | `result.metadata` |
| `images_content_metadata` | Image metadata + presigned URLs | `result.images_content_metadata.images` |

### Output Options

```python
output_options={
    "markdown": {
        "tables": {
            "output_tables_as_markdown": True,   # True = pipe tables, False = HTML
        },
    },
    "images_to_save": ["screenshot"],  # Save page screenshots for retrieval
}
```

### Processing Options

```python
processing_options={
    "ignore": {
        "ignore_diagonal_text": True,
    },
    "ocr_parameters": {
        "languages": ["en", "fr"],   # ISO 639-1 language codes
    },
    "specialized_chart_parsing": "agentic_plus",  # or "agentic"
    "auto_mode_configuration": [
        {
            "parsing_conf": {
                "high_res_ocr": True,
                "outlined_table_extraction": True,
                "custom_prompt": "Your instructions here",
            }
        }
    ],
}
```

### Typed Processing Options (Python SDK)

```python
from llama_cloud.types.parsing_create_params import (
    OutputOptions,
    OutputOptionsMarkdown,
    OutputOptionsMarkdownTables,
    ProcessingOptions,
    ProcessingOptionsAutoModeConfiguration,
    ProcessingOptionsAutoModeConfigurationParsingConf,
    AgenticOptions,
)
```

## Items View — Element Types

When using `expand=["items"]`, each page contains a list of typed items:

| Type | Description | Key Fields |
|------|-------------|------------|
| `header` | Page/section header | `md`, `bbox` |
| `heading` | Heading (H1-H6) | `level`, `md`, `value`, `bbox` |
| `text` | Paragraph text | `md`, `value`, `bbox` |
| `table` | Table with structured data | `rows`, `csv`, `html`, `md`, `bbox` |
| `figure` | Image or chart | `md`, `bbox` |

Each item has `bbox` (bounding box) with: `x`, `y`, `w`, `h`, `confidence`.

## REST API (cURL)

```bash
# Upload file
curl -X POST 'https://api.cloud.llamaindex.ai/api/v2/files' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \
  -F 'file=@document.pdf' \
  -F 'purpose=parse'

# Parse
curl -X POST 'https://api.cloud.llamaindex.ai/api/v2/parse' \
  -H "Authorization: Bearer $LLAMA_CLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "file_id": "<file_id>",
    "tier": "agentic",
    "version": "latest"
  }'
```

## Supported Formats

LlamaParse supports 130+ document formats including:
- PDF, DOCX, PPTX, XLSX
- Images (PNG, JPG, TIFF, BMP, WebP)
- HTML, XML, CSV, TSV
- Scanned documents (via OCR)
- And many more

## Links

- Dashboard: https://cloud.llamaindex.ai
- API Key: https://cloud.llamaindex.ai → Settings → API Keys
- Python SDK: https://github.com/run-llama/llama-cloud-py
- TypeScript SDK: https://github.com/run-llama/llama-cloud-ts
- Full API Reference: https://developers.api.llamaindex.ai/
- Documentation: https://developers.llamaindex.ai/python/cloud/
