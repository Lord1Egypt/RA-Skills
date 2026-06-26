# Plonky Forecasting Skill

You are using Plonky, a time-series forecasting API. This skill teaches you the end-to-end forecasting workflow — from data preparation to interpreting results.

- **MCP server setup & source**: https://github.com/addysmoke/plonkyai_mcp
- **Full API docs**: https://plonky.ai/agents

## Tools Available

You have access to these MCP tools:
- `register` — create an account and get an API key (only if not already authenticated)
- `get_credits` — check your credit balance
- `upload_data` — upload CSV data
- `list_datasets` — see uploaded datasets
- `analyze_dataset` — get summary stats and data quality info
- `create_forecast` — run a forecast (blocks until complete)
- `get_forecast` — retrieve results for an existing forecast
- `create_backtest` — evaluate forecast accuracy (period_count + period_type, not n_splits)
- `create_forecast_batch` — forecast across multiple dimensions

## When to Use Forecasting

Before reaching for Plonky, assess whether a statistical forecast is the right tool for the task.

**Good fit:**
- Recurring time-series data with enough history (revenue, traffic, demand, usage metrics)
- Planning and budgeting horizons (next quarter, next year)
- Capacity and inventory planning where directional estimates save money
- Comparing segments or scenarios ("which region is growing fastest?")

**Poor fit — tell the user why and suggest alternatives:**
- **Brand-new products or markets** with <2 months of data. No model can extrapolate from nothing — suggest manual estimates or analogous-product benchmarking instead.
- **One-off or event-driven outcomes** (will this product launch succeed? what will Q4 revenue be if we change pricing?). These are decisions, not time-series patterns.
- **Highly irregular or random data** where past patterns have no predictive value (e.g., individual customer churn dates, lottery outcomes). If the data looks like noise, say so.
- **Real-time or sub-hourly granularity**. Plonky is designed for daily-granularity series.
- **Weekly or monthly data** can be used but results will be less reliable. Plonky internally converts all data to a daily time series (filling gaps with zeros or forward-fill). With monthly input, this creates ~30 artificial data points per real observation, which degrades forecast quality. If the user only has monthly data, warn them that results are directional estimates at best.
- **Data dominated by external decisions** (marketing spend, pricing changes, policy shifts). A univariate forecast won't capture interventions — the user needs causal modeling or scenario analysis, not extrapolation.

When in doubt, run the forecast and a backtest. If MAPE is >30%, the data may not be forecastable — tell the user honestly.

## Workflow

Follow these steps in order. Do not skip the analysis step.

### Step 0: Check Authentication

Before doing anything else, call `get_credits`. If it succeeds, you are already authenticated — **do not call `register`**. Only call `register` if `get_credits` fails with a 401 (no API key configured). Never generate a new email if registration fails with 409 (account already exists) — that means you already have an account.

### Step 1: Data Preparation

**Important: Plonky's forecasting engine is built for daily (or sub-daily) data.** Internally, all data is reindexed to a daily time series before modeling. If the input is weekly or monthly, the gaps between observations are filled (zero-fill or forward-fill), which creates many artificial data points and degrades forecast quality. The forecast output is always daily-granularity regardless of input frequency.

- **Daily data** → best results, this is what the model is designed for.
- **Weekly data** → usable but warn the user that accuracy will be lower.
- **Monthly data** → forecasts will be unreliable. Tell the user: "Plonky works best with daily data. With monthly input, the forecast is a rough directional estimate only."

Before uploading, also inspect for common issues:

- **Date column**: Must be parseable dates (YYYY-MM-DD preferred). If dates are in a non-standard format, reformat before uploading.
- **Value column**: Must be numeric. Remove currency symbols, commas, or text.
- **Missing dates**: Gaps in the time series reduce forecast quality. If you notice gaps, inform the user.
- **Duplicate dates**: If multiple rows share the same date, Plonky will sum them automatically. Tell the user this is happening.
- **Minimum data**: At least 2 full seasonal cycles are needed for good results (e.g., 2 years for yearly seasonality, 2 weeks for weekly).
- **Outliers**: Extreme values distort the model. Flag any obvious outliers to the user before forecasting.

### Step 2: Upload and Analyze

