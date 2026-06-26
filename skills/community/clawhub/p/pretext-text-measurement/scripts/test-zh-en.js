#!/usr/bin/env node
// 测试中英文文本测量效果
const path = require('path');

// 强制使用纯 JS Unicode 估算模式（绕过 node-canvas）
process.env.PRETEXT_FORCE_ESTIMATE = '1';

const { execSync } = require('child_process');
const SKILL_DIR = path.resolve(__dirname, '..');

function run(text, font, width, lineHeight) {
  const args = [
    'scripts/measure.js',
    '--text', text,
    '--font', font,
    '--width', String(width),
    '--lineHeight', String(lineHeight)
  ];
  try {
    const out = execSync(`node ${args.join(' ')}`, {
      cwd: SKILL_DIR,
      encoding: 'utf8',
      env: { ...process.env, PRETEXT_FORCE_ESTIMATE: '1' }
    });
    return JSON.parse(out);
  } catch (e) {
    return JSON.parse(e.stdout || e.message);
  }
}

console.log('╔══════════════════════════════════════════════════════════════╗');
console.log('║          Pretext Skill 中英文对比测试                      ║');
console.log('╚══════════════════════════════════════════════════════════════╝\n');

const testCases = [
  {
    lang: '🇨🇳 中文',
    text: '欢迎使用 Pretext 文本测量工具，这是一款专为 AI Agent 设计的精准文本布局引擎。',
    font: '16px sans-serif',
    width: 400,
    lineHeight: 24
  },
  {
    lang: '🇨🇳 中文（窄宽度 200px）',
    text: '欢迎使用 Pretext 文本测量工具，这是一款专为 AI Agent 设计的精准文本布局引擎。',
    font: '16px sans-serif',
    width: 200,
    lineHeight: 24
  },
  {
    lang: '🇬🇧 英文',
    text: 'Welcome to Pretext, a precision text measurement engine designed for AI agents. It supports multilingual text layout with pixel-accurate results.',
    font: '16px sans-serif',
    width: 400,
    lineHeight: 24
  },
  {
    lang: '🇬🇧 英文（窄宽度 200px）',
    text: 'Welcome to Pretext, a precision text measurement engine designed for AI agents.',
    font: '16px sans-serif',
    width: 200,
    lineHeight: 24
  },
  {
    lang: '🇨🇳🇬🇧 混合（中英混排）',
    text: 'Hello 世界！Pretext 是一款支持 Chinese 中文 和 English 英文 混合排版的工具 🚀',
    font: '16px sans-serif',
    width: 350,
    lineHeight: 24
  },
  {
    lang: '🚀 Emoji 测试',
    text: '🚀 火箭出发！🌟 星星闪耀！💯 满分！👨‍👩‍👧‍👦 全家福 🇨🇳🇬🇧🇯🇵 各国旗帜 emoji！',
    font: '16px sans-serif',
    width: 400,
    lineHeight: 24
  }
];

testCases.forEach(tc => {
  const result = run(tc.text, tc.font, tc.width, tc.lineHeight);
  console.log(`【${tc.lang}】`);
  console.log(`  📝 文本: "${tc.text}"`);
  console.log(`  📐 宽度: ${tc.width}px | 行高: ${tc.lineHeight}px`);
  console.log(`  📊 结果: ${result.lineCount} 行 × ${result.height}px`);
  console.log(`  🏷️  模式: ${result.measurementModeLabel}`);
  console.log(`  💡 建议: ${result.tips?.heightAdvice || '-'}`);
  console.log('');
});
