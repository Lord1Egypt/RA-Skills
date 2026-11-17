# 量化引擎输入

将 MCP、东财和 Serenity 结果规范为一个 JSON 对象。所有百分比字段使用百分数，例如 `-3.2` 表示 `-3.2%`。

## 首选输入：HuahuaDaily 聚合上下文

正式运行优先直接使用：

```json
get_quant_strategy_context({
  "as_of_date": "YYYY-MM-DD",
  "group_id": "",
  "mode": "live",
  "history_window": "1y"
})
```

`scripts/signal_rules.py` 可直接读取该接口返回的 `schemaVersion="quant_strategy_context.v1"` JSON，无需 Agent 手工拼接旧格式。脚本会自动映射：

- `asOfDate` → `as_of`
- `execution.serverTime/isTradingDay/cutoffTime/nextTradingDay` → `execution`
- `audit.recordsDataUpdatedAt/portfolioEtag/contextHash` → `provenance`
- `market.hs300.ma20/ma60/validPoints` → `benchmark.metric_overrides`
- `market.crossMarketQuotes` → `market.indices` 的实时横截面辅助序列
- `portfolio.totalMarketValue` → `portfolio.total_market_value`
- `portfolio.risk.maxDrawdownPct/currentDrawdownPct/configuredMaxDrawdownLimitPct` → 组合风险与回撤门禁
- `portfolio.risk.cumulativeReturnPct/annualizedVolatilityPct/benchmarkReturnPct/relativeReturnPct/coveragePct` → 组合复盘指标
- `portfolio.holdings[]` → `funds[]`
- `holdings[].metrics.r20Pct/r60Pct/r120Pct/r250Pct/ma20/ma60/bias20Pct/maxDrawdownPct/annualizedVolatilityPct/navPoints` → `funds[].metric_overrides`
- `holdings[].realtime` → `funds[].realtime.estimate_*`
- `holdings[].qdiiNight` → `funds[].realtime.qdii_night_*`
- `holdings[].tradeConstraints` → `funds[].fees`
- `dca.plans` → `portfolio.dca_plans`
- `pendingTransactions.pendingBuyAmount` → `portfolio.pending_buy_amount`

聚合上下文不包含东方财富资讯、情绪或 Serenity 证据。若正式报告需要证据层，Agent 应在调用聚合接口后追加这些 skills，并把结果补到 `news_factor`、`sentiment_factor`、`serenity_checks`；如果未补充，报告必须标注“外部证据未调用/未知”，不能伪装成中性。

`readyForAnalysis=false` 时不要运行可交付策略；`readyForAction=false` 时可以运行复盘和评分，但最终可执行买入/卖出金额必须为 0。

## 兼容输入：手工构造旧 schema

仅当 `get_quant_strategy_context` 不可用或需要离线回放时，才使用以下旧 schema。

