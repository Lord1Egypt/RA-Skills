#!/usr/bin/env node

/**
 * Multi-City Flight Planner
 * 搜索和比较多种行程方案：多程、缺口程、往返组合
 * 输出格式：飞行路线对比表 + 详细航班信息 + 优缺点分析
 */

const { execSync } = require('child_process');

// 执行 flyai 命令
function runFlyai(command, args) {
  try {
    const cmd = `flyai ${command} ${args.join(' ')}`;
    const output = execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] });
    return JSON.parse(output);
  } catch (error) {
    if (error.message?.includes('429')) {
      console.error('\n⚠️  航班查询次数超限，请稍后再试\n');
    }
    return null;
  }
}

// 搜索单段航班
function searchFlight(origin, dest, date) {
  return runFlyai('search-flight', [
    '--origin', `"${origin}"`,
    '--destination', `"${dest}"`,
    '--dep-date', date,
    '--sort-type', '3'
  ]);
}

// 搜索往返航班
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

// 提取最佳航班信息
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

// 解析参数
function parseArgs(args) {
  const params = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--origin' && args[i + 1]) {
      params.origin = args[++i];
    } else if (args[i] === '--cities' && args[i + 1]) {
      const citiesStr = args[++i].replace(/[,,\uFF0C]/g, ',');
      params.cities = citiesStr.split(',').map(c => c.trim()).filter(c => c);
    } else if (args[i] === '--route' && args[i + 1]) {
      const routeStr = args[++i].replace(/[,,\uFF0C]/g, ',');
      params.route = routeStr.split(',').map(c => c.trim()).filter(c => c);
    } else if (args[i] === '--dep-date' && args[i + 1]) {
      params.depDate = args[++i];
    } else if (args[i] === '--return-date' && args[i + 1]) {
      params.returnDate = args[++i];
    } else if (args[i] === '--days-per-city' && args[i + 1]) {
      params.daysPerCity = args[++i].split(',').map(d => parseInt(d.trim()));
    } else if (args[i] === '--budget' && args[i + 1]) {
      params.budget = parseInt(args[++i]);
    } else if (args[i] === '--prefer' && args[i + 1]) {
      params.prefer = args[++i];
    }
  }
  return params;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  if (!params.origin || (!params.cities && !params.route) || !params.depDate || !params.returnDate) {
    console.error('❌ 缺少必要参数');
    console.error('用法：multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25');
    process.exit(1);
  }

  const origin = params.origin;
  const cities = params.route || params.cities;
  const city1 = cities[0];
  const city2 = cities[1];
  
  if (!city2) {
    console.error('❌ 需要至少两个城市');
    console.error('用法：multi-city-planner --origin "北京" --cities "大阪，东京" --dep-date 2026-04-15 --return-date 2026-04-25');
    process.exit(1);
  }
  
  const totalDays = new Date(params.returnDate).getTime() - new Date(params.depDate).getTime();
  const totalDaysNum = Math.ceil(totalDays / (1000 * 60 * 60 * 24));
  const midDate = new Date(params.depDate);
  midDate.setDate(midDate.getDate() + Math.floor(totalDaysNum / 2));
  const midDateStr = midDate.toISOString().split('T')[0];

  console.log('\n' + '='.repeat(100));
  console.log(`🗺️  ${origin} → ${cities.join(' + ')} | 行程类型对比`);
  console.log(`日期：${params.depDate} ~ ${params.returnDate} (${totalDaysNum}天)`);
  console.log('='.repeat(100) + '\n');

  const plans = [];

  // ========== 类型 1: 多程联订 ==========
  const M1 = extractBest(searchFlight(origin, city1, params.depDate));
  const M2 = extractBest(searchFlight(city1, city2, midDateStr));
  const M3 = extractBest(searchFlight(city2, origin, params.returnDate));

  if (M1 && M2 && M3) {
    plans.push({
      type: '多程联订',
      route: `${origin}→${city1} → ${city1}→${city2} → ${city2}→${origin}`,
      name: `${origin}→${city1}→${city2}→${origin}`,
      total: M1.price + M2.price + M3.price,
      flights: [
        { route: `${origin}→${city1}`, date: params.depDate, ...M1 },
        { route: `${city1}→${city2}`, date: midDateStr, ...M2 },
        { route: `${city2}→${origin}`, date: params.returnDate, ...M3 }
      ],
      pros: ['一次付款，管理方便', '路线合理不走回头路', '通常可行李直挂'],
      cons: ['改签不便', '某段延误影响后续']
    });
  }

  // ========== 类型 2: 缺口程 ==========
  const O1 = extractBest(searchFlight(origin, city1, params.depDate));
  const O2 = extractBest(searchFlight(city2, origin, params.returnDate));
  const O3 = extractBest(searchFlight(city1, city2, midDateStr));

  if (O1 && O2 && O3) {
    plans.push({
      type: '缺口程 + 单程',
      route: `${origin}→${city1} + ${city2}→${origin} + ${city1}→${city2}`,
      name: `${origin}→${city1} + ${city2}→${origin} + ${city1}→${city2}单买`,
      total: O1.price + O2.price + O3.price,
      flights: [
        { route: `${origin}→${city1}`, date: params.depDate, ...O1, note: '缺口程去程' },
        { route: `${city2}→${origin}`, date: params.returnDate, ...O2, note: '缺口程返程' },
        { route: `${city1}→${city2}`, date: midDateStr, ...O3, note: '中间单买' }
      ],
      pros: ['通常最便宜', '中间段灵活', '可选择不同航司'],
      cons: ['需分别购票', '行李可能需自提']
    });
  }

  // ========== 类型 3: 三个单程 ==========
  const S1 = extractBest(searchFlight(origin, city1, params.depDate));
  const S2 = extractBest(searchFlight(city1, city2, midDateStr));
  const S3 = extractBest(searchFlight(city2, origin, params.returnDate));

  if (S1 && S2 && S3) {
    plans.push({
      type: '三个单程',
      route: `${origin}→${city1} → ${city1}→${city2} → ${city2}→${origin}`,
      name: `${origin}→${city1} + ${city1}→${city2} + ${city2}→${origin}`,
      total: S1.price + S2.price + S3.price,
      flights: [
        { route: `${origin}→${city1}`, date: params.depDate, ...S1, note: '单程' },
        { route: `${city1}→${city2}`, date: midDateStr, ...S2, note: '单程' },
        { route: `${city2}→${origin}`, date: params.returnDate, ...S3, note: '单程' }
      ],
      pros: ['最灵活', '每段可单独改签', '可选择最便宜的组合'],
      cons: ['需三次购票', '行李不能直挂', '前段延误影响后续']
    });
  }

  // ========== 类型 4: 往返 city1 + 中间往返 ==========
  const R1 = extractBest(searchRoundTrip(origin, city1, params.depDate, params.returnDate));
  const R2 = extractBest(searchFlight(city1, city2, midDateStr));
  const R3 = extractBest(searchFlight(city2, city1, params.returnDate));

  if (R1 && R2 && R3) {
    plans.push({
      type: `往返${city1} + 中间往返`,
      route: `${origin}↔${city1} → ${city1}→${city2} → ${city2}→${city1}`,
      name: `${origin}↔${city1}往返 + ${city1}↔${city2}往返`,
      total: R1.price + R2.price + R3.price,
      flights: [
        { route: `${origin}↔${city1}`, date: params.depDate, ...R1, note: '往返票' },
        { route: `${city1}→${city2}`, date: midDateStr, ...R2, note: '单程' },
        { route: `${city2}→${city1}`, date: params.returnDate, ...R3, note: '单程' }
      ],
      pros: ['往返票改签灵活', `${origin}-${city1}段有保障`],
      cons: ['走回头路', '总价高', '需多次购票']
    });
  }

  // ========== 检查是否有结果 ==========
  if (plans.length === 0) {
    console.error('\n⚠️  未找到合适的航班方案，可能原因:');
    console.error('  1. 航班查询次数超限 (HTTP 429)，请稍后再试');
    console.error('  2. 指定日期无航班');
    console.error('  3. 城市名称识别问题，尝试使用机场代码\n');
    process.exit(1);
  }

  // ========== 输出对比表格 ==========
  console.log('📊 行程类型价格对比（从低到高）\n');

  plans.sort((a, b) => a.total - b.total);

  console.log('| 排名 | 行程类型 | 飞行路线 | 总价格 | 差价 |');
  console.log('|------|----------|----------|--------|------|');
  plans.forEach((p, i) => {
    const diff = i === 0 ? '-' : `+¥${(p.total - plans[0].total).toLocaleString()}`;
    console.log(`| ${i+1} | ${p.type} | ${p.route} | **¥${p.total.toLocaleString()}** | ${diff} |`);
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
  if (plans.length > 1) {
    console.log(`💵 比最贵方案省：¥${(plans[plans.length-1].total - plans[0].total).toLocaleString()}`);
  }
  console.log('='.repeat(100) + '\n');

  console.log('⚠️  注意事项:');
  console.log('  • 价格实时变动，以上仅供参考');
  console.log('  • 廉航（捷星、乐桃等）不含托运行李，需单独购买');
  console.log('  • 分开购票需注意行李直挂问题');
  console.log('  • 建议购买旅行保险\n');
  console.log('基于 fly.ai 实时航班数据 | 由 @flyai 提供航班搜索能力\n');
}

main().catch(console.error);
