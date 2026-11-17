# Tables and charts

Charts arrived in iA Presenter 1.6 ("Charts and Tables"). Any Markdown table becomes a
chart by adding metadata lines **immediately after the table** (no blank line). The
in-app Inspector (Format → Table and Charts) writes the same metadata for you. Rendering
uses billboard.js/d3 inside the engine (`infographics.js`).

## Example (verified: `Chart`, `Orientation`, `bar-type`, `yLabel`)

```
| Quarter | Revenue | Cost |
| :------ | ------: | ---: |
| Q1      | 10      | 6    |
| Q2      | 15      | 8    |
| Q3      | 25      | 12   |
Chart: bar
Orientation: horizontal
bar-type: stacked
yLabel: Millions
```

First column = categories (x axis); each further column = one series (legend entry).
Keep numbers plain (no units inside the cells).

## Keys

| Key | Values | Notes |
|---|---|---|
| `Chart` | `bar` \| `line` \| `pie` \| `donut` | required to turn the table into a chart |
| `Orientation` | `vertical` (default) \| `horizontal` | bar charts; horizontal = rotated (`is-rotated`) |
| `bar-type` | `stacked` \| (omit = separated) | stacked bars (`is-stacked`) |
| `line-type` | `step` \| (omit = normal) | stepped line (`is-step`); the Inspector action is "Steps" – the exact value is not verified, let the Inspector write it once and copy the result |
| `Color-Type` | `sequential` \| `differential` \| (omit = categorical accents) | sequential = shades of one color; differential = positive/negative coloring |
| `xLabel` | text | x-axis label |
| `yLabel` | text | y-axis label |
| `xFormat` | `date` \| `number` \| `percent` | x-axis value formatting |
| `colors` | comma-separated colors (format not verified) | override series colors (theme accents by default) |
| `Caption` | text | caption under the chart/table (or `[Caption]` line) |

Keys are case-insensitive (`chart:`, `Chart:`, `yLabel:`, `ylabel:` …).

## Theme integration

Series colors come from the theme: `--graph-data-0` … `--graph-data-7` (set per
`section`, `section.light`, `section.dark`), `--sequential-color`,
`--differential-color-positive/negative`, `--graph-font-family`, `--graph-font-size`,
`--graph-background`. Copenhagen uses pastels, New York bold colors. Themes with
`"CssClasses": "… has-graph-background"` draw charts on a white card.

## Limits

- Only bar, line, pie, donut. No scatter, radar, gauges, combos.
- PPTX export keeps tables (basic borders) but chart fidelity is limited; PDF/HTML/
  images export render charts as shown.
- A TABbed table is a code block, not a table (and therefore never a chart).
