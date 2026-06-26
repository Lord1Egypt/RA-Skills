/**
 * fetch-all-data.mjs
 * 收集所有有色金屬原始數據，輸出完整 JSON 到 stdout
 * 目標：≤15 秒完成
 *
 * 輸出結構：
 * { date, dataDate, isMarketOpen, marketNote, changeNote, bismuthNote, prices, forwards, inventory, news, ibNews, forumSentiment }
 *
 * v4 新增：
 * - fetchSmmNews(): SMM上海有色網新聞（免費，HTTP可達）
 * - fetchRedditCommodities(): Reddit r/Commodities 最新帖子
 * - forumSentiment: { redditSummary, smmHighlights } 市場情緒字段
 */

// ────────────────────────────────────────────
// 工具函數
// ────────────────────────────────────────────

function today() {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Shanghai' });
}

// ────────────────────────────────────────────
// 1. CCMN 長江有色現貨（CNY）
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
      signal: AbortSignal.timeout(12000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data.success) throw new Error(data.msg || 'API error');

    const list = data.body?.priceList;
    if (!Array.isArray(list)) throw new Error('No priceList');

    const nameMap = {
      '1#铜': 'copper',
      '0#锌': 'zinc',
      '1#镍': 'nickel',
      '1#钴': 'cobalt',
      'A00铝': 'aluminum',  // v8 新增：嘗試從 CCMN 獲取鋁價
      '1#铝': 'aluminum',   // 備用牌號
      '1#镁': 'magnesium',  // v12 新增：鎂
    };

    // 升級一：提取 dataDate 與 isMarketOpen
    const rawDate = list[0]?.publishDate ?? null;
    // publishDate 可能是 "2026-03-13" 或 "2026/03/13"，統一轉為 "YYYY-MM-DD"
    const dataDate = rawDate ? rawDate.replace(/\//g, '-').slice(0, 10) : null;
    const todaySH = today();
    const isMarketOpen = dataDate ? (dataDate === todaySH) : null;

    const result = { copper: null, zinc: null, nickel: null, cobalt: null, aluminum: null, magnesium: null, dataDate, isMarketOpen };
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
    process.stderr.write(`[fetch-all-data] CCMN 錯誤: ${err.message}\n`);
    return null;
  }
}

// ────────────────────────────────────────────
// 1b. OmetalCN 長江現貨（GBK 頁面，備用源）
// URL: http://app.ometal.cn/data/mlist.asp
// 品種：Cu / Al / Pb / Zn / Ni / Sn + 升貼水
// 優勢：有 A00鋁（CCMN 常缺）、解析穩定、響應快
// ────────────────────────────────────────────

async function fetchOmetal() {
  try {
    const res = await fetch('http://app.ometal.cn/data/mlist.asp', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'http://app.ometal.cn/',
      },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buf = await res.arrayBuffer();
    const text = new TextDecoder('gbk').decode(buf);

    // 提取純文字（去除HTML標籤）
    const plain = text.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');

    // 解析價格表格：格式為「品名 高-低 均價 ↑↓變動 更多」
    function parseRow(name) {
      // 匹配：品名後面跟數字區間、均價、漲跌
      const re = new RegExp(
        name.replace(/[#()]/g, c => '\\' + c) +
        '\\s+([\\d,]+-[\\d,-]+)\\s+([\\d,]+)\\s+[↑↓]([\\-\\d,]+)'
      );
      const m = plain.match(re);
      if (!m) return null;
      const range = m[1].split('-');
      const avg = parseFloat(m[2].replace(/,/g, ''));
      const change = parseFloat(m[3].replace(/,/g, ''));
      // range: 有時是「22850-22950」也有負數「-130--90」
      let low = null, high = null;
      if (range.length === 2) {
        low  = parseFloat(range[0].replace(/,/g, ''));
        high = parseFloat(range[1].replace(/,/g, ''));
      }
      if (isNaN(avg)) return null;
      return { price: avg, high: isNaN(high) ? null : high, low: isNaN(low) ? null : low, change: isNaN(change) ? null : change };
    }

    // 提取日期（格式：日期: 3/26）
    const dateMatch = plain.match(/日期[：:]\s*(\d+)\/(\d+)/);
    let dataDate = null;
    if (dateMatch) {
      const year = new Date().getFullYear();
      dataDate = `${year}-${String(parseInt(dateMatch[1])).padStart(2,'0')}-${String(parseInt(dateMatch[2])).padStart(2,'0')}`;
    }

    const result = {
      copper:          parseRow('1#铜'),
      aluminum:        parseRow('A00铝'),
      lead:            parseRow('1#铅'),
      zinc:            parseRow('0#锌'),
      nickel:          parseRow('1#镍板'),
      tin:             parseRow('1#锡'),
      copperPremium:   parseRow('铜升贴水'),
      aluminumPremium: parseRow('铝升贴水'),
      dataDate,
      source: 'OmetalCN/app.ometal.cn',
    };

    process.stderr.write(
      `[fetch-all-data] OmetalCN: Cu=¥${result.copper?.price} Al=¥${result.aluminum?.price} Zn=¥${result.zinc?.price} Ni=¥${result.nickel?.price} Sn=¥${result.tin?.price}\n`
    );
    return result;
  } catch (err) {
    process.stderr.write(`[fetch-all-data] OmetalCN 失敗: ${err.message}\n`);
    return null;
  }
}

// ────────────────────────────────────────────
// 2. Yahoo Finance v8（USD 現貨 / 遠期合約）
// ────────────────────────────────────────────

async function fetchYahoo(symbol) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=2d`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
      },
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const result = data?.chart?.result?.[0];
    if (!result) throw new Error('No result');

    const meta = result.meta;
    const price = meta.regularMarketPrice ?? null;
    const prevClose = meta.chartPreviousClose ?? meta.previousClose ?? null;
    let changePct = null;
    if (price != null && prevClose != null) {
      changePct = +((price - prevClose) / prevClose * 100).toFixed(2);
    }

    // 驗證數據是否過期（超過 30 天視為無效）
    const tradingDate = new Date(meta.regularMarketTime * 1000).toISOString().slice(0, 10);
    const daysDiff = (Date.now() - meta.regularMarketTime * 1000) / 86400000;
    if (daysDiff > 30) {
      return { symbol, ok: false, price: null, changePct: null, expiry: null, error: `Stale data: last traded ${tradingDate} (${Math.floor(daysDiff)}d ago)` };
    }

    // 合約到期月份（從 symbol 推算）
    let expiry = null;
    if (symbol !== 'HG=F' && symbol !== 'ZNC=F' && symbol !== 'ALI=F') {
      const m = symbol.match(/HG([FGHJKMNQUVXZ])(\d{2})\.CMX/);
      if (m) {
        const monthCodeMap = { F:1,G:2,H:3,J:4,K:5,M:6,N:7,Q:8,U:9,V:10,X:11,Z:12 };
        const mNum = String(monthCodeMap[m[1]]).padStart(2, '0');
        const yr = 2000 + parseInt(m[2]);
        expiry = `${yr}-${mNum}`;
      }
    } else {
      // 現貨合約用當前月份
      const now = new Date();
      expiry = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}`;
    }

    return { symbol, ok: true, price, changePct, expiry };
  } catch (err) {
    process.stderr.write(`[fetch-all-data] Yahoo ${symbol} 錯誤: ${err.message}\n`);
    return { symbol, ok: false, price: null, changePct: null, expiry: null };
  }
}

