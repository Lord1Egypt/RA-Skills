/**
 * 热点雷达 - HTML可视化报告生成器
 * 生成带图表的交互式HTML报告
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

// 格式化热度值
function formatHotValue(value) {
  if (value >= 100000000) {
    return (value / 100000000).toFixed(1) + '亿';
  } else if (value >= 10000) {
    return (value / 10000).toFixed(1) + '万';
  }
  return value.toString();
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

// 平台配置
const PLATFORMS = {
  weibo: { name: '微博', color: '#E6162D', bgColor: 'rgba(230,22,45,0.1)' },
  zhihu: { name: '知乎', color: '#0066FF', bgColor: 'rgba(0,102,255,0.1)' },
  bilibili: { name: 'B站', color: '#FB7299', bgColor: 'rgba(251,114,153,0.1)' },
  douyin: { name: '抖音', color: '#161823', bgColor: 'rgba(22,24,35,0.1)' },
  xiaohongshu: { name: '小红书', color: '#FF2442', bgColor: 'rgba(255,36,66,0.1)' },
};

// 趋势分析
function analyzeTrends(currentData) {
  const platforms = ['weibo', 'zhihu', 'bilibili', 'douyin', 'xiaohongshu'];
  const platformNames = { weibo: '微博', zhihu: '知乎', bilibili: 'B站', douyin: '抖音', xiaohongshu: '小红书' };

  const trends = {
    newTopics: [],
    risingTopics: [],
    fallingTopics: [],
    outTopics: [],
  };

  platforms.forEach(function (platform) {
    const current = currentData[platform] || [];
    const yesterday = loadHistory(platform, 1);

    if (yesterday.length === 0) return;

    const yesterdayTopics = new Map(yesterday.map(function (item) { return [item.topic, item.rank]; }));

    current.forEach(function (item) {
      const prevRank = yesterdayTopics.get(item.topic);
      if (prevRank === undefined) {
        trends.newTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          platformKey: platform,
          currentRank: item.rank,
          hotValue: item.hotValue,
        });
      } else if (item.rank < prevRank) {
        trends.risingTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          platformKey: platform,
          fromRank: prevRank,
          toRank: item.rank,
          delta: prevRank - item.rank,
          hotValue: item.hotValue,
        });
      } else if (item.rank > prevRank) {
        trends.fallingTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          platformKey: platform,
          fromRank: prevRank,
          toRank: item.rank,
          delta: item.rank - prevRank,
          hotValue: item.hotValue,
        });
      }
    });

    yesterday.forEach(function (item) {
      const stillExists = current.some(function (c) { return c.topic === item.topic; });
      if (!stillExists && item.rank <= 10) {
        trends.outTopics.push({
          topic: item.topic,
          platform: platformNames[platform],
          prevRank: item.rank,
        });
      }
    });
  });

  return trends;
}

// 跨平台热点分析
function findCrossPlatformTopics(currentData) {
  const platforms = ['weibo', 'zhihu', 'bilibili', 'douyin', 'xiaohongshu'];
  const platformNames = { weibo: '微博', zhihu: '知乎', bilibili: 'B站', douyin: '抖音', xiaohongshu: '小红书' };

  const topicMap = new Map();

  platforms.forEach(function (platform) {
    const data = currentData[platform] || [];
    data.slice(0, 20).forEach(function (item) {
      const normalizedTopic = item.topic.toLowerCase().trim();
      if (!topicMap.has(normalizedTopic)) {
        topicMap.set(normalizedTopic, { topic: item.topic, platforms: [], platformKeys: [] });
      }
      const entry = topicMap.get(normalizedTopic);
      if (!entry.platforms.includes(platformNames[platform])) {
        entry.platforms.push(platformNames[platform]);
        entry.platformKeys.push(platform);
      }
    });
  });

  const crossPlatform = [];
  topicMap.forEach(function (value) {
    if (value.platforms.length >= 2) {
      crossPlatform.push(value);
    }
  });

  crossPlatform.sort(function (a, b) { return b.platforms.length - a.platforms.length; });

  return crossPlatform.slice(0, 10);
}

// 话题监控检查
function checkMonitorKeywords(currentData) {
  const config = loadMonitorConfig();
  if (!config.keywords || config.keywords.length === 0) {
    return [];
  }

  const platforms = ['weibo', 'zhihu', 'bilibili', 'douyin', 'xiaohongshu'];
  const platformNames = { weibo: '微博', zhihu: '知乎', bilibili: 'B站', douyin: '抖音', xiaohongshu: '小红书' };
  const matches = [];

  platforms.forEach(function (platform) {
    const data = currentData[platform] || [];
    data.forEach(function (item) {
      const topicLower = item.topic.toLowerCase();
      config.keywords.forEach(function (keyword) {
        if (topicLower.includes(keyword.toLowerCase())) {
          matches.push({
            keyword: keyword,
            topic: item.topic,
            platform: platformNames[platform],
            platformKey: platform,
            rank: item.rank,
            hotValue: item.hotValue,
          });
        }
      });
    });
  });

  return matches;
}

// 生成HTML报告
function generateHtmlReport(currentData) {
  const today = new Date();
  const dateStr = formatDate(today);
  const timeStr = formatTime(today);
  const timestamp = today.toISOString();

  const counts = {
    weibo: currentData.weibo ? currentData.weibo.length : 0,
    zhihu: currentData.zhihu ? currentData.zhihu.length : 0,
    bilibili: currentData.bilibili ? currentData.bilibili.length : 0,
    douyin: currentData.douyin ? currentData.douyin.length : 0,
    xiaohongshu: currentData.xiaohongshu ? currentData.xiaohongshu.length : 0,
  };

  const trends = analyzeTrends(currentData);
  const crossPlatform = findCrossPlatformTopics(currentData);
  const monitorMatches = checkMonitorKeywords(currentData);

  // 构建平台数据JS
  const platformDataJson = JSON.stringify({
    weibo: (currentData.weibo || []).slice(0, 10),
    zhihu: (currentData.zhihu || []).slice(0, 10),
    bilibili: (currentData.bilibili || []).slice(0, 10),
    douyin: (currentData.douyin || []).slice(0, 10),
    xiaohongshu: (currentData.xiaohongshu || []).slice(0, 10),
  });

  // 跨平台数据
  const crossPlatformJson = JSON.stringify(crossPlatform);

  // 趋势数据
  const trendsJson = JSON.stringify({
    new: trends.newTopics.slice(0, 10),
    rising: trends.risingTopics.slice(0, 10),
    falling: trends.fallingTopics.slice(0, 10),
    out: trends.outTopics.slice(0, 10),
  });

  // 监控告警
  const monitorJson = JSON.stringify(monitorMatches);

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>热点雷达 | ` + dateStr + `</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg: #0f0f1a;
      --card: #1a1a2e;
      --card-hover: #22223a;
      --border: #2a2a4a;
      --text: #e0e0f0;
      --text-dim: #8888aa;
      --weibo: #E6162D;
      --zhihu: #0066FF;
      --bilibili: #FB7299;
      --douyin: #ff6a3c;
      --xiaohongshu: #FF2442;
      --rising: #00c853;
      --falling: #ff1744;
      --new: #00b0ff;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
      min-height: 100vh;
      padding: 24px;
    }

    .container { max-width: 1200px; margin: 0 auto; }

    /* Header */
    .header {
      text-align: center;
      margin-bottom: 32px;
    }
    .header h1 {
      font-size: 2rem;
      font-weight: 700;
      background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff, #9b59b6);
      background-size: 300% 300%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: gradient 6s ease infinite;
    }
    @keyframes gradient {
      0%, 100% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
    }
    .header .subtitle {
      color: var(--text-dim);
      margin-top: 8px;
      font-size: 0.9rem;
    }
    .header .time {
      display: inline-block;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 4px 16px;
      margin-top: 12px;
      font-size: 0.85rem;
      color: var(--text-dim);
    }

    /* Stats Cards */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }
    .stat-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      text-align: center;
      transition: all 0.2s;
    }
    .stat-card:hover {
      transform: translateY(-2px);
      border-color: var(--p-color, var(--border));
    }
    .stat-card .platform-name {
      font-size: 0.85rem;
      color: var(--text-dim);
      margin-bottom: 8px;
    }
    .stat-card .count {
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--p-color, var(--text));
    }
    .stat-card .desc {
      font-size: 0.75rem;
      color: var(--text-dim);
      margin-top: 4px;
    }

    /* Charts Grid */
    .charts-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 24px;
    }
    .chart-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
    }
    .chart-card.full-width {
      grid-column: 1 / -1;
    }
    .chart-title {
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 16px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .chart-title .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--new);
    }
    .chart-wrap {
      position: relative;
      height: 280px;
    }
    .chart-wrap.bar { height: 260px; }
    .chart-wrap.cross { height: 200px; }

    /* Platform Tables */
    .platform-section {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      margin-bottom: 16px;
      overflow: hidden;
    }
    .platform-header {
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
    }
    .platform-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 600;
    }
    .platform-badge {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .platform-count {
      font-size: 0.8rem;
      color: var(--text-dim);
      background: var(--bg);
      padding: 2px 10px;
      border-radius: 10px;
    }
    .topic-list {
      padding: 0;
    }
    .topic-item {
      display: flex;
      align-items: center;
      padding: 10px 20px;
      border-bottom: 1px solid var(--border);
      transition: background 0.15s;
      gap: 12px;
    }
    .topic-item:last-child { border-bottom: none; }
    .topic-item:hover { background: var(--card-hover); }
    .topic-rank {
      min-width: 28px;
      height: 28px;
      line-height: 28px;
      text-align: center;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 700;
    }
    .rank-top3 { background: linear-gradient(135deg, #ffd700, #ff8c00); color: #000; }
    .rank-normal { background: var(--bg); color: var(--text-dim); }
    .topic-info { flex: 1; min-width: 0; }
    .topic-name {
      font-size: 0.9rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .topic-meta {
      font-size: 0.75rem;
      color: var(--text-dim);
      margin-top: 2px;
    }
    .topic-hot {
      font-size: 0.8rem;
      color: var(--text-dim);
      font-weight: 500;
    }
    .topic-trend {
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 500;
    }
    .trend-new { background: rgba(0,176,255,0.15); color: var(--new); }
    .trend-rise { background: rgba(0,200,83,0.15); color: var(--rising); }
    .trend-fall { background: rgba(255,23,68,0.15); color: var(--falling); }

    /* Cross Platform */
    .cross-platform-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;
    }
    .cross-item {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px;
    }
    .cross-item .topic-name {
      font-size: 0.9rem;
      margin-bottom: 8px;
    }
    .cross-platforms {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .cross-p-badge {
      font-size: 0.7rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 500;
    }

    /* Monitor Alerts */
    .monitor-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 12px;
    }
    .monitor-item {
      background: var(--bg);
      border: 1px solid var(--border);
      border-left: 3px solid var(--new);
      border-radius: 8px;
      padding: 12px 14px;
    }
    .monitor-item .keyword {
      font-size: 0.75rem;
      color: var(--new);
      margin-bottom: 4px;
      font-weight: 600;
    }
    .monitor-item .topic {
      font-size: 0.88rem;
      margin-bottom: 4px;
    }
    .monitor-item .meta {
      font-size: 0.75rem;
      color: var(--text-dim);
    }

    /* Section */
    .section-title {
      font-size: 1.1rem;
      font-weight: 600;
      margin: 24px 0 16px;
      padding-left: 12px;
      border-left: 3px solid var(--weibo);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Footer */
    .footer {
      text-align: center;
      margin-top: 32px;
      padding: 16px;
      color: var(--text-dim);
      font-size: 0.8rem;
    }

    /* Responsive */
    @media (max-width: 900px) {
      .stats-grid { grid-template-columns: repeat(3, 1fr); }
      .charts-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 600px) {
      body { padding: 12px; }
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
    }

    /* Platform specific colors */
    .weibo { --p-color: var(--weibo); }
    .zhihu { --p-color: var(--zhihu); }
    .bilibili { --p-color: var(--bilibili); }
    .douyin { --p-color: var(--douyin); }
    .xiaohongshu { --p-color: var(--xiaohongshu); }
  </style>
</head>
<body>
  <div class="container">

    <!-- Header -->
    <div class="header">
      <h1>🔥 热点雷达</h1>
      <div class="subtitle">全网热点追踪 · 实时可视化报告</div>
      <div class="time">📅 ` + dateStr + ` &nbsp;⏰ ` + timeStr + `</div>
    </div>

    <!-- Stats Overview -->
    <div class="stats-grid">
      <div class="stat-card weibo">
        <div class="platform-name">微博</div>
        <div class="count">` + counts.weibo + `</div>
        <div class="desc">条热榜</div>
      </div>
      <div class="stat-card zhihu">
        <div class="platform-name">知乎</div>
        <div class="count">` + counts.zhihu + `</div>
        <div class="desc">条热榜</div>
      </div>
      <div class="stat-card bilibili">
        <div class="platform-name">B站</div>
        <div class="count">` + counts.bilibili + `</div>
        <div class="desc">条热榜</div>
      </div>
      <div class="stat-card douyin">
        <div class="platform-name">抖音</div>
        <div class="count">` + counts.douyin + `</div>
        <div class="desc">条热榜</div>
      </div>
      <div class="stat-card xiaohongshu">
        <div class="platform-name">小红书</div>
        <div class="count">` + counts.xiaohongshu + `</div>
        <div class="desc">条热榜</div>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid">
      <div class="chart-card full-width">
        <div class="chart-title"><span class="dot"></span>各平台TOP10热度对比</div>
        <div class="chart-wrap bar">
          <canvas id="platformChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-title"><span class="dot" style="background:var(--new)"></span>新增话题</div>
        <div class="chart-wrap">
          <canvas id="newChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-title"><span class="dot" style="background:var(--rising)"></span>上升话题</div>
        <div class="chart-wrap">
          <canvas id="riseChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Cross Platform -->
    ` + (crossPlatform.length > 0 ? `
    <div class="section-title">🌐 跨平台热点 (同时在多个平台登榜)</div>
    <div class="cross-platform-grid">
      ${crossPlatform.map(item => {
        const platformColors = {
          '微博': 'var(--weibo)', '知乎': 'var(--zhihu)',
          'B站': 'var(--bilibili)', '抖音': 'var(--douyin)', '小红书': 'var(--xiaohongshu)'
        };
        return `<div class="cross-item">
          <div class="topic-name">${escapeHtml(item.topic)}</div>
          <div class="cross-platforms">
            ${item.platforms.map(p => `<span class="cross-p-badge" style="background:${platformColors[p]}22;color:${platformColors[p]}">${p}</span>`).join('')}
          </div>
        </div>`;
      }).join('')}
    </div>
    ` : '') + `

    <!-- Monitor Alerts -->
    ` + (monitorMatches.length > 0 ? `
    <div class="section-title">🔔 话题监控告警</div>
    <div class="monitor-grid">
      ${monitorMatches.map(item => `<div class="monitor-item">
        <div class="keyword">关键词: ${escapeHtml(item.keyword)}</div>
        <div class="topic">${escapeHtml(item.topic)}</div>
        <div class="meta">${item.platform} · 第${item.rank}位 · 热度 ${formatHotValue(item.hotValue)}</div>
      </div>`).join('')}
    </div>
    ` : '') + `

    <!-- Platform Hot Lists -->
    <div class="section-title">📊 各平台热榜详情</div>

    ${generatePlatformSection('weibo', currentData.weibo, '微博', 'var(--weibo)')}
    ${generatePlatformSection('zhihu', currentData.zhihu, '知乎', 'var(--zhihu)')}
    ${generatePlatformSection('bilibili', currentData.bilibili, 'B站', 'var(--bilibili)')}
    ${generatePlatformSection('douyin', currentData.douyin, '抖音', 'var(--douyin)')}
    ${generatePlatformSection('xiaohongshu', currentData.xiaohongshu, '小红书', 'var(--xiaohongshu)')}

    <!-- Footer -->
    <div class="footer">
      Generated by 热点雷达 · ${timestamp}
    </div>
  </div>

  <script>
    const platformData = ` + platformDataJson + `;
    const crossPlatformData = ` + crossPlatformJson + `;
    const trendsData = ` + trendsJson + `;
    const monitorData = ` + monitorJson + `;

    const platformColors = {
      weibo: '#E6162D',
      zhihu: '#0066FF',
      bilibili: '#FB7299',
      douyin: '#ff6a3c',
      xiaohongshu: '#FF2442',
    };
    const platformNames = {
      weibo: '微博', zhihu: '知乎', bilibili: 'B站', douyin: '抖音', xiaohongshu: '小红书'
    };

    // Platform comparison chart (bar)
    (function() {
      const ctx = document.getElementById('platformChart');
      if (!ctx) return;
      const labels = [];
      const datasets = [];

      Object.keys(platformData).forEach(function(p) {
        labels.push(platformNames[p]);
        datasets.push({
          label: platformNames[p],
          data: platformData[p].map(function(item, i) {
            return {
              x: platformNames[p] + '-' + (i+1),
              y: item.hotValue || 0,
              topic: item.topic,
            };
          }),
          backgroundColor: platformColors[p] + '99',
          borderColor: platformColors[p],
          borderWidth: 1,
        });
      });

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: Object.keys(platformData).map(function(p) {
            return {
              label: platformNames[p],
              data: platformData[p].map(function(item) { return item.hotValue || 0; }),
              backgroundColor: platformColors[p] + 'aa',
              borderColor: platformColors[p],
              borderWidth: 1,
              borderRadius: 4,
            };
          }),
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: function(ctx) { return ctx[0].label; },
                label: function(ctx) {
                  const d = platformData[Object.keys(platformData)[ctx.datasetIndex]][ctx.dataIndex];
                  return d ? [d.topic, '热度: ' + d.hotValue] : '';
                }
              }
            }
          },
          scales: {
            y: { display: false },
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8888aa' } }
          }
        }
      });
    })();

    // New topics chart
    (function() {
      const ctx = document.getElementById('newChart');
      if (!ctx || trendsData.new.length === 0) return;
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: trendsData.new.map(function(d) { return truncate(d.topic, 8); }),
          datasets: [{
            label: '新增',
            data: trendsData.new.map(function(d) { return d.hotValue || 0; }),
            backgroundColor: '#00b0ff55',
            borderColor: '#00b0ff',
            borderWidth: 1,
            borderRadius: 4,
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { display: false },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8888aa', font: { size: 10 } } }
          }
        }
      });
    })();

    // Rising topics chart
    (function() {
      const ctx = document.getElementById('riseChart');
      if (!ctx || trendsData.rising.length === 0) return;
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: trendsData.rising.map(function(d) { return truncate(d.topic, 8); }),
          datasets: [{
            label: '上升',
            data: trendsData.rising.map(function(d) { return d.delta || 0; }),
            backgroundColor: '#00c85355',
            borderColor: '#00c853',
            borderWidth: 1,
            borderRadius: 4,
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { display: false },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8888aa', font: { size: 10 } } }
          }
        }
      });
    })();

    function truncate(str, len) {
      return str.length > len ? str.substring(0, len) + '...' : str;
    }
  </script>
