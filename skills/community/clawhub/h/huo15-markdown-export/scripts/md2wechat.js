#!/usr/bin/env node
// md2wechat.js — markdown → 微信公众号兼容 HTML
//
// 微信编辑器粘贴时会剥掉 <style> / <link>,只保留 inline style。
// 本脚本用 juice 把 wechat.css 的所有规则内联到 element style 属性。
// 输出:复制粘贴到微信公众号编辑器即可。
//
// 用法:
//   node md2wechat.js <input.md> [output.html]

const fs = require('fs');
const path = require('path');
const { buildHtml } = require('./lib/render.js');

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath) {
  console.error('用法: md2wechat.js <input.md> [output.html]');
  process.exit(1);
}

const markdown = fs.readFileSync(inputPath, 'utf8');
const fullHtml = buildHtml({
  markdown,
  theme: 'wechat',
  title: path.basename(inputPath, '.md'),
  includePrint: false,
  includeMermaid: false, // 微信不支持 script,mermaid 走不了
});

let inlined;
try {
  const juice = require('juice');
  inlined = juice(fullHtml, {
    preserveImportant: true,
    inlinePseudoElements: false,
    removeStyleTags: true,
  });
} catch (_) {
  console.error('未安装 juice。先在 skill 目录运行 npm install');
  process.exit(2);
}

// 微信粘贴时会自动包外层 div,我们只交付 <article> 内容,粘贴更干净
const match = inlined.match(/<article[^>]*>([\s\S]*?)<\/article>/);
const articleOnly = match ? match[1] : inlined;

const out = outputPath || inputPath.replace(/\.md$/, '.wechat.html');
fs.writeFileSync(out, articleOnly);
console.error(`✓ ${out}  — 用浏览器打开,全选复制,粘到微信公众号编辑器`);
