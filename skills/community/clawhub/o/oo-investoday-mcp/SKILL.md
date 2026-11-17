---
name: oo-investoday-mcp
description: "Investoday MCP (data-api.investoday.net). Use this skill for ANY Investoday MCP request — searching and reading data. Whenever a task involves Investoday MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Investoday MCP"
  author: "OOMOL"
  version: "1.0.3"
  services: ["investoday_mcp"]
  icon: "https://static.oomol.com/logo/third-party/investoday_mcp.png"
---

# Investoday MCP

Operate **Investoday MCP** through your OOMOL-connected account. This skill calls the `investoday_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Investoday MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "investoday_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "investoday_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a current Investoday MCP tool with JSON arguments after checking its live schema and behavior annotations.
- `entity_recognition` — Run the Investoday entity recognition operation.
- `generate_chart` — Generate chart with Investoday.
- `generate_nex_chart` — Generate nex chart with Investoday.
- `get_announcement_content` — Get announcement content data from Investoday.
- `get_chain_bond_issuers` — Get chain bond issuers data from Investoday.
- `get_chain_industry_info` — Get chain industry info data from Investoday.
- `get_chain_pro_relation` — Get chain pro relation data from Investoday.
- `get_chain_product_info` — Get chain product info data from Investoday.
- `get_chain_sec_basic_info` — Get chain sec basic info data from Investoday.
- `get_cn_trade_calender_list` — Get China trade calender list data from Investoday.
- `get_company_profiles` — Get company profiles data from Investoday.
- `get_concept_realtime_quote` — Get concept realtime quote data from Investoday.
- `get_concept_stock_realtime_quote` — Get concept stock realtime quote data from Investoday.
- `get_fin_health_history` — Get financial health history data from Investoday.
- `get_fund_award_records` — Get fund award records data from Investoday.
- `get_fund_basic_info` — Get fund basic info data from Investoday.
- `get_fund_categories` — Get fund categories data from Investoday.
- `get_fund_code_assoc` — Get fund code assoc data from Investoday.
- `get_fund_company_evals` — Get fund company evals data from Investoday.
- `get_fund_listings_record` — Get fund listings record data from Investoday.
- `get_fund_manager_basic_info` — Get fund manager basic info data from Investoday.
- `get_fund_peer_avg_metric` — Get fund peer average metric data from Investoday.
- `get_fund_performance_attribution` — Get fund performance attribution data from Investoday.
- `get_fund_quote_realtime` — Get fund quote realtime data from Investoday.
- `get_hk_stock_basic_info` — Get Hong Kong stock basic info data from Investoday.
- `get_hk_stock_name_change` — Get Hong Kong stock name change data from Investoday.
- `get_hk_stock_range_change` — Get Hong Kong stock range change data from Investoday.
- `get_hk_stock_transfers` — Get Hong Kong stock transfers data from Investoday.
- `get_hk_stock_turnrate` — Get Hong Kong stock turnrate data from Investoday.
- `get_hk_stock_valuations` — Get Hong Kong stock valuations data from Investoday.
- `get_index_basic_info` — Get index basic info data from Investoday.
- `get_index_range_gains` — Get index range gains data from Investoday.
- `get_index_realtime_quotes` — Get index realtime quotes data from Investoday.
- `get_index_valuation` — Get index valuation data from Investoday.
- `get_industry_financial_overview` — Get industry financial overview data from Investoday.
- `get_industry_market_stats` — Get industry market stats data from Investoday.
- `get_industry_realtime_quote` — Get industry realtime quote data from Investoday.
- `get_industry_stock_realtime_quote` — Get industry stock realtime quote data from Investoday.
- `get_market_change_ratio_status` — Get current market breadth, including rising, falling and limit-up or limit-down stock counts.
- `get_report_earnings_forecast_rating` — Get report earnings forecast rating data from Investoday.
- `get_stk_fundamentals` — Get stock fundamentals data from Investoday.
- `get_stk_investment_risks` — Get stock investment risks data from Investoday.
- `get_stk_sw_idu_returns` — Get stock sw industry returns data from Investoday.
- `get_stk_unwind_sig_stat` — Get stock unwind sig stat data from Investoday.
- `get_stock_basic_info` — Get basic information for one or multiple Shanghai, Shenzhen or Beijing stocks.
- `get_stock_business_themes` — Get stock business themes data from Investoday.
- `get_stock_fin_subitem_score` — Get stock financial subitem score data from Investoday.
- `get_stock_finance_growth_ability` — Get stock finance growth ability data from Investoday.
- `get_stock_finance_growth_ability_hist` — Get stock finance growth ability historical data from Investoday.
- `get_stock_finance_industry_compare` — Get stock finance industry compare data from Investoday.
- `get_stock_finance_profit_ability` — Get stock finance profit ability data from Investoday.
- `get_stock_finance_profit_ability_hist` — Get stock finance profit ability historical data from Investoday.
- `get_stock_finance_strength` — Get stock finance strength data from Investoday.
- `get_stock_finance_valuation` — Get stock finance valuation data from Investoday.
- `get_stock_finance_valuation_hist` — Get stock finance valuation historical data from Investoday.
- `get_stock_financial_strength_ext_hist` — Get stock financial strength ext historical data from Investoday.
- `get_stock_former_names` — Get stock former names data from Investoday.
- `get_stock_industries` — Get stock industries data from Investoday.
- `get_stock_margin_requirement` — Get stock margin requirement data from Investoday.
- `get_stock_margin_securities` — Get stock margin securities data from Investoday.
- `get_stock_prospects` — Get stock prospects data from Investoday.
- `get_stock_quote_realtime` — Get the latest realtime quote for one Shanghai, Shenzhen or Beijing stock.
- `get_stock_quote_rt_ext` — Get stock quote realtime ext data from Investoday.
- `get_stock_realtime_fund_flow` — Get stock realtime fund flow data from Investoday.
- `get_stock_realtime_quote_merge` — Get stock realtime quote merge data from Investoday.
- `get_stock_rights_issues` — Get stock rights issues data from Investoday.
- `get_stock_score` — Get stock score data from Investoday.
- `get_stock_val_indicators` — Get stock valuation indicators including market capitalization, PE, PB and PS over a date range.
- `get_trade_special_date` — Get trade special date data from Investoday.
- `is_trade_date` — Check whether trade date with Investoday.
- `list__idu_fin_ind_sol_avg` — List industry financial indicator sol average data from Investoday.
- `list_announcements` — List announcements data from Investoday.
- `list_bonds_basic` — List bonds basic data from Investoday.
- `list_bonds_coupons` — List bonds coupons data from Investoday.
- `list_bonds_ratings` — List bonds ratings data from Investoday.
- `list_bonds_yield_curve` — List bonds yield curve data from Investoday.
- `list_cb_basic` — List convertible bond basic data from Investoday.
- `list_cb_daily` — List convertible bond daily data from Investoday.
- `list_cb_plans` — List convertible bond plans data from Investoday.
- `list_cb_valuation` — List convertible bond valuation data from Investoday.
- `list_chain_com_main_pro` — List chain com main pro data from Investoday.
- `list_chain_pro_ind_maps` — List chain pro indicator maps data from Investoday.
- `list_concept_etf_mapping` — List concept etf mapping data from Investoday.
- `list_concept_hold_fund` — List concept hold fund data from Investoday.
- `list_concept_hold_fund_batch` — List concept hold fund batch data from Investoday.
- `list_concept_real_quote` — List concept real quote data from Investoday.
- `list_concepts` — List concepts data from Investoday.
- `list_currency_yield_history` — List currency yield history data from Investoday.
- `list_economic_cn_cpi` — List economic China cpi data from Investoday.
- `list_economic_cn_ppi` — List economic China ppi data from Investoday.
- `list_entity_related_news` — List entity related news data from Investoday.
- `list_etf_constituent_stks` — List etf constituent stks data from Investoday.
- `list_etf_sub_red_lists` — List etf sub red lists data from Investoday.
- `list_fin_ind_cash_coll_q` — List financial indicator cash coll quarterly data from Investoday.
- `list_fin_ind_cash_collect` — List financial indicator cash collect data from Investoday.
- `list_fin_ind_operating` — List financial indicator operating data from Investoday.
- `list_fin_ind_operating_q` — List financial indicator operating quarterly data from Investoday.
- `list_fin_ind_profit` — List financial indicator profit data from Investoday.
- `list_fin_ind_profit_q` — List financial indicator profit quarterly data from Investoday.
- `list_fin_ind_profit_ttm` — List financial indicator profit ttm data from Investoday.
- `list_fin_ind_solvency` — List financial indicator solvency data from Investoday.
- `list_fin_ind_solvency_q` — List financial indicator solvency quarterly data from Investoday.
- `list_fin_ind_solvency_ttm` — List financial indicator solvency ttm data from Investoday.
- `list_fund_adj_navs` — List fund adjusted navs data from Investoday.
- `list_fund_adj_quotes` — List fund adjusted quotes data from Investoday.
- `list_fund_all` — List fund all data from Investoday.
- `list_fund_announcements` — List fund announcements data from Investoday.
- `list_fund_current_manager_returns` — List fund current manager returns data from Investoday.
- `list_fund_daily_quotes` — List fund daily quotes data from Investoday.
- `list_fund_dividend_distributions` — List fund dividend distributions data from Investoday.
- `list_fund_fee_structures` — List fund fee structures data from Investoday.
- `list_fund_fin_inds` — List fund financial indicators data from Investoday.
- `list_fund_fin_inds_q` — List fund financial indicators quarterly data from Investoday.
- `list_fund_flow` — List fund flow data from Investoday.
- `list_fund_hold_industry` — List fund hold industry data from Investoday.
- `list_fund_hold_structures` — List fund hold structures data from Investoday.
- `list_fund_holdings_perf` — List fund holdings performance data from Investoday.
- `list_fund_idx_ret_corr` — List fund index ret corr data from Investoday.
- `list_fund_invest_targets` — List fund invest targets data from Investoday.
- `list_fund_margin_trade` — List fund margin trade data from Investoday.
- `list_fund_mgr_hist_per` — List fund manager historical per data from Investoday.
- `list_fund_mgr_perf` — List fund manager performance data from Investoday.
- `list_fund_mgr_returns` — List fund manager returns data from Investoday.
- `list_fund_nav_history` — List fund nav history data from Investoday.
- `list_fund_oscillator_indicators` — List fund oscillator indicators data from Investoday.
- `list_fund_perf_benchmarks` — List fund performance benchmarks data from Investoday.
- `list_fund_portfolio_asset_holdings` — List fund portfolio asset holdings data from Investoday.
- `list_fund_portfolio_bond_holdings` — List fund portfolio bond holdings data from Investoday.
- `list_fund_portfolio_stock_holdings` — List fund portfolio stock holdings data from Investoday.
- `list_fund_price_volume_indicators` — List fund price volume indicators data from Investoday.
- `list_fund_return_rate` — List fund return rate data from Investoday.
- `list_fund_share_splits` — List fund share splits data from Investoday.
- `list_fund_shares` — List fund shares data from Investoday.
- `list_fund_strength_trend_indicators` — List fund strength trend indicators data from Investoday.
- `list_fund_tech_indicators` — List fund tech indicators data from Investoday.
- `list_futures_kline_minute` — List futures kline minute data from Investoday.
- `list_gover_bond_yield` — List gover bond yield data from Investoday.
- `list_hk_stock_adjusted_quotes` — List Hong Kong stock adjusted quotes data from Investoday.
- `list_hk_stock_balance_sheet` — List Hong Kong stock balance sheet data from Investoday.
- `list_hk_stock_capital_changes` — List Hong Kong stock capital changes data from Investoday.
- `list_hk_stock_cash_flows` — List Hong Kong stock cash flows data from Investoday.
- `list_hk_stock_dividends` — List Hong Kong stock dividends data from Investoday.
- `list_hk_stock_income_statements` — List Hong Kong stock income statements data from Investoday.
- `list_hk_stock_oscillator_indicators` — List Hong Kong stock oscillator indicators data from Investoday.
- `list_hk_stock_price_volume_indicators` — List Hong Kong stock price volume indicators data from Investoday.
- `list_hk_stock_strength_trend_indicators` — List Hong Kong stock strength trend indicators data from Investoday.
- `list_idu_concept_mappings` — List industry concept mappings data from Investoday.
- `list_idu_turnover_rates` — List industry turnover rates data from Investoday.
- `list_idx_idu_exposure` — List index industry exposure data from Investoday.
- `list_ind_real_quote_v2` — List indicator real quote v2 data from Investoday.
- `list_index_finance` — List index finance data from Investoday.
- `list_index_oscillator_indicators` — List index oscillator indicators data from Investoday.
- `list_index_price_volume_indicators` — List index price volume indicators data from Investoday.
- `list_index_quote_barch` — List index quote barch data from Investoday.
- `list_index_sample` — List index sample data from Investoday.
- `list_index_strength_trend_indicators` — List index strength trend indicators data from Investoday.
- `list_index_technical_indicators` — List index technical indicators data from Investoday.
- `list_industries` — List industries data from Investoday.
- `list_industry_etf_mapping` — List industry etf mapping data from Investoday.
- `list_industry_excess_alph` — List industry excess alph data from Investoday.
- `list_industry_fin_ttm` — List industry financial ttm data from Investoday.
- `list_industry_forecasts` — List industry forecasts data from Investoday.
- `list_industry_hold_fund` — List industry hold fund data from Investoday.
- `list_industry_hold_fund_batch` — List industry hold fund batch data from Investoday.
- `list_industry_pros_idx` — List industry pros index data from Investoday.
- `list_industry_prosperity_index` — List industry prosperity index data from Investoday.
- `list_industry_quote` — List industry quote data from Investoday.
- `list_industry_rotation` — List industry rotation data from Investoday.
- `list_industry_val_ind` — List industry valuation indicator data from Investoday.
- `list_macro_equity_val` — List macro equity valuation data from Investoday.
- `list_macro_exch_rates` — List macro exch rates data from Investoday.
- `list_macro_fiscal_exp` — List macro fiscal exp data from Investoday.
- `list_macro_fixed_asset` — List macro fixed asset data from Investoday.
- `list_macro_goods_trade` — List macro goods trade data from Investoday.
- `list_macro_re_invest` — List macro re invest data from Investoday.
- `list_macro_retail_area` — List macro retail area data from Investoday.
- `list_macro_rmb_credit` — List macro rmb credit data from Investoday.
- `list_macro_soc_fin` — List macro soc financial data from Investoday.
- `list_macro_spot_quotes` — List macro spot quotes data from Investoday.
- `list_money_market_repo_in` — List money market repo in data from Investoday.
- `list_money_supplies` — List money supplies data from Investoday.
- `list_news` — List news data from Investoday.
- `list_per_share_indicators` — List per share indicators data from Investoday.
- `list_per_share_indicators_q` — List per share indicators quarterly data from Investoday.
- `list_perf_benchmark_quote` — List performance benchmark quote data from Investoday.
- `list_portfolio_fund_holdings` — List portfolio fund holdings data from Investoday.
- `list_report_institutions` — List report institutions data from Investoday.
- `list_report_research` — Find research reports by stock, industry, institution or category, with optional keywords and publication dates.
- `list_report_stock_forecast_ratings` — List report stock forecast ratings data from Investoday.
- `list_report_vector-search` — List report vector search data from Investoday.
- `list_research_sentiment` — List research sentiment data from Investoday.
- `list_social_financing_sto` — List social financing sto data from Investoday.
- `list_soctk_strength_trend_indicators` — List soctk strength trend indicators data from Investoday.
- `list_stk_balan_sheet_pit` — List stock balan sheet pit data from Investoday.
- `list_stk_balance_sht_ttm` — List stock balance sht ttm data from Investoday.
- `list_stk_consultations` — List stock consultations data from Investoday.
- `list_stk_dragon_tiger_broke_details` — List stock dragon tiger broke details data from Investoday.
- `list_stk_dupont_analysis` — List stock dupont analysis data from Investoday.
- `list_stk_fin_ind_sw_rnk_q` — List stock financial indicator sw rnk quarterly data from Investoday.
- `list_stk_income_state_pit` — List stock income state pit data from Investoday.
- `list_stk_tech_signals` — List stock tech signals data from Investoday.
- `list_stk_trend_structure` — List stock trend structure data from Investoday.
- `list_stk_unwind_signal_de` — List stock unwind signal de data from Investoday.
- `list_stock_absorption_mergers` — List stock absorption mergers data from Investoday.
- `list_stock_adjusted_quotes` — Get forward-adjusted daily stock prices over a date range, including batch queries and pagination.
- `list_stock_all` — List stock all data from Investoday.
- `list_stock_arbitration_cases` — List stock arbitration cases data from Investoday.
- `list_stock_audit_opinion` — List stock audit opinion data from Investoday.
- `list_stock_balance_sheet` — List stock balance sheet data from Investoday.
- `list_stock_balance_sheet_q` — List stock balance sheet quarterly data from Investoday.
- `list_stock_block_trades` — List stock block trades data from Investoday.
- `list_stock_capital_changes` — List stock capital changes data from Investoday.
- `list_stock_cash_flows` — List stock cash flows data from Investoday.
- `list_stock_cash_flows_pit` — List stock cash flows pit data from Investoday.
- `list_stock_cash_flows_q` — List stock cash flows quarterly data from Investoday.
- `list_stock_cash_flows_ttm` — List stock cash flows ttm data from Investoday.
- `list_stock_concept_classifications` — List stock concept classifications data from Investoday.
- `list_stock_core_mgmt_changes` — List stock core mgmt changes data from Investoday.
- `list_stock_daily_fund_flows` — List stock daily fund flows data from Investoday.
- `list_stock_dcf_result` — List stock dcf result data from Investoday.
- `list_stock_dragon_tiger_details` — List stock dragon tiger details data from Investoday.
- `list_stock_earnings_bulletins` — List stock earnings bulletins data from Investoday.
- `list_stock_esg_rating` — List stock esg rating data from Investoday.
- `list_stock_executive_shareholding_change` — List stock executive shareholding change data from Investoday.
- `list_stock_fin_derivative_inds` — List stock financial derivative indicators data from Investoday.
- `list_stock_fin_derivative_inds_q` — List stock financial derivative indicators quarterly data from Investoday.
- `list_stock_fin_derivative_inds_ttm` — List stock financial derivative indicators ttm data from Investoday.
- `list_stock_fin_ind_grow_q` — List stock financial indicator grow quarterly data from Investoday.
- `list_stock_fin_ind_growth` — List stock financial indicator growth data from Investoday.
- `list_stock_freeze_details` — List stock freeze details data from Investoday.
- `list_stock_fund_flow_s` — List stock fund flow s data from Investoday.
- `list_stock_growth_op_revs` — List stock growth op revs data from Investoday.
- `list_stock_holder_cnt` — List stock holder cnt data from Investoday.
- `list_stock_income_statement_q` — List stock income statement quarterly data from Investoday.
- `list_stock_income_statement_ttm` — List stock income statement ttm data from Investoday.
- `list_stock_income_statements` — List stock income statements data from Investoday.
- `list_stock_inst_research` — List stock inst research data from Investoday.
- `list_stock_institutional_holdings_stats` — List stock institutional holdings stats data from Investoday.
- `list_stock_limit_up_down` — List stock limit up down data from Investoday.
- `list_stock_major_contracts` — List stock major contracts data from Investoday.
- `list_stock_major_sup_cust` — List stock major sup cust data from Investoday.
- `list_stock_management_dirs` — List stock management dirs data from Investoday.
- `list_stock_margin_trade` — List stock margin trade data from Investoday.
- `list_stock_margin_trade_totals` — List stock margin trade totals data from Investoday.
- `list_stock_market_ind_dm` — List stock market indicator data mining data from Investoday.
- `list_stock_offerings` — List stock offerings data from Investoday.
- `list_stock_op_reviews` — List stock op reviews data from Investoday.
- `list_stock_oscillator_indicators` — List stock oscillator indicators data from Investoday.
- `list_stock_performance_metrics` — List stock performance metrics data from Investoday.
- `list_stock_pledge_details` — List stock pledge details data from Investoday.
- `list_stock_price_pattern` — List stock price pattern data from Investoday.
- `list_stock_price_volume_indicators` — List stock price volume indicators data from Investoday.
- `list_stock_related_transactions` — List stock related transactions data from Investoday.
- `list_stock_report_schema` — List stock report schema data from Investoday.
- `list_stock_repurchase_plans` — List stock repurchase plans data from Investoday.
- `list_stock_share_adj_factors` — List stock share adjusted factors data from Investoday.
- `list_stock_special_notices` — List stock special notices data from Investoday.
- `list_stock_strength_trend_indicators` — List stock strength trend indicators data from Investoday.
- `list_stock_tender_offers` — List stock tender offers data from Investoday.
- `list_stock_top10_circulating_shareh` — List stock top10 circulating shareh data from Investoday.
- `list_stock_turnover_rates` — List stock turnover rates data from Investoday.
- `list_stock_unadjusted_quotes` — List stock unadjusted quotes data from Investoday.
- `list_stock_up_down_list` — List stock up down list data from Investoday.
- `list_stock_val_factors` — List stock valuation factors data from Investoday.
- `list_stock_violation_penalt` — List stock violation penalt data from Investoday.
- `list_stock_vol_indicators` — List stock vol indicators data from Investoday.
- `list_stock_volume_price` — List stock volume price data from Investoday.
- `list_stocks_dividends` — List stocks dividends data from Investoday.
- `list_stocks_public_offering_place` — List stocks public offering place data from Investoday.
- `list_stocks_rights_issue_res` — List stocks rights issue res data from Investoday.
- `list_subscription_redemption_status` — List subscription redemption status data from Investoday.
- `list_tools` — Discover the current Investoday financial market data and research MCP tools with their live input schemas.
- `search` — Search securities, funds, indices, industries and concepts by name or code.
- `search_announcements` — Search announcement passages by meaning, optionally filtering by stock, announcement ID and publication dates.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Investoday MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Investoday MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/investoday_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Investoday MCP homepage: https://data-api.investoday.net/mcp
- API documentation: https://std.investoday.net/apidocs/api-overview
