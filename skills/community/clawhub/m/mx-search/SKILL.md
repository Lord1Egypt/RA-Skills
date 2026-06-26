---
name: mx_search
description: Retrieve timely, authoritative financial news, announcements, research reports, policies, and other finance‑related information using the Meixiang (妙想) search API. Use when the user asks for up‑to‑date financial insight and wants to avoid non‑official or outdated sources.
---

# 妙想资讯搜索 Skill (mx_search)

## Overview
This skill provides a safe way to query the Meixiang financial search service for news, announcements, research reports, policy documents, trading rules, specific events, impact analyses, and any other external data needed for finance‑related queries. It ensures the results come from authoritative sources and are current.

## Prerequisites
1. Obtain an API key from the Meixiang Skills page.
2. Set the API key in the environment variable `MX_APIKEY`.
   ```bash
   export MX_APIKEY="your_api_key_here"
   ```
3. Ensure `curl` is available on the system (default on macOS).

## Usage
When the user asks a finance‑related question, follow these steps:
1. Construct the query string based on the user's request.
2. Execute the POST request to the Meixiang endpoint:
   ```bash
   curl -X POST \
     --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search' \
     --header 'Content-Type: application/json' \
     --header "apikey:${MX_APIKEY}" \
     --data '{"query":"<YOUR_QUERY_HERE>"}'
   ```
3. Parse the JSON response. Important fields include:
   - `title`: concise headline of the information.
   - `secuList`: list of related securities (code, name, type).
   - `trunk`: main text or structured data block.
4. Present the information to the user in a readable format, optionally highlighting the securities involved.

## Example
**User query:** "立讯精密的资讯"

**Command executed:**
```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search' \
  --header 'Content-Type: application/json' \
  --header 'apikey:${MX_APIKEY}' \
  --data '{"query":"立讯精密的资讯"}'
```

**Sample response excerpt:**
```json
{
  "title": "立讯精密最新研报",
  "secuList": [{"secuCode":"002475","secuName":"立讯精密","secuType":"股票"}],
  "trunk": "...report content..."
}
```

**Formatted reply to user:**
- **标题:** 立讯精密最新研报
- **关联证券:** 002475 立讯精密 (股票)
- **内容摘要:** ... (provide concise summary from `trunk`)

## Saving Results (optional)
If the user wants to keep the result, you can save the raw JSON to a file in the current work directory:
```bash
curl ... > mx_search_result.json
```
Then inform the user of the file path.

## When Not to Use
Do not use this skill for non‑financial queries, or when the user explicitly asks for opinion‑based answers without needing source data.

## References
- Meixiang API documentation (internal).
- Example queries table (see above).
