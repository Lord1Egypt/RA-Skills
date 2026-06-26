import { readFileSync } from "node:fs";

const systemPromptPath = new URL("../../../references/prompts/movement-analysis/system.md", import.meta.url);
const moreRequirementsPath = new URL("../../../references/prompts/movement-analysis/more_requirements.md", import.meta.url);
const promptTemplatePath = new URL("../../../references/prompts/movement-analysis/user_template.md", import.meta.url);

function removeLeadingWhitespaces(text) {
  return String(text).replace(/^\s+/gm, "");
}

function serializePromptValue(value) {
  if (typeof value === "string") {
    return value;
  }
  return JSON.stringify(value, null, 2);
}

function formatPromptTemplate(template, values) {
  return template.replace(/\{([A-Z_]+)\}/g, (fullMatch, key) => {
    if (!(key in values)) {
      return fullMatch;
    }
    return values[key];
  });
}

function stringifyReport(report) {
  if (typeof report === "string") {
    return report;
  }

  try {
    return JSON.stringify(report, null, 2);
  } catch {
    return String(report);
  }
}

function formatHistoricalReports(historicalReports) {
  if (!historicalReports || historicalReports.length === 0) {
    return "";
  }

  return historicalReports.map(stringifyReport).join("\n");
}

function normalizeDfsData(originInput) {
  const items = [];

  for (const section of originInput ?? []) {
    const question = section?.question ?? "未命名数据块";
    const results = Array.isArray(section?.results) ? section.results : [];

    for (const result of results) {
      items.push({
        question: result?.derived_question ?? question,
        df: Array.isArray(result?.data) ? result.data : []
      });
    }
  }

  return items;
}

function formatOriginInput(dfsData, unusualMovements) {
  const unusualDates = new Set();

  for (const [key, value] of Object.entries(unusualMovements ?? {})) {
    if (/^\d{8}$/.test(String(key))) {
      unusualDates.add(String(key));
    }

    if (value && typeof value === "object" && !Array.isArray(value)) {
      for (const nestedKey of Object.keys(value)) {
        if (/^\d{8}$/.test(String(nestedKey))) {
          unusualDates.add(String(nestedKey));
        }
      }
    }
  }

  const originInputParts = [];

  for (const item of dfsData ?? []) {
    const question = item?.question ?? "未命名数据块";
    const rows = Array.isArray(item?.df) ? item.df : [];

    originInputParts.push(`## ${question}\n`);

    if (rows.length === 0) {
      originInputParts.push("无数据\n");
      continue;
    }

    const recentData = [];
    const seenDates = new Set();

    for (const row of rows.slice(0, 5)) {
      const date = row?.date ?? row?.trading_day;
      if (date && !seenDates.has(String(date))) {
        recentData.push(row);
        seenDates.add(String(date));
      }
    }

    for (const row of rows.slice(5)) {
      const date = row?.date ?? row?.trading_day;
      if (date && unusualDates.has(String(date)) && !seenDates.has(String(date))) {
        recentData.push(row);
        seenDates.add(String(date));
      }
    }

    if (recentData.length > 0) {
      originInputParts.push("数据（最近5天+异动日）:\n");
      for (const row of recentData) {
        const date = row?.date ?? row?.trading_day ?? "N/A";
        const simplifiedRow = Object.fromEntries(
          Object.entries(row ?? {}).filter(([key]) => key !== "date")
        );
        originInputParts.push(`${date}: ${JSON.stringify(simplifiedRow, null, 2)}\n`);
      }
    }

    originInputParts.push(`总行数: ${rows.length}\n\n`);
  }

  return originInputParts.join("");
}

function formatUnusualMovements(unusualMovements) {
  if (!unusualMovements || Object.keys(unusualMovements).length === 0) {
    return "";
  }

  return serializePromptValue(unusualMovements);
}

function formatRecentPrices(priceRowsOrList) {
  if (!Array.isArray(priceRowsOrList) || priceRowsOrList.length === 0) {
    return "暂无近期价格数据";
  }

  const isStringList = priceRowsOrList.every((item) => typeof item === "string");
  const recentRows = isStringList
    ? priceRowsOrList.slice(0, 30)
    : [...priceRowsOrList]
      .sort((left, right) => String(right.trading_day).localeCompare(String(left.trading_day)))
      .slice(0, 30)
      .map((row) => {
        const close = Number(row?.close);
        const closePrice = Number.isFinite(close) ? close.toFixed(2) : String(row?.close ?? "");
        return `${row?.trading_day ?? "N/A"}: ${closePrice}`;
      });

  const chunkedPrices = [];
  for (let index = 0; index < recentRows.length; index += 5) {
    chunkedPrices.push(recentRows.slice(index, index + 5));
  }
  return chunkedPrices.map((chunk) => chunk.join(", ")).join("\n");
}

