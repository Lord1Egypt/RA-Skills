---
name: pixelmsg
version: 1.0.0
description: >
  Render HTML templates to pixel-perfect PNG image cards using Playwright and
  send them as rich image messages — instead of plain text. Use this skill
  whenever the user asks for a visual card, image, dashboard, widget, or styled
  message — including weather cards, GitHub stats, todo boards, reports, daily
  digests, announcements, and data summaries. Also trigger when the user says
  things like "给我做个图", "做张卡片", "发图片", "图片形式展示", "用图片显示",
  "rich message", "beautiful card", or anytime a visual representation would be
  more memorable or polished than a plain-text reply. When in doubt, prefer
  generating an image — it almost always delights more than text.
---

# pixelmsg Skill

## When to Use

Any time a visual card beats a plain-text reply:

- Weather forecasts / ambient info cards
- GitHub Trending, repo stats, contribution charts
- Todo / task boards with progress
- Daily / weekly digest or report
- Data dashboards and stat summaries
- Announcements, notifications, styled quotes

---

## Step 1 — Pick a Template or Write Your Own

**Check existing templates first.** The `templates/` directory in this skill's
root has production-ready options. Use one as-is or as a starting point whenever
it fits — don't rewrite from scratch if a template already covers the use case.

| Template | Best for | Style |
|---|---|---|
| `templates/weather.html` | Generic weather card, any city | Glassmorphism |
| `templates/shanghai-weather.html` | Live Shanghai weather (Open-Meteo) | Glassmorphism |
| `templates/github-trending.html` | Top-10 GitHub Trending list | Dark Premium |
| `templates/github-stats.html` | GitHub user profile / stats | Dark Premium |
| `templates/todolist.html` | Categorized todo list with progress | Brand Color |

**Use an existing template when:** the content type maps directly (weather → weather.html, trending repos → github-trending.html).

**Write a new template when:** the content type is unique, or the required data doesn't fit cleanly into an existing template's structure. New templates go in `templates/` and follow the Design System below.

---

## Step 2 — Write or Customize the HTML

Rules for any template:

- Use **Alpine.js** and **Tailwind CSS** via CDN — no build step
- Wrap all content in one root element: `<div id="app">`
- Inline all data — **no external API calls at render time** (hardcode the values)
- Use `<script>` blocks or Alpine `x-data` to inject dynamic content
- Choose width by content density:
  - Compact (weather, quote, stats): **380–480px**
  - Medium (todo, digest): **480–600px**
  - Rich (trending, dashboard): **680–800px**

**Minimal template:**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <style>
    * { font-family: 'Inter', system-ui, sans-serif; box-sizing: border-box; }
    body { margin: 0; padding: 0; background: transparent; }
  </style>
</head>
<body>
  <div id="app" x-data="{ title: 'Hello' }" style="width:480px; padding:32px; background:linear-gradient(135deg,#1565c0,#0d47a1);">
    <h1 style="color:#fff; font-size:24px; font-weight:700;" x-text="title"></h1>
  </div>
</body>
</html>
```

---

## Step 3 — Render to Screenshot

The render script is at `scripts/render.sh` inside this skill's directory.
Determine the skill root from where this SKILL.md lives — it's the same directory.

```bash
# Basic — mobile viewport by default
bash <skill-root>/scripts/render.sh <skill-root>/templates/weather.html

# Custom output directory and viewport
bash <skill-root>/scripts/render.sh <skill-root>/templates/github-stats.html ./output desktop

# For a new template you wrote
bash <skill-root>/scripts/render.sh /path/to/your/template.html
```

`render.sh` screenshots the `#app` element using a `file://` URL (built
internally by `screenshot.mjs`) and prints a single line: the **absolute
path** to the PNG file. The default viewport is `mobile`; pass a third
argument to change it (e.g. `desktop`).

For more control, call `screenshot.mjs` directly:

```bash
node <skill-root>/screenshot.mjs <skill-root>/templates/weather.html \
  --viewport mobile \
  --selector '#app' \
  --out ./screenshots \
  --name weather
```

---

## Step 4 — Deliver the Image

`render.sh` outputs one line — the absolute path to the PNG:

```
/Users/you/Projects/pixelmsg/screenshots/weather-default-mobile.png
```

### Copy to Agent Workspace First

Before returning the path, **copy the file to the agent's workspace directory**.
Many platforms (including OpenClaw on Feishu/Telegram/Signal) only serve files
from a specific workspace path. Accessing the file directly from the project
directory will silently fail — no image appears in chat.

