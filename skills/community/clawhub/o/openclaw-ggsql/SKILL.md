---
name: openclaw-ggsql
description: "Generate charts from tabular data using ggsql SQL syntax extension. Use when: user wants to visualize data as charts without Python/R. Supports: scatter plots, line charts, bar charts, histograms, boxplots, heatmaps. Based on Grammar of Graphics."
homepage: https://ggsql.org
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": [], "skills": ["web-access"] } } }
---

# ggsql Visualization Skill

Generate charts from tabular data using ggsql SQL syntax.

## Overview

ggsql extends SQL with visualization capabilities based on the Grammar of Graphics. Write familiar SQL queries, add visualization clauses, and get charts - no Python/R needed.

## When to Use

✅ **USE this skill when:**

- "Visualize this data as a scatter plot"
- "Create a histogram of X"
- "Draw a bar chart comparing Y across categories"
- "Plot time series data"
- "Generate heatmap from table"
- User provides tabular data and wants a chart

## When NOT to Use

❌ **DON'T use this skill when:**

- Interactive/dynamic charts → use JavaScript libraries
- Complex statistical visualizations → use Python/R
- Large-scale data dashboards → use dedicated tools
- 3D visualizations → use specialized software

## Input Schema

```yaml
data: <CSV file path | JSON array | SQL table reference>
chart_type: point | line | bar | histogram | boxplot | violin | density | heatmap | pie
mapping:
  x: <column name>        # Required for most charts
  y: <column name>        # Required for point, line, bar, boxplot
  fill: <column name>     # Optional, for color encoding
  color: <column name>    # Optional, for stroke color
  shape: <column name>    # Optional, for point shapes
  size: <column name>     # Optional, for point sizes
options:
  title: <chart title>              # Optional
  subtitle: <chart subtitle>        # Optional
  x_label: <x-axis label>           # Optional
  y_label: <y-axis label>           # Optional
  binwidth: <number>                # For histogram
  facet: <column name>              # For small multiples
  facet_by: <column name>           # For 2D faceting
  scale_x: continuous | discrete | binned | log10
  scale_y: continuous | discrete | binned | log10
  scale_fill: continuous | discrete | binned
```

## Output

- SVG chart file (primary)
- PNG chart file (optional)
- Embedded base64 image for chat display

## Chart Types and Templates

### Scatter Plot (`point`)

**Required mapping**: `x`, `y`
**Optional mapping**: `fill`, `color`, `shape`, `size`

```sql
VISUALISE {x} AS x, {y} AS y, {fill} AS fill
FROM {data_source}
DRAW point
LABEL title => '{title}', x => '{x_label}', y => '{y_label}'
```

### Line Chart (`line`)

**Required mapping**: `x`, `y`
**Optional mapping**: `color`, `linetype`

```sql
VISUALISE {x} AS x, {y} AS y, {color} AS color
FROM {data_source}
DRAW line
LABEL title => '{title}', x => '{x_label}', y => '{y_label}'
```

### Bar Chart (`bar`)

**Required mapping**: `x`, `y` (or auto-count with just `x`)
**Optional mapping**: `fill`

```sql
SELECT {x}, COUNT(*) as count FROM {data_source}
GROUP BY {x}
VISUALISE {x} AS x, count AS y, {fill} AS fill
DRAW bar
LABEL title => '{title}', x => '{x_label}', y => '{y_label}'
```

### Histogram (`histogram`)

**Required mapping**: `x`
**Optional mapping**: `fill`, `binwidth`

```sql
VISUALISE {x} AS x, {fill} AS fill
FROM {data_source}
DRAW histogram
  SETTING binwidth => {binwidth}
LABEL title => '{title}', x => '{x_label}'
```

### Boxplot (`boxplot`)

**Required mapping**: `x`, `y` (x categorical, y numeric)
**Optional mapping**: `fill`

```sql
VISUALISE {x} AS x, {y} AS y, {fill} AS fill
FROM {data_source}
DRAW boxplot
LABEL title => '{title}', x => '{x_label}', y => '{y_label}'
```

### Heatmap (`tile`)

**Required mapping**: `x`, `y`, `fill`
**Optional mapping**: none

```sql
VISUALISE {x} AS x, {y} AS y, {fill} AS fill
FROM {data_source}
DRAW tile
SCALE BINNED fill
LABEL title => '{title}', x => '{x_label}', y => '{y_label}'
```

### Density Plot (`density`)

**Required mapping**: `x`
**Optional mapping**: `fill`

```sql
VISUALISE {x} AS x, {fill} AS fill
FROM {data_source}
DRAW density
LABEL title => '{title}', x => '{x_label}'
```

### Violin Plot (`violin`)

**Required mapping**: `x`, `y` (x categorical, y numeric)
**Optional mapping**: `fill`

```sql
VISUALISE {x} AS x, {y} AS y, {fill} AS fill
FROM {data_source}
DRAW violin
LABEL title => '{title}', x => '{x_label}', y => '{y_label}'
```

### Pie Chart (`pie` with polar projection)

**Required mapping**: `fill`
**Optional mapping**: none

