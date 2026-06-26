# Canonical Document Schema

This file defines the stable intermediate representation used by this skill.

## Purpose

All downstream modes must consume the canonical schema instead of raw document text.

Benefits:
- stable contract between parse and transform stages
- better grounding
- traceability from outputs back to source blocks
- easier testing and future model replacement

## Top-level structure

```json
{
  "schema_version": "1.0",
  "document_id": "string",
  "source": {},
  "parse_info": {},
  "pages": [],
  "tables": [],
  "figures": [],
  "entities": [],
  "outputs": {}
}
```

## Field definitions

### `schema_version`
Version of this schema.
Type: `string`

### `document_id`
Stable ID for the current document run.
Recommended format:
`<file_stem>-<short_hash>`

### `source`
Information about the original input.

```json
{
  "input_path": "string",
  "input_type": "pdf|image",
  "filename": "string",
  "sha256": "string|null"
}
```

### `parse_info`
Information about the parser run.

```json
{
  "engine": "local-document-ai-openvino",
  "engine_version": "string",
  "mode": "parse|to-code|to-data",
  "created_at": "ISO-8601 string",
  "warnings": ["string"],
  "confidence_note": "string|null"
}
```

### `pages`
Ordered list of parsed pages.

```json
[
  {
    "page_id": "page_1",
    "page_index": 1,
    "width": 2480,
    "height": 3508,
    "blocks": []
  }
]
```

### `blocks`
Ordered list of page blocks.

```json
{
  "block_id": "p1_b1",
  "type": "heading|paragraph|list|table|formula|chart|figure|seal|kv_pair|footer|header|caption|unknown",
  "bbox": [0, 0, 100, 50],
  "reading_order": 1,
  "text": "string",
  "markdown": "string|null",
  "latex": "string|null",
  "html": "string|null",
  "confidence": 0.0,
  "attributes": {
    "heading_level": 1,
    "language": "en",
    "is_rotated": false
  },
  "relations": {
    "parent_block_id": null,
    "caption_for": null,
    "table_id": null,
    "figure_id": null
  }
}
```

#### Block rules
- `page_id + block_id` must be unique
- `reading_order` must be monotonic within a page
- `type` should be as specific as possible
- `text` is plain normalized text
- `markdown` is optional rendered text
- `latex` is only for formulas
- `html` is optional for table/structured fragments

### `tables`
Normalized structured tables.

```json
[
  {
    "table_id": "t1",
    "page_id": "page_2",
    "bbox": [10, 10, 200, 150],
    "caption": "Quarterly Revenue",
    "headers": ["Quarter", "Revenue"],
    "rows": [
      ["Q1", "$1M"],
      ["Q2", "$1.2M"]
    ],
    "csv_path": "tables/t1.csv",
    "source_block_ids": ["p2_b8"]
  }
]
```

### `figures`
Saved figure assets.

```json
[
  {
    "figure_id": "f1",
    "page_id": "page_3",
    "bbox": [20, 20, 300, 200],
    "caption": "Architecture Diagram",
    "asset_path": "figures/f1.png",
    "source_block_ids": ["p3_b4"]
  }
]
```

### `entities`
Optional normalized entities.

```json
[
  {
    "entity_id": "e1",
    "type": "invoice_number|date|person|organization|amount|email|phone|custom",
    "value": "INV-1001",
    "normalized_value": "INV-1001",
    "page_id": "page_1",
    "source_block_ids": ["p1_b6"],
    "confidence": 0.96
  }
]
```

### `outputs`
Artifacts written during parse or downstream generation.

```json
{
  "parsed_markdown_path": "parsed.md",
  "task_outputs": [
    {
      "type": "react_scaffold|html_scaffold|normalized_json",
      "path": "task_output/output.ext",
      "source_map_path": "task_output/source_map.json"
    }
  ]
}
```

## Minimum parse requirements

Every successful parse must produce:
- `schema_version`
- `document_id`
- `source`
- `parse_info`
- at least one `page`
- `outputs.parsed_markdown_path`

## Minimum grounding requirements

Every downstream output must preserve:
- `page_id`
- `block_id` references for supporting source regions
- assumptions where source evidence is incomplete

## Recommended normalization rules

- normalize whitespace
- preserve line breaks in Markdown where they affect meaning
- do not merge unrelated columns into one paragraph
- do not flatten tables into plain text if a structured table can be recovered
- mark low-confidence or omitted content explicitly