```json
{
  "as_of": "2026-07-14",
  "strategy": {
    "id": "hua-personal-strategy",
    "version": "mcp-quant-v8"
  },
  "timestamps": {
    "portfolio": "2026-07-14T15:05:00+08:00",
    "portfolio_history": "2026-07-14",
    "market": "2026-07-14T14:05:00+08:00",
    "news": "2026-07-14T13:50:00+08:00"
  },
  "execution": {
    "run_at": "2026-07-14T14:30:00+08:00",
    "market_timezone": "Asia/Shanghai",
    "trade_cutoff_time": "15:00",
    "is_trading_day": true,
    "next_trading_day": "2026-07-15",
    "source": "get_status/calculate_trading_dates/get_next_trading_day"
  },
  "provenance": {
    "sync_updated_at": "2026-07-14T15:05:00+08:00",
    "sync_etag": "cloud-etag-from-get_sync_meta",
    "records_data_updated_at": "2026-07-14T15:05:00+08:00",
    "records_etag": "optional-records-etag",
    "strategy_preferences_source": "get_records.strategyPreferences",
    "input_built_at": "2026-07-14T15:08:00+08:00"
  },
  "benchmark": {
    "code": "sh000300",
    "metric_overrides": {
      "points": 250,
      "ma20": 4886.07,
      "ma60": 4852.56
    },
    "history": [
      {"date": "2026-04-01", "close": 3912.34}
    ]
  },
  "market": {
    "previous_mode": "RANGE",
    "a_share_market_regime": {
      "status": "BULL | RANGE | BEAR | RISK_VALIDATION | UNKNOWN",
      "evidence": ["上证/沪深300/创业板/科创50的日线、周线、月线或缺失说明"],
      "missing_periods": []
    },
    "growth_style_regime": {
      "status": "STRONG | WEAKENING | BROKEN | UNKNOWN",
      "evidence": ["科创50/创业板/半导体ETF/恒生科技/纳指/KOSPI"],
      "missing_periods": []
    },
    "holding_weighted_regime": {
      "status": "ATTACK | DEFENSIVE | CASH_WAIT | UNKNOWN",
      "evidence": ["方向权重、风险贡献、高相关簇、实时估值、QDII夜盘"]
    },
    "decline_type": "leverage_flush | valuation_reset | bull_washout | systemic_bear | unknown",
    "decline_type_evidence": [],
    "indices": {
      "NDX": [{"date": "2026-04-01", "value": 18000, "change": 0.42}],
      "KS11": [{"date": "2026-04-01", "value": 2850, "change": 0.31}],
      "HSTECH": [{"date": "2026-04-01", "value": 4200, "change": -0.22}],
      "000688": [{"date": "2026-04-01", "value": 980, "change": 0.18}],
      "512480": [{"date": "2026-04-01", "value": 1.12, "change": 0.65}]
    }
  },
  "portfolio": {
    "total_market_value": 120000,
    "portfolio_drawdown_pct": 8.4,
    "max_drawdown_limit_pct": 10,
    "portfolio_drawdown_source": "get_portfolio_nav_history",
    "portfolio_nav_coverage_pct": 96.5,
    "portfolio_nav_warnings": [],
    "incremental_cash_available": 8000,
    "defensive_allocation_plan": {
      "action": "现金等待 | 转入防守仓 | 无需防守迁移 | unknown",
      "cash_or_money_fund_pct": null,
      "short_bond_pct": null,
      "gold_pct": null,
      "low_vol_equity_pct": null,
      "notes": []
    },
    "dca_plans": [
      {
        "code": "000001",
        "name": "基金名称",
        "group_name": "我的账户",
        "amount": 500,
        "frequency": "每周",
        "next_date": "2026-07-17",
        "status": "active",
        "source": "HuahuaDaily"
      }
    ]
  },
  "funds": [
    {
      "code": "000001",
      "name": "必须使用 get_records 原名",
      "group_name": "必须使用 get_records 原分组",
      "direction": "半导体设备",
      "market_value": 18000,
      "holding_return_pct": -2.5,
      "history_source": "get_batch_fund_nav_history",
      "history_complete": true,
      "coverage_start": "2025-01-01",
      "coverage_end": "2026-07-14",
      "history": [
        {"date": "2026-04-01", "nav": 1.2345}
      ],
      "metric_overrides": {
        "points": 250,
        "r20": 3.2,
        "r60": 8.5,
        "r120": 18.0,
        "r250": 42.0,
        "bias20": 1.4,
        "max_drawdown_pct": 12.5,
        "annualized_volatility_pct": 28.0
      },
      "flow_3d": [],
      "eastmoney_checks": {
        "numeric_status": "supportive",
        "news_status": "none",
        "latest_source_time": "2026-07-14T13:50:00+08:00"
      },
      "news_factor": {
        "status": "supportive",
        "strength": "medium",
        "veto": false,
        "sources": [
          {"source": "东财", "published_at": "2026-07-14T13:50:00+08:00", "title": "消息标题"}
        ],
        "note": "消息面摘要"
      },
      "sentiment_factor": {
        "status": "neutral",
        "strength": "weak",
        "veto": false,
        "note": "情绪面摘要"
      },
      "realtime": {
        "estimate_change_pct": -0.8,
        "estimate_as_of": "2026-07-14T14:35:00+08:00",
        "estimate_source": "HuahuaDaily",
        "estimate_freshness": "fresh",
        "estimate_nav_date": "2026-07-13",
        "estimate_display_date": "2026-07-14",
        "estimate_publish_date": "2026-07-14",
        "estimate_official_attribution_date": "2026-07-14",
        "estimate_data_date_label": "2026-07-13",
        "estimate_vs_actual": {
          "publish_date": "2026-07-14",
          "nav_date": "2026-07-13",
          "estimate_change": 0.41,
          "actual_change": 0.38
        },
        "intraday_flow": -120000000,
        "intraday_flow_as_of": "2026-07-14T14:30:00+08:00",
        "qdii_night_status": null,
        "qdii_night_estimated_change_pct": null,
        "qdii_night_quote_as_of": null,
        "qdii_night_actual_session_date": null,
        "qdii_night_freshness": null,
        "qdii_night_coverage_pct": null,
        "qdii_night_availability": null,
        "qdii_night_reason": null,
        "qdii_night_fx": {"usd_cny": null, "hkd_cny": null},
        "qdii_night_holdings": []
      },
      "serenity_checks": {
        "evidence_strength": "strong",
        "risk_veto": false,
        "summary": "产业链证据摘要"
      },
      "catalyst_status": "confirmed",
      "evidence_strength": "strong",
      "risk_veto": false,
      "fees": {
        "purchasable": true,
        "daily_purchase_limit": 50000,
        "confirm_days": 1
      },
      "night_status": null,
      "autoInvestConfig": {
        "id": "plan_xxx",
        "enabled": true,
        "amount": 10,
        "feeRate": 0.1,
        "cycle": "DAILY",
        "nextRunDate": "2026-07-15",
        "timeMode": "PRE_MARKET"
      }
    }
  ],
  "opportunity_pool": {
    "directions": [
      {
        "name": "半导体设备",
        "asset_class": "A股主题",
        "current_weight_pct": 18.5,
        "history": [
          {"date": "2026-04-01", "close": 1234.56}
        ],
        "valuation_percentile": 68,
        "flow_5d_pct": 1.2,
        "crowding_percentile": 72,
        "max_drawdown_pct": 22,
        "news_factor": {"status": "supportive", "strength": "medium", "veto": false, "sources": [], "note": "方向消息摘要"},
        "sentiment_factor": {"status": "risk_on", "strength": "medium", "veto": false, "note": "方向情绪摘要"},
        "serenity_checks": {"evidence_strength": "medium", "risk_veto": false, "summary": "方向证据链"}
      }
    ],
    "fund_candidates": []
  }
}
```