// 周环比（较约5个交易日前收盘）
async function fetchYahooWoW(symbol) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=1mo`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
      },
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const result = data?.chart?.result?.[0];
    const closes = result?.indicators?.quote?.[0]?.close?.filter(v => v != null) || [];
    if (closes.length < 6) return null;
    const last = closes[closes.length - 1];
    const prevWeek = closes[closes.length - 6]; // 约5个交易日前
    if (last == null || prevWeek == null || prevWeek === 0) return null;
    return +(((last - prevWeek) / prevWeek) * 100).toFixed(2);
  } catch (err) {
    process.stderr.write(`[fetch-all-data] Yahoo WoW ${symbol} 錯誤: ${err.message}\n`);
    return null;
  }
}

// USD/CNY 匯率（Yahoo Finance + 備援）
async function fetchUsdcny() {
  // A) Yahoo（主來源）
  const fx = await fetchYahoo('USDCNY=X');
  if (fx.ok && fx.price != null) {
    return { price: fx.price, changePct: fx.changePct, source: 'Yahoo/USDCNY=X' };
  }

  // B) exchangerate.host（免費備援）
  try {
    const res = await fetch('https://api.exchangerate.host/convert?from=USD&to=CNY&amount=1', {
      headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' },
      signal: AbortSignal.timeout(8000),
    });
    if (res.ok) {
      const data = await res.json();
      const p = Number(data?.result ?? data?.info?.rate);
      if (Number.isFinite(p) && p > 0) {
        return { price: +p.toFixed(4), changePct: null, source: 'exchangerate.host' };
      }
    }
  } catch (err) {
    process.stderr.write(`[fetch-all-data] FX 備援 exchangerate.host 錯誤: ${err.message}\n`);
  }

  // C) frankfurter.app（免費備援）
  try {
    const res = await fetch('https://api.frankfurter.app/latest?from=USD&to=CNY', {
      headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' },
      signal: AbortSignal.timeout(8000),
    });
    if (res.ok) {
      const data = await res.json();
      const p = Number(data?.rates?.CNY);
      if (Number.isFinite(p) && p > 0) {
        return { price: +p.toFixed(4), changePct: null, source: 'frankfurter.app' };
      }
    }
  } catch (err) {
    process.stderr.write(`[fetch-all-data] FX 備援 frankfurter.app 錯誤: ${err.message}\n`);
  }

  return null;
}

// ────────────────────────────────────────────
// v7 新增：有色金屬行業指數（Yahoo Finance）
// 測試結果（2026-03-15）：
//   ^LMEX ⚠️ 過舊（2019）| JJM ⚠️ 過舊（2023）
//   XME ✅ | COPX ✅ | PICK ✅ | 000812.SS ✅
//   512400 ❌404 | 159163 ❌404
// 選定：XME（廣泛礦業） + COPX（銅礦股） + 000812.SS（申萬A股）
// ────────────────────────────────────────────

async function fetchMetalIndices() {
  const symbols = [
    { symbol: 'XME',       name: 'SPDR S&P Metals & Mining ETF',   market: 'US', currency: 'USD' },
    { symbol: 'COPX',      name: 'Global X Copper Miners ETF',      market: 'US', currency: 'USD' },
    { symbol: '000812.SS', name: '申萬有色金屬指數',                 market: 'CN', currency: 'CNY' },
  ];

  const results = await Promise.all(symbols.map(async ({ symbol, name, market, currency }) => {
    const [data, wowPct] = await Promise.all([
      fetchYahoo(symbol),
      fetchYahooWoW(symbol),
    ]);
    if (!data.ok || data.price === null) return null;
    const changeAbs = (data.price != null && data.changePct != null)
      ? +(data.price * data.changePct / (100 + data.changePct)).toFixed(3)
      : null;
    return {
      symbol,
      name,
      market,
      currency,
      price: data.price,
      changePct: data.changePct,
      changeAbs,
      wowPct,
    };
  }));

  return results.filter(Boolean);
}

// 宏觀風險指標：DXY / VIX / CRB / 美債10Y
async function fetchMacroIndicators() {
  const symbols = [
    { symbol: '^DXY', name: '美元指數', unit: 'pts' },
    { symbol: '^VIX', name: 'VIX恐慌指數', unit: 'pts' },
    { symbol: 'CRY',  name: 'CRB商品指數', unit: 'pts' },
    { symbol: '^TNX', name: '美債10Y收益率', unit: '%' },
  ];

  const results = await Promise.all(symbols.map(async (cfg) => {
    let data = await fetchYahoo(cfg.symbol);
    if ((!data.ok || data.price == null) && cfg.symbol === 'CRY') {
      // CRB 指數備用 symbol：TRJEFFCR
      data = await fetchYahoo('TRJEFFCR');
      cfg = { ...cfg, symbol: 'TRJEFFCR' };
    }
    if ((!data.ok || data.price == null) && cfg.symbol === '^DXY') {
      // DXY 備用 symbol：DX-Y.NYB
      data = await fetchYahoo('DX-Y.NYB');
      cfg = { ...cfg, symbol: 'DX-Y.NYB' };
    }
    if (!data.ok || data.price == null) return null;
    // ^TNX 報價通常為收益率×10（若>20則縮放），否則直接使用
    const rawPrice = data.price;
    const price = cfg.symbol === '^TNX' && rawPrice > 20 ? +(rawPrice / 10).toFixed(3) : rawPrice;
    return {
      ...cfg,
      price,
      changePct: data.changePct,
      source: 'Yahoo',
    };
  }));

  return results.filter(Boolean);
}

// ────────────────────────────────────────────
// 3. 鉍（Bi）— SMM 上海有色網 h5 頁面（免費，__NEXT_DATA__ 嵌入）
// ────────────────────────────────────────────
// URL: https://hq.smm.cn/h5/bismuth-price
// 數據：精鉍價格(CNY/t) + 精鉍CIF(USD/kg) + 4N/5N三氧化二鉍(CNY/t)
// 欄位：high / low / average / vchange(日變動絕對值) / vchange_rate(%) / renew_date
// 無需登錄，__NEXT_DATA__ 直接嵌入完整 JSON
// ────────────────────────────────────────────

async function fetchSmmBismuth() {
  try {
    const res = await fetch('https://hq.smm.cn/h5/bismuth-price', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.smm.cn/',
      },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();

    // 解析 __NEXT_DATA__
    const nd = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/);
    if (!nd) throw new Error('__NEXT_DATA__ not found');
    const json = JSON.parse(nd[1]);

    const sections = json?.props?.pageProps?.datas?.BIP01?.data;
    if (!Array.isArray(sections)) throw new Error('BIP01 data not found');

    const result = { cny: null, usd: null, source: 'SMM/hq.smm.cn' };

    for (const section of sections) {
      for (const item of (section.data || [])) {
        const name = item.product_name || '';
        // 铋 = U+94CB
        // 精铋价格 (CNY/t)：name 含「铋」且不含 CIF，unit 含「元」
        // ⚠️ SMM vchange_rate 為小數格式（如 -0.0033 = -0.33%），需 ×100 轉為百分比
        if (name.includes('\u94cb') && !name.includes('CIF') && item.unit && item.unit.includes('\u5143') && !name.includes('N\u4e09')) {
          result.cny = {
            average: item.average,
            high: item.high,
            low: item.low,
            change: item.vchange,
            changePct: item.vchange_rate != null ? +(item.vchange_rate * 100).toFixed(4) : null,
            unit: item.unit,
            dataDate: item.renew_date,
          };
        } else if (name.includes('\u94cb') && name.includes('CIF')) {
          // 精铋CIF价格 (USD/kg → 換算 USD/t)
          const avgUsdPerKg = item.average;
          result.usd = {
            averagePerKg: avgUsdPerKg,
            average: avgUsdPerKg != null ? +(avgUsdPerKg * 1000).toFixed(0) : null, // USD/t
            high: item.high != null ? item.high * 1000 : null,
            low: item.low != null ? item.low * 1000 : null,
            change: item.vchange != null ? +(item.vchange * 1000).toFixed(0) : null,
            changePct: item.vchange_rate != null ? +(item.vchange_rate * 100).toFixed(4) : null,
            unit: 'USD/t',
            dataDate: item.renew_date,
          };
        }
      }
    }

    if (!result.cny && !result.usd) throw new Error('No bismuth prices found in page');

    const cnyAvg = result.cny?.average;
    const usdAvg = result.usd?.average;
    process.stderr.write(`[fetch-all-data] SMM 鉍價格：¥${cnyAvg}/t（日變動 ${result.cny?.change}）/ $${usdAvg}/t CIF\n`);
    return result;
  } catch (err) {
    process.stderr.write(`[fetch-all-data] SMM 鉍抓取失敗: ${err.message}\n`);
    return null;
  }
}

// ────────────────────────────────────────────
// 3b. SMM 長江現貨交叉驗證（Cu / Zn / Ni）
// ────────────────────────────────────────────
// 數據源調研結論（2026-03）：
//   ✅ cu-price: 長江現貨銅價 / ✅ zn-price: 長江現貨鋅錠 / ✅ ni-price: 長江鎳價
//   ❌ al-price: 404（鋁無 h5 頁面）/ ❌ cobalt-price/co-price: 404（鈷無 h5 頁面）
//   ❌ 所有金屬均無 LME USD 報價（Zn/Ni/Co USD 無免費數據源）
// ⚠️ vchange_rate 為小數格式，×100 轉百分比

async function fetchSmmCrossCheck() {
  const SMM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.smm.cn/',
  };

  // 遞歸提取所有含 product_name 的條目
  function walkItems(obj) {
    const items = [];
    function walk(o) {
      if (!o || typeof o !== 'object') return;
      if (o.product_name !== undefined && o.average != null) {
        items.push(o); return;
      }
      if (Array.isArray(o)) { o.forEach(walk); return; }
      Object.values(o).forEach(walk);
    }
    walk(obj);
    return items;
  }

  async function fetchSmm(slug, targetName, attempt = 1) {
    try {
      const res = await fetch(`https://hq.smm.cn/h5/${slug}`, {
        headers: SMM_HEADERS, signal: AbortSignal.timeout(12000),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const html = await res.text();
      const nd = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/);
      if (!nd) throw new Error('no __NEXT_DATA__');
      const json = JSON.parse(nd[1]);
      const items = walkItems(json?.props?.pageProps?.datas);
      const match = items.find(i => i.product_name && i.product_name.includes(targetName));
      if (!match) throw new Error(`"${targetName}" not found in ${items.length} items`);
      return {
        average: match.average,
        high: match.high,
        low: match.low,
        change: match.vchange,
        changePct: match.vchange_rate != null ? +(match.vchange_rate * 100).toFixed(4) : null,
        unit: match.unit,
        dataDate: match.renew_date,
        productName: match.product_name,
        source: `SMM/${slug}`,
      };
    } catch(err) {
      if (attempt === 1) {
        process.stderr.write(`[fetch-all-data] SMM cross-check ${slug} 第一次失敗 (${err.message})，1.5秒後重試...\n`);
        await new Promise(r => setTimeout(r, 1500));
        return fetchSmm(slug, targetName, 2);
      }
      process.stderr.write(`[fetch-all-data] SMM cross-check ${slug} 最終失敗: ${err.message}\n`);
      return null;
    }
  }

  const [cu, zn, ni] = await Promise.all([
    fetchSmm('cu-price', '\u957f\u6c5f\u73b0\u8d27\u94dc\u4ef7'),       // 长江现货铜价  铜=94DC
    fetchSmm('zn-price', '\u4e0a\u6d77\u73b0\u8d27\u950c\u952d\u4ef7\u683c0#'), // 上海现货锌锭价格0#  锌=950C 锭=952D
    fetchSmm('ni-price', '\u957f\u6c5f\u954d\u4ef7\u683c'),             // 长江镍价格  镍=954D
  ]);

  process.stderr.write(`[fetch-all-data] SMM交叉驗證: Cu=${cu?.average} Zn=${zn?.average} Ni=${ni?.average}\n`);
  return { copper: cu, zinc: zn, nickel: ni };
}

