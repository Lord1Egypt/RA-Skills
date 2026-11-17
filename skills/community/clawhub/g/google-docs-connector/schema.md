# Google Docs Connector Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `google-docs-connector`

x402 availability: not enabled for this product.

## `batch_update`

Action slug: `batch-update`

Price: `5` credits

Execute raw Google Docs API batch update requests. Put tabId inside each raw range or location when targeting a non-first tab.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `requests` | `array` | yes | Array of raw Google Docs API request objects. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "requests": [
    {}
  ]
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "requests": {
    "description": "Array of raw Google Docs API request objects.",
    "items": {
      "type": "object"
    },
    "required": true,
    "type": "array"
  }
}
```

## `create_document`

Action slug: `create-document`

Price: `5` credits

Create a new, empty Google Doc. Prefer create_from_markdown when the content has any structure.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | no | Initial body content for the document. |
| `title` | `string` | yes | Document title. |

Sample parameters:

```json
{
  "text": "example text",
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "Initial body content for the document.",
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Document title.",
    "required": true,
    "type": "string"
  }
}
```

## `create_footer`

Action slug: `create-footer`

Price: `5` credits

Add a footer to the document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `footer_type` | `string` | no | Footer type to create. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "footer_type": "DEFAULT"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "footer_type": {
    "default": "DEFAULT",
    "description": "Footer type to create.",
    "enum": [
      "DEFAULT",
      "FIRST_PAGE",
      "EVEN_PAGE",
      "ODD_PAGE"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `create_from_markdown`

Action slug: `create-from-markdown`

Price: `5` credits

Create a new Google Doc from markdown. Drive converts the markdown into real Google Docs formatting (headings, lists, tables, bold/italic), so no index arithmetic is needed. Preferred way to author a new document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `markdown` | `string` | yes | Markdown source. Supports headings, bulleted and numbered lists (including nesting), tables, bold/italic/strikethrough, inline code, fenced code blocks, block quotes, horizontal rules and links. |
| `parent_folder_id` | `string` | no | Destination Google Drive folder ID. Defaults to My Drive root. |
| `title` | `string` | yes | Document title. |

Sample parameters:

```json
{
  "markdown": "example markdown",
  "parent_folder_id": "example parent folder id",
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "markdown": {
    "description": "Markdown source. Supports headings, bulleted and numbered lists (including nesting), tables, bold/italic/strikethrough, inline code, fenced code blocks, block quotes, horizontal rules and links.",
    "required": true,
    "type": "string"
  },
  "parent_folder_id": {
    "description": "Destination Google Drive folder ID. Defaults to My Drive root.",
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Document title.",
    "required": true,
    "type": "string"
  }
}
```

## `create_header`

Action slug: `create-header`

Price: `5` credits

Add a header to the document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `header_type` | `string` | no | Header type to create. |
| `text` | `string` | no | Header text content. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "header_type": "DEFAULT",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "header_type": {
    "default": "DEFAULT",
    "description": "Header type to create.",
    "enum": [
      "DEFAULT",
      "FIRST_PAGE",
      "EVEN_PAGE",
      "ODD_PAGE"
    ],
    "required": false,
    "type": "string"
  },
  "text": {
    "description": "Header text content.",
    "required": false,
    "type": "string"
  }
}
```

## `create_named_range`

Action slug: `create-named-range`

Price: `5` credits

