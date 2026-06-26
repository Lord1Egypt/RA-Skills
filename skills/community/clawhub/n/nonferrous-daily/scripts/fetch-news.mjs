/**
 * fetch-news.mjs
 * 抓取有色金屬相關新聞（RSS 解析，無需外部庫）
 * 數據源優先級：Google News RSS → Reuters RSS → Yahoo Finance RSS
 */

const METAL_KEYWORDS = ['copper', 'zinc', 'nickel', 'cobalt', 'metal', '铜', '锌', '镍', '钴', '有色'];

// ────────────────────────────────────────────
// RSS XML 手動解析
// ────────────────────────────────────────────
function parseRSS(xml) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
  let match;

  while ((match = itemRegex.exec(xml)) !== null) {
    const block = match[1];

    // 標題
    const titleMatch = block.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) ||
                       block.match(/<title>([\s\S]*?)<\/title>/);
    const title = titleMatch ? titleMatch[1].trim() : '';

    // URL
    const linkMatch = block.match(/<link>([\s\S]*?)<\/link>/) ||
                      block.match(/<guid[^>]*>(https?:\/\/[^\s<]+)<\/guid>/);
    const url = linkMatch ? linkMatch[1].trim() : '';

    // 發布時間
    const pubDateMatch = block.match(/<pubDate>([\s\S]*?)<\/pubDate>/);
    const publishedAt = pubDateMatch ? pubDateMatch[1].trim() : '';

    if (title) {
      items.push({ title, url, publishedAt });
    }
  }
  return items;
}

// ────────────────────────────────────────────
// 過濾金屬相關新聞（關鍵詞匹配）
// ────────────────────────────────────────────
function filterMetalNews(items) {
  return items.filter(item => {
    const text = (item.title + ' ' + (item.description || '')).toLowerCase();
    return METAL_KEYWORDS.some(kw => text.includes(kw.toLowerCase()));
  });
}

// ────────────────────────────────────────────
// 單個 RSS 源抓取
// ────────────────────────────────────────────
// ────────────────────────────────────────────
// 日期過濾（所有源通用，只保留 36h 內）
// ────────────────────────────────────────────
function filterByDate(items) {
  const cutoff = Date.now() - 36 * 60 * 60 * 1000;
  return items.filter(item => {
    if (!item.publishedAt) return true; // 無日期字段不過濾
    const ts = Date.parse(item.publishedAt);
    return isNaN(ts) || ts >= cutoff;
  });
}

async function fetchRSS(url, needFilter = false) {
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; MetalPriceBot/1.0)',
      'Accept': 'application/rss+xml, application/xml, text/xml, */*',
    },
    signal: AbortSignal.timeout(12000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const xml = await res.text();
  let items = parseRSS(xml);
  if (needFilter) items = filterMetalNews(items);
  items = filterByDate(items); // 所有源都過濾日期
  return items;
}

// ────────────────────────────────────────────
// 主函數：按優先級嘗試數據源
// ────────────────────────────────────────────
async function main() {
  const sources = [
    {
      name: 'Google News RSS',
      url: 'https://news.google.com/rss/search?q=%E6%9C%89%E8%89%B2%E9%87%91%E5%B1%9E+%E4%BB%B7%E6%A0%BC&hl=zh-CN&gl=CN&ceid=CN:zh-Hans',
      needFilter: false,
    },
    {
      name: 'Reuters RSS',
      url: 'https://feeds.reuters.com/reuters/UKBusinessNews',
      needFilter: true,
    },
    {
      name: 'Yahoo Finance RSS',
      url: 'https://finance.yahoo.com/rss/topstories',
      needFilter: true,
    },
  ];

  let news = [];
  let usedSource = null;

  for (const source of sources) {
    try {
      process.stderr.write(`[fetch-news] 嘗試 ${source.name}...\n`);
      const items = await fetchRSS(source.url, source.needFilter);
      if (items.length > 0) {
        news = items.slice(0, 5);
        usedSource = source.name;
        process.stderr.write(`[fetch-news] ✅ ${source.name} 成功，獲取 ${news.length} 條\n`);
        break;
      } else {
        process.stderr.write(`[fetch-news] ⚠️ ${source.name} 返回 0 條，繼續下一個\n`);
      }
    } catch (err) {
      process.stderr.write(`[fetch-news] ❌ ${source.name} 失敗: ${err.message}\n`);
    }
  }

  if (news.length === 0) {
    process.stderr.write('[fetch-news] 所有數據源均失敗或無相關新聞\n');
  }

  const output = {
    source: usedSource,
    count: news.length,
    items: news,
  };

  console.log(JSON.stringify(output, null, 2));
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
