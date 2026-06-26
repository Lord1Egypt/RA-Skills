<div align="center">

<h1>pixelmsg</h1>

<p><strong>Turn AI responses into beautiful image cards.</strong></p>

<p>
  <img src="https://img.shields.io/badge/node-%3E%3D18-brightgreen?style=flat-square" alt="Node.js" />
  <img src="https://img.shields.io/badge/playwright-1.58-blue?style=flat-square" alt="Playwright" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" alt="License" />
</p>

</div>

[English](README.md) | [中文](README.zh-CN.md)

---

AI agents are stuck in plain text. `pixelmsg` breaks that ceiling — give your agent an HTML template, render it with Playwright, and send a pixel-perfect PNG image to the user. Weather cards, daily reports, GitHub stats, dashboards. Whatever you can design in HTML, you can ship as a rich image message.

## Why pixelmsg

| Without pixelmsg | With pixelmsg |
|---|---|
| "Today's weather: 18°C, partly cloudy, wind NW 3..." | A clean weather card with temperature, forecast, and stats |
| "Trending repos: 1. openclaw/openclaw (9k stars today)..." | A styled GitHub Trending list, ranked and formatted |
| "Your tasks: [x] Q1 report, [ ] product review..." | A visual todo board with progress and priority |

Plain text works. Images stick.

## Demo

<table>
<tr>
<td align="center"><img src="screenshots/weather-default-mobile.png" width="200" /><br /><sub>Weather Card</sub></td>
<td align="center"><img src="screenshots/github-trending-default-mobile.png" width="200" /><br /><sub>GitHub Trending</sub></td>
<td align="center"><img src="screenshots/todolist-default-mobile.png" width="200" /><br /><sub>Todo List</sub></td>
</tr>
</table>

<table>
<tr>
<td align="center"><img src="screenshots/github-stats-default-desktop.png" width="640" /><br /><sub>GitHub Stats — Desktop</sub></td>
</tr>
</table>

## Features

- **Zero build step** — templates are plain HTML with Alpine.js + Tailwind via CDN
- **Playwright rendering** — headless Chromium, 2x retina quality by default
- **Precise cropping** — screenshots the `#app` element, not the whole page
- **Multiple viewports** — mobile (375px), tablet (768px), desktop (1440px), or custom
- **Agent-ready** — `render.sh` outputs an absolute path; compatible platforms send it as an image
- **5 production templates** — weather, GitHub trending, GitHub stats, todo list, and more
- **Composable** — pass URL params to inject dynamic data without modifying HTML

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/your-org/pixelmsg
cd pixelmsg
npm install
npx playwright install chromium

# 2. Render a template
./scripts/render.sh templates/weather.html

# 3. Use the output path
# → /absolute/path/to/screenshots/weather-default-mobile.png
```

## Template Gallery

| Template | Description | Viewport |
|---|---|---|
| `templates/weather.html` | Generic weather card — city, temperature, 3-day forecast | Mobile |
| `templates/shanghai-weather.html` | Live Shanghai weather via Open-Meteo API | Mobile |
| `templates/github-trending.html` | Top 10 GitHub Trending repos with stars and language | Mobile |
| `templates/github-stats.html` | GitHub user profile — contributions, streaks, pinned repos | Desktop |
| `templates/todolist.html` | Categorized todo list with progress overview | Mobile |

All templates use real demo data and render without a build step. Open any `.html` in a browser to preview.

## Usage

### Shell

```bash
# Render with default settings (mobile viewport, ./screenshots output)
./scripts/render.sh templates/weather.html

# Custom output directory
./scripts/render.sh templates/github-stats.html ./output desktop

# Pass URL params to inject data
node screenshot.mjs templates/todolist.html --params category=工作 --viewport mobile
```

### As an Agent Skill

pixelmsg is designed to work as an [OpenClaw](https://github.com/openclaw/openclaw) Agent Skill. The agent reads `SKILL.md` to understand when and how to use it.

```bash
# Install via npx (when published)
npx skills add pixelmsg

# Or point your agent runtime at this directory
SKILL_PATH=/path/to/pixelmsg
```

When the agent calls `render.sh`, it gets back an absolute path. OpenClaw and compatible runtimes automatically attach it as an image message — no extra code needed.

### Write your own template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
  <div id="app" x-data="{ message: 'Hello from pixelmsg' }">
    <div class="w-[390px] p-8 bg-white">
      <p class="text-2xl font-bold text-gray-900" x-text="message"></p>
    </div>
  </div>
</body>
</html>
```

Rules: wrap everything in `#app`, inline your data, avoid external API calls at render time.

## `screenshot.mjs` Options

| Flag | Default | Description |
|---|---|---|
| `--viewport` | `all` | `mobile` / `tablet` / `desktop` / `all` |
| `--width` | — | Custom width (overrides `--viewport`) |
| `--height` | `900` | Viewport height |
| `--selector` | `#app` | Element to crop to |
| `--out` | `./screenshots` | Output directory |
| `--name` | *(from filename)* | Output filename prefix |
| `--params key=val` | — | URL query params injected into the page |
| `--full-page` | off | Capture full page instead of element |
| `--device-scale` | `2` | Device pixel ratio |

## Contributing

Contributions welcome — especially new templates. A good template is:

- Self-contained (no build, no external API calls at render time)
- Fills the `#app` element cleanly at 390px or 800px width
- Uses real demo data, not placeholder text
- Follows the design principles in `SKILL.md`

Open a PR with your template in `templates/` and a screenshot in `screenshots/`.

## License

MIT
