/**
 * Book-PDF 构建脚本模板
 * 将 fragments/ 目录下的 HTML 片段合并成完整的单页 HTML
 *
 * 使用前：修改 FRAGMENT_ORDER 和 <title> 为你的项目
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

// ★ 修改这里：按你的片段文件名排序
const FRAGMENT_ORDER = [
  '00-cover.html',
  '01-toc.html',
  // 'part1-xxx.html',
  // 'part2-xxx.html',
  // ...
  // 'appendix.html',
  '99-backpage.html',
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
        content = content.replace(/文档版本：<\/strong>v[\d.]+/g,
          `文档版本：</strong>v${versionData.version}`);
        content = content.replace(/发布时间：<\/strong>[^<]+/g,
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
