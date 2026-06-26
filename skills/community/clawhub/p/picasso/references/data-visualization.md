# Data Visualization & Dashboard Design Reference

## 1. Chart Selection Decision Matrix

Select charts by the **question your data answers**, not by what looks interesting.

| Purpose | Recommended Charts | Avoid |
|---|---|---|
| **Comparison** (categories vs values) | Bar (vertical/horizontal), Grouped bar, Lollipop | Pie (hard to compare slices) |
| **Trend over time** (time-series) | Line, Area, Sparkline | Bar (unless discrete intervals) |
| **Composition** (parts of a whole) | Stacked bar, Pie/Donut (<=6 slices), Treemap | Line chart |
| **Distribution** (spread/frequency) | Histogram, Box plot, Violin, Scatter | Pie chart |
| **Relationship** (two+ numeric vars) | Scatter, Bubble (3rd variable as size) | Bar chart |
| **Ranking** (ordered comparison) | Horizontal bar (sorted), Lollipop | Pie/Donut |
| **Flow/Conversion** (sequential stages) | Funnel, Sankey | Bar chart |
| **Performance vs target** (single KPI) | Gauge, Bullet chart | Pie chart |
| **Inline trend indicator** (compact) | Sparkline (word-sized) | Full chart |
| **Intensity/correlation** (two categorical axes) | Heatmap | 3D bar charts |

### Quick Decision Flow

```
What are you showing?
  -> Change over time?  -> Line (continuous) / Bar (discrete intervals)
  -> Comparison?        -> Bar (horizontal if labels are long)
  -> Part of whole?     -> Donut (<=6 cats) / Treemap (many) / Stacked bar (over time)
  -> Relationship?      -> Scatter / Bubble
  -> Distribution?      -> Histogram / Box plot
  -> Single KPI?        -> Big number card with sparkline
```

---

## 2. Dashboard Design Patterns

### Layout Patterns

**Overview + Detail (most common):** Top row = KPI summary cards. Middle = primary charts. Bottom = detailed tables or drill-down views.

**Drill-Down:** Start with high-level aggregates; clicking reveals progressively granular data. Use breadcrumbs for navigation context.

**Contextual/Filtered:** Global filter bar at top. All panels respond to the same filter state.

### Grid System

Use a **12-column grid** with 16-24px gutters.

```
| KPI | KPI | KPI | KPI |       <- 3-col each (4 cards)
|   Primary Chart   | Secondary |  <- 8-col + 4-col
|      Data Table              |  <- 12-col full width
```

### KPI Card Anatomy

```
+----------------------------------+
|  Revenue            +12.3% ^    |  <- Label + trend indicator
|  $1,234,567                     |  <- Primary metric (large)
|  vs $1,098,000 target           |  <- Comparison context
|  ________ sparkline             |  <- Trend line (last 30 days)
+----------------------------------+
```

**Rules:**
- Always pair KPIs with context (target, prior period, benchmark).
- Semantic color only for status: green = on track, amber = warning, red = critical.
- Show "Last updated" timestamp on every dashboard.
- Limit to 4-8 KPI cards maximum per view.

### Real-Time Data Display

- Visible "live" indicator or timestamp for data freshness.
- CSS transitions for value changes (fade or count-up animation).
- Avoid polling faster than ~5s minimum.

---

## 3. Color for Data

### Sequential (low-to-high, single variable)
```
Blues:    #f7fbff -> #9ecae1 -> #08519c -> #08306b
Viridis: #fde725 -> #35b779 -> #31688e -> #440154
```
Light = low, dark = high.

### Diverging (two extremes with neutral midpoint)
```
RdBu:  #b2182b -> #f4a582 -> #f7f7f7 -> #92c5de -> #2166ac
PRGn:  #762a83 -> #c2a5cf -> #f7f7f7 -> #a6dba0 -> #1b7837
```
Use for deviation from center (profit/loss, above/below average).

### Qualitative / Categorical (distinct groups)
```
Tableau 10:  #4e79a7  #f28e2c  #e15759  #76b7b2  #59a14f  #edc949  #af7aa1  #ff9da7  #9c755f  #bab0ab
Okabe-Ito:   #E69F00  #56B4E9  #009E73  #F0E442  #0072B2  #D55E00  #CC79A7  #000000
```