Create a named range (bookmark) spanning a character range in the document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `range_end` | `integer` | yes | Zero-based exclusive UTF-16 code-unit end index. |
| `range_name` | `string` | yes | Name for the named range/bookmark. |
| `range_start` | `integer` | yes | Zero-based inclusive UTF-16 code-unit start index. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "range_end": 0,
  "range_name": "example range name",
  "range_start": 0,
  "tab_id": "example tab id"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "range_end": {
    "description": "Zero-based exclusive UTF-16 code-unit end index.",
    "minimum": 0,
    "required": true,
    "type": "integer"
  },
  "range_name": {
    "description": "Name for the named range/bookmark.",
    "required": true,
    "type": "string"
  },
  "range_start": {
    "description": "Zero-based inclusive UTF-16 code-unit start index.",
    "minimum": 0,
    "required": true,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  }
}
```

## `create_tab`

Action slug: `create-tab`

Price: `5` credits

Add a document tab and return its new tab ID, ready to pass to render_markdown or any indexed update. Uses the Docs addDocumentTab request.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `icon_emoji` | `string` | no | Emoji shown on the tab. An invalid emoji is rejected by Google. |
| `index` | `integer` | no | Zero-based position of the new tab within its parent. This is a tab ordinal, not a document character offset. Adding a tab at an index increments the index of every tab after it. |
| `parent_tab_id` | `string` | no | Parent tab ID, to nest the new tab under an existing one. Omit for a root-level tab. |
| `title` | `string` | no | Tab title. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "icon_emoji": "example icon emoji",
  "index": 0,
  "parent_tab_id": "example parent tab id",
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "icon_emoji": {
    "description": "Emoji shown on the tab. An invalid emoji is rejected by Google.",
    "required": false,
    "type": "string"
  },
  "index": {
    "description": "Zero-based position of the new tab within its parent. This is a tab ordinal, not a document character offset. Adding a tab at an index increments the index of every tab after it.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "parent_tab_id": {
    "description": "Parent tab ID, to nest the new tab under an existing one. Omit for a root-level tab.",
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Tab title.",
    "required": false,
    "type": "string"
  }
}
```

## `create_table`

Action slug: `create-table`

Price: `5` credits

Insert a table into a document, optionally populated with data. If table_data is provided, dimensions are inferred from it. A markdown pipe table through render_markdown is usually simpler.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `columns` | `integer` | no | Number of table columns (1-20). Not needed if table_data is provided. |
| `document_id` | `string` | yes | Google Docs document ID. |
| `location` | `integer` | no | Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body. |
| `rows` | `integer` | no | Number of table rows (1-100). Not needed if table_data is provided. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |
| `table_data` | `array` | no | 2D array of strings representing table cell data. |

Sample parameters:

```json
{
  "columns": 1,
  "document_id": "example document id",
  "location": 0,
  "rows": 1,
  "tab_id": "example tab id",
  "table_data": [
    [
      "example table data"
    ]
  ]
}
```

Generated JSON parameter schema:

```json
{
  "columns": {
    "description": "Number of table columns (1-20). Not needed if table_data is provided.",
    "maximum": 20,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "location": {
    "description": "Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "rows": {
    "description": "Number of table rows (1-100). Not needed if table_data is provided.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  },
  "table_data": {
    "description": "2D array of strings representing table cell data.",
    "items": {
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "required": false,
    "type": "array"
  }
}
```

## `export_document`

Action slug: `export-document`

Price: `5` credits

