# Google Docs Connector Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `google-docs-connector`

x402 availability: not enabled for this product.

## `batch_update`

Action slug: `batch-update`

Price: `5` credits

Execute raw Google Docs API batch update requests for advanced operations not covered by other actions.

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

Create a new Google Doc.

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
| `range_end` | `integer` | yes | End index of the range (1-based). |
| `range_name` | `string` | yes | Name for the named range/bookmark. |
| `range_start` | `integer` | yes | Start index of the range (1-based). |

Sample parameters:

```json
{
  "document_id": "example document id",
  "range_end": 1,
  "range_name": "example range name",
  "range_start": 1
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
    "description": "End index of the range (1-based).",
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "range_name": {
    "description": "Name for the named range/bookmark.",
    "required": true,
    "type": "string"
  },
  "range_start": {
    "description": "Start index of the range (1-based).",
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `create_table`

Action slug: `create-table`

Price: `5` credits

Insert a table into a document, optionally populated with data. If table_data is provided, dimensions are inferred from it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `columns` | `integer` | no | Number of table columns (1-20). Not needed if table_data is provided. |
| `document_id` | `string` | yes | Google Docs document ID. |
| `location` | `integer` | no | 1-based character index for table insertion. Defaults to 1. |
| `rows` | `integer` | no | Number of table rows (1-100). Not needed if table_data is provided. |
| `table_data` | `array` | no | 2D array of strings representing table cell data. |

Sample parameters:

```json
{
  "columns": 1,
  "document_id": "example document id",
  "location": 1,
  "rows": 1,
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
    "description": "1-based character index for table insertion. Defaults to 1.",
    "minimum": 1,
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

Export a document to another format. Text formats (txt, html) return content directly; binary formats return base64-encoded content.

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

Apply text and/or paragraph styling to a character range in a document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `paragraph_style` | `object` | no | Paragraph styling options. |
| `range_end` | `integer` | yes | End index of the range to format (1-based). |
| `range_start` | `integer` | yes | Start index of the range to format (1-based). |
| `text_style` | `object` | yes | Text styling options. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "paragraph_style": {
    "alignment": "START",
    "indent_end": {},
    "indent_first_line": {},
    "indent_start": {},
    "line_spacing": 1
  },
  "range_end": 1,
  "range_start": 1,
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
    "description": "Paragraph styling options.",
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
      }
    },
    "required": false,
    "type": "object"
  },
  "range_end": {
    "description": "End index of the range to format (1-based).",
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "range_start": {
    "description": "Start index of the range to format (1-based).",
    "minimum": 1,
    "required": true,
    "type": "integer"
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
    "required": true,
    "type": "object"
  }
}
```

## `get_document`

Action slug: `get-document`

Price: `5` credits

Retrieve a document's full content, text, word count, and structure.

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
| `location` | `integer` | no | 1-based character index for insertion. Defaults to 1. |
| `width` | `integer` | no | Image width in pixels. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "height": 1,
  "image_url": "https://example.com",
  "location": 1,
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
    "description": "1-based character index for insertion. Defaults to 1.",
    "minimum": 1,
    "required": false,
    "type": "integer"
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
| `location` | `integer` | no | 1-based character index for the page break. Defaults to 1. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "location": 1
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
    "description": "1-based character index for the page break. Defaults to 1.",
    "minimum": 1,
    "required": false,
    "type": "integer"
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
| `location` | `integer` | no | 1-based character index for the section break. Defaults to 1. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "location": 1
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
    "description": "1-based character index for the section break. Defaults to 1.",
    "minimum": 1,
    "required": false,
    "type": "integer"
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
| `location` | `integer` | no | 1-based character index for insertion. Defaults to 1 (beginning of document). |
| `text` | `string` | yes | Text content to insert. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "location": 1,
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
    "description": "1-based character index for insertion. Defaults to 1 (beginning of document).",
    "minimum": 1,
    "required": false,
    "type": "integer"
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

Create a document from a natural language description. If the text contains 'titled "..."' or 'called "..."', the title is extracted automatically.

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

## `replace_text`

Action slug: `replace-text`

Price: `5` credits

Find and replace all occurrences of text in a document.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `match_case` | `boolean` | no | Whether to use case-sensitive search. |
| `replace_with` | `string` | yes | Replacement text. |
| `search_text` | `string` | yes | Text to search for. |

Sample parameters:

```json
{
  "document_id": "example document id",
  "match_case": false,
  "replace_with": "example replace with",
  "search_text": "example search query"
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

Alias for format_text. Apply text and/or paragraph styling to a character range.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `string` | yes | Google Docs document ID. |
| `paragraph_style` | `object` | no | Paragraph styling options (alignment, line_spacing, indents). |
| `range_end` | `integer` | yes | End index of the range to format (1-based). |
| `range_start` | `integer` | yes | Start index of the range to format (1-based). |
| `text_style` | `object` | yes | Text styling options (bold, italic, underline, strikethrough, font_family, font_size, foreground_color, background_color, link). |

Sample parameters:

```json
{
  "document_id": "example document id",
  "paragraph_style": {},
  "range_end": 1,
  "range_start": 1,
  "text_style": {}
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
    "description": "Paragraph styling options (alignment, line_spacing, indents).",
    "required": false,
    "type": "object"
  },
  "range_end": {
    "description": "End index of the range to format (1-based).",
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "range_start": {
    "description": "Start index of the range to format (1-based).",
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "text_style": {
    "description": "Text styling options (bold, italic, underline, strikethrough, font_family, font_size, foreground_color, background_color, link).",
    "required": true,
    "type": "object"
  }
}
```
