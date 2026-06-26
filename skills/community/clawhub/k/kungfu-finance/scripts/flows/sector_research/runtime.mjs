import https from "https";
import { URL } from "url";
import {
  fetchQuote,
  fetchMoneyFlow,
  fetchSectorConstituents,
  fetchConceptSectors,
} from "../research_shared/public_api.mjs";
import { runResearchSearch } from "../research_shared/search_runtime.mjs";

export const DEFAULT_SECTOR_RESEARCH_WINDOW = 780;

const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36";
const REFERER = "https://quote.eastmoney.com";
const TIMEOUT_KLINE_MS = 15000;

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

function ymd(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}${m}${day}`;
}

function num(v) {
  if (v === null || v === undefined || v === "" || v === "-") return null;
  const n = typeof v === "number" ? v : parseFloat(String(v).replace(/,/g, ""));
  return Number.isFinite(n) ? n : null;
}

function parseJsonLoose(text) {
  const t = String(text).trim();
  try {
    return JSON.parse(t);
  } catch {
    const i = t.indexOf("{");
    const j = t.lastIndexOf("}");
    if (i >= 0 && j > i) {
      try {
        return JSON.parse(t.slice(i, j + 1));
      } catch {
        return null;
      }
    }
    return null;
  }
}

function httpGet(urlString, timeoutMs) {
  return new Promise((resolve, reject) => {
    const u = new URL(urlString);
    const opts = {
      hostname: u.hostname,
      path: u.pathname + u.search,
      method: "GET",
      headers: {
        "User-Agent": UA,
        Referer: REFERER,
      },
    };
    const req = https.request(opts, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (ch) => {
        body += ch;
      });
      res.on("end", () => resolve(body));
    });
    req.on("error", reject);
    req.setTimeout(timeoutMs, () => {
      req.destroy();
      reject(new Error("timeout"));
    });
    req.end();
  });
}

function parseEastKlineBar(line) {
  const p = String(line).split(",");
  if (p.length < 6) return null;
  return {
    d: p[0],
    o: num(p[1]),
    c: num(p[2]),
    h: num(p[3]),
    l: num(p[4]),
    v: num(p[5]),
    amount: p[6] !== undefined ? num(p[6]) : null,
    amplitude: p[7] !== undefined ? num(p[7]) : null,
    change_pct: p[8] !== undefined ? num(p[8]) : null,
    change: p[9] !== undefined ? num(p[9]) : null,
    turnover: p[10] !== undefined ? num(p[10]) : null,
  };
}

/** EastMoney 板块指数 secid：90.BKxxxx */
function sectorIndexSecid(bkCode) {
  const raw = String(bkCode).trim().toUpperCase();
  const full = raw.startsWith("BK") ? raw : `BK${raw.replace(/^BK/i, "")}`;
  return `90.${full}`;
}

async function fetchSectorIndexKline(bkCode, { klt = 101, days = 520 } = {}) {
  const endD = ymd(new Date());
  const ed = new Date();
  const bd = new Date(ed);
  bd.setDate(bd.getDate() - Math.max(1, Math.floor(Number(days) || 520)));
  const begD = ymd(bd);
  const secid = sectorIndexSecid(bkCode);
  const fields1 = "f1,f2,f3,f4,f5,f6";
  const fields2 = "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61";
  const url =
    `https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=${encodeURIComponent(secid)}` +
    `&fields1=${fields1}&fields2=${fields2}&klt=${encodeURIComponent(String(klt))}&fqt=1` +
    `&beg=${encodeURIComponent(begD)}&end=${encodeURIComponent(endD)}`;
  const text = await httpGet(url, TIMEOUT_KLINE_MS);
  const j = parseJsonLoose(text);
  const lines = j && j.data && Array.isArray(j.data.klines) ? j.data.klines : null;
  if (!lines || lines.length === 0) return null;
  const bars = [];
  for (const line of lines) {
    const b = parseEastKlineBar(line);
    if (b) bars.push(b);
  }
  return bars.length ? { bars, secid, source: "eastmoney" } : null;
}

function normalizeBkCode(id) {
  const s = String(id).trim().toUpperCase();
  if (!s) return "";
  if (s.startsWith("BK")) return s;
  return `BK${s}`;
}

function inferExchangeId(code) {
  const c = String(code).trim();
  if (c.startsWith("6")) return "SH";
  return "SZ";
}

function normalizeSectorKey(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "");
}

function normalizeSectorAliasKey(value) {
  return normalizeSectorKey(value).replace(/(概念股|概念|板块|赛道|行业|产业|指数|题材)$/gu, "");
}

function conceptRowToCandidate(row) {
  return {
    sector_id: row.code || "",
    sector_name: row.name || "",
    sector_type: "concept",
    change_pct: row.change_pct ?? null,
    similarity: null,
    resolver_source: "eastmoney/concept-sectors",
  };
}

function scoreConceptMatch(query, candidate) {
  const rawQuery = String(query || "").trim();
  const normalizedQuery = normalizeSectorKey(rawQuery);
  const aliasQuery = normalizeSectorAliasKey(rawQuery);
  const normalizedName = normalizeSectorKey(candidate.sector_name);
  const aliasName = normalizeSectorAliasKey(candidate.sector_name);

  let score = 10;
  if (normalizedName === normalizedQuery) {
    score += 120;
  } else if (aliasName === aliasQuery && aliasQuery) {
    score += 110;
  } else if (normalizedName.startsWith(normalizedQuery) && normalizedQuery) {
    score += 70;
  } else if (normalizedName.includes(normalizedQuery) && normalizedQuery) {
    score += 55;
  }
  score -= Math.max(aliasName.length - aliasQuery.length, 0);
  return score;
}

function rankConceptCandidates(query, candidates) {
  return candidates
    .map((candidate) => ({
      ...candidate,
      match_score: scoreConceptMatch(query, candidate),
    }))
    .sort((left, right) => right.match_score - left.match_score);
}

function createSectorNeedsInputError(detail) {
  const error = new Error(detail.prompt || "需要补充板块信息");
  error.code = "SECTOR_NEEDS_INPUT";
  error.detail = detail;
  return error;
}

function buildCandidatePrompt(sectorName, candidates) {
  const candidateLine = candidates
    .slice(0, 5)
    .map((item) => `${item.sector_name}${item.sector_id ? `（${item.sector_id}）` : ""}`)
    .join("、");

  return `“${sectorName}”可能对应多个板块，请从这些候选中确认一个（可提供板块代码如 BKxxxx）：${candidateLine}。`;
}

function pickResolvedSector(sectorName, matches) {
  if (!matches.length) {
    return null;
  }

  const normalizedQuery = normalizeSectorKey(sectorName);
  const aliasQuery = normalizeSectorAliasKey(sectorName);
  const exactMatch = matches.find((item) => normalizeSectorKey(item.sector_name) === normalizedQuery);
  if (exactMatch) {
    return exactMatch;
  }

  const aliasMatch = matches.find((item) => normalizeSectorAliasKey(item.sector_name) === aliasQuery);
  if (aliasMatch) {
    return aliasMatch;
  }

  const [first, second] = matches;
  if (matches.length === 1 && (first?.match_score ?? 0) >= 50) {
    return first;
  }

  if (
    (first?.match_score ?? 0) >= 100 &&
    (second?.match_score ?? Number.NEGATIVE_INFINITY) <= first.match_score - 10
  ) {
    return first;
  }

  return null;
}

async function resolveSectorFromConceptList(sectorName) {
  const list = await fetchConceptSectors({ limit: 200 });
  if (!list?.sectors?.length) {
    return {
      resolved: null,
      candidates: [],
      source_route: "eastmoney/concept-sectors",
    };
  }

  const candidates = rankConceptCandidates(
    sectorName,
    list.sectors.map(conceptRowToCandidate).filter((c) => c.sector_id && c.sector_name),
  );

  return {
    resolved: pickResolvedSector(sectorName, candidates),
    candidates,
    source_route: "eastmoney/concept-sectors",
  };
}

function buildBarStats(barWindow) {
  const bars = Array.isArray(barWindow?.data) ? barWindow.data : [];
  const closes = bars.map((item) => toNumber(item.c)).filter((item) => item !== null);
  const highs = bars.map((item) => toNumber(item.h)).filter((item) => item !== null);
  const lows = bars.map((item) => toNumber(item.l)).filter((item) => item !== null);
  const recentBars = sliceRecent(bars, Math.min(10, bars.length));
  const recentHighs = recentBars.map((item) => toNumber(item.h)).filter((item) => item !== null);
  const recentLows = recentBars.map((item) => toNumber(item.l)).filter((item) => item !== null);
  const latestClose = closes.at(-1) ?? null;
  const firstClose = closes[0] ?? null;
  const shortAverage = average(sliceRecent(closes, Math.min(5, closes.length)));
  const mediumAverage = average(sliceRecent(closes, Math.min(10, closes.length)));
  const periodChangePct =
    latestClose !== null && firstClose !== null && firstClose !== 0
      ? Number((((latestClose - firstClose) / firstClose) * 100).toFixed(2))
      : null;

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
    latest_change_pct: toNumber(barWindow?.latest_date_data?.p),
    latest_trading_day: barWindow?.latest_date_data?.d ?? barWindow?.end_date ?? null,
    short_average: shortAverage,
    medium_average: mediumAverage,
    support: recentLows.length ? Math.min(...recentLows) : null,
    resistance: recentHighs.length ? Math.max(...recentHighs) : null,
    period_low: lows.length ? Math.min(...lows) : null,
    period_high: highs.length ? Math.max(...highs) : null,
    trend,
    period_change_pct: periodChangePct,
  };
}

function normalizeConstituentFromEast(row) {
  const code = String(row.code || "").trim();
  return {
    instrument_id: code,
    exchange_id: inferExchangeId(code),
    instrument_name: row.name != null ? String(row.name) : "",
    change_pct: toNumber(row.change_pct),
    latest_price: toNumber(row.price),
  };
}

function buildBreadthFromRows(rows) {
  const sortedByStrength = [...rows].sort((left, right) => {
    return (right.change_pct ?? Number.NEGATIVE_INFINITY) - (left.change_pct ?? Number.NEGATIVE_INFINITY);
  });

  const leaders = sortedByStrength.slice(0, 5);
  const laggards = [...sortedByStrength].reverse().slice(0, 5);
  const positive = rows.filter((item) => (item.change_pct ?? 0) > 0);
  const negative = rows.filter((item) => (item.change_pct ?? 0) < 0);
  const neutral = rows.filter((item) => (item.change_pct ?? 0) === 0);
  const averageChangePct = average(rows.map((item) => item.change_pct).filter((item) => item !== null));
  const positiveRatio = rows.length ? positive.length / rows.length : 0;

  return {
    rows,
    leaders,
    laggards,
    total_count: rows.length,
    positive_count: positive.length,
    negative_count: negative.length,
    neutral_count: neutral.length,
    up: positive.length,
    down: negative.length,
    flat: neutral.length,
    average_change_pct: averageChangePct,
    positive_ratio: Number(positiveRatio.toFixed(2)),
  };
}

function buildStageSignal(barStats, breadth) {
  if (barStats.trend === "up" && breadth.positive_ratio >= 0.67) {
    return {
      label: "近期扩散偏强",
      summary: "近期窗口内，指数结构与成分股扩散同步偏强，短线观察偏顺风。",
    };
  }

  if (barStats.trend === "up") {
    return {
      label: "近期上行但分化",
      summary: "近期窗口内，指数仍在上行，但上涨主要由少数强势成分股维持。",
    };
  }

  if (barStats.trend === "sideways") {
    return {
      label: "近期震荡整理",
      summary: "近期窗口内，指数进入震荡区，板块更像等待新催化剂的整理结构。",
    };
  }

  return {
    label: "近期回撤偏弱",
    summary: "近期窗口内，指数和成分股广度都偏弱，短期更接近回撤整理。",
  };
}

function formatSectorTypeLabelFromName(sectorName) {
  const n = String(sectorName || "");
  if (/概念|题材|赛道/u.test(n)) return "概念";
  if (/行业|申万/u.test(n)) return "行业";
  return "概念";
}

function financeFromQuote(q) {
  if (!q) return null;
  const pe = q.pe;
  const pb = q.pb;
  const mc = q.market_cap;
  if (pe == null && pb == null && mc == null) return null;
  return {
    end_date: null,
    pe_ttm: pe,
    pb,
    ps: null,
    forecast_summary: null,
    forecast_type: null,
    latest_profit_q: null,
    market_cap: mc,
    circulating_cap: q.circulating_cap ?? null,
  };
}

function priceFromQuote(q) {
  if (!q) return null;
  return {
    latest_price: toNumber(q.latest_price),
    latest_change_pct: toNumber(q.change_pct),
    period_change_pct: null,
    latest_trading_day: null,
  };
}

function normalizeLeaderMoneyFlowFromPublic(mf) {
  if (!mf || !Array.isArray(mf.flows) || mf.flows.length === 0) return null;
  return {
    summary: { latest: mf.flows[mf.flows.length - 1], source: mf.source || "eastmoney" },
    recent_count: mf.flows.length,
  };
}

function buildSimilarSectorsFromConceptList(allSectors, currentId, currentName, limit = 8) {
  if (!Array.isArray(allSectors)) return [];
  const seen = new Set();
  const out = [];
  const curKey = normalizeSectorKey(currentName);

  for (const row of allSectors) {
    const code = row.code != null ? String(row.code) : "";
    const name = row.name != null ? String(row.name) : "";
    if (!code || code === String(currentId)) continue;
    if (normalizeSectorKey(name) === curKey) continue;
    const key = `${code}::${normalizeSectorKey(name)}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({
      sector_id: code,
      sector_name: name,
      similarity: toNumber(row.change_pct),
      sector_type: "concept",
      resolver_source: "eastmoney/concept-sectors",
    });
    if (out.length >= limit) break;
  }

  return out;
}

