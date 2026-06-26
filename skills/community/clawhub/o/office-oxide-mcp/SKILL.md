---
id: office-oxide-mcp
name: Office Oxide MCP Server
summary: Rust-native MCP server for Office document processing (Excel, Word, PowerPoint, PDF). Sub-millisecond, local-first, open-source alternative to Aspose.
version: 0.2.0
source_url: https://github.com/Aimino-Tech/office-oxide-mcp
license: MIT OR Apache-2.0
tags: [mcp, office, excel, word, powerpoint, pdf, rust]
---

# Office Oxide MCP Server

**Rust-native MCP server for Office document processing (Excel, Word, PowerPoint, PDF).** Sub-millisecond, local-first, open source — the "open source Aspose."

## Quick Start

```bash
cargo install office-oxide-mcp
```

Or download the [latest release](https://github.com/Aimino-Tech/office-oxide-mcp/releases).

### Claude Desktop

```json
{
  "mcpServers": {
    "office": { "command": "office-oxide-mcp", "args": ["--transport", "stdio"] }
  }
}
```

### Cursor

```json
{
  "mcpServers": {
    "office-oxide-mcp": { "command": "office-oxide-mcp", "args": ["--transport", "stdio"] }
  }
}
```

## Features

### AI Reading
- Read DOCX, XLSX, PPTX, PDF into JSON, Markdown, or semantic chunks
- Table extraction, image embedding, section detection
- Format-agnostic unified API

### Excel Write
- Create XLSX files with formatting, charts, pivot tables
- Write cells, ranges, merge cells, conditional formatting
- Column widths, sheet management

### Word Write
- Create DOCX files from Markdown
- Templates with text replacement, tables, images, headers/footers
- Comments, TOC, style management

### PPT Write
- Create presentations with charts, text boxes, images
- Slide layouts, agenda slides, callout layouts
- McKinsey-quality output

### PDF
- Read PDF as Markdown/JSON/text/chunks
- Fill AcroForm and XFA forms
- Overlay text at coordinates on flat PDFs
- Layout analysis for field detection
- Export to PDF from any format

### Skills System
- Built-in templates: `excel.table`, `word.report`, `ppt.deck`
- YAML-defined skills with validation
- Custom skill registration and execution

### Coherence Engine
- Cross-document entity tracking with DAG
- BFS propagation for bulk updates
- Integrity verification

## Tool Overview

| Tool | Description |
|------|-------------|
| `list_formats` | All supported formats + capabilities |
| `get_document_info` | File metadata (format, size, readability) |
| `office_read` | Read content → JSON / Markdown / Chunks / Text |
| `office_fill_pdf_form` | Fill AcroForm/XFA form fields |
| `office_list_pdf_fields` | List all form fields in a PDF |
| `office_overlay_pdf_text` | Text at coordinates on flat PDFs |
| `office_analyze_pdf_layout` | Layout analysis for overlay coords |
| `office_create_xlsx` | Create Excel workbooks |
| `office_create_docx` | Create Word documents |
| `office_write_docx_from_md` | Create DOCX from Markdown |
| `office_create_pptx` | Create PowerPoint presentations |
| `skill_run` / `skill_list` / `skill_validate` / `skill_register` | Skills System |
| `office_propagate_edit` / `office_check_consistency` | Coherence Engine |

## Performance

| Operation | Python | office-oxide-mcp | Speedup |
|-----------|--------|-----------------|---------|
| 10M cell XLSX read | 239s | ~25s | ~10× |
| 100K cell XLSX write | 1.8s | 152ms | ~12× |
| DOCX read (6K docs) | 11.8ms | 0.8ms | ~14× |
| PPTX read (323 slides) | 32.5ms | 0.7ms | ~46× |
| Cold start | 1-5s | <50ms | ~100× |
| Memory (idle) | 42.7MB | <2MB | ~20× |

## License

MIT OR Apache-2.0
