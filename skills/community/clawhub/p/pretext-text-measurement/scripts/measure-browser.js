#!/usr/bin/env node
/**
 * Pretext Skill — 浏览器端测量脚本（供 AI Agent 内联调用）
 *
 * 当 AI Agent 在浏览器环境中需要调用 pretext 时使用此脚本。
 * 它不直接运行（需要 DOM），而是输出可注入到浏览器的代码片段。
 *
 * 用法：
 *   node measure-browser.js --text "文字" --font "17px sans-serif" --width 560
 *   → 输出可直接在浏览器控制台执行的 JavaScript 代码
 */

'use strict';

const path = require('path');
const SKILL_DIR = __dirname;

// CLI 参数解析
const args = process.argv.slice(2);
const get = (flag) => {
  const idx = args.indexOf(flag);
  return idx >= 0 ? args[idx + 1] : null;
};

const text = get('--text') || '你好，世界！';
const font = get('--font') || '17px sans-serif';
const width = parseInt(get('--width')) || 560;
const lineHeight = get('--lineHeight') ? parseFloat(get('--lineHeight')) : 20;
const output = get('--output') || 'code'; // 'code' | 'snippet' | 'info'

// 解析 fontSize
const fontSizeMatch = font.match(/(\d+(?:\.\d+)?)(?:px)?/);
const fontSize = fontSizeMatch ? parseFloat(fontSizeMatch[1]) : 16;

// 生成浏览器端代码
const browserCode = `
// === Pretext 浏览器端测量 ===
// 依赖: <script src="https://unpkg.com/@chenglou/pretext/dist/pretext.umd.min.js"></script>

(function() {
  const text = ${JSON.stringify(text)};
  const fontSize = ${fontSize};
  const width = ${width};
  const lineHeightRatio = ${lineHeight / fontSize};

  // 方法1: layout() — 最常用，返回 {height, lineCount, estimatedWidth}
  const layout = pretext.layout(text, fontSize, lineHeightRatio, width);
  console.log('layout 结果:', layout);
  // → { height: 80, lineCount: 3, estimatedWidth: 340 }

  // 方法2: measureNaturalWidth() — 测量字符串宽度
  const w = pretext.measureNaturalWidth(text, fontSize);
  console.log('字符串宽度:', w + 'px');

  // 方法3: prepare() — 预处理文本，获取逐行信息
  const p = pretext.prepare(text, fontSize, width);
  console.log('prepare 结果（逐行）:', p);

  // 方法4: layoutNextLine() — 逐行增量布局
  const next = pretext.layoutNextLine(text, fontSize, lineHeightRatio, width, 0);
  console.log('第一行布局:', next);

  return { layout, width: w, prepare: p, nextLine: next };
})();
`.trim();

// 生成 HTML snippet（可直接粘贴到控制台）
const htmlSnippet = `<script src="https://unpkg.com/@chenglou/pretext/dist/pretext.umd.min.js"><\/script>
<script>
const result = pretext.layout(${JSON.stringify(text)}, ${fontSize}, ${(lineHeight / fontSize).toFixed(2)}, ${width});
console.log('Pretext 测量结果:', result);
<\/script>`;

// 输出
if (output === 'code') {
  console.log(browserCode);
} else if (output === 'snippet') {
  console.log(htmlSnippet);
} else if (output === 'info') {
  console.log(JSON.stringify({
    text: text.slice(0, 50),
    font,
    fontSize,
    width,
    lineHeight,
    mode: 'browser-pretext',
    available: true,
    description: '使用浏览器 Canvas 的 pretext 原版 API，精度 100%',
    loadTag: '<script src="https://unpkg.com/@chenglou/pretext/dist/pretext.umd.min.js"><\/script>',
    functions: [
      'pretext.layout(text, fontSize, lineHeightRatio, maxWidth) → {height, lineCount, estimatedWidth}',
      'pretext.measureNaturalWidth(text, fontSize) → number (px)',
      'pretext.prepare(text, fontSize, maxWidth) → {lines, _chars}',
      'pretext.layoutNextLine(text, fontSize, lineHeightRatio, maxWidth, startAt) → {...}',
    ]
  }, null, 2));
}
