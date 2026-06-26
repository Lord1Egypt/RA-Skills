#!/usr/bin/env node
/**
 * Pretext Skill — 行统计脚本（性能最优）
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
function createUnicodeFallback() {
  function doLayout(text, fontSize, width) {
    const paragraphs = text.split(/\r?\n/);
    const lines = []; let cur = '', curW = 0;
    for (const para of paragraphs) {
      if (para === '') { if (cur) { lines.push(curW); cur = ''; curW = 0; } continue; }
      for (const char of para) {
        const cw = unicodeCharWidth(char) * fontSize;
        if (curW + cw > width && cur.length > 0) { lines.push(curW); cur = char; curW = cw; }
        else { cur += char; curW += cw; }
      }
    }
    if (cur.length > 0) lines.push(curW);
    return lines;
  }
  return {
    prepareWithSegments: (text, font) => {
      const sizeMatch = font.match(/(\d+(?:\.\d+)?)(?:px)?/);
      return { _type: 'uf', text, fontSize: sizeMatch ? parseFloat(sizeMatch[1]) : 16 };
    },
    measureLineStats: (p, w) => {
      const lines = doLayout(p.text, p.fontSize, w);
      const maxLineWidth = lines.reduce ? lines.reduce((m, v) => Math.max(m, v), 0) : 0;
      return { lineCount: lines.length, maxLineWidth };
    },
    measureNaturalWidth: (p) => estimateTextWidth(p.text, p.fontSize)
  };
}

const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg.startsWith('--')) { const key = arg.slice(2); const next = args[i + 1]; if (next && !next.startsWith('--')) { params[key] = next; i++; } else params[key] = true; }
}

const text = params.text || '', font = params.font || '16px sans-serif', width = parseFloat(params.width) || 300;
if (!text) { console.error(JSON.stringify({ success: false, error: 'MISSING_TEXT', message: '缺少 --text 参数' }, null, 2)); process.exit(1); }

try {
  const prepared = pretext.prepareWithSegments(text, font);
  const stats = pretext.measureLineStats(prepared, width);
  const naturalWidth = pretext.measureNaturalWidth ? pretext.measureNaturalWidth(prepared) : stats.maxLineWidth;
  const output = {
    success: true, text, font, width,
    lineCount: stats.lineCount,
    maxLineWidth: Math.round(stats.maxLineWidth * 1000) / 1000,
    naturalWidth: Math.round(naturalWidth * 1000) / 1000,
    measurementMode: canvasMode,
    analysis: {
      wouldWrap: stats.lineCount > 1,
      fitsInWidth: naturalWidth <= width,
      verdict: stats.lineCount > 1 ? `文本在 ${width}px 宽度下会换行 ${stats.lineCount} 行` : `文本在 ${width}px 宽度下不换行`,
      shrinkToFit: naturalWidth > width ? `需要至少 ${Math.ceil(naturalWidth)}px 才能不换行` : `当前宽度 ${width}px 足够，最宽行 ${Math.ceil(naturalWidth)}px`
    }
  };
  console.log(JSON.stringify(output, null, 2));
} catch (err) {
  console.error(JSON.stringify({ success: false, error: 'STATS_FAILED', message: err.message }, null, 2));
  process.exit(1);
}
