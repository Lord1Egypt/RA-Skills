#!/usr/bin/env node

/**
 * 历史K线数据获取与技术指标计算脚本
 * 
 * 使用方法：
 *   node kline.js --symbol=600036.SH [--period=daily] [--adjust=none] [--limit=100] [--with=ma,macd] [--format=json]
 * 
 * 环境变量：
 *   JRJ_API_KEY - API Key（必须）
 */

const https = require('https');
const http = require('http');

// ==================== 配置 ====================

const DEFAULT_API_URL = 'https://quant-gw.jrj.com';
const API_URL = process.env.JRJ_API_URL || DEFAULT_API_URL;
const API_KEY = process.env.JRJ_API_KEY;

// 指标组定义
const INDICATOR_GROUPS = {
  ma: ['ma5', 'ma10', 'ma20', 'ma60'],
  macd: ['macd_dif', 'macd_dea', 'macd_hist'],
  kdj: ['kdj_k', 'kdj_d', 'kdj_j'],
  boll: ['boll_upper', 'boll_mid', 'boll_lower'],
  rsi: ['rsi6', 'rsi12', 'rsi24'],
  wr: ['wr14'],
  obv: ['obv', 'obv_ma20'],
  atr: ['atr', 'atr_ma14'],
  vol: ['vol_ma5', 'vol_ma10'],
  cci: ['cci'],
  roc: ['roc'],
};

// 指标所需的预热周期数
const INDICATOR_WARMUP = {
  ma5: 5,
  ma10: 10,
  ma20: 20,
  ma60: 60,
  ma250: 250,
  macd_dif: 34,  // 26 + 9 - 1
  macd_dea: 34,
  macd_hist: 34,
  kdj_k: 9,
  kdj_d: 9,
  kdj_j: 9,
  boll_upper: 20,
  boll_mid: 20,
  boll_lower: 20,
  rsi6: 7,
  rsi12: 13,
  rsi24: 25,
  wr14: 14,
  obv: 1,
  obv_ma20: 20,
  atr: 14,
  atr_ma14: 28,
  vol_ma5: 5,
  vol_ma10: 10,
  cci: 20,
  roc: 13,  // 需要 closes[i] 和 closes[i-12]，即 13 个点
};

// ==================== 工具函数 ====================

function parseArgs() {
  const args = {
    symbol: null,
    period: 'daily',
    adjust: 'none',
    limit: 100,
    startDate: null,
    with: [],
    format: 'json',
  };

  for (const arg of process.argv.slice(2)) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      if (key === 'symbol') args.symbol = value;
      else if (key === 'period') args.period = value;
      else if (key === 'adjust') args.adjust = value;
      else if (key === 'limit') args.limit = parseInt(value, 10);
      else if (key === 'start-date') args.startDate = parseInt(value, 10);
      else if (key === 'with') args.with = value ? value.split(',').map(s => s.trim().toLowerCase()) : [];
      else if (key === 'format') args.format = value;
      else if (key === 'help') {
        printHelp();
        process.exit(0);
      }
    }
  }

  return args;
}

function printHelp() {
  console.log(`
历史K线数据获取与技术指标计算

用法:
  node kline.js --symbol=<代码> [选项]

必填参数:
  --symbol=<代码>     证券代码，如 600036.SH, 000001.SZ

可选参数:
  --period=<周期>     K线周期: daily(默认)，目前只支持日K
  --adjust=<复权>     复权类型: none(默认), qfq(前复权), hfq(后复权)
  --limit=<数量>      K线数量，默认 100
  --start-date=<日期> 起始日期 YYYYMMDD，从该日期往最新方向取数据
  --with=<指标>       计算指标，逗号分隔，如: ma,macd,kdj
  --format=<格式>     输出格式: json(默认), markdown
  --help              显示帮助信息

指标组:
  ma      均线 (ma5, ma10, ma20, ma60)
  macd    MACD (macd_dif, macd_dea, macd_hist)
  kdj     KDJ (kdj_k, kdj_d, kdj_j)
  boll    布林带 (boll_upper, boll_mid, boll_lower)
  rsi     RSI (rsi6, rsi12, rsi24)
  wr      威廉 (wr14)
  obv     OBV (obv, obv_ma20)
  atr     ATR (atr, atr_ma14)
  vol     成交量均线 (vol_ma5, vol_ma10)
  cci     CCI (cci)
  roc     ROC (roc)

示例:
  node kline.js --symbol=600036.SH
  node kline.js --symbol=600036.SH --with=ma,macd
  node kline.js --symbol=600036.SH --start-date=20260101 --limit=100
  node kline.js --symbol=600036.SH --adjust=qfq --limit=50 --with=ma,kdj --format=markdown

环境变量:
  JRJ_API_KEY   API Key

注意: 只返回已收盘的历史日K线数据
`);
}

