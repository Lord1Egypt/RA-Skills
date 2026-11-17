---
name: oo-defillama
description: "DeFiLlama (defillama.com). Use this skill for ANY DeFiLlama request — searching and reading data. Whenever a task involves DeFiLlama, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "DeFiLlama"
  author: "OOMOL"
  version: "1.0.2"
  services: ["defillama"]
  icon: "https://static.oomol.com/logo/third-party/defillama.svg"
---

# DeFiLlama

Operate **DeFiLlama** through your OOMOL-connected account. This skill calls the `defillama` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected DeFiLlama. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "defillama" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "defillama" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_bridges_bridge_by_id` — Get summary of bridge volume and volume breakdown by chain. Requires an API plan key.
- `get_bridges_bridgedaystats_by_timestamp_by_chain` — Get a 24hr token and address volume breakdown for a bridge. Requires an API plan key.
- `get_bridges_bridges` — List all bridges along with summaries of recent bridge volumes.. Requires an API plan key.
- `get_bridges_bridgevolume_by_chain` — Get historical volumes for a bridge, chain, or bridge on a particular chain. Requires an API plan key.
- `get_bridges_transactions_by_id` — Get all transactions for a bridge within a date range. Requires an API plan key.
- `get_categories` — Overview of all categories accross all protocols. Requires an API plan key.
- `get_chain_assets` — Get assets of all chains. Requires an API plan key.
- `get_coins_batch_historical` — Get historical prices for multiple tokens at multiple different timestamps. Available with no_auth or api_key.
- `get_coins_block_by_chain_by_timestamp` — Get the closest block to a timestamp. Runs binary search over a blockchain's blocks to get the closest one to a timestamp. Every time this is run we add new data to our database, so each query permanently speeds up future queries. Available with no_auth or api_key.
- `get_coins_chart_by_coins` — Get token prices at regular time intervals. Strings accepted by period: Can use regular chart candle notion like '4h' etc where: W = week, D = day, H = hour, M = minute (not case sensitive) Available with no_auth or api_key.
- `get_coins_percentage_by_coins` — Get percentage change in price over time. Strings accepted by period: Can use regular chart candle notion like '4h' etc where: W = week, D = day, H = hour, M = minute (not case sensitive) Available with no_auth or api_key.
- `get_coins_prices_current_by_coins` — Get current prices of tokens by contract address. The goal of this API is to price as many tokens as possible, including exotic ones that never get traded, which makes them impossible to price by looking at markets. The base of our data are prices pulled from coingecko, which is then extended through multiple means: - We price all bridged tokens by using the price of the token in it's original chain, so we fetch all bridged versions of USDC on arbitrum, fantom, avax... and price all them using the price for the token on Ethereum, which we know. Right now we support 10 different bridging protocols. - We have multiple adapters to price specialized sets of tokens by running custom code: - We price yearn's yToken LPs by checking how much underlying token can be withdrawn for each LP - Aave, compound and euler LP tokens are also priced based on their relationship against underlying tokens - Uniswap, curve, balancer and stargate LPs are priced using the underlying tokens in each pair - GMX's GLP token is priced based on the value of tokens given on withdrawal (which includes calculations based on trader's PnL) - Synthetix tokens are priced using forex prices of the coin they are pegged to - For tokens that we haven't been able to price in any other way, we find the pool with most liquidity for each on uniswap, curve and serum and then use the prices provided on those exchanges. Unlike all the other tokens, we can't confirm that these prices are correct, so we only ingest the ones that have sufficient liquidity and, even in that case, we attach a `confidence` value to them that is related to the depth of liquidity and which represents our confidence in the quality of each price. API consumers can choose to filter out prices with low confidence values. Our API server is fully open source and we are constantly adding more pricing adapters, extending the amount of tokens we support. Tokens are queried using {chain}:{address}, where chain is an identifier such as ethereum, bsc, polygon, avax... You can also get tokens by coingecko id by setting `coingecko` as the chain, eg: coingecko:ethereum, coingecko:bitcoin. Examples: - ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1 - bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878 - coingecko:ethereum - arbitrum:0x4277f8f2c384827b5273592ff7cebd9f2c1ac258 Available with no_auth or api_key.
- `get_coins_prices_first_by_coins` — Get earliest timestamp price record for coins. Available with no_auth or api_key.
- `get_coins_prices_historical_by_timestamp_by_coins` — Get historical prices of tokens by contract address. See /prices/current for explanation on how prices are sourced. Available with no_auth or api_key.
- `get_dat_institutions` — Get list of all institutions with Digital Asset Treasury data. Returns comprehensive data about institutions holding digital assets, including mNAV calculations (realized, realistic, maximum) as described in the [DAT Methodology](https://docs.llama.fi/analysts/dat-methodology) Requires an API plan key.
- `get_dat_institutions_by_symbol` — Get individual institution Digital Asset Treasury details. Returns detailed data for a specific institution, including mNAV calculations (realized, realistic, maximum) as described in the [DAT Methodology](https://docs.llama.fi/analysts/dat-methodology) Requires an API plan key.
- `get_emission_by_protocol` — Unlocks data for a given token/protocol. You can find a list of available slugs to query by querying /emissions and then extracting the key `gecko_id`. Requires an API plan key.
- `get_emissions` — List of all tokens along with basic info for each. Requires an API plan key.
- `get_entities` — List all entities. Requires an API plan key.
- `get_equities_v1_companies_list` — Get list of all tracked public companies. Returns the tracked US-listed companies with their identity and sector and industry slugs, sorted by market cap (largest first). Use this to discover valid `ticker` + `country` pairs for the other equities endpoints. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_dimensions` — Get financial dimensions for a company. Returns time-series financial dimension metrics (revenue, holders revenue, earnings, and basic shares outstanding) for the given ticker, each broken down into annual and quarterly series. Every data point is a two-element array: ISO 8601 period-ending date, then the numeric value. Series are sorted by date descending (newest first). Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_earnings_calendar` — Get earnings calendar. Returns earnings report dates built from SEC EDGAR filings: past reports, plus the next four expected dates projected from each company's own filing history. Covers US-listed companies. The same path serves two shapes: - **With `ticker`**: that company's full history plus its upcoming estimates. - **Without `ticker`**: the market-wide calendar over a rolling window from about 1 month back to about 13 months ahead. Use the `ticker` form for older history. Rows are sorted by `report_date`, oldest first, so `limit` keeps the earliest matches. `?ticker=AAPL&status=estimated&limit=1` is Apple's next report. Every row says what kind of date it is in `date_status`. A future date is `estimated`, with a `max_drift_days` range, and is not a confirmed schedule. Company names are not included. Join on `ticker` against `GET /equities/v1/companies-list`. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_filings` — Get filings for a company. Returns a list of company filings (such as annual reports, quarterly reports, and other important filings) for the given ticker, sorted by filing date descending (newest first). Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_industries` — Get industries. Returns one row per industry, sorted by market cap (largest first), with the same metrics as a `GET /equities/v1/sectors` row plus the parent sector. Filter to one sector with `sector`, or to one industry with `industry`. Each row carries two weights: `weight` is the share of all tracked US equity, and `sectorWeight` is the share of the parent sector. For Technology's industries, `sectorWeight` sums to 100 while `weight` sums to Technology's own weight in the market. `rank` counts within the selected sector when `sector` is set, and across all industries otherwise. Filtering by `industry` alone keeps each row's market-wide rank. The same industry name can exist under two sectors, so `industry` alone can return more than one row. Covers US-listed companies. All monetary values are in USD. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_ohlcv` — Get OHLCV candle data for a company. Returns OHLCV bars as six-number arrays: Unix timestamp in seconds (UTC), open, high, low, close, volume. Sorted by time descending (newest first). Optional `timeframe` controls both how far back data goes and the bar resolution: `1D`, `7D` and `1W` return 5-minute bars, `1M` and longer return daily bars. Omit or empty for full history (`MAX`). Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_onchain` — Get on-chain tradeable markets for a company. Returns where the stock can be traded on-chain: `perps` are perpetual futures markets across exchanges, and `tokens` are tokenised-equity issuers. This is a live snapshot refreshed hourly and no history is kept. On-chain data is only collected for US-listed tickers, so a ticker in another market comes back with empty `perps` and `tokens` arrays rather than an error. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_price_history` — Get historical price data for a company. Returns closing prices as two-element arrays: ISO 8601 date-time string, then numeric price. Sorted by date descending (newest first). Resolution follows `timeframe`: `1D`, `7D` and `1W` are 5-minute intraday bars whose date-time carries a real time of day, while `1M` and longer are daily closes stamped `T00:00:00Z`. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_sector` — Get details for one sector. Returns one sector in full: everything its `GET /equities/v1/sectors` row has, plus a short description, the ten largest holdings, aggregate and median valuation ratios side by side, and how concentrated the sector is. Covers US-listed companies. All monetary values are in USD. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_sectors` — Get all sectors. Returns one row per sector, sorted by market cap (largest first): market cap and weight, traded value, valuation ratios, price changes over seven windows, and the three largest holdings. Covers US-listed companies. All monetary values are in USD. Sector and industry names come from the data vendor (a Morningstar-style list of 11 sectors and about 140 industries), not GICS. Companies with no sector are grouped as `Unknown` rather than dropped, so sector market caps add up to the market total. Ratios such as `trailingPE` are aggregates (total market cap / total earnings), so the group is valued as one company rather than averaging its constituents' ratios. Price changes are weighted by market cap at the start of each window. Percentages are in percent, not fractions: `1.82` means +1.82%. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_sectors_overview` — Get market-wide sector overview. Returns totals across all tracked US companies, which the per-sector rows cannot carry: the market cap every sector `weight` is measured against, aggregate and median valuation ratios for the whole market, and the best, worst, and largest sector. The constituents here are every tracked US company. Fields shared with `GET /equities/v1/sectors` mean the same thing. Covers US-listed companies. All monetary values are in USD. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_statements` — Get financial statements for a company. Returns income statement, balance sheet, and cash flow statement for the given ticker, broken down by quarterly and annual periods. Requires an API plan key. Beta API; upstream fields may change.
- `get_equities_v1_summary` — Get live market summary for a company. Returns current market data for a single ticker. This is a compact snapshot (no `ticker` / `name` fields); use `GET /equities/v1/companies-list` for the list of tracked companies with their identity details. Requires an API plan key. Beta API; upstream fields may change.
- `get_etfs_flows` — Historical Flows at the Asset Level. Requires an API plan key.
- `get_etfs_snapshot` — Get ETFs and their metrics (aum, flows, fees...). Requires an API plan key.
- `get_fdv_performance_by_period` — Get chart of narratives based on category performance (with individual coins weighted by mcap). Requires an API plan key.
- `get_forks` — Overview of all forks accross all protocols. Requires an API plan key.
- `get_hacks` — Overview of all hacks on our Hacks dashboard. Requires an API plan key.
- `get_historical_liquidity_by_token` — Read historical token liquidity. Requires an API plan key.
- `get_inflows_by_protocol_by_timestamp` — Lists the amount of inflows and outflows for a protocol at a given date. Requires an API plan key.
- `get_lst_rates` — Exchange rates and ETH peg of liquid staking tokens. Latest expected (contract) redemption rate, executable market rate and resulting ETH peg for major LSTs. Requires an API plan key.
- `get_oracles` — Overview of all oracles accross all protocols. Requires an API plan key.
- `get_overview_derivatives` — Lists all derivatives along summaries of their volumes filtering by chain. Requires an API plan key.
- `get_overview_dexs` — List all dexs along with summaries of their volumes and dataType history data. Available with no_auth or api_key.
- `get_overview_dexs_by_chain` — List all dexs along with summaries of their volumes and dataType history data filtering by chain. Available with no_auth or api_key.
- `get_overview_fees` — List all protocols along with summaries of their fees and revenue and dataType history data. Available with no_auth or api_key.
- `get_overview_fees_by_chain` — List all protocols along with summaries of their fees and revenue and dataType history data by chain. Available with no_auth or api_key.
- `get_overview_open_interest` — List all open interest dex exchanges along with summaries of their open interest. Available with no_auth or api_key.
- `get_overview_options` — List all options dexs along with summaries of their volumes and dataType history data. Available with no_auth or api_key.
- `get_overview_options_by_chain` — List all options dexs along with summaries of their volumes and dataType history data filtering by chain. Available with no_auth or api_key.
- `get_perp_funding_rates` — Funding rates and open interest of perpetual futures. Latest funding rate, open interest and index price for Binance and OKX perpetual markets, with the 7d and 30d average and sum of settled funding rates. Requires an API plan key.
- `get_pre_ipo_v1_companies_list` — Get list of all tracked pre-IPO companies. Returns every private company in the pre-IPO registry with its latest estimated valuation and derived funding metrics. Use this to discover valid `company` ids for the other pre-IPO endpoints. Companies come back in registry order, so the list is not sorted by valuation. Requires an API plan key.
- `get_pre_ipo_v1_integrations` — Get tradeable markets for a pre-IPO company. Returns where the company can actually be traded right now: perpetual futures venues and tokenised-share issuers. A pre-IPO perp settles in stablecoins against the venue's reference price, so no shares change hands and the same company can trade at a slightly different price on every venue. This is a live snapshot refreshed hourly and no history is kept. Every company in the registry gets a response: one with no listings returns empty `perps` and `tokenIssuers` arrays rather than a miss. Requires an API plan key.
- `get_pre_ipo_v1_raises` — Get funding rounds for a pre-IPO company. Returns disclosed funding rounds, oldest first. The same round is usually reported by several sources with different dates and amounts, so rounds are reconciled before being served: each cluster collapses to one canonical raise taking the earliest date, the median amount, the median valuation, and the highest-ranked series label. Requires an API plan key.
- `get_pre_ipo_v1_summary` — Get profile and latest valuation for a pre-IPO company. Returns the company profile together with its latest estimated valuation and its most recent funding round. Requires an API plan key.
- `get_pre_ipo_v1_valuations` — Get valuation history for a pre-IPO company. Returns one aggregated valuation point per calendar month, oldest first. Within a month every source's marks are averaged and then the source averages are averaged, so a source that reports daily does not outvote one that reports monthly. Points are rounded to the nearest 100 and dated `YYYY-MM-01`; months with no data are skipped, and the current month is month-to-date. Requires an API plan key.
- `get_protocol_by_protocol` — Get historical TVL of a protocol and breakdowns by token and chain. Available with no_auth or api_key.
- `get_protocols` — List all protocols on defillama along with their tvl. Available with no_auth or api_key.
- `get_raises` — Overview of all raises on our Raises dashboard. Requires an API plan key.
- `get_rwa_chain_by_chain` — List current RWA assets on a chain. Returns current RWA assets that have onchain market cap, active market cap, or DeFi active TVL on the requested chain. Requires an API plan key.
- `get_rwa_chart_chain_breakdown` — Get historical RWA metric breakdown by chain. Returns time series rows with one column per chain for the selected RWA metric. Requires an API plan key.
- `get_rwa_chart_chain_by_chain` — Get historical RWA chart data for a chain. Returns historical onchain market cap, active market cap, and DeFi active TVL totals for a chain. Requires an API plan key.
- `get_rwa_current` — List all current RWA assets. Returns current Real World Asset rows with per-chain onchain market cap, active market cap, and DeFi active TVL maps. Requires an API plan key.
- `get_rwa_list` — List RWA ids and filter values. Returns lightweight RWA lists used for discovery, search, and filters. Requires an API plan key.
- `get_rwa_stats` — Get aggregate RWA stats by chain, category, platform, and asset group. Returns RWA aggregates. For the default per-chain table, read byChain[chain].base: assetIssuers.length, assetCount, activeMcap, onChainMcap, and defiActiveTvl. Add stablecoinsOnly, governanceOnly, and stablecoinsAndGovernance when those buckets should be included. Requires an API plan key.
- `get_stablecoins_stablecoin_by_asset` — Get historical mcap and historical chain distribution of a stablecoin. Available with no_auth or api_key.
- `get_stablecoins_stablecoinchains` — Get current mcap sum of all stablecoins on each chain. Available with no_auth or api_key.
- `get_stablecoins_stablecoincharts_all` — Get historical mcap sum of all stablecoins. Available with no_auth or api_key.
- `get_stablecoins_stablecoincharts_by_chain` — Get historical mcap sum of all stablecoins in a chain. Available with no_auth or api_key.
- `get_stablecoins_stablecoindominance_by_chain` — Get stablecoin dominance per chain along with the info about the larges coin in a chain. Requires an API plan key.
- `get_stablecoins_stablecoinprices` — Get historical prices of all stablecoins. Available with no_auth or api_key.
- `get_stablecoins_stablecoins` — List all stablecoins along with their circulating amounts. Available with no_auth or api_key.
- `get_summary_derivatives_by_protocol` — Volume Details about a specific perp protocol. Requires an API plan key.
- `get_summary_dexs_by_protocol` — Get summary of dex volume with historical data. Available with no_auth or api_key.
- `get_summary_fees_by_protocol` — Get summary of protocol fees and revenue with historical data. Available with no_auth or api_key.
- `get_summary_options_by_protocol` — Get summary of options dex volume with historical data. Available with no_auth or api_key.
- `get_token_protocols_by_symbol` — Lists the amount of a certain token within all protocols. Data for the Token Usage page. Requires an API plan key.
- `get_treasuries` — List all protocols on our Treasuries dashboard. Requires an API plan key.
- `get_tvl_by_protocol` — Simplified endpoint to get current TVL of a protocol. Simplified endpoint that only returns a number, the current TVL of a protocol Available with no_auth or api_key.
- `get_usage` — Get amount of credits left in the api key, these reset on the 1st of each month. Requires an API plan key.
- `get_v2_chains` — Get current TVL of all chains. Available with no_auth or api_key.
- `get_v2_chart_by_metric` — Get historical timeseries chart data. Returns an array of [timestamp, value] pairs representing the total metric value over time. Requires an API plan key.
- `get_v2_chart_by_metric_category_by_category` — Get category historical timeseries chart data. Returns an array of [timestamp, value] pairs for the metric filtered by a specific category. Requires an API plan key.
- `get_v2_chart_by_metric_category_by_category_chain_breakdown` — Get category timeseries chart data breakdown by chain. Returns an array of [timestamp, {chain: value}] pairs showing the metric for a specific category broken down by chain. Requires an API plan key.
- `get_v2_chart_by_metric_category_by_category_chain_by_chain` — Get category chain historical timeseries chart data. Returns an array of [timestamp, value] pairs for the metric filtered by both category and chain. Requires an API plan key.
- `get_v2_chart_by_metric_category_by_category_chain_by_chain_protocol_breakdown` — Get category chain timeseries chart data breakdown by protocol. Returns an array of [timestamp, {protocol: value}] pairs showing the metric filtered by both category and chain, broken down by protocol. Requires an API plan key.
- `get_v2_chart_by_metric_category_by_category_protocol_breakdown` — Get category timeseries chart data breakdown by protocol. Returns an array of [timestamp, {protocol: value}] pairs showing the metric for a specific category broken down by protocol. Requires an API plan key.
- `get_v2_chart_by_metric_chain_breakdown` — Get historical timeseries chart data breakdown by chain. Returns an array of [timestamp, {chain: value}] pairs showing the metric broken down by chain over time. Requires an API plan key.
- `get_v2_chart_by_metric_chain_by_chain` — Get chain historical timeseries chart data. Returns an array of [timestamp, value] pairs for the metric filtered by a specific chain. Requires an API plan key.
- `get_v2_chart_by_metric_chain_by_chain_protocol_breakdown` — Get chain timeseries chart data breakdown by protocol. Returns an array of [timestamp, {protocol: value}] pairs showing the metric on a specific chain broken down by protocol. Requires an API plan key.
- `get_v2_chart_by_metric_protocol_breakdown` — Get historical timeseries chart data breakdown by protocol. Returns an array of [timestamp, {protocol: value}] pairs showing the metric broken down by protocol over time. Requires an API plan key.
- `get_v2_chart_by_metric_protocol_by_protocol` — Get protocol historical timeseries chart data. Returns an array of [timestamp, value] pairs for the metric of a specific protocol. Requires an API plan key.
- `get_v2_chart_by_metric_protocol_by_protocol_chain_breakdown` — Get protocol timeseries chart data breakdown by chain. Returns an array of [timestamp, {chain: value}] pairs showing the metric for a specific protocol broken down by chain. Requires an API plan key.
- `get_v2_chart_by_metric_protocol_by_protocol_label_breakdown` — Get protocol timeseries chart data breakdown by label. Returns an array of [timestamp, {label: value}] pairs showing the metric for a specific protocol broken down by label (e.g. Borrow Interest, Flash Loans). Currently only supported for metric=fees. Requires an API plan key.
- `get_v2_chart_by_metric_protocol_by_protocol_version_breakdown` — Get protocol timeseries chart data breakdown by version. Returns an array of [timestamp, {version: value}] pairs showing the metric for a specific protocol broken down by version (e.g. Aave V2, Aave V3). Requires an API plan key.
- `get_v2_chart_fork_protocol_breakdown` — Get timeseries chart data breakdown by protocol. Returns an array of objects with a timestamp and TVL values broken down by fork protocol. Requires an API plan key.
- `get_v2_chart_fork_protocol_by_protocol` — Get timeseries chart data by protocol. Returns an array of [timestamp, value] pairs representing TVL over time for all forks of a specific protocol. Requires an API plan key.
- `get_v2_chart_oracle` — Get timeseries chart data for all oracles. Returns an array of [timestamp, value] pairs representing total TVL across all oracles over time. Requires an API plan key.
- `get_v2_chart_oracle_chain_breakdown` — Get timeseries chart data breakdown by chain. Returns an array of objects with a timestamp and TVL values broken down by chain. Requires an API plan key.
- `get_v2_chart_oracle_chain_by_chain` — Get timeseries chart data by chain. Returns an array of [timestamp, value] pairs representing oracle TVL over time for a specific chain. Requires an API plan key.
- `get_v2_chart_oracle_chain_by_chain_protocol_breakdown` — Get protocol breakdown timeseries chart data by chain. Returns an array of objects with a timestamp and TVL values broken down by oracle/protocol for a specific chain. Requires an API plan key.
- `get_v2_chart_oracle_protocol_breakdown` — Get timeseries chart data breakdown by protocol. Returns an array of objects with a timestamp and TVL values broken down by oracle/protocol. Requires an API plan key.
- `get_v2_chart_oracle_protocol_by_protocol` — Get timeseries chart data by protocol/oracle. Returns an array of [timestamp, value] pairs representing TVL over time for a specific oracle/protocol. Requires an API plan key.
- `get_v2_chart_oracle_protocol_by_protocol_chain_breakdown` — Get chain breakdown timeseries chart data by protocol/oracle. Returns an array of objects with a timestamp and TVL values broken down by chain for a specific oracle/protocol. Requires an API plan key.
- `get_v2_chart_treasury_protocol_by_protocol` — Get historical treasury chart for a protocol. Returns an array of [timestamp, value] pairs representing the protocol's treasury value over time. By default excludes the protocol's own tokens (OwnTokens). Requires an API plan key.
- `get_v2_chart_treasury_protocol_by_protocol_chain_breakdown` — Get historical treasury chart for a protocol broken down by chain. Returns an array of [timestamp, { chain: value }] pairs showing treasury value per chain over time. By default excludes the protocol's own tokens. Requires an API plan key.
- `get_v2_chart_treasury_protocol_by_protocol_token_breakdown` — Get historical treasury chart for a protocol broken down by token. Returns an array of [timestamp, { token: value }] pairs showing treasury value per token over time. By default excludes OwnTokens and values are in USD. Use key and currency params to customize. Requires an API plan key.
- `get_v2_chart_tvl_protocol_by_protocol` — Get historical TVL chart for a protocol. Returns an array of [timestamp, value] pairs representing the protocol's TVL over time. By default returns the base TVL metric. Use the `key` parameter to select a different metric or aggregate all metrics. Requires an API plan key.
- `get_v2_chart_tvl_protocol_by_protocol_chain_breakdown` — Get historical TVL chart for a protocol broken down by chain. Returns an array of [timestamp, { chain: value }] pairs showing the selected metric per chain over time. Requires an API plan key.
- `get_v2_chart_tvl_protocol_by_protocol_token_breakdown` — Get historical TVL chart for a protocol broken down by token. Returns an array of [timestamp, { token: value }] pairs showing TVL per token over time. Values are in USD by default; use the currency selector for other denominations. Requires an API plan key.
- `get_v2_historical_chain_tvl` — Get historical TVL (excludes liquid staking and double counted tvl) of DeFi on all chains. Available with no_auth or api_key.
- `get_v2_historical_chain_tvl_by_chain` — Get historical TVL (excludes liquid staking and double counted tvl) of a chain. Available with no_auth or api_key.
- `get_v2_metrics_by_metric` — Get dimension data overview. Returns aggregate metrics for the specified dimension including totals and percentage changes across different time periods. Requires an API plan key.
- `get_v2_metrics_by_metric_category_by_category` — Get category dimension data overview. Returns aggregate metrics for the specified dimension filtered by a specific category. Requires an API plan key.
- `get_v2_metrics_by_metric_category_by_category_chain_by_chain` — Get category chain dimension data overview. Returns aggregate metrics for the specified dimension filtered by both category and chain. Requires an API plan key.
- `get_v2_metrics_by_metric_chain_by_chain` — Get chain dimension data overview. Returns aggregate metrics for the specified dimension filtered by a specific chain. Requires an API plan key.
- `get_v2_metrics_by_metric_protocol_by_protocol` — Get protocol dimension data overview. Returns protocol metadata along with aggregate metrics for the specified dimension. Requires an API plan key.
- `get_v2_metrics_financial_statement_protocol_by_protocol` — Get protocol income statement report. Returns protocol metadata, methodology details, and aggregated financial statement data (yearly, quarterly, monthly). Each period contains line items such as Gross Protocol Revenue, Cost Of Revenue, Gross Profit, Token Holder Net Income, Incentives, and Earnings, with values and optional label breakdowns. When querying a parent protocol (e.g. `aave`), the response includes a `childProtocols` array with per-version methodology. When querying a child protocol (e.g. `aave-v3`), methodology and breakdownMethodology are at the top level. Requires an API plan key. Beta API; upstream fields may change.
- `get_v2_metrics_fork` — Get fork data overview. Returns an object mapping fork names to arrays of protocol names that are forks of each protocol. Requires an API plan key.
- `get_v2_metrics_oracle` — Get oracle data overview. Returns an object mapping oracle names to arrays of protocol names that use each oracle. Requires an API plan key.
- `get_v2_metrics_treasury_protocol_by_protocol` — Get aggregate treasury metrics for a protocol. Returns protocol metadata along with current treasury figures and chain breakdowns. Requires an API plan key.
- `get_v2_metrics_tvl_protocol_by_protocol` — Get aggregate TVL metrics for a protocol. Returns protocol metadata along with current TVL figures, chain breakdowns, and other aggregate metrics. Requires an API plan key.
- `get_yields_v1_chart_by_pool` — Get historical APY and TVL of a pool in the legacy v1 response format. Daily history in the legacy v1 format. Every value is the day's last observation. Unknown pool ids return an empty `data` array. Available with no_auth or api_key. Free access ends on November 13, 2026; API-key access uses the legacy v1 format.
- `get_yields_v1_chart_lend_borrow_by_pool` — Historical borrow cost APY from a pool on a lending market in the legacy v1 response format. Daily borrow-market history in the legacy v1 format. Every value is the day's last observation. Unknown pool ids return an empty `data` array. Requires an API plan key.
- `get_yields_v1_pools` — Retrieve the latest data for all pools in the legacy v1 response format. Serves the former `/yields/pools` response format, including the extra fields from `/yields/poolsOld`. Frozen for compatibility: the shape will not change and no new fields will be added - use `/yields/v2/earn` for new integrations. Available with no_auth or api_key. Free access ends on November 13, 2026; API-key access uses the legacy v1 format.
- `get_yields_v1_pools_borrow` — Borrow costs APY of assets from lending markets in the legacy v1 response format. Serves the former `/yields/poolsBorrow` response format. Markets that cannot currently be borrowed from are not listed. Frozen for compatibility: the shape will not change and no new fields will be added - use `/yields/v2/borrow/markets` for new integrations. Requires an API plan key.
- `get_yields_v2_borrow_markets` — Retrieve the latest data for all borrow markets. One row per borrow market: collateral and debt token, maximum loan-to-value, USD supply/borrow totals and attributed APY for both sides over `current`, `avg_7d` and `avg_30d` windows. Reward emissions offset borrowing costs, so `borrow_cost_apy` totals can be negative (the borrower is net paid). Requires an API plan key.
- `get_yields_v2_borrow_markets_by_id_history` — Retrieve daily borrow-side history for a borrow market. Daily borrow totals and borrow-cost APY for one market, oldest first. APY carries `avg_1d` (that day), `avg_7d` and `avg_30d` (trailing averages ending that day) windows, each attributed into base/reward/total. Supply-side history for the same id lives at `/yields/v2/earn/{id}/history`. Requires an API plan key.
- `get_yields_v2_borrow_routes` — Retrieve the latest data for all borrow routes. Every supported borrowing route: a collateral position paired with a debt market on the same protocol and chain. Each row reports the collateral side (supply APY earned on the collateral), the borrow side (cost APY of the debt token) and `net_apy` (collateral yield minus borrow cost). Negative net APY means the position costs more than the collateral earns. Requires an API plan key.
- `get_yields_v2_earn` — Retrieve the latest data for all earn pools. Returns every tracked earn pool (supply-side yield), sorted by TVL descending. APY values are percentages, attributed into `base` (organic), `reward` (incentive emissions) and `total` (base + reward) over `current`, `avg_7d` and `avg_30d` windows. Pools whose underlying token is itself yield-bearing additionally report that yield under `intrinsic`; it is not included in the pool APY. For a filtered, paginated variant of the same rows use `/yields/v2/earn/query`. Requires an API plan key.
- `get_yields_v2_earn_by_id_history` — Retrieve daily history for an earn pool. Daily TVL, attributed APY and price per share for one earn pool, oldest first. APY carries `avg_1d` (that day), `avg_7d` and `avg_30d` (trailing averages ending that day) windows, each attributed into base/reward/total. Requires an API plan key.
- `get_yields_v2_earn_query` — Retrieve a filtered, paginated page of earn pools. Same rows as `/yields/v2/earn`, filtered and paginated server-side while keeping the TVL-descending order. All filters combine with AND; `chain` and `protocol` may be repeated to match any of up to 20 values. Unknown query parameters and out-of-range values are rejected with `400 INVALID_QUERY_PARAM`. Without parameters the top 100 pools by TVL are returned. Requires an API plan key.
- `get_yields_v2_earn_verified` — Retrieve the latest verified data for all measured earn pools. Measured yield for the `/yields/v2/earn` pools we simulate, sorted by verified TVL descending. Each figure is replayed from a real holder's withdrawal against archive state, so it shows what an exit would have paid rather than what the protocol reports; the two can disagree without either being wrong. APY is always the base leg, since a withdrawal cannot see reward emissions, and is unclamped, so it can be negative. A pool appears here only while it is listed on `/yields/v2/earn`, is not withheld for review, and has at least one measured day; join on `id`. Requires an API plan key.
- `get_yields_v2_earn_verified_by_id` — Retrieve the latest verified data for one earn pool. The same row `/yields/v2/earn/verified` serves for this pool, plus `methods`: the on-chain calls the simulation executes, in order. Requires an API plan key.
- `get_yields_v2_earn_verified_by_id_history` — Retrieve daily verified history for an earn pool. Daily measured APY, share price, verified TVL and exit health for one pool, oldest first. APY carries `avg_1d` (that day), `avg_7d` and `avg_30d` (trailing averages ending that day). Days the pool was not measured are omitted, so the dates are not contiguous. Every `range` is sliced from the same cached series. Requires an API plan key.
- `get_yields_v2_loops` — Retrieve the latest data for all loop strategies. Leveraged looping opportunities: supply a token, borrow against it and re-supply, repeated `loop_count` times at the market maximum loan-to-value. `loop_apy.total` is the resulting net APY at that leverage; `leverage` reports the accumulated supply and borrow multipliers relative to the initial capital. Borrow reward emissions offset the borrowing cost, so looped APY can exceed the plain supply APY substantially. Requires an API plan key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change DeFiLlama state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — DeFiLlama is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/defillama
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- DeFiLlama homepage: https://defillama.com
- API documentation: https://api-docs.defillama.com/
