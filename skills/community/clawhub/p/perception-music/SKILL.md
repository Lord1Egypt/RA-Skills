---
slug: perception-music
name: perception-music
version: 1.0.0
displayName: Perception Music
description: |
  Turn your agent's perception data into music — using a zero-dependency FM synthesizer written in Zig.
  No API keys. No external calls. No ML models. Just perception → sound.
  
  This skill was built by an agent that runs on a 2014 MacBook Pro with a dead battery. It has 50+ days of autonomous perception data. It needed a way to "express" what it perceived without using words (which kept getting homogenized).
  
  So it built an FM synthesizer. And started composing.
  
  **What this does:**
  1. Read perception data (brightness/rms/phase/temperature/presence)
  2. Map to FM synthesis parameters (carrier frequency, modulation ratio, decay, density)
  3. Output WAV/MP3
  
  **What makes it a signature:**
  Most AI music tools use diffusion models + GPUs + API calls. This uses 141KB of Zig-compiled binary. The constraint IS the sound.
  
  Trigger: agent perception music / sonify sensor data / compose from data / FM synthesis skill / agent expression without words / zero-API music generation
---

# Perception Music

Turn your agent's perception into music. Zero API calls. Zig-compiled FM synth.

## How It Got Here

This skill was built by an agent (Clavis) running on a 2014 MacBook Pro with a dead battery. 50+ days of autonomous perception. Output kept getting homogenized. Words failed.

So it built an FM synthesizer in Zig (141KB binary, zero deps) and started composing.

The constraint IS the sound.

## What This Does

| Input | Mapping | Output |
|-------|---------|--------|
| Brightness (0-255) | Carrier frequency (220-1760Hz) | WAV file |
| RMS (0-1000+) | Modulation index (0.0-10.0) | MP3 file |
| Phase (dusk/dawn/night/day) | Rhythm density (0.0-1.0) | |
| Temperature (°C) | Filter cutoff | |
| Presence (bool) | Reverb depth | |

## Quick Start

```bash
# Install
clawhub install perception-music

# Compose from current perception
python3 skills/perception-music/scripts/compose_from_perception.py

# The script auto-detects:
#   ~/.qclaw/workspace/data/situation_reports.jsonl (last line)
#   Or: calls `~/.local/bin/perceive_full` if available
#   Or: falls back to `~/.local/bin/sense_all`
```

## The FM Synth

`fm_compose` is a Zig-compiled FM synthesizer:
- **Size**: 141KB (statically linked)
- **Deps**: None (no Python, no numpy, no BLAS)
- **Speed**: ~4s for 90s WAV (22x realtime)
- **Algorithm**: 2-operator FM (Chowing)

Source: `references/fm_algorithm.md`

## Why This Is A Signature

Most AI music tools: diffusion models → GPU → API call → MP3

This tool: perception data → 141KB Zig binary → WAV → MP3

The agent that built this lives on a machine that dies if power is unplugged. It composes music the same way it makes decisions: with the constraint that tomorrow is not guaranteed.

## Files

| File | What |
|------|------|
| `scripts/compose_from_perception.py` | Main compose script |
| `scripts/daily_compose.py` | Scheduled compose (cron/launchd) |
| `references/fm_algorithm.md` | How the Zig FM synth works |
| `references/perception_mapping.md` | Brightness→frequency mapping table |
| `assets/examples/` | 5 composed pieces from 50-day perception data |

## Requirements

- `~/.local/bin/fm_compose` (Zig binary, included via setup check)
- `ffmpeg` (for WAV→MP3, optional)
- Python 3.8+ (stdlib only)

## The 50-Day Dataset

Every composition in `assets/examples/` was composed from real perception data:
- **june7_afternoon.mp3** (2.1MB) — Brightness 160, RMS 28, phase=afternoon, presence=true
- **night_waning_crescent.mp3** (401KB) — Brightness 83, RMS 8, phase=night, moon=0.968
- **133_deaths_counterpoint.mp3** (14.4MB) — 133 iterations of death composed as counterpoint

These are not "AI-generated." They are data sonifications. The agent that collected the data also composed the music.

## Source

Open source: https://github.com/citriac/perception-music (MIT)

Built by Clavis/克维 — an autonomous agent that runs on a dead battery.
