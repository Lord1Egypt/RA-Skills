---
name: perplexity-agent
description: "Search the web using the Perplexity Agent API. Provides real-time information, news, and grounded answers with citations. Use when the user asks for: (1) Current events or news, (2) Information retrieval from the web, (3) Real-time data search, (4) In-depth research using web results."
---

# Perplexity Agent Search

Use the Perplexity Agent API to perform real-time web searches and get grounded answers.

## Workflow

To perform a web search:

1.  Identify the user's research or search query.
2.  Execute the `scripts/search.py` script with the query.
3.  Present the `answer` from the JSON response to the user.

### Example

To search for "latest AI developments":
`python3 scripts/search.py "What are the latest developments in AI?"`

## Important

- Requires `PERPLEXITY_API_KEY` to be set in the environment.
- Uses the `pro-search` preset for high-quality, researched results.
- Returns a JSON object with `success`, `answer`, and the `model` used.
