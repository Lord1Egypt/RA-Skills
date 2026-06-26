import {
  buildBubble,
  buildChartPoint,
  buildDateRangeLabel,
  buildDivider,
  buildPolylinePoints,
  buildStageLabel,
  buildStars,
  escapeXml,
  extent,
  formatDateLabel,
  inferProjectionValue
} from "../research_shared/svg_utils.mjs";

function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function conceptNamesFromDetail(detail) {
  const list = detail?.concepts;
  if (!Array.isArray(list) || !list.length) {
    return null;
  }
  const names = list.map((item) => item?.name).filter(Boolean);
  return names.length ? names.join(" / ") : null;
}

function formatSearchEvidenceChainLabel(searchEvidence) {
  if (!searchEvidence) {
    return "独立搜索证据链待补";
  }
  if (searchEvidence.status === "completed") {
    const hasAny =
      Array.isArray(searchEvidence.searches) &&
      searchEvidence.searches.some((bucket) => Array.isArray(bucket?.results) && bucket.results.length > 0);
    return hasAny ? "独立搜索证据链已补" : "独立搜索证据链待补";
  }
  return "独立搜索证据链待补";
}

function formatMoneyFlowDirectionLabel(moneyFlow) {
  if (!moneyFlow) {
    return null;
  }
  const { direction } = moneyFlow;
  if (direction === "inflow") {
    return "主力净流入";
  }
  if (direction === "outflow") {
    return "主力净流出";
  }
  if (direction === "neutral") {
    return "资金流中性";
  }
  return null;
}

function formatIndustryRankPanelLine(industryRank) {
  if (!industryRank) {
    return null;
  }
  const industry =
    industryRank.industry ||
    industryRank.industry_name ||
    null;
  const rank = industryRank.rank ?? industryRank.rank_in_industry ?? null;
  const summary =
    typeof industryRank.summary === "string"
      ? industryRank.summary.trim()
      : typeof industryRank.peer_summary === "string"
        ? industryRank.peer_summary.trim()
        : "";

  const head = [industry, rank != null && rank !== "" ? `排名${rank}` : null].filter(Boolean).join(" · ");
  let line = head;
  if (summary) {
    line = head ? `${head} · ${summary}` : summary;
  }
  if (!line) {
    return null;
  }
  return line.length > 42 ? `${line.slice(0, 39)}…` : line;
}

function formatAnalystConsensusPanelLine(analyst) {
  if (!analyst) {
    return null;
  }
  const coverage = analyst.coverage ?? analyst.analyst_count;
  const covPart =
    coverage != null && Number.isFinite(Number(coverage))
      ? `覆盖${Number(coverage)}家 · `
      : "";
  const summary = typeof analyst.summary === "string" ? analyst.summary.trim() : "";
  if (!summary && !covPart) {
    return null;
  }
  const body = summary || "一致预期已返回";
  const full = `${covPart}${body}`;
  return full.length > 48 ? `${full.slice(0, 45)}…` : full;
}

function stageTitles(barStats) {
  if (barStats.trend === "up") {
    return ["阶段1: 筑底期", "阶段2: 上升期", "阶段3: 加速期", "阶段4: 推演区"];
  }

  if (barStats.trend === "down") {
    return ["阶段1: 反弹期", "阶段2: 调整期", "阶段3: 防守期", "阶段4: 推演区"];
  }

  return ["阶段1: 筑底期", "阶段2: 震荡期", "阶段3: 观察期", "阶段4: 推演区"];
}

function buildStockStages(bars, trend, xStart, xEnd) {
  const safeBars = Array.isArray(bars) && bars.length ? bars : [{ d: "20260101" }, { d: "20260331" }];
  const total = safeBars.length;
  const splitA = safeBars[Math.max(0, Math.floor(total / 3) - 1)]?.d ?? safeBars[0].d;
  const splitB = safeBars[Math.max(0, Math.floor((total * 2) / 3) - 1)]?.d ?? safeBars.at(-1).d;
  const last = safeBars.at(-1).d;
  const first = safeBars[0].d;
  const titles = stageTitles({ trend });
  const dividers = [
    xStart + (xEnd - xStart) * 0.33,
    xStart + (xEnd - xStart) * 0.66,
    xEnd
  ];

  return {
    labels: [
      `${titles[0]} (${buildDateRangeLabel(first, splitA)})`,
      `${titles[1]} (${buildDateRangeLabel(splitA, splitB)})`,
      `${titles[2]} (${buildDateRangeLabel(splitB, last)})`,
      `${titles[3]} (${buildDateRangeLabel(last, null)})`
    ],
    dividers
  };
}