## 兼容 schema 字段来源

- 以下字段来源适用于手工构造旧 schema。若输入是 `get_quant_strategy_context` 原始返回，脚本会按上文自动映射，不需要 Agent 手工填写。
- `timestamps.portfolio`：聚合上下文取 `audit.recordsDataUpdatedAt`；降级路径取 `get_records.dataUpdatedAt`。
- `timestamps.portfolio_history`：聚合上下文取 `portfolio.risk.dataAsOf` 或 `audit.navCutoffDate`；降级路径取 `get_portfolio_nav_history` 的截止日期或数据覆盖截止日期。
- `timestamps.market`：聚合上下文取 `audit.marketDataAsOf`；降级路径取指数、估值和资金流返回的最新时间。
- `timestamps.news`：东财资讯中用于结论的最新发布时间；没有使用资讯时填 `null`。
- `execution.run_at`：报告实际运行时间，必须使用北京时间 ISO 字符串。
- `execution.trade_cutoff_time`：场外基金常规截止线，默认 `15:00`。
- `execution.is_trading_day`：优先来自 `get_status` 或交易日接口；非交易日必须为 `false`。
- `execution.next_trading_day`：优先来自 `calculate_trading_dates` 或 `get_next_trading_day`。
- `execution.source`：交易窗口判断来源。若 `run_at >= 15:00` 或 `is_trading_day=false`，所有 `trade_action.buy_amount`、`trade_action.sell_amount` 必须为 0，报告只能写“下一交易日重新确认”，不得写“今天加仓/今天卖出/今天执行”。
- `provenance.sync_updated_at` 与 `provenance.sync_etag`：聚合上下文取 `audit.recordsDataUpdatedAt`、`audit.portfolioEtag`；降级路径取 `get_sync_meta`。
- `provenance.records_data_updated_at`：聚合上下文取 `audit.recordsDataUpdatedAt`；降级路径取 `get_records.dataUpdatedAt`。必须与报告展示的持仓同步时间一致。
- `provenance.strategy_preferences_source`：聚合上下文填 `get_quant_strategy_context.portfolio.risk.configuredMaxDrawdownLimitPct`；降级路径填 `get_records.strategyPreferences`。若无法读取，必须写 `unknown` 并禁止可执行新增金额。
- `benchmark.history`：`get_benchmark_history({"code":"sh000300"})`；按日期升序或降序均可，引擎会排序。
- `benchmark.metric_overrides`：可选。仅当上游 builder 已经用官方基准历史计算好 MA20/MA60 等字段时使用；完整 `benchmark.history` 优先，不能由 LLM 猜测。
- `portfolio.total_market_value`：聚合上下文取 `portfolio.totalMarketValue`；降级路径用 `get_records.summary` 与 `get_summary` 交叉校验。组合市值、持有收益和累计收益均为官方净值/真实交易口径，不包含盘中估算或 QDII 夜盘。
- `portfolio.portfolio_drawdown_pct`：聚合上下文取 `portfolio.risk.maxDrawdownPct`；降级路径取 `get_portfolio_nav_history` 的真实最大回撤；未知填 `null`。
- `portfolio.official_max_drawdown_pct`：官方最大回撤，等同聚合上下文 `portfolio.risk.maxDrawdownPct`。用于真实收益、审计、报告复盘。
- `portfolio.official_current_drawdown_pct`：官方当前回撤，聚合上下文取 `portfolio.risk.currentDrawdownPct`。用于估算盘中执行回撤的基准。
- `portfolio.execution_estimated_today_return_pct`：按持仓权重加总的今日实时估值/QDII 夜盘估算冲击。可由引擎计算，也可由上游服务端提供；不得计入真实收益。
- `portfolio.execution_drawdown_pct`：盘中执行回撤估算。用于风控门禁和停止新增；不得写成官方最大回撤。
- `portfolio.execution_drawdown_source`：如 `weighted_realtime_estimate_qdii_night_for_execution_only`。必须注明“仅执行层估算”。
- `portfolio.max_drawdown_limit_pct`：聚合上下文取 `portfolio.risk.configuredMaxDrawdownLimitPct`；降级路径取 `get_records.strategyPreferences.maxDrawdownLimitPct`。0 表示未启用回撤门禁，未知填 `null` 并在数据质量中标注，禁止自行假定 10%。
- `market.previous_mode`：可从 `get_quant_snapshots(latest_only=true)` 的上次 `market_mode.mode` 读取；未知填 `null`。仅用于 1.8%–2.2% 牛熊缓冲区，只保持同方向的上次 BULL/BEAR，不得用来覆盖明确趋势信号。
- `market.a_share_market_regime` / `market.growth_style_regime` / `market.holding_weighted_regime`：由 Agent 使用 HuahuaDaily、东财和必要的行情历史计算得到。它们不是 HuahuaDaily MCP 必须返回的确定性信号。缺少周线/月线时填入 `missing_periods`，不得伪造。
- `market.decline_type`：下跌性质分类，必须在涉及牛熊/离场/避险/板块迁移时填写。无法确认时填 `unknown` 并说明下一交易日验证条件。
- `market.indices` 或顶层 `indices`：可选但推荐。用于多指数加权基准和跨市场因子，键名可包含 `NDX`、`KS11`、`HSTECH`、`000688`、`512480`、`000300` 等。每个序列至少包含 `date` 和 `change`，可同时包含 `value/close`。缺失时引擎回退到单一 `benchmark.history`，但报告应标注“多指数基准未完全接入”。
- `portfolio.portfolio_drawdown_source`：聚合上下文填 `get_quant_strategy_context.portfolio.risk`；降级路径填 `get_portfolio_nav_history`；未知填 `unknown`。
- `portfolio.portfolio_nav_coverage_pct` 与 `portfolio.portfolio_nav_warnings`：聚合上下文取 `portfolio.risk.coveragePct` 和顶层 `warnings`；降级路径取 `get_portfolio_nav_history` 的覆盖率和缺失警告，用于输出解释。
- `portfolio.incremental_cash_available`：用户确认的本月剩余增量资金。未知填 `null`，引擎使用 3,000 元保守默认值并在输出标注。
- `portfolio.dca_plans` / `portfolio.scheduled_investments`：用户在 App 中设置的定投计划，聚合上下文取 `dca.plans`；降级路径取 `get_raw_sync_data({"include_json_text": false}).data.funds[].autoInvestConfig`。不得由 Agent 猜测。至少包含基金代码、金额、频率、下次日期、状态和账户分组。定投是未来现金流执行计划，不属于组合净值涨幅；若未传入，报告只能写“本轮未传入定投设置”，不能判断定投继续、暂停或转向。
- `portfolio.defensive_allocation_plan`：组合层防守安排。只表达现金/货基/短债/黄金/红利低波等资产级方向，不得伪造成系统筛选基金。宽基指数不得放入“防守仓”，只能作为低 Beta 权益观察仓。
- `funds[].autoInvestConfig`：HuahuaDaily raw 主数据中的定投原字段。输入构造器应优先把它规范成 `portfolio.dca_plans`，但可以保留该字段；引擎会兜底读取 `id/enabled/amount/cycle/nextRunDate/timeMode/feeRate`。`enabled=false` 表示暂停计划，不应当作仍在自动流入。
- `funds[].pendingBuyTransactions` 与 `funds[].inTransitAmount`：在途申购/待确认交易，只能用于解释资金占用和确认节奏，不能反推未来定投计划。
- 当前策略不使用 `defensive_fund_codes`。不要把 016858、023299 或任何持仓默认归为防御基金。
- `funds[].direction`：基金画像和真实持仓结构；不清楚填 `unknown`。
- `funds[].history`：`get_batch_fund_nav_history` 返回的官方净值序列，不逐只循环 `get_item_history`。
- `funds[].metric_overrides`：可选。只有上游 builder 已用官方净值或服务端审计口径计算好指标时才可填写；完整净值历史优先。该字段用于 Hermes/服务端传递紧凑、可审计的指标快照，不能由 LLM 猜测。`get_batch_fund_profiles.periodRanks` 只能填 R20/R60/R120/R250 作降级展示，不能填 BIAS20/MA/回撤，且不能支撑最终可执行新增。
- `funds[].history_complete/coverage_start/coverage_end`：逐基金覆盖状态；覆盖不足时在输出里标注。
- `funds[].flow_3d`：可选证据。只有三天连续同口径基金级或方向级资金流时填写；否则用空数组，不得伪造。
- `eastmoney_checks`：东财数值和资讯交叉验证结果，只能支持、反证或标注未知，不得直接生成收益分。
- `news_factor`：消息面确认/否决因子。强利好只能确认已有价格信号，不能单独触发 ADD；重大反证可设置 `veto=true`。
- `sentiment_factor`：情绪面风险温度计，只来自东财 skill 或公开市场数据。risk_on 只能确认已有价格信号；crowded/risk_off 或极端异常可设置 `veto=true`。不得使用花花社区、喵舍、弹幕、用户持有人排行或社区关注。
- `realtime.estimate_change_pct`：`get_item_estimate` 或同口径实时估值涨跌幅；非实时、过期或无法确认时间时填 `null`。QDII 普通估值多用于解释官方/估算归属收益，不作为今天申赎的主要参考。
- `realtime.estimate_as_of/source/freshness`：估值时间、来源和新鲜度。`freshness != fresh` 时不能增强买入，只能作为数据风险。
- `realtime.estimate_nav_date`：估值/官方净值对应的 D 日，来自 `navDate/jzrq/FundNav.date` 或接口等价字段。只说明净值数据日，不等于收益归属日。
- `realtime.estimate_display_date`、`realtime.estimate_publish_date`、`realtime.estimate_official_attribution_date`：QDII/T+N 的 G 日证据，优先来自 `displayDate`、`lastNavPublishDate`、`estimateVsActual.publish_date` 或服务端统一归属结果。缺少可靠 G 日时填 `null`，报告不得自行回退到 D 日。
- `realtime.estimate_data_date_label`：用户提示用数据标签，例如“反映上一海外交易日行情”；只用于解释，不用于收益归属计算。
- `realtime.estimate_vs_actual`：若后端返回官方公布日配对，原样传入。`publish_date` 是 QDII/T+N 配对锚点，不要由 Agent 自己用自然日拼。
- `realtime.intraday_flow`：东财或 HuahuaDaily 可核验的方向/板块资金流；口径不一致时填 `null`，不得伪造成基金级资金流。
- `realtime.qdii_night_status`：QDII 的 `get_night_estimate.status`。
- `realtime.qdii_night_estimated_change_pct`：QDII 的 `get_night_estimate.estimatedChangePercent`；这是今天 QDII 加减仓时点最重要的实时参考。没有该字段时视为不可执行新增。
- `realtime.qdii_night_quote_as_of` 与 `realtime.qdii_night_actual_session_date`：QDII 夜盘数据时间和对应交易夜盘日期，用于判断是否过期。
- `realtime.qdii_night_freshness`：夜盘新鲜度。`stale/expired` 时禁止可执行新增；缺失时视为未知并降低数据质量。
- `realtime.qdii_night_coverage_pct`：夜盘持仓穿透覆盖权重。覆盖率低或服务端返回 `weakCoverage=true` 时降低执行分；严重缺失时新增金额为 0。
- `realtime.qdii_night_availability/reason`：夜盘可用性和阻断原因，如 `partial/fx_missing/low_coverage/quote_rate_limited/calendar_unknown`。报告应翻译为中文数据缺口。
- `realtime.qdii_night_fx`：夜盘汇率折算信息。人民币份额 QDII 必须考虑 USD/CNY、HKD/CNY 等汇率变动；美元份额与人民币份额可能涨跌不同。
- `realtime.qdii_night_holdings`：`get_night_estimate.breakdown.holdings` 的简化明细，至少包含 `code/name/market/weight/raw_change/fx_change/combined_change/contribution/missing_reason`。它用于解释夜盘估算来源和覆盖率，不得把单个重仓股涨跌当成基金真实收益。
- `serenity_checks`：Serenity 证据链和风险否决结果；可与顶层 `risk_veto/evidence_strength` 同步。
- `catalyst_status/evidence_strength/risk_veto`：东财资讯与 Serenity 审视后的规范值。
- `fees`：历史兼容字段名，来源为 `get_batch_fund_fees` 或 `get_fund_fees`。当前策略只使用其中的申购状态、限购额度、最低金额和确认天数；费率只作背景，不进入核心信号、回测收益或调仓金额。
- `night_status`：兼容旧输入；新输入优先使用 `realtime.qdii_night_status`。非 QDII 用 `null`。
- `opportunity_pool.directions`：板块迁移方向池，来自东财数值/资讯、Huahua 当前暴露和 Serenity 证据。方向必须有历史序列；估值、资金流、拥挤度未知时填 `null` 并在报告说明。
- `opportunity_pool.fund_candidates`：兼容旧引擎字段，默认传空数组。当前策略不做自然语言全市场选基，不输出系统生成的候选基金池。
- 用户点名基金代码时，不放入“系统候选基金池”；应作为单独的“用户点名基金比较”输出，并明确标注不是系统筛选结果。
- 方向机会池结论由 `scripts/signal_rules.py` 输出 `PRIORITY_RESEARCH/WATCH/AVOID`，面向用户必须翻译为“优先研究方向/候选跟踪/暂不纳入”。

