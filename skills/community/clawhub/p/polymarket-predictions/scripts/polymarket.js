/**
 * Polymarket API 封装
 */

const POLYMARKET_API = 'https://clob.polymarket.com';

/**
 * 获取活跃市场列表
 * @param {number} limit - 返回数量
 */
async function getActiveMarkets(limit = 10) {
  const url = `${POLYMARKET_API}/markets?active=true&closed=false&limit=${limit}`;
  const resp = await fetch(url);
  const data = await resp.json();
  return data.data || []; // 数据在 data 字段中
}

/**
 * 搜索市场
 * @param {string} query - 搜索关键词
 */
async function searchMarkets(query) {
  const url = `${POLYMARKET_API}/markets?query=${encodeURIComponent(query)}`;
  const resp = await fetch(url);
  const data = await resp.json();
  return data.data || []; // 数据在 data 字段中
}

/**
 * 获取市场详情
 * @param {string} tokenId - token ID
 */
async function getMarketPrice(tokenId) {
  const url = `${POLYMARKET_API}/price?token_id=${tokenId}`;
  const resp = await fetch(url);
  return await resp.json();
}

/**
 * 获取热门市场（简化版）
 */
async function getHotMarkets(limit = 10) {
  const markets = await getActiveMarkets(limit);
  
  // 过滤并格式化
  return markets
    .filter(m => m.tokens && m.tokens.length > 0 && m.accepting_orders)
    .slice(0, limit)
    .map(m => ({
      question: m.question,
      slug: m.market_slug,
      url: `https://polymarket.com/event/${m.market_slug}`,
      options: m.tokens.map(t => ({
        outcome: t.outcome,
        price: t.price
      })),
      volume: m.volume || 'N/A'
    }));
}

/**
 * 格式化输出
 */
function formatMarketOutput(market) {
  const lines = [
    `📋 ${market.question}`,
    `🔗 ${market.url}`,
    '',
    '赔率:'
  ];
  
  for (const opt of market.options) {
    const prob = (opt.price * 100).toFixed(1);
    lines.push(`  ${opt.outcome}: ${prob}%`);
  }
  
  return lines.join('\n');
}

module.exports = {
  getActiveMarkets,
  searchMarkets,
  getMarketPrice,
  getHotMarkets,
  formatMarketOutput
};
