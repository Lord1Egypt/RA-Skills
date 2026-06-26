/**
 * PRD HTML 构建脚本
 * 将 fragments/ 目录下的 HTML 片段合并成完整的单页 HTML
 *
 * 用法：node build.js
 */

const fs = require('fs');
const path = require('path');

const FRAGMENTS_DIR = path.join(__dirname, 'fragments');
const OUTPUT_DIR = path.join(__dirname, 'output');
const CSS_FILE = path.join(__dirname, 'styles.css');
const VERSION_FILE = path.join(__dirname, 'version.json');
const versionData = JSON.parse(fs.readFileSync(VERSION_FILE, 'utf-8'));
const OUTPUT_FILE = path.join(OUTPUT_DIR, `${versionData.title}-v${versionData.version}.html`);

// 片段文件顺序 - 对应PRD 14章结构
const FRAGMENT_ORDER = [
  '00-cover.html',
  '01-toc.html',
  '02-overview.html',      // 01 项目概述
  '03-requirements.html',  // 03 需求列表
  '04-user-stories.html',  // 05 用户流程
  '05-functional.html',    // 08 功能规格
  '06-interaction.html',   // 07 UI设计规范
  '07-data.html',          // 09 数据模型
  '08-nonfunctional.html', // 11 非功能需求
  '99-backpage.html',
];

// 可选片段（存在则添加，不存在则跳过）
const OPTIONAL_FRAGMENTS = [
  '09-market.html',        // 02 市场分析
  '10-architecture.html',  // 04 信息架构
  '11-prototype.html',     // 06 原型设计
  '12-tech.html',          // 10 技术方案
  '13-testing.html',       // 12 测试方案
  '14-operation.html',     // 14 运营方案
  '15-project-plan.html',  // 15 项目计划
];

function build() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const buildTime = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  console.log(`📦 Version: v${versionData.version} (build #${versionData.build})`);

  const css = fs.readFileSync(CSS_FILE, 'utf-8');

  const fragments = [];
  const missing = [];

  for (const name of FRAGMENT_ORDER) {
    const filePath = path.join(FRAGMENTS_DIR, name);
    if (fs.existsSync(filePath)) {
      let content = fs.readFileSync(filePath, 'utf-8').trim();
      // 注入版本信息到封面
      if (name === '00-cover.html') {
        content = content.replace(/文档版本：</strong>v[\d.]+/g,
          `文档版本：</strong>v${versionData.version}`);
        content = content.replace(/发布时间：</strong>[^<]+/g,
          `发布时间：</strong>${versionData.lastUpdate} (build #${versionData.build})`);
      }
      fragments.push(`<!-- ===== ${name} ===== -->\n${content}`);
      console.log(`  ✅ ${name}`);
    } else {
      missing.push(name);
      console.log(`  ⬜ ${name} (missing, skipped)`);
    }
  }

  if (missing.length > 0) {
    console.log(`\n⚠️  ${missing.length} fragments missing, building partial HTML\n`);
  }

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${versionData.title}</title>
<style>
${css}
</style>
</head>
<body>

${fragments.join('\n\n')}

</body>
</html>`;

  fs.writeFileSync(OUTPUT_FILE, html, 'utf-8');

  const sizeKB = (Buffer.byteLength(html, 'utf-8') / 1024).toFixed(1);
  console.log(`\n✅ Built: ${OUTPUT_FILE}`);
  console.log(`   Size: ${sizeKB} KB`);
  console.log(`   Fragments: ${fragments.length}/${FRAGMENT_ORDER.length}`);
}

build();
