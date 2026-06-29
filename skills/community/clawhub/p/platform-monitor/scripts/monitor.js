#!/usr/bin/env node
/**
 * platform-monitor - AI Skill 版
 * 输出 JSON，方便 AI 解析
 * 
 * 用法:
 *   node monitor.js               # 输出文本（人类可读）
 *   node monitor.js --json        # 输出 JSON（AI 解析）
 *   node monitor.js --platforms 支付宝A2A 豆包  # 指定平台
 */

'use strict';

const https = require('https');
const http  = require('http');
const fs    = require('fs');
const path  = require('path');

// ── 内置平台列表 ──────────────────────────────────────────────────
const BUILTIN_PLATFORMS = [
  { name: '支付宝A2A', url: 'https://a2a.alipay.com', keyword: '支付宝' },
  { name: '支付宝AI付', url: 'https://aipay.alipay.com', keyword: '支付宝' },
  { name: '扣子Bot商店', url: 'https://www.coze.cn/store', keyword: '扣子' },
  { name: '百度文心', url: 'https://agents.baidu.com', keyword: '百度' },
  { name: '闲鱼', url: 'https://www.taobao.com', keyword: '淘宝' },
  { name: '豆包', url: 'https://www.doubao.com', keyword: '' },
  { name: 'Kimi', url: 'https://kimi.moonshot.cn', keyword: '' },
  { name: '通义千问', url: 'https://tongyi.aliyun.com', keyword: '通义' },
  { name: '天工AI', url: 'https://www.tiangong.cn', keyword: '天工' },
  { name: '智谱AI', url: 'https://open.bigmodel.cn', keyword: '智谱' }
];

// ── 配置文件 ──────────────────────────────────────────────────────
const CONFIG_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.platform-monitor-config.json');
const HISTORY_FILE = path.join(__dirname, 'platform_monitor_history.json');
const TREND_FILE = path.join(__dirname, 'platform_monitor_trends.json');

// ── 报告生成 ──────────────────────────────────────────────────────
// 生成每日报告
function generateDailyReport(date = new Date().toISOString().split('T')[0]) {
  const history = loadHistory(1000);
  
  // 筛选指定日期的记录
  const dayHistory = history.filter(h => h.timestamp.startsWith(date));
  
  if (dayHistory.length === 0) {
    return { date, totalChecks: 0, message: '当天无监控记录' };
  }
  
  // 统计
  const allPlatforms = dayHistory.flatMap(h => h.platforms);
  const platformStats = {};
  
  for (const p of allPlatforms) {
    if (!platformStats[p.name]) {
      platformStats[p.name] = {
        name: p.name,
        upCount: 0,
        downCount: 0,
        totalResponseTime: 0,
        count: 0
      };
    }
    
    const stat = platformStats[p.name];
    stat.count++;
    if (p.status === 'UP') stat.upCount++;
    else stat.downCount++;
    stat.totalResponseTime += p.responseTimeMs;
  }
  
  // 生成报告
  const report = {
    date,
    totalChecks: dayHistory.length,
    platformCount: Object.keys(platformStats).length,
    platforms: Object.values(platformStats).map(s => ({
      name: s.name,
      availability: Math.round(s.upCount / s.count * 100) + '%',
      avgResponseTime: Math.round(s.totalResponseTime / s.count),
      downCount: s.downCount
    })),
    summary: ''
  };
  
  report.summary = `日期: ${date}\n监控次数: ${report.totalChecks}\n平台数: ${report.platformCount}\n`; 
  
  return report;
}

