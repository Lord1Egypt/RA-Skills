---
name: jpeng-knitting-pattern
description: "Find knitting patterns"
version: "1.0.0"
author: "jpeng"
tags: ["crafts", "knitting", "diy"]
---

# Knitting Pattern

Find knitting patterns

## When to Use

- User needs crafts related functionality
- Automating knitting tasks
- Diy operations

## Usage

```bash
python3 scripts/knitting_pattern.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export KNITTING_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
