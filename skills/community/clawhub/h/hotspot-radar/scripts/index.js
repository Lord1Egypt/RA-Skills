/**
 * 热点雷达 - 主入口
 * 一站式全网热榜追踪工具
 */

const path = require('path');
const fs = require('fs');

// 引入子模块
const collector = require('./collector');
const reporter = require('./reporter');
const htmlReporter = require('./htmlReporter');
const monitor = require('./monitor');

// 配置
const CONFIG = {
  scriptsDir: __dirname,
  dataDir: path.join(__dirname, '../data'),
  configDir: path.join(__dirname, '../config'),
};

// 显示Banner
function showBanner() {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🌐  热 点 雷 达  -  全网热榜追踪器                     ║
║                                                           ║
║     聚合微博/知乎/抖音/B站/小红书热搜榜单                 ║
║     支持趋势分析、话题监控、定时推送                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);
}

// 显示帮助
function showHelp() {
  console.log(`
📖 使用指南

命令:
  node index.js fetch          采集今日全网热榜数据
  node index.js report         生成今日热点报告
  node index.js html           生成HTML可视化报告（含图表）
  node index.js trend          分析趋势变化（需有历史数据）
  node index.js monitor        话题监控管理
  node index.js quick          快速模式：采集+报告一步完成
  node index.js init           初始化目录结构
  node index.js help           显示帮助

快速开始:
  1. node index.js init        初始化目录
  2. node index.js quick       一键采集并生成报告

示例:
  node index.js fetch          获取最新热榜
  node index.js report         生成Markdown报告
  node index.js monitor add "AI"   添加监控关键词
`);
}

// 初始化目录
function init() {
  console.log('📁 初始化目录结构...');
  collector.ensureDirs ? collector.ensureDirs() : null;

  // 确保配置目录存在
  if (!fs.existsSync(CONFIG.configDir)) {
    fs.mkdirSync(CONFIG.configDir, { recursive: true });
  }

  // 创建默认监控配置
  const monitorConfigPath = path.join(CONFIG.configDir, 'monitor.json');
  if (!fs.existsSync(monitorConfigPath)) {
    fs.writeFileSync(monitorConfigPath, JSON.stringify({ keywords: [], enabled: true }, null, 2), 'utf-8');
    console.log('✅ 已创建默认监控配置');
  }

  // 创建README
  const readmePath = path.join(__dirname, '../README.md');
  if (!fs.existsSync(readmePath)) {
    const readme = `# 🌐 热点雷达 - 全网热榜追踪器

> 聚合微博/知乎/抖音/B站/小红书热搜榜单，支持趋势分析和话题监控

## 功能特性

- ✅ 实时采集五大平台热榜
- ✅ 趋势追踪：对比昨日发现新上榜/落榜话题
- ✅ 跨平台热点：发现同时在多个平台发酵的话题
- ✅ 话题监控：关键词订阅，有动态时及时提醒
- ✅ 每日报告：自动生成Markdown格式热点日报

## 快速开始

\`\`\`bash
# 采集今日热榜
node scripts/index.js fetch

# 生成今日报告
node scripts/index.js report

# 一键完成（采集+报告）
node scripts/index.js quick
\`\`\`

## 目录结构

\`\`\`
hotspot-radar/
├── data/                    # 数据存储
│   ├── history/            # 历史热榜
│   │   ├── weibo/
│   │   ├── zhihu/
│   │   ├── bilibili/
│   │   ├── douyin/
│   │   └── xiaohongshu/
│   ├── trends/             # 每日趋势快照
│   └── reports/           # 生成的报告
├── config/                 # 配置文件
│   └── monitor.json       # 监控关键词配置
└── scripts/                # 脚本文件
    ├── index.js           # 主入口
    ├── collector.js       # 数据采集
    ├── reporter.js        # 报告生成
    └── monitor.js         # 监控管理
\`\`\`

## 话题监控

\`\`\`bash
# 添加监控关键词
node scripts/monitor.js add "人工智能"

# 移除监控关键词
node scripts/monitor.js remove "人工智能"

# 列出所有关键词
node scripts/monitor.js list
\`\`\`

## 数据来源

- 微博热搜
- 知乎热榜
- 抖音热搜
- B站热榜
- 小红书热榜

---
*由「热点雷达」Skill生成*
`;
    fs.writeFileSync(readmePath, readme, 'utf-8');
    console.log('✅ 已创建README.md');
  }

  console.log('\n✅ 初始化完成！');
  console.log('\n下一步:');
  console.log('  1. node index.js quick   # 一键采集+生成报告');
  console.log('  2. node index.js monitor add "关键词"  # 添加监控话题\n');
}

// 快速模式
async function quick() {
  console.log('🚀 快速模式：采集 + 生成报告\n');
  try {
    await collector.main();
    await reporter.main();
    console.log('\n✅ 全部完成！');
  } catch (e) {
    console.error('❌ 执行失败:', e);
    process.exit(1);
  }
}

// 主函数
async function main() {
  showBanner();

  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'fetch':
      try {
        const data = await collector.fetchAll();
        collector.saveHistory(data);
        console.log('\n✅ 数据采集完成');
      } catch (e) {
        console.error('❌ 采集失败:', e);
        process.exit(1);
      }
      break;

    case 'report':
      try {
        await reporter.main();
      } catch (e) {
        console.error('❌ 报告生成失败:', e);
        process.exit(1);
      }
      break;

    case 'html':
      try {
        await htmlReporter.main();
      } catch (e) {
        console.error('❌ HTML报告生成失败:', e);
        process.exit(1);
      }
      break;

    case 'trend':
      console.log('📈 趋势分析模式');
      // TODO: 实现独立趋势分析
      break;

    case 'monitor':
      // 传递给monitor模块
      monitor.main();
      break;

    case 'quick':
      await quick();
      break;

    case 'init':
      init();
      break;

    case 'help':
    default:
      showHelp();
  }
}

// 导出模块接口
module.exports = {
  fetchAll: collector.fetchAll,
  saveHistory: collector.saveHistory,
  generateReport: reporter.generateReport,
  saveReport: reporter.saveReport,
  generateHtmlReport: htmlReporter.generateHtmlReport,
  saveHtmlReport: htmlReporter.saveHtmlReport,
  addMonitor: monitor.addKeyword,
  removeMonitor: monitor.removeKeyword,
  listMonitor: monitor.listKeywords,
};

// 直接运行时执行
if (require.main === module) {
  main();
}