## Hermes 构造 `execution` 的强制流程

`execution` 必须在运行 `scripts/signal_rules.py` 前写入输入 JSON。不要让 LLM 在报告阶段临时补；报告阶段只能展示引擎结果。

推荐伪代码：

```python
now = datetime.now(ZoneInfo("Asia/Shanghai"))
status = huahua.get_status()
next_day = huahua.get_next_trading_day(date=now.date().isoformat())

payload["execution"] = {
    "run_at": now.isoformat(),
    "market_timezone": "Asia/Shanghai",
    "trade_cutoff_time": "15:00",
    "is_trading_day": bool(status.get("isTradingDay") or status.get("is_trading_day")),
    "next_trading_day": next_day.get("date") or next_day.get("next_trading_day"),
    "source": "get_status/get_next_trading_day"
}
```

如果使用 `calculate_trading_dates`：

```python
dates = huahua.calculate_trading_dates(start_date=now.date().isoformat(), count=2)
payload["execution"]["next_trading_day"] = dates["nextTradingDay"] 或 dates["next_trading_day"]
payload["execution"]["source"] = "get_status/calculate_trading_dates"
```

字段归属：

| 字段 | 必填 | 来源 | 说明 |
|---|---:|---|---|
| `run_at` | 是 | Hermes 当前北京时间 | 报告实际运行时间，不能用云同步/行情/净值时间替代 |
| `market_timezone` | 是 | 固定值 | `"Asia/Shanghai"` |
| `trade_cutoff_time` | 是 | 固定值 | 场外基金常规截止线 `"15:00"` |
| `is_trading_day` | 是 | `get_status` 或交易日接口 | 无法确认时保守视为不可执行 |
| `next_trading_day` | 强烈建议 | `get_next_trading_day` / `calculate_trading_dates` | 三点后或非交易日展示“哪天再确认” |
| `source` | 是 | 构造器填写 | 用于审计数据来源 |