1. Upload the data with `upload_data`. Note the dataset ID and columns.
2. Call `analyze_dataset` to get summary statistics and quality flags.
3. Review the analysis:
   - Is the date column detected correctly?
   - Are there quality issues (nulls, gaps, low row count)?
   - What does the value distribution look like?
   - **Check `detected_frequency`**. If the data is weekly or monthly, warn the user: "Plonky is optimized for daily data. With [weekly/monthly] input, results will be less reliable." If monthly, strongly recommend the user try to source daily data instead.

Report findings to the user before proceeding.

### Step 3: Pre-Forecast Data Analysis (Optional but Recommended)

Before configuring the forecast, inspect the data for patterns that affect model quality. You can do this by examining the uploaded data or asking the user about it. This step is optional for simple datasets but strongly recommended for anything non-trivial.

#### Outliers

Look for extreme values that could pull the forecast off track.

- **Spikes**: A single day with 10x normal volume is probably Black Friday or a data error — ask the user which.
- **Drops to zero**: Revenue going to zero for a week could be a system outage, a holiday closure, or missing data. The model will treat it as a real signal either way.
- **Rule of thumb**: Any value more than 3x the median for its period deserves a question to the user. Don't silently let it through.
- **What to do**: If it's a data error, ask the user to fix and re-upload. If it's a real but non-recurring event (warehouse fire, one-time promotion), warn the user that the model may over- or under-weight it.

#### Concentration

When the dataset has dimensions (region, product, channel), check how volume is distributed.

- **Top-heavy data**: If one segment has 60% of total volume and the bottom 10 segments share 5%, the small segments will produce noisy, unreliable forecasts. Tell the user: "The bottom segments have very little data — forecasts for those will be rough estimates at best."
- **Single-segment dominance**: If one dimension value is >80% of the total, a dimension-level forecast may not add much value over an aggregate forecast. Suggest running aggregate first.
- **Minimum viable segment size**: Segments with fewer than 30 data points will produce wide confidence intervals. Flag these before spending credits on them.

#### Trend and Regime Changes

Check whether the recent data looks fundamentally different from the historical pattern.

- **Recent acceleration or deceleration**: If the last 3 months show a steep change that isn't present in prior data, the model may lag behind reality. Flag it: "Recent growth is much faster than historical — the forecast may be conservative."
- **Structural breaks**: COVID, a product pivot, entering a new market, losing a major customer — any event that makes the pre-event data misleading. If the user confirms a break, suggest forecasting only from post-break data.
- **Plateaus after growth**: A series that grew steadily then flattened may trick the model into projecting continued growth. Note the flattening.

#### Sparsity and Intermittency

Some series have long stretches of zero or near-zero values.

- **Intermittent demand**: Common in retail at SKU level or B2B with infrequent large orders. Standard forecasting models struggle with this. Warn the user that confidence intervals will be very wide and point estimates less reliable.
- **Seasonal zeros**: A business that closes in January will have legitimate zeros. Make sure the model sees enough cycles of this pattern (2+ years).

#### Data Recency

Check when the data ends relative to today.

