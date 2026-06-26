---
name: jpeng-job-poster
description: "Post job listings"
version: "1.0.0"
author: "jpeng"
tags: ["recruitment", "job", "hr"]
---

# Job Poster

Post job listings

## When to Use

- User needs recruitment related functionality
- Automating job tasks
- Hr operations

## Usage

```bash
python3 scripts/job_poster.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export JOB_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