// 生成每周报告
function generateWeeklyReport(weekOffset = 0) {
  const now = new Date();
  now.setDate(now.getDate() + weekOffset * 7);
  const dayOfWeek = now.getDay();
  const monday = new Date(now);
  monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
  
  const weekStart = monday.toISOString().split('T')[0];
  const weekEnd = new Date(monday);
  weekEnd.setDate(monday.getDate() + 6);
  
  const history = loadHistory(1000);
  const weekHistory = history.filter(h => {
    const d = h.timestamp.split('T')[0];
    return d >= weekStart && d <= weekEnd.toISOString().split('T')[0];
  });
  
  if (weekHistory.length === 0) {
    return { weekStart, weekEnd: weekEnd.toISOString().split('T')[0], totalChecks: 0, message: '当周无监控记录' };
  }
  
  // 统计（类似每日报告，但按平台汇总）
  const allPlatforms = weekHistory.flatMap(h => h.platforms);
  const platformStats = {};
  
  for (const p of allPlatforms) {
    if (!platformStats[p.name]) {
      platformStats[p.name] = {
        name: p.name,
        upCount: 0,
        downCount: 0,
        totalResponseTime: 0,
        count: 0
      };
    }
    
    const stat = platformStats[p.name];
    stat.count++;
    if (p.status === 'UP') stat.upCount++;
    else stat.downCount++;
    stat.totalResponseTime += p.responseTimeMs;
  }
  
  const report = {
    weekStart,
    weekEnd: weekEnd.toISOString().split('T')[0],
    totalChecks: weekHistory.length,
    platformCount: Object.keys(platformStats).length,
    platforms: Object.values(platformStats).map(s => ({
      name: s.name,
      availability: Math.round(s.upCount / s.count * 100) + '%',
      avgResponseTime: Math.round(s.totalResponseTime / s.count),
      downCount: s.downCount
    })),
    summary: ''
  };
  
  report.summary = `周期: ${weekStart} ~ ${report.weekEnd}\n监控次数: ${report.totalChecks}\n平台数: ${report.platformCount}\n`;
  
  return report;
}

// ── 报告生成 ──────────────────────────────────────────────────────
// 生成每日报告
function generateDailyReport(date = new Date().toISOString().split('T')[0]) {
  const history = loadHistory(1000);
  
  // 筛选指定日期的记录
  const dayHistory = history.filter(h => h.timestamp.startsWith(date));
  
  if (dayHistory.length === 0) {
    return { date, totalChecks: 0, platforms: [], summary: '当天无监控记录' };
  }
  
  // 统计
  const allPlatforms = dayHistory.flatMap(h => h.platforms);
  const platformStats = {};
  
  for (const p of allPlatforms) {
    if (!platformStats[p.name]) {
      platformStats[p.name] = {
        name: p.name,
        upCount: 0,
        downCount: 0,
        totalResponseTime: 0,
        count: 0
      };
    }
    
    const stat = platformStats[p.name];
    stat.count++;
    if (p.status === 'UP') stat.upCount++;
    else stat.downCount++;
    stat.totalResponseTime += p.responseTimeMs;
  }
  
  // 生成报告
  const report = {
    date,
    totalChecks: dayHistory.length,
    platformCount: Object.keys(platformStats).length,
    platforms: Object.values(platformStats).map(s => ({
      name: s.name,
      availability: Math.round(s.upCount / s.count * 100) + '%',
      avgResponseTime: Math.round(s.totalResponseTime / s.count),
      downCount: s.downCount
    })),
    summary: `日期: ${date}\n监控次数: ${dayHistory.length}\n平台数: ${Object.keys(platformStats).length}\n`
  };
  
  return report;
}

// 生成每周报告
function generateWeeklyReport(weekOffset = 0) {
  const now = new Date();
  now.setDate(now.getDate() + weekOffset * 7);
  const dayOfWeek = now.getDay();
  const monday = new Date(now);
  monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
  
  const weekStart = monday.toISOString().split('T')[0];
  const weekEnd = new Date(monday);
  weekEnd.setDate(monday.getDate() + 6);
  
  const history = loadHistory(1000);
  const weekHistory = history.filter(h => {
    const d = h.timestamp.split('T')[0];
    return d >= weekStart && d <= weekEnd.toISOString().split('T')[0];
  });
  
  if (weekHistory.length === 0) {
    return { weekStart, weekEnd: weekEnd.toISOString().split('T')[0], totalChecks: 0, platforms: [], summary: '当周无监控记录' };
  }
  
  // 统计（类似每日报告）
  const allPlatforms = weekHistory.flatMap(h => h.platforms);
  const platformStats = {};
  
  for (const p of allPlatforms) {
    if (!platformStats[p.name]) {
      platformStats[p.name] = {
        name: p.name,
        upCount: 0,
        downCount: 0,
        totalResponseTime: 0,
        count: 0
      };
    }
    
    const stat = platformStats[p.name];
    stat.count++;
    if (p.status === 'UP') stat.upCount++;
    else stat.downCount++;
    stat.totalResponseTime += p.responseTimeMs;
  }
  
  const report = {
    weekStart,
    weekEnd: weekEnd.toISOString().split('T')[0],
    totalChecks: weekHistory.length,
    platformCount: Object.keys(platformStats).length,
    platforms: Object.values(platformStats).map(s => ({
      name: s.name,
      availability: Math.round(s.upCount / s.count * 100) + '%',
      avgResponseTime: Math.round(s.totalResponseTime / s.count),
      downCount: s.downCount
    })),
    summary: `周期: ${weekStart} ~ ${report.weekEnd}\n监控次数: ${weekHistory.length}\n平台数: ${Object.keys(platformStats).length}\n`
  };
  
  return report;
}

