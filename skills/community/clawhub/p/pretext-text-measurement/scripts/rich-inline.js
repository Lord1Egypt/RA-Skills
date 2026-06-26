#!/usr/bin/env node
/**
 * Pretext Skill — 富文本内联布局脚本
 * 基于 @chenglou/pretext/rich-inline（MIT License）
 *
 * 功能：测量含不同样式片段的富文本（@提及、#标签、代码块）高度
 * 用法：node rich-inline.js --items '[{"text":"文字","font":"16px Inter"},{"text":"@用户","font":"bold 14px Inter","break":"never"}]' --width 300
 */

'use strict';

let pretext = null, canvasMode = 'unavailable';
try {
  pretext = require('@chenglou/pretext/rich-inline');
  const { createCanvas } = require('canvas');
  canvasMode = 'canvas';
  global.document = { createElement: (tag) => { if (tag === 'canvas') return createCanvas(0, 0); return { getContext: () => ({}) }; } };
} catch (_) { pretext = null; }
if (!pretext) {
  try {
    pretext = require('@chenglou/pretext');
    canvasMode = 'mock';
    global.document = { createElement: () => ({ getContext: () => {
      const self = {};
      self.measureText = function(text) {
        const sizeMatch = (self._font || '16px sans-serif').match(/(\d+(?:\.\d+)?)(?:px)?/);
        return { width: estimateTextWidth(text, sizeMatch ? parseFloat(sizeMatch[1]) : 16) };
      };
      self._font = '16px sans-serif';
      Object.defineProperty(self, 'font', { get: () => self._font, set: (v) => { self._font = v; } });
      return self;
    }}) };
  } catch (_) { pretext = null; canvasMode = 'unicode-estimate'; }
}
if (!pretext) pretext = createRichInlineFallback();

// 共享的 Unicode 估算
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
  if (/[,.:;!?\-_'"()[\]{}—–]/.test(char)) return 0.35;
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
function estimateTextWidth(text, fontSize) { let total = 0; for (const c of text) total += unicodeCharWidth(c); return total * fontSize; }

// Rich-inline 的纯 JS fallback
function createRichInlineFallback() {
  function layoutRich(items, width, lineHeight) {
    const lines = []; let curLine = [], curWidth = 0, lineY = 0;
    for (const item of items) {
      const sizeMatch = (item.font || '16px sans-serif').match(/(\d+(?:\.\d+)?)(?:px)?/);
      const fontSize = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
      const itemWidth = estimateTextWidth(item.text, fontSize) + (item.extraWidth || 0);
      const breakNever = item.break === 'never';
      if (!breakNever && curWidth + itemWidth > width && curLine.length > 0) {
        lines.push({ fragments: curLine, width: curWidth, y: lineY });
        lineY += lineHeight; curLine = [{ ...item, occupiedWidth: itemWidth }]; curWidth = itemWidth;
      } else {
        curLine.push({ ...item, occupiedWidth: itemWidth }); curWidth += itemWidth;
      }
    }
    if (curLine.length > 0) { lines.push({ fragments: curLine, width: curWidth, y: lineY }); lineY += lineHeight; }
    return { lines, totalHeight: lineY };
  }
  return {
    prepareRichInline: (items) => ({ _type: 'rf', items }),
    walkRichInlineLineRanges: (prepared, width, onLine) => {
      const result = layoutRich(prepared.items, width, 24);
      for (const line of result.lines) onLine(line);
      return result.lines.length;
    }
  };
}

// args
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg.startsWith('--')) { const key = arg.slice(2); const next = args[i + 1]; if (next && !next.startsWith('--')) { params[key] = next; i++; } else params[key] = true; }
}

let items = [];
if (params.items) {
  try { items = JSON.parse(params.items); }
  catch (e) { console.error(JSON.stringify({ success: false, error: 'INVALID_JSON', message: 'items 参数必须是有效 JSON 数组', example: '--items \'[{"text":"文字","font":"16px Inter"}]\'' }, null, 2)); process.exit(1); }
}
const width = parseFloat(params.width) || 300, lineHeight = parseFloat(params.lineHeight) || 24;

if (!items || items.length === 0) {
  console.error(JSON.stringify({ success: false, error: 'MISSING_ITEMS', message: '缺少 --items 参数，需提供 JSON 数组', example: 'node rich-inline.js --items \'[{"text":"@maya","font":"bold 14px Inter","break":"never","extraWidth":22}]\' --width 300' }, null, 2));
  process.exit(1);
}

try {
  const prepared = pretext.prepareRichInline(items);
  let lineCount = 0, totalHeight = 0;
  const lines = [];
  pretext.walkRichInlineLineRanges(prepared, width, (range) => {
    lineCount++;
    totalHeight = lineCount * lineHeight;
    lines.push({ lineIndex: lineCount - 1, fragments: (range.fragments || []).map(f => ({ text: f.text, font: f.font || 'unknown', occupiedWidth: Math.round((f.occupiedWidth || 0) * 1000) / 1000 })), width: Math.round((range.width || 0) * 1000) / 1000, y: (lineCount - 1) * lineHeight });
  });
  if (lineCount === 0) { lineCount = 1; totalHeight = lineHeight; }

  const output = {
    success: true, width, lineHeight, lineCount, totalHeight: Math.round(totalHeight * 1000) / 1000,
    measurementMode: canvasMode,
    lines,
    renderingHint: { cssHeight: Math.round(totalHeight) + 'px', fragmentCount: lines.reduce((s, l) => s + (l.fragments?.length || 0), 0), note: '每行可能有多个不同字体的片段，需分别设置 font 属性绘制' }
  };
  console.log(JSON.stringify(output, null, 2));
} catch (err) {
  console.error(JSON.stringify({ success: false, error: 'RICH_INLINE_FAILED', message: err.message }, null, 2));
  process.exit(1);
}
