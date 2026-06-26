---
name: model-pricing-calculator
description: "This skill should be used when the user needs to fetch AI model pricing data from multiple API platforms, calculate model ratios, completion ratios, and group ratios based on a unified pricing formula, and output the results in a standardized JSON format."
---

# Model Pricing Calculator

A skill for fetching AI model pricing data from configured platform APIs and computing
standardized pricing ratios (model ratio, completion ratio, group ratio).

## When to Use

- Fetching model pricing information from AI API aggregation platforms
- Computing model ratios, completion ratios, and group ratios from raw pricing data
- Unifying pricing across multiple platforms using a consistent model ratio + group ratio scheme
- Reverse-calculating ratio configurations from target input/output prices
- Adding new pricing source URLs to the configuration

## Core Concepts

### Pricing Formula

```
Base price: $0.002 / 1K tokens (1 USD = 500,000 quota)

Mode 1 - Ratio-based (per-token):
  Cost = (InputTokens + OutputTokens × CompletionRatio) × ModelRatio × GroupRatio

Mode 2 - Fixed price (per-call, higher priority):
  Cost = ModelPrice(USD) × 500,000 × GroupRatio
```

### Reverse Calculation

```
ModelRatio = InputPrice_per_1K / 0.002
CompletionRatio = OutputPrice_per_1K / InputPrice_per_1K
```

## Workflow

### Step 1: Check and Update URL Configuration

Read `references/pricing_urls.json` to verify configured platform URLs. To add a new
platform, append a new entry with `name`, `pricing_page`, and `api_endpoint` fields.

The API endpoints typically follow the pattern `{base_url}/api/pricing` for platforms
built on New API / One API systems.

### Step 2: Fetch and Calculate Ratios

Run the calculation script:

```bash
python scripts/fetch_and_calculate.py
```

Options:
- `--urls-file <path>` — custom URL config file path
- `--output-dir <path>` — save results as separate JSON files to the specified directory
- `--verify` — print a price verification table showing actual prices per group
- `--no-snapshot` — skip snapshot saving and diff comparison
- `--models <patterns>` — filter by model names, comma-separated, supports wildcard `*` (e.g. `gpt-4*,claude-*`)
- `--groups <patterns>` — filter by group names, comma-separated, supports wildcard `*` (e.g. `default,aws*`)
- `--source <patterns>` — filter by data source name, comma-separated, supports wildcard `*` (e.g. `PackyAPI` or `12AI,Packy*`). Names correspond to `name` field in `pricing_urls.json`

The script will:
1. Fetch pricing data from each configured API endpoint
2. Extract model ratios, completion ratios, and group ratios
3. Unify duplicate models across platforms (first-source wins for ratios)
4. Apply `--models` / `--groups` filters if specified (supports wildcard `*`)
5. Output results in three standardized JSON blocks
6. Compare with previous snapshot (if exists, skipped in filter mode) and report any additions, removals, or value changes
7. Save current data as `data/latest_snapshot.json` (skipped in filter mode to avoid partial data overwriting full snapshot)

#### Filter Examples

Query specific models only:
```bash
python scripts/fetch_and_calculate.py --models "gpt-4*,claude-opus*"
```

Query specific groups only:
```bash
python scripts/fetch_and_calculate.py --groups "default,aws"
```

Combine both filters:
```bash
python scripts/fetch_and_calculate.py --models "gpt-4o*" --groups "default,gemini*"
```

Query from a specific data source only:
```bash
python scripts/fetch_and_calculate.py --source "PackyAPI"
```

Combine source, model and group filters:
```bash
python scripts/fetch_and_calculate.py --source "PackyAPI" --models "claude-*" --groups "aws*"
```

> **Note**: When `--models`, `--groups`, or `--source` is used, snapshot saving and diff comparison are automatically skipped to prevent partial data from overwriting the complete snapshot.

### Step 3: Review Output Format

The output strictly follows this exact structure with 3 JSON blocks:

```
（1）模型倍率
{
  "claude-haiku-4-5-20251001": 1,
  "claude-opus-4-5-20251101": 2.5,
  "claude-opus-4-6": 2.5
}
（2）模型补全倍率
{
  "claude-haiku-4-5-20251001": 5,
  "claude-opus-4-5-20251101": 5,
  "claude-opus-4-6": 5
}
（3）分组倍率
{
  "default": 1.2,
  "aws": 2,
  "gemini": 0.6,
  "gemini-1": 3
}
```

### Step 4: Snapshot and Diff

Each run automatically:
- Loads the previous snapshot from `data/latest_snapshot.json` (if it exists)
- Compares current results with the previous snapshot
- Reports all differences: added models, removed models, and changed values
- Overwrites the snapshot with the latest data

The diff report format:

```
============================================================
与上次数据对比（上次保存时间: 2025-03-23 10:00:00）
============================================================
  模型倍率:
    【新增 2 项】
      + new-model-a: 1.5
      + new-model-b: 2.0
    【删除 1 项】
      - old-model-x: 0.8
    【数值变化 1 项】
      * gpt-5: 0.625 → 0.75
  模型补全倍率: 无变化
  分组倍率: 无变化
```

Use `--no-snapshot` to skip this behavior.

### Step 5: Cross-Platform Unification Strategy

When the same model appears on multiple platforms:
- Model ratio and completion ratio remain **identical** across platforms
- Price differences are controlled through **group ratios** assigned to each platform/channel
- Each platform's pricing channel corresponds to a specific group in the `group_ratio` map

For detailed pricing rules and formulas, refer to `references/pricing_rules.md`.

## Bundled Resources

| Resource | Purpose |
|----------|---------|
| `scripts/fetch_and_calculate.py` | Main script for data fetching, ratio calculation, snapshot and diff |
| `references/pricing_urls.json` | Platform URL configuration (add new sources here) |
| `references/pricing_rules.md` | Detailed pricing calculation rules and output format spec |
| `data/latest_snapshot.json` | Auto-generated snapshot of the latest run (created after first run) |
