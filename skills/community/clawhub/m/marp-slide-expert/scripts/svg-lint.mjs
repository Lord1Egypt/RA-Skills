#!/usr/bin/env node
// svg-lint — 内联 SVG 图形合规检查
//
// 用法: node scripts/svg-lint.mjs <file.marp.md|file.html> [更多文件...]
//
// 抓「必然错」的问题：空行切断、--- 分页、id 冲突、悬空引用、坐标越界。
// 不抓「看起来错」的问题：重叠、对比度、文字溢出——那些交给渲染后肉眼过。
// 详见 references/infographics-svg/craft/qa.md

import { readFileSync } from 'node:fs';

const EXPECTED_VIEWBOX_W = 1020;
const TOLERANCE = 2; // 允许描边宽度级别的溢出

const INK = { r: '\x1b[31m', y: '\x1b[33m', g: '\x1b[32m', d: '\x1b[2m', x: '\x1b[0m', b: '\x1b[1m' };
const useColor = process.stdout.isTTY && !process.env.NO_COLOR;
const c = (k, s) => (useColor ? INK[k] + s + INK.x : s);

const findings = [];
let skipCodes = new Set();
const add = (level, file, line, code, msg, hint) => {
  if (skipCodes.has(code)) return;   // 文件内显式豁免（见 svg-lint-ignore 注释）
  findings.push({ level, file, line, code, msg, hint });
};

// ---------- 解析 ----------

function lineOf(text, index) {
  let n = 1;
  for (let i = 0; i < index && i < text.length; i++) if (text[i] === '\n') n++;
  return n;
}

function parseViewBox(block) {
  const m = block.match(/viewBox\s*=\s*"([^"]+)"/);
  if (!m) return null;
  const p = m[1].trim().split(/[\s,]+/).map(Number);
  if (p.length !== 4 || p.some(Number.isNaN)) return null;
  return { x: p[0], y: p[1], w: p[2], h: p[3] };
}

const attr = (tag, name) => {
  const m = tag.match(new RegExp(`\\b${name}\\s*=\\s*"([^"]*)"`));
  return m ? m[1] : null;
};
const num = (tag, name) => {
  const v = attr(tag, name);
  if (v === null) return null;
  const n = parseFloat(v);
  return Number.isNaN(n) ? null : n;
};

// 抽出一个元素的几何包围盒；抽不出就返回 null（跳过，不误报）
function bboxOf(tag, name) {
  const t = name.toLowerCase();
  if (t === 'rect' || t === 'image' || t === 'foreignobject') {
    const x = num(tag, 'x') ?? 0, y = num(tag, 'y') ?? 0;
    const w = num(tag, 'width'), h = num(tag, 'height');
    if (w === null || h === null) return null;
    return { x1: x, y1: y, x2: x + w, y2: y + h };
  }
  if (t === 'circle') {
    const cx = num(tag, 'cx'), cy = num(tag, 'cy'), r = num(tag, 'r');
    if (cx === null || cy === null || r === null) return null;
    return { x1: cx - r, y1: cy - r, x2: cx + r, y2: cy + r };
  }
  if (t === 'ellipse') {
    const cx = num(tag, 'cx'), cy = num(tag, 'cy');
    const rx = num(tag, 'rx'), ry = num(tag, 'ry');
    if (cx === null || cy === null || rx === null || ry === null) return null;
    return { x1: cx - rx, y1: cy - ry, x2: cx + rx, y2: cy + ry };
  }
  if (t === 'line') {
    const x1 = num(tag, 'x1'), y1 = num(tag, 'y1'), x2 = num(tag, 'x2'), y2 = num(tag, 'y2');
    if (x1 === null || y1 === null || x2 === null || y2 === null) return null;
    return { x1: Math.min(x1, x2), y1: Math.min(y1, y2), x2: Math.max(x1, x2), y2: Math.max(y1, y2) };
  }
  if (t === 'text' || t === 'tspan') {
    const x = num(tag, 'x'), y = num(tag, 'y');
    if (x === null || y === null) return null;
    // 文本以基线定位，向上延伸约一个字高。只校验锚点，避免误报。
    return { x1: x, y1: y, x2: x, y2: y };
  }
  if (t === 'path' || t === 'polyline' || t === 'polygon') {
    // 抽取所有数字对作为路径上的点，取包围盒。
    // 只处理「每个数字都是 x,y 对」的命令集：M L C Q Z（+ polyline/polygon 的 points）。
    // H/V/S/T/A 是单轴命令，相对命令（小写）是增量，两者都会打乱配对关系，
    // 硬算会产生假报警 —— 遇到就跳过，交给渲染后的肉眼检查。
    const d = attr(tag, 'd') || attr(tag, 'points');
    if (!d) return null;
    if (/[HhVvSsTtAa]/.test(d)) return null;
    if (/[a-z]/.test(d.replace(/e[+-]?\d+/gi, ''))) return null;
    const nums = (d.match(/-?\d+(\.\d+)?/g) || []).map(Number);
    if (nums.length < 2 || nums.length % 2 !== 0) return null;
    const xs = nums.filter((_, i) => i % 2 === 0);
    const ys = nums.filter((_, i) => i % 2 === 1);
    return { x1: Math.min(...xs), y1: Math.min(...ys), x2: Math.max(...xs), y2: Math.max(...ys) };
  }
  return null;
}