Export a document to another format. Text formats (txt, html, md) return content directly; binary formats return base64-encoded content. Use md to read a document as markdown, revise it, and send it back through render_markdown or replace_with_markdown.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `export_format` | `string` | yes | Target export format. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "export_format": "pdf"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "export_format": {
    "description": "Target export format.",
    "enum": [
      "pdf",
      "docx",
      "odt",
      "rtf",
      "txt",
      "html",
      "md",
      "epub",
      "zip"
    ],
    "required": true,
    "type": "string"
  }
}
```

## `format_text`

Action slug: `format-text`

Price: `5` credits

Apply text and/or paragraph styling to a zero-based UTF-16 range in a specific document tab. Provide at least one non-empty style object.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `paragraph_style` | `object` | no | Paragraph styling options, including real Google Docs named heading styles. |
| `range_end` | `integer` | yes | Zero-based exclusive UTF-16 code-unit end index. |
| `range_start` | `integer` | yes | Zero-based inclusive UTF-16 code-unit start index. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |
| `text_style` | `object` | no | Text styling options. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "paragraph_style": {
    "alignment": "START",
    "indent_end": {},
    "indent_first_line": {},
    "indent_start": {},
    "line_spacing": 1,
    "named_style_type": "NORMAL_TEXT",
    "spacing_mode": "NEVER_COLLAPSE"
  },
  "range_end": 0,
  "range_start": 0,
  "tab_id": "example tab id",
  "text_style": {
    "background_color": {},
    "bold": true,
    "font_family": "example font family",
    "font_size": {
      "magnitude": 1,
      "unit": "example unit"
    },
    "foreground_color": {},
    "italic": true,
    "link": "example link",
    "strikethrough": true
  }
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "paragraph_style": {
    "description": "Paragraph styling options, including real Google Docs named heading styles.",
    "properties": {
      "alignment": {
        "description": "Text alignment.",
        "enum": [
          "START",
          "CENTER",
          "END",
          "JUSTIFIED"
        ],
        "required": false,
        "type": "string"
      },
      "indent_end": {
        "description": "Right indent with magnitude and unit.",
        "required": false,
        "type": "object"
      },
      "indent_first_line": {
        "description": "First line indent with magnitude and unit.",
        "required": false,
        "type": "object"
      },
      "indent_start": {
        "description": "Left indent with magnitude and unit.",
        "required": false,
        "type": "object"
      },
      "line_spacing": {
        "description": "Line spacing (100=single, 150=1.5x, 200=double).",
        "required": false,
        "type": "number"
      },
      "named_style_type": {
        "description": "Google Docs named paragraph style.",
        "enum": [
          "NORMAL_TEXT",
          "TITLE",
          "SUBTITLE",
          "HEADING_1",
          "HEADING_2",
          "HEADING_3",
          "HEADING_4",
          "HEADING_5",
          "HEADING_6"
        ],
        "required": false,
        "type": "string"
      },
      "spacing_mode": {
        "description": "Paragraph spacing mode.",
        "enum": [
          "NEVER_COLLAPSE",
          "COLLAPSE_LISTS"
        ],
        "required": false,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "range_end": {
    "description": "Zero-based exclusive UTF-16 code-unit end index.",
    "minimum": 0,
    "required": true,
    "type": "integer"
  },
  "range_start": {
    "description": "Zero-based inclusive UTF-16 code-unit start index.",
    "minimum": 0,
    "required": true,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  },
  "text_style": {
    "description": "Text styling options.",
    "properties": {
      "background_color": {
        "description": "Text highlight color as RGB values (0-1).",
        "required": false,
        "type": "object"
      },
      "bold": {
        "description": "Apply bold formatting.",
        "required": false,
        "type": "boolean"
      },
      "font_family": {
        "description": "Font family name (e.g., 'Arial', 'Times New Roman').",
        "required": false,
        "type": "string"
      },
      "font_size": {
        "description": "Font size with magnitude and unit.",
        "properties": {
          "magnitude": {
            "description": "Size value.",
            "required": true,
            "type": "number"
          },
          "unit": {
            "description": "Size unit (typically 'PT').",
            "required": true,
            "type": "string"
          }
        },
        "required": false,
        "type": "object"
      },
      "foreground_color": {
        "description": "Text color as RGB values (0-1).",
        "required": false,
        "type": "object"
      },
      "italic": {
        "description": "Apply italic formatting.",
        "required": false,
        "type": "boolean"
      },
      "link": {
        "description": "URL to create a hyperlink.",
        "required": false,
        "type": "string"
      },
      "strikethrough": {
        "description": "Apply strikethrough formatting.",
        "required": false,
        "type": "boolean"
      },
      "underline": {
        "description": "Apply underline formatting.",
        "required": false,
        "type": "boolean"
      }
    },
    "required": false,
    "type": "object"
  }
}
```

## `get_document`

Action slug: `get-document`

Price: `5` credits

Retrieve content and indexed structure from every document tab, including nested child tabs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID (from the document URL). |

Sample parameters:

```json
{
  "document_id": "example document id"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID (from the document URL).",
    "required": true,
    "type": "string"
  }
}
```

## `get_permissions`

Action slug: `get-permissions`

Price: `5` credits

List the current sharing permissions on a document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |

Sample parameters:

```json
{
  "document_id": "example document id"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  }
}
```

## `insert_image`

Action slug: `insert-image`

Price: `5` credits

