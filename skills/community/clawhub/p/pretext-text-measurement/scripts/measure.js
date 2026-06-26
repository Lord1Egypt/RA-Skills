#!/usr/bin/env node
/**
 * Pretext Skill — 核心测量脚本
 * 基于 @chenglou/pretext（MIT License）
 * Copyright (c) 2026 Pretext contributors
 *
 * 功能：纯算术文本测量，无需触碰 DOM
 * 环境：自动检测最佳运行模式
 *   - 优先：@chenglou/pretext + node-canvas → 高精度
 *   - 其次：@chenglou/pretext + 全局 document mock（无 canvas）→ 标准精度
 *   - 最后：纯 JS Unicode 估算 fallback → 功能可用，精度中等
 */

'use strict';

const path = require('path');
const SKILL_DIR = __dirname;

// ============================================================
//  Canvas 兼容层
// ============================================================

let canvasMode = 'unavailable';
let pretext = null;

// 模式 A：@chenglou/pretext + node-canvas
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

// 模式 B：@chenglou/pretext + 纯 mock（无 canvas 库）
if (!pretext) {
  try {
    pretext = require('@chenglou/pretext');
    canvasMode = 'mock';
    global.document = {
      createElement: () => ({
        getContext: () => {
          // 使用 Node.js 内置 TextEncoder + 启发式估算
          const self = {};
          self.measureText = function(text) {
            const sizeMatch = (self._font || '16px sans-serif').match(/(\d+(?:\.\d+)?)(?:px)?/);
            const fontSize = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
            const width = estimateTextWidth(text, fontSize);
            return { width };
          };
          self._font = '16px sans-serif';
          Object.defineProperty(self, 'font', {
            get: () => self._font,
            set: (v) => { self._font = v; }
          });
          return self;
        }
      })
    };
  } catch (_) {
    pretext = null;
    canvasMode = 'unicode-estimate';
  }
}

// ============================================================
//  Unicode 启发式估算（最终 fallback）
// ============================================================

