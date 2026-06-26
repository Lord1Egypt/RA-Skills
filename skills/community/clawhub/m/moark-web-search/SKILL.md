---
name: moark-web-search
description: Search web content such as webpages, images, and videos using the /web-search API with an Access Token.
metadata:
  {
    "openclaw":
      {
        "emoji":"🔎",
        "requires": { "env": ["GITEEAI_API_KEY"]},
        "primaryEnv": "GITEEAI_API_KEY"
      }
  }
---

# Web Search

This skill allows users to search web content through the `/web-search` API. It is suitable for information lookup, recent content discovery, webpage search, image search, and video search.

## Usage

Ensure you have installed the required dependency (`pip install requests`). Use the bundled script to perform the search.

```bash
python {baseDir}/scripts/perform_web_search.py \
  --query "阿里巴巴2024年的ESG报告" \
  --summary true \
  --freshness noLimit \
  --count 10 \
  --api-key YOUR_API_KEY
```

## Options

- `--query` - Search keywords or a natural language question.
- `--summary` - Whether to include summaries in the results. Accepts `true` or `false`. Default is `true`.
- `--freshness` - Time filter. Options: `noLimit`, `oneDay`, `oneWeek`, `oneMonth`, `oneYear`.
- `--count` - Number of results to return. Default is `10`.
- `--api-key` - API key used in the `Authorization: Bearer` header. If omitted, read from `GITEEAI_API_KEY`.

## Workflow

1. Execute `perform_web_search.py` with the user parameters.
2. Parse the script output and find the line starting with `SEARCH_RESULTS_JSON:`.
3. Extract the JSON payload from that line.
4. Summarize the most relevant results for the user, prioritizing `webPages.value`.

## Notes

- The response language should be consistent with the user's question.
- Prefer `webPages.value` unless the user explicitly asks for images or videos.
- If the user asks for recent information, set `--freshness` accordingly.
- If the API returns no results, say that directly instead of fabricating answers.
- If `GITEEAI_API_KEY` is missing, the user must provide `--api-key`.
- The script prints `SEARCH_RESULTS_JSON:` in the output. Always parse that line.
