# Data Literacy Engine

Complete data fluency — understanding, working with, analyzing, and communicating data at every level.

---

## 1. Data Types & Formats

### Primitive Types
| Type | Example | Operations |
|---|---|---|
| Integer | `42`, `-7`, `0` | Arithmetic, comparison |
| Float | `3.14`, `-0.001`, `1e6` | Arithmetic, rounding |
| String | `"hello"`, `'data'` | Concat, slice, search, replace |
| Boolean | `true`, `false` | Logic (AND, OR, NOT) |
| Null | `null`, `None`, `nil` | Existence checks |

### Composite Types
| Type | Structure | Use Case |
|---|---|---|
| Array/List | `[1, 2, 3]` | Ordered collections |
| Object/Dict | `{"key": "value"}` | Key-value records |
| Set | `{1, 2, 3}` | Unique items |
| Tuple | `(1, "a", true)` | Fixed records |

### Data Serialization Formats
| Format | Type | Best For | Size |
|---|---|---|---|
| JSON | Text | APIs, config | Medium |
| CSV | Text | Tabular data | Small |
| XML | Text | Legacy systems | Large |
| YAML | Text | Config, human-edit | Medium |
| Parquet | Binary | Analytics, columnar | Tiny |
| Avro | Binary | Streaming, schema | Small |
| Protobuf | Binary | RPC, performance | Tiny |
| MessagePack | Binary | Fast serialization | Small |

---

## 2. Data Structures in Practice

### Tabular Data (Rows × Columns)
The most common data shape. Think spreadsheets, SQL tables, CSV files.
```
| Name    | Age | City      | Score |
|---------|-----|-----------|-------|
| Alice   | 30  | NYC       | 95.2  |
| Bob     | 25  | LA        | 87.1  |
| Charlie | 35  | Chicago   | 91.8  |
```
- Each row = one record/observation
- Each column = one feature/variable
- Column types should be consistent

### Time Series Data
Data points indexed by time.
```
| Timestamp           | Value |
|---------------------|-------|
| 2026-04-01 00:00:00 | 42.1  |
| 2026-04-01 01:00:00 | 43.5  |
| 2026-04-01 02:00:00 | 41.8  |
```
- Regular intervals (hourly, daily, etc.)
- Trend analysis, seasonality, forecasting
- Tools: pandas, matplotlib, plotly

### Hierarchical/Nested Data
Tree structures: JSON, XML, file systems.
```json
{
  "company": "Acme",
  "departments": [
    {
      "name": "Engineering",
      "employees": [{"name": "Alice", "role": "Lead"}]
    }
  ]
}
```

### Graph/Network Data
Nodes and edges: social networks, dependencies, maps.
```
Nodes: [A, B, C, D]
Edges: [(A→B), (B→C), (A→C), (C→D)]
```

---

## 3. Statistical Literacy

### Descriptive Statistics
| Measure | What It Tells You | Formula |
|---|---|---|
| Mean | Average value | Σx / n |
| Median | Middle value | Sort → pick center |
| Mode | Most frequent | Count occurrences |
| Std Dev | Spread around mean | √(Σ(x-μ)² / n) |
| Variance | Squared spread | σ² |
| Range | Full spread | max - min |
| IQR | Middle 50% spread | Q3 - Q1 |
| Percentile | Position in distribution | Sort → interpolate |

### Probability Concepts
- **Probability**: P(A) = favorable / total outcomes
- **Conditional**: P(A|B) = P(A∩B) / P(B)
- **Bayes' Theorem**: P(A|B) = P(B|A) × P(A) / P(B)
- **Independence**: P(A∩B) = P(A) × P(B)

### Distributions
| Distribution | Shape | Use Case |
|---|---|---|
| Normal (Gaussian) | Bell curve | Heights, test scores, errors |
| Uniform | Flat | Random numbers, dice |
| Binomial | Skewed | Success/failure counts |
| Poisson | Right-skewed | Events per time period |
| Exponential | Decay | Time between events |

### Correlation vs Causation
- **Correlation**: Two things move together (r = -1 to +1)
- **Causation**: One thing causes the other (requires experiment)
- Correlation ≠ Causation (always)
- Confounding variables can create false correlations