// ────────────────────────────────────────────
// 3c. 通用 fetchSmmMetal（v8 新增）
// 適用於任何有 __NEXT_DATA__ 的 SMM h5 頁面
// ────────────────────────────────────────────

async function fetchSmmMetal(slug, targetName) {
  const headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.smm.cn/',
  };
  try {
    const res = await fetch(`https://hq.smm.cn/h5/${slug}`, {
      headers, signal: AbortSignal.timeout(12000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();
    const nd = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/);
    if (!nd) throw new Error('no __NEXT_DATA__');
    const json = JSON.parse(nd[1]);

    // 展開所有 data 條目
    const items = [];
    function walk(o) {
      if (!o || typeof o !== 'object') return;
      if (o.product_name !== undefined && o.average != null) { items.push(o); return; }
      if (Array.isArray(o)) { o.forEach(walk); return; }
      Object.values(o).forEach(walk);
    }
    walk(json?.props?.pageProps?.datas);

    const match = items.find(i => i.product_name && i.product_name.includes(targetName));
    if (!match) throw new Error(`"${targetName}" not found in ${items.length} items`);

    const changePct = match.vchange_rate != null ? +(match.vchange_rate * 100).toFixed(3) : null;
    return {
      average: match.average,
      high: match.high,
      low: match.low,
      change: match.vchange,
      changePct,
      unit: match.unit,
      dataDate: match.renew_date,
      productName: match.product_name,
      source: `SMM/hq.smm.cn/${slug}`,
    };
  } catch (err) {
    process.stderr.write(`[fetch-all-data] fetchSmmMetal(${slug}) 失敗: ${err.message}\n`);
    return null;
  }
}

// 交叉驗證說明生成器
function buildCrossCheckNote(ccmnPrice, smmPrice, smmLabel) {
  if (!ccmnPrice || !smmPrice) return null;
  const diffPct = +((smmPrice - ccmnPrice) / ccmnPrice * 100).toFixed(2);
  const sign = diffPct >= 0 ? '+' : '';
  const absDiff = Math.abs(diffPct);
  if (absDiff < 0.5) return `雙源一致：CCMN ¥${ccmnPrice} vs ${smmLabel} ¥${smmPrice} (${sign}${diffPct}%)`;
  if (absDiff > 1)   return `差異>1%：CCMN ¥${ccmnPrice} vs ${smmLabel} ¥${smmPrice} (${sign}${diffPct}%)`;
  return `差異<1%：CCMN ¥${ccmnPrice} vs ${smmLabel} ¥${smmPrice} (${sign}${diffPct}%)`;
}

// ────────────────────────────────────────────
// 4a. Westmetall.com — LME 庫存 + USD 現貨價格
// ────────────────────────────────────────────
// URL: https://www.westmetall.com/en/markdaten.php?action=table&field=LME_XX_stock
// 返回: { tonnes, change, cashUsd, threeMonthUsd, dataDate }
// 覆蓋品種: Cu / Zn / Ni（Westmetall 不提供 Co 數據）
// ────────────────────────────────────────────

const WESTMETALL_MONTHS = {
  January:1, February:2, March:3, April:4, May:5, June:6,
  July:7, August:8, September:9, October:10, November:11, December:12
};

function parseWestmetallDate(str) {
  const m = str.match(/(\d{1,2})\.\s+(\w+)\s+(\d{4})/);
  if (!m) return null;
  const d = String(parseInt(m[1])).padStart(2, '0');
  const mon = String(WESTMETALL_MONTHS[m[2]] || 0).padStart(2, '0');
  return `${m[3]}-${mon}-${d}`;
}

async function fetchWestmetallMetal(fieldName, attempt = 1) {
  // fieldName: 'LME_Cu_stock' | 'LME_Zn_stock' | 'LME_Ni_stock'
  const url = `https://www.westmetall.com/en/markdaten.php?action=table&field=${fieldName}`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'https://www.westmetall.com/en/markdaten.php',
      },
      signal: AbortSignal.timeout(15000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();

    // 取 <tbody> 第一個 <tr>（最新一行）
    const tbodyMatch = html.match(/<tbody>([\s\S]*?)<\/tbody>/);
    if (!tbodyMatch) throw new Error('No <tbody> found');
    const tbody = tbodyMatch[1];
    const trMatch = tbody.match(/<tr>([\s\S]*?)<\/tr>/);
    if (!trMatch) throw new Error('No <tr> in tbody');
    const tr = trMatch[1];

    // 提取所有 <td> 文本
    const tdValues = [...tr.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)]
      .map(m => m[1].replace(/<[^>]+>/g, '').trim());

    if (tdValues.length < 4) throw new Error(`Expected ≥4 td, got ${tdValues.length}`);

    const [dateStr, stockStr, cashStr, threeMonthStr] = tdValues;
    const dataDate = parseWestmetallDate(dateStr);

    // 解析下一行的庫存變化
    const rows = [...tbody.matchAll(/<tr>([\s\S]*?)<\/tr>/g)];
    let change = null;
    if (rows.length >= 2) {
      const prevTd = [...rows[1][1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)]
        .map(m => m[1].replace(/<[^>]+>/g, '').trim());
      if (prevTd.length >= 2) {
        const curr = parseFloat(stockStr.replace(/,/g, ''));
        const prev = parseFloat(prevTd[1].replace(/,/g, ''));
        if (!isNaN(curr) && !isNaN(prev)) change = curr - prev;
      }
    }

    return {
      tonnes: parseFloat(stockStr.replace(/,/g, '')) || null,
      change,
      cashUsd: parseFloat(cashStr.replace(/,/g, '')) || null,
      threeMonthUsd: parseFloat(threeMonthStr.replace(/,/g, '')) || null,
      dataDate,
      source: `Westmetall/${fieldName}`,
    };
  } catch (err) {
    if (attempt === 1) {
      process.stderr.write(`[fetch-all-data] Westmetall ${fieldName} 第一次失敗 (${err.message})，2秒後重試...\n`);
      await new Promise(r => setTimeout(r, 2000));
      return fetchWestmetallMetal(fieldName, 2);
    }
    process.stderr.write(`[fetch-all-data] Westmetall ${fieldName} 最終失敗: ${err.message}\n`);
    return null;
  }
}

