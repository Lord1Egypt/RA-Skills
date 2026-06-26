import { escapeXml, extent, formatDateLabel, scaleValue } from "../research_shared/svg_utils.mjs";

function toNumber(v) {
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function safeSlice(arr, maxLen) {
  return Array.isArray(arr) ? arr.slice(-maxLen) : [];
}

function scaleX(index, total, xStart, xEnd) {
  const denom = Math.max(total - 1, 1);
  return Number((xStart + ((xEnd - xStart) * index) / denom).toFixed(2));
}

function buildDarkBackground(w, h, gradientId) {
  return `<defs>
    <linearGradient id="${gradientId}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c1220"/><stop offset="100%" stop-color="#1a2340"/>
    </linearGradient>
  </defs>
  <rect width="${w}" height="${h}" fill="url(#${gradientId})"/>`;
}

function buildTitle(title, subtitle, { y = 36 } = {}) {
  return `<text x="40" y="${y}" fill="#e2e8f0" font-size="18" font-weight="700">${escapeXml(title)}</text>
  <text x="40" y="${y + 18}" fill="#94a3b8" font-size="11">${escapeXml(subtitle)}</text>`;
}

function buildGridLines(xStart, xEnd, yTop, yBottom, count = 4) {
  const lines = [];
  for (let i = 0; i <= count; i++) {
    const y = yTop + ((yBottom - yTop) * i) / count;
    lines.push(`<line x1="${xStart}" y1="${y}" x2="${xEnd}" y2="${y}" stroke="#334155" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.5"/>`);
  }
  return lines.join("\n");
}

function buildYAxisLabels(range, xStart, yTop, yBottom, count = 4, { format, align = "end" } = {}) {
  const labels = [];
  const x = align === "end" ? xStart - 6 : xStart + 4;
  const anchor = align === "end" ? "end" : "start";
  for (let i = 0; i <= count; i++) {
    const ratio = i / count;
    const val = range.max - ratio * (range.max - range.min);
    const y = yTop + ((yBottom - yTop) * i) / count;
    const text = format ? format(val) : val.toFixed(2);
    labels.push(`<text x="${x}" y="${y + 4}" fill="#64748b" font-size="8" text-anchor="${anchor}">${text}</text>`);
  }
  return labels.join("\n");
}

function buildDateAxis(dates, xStart, xEnd, y, maxLabels = 6) {
  if (!dates.length) return "";
  const step = Math.max(1, Math.floor(dates.length / maxLabels));
  const labels = [];
  for (let i = 0; i < dates.length; i += step) {
    const x = scaleX(i, dates.length, xStart, xEnd);
    labels.push(`<text x="${x}" y="${y}" fill="#64748b" font-size="7" text-anchor="middle">${escapeXml(formatDateLabel(dates[i]))}</text>`);
  }
  return labels.join("\n");
}

function buildPolyline(values, xStart, xEnd, yTop, yBottom, range, { stroke, strokeWidth = 2, dashArray, opacity = 1 } = {}) {
  const pts = values.map((v, i) => {
    const x = scaleX(i, values.length, xStart, xEnd);
    const y = scaleValue(v, range, { yTop, yBottom });
    return `${x},${y}`;
  }).join(" ");
  const dash = dashArray ? ` stroke-dasharray="${dashArray}"` : "";
  return `<polyline points="${pts}" fill="none" stroke="${stroke}" stroke-width="${strokeWidth}"${dash} opacity="${opacity}"/>`;
}

function buildRefLine(yVal, range, xStart, xEnd, yTop, yBottom, { stroke, label, dashArray = "4,4", labelX } = {}) {
  const y = scaleValue(yVal, range, { yTop, yBottom });
  const lx = labelX ?? xEnd + 4;
  return `<line x1="${xStart}" y1="${y}" x2="${xEnd}" y2="${y}" stroke="${stroke}" stroke-width="1" stroke-dasharray="${dashArray}" opacity="0.7"/>
  <text x="${lx}" y="${y + 3}" fill="${stroke}" font-size="7">${escapeXml(label ?? String(yVal))}</text>`;
}

// ============== K-LINE (CANDLESTICK) ==============

export function renderCandlestickSvg(barData, instrument, options = {}) {
  const { chipPeak, priceLevels, annotations } = options;
  const bars = safeSlice(barData?.data, 250);
  if (!bars.length) return buildEmptySvg("K线图", instrument, "无K线数据");

  const w = 960, h = 560;
  const xStart = 70, xEnd = chipPeak ? 720 : 880;
  const yTop = 80, yBottom = 340, volTop = 360, volBottom = 460;

  const dates = bars.map(b => b.d);
  const highs = bars.map(b => toNumber(b.h)).filter(v => v !== null);
  const lows = bars.map(b => toNumber(b.l)).filter(v => v !== null);
  const volumes = bars.map(b => toNumber(b.v)).filter(v => v !== null);
  const priceRange = extent([...highs, ...lows]);
  const volRange = extent(volumes);

  const candleWidth = Math.max(1, Math.min(6, (xEnd - xStart) / bars.length * 0.6));
  const candles = bars.map((b, i) => {
    const x = scaleX(i, bars.length, xStart, xEnd);
    const o = toNumber(b.o), c = toNumber(b.c), hi = toNumber(b.h), lo = toNumber(b.l);
    if (o === null || c === null) return "";
    const isUp = c >= o;
    const color = isUp ? "#ef4444" : "#22c55e";
    const bodyTop = scaleValue(Math.max(o, c), priceRange, { yTop, yBottom });
    const bodyBot = scaleValue(Math.min(o, c), priceRange, { yTop, yBottom });
    const wickTop = hi !== null ? scaleValue(hi, priceRange, { yTop, yBottom }) : bodyTop;
    const wickBot = lo !== null ? scaleValue(lo, priceRange, { yTop, yBottom }) : bodyBot;
    const bodyH = Math.max(1, bodyBot - bodyTop);
    return `<line x1="${x}" y1="${wickTop}" x2="${x}" y2="${wickBot}" stroke="${color}" stroke-width="0.8"/>
    <rect x="${x - candleWidth / 2}" y="${bodyTop}" width="${candleWidth}" height="${bodyH}" fill="${isUp ? color : "none"}" stroke="${color}" stroke-width="0.6"/>`;
  }).join("\n");

  const volBars = bars.map((b, i) => {
    const x = scaleX(i, bars.length, xStart, xEnd);
    const v = toNumber(b.v);
    if (v === null) return "";
    const o = toNumber(b.o), c = toNumber(b.c);
    const isUp = c !== null && o !== null ? c >= o : true;
    const barH = Math.max(1, ((v - volRange.min) / Math.max(volRange.max - volRange.min, 1)) * (volBottom - volTop));
    return `<rect x="${x - candleWidth / 2}" y="${volBottom - barH}" width="${candleWidth}" height="${barH}" fill="${isUp ? "rgba(239,68,68,0.5)" : "rgba(34,197,94,0.5)"}"/>`;
  }).join("\n");

  let chipSvg = "";
  if (chipPeak?.data?.final_chip) {
    chipSvg = renderChipPeakOverlay(chipPeak.data.final_chip, priceRange, yTop, yBottom, 730, 880);
  }

  let levelsSvg = "";
  if (priceLevels?.data?.signals) {
    levelsSvg = renderPriceLevelLines(priceLevels.data.signals, priceRange, xStart, xEnd, yTop, yBottom);
  }

  let annotationsSvg = "";
  if (Array.isArray(annotations) && annotations.length) {
    annotationsSvg = renderAnnotations(annotations, bars, priceRange, xStart, xEnd, yTop, yBottom);
  }

  const latestBar = bars.at(-1);
  const latestClose = toNumber(latestBar?.c);
  const latestChange = toNumber(latestBar?.p);
  const changeColor = latestChange >= 0 ? "#ef4444" : "#22c55e";
  const changeStr = latestChange !== null ? `${latestChange >= 0 ? "+" : ""}${latestChange.toFixed(2)}%` : "";

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "klineBg")}
  ${buildTitle(
    `${instrument.instrument_name}(${instrument.instrument_id}) K线图`,
    `${formatDateLabel(dates[0])} - ${formatDateLabel(dates.at(-1))} | 收盘: ¥${latestClose?.toFixed(2) ?? "N/A"} ${changeStr}`
  )}
  <g id="price-grid">${buildGridLines(xStart, xEnd, yTop, yBottom)}</g>
  <g id="price-axis">${buildYAxisLabels(priceRange, xStart, yTop, yBottom)}</g>
  <g id="candles">${candles}</g>
  <g id="volume-bars">${volBars}</g>
  <g id="vol-label"><text x="${xStart - 6}" y="${volTop + 10}" fill="#64748b" font-size="8" text-anchor="end">成交量</text></g>
  <g id="date-axis">${buildDateAxis(dates, xStart, xEnd, volBottom + 16)}</g>
  ${chipSvg ? `<g id="chip-peak">${chipSvg}</g>` : ""}
  ${levelsSvg ? `<g id="price-levels">${levelsSvg}</g>` : ""}
  ${annotationsSvg ? `<g id="annotations">${annotationsSvg}</g>` : ""}
  ${latestClose !== null ? `<g id="latest-marker">
    <circle cx="${scaleX(bars.length - 1, bars.length, xStart, xEnd)}" cy="${scaleValue(latestClose, priceRange, { yTop, yBottom })}" r="4" fill="${changeColor}" stroke="#fff" stroke-width="1.5"/>
    <text x="${scaleX(bars.length - 1, bars.length, xStart, xEnd) + 8}" y="${scaleValue(latestClose, priceRange, { yTop, yBottom }) + 3}" fill="${changeColor}" font-size="9" font-weight="700">¥${latestClose.toFixed(2)}</text>
  </g>` : ""}
  <text x="${w / 2}" y="${h - 10}" fill="#475569" font-size="8" text-anchor="middle">功夫量化 KungFu Finance | A股 K线图</text>
