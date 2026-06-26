#!/usr/bin/env node
/**
 * render-dom.js — 将 Pretext 测量结果渲染到真实 DOM 元素
 *
 * 适用场景：
 *   - Accordion（展开折叠，高度由 Pretext 预计算）
 *   - Chat Bubbles（消息气泡，保持精确高度）
 *   - Masonry（瀑布流，高度预测避免 DOM 回流）
 *   - 任何需要将文本渲染到页面的场景
 *
 * 用法：
 *   node scripts/render-dom.js --text "你好，世界！" --font "16px sans-serif" --width 300 --lineHeight 24
 *
 * 输出：
 *   - HTML 片段（可粘贴到浏览器控制台）
 *   - 也可直接被 Node.js require() 使用
 */

const path = require('path');
const SKILL_DIR = path.resolve(__dirname, '..');

// ── 内联 pretext 核心（最小化，不依赖外部模块）───────────────
function unicodeCharWidth(char) {
  const code = char.codePointAt(0);
  if (code >= 0x4E00 && code <= 0x9FFF) return 1.0;
  if (code >= 0x3400 && code <= 0x4DBF) return 1.0;
  if (code >= 0x20000 && code <= 0x2A6DF) return 1.0;
  if (code >= 0xAC00 && code <= 0xD7AF) return 1.0;
  if (code >= 0x3040 && code <= 0x309F) return 1.0;
  if (code >= 0x30A0 && code <= 0x30FF) return 1.0;
  if (code >= 0xFF00 && code <= 0xFFEF) return 1.0;
  if (code >= 0x1F300 && code <= 0x1F9FF) return 1.5;
  if (code >= 0x1FA00 && code <= 0x1FAD6) return 1.5;
  if (code === 0x200D) return 0;
  if (code === 0xFE0F) return 0;
  if (code === 0xFE0E) return 0;
  if (code >= 0x1F1E6 && code <= 0x1F1FF) return 0.8;
  if (/[,.:;!?\-_'\"()\[\]{}—–]/.test(char)) return 0.35;
  if (/[，。、；：？！""''【】《》（）]/.test(char)) return 0.5;
  if (/[@#&$%+=*<>|\\\/^~`]/.test(char)) return 0.5;
  if (char === ' ' || char === '\u00A0') return 0.25;
  if (char === '\t') return 2.0;
  if (char === '\n' || char === '\r') return 0;
  if (/[A-Z]/.test(char)) return 0.7;
  if (/[a-z]/.test(char)) return 0.55;
  if (/[0-9]/.test(char)) return 0.55;
  return 0.55;
}

function estimateWidth(text, fontSize) {
  let w = 0;
  for (const ch of text) w += unicodeCharWidth(ch);
  return w * fontSize;
}

function wrapText(text, maxWidth, fontSize) {
  const lines = [];
  const paras = text.split('\n');
  for (const para of paras) {
    if (!para.trim()) { if (lines.length) lines.push(''); continue; }
    let current = '';
    let currentW = 0;
    for (const ch of para) {
      const chW = unicodeCharWidth(ch) * fontSize;
      if (currentW + chW <= maxWidth) {
        current += ch; currentW += chW;
      } else {
        if (current) lines.push(current);
        current = ch; currentW = chW;
      }
    }
    if (current) lines.push(current);
  }
  return lines;
}

/**
 * 核心渲染函数：将文本渲染为 DOM 行元素数组
 *
 * @param {string} text - 要渲染的文本
 * @param {object} options - 渲染选项
 * @param {string} options.font - CSS font 字符串，如 '16px sans-serif'
 * @param {number} options.width - 最大宽度（px）
 * @param {number} options.lineHeight - 行高（px）
 * @param {string} options.align - 文本对齐：'left' | 'center' | 'right' | 'justify'
 * @param {string} options.tagName - 外层标签名，默认 'div'
 * @param {string} options.lineClass - 每行元素的 class 名
 * @param {string} options.containerId - 容器 ID
 * @returns {object} 渲染结果 { containerHtml, lines, stats }
 */
function renderToDOM(text, options = {}) {
  const {
    font = '16px sans-serif',
    width = 400,
    lineHeight = 24,
    align = 'left',
    tagName = 'div',
    lineClass = 'pretext-line',
    containerId = 'pretext-container',
    fontSize = parseFontSize(font),
  } = options;

  const lines = wrapText(text, width, fontSize);
  const totalHeight = lines.length * lineHeight;

  // 构建行 HTML
  const lineHtmls = lines.map((line, i) => {
    const w = estimateWidth(line, fontSize);
    const alignStyle = align === 'justify' ? 'text-align:justify' : `text-align:${align}`;
    const rpad = align === 'left' || align === 'justify' ? '' : `padding-right:${width - w}px`;
    return `  <${tagName} class="${lineClass}" data-line="${i}" style="height:${lineHeight}px;line-height:${lineHeight}px;font:${font};${alignStyle};${rpad}overflow:hidden;white-space:nowrap;">${escapeHtml(line)}</${tagName}>`;
  });

  const containerHtml = `<${tagName} id="${containerId}" class="pretext-rendered" style="width:${width}px;font:${font};overflow:hidden;">\n${lineHtmls.join('\n')}\n</${tagName}>`;

  // CSS 片段
  const css = `.pretext-rendered { position:relative; overflow:hidden; }\n.${lineClass} { width:${width}px; box-sizing:border-box; }\n`;

  return {
    containerHtml,
    css,
    lines,
    stats: {
      text,
      font,
      width,
      lineHeight,
      fontSize,
      lineCount: lines.length,
      totalHeight,
      maxLineWidth: Math.max(...lines.map(l => estimateWidth(l, fontSize))),
      align,
      renderedAt: new Date().toISOString(),
    },
    // 浏览器控制台粘贴代码
    browserSnippet: `<style>${css}</style>\n${containerHtml}\n<script>
// 动画：逐字高亮
document.querySelectorAll('.${lineClass}').forEach((el, lineIdx) => {
  const text = el.textContent;
  el.innerHTML = text.split('').map((ch, i) =>
    \`<span class="char" data-i="\${i}" style="display:inline-block;transition:all 0.3s \${i*30}ms">\${ch}</span>\`
  ).join('');
  el.addEventListener('mouseenter', () => {
    el.querySelectorAll('.char').forEach(c => { c.style.color = 'hsl(' + (Math.random()*360) + ',80%,50%)'; c.style.transform = 'translateY(-2px)'; });
  });
  el.addEventListener('mouseleave', () => {
    el.querySelectorAll('.char').forEach(c => { c.style.color = ''; c.style.transform = ''; });
  });
});
<\/script>`,
  };
}

/**
 * 流式布局：逐字追加（用于打字机效果、聊天消息等）
 * 返回每一步的布局状态
 *
 * @param {string} text - 完整文本
 * @param {number} maxWidth - 最大宽度
 * @param {number} fontSize - 字号
 * @param {number} lineHeight - 行高
 * @returns {Array} 每一步的 { char, lineIndex, x, y, cursor }
 */
function streamingLayout(text, maxWidth, fontSize, lineHeight) {
  const steps = [];
  let x = 0, y = 0;
  let lineStartIndex = 0;

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '\n') {
      x = 0; y += lineHeight;
      steps.push({ char: ch, lineIndex: steps.filter(s => s.lineIndex === steps[steps.length - 1]?.lineIndex).length, x: 0, y, cursor: i });
      continue;
    }
    if (ch === '\r') continue;

    const chW = unicodeCharWidth(ch) * fontSize;
    if (x + chW > maxWidth) {
      x = chW; y += lineHeight;
    } else {
      x += chW;
    }
    steps.push({ char: ch, x: x - chW, y, width: chW });
  }
  return steps;
}

/**
 * Accordion 场景：给定一组不同高度的文本，预计算每个的 totalHeight
 * 返回可直接渲染的 HTML
 */
function renderAccordion(items, font, width, lineHeight) {
  const result = items.map((item, i) => {
    const lines = wrapText(item.text, width, parseFontSize(font));
    const height = lines.length * lineHeight;
    return {
      ...item,
      height,
      lineCount: lines.length,
      html: `<div class="accordion-item" data-index="${i}">
  <div class="accordion-header" onclick="this.parentElement.classList.toggle('open')">
    <span class="accordion-title">${escapeHtml(item.title)}</span>
    <span class="accordion-icon">▶</span>
  </div>
  <div class="accordion-body" style="height:0;overflow:hidden;transition:height ${item.duration || 300}ms">
    <div class="accordion-content" data-height="${height}" style="padding:1rem;font:${font}">
      ${lines.map(l => `<div style="line-height:${lineHeight}px;height:${lineHeight}px">${escapeHtml(l)}</div>`).join('')}
    </div>
  </div>
</div>`,
    };
  });

  return {
    items: result,
    totalClosedHeight: items.length * 48, // 每个 header 约 48px
    totalOpenHeight: items.reduce((a, it) => a + it.height, 0) + items.length * 48,
    accordionHtml: `<div class="accordion" style="width:${width}px">
  ${result.map(r => r.html).join('\n')}
</div>
<style>
.accordion { font-family:sans-serif; }
.accordion-item { border:1px solid #e0e0e0; border-radius:8px; margin-bottom:8px; overflow:hidden; }
.accordion-header { display:flex; justify-content:space-between; align-items:center; padding:12px 16px; background:#f8f9fa; cursor:pointer; }
.accordion-header:hover { background:#f0f0f0; }
.accordion-icon { transition:transform 0.3s; display:inline-block; }
.accordion-item.open .accordion-icon { transform:rotate(90deg); }
.accordion-item.open .accordion-body { height:var(--h) !important; }
</style>
<script>
document.querySelectorAll('.accordion-content').forEach(el => {
  const h = el.dataset.height + 'px';
  el.closest('.accordion-body').style.setProperty('--h', h);
});
<\/script>`,
  };
}

/**
 * Chat Bubbles 场景：消息气泡流式布局
 */
function renderChatBubbles(messages, font, bubbleWidth, lineHeight) {
  const fontSize = parseFontSize(font);
  return messages.map((msg, i) => {
    const lines = wrapText(msg.text, bubbleWidth - 24, fontSize);
    const isUser = msg.role === 'user';
    return {
      ...msg,
      lineCount: lines.length,
      height: lines.length * lineHeight,
      html: `<div class="chat-bubble ${isUser ? 'user' : 'bot'}" style="align-self:${isUser ? 'flex-end' : 'flex-start'};max-width:${bubbleWidth}px">
  ${lines.map(l => `<div style="line-height:${lineHeight}px;min-height:${lineHeight}px">${escapeHtml(l)}</div>`).join('')}
  <div class="chat-meta">${msg.time || ''}</div>
</div>`,
    };
  });
}

// ── 工具函数 ─────────────────────────────────────────────────
function parseFontSize(font) {
  const m = font.match(/(\d+(?:\.\d+)?)\s*px/i);
  return m ? parseFloat(m[1]) : 16;
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function printUsage() {
  console.log(`
📐 render-dom.js — Pretext DOM 渲染脚本

用法:
  node scripts/render-dom.js --text "文本" [选项...]

必需参数:
  --text          要渲染的文本（支持多行）

可选参数:
  --font          CSS font 字符串，默认 "16px sans-serif"
  --width         最大宽度（px），默认 400
  --lineHeight    行高（px），默认 24
  --align         对齐方式：left | center | right，默认 left
  --mode          渲染模式：dom | accordion | chat | streaming，默认 dom
  --output        输出格式：html | json | snippet，默认 html

示例:
  node scripts/render-dom.js --text "你好，世界！" --width 300 --lineHeight 28
  node scripts/render-dom.js --mode accordion --font "14px sans-serif" --width 320
  node scripts/render-dom.js --mode streaming --text "逐字布局演示" --width 400

输出:
  - HTML 片段（可直接粘贴到浏览器）
  - 逐行信息 + 统计数据
`);
}

// ── CLI 入口 ─────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  const opts = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--text') opts.text = args[++i];
    else if (arg === '--font') opts.font = args[++i];
    else if (arg === '--width') opts.width = parseInt(args[++i]);
    else if (arg === '--lineHeight') opts.lineHeight = parseInt(args[++i]);
    else if (arg === '--align') opts.align = args[++i];
    else if (arg === '--mode') opts.mode = args[++i];
    else if (arg === '--output') opts.output = args[++i];
    else if (arg === '--help' || arg === '-h') { printUsage(); return; }
  }

  if (!opts.text) {
    console.error('❌ 缺少 --text 参数');
    printUsage();
    process.exit(1);
  }

  const font = opts.font || '16px sans-serif';
  const width = opts.width || 400;
  const lineHeight = opts.lineHeight || 24;
  const align = opts.align || 'left';
  const mode = opts.mode || 'dom';
  const output = opts.output || 'html';

  if (mode === 'streaming') {
    const fontSize = parseFontSize(font);
    const steps = streamingLayout(opts.text, width, fontSize, lineHeight);
    const result = { steps, stats: { totalChars: steps.length, fontSize, width, lineHeight } };
    if (output === 'json') {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log('📐 Streaming 布局结果');
      console.log('─'.repeat(50));
      steps.slice(0, 30).forEach(s => {
        process.stdout.write(`[${String(s.x).padStart(4)}px, ${String(s.y).padStart(3)}px] "${s.char}"\n`);
      });
      if (steps.length > 30) console.log(`... 共 ${steps.length} 个字符`);
    }
    return;
  }

  const result = renderToDOM(opts.text, { font, width, lineHeight, align });

  if (output === 'json') {
    console.log(JSON.stringify(result.stats, null, 2));
  } else if (output === 'snippet') {
    console.log('\n🎨 浏览器控制台粘贴代码：\n');
    console.log(result.browserSnippet);
  } else {
    console.log('\n📐 Pretext DOM 渲染结果');
    console.log('═'.repeat(56));
    console.log(`  文本: "${opts.text.substring(0, 40)}${opts.text.length > 40 ? '...' : ''}"`);
    console.log(`  字体: ${font}`);
    console.log(`  宽度: ${width}px  行高: ${lineHeight}px`);
    console.log(`  对齐: ${align}`);
    console.log('─'.repeat(56));
    console.log(`  行数: ${result.stats.lineCount}`);
    console.log(`  总高度: ${result.stats.totalHeight}px`);
    console.log(`  最宽行: ${result.stats.maxLineWidth}px`);
    console.log('─'.repeat(56));
    console.log('\n📄 HTML 片段：\n');
    console.log(result.containerHtml);
    console.log('\n🎨 动画版本（粘贴到浏览器控制台）：\n');
    console.log(result.browserSnippet);
  }
}

if (require.main === module) main();
else module.exports = { renderToDOM, streamingLayout, renderAccordion, renderChatBubbles };
