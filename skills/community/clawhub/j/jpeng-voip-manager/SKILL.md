---
name: jpeng-voip-manager
description: "Manage VoIP calls"
version: "1.0.0"
author: "jpeng"
tags: ["voice", "voip", "communication"]
---

# VoIP Manager

Manage VoIP calls

## When to Use

- User needs voice related functionality
- Automating voip tasks
- Communication operations

## Usage

```bash
python3 scripts/voip_manager.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export VOIP_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
