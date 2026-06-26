#!/usr/bin/env node
/**
 * Pretext Skill — 逐行布局脚本
 * 基于 @chenglou/pretext（MIT License）
 */

'use strict';

let pretext = null, canvasMode = 'unavailable';

// node-canvas
try {
  pretext = require('@chenglou/pretext');
  const { createCanvas } = require('canvas');
  canvasMode = 'canvas';
  global.document = {
    createElement: (tag) => {
      if (tag === 'canvas') return createCanvas(0, 0);
      return { getContext: () => ({}) };
    }
  };
} catch (_) { pretext = null; }

// mock canvas
if (!pretext) {
  try {
    pretext = require('@chenglou/pretext');
    canvasMode = 'mock';
    global.document = {
      createElement: () => ({
        getContext: () => {
          const self = {};
          self.measureText = function(text) {
            const sizeMatch = (self._font || '16px sans-serif').match(/(\d+(?:\.\d+)?)(?:px)?/);
            const fontSize = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
            return { width: estimateTextWidth(text, fontSize) };
          };
          self._font = '16px sans-serif';
          Object.defineProperty(self, 'font', {
            get: () => self._font, set: (v) => { self._font = v; }
          });
          return self;
        }
      })
    };
  } catch (_) { pretext = null; canvasMode = 'unicode-estimate'; }
}

// Unicode fallback
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

function estimateTextWidth(text, fontSize) {
  let total = 0;
  for (const char of text) total += unicodeCharWidth(char);
  return total * fontSize;
}

function createUnicodeFallback() {
  function layoutLines(text, font, width, lineHeight) {
    const sizeMatch = font.match(/(\d+(?:\.\d+)?)(?:px)?/);
    const fontSize = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
    const paragraphs = text.split(/\r?\n/);
    const lines = [];
    let totalHeight = 0;
    let lineIdx = 0;
    for (const para of paragraphs) {
      if (para === '') { totalHeight += lineHeight; continue; }
      const chars = [...para]; let cur = '', curW = 0;
      for (const char of chars) {
        const cw = unicodeCharWidth(char) * fontSize;
        if (curW + cw > width && cur.length > 0) {
          lines.push({ lineIndex: lineIdx++, text: cur, width: curW, y: (lines.length) * lineHeight });
          totalHeight += lineHeight; cur = char; curW = cw;
        } else { cur += char; curW += cw; }
      }
      if (cur.length > 0) { lines.push({ lineIndex: lineIdx++, text: cur, width: curW, y: (lines.length) * lineHeight }); totalHeight += lineHeight; }
      if (para) totalHeight += lineHeight * 0.5;
    }
    return { lines, totalHeight };
  }
  return {
    prepareWithSegments: (text, font) => ({ _type: 'uf', text, font }),
    layoutWithLines: (p, w, lh) => { const r = layoutLines(p.text, p.font, w, lh); return { height: r.totalHeight, lineCount: r.lines.length, lines: r.lines }; }
  };
}

// args
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg.startsWith('--')) {
    const key = arg.slice(2);
    const next = args[i + 1];
    if (next && !next.startsWith('--')) { params[key] = next; i++; }
    else params[key] = true;
  }
}

const text = params.text || '';
const font = params.font || '16px sans-serif';
const width = parseFloat(params.width) || 300;
const lineHeight = parseFloat(params.lineHeight) || 24;

if (!text) { console.error(JSON.stringify({ success: false, error: 'MISSING_TEXT', message: '缺少 --text 参数' }, null, 2)); process.exit(1); }

try {
  const prepared = pretext.prepareWithSegments(text, font);
  const result = pretext.layoutWithLines(prepared, width, lineHeight);

  const lines = result.lines.map((l, idx) => ({
    lineIndex: l.lineIndex !== undefined ? l.lineIndex : idx,
    text: l.text,
    width: Math.round((l.width || 0) * 1000) / 1000,
    y: (l.y != null && !isNaN(l.y)) ? Math.round(l.y * 1000) / 1000 : (l.lineIndex != null ? l.lineIndex : idx) * lineHeight,
    charCount: l.text.length
  }));

  const output = {
    success: true,
    text, font, width, lineHeight,
    totalHeight: Math.round(result.height * 1000) / 1000,
    lineCount: result.lineCount,
    measurementMode: canvasMode,
    lines,
    canvasCode: `// Canvas 绘制 ${result.lineCount} 行文本\nconst ctx = canvas.getContext('2d');\nctx.font = '${font}';\n${lines.map(l => `ctx.fillText('${l.text.replace(/'/g, "\\'")}', 0, ${l.y});`).join('\n')}`
  };
  console.log(JSON.stringify(output, null, 2));
} catch (err) {
  console.error(JSON.stringify({ success: false, error: 'LAYOUT_FAILED', message: err.message }, null, 2));
  process.exit(1);
}
