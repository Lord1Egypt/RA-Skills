# Olostep OpenClaw Skill

Scrape, search, crawl, map, batch, and get AI answers from the web — directly from your OpenClaw agent.

## Install

```bash
clawhub install olostep
```

Or manually: clone this repo and symlink/copy the directory into your OpenClaw skills folder.

## Setup

1. Get a free API key at [olostep.com/auth](https://olostep.com/auth) (500 requests/month, no credit card)
2. Set it in your OpenClaw config:

```bash
openclaw config set skills.entries.olostep.env.OLOSTEP_API_KEY "your-key-here"
```

Or set the environment variable:
```bash
export OLOSTEP_API_KEY="your-key-here"
```

## What it does

| Tool | Description |
|------|-------------|
| **Scrape** | Extract content from any URL as markdown/HTML/text/JSON with JS rendering |
| **Search** | Structured Google search results (titles, URLs, snippets, knowledge graph) |
| **Crawl** | Recursively crawl websites following links |
| **Batch** | Scrape up to 10,000 URLs in parallel |
| **Map** | Discover all URLs on a site with glob filtering |
| **Answers** | AI-powered answers with source citations and optional JSON schema |

## Links

- [Olostep API Docs](https://docs.olostep.com)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.ai)
