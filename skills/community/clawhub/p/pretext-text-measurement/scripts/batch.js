#!/usr/bin/env node
/**
 * Pretext Skill — 批量测量脚本
 * 基于 @chenglou/pretext（MIT License）
 */

'use strict';

let pretext = null, canvasMode = 'unavailable';
try {
  pretext = require('@chenglou/pretext');
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
if (!pretext) pretext = createUnicodeFallback();

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
function measureItem(text, font, width, lineHeight) {
  const sizeMatch = font.match(/(\d+(?:\.\d+)?)(?:px)?/);
  const fontSize = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
  const paragraphs = text.split(/\r?\n/);
  let totalHeight = 0, lineCount = 0, cur = '', curW = 0;
  function flush() { if (cur.length > 0) { totalHeight += lineHeight; lineCount++; cur = ''; curW = 0; } }
  for (const para of paragraphs) {
    if (para === '') { flush(); totalHeight += lineHeight * 0.5; continue; }
    for (const char of para) {
      const cw = unicodeCharWidth(char) * fontSize;
      if (curW + cw > width && cur.length > 0) { flush(); cur += char; curW = cw; }
      else { cur += char; curW += cw; }
    }
  }
  flush();
  return { height: totalHeight, lineCount };
}
function createUnicodeFallback() {
  return {
    prepare: (text, font) => ({ _type: 'uf', text, font }),
    layout: (p, w, lh) => { const r = measureItem(p.text, p.font, w, lh); return { height: r.height, lineCount: r.lineCount }; }
  };
}

// args
const args = process.argv.slice(2);
const params = {}; let items = [];
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '--items') { items.push(args[i + 1]); i++; }
  else if (arg.startsWith('--')) { const key = arg.slice(2); const next = args[i + 1]; if (next && !next.startsWith('--')) { params[key] = next; i++; } else params[key] = true; }
}
if (params.items) { try { items = JSON.parse(params.items); } catch (_) { items = [params.items]; } }

const font = params.font || '16px sans-serif', width = parseFloat(params.width) || 300, lineHeight = parseFloat(params.lineHeight) || 20;

if (items.length === 0) {
  console.error(JSON.stringify({ success: false, error: 'MISSING_ITEMS', message: '请提供 --items 参数，至少一条文本', usage: 'node batch.js --items "文本1" --items "文本2" --font "14px Inter" --width 375' }, null, 2));
  process.exit(1);
}

try {
  const results = items.map((text, idx) => {
    const layout = pretext.layout(pretext.prepare(text, font), width, lineHeight);
    return { index: idx, text, textPreview: text.length > 30 ? text.slice(0, 30) + '...' : text, height: Math.round(layout.height * 1000) / 1000, lineCount: layout.lineCount, cssHeight: Math.round(layout.height) + 'px' };
  });

  const totalHeight = results.reduce((s, r) => s + r.height, 0);
  const avgHeight = totalHeight / results.length;
  const maxHeight = Math.max(...results.map(r => r.height));
  const wrappedCount = results.filter(r => r.lineCount > 1).length;

  const output = {
    success: true, font, width, lineHeight, itemCount: items.length,
    measurementMode: canvasMode,
    summary: { totalHeight: Math.round(totalHeight * 1000) / 1000, averageHeight: Math.round(avgHeight * 1000) / 1000, maxItemHeight: maxHeight, wrappedItems: wrappedCount, wrappedRatio: Math.round(wrappedCount / items.length * 100) + '%' },
    items: results,
    virtualScrollHint: `总高度 ${Math.round(totalHeight)}px，平均每条 ${Math.round(avgHeight)}px，可直接用于虚拟滚动容器初始化`
  };
  console.log(JSON.stringify(output, null, 2));
} catch (err) {
  console.error(JSON.stringify({ success: false, error: 'BATCH_FAILED', message: err.message }, null, 2));
  process.exit(1);
}
