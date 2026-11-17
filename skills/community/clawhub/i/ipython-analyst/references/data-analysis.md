# Data Analysis Reference

Loading, cleaning, transforming, and visualizing data with pandas + numpy + matplotlib + seaborn. **Load this reference when the user wants to analyze a CSV/Excel/JSON file, compute statistics, or produce a diagnostic chart.**

## Loading Data

```python
import pandas as pd
import numpy as np

# CSV
df = pd.read_csv('/home/z/my-project/upload/data.csv')

# Excel (multiple sheets → dict of DataFrames)
df = pd.read_excel('/home/z/my-project/upload/data.xlsx', sheet_name='Sheet1')
all_sheets = pd.read_excel('/home/z/my-project/upload/data.xlsx', sheet_name=None)

# JSON (nested → use json_normalize)
import json
with open('/home/z/my-project/upload/data.json') as f:
    raw = json.load(f)
df = pd.json_normalize(raw)

# Large CSV (streaming — see references/distributed.md)
chunk_iter = pd.read_csv('/home/z/my-project/upload/huge.csv', chunksize=50_000)
for chunk in chunk_iter:
    process(chunk)
```

### Smart loading for messy data
```python
# Auto-detect separator
with open('/home/z/my-project/upload/data.csv') as f:
    first_line = f.readline()
sep = ',' if ',' in first_line else '\t' if '\t' in first_line else ';'
df = pd.read_csv(path, sep=sep)

# Handle encoding issues
df = pd.read_csv(path, encoding='utf-8', errors='replace')
# Or try common encodings
for enc in ['utf-8', 'latin-1', 'cp1252']:
    try:
        df = pd.read_csv(path, encoding=enc)
        break
    except UnicodeDecodeError:
        continue

# Parse dates on load
df = pd.read_csv(path, parse_dates=['created_at', 'updated_at'])

# Lower memory: use category dtype for low-cardinality strings
df = pd.read_csv(path, dtype={'category_col': 'category'})
```

## Quick Exploration

```python
# Shape and types
print(df.shape)         # (rows, cols)
print(df.dtypes)        # column types
print(df.head(10))      # first 10 rows
print(df.describe())    # numeric summary
print(df.describe(include='all'))  # include categoricals

# Missing values
print(df.isnull().sum())
print(df.isnull().sum() / len(df))  # percentage missing

# Unique values per column
print(df.nunique())

# Value counts for categoricals
print(df['category'].value_counts())
print(df['category'].value_counts(normalize=True))
```

## Cleaning Patterns

```python
# Standardize column names (lowercase, underscores)
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

# Strip whitespace from string columns
str_cols = df.select_dtypes(include='object').columns
df[str_cols] = df[str_cols].apply(lambda s: s.str.strip())

# Convert dtypes (pandas 1.0+)
df = df.convert_dtypes()  # auto-convert to best dtype
# Or specific
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # invalid → NaT
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # invalid → NaN

# Handle missing values
df = df.dropna(subset=['required_col'])  # drop rows missing required field
df['optional_col'] = df['optional_col'].fillna(df['optional_col'].median())
df['category'] = df['category'].fillna('unknown')

# Remove duplicates
df = df.drop_duplicates()
df = df.drop_duplicates(subset=['id'], keep='last')
```

## Aggregation Patterns

```python
# Group by + aggregate
summary = df.groupby('category').agg(
    count=('id', 'count'),
    total=('amount', 'sum'),
    avg=('amount', 'mean'),
    median=('amount', 'median'),
).reset_index()

# Multi-level groupby
pivot = df.groupby(['category', 'region'])['amount'].sum().unstack(fill_value=0)

# Rolling window
df['7d_avg'] = df.set_index('date')['amount'].rolling('7D').mean().values

# Cumulative
df['cumsum'] = df['amount'].cumsum()
df['cummax'] = df['amount'].cummax()
```

## Visualization (Diagnostic — For Publication Charts Use the `charts` Skill)

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Register Chinese fonts if any labels might be CJK
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

import seaborn as sns
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# CRITICAL: use constrained_layout=True, NOT tight_layout()
# Pick ONE layout engine per figure — they conflict if combined.
fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)

# Top-left: distribution
sns.histplot(df['amount'], kde=True, ax=axes[0, 0])
axes[0, 0].set_title('Distribution of Amount')

# Top-right: by category
df.groupby('category')['amount'].sum().plot.bar(ax=axes[0, 1])
axes[0, 1].set_title('Total by Category')
axes[0, 1].tick_params(axis='x', rotation=45)

# Bottom-left: time series
df.set_index('date')['amount'].plot(ax=axes[1, 0])
axes[1, 0].set_title('Amount Over Time')

# Bottom-right: correlation heatmap
numeric = df.select_dtypes(include='number')
sns.heatmap(numeric.corr(), annot=True, cmap='coolwarm', center=0, ax=axes[1, 1])
axes[1, 1].set_title('Correlation Matrix')

plt.savefig('/home/z/my-project/download/eda_summary.png', dpi=150)
```

### Layout rules (mandatory)
- Pass `constrained_layout=True` to `plt.subplots()` or `plt.figure()`.
- Do NOT also call `plt.tight_layout()`, `subplots_adjust(...)`, or pass `bbox_inches='tight'` to `savefig()` — these conflict with `constrained_layout` and silently break its margin computation.
- For legends outside the plot area, use `bbox_to_anchor=(1.05, 1)` and `loc='upper left'`. Don't use `loc='best'` — it can place the legend on top of data.
- Match the user's language for all labels (title, xlabel, ylabel, legend entries, tick labels for categorical axes).

## Common Pitfalls

### SettingWithCopyWarning
```python
# BAD — chained assignment, may not work
df[df['x'] > 0]['y'] = 1

# GOOD — use .loc
df.loc[df['x'] > 0, 'y'] = 1

# Or explicit copy
subset = df[df['x'] > 0].copy()
subset['y'] = 1
```

### Memory usage on large DataFrames
```python
# Check actual memory (deep=True accounts for object dtype)
print(df.memory_usage(deep=True).sum() / 1024 / 1024, 'MB')

# Reduce by downcasting numerics
for col in df.select_dtypes(include='int').columns:
    df[col] = pd.to_numeric(df[col], downcast='integer')
for col in df.select_dtypes(include='float').columns:
    df[col] = pd.to_numeric(df[col], downcast='float')

# Convert low-cardinality strings to category
for col in df.select_dtypes(include='object').columns:
    if df[col].nunique() / len(df) < 0.5:
        df[col] = df[col].astype('category')
```

### Time zone handling
```python
# Localize naive timestamps
df['ts'] = pd.to_datetime(df['ts']).dt.tz_localize('UTC')
# Convert to local
df['ts_local'] = df['ts'].dt.tz_convert('Asia/Shanghai')
# Strip tz for storage
df['ts_naive'] = df['ts_local'].dt.tz_localize(None)
```

## Output

```python
# CSV (no index)
df.to_csv('/home/z/my-project/download/result.csv', index=False, encoding='utf-8-sig')
# utf-8-sig includes BOM — Excel opens it correctly with CJK chars

# Excel with multiple sheets
with pd.ExcelWriter('/home/z/my-project/download/result.xlsx') as writer:
    df.to_excel(writer, sheet_name='data', index=False)
    summary.to_excel(writer, sheet_name='summary', index=False)

# Parquet (efficient columnar)
df.to_parquet('/home/z/my-project/download/result.parquet')

# JSON (records orientation is most portable)
df.to_json('/home/z/my-project/download/result.json', orient='records', force_ascii=False, indent=2)
```
