# MarkItDown Hosted Markdown Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `markitdown`

x402 availability: not enabled for this product.

## `convert`

Action slug: `convert`

Price: `5` credits

Convert a file to Markdown. Provide the file using exactly one of: url, file_id, or file_base64. Supports PDF, Word, Excel, PowerPoint, HTML, CSV, JSON, XML, images, audio, EPub, and ZIP. Max 50MB.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_base64` | `string` | no | Base64-encoded file content |
| `file_id` | `string` | no | File ID from the file upload tool |
| `filename` | `string` | no | Original filename with extension (helps detect format when using file_base64) |
| `url` | `string` | no | Public URL or signed storage URL of the file to convert |

Sample parameters:

```json
{
  "file_base64": "example file base64",
  "file_id": "example file id",
  "filename": "example filename",
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "file_base64": {
    "description": "Base64-encoded file content",
    "required": false,
    "type": "string"
  },
  "file_id": {
    "description": "File ID from the file upload tool",
    "required": false,
    "type": "string"
  },
  "filename": {
    "description": "Original filename with extension (helps detect format when using file_base64)",
    "required": false,
    "type": "string"
  },
  "url": {
    "description": "Public URL or signed storage URL of the file to convert",
    "required": false,
    "type": "string"
  }
}
```
