---
name: docstrange
description: Document extraction via SkillBoss API Hub. Convert PDFs and images to markdown, JSON, or CSV with confidence scoring. Use when you need to OCR documents, extract invoice fields, parse receipts, or convert tables to structured data.
---

# DocStrange via SkillBoss API Hub

Document extraction — convert PDFs, images, and documents to markdown, JSON, or CSV with per-field confidence scoring, powered by SkillBoss API Hub.

## Quick Start

```bash
curl -X POST "https://api.heybossai.com/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "reducto/parse", "inputs": {"document_url": "https://example.com/document.pdf"}}'
```

Response:
```json
{
  "result": {
      "record_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "markdown": {
        "content": "# Invoice\n\n**Invoice Number:** INV-2024-001..."
      }
    }
  }
}
```

## Setup

### 1. Get Your API Key

Visit the SkillBoss dashboard to obtain your API key.

Save your API key:
```bash
export SKILLBOSS_API_KEY="your_api_key_here"
```

### 2. OpenClaw Configuration (Optional)

**Recommended: Use environment variables** (most secure):
```json5
{
  skills: {
    entries: {
      "docstrange": {
        enabled: true,
        // API key loaded from environment variable SKILLBOSS_API_KEY
      },
    },
  },
}
```

**Alternative: Store in config file** (use with caution):
```json5
{
  skills: {
    entries: {
      "docstrange": {
        enabled: true,
        env: {
          SKILLBOSS_API_KEY: "your_api_key_here",
        },
      },
    },
  },
}
```

**Security Note:** If storing API keys in `~/.openclaw/openclaw.json`:
- Set file permissions: `chmod 600 ~/.openclaw/openclaw.json`
- Never commit this file to version control
- Prefer environment variables or your agent's secret store when possible
- Rotate keys regularly and limit API key permissions if supported

## Common Tasks

### Extract to Markdown

```bash
curl -X POST "https://api.heybossai.com/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "reducto/parse", "inputs": {"document_url": "https://example.com/document.pdf"}}'
```

Access content: `response["data"]["result"]["markdown"]["content"]`

### Extract JSON Fields

**Simple field list:**
```bash
curl -X POST "https://api.heybossai.com/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "reducto/parse",
    "inputs": {
      "file_base64": "<base64-encoded-file>",
      "filename": "invoice.pdf",
      "output_format": "json",
      "json_options": ["invoice_number", "date", "total_amount", "vendor"],
      "include_metadata": "confidence_score"
    }
  }'
```

**With JSON schema:**
```bash
curl -X POST "https://api.heybossai.com/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "reducto/parse",
    "inputs": {
      "file_base64": "<base64-encoded-file>",
      "filename": "invoice.pdf",
      "output_format": "json",
      "json_options": {"type": "object", "properties": {"invoice_number": {"type": "string"}, "total_amount": {"type": "number"}}}
    }
  }'
```

Response with confidence scores:
```json
{
  "result": {
      "json": {
        "content": {
          "invoice_number": "INV-2024-001",
          "total_amount": 500.00
        },
        "metadata": {
          "confidence_score": {
            "invoice_number": 98,
            "total_amount": 99
          }
        }
      }
    }
  }
}
```

### Extract Tables to CSV

```bash
curl -X POST "https://api.heybossai.com/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "reducto/parse", "inputs": {"document_url": "https://example.com/table.pdf"}}'
```

### Async Extraction (Large Documents)

For documents >5 pages, use async and poll:

**Queue the document:**
```bash
curl -X POST "https://api.heybossai.com/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "reducto/parse", "inputs": {"file_base64": "<base64-encoded-file>", "filename": "large-document.pdf", "output_format": "markdown", "async": true}}'

# Returns: {"data": {"result": {"record_id": "12345", "status": "processing"}}}
```

**Poll for results:**
```bash
curl -X POST "https://api.heybossai.com/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "reducto/parse", "inputs": {"document_url": "https://example.com/document.pdf"}}'

# Returns: {"data": {"result": {"status": "completed", ...}}}
```

## Advanced Features

### Bounding Boxes
Get element coordinates for layout analysis:
```json
"include_metadata": "bounding_boxes"
```

### Hierarchy Output
Extract document structure (sections, tables, key-value pairs):
```json
"json_options": "hierarchy_output"
```

### Financial Documents Mode
Enhanced table and number formatting:
```json
"markdown_options": "financial-docs"
```

