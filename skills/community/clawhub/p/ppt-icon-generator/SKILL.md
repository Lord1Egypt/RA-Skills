---
name: ppt-icon-generator
description: |
  Generate or search PNG transparent icons for PowerPoint presentations.
  Use when: (1) Need icons for PPT slides, (2) Want custom icons from text prompts,
  (3) Need transparent PNG icons in specific styles (flat, line, filled, etc.).
  Supports icon search from Iconify API, SVG to PNG conversion, and AI-style icon generation.
---

# PPT Icon Generator

Generate professional PNG transparent icons for your PowerPoint presentations.

## Features

- 🔍 **Search Icons**: Search 200,000+ icons from Iconify API
- 🎨 **Generate Icons**: Create custom icons from text prompts using AI/Copilot
- 🖼️ **SVG to PNG**: Convert SVG icons to transparent PNG
- 📐 **Custom Size**: Generate icons in any size (default: 512x512)
- 🎯 **Multiple Styles**: Flat, line, filled, outline, duotone

## Quick Start

### Search and Download Icon

```bash
# Search for "chart" icons
python3 scripts/icon_search.py --query "chart" --limit 5

# Download first result as PNG
python3 scripts/icon_search.py --query "chart" --download --output ~/workspace/chart_icon.png
```

### Generate Custom Icon

```bash
# Generate a "rocket" icon with gradient style
python3 scripts/icon_generate.py --prompt "rocket launching with fire trail" --style gradient --output rocket.png

# Generate line-style icon
python3 scripts/icon_generate.py --prompt "data analytics dashboard" --style line --size 256
```

## Usage Methods

### Method 1: Search Existing Icons (Recommended)

Search from 200,000+ open source icons:

```javascript
// Search icons
{
  "tool": "exec",
  "command": "python3 /root/.openclaw/skills/ppt-icon-generator/scripts/icon_search.py --query 'analytics' --limit 10"
}

// Download specific icon
{
  "tool": "exec",
  "command": "python3 /root/.openclaw/skills/ppt-icon-generator/scripts/icon_search.py --query 'chart-line' --download --output /root/.openclaw/workspace/chart.png"
}
```

### Method 2: Generate with AI/Canvas

Use browser automation to generate icons via AI tools:

```javascript
// Use Copilot/ChatGPT to generate icon
{
  "tool": "browser",
  "action": "open",
  "targetUrl": "https://copilot.microsoft.com"
}

// Prompt example:
// "Generate a minimalist icon of [DESCRIPTION], transparent background, 
//  suitable for PowerPoint, flat design style, single color"
```

### Method 3: Create with Python (Pillow)

Generate simple geometric icons:

```bash
# Create basic shapes with transparency
python3 scripts/icon_generate.py --shape circle --color "#FF6B6B" --output icon.png

# Create text-based icon
python3 scripts/icon_generate.py --text "AI" --bg-gradient "#667eea,#764ba2" --output ai_icon.png
```

## Icon Search Examples

### Common PPT Icon Categories

```bash
# Business & Analytics
python3 scripts/icon_search.py --query "chart-bar" --download
python3 scripts/icon_search.py --query "trending-up" --download
python3 scripts/icon_search.py --query "pie-chart" --download

# Technology
python3 scripts/icon_search.py --query "cpu" --download
python3 scripts/icon_search.py --query "cloud" --download
python3 scripts/icon_search.py --query "database" --download

# Communication
python3 scripts/icon_search.py --query "message" --download
python3 scripts/icon_search.py --query "email" --download
python3 scripts/icon_search.py --query "share" --download

# UI Elements
python3 scripts/icon_search.py --query "check-circle" --download
python3 scripts/icon_search.py --query "alert" --download
python3 scripts/icon_search.py --query "settings" --download
```

## Icon Generation Examples

### From Text Prompt

```bash
# Generate abstract tech icon
python3 scripts/icon_generate.py \
  --prompt "neural network nodes connected" \
  --style flat \
  --color "#4ECDC4" \
  --output neural_icon.png

# Generate arrow icon
python3 scripts/icon_generate.py \
  --prompt "arrow pointing right with curved path" \
  --style line \
  --size 512 \
  --output arrow.png
```

### Simple Geometric Icons

```bash
# Solid circle icon
python3 scripts/icon_generate.py --shape circle --color "#FF6B6B" --output red_circle.png

# Square with rounded corners
python3 scripts/icon_generate.py --shape rounded-rect --color "#4ECDC4" --output teal_box.png

# Diamond shape
python3 scripts/icon_generate.py --shape diamond --color "#FFE66D" --output yellow_diamond.png
```

## Icon Styles for PPT

