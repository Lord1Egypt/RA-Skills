#!/usr/bin/env node

/**
 * 多方案详细对比工具
 * 展示所有可能的行程组合及其价格、时间、优缺点
 */

const { execSync } = require('child_process');

// 执行 flyai 命令
function runFlyai(command, args) {
  try {
    const cmd = `flyai ${command} ${args.join(' ')}`;
    const output = execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] });
    return JSON.parse(output);
  } catch (error) {
    return null;
  }
}

// 搜索单段航班
function searchFlight(origin, dest, date) {
  const args = [
    '--origin', `"${origin}"`,
    '--destination', `"${dest}"`,
    '--dep-date', date,
    '--sort-type', '3'
  ];
  return runFlyai('search-flight', args);
}

// 搜索往返航班
function searchRoundTrip(origin, dest, depDate, retDate) {
  const args = [
    '--origin', `"${origin}"`,
    '--destination', `"${dest}"`,
    '--dep-date', depDate,
    '--back-date', retDate,
    '--journey-type', '1',
    '--sort-type', '3'
  ];
  return runFlyai('search-flight', args);
}

// 提取最低价格和最佳航班
function extractBest(result) {
  if (!result || !result.data || !result.data.itemList || result.data.itemList.length === 0) {
    return null;
  }
  const sorted = result.data.itemList.slice().sort((a, b) => {
    const priceA = parseFloat(String(a.ticketPrice || a.adultPrice || '999999').replace(/[¥,]/g, ''));
    const priceB = parseFloat(String(b.ticketPrice || b.adultPrice || '999999').replace(/[¥,]/g, ''));
    return priceA - priceB;
  });
  
  const best = sorted[0];
  const price = parseFloat(String(best.ticketPrice || best.adultPrice).replace(/[¥,]/g, ''));
  
  // 提取时刻信息
  let depTime = '', arrTime = '', airline = '', flightNo = '';
  if (best.journeys && best.journeys[0] && best.journeys[0].segments && best.journeys[0].segments[0]) {
    const seg = best.journeys[0].segments[0];
    depTime = seg.depDateTime?.split(' ')[1] || '';
    arrTime = seg.arrDateTime?.split(' ')[1] || '';
    airline = seg.marketingTransportName || '';
    flightNo = seg.marketingTransportNo || '';
  }
  
  return {
    price,
    depTime,
    arrTime,
    airline,
    flightNo,
    jumpUrl: best.jumpUrl,
    duration: best.totalDuration
  };
}

// 解析参数
const args = process.argv.slice(2);
let origin = '北京', cities = ['大阪', '东京'], depDate = '2026-04-10', retDate = '2026-04-20';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--origin' && args[i+1]) origin = args[++i];
  if (args[i] === '--cities' && args[i+1]) {
    const citiesStr = args[++i].replace(/[,,\uFF0C]/g, ',');
    cities = citiesStr.split(',').map(c => c.trim()).filter(c => c);
  }
  if (args[i] === '--dep-date' && args[i+1]) depDate = args[++i];
  if (args[i] === '--return-date' && args[i+1]) retDate = args[++i];
}



console.log('\n' + '='.repeat(90));
console.log(`🗺️  ${origin} → ${cities.join(' + ')} 多方案详细对比`);
console.log(`日期：${depDate} ~ ${retDate}`);
console.log('='.repeat(90) + '\n');

const results = [];

// ========== 方案 A: 大阪先玩 (大阪→东京) ==========
console.log('🔍 搜索方案 A: 大阪先玩 (北京→大阪→东京→北京)...\n');

const A1 = extractBest(searchFlight(origin, cities[0], depDate)); // 北京→大阪
const midDate = new Date(depDate); midDate.setDate(midDate.getDate() + 5);
const A2 = extractBest(searchFlight(cities[0], cities[1], midDate.toISOString().split('T')[0])); // 大阪→东京
const A3 = extractBest(searchFlight(cities[1], origin, retDate)); // 东京→北京

if (A1 && A2 && A3) {
  results.push({
    name: '方案 A: 大阪先玩',
    route: `${origin}→${cities[0]}→${cities[1]}→${origin}`,
    price: A1.price + A2.price + A3.price,
    flights: [
      { from: origin, to: cities[0], date: depDate, ...A1 },
      { from: cities[0], to: cities[1], date: midDate.toISOString().split('T')[0], ...A2 },
      { from: cities[1], to: origin, date: retDate, ...A3 }
    ],
    type: '多程'
  });
}

// ========== 方案 B: 东京先玩 (东京→大阪) ==========
console.log('🔍 搜索方案 B: 东京先玩 (北京→东京→大阪→北京)...\n');

const B1 = extractBest(searchFlight(origin, cities[1], depDate)); // 北京→东京
const B2 = extractBest(searchFlight(cities[1], cities[0], midDate.toISOString().split('T')[0])); // 东京→大阪
const B3 = extractBest(searchFlight(cities[0], origin, retDate)); // 大阪→北京

if (B1 && B2 && B3) {
  results.push({
    name: '方案 B: 东京先玩',
    route: `${origin}→${cities[1]}→${cities[0]}→${origin}`,
    price: B1.price + B2.price + B3.price,
    flights: [
      { from: origin, to: cities[1], date: depDate, ...B1 },
      { from: cities[1], to: cities[0], date: midDate.toISOString().split('T')[0], ...B2 },
      { from: cities[0], to: origin, date: retDate, ...B3 }
    ],
    type: '多程'
  });
}

