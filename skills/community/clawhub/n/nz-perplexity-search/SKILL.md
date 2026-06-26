---
name: perplexity-search
version: 1.0.0
description: Search the web with Perplexity Sonar API for current information, citations, and web-grounded answers.
homepage: https://clawhub.ai
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["python3"],"env":["PERPLEXITY_API_KEY"]},"primaryEnv":"PERPLEXITY_API_KEY","files":["scripts/*"]}}
---

# Perplexity Search

Use this skill to search the web via the Perplexity Sonar API. It returns accurate, cited, real-time answers grounded in current web sources.

## When to use this skill

Invoke this skill automatically when the user asks about:
- Current events, recent news, or anything that may have changed recently
- Product releases, software versions, or API documentation
- Research questions that benefit from citations and web sources
- Comparisons, pricing, or availability that requires live data
- Any question where freshness or sourcing matters

**Trigger phrases:** "search for", "look up", "find out", "what's the latest", "current", "recent", "news about", "web search", "perplexity search"

## Setup

Set your Perplexity API key in the environment before starting OpenClaw:

```bash
# Add to ~/.openclaw/.env
PERPLEXITY_API_KEY=pplx-your-key-here
```

Get a key at https://www.perplexity.ai/settings/api

## Command

```bash
python3 {baseDir}/scripts/perplexity_search.py --query "<the user's question>"
```

### Optional flags

| Flag | Default | Description |
|------|---------|-------------|
| `--model sonar` | sonar | Fast, general-purpose search |
| `--model sonar-pro` | — | Higher quality synthesis (costs more) |
| `--model sonar-reasoning` | — | Step-by-step reasoning |
| `--domains example.com` | — | Comma-separated domain allowlist |
| `--max-results 8` | 8 | Cap displayed search results |
| `--temperature 0.2` | 0.2 | Lower = more factual |
| `--json` | — | Print raw JSON response |

## Usage examples

```bash
# General search
python3 {baseDir}/scripts/perplexity_search.py --query "latest AI agent frameworks 2025"

# Higher quality synthesis
python3 {baseDir}/scripts/perplexity_search.py --query "compare Perplexity vs Tavily search APIs" --model sonar-pro

# Restrict to a specific site
python3 {baseDir}/scripts/perplexity_search.py --query "PostgreSQL 17 release notes" --domains postgresql.org

# Reasoning mode for complex topics
python3 {baseDir}/scripts/perplexity_search.py --query "why did SVB fail" --model sonar-reasoning
```

## Output

The script prints a structured markdown report with:
1. **Answer** — concise, web-grounded response
2. **Citations** — numbered source URLs
3. **Search Results** — titles, URLs, and snippets
4. **Related Questions** — follow-up ideas
5. **Usage** — token and cost metadata

## Agent workflow

1. Identify the user's search intent from their message.
2. Extract a clean, specific query (avoid filler words).
3. Choose `sonar` for speed, `sonar-pro` for depth.
4. Run the command with `python3 {baseDir}/scripts/perplexity_search.py --query "..."`.
5. Present the Answer and Citations to the user in a readable format.
6. Offer related questions as follow-up options.

## Security notes

- The script reads `PERPLEXITY_API_KEY` from the environment only — never from arguments.
- The API key is never logged or printed.
- All external calls go only to `https://api.perplexity.ai/chat/completions`.
- No local files are written.

## SECURITY MANIFEST
- Environment variables accessed: PERPLEXITY_API_KEY (only)
- External endpoints called: https://api.perplexity.ai/chat/completions (only)
- Local files read: none
- Local files written: none
