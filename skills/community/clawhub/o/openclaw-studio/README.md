<p align="center">
  <img src="./assets/github-hero.svg" alt="OpenClaw Studio hero banner" width="100%" />
</p>

# OpenClaw Studio

**A polished local operations dashboard for OpenClaw, with lovable robots, clear live visualization, and controls that feel professional instead of improvised.**

OpenClaw Studio turns one active OpenClaw worker into something you can actually supervise at a glance. It blends expressive robot identity, real-time status, efficiency tracking, chat access, and optional recovery controls into a single page that looks good enough for GitHub, ClawHub, and your own desktop.

## Why it feels different

- Cute robots on the surface, serious operational visibility underneath
- Live status, score, activity freshness, and trend signals in one glance
- A local-first dashboard that does not depend on a cloud backend
- A presentation layer strong enough for public release pages and listings
- Enough personality to make the product memorable without making it childish

## What you can do

- See whether your OpenClaw agent is working, thinking, idle, overdue, stalled, or down
- Watch efficiency and token-related signals move over time
- Nudge the agent directly from the dashboard
- Enable optional auto-heal and watchdog helpers for long silent periods
- Customize robot styles, headwear, hands, wings, themes, and background effects

## Cute Robot Showcase

<p align="center">
  <img src="./assets/robot-showcase.svg" alt="Cute OpenClaw robot styles" width="100%" />
</p>

The robot layer is not decorative filler. It gives the dashboard a recognizable face, makes state changes easier to notice, and gives GitHub and ClawHub a stronger first impression than a plain control panel screenshot.

## Visual Dashboard Showcase

<p align="center">
  <img src="./assets/visualization-showcase.svg" alt="OpenClaw Studio metrics and visualization showcase" width="100%" />
</p>

The visual side is designed to feel clean and readable: a clear hero area, dashboard cards with hierarchy, trend views that make progress legible, and enough atmosphere to feel premium without becoming noisy.

## Quick Start

Install and run locally:

```bash
python3 -m pip install -r requirements.txt
cp config.example.json config.json
./run_monitor.sh
```

Open the dashboard at `http://127.0.0.1:18991/`.

If you want it in the background instead, use:

```bash
./start_bg.sh
```

## Project Scope

- Single-agent local dashboard for OpenClaw
- Live status, chat panel, trend cards, and control actions
- macOS-friendly launch flow and helper scripts
- Optional watchdog and auto-heal support
- Publish-ready copy structure for GitHub and ClawHub

## Why it works for release pages

GitHub and ClawHub need more than a working tool. They need a product story, a recognizable face, and visuals that communicate value quickly. This repository now includes:

- a hero banner for README and social previews
- a robot lineup render for the cute side of the product
- a visualization render for the professional side
- structured release copy and screenshot planning documents

## Key Files

- `index.html`
- `server.py`
- `monitor_config.py`
- `config.example.json`
- `MARKET_LISTING.md`
- `GITHUB_RELEASE_COPY.md`
- `SCREENSHOT_PLAN.md`

## Release Direction

This repository is being prepared for:

1. GitHub publication
2. ClawHub listing
3. future multi-agent expansion