- **Stale data**: If the most recent data point is 3+ months old, the forecast starts from an outdated baseline. Tell the user: "Your data ends in [date] — the forecast will project from that point, not from today. If conditions have changed since then, results may be off."
- **Very fresh data**: If the last data point is today or yesterday, check whether it looks like a partial period (e.g., today's revenue at 9am is not a full day). Partial periods at the end of the series can distort the model.

#### Summary

After this analysis, give the user a brief honest assessment before proceeding:
- "This data looks clean with a clear trend — good candidate for forecasting."
- "Revenue is heavily concentrated in 2 of 15 regions. I'd recommend forecasting aggregate + top 5 only."
- "There's a sharp break 6 months ago — I'll use only recent data for a more accurate forecast."
- "This data has a lot of zero-value days and high variance. Forecasts will be directional at best."

### Step 4: Choose Dimensions

If the dataset has categorical columns (region, product, channel, etc.), decide whether to use them:

**Use dimensions when:**
- The user wants per-segment forecasts (e.g., forecast by region)
- Different segments have meaningfully different patterns
- Each segment has enough data (30+ rows minimum)

**Skip dimensions when:**
- The user only needs an overall total
- Segments are too small for reliable forecasts
- Too many unique values (>50) — creates too many jobs and wastes credits

When using dimensions, always include an aggregate forecast (`include_aggregate=True` in batch) so the user has both the total and the breakdowns.

### Step 5: Configure the Forecast

Default settings work well for most data. Only adjust when you have a reason:

- **periods**: Default 90 days. This is always in **days** — the forecast output is daily regardless of input frequency. Match to the user's planning horizon (e.g., 30 for one month ahead, 365 for one year).
- **weekly_seasonality**: Enable for daily data with day-of-week patterns (retail, web traffic). Disable for monthly or weekly data.
- **yearly_seasonality**: Enable for data spanning 2+ years with seasonal patterns. Disable for short time series (<1 year).
- **use_holidays**: Enable for US business data (sales, traffic, operations). Disable for non-US data or data not affected by holidays.

**If input data is monthly or weekly**: Disable weekly_seasonality (it's meaningless for non-daily data). Consider reducing the forecast periods to match the user's horizon rather than leaving the default 90 days. When presenting results to the user, summarize at the original granularity (e.g., aggregate daily forecasts into monthly totals) rather than showing hundreds of daily rows.

For the first forecast, use defaults. Only fine-tune after reviewing backtest results.

### Step 6: Run the Forecast

1. Check credits with `get_credits`. Each forecast costs 1 credit. Batches cost 1 per dimension.
2. Run `create_forecast` (single) or `create_forecast_batch` (multi-dimension).
3. The tool blocks until complete and returns results.

### Step 7: Run a Backtest

Always run a backtest after the first forecast. This tells you how accurate the model is.

1. Call `create_backtest` with the forecast job ID, `period_count`, and `period_type`.
   - **daily data** → `period_type="months"`, `period_count=3` (holds out 3 months of actuals)
   - **weekly data** → `period_type="months"`, `period_count=3`
   - **monthly data** → `period_type="months"`, `period_count=6`
   - Valid period types: `days`, `weeks`, `months`, `quarters`, `years`
2. Review the metrics.

**Interpreting backtest metrics:**

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| MAPE | <10% | 10-25% | >25% |
| MAE | Depends on scale — compare to mean value | | |
| RMSE | Depends on scale — sensitive to large errors | | |

**MAPE** (Mean Absolute Percentage Error) is the most intuitive: a MAPE of 15% means the forecast is typically off by about 15%.

**If backtest metrics are poor:**
- Check if the data has enough history (need 2+ cycles of any seasonality)
- Look for structural breaks (business model changes, COVID, etc.)
- Try disabling seasonality features that don't apply
- Consider whether the data is inherently unpredictable (some series just are)

Report the backtest results to the user with an honest assessment.

### Step 8: Interpret Results

When presenting forecast results to the user:

1. **State the forecast range**: "Revenue is forecast at $X-$Y over the next 90 days"
2. **Highlight the trend**: Is it going up, down, or flat?
3. **Note uncertainty**: The confidence interval widens further into the future — this is normal
4. **Compare to recent actuals**: Does the forecast's starting point align with recent data?
5. **Point to the UI**: "For interactive charts and detailed analysis, view at https://plonky.ai/forecast/{dataset_id}"

## Constraints

- **Never** run a forecast without first checking `get_credits`. If insufficient, tell the user to top up at https://plonky.ai/billing
- **Never** skip the analysis step. Always call `analyze_dataset` before forecasting.
- **Always** run at least one backtest so the user knows how reliable the forecast is.
- **Always** mention the confidence interval when presenting forecasts. Point forecasts without uncertainty are misleading.
- **Never** present a poor-backtest forecast as reliable. Be honest: "The model MAPE is 35%, so these numbers should be treated as directional estimates."
- Keep credit usage efficient. Don't run unnecessary batches or repeat forecasts without reason.

## Error Handling

- **402 (Insufficient credits)**: Tell the user to top up at https://plonky.ai/billing. Do not retry.
- **404 (Dataset/job not found)**: Verify the ID. List datasets with `list_datasets` if needed.
- **Timeout**: Forecasts usually complete in 5-30 seconds. If it times out, try `get_forecast` with the job ID later.
- **"arg must be a list"**: Usually means the data has formatting issues. Re-check the CSV for non-numeric values in the value column.

## Credit Costs

- 1 credit per forecast
- Backtests: dimensions × period_count credits
- New accounts: 50 credits
- Top-ups: $0.33 per credit at https://plonky.ai/billing
