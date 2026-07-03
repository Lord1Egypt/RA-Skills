#!/usr/bin/env node
/**
 * md-pdf-render — 将 Markdown 转为高保真 PDF，效果与编辑器预览一致
 *
 * 用法: node md-pdf-render.mjs <input.md> [output.pdf] [--css custom.css] [--theme github|vscode]
 *
 * CJK 字体说明：
 *   macOS 自带 "Hiragino Sans GB", "Songti SC", "Heiti SC", "STSong"
 *   Windows 自带 "Microsoft YaHei", "SimSun", "SimHei"
 *   建议安装 Noto Sans CJK SC 以获得最佳跨平台体验
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import MarkdownIt from 'markdown-it';
import markdownItAnchor from 'markdown-it-anchor';
import markdownItTaskLists from 'markdown-it-task-lists';
import { full as markdownItEmoji } from 'markdown-it-emoji';
import texmath from 'markdown-it-texmath';
import katex from 'katex';
import hljs from 'highlight.js';
import puppeteer from 'puppeteer';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ─── 参数解析 ───────────────────────────────────────────────
const args = process.argv.slice(2);
if (args.length === 0 || args.includes('--help')) {
  console.log(`用法: node md-pdf-render.mjs <input.md> [output.pdf] [选项]

选项:
  --css <path>        自定义 CSS 文件路径
  --theme <name>      内置主题: github (默认) | vscode
  --margin <value>    页面边距，如 "20mm"（默认 15mm）
  --format <size>     纸张大小: A4 (默认) | Letter | A3
  --landscape         横向排版
  --toc               生成目录
  --mermaid           启用 Mermaid 图表渲染（默认禁用）
  --header <text>     页眉文本（支持 %title%, %page%, %total%）
  --footer <text>     页脚文本（支持 %title%, %page%, %total%）
  --no-math           禁用数学公式渲染
  --no-emoji          禁用 Emoji 渲染
  --pagebreak         在每段 h1 标题前自动分页（适用于书籍章节合集）
  --timeout <ms>      超时时间（毫秒），默认 60000
  --help              显示帮助`);
  process.exit(0);
}

function getArg(flag) {
  const idx = args.indexOf(flag);
  if (idx === -1) return null;
  return args[idx + 1];
}

const inputFile = args.find(a => !a.startsWith('--') && a.endsWith('.md'));
if (!inputFile) {
  console.error('错误: 请指定输入的 Markdown 文件');
  process.exit(1);
}

const outputFile = args.find(a => !a.startsWith('--') && a.endsWith('.pdf'))
  || inputFile.replace(/\.md$/, '.pdf');
const customCss = getArg('--css');
const theme = getArg('--theme') || 'github';
const margin = getArg('--margin') || '15mm';
const format = getArg('--format') || 'A4';
const landscape = args.includes('--landscape');
const toc = args.includes('--toc');
const mermaid = args.includes('--mermaid');
const headerText = getArg('--header');
const footerText = getArg('--footer');
const noMath = args.includes('--no-math');
const noEmoji = args.includes('--no-emoji');
const pagebreak = args.includes('--pagebreak');
const timeout = parseInt(getArg('--timeout')) || 60000;

// ─── Markdown 渲染 ──────────────────────────────────────────
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    // 特殊处理 mermaid 代码块 - 保留原始 class 用于后续渲染
    if (lang === 'mermaid') {
      return `<pre><code class="language-mermaid">${md.utils.escapeHtml(str)}</code></pre>`;
    }
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`;
      } catch (_) {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  }
});

// 基础插件
md.use(markdownItAnchor);
md.use(markdownItTaskLists, { enabled: true });

// Emoji 支持
if (!noEmoji) {
  md.use(markdownItEmoji);
  // 自定义 emoji 渲染（使用 Twemoji CDN）
  md.renderer.rules.emoji = function(tokens, idx) {
    const emoji = tokens[idx].markup;
    return `<span class="emoji" title=":${emoji}:">:${emoji}:</span>`;
  };
}

// 数学公式支持 (KaTeX)
if (!noMath) {
  md.use(texmath, {
    engine: katex,
    delimiters: 'dollars',
    katexOptions: {
      macros: {
        '\\R': '\\mathbb{R}',
        '\\N': '\\mathbb{N}',
        '\\Z': '\\mathbb{Z}',
        '\\Q': '\\mathbb{Q}',
        '\\C': '\\mathbb{C}'
      }
    }
  });
}

let markdown = fs.readFileSync(inputFile, 'utf-8');

// ─── 分页标记处理 ─────────────────────────────────────────────
// 支持 Markdown 中的 <!-- pagebreak --> 注释，替换为分页 div
markdown = markdown.replace(/<!--\s*pagebreak\s*-->/gi, '<div class="page-break"></div>\n');

let htmlBody = md.render(markdown);

// --pagebreak 模式：在每个 h1 前自动分页（第一个除外）
if (pagebreak) {
  // 在第一个 h1 上标记 skip，其余 h1 前插入分页
  htmlBody = htmlBody.replace(/<h1/g, (match, offset) => {
    // 第一个出现的 h1 不加分页
    if (htmlBody.indexOf('<h1') === offset) {
      return '<h1 class="no-page-break"';
    }
    return '<div class="page-break"></div>\n<h1';
  });
}

// ─── TOC 生成 ────────────────────────────────────────────────
if (toc) {
  const tocItems = [];
  const headingRegex = /<h([1-3]) id="([^"]*)"[^>]*>(.*?)<\/h[1-3]>/g;
  let match;
  while ((match = headingRegex.exec(htmlBody)) !== null) {
    const level = parseInt(match[1]);
    const id = match[2];
    const text = match[3].replace(/<[^>]+>/g, '');
    tocItems.push({ level, id, text });
  }
  if (tocItems.length > 0) {
    let tocHtml = '<div class="toc"><h2>目录</h2><ul>';
    for (const item of tocItems) {
      tocHtml += `<li class="toc-level-${item.level}"><a href="#${item.id}">${item.text}</a></li>`;
    }
    tocHtml += '</ul></div><hr>';
    htmlBody = tocHtml + htmlBody;
  }
}

// ─── 主题 CSS ────────────────────────────────────────────────
const themes = {
  github: `
    :root {
      --color-fg: #1f2328;
      --color-bg: #ffffff;
      --color-border: #d1d9e0;
      --color-link: #0969da;
      --color-code-bg: #f6f8fa;
      --color-blockquote: #656d76;
      --font-body: "Hiragino Sans GB", "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "WenQuanYi Micro Hei", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
      --font-code: "Hiragino Sans GB", "PingFang SC", "Microsoft YaHei", ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    }
  `,
  vscode: `
    :root {
      --color-fg: #d4d4d4;
      --color-bg: #1e1e1e;
      --color-border: #3e3e3e;
      --color-link: #4fc1ff;
      --color-code-bg: #2d2d2d;
      --color-blockquote: #9e9e9e;
      --font-body: "Hiragino Sans GB", "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "WenQuanYi Micro Hei", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --font-code: "Hiragino Sans GB", "PingFang SC", "Microsoft YaHei", "Cascadia Code", Menlo, Monaco, "Courier New", monospace;
    }
  `
};

const baseCSS = `
${themes[theme] || themes.github}

* { box-sizing: border-box; }

body {
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-fg);
  background: var(--color-bg);
  max-width: 980px;
  margin: 0 auto;
  padding: 24px;
  word-wrap: break-word;
}

h1, h2, h3, h4, h5, h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  /* 标题避免在页面底部被截断 */
  break-after: avoid;
  page-break-after: avoid;
}
h1 { font-size: 2em; padding-bottom: 0.3em; border-bottom: 1px solid var(--color-border); }
h2 { font-size: 1.5em; padding-bottom: 0.3em; border-bottom: 1px solid var(--color-border); }
h3 { font-size: 1.25em; }
h4 { font-size: 1em; }