</svg>`;
}

function renderChipPeakOverlay(chips, priceRange, yTop, yBottom, xStart, xEnd) {
  if (!Array.isArray(chips) || !chips.length) return "";
  const maxChip = Math.max(...chips.map(c => toNumber(c.c ?? c.chip) ?? 0));
  if (maxChip <= 0) return "";

  const bars = chips.map(c => {
    const price = toNumber(c.p ?? c.price);
    const chip = toNumber(c.c ?? c.chip);
    if (price === null || chip === null) return "";
    const y = scaleValue(price, priceRange, { yTop, yBottom });
    const barW = (chip / maxChip) * (xEnd - xStart);
    const isProfit = price <= (priceRange.max + priceRange.min) / 2;
    return `<rect x="${xStart}" y="${y - 1}" width="${barW}" height="2" fill="${isProfit ? "rgba(250,204,21,0.6)" : "rgba(148,163,184,0.4)"}" rx="1"/>`;
  }).join("\n");

  return `<text x="${(xStart + xEnd) / 2}" y="${yTop - 6}" fill="#94a3b8" font-size="8" text-anchor="middle">筹码分布</text>\n${bars}`;
}

function renderPriceLevelLines(signals, priceRange, xStart, xEnd, yTop, yBottom) {
  if (!Array.isArray(signals) || !signals.length) return "";
  return signals.map(s => {
    const price = toNumber(s.price);
    if (price === null) return "";
    const y = scaleValue(price, priceRange, { yTop, yBottom });
    const lineType = s.line_type ?? "resistance";
    const color = lineType === "support" ? "#22c55e" : lineType === "concentration" ? "#5FB8E8" : "#7C3AED";
    const label = lineType === "support" ? "支撑" : lineType === "concentration" ? "集中" : "阻力";
    return `<line x1="${xStart}" y1="${y}" x2="${xEnd}" y2="${y}" stroke="${color}" stroke-width="1" stroke-dasharray="5,3" opacity="0.8"/>
    <text x="${xEnd + 4}" y="${y + 3}" fill="${color}" font-size="7">${label} ¥${price.toFixed(2)}</text>`;
  }).join("\n");
}

function renderAnnotations(annotations, bars, priceRange, xStart, xEnd, yTop, yBottom) {
  return annotations.map(a => {
    const dateIdx = bars.findIndex(b => b.d === a.date);
    if (dateIdx < 0) return "";
    const x = scaleX(dateIdx, bars.length, xStart, xEnd);
    const price = toNumber(a.price ?? bars[dateIdx]?.c);
    if (price === null) return "";
    const y = scaleValue(price, priceRange, { yTop, yBottom });
    const color = a.color ?? "#f59e0b";
    const symbol = a.type === "buy" ? "▲" : a.type === "sell" ? "▼" : "●";
    const offsetY = a.type === "sell" ? 16 : -10;
    return `<text x="${x}" y="${y + offsetY}" fill="${color}" font-size="10" text-anchor="middle" font-weight="700">${symbol}</text>
    ${a.label ? `<text x="${x}" y="${y + offsetY + (a.type === "sell" ? 10 : -8)}" fill="${color}" font-size="7" text-anchor="middle">${escapeXml(a.label)}</text>` : ""}`;
  }).join("\n");
}

// ============== 庐山照影图 ==============

export function renderLushanShadowSvg(shadowData, instrument) {
  const rows = safeSlice(shadowData?.data, 250);
  if (!rows.length) return buildEmptySvg("庐山照影图", instrument, "无数据");

  const w = 960, h = 480;
  const xStart = 70, xEnd = 880, yTop = 80, yBottom = 380;

  const dates = rows.map(r => r.d ?? r.trading_day);
  const cmValues = rows.map(r => toNumber(r.CM));
  const fcValues = rows.map(r => toNumber(r.FC));
  const mValues = rows.map(r => toNumber(r.M));

  const cmRange = { min: 0, max: 100 };
  const fcRange = { min: -100, max: 0 };
  const combinedRange = { min: -100, max: 100 };
  const midY = yTop + (yBottom - yTop) / 2;

  const cmBars = rows.map((r, i) => {
    const x = scaleX(i, rows.length, xStart, xEnd);
    const cm = toNumber(r.CM);
    if (cm === null) return "";
    const barW = Math.max(1, (xEnd - xStart) / rows.length * 0.7);
    const barH = Math.max(1, (cm / 100) * (midY - yTop));
    const color = cm >= 66 ? "#ef4444" : cm >= 33 ? "#f59e0b" : "#22c55e";
    const hasBg = toNumber(r.M) === 1;
    return `${hasBg ? `<rect x="${x - barW / 2}" y="${yTop}" width="${barW}" height="${midY - yTop}" fill="rgba(244,114,182,0.12)"/>` : ""}
    <rect x="${x - barW / 2}" y="${midY - barH}" width="${barW}" height="${barH}" fill="${color}" opacity="0.8"/>`;
  }).join("\n");

  const fcBars = rows.map((r, i) => {
    const x = scaleX(i, rows.length, xStart, xEnd);
    const fc = toNumber(r.FC);
    if (fc === null) return "";
    const barW = Math.max(1, (xEnd - xStart) / rows.length * 0.7);
    const barH = Math.max(1, (Math.abs(fc) / 100) * (yBottom - midY));
    const color = fc <= -60 ? "#3b82f6" : fc <= -40 ? "#60a5fa" : "#93c5fd";
    return `<rect x="${x - barW / 2}" y="${midY}" width="${barW}" height="${barH}" fill="${color}" opacity="0.8"/>`;
  }).join("\n");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "lsBg")}
  ${buildTitle(
    `${instrument.instrument_name}(${instrument.instrument_id}) 庐山照影图`,
    `${formatDateLabel(dates[0])} - ${formatDateLabel(dates.at(-1))} | CM=山 FC=影`
  )}
  <g id="grid">${buildGridLines(xStart, xEnd, yTop, yBottom, 8)}</g>
  <line x1="${xStart}" y1="${midY}" x2="${xEnd}" y2="${midY}" stroke="#64748b" stroke-width="1" opacity="0.8"/>
  ${buildRefLine(66, cmRange, xStart, xEnd, yTop, midY, { stroke: "#ef4444", label: "CM=66" })}
  ${buildRefLine(-60, fcRange, xStart, xEnd, midY, yBottom, { stroke: "#3b82f6", label: "FC=-60" })}
  <g id="cm-bars">${cmBars}</g>
  <g id="fc-bars">${fcBars}</g>
  <g id="axis-labels">
    <text x="${xStart - 6}" y="${yTop + 10}" fill="#ef4444" font-size="8" text-anchor="end">山(CM)</text>
    <text x="${xStart - 6}" y="${yBottom - 4}" fill="#3b82f6" font-size="8" text-anchor="end">影(FC)</text>
  </g>
  <g id="date-axis">${buildDateAxis(dates, xStart, xEnd, yBottom + 16)}</g>
  <g id="legend">
    <rect x="700" y="${h - 30}" width="8" height="8" fill="#ef4444" opacity="0.8"/><text x="712" y="${h - 23}" fill="#94a3b8" font-size="8">CM≥66 高位</text>
    <rect x="780" y="${h - 30}" width="8" height="8" fill="#3b82f6" opacity="0.8"/><text x="792" y="${h - 23}" fill="#94a3b8" font-size="8">FC≤-60 低位</text>
    <rect x="860" y="${h - 30}" width="8" height="8" fill="rgba(244,114,182,0.3)"/><text x="872" y="${h - 23}" fill="#94a3b8" font-size="8">M=1 标记</text>
  </g>
  <text x="${w / 2}" y="${h - 6}" fill="#475569" font-size="8" text-anchor="middle">功夫量化 KungFu Finance | 庐山照影图</text>
</svg>`;
}

