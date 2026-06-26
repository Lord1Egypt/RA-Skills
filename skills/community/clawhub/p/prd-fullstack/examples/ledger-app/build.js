/**
 * 简记账 PRD 构建脚本
 * 将各章节 Markdown 合并为完整 PRD 文档
 */

const fs = require('fs');
const path = require('path');

const chapters = [
  '01-overview.md',
  '02-market.md',
  '03-requirements.md',
  '08-functional.md',
  '09-data-model.md',
  '12-testing.md',
  '15-project-plan.md',
];

const versionData = JSON.parse(fs.readFileSync('version.json', 'utf-8'));

function build() {
  console.log(`📦 Building 简记账 PRD v${versionData.version}`);
  console.log('');

  const contents = [];

  // 添加文档头
  contents.push(`# ${versionData.title}\n`);
  contents.push(`**版本**: v${versionData.version}\n`);
  contents.push(`**更新日期**: ${versionData.lastUpdate}\n`);
  contents.push('---\n');

  // 合并各章节
  for (const chapter of chapters) {
    if (fs.existsSync(chapter)) {
      const content = fs.readFileSync(chapter, 'utf-8');
      contents.push(content);
      contents.push('\n---\n');
      console.log(`  ✅ ${chapter}`);
    } else {
      console.log(`  ⬜ ${chapter} (missing)`);
    }
  }

  // 写入输出文件
  const outputFile = `简记账-PRD-v${versionData.version}.md`;
  fs.writeFileSync(outputFile, contents.join('\n'), 'utf-8');

  const sizeKB = (Buffer.byteLength(contents.join('\n'), 'utf-8') / 1024).toFixed(1);
  console.log('');
  console.log(`✅ Built: ${outputFile}`);
  console.log(`   Size: ${sizeKB} KB`);
}

build();
