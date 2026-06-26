#!/usr/bin/env node
/*
Render a math-heavy "конспект" to PNG.

Input: a UTF-8 .md-like text file supporting:
- Display math blocks: lines between $$ ... $$ (delimiters on their own lines)
- Inline math: $...$ inside text lines

Output: PNG screenshot rendered via KaTeX + headless Brave.

Usage:
  node render_note_png.js input.md output.png [--brave=/usr/bin/brave-browser]
*/

const fs = require('fs');
const path = require('path');
const katex = require('katex');
const { spawnSync } = require('child_process');

function escHtml(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderMath(tex, displayMode) {
  return katex.renderToString(tex, {
    displayMode,
    throwOnError: false,
    strict: 'ignore',
    output: 'html',
  });
}

function renderTextWithInlineMath(line) {
  // Minimal inline math parser: split by unescaped $...$.
  // Assumptions: no nested $, and display math uses $$ blocks (handled separately).
  let out = '';
  let i = 0;
  while (i < line.length) {
    const dollar = line.indexOf('$', i);
    if (dollar === -1) {
      out += escHtml(line.slice(i));
      break;
    }
    // If escaped \$, treat as literal
    if (dollar > 0 && line[dollar - 1] === '\\') {
      out += escHtml(line.slice(i, dollar - 1)) + '$';
      i = dollar + 1;
      continue;
    }
    // text before math
    out += escHtml(line.slice(i, dollar));
    const end = line.indexOf('$', dollar + 1);
    if (end === -1) {
      // unmatched $ -> treat as literal
      out += '$' + escHtml(line.slice(dollar + 1));
      break;
    }
    const tex = line.slice(dollar + 1, end).trim();
    out += `<span class="mi">${renderMath(tex, false)}</span>`;
    i = end + 1;
  }
  return out;
}

function parseBlocks(src) {
  const lines = src.split(/\r?\n/);
  const blocks = [];

  let inDisplay = false;
  let buf = [];

  const flushText = (textLines) => {
    const joined = textLines.join('\n');
    if (joined.trim() === '') return;
    blocks.push({ type: 'text', text: joined });
  };

  const flushDisplay = (mathLines) => {
    const tex = mathLines.join('\n').trim();
    blocks.push({ type: 'math', tex, display: true });
  };

  let textBuf = [];

  for (const line of lines) {
    if (!inDisplay && line.trim() === '$$') {
      flushText(textBuf);
      textBuf = [];
      inDisplay = true;
      buf = [];
      continue;
    }
    if (inDisplay && line.trim() === '$$') {
      flushDisplay(buf);
      inDisplay = false;
      buf = [];
      continue;
    }
    if (inDisplay) buf.push(line);
    else textBuf.push(line);
  }

  if (inDisplay) {
    // If $$ not closed, treat as text
    textBuf.push('$$');
    textBuf.push(...buf);
  }
  flushText(textBuf);

  return blocks;
}

function buildHtml(title, blocks) {
  // Link to local KaTeX CSS so fonts/ urls resolve
  let katexCssHref = '';
  try {
    const katexCssPath = require.resolve('katex/dist/katex.min.css');
    katexCssHref = 'file://' + katexCssPath;
  } catch (e) {
    katexCssHref = '';
  }

  const body = blocks
    .map((b) => {
      if (b.type === 'math') {
        return `<div class="m">${renderMath(b.tex, true)}</div>`;
      }
      // text: render each line with inline math
      const lines = String(b.text ?? '').split(/\r?\n/);
      const htmlLines = lines.map((ln) => renderTextWithInlineMath(ln));
      return `<div class="p">${htmlLines.join('<br/>')}</div>`;
    })
    .join('\n');

  const safeTitle = title ? escHtml(title) : '';

  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  ${katexCssHref ? `<link rel="stylesheet" href="${katexCssHref}">` : ''}
  <style>
    body { margin: 0; background: #fff; color: #111; font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif; }
    .wrap { width: 980px; padding: 42px 56px; box-sizing: border-box; }
    .title { font-size: 28px; font-weight: 700; margin: 0 0 18px 0; }
    .p { font-size: 20px; line-height: 1.5; margin: 10px 0; }
    .m { margin: 14px 0; font-size: 1.15em; }
    .mi .katex { font-size: 1.05em; }
    .katex { font-size: 1.08em; }
  </style>
</head>
<body>
  <div class="wrap">
    ${safeTitle ? `<div class="title">${safeTitle}</div>` : ''}
    ${body}
  </div>
</body>
</html>`;
}

function usage() {
  console.error('Usage: render_note_png.js input.md output.png [--title="..."] [--brave=/usr/bin/brave-browser]');
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length < 2) usage();

const inPath = args[0];
const outPng = args[1];
let bravePath = 'brave-browser';
let title = '';
for (const a of args.slice(2)) {
  if (a.startsWith('--brave=')) bravePath = a.slice('--brave='.length);
  if (a.startsWith('--title=')) title = a.slice('--title='.length);
}

const src = fs.readFileSync(inPath, 'utf8');

// --- Preflight lint (helps avoid common "KaTeX skill" казусы) ---
(function preflightLint(text) {
  const lines = text.split(/\r?\n/);
  const headerLines = [];
  const suspiciousHits = []; // {line, ch, name, hint}

  // Confusables / "looks like" symbols that often sneak into math/identifiers and break meaning.
  // IMPORTANT: we lint these mainly inside math regions ($...$ or $$...$$) to avoid noise in Russian prose.
  const confusables = [
    // Greek letters that look like Latin
    { ch: 'ν', name: 'Greek nu', hint: 'often mistaken for Latin v/u' },
    { ch: 'μ', name: 'Greek mu', hint: 'often mistaken for Latin u' },
    { ch: 'ο', name: 'Greek omicron', hint: 'looks like Latin o' },
    { ch: 'ρ', name: 'Greek rho', hint: 'looks like Latin p' },
    { ch: 'κ', name: 'Greek kappa', hint: 'looks like Latin k' },
    { ch: 'τ', name: 'Greek tau', hint: 'looks like Latin t' },
    { ch: 'χ', name: 'Greek chi', hint: 'looks like Latin x' },
    // Cyrillic letters that look like Latin (warn only inside math)
    { ch: 'а', name: 'Cyrillic a', hint: 'looks like Latin a' },
    { ch: 'е', name: 'Cyrillic e', hint: 'looks like Latin e' },
    { ch: 'о', name: 'Cyrillic o', hint: 'looks like Latin o' },
    { ch: 'р', name: 'Cyrillic er', hint: 'looks like Latin p' },
    { ch: 'с', name: 'Cyrillic es', hint: 'looks like Latin c' },
    { ch: 'х', name: 'Cyrillic ha', hint: 'looks like Latin x' },
    { ch: 'у', name: 'Cyrillic u', hint: 'looks like Latin y/u depending on font' },
    { ch: 'к', name: 'Cyrillic ka', hint: 'looks like Latin k' },
    { ch: 'м', name: 'Cyrillic em', hint: 'looks like Latin m' },
    { ch: 'т', name: 'Cyrillic te', hint: 'looks like Latin t' },
    // Punctuation/minus variants (warn mainly inside math)
    { ch: '−', name: 'U+2212 minus', hint: 'use ASCII hyphen-minus "-"; in LaTeX use - inside math' },
    { ch: '–', name: 'en dash', hint: 'use "-" unless you intentionally need an en dash' },
    { ch: '×', name: 'multiply sign', hint: 'prefer LaTeX \\cdot or \\times inside math' },
  ];

  function extractInlineMathSegments(s) {
    const segs = [];
    let i = 0;
    while (i < s.length) {
      const dollar = s.indexOf('$', i);
      if (dollar === -1) break;
      if (dollar > 0 && s[dollar - 1] === '\\') {
        i = dollar + 1;
        continue;
      }
      const end = s.indexOf('$', dollar + 1);
      if (end === -1) break;
      segs.push(s.slice(dollar + 1, end));
      i = end + 1;
    }
    return segs;
  }

  // Heuristic checks for common "not-in-LaTeX" subscripts/superscripts usage in plain text.
  // (These won't render as intended unless inside $...$ or $$...$$.)
  const unicodeSupers = /[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ]/;
  const unicodeSubsers = /[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕₖₗₘₙₒₚₛₜₓ]/;

  function stripInlineMath(s) {
    // Remove unescaped $...$ regions to avoid false positives inside math.
    let out = '';
    let i = 0;
    while (i < s.length) {
      const dollar = s.indexOf('$', i);
      if (dollar === -1) {
        out += s.slice(i);
        break;
      }
      if (dollar > 0 && s[dollar - 1] === '\\') {
        out += s.slice(i, dollar + 1);
        i = dollar + 1;
        continue;
      }
      out += s.slice(i, dollar);
      const end = s.indexOf('$', dollar + 1);
      if (end === -1) break;
      i = end + 1;
    }
    return out;
  }

  let inDisplay = false;

  for (let i = 0; i < lines.length; i++) {
    const ln = lines[i];
    const lineNo = i + 1;

    // Track display-math blocks $$ ... $$ (delimiters must be on their own lines)
    if (ln.trim() === '$$') {
      inDisplay = !inDisplay;
      continue;
    }

    if (/^\s*#{1,6}\s+/.test(ln)) headerLines.push(lineNo);

    // Confusables: check inside math regions only to avoid noise in prose.
    if (inDisplay) {
      for (const c of confusables) {
        if (ln.includes(c.ch)) suspiciousHits.push({ line: lineNo, ...c });
      }
    } else {
      const inlineSegs = extractInlineMathSegments(ln);
      for (const seg of inlineSegs) {
        for (const c of confusables) {
          if (seg.includes(c.ch)) suspiciousHits.push({ line: lineNo, ...c });
        }
        if (unicodeSupers.test(seg)) {
          suspiciousHits.push({
            line: lineNo,
            ch: '⁽sup⁾',
            name: 'Unicode superscript inside inline math',
            hint: 'use LaTeX superscripts: x^2, x^{n+1}'
          });
        }
        if (unicodeSubsers.test(seg)) {
          suspiciousHits.push({
            line: lineNo,
            ch: '₍sub₎',
            name: 'Unicode subscript inside inline math',
            hint: 'use LaTeX subscripts: x_1, x_{n+1}'
          });
        }
      }

      // Only lint "plain text" areas (outside $$...$$ and outside inline $...$)
      const plain = stripInlineMath(ln);

      // underscores for indices in plain text (x_1, a_{n+1}, etc.)
      // Heuristic: warn only when underscore looks like a LaTeX-ish identifier, to reduce false positives.
      const plainNoEsc = plain.replace(/\\_/g, '');
      const underscoreLooksLikeIndex = /\b[A-Za-z][A-Za-z0-9]*_\{?[A-Za-z0-9]/.test(plainNoEsc);
      if (underscoreLooksLikeIndex) {
        suspiciousHits.push({
          line: lineNo,
          ch: '_',
          name: 'underscore looks like an index in plain text',
          hint: 'wrap indices in math: use $x_1$, $a_{n+1}$; underscores won\'t format outside $...$'
        });
      }

      if (unicodeSupers.test(plain)) {
        suspiciousHits.push({
          line: lineNo,
          ch: '⁽sup⁾',
          name: 'Unicode superscript',
          hint: 'use LaTeX superscripts inside math: $x^2$, $x^{n+1}$'
        });
      }

      if (unicodeSubsers.test(plain)) {
        suspiciousHits.push({
          line: lineNo,
          ch: '₍sub₎',
          name: 'Unicode subscript',
          hint: 'use LaTeX subscripts inside math: $x_1$, $x_{n+1}$'
        });
      }
    }
  }

  if (headerLines.length) {
    console.error(
      `[katex-note] WARNING: Markdown headings (#/##/...) are not parsed. ` +
        `Found on lines: ${headerLines.join(', ')}. ` +
        `Use --title="..." for the main title; for sections use plain text (e.g., "1) ...").`
    );
  }

  if (suspiciousHits.length) {
    // Group by character
    const byChar = new Map();
    for (const h of suspiciousHits) {
      const key = h.ch;
      if (!byChar.has(key)) byChar.set(key, { ...h, lines: [] });
      byChar.get(key).lines.push(h.line);
    }

    for (const [ch, info] of byChar.entries()) {
      const uniqLines = [...new Set(info.lines)].slice(0, 30);
      console.error(
        `[katex-note] WARNING: Found '${ch}' (${info.name}) on lines: ${uniqLines.join(', ')}. ` +
          `${info.hint ? `Hint: ${info.hint}.` : ''}`
      );
    }
  }
})(src);

const blocks = parseBlocks(src);
const html = buildHtml(title, blocks);

const tmpDir = fs.mkdtempSync(path.join('/tmp/', 'katex-note-'));
const htmlPath = path.join(tmpDir, 'doc.html');
fs.writeFileSync(htmlPath, html, 'utf8');

const res = spawnSync(bravePath, [
  '--headless=new',
  '--disable-gpu',
  '--hide-scrollbars',
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-dev-shm-usage',
  '--allow-file-access-from-files',
  // Avoid disabling web security unless absolutely required.
  // We render a local file:// HTML that links local KaTeX CSS/fonts.
  // If you hit asset-loading issues, revisit this decision.
  '--force-device-scale-factor=2',
  '--window-size=1200,2000',
  `--screenshot=${outPng}`,
  htmlPath,
], { stdio: 'inherit' });

if (res.status !== 0) process.exit(res.status || 1);
