# open-perplexity

A tiny OpenClaw/ClawHub browser skill that opens **Perplexity AI** directly in the user's **Brave** browser.

## Features

- Opens `https://www.perplexity.ai/`
- Reuses an existing Brave session when possible
- Avoids duplicate Perplexity tabs when one is already open
- Can optionally search or submit a prompt when explicitly requested
- Verifies that the page actually loaded
- Requires no API key

## Trigger examples

```text
Open Perplexity
Go to Perplexity
Open Perplexity AI
Start a Perplexity session
Search Perplexity for the latest AI news
Ask Perplexity what MCP is
```

## Installation

Place the folder in your OpenClaw workspace:

```text
skills/open-perplexity/
```

The required file is:

```text
SKILL.md
```

## Configuration

`config.yaml` documents the target browser and URL. It does not contain credentials.

## Privacy

This skill does not request or store credentials, cookies, or API keys.

## License

MIT
