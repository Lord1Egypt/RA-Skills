#!/usr/bin/env node

/**
 * 按行程类型对比：多程、缺口程、往返、单程组合
 */

const { execSync } = require('child_process');

function runFlyai(command, args) {
  try {
    const cmd = `flyai ${command} ${args.join(' ')}`;
    const output = execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] });
    return JSON.parse(output);
  } catch (error) {
    return null;
  }
}

function searchFlight(origin, dest, date) {
  return runFlyai('search-flight', [
    '--origin', `"${origin}"`,
    '--destination', `"${dest}"`,
    '--dep-date', date,
    '--sort-type', '3'
  ]);
}

function searchRoundTrip(origin, dest, depDate, retDate) {
  return runFlyai('search-flight', [
    '--origin', `"${origin}"`,
    '--destination', `"${dest}"`,
    '--dep-date', depDate,
    '--back-date', retDate,
    '--journey-type', '1',
    '--sort-type', '3'
  ]);
}

function extractBest(result) {
  if (!result || !result.data || !result.data.itemList || result.data.itemList.length === 0) return null;
  const sorted = result.data.itemList.slice().sort((a, b) => {
    const priceA = parseFloat(String(a.ticketPrice || a.adultPrice || '999999').replace(/[¥,]/g, ''));
    const priceB = parseFloat(String(b.ticketPrice || b.adultPrice || '999999').replace(/[¥,]/g, ''));
    return priceA - priceB;
  });
  const best = sorted[0];
  const price = parseFloat(String(best.ticketPrice || best.adultPrice).replace(/[¥,]/g, ''));
  let depTime = '', arrTime = '', airline = '', flightNo = '';
  if (best.journeys && best.journeys[0] && best.journeys[0].segments && best.journeys[0].segments[0]) {
    const seg = best.journeys[0].segments[0];
    depTime = seg.depDateTime?.split(' ')[1] || '';
    arrTime = seg.arrDateTime?.split(' ')[1] || '';
    airline = seg.marketingTransportName || '';
    flightNo = seg.marketingTransportNo || '';
  }
  return { price, depTime, arrTime, airline, flightNo, jumpUrl: best.jumpUrl };
}

// 参数
const origin = '北京';
const city1 = '大阪';
const city2 = '东京';
const depDate = '2026-04-10';
const retDate = '2026-04-20';
const midDate = '2026-04-15';

console.log('\n' + '='.repeat(100));
console.log(`🗺️  北京 → 大阪 + 东京 | 行程类型对比`);
console.log(`日期：${depDate} ~ ${retDate} (10 天)`);
console.log('='.repeat(100) + '\n');

const plans = [];

// ========== 类型 1: 多程 (Multi-city) ==========
console.log('🔍 搜索类型 1: 多程联订 (Multi-city)...\n');
const M1 = extractBest(searchFlight(origin, city1, depDate));
const M2 = extractBest(searchFlight(city1, city2, midDate));
const M3 = extractBest(searchFlight(city2, origin, retDate));

if (M1 && M2 && M3) {
  plans.push({
    type: '多程联订',
    name: '北京→大阪→东京→北京',
    total: M1.price + M2.price + M3.price,
    flights: [
      { route: `${origin}→${city1}`, date: depDate, ...M1 },
      { route: `${city1}→${city2}`, date: midDate, ...M2 },
      { route: `${city2}→${origin}`, date: retDate, ...M3 }
    ],
    pros: ['一次付款，管理方便', '路线合理不走回头路', '通常可行李直挂'],
    cons: ['改签不便', '某段延误影响后续']
  });
}

// ========== 类型 2: 缺口程 (Open-jaw) ==========
console.log('🔍 搜索类型 2: 缺口程 (Open-jaw)...\n');
// 缺口程：北京→大阪，东京→北京（中间大阪 - 东京单独买）
const O1 = extractBest(searchFlight(origin, city1, depDate));
const O2 = extractBest(searchFlight(city2, origin, retDate));
const O3 = extractBest(searchFlight(city1, city2, midDate));

if (O1 && O2 && O3) {
  plans.push({
    type: '缺口程 + 单程',
    name: '北京→大阪 + 东京→北京 + 大阪→东京单买',
    total: O1.price + O2.price + O3.price,
    flights: [
      { route: `${origin}→${city1}`, date: depDate, ...O1, note: '缺口程去程' },
      { route: `${city2}→${origin}`, date: retDate, ...O2, note: '缺口程返程' },
      { route: `${city1}→${city2}`, date: midDate, ...O3, note: '中间单买' }
    ],
    pros: ['通常最便宜', '中间段灵活', '可选择不同航司'],
    cons: ['需分别购票', '行李可能需自提']
  });
}

// ========== 类型 3: 往返大阪 + 单程大阪东京往返 ==========
console.log('🔍 搜索类型 3: 往返大阪 + 中间往返...\n');
const R1 = extractBest(searchRoundTrip(origin, city1, depDate, retDate));
const R2 = extractBest(searchFlight(city1, city2, midDate));
const R3 = extractBest(searchFlight(city2, city1, retDate));

