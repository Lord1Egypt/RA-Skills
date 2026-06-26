---
name: CWV Budget Guard
description: Core Web Vitals budget enforcer that runs Lighthouse against a local dev server or staging URL, extracts LCP, INP, CLS, FCP, and TTFB scores, compares against a project .cwv-budget.json config, and fails CI if any metric regresses. Identifies which source file, image, render-blocking resource, or JavaScript chunk caused each metric violation with specific fix recommendations. Tracks metric trends across runs by appending to a local history file. Works with any framework (Next.js, Vite, CRA, Rails, Django). Zero external cloud account — runs Lighthouse via npx locally. Triggers on "core web vitals", "LCP slow", "CLS regression", "Lighthouse score dropped", "performance budget", "web vitals", "/cwv-check".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - performance
    - web-vitals
    - lighthouse
    - seo
    - lcp
    - cls
    - inp
    - developer-tools
    - ci
    - frontend
---

# Core Web Vitals Budget Guard

Your Lighthouse score was 94. You merged a PR. It's now 71. Google starts demoting your pages.

This skill enforces a CWV budget — run it in CI, get a specific diagnosis when a metric regresses, and fix it before it ships.

**Runs Lighthouse locally via npx. No cloud account. Works with any framework.**

---

## Trigger Phrases

- "core web vitals", "web vitals check", "cwv audit"
- "LCP slow", "CLS regression", "INP too high"
- "Lighthouse score dropped", "performance budget"
- "which file is slowing down my LCP"
- "web vitals CI", "performance regression"
- "/cwv-check"

---

## How to Provide Input

```bash
# Option 1: Run against local dev server (auto-starts if needed)
/cwv-check http://localhost:3000

# Option 2: Run against a specific route
/cwv-check http://localhost:3000/dashboard
/cwv-check http://localhost:3000/products/123

# Option 3: Run against staging URL
/cwv-check https://staging.myapp.com

# Option 4: Set/update budget thresholds
/cwv-check --set-budget LCP=2500 CLS=0.1 INP=200

# Option 5: CI mode (exits 1 on regression)
/cwv-check http://localhost:3000 --ci

# Option 6: Compare against last run
/cwv-check http://localhost:3000 --diff

# Option 7: Run across multiple routes
/cwv-check --routes /,/dashboard,/products --url http://localhost:3000
```

---

## Step 1: Check Dependencies

```bash
# Check if Lighthouse CLI is available
if npx --yes lighthouse --version > /dev/null 2>&1; then
    echo "✅ Lighthouse CLI available"
else
    echo "Installing Lighthouse CLI..."
    npm install -D @lhci/cli
    # OR: use npx (auto-downloads, ~50MB, slower first run)
fi

# Alternative: use Chrome DevTools protocol directly
# node -e "require('chrome-launcher')" 2>/dev/null && echo "✅ chrome-launcher available"
```

---

## Step 2: Run Lighthouse

```bash
# Single URL, JSON output for parsing
npx lighthouse $URL \
    --output=json \
    --output-path=./cwv-report.json \
    --chrome-flags="--headless --no-sandbox --disable-gpu" \
    --only-categories=performance \
    --quiet

# OR via @lhci/cli for CI integration
npx @lhci/cli collect \
    --url=$URL \
    --numberOfRuns=3 \
    --settings.onlyCategories=performance

# Extract just the metrics we care about
python3 -c "
import json
report = json.load(open('cwv-report.json'))
audits = report['audits']

metrics = {
    'LCP':  audits.get('largest-contentful-paint', {}).get('numericValue', 0),
    'CLS':  audits.get('cumulative-layout-shift', {}).get('numericValue', 0),
    'INP':  audits.get('interaction-to-next-paint', {}).get('numericValue', 0),
    'FCP':  audits.get('first-contentful-paint', {}).get('numericValue', 0),
    'TTFB': audits.get('server-response-time', {}).get('numericValue', 0),
    'TBT':  audits.get('total-blocking-time', {}).get('numericValue', 0),
    'Score': int(report['categories']['performance']['score'] * 100),
}

for k, v in metrics.items():
    if k in ['LCP', 'FCP', 'TTFB', 'TBT', 'INP']:
        print(f'{k}: {v:.0f}ms')
    elif k == 'CLS':
        print(f'{k}: {v:.3f}')
    else:
        print(f'{k}: {v}')
"
```

---

## Step 3: Budget Config

