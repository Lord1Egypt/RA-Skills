# Perplexica Search Skill 🔍

An [OpenClaw](https://open-claw.bot) skill that runs AI-powered search against your **local** [Perplexica](https://github.com/ItzCrazyKns/Perplexica) instance. Uses deep research (quality mode), web search, and LLM reasoning to return answers with cited sources in OpenClaw while keeping search/RAG state in Perplexica.

**Local-only:** only `localhost`, `127.0.0.1`, `::1`, or `host.docker.internal` (Docker) are allowed; remote URLs are rejected. HTTP redirects are not followed.

## Installation

```bash
# From ClawHub (when published)
clawhub install perplexica-search

# From GitHub
git clone https://github.com/eplt/perplexica-search.git ~/.openclaw/skills/perplexica-search
```

## Prerequisites

- **python3** (required)
- Perplexica running locally (default: `http://localhost:3000`)
- At least one chat model provider configured in Perplexica
- Python 3.8+

## Quick Start

```bash
# Basic search
python3 scripts/perplexica_search.py "What is quantum computing?"

# Quality mode with academic sources
python3 scripts/perplexica_search.py "Transformer architecture 2024" --mode quality --sources academic

# JSON output for programmatic use
python3 scripts/perplexica_search.py "Python async best practices" --json
```

## Usage

```
usage: perplexica_search.py [-h] [-u URL] [-m {speed,balanced,quality}]
                            [-s SOURCES] [--chat-model CHAT_MODEL]
                            [--embedding-model EMBEDDING_MODEL]
                            [-i INSTRUCTIONS] [--history HISTORY] [-j]
                            [--stream]
                            query

AI-powered search using local Perplexica instance

positional arguments:
  query                 Search query

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Local Perplexica base URL only (default: http://localhost:3000). Allowed: localhost, 127.0.0.1, ::1, host.docker.internal.
  -m {speed,balanced,quality}, --mode {speed,balanced,quality}
                        Optimization mode
  -s SOURCES, --sources SOURCES
                        Search sources: web,academic,discussions
  --chat-model CHAT_MODEL
                        Chat model key (e.g., gpt-4o-mini)
  --embedding-model EMBEDDING_MODEL
                        Embedding model key
  -i INSTRUCTIONS, --instructions INSTRUCTIONS
                        Custom system instructions
  --history HISTORY     Conversation history as JSON array
  -j, --json            Output raw JSON
  --stream              Enable streaming
```

## Examples

### Quick Fact Check
```bash
python3 scripts/perplexica_search.py "Who won the 2024 Nobel Prize in Physics?"
```

### Academic Research
```bash
python3 scripts/perplexica_search.py "CRISPR gene editing advances" --sources academic --mode quality
```

### Technical Deep Dive
```bash
python3 scripts/perplexica_search.py "Rust memory safety vs C++" \
  --instructions "Focus on practical examples and performance comparisons"
```

### Multi-Turn Conversation
```bash
python3 scripts/perplexica_search.py "Explain more about that" \
  --history '[["human", "What is quantum entanglement?"], ["assistant", "Quantum entanglement is..."]]'
```

## Configuration

Optional: copy `config.json.example` to `config.json` in the skill directory and edit as needed. **`perplexica_url` must be a local URL only** (localhost, 127.0.0.1, ::1, or host.docker.internal). See [config.json.example](config.json.example) for the full schema.

## Streaming (avoids timeouts)

The skill uses **streaming** (same as the Perplexica web UI): the server sends chunks as they’re generated, so long-running quality/deep research doesn’t hit a single full-response timeout. The `--timeout` option (default 180s) is the max time to wait *between* chunks; increase it if your LLM is slow:

```bash
python3 scripts/perplexica_search.py "Your query" --mode quality --timeout 300
```

## Library / past chats in Perplexica

Searches you run with this skill (via the API) **do not** show up in the Perplexica web UI’s “library of past chats and sources.” Only searches done in the web UI are saved there. The skill still returns the full answer and cited sources in OpenClaw.

## Security

This skill is **local-only**. The script rejects any Perplexica URL that is not `localhost`, `127.0.0.1`, `::1`, or `host.docker.internal`. HTTP redirects are not followed, so the client cannot be sent to a remote host. Do not point `--url` or `config.json` at remote servers; the script will exit with an error.

## Publishing to ClawHub

1. Ensure the skill runs correctly locally (see Quick Start).
2. From the skill directory:

```bash
clawhub login
clawhub publish . --slug perplexica-search --name "Perplexica Search" --version 1.0.0 --changelog "Initial release"
```

If publish fails (e.g. due to `.git` or other files), publish from a clean copy:

```bash
rsync -av --exclude=.git --exclude=__pycache__ ./ /tmp/perplexica-search-pub/
clawhub publish /tmp/perplexica-search-pub --slug perplexica-search --name "Perplexica Search" --version 1.0.0 --changelog "Initial release"
```

Exclusions are listed in [.clawhubignore](.clawhubignore) for reference (ClawHub may not yet honor this file).

## Contributing

Contributions are welcome. Open an issue or pull request on GitHub.

## License

[MIT](LICENSE)

## Links

- [Perplexica](https://github.com/ItzCrazyKns/Perplexica) — local AI-powered search engine
- [OpenClaw](https://open-claw.bot) — AI agent platform
- [ClawHub](https://clawhub.ai) — skill registry
