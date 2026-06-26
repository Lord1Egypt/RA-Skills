---
name: back-testing-predmarket
version: 1.0.2
description: Backtest Polymarket recommendation history. Fetches current market prices, computes P&L for each historical recommendation, evaluates returns by category and direction, and generates a strategy reflection report. Use when the user asks to backtest, evaluate performance, review returns, or analyze P&L of their Polymarket recommendations.
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["python3"]}}}
---

# Polymarket Recommendation Backtest

Evaluate the performance of all historical Polymarket recommendations by fetching live market prices, computing P&L for each position, analyzing returns by category and direction, and generating a strategy reflection report.

## Workflow

Execute the following 5 steps in order.

### Step 1: Run Backtest Script

Run the backtest script to parse history, fetch current prices, and compute P&L:

```bash
python3 scripts/backtest.py --output /tmp/backtest-results.json
```

The script:
1. Parses `~/polymarket-reports/recommendation-history.md` (all historical recommendations)
2. Scans `~/polymarket-reports/market-pulse-*.md` files to extract event slugs from URLs
3. Matches each recommendation to an event slug via fuzzy text matching
4. Fetches current prices from Polymarket Gamma API and CLOB midpoint API
5. Computes P&L for each position (unrealized for open markets, realized for settled)
6. Outputs structured JSON with per-position details and aggregate statistics

**Default paths:** `--history ~/polymarket-reports/recommendation-history.md`, `--reports-dir ~/polymarket-reports/`

If the script fails, check:
- Network connectivity to `gamma-api.polymarket.com` and `clob.polymarket.com`
- That `recommendation-history.md` exists and has the expected table format
- That at least some `market-pulse-*.md` reports exist with `polymarket.com/event/` URLs

### Step 2: Review Data Quality

Read the JSON output and check:

1. **Unmatched records** — The `unmatched` array lists markets that couldn't be matched to an event slug. For each:
   - Try to manually find the event slug on Polymarket
   - If found, note the correct price for inclusion in the report
   - If truly unreachable, mark as "data unavailable" in the report

2. **Anomalous P&L** — Check for extreme outliers (>500% gain or >100% loss). These may indicate:
   - Wrong token ID matched (multi-market event mismatch)
   - Market settled since last check
   - Price data stale or missing

3. **Settled markets** — Records with `resolved_status: "won"` or `"lost"` should have their Status updated in Step 4.

### Step 3: Generate Backtest Report

Format the results using the template in [references/output-template.md](references/output-template.md).

The report must include:

1. **Performance Overview** — Total invested, current value, total P&L (realized + unrealized), win rate
2. **Position Details** — Per-recommendation breakdown with entry price, current price, P&L, days held
3. **Category Analysis** — Performance grouped by market category (crypto, geopolitics, sports, tech, politics)
4. **Direction Analysis** — Buy Yes vs Buy No performance comparison
5. **Edge Calibration** — Compare AI-estimated edge vs actual return for each position
6. **Strategy Reflection** — AI-generated analysis covering:
   - Best and worst performers with root cause analysis
   - Category-level insights (which topics does the model predict well?)
   - Longshot bias validation (do Buy No positions on low-Yes markets outperform?)
   - Position sizing evaluation (did Kelly sizing improve returns vs flat sizing?)
   - 3-5 concrete improvement recommendations for future market pulse runs

**Timestamp:** All times in UTC, format `YYYY-MM-DD HH:MM:SS`.

### Step 4: Update Recommendation History

For any settled markets (won/lost), update `~/polymarket-reports/recommendation-history.md`:
- Change the Status column from "Open" to "Won" or "Lost"
- Use the Edit tool to make targeted replacements
- Do not modify any other columns

### Step 5: Save Report

Save the backtest report as Markdown:

```bash
mkdir -p ~/polymarket-reports
```

**File path:** `~/polymarket-reports/backtest-{YYYY-MM-DD}-{HHMMSS}.md`

Use the Write tool to save. Confirm the file path to the user after saving.

## Troubleshooting

- **Many unmatched records**: The slug matching depends on pulse report files existing in `~/polymarket-reports/`. If reports were deleted, the script cannot extract slugs. Manually search Polymarket for the market name.
- **Midpoint returns None**: The market may be very illiquid or the CLOB API may be down. The script falls back to Gamma API `outcomePrices`.
- **Stale prices**: Gamma API `outcomePrices` can lag behind the CLOB midpoint. If precision matters, verify against the Polymarket website.
- **Script timeout**: With 20+ unique events, the script makes ~40-60 API calls. This may need 30-60 seconds. Be patient.

## Reference Files

- [references/output-template.md](references/output-template.md) — Report formatting template
