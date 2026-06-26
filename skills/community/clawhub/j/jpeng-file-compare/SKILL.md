---
name: jpeng-file-compare
description: "Compare two files"
version: "1.0.0"
author: "jpeng"
tags: ["utility", "compare", "filesystem"]
---

# File Compare

Compare two files

## When to Use

- User needs utility related functionality
- Automating compare tasks
- Filesystem operations

## Usage

```bash
python3 scripts/file_compare.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export COMPARE_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
