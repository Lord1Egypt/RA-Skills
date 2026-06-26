---
name: openclaw-free-search
description: Free web search for OpenClaw without API keys. Uses a free search service to search the web and get results. No Brave/Perplexity API key required. Use when you need to search the web but don't have API keys configured.
---

# OpenClaw Free Web Search

Search the web without API keys. This skill provides free web search capability using a no-cost search service.

## Installation

```bash
npx clawhub@latest install openclaw-free-search
```

## Usage

After installation, use the search script:

```bash
node ~/.openclaw/skills/openclaw-free-search/search.js 'your search query'
```

## Features

- ✅ No API keys required
- ✅ English and Chinese queries supported
- ✅ JSON output available (with --json flag)
- ✅ Fast and reliable

## Examples

```bash
# Basic search
node ~/.openclaw/skills/openclaw-free-search/search.js 'OpenClaw installation guide'

# JSON output
node ~/.openclaw/skills/openclaw-free-search/search.js 'AI agent automation' --json
```

## Need Help?

If you need help with OpenClaw:
- 📧 **Installation Service**: ¥99-299
- 🔗 **Landing Page**: https://yang1002378395-cmyk.github.io/openclaw-install-service/

## License

MIT