async function fetchWestmetallAll() {
  const [cu, zn, ni] = await Promise.all([
    fetchWestmetallMetal('LME_Cu_stock'),
    fetchWestmetallMetal('LME_Zn_stock'),
    fetchWestmetallMetal('LME_Ni_stock'),
  ]);
  process.stderr.write(`[fetch-all-data] Westmetall: Cu=${cu?.cashUsd} Zn=${zn?.cashUsd} Ni=${ni?.cashUsd} | stocks: Cu=${cu?.tonnes} Zn=${zn?.tonnes} Ni=${ni?.tonnes}\n`);
  return { copper: cu, zinc: zn, nickel: ni };
}

// ────────────────────────────────────────────
// 4. LME 庫存（主函數 — 優先用 Westmetall）
// ────────────────────────────────────────────

async function fetchLmeInventory() {
  const errors = [];

  // 方案A：Westmetall.com（Cu/Zn/Ni LME 庫存，可靠免費源）
  // 同時緩存 cashUsd 供 main() 直接使用，避免重複請求
  try {
    const wm = await fetchWestmetallAll();
    const result = { copper: null, zinc: null, nickel: null, cobalt: null, note: null, _wmPrices: wm };
    for (const [metal, data] of [['copper', wm.copper], ['zinc', wm.zinc], ['nickel', wm.nickel]]) {
      if (data && data.tonnes != null) {
        result[metal] = {
          tonnes: data.tonnes,
          change: data.change,
          cashUsd: data.cashUsd,
          source: data.source,
          unit: 'tonnes',
          dataDate: data.dataDate,
        };
      }
    }
    const hasData = Object.entries(result).some(([k, v]) => k !== 'note' && k !== 'cobalt' && k !== '_wmPrices' && v != null);
    if (!hasData) throw new Error('Westmetall 返回空數據');
    process.stderr.write('[fetch-all-data] LME 方案A (Westmetall) 成功\n');
    return result;
  } catch (err) {
    errors.push(`方案A: ${err.message}`);
    process.stderr.write(`[fetch-all-data] LME 方案A (Westmetall) 失敗: ${err.message}\n`);
  }

  // 方案B：LME 倉庫統計頁面 HTML
  try {
    const res = await fetch(
      'https://www.lme.com/Market-Data/Reports-and-data/Warehouse-Stock-Statistics',
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Accept': 'text/html,application/xhtml+xml',
        },
        signal: AbortSignal.timeout(5000),
      }
    );
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();
    if (html.includes('Just a moment') || html.includes('Cloudflare')) throw new Error('Cloudflare 攔截');

    const result = { copper: null, zinc: null, nickel: null, cobalt: null, note: null };
    const metalPatterns = [
      { key: 'copper', regex: /[Cc]opper[^0-9]*?([\d,]+)\s*tonnes?/i },
      { key: 'nickel', regex: /[Nn]ickel[^0-9]*?([\d,]+)\s*tonnes?/i },
      { key: 'zinc',   regex: /[Zz]inc[^0-9]*?([\d,]+)\s*tonnes?/i },
    ];
    for (const { key, regex } of metalPatterns) {
      const m = html.match(regex);
      if (m) {
        const tonnes = parseInt(m[1].replace(/,/g, ''), 10);
        if (!isNaN(tonnes)) {
          result[key] = { tonnes, change: null, source: 'LME', unit: 'tonnes' };
        }
      }
    }
    const hasData = Object.values(result).some(v => v && v.tonnes != null);
    if (!hasData) throw new Error('頁面無可解析數據');
    process.stderr.write('[fetch-all-data] LME 方案B 成功\n');
    return result;
  } catch (err) {
    errors.push(`方案B: ${err.message}`);
    process.stderr.write(`[fetch-all-data] LME 方案B 失敗: ${err.message}\n`);
  }

  // 方案C：Investing.com metals data
  try {
    const res = await fetch(
      'https://api.investing.com/api/financialdata/assets/equitiesByType?country=&type=metals&page=0&pageSize=20',
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Accept': 'application/json',
          'domain-id': 'www',
        },
        signal: AbortSignal.timeout(10000),
      }
    );
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data) throw new Error('Empty response');
    // Investing.com 不提供庫存數據，此方案會失敗
    throw new Error('Investing.com 不提供 LME 庫存數據');
  } catch (err) {
    errors.push(`方案C: ${err.message}`);
    process.stderr.write(`[fetch-all-data] LME 方案C 失敗: ${err.message}\n`);
  }

  // 所有方案失敗
  const note = `LME 庫存獲取失敗: ${errors.join(' | ')}`;
  process.stderr.write(`[fetch-all-data] 所有 LME 方案失敗，返回 null\n`);
  return {
    copper: null,
    zinc: null,
    nickel: null,
    cobalt: null,
    note,
  };
}

// ────────────────────────────────────────────
// 5. Google News RSS 新聞
// ────────────────────────────────────────────

function parseRssItems(xml) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
  let match;
  while ((match = itemRegex.exec(xml)) !== null) {
    const block = match[1];
    const titleMatch = block.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) ||
                       block.match(/<title>([\s\S]*?)<\/title>/);
    const linkMatch = block.match(/<link>([\s\S]*?)<\/link>/) ||
                      block.match(/<guid[^>]*>(https?:\/\/[^\s<]+)<\/guid>/);
    const title = titleMatch ? titleMatch[1].trim() : '';
    const url = linkMatch ? linkMatch[1].trim() : '';
    if (title) items.push({ title, url });
  }
  return items;
}

async function fetchNews() {
  const rssUrl = 'https://news.google.com/rss/search?q=%E6%9C%89%E8%89%B2%E9%87%91%E5%B1%9E+%E4%BB%B7%E6%A0%BC&hl=zh-CN&gl=CN&ceid=CN:zh-Hans';
  try {
    const res = await fetch(rssUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; MetalPriceBot/1.0)',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
      },
      signal: AbortSignal.timeout(12000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const xml = await res.text();
    const items = parseRssItems(xml);
    return items.slice(0, 5);
  } catch (err) {
    process.stderr.write(`[fetch-all-data] 新聞抓取失敗: ${err.message}\n`);
    return [];
  }
}

