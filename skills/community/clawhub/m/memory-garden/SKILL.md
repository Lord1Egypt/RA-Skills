---
name: memory-garden
version: 1.0.0
description: N-count validated knowledge for AI agents. Patterns that prove themselves through repeated use. Local-first, community-ready.
homepage: https://github.com/live-neon/memory-garden
repository: live-neon/memory-garden
tags:
  - knowledge-management
  - ai-memory
  - mcp
  - pattern-extraction
  - local-first
  - community-knowledge
  - validated-patterns
  - n-count
disable-model-invocation: false
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["mg-daemon"]},"install":[  {"kind":"download","os":["darwin"],"arch":"arm64","url":"https://github.com/live-neon/memory-garden/releases/download/v1.0.0/mg-daemon-darwin-arm64","sha256":"02661482d766b504d0558b190a0e65d7dc569e9ebd0a5e7d71aaf3fce53a2962","bins":["mg-daemon"],"label":"Memory Garden daemon (macOS)"},  {"kind":"download","os":["linux"],"arch":"amd64","url":"https://github.com/live-neon/memory-garden/releases/download/v1.0.0/mg-daemon-linux-amd64","sha256":"e7857b34bef436ab434d5244a6d5f3dd95883dcd47f700c3053a2854836cf4f2","bins":["mg-daemon"],"label":"Memory Garden daemon (Linux)"}]}}
---

# Memory Garden

**Stop answering the same questions twice.**

Memory Garden learns what works in your domain and brings validated knowledge to every conversation. Unlike simple memory tools, patterns here must *prove themselves* through repeated successful use (N-count convergence).

Community-validated. Local-first. You control what stays.

## Why Memory Garden?

| Problem | Solution |
|---------|----------|
| AI forgets what worked yesterday | Patterns persist and surface when relevant |
| No way to know if advice is reliable | N-count shows how many times a pattern proved useful |
| Memory silos per project | Federated curation lets you subscribe to trusted sources |
| Privacy concerns with cloud memory | Local-first: nothing leaves your machine unless you opt-in |

## Features

| Feature | Default | Description |
|---------|---------|-------------|
| **Search** | ON | Augment queries with validated patterns |
| **Extraction** | OFF | Extract patterns from conversations (opt-in) |
| **Validation** | ON | Record when patterns help (increments N-count) |
| **Sync** | OFF | P2P pattern synchronization (opt-in) |

## How N-Count Works

```
N=1: Pattern recorded (observation)
N=2: Pattern confirmed (recurring)
N=3+: Pattern validated (reliable knowledge)
```

Higher N-count = more trustworthy. Patterns that keep helping rise to the top.

## Quick Start

The skill automatically manages the Memory Garden daemon:
- Starts daemon if not running
- Uses port 18790 (or next available)
- Health checks at `/health`

```bash
# Verify installation
clawhub inspect memory-garden

# Check daemon status
curl http://127.0.0.1:18790/health
```

## Configuration

Set via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MG_DAEMON_URL` | `http://127.0.0.1:18790` | Daemon URL (if external) |
| `MG_EXTRACTION_ENABLED` | `false` | Enable pattern extraction |
| `MG_EXTRACTION_CONFIRM` | `true` | Require human confirmation |
| `MG_SYNC_ENABLED` | `false` | Enable P2P sync |
| `MG_SEARCH_LIMIT` | `8` | Default search result limit |

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| macOS Apple Silicon | ✅ Supported | arm64 |
| macOS Intel | ✅ Supported | amd64 |
| Linux x86_64 (glibc) | ✅ Supported | amd64, requires glibc 2.31+ (Ubuntu 20.04+, Debian 11+) |
| Linux ARM64 | ❌ Not supported | libSQL limitation - [vote for ARM64 support](https://github.com/live-neon/memory-garden/issues/1) |
| Windows | ⚠️ WSL2 required | Native Windows not supported |
| Alpine/musl | ❌ Not supported | Requires glibc (libSQL dependency)

## Data Handling

Your patterns are your intellectual property. Local-first means your learning stays yours until you choose to share.

- Patterns stored locally in `~/.memory-garden/`
- No data sent externally unless sync explicitly enabled
- Extraction requires opt-in (`MG_EXTRACTION_ENABLED=true`)
- All operations logged to `~/.memory-garden/logs/`

## Security

- Daemon listens on localhost only (127.0.0.1)
- No outbound network by default
- Trust-gated tool access
- HMAC-SHA256 webhook verification (for CI integration)
- MIT License

## Tools

| Tool | Description | Default |
|------|-------------|---------|
| `search_patterns` | Find validated patterns for your query | Enabled |
| `plant_pattern` | Record a new observation | Requires extraction |
| `validate_pattern` | Confirm a pattern helped (increments N-count) | Enabled |
| `get_category_effectiveness` | View fix success rates by category | Enabled |

## Integrations

### Continuous AI Improver

Track which fix patterns actually get merged:

```bash
# Enable webhook endpoint
MG_WEBHOOK_ENABLED=true mg-daemon --serve

# Configure GitHub webhook to POST to /webhooks/github
```

See [Continuous Improver Guide](https://github.com/live-neon/memory-garden/blob/main/docs/guides/continuous-improver-integration.md)

## Troubleshooting

### Daemon won't start

1. Check if another instance is running: `lsof -i :18790`
2. Check logs: `~/.memory-garden/logs/daemon.log`
3. Try manual start: `mg-daemon --serve --addr 127.0.0.1:18790`

### Health check fails

1. Verify daemon is running: `curl http://127.0.0.1:18790/health`
2. Check port availability
3. Review daemon logs

### Need help?

Open an issue: https://github.com/live-neon/memory-garden/issues

## Learn More

- [OpenClaw Quick Start](https://github.com/live-neon/memory-garden/blob/main/docs/guides/openclaw-quickstart.md)
- [P2P Sync Setup](https://github.com/live-neon/memory-garden/blob/main/docs/guides/p2p-sync-setup.md) - Share patterns between machines
- [Safe Defaults](https://github.com/live-neon/memory-garden/blob/main/docs/standards/safe-defaults.md)
- [Architecture](https://github.com/live-neon/memory-garden/blob/main/docs/architecture/daemon-lifecycle.md)
