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

function getLeaderFundamentalsRows(normalized) {
  return Array.isArray(normalized?.leader_fundamentals) ? normalized.leader_fundamentals : [];
}

function countLeadersWithFinance(normalized) {
  return getLeaderFundamentalsRows(normalized).filter((row) => row?.finance).length;
}

function countLeadersWithMoneyFlow(normalized) {
  return getLeaderFundamentalsRows(normalized).filter((row) => row?.money_flow != null).length;
}

function clipBubbleText(text, maxLen = 36) {
  if (text == null || text === "") {
    return text;
  }

  if (text.length <= maxLen) {
    return text;
  }

  return `${text.slice(0, Math.max(0, maxLen - 1))}…`;
}

function formatLeaderFundamentalsLine(row) {
  if (!row?.instrument_name) {
    return null;
  }

  const parts = [String(row.instrument_name).trim()].filter(Boolean);
  const latestPrice = toNumber(row.price?.latest_price);
  if (latestPrice !== null) {
    parts.push(latestPrice.toFixed(2));
  }

  const chg = toNumber(row.price?.latest_change_pct);
  if (chg !== null) {
    parts.push(`${chg >= 0 ? "+" : ""}${chg.toFixed(2)}%`);
  }

  return parts.join(" ");
}

function formatBreadthLeaderLine(item) {
  if (!item) {
    return null;
  }

  return `${item.instrument_name} ${item.change_pct ?? "N/A"}%`;
}

function buildSimilarSectorsSpreadLine(normalized) {
  const similar = Array.isArray(normalized?.similar_sectors) ? normalized.similar_sectors : [];
  const names = similar.map((item) => item?.sector_name).filter(Boolean);
  if (!names.length) {
    return null;
  }

  return names.slice(0, 2).join(" · ");
}

function buildMoneyFlowValidationLine(normalized) {
  const hasSectorFlow = Boolean(normalized?.sector_money_flow);
  const financeCount = countLeadersWithFinance(normalized);
  const leaderFlowCount = countLeadersWithMoneyFlow(normalized);

  if (hasSectorFlow && financeCount > 0 && leaderFlowCount > 0) {
    return `板块资金流已接；${leaderFlowCount}只龙头资金流；财务${financeCount}只`;
  }

  if (hasSectorFlow && financeCount > 0) {
    return "板块资金流与龙头财务已接";
  }

  if (hasSectorFlow && leaderFlowCount > 0) {
    return `板块与${leaderFlowCount}只龙头资金流已接`;
  }

  if (hasSectorFlow) {
    return "板块级资金流字段已接";
  }

  if (leaderFlowCount > 0 && financeCount > 0) {
    return `${leaderFlowCount}只龙头资金流；财务${financeCount}只已接`;
  }

  if (leaderFlowCount > 0) {
    return `${leaderFlowCount}只龙头个股资金流已接`;
  }

  if (financeCount > 0) {
    return `龙头财务${financeCount}只已接；资金流待补`;
  }

  return "资金流与成分股财务横比仍待补";
}

function inferStageNames(label) {
  if (label === "近期扩散偏强") {
    return ["阶段1: 沉寂", "阶段2: 觉醒", "阶段3: 扩散", "阶段4: 推演区"];
  }

  if (label === "近期上行但分化") {
    return ["阶段1: 沉寂", "阶段2: 拉升", "阶段3: 分化", "阶段4: 推演区"];
  }

  if (label === "近期回撤偏弱") {
    return ["阶段1: 反弹", "阶段2: 震荡", "阶段3: 回撤", "阶段4: 推演区"];
  }

  return ["阶段1: 沉寂", "阶段2: 观察", "阶段3: 震荡", "阶段4: 推演区"];
}

function buildSectorStages(bars, stageLabel) {
  const safeBars = Array.isArray(bars) && bars.length ? bars : [{ d: "20260101" }, { d: "20260331" }];
  const total = safeBars.length;
  const splitA = safeBars[Math.max(0, Math.floor(total / 3) - 1)]?.d ?? safeBars[0].d;
  const splitB = safeBars[Math.max(0, Math.floor((total * 2) / 3) - 1)]?.d ?? safeBars.at(-1).d;
  const first = safeBars[0].d;
  const last = safeBars.at(-1).d;
  const titles = inferStageNames(stageLabel);

  return [
    `${titles[0]} (${buildDateRangeLabel(first, splitA)})`,
    `${titles[1]} (${buildDateRangeLabel(splitA, splitB)})`,
    `${titles[2]} (${buildDateRangeLabel(splitB, last)})`,
    `${titles[3]} (${buildDateRangeLabel(last, null)})`
  ];
}

