#!/usr/bin/env node
/**
 * MD to Mobile Image - Optimized for Telegram
 * 白底黑字，压缩后更清晰
 */

const { chromium } = require('playwright');
const fs = require('fs');
const { marked } = require('marked');
const hljs = require('highlight.js');

const TARGET_WIDTH = 1080;  // 1x base width
const MAX_HEIGHT = 3800;
const OUTPUT_DIR = '/tmp/md-to-img';

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value;
      } catch (e) {}
    }
    return hljs.highlightAuto(code).value;
  }
});

// Light theme - optimized for clarity and compression
const CSS = `
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  font-size: 32px;  /* Large base font */
  line-height: 1.7;
  color: #1a1a1a;
  background: #ffffff;
  padding: 40px 36px;
  width: ${TARGET_WIDTH}px;
}

h1 {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.25;
  margin-bottom: 32px;
  color: #000000;
  letter-spacing: -1px;
}

h2 {
  font-size: 42px;
  font-weight: 700;
  line-height: 1.3;
  margin: 48px 0 24px;
  color: #2563eb;
  border-bottom: 3px solid #e5e7eb;
  padding-bottom: 12px;
}

h3 {
  font-size: 36px;
  font-weight: 700;
  line-height: 1.35;
  margin: 36px 0 18px;
  color: #1e40af;
}

h4 {
  font-size: 32px;
  font-weight: 600;
  margin: 32px 0 16px;
  color: #374151;
}

p {
  margin: 20px 0;
  font-size: 30px;
  line-height: 1.8;
  color: #333333;
}

ul, ol {
  margin: 20px 0 20px 36px;
}

li {
  margin: 14px 0;
  font-size: 30px;
  line-height: 1.7;
}

strong {
  font-weight: 800;
  color: #000000;
}

em {
  font-style: italic;
}

code {
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 26px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 8px;
  background: #f3f4f6;
  color: #dc2626;
  border: 1px solid #e5e7eb;
}

pre {
  margin: 28px 0;
  padding: 28px;
  border-radius: 16px;
  background: #1e1e1e;
  overflow-x: auto;
  border: 2px solid #333;
}

pre code {
  padding: 0;
  background: none;
  font-size: 24px;
  line-height: 1.7;
  color: #e5e5e5;
  border: none;
}

blockquote {
  margin: 28px 0;
  padding: 24px 32px;
  border-radius: 0 16px 16px 0;
  border-left: 8px solid #2563eb;
  background: #eff6ff;
}

blockquote p {
  margin: 0;
  font-size: 30px;
  color: #1e40af;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 28px 0;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #e5e7eb;
  font-size: 26px;
}

th {
  background: #2563eb;
  color: #ffffff;
  font-weight: 700;
  padding: 20px 16px;
  text-align: left;
  font-size: 26px;
}

td {
  padding: 18px 16px;
  border-bottom: 1px solid #f3f4f6;
  color: #333;
}

tr:last-child td { border-bottom: none; }
tr:nth-child(even) { background: #f9fafb; }

img { max-width: 100%; height: auto; border-radius: 12px; margin: 16px 0; }
a { color: #2563eb; text-decoration: none; }

hr { margin: 40px 0; border: none; height: 4px; background: #e5e7eb; border-radius: 2px; }

.hljs-keyword { color: #ff79c6; }
.hljs-string { color: #a8e6cf; }
.hljs-number { color: #bd93f9; }
.hljs-comment { color: #6272a4; }
.hljs-function { color: #50fa7b; }
.hljs-class { color: #8be9fd; }
`;

function buildHtml(markdown) {
  const content = marked(markdown);
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>${CSS}</style>
</head>
<body>
${content}
</body>
</html>`;
}

async function generateImage(html, outputPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.setViewportSize({ width: TARGET_WIDTH, height: 8000 });
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  const height = await page.evaluate(() => document.body.scrollHeight);
  await page.setViewportSize({ width: TARGET_WIDTH, height: Math.min(height, MAX_HEIGHT) });
  
  await page.screenshot({
    path: outputPath,
    fullPage: true,
    type: 'png'
  });
  
  await browser.close();
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: md-to-image <md-file>');
    process.exit(1);
  }
  
  const mdFile = args[0];
  if (!fs.existsSync(mdFile)) {
    console.error(`File not found: ${mdFile}`);
    process.exit(1);
  }
  
  const mdContent = fs.readFileSync(mdFile, 'utf-8');
  console.log(`Converting: ${mdFile}`);
  
  const html = buildHtml(mdContent);
  const timestamp = Date.now();
  const outputPath = `${OUTPUT_DIR}/output_${timestamp}.png`;
  
  console.log('Generating...');
  await generateImage(html, outputPath);
  
  console.log(`DONE:${outputPath}`);
}

main().catch(console.error);
