# Reusable Components

These components are placed inside `.slide-content` of Content Slides. Always add `class="reveal"` to the component wrapper for entrance animation.

All components use CSS custom properties for colors, so they automatically adapt to any brand preset.

---

## 1. Metrics Grid

3-column KPI cards with label, large value, and change indicator. Great for dashboards, status updates, quarterly metrics.

```html
<div class="metrics-grid reveal">
    <div class="metric-card">
        <span class="metric-label">Label</span>
        <span class="metric-value">7,800+</span>
        <span class="metric-change positive">+12.5% vs last period</span>
    </div>
    <div class="metric-card">
        <span class="metric-label">Label</span>
        <span class="metric-value">3,200+</span>
        <span class="metric-change negative">-8.3% vs target</span>
    </div>
    <div class="metric-card">
        <span class="metric-label">Label</span>
        <span class="metric-value">34%</span>
        <span class="metric-change neutral">Stable</span>
    </div>
</div>
```

### CSS

```css
.metrics-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: clamp(8px, 1.2vw, 16px); width: 100%;
}
.metric-card {
    background: var(--bg-secondary);
    border-radius: clamp(6px, 0.8vw, 12px);
    padding: clamp(10px, 1.5vh, 20px) clamp(10px, 1.2vw, 18px);
    display: flex; flex-direction: column; gap: clamp(3px, 0.5vh, 8px);
    border-left: 3px solid var(--accent);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
.metric-label { font-family: var(--font-body); font-size: var(--small-size); color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.metric-value { font-family: var(--font-display); font-size: var(--cta-size); font-weight: 900; color: var(--color-heading); line-height: 1; }
.metric-change { font-family: var(--font-body); font-size: var(--small-size); font-weight: 600; }
.metric-change.positive { color: #16803c; }
.metric-change.negative { color: #dc2626; }
.metric-change.neutral { color: var(--text-muted); }
```

---

## 2. Comparison Table with Insights

2-column layout: left is a comparison table, right is insight cards. Best for period-over-period metrics, bi-weekly/quarterly comparisons.

```html
<div class="comparison-grid reveal">
    <div class="comparison-table-wrap">
        <div class="comparison-table-caption">Comparison Table</div>
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>Section</th><th>Metric</th>
                    <th class="num">Period 1</th><th class="num">Period 2</th>
                    <th class="num">&Delta;</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="section-cell" rowspan="2">Group A</td>
                    <td>Metric 1</td>
                    <td class="num">2,121</td><td class="num">2,349</td>
                    <td class="num delta-pos">+10.7%</td>
                </tr>
                <tr>
                    <td>Metric 2</td>
                    <td class="num">65,219</td><td class="num">74,826</td>
                    <td class="num delta-pos">+14.7%</td>
                </tr>
                <tr class="section-divider">
                    <td class="section-cell" rowspan="2">Group B</td>
                    <td>Metric 3</td>
                    <td class="num">1,253,158</td><td class="num">993,785</td>
                    <td class="num delta-neg">&minus;20.7%</td>
                </tr>
                <tr>
                    <td class="indent">Sub-metric</td>
                    <td class="num">222,879</td><td class="num">261,876</td>
                    <td class="num delta-pos">+17.5%</td>
                </tr>
            </tbody>
        </table>
        <div class="comparison-source">Source: ...</div>
    </div>
    <div class="comparison-insights">
        <div class="insight-card">
            <span class="insight-num">01 &middot; Theme</span>
            <span class="insight-title">Key Insight Headline</span>
            <p class="insight-body">Narrative with <span class="pos">+10.7%</span> inline.</p>
        </div>
        <!-- Up to 3 insight cards -->
    </div>
</div>
```

Key CSS classes: `.comparison-grid` (2-column grid), `.comparison-table`, `.insight-card`, `.delta-pos`, `.delta-neg`, `.pos`, `.neg`.

---

## 3. Feature / Scope Table

General-purpose table for feature comparisons, scope definitions, capability matrices.

