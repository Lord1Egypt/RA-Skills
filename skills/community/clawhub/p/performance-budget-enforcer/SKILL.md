---
name: performance-budget-enforcer
description: Define, measure, and enforce web performance budgets — bundle sizes, asset counts, image weights, third-party scripts. Fails CI when budgets are exceeded. Tracks trends across builds.
---

# Performance Budget Enforcer

Set performance budgets for web projects and enforce them in CI. Measures JS/CSS bundle sizes, image weights, font sizes, third-party script counts, and total transfer size. Compares against budgets, flags regressions, and tracks trends.

Use when: "check bundle size", "set performance budget", "are we over budget", "track asset size", "web performance audit", "lighthouse budget", or integrating perf checks into CI/CD.

## Commands

### 1. `measure` — Measure Current Asset Sizes

Scan the build output directory and measure everything.

```bash
# Auto-detect build output directory
BUILD_DIR=""
for dir in dist build out .next/static public/build _site; do
  if [ -d "$dir" ]; then
    BUILD_DIR="$dir"
    break
  fi
done

if [ -z "$BUILD_DIR" ]; then
  echo "No build directory found. Run your build command first, or specify the directory."
  exit 1
fi

echo "Scanning: $BUILD_DIR"
```

#### JavaScript Bundles
```bash
# JS files with sizes (sorted largest first)
find "$BUILD_DIR" -name "*.js" -type f -exec du -b {} + 2>/dev/null | sort -rn | head -20
TOTAL_JS=$(find "$BUILD_DIR" -name "*.js" -type f -exec du -b {} + 2>/dev/null | awk '{s+=$1} END {print s+0}')
echo "Total JS: $TOTAL_JS bytes ($(echo "scale=1; $TOTAL_JS / 1024" | bc) KB)"

# Gzipped sizes (more realistic transfer size)
find "$BUILD_DIR" -name "*.js" -type f | while read f; do
  ORIG=$(wc -c < "$f")
  GZIP=$(gzip -c "$f" | wc -c)
  echo "$GZIP $ORIG $f"
done | sort -rn | head -10
TOTAL_JS_GZ=$(find "$BUILD_DIR" -name "*.js" -type f -exec sh -c 'gzip -c "$1" | wc -c' _ {} \; 2>/dev/null | awk '{s+=$1} END {print s+0}')
echo "Total JS (gzip): $TOTAL_JS_GZ bytes ($(echo "scale=1; $TOTAL_JS_GZ / 1024" | bc) KB)"
```

#### CSS Bundles
```bash
find "$BUILD_DIR" -name "*.css" -type f -exec du -b {} + 2>/dev/null | sort -rn | head -10
TOTAL_CSS=$(find "$BUILD_DIR" -name "*.css" -type f -exec du -b {} + 2>/dev/null | awk '{s+=$1} END {print s+0}')
echo "Total CSS: $TOTAL_CSS bytes ($(echo "scale=1; $TOTAL_CSS / 1024" | bc) KB)"
```

#### Images
```bash
find "$BUILD_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.webp" -o -name "*.avif" \) \
  -exec du -b {} + 2>/dev/null | sort -rn | head -15
TOTAL_IMG=$(find "$BUILD_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.webp" -o -name "*.avif" \) \
  -exec du -b {} + 2>/dev/null | awk '{s+=$1} END {print s+0}')
echo "Total images: $TOTAL_IMG bytes ($(echo "scale=1; $TOTAL_IMG / 1024" | bc) KB)"

# Flag unoptimized images (PNG > 100KB, JPG > 200KB without WebP alternative)
find "$BUILD_DIR" -name "*.png" -size +100k -type f 2>/dev/null
find "$BUILD_DIR" -name "*.jpg" -size +200k -type f 2>/dev/null
```

#### Fonts
```bash
find "$BUILD_DIR" -type f \( -name "*.woff" -o -name "*.woff2" -o -name "*.ttf" -o -name "*.otf" -o -name "*.eot" \) \
  -exec du -b {} + 2>/dev/null | sort -rn
TOTAL_FONT=$(find "$BUILD_DIR" -type f \( -name "*.woff" -o -name "*.woff2" -o -name "*.ttf" -o -name "*.otf" -o -name "*.eot" \) \
  -exec du -b {} + 2>/dev/null | awk '{s+=$1} END {print s+0}')
echo "Total fonts: $TOTAL_FONT bytes ($(echo "scale=1; $TOTAL_FONT / 1024" | bc) KB)"

# Flag non-woff2 fonts (should be woff2 in 2026)
find "$BUILD_DIR" -type f \( -name "*.ttf" -o -name "*.otf" -o -name "*.eot" -o -name "*.woff" \) 2>/dev/null
```

#### Total Transfer Size
```bash
TOTAL=$(find "$BUILD_DIR" -type f -exec du -b {} + 2>/dev/null | awk '{s+=$1} END {print s+0}')
echo "Total build output: $TOTAL bytes ($(echo "scale=1; $TOTAL / 1024 / 1024" | bc) MB)"
FILE_COUNT=$(find "$BUILD_DIR" -type f | wc -l)
echo "Total files: $FILE_COUNT"
```

### 2. `budget` — Define Performance Budget

Create or update a `.perfbudget.json` file in the project root.

Default budgets (adjust per project type):

