/**
 * fetch-prices.mjs
 * 抓取有色金属现货/期货价格
 * 数据源：Yahoo Finance v8 API + 长江有色(CCMN) + Stooq
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..');

// ────────────────────────────────────────────
// 读取 .env
// ────────────────────────────────────────────
function loadEnv() {
  const envPath = join(PROJECT_ROOT, '.env');
  const env = {};
  try {
    const content = readFileSync(envPath, 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIdx = trimmed.indexOf('=');
      if (eqIdx === -1) continue;
      const key = trimmed.slice(0, eqIdx).trim();
      const value = trimmed.slice(eqIdx + 1).trim().replace(/^["']|["']$/g, '');
      env[key] = value;
    }
  } catch { /* ignore */ }
  return env;
}

// ────────────────────────────────────────────
// Yahoo Finance v8 API
// ────────────────────────────────────────────
async function fetchYahooPrice(symbol, name, unit, exchange) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=2d`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
      },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const result = data?.chart?.result?.[0];
    if (!result) throw new Error('No result in response');

    const meta = result.meta;
    const currentPrice = meta.regularMarketPrice;
    const prevClose = meta.chartPreviousClose ?? meta.previousClose;

    let changePct = null;
    if (prevClose && currentPrice) {
      changePct = +((currentPrice - prevClose) / prevClose * 100).toFixed(2);
    }

    return {
      name,
      price: currentPrice ?? null,
      changePct,
      unit,
      exchange,
      source: 'Yahoo Finance',
      ccmnPrice: null,
      ccmnUpdown: null,
    };
  } catch (err) {
    process.stderr.write(`[fetch-prices] Yahoo Finance ${symbol} error: ${err.message}\n`);
    return {
      name,
      price: null,
      changePct: null,
      unit,
      exchange,
      source: 'Yahoo Finance',
      ccmnPrice: null,
      ccmnUpdown: null,
    };
  }
}

// ────────────────────────────────────────────
// Stooq CSV API（镍 NI.F 等，备用）
// 价格单位：美分/磅（cents/lb），需转换为 USD/t
// ────────────────────────────────────────────
async function fetchStooqPrice(symbol, name, unit, exchange) {
  const url = `https://stooq.com/q/l/?s=${encodeURIComponent(symbol)}&f=sd2t2ohlcv&h&e=csv`;
  try {
    const res = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0' },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();
    const lines = text.trim().split('\n');
    if (lines.length < 2) throw new Error('Empty CSV');
    const headers = lines[0].split(',').map(h => h.trim());
    const values = lines[1].split(',').map(v => v.trim());

    const obj = {};
    headers.forEach((h, i) => { obj[h] = values[i]; });

    if (obj['Close'] === 'N/D' || !obj['Close']) throw new Error('No data (N/D)');

    const rawPrice = parseFloat(obj['Close']);
    if (isNaN(rawPrice)) throw new Error('Invalid price');

    let price = rawPrice;
    if (unit === 'USD/t') {
      price = +(rawPrice / 100 * 2204.62).toFixed(2);
    }

    return {
      name,
      price,
      changePct: null,
      unit,
      exchange,
      source: 'Stooq',
      ccmnPrice: null,
      ccmnUpdown: null,
    };
  } catch (err) {
    process.stderr.write(`[fetch-prices] Stooq ${symbol} error: ${err.message}\n`);
    return {
      name,
      price: null,
      changePct: null,
      unit,
      exchange,
      source: 'Stooq',
      ccmnPrice: null,
      ccmnUpdown: null,
    };
  }
}

// ────────────────────────────────────────────
// 长江有色 CCMN API
// 提供 Cu/Zn/Ni/Co 人民币现货价 + 涨跌额
// ────────────────────────────────────────────
async function fetchCcmnPrices() {
  const url = 'https://m.ccmn.cn/mhangqing/getCorpStmarketPriceList?marketVmid=40288092327140f601327141c0560001';
  try {
    const res = await fetch(url, {
      headers: {
        'Referer': 'https://m.ccmn.cn/mhangqing/mcjxh/',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      },
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data.success) throw new Error(data.msg || 'API error');

    const list = data.body?.priceList;
    if (!Array.isArray(list)) throw new Error('No priceList in response');

    // productSortName -> key 映射
    const nameMap = {
      '1#铜': 'copper',
      '0#锌': 'zinc',
      '1#镍': 'nickel',
      '1#钴': 'cobalt',
    };

    const result = { copper: null, zinc: null, nickel: null, cobalt: null };

    for (const item of list) {
      const key = nameMap[item.productSortName];
      if (key) {
        const price = parseFloat(item.avgPrice);
        const updown = parseFloat(item.highsLowsAmount);
        result[key] = {
          price: isNaN(price) ? null : price,
          updown: isNaN(updown) ? null : updown,
        };
      }
    }

    return result;
  } catch (err) {
    process.stderr.write(`[fetch-prices] CCMN API error: ${err.message}\n`);
    return null;
  }
}

// ────────────────────────────────────────────
// 主函数
// ────────────────────────────────────────────
async function main() {
  // 1. 并行：Yahoo Finance (Cu/Zn USD) + CCMN (Cu/Zn/Ni/Co CNY)
  const [copperRaw, zincRaw, ccmn] = await Promise.all([
    fetchYahooPrice('HG=F', '铜', 'USD/lb', 'COMEX'),
    fetchYahooPrice('ZNC=F', '锌', 'USD/t',  'LME'),
    fetchCcmnPrices(),
  ]);

  // 2. Cu：Yahoo Finance 为主，CCMN 补充人民币数据
  const copper = {
    ...copperRaw,
    ccmnPrice: ccmn?.copper?.price ?? null,
    ccmnUpdown: ccmn?.copper?.updown ?? null,
  };

  // 3. Zn：Yahoo Finance 为主，CCMN 补充人民币数据
  const zinc = {
    ...zincRaw,
    ccmnPrice: ccmn?.zinc?.price ?? null,
    ccmnUpdown: ccmn?.zinc?.updown ?? null,
  };

  // 4. Ni：优先 CCMN（有涨跌数据），Stooq 作备用
  let nickel;
  if (ccmn?.nickel?.price != null) {
    nickel = {
      name: '镍',
      price: null,
      changePct: null,
      unit: 'CNY/t',
      exchange: '長江現貨',
      source: 'ccmn',
      ccmnPrice: ccmn.nickel.price,
      ccmnUpdown: ccmn.nickel.updown,
    };
  } else {
    process.stderr.write('[fetch-prices] CCMN 镍数据不可用，回退到 Stooq\n');
    const stooqNi = await fetchStooqPrice('NI.F', '镍', 'USD/t', 'LME');
    nickel = {
      ...stooqNi,
      ccmnPrice: null,
      ccmnUpdown: null,
    };
  }

  // 5. Co：优先 CCMN（唯一免费来源），失败则 null
  const cobalt = {
    name: '钴',
    price: null,
    changePct: null,
    unit: 'CNY/t',
    exchange: '長江現貨',
    source: ccmn?.cobalt?.price != null ? 'ccmn' : 'none',
    ccmnPrice: ccmn?.cobalt?.price ?? null,
    ccmnUpdown: ccmn?.cobalt?.updown ?? null,
  };

  // 6. Bi：暂无免费数据源
  const bismuth = {
    name: '铋',
    price: null,
    changePct: null,
    unit: 'USD/t',
    exchange: 'N/A',
    source: 'none',
    ccmnPrice: null,
    ccmnUpdown: null,
  };

  const results = [copper, zinc, nickel, cobalt, bismuth];
  console.log(JSON.stringify(results));
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