| Style | Use Case | Command |
|-------|----------|---------|
| Flat | Modern, clean slides | `--style flat` |
| Line | Minimalist, outline | `--style line` |
| Filled | Bold, emphasis | `--style filled` |
| Gradient | Eye-catching titles | `--style gradient` |
| Duotone | Professional reports | `--style duotone` |

## Workflow: Get Icon for PPT

### Step 1: Search or Describe

```bash
# Option A: Search existing icons
python3 scripts/icon_search.py --query "your-keyword" --limit 5

# Option B: Describe what you need
python3 scripts/icon_generate.py --prompt "your description" --preview
```

### Step 2: Download/Generate

```bash
# Download selected icon
python3 scripts/icon_search.py --query "selected-icon-name" --download --output my_icon.png

# Or generate custom
python3 scripts/icon_generate.py --prompt "description" --output my_icon.png
```

### Step 3: Verify and Use

```bash
# Check icon properties
python3 scripts/icon_verify.py --file my_icon.png

# Resize if needed
python3 scripts/icon_resize.py --input my_icon.png --size 256 --output my_icon_256.png
```

### Step 4: Send to User

```javascript
{
  "tool": "message",
  "action": "send",
  "filePath": "/root/.openclaw/workspace/my_icon.png",
  "filename": "my_ppt_icon.png"
}
```

## API Reference

### icon_search.py

```bash
python3 scripts/icon_search.py [options]

Options:
  --query TEXT        Search query (required)
  --limit N           Number of results (default: 10)
  --download          Download first result as PNG
  --output PATH       Output file path
  --style STYLE       Filter by style: flat, line, filled
  --color COLOR       Filter by color theme
```

### icon_generate.py

```bash
python3 scripts/icon_generate.py [options]

Options:
  --prompt TEXT       Description of icon to generate
  --shape SHAPE       Basic shape: circle, square, diamond, star
  --text TEXT         Text to render as icon
  --style STYLE       Style: flat, line, gradient, duotone
  --color COLOR       Primary color (hex)
  --size N            Output size in pixels (default: 512)
  --output PATH       Output file path
  --bg-color COLOR    Background color (default: transparent)
```

### icon_convert.py

```bash
python3 scripts/icon_convert.py [options]

Options:
  --input PATH        Input SVG file
  --output PATH       Output PNG file
  --size N            Output size (default: 512)
  --color COLOR       Override icon color
```

## Best Practices

1. **Size**: Use 512x512 for flexibility, resize in PPT
2. **Format**: Always PNG with transparency
3. **Style**: Match your PPT theme (flat for modern, line for minimal)
4. **Color**: Use brand colors or neutral (#333, #666, #999)
5. **Consistency**: Use same style throughout presentation

## Common PPT Icon Needs

| Use Case | Recommended Query |
|----------|-------------------|
| Section headers | `title`, `heading`, `flag` |
| Bullet points | `check`, `dot`, `star` |
| Process steps | `arrow-right`, `number-1`, `timeline` |
| Data charts | `chart`, `graph`, `analytics` |
| Contact info | `email`, `phone`, `location` |
| Social media | `twitter`, `linkedin`, `github` |

## Troubleshooting

### Icon not found
- Try synonyms: "chart" → "graph" → "analytics"
- Use broader terms: "email" instead of "gmail"

### Generated icon looks wrong
- Be more specific in prompt
- Try different style: `--style line` vs `--style flat`
- Adjust colors for better contrast

### PNG has white background
- Verify transparency is enabled
- Use PNG format (not JPG)
- Check with: `python3 scripts/icon_verify.py --file icon.png`

## Examples

### Example 1: Full Workflow

User: "I need an icon for AI analytics section in my PPT"

```bash
# Search relevant icons
python3 scripts/icon_search.py --query "ai-brain" --limit 5

# Download best match
python3 scripts/icon_search.py --query "brain-circuit" --download --output ai_icon.png

# Or generate custom
python3 scripts/icon_generate.py --prompt "AI brain with circuit patterns" --style gradient --output ai_custom.png
```

### Example 2: Batch Generate Icons

```bash
# Create icon set
for theme in "strategy" "growth" "innovation" "team"; do
  python3 scripts/icon_generate.py --prompt "$theme concept" --output "${theme}_icon.png"
done
```

### Example 3: Style Matching

```bash
# Generate icons matching your PPT theme color
python3 scripts/icon_generate.py --shape circle --color "#YOUR_BRAND_COLOR" --output brand_icon.png
```

## Links & Resources

- Iconify API: https://api.iconify.design/
- Icon Sets: Material Design, Fluent, Heroicons, Phosphor
- Color Picker: https://colorpicker.me/