function unicodeCharWidth(char) {
  const code = char.codePointAt(0);
  // CJK：中日韩表意文字、日文假名、韩文字母 → 1 个 em 宽度
  if (code >= 0x4E00 && code <= 0x9FFF) return 1.0;    // 中日韩表意文字
  if (code >= 0x3400 && code <= 0x4DBF) return 1.0;   // CJK Extension A
  if (code >= 0x20000 && code <= 0x2A6DF) return 1.0; // CJK Extension B-F
  if (code >= 0xAC00 && code <= 0xD7AF) return 1.0;   // 韩文字母
  if (code >= 0x3040 && code <= 0x309F) return 1.0;   // 日文平假名
  if (code >= 0x30A0 && code <= 0x30FF) return 1.0;   // 日文片假名
  if (code >= 0xFF00 && code <= 0xFFEF) return 1.0;   // 全角符号
  // Emoji 组合序列
  if (code >= 0x1F300 && code <= 0x1F9FF) return 1.5; // 杂项符号和 emoji
  if (code >= 0x1FA00 && code <= 0x1FAD6) return 1.5; // emoji 扩展
  // Emoji 修饰序列（ZWJ 连接符视为零宽）
  if (code === 0x200D) return 0; // 零宽连接符
  if (code === 0xFE0F) return 0; // emoji 变体选择符
  if (code === 0xFE0E) return 0; // text 变体选择符
  // 国家/地区旗帜 → 2 个零宽字符组合
  if (code >= 0x1F1E6 && code <= 0x1F1FF) return 0.8;
  // 标点符号
  if (/[,.:;!?\-_'"()[\]{}—–]/.test(char)) return 0.35;
  if (/[，。、；：？！""''【】《》（）]/.test(char)) return 0.5;
  if (/[@#&$%+=*<>|\\\/^~`]/.test(char)) return 0.5;
  // 空格
  if (char === ' ' || char === '\u00A0') return 0.25;
  if (char === '\t') return 2.0;
  if (char === '\n' || char === '\r') return 0;
  // 拉丁字母、数字 → 约 0.55 em（大多数 sans-serif 字体中 x-height 比例）
  if (/[A-Z]/.test(char)) return 0.7;
  if (/[a-z]/.test(char)) return 0.55;
  if (/[0-9]/.test(char)) return 0.55;
  return 0.55; // 通用 fallback（俄文、泰文等）
}

function estimateTextWidth(text, fontSize) {
  let total = 0;
  for (const char of text) {
    total += unicodeCharWidth(char);
  }
  return total * fontSize;
}

function unicodeFallbackPrepare(text, font) {
  const sizeMatch = font.match(/(\d+(?:\.\d+)?)(?:px)?/);
  const fontSize = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
  return { _type: 'uf', text, font, fontSize };
}

function unicodeFallbackLayout(prepared, maxWidth, lineHeight) {
  if (prepared._type !== 'uf') throw new Error('Invalid prepared object');
  const { text, fontSize } = prepared;
  const lines = [];
  let totalHeight = 0;

  const paragraphs = text.split(/\r?\n/);
  for (let p = 0; p < paragraphs.length; p++) {
    const para = paragraphs[p];
    if (para === '') { totalHeight += lineHeight; continue; }
    const chars = [...para];
    let cur = '', curW = 0;
    for (const char of chars) {
      const cw = unicodeCharWidth(char) * fontSize;
      if (curW + cw > maxWidth && cur.length > 0) {
        lines.push({ text: cur, width: curW });
        totalHeight += lineHeight;
        cur = char; curW = cw;
      } else {
        cur += char; curW += cw;
      }
    }
    if (cur.length > 0) { lines.push({ text: cur, width: curW }); totalHeight += lineHeight; }
    if (p < paragraphs.length - 1) totalHeight += lineHeight * 0.5;
  }

  return { lines, height: totalHeight, lineCount: lines.length };
}

// 最终：如果 pretext 不可用，用纯估算对象
if (!pretext) {
  pretext = {
    prepare: unicodeFallbackPrepare,
    layout: (p, w, lh) => {
      const r = unicodeFallbackLayout(p, w, lh);
      return { height: r.height, lineCount: r.lineCount };
    },
    prepareWithSegments: unicodeFallbackPrepare,
    layoutWithLines: (p, w, lh) => {
      const r = unicodeFallbackLayout(p, w, lh);
      return {
        height: r.height,
        lineCount: r.lineCount,
        lines: r.lines.map((l, i) => ({
          text: l.text, width: l.width,
          start: { segmentIndex: 0, graphemeIndex: i },
          end: { segmentIndex: 0, graphemeIndex: i + 1 }
        }))
      };
    },
    measureLineStats: (p, w) => {
      const r = unicodeFallbackLayout(p, w, 20);
      const maxW = r.lines.reduce((m, l) => Math.max(m, l.width), 0);
      return { lineCount: r.lineCount, maxLineWidth: maxW };
    },
    measureNaturalWidth: (p) => estimateTextWidth(p.text, p.fontSize),
    layoutNextLineRange: () => null,
    materializeLineRange: (p, r) => ({ text: p.text.slice(0, 20), width: r.width, start: r.start, end: r.end }),
    setLocale: () => {},
    clearCache: () => {}
  };
}

// ============================================================
//  参数解析
// ============================================================

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
const lineHeight = parseFloat(params.lineHeight) || 20;
const whiteSpace = params.whiteSpace || 'normal';
const wordBreak = params.wordBreak || 'normal';

if (!text) {
  console.error(JSON.stringify({ success: false, error: 'MISSING_TEXT', message: '缺少 --text 参数，请提供要测量的文本内容' }, null, 2));
  process.exit(1);
}

if (params.locale && pretext.setLocale) pretext.setLocale(params.locale);

try {
  const options = {};
  if (whiteSpace !== 'normal') options.whiteSpace = whiteSpace;
  if (wordBreak !== 'normal') options.wordBreak = wordBreak;

  const prepared = pretext.prepare(text, font, options);
  const result = pretext.layout(prepared, width, lineHeight);

  const modeLabels = {
    'canvas': '高精度（node-canvas）',
    'mock': '标准精度（@chenglou/pretext + mock canvas）',
    'unicode-estimate': '估算模式（纯 JS fallback）'
  };

  const output = {
    success: true,
    text: text,
    font: font,
    width: width,
    lineHeight: lineHeight,
    height: Math.round(result.height * 1000) / 1000,
    lineCount: result.lineCount,
    whiteSpace, wordBreak,
    measurementMode: canvasMode,
    measurementModeLabel: modeLabels[canvasMode] || canvasMode,
    unit: 'px',
    tips: {
      heightAdvice: result.lineCount === 0
        ? '文本为空，设置 height=0'
        : result.lineCount === 1
          ? '文本不换行（单行）'
          : `文本换行 ${result.lineCount} 行，总高度约 ${Math.round(result.height)}px`,
      cssHint: `可用作 CSS: height: ${Math.ceil(result.height)}px`,
      containerHint: result.height > 0 ? `容器建议 min-height: ${Math.ceil(result.height)}px` : null
    }
  };

  console.log(JSON.stringify(output, null, 2));

} catch (err) {
  console.error(JSON.stringify({
    success: false,
    error: 'MEASUREMENT_FAILED',
    message: err.message,
    hint: '常见原因：字体名称拼写错误、宽度 <= 0、宽度需要 > 0',
    canvasMode: canvasMode
  }, null, 2));
  process.exit(1);
}
