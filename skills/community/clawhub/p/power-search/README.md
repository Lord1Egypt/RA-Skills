# Power Search

🔍 Self-hosted web research tool combining Brave Search API + Browserless content fetching.

## Quick Start

```bash
# Install
clawhub install power-search

# Use
search "nodejs frameworks"
search "machine learning" --fetch --limit 5
```

## Features

✨ **Fast search** via Brave API (10 results in <1s)  
📄 **Content fetching** with Browserless headless browser  
🧹 **HTML extraction** with clean text parsing  
💻 **CLI tool** for quick access  
📱 **Telegram integration** ready (OpenClaw)  
🏠 **Self-hosted** — no cloud dependencies  

## Requirements

- Docker (for Browserless)
- Node.js 18+
- Brave Search API key (free, 100/day)

## Setup

See [SKILL.md](SKILL.md) for detailed installation and configuration.

## Usage

### Basic Search
```bash
search "artemis 2"
```

### Search + Fetch Content
```bash
search "artemis 2" --fetch --limit 3
```

### Verbose Mode
```bash
search "artemis 2" --fetch --verbose
```

## Documentation

- **[SKILL.md](SKILL.md)** — Full documentation, API, troubleshooting
- **[OpenClaw Manifest](openclaw.json)** — Integration configuration

## Performance

- **Search:** <1 second
- **Fetch:** 2-10 seconds per page
- **Extract:** <500ms

## License

MIT

## Author

Kaito
