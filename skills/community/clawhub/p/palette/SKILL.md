---
name: palette
version: "1.0.0"
description: "Create and manage color palettes using color theory algorithms. Use when designing UIs or building brand color systems."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [color, palette, design, ui, css, branding]
---

# Palette — Color Palette Generation & Management Tool

Generate harmonious color palettes using color theory (complementary, analogous, triadic), create random palettes, preview colors in terminal, export to CSS/JSON/SVG, and manage a library of saved palettes. Essential for designers, frontend developers, and anyone working with color systems.

## Prerequisites

- Python 3.8+
- `bash` shell
- Terminal with ANSI color support (for previews)

## Data Storage

All palette data is stored in `~/.palette/data.jsonl` as newline-delimited JSON. Each record contains palette name, colors (hex values), color theory type, and metadata.

Configuration is stored in `~/.palette/config.json`.

## Commands

### `create`
Create a new named palette from a list of hex color values.

```
PALETTE_NAME="ocean-breeze" PALETTE_COLORS="#0077B6,#00B4D8,#90E0EF,#CAF0F8,#023E8A" bash scripts/script.sh create
```

### `random`
Generate a random palette with a specified number of colors (default: 5). Optionally constrain by hue range or saturation.

```
PALETTE_COUNT=5 PALETTE_HUE_MIN=180 PALETTE_HUE_MAX=270 bash scripts/script.sh random
```

### `complementary`
Generate a complementary color palette from a base color. Returns the base color and its complement with optional shades.

```
PALETTE_BASE="#FF6B35" PALETTE_SHADES=3 bash scripts/script.sh complementary
```

### `analogous`
Generate an analogous color palette from a base color. Returns colors adjacent on the color wheel (±30°).

```
PALETTE_BASE="#2EC4B6" PALETTE_COUNT=5 bash scripts/script.sh analogous
```

### `triadic`
Generate a triadic color palette from a base color. Returns three colors equally spaced (120°) on the color wheel.

```
PALETTE_BASE="#E71D36" PALETTE_SHADES=2 bash scripts/script.sh triadic
```

### `export`
Export a palette to various formats: CSS custom properties, JSON, SVG swatches, Tailwind config, or SCSS variables.

```
PALETTE_ID=<id> PALETTE_FORMAT=css PALETTE_OUTPUT=./colors.css bash scripts/script.sh export
```

### `preview`
Display a palette in the terminal using ANSI color blocks. Shows hex values, RGB, and HSL alongside color swatches.

```
PALETTE_ID=<id> bash scripts/script.sh preview
```

### `list`
List all saved palettes with their names, color counts, and creation dates.

```
bash scripts/script.sh list
```

### `save`
Save/bookmark the most recently generated palette with a name and optional tags for organization.

```
PALETTE_NAME="sunset-vibes" PALETTE_TAGS="warm,sunset,gradient" bash scripts/script.sh save
```

### `config`
View or update configuration (default color count, preferred format, terminal color mode).

```
PALETTE_KEY=default_count PALETTE_VALUE=7 bash scripts/script.sh config
```

### `help`
Show usage information and available commands.

```
bash scripts/script.sh help
```

### `version`
Display the current version of the palette skill.

```
bash scripts/script.sh version
```

## Examples

```bash
# Generate a triadic palette from a brand color
PALETTE_BASE="#6C63FF" bash scripts/script.sh triadic

# Save it with a name
PALETTE_NAME="brand-triadic" bash scripts/script.sh save

# Preview in terminal
PALETTE_ID=<id> bash scripts/script.sh preview

# Export as CSS custom properties
PALETTE_ID=<id> PALETTE_FORMAT=css PALETTE_OUTPUT=./brand-colors.css bash scripts/script.sh export
```

## Color Theory Quick Reference

- **Complementary**: Opposite on the color wheel (high contrast)
- **Analogous**: Adjacent colors (harmonious, low contrast)
- **Triadic**: Three equidistant colors (vibrant, balanced)
- **Random**: Algorithmically generated with optional constraints

## Notes

- Colors are stored and processed as hex values internally, converted to RGB/HSL as needed.
- Terminal preview requires a terminal that supports 24-bit (truecolor) ANSI codes.
- Export formats include CSS, JSON, SVG, SCSS, and Tailwind — easily extensible.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