```json
// .cwv-budget.json — place in project root
{
  "budgets": [
    {
      "path": "/*",
      "timings": [
        { "metric": "largest-contentful-paint", "budget": 2500 },
        { "metric": "cumulative-layout-shift",  "budget": 0.1  },
        { "metric": "interaction-to-next-paint", "budget": 200 },
        { "metric": "first-contentful-paint",   "budget": 1800 },
        { "metric": "server-response-time",     "budget": 600  },
        { "metric": "total-blocking-time",      "budget": 200  }
      ],
      "resourceSizes": [
        { "resourceType": "script",    "budget": 300 },
        { "resourceType": "image",     "budget": 500 },
        { "resourceType": "stylesheet","budget": 50  },
        { "resourceType": "total",     "budget": 1000}
      ]
    }
  ]
}
```

**Google's thresholds for reference:**

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤2.5s | 2.5–4s | >4s |
| INP | ≤200ms | 200–500ms | >500ms |
| CLS | ≤0.1 | 0.1–0.25 | >0.25 |
| FCP | ≤1.8s | 1.8–3s | >3s |
| TTFB | ≤800ms | 800ms–1.8s | >1.8s |

---

## Step 4: Parse Lighthouse Opportunities

```python
import json
from pathlib import Path

def parse_opportunities(report_path='cwv-report.json'):
    """Extract Lighthouse opportunity/diagnostic items linked to failing metrics."""
    report = json.load(open(report_path))
    audits = report['audits']

    opportunities = []

    # LCP attribution
    lcp_audit = audits.get('largest-contentful-paint-element', {})
    if lcp_audit.get('details', {}).get('items'):
        for item in lcp_audit['details']['items']:
            node = item.get('node', {})
            opportunities.append({
                'metric': 'LCP',
                'type': 'LCP_ELEMENT',
                'description': f"LCP element: {node.get('snippet', 'unknown')}",
                'savings': None,
                'fix': 'Preload this element or reduce its server response time.',
            })

    # Render-blocking resources (affects LCP and FCP)
    rbl = audits.get('render-blocking-resources', {})
    if rbl.get('numericValue', 0) > 0:
        for item in rbl.get('details', {}).get('items', []):
            opportunities.append({
                'metric': 'FCP/LCP',
                'type': 'RENDER_BLOCKING',
                'description': f"Render-blocking: {item.get('url', 'unknown')}",
                'savings': f"{item.get('wastedMs', 0):.0f}ms",
                'fix': 'Add rel="preload" or defer/async. Move CSS to inline critical styles.',
            })

    # Unused JavaScript (affects TBT/INP)
    unused_js = audits.get('unused-javascript', {})
    if unused_js.get('numericValue', 0) > 0:
        for item in unused_js.get('details', {}).get('items', []):
            if item.get('wastedBytes', 0) > 10000:  # >10KB
                opportunities.append({
                    'metric': 'TBT/INP',
                    'type': 'UNUSED_JS',
                    'description': f"Unused JS: {item.get('url', 'unknown')} "
                                   f"({item.get('wastedBytes', 0)/1024:.0f}KB unused)",
                    'savings': f"{item.get('wastedBytes', 0)/1024:.0f}KB",
                    'fix': 'Tree-shake unused exports. Use dynamic import() for below-fold code.',
                })

    # Unoptimized images (affects LCP)
    img_audit = audits.get('uses-optimized-images', {})
    for item in img_audit.get('details', {}).get('items', []):
        if item.get('wastedBytes', 0) > 20000:
            opportunities.append({
                'metric': 'LCP',
                'type': 'IMAGE_SIZE',
                'description': f"Over-sized image: {item.get('url', 'unknown')} "
                               f"({item.get('totalBytes', 0)/1024:.0f}KB → "
                               f"{item.get('wastedBytes', 0)/1024:.0f}KB wasted)",
                'savings': f"{item.get('wastedBytes', 0)/1024:.0f}KB",
                'fix': 'Convert to WebP/AVIF. Add width/height attributes. Use <img loading="lazy"> for below-fold.',
            })

    # CLS attribution
    cls_items = audits.get('layout-shift-elements', {}).get('details', {}).get('items', [])
    for item in cls_items:
        node = item.get('node', {})
        opportunities.append({
            'metric': 'CLS',
            'type': 'LAYOUT_SHIFT_ELEMENT',
            'description': f"Layout shift source: {node.get('snippet', 'unknown')}",
            'savings': None,
            'fix': 'Add explicit width/height. Use CSS aspect-ratio. Avoid inserting content above existing.',
        })

    return opportunities
```

---

## Step 5: Track History and Diff

