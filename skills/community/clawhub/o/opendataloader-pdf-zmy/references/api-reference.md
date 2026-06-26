# OpenDataLoader PDF — API Reference

## Python API

### `convert()` — Main Entry Point

```python
from opendataloader_pdf import convert

convert(
    input_path: list[str],       # Files and/or folders
    output_dir: str,              # Output directory
    format: str = "markdown",     # "markdown" | "json" | "html" | "text" | combined e.g. "markdown,json"
    hybrid: str = None,          # "docling-fast" | "docling" | "unstructured"; omit for basic mode
    hybrid_mode: str = None,      # "fast" | "full"; only with hybrid
    image_output: str = "off",    # "off" | "embedded" | "external"
    image_format: str = "jpeg",   # "png" | "jpeg"
    use_struct_tree: bool = False,  # Use PDF structure tags
    sanitize: bool = False,       # Remove prompt injection risks
    **kwargs
)
```

### `OpenDataLoaderPDF` Class

```python
from opendataloader_pdf import OpenDataLoaderPDF

pdf = OpenDataLoaderPDF("document.pdf")

# Extract as different formats
markdown = pdf.extract(format="markdown")
json_data = pdf.extract(format="json")
html_data = pdf.extract(format="html")
text_data = pdf.extract(format="text")

# Hybrid mode
pdf_hybrid = OpenDataLoaderPDF("complex_doc.pdf", hybrid="docling-fast")
markdown = pdf_hybrid.extract(format="markdown", hybrid_mode="full")
```

### LangChain Loader

```python
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader

loader = OpenDataLoaderPDFLoader(
    file_path="document.pdf",   # str, list[str], or Path
    format="text"               # "text" | "markdown"
)
documents = loader.load()       # Returns list[Document]
```

## JSON Output Schema

Each element in the JSON output:

```json
{
  "type": "heading | paragraph | table | list | image | caption | formula",
  "id": 42,
  "page number": 1,
  "bounding box": [left, bottom, right, top],  // PDF points (72pt = 1 inch)
  "heading level": 1,
  "font": "Helvetica-Bold",
  "font size": 24.0,
  "content": "Extracted text content"
}
```

## Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | list[str] | required | PDF files/folders |
| `output_dir` | str | required | Output directory |
| `format` | str | `"markdown"` | Output format(s) |
| `hybrid` | str | None | AI backend: `"docling-fast"` recommended |
| `hybrid_mode` | str | `"fast"` | `"fast"` or `"full"` (with formula/chart enrichment) |
| `image_output` | str | `"off"` | Image embedding mode |
| `image_format` | str | `"jpeg"` | `"png"` or `"jpeg"` |
| `use_struct_tree` | bool | False | Use native PDF structure |
| `sanitize` | bool | False | Remove prompt injection |

## Performance

| Mode | Speed | GPU Required |
|------|-------|-------------|
| Basic | ~20 pages/sec | No |
| Hybrid Fast | ~2 pages/sec | No |
| Hybrid Full | ~0.5 pages/sec | No |
| Batch (8+ cores) | 100+ pages/sec | No |
