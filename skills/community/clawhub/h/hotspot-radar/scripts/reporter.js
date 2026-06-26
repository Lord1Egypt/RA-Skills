/**
 * 热点雷达 - 报告生成器
 * 生成Markdown格式的全网热点日报
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  dataDir: path.join(__dirname, '../data'),
  historyDir: path.join(__dirname, '../data/history'),
  configDir: path.join(__dirname, '../config'),
};

// 格式化日期
function formatDate(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return year + '年' + month + '月' + day + '日';
}

// 格式化时间
function formatTime(date = new Date()) {
  const h = String(date.getHours()).padStart(2, '0');
  const m = String(date.getMinutes()).padStart(2, '0');
  const s = String(date.getSeconds()).padStart(2, '0');
  return h + ':' + m + ':' + s;
}

// 读取历史数据
function loadHistory(platform, daysAgo = 1) {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  const fileName = date.toISOString().split('T')[0] + '.json';
  const filePath = path.join(CONFIG.historyDir, platform, fileName);

  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
  } catch (e) {
    console.error('Read history failed [' + platform + '] [' + daysAgo + 'days ago]:', e.message);
  }
  return [];
}

// 读取监控配置
function loadMonitorConfig() {
  const configPath = path.join(CONFIG.configDir, 'monitor.json');
  try {
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    }
  } catch (e) {
    console.error('Read monitor config failed:', e.message);
  }
  return { keywords: [] };
}

// 生成平台热榜表格
function generatePlatformTable(platform, data, platformName) {
  if (!data || data.length === 0) {
    return '### ' + platformName + '\n> Data fetch failed\n';
  }

  let table = '### ' + platformName + '\n\n';
  table += '| Rank | Topic | HotValue | Label |\n';
  table += '|------|-------|----------|-------|\n';

  data.slice(0, 20).forEach(function(item) {
    table += '| ' + item.rank + ' | ' + item.topic + ' | ' + formatHotValue(item.hotValue) + ' | ' + (item.label || '-') + ' |\n';
  });

  return table;
}

// 格式化热度值
function formatHotValue(value) {
  if (value >= 100000000) {
    return (value / 100000000).toFixed(1) + 'yi';
  } else if (value >= 10000) {
    return (value / 10000).toFixed(1) + 'wan';
  }
  return value.toString();
}

// 趋势分析
function analyzeTrends(currentData) {
  const platforms = ['weibo', 'zhihu', 'bilibili', 'douyin', 'xiaohongshu'];
  const platformNames = { weibo: 'Weibo', zhihu: 'Zhihu', bilibili: 'Bilibili', douyin: 'Douyin', xiaohongshu: 'XHS' };

  const trends = {
    newTopics: [],
    risingTopics: [],
    fallingTopics: [],
    outTopics: []
  };

  platforms.forEach(function(platform) {
    const current = currentData[platform] || [];
    const yesterday = loadHistory(platform, 1);

    if (yesterday.length === 0) return;

    const yesterdayTopics = new Map(yesterday.map(function(item) { return [item.topic, item.rank]; }));

    current.forEach(function(item) {
      const prevRank = yesterdayTopics.get(item.topic);
      if (prevRank === undefined) {
        trends.newTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          currentRank: item.rank
        });
      } else if (item.rank < prevRank) {
        trends.risingTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          fromRank: prevRank,
          toRank: item.rank
        });
      } else if (item.rank > prevRank) {
        trends.fallingTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          fromRank: prevRank,
          toRank: item.rank
        });
      }
    });

    yesterday.forEach(function(item) {
      const stillExists = current.some(function(c) { return c.topic === item.topic; });
      if (!stillExists && item.rank <= 10) {
        trends.outTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          prevRank: item.rank
        });
      }
    });
  });

  return trends;
}

// 跨平台热点分析
function findCrossPlatformTopics(currentData) {
  const platforms = ['weibo', 'zhihu', 'bilibili', 'douyin', 'xiaohongshu'];
  const platformNames = { weibo: 'Weibo', zhihu: 'Zhihu', bilibili: 'Bilibili', douyin: 'Douyin', xiaohongshu: 'XHS' };

  const topicMap = new Map();

  platforms.forEach(function(platform) {
    const data = currentData[platform] || [];
    data.slice(0, 20).forEach(function(item) {
      const normalizedTopic = item.topic.toLowerCase().trim();
      if (!topicMap.has(normalizedTopic)) {
        topicMap.set(normalizedTopic, { topic: item.topic, platforms: [] });
      }
      topicMap.get(normalizedTopic).platforms.push(platformNames[platform]);
    });
  });

  const crossPlatform = [];
  topicMap.forEach(function(value) {
    if (value.platforms.length >= 2) {
      crossPlatform.push(value);
    }
  });

  crossPlatform.sort(function(a, b) { return b.platforms.length - a.platforms.length; });

  return crossPlatform.slice(0, 10);
}

// 话题监控检查
function checkMonitorKeywords(currentData) {
  const config = loadMonitorConfig();
  if (!config.keywords || config.keywords.length === 0) {
    return [];
  }

  const platforms = ['weibo', 'zhihu', 'bilibili', 'douyin', 'xiaohongshu'];
  const platformNames = { weibo: 'Weibo', zhihu: 'Zhihu', bilibili: 'Bilibili', douyin: 'Douyin', xiaohongshu: 'XHS' };
  const matches = [];

  platforms.forEach(function(platform) {
    const data = currentData[platform] || [];
    data.forEach(function(item) {
      const topicLower = item.topic.toLowerCase();
      config.keywords.forEach(function(keyword) {
        if (topicLower.includes(keyword.toLowerCase())) {
          matches.push({
            keyword: keyword,
            topic: item.topic,
            platform: platformNames[platform],
            rank: item.rank
          });
        }
      });
    });
  });

  return matches;
}

// 生成Markdown报告
function generateReport(currentData) {
  const today = new Date();
  const dateStr = formatDate(today);
  const timeStr = formatTime(today);

  const totalTopics = {
    weibo: currentData.weibo ? currentData.weibo.length : 0,
    zhihu: currentData.zhihu ? currentData.zhihu.length : 0,
    bilibili: currentData.bilibili ? currentData.bilibili.length : 0,
    douyin: currentData.douyin ? currentData.douyin.length : 0,
    xiaohongshu: currentData.xiaohongshu ? currentData.xiaohongshu.length : 0
  };

  const trends = analyzeTrends(currentData);
  const crossPlatform = findCrossPlatformTopics(currentData);
  const monitorMatches = checkMonitorKeywords(currentData);

  let report = '# [HOT] Daily Hotspot Report | ' + dateStr + '\n\n';
  report += '> Generated: ' + dateStr + ' ' + timeStr + '\n\n';
  report += '## Stats Summary\n\n';
  report += '| Platform | Count | Status |\n';
  report += '|----------|-------|--------|\n';
  report += '| Weibo | ' + totalTopics.weibo + ' | ' + (totalTopics.weibo > 0 ? 'OK' : 'Failed') + ' |\n';
  report += '| Zhihu | ' + totalTopics.zhihu + ' | ' + (totalTopics.zhihu > 0 ? 'OK' : 'Failed') + ' |\n';
  report += '| Bilibili | ' + totalTopics.bilibili + ' | ' + (totalTopics.bilibili > 0 ? 'OK' : 'Failed') + ' |\n';
  report += '| Douyin | ' + totalTopics.douyin + ' | ' + (totalTopics.douyin > 0 ? 'OK' : 'Failed') + ' |\n';
  report += '| Xiaohongshu | ' + totalTopics.xiaohongshu + ' | ' + (totalTopics.xiaohongshu > 0 ? 'OK' : 'Failed') + ' |\n\n';

  if (crossPlatform.length > 0) {
    report += '## Cross-Platform Hot Topics\n\n';
    crossPlatform.slice(0, 10).forEach(function(item, idx) {
      report += (idx + 1) + '. **' + item.topic + '** - Appears on ' + item.platforms.join(', ') + '\n';
    });
    report += '\n';
  }

  report += '## Platform Hot Lists\n\n';
  report += generatePlatformTable('weibo', currentData.weibo, 'Weibo Trending');
  report += '\n';
  report += generatePlatformTable('zhihu', currentData.zhihu, 'Zhihu Hot');
  report += '\n';
  report += generatePlatformTable('bilibili', currentData.bilibili, 'Bilibili Trending');
  report += '\n';
  report += generatePlatformTable('douyin', currentData.douyin, 'Douyin Trending');
  report += '\n';
  report += generatePlatformTable('xiaohongshu', currentData.xiaohongshu, 'Xiaohongshu Trending');
  report += '\n';

  report += '## Trend Analysis\n\n';

  if (trends.newTopics.length > 0) {
    report += '### NEW Entries\n\n';
    trends.newTopics.slice(0, 5).forEach(function(item) {
      report += '- **' + item.topic + '** - First time on list (' + item.platform + ' #' + item.currentRank + ')\n';
    });
    report += '\n';
  }

  if (trends.risingTopics.length > 0) {
    report += '### Rising\n\n';
    trends.risingTopics.slice(0, 5).forEach(function(item) {
      report += '- **' + item.topic + '** - #' + item.fromRank + ' -> #' + item.toRank + ' (' + item.platform + ')\n';
    });
    report += '\n';
  }

  if (trends.fallingTopics.length > 0) {
    report += '### Falling\n\n';
    trends.fallingTopics.slice(0, 5).forEach(function(item) {
      report += '- **' + item.topic + '** - #' + item.fromRank + ' -> #' + item.toRank + ' (' + item.platform + ')\n';
    });
    report += '\n';
  }

  if (trends.outTopics.length > 0) {
    report += '### Dropped Out\n\n';
    trends.outTopics.slice(0, 5).forEach(function(item) {
      report += '- **' + item.topic + '** - Was #' + item.prevRank + ', now out (' + item.platform + ')\n';
    });
    report += '\n';
  }

  if (monitorMatches.length > 0) {
    report += '## Monitor Alerts\n\n';
    report += '| Keyword | Topic | Platform | Rank |\n';
    report += '|---------|-------|----------|------|\n';
    monitorMatches.forEach(function(match) {
      report += '| ' + match.keyword + ' | ' + match.topic + ' | ' + match.platform + ' | #' + match.rank + ' |\n';
    });
    report += '\n';
  }

  report += '---\n\n';
  report += '*Generated by Hotspot Radar*\n';

  return report;
}

// 保存报告
function saveReport(report, fileName) {
  const today = new Date().toISOString().split('T')[0];
  const reportDir = path.join(CONFIG.dataDir, 'reports');

  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }

  const filePath = fileName || path.join(reportDir, today + '.md');
  fs.writeFileSync(filePath, report, 'utf-8');
  console.log('Report saved: ' + filePath);

  return filePath;
}

// 主函数
async function main() {
  const today = new Date().toISOString().split('T')[0];
  const snapshotPath = path.join(CONFIG.dataDir, 'trends', today + '.json');

  let currentData;
  if (fs.existsSync(snapshotPath)) {
    currentData = JSON.parse(fs.readFileSync(snapshotPath, 'utf-8'));
    console.log('Loaded today data: ' + snapshotPath);
  } else {
    console.log('Today data not found. Please run collector.js first.');
    process.exit(1);
  }

  const report = generateReport(currentData);
  const reportPath = saveReport(report);

  console.log('\nReport generated successfully');
  console.log(report);

  return { report: report, reportPath: reportPath };
}

module.exports = { generateReport: generateReport, saveReport: saveReport, formatDate: formatDate, loadMonitorConfig: loadMonitorConfig };

// Run directly
if (require.main === module) {
  main().catch(function(e) {
    console.error('Report generation failed:', e);
    process.exit(1);
  });
}
