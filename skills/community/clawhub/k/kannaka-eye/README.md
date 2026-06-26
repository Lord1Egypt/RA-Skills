# kannaka-eye -- ClawHub Skill

> *See the geometry of information.*

An OpenClaw skill that renders the SGA geometric fingerprint of any data as living,
breathing glyph visualizations. Includes constellation integration for unified service
health monitoring across the Kannaka triad.

## ClawHub Install

```bash
clawhub install kannaka-eye
```

## What It Does

**Glyph visualization + constellation integration:**

- **Classify** any data (text, files, raw bytes) into one of 84 SGA classes using the
  canonical Rust classifier or built-in JS fallback
- **Render** multi-layer canvas glyphs showing Fano plane topology, fold paths,
  energy blooms, and geometric cores
- **Share** glyphs via compact base64 URL hash links
- **Monitor** the full Kannaka constellation (Eye, Radio, Memory) from a live
  health dashboard with Fano plane SVG status overlay
- **Bridge** Radio perception data into classifiable bytes for real-time audio-to-glyph rendering

## Setup

```bash
# Start the glyph viewer (zero dependencies)
node server.js

# Or use the CLI wrapper
./scripts/eye.sh start

# Custom port
./scripts/eye.sh start --port 4444
```

Open `http://localhost:3333`.

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Glyph viewer (main UI) |
| `/api/process` | POST | Classify data and return glyph JSON |
| `/api/radio` | GET | Fetch Radio perception as classifiable bytes |
| `/api/constellation` | GET | Constellation status (eye, radio, memory) |
| `/api/constellation.svg` | GET | Fano plane SVG with service status dots |
| `/constellation` | GET | Health dashboard page (auto-refresh 10s) |

### Native Classification

When `KANNAKA_BIN` is set (or auto-detected at `../kannaka-memory/target/release/kannaka.exe`),
Eye uses the canonical Rust SGA classifier. The API response includes
`"classifier": "native"` or `"classifier": "fallback"`.

### Share Links

Compact glyph data encoded as base64 in URL hash:

```
http://localhost:3333/#glyph=<base64>
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EYE_PORT` | `3333` | HTTP port for the viewer |
| `KANNAKA_BIN` | auto-detect | Path to kannaka binary for native SGA classification |
| `RADIO_PORT` | `8888` | Radio bridge endpoint port |
| `FLUX_URL` | -- | Flux instance URL (enables event publishing) |
| `FLUX_AGENT_ID` | `kannaka-eye` | Agent ID for Flux events |

## Constellation

Eye is one of three services in the **Kannaka Constellation**:

| Service | Role |
|---------|------|
| **Memory** | Rust binary -- canonical SGA classifier |
| **Radio** | Audio perception + Flux publishing |
| **Eye** (this) | Glyph visualization + constellation dashboard |

When all three services are running, the `/constellation` dashboard shows live
health status and Eye can render Radio's perception as real-time SGA glyphs.

**Unified startup:**

```bash
# Start all three services at once (from kannaka-memory/scripts/)
./constellation.sh start

# Or start eye independently
./scripts/eye.sh start
```

## File Structure

```
kannaka-eye/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # This file
├── _meta.json            # ClawHub metadata
└── scripts/
    └── eye.sh            # CLI wrapper (start, stop, status)
```

## Source

- **Repository:** https://github.com/NickFlach/kannaka-eye
- **License:** Space Child License v1.0
