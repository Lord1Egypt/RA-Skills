#!/usr/bin/env node
// md2image.js — markdown → PNG 长图(小红书 / 朋友圈)
//
// 默认 1080px 宽,内容高度自适应,无最大高度限制。
// 主题默认 xiaohongshu(暖色 / 大字号),也可指定 typora-newsprint / huo15-brand 输出沉稳风。
//
// 用法:
//   node md2image.js <input.md> [output.png] [--theme xiaohongshu] [--width 1080] [--scale 2]

const fs = require('fs');
const path = require('path');
const { buildHtml, AVAILABLE_THEMES } = require('./lib/render.js');

function parseArgs(argv) {
  const args = { positional: [], opts: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2); const n = argv[i + 1];
      if (n === undefined || n.startsWith('--')) args.opts[k] = true;
      else { args.opts[k] = n; i++; }
    } else args.positional.push(a);
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const [inputPath, outputPath] = args.positional;
  if (!inputPath) {
    console.error('用法: md2image.js <input.md> [output.png] [--theme xiaohongshu] [--width 1080] [--scale 2]');
    process.exit(1);
  }

  const theme = args.opts.theme || 'xiaohongshu';
  const width = parseInt(args.opts.width || '1080', 10);
  const scale = parseFloat(args.opts.scale || '2');
  const out = outputPath || inputPath.replace(/\.md$/, '.png');

  const markdown = fs.readFileSync(inputPath, 'utf8');
  const html = buildHtml({
    markdown,
    theme,
    title: path.basename(inputPath, '.md'),
    includePrint: false,
    includeMermaid: true,
  });

  let puppeteer;
  try { puppeteer = require('puppeteer'); }
  catch (_) { console.error('未安装 puppeteer。先在 skill 目录运行 npm install'); process.exit(2); }

  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width, height: 800, deviceScaleFactor: scale });
    await page.setContent(html, { waitUntil: 'networkidle0' });

    if (html.includes('class="mermaid"')) {
      await page.waitForFunction(() => {
        const els = document.querySelectorAll('.mermaid');
        if (!els.length) return true;
        return Array.from(els).every(el => el.querySelector('svg'));
      }, { timeout: 5000 }).catch(() => {});
    }

    const body = await page.$('body');
    await body.screenshot({ path: out, type: 'png' });
    const stats = fs.statSync(out);
    console.error(`✓ ${out}  (theme=${theme}  ${width}px @${scale}x  ${(stats.size / 1024).toFixed(1)}KB)`);
  } finally {
    await browser.close();
  }
}

main().catch(e => { console.error(e); process.exit(2); });