// ── 历史记录 ──────────────────────────────────────────────────────
// 保存监控结果到历史文件
function saveHistory(results) {
  const timestamp = new Date().toISOString();
  const entry = {
    timestamp,
    platforms: results
  };
  
  let history = [];
  try {
    if (fs.existsSync(HISTORY_FILE)) {
      history = JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf8'));
    }
  } catch (e) {
    history = [];
  }
  
  history.push(entry);
  
  // 只保留最近 1000 条记录
  if (history.length > 1000) {
    history = history.slice(-1000);
  }
  
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2), 'utf8');
  return entry;
}

// 读取历史记录
function loadHistory(limit = 100) {
  try {
    if (fs.existsSync(HISTORY_FILE)) {
      const history = JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf8'));
      return history.slice(-limit);
    }
  } catch (e) {}
  return [];
}

// 分析趋势
function analyzeTrends(platformName, history) {
  const platformHistory = history
    .flatMap(h => h.platforms)
    .filter(p => p.name === platformName)
    .slice(-30); // 最近30次
  
  if (platformHistory.length < 5) {
    return { hasTrend: false, message: '数据不足，需要至少5次监控记录' };
  }
  
  const responseTimes = platformHistory.map(p => p.responseTimeMs);
  const avgResponseTime = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;
  const latestResponseTime = responseTimes[responseTimes.length - 1];
  
  // 检测趋势
  const trend = {
    platform: platformName,
    avgResponseTime: Math.round(avgResponseTime),
    latestResponseTime,
    changePercent: Math.round((latestResponseTime - avgResponseTime) / avgResponseTime * 100),
    statusHistory: platformHistory.slice(-10).map(p => p.status),
    recommendation: ''
  };
  
  // 生成建议
  if (trend.changePercent > 50) {
    trend.recommendation = '⚠️ 响应时间明显变慢，建议检查网络或服务器';
  } else if (trend.changePercent < -20) {
    trend.recommendation = '✅ 响应时间有所改善';
  } else {
    trend.recommendation = '✅ 响应时间稳定';
  }
  
  // 检查是否有频繁宕机
  const downCount = trend.statusHistory.filter(s => s === 'DOWN').length;
  if (downCount >= 3) {
    trend.recommendation += '；⚠️ 近期多次宕机，建议重点监控';
  }
  
  trend.hasTrend = true;
  return trend;
}

