#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');
const { marked } = require('marked');
const twemoji = require('twemoji');

const [, , input, output, cdp = process.env.BROWSER_CDP_URL || 'http://127.0.0.1:9222'] = process.argv;
if (!input || !output) {
  console.error('Usage: node scripts/md2pdf_browser.js <input.md> <output.pdf> [cdpUrl]');
  process.exit(1);
}
if (!fs.existsSync(input)) {
  console.error(`[ERROR] Input file not found: ${input}`);
  process.exit(1);
}

marked.setOptions({ gfm: true, breaks: true });
const markdown = fs.readFileSync(input, 'utf8');
const bodyHtml = marked.parse(markdown);
const htmlWithEmoji = twemoji.parse(bodyHtml, {
  folder: 'svg',
  ext: '.svg',
  className: 'emoji',
  base: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/'
});

const title = path.basename(input, path.extname(input));
const html = `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>${title}</title>
<style>
  :root { color-scheme: light; }
  html, body { margin: 0; padding: 0; background: #fff; color: #1f2328; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
    line-height: 1.65;
    font-size: 16px;
  }
  .page {
    max-width: 860px;
    margin: 0 auto;
    padding: 32px 40px 56px;
  }
  h1,h2,h3,h4 { line-height: 1.3; margin: 1.2em 0 0.5em; }
  h1 { font-size: 2em; border-bottom: 1px solid #d0d7de; padding-bottom: .3em; }
  h2 { font-size: 1.5em; border-bottom: 1px solid #d0d7de; padding-bottom: .2em; }
  h3 { font-size: 1.2em; }
  p, ul, ol, table, blockquote { margin: 0.7em 0; }
  ul, ol { padding-left: 1.5em; }
  li { margin: 0.3em 0; }
  table { width: 100%; border-collapse: collapse; font-size: 0.95em; display: block; overflow-x: auto; }
  th, td { border: 1px solid #d0d7de; padding: 8px 10px; vertical-align: top; }
  th { background: #f6f8fa; text-align: left; }
  code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; background: #f6f8fa; padding: .15em .3em; border-radius: 4px; }
  pre { background: #f6f8fa; padding: 12px 14px; border-radius: 8px; overflow: auto; }
  blockquote { margin-left: 0; padding: 0 1em; color: #57606a; border-left: 4px solid #d0d7de; }
  img.emoji { height: 1.1em; width: 1.1em; margin: 0 .06em 0 .08em; vertical-align: -0.15em; }
  hr { border: none; border-top: 1px solid #d0d7de; margin: 1.4em 0; }
  @page { size: A4; margin: 16mm 14mm 16mm 14mm; }
</style>
</head>
<body>
  <main class="page">${htmlWithEmoji}</main>
</body>
</html>`;

(async () => {
  const browser = await puppeteer.connect({ browserURL: cdp, defaultViewport: { width: 1280, height: 1800 } });
  const page = await browser.newPage();
  try {
    await page.setContent(html, { waitUntil: 'networkidle0' });
    await page.emulateMediaType('screen');
    await page.pdf({
      path: output,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' }
    });
    console.log(`[OK] Generated browser PDF: ${output}`);
  } finally {
    await page.close();
    await browser.disconnect();
  }
})().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