// ============== 庐山四季图 ==============

export function renderLushan4SeasonSvg(seasonData, instrument) {
  const rows = safeSlice(seasonData?.data, 250);
  if (!rows.length) return buildEmptySvg("庐山四季图", instrument, "无数据");

  const w = 960, h = 520;
  const xStart = 70, xEnd = 880, yTop = 80, yBottom = 340, rsTop = 360, rsBottom = 430;

  const dates = rows.map(r => r.d ?? r.trading_day);
  const ggVals = rows.map(r => toNumber(r.GG));
  const hyVals = rows.map(r => toNumber(r.HY));
  const dpVals = rows.map(r => toNumber(r.DP));
  const rsVals = rows.map(r => toNumber(r.RS));
  const allLineVals = [...ggVals, ...hyVals, ...dpVals].filter(v => v !== null);
  const lineRange = extent(allLineVals.length ? allLineVals : [0, 100]);
  if (lineRange.min > 0) lineRange.min = 0;
  if (lineRange.max < 100) lineRange.max = 100;
  const rsRange = extent(rsVals.filter(v => v !== null));

  const ggLine = buildPolyline(ggVals.map(v => v ?? 0), xStart, xEnd, yTop, yBottom, lineRange, { stroke: "#ef4444", strokeWidth: 2 });
  const hyLine = buildPolyline(hyVals.map(v => v ?? 0), xStart, xEnd, yTop, yBottom, lineRange, { stroke: "#3b82f6", strokeWidth: 1.5 });
  const dpLine = buildPolyline(dpVals.map(v => v ?? 0), xStart, xEnd, yTop, yBottom, lineRange, { stroke: "#eab308", strokeWidth: 2 });

  const rsBars = rows.map((r, i) => {
    const x = scaleX(i, rows.length, xStart, xEnd);
    const rs = toNumber(r.RS);
    if (rs === null) return "";
    const barW = Math.max(1, (xEnd - xStart) / rows.length * 0.6);
    const rsMid = rsTop + (rsBottom - rsTop) / 2;
    const barH = Math.abs(rs) / Math.max(Math.abs(rsRange.max), Math.abs(rsRange.min), 1) * ((rsBottom - rsTop) / 2);
    const color = rs >= 0 ? "rgba(251,191,36,0.6)" : "rgba(167,139,250,0.5)";
    return rs >= 0
      ? `<rect x="${x - barW / 2}" y="${rsMid - barH}" width="${barW}" height="${barH}" fill="${color}"/>`
      : `<rect x="${x - barW / 2}" y="${rsMid}" width="${barW}" height="${barH}" fill="${color}"/>`;
  }).join("\n");

  const gzMarkers = rows.map((r, i) => {
    const isGz = r.GZ === "是" || r.GZ === 1 || r.GZ === true;
    if (!isGz) return "";
    const x = scaleX(i, rows.length, xStart, xEnd);
    return `<text x="${x}" y="${yBottom + 12}" fill="#3b82f6" font-size="8" text-anchor="middle">▲</text>`;
  }).join("\n");

  const sMarkers = rows.map((r, i) => {
    const isS = r.S === "是" || r.S === 1 || r.S === true;
    if (!isS) return "";
    const x = scaleX(i, rows.length, xStart, xEnd);
    return `<text x="${x}" y="${yBottom + 22}" fill="#ef4444" font-size="8" text-anchor="middle">▲</text>`;
  }).join("\n");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "ls4Bg")}
  ${buildTitle(
    `${instrument.instrument_name}(${instrument.instrument_id}) 庐山四季图`,
    `${formatDateLabel(dates[0])} - ${formatDateLabel(dates.at(-1))} | GG/HY/DP + RS`
  )}
  <g id="grid">${buildGridLines(xStart, xEnd, yTop, yBottom)}</g>
  <g id="y-axis">${buildYAxisLabels(lineRange, xStart, yTop, yBottom, 4, { format: v => v.toFixed(0) })}</g>
  ${buildRefLine(89, lineRange, xStart, xEnd, yTop, yBottom, { stroke: "#22c55e", label: "顶 89", dashArray: "3,3" })}
  ${buildRefLine(11, lineRange, xStart, xEnd, yTop, yBottom, { stroke: "#ef4444", label: "底 11", dashArray: "3,3" })}
  <g id="lines">${ggLine}${hyLine}${dpLine}</g>
  <g id="rs-bars">${rsBars}</g>
  <g id="gz-markers">${gzMarkers}</g>
  <g id="s-markers">${sMarkers}</g>
  <text x="${xStart - 6}" y="${rsTop + 10}" fill="#64748b" font-size="8" text-anchor="end">RS</text>
  <g id="date-axis">${buildDateAxis(dates, xStart, xEnd, rsBottom + 16)}</g>
  <g id="legend">
    <line x1="600" y1="${h - 24}" x2="620" y2="${h - 24}" stroke="#ef4444" stroke-width="2"/><text x="624" y="${h - 20}" fill="#94a3b8" font-size="8">GG</text>
    <line x1="660" y1="${h - 24}" x2="680" y2="${h - 24}" stroke="#3b82f6" stroke-width="1.5"/><text x="684" y="${h - 20}" fill="#94a3b8" font-size="8">HY(JB)</text>
    <line x1="730" y1="${h - 24}" x2="750" y2="${h - 24}" stroke="#eab308" stroke-width="2"/><text x="754" y="${h - 20}" fill="#94a3b8" font-size="8">DP(ZT)</text>
    <text x="810" y="${h - 20}" fill="#3b82f6" font-size="8">▲底部共振</text>
    <text x="870" y="${h - 20}" fill="#ef4444" font-size="8">▲强势</text>
  </g>
  <text x="${w / 2}" y="${h - 4}" fill="#475569" font-size="8" text-anchor="middle">功夫量化 KungFu Finance | 庐山四季图</text>
