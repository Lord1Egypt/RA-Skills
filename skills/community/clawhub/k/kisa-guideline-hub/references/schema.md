# Notion Database Schema for Guidelines

## Database Properties

**GUIDE_DATABASE_ID**: Notion database ID for guidelines
- Environment variable: `SECURITY_GUIDE_DATABASE_ID`
- Falls back to: `SECURITY_NEWS_DATABASE_ID`

## Required Properties

### Title (title type)
- Guideline name
- Example: "2025년 사이버 위협 대응 가이드라인"

### Category (select type)
- Values:
  - "KISA 가이드라인"
  - "보호나라 가이드라인"

### Date (date type)
- Publication date
- Format: YYYY-MM-DD

### URL (url type)
- Original source URL
- Example: "https://인터넷진흥원.한국/2060207?page=1"

## Optional Properties

### Content (text type)
- Brief description
- Max 2000 characters

### Files (file type)
- PDF attachments
- Boho guidelines only
- Max 20MB per file

## Block Structure

Guideline pages contain:

1. **Content block** (paragraph)
   - Brief description
   - Empty if not available

2. **File blocks** (Boho only)
   - PDF files
   - Uploaded via Notion API

## Example Page

```json
{
  "parent": {
    "database_id": "GUIDE_DATABASE_ID"
  },
  "properties": {
    "제목": {
      "title": [
        {
          "text": {
            "content": "2025년 사이버 위협 대응 가이드라인"
          }
        }
      ]
    },
    "category": {
      "select": {
        "name": "KISA 가이드라인"
      }
    },
    "date": {
      "date": {
        "start": "2025-03-09"
      }
    },
    "url": {
      "url": "https://인터넷진흥원.한국/2060207?page=1"
    }
  }
}
```

## Duplicate Prevention

- Uses `Duplicate_check()` function
- Based on URL matching
- Safe to run multiple times
- Existing pages are skipped

## File Upload Process

1. Download PDF to `temp_downloads_boho/`
2. Upload to Notion via `upload_file_to_notion()`
3. Create file block with `file_upload` type
4. Add to page children blocks

## API Version

- Notion-Version: 2025-09-03
- Supports file uploads via `file_upload` type