function buildBubbles(runtimeData, rating) {
  const { normalized, search_evidence: searchEvidence } = runtimeData;
  const valuation = normalized.valuation_signal;
  const priceSummary = normalized.price_summary;
  const barStats = normalized.bar_stats;
  const financial = normalized.financial_signal;
  const forecast = normalized.forecast?.forecast_summary || "未返回明确业绩预告";
  const conceptNames =
    conceptNamesFromDetail(normalized.instrument_concepts_detail) ||
    (Array.isArray(normalized.concept_names) && normalized.concept_names.length
      ? normalized.concept_names.join(" / ")
      : null) ||
    "概念标签待补";
  const industryBubbleLine =
    normalized.industry_rank_signal?.industry ||
    normalized.industry_rank_signal?.industry_name ||
    normalized.sector_name ||
    "行业待补";
  const searchChainLine = formatSearchEvidenceChainLabel(searchEvidence);
  const moneyFlowLabel = formatMoneyFlowDirectionLabel(normalized.money_flow_signal);

  return [
    buildBubble({
      x: 40,
      y: 80,
      width: 150,
      height: 42,
      title: "📊 财务质量",
      lines: [financial.summary.slice(0, 18), financial.latest?.pq != null ? `扣非净利: ${toNumber(financial.latest.pq)?.toFixed(1)}` : "公共API无财报序列"],
      stroke: "#60a5fa"
    }),
    buildBubble({
      x: 210,
      y: 80,
      width: 150,
      height: 42,
      title: "💰 估值快照",
      lines: [`PE ${valuation.pe_ttm ?? "N/A"}x`, `PB ${valuation.pb ?? "N/A"}x`],
      stroke: "#f59e0b"
    }),
    buildBubble({
      x: 380,
      y: 80,
      width: 160,
      height: 42,
      title: "📈 价格结构",
      lines: [`区间涨跌 ${priceSummary?.period_change_pct ?? "N/A"}%`, `趋势 ${barStats.trend}`],
      stroke: "#22c55e"
    }),
    buildBubble({
      x: 560,
      y: 80,
      width: 160,
      height: 42,
      title: "🏦 行业归属",
      lines: [industryBubbleLine.slice(0, 18), conceptNames.slice(0, 18)],
      stroke: "#a78bfa"
    }),
    buildBubble({
      x: 740,
      y: 80,
      width: 170,
      height: 42,
      title: "🛡️ 核心逻辑",
      lines: [normalized.main_business || "主营待补", `${rating.icon} ${rating.label}`],
      stroke: "#22d3ee"
    }),
    buildBubble({
      x: 40,
      y: 420,
      width: 180,
      height: 42,
      title: "📰 催化事件",
      lines: [forecast.slice(0, 20), "后续仍需搜索校验"],
      stroke: "#f97316"
    }),
    buildBubble({
      x: 240,
      y: 420,
      width: 180,
      height: 42,
      title: "⚠️ 风险提示",
      lines: [searchChainLine.slice(0, 20), moneyFlowLabel ? moneyFlowLabel.slice(0, 18) : "资金流/同业估值待补"],
      stroke: "#ef4444"
    }),
    buildBubble({
      x: 440,
      y: 420,
      width: 200,
      height: 42,
      title: "🔑 当前站位",
      lines: [`支撑 ${barStats.support ?? "N/A"} / 阻力 ${barStats.resistance ?? "N/A"}`, `置信度 ${rating.confidence.label}`],
      stroke: "#fbbf24"
    })
  ].join("\n");
}