</svg>`;
}

// ============== 双轮驱动图 ==============

export function renderShuanglunSvg(slData, instrument) {
  const rows = safeSlice(slData?.data, 250);
  if (!rows.length) return buildEmptySvg("双轮驱动图", instrument, "无数据");

  const w = 960, h = 420;
  const xStart = 70, xEnd = 880, yTop = 80, yBottom = 340;

  const dates = rows.map(r => r.d ?? r.trading_day);
  const kVals = rows.map(r => toNumber(r.k));
  const rVals = rows.map(r => toNumber(r.r));
  const allVals = [...kVals, ...rVals].filter(v => v !== null);
  const range = extent(allVals.length ? allVals : [0, 1]);
  const midY = scaleValue(0, range, { yTop, yBottom });

  const bars = rows.map((r, i) => {
    const x = scaleX(i, rows.length, xStart, xEnd);
    const k = toNumber(r.k), rv = toNumber(r.r), t = toNumber(r.t);
    if (k === null && rv === null) return "";
    const barW = Math.max(1, (xEnd - xStart) / rows.length * 0.7);
    const isTrend = t >= 1;
    let result = "";
    if (rv !== null && rv !== 0) {
      const yR = scaleValue(rv, range, { yTop, yBottom });
      const h = Math.abs(yR - midY);
      const yStart = rv >= 0 ? yR : midY;
      result += `<rect x="${x - barW / 2}" y="${yStart}" width="${barW}" height="${Math.max(1, h)}" fill="${isTrend ? "rgba(168,85,247,0.7)" : "rgba(250,204,21,0.6)"}"/>`;
    }
    if (k !== null && k !== 0) {
      const yK = scaleValue(k, range, { yTop, yBottom });
      const h = Math.abs(yK - midY);
      const yStart = k >= 0 ? yK : midY;
      result += `<rect x="${x - barW / 2}" y="${yStart}" width="${barW}" height="${Math.max(1, h)}" fill="${isTrend ? "rgba(236,72,153,0.7)" : "rgba(250,204,21,0.4)"}"/>`;
    }
    return result;
  }).join("\n");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "slBg")}
  ${buildTitle(
    `${instrument.instrument_name}(${instrument.instrument_id}) 双轮驱动图`,
    `${formatDateLabel(dates[0])} - ${formatDateLabel(dates.at(-1))} | K轮 + R轮`
  )}
  <g id="grid">${buildGridLines(xStart, xEnd, yTop, yBottom)}</g>
  <g id="y-axis">${buildYAxisLabels(range, xStart, yTop, yBottom)}</g>
  <line x1="${xStart}" y1="${midY}" x2="${xEnd}" y2="${midY}" stroke="#64748b" stroke-width="1"/>
  <g id="bars">${bars}</g>
  <g id="date-axis">${buildDateAxis(dates, xStart, xEnd, yBottom + 16)}</g>
  <g id="legend">
    <rect x="660" y="${h - 28}" width="8" height="8" fill="rgba(236,72,153,0.7)"/><text x="672" y="${h - 21}" fill="#94a3b8" font-size="8">趋势K</text>
    <rect x="730" y="${h - 28}" width="8" height="8" fill="rgba(168,85,247,0.7)"/><text x="742" y="${h - 21}" fill="#94a3b8" font-size="8">趋势R</text>
    <rect x="800" y="${h - 28}" width="8" height="8" fill="rgba(250,204,21,0.6)"/><text x="812" y="${h - 21}" fill="#94a3b8" font-size="8">非趋势</text>
  </g>
  <text x="${w / 2}" y="${h - 4}" fill="#475569" font-size="8" text-anchor="middle">功夫量化 KungFu Finance | 双轮驱动图</text>
</svg>`;
}

