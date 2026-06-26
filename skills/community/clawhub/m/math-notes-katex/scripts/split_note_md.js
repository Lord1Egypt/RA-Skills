#!/usr/bin/env node
/*
Split a KaTeX note markdown into multiple parts (pages) heuristically.

Why: headless screenshotting a very tall page is fragile; instead we split the source
into smaller chunks and render each chunk separately.

Heuristic:
- Keep $$...$$ display-math blocks intact
- Prefer breaking on blank lines
- Limit by approx maxLines per page

Usage:
  node split_note_md.js input.md out_dir --max-lines=55
Outputs:
  out_dir/page-001.md, page-002.md, ...
*/

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = { _: [] };
  for (const a of argv) {
    if (a.startsWith('--max-lines=')) args.maxLines = parseInt(a.split('=')[1], 10);
    else args._.push(a);
  }
  if (!args.maxLines || Number.isNaN(args.maxLines)) args.maxLines = 55;
  return args;
}

function splitIntoBlocks(src) {
  const lines = src.split(/\r?\n/);
  const blocks = [];

  let inDisplay = false;
  let buf = [];

  function flushText(textLines) {
    if (!textLines.length) return;
    // split text further by blank lines into paragraphs
    let para = [];
    const pushPara = () => {
      if (!para.length) return;
      blocks.push({ type: 'text', lines: para });
      para = [];
    };
    for (const ln of textLines) {
      if (ln.trim() === '') {
        pushPara();
        // keep a blank line separator as its own tiny block to preserve spacing
        blocks.push({ type: 'blank', lines: [''] });
      } else {
        para.push(ln);
      }
    }
    pushPara();
  }

  for (const ln of lines) {
    if (!inDisplay && ln.trim() === '$$') {
      flushText(buf);
      buf = [];
      inDisplay = true;
      blocks.push({ type: 'math_delim', lines: ['$$'] });
      continue;
    }
    if (inDisplay && ln.trim() === '$$') {
      // end display
      blocks.push({ type: 'math', lines: buf });
      blocks.push({ type: 'math_delim', lines: ['$$'] });
      buf = [];
      inDisplay = false;
      continue;
    }
    buf.push(ln);
  }

  if (inDisplay) {
    // unclosed $$: treat as text
    flushText(['$$', ...buf]);
  } else {
    flushText(buf);
  }

  // compact consecutive blank blocks
  const compacted = [];
  for (const b of blocks) {
    if (b.type === 'blank' && compacted.length && compacted[compacted.length - 1].type === 'blank') continue;
    compacted.push(b);
  }
  return compacted;
}

function blocksToPages(blocks, maxLines) {
  const pages = [];
  let cur = [];
  let curLines = 0;

  const blockLineCount = (b) => b.lines.length;

  function pushPage() {
    // trim leading/trailing blanks
    while (cur.length && cur[0].type === 'blank') cur.shift();
    while (cur.length && cur[cur.length - 1].type === 'blank') cur.pop();
    if (!cur.length) return;
    pages.push(cur);
    cur = [];
    curLines = 0;
  }

  for (const b of blocks) {
    const n = blockLineCount(b);
    // If block alone is too big, still force it into a page (avoid infinite loop)
    if (curLines > 0 && curLines + n > maxLines) pushPage();
    cur.push(b);
    curLines += n;
    // If we hit a blank line and already near limit, break page there
    if (b.type === 'blank' && curLines >= Math.floor(maxLines * 0.85)) pushPage();
  }
  pushPage();
  return pages;
}

function pageToText(pageBlocks) {
  const out = [];
  for (const b of pageBlocks) out.push(...b.lines);
  // ensure newline at end
  return out.join('\n').replace(/\n+$/,'') + '\n';
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const [inPath, outDir] = args._;
  if (!inPath || !outDir) {
    console.error('Usage: node split_note_md.js input.md out_dir [--max-lines=55]');
    process.exit(2);
  }

  const src = fs.readFileSync(inPath, 'utf8');
  const blocks = splitIntoBlocks(src);
  const pages = blocksToPages(blocks, args.maxLines);

  fs.mkdirSync(outDir, { recursive: true });

  for (let i = 0; i < pages.length; i++) {
    const p = String(i + 1).padStart(3, '0');
    const fp = path.join(outDir, `page-${p}.md`);
    fs.writeFileSync(fp, pageToText(pages[i]), 'utf8');
  }

  console.log(`pages=${pages.length}`);
}

main();
