---
name: jpeng-ab-test-analyzer
description: "Analyze A/B test results"
version: "1.0.0"
author: "jpeng"
tags: ["testing", "ab", "analytics"]
---

# A/B Test Analyzer

Analyze A/B test results

## When to Use

- User needs testing related functionality
- Automating ab tasks
- Analytics operations

## Usage

```bash
python3 scripts/ab_test_analyzer.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export AB_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
