#!/usr/bin/env node

/**
 * Multi-City Planner - 统一入口脚本
 * 根据城市数量自动选择对应的规划脚本
 */

const { execSync } = require('child_process');
const path = require('path');

// 解析参数
const args = process.argv.slice(2);
let origin = '', cities = [], depDate = '', retDate = '', region = 'auto';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--origin' && args[i + 1]) {
    origin = args[++i];
  } else if (args[i] === '--cities' && args[i + 1]) {
    const citiesStr = args[++i].replace(/[,,]/g, ',');
    cities = citiesStr.split(',').map(c => c.trim()).filter(c => c);
  } else if (args[i] === '--dep-date' && args[i + 1]) {
    depDate = args[++i];
  } else if (args[i] === '--return-date' && args[i + 1]) {
    retDate = args[++i];
  } else if (args[i] === '--region' && args[i + 1]) {
    region = args[++i];
  } else if (args[i] === '--help' || args[i] === '-h') {
    console.log(`
🗺️  Multi-City Planner - 多目的地行程规划

用法:
  node plan.js --origin "北京" --cities "巴黎，罗马，米兰" --dep-date 2026-04-10 --return-date 2026-04-21

参数:
  --origin       出发城市（必填）
  --cities       目的地城市列表，逗号分隔（必填）
  --dep-date     出发日期（必填）
  --return-date  返回日期（必填）
  --region       区域：auto（自动）| europe（欧洲）| japan（日本）
  --help, -h     显示帮助

示例:
  # 日本游
  node plan.js --origin "北京" --cities "大阪，东京" --dep-date 2026-04-10 --return-date 2026-04-20
  
  # 欧洲游
  node plan.js --origin "北京" --cities "巴黎，罗马，米兰" --dep-date 2026-04-10 --return-date 2026-04-21 --region europe
  
  # 北海道游
  node plan.js --origin "北京" --cities "札幌，函馆，旭川" --dep-date 2026-04-10 --return-date 2026-04-20 --region japan
`);
    process.exit(0);
  }
}

// 检查必要参数
if (!origin || cities.length === 0 || !depDate || !retDate) {
  console.error('❌ 缺少必要参数');
  console.error('用法：node plan.js --origin "北京" --cities "巴黎，罗马" --dep-date 2026-04-10 --return-date 2026-04-21');
  console.error('使用 --help 查看帮助');
  process.exit(1);
}

// 自动选择脚本
const scriptDir = __dirname;
let script = '';

// 检测区域
const allCities = origin + cities.join('');
const isEurope = region === 'europe' || /巴黎 | 罗马 | 米兰 | 苏黎世 | 伦敦 | 柏林/i.test(allCities);
const isJapan = region === 'japan' || /大阪 | 东京 | 札幌 | 函馆 | 旭川 | 北海道/i.test(allCities);

if (isEurope && cities.length >= 3) {
  script = 'europe-4cities-complete.js';
} else if (isEurope && cities.length === 2) {
  script = 'europe-3cities.js';
} else if (isJapan && cities.length >= 3) {
  if (/东京/i.test(allCities) && cities.length >= 4) {
    script = 'hokkaido-tokyo-4cities.js';
  } else {
    script = 'hokkaido-3cities.js';
  }
} else if (cities.length >= 3) {
  script = 'compare-complete.js';
} else {
  script = 'search-multi-city.js';
}

const scriptPath = path.join(scriptDir, 'scripts', script);

console.log(`\n🗺️  Multi-City Planner - 多目的地行程规划`);
console.log(`出发地：${origin}`);
console.log(`目的地：${cities.join(' + ')}`);
console.log(`日期：${depDate} ~ ${retDate}`);
console.log(`使用脚本：${script}\n`);
console.log('='.repeat(80) + '\n');

// 执行脚本
try {
  const cmd = `node "${scriptPath}" --origin "${origin}" --cities "${cities.join(',')}" --dep-date "${depDate}" --return-date "${retDate}"`;
  execSync(cmd, { stdio: 'inherit' });
} catch (error) {
  console.error('❌ 执行失败:', error.message);
  process.exit(1);
}