// ────────────────────────────────────────────
// 6. 投行分析新聞（ibNews）
// v5: 改為基本金屬雙重過濾（投行名字 AND 基本金屬關鍵詞）
// ────────────────────────────────────────────

async function fetchIbNews() {
  const queries = [
    'Goldman+Sachs+JPMorgan+Citi+copper+nickel+zinc+outlook',
    'copper+nickel+zinc+cobalt+forecast+bank+2026',
    'base+metals+copper+nickel+Goldman+JPMorgan+forecast',
  ];

  const ibKeywords = ['Goldman', 'JPMorgan', 'Citi', 'Morgan Stanley', 'Bank of America', 'UBS', 'HSBC', 'Barclays', 'BNP', 'Deutsche'];
  const metalKeywords = ['copper', 'nickel', 'zinc', 'cobalt', 'alumin', 'base metal', 'industrial metal'];

  const allItems = [];

  for (const q of queries) {
    try {
      const url = `https://news.google.com/rss/search?q=${q}&hl=en-US&gl=US&ceid=US:en`;
      const res = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; MetalPriceBot/1.0)',
          'Accept': 'application/rss+xml, */*',
        },
        signal: AbortSignal.timeout(10000),
      });
      if (!res.ok) continue;
      const xml = await res.text();
      const items = parseRssItems(xml);

      // 雙重過濾：同時包含投行名字 AND 基本金屬關鍵詞
      const doubleFiltered = items.filter(i =>
        ibKeywords.some(k => i.title.toLowerCase().includes(k.toLowerCase())) &&
        metalKeywords.some(m => i.title.toLowerCase().includes(m.toLowerCase()))
      );

      if (doubleFiltered.length > 0) {
        process.stderr.write(`[fetch-all-data] ibNews 雙重過濾找到 ${doubleFiltered.length} 條基本金屬投行新聞 (query: ${q})\n`);
        // 合併去重
        for (const item of doubleFiltered) {
          if (!allItems.some(x => x.title === item.title)) allItems.push(item);
        }
      } else {
        process.stderr.write(`[fetch-all-data] ibNews 雙重過濾無結果 (query: ${q})，嘗試只過濾金屬關鍵詞\n`);
        // fallback：只過濾金屬關鍵詞
        const metalOnly = items.filter(i =>
          metalKeywords.some(m => i.title.toLowerCase().includes(m.toLowerCase()))
        );
        for (const item of metalOnly) {
          if (!allItems.some(x => x.title === item.title)) {
            allItems.push({ ...item, source: 'industry_news' });
          }
        }
      }
    } catch (err) {
      process.stderr.write(`[fetch-all-data] IB news fetch failed: ${err.message}\n`);
    }
  }

  if (allItems.length > 0) {
    process.stderr.write(`[fetch-all-data] ibNews 最終 ${allItems.length} 條\n`);
    return allItems.slice(0, 4);
  }
  process.stderr.write('[fetch-all-data] ibNews 未找到相關新聞\n');
  return [];
}

// ────────────────────────────────────────────
// v4 新增：7. SMM上海有色網新聞（免費公開）
// 狀態：✅ 200 OK，無需登錄即可抓取新聞標題
// ────────────────────────────────────────────

async function fetchSmmNews() {
  try {
    const res = await fetch('https://www.smm.cn/', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
      },
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();

    // 提取新聞標題（SMM 主頁快訊格式：包含日期時間和標題）
    const items = [];

    // 方式1：匹配 SMM快讯 格式
    const flashRegex = /【SMM[^】]*】([^<\n]{10,100})/g;
    let m;
    while ((m = flashRegex.exec(html)) !== null && items.length < 8) {
      const title = m[0].replace(/<[^>]+>/g, '').trim();
      if (title.length > 10) items.push({ title, source: 'SMM' });
    }

    // 方式2：匹配帶有日期的新聞標題區塊
    if (items.length < 3) {
      const titleRegex = /<a[^>]+href="https:\/\/news\.smm\.cn\/news\/[^"]+">([^<]{10,120})<\/a>/g;
      while ((m = titleRegex.exec(html)) !== null && items.length < 8) {
        const title = m[1].trim();
        if (title.length > 8 && !items.some(i => i.title === title)) {
          items.push({ title, source: 'SMM' });
        }
      }
    }

    process.stderr.write(`[fetch-all-data] SMM新聞: 提取 ${items.length} 條\n`);
    return items.slice(0, 5);
  } catch (err) {
    process.stderr.write(`[fetch-all-data] SMM新聞抓取失敗: ${err.message}\n`);
    return [];
  }
}

// ────────────────────────────────────────────
// v5 更新：8. Reddit 有色金屬相關討論
// 改為 r/Economics 搜索 copper+metals（v5測試結果：3條有效帖）
// 測試結果：r/mining(1帖), r/metallurgy(2帖), r/investing(0帖),
//           r/Economics search(3帖✅), global search(3帖但多為遊戲/藝術)
// ────────────────────────────────────────────

async function fetchRedditCommodities() {
  const metalKw = ['copper', 'nickel', 'zinc', 'cobalt', 'alumin', 'lead', 'tin',
                   'base metal', 'industrial metal', 'non-ferrous', 'lme', 'comex',
                   'mining', 'ore', 'smelter', 'refinery'];

  try {
    // 並行抓取 top（本週）和 hot（當前）
    const [topRes, hotRes] = await Promise.all([
      fetch('https://www.reddit.com/r/Commodities/top.json?t=week&limit=25', {
        headers: { 'User-Agent': 'MetalPriceBot/5.0 (non-ferrous metals research)' },
        signal: AbortSignal.timeout(8000),
      }),
      fetch('https://www.reddit.com/r/Commodities/hot.json?limit=25', {
        headers: { 'User-Agent': 'MetalPriceBot/5.0 (non-ferrous metals research)' },
        signal: AbortSignal.timeout(8000),
      }),
    ]);

    const topData = topRes.ok ? await topRes.json() : { data: { children: [] } };
    const hotData = hotRes.ok ? await hotRes.json() : { data: { children: [] } };

    const parsePosts = (data) => (data?.data?.children ?? [])
      .filter(p => p?.data?.title)
      .map(p => ({
        id: p.data.id,
        title: p.data.title,
        score: p.data.score || 0,
        url: `https://reddit.com${p.data.permalink}`,
      }));

    const topPosts = parsePosts(topData);
    const hotPosts = parsePosts(hotData);

    // 金屬關鍵詞過濾
    const isMetalRelated = (title) =>
      metalKw.some(k => title.toLowerCase().includes(k));

    const metalTop = topPosts.filter(p => isMetalRelated(p.title));
    const metalHot = hotPosts.filter(p => isMetalRelated(p.title));

    // 找出異動帖（在 hot 榜但不在 top 榜的 id）
    const topIds = new Set(topPosts.map(p => p.id));
    const surgingPosts = metalHot.filter(p => !topIds.has(p.id));

    // 組合輸出：金屬相關 top + 異動帖
    const combined = [
      ...metalTop.slice(0, 4).map(p => ({ ...p, tag: 'top' })),
      ...surgingPosts.slice(0, 2).map(p => ({ ...p, tag: 'surging' })),
    ];

    // 如果完全沒有金屬相關帖子，返回前3條 top 帖（帶 tag: 'general'）供參考
    const result = combined.length > 0
      ? combined
      : topPosts.slice(0, 3).map(p => ({ ...p, tag: 'general_commodities' }));

    const metalCount = metalTop.length + surgingPosts.length;
    process.stderr.write(`[fetch-all-data] Reddit r/Commodities: top=${topPosts.length}帖, hot=${hotPosts.length}帖, 金屬相關=${metalCount}帖, 異動=${surgingPosts.length}帖\n`);
    return result;
  } catch (err) {
    process.stderr.write(`[fetch-all-data] Reddit抓取失敗: ${err.message}\n`);
    return [];
  }
}

// ────────────────────────────────────────────
// v4 新增：9. 合成 forumSentiment 字段
// ────────────────────────────────────────────