```html
<table class="data-table reveal">
    <thead>
        <tr><th>Column 1</th><th>Column 2</th><th>Column 3</th></tr>
    </thead>
    <tbody>
        <tr>
            <td class="row-label">Row Label</td>
            <td>Value</td>
            <td>Value</td>
        </tr>
    </tbody>
</table>
```

### CSS

```css
.data-table { width: 100%; border-collapse: separate; border-spacing: 0; font-family: var(--font-body); }
.data-table thead th {
    font-family: var(--font-display); font-weight: 700; font-size: var(--small-size);
    color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;
    padding: clamp(6px, 1vh, 12px) clamp(8px, 1vw, 14px);
    border-bottom: 2px solid var(--color-heading);
}
.data-table tbody td {
    padding: clamp(6px, 1vh, 12px) clamp(8px, 1vw, 14px);
    border-bottom: 1px solid var(--border-card);
}
.data-table tbody tr:hover { background: var(--bg-secondary); }
.row-label { font-weight: 600; color: var(--color-heading); }
```

---

## 4. Two-Column Grid (Findings vs Actions / Pros vs Cons)

2-column layout for problem/solution, pros/cons, before/after, findings/actions.

```html
<div class="two-col-grid reveal">
    <div class="col-block col-left">
        <h3>Left Column Title</h3>
        <ul class="col-list">
            <li>Point 1</li>
            <li>Point 2</li>
        </ul>
    </div>
    <div class="col-block col-right">
        <h3>Right Column Title</h3>
        <ul class="col-list">
            <li>Point 1</li>
            <li>Point 2</li>
        </ul>
    </div>
</div>
```

### CSS

```css
.two-col-grid { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(10px, 1.5vw, 20px); width: 100%; }
.col-block h3 { margin-bottom: clamp(6px, 1vh, 12px); padding-bottom: clamp(4px, 0.6vh, 8px); border-bottom: 2px solid var(--color-heading); }
.col-left h3 { color: #dc2626; border-color: #dc2626; }
.col-right h3 { color: #16803c; border-color: #16803c; }
.col-list { list-style: none; display: flex; flex-direction: column; gap: clamp(4px, 0.8vh, 10px); }
.col-list li {
    font-family: var(--font-body); font-size: var(--body-size);
    color: var(--text-secondary); line-height: 1.45;
    padding-left: clamp(12px, 1.5vw, 18px); position: relative;
}
.col-list li::before {
    content: ''; position: absolute; left: 0; top: clamp(5px, 0.7vh, 7px);
    width: clamp(5px, 0.5vw, 7px); height: clamp(5px, 0.5vw, 7px); border-radius: 50%;
}
.col-left .col-list li::before { background: #fca5a5; }
.col-right .col-list li::before { background: #86efac; }
```

**Tip:** The left/right color scheme (red/green) is the default for Findings vs Actions. For neutral comparisons (e.g., Option A vs Option B), use `color: var(--color-heading); border-color: var(--color-heading);` on both columns.

---

## 5. Action List

Vertical list of items with owner labels and descriptions. Works for action items, decisions, scope items, roadmap entries.

```html
<div class="action-list reveal">
    <div class="action-item">
        <span class="action-owner">Owner / Label</span>
        <span class="action-desc">Description of the item.</span>
    </div>
</div>
```

### CSS

```css
.action-list { list-style: none; display: flex; flex-direction: column; gap: clamp(6px, 1vh, 14px); width: 100%; }
.action-item {
    display: flex; align-items: flex-start; gap: clamp(8px, 1.2vw, 16px);
    padding: clamp(8px, 1.2vh, 16px) clamp(10px, 1.5vw, 20px);
    background: var(--bg-secondary); border-radius: clamp(6px, 0.8vw, 10px);
    border-left: 3px solid var(--accent);
}
.action-owner { font-family: var(--font-display); font-size: var(--small-size); font-weight: 700; color: var(--accent); white-space: nowrap; min-width: clamp(80px, 10vw, 130px); }
.action-desc { font-family: var(--font-body); line-height: 1.5; }
```

---

## 6. Timeline

