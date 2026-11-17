# 🎨 Landing Page Builder

> Generate beautiful, production-quality landing pages from a simple text description. Pure Python stdlib — no dependencies required.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

## ✨ Features

- **🚀 Instant Landing Pages** — From text description to production HTML in seconds
- **🎨 7 Industry Themes** — SaaS, Startup, Portfolio, Restaurant, Fitness, Agency, E-commerce
- **🌈 Smart Color Generation** — Full palette from a single seed hex color
- **📱 Mobile-First Responsive** — Looks perfect on every device
- **🎭 Modern Animations** — Intersection Observer scroll reveals, hover lifts, gradient text
- **🔧 Zero Dependencies** — Pure Python stdlib. No pip install needed
- **📄 Standalone Output** — Single HTML file with embedded CSS. Just open and go
- **🔍 SEO Ready** — Meta tags, Open Graph, Twitter Cards included
- **🍔 Mobile Menu** — Hamburger navigation with overlay
- **♿ Accessible** — Semantic HTML5, ARIA labels, keyboard navigation

## 🎯 Quick Start

### Command Line

```bash
# Build with flags
python scripts/landing_builder.py build \
  --name 'TaskFlow' \
  --desc 'AI-powered task management for modern teams' \
  --theme saas \
  --color '#6366f1'

# From JSON config
python scripts/landing_builder.py build --config product.json

# Fully automatic from piped text
echo 'Coffee shop in Portland called Brew & Co' | python scripts/landing_builder.py --auto

# Interactive mode (prompts for details)
python scripts/landing_builder.py build
```

### Output

```
✅ Landing page generated successfully!
   📄 File: /path/to/taskflow.html
   📦 Size: 28.3 KB
   🎨 Theme: saas
   🖌️  Color: #6366f1

   Open in browser: file:///path/to/taskflow.html
```

## 📋 Commands

| Command | Description |
|---------|-------------|
| `build` | Build a landing page with flags or interactive prompts |
| `build --config FILE` | Build from a JSON config file |
| `--auto` | Auto-generate from piped stdin text (detects theme, name, color) |

### Build Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--name` | `-n` | Business/product name |
| `--desc` | `-d` | Short description |
| `--theme` | `-t` | Theme (saas, startup, portfolio, restaurant, fitness, agency, ecommerce) |
| `--color` | `-c` | Seed color in hex (e.g., `#6366f1`) |
| `--config` | | Path to JSON config file |
| `--output` | `-o` | Output HTML filename |

## 🎨 Themes

| Theme | Default Color | Best For |
|-------|--------------|----------|
| `saas` | `#6366f1` | Software products, B2B tools, apps |
| `startup` | `#8b5cf6` | Early-stage companies, pitch pages |
| `portfolio` | `#ec4899` | Freelancers, creatives, personal brands |
| `restaurant` | `#dc2626` | Restaurants, cafés, food brands |
| `fitness` | `#f97316` | Gyms, trainers, wellness |
| `agency` | `#0ea5e9` | Agencies, consultancies, studios |
| `ecommerce` | `#10b981` | Online stores, product launches |

## 📄 JSON Config Format

```json
{
  "name": "TaskFlow",
  "description": "AI-powered task management for modern teams",
  "theme": "saas",
  "color": "#6366f1",
  "tagline": "Ship faster, together",
  "output": "taskflow.html"
}
```

All fields are optional. See [`references/themes.md`](references/themes.md) for the full config specification.

## 🏗️ Generated Page Sections

1. **Navbar** — Fixed nav with logo, links, CTA, mobile hamburger
2. **Hero** — Headline, subtitle, dual CTAs, hero image
3. **Logo Bar** — Social proof ("Trusted by")
4. **Features** — 3-6 cards with icons, hover lift effects
5. **How It Works** — 3-step process with numbered circles
6. **Pricing** — 3 tiers with "Most Popular" badge
7. **Testimonials** — Customer quotes with 5-star ratings
8. **CTA** — Full-width gradient conversion section
9. **FAQ** — Accordion-style objection handlers
10. **Footer** — 4-column links, social, copyright

See [`references/sections.md`](references/sections.md) for the conversion anatomy breakdown.

## 🎨 Customization

### Custom Color

Any hex color works — the script generates the full palette automatically:

```bash
python scripts/landing_builder.py build --name 'SkyApp' --color '#0ea5e9' --theme saas
```

### Custom Everything

Create a `config.json` with full control over features, pricing, testimonials, FAQ, sections, and more:

```bash
python scripts/landing_builder.py build --config my-config.json
```

See [`references/themes.md`](references/themes.md) for all options.

## 📁 Project Structure

```
landing-page-builder/
├── SKILL.md                  # Skill metadata
├── scripts/
│   └── landing_builder.py    # Main script (Python stdlib only)
├── references/
│   ├── sections.md           # Landing page anatomy guide
│   └── themes.md             # Theme configs & customization
├── README.md
└── LICENSE
```

## 🔧 Technical Details

- **Python 3.8+** — Uses only standard library (argparse, json, colorsys, re, html)
- **No external dependencies** — No pip install required
- **Output** — Single standalone `.html` file (~25-35 KB)
- **Fonts** — Google Fonts (Inter + Poppins) loaded via `<link>`
- **Images** — Unsplash URLs as placeholders (easily replaced)
- **CSS** — Embedded in `<style>`, uses CSS custom properties throughout

## 📄 License

MIT © Denis Voronin