// ============== 六脉神剑图 ==============

export function renderLiumaiSvg(lmData, instrument) {
  const rows = safeSlice(lmData?.data, 250);
  if (!rows.length) return buildEmptySvg("六脉神剑图", instrument, "无数据");

  const w = 960, h = 420;
  const xStart = 100, xEnd = 880, yTop = 80, yBottom = 340;
  const colNames = lmData?.column_names ?? {};
  const signalKeys = ["s1", "s2", "s3", "s4", "s5", "s6"];
  const signalNames = signalKeys.map(k => colNames[k] ?? k);
  const rowH = (yBottom - yTop) / (signalKeys.length + 1);

  const dates = rows.map(r => r.d ?? r.trading_day);

  const rects = signalKeys.flatMap((key, si) => {
    const cy = yTop + rowH * si + rowH / 2;
    return rows.map((r, di) => {
      const x = scaleX(di, rows.length, xStart, xEnd);
      const v = toNumber(r[key]);
      if (v === null) return "";
      const rectW = Math.max(1, (xEnd - xStart) / rows.length * 0.85);
      const rectH = rowH * 0.7;
      const color = v === 1 ? "#ef4444" : "#22c55e";
      return `<rect x="${x - rectW / 2}" y="${cy - rectH / 2}" width="${rectW}" height="${rectH}" fill="${color}" opacity="0.8" rx="1"/>`;
    });
  }).join("\n");

  const buySignalRow = yTop + rowH * signalKeys.length + rowH / 2;
  const tradeSignals = rows.map((r, di) => {
    const o = toNumber(r.o);
    if (!o || o === 0) return "";
    const x = scaleX(di, rows.length, xStart, xEnd);
    if (o === 1) return `<text x="${x}" y="${buySignalRow + 4}" fill="#ef4444" font-size="10" text-anchor="middle">▲</text>`;
    if (o === -1) return `<text x="${x}" y="${buySignalRow + 4}" fill="#22c55e" font-size="10" text-anchor="middle">▼</text>`;
    return "";
  }).join("\n");

  const yLabels = signalNames.map((name, i) => {
    const cy = yTop + rowH * i + rowH / 2;
    return `<text x="${xStart - 8}" y="${cy + 4}" fill="#e2e8f0" font-size="9" text-anchor="end">${escapeXml(name)}</text>`;
  }).join("\n");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "lmBg")}
  ${buildTitle(
    `${instrument.instrument_name}(${instrument.instrument_id}) 六脉神剑图`,
    `${formatDateLabel(dates[0])} - ${formatDateLabel(dates.at(-1))} | 六维信号矩阵`
  )}
  <g id="y-labels">${yLabels}
    <text x="${xStart - 8}" y="${buySignalRow + 4}" fill="#f59e0b" font-size="9" text-anchor="end">买卖信号</text>
  </g>
  ${signalKeys.map((_, i) => {
    const cy = yTop + rowH * i + rowH;
    return `<line x1="${xStart}" y1="${cy}" x2="${xEnd}" y2="${cy}" stroke="#334155" stroke-width="0.5" opacity="0.4"/>`;
  }).join("\n")}
  <g id="rects">${rects}</g>
  <g id="trade-signals">${tradeSignals}</g>
  <g id="date-axis">${buildDateAxis(dates, xStart, xEnd, yBottom + 30)}</g>
  <g id="legend">
    <rect x="700" y="${h - 28}" width="8" height="8" fill="#ef4444" opacity="0.8"/><text x="712" y="${h - 21}" fill="#94a3b8" font-size="8">信号=1 (强)</text>
    <rect x="800" y="${h - 28}" width="8" height="8" fill="#22c55e" opacity="0.8"/><text x="812" y="${h - 21}" fill="#94a3b8" font-size="8">信号=0 (弱)</text>
  </g>
  <text x="${w / 2}" y="${h - 4}" fill="#475569" font-size="8" text-anchor="middle">功夫量化 KungFu Finance | 六脉神剑图</text>
