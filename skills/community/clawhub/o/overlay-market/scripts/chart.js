#!/usr/bin/env node

// Overlay Protocol — Market Chart Data
// Fetches OHLC candles + computed indicators for a single market.
// Usage: node chart.js <market-name-or-address> [timeframe] [candles]

import { CHARTS_API, resolveMarket, fetchWithTimeout, fmtPrice, fmtPct, padCol } from "./common.js";

const TIMEFRAMES = {
  "5m":  { binSize: 5,   binUnit: "minute", ms: 5 * 60000 },
  "15m": { binSize: 15,  binUnit: "minute", ms: 15 * 60000 },
  "30m": { binSize: 30,  binUnit: "minute", ms: 30 * 60000 },
  "1h":  { binSize: 60,  binUnit: "minute", ms: 60 * 60000 },
  "4h":  { binSize: 240, binUnit: "minute", ms: 240 * 60000 },
  "12h": { binSize: 720, binUnit: "minute", ms: 720 * 60000 },
  "1d":  { binSize: 1,   binUnit: "day",    ms: 86400000 },
};

function sma(closes, period) {
  if (closes.length < period) return null;
  return closes.slice(-period).reduce((a, b) => a + b, 0) / period;
}

function rsi(closes, period) {
  if (closes.length < period + 1) return null;
  let gains = 0, losses = 0;
  for (let i = closes.length - period; i < closes.length; i++) {
    const diff = closes[i] - closes[i - 1];
    if (diff > 0) gains += diff; else losses -= diff;
  }
  const avgLoss = losses / period;
  if (avgLoss === 0) return 100;
  return 100 - 100 / (1 + gains / period / avgLoss);
}

function atr(candles, period) {
  if (candles.length < period + 1) return null;
  const trs = [];
  for (let i = candles.length - period; i < candles.length; i++) {
    const c = candles[i], prev = candles[i - 1].close;
    trs.push(Math.max(c.high - c.low, Math.abs(c.high - prev), Math.abs(c.low - prev)));
  }
  return trs.reduce((a, b) => a + b, 0) / period;
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error("Usage: node chart.js <market-name-or-address> [timeframe] [candles]");
  console.error("  timeframe: 5m, 15m, 30m, 1h, 4h, 12h, 1d (default: 1h)");
  console.error("  candles:   number of candles (default: 48)");
  process.exit(1);
}

const tfKey = (args[1] || "1h").toLowerCase();
const numCandles = parseInt(args[2]) || 48;
const tf = TIMEFRAMES[tfKey];

if (!tf) {
  console.error(`Invalid timeframe: ${tfKey}. Valid: ${Object.keys(TIMEFRAMES).join(", ")}`);
  process.exit(1);
}

const market = await resolveMarket(args[0]);
const from = new Date(Date.now() - numCandles * tf.ms).toISOString();
const url = `${CHARTS_API}?market=${market.address}&binSize=${tf.binSize}&binUnit=${tf.binUnit}&from=${from}`;
const raw = await fetchWithTimeout(url).then((r) => r.json());

if (!Array.isArray(raw) || raw.length === 0) {
  console.error(`No candle data for ${market.name} (${market.address})`);
  process.exit(1);
}

raw.sort((a, b) => new Date(a._id.time) - new Date(b._id.time));
const candles = raw.slice(-numCandles);
const closes = candles.map((c) => c.close);
const current = closes[closes.length - 1];

const sma20 = sma(closes, 20);
const rsi14 = rsi(closes, 14);
const atr14 = atr(candles, 14);
const atrPct = atr14 != null && current > 0 ? (atr14 / current) * 100 : null;

const rangeHigh = Math.max(...candles.map((c) => c.high));
const rangeLow = Math.min(...candles.map((c) => c.low));
const rangePos = rangeHigh !== rangeLow ? ((current - rangeLow) / (rangeHigh - rangeLow)) * 100 : 50;

const candlesPerDay = Math.max(1, Math.floor(86400000 / tf.ms));
const recent24h = candles.slice(-Math.min(candlesPerDay, candles.length));
const r24High = Math.max(...recent24h.map((c) => c.high));
const r24Low = Math.min(...recent24h.map((c) => c.low));
const r24Pos = r24High !== r24Low ? ((current - r24Low) / (r24High - r24Low)) * 100 : 50;

const firstClose = closes[0];
const periodChange = firstClose > 0 ? ((current - firstClose) / Math.abs(firstClose)) * 100 : null;

console.log(`== ${market.name} (${market.address}) ==`);
console.log(`${tfKey} candles | ${candles.length} periods | ${new Date().toISOString().replace(/\.\d+Z/, "Z")}`);
console.log("");
console.log("Current Price: " + fmtPrice(current));
console.log(`Period Change: ${fmtPct(periodChange)} (over ${candles.length} candles)`);
console.log("SMA(20): " + (sma20 != null ? fmtPrice(sma20) : "N/A (need 20+ candles)"));
console.log("RSI(14): " + (rsi14 != null ? rsi14.toFixed(1) : "N/A (need 15+ candles)"));
console.log("ATR(14): " + (atr14 != null ? `${fmtPrice(atr14)} (${atrPct.toFixed(2)}% of price)` : "N/A (need 15+ candles)"));
console.log(`Range: ${fmtPrice(rangeLow)} — ${fmtPrice(rangeHigh)} (position: ${rangePos.toFixed(1)}%)`);
if (candles.length > candlesPerDay && candlesPerDay > 1) {
  console.log(`24h Range: ${fmtPrice(r24Low)} — ${fmtPrice(r24High)} (position: ${r24Pos.toFixed(1)}%)`);
}

const display = candles.slice(-20);
console.log("");
console.log(padCol("Time", 22, true) + padCol("Open", 16) + padCol("High", 16) + padCol("Low", 16) + padCol("Close", 16));
console.log("-".repeat(86));
for (const c of display) {
  const t = c._id.time.replace("T", " ").replace(/\.\d+Z/, "").replace("Z", "");
  console.log(padCol(t, 22, true) + padCol(fmtPrice(c.open), 16) + padCol(fmtPrice(c.high), 16) + padCol(fmtPrice(c.low), 16) + padCol(fmtPrice(c.close), 16));
}
if (candles.length > 20) console.log(`(showing last 20 of ${candles.length} candles)`);
console.log(`\nFor market description: node scripts/scan.js --details "${market.name}"`);
