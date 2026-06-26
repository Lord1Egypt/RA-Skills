// stats-panel.mjs - 记忆健康度统计面板 v1.1
// 生成 HTML 可视化报告

import fs from 'fs';
import path from 'path';
import { loadConfig, getPath } from './config-loader.mjs';

const config = loadConfig();
const INDEX_PATH = getPath('indexFile', config);
const DREAM_LOG_PATH = getPath('dreamLog', config);
const STATS_DIR = getPath('statsDir', config);

function loadIndex() {
  if (!fs.existsSync(INDEX_PATH)) return { memories: [] };
  return JSON.parse(fs.readFileSync(INDEX_PATH, 'utf-8'));
}

function analyzeMemories(index) {
  const memories = index.memories || [];
  const layerStats = {
    flash: { count: 0, avgTTL: 0, expiring: [] },
    active: { count: 0, avgTTL: 0, expiring: [] },
    attention: { count: 0, avgTTL: 0, expiring: [] },
    settled: { count: 0, avgTTL: 0, expiring: [] },
  };
  
  const tagCloud = {};
  const recallHeat = {};
  
  const today = new Date().toISOString().split('T')[0];
  
  for (const mem of memories) {
    // 层级统计
    const layer = mem.layer || 'active';
    layerStats[layer].count++;
    layerStats[layer].avgTTL += mem.ttl || 7;
    
    // TTL预警（<3天）
    const lastActive = mem.lastActive || mem.created;
    const daysSince = Math.floor((new Date(today) - new Date(lastActive)) / (1000 * 60 * 60 * 24));
    if ((mem.ttl || 7) - daysSince < 3) {
      layerStats[layer].expiring.push({
        title: mem.title,
        daysLeft: (mem.ttl || 7) - daysSince,
      });
    }
    
    // 标签云
    for (const tag of mem.tags || []) {
      tagCloud[tag] = (tagCloud[tag] || 0) + 1;
    }
    
    // 召回频次
    const recallCount = mem.recallCount || 0;
    recallHeat[recallCount] = (recallHeat[recallCount] || 0) + 1;
  }
  
  // 计算平均TTL
  for (const layer of Object.keys(layerStats)) {
    const s = layerStats[layer];
    s.avgTTL = s.count > 0 ? (s.avgTTL / s.count).toFixed(1) : 0;
  }
  
  return { layerStats, tagCloud, recallHeat };
}

function parseDreamLog() {
  if (!fs.existsSync(DREAM_LOG_PATH)) return [];
  
  const log = fs.readFileSync(DREAM_LOG_PATH, 'utf-8');
  const entries = [];
  let currentDate = '';
  
  for (const line of log.split('\n')) {
    if (line.startsWith('## ')) {
      currentDate = line.slice(3).trim();
    } else if (line.trim() && currentDate) {
      const match = line.match(/^([🧠📦🗑️🔗✨💤✏️])\s+(.+)$/);
      if (match) {
        entries.push({
          date: currentDate,
          icon: match[1],
          message: match[2],
        });
      }
    }
  }
  
  return entries.slice(-50); // 最近50条
}

