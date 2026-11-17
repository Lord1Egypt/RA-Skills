#!/usr/bin/env node
'use strict';

/** Render a local 1080x1440 text cover using an already installed node-canvas. */
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { createRequire } = require('node:module');

/** Find canvas through normal resolution or an existing WorkBuddy runtime. */
function loadCanvas(modulePath) {
  const candidates = modulePath ? [path.resolve(modulePath)] : [];
  if (!modulePath) {
    for (const base of [__filename, process.execPath]) {
      try { candidates.push(createRequire(base).resolve('canvas')); } catch { /* Try bundled runtime. */ }
    }
    const versions = path.join(os.homedir(), '.workbuddy', 'binaries', 'node', 'versions');
    if (fs.existsSync(versions)) {
      for (const entry of fs.readdirSync(versions, { withFileTypes: true }).filter(e => e.isDirectory()).sort((a, b) => b.name.localeCompare(a.name, undefined, { numeric: true }))) {
        candidates.push(path.join(versions, entry.name, 'node_modules', '@tencent', 'slidep', 'node_modules', 'canvas'));
      }
    }
  }
  const failures = [];
  for (const candidate of [...new Set(candidates)]) {
    if (!fs.existsSync(candidate)) continue;
    try {
      const canvas = require(candidate);
      canvas.createCanvas(1, 1).toBuffer('image/png');
      return canvas;
    } catch (error) { failures.push(`${candidate}: ${error.message}`); }
  }
  throw new Error(`No usable installed node-canvas. Use a verified host renderer; no dependency was installed.${failures.length ? ` Load failures: ${failures.join('; ')}` : ''}`);
}

/** Validate the bounded, data-only cover specification before rendering. */
function validateSpec(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Cover spec must be an object.');
  const allowed = new Set(['title', 'subtitle', 'label', 'points', 'accent', 'fontFamily']);
  for (const key of Object.keys(value)) if (!allowed.has(key)) throw new Error(`Unsupported cover field: ${key}`);
  for (const [key, limit] of [['title', 80], ['subtitle', 160], ['label', 40], ['fontFamily', 200]]) {
    if (value[key] !== undefined && (typeof value[key] !== 'string' || !value[key].trim() || [...value[key]].length > limit || /[\x00-\x1f]/.test(value[key]))) {
      throw new Error(`${key} must be nonempty text up to ${limit} characters without control characters.`);
    }
  }
  if (!value.title) throw new Error('title is required.');
  if (value.accent !== undefined && !/^#[0-9a-f]{6}$/i.test(value.accent)) throw new Error('accent must be a six-digit hex color.');
  if (value.points !== undefined && (!Array.isArray(value.points) || value.points.length > 4 || value.points.some(p => typeof p !== 'string' || !p.trim() || [...p].length > 80 || /[\x00-\x1f]/.test(p)))) {
    throw new Error('points must contain at most four nonempty strings of at most 80 characters.');
  }
  return { label: 'QUICK GUIDE', subtitle: '', points: [], accent: '#2563EB', fontFamily: '"Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif', ...value };
}

/** Wrap Unicode code points to measured width; never silently truncate text. */
function wrapText(ctx, text, width) {
  const lines = [];
  let line = '';
  for (const character of text) {
    if (line && ctx.measureText(line + character).width > width) { lines.push(line.trim()); line = ''; }
    line += character;
  }
  if (line.trim()) lines.push(line.trim());
  return lines;
}

/** Fit text within a fixed box or report overflow without clipping the output. */
function drawText(ctx, text, box, family, maxSize, minSize, color, weight = 'normal') {
  if (!text) return;
  for (let size = maxSize; size >= minSize; size -= 2) {
    ctx.font = `${weight} ${size}px ${family}`;
    const lines = wrapText(ctx, text, box.width);
    const lineHeight = Math.ceil(size * 1.35);
    if (lines.length * lineHeight > box.height) continue;
    ctx.fillStyle = color;
    ctx.textBaseline = 'top';
    lines.forEach((line, index) => ctx.fillText(line, box.x, box.y + index * lineHeight));
    return;
  }
  throw new Error('Cover text does not fit the template. Shorten the affected copy; nothing was exported.');
}

/** Build the PNG in memory, then create a new output file without overwriting. */
function renderCover(canvasModule, input, output) {
  const spec = validateSpec(input);
  if (path.extname(output).toLowerCase() !== '.png') throw new Error('Output must have a .png extension.');
  if (fs.existsSync(output)) throw new Error('Output already exists. Choose a new revision filename.');
  const canvas = canvasModule.createCanvas(1080, 1440);
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#F6F3EC'; ctx.fillRect(0, 0, 1080, 1440);
  ctx.fillStyle = spec.accent; ctx.fillRect(72, 72, 96, 12);
  const text = (value, x, y, width, height, max, min, color = '#152238', weight) => drawText(ctx, value, { x, y, width, height }, spec.fontFamily, max, min, color, weight);
  text(spec.label, 72, 110, 936, 100, 30, 22, '#445269', 'bold');
  text(spec.title, 72, 240, 936, 405, 96, 56, '#152238', 'bold');
  text(spec.subtitle, 72, 670, 936, 140, 38, 26, '#445269');
  spec.points.forEach((point, index) => {
    const y = 860 + index * 116;
    ctx.fillStyle = spec.accent; ctx.fillRect(72, y + 12, 8, 48);
    text(point, 108, y, 900, 100, 34, 24);
  });
  const bytes = canvas.toBuffer('image/png');
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, bytes, { flag: 'wx' });
  return { status: 'rendered', output: path.resolve(output), width: 1080, height: 1440, bytes: bytes.length, visualInspection: 'required' };
}

function main(argv) {
  const options = {};
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--check') { options.check = true; continue; }
    if (!['--input', '--output', '--canvas-module'].includes(key) || !argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error('Usage: node render-cover.cjs --check | --input spec.json --output cover.png [--canvas-module /installed/canvas]');
    if (options[key] !== undefined) throw new Error(`Repeated option: ${key}`);
    options[key] = argv[++i];
  }
  if (!options.check && (!options['--input'] || !options['--output'])) throw new Error('--input and --output are required.');
  const canvas = loadCanvas(options['--canvas-module']);
  if (options.check) return { status: 'available', renderer: 'node-canvas', width: 1080, height: 1440, fontInspection: 'required for the output language' };
  const input = fs.readFileSync(options['--input']);
  if (input.length > 16384) throw new Error('Cover spec exceeds 16 KiB.');
  return renderCover(canvas, JSON.parse(input.toString('utf8')), path.resolve(options['--output']));
}

if (require.main === module) {
  try { console.log(JSON.stringify(main(process.argv.slice(2)))); }
  catch (error) { console.error(JSON.stringify({ status: 'failed', error: error.message })); process.exitCode = 1; }
}
module.exports = { validateSpec, wrapText, renderCover };
