---
name: lh-html-to-image
description: Generate images from HTML+CSS via Chrome headless screenshot. Perfect for covers, posters, info cards, and text-layout images. Zero API cost, 100% accurate text rendering. Triggers: "generate cover", "poster", "HTML to image", "make image".
homepage: https://github.com/liuhedev/lh-openclaw-kit
---

# HTML to Image

Generate images from HTML+CSS using Chrome headless screenshots. Ideal for covers, posters, info cards, and any text-heavy visual content. Zero API cost, 100% accurate text rendering.

## Use Cases

- ✅ Cover images (title + subtitle + tags)
- ✅ Info cards (data display, comparison charts)
- ✅ Text layout images (quote cards, highlight cards)
- ❌ Illustrations, photos (use an AI image generation tool)

## Workflow

### Step 1: Write HTML

Create an HTML file with inline CSS:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    width: 1080px;
    height: 1440px;   /* 3:4 portrait */
    margin: 0;
    overflow: hidden;
    font-family: -apple-system, "PingFang SC", "Noto Sans SC", sans-serif;
  }
</style>
</head>
<body>
  <!-- Your content here -->
</body>
</html>
```

### Step 2: Chrome Headless Screenshot

```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --disable-gpu \
  --screenshot="output.png" \
  --window-size=1080,1440 \
  --hide-scrollbars \
  --force-device-scale-factor=2 \
  "file:///absolute/path/to/your.html"

# Linux (auto-detect chrome/chromium)
google-chrome --headless=new --disable-gpu \
  --screenshot="output.png" \
  --window-size=1080,1440 \
  --hide-scrollbars \
  "file:///absolute/path/to/your.html"
```

Chrome path can be overridden via `CHROME_PATH` environment variable.

## Common Sizes

| Purpose | Width×Height | Ratio |
|---------|-------------|-------|
| Portrait cover | 1080×1440 | 3:4 |
| Square cover | 1080×1080 | 1:1 |
| Widescreen cover | 1920×1080 | 16:9 |
| Social media banner | 1280×720 | 16:9 |

## Tips

- Chrome GPU error logs can be safely ignored
- Use `--force-device-scale-factor=2` for retina/high-DPI output (doubles pixel dimensions)
- Use `--force-device-scale-factor=1` for exact pixel dimensions
- CJK fonts: PingFang SC (macOS built-in), Noto Sans SC (Linux, install via `apt install fonts-noto-cjk`)
- For complex layouts, test in a regular browser first, then screenshot
