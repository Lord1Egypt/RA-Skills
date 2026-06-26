#!/usr/bin/env node
/**
 * Pretext Skill — 文本绕排布局脚本
 * 基于 @chenglou/pretext（MIT License）
 *
 * 功能：模拟文本围绕浮动元素（如图片、侧边栏）排版
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
if (!pretext) pretext = createWrapFallback();

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
function createWrapFallback() {
  return {
    prepareWithSegments: (text, font) => ({ _type: 'wf', text, font }),
    layoutNextLineRange: () => null,
    materializeLineRange: () => ({ text: '', width: 0 })
  };
}

// args
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg.startsWith('--')) { const key = arg.slice(2); const next = args[i + 1]; if (next && !next.startsWith('--')) { params[key] = next; i++; } else params[key] = true; }
}

const text = params.text || '', font = params.font || '16px sans-serif', width = parseFloat(params.width) || 600;
const floatWidth = parseFloat(params.floatWidth) || 200, floatHeight = parseFloat(params.floatHeight) || 200;
const lineHeight = parseFloat(params.lineHeight) || 22, floatSide = params.floatSide || 'left';

if (!text) { console.error(JSON.stringify({ success: false, error: 'MISSING_TEXT', message: '缺少 --text 参数' }, null, 2)); process.exit(1); }

// 使用 wrap 算法的纯 JS 实现
const sizeMatch = font.match(/(\d+(?:\.\d+)?)(?:px)?/);
const fontSize = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
const floatBottom = floatHeight;
let y = 0, lineIdx = 0, cursor = 0;
const lines = [];
const chars = [...text];

while (cursor < chars.length) {
  const effectiveWidth = y < floatBottom ? width - floatWidth : width;
  let cur = '', curW = 0, wrapped = false;
  while (cursor < chars.length) {
    const char = chars[cursor];
    const cw = unicodeCharWidth(char) * fontSize;
    if (curW + cw > effectiveWidth && cur.length > 0) { wrapped = true; break; }
    cur += char; curW += cw; cursor++;
  }
  if (cur.length === 0) break;
  const xOffset = (floatSide === 'left' && y < floatBottom) ? floatWidth : 0;
  lines.push({ lineIndex: lineIdx++, text: cur, width: Math.round(curW * 1000) / 1000, x: xOffset, y: Math.round(y * 1000) / 1000, inFloatZone: y < floatBottom });
  y += lineHeight;
  if (!wrapped && cursor < chars.length) cursor++; else if (wrapped) {}
}
if (lines.length === 0 && text.length > 0) {
  lines.push({ lineIndex: 0, text: text.slice(0, 20), width: 0, x: 0, y: 0, inFloatZone: false });
}

const output = {
  success: true, text, font, containerWidth: width, floatWidth, floatHeight, floatSide, lineHeight,
  lineCount: lines.length, totalHeight: Math.round(y * 1000) / 1000, measurementMode: canvasMode,
  lines,
  canvasCode: `// Canvas 绘制文本绕排（浮动元素 ${floatSide}侧）\nconst ctx = canvas.getContext('2d');\nctx.font = '${font}';\n${lines.map(l => `ctx.fillText('${l.text.replace(/'/g, "\\'")}', ${l.x}, ${l.y});`).join('\n')}`,
  layoutAdvice: {
    containerHeight: Math.round(y) + 'px',
    floatPosition: floatSide === 'left' ? `左浮动，left:0, top:0, width:${floatWidth}px, height:${floatHeight}px` : `右浮动，right:0, top:0, width:${floatWidth}px, height:${floatHeight}px`
  }
};
console.log(JSON.stringify(output, null, 2));
