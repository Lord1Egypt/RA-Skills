# Knowledge Base Index Schema

## Document Entry Structure

Each ingested document creates two files:

### 1. Text File: `kb/docs/<id>.txt`
Plain text extracted from the PDF.

### 2. Metadata: `kb/index/<id>.json`
```json
{
  "id": "abc123",           // 12-char MD5 hash of source path
  "name": "document-name", // Original filename (no extension)
  "source": "/full/path/to/source.pdf",
  "ingested": "2026-03-21T09:00:00+08:00",
  "text_file": "/path/to/kb/docs/abc123.txt"
}
```

## Query Patterns

### Find document by ID
```bash
cat "$KB_ROOT/index/${DOC_ID}.json"
```

### List all documents
```bash
ls "$KB_ROOT/index/" | sed 's/.json$//'
```

### Search metadata field
```bash
grep -o '"name": *"[^"]*"' "$META" | cut -d'"' -f4
```

## Future Extensions

For production use, consider adding:
- Vector embeddings (use `sentence-transformers` or Ollama embeddings)
- Document tags and categories
- Citation/references extraction
- Automatic concept graph building