```python
import json
import os
from datetime import datetime

HISTORY_FILE = '.cwv-history.json'

def save_run(url, metrics):
    """Append metrics to local history file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        history = json.load(open(HISTORY_FILE))

    history.append({
        'timestamp': datetime.utcnow().isoformat(),
        'url': url,
        'metrics': metrics,
        'git_sha': os.popen('git rev-parse --short HEAD 2>/dev/null').read().strip(),
        'branch': os.popen('git branch --show-current 2>/dev/null').read().strip(),
    })

    # Keep last 50 runs
    json.dump(history[-50:], open(HISTORY_FILE, 'w'), indent=2)


def diff_vs_last_run(current_metrics):
    """Compare current metrics against the previous run."""
    if not os.path.exists(HISTORY_FILE):
        return None

    history = json.load(open(HISTORY_FILE))
    if len(history) < 2:
        return None

    prev = history[-2]['metrics']  # -1 is current, -2 is previous
    diffs = {}
    for metric, value in current_metrics.items():
        if metric in prev:
            prev_value = prev[metric]
            change = value - prev_value
            pct = (change / prev_value * 100) if prev_value else 0
            diffs[metric] = {
                'prev': prev_value,
                'current': value,
                'change': change,
                'pct': pct,
                'regressed': change > 0 and metric != 'Score',  # higher is worse except score
            }
    return diffs
```

---

## Step 6: Output Report

```markdown
## Core Web Vitals Audit
URL: http://localhost:3000 | Branch: feature/new-hero | Run: 2026-03-19 09:14

---

### Metrics vs Budget

| Metric | Score | Budget | Status | vs Last Run |
|--------|-------|--------|--------|-------------|
| LCP | 3,240ms | ≤2,500ms | 🔴 FAIL (+740ms) | ↑ +890ms |
| INP | 187ms | ≤200ms | ✅ PASS | → +12ms |
| CLS | 0.08 | ≤0.10 | ✅ PASS | → -0.01 |
| FCP | 1,650ms | ≤1,800ms | ✅ PASS | → +20ms |
| TTFB | 210ms | ≤600ms | ✅ PASS | → +5ms |
| Performance Score | 68 | ≥80 | 🔴 FAIL (-12pts) | ↓ -13pts |

**Verdict: 🔴 FAIL — LCP regression since last run (+890ms)**

---

### Root Cause: LCP Regression

**LCP Element:** `<img src="/hero-banner-v2.jpg" class="hero-banner">`

**Cause 1 — Image not preloaded (saves ~720ms)**
The new hero image `/hero-banner-v2.jpg` (847KB) is discovered late — the browser finds it only after parsing CSS.

```html
<!-- Add to <head>: -->
<link rel="preload" href="/hero-banner-v2.jpg" as="image" fetchpriority="high">
```

**Cause 2 — Image not optimized (saves ~580KB)**
`/hero-banner-v2.jpg` — 847KB JPEG (should be ~120KB WebP)

```bash
# Convert to WebP:
npx @squoosh/cli --webp '{"quality":80}' public/hero-banner-v2.jpg
# Saves ~700KB → LCP estimated improvement: ~400ms

# Or in Next.js: use <Image> component (auto-optimizes)
import Image from 'next/image'
<Image src="/hero-banner-v2.jpg" priority width={1200} height={600} />
```

**Cause 3 — Render-blocking stylesheet (saves ~180ms)**
`/styles/themes/dark-mode.css` (67KB) is render-blocking.

```html
<!-- Change from: -->
<link rel="stylesheet" href="/styles/themes/dark-mode.css">

<!-- To (load async): -->
<link rel="preload" href="/styles/themes/dark-mode.css" as="style"
      onload="this.onload=null;this.rel='stylesheet'">
```

---

### Trend (last 5 runs)

```
Date        Branch                LCP     CLS    INP    Score
2026-03-17  main                  1,850ms 0.09  175ms   86  ← baseline
2026-03-18  main                  1,920ms 0.09  180ms   84
2026-03-19  feature/new-hero      3,240ms 0.08  187ms   68  ← REGRESSION ⚠️
```

LCP jumped 1,390ms between yesterday's main and this branch. The new hero image is the culprit.

---

### CI Integration

```bash
# Add to .github/workflows/ci.yml
- name: Core Web Vitals check
  run: |
    npx serve -s build -l 3000 &
    sleep 3
    npx lighthouse http://localhost:3000 \
      --budget-path=.cwv-budget.json \
      --output=json \
      --quiet \
      --chrome-flags="--headless --no-sandbox" | \
    python3 scripts/cwv-check.py --fail-on-budget-exceeded
```
```

---

## Quick Mode Output

```
CWV Audit: http://localhost:3000 (feature/new-hero)

🔴 LCP: 3,240ms (budget: 2,500ms) — FAIL, +890ms vs last run
✅ INP: 187ms   ✅ CLS: 0.08   ✅ FCP: 1,650ms   ✅ TTFB: 210ms
Performance Score: 68/100 (budget: 80)

Root cause: /hero-banner-v2.jpg (847KB, not preloaded)
Fix 1: Add <link rel="preload"> → saves ~720ms
Fix 2: Convert to WebP (80q) → saves ~400ms
Combined: LCP drops to ~2,100ms ✅

Run /cwv-check --diff for trend chart vs last 5 commits
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