function generateHTML(stats, dreamEntries) {
  const { layerStats, tagCloud, recallHeat } = stats;
  
  const total = Object.values(layerStats).reduce((s, l) => s + l.count, 0);
  
  // 标签云排序
  const topTags = Object.entries(tagCloud)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20);
  
  // 梦境日志最近10条
  const recentDreams = dreamEntries.slice(-10);
  
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>记忆健康度面板 | layered-memory-sys v1.1</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f1a; color: #e0e0e0; padding: 20px; }
    .container { max-width: 1200px; margin: 0 auto; }
    h1 { color: #7c3aed; margin-bottom: 20px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
    .card { background: #1a1a2e; border-radius: 12px; padding: 20px; border: 1px solid #2a2a4a; }
    .card h2 { color: #a78bfa; margin-bottom: 15px; font-size: 16px; }
    .layer-stat { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #2a2a4a; }
    .layer-stat:last-child { border-bottom: none; }
    .layer-name { font-weight: 600; }
    .layer-flash { color: #fbbf24; }
    .layer-active { color: #34d399; }
    .layer-attention { color: #60a5fa; }
    .layer-settled { color: #a78bfa; }
    .expiring { color: #ef4444; font-size: 12px; margin-top: 10px; }
    .tag-cloud { display: flex; flex-wrap: wrap; gap: 8px; }
    .tag { background: #2a2a4a; padding: 4px 12px; border-radius: 16px; font-size: 12px; }
    .tag-size-1 { font-size: 10px; opacity: 0.7; }
    .tag-size-2 { font-size: 12px; }
    .tag-size-3 { font-size: 14px; font-weight: 600; }
    .dream-log { max-height: 300px; overflow-y: auto; }
    .dream-entry { padding: 8px 0; border-bottom: 1px solid #2a2a4a; font-size: 13px; }
    .dream-date { color: #6b7280; font-size: 11px; }
    .summary { text-align: center; padding: 30px; }
    .summary .big { font-size: 48px; font-weight: 700; color: #7c3aed; }
    .summary .label { color: #6b7280; margin-top: 10px; }
    canvas { max-height: 250px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>📊 记忆健康度面板 v1.1</h1>
    
    <div class="grid">
      <div class="card summary">
        <div class="big">${total}</div>
        <div class="label">活跃记忆总数</div>
      </div>
      
      <div class="card">
        <h2>📊 各层记忆分布</h2>
        <canvas id="layerChart"></canvas>
      </div>
      
      <div class="card">
        <h2>🏷️ 热门标签</h2>
        <div class="tag-cloud">
          ${topTags.map(([tag, count]) => 
            `<span class="tag tag-size-${count >= 5 ? 3 : count >= 2 ? 2 : 1}">${tag} (${count})</span>`
          ).join('')}
        </div>
      </div>
      
      <div class="card">
        <h2>⏰ TTL预警</h2>
        ${Object.entries(layerStats).map(([layer, s]) => 
          s.expiring.length > 0 ? `
            <div class="layer-stat layer-${layer}">
              <span class="layer-name">${layer}层</span>
              <span>${s.expiring.length}条即将过期</span>
            </div>
            <div class="expiring">${s.expiring.map(e => `• ${e.title} (${e.daysLeft}天)`).join('<br>')}</div>
          ` : ''
        ).join('')}
        ${Object.values(layerStats).every(s => s.expiring.length === 0) ? '<div style="color:#6b7280">✅ 无即将过期的记忆</div>' : ''}
      </div>
      
      <div class="card">
        <h2>📈 召回频次分布</h2>
        <canvas id="recallChart"></canvas>
      </div>
      
      <div class="card">
        <h2>🌙 最近梦境日志</h2>
        <div class="dream-log">
          ${recentDreams.map(d => `
            <div class="dream-entry">
              <span class="dream-date">${d.date}</span> ${d.icon} ${d.message}
            </div>
          `).join('')}
        </div>
      </div>
    </div>
    
    <div style="text-align:center;color:#6b7280;font-size:12px;margin-top:20px;">
      生成时间: ${new Date().toLocaleString('zh-CN')} | layered-memory-sys v1.1
    </div>
  </div>
  
  <script>
    // 层级饼图
    new Chart(document.getElementById('layerChart'), {
      type: 'doughnut',
      data: {
        labels: ['flash', 'active', 'attention', 'settled'],
        datasets: [{
          data: [${layerStats.flash.count}, ${layerStats.active.count}, ${layerStats.attention.count}, ${layerStats.settled.count}],
          backgroundColor: ['#fbbf24', '#34d399', '#60a5fa', '#a78bfa'],
        }]
      },
      options: { plugins: { legend: { position: 'bottom' } } }
    });
    
    // 召回频次柱图
    new Chart(document.getElementById('recallChart'), {
      type: 'bar',
      data: {
        labels: ${JSON.stringify(Object.keys(recallHeat).sort((a,b) => a-b))},
        datasets: [{
          label: '记忆数',
          data: ${JSON.stringify(Object.keys(recallHeat).sort((a,b) => a-b).map(k => recallHeat[k]))},
          backgroundColor: '#7c3aed',
        }]
      },
      options: { plugins: { legend: { display: false } } }
    });
  </script>
</body>
</html>`;
}

function generateStats() {
  console.log('📊 生成记忆健康度面板...\n');
  
  const index = loadIndex();
  const stats = analyzeMemories(index);
  const dreamEntries = parseDreamLog();
  
  const html = generateHTML(stats, dreamEntries);
  
  if (!fs.existsSync(STATS_DIR)) {
    fs.mkdirSync(STATS_DIR, { recursive: true });
  }
  
  const outputPath = path.join(STATS_DIR, 'health-panel.html');
  fs.writeFileSync(outputPath, html);
  
  console.log(`✅ 报告已生成: ${outputPath}`);
  console.log(`\n📊 记忆统计:`);
  console.log(`   总计: ${Object.values(stats.layerStats).reduce((s,l) => s+l.count, 0)} 条`);
  for (const [layer, s] of Object.entries(stats.layerStats)) {
    console.log(`   ${layer}: ${s.count} 条 (avg TTL: ${s.avgTTL}天)`);
  }
  console.log(`   热门标签: ${Object.entries(stats.tagCloud).sort((a,b) => b[1]-a[1]).slice(0,5).map(([t,c]) => `${t}(${c})`).join(', ')}`);
}

generateStats();
