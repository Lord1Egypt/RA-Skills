# OpenClaw Usage Dashboard

A zero-dependency Node.js dashboard that reads your OpenClaw session logs and visualises token usage, model activity, and system health in real time. Runs entirely on your machine — no data ever leaves localhost.

![Dashboard](references/screenshot.png)

## Features

- **Timeline chart** — token usage over time with Models / Agents / Both filter toggle
- **Model cards** — token counts and request counts per model, sorted by most used
- **Agent activity** — breakdown of which agent made how many requests
- **Session heatmap** — activity distribution by hour of day
- **Token efficiency** — cache hit ratio and average prompt size
- **System health strip** — RAM (VM-aware on macOS), disk, uptime, and OpenClaw version
- **Time period selector** — Hour / Day / Week / Month / Year (keyboard shortcuts `1`–`5`)
- **Dark theme** — `#0a0e1a` background with 🦞 favicon
- **Localhost-only** — reads `~/.openclaw/agents/*/sessions/*.jsonl`; no network calls

## Quick Start

```bash
node server.js
```

Open **http://localhost:7842** in your browser.

### Custom port

```bash
node server.js --port 8080
```

## Install via ClawHub

```bash
openclaw skills install openclaw-usage-dashboard
```

## Requirements

- Node.js 18+
- No `npm install` needed — zero external dependencies

## Platform Support

| Platform | Supported |
|----------|-----------|
| macOS    | ✅        |
| Linux    | ✅        |
| Windows  | ✅        |

## Security

`server.js` uses `child_process.execSync` for **system health only** — fixed commands like `vm_stat`, `df`, `powershell` (disk/RAM info) and `openclaw version`. No user input is ever interpolated into a shell command. All calls have hard timeouts and try/catch wrappers. Data never leaves localhost.

## Roadmap

- Rate limits tracking — [GitHub issue #55934](https://github.com/openclaw/openclaw/issues/55934)

## License

MIT
