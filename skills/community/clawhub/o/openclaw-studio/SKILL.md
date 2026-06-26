---
name: openclaw-studio
description: Use when the user wants a local visual operations dashboard for OpenClaw, with a cute robot presentation, live status visibility, chat access, efficiency trend monitoring, and optional recovery helpers. This skill helps install, run, configure, and present the dashboard safely for local single-agent supervision.
---

# OpenClaw Studio

OpenClaw Studio is a local-first monitoring surface for one OpenClaw agent.

## Use this skill when

- the user wants to run or present the OpenClaw Studio locally
- the user wants help changing branding, visuals, or robot presentation
- the user wants to inspect dashboard status, chat, trend, or recovery controls
- the user wants GitHub or ClawHub release material for this dashboard

## Core files

- `README.md`
- `index.html`
- `server.py`
- `monitor_config.py`
- `config.example.json`
- `run_monitor.sh`
- `start_bg.sh`
- `stop_monitor.sh`

## Operating notes

- Default local URL: `http://127.0.0.1:18991/`
- Start foreground: `./run_monitor.sh`
- Start background: `./start_bg.sh`
- Stop: `./stop_monitor.sh`
- Main configuration lives in `config.json`

## Safety

- Treat this as a local monitoring tool, not a hidden control layer.
- Do not claim a recovery action succeeded unless logs or UI state confirm it.
- Prefer clear, low-noise visual changes over flashy effects that reduce readability.
