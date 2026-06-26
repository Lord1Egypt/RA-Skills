#!/usr/bin/env node
/**
 * Polymarket Book Arbitrage Scanner
 * 
 * 原理：真正互斥的多选市场，所有选项 YES 价格之和应 = 1.0
 * 偏离越多 = 套利空间越大
 * 
 * > 1.0 (overbook)：做空所有选项（买全部 NO）
 * < 1.0 (underbook)：做多所有选项（买全部 YES）
 */

const GAMMA_API = 'https://gamma-api.polymarket.com';

const CONFIG = {
  minVolume: 10000,     // 最小成交量 $10k
  minMarkets: 2,        // 至少2个选项
  minThreshold: 0.03,   // 最小偏离 3%（低于此不值得操作）
  maxThreshold: 0.50,   // 最大偏离 50%（高于此几乎都是假信号）
  minPrice: 0.03,       // 单个选项最低有效价格（低于此说明几乎不可能）
  maxPrice: 0.97,       // 单个选项最高有效价格（高于此说明结果快/已出）
  minHealthyMarkets: 2, // 至少需要这么多"健康"选项
  pageSize: 100,
};

// 过滤关键词：包含这些词的问题不是真正互斥市场
const EXCLUDE_KEYWORDS = [
  'o/u', 'over/under', 'over ', 'under ',
  'above', 'below', 'reach ', 'dip to',
  'spread:', '+/-', 'handicap',
  'points o/u', 'rebounds o/u', 'assists o/u',
  '1h o/u', 'moneyline', 'total sets',
  'total kills', 'first blood',
  'map 1 winner', 'map 2 winner',
  'set 1 winner', 'set handicap',
  'games o/u', 'match o/u', 'set 1 games',
  'both teams to score',
];

