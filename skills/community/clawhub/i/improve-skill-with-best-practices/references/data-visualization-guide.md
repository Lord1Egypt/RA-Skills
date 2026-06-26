# Data Visualization Guide

## Visualization Principles

1. **Chart-first reporting**: When presenting data findings, always generate a chart BEFORE writing the textual interpretation. The chart is the primary evidence; the text explains the insight.
2. **One chart, one insight**: Each chart should communicate a single clear message. Use the chart title to state the insight (e.g., "Mobile bounce rate is 2x desktop" instead of "Bounce rate by device").
3. **Goal-aligned visualization**: Highlight goal-relevant thresholds, targets, or benchmarks in charts using reference lines or color coding.
4. **Consistent style**: Use a consistent color palette and style across all charts in a single report.

## Chart Generation Method

Use Python with `matplotlib` to generate charts. Each analysis script should combine **data processing and chart generation in one script** — read raw JSON from `$DATA_DIR/data/`, process/aggregate the data, output structured results, and generate charts in the same execution. This ensures charts are always consistent with the analysis data.

**Standard pattern** (data analysis + chart generation in one script):

```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend, MUST be set before importing pyplot
import matplotlib.pyplot as plt
import json
import os
import platform

# ── Configuration ──────────────────────────────────────────
DATA_DIR = os.environ.get("DATA_DIR", ".skills-data/google-analytics-and-search-improve")
CHARTS_DIR = os.path.join(DATA_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ── CJK font support (Chinese / Japanese / Korean) ────────
_system = platform.system()
if _system == "Darwin":
    _cjk_fonts = ["Arial Unicode MS", "PingFang SC", "Heiti SC", "STHeiti"]
elif _system == "Linux":
    _cjk_fonts = ["WenQuanYi Micro Hei", "Noto Sans CJK SC", "DejaVu Sans"]
else:  # Windows
    _cjk_fonts = ["Microsoft YaHei", "SimHei", "SimSun"]

# ── Style defaults ─────────────────────────────────────────
plt.rcParams.update({
    "font.sans-serif": _cjk_fonts,
    "axes.unicode_minus": False,     # Fix minus sign rendering with CJK fonts
    "figure.figsize": (10, 6),
    "figure.dpi": 150,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
})

# Color palette (consistent across all charts)
COLORS = ["#4285F4", "#EA4335", "#FBBC04", "#34A853", "#FF6D01", "#46BDC6", "#7B61FF", "#F538A0"]
COLOR_GOOD = "#34A853"
COLOR_WARN = "#FBBC04"
COLOR_BAD = "#EA4335"
COLOR_NEUTRAL = "#4285F4"

# ── Load data ──────────────────────────────────────────────
with open(os.path.join(DATA_DIR, "data", "DATAFILE.json")) as f:
    data = json.load(f)

# ── Plot ───────────────────────────────────────────────────
fig, ax = plt.subplots()
# ... plotting code ...
ax.set_title("Insight-Driven Chart Title")
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")

output_path = os.path.join(CHARTS_DIR, "chart_name.png")
fig.savefig(output_path)
plt.close(fig)
print(f"Chart saved: {output_path}")
```

**Embed in Markdown report**:
```markdown
### Finding: [Insight Title]

![Chart description](../charts/chart_name.png)

[Textual interpretation of what the chart reveals and recommended action]
```

## Chart Type Selection Guide

| Data Pattern | Recommended Chart | When to Use |
|---|---|---|
| **Trend over time** | Line chart | GSC daily clicks/impressions, GA4 traffic trends, funnel trends |
| **Category comparison** | Horizontal bar chart | Top queries by clicks, pages by traffic, channels comparison |
| **Part of whole** | Stacked bar or pie chart (≤6 slices) | Traffic source distribution, device breakdown |
| **Funnel / conversion flow** | Funnel chart (horizontal stacked bars) | User journey drop-off, signup/purchase funnel |
| **Two metrics correlation** | Scatter plot | CTR vs position, bounce rate vs page load time |
| **Distribution** | Histogram or box plot | Session duration distribution, page load time spread |
| **Before/After or Gap** | Grouped bar chart | Expected vs actual behavior, mobile vs desktop comparison |
| **Performance scores** | Gauge or bullet chart | PSI scores, CWV metrics against thresholds |
| **Ranking with values** | Horizontal bar + value labels | Top 10 keywords, top pages by any metric |

## Required Charts per Phase

**Phase 2 (GSC Analysis)** — generate and embed:
- **Keyword intent distribution**: Stacked bar or pie chart showing query distribution across Awareness / Consideration / Decision / Retention stages
- **Top queries performance**: Horizontal bar chart of top 15 queries by clicks, with CTR annotated
- **CTR vs Position scatter**: Scatter plot of queries showing CTR vs average position, highlighting high-impression low-CTR outliers
- **Trend chart**: Line chart of daily clicks & impressions over the analysis period
- **Device/country breakdown**: Bar chart of clicks by device type and/or top countries

**Phase 3 (GA4 Analysis)** — generate and embed:
- **Traffic channel breakdown**: Pie or bar chart of sessions by source/medium
- **Top landing pages**: Horizontal bar chart with engagement rate or bounce rate overlay
- **Journey gap visualization**: Grouped bar chart comparing expected vs actual conversion rates at each journey stage
- **Device comparison**: Side-by-side bars comparing key metrics (bounce rate, engagement rate, conversion) across desktop/mobile/tablet
- **Trend chart**: Line chart of sessions/users over the analysis period

**Phase 3b (Funnel Analysis)** — generate and embed:
- **Funnel chart**: Horizontal funnel visualization showing step-by-step user counts and drop-off percentages
- **Funnel by device/channel**: Grouped funnel comparison across segments
- **Funnel trend**: Line chart of daily conversion rates for key funnel steps

**Phase 4 (Site Audit)** — generate and embed:
- **PSI scores radar/bar**: Bar chart of Performance, SEO, Accessibility, Best Practices scores (mobile & desktop)
- **Core Web Vitals**: Bar or gauge chart of LCP, FID/INP, CLS against Good/Needs Improvement/Poor thresholds

**Phase 6 (Final Report)** — generate and embed:
- **Executive summary dashboard**: A multi-panel figure (2×2 or 2×3 subplots) summarizing the most critical metrics at a glance
- **Goal achievement scorecard**: Bar chart showing goal achievement percentage for each journey stage
- **Priority distribution**: Horizontal bar chart showing count of issues by P0/P1/P2/P3 priority
- Reuse the most impactful charts from Phase 2-4 in the final report (reference the same image files)

## CJK Font Support

> **Note**: The standard pattern template above already includes CJK font auto-detection. You do NOT need to add it separately — it is built into the `plt.rcParams` block. The logic below is kept for reference only.

When the site content or data contains Chinese/Japanese/Korean characters, matplotlib needs a CJK-compatible font. The standard template handles this automatically via `platform.system()` detection:

- **macOS (Darwin)**: Arial Unicode MS → PingFang SC → Heiti SC → STHeiti
- **Linux**: WenQuanYi Micro Hei → Noto Sans CJK SC → DejaVu Sans
- **Windows**: Microsoft YaHei → SimHei → SimSun

Key `rcParams` that must be set:
```python
plt.rcParams["font.sans-serif"] = ["PingFang SC", ...]  # CJK-capable font list
plt.rcParams["axes.unicode_minus"] = False               # Fix minus sign rendering
```