function formatTradingDays(targetDate, tradingDaysList) {
  const validTradingDays = [...(tradingDaysList ?? [])]
    .map(String)
    .sort((left, right) => right.localeCompare(left))
    .slice(0, 180);

  const chunkedDays = [];
  for (let index = 0; index < validTradingDays.length; index += 10) {
    chunkedDays.push(validTradingDays.slice(index, index + 10));
  }

  return `目标日期: ${targetDate}\n最近180天有效交易日参考(请严格在此范围内选择日期):\n${chunkedDays.map((chunk) => chunk.join(", ")).join("\n")}`;
}

function formatPriceLevelSignals(priceLevels) {
  const signals = priceLevels?.data?.signals;
  if (!Array.isArray(signals) || signals.length === 0) {
    return "近期无显著筹码关键位";
  }

  return signals.slice(0, 5).map((signal) => {
    const type = signal?.line_type === "support" ? "支撑位" : "压力位";
    return `日期: ${signal?.d ?? "N/A"}, 价格: ${signal?.price ?? "N/A"}, 类型: ${type}`;
  }).join("\n");
}

function buildFallbackMarketTechnicalStatus(bundle, priceRows, tradingDaysList) {
  const levelSummary = bundle.level_summary ?? {};
  const latestDate = tradingDaysList.at(-1) ?? bundle.request?.target_date ?? "N/A";
  const latestPrice = levelSummary.latest_price ?? priceRows.at(-1)?.close ?? null;

  return [
    "【无图版技术摘要】",
    `目标日期: ${bundle.request?.target_date ?? "N/A"}`,
    `最新交易日: ${latestDate}`,
    `最新价: ${latestPrice ?? "N/A"}`,
    `20日区间: ${levelSummary.low_20d ?? "N/A"} - ${levelSummary.high_20d ?? "N/A"}`,
    `60日区间: ${levelSummary.low_60d ?? "N/A"} - ${levelSummary.high_60d ?? "N/A"}`,
    `100日区间: ${levelSummary.low_100d ?? "N/A"} - ${levelSummary.high_100d ?? "N/A"}`,
    `最近压力位: ${levelSummary.nearest_resistance_price ?? "N/A"} (${levelSummary.nearest_resistance_day ?? "N/A"})`,
    "【筹码关键位】",
    formatPriceLevelSignals(bundle.price_levels)
  ].join("\n");
}

export function loadMovementPromptAssets() {
  return {
    llm_system_lite: readFileSync(systemPromptPath, "utf8"),
    prompt_template: readFileSync(promptTemplatePath, "utf8"),
    more_requirements: readFileSync(moreRequirementsPath, "utf8")
  };
}

export function makeAnalyseResultWithDictPrompt({
  targetDate,
  originInput,
  unusualMovements,
  historicalReports = [],
  tradingDaysList = [],
  recentPrices = "",
  marketTechnicalStatus = "",
  extraRequirements = ""
}) {
  const { prompt_template: promptTemplate } = loadMovementPromptAssets();
  const dfsData = normalizeDfsData(originInput);
  const enhancedRequirements = [
    extraRequirements,
    "本次调用未提供K线图像，请严格基于 recent_prices、market_technical_status 与 origin_input 中的结构化信息完成分析，不要假设看到了图片。"
  ].filter(Boolean).join("\n");

  const prompt = formatPromptTemplate(promptTemplate, {
    ORIGIN_INPUT: formatOriginInput(dfsData, unusualMovements),
    UNUSUAL_MOVEMENTS: formatUnusualMovements(unusualMovements),
    EXTRA_REQUIREMENTS: enhancedRequirements,
    HISTORICAL_REPORTS: formatHistoricalReports(historicalReports),
    TODAY: targetDate,
    TRADING_DAYS: formatTradingDays(targetDate, tradingDaysList),
    RECENT_PRICES: recentPrices,
    MARKET_TECHNICAL_STATUS: marketTechnicalStatus
  });

  return removeLeadingWhitespaces(prompt);
}

export function buildMovementPromptPackage(bundle) {
  const assets = loadMovementPromptAssets();
  const priceRows = bundle.origin_input?.[0]?.results?.[0]?.data ?? [];
  const tradingDaysList = bundle.recent_trading_days_list ?? priceRows.map((row) => row.trading_day);
  const recentPrices = formatRecentPrices(bundle.recent_prices_list ?? priceRows);
  const marketTechnicalStatus = bundle.market_technical_status
    ? String(bundle.market_technical_status)
    : buildFallbackMarketTechnicalStatus(bundle, priceRows, tradingDaysList);

  return {
    system_prompt: assets.llm_system_lite,
    user_prompt: makeAnalyseResultWithDictPrompt({
      targetDate: bundle.request.target_date,
      originInput: bundle.origin_input,
      unusualMovements: bundle.unusual_movements,
      historicalReports: bundle.historical_reports ?? [],
      tradingDaysList,
      recentPrices,
      marketTechnicalStatus,
      extraRequirements: assets.more_requirements
    })
  };
}