// ========== 方案 C: 往返大阪 + 单买大阪东京 ==========
console.log('🔍 搜索方案 C: 往返大阪 + 单买中间段...\n');

const C1 = extractBest(searchRoundTrip(origin, cities[0], depDate, retDate)); // 北京↔大阪往返
const C2 = extractBest(searchFlight(cities[0], cities[1], midDate.toISOString().split('T')[0])); // 大阪→东京
const C3 = extractBest(searchFlight(cities[1], cities[0], new Date(midDate.getTime() + 5*86400000).toISOString().split('T')[0])); // 东京→大阪

if (C1 && C2 && C3) {
  results.push({
    name: '方案 C: 往返大阪 + 中间单买',
    route: `${origin}↔${cities[0]} + ${cities[0]}→${cities[1]}→${cities[0]}`,
    price: C1.price + C2.price + C3.price,
    flights: [
      { from: origin, to: cities[0], date: depDate, ...C1, type: '往返' },
      { from: cities[0], to: cities[1], date: midDate.toISOString().split('T')[0], ...C2 },
      { from: cities[1], to: cities[0], date: retDate, ...C3 }
    ],
    type: '往返 + 单程'
  });
}

// ========== 方案 D: 往返东京 + 单买大阪东京 ==========
console.log('🔍 搜索方案 D: 往返东京 + 单买中间段...\n');

const D1 = extractBest(searchRoundTrip(origin, cities[1], depDate, retDate)); // 北京↔东京往返
const D2 = extractBest(searchFlight(cities[1], cities[0], midDate.toISOString().split('T')[0])); // 东京→大阪
const D3 = extractBest(searchFlight(cities[0], cities[1], new Date(midDate.getTime() + 5*86400000).toISOString().split('T')[0])); // 大阪→东京

if (D1 && D2 && D3) {
  results.push({
    name: '方案 D: 往返东京 + 中间单买',
    route: `${origin}↔${cities[1]} + ${cities[1]}→${cities[0]}→${cities[1]}`,
    price: D1.price + D2.price + D3.price,
    flights: [
      { from: origin, to: cities[1], date: depDate, ...D1, type: '往返' },
      { from: cities[1], to: cities[0], date: midDate.toISOString().split('T')[0], ...D2 },
      { from: cities[0], to: cities[1], date: retDate, ...D3 }
    ],
    type: '往返 + 单程'
  });
}

// ========== 输出对比表格 ==========
console.log('\n' + '='.repeat(90));
console.log('📊 所有方案价格对比（按价格从低到高排序）');
console.log('='.repeat(90) + '\n');

results.sort((a, b) => a.price - b.price);

console.log('| 排名 | 方案 | 路线 | 总价格 | 差价 |');
console.log('|------|------|------|--------|------|');
results.forEach((r, i) => {
  const diff = i === 0 ? '-' : `+¥${r.price - results[0].price}`;
  console.log(`| ${i+1} | ${r.name} | ${r.route} | **¥${r.price.toLocaleString()}** | ${diff} |`);
});

console.log('\n' + '='.repeat(90));
console.log('📋 各方案详细航班信息');
console.log('='.repeat(90) + '\n');

results.forEach((r, idx) => {
  console.log(`### ${r.name} (¥${r.price.toLocaleString()})\n`);
  console.log('**航班详情:**\n');
  console.log('| 航段 | 日期 | 时间 | 航班 | 价格 |');
  console.log('|------|------|------|------|------|');
  r.flights.forEach((f, i) => {
    const timeStr = f.type === '往返' ? `${f.depTime} - ${f.arrTime} (往返)` : `${f.depTime} - ${f.arrTime}`;
    console.log(`| ${i+1}. ${f.from}→${f.to} | ${f.date} | ${timeStr} | ${f.airline}${f.flightNo} | ¥${f.price.toLocaleString()} |`);
  });
  
  console.log('\n**优缺点分析:**\n');
  if (r.type === '多程') {
    console.log('✅ 优点:');
    console.log('  • 路线合理，不走回头路');
    console.log('  • 一次购买多段，管理方便');
    console.log('  • 通常可行李直挂（同联盟航司）');
    console.log('\n❌ 缺点:');
    console.log('  • 改签不便，需整体调整');
    console.log('  • 某段延误可能影响后续');
  } else if (r.type === '往返 + 单程') {
    console.log('✅ 优点:');
    console.log('  • 往返票改签灵活');
    console.log('  • 中间段可自由选择时间');
    console.log('\n❌ 缺点:');
    console.log('  • 需要多次购票');
    console.log('  • 可能有重复路段（走回头路）');
    console.log('  • 总价通常较高');
  }
  console.log('\n');
});

console.log('='.repeat(90));
console.log(`🏆 推荐：${results[0].name}`);
console.log(`💰 价格：¥${results[0].price.toLocaleString()}`);
if (results.length > 1) {
  console.log(`💵 比最贵方案省：¥${results[results.length-1].price - results[0].price.toLocaleString()}`);
}
console.log('='.repeat(90) + '\n');

console.log('⚠️  注意事项:');
console.log('  • 价格实时变动，以上仅供参考');
console.log('  • 廉航（捷星、乐桃等）不含托运行李，需单独购买');
console.log('  • 分开购票需注意行李直挂问题');
console.log('  • 建议购买旅行保险');
console.log('\n基于 fly.ai 实时航班数据 | 由 @flyai 提供航班搜索能力\n');