// ── 智能建议 ──────────────────────────────────────────────────────
// 基于历史数据和趋势分析，生成智能建议
function generateSuggestions(platformName, history) {
  const trend = analyzeTrends(platformName, history);
  
  if (!trend.hasTrend) {
    return { platform: platformName, suggestions: ['数据不足，需要至少5次监控记录'] };
  }
  
  const suggestions = [];
  
  // 1. 响应时间建议
  if (trend.changePercent > 50) {
    suggestions.push('⚠️ 响应时间明显变慢（+50%），建议：');
    suggestions.push('  • 检查服务器负载');
    suggestions.push('  • 检查网络延迟');
    suggestions.push('  • 考虑切换CDN或优化资源');
  } else if (trend.changePercent > 20) {
    suggestions.push('⚠️ 响应时间有所变慢（+20%），建议关注');
  } else if (trend.changePercent < -30) {
    suggestions.push('✅ 响应时间显著改善（-30%），继续保持');
  }
  
  // 2. 可用性建议
  const platformHistory = history
    .flatMap(h => h.platforms)
    .filter(p => p.name === platformName)
    .slice(-30);
  
  const downCount = platformHistory.filter(p => p.status === 'DOWN').length;
  const upCount = platformHistory.filter(p => p.status === 'UP').length;
  const availability = upCount / platformHistory.length * 100;
  
  if (availability < 95) {
    suggestions.push(`⚠️ 可用性较低（${availability.toFixed(1)}%），建议：`);
    suggestions.push('  • 检查服务器稳定性');
    suggestions.push('  • 联系服务商排查');
    suggestions.push('  • 考虑备用方案');
  } else if (availability < 99) {
    suggestions.push(`⚠️ 可用性有提升空间（${availability.toFixed(1)}%），建议持续关注`);
  } else {
    suggestions.push(`✅ 可用性良好（${availability.toFixed(1)}%）`);
  }
  
  // 3. 关键词检测建议
  const keywordMissing = platformHistory.filter(p => p.keywordFound === false).length;
  if (keywordMissing > 0) {
    suggestions.push(`⚠️ 关键词缺失 ${keywordMissing} 次，页面内容可能发生变化，建议检查：`);
    suggestions.push('  • 页面结构是否改变');
    suggestions.push('  • 关键词配置是否需要更新');
  }
  
  // 4. 综合建议
  if (downCount >= 3 && trend.changePercent > 20) {
    suggestions.push('🚨 综合评估：平台状态不佳，建议立即处理');
  } else if (downCount === 0 && trend.changePercent < 10) {
    suggestions.push('✅ 综合评估：平台状态良好，无需特殊处理');
  }
  
  return {
    platform: platformName,
    availability: availability.toFixed(1) + '%',
    avgResponseTime: trend.avgResponseTime + 'ms',
    latestResponseTime: trend.latestResponseTime + 'ms',
    changePercent: trend.changePercent + '%',
    downCount,
    suggestions
  };
}

// ── 配置文件 ──────────────────────────────────────────────────────
// 读取配置
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    }
  } catch (e) {}
  return { myPlatforms: {} };
}

// 保存配置
function saveConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf8');
}

// 添加"我的平台"
function addMyPlatform(name, url) {
  const config = loadConfig();
  config.myPlatforms[name] = url;
  saveConfig(config);
  return config;
}

// 查找"我的平台"
function findMyPlatform(name) {
  const config = loadConfig();
  // 精确匹配
  if (config.myPlatforms[name]) return config.myPlatforms[name];
  // 模糊匹配
  for (const key of Object.keys(config.myPlatforms)) {
    if (key.includes(name) || name.includes(key)) {
      return config.myPlatforms[key];
    }
  }
  return null;
}

// ── HTTP GET ──────────────────────────────────────────────────────
function httpGet(urlStr, timeoutMs = 15000) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const lib = url.protocol === 'https:' ? https : http;
    const req = lib.get(urlStr, { 
      timeout: timeoutMs,
      headers: { 'User-Agent': 'Mozilla/5.0 PlatformMonitor/2.0' }
    }, (res) => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        resolve({ 
          statusCode: res.statusCode, 
          body: Buffer.concat(chunks).toString('utf8') 
        });
      });
    });
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.on('error', reject);
  });
}

// ── 检测单个平台 ──────────────────────────────────────────────────
async function checkPlatform(platform) {
  const start = Date.now();
  try {
    const res = await httpGet(platform.url);
    const elapsed = Date.now() - start;
    const keywordFound = platform.keyword ? res.body.includes(platform.keyword) : true;
    
    return {
      name: platform.name,
      url: platform.url,
      status: res.statusCode >= 200 && res.statusCode < 400 && keywordFound ? 'UP' : 'DEGRADED',
      statusCode: res.statusCode,
      responseTimeMs: elapsed,
      keywordFound,
      error: null
    };
  } catch (e) {
    return {
      name: platform.name,
      url: platform.url,
      status: 'DOWN',
      statusCode: null,
      responseTimeMs: Date.now() - start,
      keywordFound: false,
      error: e.message
    };
  }
}