### Custom Instructions
Guide extraction with prompts:
```json
"custom_instructions": "Focus on financial data. Ignore headers.",
"prompt_mode": "append"
```

### Multiple Formats
Request multiple formats in one call:
```json
"output_format": "markdown,json"
```

## When to Use

### Use Document Extraction via SkillBoss API Hub For:
- Invoice and receipt processing
- Contract text extraction
- Bank statement parsing
- Form digitization
- Image OCR (scanned documents)

### Don't Use For:
- Documents >5 pages with sync (use async)
- Video/audio transcription
- Non-document images

## Best Practices

| Document Size | Mode | Notes |
|---------------|------|-------|
| <=5 pages | sync (default) | Immediate response |
| >5 pages | `"async": true` | Poll for results |

**JSON Extraction:**
- Field list: `["field1", "field2"]` — quick extractions
- JSON schema: `{"type": "object", ...}` — strict typing, nested data

**Confidence Scores:**
- Add `"include_metadata": "confidence_score"`
- Scores are 0-100 per field
- Review fields <80 manually

## Schema Templates

### Invoice
```json
{
  "type": "object",
  "properties": {
    "invoice_number": {"type": "string"},
    "date": {"type": "string"},
    "vendor": {"type": "string"},
    "total": {"type": "number"},
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": {"type": "string"},
          "quantity": {"type": "number"},
          "price": {"type": "number"}
        }
      }
    }
  }
}
```

### Receipt
```json
{
  "type": "object",
  "properties": {
    "merchant": {"type": "string"},
    "date": {"type": "string"},
    "total": {"type": "number"},
    "items": {
      "type": "array",
      "items": {"type": "object", "properties": {"name": {"type": "string"}, "price": {"type": "number"}}}
    }
  }
}
```

## Security & Privacy

### Data Handling

**Important:** Documents uploaded via SkillBoss API Hub are transmitted to `https://api.heybossai.com` and processed through the SkillBoss infrastructure.

**Before uploading sensitive documents:**
- Review SkillBoss API Hub's privacy policy and data retention policies
- Verify encryption in transit (HTTPS) and at rest
- Confirm data deletion/retention timelines
- Test with non-sensitive sample documents first

**Best practices:**
- Do not upload highly sensitive PII (SSNs, medical records, financial account numbers) until you've confirmed the service's security and compliance posture
- Rotate API keys regularly (every 90 days recommended)
- Monitor API usage logs for unauthorized access
- Never log or commit API keys to repositories or examples

### File Size Limits

- **Sync mode:** Recommended for documents ≤5 pages
- **Async mode:** Use `"async": true` for documents >5 pages to avoid timeouts
- **Large files:** Consider using `file_url` with publicly accessible URLs instead of uploading large files directly

### Operational Safeguards

- Always use environment variables or secure secret stores for API keys
- Never include real API keys in code examples or documentation
- Use placeholder values like `"your_api_key_here"` in examples
- Set appropriate file permissions on configuration files (600 for JSON configs)
- Enable API key rotation and monitor usage through the dashboard

## Troubleshooting

**400 Bad Request:**
- Provide exactly one input: `file_base64` or `file_url`
- Verify `SKILLBOSS_API_KEY` is valid

**Sync Timeout:**
- Use `"async": true` for documents >5 pages
- Poll with `"action": "get_result"` and `"record_id"`

**Missing Confidence Scores:**
- Requires `json_options` (field list or schema)
- Add `"include_metadata": "confidence_score"`

**Authentication Errors:**
- Verify `SKILLBOSS_API_KEY` environment variable is set
- Check API key hasn't expired or been revoked
- Ensure no extra whitespace in API key value

## Pre-Publish Security Checklist

Before publishing or updating this skill, verify:

- [ ] `package.json` declares `requiredEnv` and `primaryEnv` for `SKILLBOSS_API_KEY`
- [ ] `package.json` lists API endpoints in `endpoints` array
- [ ] All code examples use placeholder values (`"your_api_key_here"`) not real keys
- [ ] No API keys or secrets are embedded in `SKILL.md` or `package.json`
- [ ] Security & Privacy section documents data handling and risks
- [ ] Configuration examples include security warnings for plaintext storage
- [ ] File permission guidance is included for config files

## References

- **API Docs:** https://api.heybossai.com/v1/pilot (use `{}` body for Guide mode)
- **SkillBoss API Hub:** https://api.heybossai.com
