---
name: google-docs
description: |
  Google Docs API integration with managed OAuth via Maton. Create documents, read full text, write/append content, search and replace, apply paragraph styles and text formatting (bold/heading), and export to PDF or DOCX. Use this skill when users want to read from or write to Google Docs.
compatibility: Requires network access and valid Maton API key
metadata:
  author: local
  version: "1.0.0"
  clawdbot:
    emoji: 📄
    requires:
      env:
        - MATON_API_KEY
---

# Google Docs

Access the Google Docs API with managed OAuth authentication. Create documents, read and write content, apply formatting, search & replace, and export files.

## Quick Start

```bash
# Read a document
python << 'EOF'
import urllib.request, os, json
doc_id = "YOUR_DOCUMENT_ID"
req = urllib.request.Request(f'https://gateway.maton.ai/google-docs/v1/documents/{doc_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
doc = json.load(urllib.request.urlopen(req))
# Extract plain text
text = ''.join(
    pe.get('textRun', {}).get('content', '')
    for elem in doc.get('body', {}).get('content', [])
    for pe in elem.get('paragraph', {}).get('elements', [])
)
print(json.dumps({'title': doc['title'], 'content': text}, ensure_ascii=False, indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/google-docs/{native-api-path}
```

The gateway proxies requests to `docs.googleapis.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:**

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Google OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python << 'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-docs&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python << 'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-docs'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
result = json.load(urllib.request.urlopen(req))
print(json.dumps(result, indent=2))
print('\n👉 Open this URL in a browser to authorize:', result['connection']['url'])
EOF
```

## API Reference

### Get Document

```
GET /google-docs/v1/documents/{documentId}
```

Returns the full document structure. Extract plain text:

```python
import os, json, urllib.request

def get_doc_text(doc_id):
    req = urllib.request.Request(
        f'https://gateway.maton.ai/google-docs/v1/documents/{doc_id}')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    doc = json.load(urllib.request.urlopen(req))
    text = ''.join(
        pe.get('textRun', {}).get('content', '')
        for elem in doc.get('body', {}).get('content', [])
        for pe in elem.get('paragraph', {}).get('elements', [])
    )
    return {'title': doc['title'], 'content': text, 'documentId': doc['documentId']}
```

### Create Document

```
POST /google-docs/v1/documents
Content-Type: application/json

{"title": "My New Document"}
```

```python
import os, json, urllib.request

data = json.dumps({'title': 'My New Document'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-docs/v1/documents',
                             data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
doc = json.load(urllib.request.urlopen(req))
print(f"Created: https://docs.google.com/document/d/{doc['documentId']}/edit")
```

### Batch Update (write, format, replace)

All content modifications use `batchUpdate`:

```
POST /google-docs/v1/documents/{documentId}:batchUpdate
Content-Type: application/json

{"requests": [...]}
```

## Common batchUpdate Requests

### Insert Text (append to end)

```python
import os, json, urllib.request

def append_text(doc_id, text):
    # First, get the document end index
    req = urllib.request.Request(
        f'https://gateway.maton.ai/google-docs/v1/documents/{doc_id}')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    doc = json.load(urllib.request.urlopen(req))
    content = doc.get('body', {}).get('content', [])
    end_index = content[-1].get('endIndex', 1) - 1 if content else 1

    # Insert text at end
    body = json.dumps({'requests': [{'insertText': {
        'location': {'index': end_index},
        'text': text
    }}]}).encode()
    req2 = urllib.request.Request(
        f'https://gateway.maton.ai/google-docs/v1/documents/{doc_id}:batchUpdate',
        data=body, method='POST')
    req2.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    req2.add_header('Content-Type', 'application/json')
    urllib.request.urlopen(req2)
    print(f'Appended {len(text)} chars')
```

### Search & Replace All

```json
{
  "requests": [{
    "replaceAllText": {
      "containsText": {"text": "old text", "matchCase": true},
      "replaceText": "new text"
    }
  }]
}
```

```python
import os, json, urllib.request

def replace_all(doc_id, find, replace):
    body = json.dumps({'requests': [{'replaceAllText': {
        'containsText': {'text': find, 'matchCase': True},
        'replaceText': replace
    }}]}).encode()
    req = urllib.request.Request(
        f'https://gateway.maton.ai/google-docs/v1/documents/{doc_id}:batchUpdate',
        data=body, method='POST')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    req.add_header('Content-Type', 'application/json')
    result = json.load(urllib.request.urlopen(req))
    n = result['replies'][0].get('replaceAllText', {}).get('occurrencesChanged', 0)
    print(f'Replaced {n} occurrences')
```