</body>
</html>`;

  return html;
}

// 生成平台热榜区块HTML
function generatePlatformSection(platformKey, data, platformName, color) {
  if (!data || data.length === 0) {
    return `<div class="platform-section ${platformKey}">
      <div class="platform-header">
        <div class="platform-title">
          <span class="platform-badge" style="background:${color}"></span>
          ${platformName}
        </div>
        <span class="platform-count">数据获取失败</span>
      </div>
    </div>`;
  }

  const items = data.slice(0, 10).map(function(item) {
    const rankClass = item.rank <= 3 ? 'rank-top3' : 'rank-normal';
    const trendLabel = getTrendLabel(item, platformKey);
    const trendClass = getTrendClass(item, platformKey);

    return `<div class="topic-item">
      <span class="topic-rank ${rankClass}">${item.rank}</span>
      <div class="topic-info">
        <div class="topic-name">${escapeHtml(item.topic)}</div>
        ${item.label ? `<div class="topic-meta">${escapeHtml(item.label)}</div>` : ''}
      </div>
      ${trendLabel ? `<span class="topic-trend ${trendClass}">${trendLabel}</span>` : ''}
      <span class="topic-hot">${formatHotValue(item.hotValue)}</span>
    </div>`;
  }).join('');

  return `<div class="platform-section ${platformKey}">
    <div class="platform-header">
      <div class="platform-title">
        <span class="platform-badge" style="background:${color}"></span>
        ${platformName}
      </div>
      <span class="platform-count">${data.length}条</span>
    </div>
    <div class="topic-list">
      ${items}
    </div>
  </div>`;
}

// 获取话题趋势标签
function getTrendLabel(item, platformKey) {
  // 这个函数在HTML中是静态调用的，但数据在JS中
  // 我们通过注入的trendsData来动态显示
  return '';
}

function getTrendClass(item, platformKey) {
  return '';
}

// HTML转义
function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// 保存HTML报告
function saveHtmlReport(html, fileName) {
  const today = new Date().toISOString().split('T')[0];
  const reportDir = path.join(CONFIG.dataDir, 'reports');

  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }

  const filePath = fileName || path.join(reportDir, today + '.html');
  fs.writeFileSync(filePath, html, 'utf-8');
  console.log('HTML Report saved: ' + filePath);

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

  const html = generateHtmlReport(currentData);
  const reportPath = saveHtmlReport(html);

  console.log('\nHTML Report generated successfully');
  console.log('File: ' + reportPath);

  return { html: html, reportPath: reportPath };
}

// 导出
module.exports = {
  generateHtmlReport: generateHtmlReport,
  saveHtmlReport: saveHtmlReport,
  formatDate: formatDate,
  formatHotValue: formatHotValue,
  main: main,
};

// 直接运行
if (require.main === module) {
  main().catch(function (e) {
    console.error('HTML report generation failed:', e);
    process.exit(1);
  });
}