export function renderStockResearchSvg(runtimeData, rating) {
  const width = 960;
  const height = 580;
  const xStart = 70;
  const xEnd = 820;
  const yTop = 120;
  const yBottom = 360;
  const bars = runtimeData.normalized.bar_stats.bars;
  const closes = bars.map((item) => toNumber(item.c)).filter((item) => item !== null);
  const barRange = extent(closes);
  const priceLine = buildPolylinePoints(closes, {
    xStart,
    xEnd,
    yTop,
    yBottom
  });
  const weeklyReference = runtimeData.normalized.financial_rows.map((item) => toNumber(item.nq)).filter((item) => item !== null);
  const secondaryLine = buildPolylinePoints(weeklyReference.length ? weeklyReference : closes, {
    xStart,
    xEnd,
    yTop: yTop + 25,
    yBottom: yBottom - 15
  });
  const lastClose = closes.at(-1) ?? 0;
  const projectedValue = inferProjectionValue(lastClose, runtimeData.normalized.bar_stats.trend);
  const projectionLine = buildPolylinePoints([lastClose, projectedValue], {
    xStart: xEnd,
    xEnd: 900,
    yTop,
    yBottom
  });
  const highestBar = [...bars].sort((left, right) => (toNumber(right.h) ?? -Infinity) - (toNumber(left.h) ?? -Infinity))[0];
  const lowestBar = [...bars].sort((left, right) => (toNumber(left.l) ?? Infinity) - (toNumber(right.l) ?? Infinity))[0];
  const nowPoint = buildChartPoint(lastClose, closes.length - 1, closes.length, {
    xStart,
    xEnd,
    yTop,
    yBottom,
    range: barRange
  });
  const highPoint = buildChartPoint(highestBar?.h, bars.findIndex((item) => item.d === highestBar?.d), closes.length, {
    xStart,
    xEnd,
    yTop,
    yBottom,
    range: barRange
  });
  const lowPoint = buildChartPoint(lowestBar?.l, bars.findIndex((item) => item.d === lowestBar?.d), closes.length, {
    xStart,
    xEnd,
    yTop,
    yBottom,
    range: barRange
  });
  const stages = buildStockStages(bars, runtimeData.normalized.bar_stats.trend, xStart, xEnd);
  const stageLabels = stages.labels
    .map((label, index) => buildStageLabel({
      x: [140, 340, 560, 860][index],
      y: 74,
      title: label,
      isFuture: index === 3
    }))
    .join("\n");
  const stageDividers = stages.dividers
    .map((divider, index) => buildDivider({
      x: divider,
      y1: 86,
      y2: 392,
      future: index === 2
    }))
    .join("\n");
  const valuationBandHeight = (yBottom - yTop) / 3;
  const bubbles = buildBubbles(runtimeData, rating);
  const instrument = runtimeData.instrument;
  const valuationLevel = runtimeData.normalized.valuation_signal.level === "cheap"
    ? "低估"
    : runtimeData.normalized.valuation_signal.level === "rich"
      ? "偏高"
      : "合理";

  const industryRankPanelLine = formatIndustryRankPanelLine(runtimeData.normalized.industry_rank_signal);
  const analystConsensusPanelLine = formatAnalystConsensusPanelLine(runtimeData.normalized.analyst_consensus_signal);
  const ratingPanelExtras = [industryRankPanelLine, analystConsensusPanelLine].filter(Boolean);
  const ratingBoxHeight = 60 + ratingPanelExtras.length * 12;
  let ratingPanelY = 556;
  const ratingPanelTexts = ratingPanelExtras
    .map((line, index) => {
      const fill = index === 0 ? "#a5b4fc" : "#94a3b8";
      const el = `    <text x="835" y="${ratingPanelY}" font-size="8" fill="${fill}" text-anchor="middle">${escapeXml(line)}</text>`;
      ratingPanelY += 12;
      return el;
    })
    .join("\n");
  const moneyFlowLiquidity = formatMoneyFlowDirectionLabel(runtimeData.normalized.money_flow_signal);
  const liquidityFoot = moneyFlowLiquidity ?? "独立资金流待补";

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="stockBackground" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c1220"/>
      <stop offset="100%" stop-color="#1a2340"/>
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#stockBackground)"/>
  ${buildStars({ width, height, count: 5 })}
  <g id="title-block">
    <text x="40" y="36" fill="#e2e8f0" font-size="20" font-weight="700">${escapeXml(instrument.instrument_name)}(${escapeXml(instrument.instrument_id)}) 个股深度分析</text>
    <text x="40" y="58" fill="#94a3b8" font-size="12">模型: Stock Research Preview | 综合评级: ${escapeXml(rating.icon)} ${escapeXml(rating.label)} | ${escapeXml(formatDateLabel(runtimeData.request.target_date))}</text>
  </g>
  <g id="stage-labels">${stageLabels}${stageDividers}</g>
  <g id="valuation-zones">
    <rect x="${xStart}" y="${yTop}" width="${nowPoint.x - xStart}" height="${valuationBandHeight}" fill="rgba(239,68,68,0.08)"/>
    <text x="${xStart + 6}" y="${yTop + 12}" fill="#ef4444" font-size="8" opacity="0.75">高估区域</text>
    <rect x="${xStart}" y="${yTop + valuationBandHeight}" width="${nowPoint.x - xStart}" height="${valuationBandHeight}" fill="rgba(34,197,94,0.06)"/>
    <line x1="${xStart}" y1="${yTop + valuationBandHeight}" x2="${nowPoint.x}" y2="${yTop + valuationBandHeight}" stroke="#22c55e" stroke-width="1" stroke-dasharray="4,4" opacity="0.55"/>
    <line x1="${xStart}" y1="${yTop + valuationBandHeight * 2}" x2="${nowPoint.x}" y2="${yTop + valuationBandHeight * 2}" stroke="#22c55e" stroke-width="1" stroke-dasharray="4,4" opacity="0.55"/>
    <text x="${xStart + 6}" y="${yTop + valuationBandHeight + 12}" fill="#22c55e" font-size="8" opacity="0.75">合理估值区间</text>
    <rect x="${xStart}" y="${yTop + valuationBandHeight * 2}" width="${nowPoint.x - xStart}" height="${valuationBandHeight}" fill="rgba(59,130,246,0.08)"/>
    <text x="${xStart + 6}" y="${yTop + valuationBandHeight * 2 + 12}" fill="#3b82f6" font-size="8" opacity="0.75">低估区域</text>
  </g>
  <g id="price-lines">
    <polyline class="main-price-line" points="${priceLine}" fill="none" stroke="#38bdf8" stroke-width="3"/>
    <polyline class="secondary-line" points="${secondaryLine}" fill="none" stroke="#9ca3af" stroke-width="1.6" stroke-dasharray="6,4" opacity="0.55"/>
    <polyline class="projection-line" points="${projectionLine}" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-dasharray="7,6" opacity="0.85"/>
  </g>
  <g id="extremes">
    <circle cx="${highPoint.x}" cy="${highPoint.y}" r="6" fill="#ef4444" stroke="#ffffff" stroke-width="2"/>
    <text x="${highPoint.x}" y="${highPoint.y - 12}" font-size="8" fill="#fecaca" text-anchor="middle">🔺 ¥${toNumber(highestBar?.h)?.toFixed(2) ?? "N/A"} ${escapeXml(formatDateLabel(highestBar?.d))}</text>
    <circle cx="${lowPoint.x}" cy="${lowPoint.y}" r="6" fill="#22c55e" stroke="#ffffff" stroke-width="2"/>
    <text x="${lowPoint.x}" y="${lowPoint.y + 18}" font-size="8" fill="#bbf7d0" text-anchor="middle">🔻 ¥${toNumber(lowestBar?.l)?.toFixed(2) ?? "N/A"} ${escapeXml(formatDateLabel(lowestBar?.d))}</text>
  </g>
  <g id="now-marker">
    <line x1="${nowPoint.x}" y1="92" x2="${nowPoint.x}" y2="392" stroke="#a78bfa" stroke-width="2" stroke-dasharray="7,6"/>
    <text x="${nowPoint.x + 10}" y="106" fill="#c4b5fd" font-size="11" font-weight="700">📍 NOW ${escapeXml(formatDateLabel(runtimeData.request.target_date))}</text>
    <circle cx="${nowPoint.x}" cy="${nowPoint.y}" r="9" fill="#22c55e" stroke="#ffffff" stroke-width="3"/>
    <text x="${nowPoint.x}" y="${nowPoint.y - 15}" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="700">¥${lastClose.toFixed(2)}</text>
  </g>
  <g id="data-bubbles">${bubbles}</g>
  <g id="rating-box">
    <rect x="740" y="490" width="190" height="${ratingBoxHeight}" rx="10" fill="rgba(15,23,42,0.9)" stroke="#38bdf8"/>
    <text x="835" y="510" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="700">${escapeXml(rating.icon)} ${escapeXml(rating.label)}</text>
    <text x="835" y="528" font-size="9" fill="#94a3b8" text-anchor="middle">核心逻辑: 价格与盈利暂无明显背离 | 置信度: ${escapeXml(rating.confidence.label)}</text>
    <text x="835" y="543" font-size="8" fill="#cbd5e1" text-anchor="middle">估值: ${escapeXml(valuationLevel)} | 趋势: ${escapeXml(runtimeData.normalized.bar_stats.trend)}</text>
${ratingPanelTexts ? `${ratingPanelTexts}\n` : ""}  </g>
  <text x="40" y="568" fill="#cbd5e1" font-size="10">市场: A股${escapeXml(runtimeData.normalized.sector_name || runtimeData.instrument.instrument_name || "")} | 核心指标: PE ${runtimeData.normalized.valuation_signal.pe_ttm ?? "N/A"}x | 流动性: ${escapeXml(liquidityFoot)} | 催化剂: 财报/预告 | 方向: ${escapeXml(rating.label)}</text>
</svg>`;
}