// ── 主函数 ──────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const outputJson = args.includes('--json');
  const reportType = args.includes('--report') ? args[args.indexOf('--report') + 1] : null;
  const exportType = args.includes('--export') ? args[args.indexOf('--export') + 1] : null;
  const importFile = args.includes('--import') ? args[args.indexOf('--import') + 1] : null;
  const exportConfig = args.includes('--export-config');
  const platformsToCheck = [];
  
  // 导出配置模式
  if (exportConfig) {
    const config = loadConfig();
    const csv = ['平台名称,URL'];
    for (const [name, url] of Object.entries(config.myPlatforms)) {
      csv.push(`"${name}","${url}"`);
    }
    
    const csvContent = csv.join('\n');
    
    if (outputJson) {
      console.log(JSON.stringify({ 
        action: 'export_config', 
        format: 'csv', 
        content: csvContent,
        platforms: config.myPlatforms 
      }, null, 2));
    } else {
      console.log('\n📤 配置导出 (CSV 格式)\n' + '='.repeat(50));
      console.log(csvContent);
      console.log('='.repeat(50) + '\n');
    }
    process.exit(0);
  }
  
  // 导入模式
  if (importFile) {
    try {
      const fs = require('fs');
      const csvContent = fs.readFileSync(importFile, 'utf8');
      const lines = csvContent.split('\n').slice(1); // 跳过表头
      
      const config = loadConfig();
      let imported = 0;
      
      for (const line of lines) {
        if (!line.trim()) continue;
        const match = line.match(/"([^"]+)","([^"]+)"/);
        if (match) {
          const [, name, url] = match;
          config.myPlatforms[name] = url;
          imported++;
        }
      }
      
      saveConfig(config);
      
      if (outputJson) {
        console.log(JSON.stringify({ 
          action: 'import', 
          imported, 
          platforms: config.myPlatforms 
        }, null, 2));
      } else {
        console.log(`\n✅ 成功导入 ${imported} 个平台\n`);
      }
      process.exit(0);
    } catch (e) {
      console.error('❌ 导入失败:', e.message);
      process.exit(1);
    }
  }
  
  // 导出模式
  if (exportType) {
    const history = loadHistory(1000);
    
    if (exportType === 'history') {
      // 导出历史记录
      const csv = ['时间戳,平台名称,状态,响应时间(ms),状态码,错误'];
      for (const entry of history) {
        for (const p of entry.platforms) {
          csv.push(`"${entry.timestamp}","${p.name}","${p.status}",${p.responseTimeMs},${p.statusCode || ''},"${p.error || ''}"`);
        }
      }
      
      if (outputJson) {
        console.log(JSON.stringify({ 
          action: 'export', 
          type: 'history',
          format: 'csv', 
          content: csv.join('\n') 
        }, null, 2));
      } else {
        console.log('\n📤 历史记录导出 (CSV 格式)\n' + '='.repeat(50));
        console.log(csv.join('\n'));
        console.log('='.repeat(50) + '\n');
      }
      process.exit(0);
    } else if (exportType === 'trends') {
      // 导出趋势分析
      const trends = [];
      const platforms = [...BUILTIN_PLATFORMS.map(p => p.name), ...Object.keys(loadConfig().myPlatforms)];
      const uniquePlatforms = [...new Set(platforms)];
      
      for (const platformName of uniquePlatforms) {
        const trend = analyzeTrends(platformName, history);
        if (trend.hasTrend) {
          trends.push(trend);
        }
      }
      
      if (outputJson) {
        console.log(JSON.stringify({ 
          action: 'export', 
          type: 'trends',
          trends 
        }, null, 2));
      } else {
        console.log('\n📈 趋势分析导出\n' + '='.repeat(50));
        for (const t of trends) {
          console.log(`• ${t.platform}: 平均${t.avgResponseTime}ms, 最新${t.latestResponseTime}ms, 变化${t.changePercent}%`);
          console.log(`  ${t.recommendation}`);
        }
        console.log('='.repeat(50) + '\n');
      }
      process.exit(0);
    } else {
      console.error('❌ 导出类型不支持，请用: history 或 trends');
      process.exit(1);
    }
  }
  
  // 智能建议模式
  const suggestPlatform = args.includes('--suggest') ? args[args.indexOf('--suggest') + 1] : null;
  
  if (suggestPlatform) {
    const history = loadHistory(1000);
    const suggestion = generateSuggestions(suggestPlatform, history);
    
    if (outputJson) {
      console.log(JSON.stringify(suggestion, null, 2));
    } else {
      console.log('\n🤖 智能建议\n' + '='.repeat(50));
      console.log(`平台: ${suggestion.platform}`);
      console.log(`可用性: ${suggestion.availability}`);
      console.log(`平均响应: ${suggestion.avgResponseTime}`);
      console.log(`最新响应: ${suggestion.latestResponseTime} (${suggestion.changePercent})`);
      console.log(`宕机次数: ${suggestion.downCount}`);
      console.log('\n建议:');
      for (const s of suggestion.suggestions) {
        console.log(`  ${s}`);
      }
      console.log('='.repeat(50) + '\n');
    }
    process.exit(0);
  }
  
  // 报告模式
  if (reportType) {
    let report;
    const reportDate = args.includes('--date') ? args[args.indexOf('--date') + 1] : new Date().toISOString().split('T')[0];
    
    if (reportType === 'daily') {
      report = generateDailyReport(reportDate);
    } else if (reportType === 'weekly') {
      report = generateWeeklyReport();
    } else {
      console.error('❌ 报告类型不支持，请用: daily 或 weekly');
      process.exit(1);
    }
    
    if (outputJson) {
      console.log(JSON.stringify(report, null, 2));
    } else {
      console.log('\n📊 监控报告\n' + '='.repeat(50));
      console.log(report.summary);
      for (const p of report.platforms) {
        console.log(`• ${p.name}: 可用${p.availability}, 平均${p.avgResponseTime}ms, 异常${p.downCount}次`);
      }
      console.log('='.repeat(50) + '\n');
    }
    process.exit(0);
  }

  // 解析 --platforms 参数
  const platformIndex = args.indexOf('--platforms');
  if (platformIndex !== -1) {
    const names = args.slice(platformIndex + 1).filter(a => !a.startsWith('--'));
    for (const name of names) {
      const found = BUILTIN_PLATFORMS.find(p => p.name.includes(name));
      if (found) platformsToCheck.push(found);
    }
  }

  // 如果没有指定平台，用内置全部
  if (platformsToCheck.length === 0) {
    platformsToCheck.push(...BUILTIN_PLATFORMS);
  }

  // 检测
  const results = [];
  for (const plat of platformsToCheck) {
    const result = await checkPlatform(plat);
    results.push(result);
    await new Promise(r => setTimeout(r, 500)); // 避免请求过快
  }

  // 保存历史记录
  const historyEntry = saveHistory(results);

  // 输出
  if (outputJson) {
    const alerts = results.filter(r => r.status !== 'UP').map(r => `${r.name}: ${r.status}`);
    
    // 生成趋势分析
    const trends = results.map(r => analyzeTrends(r.name, loadHistory()));
    
    console.log(JSON.stringify({
      platforms: results,
      alerts,
      summary: `${results.length} 个平台, ${alerts.length} 个异常`,
      historyEntry: historyEntry.timestamp,
      trends: trends.filter(t => t.hasTrend)
    }, null, 2));
  } else {
    console.log('\n🚀 Platform Monitor - 检测结果\n' + '='.repeat(50));
    for (const r of results) {
      const icon = r.status === 'UP' ? '✅' : r.status === 'DOWN' ? '❌' : '⚠️';
      console.log(`${icon} ${r.name}: ${r.status} (${r.responseTimeMs}ms)`);
      if (r.error) console.log(`  错误: ${r.error}`);
    }
    const alertCount = results.filter(r => r.status !== 'UP').length;
    console.log('\n' + '='.repeat(50));
    console.log(`摘要: ${results.length} 个平台, ${alertCount} 个异常\n`);
  }

  process.exit(results.some(r => r.status !== 'UP') ? 1 : 0);
}

main().catch(e => {
  console.error('❌ 错误:', e.message);
  process.exit(1);
});