a { color: var(--color-link); text-decoration: none; }
a:hover { text-decoration: underline; }

p { margin-top: 0; margin-bottom: 16px; }

blockquote {
  margin: 0 0 16px 0;
  padding: 0 1em;
  color: var(--color-blockquote);
  border-left: 0.25em solid var(--color-border);
}

code {
  font-family: var(--font-code);
  font-size: 85%;
  padding: 0.2em 0.4em;
  background: var(--color-code-bg);
  border-radius: 6px;
}

pre {
  margin-bottom: 16px;
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background: var(--color-code-bg);
  border-radius: 6px;
  /* 代码块避免被截断到两页 */
  break-inside: avoid;
  page-break-inside: avoid;
}
pre code {
  padding: 0;
  background: transparent;
  border-radius: 0;
  font-size: 100%;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 16px;
  /* 表格避免被截断 */
  break-inside: avoid;
  page-break-inside: avoid;
}
th, td {
  padding: 6px 13px;
  border: 1px solid var(--color-border);
}
th { font-weight: 600; background: var(--color-code-bg); }
tr:nth-child(2n) { background: var(--color-code-bg); }

img { max-width: 100%; height: auto; }

hr {
  height: 0.25em;
  padding: 0;
  margin: 24px 0;
  background-color: var(--color-border);
  border: 0;
}