```sql
SELECT {fill}, COUNT(*) as count FROM {data_source}
GROUP BY {fill}
VISUALISE {fill} AS fill, count AS y
DRAW bar
PROJECT polar
LABEL title => '{title}'
```

## Scale Types

| Scale | Use Case | Example |
|-------|----------|---------|
| `CONTINUOUS` | Numeric values | `SCALE CONTINUOUS x FROM [0, null]` |
| `DISCRETE` | Categories | `SCALE DISCRETE fill TO ['red', 'blue']` |
| `BINNED` | Binning continuous | `SCALE BINNED fill` |
| `ORDINAL` | Ordered categories | `SCALE ORDINAL x` |
| `IDENTITY` | Direct values | `SCALE IDENTITY color` |
| `log10` | Log transform | `SCALE CONTINUOUS y VIA log10` |

## Faceting (Small Multiples)

### 1D Faceting

```sql
VISUALISE {x} AS x, {y} AS y
FROM {data_source}
DRAW point
FACET {facet_column}
```

### 2D Faceting

```sql
VISUALISE {x} AS x, {y} AS y
FROM {data_source}
DRAW point
FACET {facet_column} BY {facet_by_column}
```

## Multi-layer Charts

Combine multiple `DRAW` clauses:

```sql
VISUALISE {x} AS x, {y} AS y
FROM {data_source}
DRAW line
  MAPPING {group} AS color
DRAW point
  MAPPING {group} AS fill
LABEL title => '{title}'
```

## Execution Methods

### Method 1: WASM Playground (Recommended for Testing)

1. Visit https://ggsql.org/wasm/
2. Use built-in datasets: `ggsql:penguins`, `ggsql:airquality`
3. Upload CSV via "Upload Data" button
4. Run SQL and save as SVG/PNG

### Method 2: CLI (Local Execution)

```bash
# Install
cargo install ggsql-cli

# Run
ggsql-cli run -f input.sql -o output.svg
```

### Method 3: Jupyter Kernel

```bash
uv tool install ggsql-jupyter
ggsql-jupyter --install
```

## Examples

### Example 1: Scatter Plot with Color

**Input**:
```yaml
data: penguins.csv
chart_type: point
mapping:
  x: bill_length_mm
  y: bill_depth_mm
  fill: species
options:
  title: Penguin Bill Dimensions
  x_label: Bill Length (mm)
  y_label: Bill Depth (mm)
```

**Generated SQL**:
```sql
SELECT * FROM 'penguins.csv'
VISUALISE bill_length_mm AS x, bill_depth_mm AS y, species AS fill
DRAW point
LABEL
  title => 'Penguin Bill Dimensions',
  x => 'Bill Length (mm)',
  y => 'Bill Depth (mm)'
```

### Example 2: Histogram

**Input**:
```yaml
data: sales.csv
chart_type: histogram
mapping:
  x: revenue
options:
  title: Revenue Distribution
  binwidth: 1000
```

**Generated SQL**:
```sql
SELECT * FROM 'sales.csv'
VISUALISE revenue AS x
DRAW histogram
  SETTING binwidth => 1000
LABEL title => 'Revenue Distribution'
```

### Example 3: Faceted Scatter Plot

**Input**:
```yaml
data: penguins.csv
chart_type: point
mapping:
  x: bill_length_mm
  y: bill_depth_mm
  fill: species
options:
  title: Penguins by Island
  facet: island
```

**Generated SQL**:
```sql
SELECT * FROM 'penguins.csv'
VISUALISE bill_length_mm AS x, bill_depth_mm AS y, species AS fill
DRAW point
FACET island
LABEL title => 'Penguins by Island'
```

### Example 4: Multi-layer Chart

**Input**:
```yaml
data: sales.csv
chart_type: multi
mapping:
  x: date
  y: revenue
  group: region
options:
  title: Revenue Trend by Region
```

**Generated SQL**:
```sql
SELECT * FROM 'sales.csv'
VISUALISE date AS x, revenue AS y
DRAW line
  MAPPING region AS color
DRAW point
  MAPPING region AS fill
LABEL title => 'Revenue Trend by Region'
```

## SQL Generation Logic

When receiving YAML input:

1. Parse `chart_type` to select template
2. Validate required mapping fields
3. Build `VISUALISE` clause from mapping
4. Add `DRAW` clause with layer type
5. Add optional clauses: `SCALE`, `FACET`, `LABEL`
6. If `data` is CSV, use `FROM 'path/to/file.csv'`
7. If `data` is table reference, use `FROM table_name`

## Notes

- ggsql is in alpha stage (v0.2.7), syntax may evolve
- WASM Playground is the easiest way to test
- No Python/R environment needed
- Charts are static (SVG/PNG), not interactive
- Grammar of Graphics philosophy: compose from layers, scales, coordinates

## Resources

- [Official Website](https://ggsql.org)
- [Syntax Documentation](https://ggsql.org/syntax/)
- [Example Gallery](https://ggsql.org/gallery/)
- [GitHub Repository](https://github.com/posit-dev/ggsql)
- [WASM Playground](https://ggsql.org/wasm/)
