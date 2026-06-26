# openclaw-ggsql

OpenClaw skill for generating charts from tabular data using ggsql SQL syntax.

## Overview

ggsql extends SQL with visualization capabilities based on the Grammar of Graphics. This skill provides a structured way to generate ggsql SQL from YAML input specifications.

## Installation

Install as an OpenClaw skill:

```bash
# Clone to skills directory
cd ~/.openclaw/skills/
git clone https://github.com/fanzhidongyzby/openclaw-ggsql.git
```

## Usage

### Input YAML

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

### Generated SQL

```sql
SELECT * FROM 'penguins.csv'
VISUALISE bill_length_mm AS x, bill_depth_mm AS y, species AS fill
DRAW point
LABEL
  title => 'Penguin Bill Dimensions',
  x => 'Bill Length (mm)',
  y => 'Bill Depth (mm)'
```

### Execute

Use ggsql WASM playground: https://ggsql.org/wasm/

## Chart Types

| Type | Template | Required Mapping |
|------|----------|------------------|
| Scatter | templates/scatter.sql | x, y |
| Line | templates/line.sql | x, y |
| Bar | templates/bar.sql | x, y |
| Histogram | templates/histogram.sql | x |
| Boxplot | templates/boxplot.sql | x, y |
| Heatmap | templates/heatmap.sql | x, y, fill |

## Resources

- [ggsql Official](https://ggsql.org)
- [Syntax Docs](https://ggsql.org/syntax/)
- [Gallery](https://ggsql.org/gallery/)
- [GitHub](https://github.com/posit-dev/ggsql)

## License

MIT