function error(msg) {
  console.error(`错误: ${msg}`);
  process.exit(1);
}

// ==================== API 调用 ====================

async function fetchKline(symbol, period, adjust, limit, startDate) {
  if (!API_KEY) error('请设置环境变量 JRJ_API_KEY');

  const url = new URL('/v1/quote/kline', API_URL);
  const body = {
    symbol,
    period,
    adjust,
    limit,
  };
  
  // 可选参数
  if (startDate) {
    body.start_date = startDate;
  }

  return new Promise((resolve, reject) => {
    const protocol = url.protocol === 'https:' ? https : http;
    const req = protocol.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.code !== 0) {
            reject(new Error(`API错误 [${json.code}]: ${json.msg}`));
          } else {
            resolve(json.data);
          }
        } catch (e) {
          reject(new Error(`响应解析失败: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(body));
    req.end();
  });
}

// ==================== 指标计算 ====================

/**
 * 简单移动平均 SMA
 */
function sma(data, period) {
  const result = new Array(data.length).fill(null);
  for (let i = period - 1; i < data.length; i++) {
    let sum = 0;
    for (let j = 0; j < period; j++) {
      sum += data[i - j];
    }
    result[i] = sum / period;
  }
  return result;
}

/**
 * 指数移动平均 EMA
 */
function ema(data, period) {
  const result = new Array(data.length).fill(null);
  const multiplier = 2 / (period + 1);
  
  // 第一个值使用 SMA
  let sum = 0;
  for (let i = 0; i < period && i < data.length; i++) {
    sum += data[i];
  }
  if (period <= data.length) {
    result[period - 1] = sum / period;
  }
  
  // 后续使用 EMA 公式
  for (let i = period; i < data.length; i++) {
    result[i] = (data[i] - result[i - 1]) * multiplier + result[i - 1];
  }
  
  return result;
}

/**
 * 计算 MACD
 */
function calcMACD(closes) {
  const ema12 = ema(closes, 12);
  const ema26 = ema(closes, 26);
  
  const dif = new Array(closes.length).fill(null);
  for (let i = 0; i < closes.length; i++) {
    if (ema12[i] !== null && ema26[i] !== null) {
      dif[i] = ema12[i] - ema26[i];
    }
  }
  
  // DEA 是 DIF 的 9 日 EMA
  const validDif = dif.map(v => v === null ? 0 : v);
  const dea = ema(validDif, 9);
  
  // 修正 DEA 的前置 null
  for (let i = 0; i < 25; i++) {
    dea[i] = null;
  }
  
  const hist = new Array(closes.length).fill(null);
  for (let i = 0; i < closes.length; i++) {
    if (dif[i] !== null && dea[i] !== null) {
      hist[i] = (dif[i] - dea[i]) * 2;  // MACD 柱状图通常乘以 2
    }
  }
  
  return { dif, dea, hist };
}

/**
 * 计算 KDJ
 */
function calcKDJ(highs, lows, closes, period = 9) {
  const len = closes.length;
  const rsv = new Array(len).fill(null);
  const k = new Array(len).fill(null);
  const d = new Array(len).fill(null);
  const j = new Array(len).fill(null);
  
  for (let i = period - 1; i < len; i++) {
    let highestHigh = -Infinity;
    let lowestLow = Infinity;
    
    for (let j = 0; j < period; j++) {
      highestHigh = Math.max(highestHigh, highs[i - j]);
      lowestLow = Math.min(lowestLow, lows[i - j]);
    }
    
    if (highestHigh !== lowestLow) {
      rsv[i] = ((closes[i] - lowestLow) / (highestHigh - lowestLow)) * 100;
    } else {
      rsv[i] = 50;
    }
  }
  
  // K = 2/3 * 前K + 1/3 * RSV，初始 K = 50
  // D = 2/3 * 前D + 1/3 * K，初始 D = 50
  let prevK = 50;
  let prevD = 50;
  
  for (let i = period - 1; i < len; i++) {
    k[i] = (2 / 3) * prevK + (1 / 3) * rsv[i];
    d[i] = (2 / 3) * prevD + (1 / 3) * k[i];
    j[i] = 3 * k[i] - 2 * d[i];
    prevK = k[i];
    prevD = d[i];
  }
  
  return { k, d, j };
}

/**
 * 计算布林带
 */
function calcBOLL(closes, period = 20, multiplier = 2) {
  const mid = sma(closes, period);
  const upper = new Array(closes.length).fill(null);
  const lower = new Array(closes.length).fill(null);
  
  for (let i = period - 1; i < closes.length; i++) {
    // 计算标准差
    let sum = 0;
    for (let j = 0; j < period; j++) {
      sum += Math.pow(closes[i - j] - mid[i], 2);
    }
    const std = Math.sqrt(sum / period);
    
    upper[i] = mid[i] + multiplier * std;
    lower[i] = mid[i] - multiplier * std;
  }
  
  return { upper, mid, lower };
}

/**
 * 计算 RSI
 */
function calcRSI(closes, period) {
  const len = closes.length;
  const rsi = new Array(len).fill(null);
  
  if (len < period + 1) return rsi;
  
  // 计算涨跌幅
  const changes = new Array(len).fill(0);
  for (let i = 1; i < len; i++) {
    changes[i] = closes[i] - closes[i - 1];
  }
  
  // 初始平均涨幅和跌幅
  let avgGain = 0;
  let avgLoss = 0;
  
  for (let i = 1; i <= period; i++) {
    if (changes[i] > 0) avgGain += changes[i];
    else avgLoss += Math.abs(changes[i]);
  }
  
  avgGain /= period;
  avgLoss /= period;
  
  if (avgLoss === 0) {
    rsi[period] = 100;
  } else {
    rsi[period] = 100 - (100 / (1 + avgGain / avgLoss));
  }
  
  // 后续使用平滑方式
  for (let i = period + 1; i < len; i++) {
    const change = changes[i];
    const gain = change > 0 ? change : 0;
    const loss = change < 0 ? Math.abs(change) : 0;
    
    avgGain = (avgGain * (period - 1) + gain) / period;
    avgLoss = (avgLoss * (period - 1) + loss) / period;
    
    if (avgLoss === 0) {
      rsi[i] = 100;
    } else {
      rsi[i] = 100 - (100 / (1 + avgGain / avgLoss));
    }
  }
  
  return rsi;
}

/**
 * 计算威廉指标 WR
 */
function calcWR(highs, lows, closes, period = 14) {
  const len = closes.length;
  const wr = new Array(len).fill(null);
  
  for (let i = period - 1; i < len; i++) {
    let highestHigh = -Infinity;
    let lowestLow = Infinity;
    
    for (let j = 0; j < period; j++) {
      highestHigh = Math.max(highestHigh, highs[i - j]);
      lowestLow = Math.min(lowestLow, lows[i - j]);
    }
    
    if (highestHigh !== lowestLow) {
      wr[i] = ((highestHigh - closes[i]) / (highestHigh - lowestLow)) * -100;
    } else {
      wr[i] = -50;
    }
  }
  
  return wr;
}

/**
 * 计算 OBV
 */
function calcOBV(closes, volumes) {
  const len = closes.length;
  const obv = new Array(len).fill(null);
  
  obv[0] = volumes[0];
  
  for (let i = 1; i < len; i++) {
    if (closes[i] > closes[i - 1]) {
      obv[i] = obv[i - 1] + volumes[i];
    } else if (closes[i] < closes[i - 1]) {
      obv[i] = obv[i - 1] - volumes[i];
    } else {
      obv[i] = obv[i - 1];
    }
  }
  
  return obv;
}

/**
 * 计算 ATR (Average True Range)
 */
function calcATR(highs, lows, closes, period = 14) {
  const len = closes.length;
  const tr = new Array(len).fill(null);
  const atr = new Array(len).fill(null);
  
  // True Range
  tr[0] = highs[0] - lows[0];
  for (let i = 1; i < len; i++) {
    const hl = highs[i] - lows[i];
    const hc = Math.abs(highs[i] - closes[i - 1]);
    const lc = Math.abs(lows[i] - closes[i - 1]);
    tr[i] = Math.max(hl, hc, lc);
  }
  
  // ATR = SMA of TR
  for (let i = period - 1; i < len; i++) {
    let sum = 0;
    for (let j = 0; j < period; j++) {
      sum += tr[i - j];
    }
    atr[i] = sum / period;
  }
  
  return atr;
}

/**
 * 计算 CCI (Commodity Channel Index)
 */
function calcCCI(highs, lows, closes, period = 20) {
  const len = closes.length;
  const cci = new Array(len).fill(null);
  
  // 典型价格 TP = (H + L + C) / 3
  const tp = new Array(len);
  for (let i = 0; i < len; i++) {
    tp[i] = (highs[i] + lows[i] + closes[i]) / 3;
  }
  
  for (let i = period - 1; i < len; i++) {
    // TP 的 SMA
    let smaTP = 0;
    for (let j = 0; j < period; j++) {
      smaTP += tp[i - j];
    }
    smaTP /= period;
    
    // 平均绝对偏差 MAD
    let mad = 0;
    for (let j = 0; j < period; j++) {
      mad += Math.abs(tp[i - j] - smaTP);
    }
    mad /= period;
    
    if (mad !== 0) {
      cci[i] = (tp[i] - smaTP) / (0.015 * mad);
    } else {
      cci[i] = 0;
    }
  }
  
  return cci;
}

/**
 * 计算 ROC (Rate of Change)
 */
function calcROC(closes, period = 12) {
  const len = closes.length;
  const roc = new Array(len).fill(null);
  
  for (let i = period; i < len; i++) {
    if (closes[i - period] !== 0) {
      roc[i] = ((closes[i] - closes[i - period]) / closes[i - period]) * 100;
    }
  }
  
  return roc;
}

// ==================== 主逻辑 ====================

/**
 * 解析指标列表，展开指标组
 */
function parseIndicators(withList) {
  const indicators = new Set();
  
  for (const item of withList) {
    if (INDICATOR_GROUPS[item]) {
      // 是指标组，展开
      for (const ind of INDICATOR_GROUPS[item]) {
        indicators.add(ind);
      }
    } else {
      // 是单个指标
      indicators.add(item);
    }
  }
  
  return Array.from(indicators);
}

/**
 * 计算所需的预热周期
 */
function getWarmupPeriod(indicators) {
  let maxWarmup = 0;
  for (const ind of indicators) {
    const warmup = INDICATOR_WARMUP[ind] || 0;
    maxWarmup = Math.max(maxWarmup, warmup);
  }
  return maxWarmup;
}

/**
 * 计算指标并添加到 K 线数据
 */
function calculateIndicators(klines, indicators) {
  if (indicators.length === 0 || klines.length === 0) return klines;
  
  // 提取价格数组
  const opens = klines.map(k => k.open);
  const highs = klines.map(k => k.high);
  const lows = klines.map(k => k.low);
  const closes = klines.map(k => k.close);
  const volumes = klines.map(k => k.volume);
  
  const indicatorSet = new Set(indicators);
  
  // MA 系列
  if (indicatorSet.has('ma5')) {
    const ma = sma(closes, 5);
    klines.forEach((k, i) => k.ma5 = ma[i]);
  }
  if (indicatorSet.has('ma10')) {
    const ma = sma(closes, 10);
    klines.forEach((k, i) => k.ma10 = ma[i]);
  }
  if (indicatorSet.has('ma20')) {
    const ma = sma(closes, 20);
    klines.forEach((k, i) => k.ma20 = ma[i]);
  }
  if (indicatorSet.has('ma60')) {
    const ma = sma(closes, 60);
    klines.forEach((k, i) => k.ma60 = ma[i]);
  }
  if (indicatorSet.has('ma250')) {
    const ma = sma(closes, 250);
    klines.forEach((k, i) => k.ma250 = ma[i]);
  }
  
  // MACD
  if (indicatorSet.has('macd_dif') || indicatorSet.has('macd_dea') || indicatorSet.has('macd_hist')) {
    const { dif, dea, hist } = calcMACD(closes);
    if (indicatorSet.has('macd_dif')) klines.forEach((k, i) => k.macd_dif = dif[i]);
    if (indicatorSet.has('macd_dea')) klines.forEach((k, i) => k.macd_dea = dea[i]);
    if (indicatorSet.has('macd_hist')) klines.forEach((k, i) => k.macd_hist = hist[i]);
  }
  
  // KDJ
  if (indicatorSet.has('kdj_k') || indicatorSet.has('kdj_d') || indicatorSet.has('kdj_j')) {
    const { k, d, j } = calcKDJ(highs, lows, closes);
    if (indicatorSet.has('kdj_k')) klines.forEach((kl, i) => kl.kdj_k = k[i]);
    if (indicatorSet.has('kdj_d')) klines.forEach((kl, i) => kl.kdj_d = d[i]);
    if (indicatorSet.has('kdj_j')) klines.forEach((kl, i) => kl.kdj_j = j[i]);
  }
  
  // BOLL
  if (indicatorSet.has('boll_upper') || indicatorSet.has('boll_mid') || indicatorSet.has('boll_lower')) {
    const { upper, mid, lower } = calcBOLL(closes);
    if (indicatorSet.has('boll_upper')) klines.forEach((k, i) => k.boll_upper = upper[i]);
    if (indicatorSet.has('boll_mid')) klines.forEach((k, i) => k.boll_mid = mid[i]);
    if (indicatorSet.has('boll_lower')) klines.forEach((k, i) => k.boll_lower = lower[i]);
  }
  
  // RSI
  if (indicatorSet.has('rsi6')) {
    const rsi = calcRSI(closes, 6);
    klines.forEach((k, i) => k.rsi6 = rsi[i]);
  }
  if (indicatorSet.has('rsi12')) {
    const rsi = calcRSI(closes, 12);
    klines.forEach((k, i) => k.rsi12 = rsi[i]);
  }
  if (indicatorSet.has('rsi24')) {
    const rsi = calcRSI(closes, 24);
    klines.forEach((k, i) => k.rsi24 = rsi[i]);
  }
  
  // WR
  if (indicatorSet.has('wr14')) {
    const wr = calcWR(highs, lows, closes, 14);
    klines.forEach((k, i) => k.wr14 = wr[i]);
  }
  
  // OBV
  if (indicatorSet.has('obv') || indicatorSet.has('obv_ma20')) {
    const obv = calcOBV(closes, volumes);
    if (indicatorSet.has('obv')) klines.forEach((k, i) => k.obv = obv[i]);
    if (indicatorSet.has('obv_ma20')) {
      const obvMa = sma(obv.map(v => v || 0), 20);
      klines.forEach((k, i) => k.obv_ma20 = obvMa[i]);
    }
  }
  
  // ATR
  if (indicatorSet.has('atr') || indicatorSet.has('atr_ma14')) {
    const atr = calcATR(highs, lows, closes);
    if (indicatorSet.has('atr')) klines.forEach((k, i) => k.atr = atr[i]);
    if (indicatorSet.has('atr_ma14')) {
      const atrMa = sma(atr.map(v => v || 0), 14);
      klines.forEach((k, i) => k.atr_ma14 = atrMa[i]);
    }
  }
  
  // VOL MA
  if (indicatorSet.has('vol_ma5')) {
    const ma = sma(volumes, 5);
    klines.forEach((k, i) => k.vol_ma5 = ma[i]);
  }
  if (indicatorSet.has('vol_ma10')) {
    const ma = sma(volumes, 10);
    klines.forEach((k, i) => k.vol_ma10 = ma[i]);
  }
  
  // CCI
  if (indicatorSet.has('cci')) {
    const cci = calcCCI(highs, lows, closes);
    klines.forEach((k, i) => k.cci = cci[i]);
  }
  
  // ROC
  if (indicatorSet.has('roc')) {
    const roc = calcROC(closes);
    klines.forEach((k, i) => k.roc = roc[i]);
  }
  
  return klines;
}

/**
 * 格式化数字
 */
function formatNumber(val, decimals = 2) {
  if (val === null || val === undefined) return '-';
  return val.toFixed(decimals);
}

/**
 * 格式化成交量（万/亿）
 */
function formatVolume(vol) {
  if (vol === null || vol === undefined) return '-';
  if (vol >= 1e8) return (vol / 1e8).toFixed(2) + '亿';
  if (vol >= 1e4) return (vol / 1e4).toFixed(2) + '万';
  return vol.toString();
}

/**
 * 输出 Markdown 格式
 */
function outputMarkdown(data, indicators) {
  const { symbol, period, adjust, klines } = data;
  
  // 基础列
  const baseCols = ['日期', '开盘', '最高', '最低', '收盘', '成交量'];
  const baseKeys = ['date', 'open', 'high', 'low', 'close', 'volume'];
  
  // 指标列
  const indCols = indicators.map(ind => ind.toUpperCase().replace('_', ' '));
  
  const allCols = [...baseCols, ...indCols];
  const allKeys = [...baseKeys, ...indicators];
  
  // 表头
  let md = `## ${symbol} K线数据\n\n`;
  md += `> 周期: ${period} | 复权: ${adjust} | 数量: ${klines.length}\n\n`;
  md += '| ' + allCols.join(' | ') + ' |\n';
  md += '|' + allCols.map(() => '------').join('|') + '|\n';
  
  // 数据行
  for (const k of klines) {
    const row = allKeys.map(key => {
      if (key === 'date') return k.date;
      if (key === 'volume') return formatVolume(k.volume);
      return formatNumber(k[key]);
    });
    md += '| ' + row.join(' | ') + ' |\n';
  }
  
  return md;
}

/**
 * 主函数
 */
async function main() {
  const args = parseArgs();
  
  // 验证必填参数
  if (!args.symbol) {
    error('缺少必填参数 --symbol，使用 --help 查看帮助');
  }
  
  // 解析指标
  const indicators = parseIndicators(args.with);
  
  // 计算预热周期（仅在没有指定 startDate 时需要）
  const warmup = args.startDate ? 0 : getWarmupPeriod(indicators);
  const fetchLimit = args.limit + warmup;
  
  try {
    // 获取历史 K 线数据
    const data = await fetchKline(args.symbol, args.period, args.adjust, fetchLimit, args.startDate);
    
    // 检查是否有更多数据
    if (data.truncated) {
      if (indicators.length > 0) {
        console.warn('提示: 指标计算可能不准确（预热数据不足），建议调整 --limit 值。');
      } else {
        console.warn('提示: 可能有更多历史数据未返回，建议调整 --limit 值。');
      }
    }
    
    // 计算指标
    if (indicators.length > 0) {
      calculateIndicators(data.klines, indicators);
    }
    
    // 截取用户请求的数量（去掉预热数据）
    if (warmup > 0 && data.klines.length > args.limit) {
      data.klines = data.klines.slice(-args.limit);
      data.count = data.klines.length;
    }
    
    // 清理 null 值和 truncated 标记
    delete data.truncated;
    for (const k of data.klines) {
      for (const key of Object.keys(k)) {
        if (k[key] === null) delete k[key];
      }
    }
    
    // 输出
    if (args.format === 'markdown') {
      console.log(outputMarkdown(data, indicators));
    } else {
      console.log(JSON.stringify(data, null, 2));
    }
    
  } catch (err) {
    error(err.message);
  }
}

main();