ul, ol { padding-left: 2em; margin-bottom: 16px; }
li + li { margin-top: 0.25em; }

/* 列表项避免被截断 */
li {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* Task list */
.task-list-item { list-style-type: none; }
.task-list-item input { margin: 0 0.35em 0 -1.6em; vertical-align: middle; }

/* TOC */
.toc { margin-bottom: 24px; }
.toc ul { list-style: none; padding-left: 0; }
.toc-level-2 { padding-left: 1.5em; }
.toc-level-3 { padding-left: 3em; }
.toc a { color: var(--color-link); }

/* highlight.js overrides */
.hljs { background: var(--color-code-bg) !important; color: var(--color-fg); }

/* 数学公式样式 */
.katex-display {
  margin: 16px 0;
  overflow-x: auto;
  overflow-y: hidden;
}
.katex {
  font-size: 1.1em;
}

/* Emoji 样式 */
.emoji {
  font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji";
  font-size: 1.2em;
}

/* 分页控制 */
.page-break {
  page-break-before: always;
  break-before: page;
}

/* 避免孤立/widow */
p, li {
  orphans: 3;
  widows: 3;
}
`;

// ─── 组装 HTML ───────────────────────────────────────────────
let extraCss = '';
if (customCss) {
  extraCss = fs.readFileSync(customCss, 'utf-8');
}

// highlight.js CSS
const hljsCssPath = path.join(__dirname, 'node_modules', 'highlight.js', 'styles',
  theme === 'vscode' ? 'vs2015.css' : 'github.css');
const hljsCss = fs.existsSync(hljsCssPath) ? fs.readFileSync(hljsCssPath, 'utf-8') : '';

// KaTeX CSS
const katexCssPath = path.join(__dirname, 'node_modules', 'katex', 'dist', 'katex.min.css');
const katexCss = (!noMath && fs.existsSync(katexCssPath)) ? fs.readFileSync(katexCssPath, 'utf-8') : '';

// Mermaid 支持
const mermaidScript = mermaid ? `
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
    startOnLoad: false,
    theme: '${theme === 'vscode' ? 'dark' : 'default'}',
    securityLevel: 'loose',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
  });
  
  // 渲染所有 mermaid 代码块
  async function renderMermaid() {
    const codeBlocks = document.querySelectorAll('code.language-mermaid');
    for (let i = 0; i < codeBlocks.length; i++) {
      const code = codeBlocks[i];
      const pre = code.parentElement;
      const graphDefinition = code.textContent;
      const graphId = 'mermaid-' + i;
      
      try {
        const { svg } = await mermaid.render(graphId, graphDefinition);
        const div = document.createElement('div');
        div.className = 'mermaid';
        div.innerHTML = svg;
        pre.replaceWith(div);
      } catch (error) {
        console.error('Mermaid rendering error:', error);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'mermaid-error';
        errorDiv.innerHTML = '<p style="color: red;">Mermaid 渲染错误: ' + error.message + '</p><pre>' + graphDefinition + '</pre>';
        pre.replaceWith(errorDiv);
      }
    }
  }
  
  // 等待 DOM 加载完成后渲染
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderMermaid);
  } else {
    renderMermaid();
  }