---

## 4. Data Quality

### The 6 Dimensions
1. **Accuracy** — Does data reflect reality?
2. **Completeness** — Are there missing values?
3. **Consistency** — Same data across sources?
4. **Timeliness** — Is data current enough?
5. **Validity** — Does it conform to rules/schema?
6. **Uniqueness** — Are there duplicates?

### Common Data Issues
| Issue | Detection | Fix |
|---|---|---|
| Missing values | `isnull()`, `isna()` | Drop, fill (mean/median/mode), interpolate |
| Duplicates | `duplicated()` | `drop_duplicates()` |
| Outliers | Box plot, z-score > 3 | Cap, remove, or investigate |
| Wrong types | `dtype` check | Convert: `astype()`, `int()`, `str()` |
| Inconsistent formats | Regex, unique values | Normalize: `.lower()`, `.strip()`, regex |
| Encoding issues | Garbled text | Specify encoding: `utf-8`, `latin-1` |

### Data Cleaning Pipeline
```
Raw Data
  → Profile (understand shape, types, nulls)
  → Clean (fix types, handle nulls, remove dupes)
  → Validate (check ranges, formats, logic)
  → Transform (normalize, encode, scale)
  → Document (what changed and why)
```

---

## 5. Data Visualization

### Chart Selection Guide
| Question | Chart Type |
|---|---|
| Comparison between categories | Bar chart |
| Trend over time | Line chart |
| Part of whole | Pie chart (sparingly), stacked bar |
| Distribution | Histogram, box plot |
| Relationship | Scatter plot |
| Geographic | Choropleth, bubble map |
| Composition over time | Area chart, stacked bar |
| Multiple variables | Heatmap, parallel coordinates |

### Visualization Best Practices
- Label axes clearly with units
- Title should state the insight, not just describe
- Use color purposefully, not decoratively
- Start y-axis at zero for bar charts
- Avoid 3D charts (misleading)
- Gridlines help reading, not decoration
- Show data, not chartjunk
- Annotate significant points

### Python Quick Viz
```python
import matplotlib.pyplot as plt
import pandas as pd

# Line chart
df.plot(x='date', y='value', kind='line')
plt.title('Value Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.savefig('chart.png')

# Bar chart
df.groupby('category').size().plot(kind='bar')

# Scatter plot
plt.scatter(df['x'], df['y'], alpha=0.5)

# Histogram
df['score'].hist(bins=20)
```

---

## 6. Data Transformation

### Normalization & Scaling
- **Min-Max**: (x - min) / (max - min) → [0, 1]
- **Z-Score**: (x - mean) / std → mean=0, std=1
- **Log**: log(x) → compresses large ranges

### Encoding Categorical Data
- **Label Encoding**: Category → integer (A=0, B=1, C=2)
- **One-Hot Encoding**: Category → binary columns ([1,0,0], [0,1,0])
- **Ordinal Encoding**: Ordered categories → integers (Low=1, Med=2, High=3)

### Aggregation
```python
df.groupby('category').agg({
    'value': ['mean', 'sum', 'count'],
    'date': 'max'
})
```

### Pivoting & Reshaping
```python
# Long → Wide
df.pivot(index='date', columns='category', values='value')

# Wide → Long
df.melt(id_vars=['date'], value_vars=['A', 'B', 'C'])
```

---

## 7. Data Literacy Skills

### Reading Data
- Understand what each column represents
- Check data types match expectations
- Look at distribution (histogram)
- Spot anomalies (outliers, gaps)

### Interpreting Statistics
- "Average" could be mean, median, or mode — know which
- Sample size matters — 10 vs 10,000 observations
- Confidence intervals > point estimates
- p-value < 0.05 means "unlikely by chance" not "definitely true"

### Communicating Data
- Lead with the insight, not the method
- Use comparisons: "3× larger" > "300% increase"
- Round appropriately: "About 42%" not "42.37%"
- Show uncertainty: "between 40-44%" not just "42%"
- Tell the story: What happened? Why? What next?

### Data Ethics
- Privacy: anonymize personal data
- Bias: check for sampling bias, measurement bias
- Representation: does data reflect reality?
- Consent: was data collected with permission?
- Transparency: document methodology