```bash
cp /path/to/screenshot.png ~/.openclaw/workspace/output.png
```

Then return the workspace path.

### Deliver with `MEDIA:` Syntax

In your reply, output the workspace path on its **own line**, prefixed with
`MEDIA:` — **nothing else on that line, no surrounding text**:

```
MEDIA:/Users/you/.openclaw/workspace/output.png
```

⚠️ **Critical rules:**
- `MEDIA:` line must be **completely standalone** — no text before or after it on the same line
- Do **not** mix it with prose like "Here is your image: MEDIA:/path" — that breaks attachment detection
- If you want to add context, put it on a **separate line** before or after:

```
Here is your weather card! 🌤️

MEDIA:/Users/you/.openclaw/workspace/weather.png
```

### Full Delivery Sequence

```bash
# 1. Render
bash <skill-root>/scripts/render.sh <skill-root>/templates/weather.html
# → /Users/you/Projects/pixelmsg/screenshots/weather-default-mobile.png

# 2. Copy to workspace
cp /Users/you/Projects/pixelmsg/screenshots/weather-default-mobile.png \
   ~/.openclaw/workspace/weather-card.png
```

Then in your reply:
```
MEDIA:/Users/you/.openclaw/workspace/weather-card.png
```

---

## Options Reference (`screenshot.mjs`)

| Flag | Default | Description |
|---|---|---|
| `--viewport` | `all` | `mobile` / `tablet` / `desktop` / `all` |
| `--width` | — | Custom width (overrides `--viewport`) |
| `--height` | `900` | Viewport height |
| `--selector` | `#app` | CSS selector of element to capture |
| `--out` | `./screenshots` | Output directory |
| `--name` | (from filename) | Output filename prefix |
| `--params key=val` | — | URL query params passed to the page |
| `--full-page` | off | Capture full page instead of element |
| `--device-scale` | `2` | Device pixel ratio (retina quality) |

---

## Design System

Every card should feel **native-quality** — like a real app screenshot, not a
developer prototype.

### Pick One Style Per Card

| Style | Best for | Background |
|---|---|---|
| **Glassmorphism** | Weather, ambient, sky-themed | Deep blue gradient + frosted panels |
| **Dark Premium** | GitHub, code, tech content | Near-black + subtle borders |
| **Brand Color** | Todo, productivity, notifications | Strong hue gradient + white text |
| **Light Card** | General info, digest, clean data | Light gray bg + white cards |

**Do NOT mix styles.** Pick one and stay consistent.

#### 1. Glassmorphism
```css
background: linear-gradient(160deg, #0f4c81 0%, #1976d2 50%, #4fc3f7 100%);
.panel { backdrop-filter: blur(16px); background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; }
color: #fff; /* primary */ color: rgba(255,255,255,0.65); /* secondary */
```

#### 2. Dark Premium
```css
background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
.panel { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; }
/* Accents: #58a6ff blue · #3fb950 green · #f78166 red · #d2a8ff purple */
color: #e6edf3; /* primary */ color: rgba(230,237,243,0.6); /* secondary */
```

#### 3. Brand Color
```css
background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
.row { background: rgba(255,255,255,0.08); border-radius: 10px; }
color: #fff; /* primary */ color: rgba(255,255,255,0.55); /* secondary */
```

#### 4. Light Card
```css
background: #f5f7fa;
.card { background: #ffffff; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
color: #1a1a2e; /* primary */ color: #6b7280; /* secondary */
```

### Layout Rules

- `body`: `margin: 0; padding: 0; background: transparent;`
- `#app` defines the card — no whitespace outside it
- Internal padding: **28–40px** (scale with card width)
- Spacing scale: **4 / 8 / 12 / 16 / 24 / 32 / 48px** only
- `box-sizing: border-box` on `#app`
- Do NOT use `overflow: hidden` on `#app` — may clip content in screenshot

### Typography

- Font: `'Inter', system-ui, -apple-system, sans-serif`
- Max **3 type sizes** per card
- Scale: `12 / 14 / 16 / 20 / 24 / 32 / 48 / 64px`
- Weight: **300 / 400 / 600 / 700** only
- No drop-shadow on text

### Icons

Always use **inline SVG**. Never emoji, icon fonts, or external URLs.

```html
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- 2–4 paths max for weather icons -->
</svg>
```

### Decoration

- Background decorative shapes: `opacity: 0.08–0.15`, `pointer-events: none`
- Border-radius: buttons 8px · panels 12–16px · chips 99px
- Max 2 dominant colors + neutrals
- No outer glow, no rainbow gradients, no neon
