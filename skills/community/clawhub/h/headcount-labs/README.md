# Headcount Labs for OpenClaw

An OpenClaw skill that connects your agent to the Headcount Labs job-postings
MCP server: **8.4M current job postings from 200k+ job boards**, refreshed
daily. Search jobs, count matches, get salary ranges, and analyze the job
market — no account or API key needed.

## Install

```bash
clawhub install headcount-labs
```

Then register the MCP server once:

```bash
openclaw mcp set headcountlabs '{"url":"https://api.headcountlabs.com/mcp/public","transport":"streamable-http"}'
```

## Try it

- "Find me remote backend engineer jobs in Texas"
- "How many companies are hiring data analysts right now?"
- "What's the salary range for a store associate in Ohio?"
- "Which employers posted the most jobs this week?"

## Details

- Tools (all read-only): `search_jobs`, `get_job`, `count_jobs`,
  `market_lookup`, `market_breakdown`, `salary_range`, `market_dimensions`,
  `list_fields`, `search_docs`
- Free public endpoint limits: 50 jobs per page, 250 per search
- Optional free account: first 100,000 records/month free, then $0.01 per
  1,000 records — https://headcountlabs.com/pricing/
- Docs: https://headcountlabs.com/mcp/
- Bulk dataset (CC BY 4.0): https://huggingface.co/datasets/HeadcountLabs/job-postings

Published by Headcount Labs. We sell data, not scrapers.
