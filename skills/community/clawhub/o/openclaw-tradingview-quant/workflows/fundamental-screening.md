---
description: Fundamental Screening Workflow - Use multiple columnsets to screen value stocks
---

# Fundamental Screening Workflow

Use `tradingview_get_leaderboard` with various columnsets (valuation/profitability/dividends/balance_sheet/income_statement/cash_flow) to screen quality stocks from a fundamental perspective.

## Execution Steps

### Step 1: Determine Screening Strategy

Determine screening strategy based on user needs:

| Strategy | Core Columnset | Key Metrics |
|----------|---------------|-------------|
| Value Investing | valuation | Low PE, Low PB, Low PS |
| High Dividend | dividends | High dividend yield, stable dividends |
| Growth Stocks | profitability + income_statement | High ROE, revenue growth |
| Financial Health | balance_sheet + cash_flow | Low debt ratio, ample cash flow |

### Step 2: Get Metadata

```
tradingview_get_metadata(type='markets')        # Get market_code
tradingview_get_metadata(type='columnsets')      # Confirm available columnsets
```

### Step 3: Get Leaderboard Data (Multiple Columnsets)

Call based on strategy combination, using value investing as example:

```
# Get valuation data
tradingview_get_leaderboard(
  asset_type='stocks', tab='all-stocks',
  market_code='china', columnset='valuation', count=100
)

# Get profitability data
tradingview_get_leaderboard(
  asset_type='stocks', tab='all-stocks',
  market_code='china', columnset='profitability', count=100
)

# Get dividend data
tradingview_get_leaderboard(
  asset_type='stocks', tab='high-dividend',
  market_code='china', columnset='dividends', count=50
)
```

### Step 4: Cross-Filter

Cross-filter results from multiple columnsets:

**Value Investing Filter Example**:
- PE < 20 (reasonable valuation)
- PB < 3 (asset discount)
- ROE > 15% (strong profitability)
- Dividend yield > 2% (dividend protection)

**Growth Stock Filter Example**:
- Revenue YoY growth > 20%
- Net profit growth > 15%
- ROE > 20%
- Gross margin > 40%

### Step 5: Technical Validation

For top candidates (5-10), call individually:

```
tradingview_get_ta(symbol, include_indicators=true)
```

Filter out stocks with obviously weak technicals (e.g., RSI > 80 overbought, MACD death cross).

### Step 6: Generate Screening Report

```markdown
# Fundamental Screening Results - [Strategy Name]

## Screening Criteria
- [List all criteria]

## Qualified Stocks (Total: N)

| Rank | Stock | PE | PB | ROE | Dividend Yield | Technical Score |
|------|-------|----|----|-----|----------------|-----------------|
| 1 | ... | ... | ... | ... | ... | ... |

## Detailed Analysis (Top 5)
### 1. [Stock Name]
- Valuation: ...
- Profitability: ...
- Technical: ...
- Buy recommendation: ...
```

## Common Screening Combinations

### High Dividend Strategy
```
tab='high-dividend' + columnset='dividends' → Dividend yield ranking
Cross with columnset='profitability' → Confirm sustainable earnings
Cross with columnset='balance_sheet' → Confirm financial health
```

### Low Valuation Strategy
```
tab='all-stocks' + columnset='valuation' → PE/PB ranking
Cross with columnset='income_statement' → Confirm revenue and profit
Cross with columnset='cash_flow' → Confirm cash flow
```

### Blue Chip Strategy
```
tab='large-cap' + columnset='profitability' → Large-cap high ROE
Cross with columnset='performance' → Confirm performance trend
Cross with columnset='dividends' → Dividend protection
```