// ---------- 各项检查 ----------

function checkBlock(text, file, start, end) {
  const block = text.slice(start, end);
  const firstLine = lineOf(text, start);

  // 1. 空行
  const blankRel = /\n[ \t]*\n/.exec(block);
  if (blankRel) {
    add('error', file, lineOf(text, start + blankRel.index),
      'blank-line', 'SVG 块内有空行',
      'markdown 在空行处切断 HTML 块，图形会静默消失。删掉这个空行。');
  }

  // 2. --- 分页符
  if (/^\s*---\s*$/m.test(block)) {
    add('error', file, firstLine, 'page-break', 'SVG 块内有 ---',
      '仍被解析为 marp 分页符，这一页会裂成两页。');
  }

  // 3. 硬编码 font-size
  const fsRe = /<[^>]*\bfont-size\s*=\s*"[^"]*"[^>]*>/g;
  let fm;
  while ((fm = fsRe.exec(block))) {
    add('warning', file, lineOf(text, start + fm.index), 'inline-font-size',
      `元素上写死了 ${attr(fm[0], 'font-size')}`,
      '字号应走 CSS class（.t/.tb/.sm/.qt/.lbl），否则改字号时这张图不同步。');
  }

  // 4. viewBox 宽度
  const vb = parseViewBox(block);
  if (vb) {
    if (vb.w !== EXPECTED_VIEWBOX_W) {
      add('warning', file, firstLine, 'viewbox-width',
        `viewBox 宽度是 ${vb.w}，标准是 ${EXPECTED_VIEWBOX_W}`,
        '宽度不统一会导致缩放比例不一致，同一份 deck 里图形大小参差。');
    }
    // 5. 坐标越界
    const tagRe = /<(rect|circle|ellipse|line|text|path|polyline|polygon|image)\b[^>]*>/g;
    let tm;
    while ((tm = tagRe.exec(block))) {
      const b = bboxOf(tm[0], tm[1]);
      if (!b) continue;
      const over = [];
      if (b.x1 < vb.x - TOLERANCE) over.push(`左 ${(vb.x - b.x1).toFixed(0)}px`);
      if (b.y1 < vb.y - TOLERANCE) over.push(`上 ${(vb.y - b.y1).toFixed(0)}px`);
      if (b.x2 > vb.x + vb.w + TOLERANCE) over.push(`右 ${(b.x2 - vb.x - vb.w).toFixed(0)}px`);
      if (b.y2 > vb.y + vb.h + TOLERANCE) over.push(`下 ${(b.y2 - vb.y - vb.h).toFixed(0)}px`);
      if (over.length) {
        add('error', file, lineOf(text, start + tm.index), 'out-of-viewbox',
          `元素超出 viewBox（${over.join('，')}）`,
          `<${tm[1]}> 画到了画布外，渲染时被裁掉。检查坐标或调大 viewBox 高度。`);
      }
    }
  } else {
    add('warning', file, firstLine, 'no-viewbox', 'SVG 没有 viewBox',
      '没有 viewBox 就无法自适应宽度，也没法做越界检查。');
  }
}