Vertical timeline with dots, dates, and descriptions. Use for roadmaps, project phases, milestones.

```html
<div class="timeline reveal">
    <div class="timeline-step">
        <div class="timeline-dot"></div>
        <div class="timeline-step-header">
            <h4>Milestone Title</h4>
            <span class="timeline-date">Q2 2026</span>
        </div>
        <p class="timeline-desc">Description.</p>
    </div>
</div>
```

### CSS

```css
.timeline { display: flex; flex-direction: column; position: relative; padding-left: clamp(16px, 2.5vw, 32px); }
.timeline::before {
    content: ''; position: absolute;
    left: clamp(5px, 0.7vw, 10px); top: clamp(6px, 1vh, 10px); bottom: clamp(6px, 1vh, 10px);
    width: 2px; background: linear-gradient(to bottom, var(--accent), var(--color-heading));
}
.timeline-dot {
    width: clamp(10px, 1.2vw, 14px); height: clamp(10px, 1.2vw, 14px);
    border-radius: 50%; background: var(--accent); flex-shrink: 0;
    position: absolute; z-index: 2;
}
.timeline-date { font-family: var(--font-body); font-size: var(--small-size); color: var(--accent); font-weight: 600; }
```

---

## 7. Status Badge

Inline status indicators for tables or lists.

```html
<span class="status-badge on-track">On Track</span>
<span class="status-badge at-risk">At Risk</span>
<span class="status-badge done">Done</span>
<span class="status-badge pending">Pending</span>
```

```css
.status-badge {
    display: inline-block;
    padding: clamp(2px, 0.3vh, 4px) clamp(6px, 0.8vw, 12px);
    border-radius: 100px; font-size: var(--small-size); font-weight: 600;
}
.status-badge.on-track { background: #dcfce7; color: #16803c; }
.status-badge.at-risk { background: #fef2f2; color: #dc2626; }
.status-badge.done { background: #dbeafe; color: #1d4ed8; }
.status-badge.pending { background: #f3f4f6; color: #6b7280; }
```

---

## 8. Screenshot Slot

Replaceable, croppable image placeholder for embedding operational screenshots into slides. Shows a dashed placeholder with label when `src` is empty; displays the image when `src` is set.

```html
<div class="screenshot-slot reveal">
    <img src="" alt="Description">
    <div class="screenshot-label">Screenshot: Description (replace src to update)</div>
</div>
```

To update: set `src` to a local file path, URL, or base64 data URI. Use `object-position` on the `img` for cropping.

```html
<!-- With image -->
<div class="screenshot-slot reveal">
    <img src="path/to/screenshot.png" alt="Create dialog" style="object-position: top left;">
    <div class="screenshot-label">Screenshot: Create Skill</div>
</div>
```

### CSS

```css
.screenshot-slot {
    width: 100%; max-height: 42vh;
    border: 2px dashed var(--border-card); border-radius: clamp(6px, 0.8vw, 12px);
    overflow: hidden; position: relative;
    display: flex; align-items: center; justify-content: center;
    background: var(--bg-secondary); margin-top: var(--element-gap);
}
.screenshot-slot img {
    width: 100%; height: 100%; object-fit: contain; display: block;
}
.screenshot-slot img[src=""], .screenshot-slot img:not([src]) { display: none; }
.screenshot-slot .screenshot-label {
    position: absolute; font-family: var(--font-body); font-size: var(--small-size);
    color: var(--text-muted); text-align: center;
    padding: clamp(20px, 4vh, 40px);
}
.screenshot-slot img[src]:not([src=""]) ~ .screenshot-label { display: none; }
```

### Usage Notes

- The label auto-hides when an image `src` is provided
- Adjust `max-height` to fit slide layout (default 42vh)
- Use `object-position` CSS on `img` for cropping (e.g., `object-position: top center`)
- Use `object-fit: cover` instead of `contain` for full-bleed cropping
- For bilingual labels, use `<span class="lang-en">...</span><span class="lang-cn">...</span>` inside `.screenshot-label`