Insert an inline image from a publicly accessible URL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `height` | `integer` | no | Image height in pixels. |
| `image_url` | `string` | yes | Publicly accessible URL of the image to insert. |
| `location` | `integer` | no | Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |
| `width` | `integer` | no | Image width in pixels. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "height": 1,
  "image_url": "https://example.com",
  "location": 0,
  "tab_id": "example tab id",
  "width": 1
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "height": {
    "description": "Image height in pixels.",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "image_url": {
    "description": "Publicly accessible URL of the image to insert.",
    "required": true,
    "type": "string"
  },
  "location": {
    "description": "Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  },
  "width": {
    "description": "Image width in pixels.",
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `insert_page_break`

Action slug: `insert-page-break`

Price: `5` credits

Insert a page break at a specific position.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `location` | `integer` | no | Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "location": 0,
  "tab_id": "example tab id"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "location": {
    "description": "Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  }
}
```

## `insert_section_break`

Action slug: `insert-section-break`

Price: `5` credits

Insert a section break at a specific position.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `location` | `integer` | no | Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "location": 0,
  "tab_id": "example tab id"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "location": {
    "description": "Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  }
}
```

## `insert_text`

Action slug: `insert-text`

Price: `5` credits

Insert text at a specific character position in a document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `location` | `integer` | no | Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |
| `text` | `string` | yes | Text content to insert. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "location": 0,
  "tab_id": "example tab id",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "location": {
    "description": "Zero-based UTF-16 code-unit index. Defaults to 1, normally the beginning of a tab body.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  },
  "text": {
    "description": "Text content to insert.",
    "required": true,
    "type": "string"
  }
}
```

## `quick_create`

Action slug: `quick-create`

Price: `5` credits

Create a document from a natural language description. Any markdown in the description becomes real formatting. If the text contains 'titled "..."' or 'called "..."', the title is extracted automatically.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | yes | Natural language description or content for the document. |
| `title` | `string` | no | Document title. If omitted, may be extracted from the text description. |

Sample parameters:

```json
{
  "text": "example text",
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "text": {
    "description": "Natural language description or content for the document.",
    "required": true,
    "type": "string"
  },
  "title": {
    "description": "Document title. If omitted, may be extracted from the text description.",
    "required": false,
    "type": "string"
  }
}
```

## `rename_document`

Action slug: `rename-document`

Price: `5` credits

Rename an existing Google Doc file without changing its document tabs or ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | ID of the Google Doc to rename. |
| `new_title` | `string` | yes | Nonblank new file title. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "new_title": "example new title"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "ID of the Google Doc to rename.",
    "required": true,
    "type": "string"
  },
  "new_title": {
    "description": "Nonblank new file title.",
    "required": true,
    "type": "string"
  }
}
```

## `render_markdown`

Action slug: `render-markdown`

Price: `5` credits

Render markdown into an existing document without destroying the rest of it. The tool computes every UTF-16 index, so the caller supplies only markdown and an insertion point. Preferred way to add formatted content to an existing document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `location` | `integer` | no | Zero-based UTF-16 index to insert at. Defaults to 1, the beginning of the tab body, or to range_start when replacing a range. |
| `markdown` | `string` | yes | Markdown source. Supports headings, bulleted and numbered lists (including nesting), tables, bold/italic/strikethrough, inline code, fenced code blocks, block quotes, horizontal rules and links. |
| `range_end` | `integer` | no | Zero-based exclusive end of the range to replace. Must be greater than range_start. |
| `range_start` | `integer` | no | Zero-based inclusive start of an existing range to replace. Provide with range_end, or omit both to insert without deleting. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id, or from create_tab. If omitted, targets the first tab. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "location": 0,
  "markdown": "example markdown",
  "range_end": 0,
  "range_start": 0,
  "tab_id": "example tab id"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "location": {
    "description": "Zero-based UTF-16 index to insert at. Defaults to 1, the beginning of the tab body, or to range_start when replacing a range.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "markdown": {
    "description": "Markdown source. Supports headings, bulleted and numbered lists (including nesting), tables, bold/italic/strikethrough, inline code, fenced code blocks, block quotes, horizontal rules and links.",
    "required": true,
    "type": "string"
  },
  "range_end": {
    "description": "Zero-based exclusive end of the range to replace. Must be greater than range_start.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "range_start": {
    "description": "Zero-based inclusive start of an existing range to replace. Provide with range_end, or omit both to insert without deleting.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id, or from create_tab. If omitted, targets the first tab.",
    "required": false,
    "type": "string"
  }
}
```

## `replace_text`

Action slug: `replace-text`

Price: `5` credits

Find and replace text in one tab, or in all tabs when tab_id is omitted.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `match_case` | `boolean` | no | Whether to use case-sensitive search. |
| `replace_with` | `string` | yes | Replacement text. |
| `search_text` | `string` | yes | Text to search for. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, replacement applies to all tabs. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "match_case": false,
  "replace_with": "example replace with",
  "search_text": "example search query",
  "tab_id": "example tab id"
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "match_case": {
    "default": false,
    "description": "Whether to use case-sensitive search.",
    "required": false,
    "type": "boolean"
  },
  "replace_with": {
    "description": "Replacement text.",
    "required": true,
    "type": "string"
  },
  "search_text": {
    "description": "Text to search for.",
    "required": true,
    "type": "string"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, replacement applies to all tabs.",
    "required": false,
    "type": "string"
  }
}
```

## `replace_with_markdown`

Action slug: `replace-with-markdown`

Price: `5` credits

Replace an existing document's entire body from markdown, keeping its document ID, URL and sharing. Destructive: prefer render_markdown unless a full-body rewrite is intended.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm_replace` | `boolean` | yes | Required acknowledgement, must be true. Discards the entire existing body: comments and suggestions lose their anchors, and headers, footers, section breaks, named ranges, images and extra tabs are dropped. |
| `document_id` | `string` | yes | Google Docs document ID. |
| `markdown` | `string` | yes | Markdown source that becomes the document's complete new body. |
| `new_title` | `string` | no | Optional new file title to set at the same time. |

Sample parameters:

```json
{
  "confirm_replace": true,
  "document_id": "example document id",
  "markdown": "example markdown",
  "new_title": "example new title"
}
```

Generated JSON parameter schema:

```json
{
  "confirm_replace": {
    "description": "Required acknowledgement, must be true. Discards the entire existing body: comments and suggestions lose their anchors, and headers, footers, section breaks, named ranges, images and extra tabs are dropped.",
    "required": true,
    "type": "boolean"
  },
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "markdown": {
    "description": "Markdown source that becomes the document's complete new body.",
    "required": true,
    "type": "string"
  },
  "new_title": {
    "description": "Optional new file title to set at the same time.",
    "required": false,
    "type": "string"
  }
}
```

## `search_documents`

Action slug: `search-documents`

Price: `5` credits

Search for Google Docs by name. Returns documents sorted by most recently modified. Omit query to list recent documents.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_results` | `integer` | no | Maximum results to return (1-100). |
| `query` | `string` | no | Search term that matches document names (contains match). |

Sample parameters:

```json
{
  "max_results": 20,
  "query": "example search query"
}
```

Generated JSON parameter schema:

```json
{
  "max_results": {
    "default": 20,
    "description": "Maximum results to return (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Search term that matches document names (contains match).",
    "required": false,
    "type": "string"
  }
}
```

## `share_document`

Action slug: `share-document`

Price: `5` credits

Set sharing permissions on a document via Google Drive.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `email_message` | `string` | no | Custom message for the sharing notification email. |
| `send_notification` | `boolean` | no | Send email notification when sharing. |
| `share_with` | `array` | yes | List of permission objects defining who to share with. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "email_message": "user@example.com",
  "send_notification": true,
  "share_with": [
    {
      "domain": "example domain",
      "email": "user@example.com",
      "permission_type": "user",
      "role": "reader"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "email_message": {
    "description": "Custom message for the sharing notification email.",
    "required": false,
    "type": "string"
  },
  "send_notification": {
    "default": true,
    "description": "Send email notification when sharing.",
    "required": false,
    "type": "boolean"
  },
  "share_with": {
    "description": "List of permission objects defining who to share with.",
    "items": {
      "properties": {
        "domain": {
          "description": "Domain for domain-wide sharing.",
          "required": false,
          "type": "string"
        },
        "email": {
          "description": "Email address (for user or group permissions).",
          "required": false,
          "type": "string"
        },
        "permission_type": {
          "description": "Permission type.",
          "enum": [
            "user",
            "group",
            "domain",
            "anyone"
          ],
          "required": true,
          "type": "string"
        },
        "role": {
          "description": "Permission level.",
          "enum": [
            "reader",
            "writer",
            "commenter"
          ],
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": true,
    "type": "array"
  }
}
```

## `update_style`

Action slug: `update-style`

Price: `5` credits

Alias for format_text. Apply text and/or paragraph styling to a zero-based UTF-16 range in a specific tab.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `paragraph_style` | `object` | no | Paragraph styling options, including real Google Docs named heading styles. |
| `range_end` | `integer` | yes | Zero-based exclusive UTF-16 code-unit end index. |
| `range_start` | `integer` | yes | Zero-based inclusive UTF-16 code-unit start index. |
| `tab_id` | `string` | no | Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab. |
| `text_style` | `object` | no | Text styling options. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "paragraph_style": {
    "alignment": "START",
    "indent_end": {},
    "indent_first_line": {},
    "indent_start": {},
    "line_spacing": 1,
    "named_style_type": "NORMAL_TEXT",
    "spacing_mode": "NEVER_COLLAPSE"
  },
  "range_end": 0,
  "range_start": 0,
  "tab_id": "example tab id",
  "text_style": {
    "background_color": {},
    "bold": true,
    "font_family": "example font family",
    "font_size": {
      "magnitude": 1,
      "unit": "example unit"
    },
    "foreground_color": {},
    "italic": true,
    "link": "example link",
    "strikethrough": true
  }
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Google Docs document ID.",
    "required": true,
    "type": "string"
  },
  "paragraph_style": {
    "description": "Paragraph styling options, including real Google Docs named heading styles.",
    "properties": {
      "alignment": {
        "description": "Text alignment.",
        "enum": [
          "START",
          "CENTER",
          "END",
          "JUSTIFIED"
        ],
        "required": false,
        "type": "string"
      },
      "indent_end": {
        "description": "Right indent with magnitude and unit.",
        "required": false,
        "type": "object"
      },
      "indent_first_line": {
        "description": "First line indent with magnitude and unit.",
        "required": false,
        "type": "object"
      },
      "indent_start": {
        "description": "Left indent with magnitude and unit.",
        "required": false,
        "type": "object"
      },
      "line_spacing": {
        "description": "Line spacing (100=single, 150=1.5x, 200=double).",
        "required": false,
        "type": "number"
      },
      "named_style_type": {
        "description": "Google Docs named paragraph style.",
        "enum": [
          "NORMAL_TEXT",
          "TITLE",
          "SUBTITLE",
          "HEADING_1",
          "HEADING_2",
          "HEADING_3",
          "HEADING_4",
          "HEADING_5",
          "HEADING_6"
        ],
        "required": false,
        "type": "string"
      },
      "spacing_mode": {
        "description": "Paragraph spacing mode.",
        "enum": [
          "NEVER_COLLAPSE",
          "COLLAPSE_LISTS"
        ],
        "required": false,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "range_end": {
    "description": "Zero-based exclusive UTF-16 code-unit end index.",
    "minimum": 0,
    "required": true,
    "type": "integer"
  },
  "range_start": {
    "description": "Zero-based inclusive UTF-16 code-unit start index.",
    "minimum": 0,
    "required": true,
    "type": "integer"
  },
  "tab_id": {
    "description": "Target Google Docs tab ID from get_document tabs[].tab_id. If omitted, this indexed update targets the first tab.",
    "required": false,
    "type": "string"
  },
  "text_style": {
    "description": "Text styling options.",
    "properties": {
      "background_color": {
        "description": "Text highlight color as RGB values (0-1).",
        "required": false,
        "type": "object"
      },
      "bold": {
        "description": "Apply bold formatting.",
        "required": false,
        "type": "boolean"
      },
      "font_family": {
        "description": "Font family name (e.g., 'Arial', 'Times New Roman').",
        "required": false,
        "type": "string"
      },
      "font_size": {
        "description": "Font size with magnitude and unit.",
        "properties": {
          "magnitude": {
            "description": "Size value.",
            "required": true,
            "type": "number"
          },
          "unit": {
            "description": "Size unit (typically 'PT').",
            "required": true,
            "type": "string"
          }
        },
        "required": false,
        "type": "object"
      },
      "foreground_color": {
        "description": "Text color as RGB values (0-1).",
        "required": false,
        "type": "object"
      },
      "italic": {
        "description": "Apply italic formatting.",
        "required": false,
        "type": "boolean"
      },
      "link": {
        "description": "URL to create a hyperlink.",
        "required": false,
        "type": "string"
      },
      "strikethrough": {
        "description": "Apply strikethrough formatting.",
        "required": false,
        "type": "boolean"
      },
      "underline": {
        "description": "Apply underline formatting.",
        "required": false,
        "type": "boolean"
      }
    },
    "required": false,
    "type": "object"
  }
}
```