function buildSectorBubbles(runtimeData, rating) {
  const normalized = runtimeData.normalized;
  const breadth = normalized.breadth;
  const leaderRows = getLeaderFundamentalsRows(normalized);
  const breadthLeaderLines = breadth.leaders.map((item) => formatBreadthLeaderLine(item)).filter(Boolean);
  const leaderLine1 =
    clipBubbleText(formatLeaderFundamentalsLine(leaderRows[0]) || breadthLeaderLines[0]) || "龙头数据待补";
  const similarSpread = buildSimilarSectorsSpreadLine(normalized);
  const leaderLine2 = clipBubbleText(similarSpread) || "扩散数据待补";
  const searchReady = runtimeData.search_evidence?.status === "completed";
  const moneyFlowLine = clipBubbleText(buildMoneyFlowValidationLine(normalized), 40);

  return [
    buildBubble({
      x: 38,
      y: 78,
      width: 170,
      height: 42,
      title: "📊 板块广度",
      lines: [`上涨家数 ${breadth.positive_count}/${breadth.total_count}`, `正收益占比 ${Math.round((breadth.positive_ratio ?? 0) * 100)}%`],
      stroke: "#60a5fa"
    }),
    buildBubble({
      x: 228,
      y: 78,
      width: 185,
      height: 42,
      title: "🚀 龙头表现",
      lines: [leaderLine1, leaderLine2],
      stroke: "#22c55e"
    }),
    buildBubble({
      x: 433,
      y: 78,
      width: 180,
      height: 42,
      title: "🧭 当前结构",
      lines: [normalized.stage_signal.label, `${rating.icon} ${rating.label}`],
      stroke: "#a78bfa"
    }),
    buildBubble({
      x: 633,
      y: 78,
      width: 220,
      height: 42,
      title: "⚠️ 校验状态",
      lines: [searchReady ? "宏观/催化剂搜索已补" : "宏观/催化剂搜索待补", moneyFlowLine],
      stroke: "#ef4444"
    })
  ].join("\n");
}

