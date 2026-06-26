# keyword-intelligence

Multi-source keyword research and autocomplete intelligence — no API keys, no paid tools. Pulls real-time suggestions from Google, YouTube, Amazon, and DuckDuckGo in one command.

## The Problem This Solves

Keyword research tools are expensive, slow, or require API keys. Google Keyword Planner hides data behind ad spend. Most free tools only check one source.

## The Solution

A single script that queries all major autocomplete APIs simultaneously, with an optional expand mode that fetches suggestions *of* suggestions — giving you 10x more keywords in seconds.

## What's Included

- `SKILL.md` — Full usage guide and workflow
- `scripts/fetch_suggestions.py` — Zero-dependency Python script (stdlib only)

## Features

- **4 Sources**: Google, YouTube, Amazon, DuckDuckGo
- **Expand Mode**: 2nd-level suggestions (~10x more keywords)
- **Multi-language/region**: `--lang de`, `--lang en`, `--region us`, etc.
- **JSON output**: Pipe into other tools or workflows
- **No API key needed**: Works out of the box

## Quick Start

```bash
# All sources, German
python3 scripts/fetch_suggestions.py "keyword"

# English, US region
python3 scripts/fetch_suggestions.py "keyword" --lang en --region us

# Deep expand mode (10x keywords)
python3 scripts/fetch_suggestions.py "keyword" --sources google --expand

# JSON output
python3 scripts/fetch_suggestions.py "keyword" --json
```

## Who This Is For

- SEO professionals and content marketers
- Agency owners doing keyword research for clients
- Developers building keyword tools or content pipelines
- Anyone who wants to know what people actually search for