function buildSectorSearchQueries({ sector, request }) {
  const sectorName = sector.sector_name || sector.sector_code || sector.sector_id;
  const year =
    String(request.target_date || "").slice(0, 4) || String(new Date().getFullYear());

  return [
    {
      search_id: "macro_context",
      topic: "macro",
      query: `${sectorName} 宏观 政策 行业景气 ${year}`,
    },
    {
      search_id: "catalyst_context",
      topic: "catalyst",
      query: `${sectorName} 催化剂 产业新闻 政策 ${year}`,
    },
    {
      search_id: "risk_context",
      topic: "risk",
      query: `${sectorName} 监管 风险 负面 ${year}`,
    },
    {
      search_id: "industry_trend_context",
      topic: "industry",
      query: `${sectorName} 行业规模 CAGR 渗透率 市场前景`,
    },
    {
      search_id: "competition_context",
      topic: "competition",
      query: `${sectorName} 龙头企业 市场份额 竞争格局`,
    },
    {
      search_id: "policy_context",
      topic: "policy",
      query: `${sectorName} 政策 补贴 法规 ${year}`,
    },
    {
      search_id: "money_flow_context",
      topic: "flow",
      query: `${sectorName} 资金流向 机构持仓 ETF 龙虎榜`,
    },
  ];
}

