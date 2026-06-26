#!/usr/bin/env node
/**
 * 智能投资简报生成器
 * 基于 Tavily AI 搜索的股票分析工具
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const TAVILY_API_KEY = process.env.TAVILY_API_KEY;

if (!TAVILY_API_KEY) {
  console.error('❌ 错误: 请设置 TAVILY_API_KEY 环境变量');
  console.error('export TAVILY_API_KEY=your_api_key_here');
  process.exit(1);
}

// 解析命令行参数
const args = process.argv.slice(2);
const options = {
  stock: null,
  name: null,
  market: false,
  portfolio: false,
  output: null
};

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--stock':
    case '-s':
      options.stock = args[++i];
      break;
    case '--name':
    case '-n':
      options.name = args[++i];
      break;
    case '--market':
    case '-m':
      options.market = true;
      break;
    case '--portfolio':
    case '-p':
      options.portfolio = true;
      break;
    case '--output':
    case '-o':
      options.output = args[++i];
      break;
    case '--help':
    case '-h':
      showHelp();
      process.exit(0);
      break;
  }
}

function showHelp() {
  console.log(`
📈 智能投资简报生成器

用法:
  node generate-brief.mjs [选项]

选项:
  -s, --stock <code>     股票代码 (如: 002837)
  -n, --name <name>      股票名称 (如: 英维克)
  -m, --market           生成市场热点简报
  -p, --portfolio        监控持仓股
  -o, --output <file>    输出文件路径
  -h, --help             显示帮助

示例:
  node generate-brief.mjs -s 002837 -n 英维克
  node generate-brief.mjs --market
  node generate-brief.mjs --portfolio -o ~/portfolio.md
`);
}

// 获取 Tavily 搜索脚本路径
const skillDir = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const tavilySearchScript = path.join(process.env.HOME, '.openclaw', 'skills', 'tavily-search', 'scripts', 'search.mjs');

async function tavilySearch(query, options = {}) {
  const { topic = 'news', maxResults = 5 } = options;
  const cmd = `node "${tavilySearchScript}" "${query}" -n ${maxResults} ${topic === 'news' ? '--topic news' : ''}`;
  
  try {
    const result = execSync(cmd, { 
      encoding: 'utf-8',
      env: { ...process.env, TAVILY_API_KEY }
    });
    return result;
  } catch (error) {
    console.error('搜索失败:', error.message);
    return null;
  }
}

// 生成个股分析报告
async function generateStockBrief(stockCode, stockName) {
  console.log(`🔍 正在分析 ${stockName}(${stockCode})...\n`);
  
  // 并行搜索多个维度
  const [priceInfo, newsInfo, analysisInfo] = await Promise.all([
    tavilySearch(`${stockName} ${stockCode} 股价 实时行情 今日`, { maxResults: 3 }),
    tavilySearch(`${stockName} ${stockCode} 最新消息 公告 利好`, { maxResults: 3 }),
    tavilySearch(`${stockName} ${stockCode} 券商研报 评级 目标价`, { maxResults: 3 })
  ]);
  
  const brief = generateBriefContent(stockCode, stockName, {
    price: priceInfo,
    news: newsInfo,
    analysis: analysisInfo
  });
  
  return brief;
}

// 生成简报内容
function generateBriefContent(stockCode, stockName, data) {
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  
  let content = `# 📊 ${stockName}(${stockCode}) 投资简报

**生成时间**: ${now}

---

`;

  // 价格信息
  if (data.price) {
    content += `## 💰 行情概览

${data.price}

---

`;
  }

  // 最新消息
  if (data.news) {
    content += `## 📰 最新消息

${data.news}

---

`;
  }

  // 研报分析
  if (data.analysis) {
    content += `## 📈 机构观点

${data.analysis}

---

`;
  }

  // AI 总结
  content += `## 🤖 AI 分析总结

基于 Tavily AI 搜索的综合分析：

- **数据来源**: 实时网络搜索
- **分析维度**: 价格走势、市场消息、机构观点
- **建议**: 建议结合技术面和基本面综合判断

---

*本简报由 智能投资简报生成器 自动生成*
*数据来源: Tavily AI Search*
`;

  return content;
}

// 生成市场热点简报
async function generateMarketBrief() {
  console.log('🔍 正在生成市场热点简报...\n');
  
  const [marketInfo, hotSectors, fundFlow] = await Promise.all([
    tavilySearch('A股 上证指数 今日行情 走势分析', { maxResults: 3 }),
    tavilySearch('A股 热门板块 今日涨幅 资金流向', { maxResults: 3 }),
    tavilySearch('北向资金 今日流入 主力资金', { maxResults: 3 })
  ]);
  
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  
  return `# 📈 A股市场热点简报

**生成时间**: ${now}

---

## 📊 大盘概况

${marketInfo || '暂无数据'}

---

## 🔥 热门板块

${hotSectors || '暂无数据'}

---

## 💰 资金流向

${fundFlow || '暂无数据'}

---

*本简报由 智能投资简报生成器 自动生成*
`;
}

// 主函数
async function main() {
  let brief = '';
  
  if (options.stock) {
    brief = await generateStockBrief(options.stock, options.name || options.stock);
  } else if (options.market) {
    brief = await generateMarketBrief();
  } else if (options.portfolio) {
    console.log('📁 持仓监控功能开发中...');
    console.log('请使用 --stock 参数分析个股');
    process.exit(0);
  } else {
    console.error('❌ 请指定操作类型');
    console.error('使用 --help 查看帮助');
    process.exit(1);
  }
  
  // 输出结果
  if (options.output) {
    fs.writeFileSync(options.output, brief, 'utf-8');
    console.log(`✅ 简报已保存至: ${options.output}`);
  } else {
    console.log('\n' + '='.repeat(60));
    console.log(brief);
    console.log('='.repeat(60));
  }
}

main().catch(console.error);
