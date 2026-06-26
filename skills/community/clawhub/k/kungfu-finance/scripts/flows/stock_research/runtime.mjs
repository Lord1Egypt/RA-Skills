import {
  fetchQuote,
  fetchKline,
  fetchMoneyFlow,
  resolveSecid
} from "../research_shared/public_api.mjs";
import { runResearchSearch } from "../research_shared/search_runtime.mjs";

export const DEFAULT_STOCK_RESEARCH_WINDOW = 520;

function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function average(values) {
  if (!values.length) {
    return null;
  }

  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function sliceRecent(values, size) {
  if (!Array.isArray(values) || size <= 0) {
    return [];
  }
  return values.slice(Math.max(values.length - size, 0));
}

function formatTodayYmd() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}${m}${day}`;
}

function inferExchangeId(instrumentId) {
  const c = String(instrumentId ?? "").trim();
  if (c.startsWith("6") || c.startsWith("68")) {
    return "SSE";
  }
  return "SZE";
}

function buildBarStats(barWindow) {
  const bars = Array.isArray(barWindow?.data) ? barWindow.data : [];
  const closes = bars.map((item) => toNumber(item.c)).filter((item) => item !== null);
  const lows = bars.map((item) => toNumber(item.l)).filter((item) => item !== null);
  const highs = bars.map((item) => toNumber(item.h)).filter((item) => item !== null);
  const recentBars = sliceRecent(bars, Math.min(20, bars.length));
  const recentLows = recentBars.map((item) => toNumber(item.l)).filter((item) => item !== null);
  const recentHighs = recentBars.map((item) => toNumber(item.h)).filter((item) => item !== null);
  const shortAverage = average(sliceRecent(closes, Math.min(5, closes.length)));
  const mediumAverage = average(sliceRecent(closes, Math.min(10, closes.length)));
  const latestClose = closes.at(-1) ?? null;

  let trend = "sideways";
  if (latestClose !== null && shortAverage !== null && mediumAverage !== null) {
    if (latestClose >= shortAverage && shortAverage >= mediumAverage) {
      trend = "up";
    } else if (latestClose <= shortAverage && shortAverage <= mediumAverage) {
      trend = "down";
    }
  }

  return {
    bars,
    latest_close: latestClose,
    short_average: shortAverage,
    medium_average: mediumAverage,
    support: recentLows.length ? Math.min(...recentLows) : null,
    resistance: recentHighs.length ? Math.max(...recentHighs) : null,
    period_low: lows.length ? Math.min(...lows) : null,
    period_high: highs.length ? Math.max(...highs) : null,
    trend
  };
}

function mapWeeklyBarsFromKline(klineResult) {
  const bars = Array.isArray(klineResult?.bars) ? klineResult.bars : [];
  return bars.map((bar) => {
    const open = toNumber(bar.o);
    const close = toNumber(bar.c);
    const change_pct =
      open && close ? Number((((close - open) / open) * 100).toFixed(2)) : toNumber(bar.change_pct);
    const d = bar.d != null ? String(bar.d) : "";
    return {
      week_start: d,
      start_date: d,
      end_date: d,
      open,
      close,
      high: toNumber(bar.h),
      low: toNumber(bar.l),
      volume: toNumber(bar.v) ?? 0,
      change_pct
    };
  });
}

function buildFinancialSignal(financeRows) {
  const rows = Array.isArray(financeRows) ? financeRows : [];
  const latest = rows.at(-1) ?? null;
  const previous = rows.length >= 2 ? rows.at(-2) : null;

  if (!latest) {
    return {
      direction: "unknown",
      latest,
      previous,
      summary: "缺少可用财务时间序列"
    };
  }

  if (!previous) {
    return {
      direction: "limited",
      latest,
      previous,
      summary: "财务时间序列不足两期，仅能读取最新报告期快照"
    };
  }

  const latestNq = toNumber(latest.nq);
  const previousNq = toNumber(previous.nq);
  const latestPq = toNumber(latest.pq);
  const previousPq = toNumber(previous.pq);

  let direction = "flat";
  if ((latestNq ?? 0) > (previousNq ?? 0) && (latestPq ?? 0) >= (previousPq ?? 0)) {
    direction = "improving";
  } else if ((latestNq ?? 0) < (previousNq ?? 0) && (latestPq ?? 0) <= (previousPq ?? 0)) {
    direction = "weakening";
  }

  const summary =
    direction === "improving"
      ? "最新两个报告期的净利润与扣非利润同步改善"
      : direction === "weakening"
        ? "最新两个报告期的净利润与扣非利润同步走弱"
        : "最新两个报告期的利润表现分化，趋势不够一致";

  return {
    direction,
    latest,
    previous,
    summary
  };
}

function buildForecastSignal(forecast) {
  const summary = forecast?.forecast_summary || "";
  const positiveKeywords = ["预增", "增长", "改善", "向上", "扭亏"];
  const negativeKeywords = ["预减", "下滑", "亏损", "承压", "恶化"];

  const isPositive = positiveKeywords.some((keyword) => summary.includes(keyword));
  const isNegative = negativeKeywords.some((keyword) => summary.includes(keyword));

  return {
    tone: isPositive ? "positive" : isNegative ? "negative" : "neutral",
    summary: summary || "未看到明确业绩预告摘要"
  };
}

function buildValuationSignal(valuation) {
  const pe = toNumber(valuation?.pe_ttm);
  const pb = toNumber(valuation?.pb);

  let level = "unknown";
  if (pe !== null || pb !== null) {
    if ((pe !== null && pe >= 30) || (pb !== null && pb >= 5)) {
      level = "rich";
    } else if ((pe !== null && pe <= 15) || (pb !== null && pb <= 2)) {
      level = "cheap";
    } else {
      level = "neutral";
    }
  }

  return {
    level,
    pe_ttm: pe,
    pb,
    ps: toNumber(valuation?.ps),
    market_cap: toNumber(valuation?.market_cap),
    circulating_market_cap: toNumber(valuation?.circulating_market_cap)
  };
}

function buildMoneyFlowSignalFromPublic(moneyFlowResult) {
  if (!moneyFlowResult || !Array.isArray(moneyFlowResult.flows) || moneyFlowResult.flows.length === 0) {
    return {
      main_force_net_amount: null,
      direction: "neutral",
      recent_main_net: [],
      record_count: 0
    };
  }

  const flows = moneyFlowResult.flows;
  const recentMainNet = flows.map((f) => ({
    d: f.d != null ? String(f.d) : null,
    main_net: toNumber(f.main_net)
  }));

  let sum = 0;
  for (const f of flows) {
    const n = toNumber(f.main_net);
    if (n !== null) {
      sum += n;
    }
  }

  let direction = "neutral";
  if (sum > 0) {
    direction = "inflow";
  } else if (sum < 0) {
    direction = "outflow";
  }

  return {
    main_force_net_amount: sum,
    direction,
    recent_main_net: sliceRecent(recentMainNet, 5),
    record_count: flows.length
  };
}

function buildStockSearchQueries({ instrument, normalized, request }) {
  const instrumentName = instrument.instrument_name || instrument.instrument_id;
  const sectorName = normalized.sector_name || "A股行业";
  const year =
    String(request.target_date || "").slice(0, 4) || String(new Date().getFullYear());

  return [
    {
      search_id: "macro_context",
      topic: "macro",
      query: `${instrumentName} ${sectorName} 宏观 政策 行业景气 ${year}`
    },
    {
      search_id: "catalyst_context",
      topic: "catalyst",
      query: `${instrumentName} 催化剂 产业新闻 政策 财报 ${year}`
    },
    {
      search_id: "risk_context",
      topic: "risk",
      query: `${instrumentName} 监管 风险 负面 新闻 ${year}`
    },
    {
      search_id: "competition_context",
      topic: "competition",
      query: `${instrumentName} 竞争优势 市场份额 竞品`
    },
    {
      search_id: "financials_context",
      topic: "financials",
      query: `${instrumentName} 财报 营收 净利润 毛利率 ROE ${year}`
    },
    {
      search_id: "company_profile_context",
      topic: "company_profile",
      query: `${instrumentName} 主营业务 商业模式 护城河 管理层`
    },
    {
      search_id: "governance_context",
      topic: "governance",
      query: `${instrumentName} 管理层 治理 质押 内部交易`
    },
    {
      search_id: "sector_trend_context",
      topic: "sector_trend",
      query: `${sectorName} 行业趋势 景气 政策 ${year}`
    }
  ];
}

export async function fetchStockResearchRuntime(request) {
  const code = String(request.instrument_id ?? "").trim();
  const exchange_id = request.exchange_id || inferExchangeId(code);
  const instrument_name =
    request.instrument_name != null ? request.instrument_name : null;

  resolveSecid(code);

  const visualDays = Math.max(
    1,
    Math.floor(Number(request.visual_days_len) || DEFAULT_STOCK_RESEARCH_WINDOW)
  );

  const [quote, dailyKline, weeklyKline, moneyFlowResult] = await Promise.all([
    fetchQuote(code).catch(() => null),
    fetchKline(code, { klt: 101, days: visualDays }).catch(() => null),
    fetchKline(code, { klt: 102, days: 520 }).catch(() => null),
    fetchMoneyFlow(code, { days: 20 }).catch(() => null)
  ]);

  const dailyBars = Array.isArray(dailyKline?.bars) ? dailyKline.bars : [];
  const barSeriesForStats = { data: dailyBars };
  const barStats = buildBarStats(barSeriesForStats);
  const weeklyBars = mapWeeklyBarsFromKline(weeklyKline);

  const todayStr = formatTodayYmd();
  const quoteName = quote?.name && String(quote.name).trim() ? quote.name : instrument_name;
  const resolvedInstrumentName = quoteName || code;

  const instrument = {
    instrument_id: code,
    exchange_id,
    instrument_name: resolvedInstrumentName
  };

  const valuation = {
    pe_ttm: quote?.pe ?? null,
    pb: quote?.pb ?? null,
    ps: null,
    market_cap: quote?.market_cap ?? null,
    circulating_market_cap: quote?.circulating_cap ?? null
  };

  const price_summary = {
    latest_price: quote?.latest_price ?? null,
    period_change_pct: quote?.change_pct ?? null,
    latest_trading_day: todayStr
  };

  const financial_rows = [];
  const financial_signal = {
    direction: "unknown",
    latest: null,
    previous: null,
    summary: "本版使用公共API，财务时间序列通过搜索补充"
  };

  const forecast_signal = {
    tone: "neutral",
    summary: "公共API无业绩预告数据，通过搜索补充"
  };

  const valuation_signal = buildValuationSignal(valuation);
  const money_flow_signal = buildMoneyFlowSignalFromPublic(moneyFlowResult);

  const barStart = dailyBars.length ? String(dailyBars[0].d) : null;
  const barEnd = dailyBars.length ? String(dailyBars[dailyBars.length - 1].d) : null;

  const normalized = {
    sector_name: null,
    concept_names: [],
    main_business: null,
    forecast: null,
    financial_rows,
    valuation,
    dividend: [],
    price_summary,
    price_levels: null,
    level_summary: null,
    bar_stats: barStats,
    weekly_bars: weeklyBars,
    financial_signal,
    forecast_signal,
    valuation_signal,
    money_flow_signal,
    instrument_concepts_detail: null,
    holder_signal: null,
    industry_rank_signal: null,
    valuation_detail_signal: null,
    analyst_consensus_signal: null
  };

  const searchEvidence = await runResearchSearch({
    flow: "stock-research",
    target_date: request.target_date,
    subject: {
      type: "stock",
      instrument_id: instrument.instrument_id,
      exchange_id: instrument.exchange_id,
      instrument_name: instrument.instrument_name
    },
    queries: buildStockSearchQueries({
      instrument,
      normalized,
      request
    })
  });

  const sources = [
    { route: "eastmoney/quote", source: "东方财富实时报价", as_of: todayStr },
    {
      route: "eastmoney/kline",
      source: "东方财富日K线",
      as_of: todayStr,
      start_date: barStart,
      end_date: barEnd
    },
    { route: "eastmoney/weekly", source: "东方财富周K线", as_of: todayStr },
    ...(moneyFlowResult
      ? [{ route: "eastmoney/fflow", source: "东方财富资金流向", as_of: todayStr }]
      : [])
  ];

  return {
    instrument: {
      instrument_id: instrument.instrument_id,
      exchange_id: instrument.exchange_id,
      instrument_name: request.instrument_name ?? instrument.instrument_name ?? null
    },
    request: {
      target_date: request.target_date,
      visual_days_len: request.visual_days_len
    },
    finance_context: null,
    finance_basic_indicators: null,
    price_snapshot: price_summary,
    bar_series: {
      data: dailyBars,
      start_date: barStart,
      end_date: barEnd,
      source: dailyKline?.source ?? null
    },
    weekly_kline: weeklyKline,
    price_levels: null,
    level_summary: null,
    holder_context: null,
    instrument_concepts: null,
    money_flow: moneyFlowResult,
    finance_industry_rank: null,
    finance_valuation_detail: null,
    finance_profit_forecast: null,
    quote,
    search_evidence: searchEvidence,
    normalized,
    sources
  };
}