硬性规则：

- `run_at >= 15:00`：同日申赎窗口已关闭，所有交易金额为 0。
- `is_trading_day=false`：所有交易金额为 0。
- `next_trading_day` 缺失时，报告只能写“下一交易日再确认”，不能写具体执行日。
- `execution` 缺失时，引擎会用本机北京时间兜底，但最终交付给用户或保存快照的正式报告必须显式包含 `execution`。

## 禁止

- 禁止把排名字段、模型生成分数或旧新闻伪装成净值收益率。
- 禁止只用 `periodRanks` 生成最终可执行报告；缺少完整净值或审计指标时，新增执行金额必须为 0。
- 禁止从交易账本在 Agent 内重建组合单位净值、最大回撤或回测收益。
- 禁止在 Agent 内用当前持仓权重和单只基金历史构造组合回撤代理。
- 禁止把组合净值涨幅写成交易收益、定投收益或账户收益率；它只表示服务端组合单位净值表现，不涉及本次买卖、加减仓或未来定投扣款。
- 禁止在未传入 `portfolio.dca_plans` 且没有 `funds[].autoInvestConfig` 时猜测用户定投计划。
- 禁止在传给 `save_quant_snapshot` 的内容里包含建议金额、建议份额、虚拟现金或虚拟收益。
- 禁止把自然语言开放式查数结果包装成全市场基金推荐。
- 禁止绕过方向池直接推荐单只基金；用户点名基金只能做比较，不得写成系统推荐。
