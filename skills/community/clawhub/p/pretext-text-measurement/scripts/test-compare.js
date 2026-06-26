#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

const SKILL = path.resolve(__dirname, '..');

const cases = [
  { label: '中文 400px', text: '欢迎使用Pretext文本测量工具，这是一款专为AI Agent设计的精准文本布局引擎', w: 400, lh: 24 },
  { label: '中文 200px', text: '欢迎使用Pretext文本测量工具，这是一款专为AI Agent设计的精准文本布局引擎', w: 200, lh: 24 },
  { label: '英文 400px', text: 'Welcome to Pretext, a precision text measurement engine designed for AI agents. It supports multilingual text layout.', w: 400, lh: 24 },
  { label: '英文 200px', text: 'Welcome to Pretext, a precision text measurement engine designed for AI agents.', w: 200, lh: 24 },
];

const pad = (s, n) => String(s).padEnd(n, ' ');
const bar = '─'.repeat(50);

console.log('\n  Pretext Skill 中英文测量对比测试\n');
console.log('  字体: 16px sans-serif | 行高: 24px\n');
console.log('  ┌────────────┬────────┬────────┬──────────┬────────────┐');
console.log('  │ 测试场景          │ 宽度   │ 行数   │ 总高度   │ 模式        │');
console.log('  ├────────────┼────────┼────────┼──────────┼────────────┤');

cases.forEach(c => {
  try {
    const out = execSync(
      `node scripts/measure.js --text "${c.text}" --font "16px sans-serif" --width ${c.w} --lineHeight ${c.lh}`,
      { cwd: SKILL, encoding: 'utf8' }
    );
    const r = JSON.parse(out);
    const mode = r.measurementMode === 'canvas' ? 'node-canvas高精度'
      : r.measurementMode === 'mock' ? 'mock canvas标准'
      : '纯JS估算';
    console.log(
      `  │ ${pad(c.label, 10)} │ ${pad(c.w + 'px', 6)} │ ${pad(r.lineCount + '行', 6)} │ ${pad(r.height + 'px', 8)} │ ${pad(mode, 10)} │`
    );
  } catch (e) {
    console.log(`  │ ${pad(c.label, 10)} │ ERROR: ${e.message.slice(0, 30)}`);
  }
});

console.log('  └────────────┴────────┴────────┴──────────┴────────────┘\n');

// 逐行详情测试
console.log('  ── 逐行布局详情（中文 200px）──');
try {
  const out = execSync(
    'node scripts/layout-lines.js --text "欢迎使用Pretext文本测量工具" --font "16px sans-serif" --width 200 --lineHeight 24',
    { cwd: SKILL, encoding: 'utf8' }
  );
  const r = JSON.parse(out);
  r.lines.forEach((l, i) => {
    console.log(`    第${i + 1}行: "${l.text}" (宽度: ${l.width}px, y: ${l.y}px)`);
  });
  console.log(`    总计: ${r.lineCount} 行 × ${r.height}px\n`);
} catch (e) {
  console.log('  错误: ' + e.message.split('\n')[0]);
}

console.log('  ── 逐行布局详情（英文 200px）──');
try {
  const out = execSync(
    'node scripts/layout-lines.js --text "Welcome to Pretext text measurement engine" --font "16px sans-serif" --width 200 --lineHeight 24',
    { cwd: SKILL, encoding: 'utf8' }
  );
  const r = JSON.parse(out);
  r.lines.forEach((l, i) => {
    console.log(`    第${i + 1}行: "${l.text}" (宽度: ${l.width}px, y: ${l.y}px)`);
  });
  console.log(`    总计: ${r.lineCount} 行 × ${r.height}px\n`);
} catch (e) {
  console.log('  错误: ' + e.message.split('\n')[0]);
}

console.log('  ✅ 测试完成\n');
