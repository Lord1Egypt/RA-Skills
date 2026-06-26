---
name: gumroad-product-images
description: Generate professional product cover images (600x600) and preview/showcase images (1280x720) for Gumroad digital products. Use when creating, updating, or batch-generating Gumroad product images including covers, previews, and thumbnails. Generates HTML templates with modern dark-theme designs, then screenshots them to PNG using Edge headless. Supports custom color themes, badges, content lists, and CTA buttons. No external API or AI image generation needed.
---

# Gumroad Product Images

Generate professional Gumroad product images from HTML templates using Edge headless screenshots.

## Image Types

| Type | Size | Use |
|------|------|-----|
| **Cover** | 600x600 | Gumroad thumbnail, Discover, profile page |
| **Preview** | 1280x720 | Product page showcase image |

## Workflow

### 1. Gather Product Info

Collect from user:
- Product name
- Subtitle / value proposition
- Category tags (3-5 short labels with emoji)
- "What's inside" list (5-6 items)
- Color theme preference (or auto-select from assets/themes.json)

### 2. Generate HTML

Use templates in `assets/` as base. Key rules:
- **All emoji must use HTML entities** (e.g. `&#x26A1;` not ⚡) to prevent encoding corruption on Windows
- **Never include prices or "free"** on images — prices may change
- Set `html { background: <darkest-color>; }` to prevent white edges on screenshot
- Use `100vw`/`100vh` for body dimensions, not fixed pixels
- Font: `'Segoe UI', system-ui, sans-serif`

#### Cover (600x600)
Layout: centered card with badge, icon/number, title, subtitle, tags.

#### Preview (1280x720)  
Layout: left side (badge + icon + title + subtitle + tags) | right side (content list card + CTA button).

CTA button text: "Get Instant Access &#x2192;" (never mention price/free).

### 3. Serve & Screenshot

Start a local HTTP server if not running:
```powershell
cd <product-images-dir>; npx http-server -p 8765 --cors -c-1
```

Screenshot with Edge headless:
```powershell
# Cover (600x600)
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --screenshot="cover.png" --window-size=600,600 --force-device-scale-factor=1 "<url>/cover.html"

# Preview (1280x720)
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --screenshot="preview.png" --window-size=1280,720 --force-device-scale-factor=1 "<url>/preview.html"
```

### 4. Batch Processing

For multiple products, loop:
```powershell
$products = @("product-a","product-b","product-c")
foreach($name in $products) {
  $types = @(@{file="cover";w=600;h=600}, @{file="preview";w=1280;h=720})
  foreach($t in $types) {
    $png = "F:\path\$name\$($t.file).png"
    & "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --screenshot="$png" --window-size="$($t.w),$($t.h)" --force-device-scale-factor=1 "http://127.0.0.1:8765/$name/$($t.file).html"
  }
  Write-Host "Done: $name"
}
```

### 5. Verify

After screenshot, check:
- [ ] No white edges (right/bottom)
- [ ] No emoji garbled text (use HTML entities only)
- [ ] No prices or "free" text on images
- [ ] File size > 50KB (not blank)

## Color Themes

See `assets/themes.json` for predefined themes. Each theme has:
- `bg`: gradient stops for body background
- `html_bg`: solid color for html element
- `accent`: primary accent color for badges/CTAs
- `accent2`: secondary accent for gradients
- `dot`: color for list dots
- `highlight`: color for headings/titles