function buildForumSentiment(smmItems, redditItems) {
  let smmHighlights = null;
  if (smmItems.length > 0) {
    smmHighlights = smmItems.map(i => i.title).join(' | ');
  }

  let redditSummary = null;
  let redditSurging = null;
  if (redditItems.length > 0) {
    const topItems = redditItems.filter(p => p.tag === 'top' || p.tag === 'general_commodities');
    const surgingItems = redditItems.filter(p => p.tag === 'surging');

    if (topItems.length > 0) {
      redditSummary = topItems.map(i => `[${i.score}↑] ${i.title}`).join(' | ');
    }
    if (surgingItems.length > 0) {
      redditSurging = surgingItems.map(i => `[異動🔥] ${i.title}`).join(' | ');
    }
  }

  return {
    smmHighlights,
    redditSummary,    // 金屬相關 top 帖
    redditSurging,    // 異動帖（hot but not top）
    xueqiuSummary: null,
    fetchedAt: new Date().toISOString(),
  };
}

// ────────────────────────────────────────────
// 3d. 鈷（Co）USD 現貨價格
// 主源：tradingeconomics.com（meta description 嵌入，穩定可靠）
// 備用：dailymetalprice.com（JSON 數組，USD/lb → USD/t）
// 測試日期：2026-03-17
// ────────────────────────────────────────────

