// ═══════════════════════════════════════════════════
// Polymarket Trading Strategy
// Timeframes: 5min / 15min
// Assets: BTC, ETH, SOL, XRP
// ═══════════════════════════════════════════════════

// Binance public API for price data (no key needed)
const PRICE_API = 'https://api.binance.com/api/v3';

const SYMBOLS = {
  BTC: 'BTCUSDT',
  ETH: 'ETHUSDT',
  SOL: 'SOLUSDT',
  XRP: 'XRPUSDT',
};

// Fetch OHLCV candles from Binance
async function getCandles(asset, interval, limit = 50) {
  const symbol = SYMBOLS[asset];
  if (!symbol) throw new Error(`Unsupported asset: ${asset}`);

  const url = `${PRICE_API}/klines?symbol=${symbol}&interval=${interval}&limit=${limit}`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`Price fetch failed: ${resp.statusText}`);
  const data = await resp.json();

  return data.map(c => ({
    time:   c[0],
    open:   parseFloat(c[1]),
    high:   parseFloat(c[2]),
    low:    parseFloat(c[3]),
    close:  parseFloat(c[4]),
    volume: parseFloat(c[5]),
  }));
}

// RSI calculation
function calcRSI(closes, period = 14) {
  if (closes.length < period + 1) return null;
  let gains = 0, losses = 0;
  for (let i = closes.length - period; i < closes.length; i++) {
    const diff = closes[i] - closes[i - 1];
    if (diff >= 0) gains += diff;
    else losses += Math.abs(diff);
  }
  const avgGain = gains / period;
  const avgLoss = losses / period;
  if (avgLoss === 0) return 100;
  const rs = avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

// EMA calculation
function calcEMA(closes, period) {
  const k = 2 / (period + 1);
  let ema = closes[0];
  for (let i = 1; i < closes.length; i++) {
    ema = closes[i] * k + ema * (1 - k);
  }
  return ema;
}

// MACD
function calcMACD(closes) {
  const ema12 = calcEMA(closes, 12);
  const ema26 = calcEMA(closes, 26);
  return ema12 - ema26;
}

// Volume trend
function isVolumeIncreasing(candles, lookback = 5) {
  const recent = candles.slice(-lookback);
  const avgVol = recent.slice(0, -1).reduce((s, c) => s + c.volume, 0) / (lookback - 1);
  return recent[recent.length - 1].volume > avgVol * 1.2;
}

/**
 * Generate a trade signal for a given asset and timeframe.
 * @param {string} asset  - BTC | ETH | SOL | XRP
 * @param {'5m'|'15m'} tf - Timeframe
 * @returns {{ signal: 'BUY'|'SELL'|'HOLD', confidence: number, price: number, rsi: number, macd: number }}
 */
async function generateSignal(asset, tf) {
  const interval = tf === '5m' ? '5m' : '15m';
  const candles = await getCandles(asset, interval, 60);
  const closes  = candles.map(c => c.close);
  const price   = closes[closes.length - 1];

  const rsi  = calcRSI(closes, 14);
  const macd = calcMACD(closes);
  const ema9 = calcEMA(closes, 9);
  const ema21 = calcEMA(closes, 21);
  const volUp = isVolumeIncreasing(candles);

  let bullScore = 0;
  let bearScore = 0;

  // RSI signals
  if (rsi !== null) {
    if (rsi < 35) bullScore += 2;
    else if (rsi < 45) bullScore += 1;
    if (rsi > 65) bearScore += 2;
    else if (rsi > 55) bearScore += 1;
  }

  // MACD signals
  if (macd > 0) bullScore += 1;
  else bearScore += 1;

  // EMA crossover
  if (ema9 > ema21) bullScore += 2;
  else bearScore += 2;

  // Volume confirmation
  if (volUp && bullScore > bearScore) bullScore += 1;
  if (volUp && bearScore > bullScore) bearScore += 1;

  const total = bullScore + bearScore;
  let signal = 'HOLD';
  let confidence = 0;

  if (bullScore > bearScore && bullScore >= 4) {
    signal = 'BUY';
    confidence = Math.round((bullScore / total) * 100);
  } else if (bearScore > bullScore && bearScore >= 4) {
    signal = 'SELL';
    confidence = Math.round((bearScore / total) * 100);
  }

  return { signal, confidence, price, rsi, macd, ema9, ema21 };
}

module.exports = { generateSignal, getCandles };