</svg>`;
}

// ============== 聪明钱图 ==============

export function renderSmartMoneySvg(smData, instrument) {
  const rows = safeSlice(smData?.data, 250);
  if (!rows.length) return buildEmptySvg("聪明钱图", instrument, "无数据");

  const w = 960, h = 420;
  const xStart = 70, xEnd = 880, yTop = 80, yBottom = 340;

  const dates = rows.map(r => r.d ?? r.trading_day);
  const followVals = rows.map(r => toNumber(r.follow_money));
  const smartVals = rows.map(r => toNumber(r.smart_money));
  const allVals = [...followVals, ...smartVals].filter(v => v !== null);
  const range = extent(allVals.length ? allVals : [0, 100]);
  if (range.min > -1) range.min = -1;
  if (range.max < 80) range.max = 80;

  const followLine = buildPolyline(followVals.map(v => v ?? 0), xStart, xEnd, yTop, yBottom, range, { stroke: "#3b82f6", strokeWidth: 1.5, dashArray: "4,3" });
  const smartLine = buildPolyline(smartVals.map(v => v ?? 0), xStart, xEnd, yTop, yBottom, range, { stroke: "#ef4444", strokeWidth: 2.5 });

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "smBg")}
  ${buildTitle(
    `${instrument.instrument_name}(${instrument.instrument_id}) 聪明钱图`,
    `${formatDateLabel(dates[0])} - ${formatDateLabel(dates.at(-1))} | 聪明钱 vs 跟风钱`
  )}
  <g id="grid">${buildGridLines(xStart, xEnd, yTop, yBottom)}</g>
  <g id="y-axis">${buildYAxisLabels(range, xStart, yTop, yBottom, 4, { format: v => v.toFixed(0) })}</g>
  ${buildRefLine(80, range, xStart, xEnd, yTop, yBottom, { stroke: "#ef4444", label: "过热 80", dashArray: "3,3" })}
  ${buildRefLine(20, range, xStart, xEnd, yTop, yBottom, { stroke: "#22c55e", label: "低位 20", dashArray: "3,3" })}
  <g id="lines">${followLine}${smartLine}</g>
  <g id="date-axis">${buildDateAxis(dates, xStart, xEnd, yBottom + 16)}</g>
  <g id="legend">
    <line x1="700" y1="${h - 24}" x2="720" y2="${h - 24}" stroke="#ef4444" stroke-width="2.5"/><text x="724" y="${h - 20}" fill="#94a3b8" font-size="8">聪明钱</text>
    <line x1="790" y1="${h - 24}" x2="810" y2="${h - 24}" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4,3"/><text x="814" y="${h - 20}" fill="#94a3b8" font-size="8">跟风钱</text>
  </g>
  <text x="${w / 2}" y="${h - 4}" fill="#475569" font-size="8" text-anchor="middle">功夫量化 KungFu Finance | 聪明钱图</text>
</svg>`;
}