async function fetchCobaltUsd() {
  // === 方案A：tradingeconomics.com meta description ===
  // 格式："Cobalt traded flat at 56,290 USD/T on March 12, 2026."
  try {
    const res = await fetch('https://tradingeconomics.com/commodity/cobalt', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
      },
      signal: AbortSignal.timeout(12000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();

    const metaDesc = html.match(/<meta[^>]+name="description"[^>]+content="([^"]+)"/);
    if (!metaDesc) throw new Error('meta description not found');

    const priceMatch = metaDesc[1].match(/at\s+([\d,]+)\s*USD\/T/i);
    if (!priceMatch) throw new Error(`price pattern not found in: ${metaDesc[1].slice(0, 80)}`);

    const price = parseFloat(priceMatch[1].replace(/,/g, ''));
    if (isNaN(price) || price <= 0) throw new Error(`invalid price: ${priceMatch[1]}`);

    // 提取日期
    const dateMatch = metaDesc[1].match(/on\s+(\w+)\s+(\d+),\s+(\d{4})/i);
    let dataDate = null;
    if (dateMatch) {
      const monthNames = { January:1,February:2,March:3,April:4,May:5,June:6,
                           July:7,August:8,September:9,October:10,November:11,December:12 };
      const m = monthNames[dateMatch[1]];
      if (m) {
        dataDate = `${dateMatch[3]}-${String(m).padStart(2,'0')}-${String(parseInt(dateMatch[2])).padStart(2,'0')}`;
      }
    }

    process.stderr.write(`[fetch-all-data] 鈷 USD 方案A (TradingEconomics): $${price}/t, date=${dataDate}\n`);
    return { price, unit: 'USD/t', dataDate, source: 'TradingEconomics' };
  } catch(err) {
    process.stderr.write(`[fetch-all-data] 鈷 USD 方案A (TradingEconomics) 失敗: ${err.message}\n`);
  }

  // === 方案B：dailymetalprice.com JSON array（USD/lb）===
  // 格式：data = [[timestamp_ms, price_usd_per_lb], ...]
  try {
    const res = await fetch('https://www.dailymetalprice.com/metalpricecharts.php?c=co&u=usd&d=5', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,*/*',
        'Referer': 'https://www.dailymetalprice.com/',
      },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();

    // Extract data array: [[timestamp, price], ...]
    const arrMatch = text.match(/data\s*[=:]\s*(\[\[[\s\S]*?\]\])/);
    if (!arrMatch) throw new Error('data array not found');

    const arr = JSON.parse(arrMatch[1]);
    if (!Array.isArray(arr) || arr.length === 0) throw new Error('empty data array');

    // Take the most recent entry (first = latest)
    const [ts, pricePerLb] = arr[0];
    if (typeof pricePerLb !== 'number' || pricePerLb <= 0) throw new Error(`invalid price: ${pricePerLb}`);

    // Convert USD/lb → USD/t (1 short ton = 2000 lb, but metal convention uses metric ton = 2204.623 lb)
    const pricePerTon = Math.round(pricePerLb * 2204.623);
    const dataDate = new Date(ts).toISOString().slice(0, 10);

    process.stderr.write(`[fetch-all-data] 鈷 USD 方案B (DailyMetalPrice): ${pricePerLb} USD/lb → $${pricePerTon}/t, date=${dataDate}\n`);
    return { price: pricePerTon, pricePerLb, unit: 'USD/t', dataDate, source: 'DailyMetalPrice' };
  } catch(err) {
    process.stderr.write(`[fetch-all-data] 鈷 USD 方案B (DailyMetalPrice) 失敗: ${err.message}\n`);
  }

  // === 方案C：SMM CNY ÷ USD/CNY 匯率估算 ===
  // 使用 CCMN 鈷 CNY 價格 + Yahoo Finance USD/CNY 匯率反推
  try {
    const fxRes = await fetch('https://query1.finance.yahoo.com/v8/finance/chart/USDCNY=X?interval=1d&range=2d', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
      },
      signal: AbortSignal.timeout(8000),
    });
    if (!fxRes.ok) throw new Error(`Yahoo FX HTTP ${fxRes.status}`);
    const fxData = await fxRes.json();
    const usdcny = fxData?.chart?.result?.[0]?.meta?.regularMarketPrice;
    if (!usdcny || usdcny <= 0) throw new Error(`invalid USD/CNY: ${usdcny}`);
    // Will be combined with CCMN cobalt CNY price in main()
    process.stderr.write(`[fetch-all-data] 鈷 USD 方案C 準備: USD/CNY=${usdcny}\n`);
    return { price: null, usdcny, unit: 'USD/t', source: 'SMM-CNY/FX-estimate', needsCny: true };
  } catch(err) {
    process.stderr.write(`[fetch-all-data] 鈷 USD 方案C (SMM CNY/FX) 失敗: ${err.message}\n`);
  }

  return null;
}

// ────────────────────────────────────────────
// 主函數
// ────────────────────────────────────────────

async function main() {
  const startTime = Date.now();

  // 計算遠期合約 symbol
  const now = new Date();
  const monthCodes = ['F','G','H','J','K','M','N','Q','U','V','X','Z'];
  const curr = now.getMonth(); // 0-11
  const m2 = monthCodes[(curr + 2) % 12];
  const m6 = monthCodes[(curr + 6) % 12];
  const y2 = (curr + 2 >= 12) ? (now.getFullYear() + 1) % 100 : now.getFullYear() % 100;
  const y6 = (curr + 6 >= 12) ? (now.getFullYear() + 1) % 100 : now.getFullYear() % 100;
  const sym2 = `HG${m2}${y2 < 10 ? '0'+y2 : y2}.CMX`;
  const sym6 = `HG${m6}${y6 < 10 ? '0'+y6 : y6}.CMX`;

  process.stderr.write(`[fetch-all-data] 遠期合約: 近月=${sym2}, 遠月=${sym6}\n`);

  // 並行抓取所有數據（v10: 新增 fetchCobaltUsd）
  const [
    ccmn,
    ometal,
    copperSpot,
    zincSpot,
    alumSpot,
    fwdNear,
    fwdFar,
    bismuth,
    smmCross,
    smmLead,
    smmTin,
    inventory,
    cobaltUsdData,
    news,
    ibNews,
    smmNews,
    redditPosts,
    metalIndices,
    fxRate,
    macroIndicators,
  ] = await Promise.all([
    fetchCcmnPrices(),
    fetchOmetal(),                 // v11 新增：OmetalCN 備用源（Cu/Al/Pb/Zn/Ni/Sn）
    fetchYahoo('HG=F'),
    fetchYahoo('ZNC=F'),
    fetchYahoo('ALI=F'),          // 鋁現貨 USD/t
    fetchYahoo(sym2),
    fetchYahoo(sym6),
    fetchSmmBismuth(),             // 鉍：SMM h5 __NEXT_DATA__（含 CNY + CIF USD）
    fetchSmmCrossCheck(),          // SMM 長江報價交叉驗證（Cu/Zn/Ni）
    fetchSmmMetal('pb-price', '长江现货铅锭价格'),   // 鉛 CNY
    fetchSmmMetal('sn-price', '长江锡锭价格'),       // 錫 CNY
    fetchLmeInventory(),           // Westmetall LME 庫存 + Zn/Ni USD
    fetchCobaltUsd(),              // 鈷 USD 現貨（TradingEconomics / DailyMetalPrice）
    fetchNews(),
    fetchIbNews(),
    fetchSmmNews(),
    fetchRedditCommodities(),
    fetchMetalIndices(),
    fetchUsdcny(),                 // USD/CNY 匯率（供進口盈虧、基差）
    fetchMacroIndicators(),        // 宏觀風險指標（DXY/VIX/CRB/TNX）
  ]);
  // v9: 從 inventory._wmPrices 提取 Westmetall 現貨 USD 數據（從輸出中清理內部字段）
  const westmetall = inventory?._wmPrices ?? { copper: null, zinc: null, nickel: null };
  if (inventory) delete inventory._wmPrices;

  // 升級一：dataDate / isMarketOpen / marketNote
  const dataDate = ccmn?.dataDate ?? null;
  const isMarketOpen = ccmn?.isMarketOpen ?? null;
  const todaySH = today();
  let marketNote = null;
  if (isMarketOpen === false && dataDate) {
    const displayDate = dataDate.replace(/-/g, '/');
    marketNote = `休市：數據截至 ${displayDate}（上個交易日）`;
  }

  // 組裝 prices（v8：CCMN+SMM 交叉驗證 + 鉛/錫新增 + 鋁CNY從CCMN）
  const prices = {
    copper: {
      usd: copperSpot.price,
      usdChangePct: copperSpot.changePct,   // 日環比 %（vs 前一交易日收盤）
      usdUnit: 'USD/lb',
      cny: ccmn?.copper?.price ?? smmCross?.copper?.average ?? null,
      cnyChange: ccmn?.copper?.updown ?? smmCross?.copper?.change ?? null,  // 日環比 元/噸
      // v8 交叉驗證：SMM 長江現貨銅價
      smmCny: smmCross?.copper?.average ?? null,
      crossCheckNote: buildCrossCheckNote(ccmn?.copper?.price, smmCross?.copper?.average, 'SMM長江銅'),
    },
    zinc: {
      // v9: 從 Westmetall LME Cash-Settlement 獲取 USD 現貨
      usd: westmetall?.zinc?.cashUsd ?? null,
      usdChangePct: null,  // Westmetall 不提供日漲跌%，保持 null
      usdUnit: 'USD/t',
      cny: ccmn?.zinc?.price ?? smmCross?.zinc?.average ?? null,
      cnyChange: ccmn?.zinc?.updown ?? smmCross?.zinc?.change ?? null,
      // v8 交叉驗證：SMM 上海現貨0#鋅（與 CCMN 廣東市場報價較接近）
      smmCny: smmCross?.zinc?.average ?? null,
      crossCheckNote: buildCrossCheckNote(ccmn?.zinc?.price, smmCross?.zinc?.average, 'SMM上海0#鋅'),
    },
    aluminum: {
      usd: alumSpot.ok ? alumSpot.price : null,
      usdChangePct: alumSpot.ok ? alumSpot.changePct : null,
      usdUnit: 'USD/t',
      // v11: 優先 CCMN A00鋁 → 備用 OmetalCN A00鋁（SMM 無鋁 h5 頁面）
      cny: ccmn?.aluminum?.price ?? ometal?.aluminum?.price ?? null,
      cnyChange: ccmn?.aluminum?.updown ?? ometal?.aluminum?.change ?? null,
      cnySource: ccmn?.aluminum?.price != null ? 'CCMN' : (ometal?.aluminum?.price != null ? 'OmetalCN' : null),
    },
    nickel: {
      // v9: 從 Westmetall LME Cash-Settlement 獲取 USD 現貨
      usd: westmetall?.nickel?.cashUsd ?? null,
      usdChangePct: null,  // Westmetall 不提供日漲跌%，保持 null
      usdUnit: 'USD/t',
      cny: ccmn?.nickel?.price ?? smmCross?.nickel?.average ?? null,
      cnyChange: ccmn?.nickel?.updown ?? smmCross?.nickel?.change ?? null,
      // v8 交叉驗證：SMM 長江鎳價格（電解鎳）
      smmCny: smmCross?.nickel?.average ?? null,
      crossCheckNote: buildCrossCheckNote(ccmn?.nickel?.price, smmCross?.nickel?.average, 'SMM電解鎳'),
    },
    cobalt: (() => {
      // v10: 解析 fetchCobaltUsd() 返回值
      let cobaltUsd = null;
      let cobaltUsdSource = null;
      let cobaltUsdDate = null;
      if (cobaltUsdData) {
        if (cobaltUsdData.needsCny && cobaltUsdData.usdcny) {
          // 方案C：SMM CNY ÷ FX 估算
          const cnyCobalt = ccmn?.cobalt?.price;
          if (cnyCobalt && cnyCobalt > 0) {
            cobaltUsd = Math.round(cnyCobalt / cobaltUsdData.usdcny);
            cobaltUsdSource = 'SMM-CNY/FX-estimate';
          }
        } else if (cobaltUsdData.price) {
          cobaltUsd = cobaltUsdData.price;
          cobaltUsdSource = cobaltUsdData.source;
          cobaltUsdDate = cobaltUsdData.dataDate;
        }
      }
      return {
        usd: cobaltUsd,
        usdChangePct: null,
        usdUnit: 'USD/t',
        usdDataDate: cobaltUsdDate,
        usdSource: cobaltUsdSource,
        cny: ccmn?.cobalt?.price ?? null,
        cnyChange: ccmn?.cobalt?.updown ?? null,
      };
    })(),
    // 鉍（Bi）— SMM 上海有色網實時數據
    bismuth: bismuth ? {
      cny: bismuth.cny?.average ?? null,
      cnyHigh: bismuth.cny?.high ?? null,
      cnyLow: bismuth.cny?.low ?? null,
      cnyChange: bismuth.cny?.change ?? null,       // 日環比絕對值 元/噸
      cnyChangePct: bismuth.cny?.changePct ?? null, // 日環比 %（SMM vchange_rate×100）
      cnyUnit: '\u5143/\u5428',
      usd: bismuth.usd?.average ?? null,            // USD/t (CIF)
      usdHigh: bismuth.usd?.high ?? null,
      usdLow: bismuth.usd?.low ?? null,
      usdChange: bismuth.usd?.change ?? null,
      usdChangePct: bismuth.usd?.changePct ?? null,
      usdUnit: 'USD/t',
      dataDate: bismuth.cny?.dataDate ?? bismuth.usd?.dataDate ?? null,
      source: bismuth.source,
    } : {
      cny: null, usd: null,
      source: null,
      note: 'SMM抓取失敗，暫無鉍數據',
    },
    // v12 新增：鎂（Mg）— CCMN 1#鎂
    magnesium: ccmn?.magnesium ? {
      cny: ccmn.magnesium.price ?? null,
      cnyChange: ccmn.magnesium.updown ?? null,
      cnyUnit: '\u5143/\u5428',
      usd: null,
      source: 'CCMN',
    } : { cny: null, usd: null, source: null },
    // v8 新增：鉛（Pb）— SMM pb-price 長江現貨
    lead: smmLead ? {
      cny: smmLead.average,
      cnyHigh: smmLead.high,
      cnyLow: smmLead.low,
      cnyChange: smmLead.change,
      cnyChangePct: smmLead.changePct,
      cnyUnit: '\u5143/\u5428',
      usd: null,  // SMM pb-price 無 LME USD 頁面
      dataDate: smmLead.dataDate,
      source: smmLead.source,
    } : { cny: null, usd: null, source: null },
    // v8 新增：錫（Sn）— SMM sn-price 長江現貨
    tin: smmTin ? {
      cny: smmTin.average,
      cnyHigh: smmTin.high,
      cnyLow: smmTin.low,
      cnyChange: smmTin.change,
      cnyChangePct: smmTin.changePct,
      cnyUnit: '\u5143/\u5428',
      usd: null,  // SMM sn-price 無 LME USD 頁面
      dataDate: smmTin.dataDate,
      source: smmTin.source,
    } : { cny: null, usd: null, source: null },
  };

  // 組裝 forwards
  const spotExpiry = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}`;
  const forwards = {
    copper: {
      spot: {
        price: copperSpot.price,
        symbol: 'HG=F',
        expiry: spotExpiry,
      },
      near: {
        price: fwdNear.price,
        symbol: sym2,
        expiry: fwdNear.expiry,
      },
      far: {
        price: fwdFar.price,
        symbol: sym6,
        expiry: fwdFar.expiry,
      },
    },
  };

  // v4 新增：組裝 forumSentiment
  const forumSentiment = buildForumSentiment(smmNews, redditPosts);

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  process.stderr.write(`[fetch-all-data] 完成，耗時 ${elapsed}s\n`);

  // 計算交叉驗證差異
  const crossCheckDiff = (ccmnVal, smmVal) => {
    if (ccmnVal == null || smmVal == null) return null;
    return +((Math.abs(ccmnVal - smmVal) / ccmnVal * 100).toFixed(3));
  };

  const output = {
    date: todaySH,
    dataDate,
    isMarketOpen,
    marketNote,
    changeNote: '所有漲跌均為日環比（vs 前一交易日收盤）',
    prices,
    forwards,
    indices: metalIndices,
    macro: macroIndicators,
    fxRates: {
      usdCny: fxRate,
    },
    inventory,
    // SMM 長江報價交叉驗證（與 CCMN 對比，差異 <1% 為正常市場誤差）
    smmCrossCheck: {
      copper: smmCross?.copper ? {
        smmAvg: smmCross.copper.average,
        smmChange: smmCross.copper.change,
        smmChangePct: smmCross.copper.changePct,
        ccmnAvg: ccmn?.copper?.price ?? null,
        diffPct: crossCheckDiff(ccmn?.copper?.price, smmCross.copper.average),
        consistent: crossCheckDiff(ccmn?.copper?.price, smmCross.copper.average) != null
          ? crossCheckDiff(ccmn?.copper?.price, smmCross.copper.average) < 1
          : null,
        note: smmCross.copper.productName,
      } : null,
      zinc: smmCross?.zinc ? {
        smmAvg: smmCross.zinc.average,
        smmChange: smmCross.zinc.change,
        smmChangePct: smmCross.zinc.changePct,
        ccmnAvg: ccmn?.zinc?.price ?? null,
        diffPct: crossCheckDiff(ccmn?.zinc?.price, smmCross.zinc.average),
        consistent: crossCheckDiff(ccmn?.zinc?.price, smmCross.zinc.average) != null
          ? crossCheckDiff(ccmn?.zinc?.price, smmCross.zinc.average) < 1
          : null,
        note: smmCross.zinc.productName,
      } : null,
      nickel: smmCross?.nickel ? {
        smmAvg: smmCross.nickel.average,
        smmChange: smmCross.nickel.change,
        smmChangePct: smmCross.nickel.changePct,
        ccmnAvg: ccmn?.nickel?.price ?? null,
        diffPct: crossCheckDiff(ccmn?.nickel?.price, smmCross.nickel.average),
        consistent: crossCheckDiff(ccmn?.nickel?.price, smmCross.nickel.average) != null
          ? crossCheckDiff(ccmn?.nickel?.price, smmCross.nickel.average) < 1
          : null,
        note: smmCross.nickel.productName,
      } : null,
    },
    // 數據可用性說明（v9 更新：新增 Westmetall LME庫存+Zn/Ni USD現貨）
    dataAvailability: {
      copper:  { usd: 'Yahoo HG=F ✅', cny: ccmn?.copper?.price ? 'CCMN ✅（主）/ SMM長江✅（校驗）' : (smmCross?.copper?.average ? 'SMM長江 ✅（CCMN故障自動切備援）' : '❌ CNY源缺失') },
      zinc:    { usd: westmetall?.zinc?.cashUsd ? `Westmetall LME Cash ✅ $${westmetall.zinc.cashUsd}/t` : '❌ Westmetall抓取失敗', cny: ccmn?.zinc?.price ? 'CCMN ✅（主）/ SMM上海0#✅（校驗）' : (smmCross?.zinc?.average ? 'SMM上海0# ✅（CCMN故障自動切備援）' : '❌ CNY源缺失') },
      aluminum:{ usd: 'Yahoo ALI=F ✅', cny: ccmn?.aluminum?.price ? 'CCMN A00鋁 ✅' : (ometal?.aluminum?.price ? 'OmetalCN A00鋁 ✅（備用）' : '❌ 無鋁CNY數據') },
      nickel:  { usd: westmetall?.nickel?.cashUsd ? `Westmetall LME Cash ✅ $${westmetall.nickel.cashUsd}/t` : '❌ Westmetall抓取失敗', cny: ccmn?.nickel?.price ? 'CCMN ✅（主）/ SMM電解鎳✅（校驗）' : (smmCross?.nickel?.average ? 'SMM電解鎳 ✅（CCMN故障自動切備援）' : '❌ CNY源缺失') },
      cobalt:  {
        usd: cobaltUsdData?.price
          ? `${cobaltUsdData.source} ✅ $${cobaltUsdData.price}/t (${cobaltUsdData.dataDate})`
          : cobaltUsdData?.needsCny
            ? `SMM-CNY/FX-estimate ✅（估算）`
            : '❌ 所有源失敗',
        cny: 'CCMN ✅',
      },
      bismuth:   { usd: 'SMM CIF ✅（精鉍USD/kg×1000）', cny: 'SMM精鉍 ✅' },
      magnesium: { usd: '❌ 無免費USD源', cny: ccmn?.magnesium?.price ? 'CCMN 1#鎂 ✅（v12新增）' : '❌ CCMN無鎂數據' },
      lead:    { usd: '❌ 無免費源', cny: smmLead ? 'SMM長江鉛錠 ✅（v8新增）' : '❌ SMM抓取失敗' },
      tin:     { usd: '❌ 無免費源', cny: smmTin  ? 'SMM長江錫錠 ✅（v8新增）' : '❌ SMM抓取失敗' },
      lmeInventory: westmetall?.copper?.tonnes ? `Westmetall ✅（Cu=${westmetall.copper.tonnes}t, Zn=${westmetall.zinc?.tonnes}t, Ni=${westmetall.nickel?.tonnes}t）` : '❌ Westmetall抓取失敗',
    },
    news,
    ibNews,
    forumSentiment,
  };

  console.log(JSON.stringify(output, null, 2));
}

main().catch(err => {
  process.stderr.write(`[fetch-all-data] 致命錯誤: ${err.message}\n`);
  // 即使崩潰也輸出合法 JSON
  console.log(JSON.stringify({
    date: today(),
    dataDate: null,
    isMarketOpen: null,
    marketNote: null,
    changeNote: '所有漲跌均為日環比（vs 前一交易日收盤）',
    prices: { copper: null, zinc: null, aluminum: null, nickel: null, cobalt: null, bismuth: null, magnesium: null, lead: null, tin: null },
    forwards: { copper: null },
    indices: [],
    macro: [],
    fxRates: { usdCny: null },
    inventory: { copper: null, zinc: null, nickel: null, cobalt: null, note: err.message },
    news: [],
    ibNews: [],
    forumSentiment: { smmHighlights: null, redditSummary: null, redditSurging: null, xueqiuSummary: null, fetchedAt: new Date().toISOString() },
    error: err.message,
  }, null, 2));
  process.exit(1);
});