```json
{
  "budgets": {
    "js_total_kb": 300,
    "js_total_gzip_kb": 100,
    "js_single_file_kb": 150,
    "css_total_kb": 100,
    "css_single_file_kb": 50,
    "img_total_kb": 1000,
    "img_single_file_kb": 200,
    "font_total_kb": 200,
    "total_transfer_mb": 3,
    "total_file_count": 200,
    "third_party_scripts": 5
  },
  "presets": {
    "strict": {
      "js_total_gzip_kb": 50,
      "total_transfer_mb": 1
    },
    "mobile": {
      "js_total_gzip_kb": 70,
      "img_total_kb": 500,
      "total_transfer_mb": 2
    }
  }
}
```

Preset suggestions based on project type:
- **SPA (React/Vue/Svelte)**: JS 150KB gzip, total 2MB
- **Static site / blog**: JS 50KB gzip, total 1MB
- **E-commerce**: JS 200KB gzip, images 2MB, total 5MB
- **Dashboard / admin**: JS 300KB gzip, total 5MB (internal tools can be larger)

### 3. `check` — Enforce Budget

Compare measurements against `.perfbudget.json`. This is the CI command.

```bash
# Read budget file
if [ ! -f ".perfbudget.json" ]; then
  echo "No .perfbudget.json found. Run 'budget' command first to create one."
  echo "Using default budgets..."
fi
```

For each metric, compare measured vs budget:

```
✅ JS total (gzip):   87 KB / 100 KB budget (87%)
✅ CSS total:          34 KB / 100 KB budget (34%)
⚠️  Images total:     890 KB / 1000 KB budget (89%) — approaching limit
❌ JS single file:    180 KB / 150 KB budget (120%) — OVER BUDGET
   └─ dist/vendor.chunk.js: 180 KB
❌ Total transfer:    3.4 MB / 3 MB budget (113%) — OVER BUDGET

RESULT: 2 budget violations found
```

Exit codes:
- 0: All within budget
- 1: One or more budgets exceeded
- 2: Budget file missing (warning only)

### 4. `trend` — Track Size Over Time

Append current measurements to `.perfbudget-history.json`:

```json
{
  "history": [
    {
      "date": "2026-04-28",
      "commit": "abc123",
      "branch": "main",
      "js_total_gzip_kb": 87,
      "css_total_kb": 34,
      "img_total_kb": 890,
      "total_transfer_mb": 2.1
    }
  ]
}
```

Display trend:
```
JS (gzip) over last 10 builds:
  Apr 20: 72 KB ██████████████
  Apr 21: 75 KB ███████████████
  Apr 23: 82 KB ████████████████
  Apr 25: 87 KB █████████████████   ↑ +20.8% in 8 days
  Budget: 100 KB ████████████████████ (limit)
```

Flag: "JS bundle grew 20.8% in 8 days — investigate recent additions."

### 5. `third-party` — Audit Third-Party Scripts

Scan HTML files and JS bundles for external domains:

```bash
# Find external script tags
rg -n 'src="https?://[^"]*"' -g '*.html' "$BUILD_DIR" 2>/dev/null

# Find external URLs in JS bundles
rg -o 'https?://[a-zA-Z0-9.-]+\.[a-z]{2,}' -g '*.js' "$BUILD_DIR" 2>/dev/null | \
  awk -F: '{print $NF}' | sort -u

# Common third-party domains to flag
# Analytics: google-analytics, segment, mixpanel, amplitude, hotjar, fullstory
# Ads: doubleclick, googlesyndication, facebook, criteo
# Chat: intercom, drift, zendesk, crisp
# A/B: optimizely, launchdarkly, split.io
```

Categorize by type (analytics, ads, chat, A/B testing, error tracking, CDN) and report impact on load time.

### 6. `optimize` — Suggest Optimizations

Based on measurements, provide specific actionable suggestions:

- **Large JS bundles**: Suggest code splitting, dynamic imports, tree shaking. Show which chunks are largest.
- **Uncompressed assets**: Check if gzip/brotli is configured. Measure compression ratios.
- **Unoptimized images**: Suggest WebP/AVIF conversion, lazy loading, responsive images.
- **Too many fonts**: Suggest subsetting, reducing font weights, system font fallbacks.
- **Third-party bloat**: Suggest self-hosting, defer/async loading, removing unused scripts.
- **Large CSS**: Suggest PurgeCSS/Tailwind purge, critical CSS extraction, unused CSS removal.

## Output Formats

- **text** (default): Human-readable with color indicators and bar charts
- **json**: Machine-readable `{measurements: {}, budget: {}, violations: [], suggestions: []}`
- **markdown**: PR comment format with tables and status icons
- **github-annotations**: `::warning file=...::Budget exceeded` format for GitHub Actions

## CI Integration Examples

```yaml
# GitHub Actions
- name: Check performance budget
  run: |
    npm run build
    # Agent runs: performance-budget-enforcer check
    # Exits 1 if over budget

# As PR comment (markdown format)
- name: Post budget report
  run: |
    # Agent runs: performance-budget-enforcer check --format markdown > budget-report.md
    gh pr comment $PR_NUMBER --body-file budget-report.md
```

## Notes

- Requires a built project (run your build command first)
- Gzip size measurement uses actual gzip compression, not estimates
- History file (`.perfbudget-history.json`) should be committed to track trends
- Does not run Lighthouse or browser-based metrics — focuses on static asset analysis which is fast and deterministic
- For Core Web Vitals (CLS, LCP, FID), use Lighthouse or web-vitals library separately