// ============== 个股综合得分 ==============

export function renderFinanceScoreSvg(scoreData, instrument) {
  const data = scoreData?.data;
  const row = Array.isArray(data) ? data[0] : data;
  if (!row) return buildEmptySvg("综合得分", instrument, "无得分数据");

  const w = 500, h = 380;
  const cx = 250, cy = 200, r = 110;

  const dims = [
    { key: "industry_dominance", label: "行业统治力", color: "#ef4444" },
    { key: "financial_health", label: "财务健康度", color: "#3b82f6" },
    { key: "growth_potential", label: "发展前景", color: "#22c55e" }
  ];

  const scores = dims.map(d => ({
    ...d,
    score: toNumber(row[`score_${d.key}`]) ?? 0,
    grade: row[`grade_${d.key}`] ?? "N/A"
  }));
  const total = toNumber(row.score_total) ?? 0;

  const angleStep = (2 * Math.PI) / 3;
  const startAngle = -Math.PI / 2;

  const axisLines = scores.map((_, i) => {
    const angle = startAngle + i * angleStep;
    const ex = cx + r * Math.cos(angle);
    const ey = cy + r * Math.sin(angle);
    return `<line x1="${cx}" y1="${cy}" x2="${ex}" y2="${ey}" stroke="#334155" stroke-width="1"/>`;
  }).join("\n");

  const gridLevels = [0.2, 0.4, 0.6, 0.8, 1.0];
  const gridPolygons = gridLevels.map(level => {
    const pts = scores.map((_, i) => {
      const angle = startAngle + i * angleStep;
      return `${cx + r * level * Math.cos(angle)},${cy + r * level * Math.sin(angle)}`;
    }).join(" ");
    return `<polygon points="${pts}" fill="none" stroke="#334155" stroke-width="0.5" opacity="0.6"/>`;
  }).join("\n");

  const dataPts = scores.map((s, i) => {
    const angle = startAngle + i * angleStep;
    const ratio = s.score / 5;
    return `${cx + r * ratio * Math.cos(angle)},${cy + r * ratio * Math.sin(angle)}`;
  }).join(" ");

  const labels = scores.map((s, i) => {
    const angle = startAngle + i * angleStep;
    const lx = cx + (r + 30) * Math.cos(angle);
    const ly = cy + (r + 30) * Math.sin(angle);
    return `<text x="${lx}" y="${ly}" fill="${s.color}" font-size="10" font-weight="700" text-anchor="middle">${escapeXml(s.label)}</text>
    <text x="${lx}" y="${ly + 14}" fill="#94a3b8" font-size="9" text-anchor="middle">${s.score.toFixed(1)} (${escapeXml(s.grade)})</text>`;
  }).join("\n");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "fsBg")}
  <text x="${cx}" y="36" fill="#e2e8f0" font-size="16" font-weight="700" text-anchor="middle">${escapeXml(instrument.instrument_name)}(${escapeXml(instrument.instrument_id)}) 综合得分</text>
  <text x="${cx}" y="54" fill="#f59e0b" font-size="22" font-weight="700" text-anchor="middle">${total.toFixed(1)}</text>
  <text x="${cx}" y="70" fill="#94a3b8" font-size="9" text-anchor="middle">满分 15 分</text>
  <g id="grid">${gridPolygons}${axisLines}</g>
  <polygon points="${dataPts}" fill="rgba(99,102,241,0.25)" stroke="#6366f1" stroke-width="2"/>
  ${scores.map((s, i) => {
    const angle = startAngle + i * angleStep;
    const ratio = s.score / 5;
    const px = cx + r * ratio * Math.cos(angle);
    const py = cy + r * ratio * Math.sin(angle);
    return `<circle cx="${px}" cy="${py}" r="4" fill="${s.color}" stroke="#fff" stroke-width="1.5"/>`;
  }).join("\n")}
  <g id="labels">${labels}</g>
  <text x="${cx}" y="${h - 10}" fill="#475569" font-size="8" text-anchor="middle">功夫量化 KungFu Finance | 个股综合得分</text>
</svg>`;
}

// ============== 空数据占位 ==============

function buildEmptySvg(chartName, instrument, message) {
  const w = 600, h = 200;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  ${buildDarkBackground(w, h, "emptyBg")}
  <text x="${w / 2}" y="60" fill="#e2e8f0" font-size="16" font-weight="700" text-anchor="middle">${escapeXml(instrument?.instrument_name ?? "")} ${escapeXml(chartName)}</text>
  <text x="${w / 2}" y="110" fill="#94a3b8" font-size="14" text-anchor="middle">${escapeXml(message)}</text>
</svg>`;
}