### Apply Paragraph Style (Heading)

Named styles: `NORMAL_TEXT` | `HEADING_1` ~ `HEADING_6` | `TITLE` | `SUBTITLE`

```json
{
  "requests": [{
    "updateParagraphStyle": {
      "range": {"startIndex": 1, "endIndex": 20},
      "paragraphStyle": {"namedStyleType": "HEADING_1"},
      "fields": "namedStyleType"
    }
  }]
}
```

### Apply Text Formatting (Bold / Italic)

```json
{
  "requests": [{
    "updateTextStyle": {
      "range": {"startIndex": 5, "endIndex": 15},
      "textStyle": {"bold": true, "italic": false},
      "fields": "bold,italic"
    }
  }]
}
```

### Delete Content Range

```json
{
  "requests": [{
    "deleteContentRange": {
      "range": {"startIndex": 1, "endIndex": 100}
    }
  }]
}
```

### Insert Page Break

```json
{
  "requests": [{
    "insertPageBreak": {
      "location": {"index": 50}
    }
  }]
}
```

## Export to PDF / DOCX (via Google Drive API)

Exports go through the Google Drive API (also proxied by Maton):

```python
import os, urllib.request, urllib.parse

def export_doc(doc_id, mime_type, output_path):
    # mime_type examples:
    #   'application/pdf'
    #   'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    #   'text/plain'
    url = (f'https://gateway.maton.ai/google-drive/drive/v3/files/{doc_id}/export'
           f'?mimeType={urllib.parse.quote(mime_type)}')
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    with urllib.request.urlopen(req) as resp:
        with open(output_path, 'wb') as f:
            f.write(resp.read())
    print(f'Exported to {output_path}')

# Export as PDF
export_doc('YOUR_DOC_ID', 'application/pdf', '/tmp/document.pdf')

# Export as Word
export_doc('YOUR_DOC_ID',
           'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
           '/tmp/document.docx')
```

## CLI Convenience Tool

A Python CLI wrapper is included for quick operations:

```bash
# Setup
pip install requests

# Set API key
export MATON_API_KEY="your_key"

# Manage connections
python3 gdocs_driver.py connections list
python3 gdocs_driver.py connections create   # Opens auth URL

# Create a document
python3 gdocs_driver.py create --title "My Document"

# Read document content
python3 gdocs_driver.py get --id DOCUMENT_ID_OR_URL

# Append text
python3 gdocs_driver.py append --id DOCUMENT_ID --content "New content here"

# Overwrite entire document
python3 gdocs_driver.py write --id DOCUMENT_ID --content "Fresh content"

# Search and replace
python3 gdocs_driver.py replace --id DOCUMENT_ID --find "old" --replace "new"

# Apply heading style
python3 gdocs_driver.py heading --id DOCUMENT_ID --text "Introduction" --level 1

# Bold specific text
python3 gdocs_driver.py bold --id DOCUMENT_ID --text "important phrase"

# Export to PDF
python3 gdocs_driver.py export --id DOCUMENT_ID --format pdf --output /tmp/doc.pdf
```

## Specifying a Connection

If you have multiple Google accounts connected, specify which one:

```bash
python << 'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-docs/v1/documents/DOC_ID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'YOUR_CONNECTION_ID')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Document ID

Extract the document ID from a Google Docs URL:

```
https://docs.google.com/document/d/{DOCUMENT_ID}/edit
```

The `{DOCUMENT_ID}` is the string between `/d/` and `/edit`.

## Notes

- `batchUpdate` requests are processed atomically — all succeed or all fail
- Index positions in the document are character-based (0-indexed); the document body starts at index 1
- For `replaceAllText`, the response includes `occurrencesChanged` — check this to confirm success
- Export via Google Drive API requires the same OAuth scope; use `google-drive` in the Maton gateway path
- IMPORTANT: When piping curl output, environment variables like `$MATON_API_KEY` may not expand correctly in some shells. Use Python snippets instead.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Google Docs connection or malformed request |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions on the document |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Google Docs API |

## Resources

- [Google Docs API Overview](https://developers.google.com/workspace/docs/api/reference/rest)
- [documents.get](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/get)
- [documents.create](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/create)
- [documents.batchUpdate](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/batchUpdate)
- [Request types](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/request)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
