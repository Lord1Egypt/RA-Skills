#!/usr/bin/env node
/**
 * A股/港股盯盘系统 - 主监控脚本
 * 
 * 功能：
 * 1. 获取实时股价数据
 * 2. 技术指标计算与分析
 * 3. 趋势判断
 * 4. 买卖建议生成
 * 5. 数据持久化（6个月）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { fetchStockData: fetchStockDataMultiSource } = require('./data-sources.js');

// 配置
const CONFIG = {
  // A股
  aStocks: [
    { name: '美的集团', code: '000333.SZ', market: 'A股' },
    { name: '中控技术', code: '688777.SH', market: 'A股' },
    { name: '工商银行', code: '601398.SH', market: 'A股' },
    { name: '中国中车', code: '601766.SH', market: 'A股' },
    { name: '长安汽车', code: '000625.SZ', market: 'A股' },
    { name: '爱尔眼科', code: '300015.SZ', market: 'A股' },
    { name: '宋城演艺', code: '300144.SZ', market: 'A股' },
    { name: '青岛啤酒', code: '600600.SH', market: 'A股' }
  ],
  // 港股
  hkStocks: [
    { name: '美团-W', code: '3690.HK', market: '港股' },
    { name: '阿里巴巴-SW', code: '9988.HK', market: '港股' },
    { name: '腾讯控股', code: '0700.HK', market: '港股' },
    { name: '吉利汽车', code: '0175.HK', market: '港股' },
    { name: '山高控股', code: '0412.HK', market: '港股' },
    { name: '华润燃气', code: '1193.HK', market: '港股' },
    { name: '顺丰控股', code: '6936.HK', market: '港股' },
    { name: '海尔智家', code: '6690.HK', market: '港股' }
  ],
  // 国债逆回购
  repos: [
    { name: 'GC001', code: '204001.SH', desc: '1天期国债逆回购' },
    { name: 'GC002', code: '204002.SH', desc: '2天期国债逆回购' },
    { name: 'GC007', code: '204007.SH', desc: '7天期国债逆回购' },
    { name: 'R-001', code: '131810.SZ', desc: '1天期深市逆回购' }
  ],
  // 交易时间 (北京时间，前后延长30分钟)
  tradingHours: {
    aStock: {
      morning: { start: '09:00', end: '12:00' },
      afternoon: { start: '12:30', end: '15:30' }
    },
    hkStock: {
      morning: { start: '09:00', end: '12:30' },
      afternoon: { start: '12:30', end: '16:30' }
    }
  },
  // 数据保留期限 (天)
  retentionDays: 180,
  // 数据目录
  dataDir: path.join(__dirname, '..', 'data'),
  reportsDir: path.join(__dirname, '..', 'reports'),
  // QVeris API
  qverisApiKey: process.env.QVERIS_API_KEY || 'sk-pQbZOXNY3p1gPIg4cXPRiM7k6_SfXpw190ZRO7ac5Gs',
  qverisScript: path.join(__dirname, '../../skills/qveris-official/scripts/qveris_tool.mjs')
};

// 获取北京时间 (系统已是北京时间 CST +0800)
function getBeijingTime() {
  return new Date();
}

// 格式化日期 (使用本地时间，系统已是北京时间)
function formatDate(date, format = 'YYYY-MM-DD') {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');
  
  if (format === 'YYYY-MM-DD') return `${year}-${month}-${day}`;
  if (format === 'YYYY-MM-DD HH:mm:ss') return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  if (format === 'HH:mm') return `${hours}:${minutes}`;
  return `${year}-${month}-${day}`;
}

// 检查是否在交易时间内
function isInTradingHours(market) {
  const beijing = getBeijingTime();
  const timeStr = formatDate(beijing, 'HH:mm');
  const dayOfWeek = beijing.getDay();
  
  // 周末不交易
  if (dayOfWeek === 0 || dayOfWeek === 6) return false;
  
  const hours = CONFIG.tradingHours[market === 'A股' ? 'aStock' : 'hkStock'];
  
  const isInRange = (start, end) => {
    return timeStr >= start && timeStr <= end;
  };
  
  return isInRange(hours.morning.start, hours.morning.end) || 
         isInRange(hours.afternoon.start, hours.afternoon.end);
}

// 调用多数据源获取股票数据（优先新浪财经，备用QVeris）
async function fetchStockData(stocks) {
  return await fetchStockDataMultiSource(stocks);
}

// 技术分析
function analyzeStock(stockInfo, rawData) {
  const data = rawData.find(d => d.thscode === stockInfo.code);
  if (!data) return null;
  
  const analysis = {
    name: stockInfo.name,
    code: stockInfo.code,
    market: stockInfo.market,
    timestamp: data.time || formatDate(getBeijingTime(), 'YYYY-MM-DD HH:mm:ss'),
    price: {
      latest: data.latest || data.lastest_price,
      open: data.open,
      high: data.high,
      low: data.low,
      preClose: data.preClose,
      change: data.change,
      changeRatio: data.changeRatio,
      swing: data.swing
    },
    volume: {
      volume: data.volume,
      amount: data.amount,
      turnoverRatio: data.turnoverRatio,
      volRatio: data.vol_ratio
    },
    valuation: {
      pe_ttm: data.pe_ttm,
      pb: data.pb || data.pbr_lf,
      mv: data.mv
    },
    indicators: {},
    trend: {},
    recommendation: {}
  };
  
  // 技术指标计算
  analysis.indicators = {
    // 量价关系
    volumePriceTrend: analyzeVolumePrice(data),
    // 涨跌幅位置
    pricePosition: analyzePricePosition(data),
    // 委比分析
    committeeAnalysis: analyzeCommittee(data),
    // 振幅分析
    swingAnalysis: analyzeSwing(data)
  };
  
  // 趋势判断
  analysis.trend = determineTrend(analysis);
  
  // 买卖建议
  analysis.recommendation = generateRecommendation(analysis);
  
  return analysis;
}

// 量价关系分析
function analyzeVolumePrice(data) {
  const changeRatio = data.changeRatio || 0;
  const volRatio = data.vol_ratio || 1;
  
  if (changeRatio > 0 && volRatio > 1) {
    return { signal: '放量上涨', score: 3, description: '量价配合良好，买盘积极' };
  } else if (changeRatio > 0 && volRatio < 1) {
    return { signal: '缩量上涨', score: 1, description: '上涨但成交萎缩，需警惕' };
  } else if (changeRatio < 0 && volRatio > 1) {
    return { signal: '放量下跌', score: -2, description: '下跌放量，抛压较重' };
  } else if (changeRatio < 0 && volRatio < 1) {
    return { signal: '缩量下跌', score: -1, description: '下跌但成交萎缩，观望为主' };
  } else {
    return { signal: '横盘整理', score: 0, description: '量价平稳，等待方向选择' };
  }
}

// 涨跌幅位置分析
function analyzePricePosition(data) {
  const changeRatio = data.changeRatio || 0;
  const swing = data.swing || 0;
  
  if (changeRatio > 5) {
    return { position: '强势上涨', score: 3, risk: '高' };
  } else if (changeRatio > 2) {
    return { position: '稳健上涨', score: 2, risk: '中' };
  } else if (changeRatio > 0) {
    return { position: '小幅上涨', score: 1, risk: '低' };
  } else if (changeRatio > -2) {
    return { position: '小幅下跌', score: -1, risk: '低' };
  } else if (changeRatio > -5) {
    return { position: '明显下跌', score: -2, risk: '中' };
  } else {
    return { position: '大幅下跌', score: -3, risk: '高' };
  }
}

// 委比分析
function analyzeCommittee(data) {
  const committee = data.committee || 0;
  
  if (committee > 30) {
    return { signal: '买盘强劲', score: 2, description: `委比${committee.toFixed(2)}%，买盘明显占优` };
  } else if (committee > 10) {
    return { signal: '买盘占优', score: 1, description: `委比${committee.toFixed(2)}%，买盘略占优` };
  } else if (committee > -10) {
    return { signal: '买卖均衡', score: 0, description: `委比${committee.toFixed(2)}%，多空相对平衡` };
  } else if (committee > -30) {
    return { signal: '卖盘占优', score: -1, description: `委比${committee.toFixed(2)}%，卖盘略占优` };
  } else {
    return { signal: '卖压较重', score: -2, description: `委比${committee.toFixed(2)}%，卖盘明显占优` };
  }
}

// 振幅分析
function analyzeSwing(data) {
  const swing = data.swing || 0;
  
  if (swing > 5) {
    return { level: '剧烈波动', score: -1, description: `振幅${swing.toFixed(2)}%，波动剧烈，风险较高` };
  } else if (swing > 3) {
    return { level: '大幅波动', score: 0, description: `振幅${swing.toFixed(2)}%，波动较大，关注方向` };
  } else if (swing > 1.5) {
    return { level: '正常波动', score: 1, description: `振幅${swing.toFixed(2)}%，波动正常` };
  } else {
    return { level: '波动较小', score: 0, description: `振幅${swing.toFixed(2)}%，交投清淡` };
  }
}

// 趋势判断
function determineTrend(analysis) {
  const scores = [
    analysis.indicators.volumePriceTrend.score,
    analysis.indicators.pricePosition.score,
    analysis.indicators.committeeAnalysis.score,
    analysis.indicators.swingAnalysis.score
  ];
  
  const totalScore = scores.reduce((a, b) => a + b, 0);
  
  if (totalScore >= 5) {
    return { direction: '强势上涨', confidence: '高', score: totalScore };
  } else if (totalScore >= 3) {
    return { direction: '上涨', confidence: '中高', score: totalScore };
  } else if (totalScore >= 1) {
    return { direction: '偏强', confidence: '中', score: totalScore };
  } else if (totalScore >= -1) {
    return { direction: '震荡', confidence: '中', score: totalScore };
  } else if (totalScore >= -3) {
    return { direction: '偏弱', confidence: '中', score: totalScore };
  } else if (totalScore >= -5) {
    return { direction: '下跌', confidence: '中高', score: totalScore };
  } else {
    return { direction: '弱势下跌', confidence: '高', score: totalScore };
  }
}

// 买卖建议
function generateRecommendation(analysis) {
  const trend = analysis.trend;
  const price = analysis.price;
  const indicators = analysis.indicators;
  
  let action = '观望';
  let reason = '';
  let riskLevel = '中';
  let confidence = 0;
  
  if (trend.score >= 4) {
    if (indicators.pricePosition.risk === '高') {
      action = '谨慎持有';
      reason = '涨幅较大，建议设好止盈位，可适当减仓';
      riskLevel = '高';
      confidence = 70;
    } else {
      action = '持有/逢低加仓';
      reason = '趋势向好，量价配合，可考虑逢低加仓';
      riskLevel = '低';
      confidence = 80;
    }
  } else if (trend.score >= 2) {
    action = '持有';
    reason = '走势偏强，可继续持有观察';
    riskLevel = '低';
    confidence = 70;
  } else if (trend.score >= 0) {
    action = '观望';
    reason = '方向不明，建议等待明确信号';
    riskLevel = '中';
    confidence = 60;
  } else if (trend.score >= -2) {
    action = '谨慎观望';
    reason = '走势偏弱，暂不急于抄底';
    riskLevel = '中';
    confidence = 65;
  } else if (trend.score >= -4) {
    action = '减仓';
    reason = '下跌趋势明显，建议减仓或止损';
    riskLevel = '高';
    confidence = 75;
  } else {
    action = '止损';
    reason = '弱势下跌，建议及时止损离场';
    riskLevel = '高';
    confidence = 80;
  }
  
  // 特殊情况判断
  if (price.changeRatio > 0 && price.changeRatio < 1 && indicators.volumePriceTrend.signal === '缩量上涨') {
    action = '高抛低吸';
    reason = '缩量上涨动力不足，可考虑高抛低吸操作';
    confidence = 60;
  }
  
  return {
    action,
    reason,
    riskLevel,
    confidence
  };
}

// 保存数据
function saveData(analysisList) {
  const beijing = getBeijingTime();
  const dateStr = formatDate(beijing, 'YYYY-MM-DD');
  const timeStr = formatDate(beijing, 'YYYY-MM-DD HH:mm:ss');
  
  // 确保目录存在
  if (!fs.existsSync(CONFIG.dataDir)) {
    fs.mkdirSync(CONFIG.dataDir, { recursive: true });
  }
  
  // 按日期保存数据
  const dailyFile = path.join(CONFIG.dataDir, `${dateStr}.json`);
  let dailyData = { date: dateStr, records: [] };
  
  if (fs.existsSync(dailyFile)) {
    dailyData = JSON.parse(fs.readFileSync(dailyFile, 'utf-8'));
  }
  
  dailyData.records.push({
    time: timeStr,
    stocks: analysisList
  });
  
  fs.writeFileSync(dailyFile, JSON.stringify(dailyData, null, 2));
  
  // 清理过期数据
  cleanupOldData();
  
  console.log(`Data saved to ${dailyFile}`);
}

// 清理过期数据
function cleanupOldData() {
  const cutoffDate = new Date(getBeijingTime());
  cutoffDate.setDate(cutoffDate.getDate() - CONFIG.retentionDays);
  const cutoffStr = formatDate(cutoffDate, 'YYYY-MM-DD');
  
  if (!fs.existsSync(CONFIG.dataDir)) return;
  
  const files = fs.readdirSync(CONFIG.dataDir);
  files.forEach(file => {
    const match = file.match(/(\d{4}-\d{2}-\d{2})\.json/);
    if (match && match[1] < cutoffStr) {
      fs.unlinkSync(path.join(CONFIG.dataDir, file));
      console.log(`Deleted old data file: ${file}`);
    }
  });
}

// 生成报告
function generateReport(analysisList) {
  const beijing = getBeijingTime();
  const timeStr = formatDate(beijing, 'YYYY-MM-DD HH:mm:ss');
  
  let report = `📊 **盯盘报告** ${timeStr} (北京时间)\n\n`;
  report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  
  for (const stock of analysisList) {
    const trendEmoji = stock.trend.score >= 2 ? '📈' : (stock.trend.score <= -2 ? '📉' : '➡️');
    const actionEmoji = stock.recommendation.action.includes('持有') ? '🟢' : 
                       (stock.recommendation.action.includes('减仓') || stock.recommendation.action.includes('止损') ? '🔴' : '🟡');
    
    report += `### ${trendEmoji} ${stock.name} (${stock.code})\n\n`;
    report += `**实时行情**\n`;
    report += `| 指标 | 数值 |\n`;
    report += `|------|------|\n`;
    const formatNum = (val, decimals = 2, prefix = '¥') => {
      if (val === null || val === undefined || isNaN(val)) return '-';
      return `${prefix}${val.toFixed(decimals)}`;
    };
    const formatPercent = (val, decimals = 2) => {
      if (val === null || val === undefined || isNaN(val)) return '-';
      return `${val >= 0 ? '+' : ''}${val.toFixed(decimals)}%`;
    };
    
    report += `| 最新价 | ${formatNum(stock.price.latest)} |\n`;
    report += `| 涨跌幅 | ${formatPercent(stock.price.changeRatio)} |\n`;
    const changeVal = stock.price.change;
    report += `| 涨跌额 | ${changeVal != null ? (changeVal >= 0 ? '+' : '') + formatNum(changeVal, 2, '¥') : '-'} |\n`;
    report += `| 今开/昨收 | ${formatNum(stock.price.open)} / ${formatNum(stock.price.preClose)} |\n`;
    report += `| 最高/最低 | ${formatNum(stock.price.high)} / ${formatNum(stock.price.low)} |\n`;
    report += `| 振幅 | ${stock.price.swing != null ? stock.price.swing.toFixed(2) + '%' : '-'} |\n`;
    report += `| 成交额 | ${stock.volume.amount ? '¥' + (stock.volume.amount / 100000000).toFixed(2) + '亿' : '-'} |\n`;
    report += `| 换手率 | ${stock.volume.turnoverRatio != null ? stock.volume.turnoverRatio.toFixed(2) + '%' : '-'} |\n`;
    report += `| 量比 | ${stock.volume.volRatio != null ? stock.volume.volRatio.toFixed(2) : '-'} |\n`;
    
    if (stock.valuation.pe_ttm) {
      report += `| 市盈率(TTM) | ${stock.valuation.pe_ttm.toFixed(2)}倍 |\n`;
    }
    if (stock.valuation.pb) {
      report += `| 市净率 | ${stock.valuation.pb.toFixed(2)}倍 |\n`;
    }
    
    report += `\n**技术分析**\n`;
    report += `- 量价关系: ${stock.indicators.volumePriceTrend.signal} (${stock.indicators.volumePriceTrend.description})\n`;
    report += `- 涨跌位置: ${stock.indicators.pricePosition.position} (风险: ${stock.indicators.pricePosition.risk})\n`;
    report += `- 委比分析: ${stock.indicators.committeeAnalysis.signal} - ${stock.indicators.committeeAnalysis.description}\n`;
    report += `- 振幅分析: ${stock.indicators.swingAnalysis.level} - ${stock.indicators.swingAnalysis.description}\n`;
    
    report += `\n**趋势判断**: ${stock.trend.direction} (信心度: ${stock.trend.confidence})\n`;
    
    report += `\n**${actionEmoji} 操作建议**: ${stock.recommendation.action}\n`;
    report += `> ${stock.recommendation.reason}\n`;
    report += `> 风险等级: ${stock.recommendation.riskLevel} | 信心度: ${stock.recommendation.confidence}%\n`;
    
    report += `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  }
  
  // 汇总建议
  report += `### 📋 今日汇总\n\n`;
  const buyStocks = analysisList.filter(s => s.recommendation.action.includes('加仓') || s.recommendation.action.includes('持有'));
  const sellStocks = analysisList.filter(s => s.recommendation.action.includes('减仓') || s.recommendation.action.includes('止损'));
  const holdStocks = analysisList.filter(s => s.recommendation.action === '观望');
  
  if (buyStocks.length > 0) {
    report += `**可关注**: ${buyStocks.map(s => s.name).join('、')}\n`;
  }
  if (holdStocks.length > 0) {
    report += `**观望**: ${holdStocks.map(s => s.name).join('、')}\n`;
  }
  if (sellStocks.length > 0) {
    report += `**需警惕**: ${sellStocks.map(s => s.name).join('、')}\n`;
  }
  
  return report;
}

// 主函数
async function main() {
  console.log('='.repeat(50));
  console.log('盯盘系统启动');
  console.log('北京时间:', formatDate(getBeijingTime(), 'YYYY-MM-DD HH:mm:ss'));
  console.log('='.repeat(50));
  
  // 检查交易时间
  const beijing = getBeijingTime();
  const dayOfWeek = beijing.getDay();
  
  if (dayOfWeek === 0 || dayOfWeek === 6) {
    console.log('⚠️  今日为周末，非交易日');
    return;
  }
  
  // 获取A股数据
  console.log('\n获取A股数据...');
  const aStockData = await fetchStockData(CONFIG.aStocks);
  
  // 获取港股数据
  console.log('获取港股数据...');
  const hkStockData = await fetchStockData(CONFIG.hkStocks);
  
  // 分析数据
  console.log('\n分析数据...');
  const analysisList = [];
  
  for (const stock of CONFIG.aStocks) {
    const analysis = analyzeStock(stock, aStockData);
    if (analysis && analysis.price && analysis.price.latest != null) {
      analysisList.push(analysis);
      const priceStr = analysis.price.latest.toFixed(2);
      const changeStr = analysis.price.changeRatio != null 
        ? `${analysis.price.changeRatio >= 0 ? '+' : ''}${analysis.price.changeRatio.toFixed(2)}%`
        : 'N/A';
      console.log(`  ✓ ${stock.name}: ¥${priceStr} (${changeStr})`);
    } else {
      console.log(`  ⚠ ${stock.name}: 数据获取失败`);
    }
  }
  
  for (const stock of CONFIG.hkStocks) {
    const analysis = analyzeStock(stock, hkStockData);
    if (analysis && analysis.price && analysis.price.latest != null) {
      analysisList.push(analysis);
      const priceStr = analysis.price.latest.toFixed(2);
      const changeStr = analysis.price.changeRatio != null 
        ? `${analysis.price.changeRatio >= 0 ? '+' : ''}${analysis.price.changeRatio.toFixed(2)}%`
        : 'N/A';
      console.log(`  ✓ ${stock.name}: HK$${priceStr} (${changeStr})`);
    } else {
      console.log(`  ⚠ ${stock.name}: 数据获取失败`);
    }
  }
  
  // 保存数据
  if (analysisList.length > 0) {
    saveData(analysisList);
    
    // 生成报告
    const report = generateReport(analysisList);
    
    // 保存报告
    if (!fs.existsSync(CONFIG.reportsDir)) {
      fs.mkdirSync(CONFIG.reportsDir, { recursive: true });
    }
    const reportFile = path.join(CONFIG.reportsDir, `report_${formatDate(getBeijingTime(), 'YYYY-MM-DD_HHmmss')}.md`);
    fs.writeFileSync(reportFile, report);
    console.log(`\n报告已保存: ${reportFile}`);
    
    // 输出报告
    console.log('\n' + '='.repeat(50));
    console.log(report);
  } else {
    console.log('⚠️  未获取到任何股票数据');
  }
}

// 运行
main().catch(console.error);