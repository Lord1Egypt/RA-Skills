---
version: "1.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
description: "Generate CSS gradient code, preview gradient combinations, and build gradient palettes using bash and Python. Use when creating linear, radial, or conic gradients for web design."
---

# Gradient — CSS Gradient Generator & Palette Builder

Generate production-ready CSS gradient code for linear, radial, and conic gradients. Create gradient palettes, preview combinations, adjust angles and color stops, and export gradient collections. All gradient definitions are stored locally in JSONL format for reuse and sharing.

## Prerequisites

- Python 3.6+
- Bash 4+

## Data Storage

All gradient records and palettes are stored in `~/.gradient/data.jsonl`. Each record is a JSON object with fields including `id`, `name`, `type` (linear, radial, conic), `css`, `stops`, `angle`, `created_at`, and additional metadata.

## Commands

Run via: `bash scripts/script.sh <command> [options]`

| Command | Description |
|---|---|
| `create` | Create a new gradient with type, colors, angle, and optional name |
| `list` | List all saved gradients with names, types, and CSS preview |
| `get` | Get full details and CSS code for a specific gradient by ID or name |
| `update` | Update an existing gradient's colors, angle, or name |
| `delete` | Remove a gradient from the collection by ID |
| `linear` | Shortcut to generate a linear gradient with angle and color stops |
| `radial` | Shortcut to generate a radial gradient with shape, position, and stops |
| `conic` | Shortcut to generate a conic gradient with start angle and stops |
| `random` | Generate random gradients with optional constraints on hue or type |
| `palette` | Generate a collection of related gradients from a base color |
| `export` | Export gradients as CSS classes, Tailwind config, or SCSS variables |
| `preview` | Generate an HTML preview page for one or all gradients |
| `help` | Show usage information |
| `version` | Print the tool version |

## Usage Examples

```bash
# Create a simple linear gradient
bash scripts/script.sh create --name sunset --type linear --angle 135 --stops "#ff6b6b,#feca57,#48dbfb"

# Shortcut for linear gradient
bash scripts/script.sh linear --angle 90 --stops "#667eea,#764ba2"

# Create a radial gradient
bash scripts/script.sh radial --shape circle --position center --stops "#00d2ff,#3a7bd5"

# Create a conic gradient
bash scripts/script.sh conic --from 0 --stops "#ff0000,#00ff00,#0000ff,#ff0000"

# List all saved gradients
bash scripts/script.sh list

# Get details for a gradient
bash scripts/script.sh get --id abc123

# Update a gradient
bash scripts/script.sh update --id abc123 --angle 180 --stops "#e74c3c,#9b59b6"

# Delete a gradient
bash scripts/script.sh delete --id abc123

# Generate 5 random gradients
bash scripts/script.sh random --count 5

# Generate gradients with warm hues only
bash scripts/script.sh random --count 3 --hue 0-60

# Build a palette from a base color
bash scripts/script.sh palette --color "#3498db" --count 5

# Export as CSS
bash scripts/script.sh export --format css --output gradients.css

# Export as Tailwind config
bash scripts/script.sh export --format tailwind --output tailwind-gradients.js

# Generate HTML preview
bash scripts/script.sh preview --output preview.html
```

## Output Format

`create`, `linear`, `radial`, and `conic` output the CSS gradient string to stdout. `list` returns a formatted table. `get` returns full JSON metadata. `export` writes to the specified file format. `preview` generates a self-contained HTML file.

## Notes

- Gradient types: `linear`, `radial`, `conic`.
- Linear gradients support angles in degrees (0-360) or keywords (`to right`, `to bottom left`).
- Radial gradients support shapes: `circle`, `ellipse`; positions: `center`, `top left`, etc.
- Color stops accept hex (`#rrggbb`), `rgb()`, `hsl()`, or CSS named colors.
- Each stop can include an optional position percentage: `#ff0000:30%`.
- The `palette` command generates harmonious gradient variations from a single base color.
- Export formats: `css` (classes), `tailwind` (JS config), `scss` (variables with mixins).
- Preview HTML includes responsive cards showing each gradient with its CSS code.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