export function renderSectorResearchSvg(runtimeData, rating) {
  const width = 900;
  const height = 550;
  const xStart = 70;
  const xEnd = 760;
  const yTop = 110;
  const yBottom = 350;
  const bars = runtimeData.normalized.bar_stats.bars;
  const closes = bars.map((item) => toNumber(item.c)).filter((item) => item !== null);
  const volumes = bars.map((item) => toNumber(item.v)).filter((item) => item !== null);
  const mainLine = buildPolylinePoints(closes, {
    xStart,
    xEnd,
    yTop,
    yBottom
  });
  const secondaryLine = buildPolylinePoints(volumes.length ? volumes : closes, {
    xStart,
    xEnd,
    yTop: yTop + 30,
    yBottom: yBottom - 20
  });
  const range = extent(closes);
  const latestClose = closes.at(-1) ?? 0;
  const nowPoint = buildChartPoint(latestClose, closes.length - 1, closes.length, {
    xStart,
    xEnd,
    yTop,
    yBottom,
    range
  });
  const projectedValue = inferProjectionValue(latestClose, runtimeData.normalized.bar_stats.trend, {
    up: 0.06,
    flat: 0.01,
    down: -0.06
  });
  const projectionLine = buildPolylinePoints([latestClose, projectedValue], {
    xStart: xEnd,
    xEnd: 830,
    yTop,
    yBottom
  });
  const labels = buildSectorStages(bars, runtimeData.normalized.stage_signal.label);
  const bubbles = buildSectorBubbles(runtimeData, rating);
  const normalized = runtimeData.normalized;
  const financeLeaderCount = countLeadersWithFinance(normalized);
  const similarSectorCount = Array.isArray(normalized.similar_sectors) ? normalized.similar_sectors.length : 0;
  const evidenceInfoParts = [];
  if (financeLeaderCount > 0) {
    evidenceInfoParts.push(`龙头财务数据: ${financeLeaderCount}只`);
  }

  if (similarSectorCount > 0) {
    evidenceInfoParts.push(`相似赛道: ${similarSectorCount}个`);
  }

  const evidenceInfoSuffix = evidenceInfoParts.length ? ` | ${evidenceInfoParts.join(" | ")}` : "";

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="sectorBackground" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0a20"/>
      <stop offset="100%" stop-color="#1a1a40"/>
    </linearGradient>
    <linearGradient id="emotionGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22c55e"/>
      <stop offset="30%" stop-color="#84cc16"/>
      <stop offset="60%" stop-color="#eab308"/>
      <stop offset="80%" stop-color="#f97316"/>
      <stop offset="100%" stop-color="#ef4444"/>
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#sectorBackground)"/>
  ${buildStars({ width, height, count: 6 })}
  <g id="title-block">
    <text x="36" y="34" fill="#e2e8f0" font-size="20" font-weight="700">${escapeXml(runtimeData.sector.sector_name)} 板块情绪周期图</text>
    <text x="36" y="56" fill="#94a3b8" font-size="12">模型: Sector Research Preview | 方向: ${escapeXml(rating.icon)} ${escapeXml(rating.label)} | ${escapeXml(formatDateLabel(runtimeData.request.target_date))}</text>
  </g>
  <g id="stage-labels">
    ${labels.map((label, index) => buildStageLabel({
      x: [135, 315, 515, 760][index],
      y: 74,
      title: label,
      isFuture: index === 3
    })).join("\n")}
    ${[xStart + 220, xStart + 450, xEnd].map((x, index) => buildDivider({
      x,
      y1: 88,
      y2: 372,
      future: index === 2
    })).join("\n")}
  </g>
  <g id="price-lines">
    <polyline class="main-sector-line" points="${mainLine}" fill="none" stroke="#38bdf8" stroke-width="3"/>
    <polyline class="secondary-line" points="${secondaryLine}" fill="none" stroke="#9ca3af" stroke-width="1.6" stroke-dasharray="6,4" opacity="0.6"/>
    <polyline class="projection-line" points="${projectionLine}" fill="none" stroke="#fbbf24" stroke-width="2.2" stroke-dasharray="7,6" opacity="0.85"/>
  </g>
  <g id="now-marker">
    <line x1="${nowPoint.x}" y1="92" x2="${nowPoint.x}" y2="390" stroke="#a78bfa" stroke-width="2" stroke-dasharray="7,6"/>
    <text x="${nowPoint.x + 10}" y="106" fill="#c4b5fd" font-size="11" font-weight="700">📍 NOW ${escapeXml(formatDateLabel(runtimeData.request.target_date))}</text>
    <circle cx="${nowPoint.x}" cy="${nowPoint.y}" r="8" fill="#ffffff" stroke="#22c55e" stroke-width="3"/>
  </g>
  <g id="data-bubbles">${bubbles}</g>
  <g id="emotion-bar">
    <rect x="${xStart}" y="420" width="760" height="24" rx="5" fill="url(#emotionGradient)"/>
    <circle cx="${nowPoint.x}" cy="432" r="7" fill="#ffffff" stroke="#22c55e" stroke-width="3"/>
    <text x="120" y="436" font-size="9" fill="#ffffff" font-weight="700" text-anchor="middle">沉寂</text>
    <text x="295" y="436" font-size="9" fill="#ffffff" font-weight="700" text-anchor="middle">觉醒</text>
    <text x="485" y="436" font-size="9" fill="#ffffff" font-weight="700" text-anchor="middle">扩散</text>
    <text x="700" y="436" font-size="9" fill="#ffffff" font-weight="700" text-anchor="middle">推演</text>
  </g>
  <g id="direction-box">
    <rect x="662" y="470" width="200" height="56" rx="10" fill="rgba(15,23,42,0.9)" stroke="#38bdf8"/>
    <text x="762" y="490" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="700">${escapeXml(rating.icon)} ${escapeXml(rating.label)}</text>
    <text x="762" y="508" font-size="9" fill="#94a3b8" text-anchor="middle">结构: ${escapeXml(runtimeData.normalized.stage_signal.label)} | 置信度: ${escapeXml(rating.confidence.label)}</text>
    <text x="762" y="522" font-size="8" fill="#cbd5e1" text-anchor="middle">方向只给判断，不给仓位和交易指令</text>
  </g>
  <text x="36" y="540" fill="#cbd5e1" font-size="10">市场: A股板块指数 | 核心指标: 正收益占比 ${Math.round((runtimeData.normalized.breadth.positive_ratio ?? 0) * 100)}% | 流动性: 成交量副线 | 催化剂: ${runtimeData.search_evidence?.status === "completed" ? "已补搜索" : "待补搜索"} | 方向: ${escapeXml(rating.label)}${escapeXml(evidenceInfoSuffix)}</text>
</svg>`;
}