async function fetchEvents(offset = 0) {
  const url = `${GAMMA_API}/events?active=true&closed=false&limit=${CONFIG.pageSize}&offset=${offset}&order=volume&ascending=false`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

async function fetchAllEvents() {
  const events = [];
  let offset = 0;
  while (true) {
    const batch = await fetchEvents(offset);
    if (!batch || batch.length === 0) break;
    events.push(...batch);
    if (batch.length < CONFIG.pageSize) break;
    offset += CONFIG.pageSize;
    if (events.length >= 500) break;
  }
  return events;
}

function isExcludedQuestion(question) {
  const q = (question || '').toLowerCase();
  return EXCLUDE_KEYWORDS.some(kw => q.includes(kw));
}

function parsePrice(outcomePrices) {
  try {
    const prices = typeof outcomePrices === 'string'
      ? JSON.parse(outcomePrices)
      : outcomePrices;
    return parseFloat(prices[0]);
  } catch {
    return null;
  }
}

function analyzeEvent(event) {
  const eventVolume = parseFloat(event.volume) || 0;
  if (eventVolume < CONFIG.minVolume) return null;

  const allMarkets = (event.markets || []).filter(m => m.active && !m.closed);
  if (allMarkets.length < CONFIG.minMarkets) return null;

  // 过滤掉非互斥选项（O/U、spread 等）
  const validMarkets = allMarkets.filter(m => !isExcludedQuestion(m.question));
  if (validMarkets.length < CONFIG.minMarkets) return null;

  // 解析每个选项的 YES 价格
  const breakdown = [];
  for (const market of validMarkets) {
    const yesPrice = parsePrice(market.outcomePrices);
    if (yesPrice === null || isNaN(yesPrice)) continue;
    breakdown.push({
      question: market.question,
      yesPrice,
      marketId: market.id,
      slug: market.slug,
    });
  }

  if (breakdown.length < CONFIG.minMarkets) return null;

  // 关键过滤：健康选项数量（排除已结算的极端价格）
  const healthyMarkets = breakdown.filter(
    m => m.yesPrice >= CONFIG.minPrice && m.yesPrice <= CONFIG.maxPrice
  );

  if (healthyMarkets.length < CONFIG.minHealthyMarkets) return null;

  // 只用健康选项计算总和（排除接近0/1的选项）
  // 但展示时包含所有选项
  const sum = breakdown.reduce((acc, m) => acc + m.yesPrice, 0);
  const deviation = sum - 1.0;
  const absDeviation = Math.abs(deviation);

  // 过滤：偏离必须在合理范围内
  if (absDeviation < CONFIG.minThreshold) return null;
  if (absDeviation > CONFIG.maxThreshold) return null;

  // 额外检查：如果所有选项都很接近0或1，跳过（已结算市场）
  const hasExtreme = breakdown.some(
    m => m.yesPrice > CONFIG.maxPrice || m.yesPrice < CONFIG.minPrice
  );
  const extremeCount = breakdown.filter(
    m => m.yesPrice > CONFIG.maxPrice || m.yesPrice < CONFIG.minPrice
  ).length;

  // 如果超过一半的选项是极端值，跳过
  if (extremeCount > breakdown.length / 2) return null;

  // negRisk 市场是 Polymarket 专门设计的互斥多选市场，优先级更高
  const isNegRisk = event.negRisk === true;

  return {
    eventId: event.id,
    title: event.title,
    slug: event.slug,
    volume: eventVolume,
    volume24hr: parseFloat(event.volume24hr) || 0,
    sum,
    deviation,
    absDeviation,
    type: deviation > 0 ? 'OVERBOOK' : 'UNDERBOOK',
    strategy: deviation > 0
      ? '买全部 NO（做空所有选项）'
      : '买全部 YES（做多所有选项）',
    expectedProfit: `${(absDeviation * 100).toFixed(2)}%`,
    isNegRisk,
    marketCount: breakdown.length,
    healthyCount: healthyMarkets.length,
    markets: breakdown.sort((a, b) => b.yesPrice - a.yesPrice),
    url: `https://polymarket.com/event/${event.slug}`,
  };
}

function formatReport(opportunities, scanTime) {
  if (opportunities.length === 0) {
    return `[${scanTime}] 扫描完成，暂无套利机会（阈值 ${CONFIG.minThreshold * 100}%-${CONFIG.maxThreshold * 100}%）`;
  }

  // 分组展示
  const negRisk = opportunities.filter(o => o.isNegRisk);
  const regular = opportunities.filter(o => !o.isNegRisk);

  let report = `\n🎯 Polymarket Book套利机会 [${scanTime}]\n`;
  report += `发现 ${opportunities.length} 个机会`;
  if (negRisk.length > 0) report += `（其中 ${negRisk.length} 个 NegRisk 高质量市场）`;
  report += '\n' + '='.repeat(60) + '\n';

  const printOpps = (opps, label) => {
    if (opps.length === 0) return '';
    let out = `\n${label}\n${'─'.repeat(40)}\n`;
    for (const opp of opps) {
      out += `\n【${opp.type}】${opp.title}\n`;
      out += `📊 总成交量: $${(opp.volume / 1000).toFixed(0)}k`;
      if (opp.volume24hr > 0) out += `  | 24h: $${(opp.volume24hr / 1000).toFixed(0)}k`;
      out += '\n';
      out += `📐 概率总和: ${(opp.sum * 100).toFixed(2)}%（偏离 ${opp.deviation > 0 ? '+' : ''}${(opp.deviation * 100).toFixed(2)}%）\n`;
      out += `💰 理论利润: ${opp.expectedProfit}  |  选项数: ${opp.marketCount}（健康: ${opp.healthyCount}）\n`;
      out += `🎯 策略: ${opp.strategy}\n`;
      out += `🔗 ${opp.url}\n`;
      out += `选项:\n`;
      for (const m of opp.markets) {
        const bar = '█'.repeat(Math.round(m.yesPrice * 20));
        out += `  ${(m.yesPrice * 100).toFixed(1).padStart(5)}%  ${bar}  ${m.question.slice(0, 60)}\n`;
      }
      out += '─'.repeat(60) + '\n';
    }
    return out;
  };

  if (negRisk.length > 0) {
    report += printOpps(negRisk, '⭐ NegRisk 市场（最干净的互斥多选）');
  }
  if (regular.length > 0) {
    report += printOpps(regular, '📋 普通多选市场');
  }

  return report;
}

async function main() {
  const scanTime = new Date().toLocaleString('zh-CN', { timeZone: 'Europe/Stockholm' });
  console.log(`[${scanTime}] 开始扫描 Polymarket...`);

  try {
    const events = await fetchAllEvents();
    console.log(`获取到 ${events.length} 个活跃 events`);

    const opportunities = [];
    for (const event of events) {
      const result = analyzeEvent(event);
      if (result) opportunities.push(result);
    }

    // 按偏离程度排序
    opportunities.sort((a, b) => b.absDeviation - a.absDeviation);

    const report = formatReport(opportunities, scanTime);
    console.log(report);

    // 保存结果
    const fs = await import('fs');
    const outputPath = new URL('./opportunities.json', import.meta.url).pathname;
    fs.writeFileSync(outputPath, JSON.stringify({
      scannedAt: new Date().toISOString(),
      count: opportunities.length,
      opportunities,
    }, null, 2));

    return opportunities;
  } catch (err) {
    console.error('扫描失败:', err.message);
    process.exit(1);
  }
}

main();