function checkIds(text, file) {
  // 整个文件共用一个 DOM，所以 id 唯一性要在全文范围查
  const idRe = /\sid\s*=\s*"([^"]+)"/g;
  const seen = new Map();
  let m;
  while ((m = idRe.exec(text))) {
    const line = lineOf(text, m.index);
    if (seen.has(m[1])) {
      add('error', file, line, 'duplicate-id', `id="${m[1]}" 重复（第 ${seen.get(m[1])} 行已定义）`,
        '导出成单个 HTML 时所有 SVG 共享一个 DOM，重复 id 会让箭头/裁剪区全部串到第一个定义上。加图表前缀：a1/a2/a3…');
    } else {
      seen.set(m[1], line);
    }
  }
  // 悬空引用
  const refRe = /url\(\s*#([^)\s]+)\s*\)/g;
  while ((m = refRe.exec(text))) {
    if (!seen.has(m[1])) {
      add('error', file, lineOf(text, m.index), 'dangling-ref', `引用了未定义的 #${m[1]}`,
        `检查 id 拼写，或补上 <marker id="${m[1]}"> 定义。`);
    }
  }
}

// 豁免写法（代码写在指令行的逗号列表里，其余行写理由）：
//   <!-- svg-lint-ignore: duplicate-id
//        理由写在这里 -->
// 显式豁免某些检查。
// 用途：references/ 里的模板故意复用 a1 这类占位 id（实际使用时按图序重编号），
// 紧凑预览图故意用非 1020 宽度。豁免必须写在文件里，不做静默跳过。
function parseIgnores(text) {
  const out = new Set();
  // 指令可以出现在注释的任何位置，不要求紧跟 <!--
  for (const d of text.match(/<!--[\s\S]*?svg-lint-ignore:[\s\S]*?-->/g) || []) {
    // 只取指令行的逗号列表；其余行是给人看的理由
    const body = d.replace(/<!--[\s\S]*?svg-lint-ignore:/, '').trim().split('\n')[0];
    for (const code of body.split(',')) {
      const t = code.replace(/[*_`]/g, '').trim();
      if (t) out.add(t);
    }
  }
  return out;
}

// ---------- 主流程 ----------

const files = process.argv.slice(2);
if (!files.length) {
  console.error('用法: node scripts/svg-lint.mjs <file.marp.md|file.html> [更多文件...]');
  console.error('豁免：在文件里写 <!-- svg-lint-ignore: duplicate-id, viewbox-width -->');
  process.exit(2);
}

// 豁免写法（代码写在指令行的逗号列表里，其余行写理由）：
//   <!-- svg-lint-ignore: duplicate-id
//        理由写在这里 -->
// 显式豁免某些检查。
// 用途：references/ 里的模板故意复用 a1 这类占位 id（实际使用时按图序重编号），
// 紧凑预览图故意用非 1020 宽度。豁免必须显式写出来，不做静默跳过。
let total = 0;
for (const file of files) {
  let text;
  try {
    text = readFileSync(file, 'utf8');
  } catch (e) {
    console.error(`${c('r', '读不了')} ${file}: ${e.message}`);
    process.exit(2);
  }
  const before = findings.length;
  const prevSkip = skipCodes;
  skipCodes = parseIgnores(text);

  const re = /<svg\b[\s\S]*?<\/svg>/g;
  let m;
  while ((m = re.exec(text))) checkBlock(text, file, m.index, m.index + m[0].length);
  checkIds(text, file);

  skipCodes = prevSkip;
  const n = findings.length - before;
  total += n;
  // 数实际的 svg 块，而不是 <svg 字符串出现次数——正文里提到 `<svg>` 不算图
  const svgCount = (text.match(/<svg\b[\s\S]*?<\/svg>/g) || []).length;
  if (n === 0) {
    console.log(`${c('g', '✓')} ${file} — ${svgCount} 个 SVG，全部通过`);
  } else {
    console.log(`${c('b', file)} — ${svgCount} 个 SVG，${n} 个问题\n`);
  }
}

const errors = findings.filter((f) => f.level === 'error');
const warns = findings.filter((f) => f.level === 'warning');
for (const f of findings) {
  const tag = f.level === 'error' ? c('r', 'ERROR  ') : c('y', 'WARNING');
  console.log(`  ${tag} ${c('d', `${f.file}:${f.line}`)}  ${f.msg}`);
  if (f.hint) console.log(`          ${c('d', '→ ' + f.hint)}`);
}

console.log();
if (total === 0) {
  console.log(c('g', '全部通过。') + c('d', '  别忘了渲染 PNG 肉眼过一遍——lint 抓不到重叠和错位。'));
} else {
  console.log(`${errors.length} error, ${warns.length} warning`);
  if (errors.length === 0) console.log(c('y', '没有阻断项，但每条 warning 都该看一眼。'));
}
process.exit(errors.length ? 1 : 0);