### OKLCH Programmatic Palettes

```css
/* Sequential: same hue, vary lightness */
--color-1: oklch(0.95 0.03 250);  /* lightest */
--color-2: oklch(0.75 0.08 250);
--color-3: oklch(0.55 0.13 250);
--color-4: oklch(0.35 0.15 250);  /* darkest */

/* Qualitative: same lightness+chroma, rotate hue */
--cat-1: oklch(0.7 0.12 30);   /* orange */
--cat-2: oklch(0.7 0.12 230);  /* blue */
--cat-3: oklch(0.7 0.12 150);  /* green */
--cat-4: oklch(0.7 0.12 330);  /* pink */
```

### Colorblind-Safe Rules

1. **Default to Okabe-Ito** for categorical data.
2. **Never use red/green as the only differentiator.**
3. **Use Viridis** for sequential scales.
4. **Blue is the safest single hue.**
5. **Supplement color with shape, pattern, or label** (WCAG 1.4.1).
6. **Limit categorical colors to 6-8 max.**

---

## 4. Chart Accessibility

### Text Alternatives (WCAG 1.1.1)

```jsx
<figure>
  <svg role="img" aria-labelledby="chart-title" aria-describedby="chart-desc">
    <title id="chart-title">Quarterly Revenue</title>
    <desc id="chart-desc">Bar chart showing revenue growth from $1.2M in Q1 to $1.5M in Q4.</desc>
  </svg>
  <details>
    <summary>View data table</summary>
    <table><!-- structured data as accessible fallback --></table>
  </details>
</figure>
```

### Keyboard Navigation
- All interactive chart elements must be focusable.
- Arrow keys move between data points within a series.
- Enter/Space to activate (drill-down, tooltip).
- Escape to dismiss tooltips.

### Visual Patterns for Colorblindness
Use SVG fill patterns alongside color so colorblind users and grayscale remain readable.

---

## 5. React Charting Libraries

| Library | Best For | Bundle Size | Learning Curve |
|---|---|---|---|
| **Recharts** | Standard dashboards, rapid prototyping | Light | Low |
| **Nivo** | Rich chart variety, theming, SSR | ~371KB/module | Moderate |
| **Victory** | Cross-platform (React + React Native) | ~1.16MB | Low |
| **visx** | Custom/brand-specific visualizations | ~12.3KB | High |
| **Chart.js** | Large datasets (up to 1M points) | 14-48KB | Low |
| **D3** | Full control, custom viz libraries | Varies | Very High |

```
Need it fast with standard charts?         -> Recharts
Need rich chart types + theming?           -> Nivo
Need web + React Native?                   -> Victory
Need pixel-perfect custom viz?             -> visx
Need to render 100K+ data points?          -> Chart.js (Canvas)
Need full control?                         -> D3 directly
```

### Recharts Example

```tsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function RevenueChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="month" />
        <YAxis tickFormatter={(v) => `$${v / 1000}k`} />
        <Tooltip formatter={(v) => [`$${v.toLocaleString()}`, 'Revenue']} />
        <Bar dataKey="revenue" fill="#4e79a7" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

---

## 6. Data-Ink Ratio (Tufte Principles)

### Core Rules
1. **Above all else, show the data.**
2. **Maximize data-ink ratio** = (ink used for data) / (total ink).
3. **Erase non-data-ink** -- gridlines, borders, backgrounds that carry no information.
4. **Erase redundant data-ink** -- if a label says "42%", you don't also need a gridline at 42.

### Remove (Chartjunk)
3D effects, gradient fills, heavy gridlines, decorative icons, redundant legends, box borders around charts, background colors (unless encoding data).

### Add
Direct labels on bars/lines, annotations on key events, reference lines (target, average, benchmark).

### Small Multiples
Instead of one cluttered multi-series chart, repeat the same simple chart for each category. Same axes, same scale, side by side.

### Sparklines
Word-sized graphics embedded inline. No axes, no labels -- pure trend.

```tsx
<ResponsiveContainer width={80} height={20}>
  <LineChart data={trend}>
    <Line type="monotone" dataKey="value" stroke="#4e79a7" dot={false} strokeWidth={1.5} />
  </LineChart>
</ResponsiveContainer>
```

Use in: KPI cards, table cells, inline with text.