</script>
` : '';

const mermaidStyles = mermaid ? `
/* Mermaid 图表样式 */
.mermaid {
  text-align: center;
  margin: 16px 0;
  overflow-x: auto;
  /* Mermaid 图表避免被截断 */
  break-inside: avoid;
  page-break-inside: avoid;
}
.mermaid svg {
  max-width: 100%;
  height: auto;
}
.mermaid-error {
  background: #fff3f3;
  border: 1px solid #ffcccc;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
}
.mermaid-error pre {
  background: #f8f8f8;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
}
` : '';

const fullHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>${hljsCss}</style>
  <style>${katexCss}</style>
  <style>${baseCSS}</style>
  <style>${extraCss}</style>
  <style>${mermaidStyles}</style>
</head>
<body>${htmlBody}</body>
${mermaidScript}
</html>`;

// ─── PDF 生成 ────────────────────────────────────────────────
console.log(`转换中: ${inputFile} → ${outputFile}`);
console.log(`主题: ${theme} | 纸张: ${format} | 边距: ${margin}${mermaid ? ' | Mermaid: 启用' : ''}${!noMath ? ' | KaTeX: 启用' : ''}${!noEmoji ? ' | Emoji: 启用' : ''}${pagebreak ? ' | 章节分页: 启用' : ''}`);

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setContent(fullHtml, { waitUntil: 'load', timeout });

// 如果启用了 mermaid，等待渲染完成
if (mermaid) {
  console.log('正在渲染 Mermaid 图表...');
  // 等待所有 mermaid 图表渲染完成
  await page.waitForFunction(() => {
    const mermaidElements = document.querySelectorAll('.mermaid');
    const errorElements = document.querySelectorAll('.mermaid-error');
    const codeBlocks = document.querySelectorAll('code.language-mermaid');
    // 如果没有 mermaid 代码块了，说明渲染完成
    return codeBlocks.length === 0;
  }, { timeout: 30000 });
  
  // 额外等待确保 SVG 完全渲染
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // 验证渲染结果
  const mermaidCount = await page.evaluate(() => document.querySelectorAll('.mermaid svg').length);
  const errorCount = await page.evaluate(() => document.querySelectorAll('.mermaid-error').length);
  console.log(`Mermaid 图表渲染完成: ${mermaidCount} 个成功, ${errorCount} 个失败`);
}

// 生成 PDF 书签/大纲
await page.evaluate(() => {
  // 为所有标题添加 PDF 书签属性
  const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
  headings.forEach((heading, index) => {
    heading.setAttribute('data-pdf-outline', 'true');
    heading.setAttribute('data-pdf-level', heading.tagName.charAt(1));
  });
});

// 构建页眉页脚模板
const defaultHeaderTemplate = `
<div style="font-size: 8px; width: 100%; text-align: center; color: #666; padding: 5px 50px;">
  ${headerText ? headerText.replace('%title%', path.basename(inputFile, '.md')) : ''}
</div>`;

const defaultFooterTemplate = `
<div style="font-size: 8px; width: 100%; text-align: center; color: #666; padding: 5px 50px;">
  ${footerText ? footerText
    .replace('%page%', '<span class="pageNumber"></span>')
    .replace('%total%', '<span class="totalPages"></span>')
    .replace('%title%', path.basename(inputFile, '.md'))
  : '<span class="pageNumber"></span> / <span class="totalPages"></span>'}
</div>`;

const pdfOptions = {
  path: outputFile,
  format,
  landscape,
  margin: { top: margin, right: margin, bottom: margin, left: margin },
  printBackground: true,
  displayHeaderFooter: Boolean(headerText || footerText),
  headerTemplate: defaultHeaderTemplate,
  footerTemplate: defaultFooterTemplate,
  // 生成 PDF 书签/大纲
  outline: true,
  // 标签化 PDF（可访问性）
  tagged: true,
};

await page.pdf(pdfOptions);

await browser.close();
console.log(`完成: ${outputFile}`);