if (R1 && R2 && R3) {
  plans.push({
    type: '往返大阪 + 中间往返',
    name: '北京↔大阪往返 + 大阪↔东京往返',
    total: R1.price + R2.price + R3.price,
    flights: [
      { route: `${origin}↔${city1}`, date: depDate, ...R1, note: '往返票' },
      { route: `${city1}→${city2}`, date: midDate, ...R2, note: '单程' },
      { route: `${city2}→${city1}`, date: retDate, ...R3, note: '单程' }
    ],
    pros: ['往返票改签灵活', '北京 - 大阪段有保障'],
    cons: ['走回头路', '总价高', '需多次购票']
  });
}

// ========== 类型 4: 往返东京 + 单程大阪东京往返 ==========
console.log('🔍 搜索类型 4: 往返东京 + 中间往返...\n');
const T1 = extractBest(searchRoundTrip(origin, city2, depDate, retDate));
const T2 = extractBest(searchFlight(city2, city1, midDate));
const T3 = extractBest(searchFlight(city1, city2, retDate));

if (T1 && T2 && T3) {
  plans.push({
    type: '往返东京 + 中间往返',
    name: '北京↔东京往返 + 东京↔大阪往返',
    total: T1.price + T2.price + T3.price,
    flights: [
      { route: `${origin}↔${city2}`, date: depDate, ...T1, note: '往返票' },
      { route: `${city2}→${city1}`, date: midDate, ...T2, note: '单程' },
      { route: `${city1}→${city2}`, date: retDate, ...T3, note: '单程' }
    ],
    pros: ['往返票改签灵活', '北京 - 东京段有保障'],
    cons: ['走回头路', '总价高', '需多次购票']
  });
}

// ========== 类型 5: 三个单程 ==========
console.log('🔍 搜索类型 5: 三个单程...\n');
const S1 = extractBest(searchFlight(origin, city1, depDate));
const S2 = extractBest(searchFlight(city1, city2, midDate));
const S3 = extractBest(searchFlight(city2, origin, retDate));

if (S1 && S2 && S3) {
  plans.push({
    type: '三个单程',
    name: '北京→大阪 + 大阪→东京 + 东京→北京',
    total: S1.price + S2.price + S3.price,
    flights: [
      { route: `${origin}→${city1}`, date: depDate, ...S1, note: '单程' },
      { route: `${city1}→${city2}`, date: midDate, ...S2, note: '单程' },
      { route: `${city2}→${origin}`, date: retDate, ...S3, note: '单程' }
    ],
    pros: ['最灵活', '每段可单独改签', '可选择最便宜的组合'],
    cons: ['需三次购票', '行李不能直挂', '前段延误影响后续']
  });
}

// ========== 输出对比 ==========
console.log('\n' + '='.repeat(100));
console.log('📊 行程类型价格对比（从低到高）');
console.log('='.repeat(100) + '\n');

plans.sort((a, b) => a.total - b.total);

console.log('| 排名 | 行程类型 | 飞行路线 | 总价格 | 差价 | 购票次数 |');
console.log('|------|----------|----------|--------|------|----------|');
plans.forEach((p, i) => {
  const diff = i === 0 ? '-' : `+¥${(p.total - plans[0].total).toLocaleString()}`;
  const routeStr = p.flights.map(f => f.route).join(' → ');
  console.log(`| ${i+1} | ${p.type} | ${routeStr} | **¥${p.total.toLocaleString()}** | ${diff} | ${p.flights.length}次 |`);
});

console.log('\n' + '='.repeat(100));
console.log('📋 各类型详细航班对比');
console.log('='.repeat(100) + '\n');

plans.forEach((p, idx) => {
  console.log(`### ${idx + 1}. ${p.type} - ¥${p.total.toLocaleString()}\n`);
  console.log(`**路线**: ${p.name}\n`);
  console.log('**航班详情:**\n');
  console.log('| 航段 | 日期 | 时间 | 航班 | 价格 |');
  console.log('|------|------|------|------|------|');
  p.flights.forEach((f, i) => {
    const timeStr = f.note === '往返票' ? `${f.depTime} (往返)` : `${f.depTime}-${f.arrTime}`;
    console.log(`| ${i+1}. ${f.route} | ${f.date} | ${timeStr} | ${f.airline}${f.flightNo} | ¥${f.price.toLocaleString()} |`);
  });
  
  console.log('\n**优缺点:**\n');
  console.log('✅ ' + p.pros.join(' | '));
  console.log('\n❌ ' + p.cons.join(' | '));
  console.log('\n');
});

console.log('='.repeat(100));
console.log(`🏆 推荐：${plans[0].type}`);
console.log(`💰 价格：¥${plans[0].total.toLocaleString()}`);
console.log(`💵 比最贵方案省：¥${(plans[plans.length-1].total - plans[0].total).toLocaleString()}`);
console.log('='.repeat(100) + '\n');

console.log('⚠️  注意事项:');
console.log('  • 价格实时变动，以上仅供参考');
console.log('  • 廉航（捷星、乐桃等）不含托运行李，需单独购买');
console.log('  • 分开购票需注意行李直挂问题');
console.log('  • 建议购买旅行保险\n');
console.log('基于 fly.ai 实时航班数据 | 由 @flyai 提供航班搜索能力\n');
