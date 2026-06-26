#!/usr/bin/env node
// md2html.js — markdown → 单文件自包含 HTML
// 所有 CSS / KaTeX / 代码高亮全部内嵌,可发邮件/上传/离线阅读
//
// 用法:
//   node md2html.js <input.md> [output.html] [--theme github] [--no-mermaid]
//                    [--og-title TEXT] [--og-description TEXT] [--og-image URL] [--og-url URL]
//
// OG 标签:不传 --og-title / --og-description 时,自动从 markdown 抽 H1 + 首段。
// 输出 HTML 在企微/微信/Twitter/Slack 粘贴时显示卡片预览。

const fs = require('fs');
const path = require('path');
const { buildHtml, AVAILABLE_THEMES } = require('./lib/render.js');

function parseArgs(argv) {
  const args = { positional: [], opts: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        args.opts[key] = true;
      } else {
        args.opts[key] = next; i++;
      }
    } else args.positional.push(a);
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
const [inputPath, outputPath] = args.positional;
if (!inputPath) {
  console.error('用法: md2html.js <input.md> [output.html] [--theme typora-newsprint] [--og-title TEXT] [--og-description TEXT] [--og-image URL] [--og-url URL]');
  console.error('主题: ' + AVAILABLE_THEMES.join(' / '));
  process.exit(1);
}

const markdown = fs.readFileSync(inputPath, 'utf8');
const out = outputPath || inputPath.replace(/\.md$/, '.html');
const html = buildHtml({
  markdown,
  theme: args.opts.theme || 'apple-tech',
  title: path.basename(inputPath, '.md'),
  includePrint: false,
  includeMermaid: !args.opts['no-mermaid'],
  ogTitle: args.opts['og-title'] || undefined,
  ogDescription: args.opts['og-description'] || undefined,
  ogImage: args.opts['og-image'] || undefined,
  ogUrl: args.opts['og-url'] || undefined,
});

fs.writeFileSync(out, html);
console.error(`✓ ${out}  (theme=${args.opts.theme || 'apple-tech'}${args.opts['og-image'] ? '  +og:image' : ''}${args.opts['og-url'] ? '  +og:url' : ''})`);
