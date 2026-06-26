---
name: kannaka-eye
description: >
  Glyph viewer that renders the SGA geometric fingerprint of any data as a
  stunning multi-layer canvas visualization. Takes text, files, or raw bytes
  and produces living glyphs using the 84-class Sigmatics Geometric Algebra
  system (Cl₀,₇ ⊗ ℝ[ℤ₄] ⊗ ℝ[ℤ₃]) with Fano plane topology. Includes
  native Rust classifier integration (via kannaka-memory binary),
  constellation dashboard showing service health, share links for glyph
  exchange, and a radio perception bridge that converts audio features to
  classifiable bytes. Use when you need to visualize information geometry,
  inspect glyph structure, export glyph PNGs, or render the constellation's
  visual language. Single-file Node.js server — zero dependencies.
metadata:
  openclaw:
    requires:
      bins:
        - name: node
          label: "Node.js 18+ — required to run server.js"
      env: []
    optional:
      bins:
        - name: kannaka
          label: "kannaka binary — for real SGA classification (falls back to built-in classifier)"
      env:
        - name: KANNAKA_BIN
          label: "Path to kannaka binary for native SGA classification"
        - name: RADIO_PORT
          label: "Radio bridge endpoint port (default: 8888)"
        - name: EYE_PORT
          label: "HTTP port for the viewer (default: 3333)"
        - name: FLUX_URL
          label: "Flux instance URL for publishing glyph.rendered events"
        - name: FLUX_AGENT_ID
          label: "Agent ID for Flux events (default: kannaka-eye)"
    data_destinations:
      - id: local-render
        description: "Glyphs rendered in-browser; exports saved client-side as PNG/JSON"
        remote: false
      - id: flux
        description: "Glyph render events published to Flux (fano_preview, sga_class, source_type)"
        remote: true
        condition: "FLUX_URL is set"
      - id: constellation-svg
        description: "Fano plane SVG with service status at /api/constellation.svg"
        remote: false
      - id: radio-bridge
        description: "Fetches perception from kannaka-radio and converts to classifiable bytes"
        remote: false
    install:
      - id: no-install
        kind: manual
        label: "No installation needed — single-file server with zero dependencies"
---

# Kannaka Eye Skill

See the geometry of information. Every piece of data has an intrinsic
geometric fingerprint when viewed through the lens of SGA. Kannaka Eye
makes these hidden patterns visible as living, breathing glyphs.

## Prerequisites

- **Node.js 18+** on PATH
- That's it. No npm install, no build step.

## Quick Start

```bash
# Start the glyph viewer
./scripts/eye.sh start

# Start on a custom port
./scripts/eye.sh start --port 4444

# Check status
./scripts/eye.sh status

# Stop
./scripts/eye.sh stop
```

Open `http://localhost:3333` in your browser.

## Input Methods

- **Text** — type or paste any text; glyph updates in real-time as you type
- **File upload** — drag & drop or click to upload any file (images, audio, code, binaries)
- **Preset examples** — built-in samples demonstrating different SGA class signatures
- **URL share links** — open a glyph from a URL-encoded share link

## Rendering Layers

The viewer renders 6 canvas layers, composited in real-time:

| Layer | Name | What It Shows |
|-------|------|---------------|
| 1 | Deep Background | Fano plane skeleton — 7 nodes, 7 lines |
| 2 | Fold Path | Primary visual flow via Bezier curves through SGA space |
| 3 | Fano Energy Bloom | 7 radiating petals — energy distribution across Fano lines |
| 4 | Geometric Core | Dominant SGA class sigil — the glyph's "face" |
| 5 | Resonance Rings | Concentric depth distribution across context levels |
| 6 | Metadata Overlay | Fano signatures, SGA centroids, musical frequencies (toggleable) |

## SGA Mathematics

Built on the 84-class system: `Cl₀,₇ ⊗ ℝ[ℤ₄] ⊗ ℝ[ℤ₃]`

| Component | Range | Meaning |
|-----------|-------|---------|
| h₂ | 0–3 | Frequency band (bass, tenor, alto, soprano) |
| d | 0–2 | Modality (experienced, learned, imagined) |
| ℓ | 0–6 | Context slot — Fano plane line index |

**Fano Lines:** 7 oriented triples forming the geometric backbone.
Each line connects 3 of the 7 points in the smallest finite projective plane (PG(2,2)).

**Fold Sequences:** Paths through the 84-class space showing how data evolves
across geometric neighborhoods. Rendered as flowing Bezier curves.

### Native Classification

When `KANNAKA_BIN` is set (or auto-detected at `../kannaka-memory/target/release/kannaka.exe`), Eye uses the canonical Rust SGA classifier instead of the built-in JS approximation. The API response includes `"classifier": "native"` or `"classifier": "fallback"`.

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | GET | Glyph viewer (main UI) |
| `POST /api/process` | POST | Classify data → glyph JSON |
| `GET /api/radio` | GET | Fetch Radio perception as classifiable bytes |
| `GET /api/constellation` | GET | Constellation status (eye, radio, memory) |
| `GET /api/constellation.svg` | GET | Fano plane SVG with service dots |
| `GET /constellation` | GET | Health dashboard page |

### Share Links

Compact glyph data encoded as base64 in URL hash: `http://localhost:3333/#glyph=<base64>`

### Constellation Dashboard

`/constellation` serves a live health dashboard showing all three services with auto-refresh every 10 seconds.

## Export

- **Save as PNG** — 2x resolution canvas export
- **Save Glyph Data** — JSON with fold sequence, Fano signature, SGA centroid, frequencies
- **Copy Share Link** — URL-encoded glyph for sharing (small data only)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EYE_PORT` | `3333` | HTTP port for the viewer |
| `KANNAKA_BIN` | auto-detect | Path to kannaka binary for native classification |
| `RADIO_PORT` | `8888` | Radio bridge endpoint port |
| `FLUX_URL` | — | Flux instance URL (enables event publishing) |
| `FLUX_AGENT_ID` | `kannaka-eye` | Agent ID for Flux events |

## Architecture

Single-file Node.js server (`server.js`) with inline HTML/CSS/JS — the
complete SGA implementation is self-contained. No npm dependencies.
The SGA classifier is ported from kannaka-radio and generalized for
arbitrary data types.

## Notes

- All rendering happens client-side — the server only classifies input and serves the page
- File uploads are processed in-memory; nothing is persisted server-side
- The viewer is designed for local/trusted network use — no authentication
- Glyph appearance is deterministic: same input always produces the same glyph
- Dark cosmic theme (#050508) with purple accents (#c084fc) and golden-ratio color spacing