function createUpstreamPayloadError(message, route) {
  const error = new Error(message);
  error.code = "SECTOR_UPSTREAM_INVALID";
  error.route = route;
  return error;
}

function standardInvalidationConditions() {
  return [
    {
      type: "结构失效",
      trigger: "板块指数跌破近端支撑且成分股正收益占比继续下降",
      verify: "复查东方财富板块K线与板块成分股列表",
    },
    {
      type: "情绪失效",
      trigger: "龙头股仍强但板块平均涨幅转负，扩散被证伪",
      verify: "对比龙头涨幅与全板块广度",
    },
    {
      type: "叙事失效",
      trigger: "后续搜索验证不到产业/政策催化",
      verify: "独立搜索与新闻交叉验证",
    },
  ];
}

export async function fetchSectorResearchRuntime(request) {
  const todayStr =
    request.target_date && String(request.target_date).length >= 8
      ? String(request.target_date).slice(0, 8)
      : ymd(new Date());

  let conceptBoardListMemo;
  const loadConceptBoardListOnce = async () => {
    if (conceptBoardListMemo !== undefined) {
      return conceptBoardListMemo;
    }
    conceptBoardListMemo = await fetchConceptSectors({ limit: 200 }).catch(() => null);
    return conceptBoardListMemo;
  };

  let sectorResolution = null;
  let sectorCode = null;
  let sectorName = null;

  if (request.sector_id) {
    sectorCode = normalizeBkCode(request.sector_id);
    sectorName = request.sector_name || sectorCode;
    if (!request.sector_name) {
      const list = await loadConceptBoardListOnce();
      const hit = list?.sectors?.find((row) => normalizeBkCode(row.code) === sectorCode);
      if (hit?.name) {
        sectorName = hit.name;
      }
    }
  } else if (request.sector_name) {
    sectorResolution = await resolveSectorFromConceptList(request.sector_name);
    if (!sectorResolution.resolved) {
      if (sectorResolution.candidates.length) {
        throw createSectorNeedsInputError({
          prompt: buildCandidatePrompt(request.sector_name, sectorResolution.candidates),
          reason: "ambiguous_sector_name",
          missing: ["sector"],
          attempted: { sector_name: request.sector_name },
          candidates: sectorResolution.candidates,
        });
      }

      throw createSectorNeedsInputError({
        prompt: `未能识别板块“${request.sector_name}”，请提供更准确的板块名称或直接提供东方财富板块代码（如 BK0732）。`,
        reason: "unresolved_sector_name",
        missing: ["sector"],
        attempted: { sector_name: request.sector_name },
      });
    }

    sectorCode = normalizeBkCode(sectorResolution.resolved.sector_id);
    sectorName = sectorResolution.resolved.sector_name || sectorCode;
  } else {
    throw createSectorNeedsInputError({
      prompt: "请提供 sector_name 或 sector_id（板块代码，如 BK0732）。",
      reason: "missing_sector",
      missing: ["sector"],
      attempted: {},
    });
  }

  const constituentsEnvelope = await fetchSectorConstituents(sectorCode, { limit: 500 });
  if (!constituentsEnvelope?.stocks?.length) {
    throw createUpstreamPayloadError("板块成分股数据无效或为空", "eastmoney/sector-constituents");
  }

  const rawStocks = constituentsEnvelope.stocks;
  const constituentRows = rawStocks.map(normalizeConstituentFromEast);
  const breadth = buildBreadthFromRows(constituentRows);

  const klinePack = await fetchSectorIndexKline(sectorCode, { days: request.visual_days_len || 520 }).catch(
    () => null,
  );

  let sectorPerformance;
  if (klinePack?.bars?.length) {
    const bars = klinePack.bars;
    const last = bars[bars.length - 1];
    sectorPerformance = {
      sector_id: sectorCode,
      sector_name: sectorName,
      sector_type: "concept",
      success: true,
      data: bars,
      latest_date_data: {
        d: last?.d ?? null,
        p: toNumber(last?.change_pct),
      },
      end_date: last?.d ?? null,
      source: "eastmoney",
    };
  } else {
    sectorPerformance = {
      sector_id: sectorCode,
      sector_name: sectorName,
      sector_type: "concept",
      success: false,
      data: [],
      latest_date_data: null,
      end_date: null,
      source: "eastmoney",
    };
  }

  const barStats = buildBarStats(sectorPerformance);
  const stageSignal = buildStageSignal(barStats, breadth);

  const leaderInstruments = breadth.leaders.slice(0, 5);
  const leaderBackendRows = await Promise.all(
    leaderInstruments.map(async (instrument) => {
      const code = instrument.instrument_id;
      const [quote, moneyFlow] = await Promise.all([
        fetchQuote(code).catch(() => null),
        fetchMoneyFlow(code, { days: 20 }).catch(() => null),
      ]);
      return { instrument, quote, money_flow: moneyFlow };
    }),
  );

  const leaderFundamentals = leaderBackendRows.map((row) => {
    const q = row.quote;
    return {
      instrument_id: row.instrument.instrument_id,
      exchange_id: row.instrument.exchange_id,
      instrument_name: q?.name || row.instrument.instrument_name,
      finance: financeFromQuote(q),
      price: priceFromQuote(q),
      money_flow: normalizeLeaderMoneyFlowFromPublic(row.money_flow),
      quote: q
        ? {
            latest_price: q.latest_price,
            pe: q.pe,
            pb: q.pb,
            market_cap: q.market_cap,
            change_pct: q.change_pct,
          }
        : null,
    };
  });

  const conceptListForSimilar = await loadConceptBoardListOnce();
  const similarSectors = buildSimilarSectorsFromConceptList(
    conceptListForSimilar?.sectors,
    sectorCode,
    sectorName,
    8,
  );

  const sector = {
    sector_id: sectorCode,
    sector_name: sectorName,
    sector_code: sectorCode,
    sector_type: "concept",
  };

  const invalidation_conditions = standardInvalidationConditions();

  const normalized = {
    sector_type_label: formatSectorTypeLabelFromName(sectorName),
    constituents: constituentRows,
    leaders: breadth.leaders,
    laggards: breadth.laggards,
    breadth,
    bar_stats: barStats,
    stage_signal: stageSignal,
    similar_sectors: similarSectors,
    leader_fundamentals: leaderFundamentals,
    sector_money_flow: null,
    invalidation_conditions,
  };

  const searchEvidence = await runResearchSearch({
    flow: "sector-research",
    target_date: request.target_date,
    subject: {
      type: "sector",
      sector_id: sectorCode,
      sector_name: sectorName,
      sector_type: "concept",
    },
    queries: buildSectorSearchQueries({ sector, request }),
  });

  const sectorConstituents = {
    sector_id: sectorCode,
    sector_name: sectorName,
    data: constituentRows,
    latest_date: barStats.latest_trading_day || todayStr,
    total: constituentsEnvelope.total ?? constituentRows.length,
    source: "eastmoney",
  };

  const sources = [
    { route: "eastmoney/concept-sectors", source: "东方财富概念板块列表", as_of: todayStr },
    { route: "eastmoney/sector-constituents", source: "东方财富板块成分股", as_of: todayStr },
    { route: "eastmoney/sector-kline", source: "东方财富板块K线", as_of: todayStr },
    ...leaderInstruments.map((item) => ({
      route: "eastmoney/quote+moneyflow",
      source: `东方财富行情与资金流（${item.instrument_id}）`,
      as_of: todayStr,
    })),
  ];

  return {
    sector,
    request,
    sector_performance: sectorPerformance,
    sector_constituents: sectorConstituents,
    sector_resolution: sectorResolution,
    similar_sectors_raw: conceptListForSimilar,
    leader_backend_rows: leaderBackendRows,
    search_evidence: searchEvidence,
    normalized,
    sources,
  };
}
