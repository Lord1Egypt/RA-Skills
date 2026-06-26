#!/usr/bin/env node
// quality-score — 0..100 score per bundle, with per-axis breakdown.
// Usage:
//   node scripts/quality-score.mjs <bundle.prompt.md>
//   node scripts/quality-score.mjs --json <bundle.prompt.md>
//   node scripts/quality-score.mjs --strict <bundle.prompt.md>   # exit 1 if < 80

import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { scoreBundle } from './lib/bundle-scanner.mjs';

const args = process.argv.slice(2);
const jsonOut = args.includes('--json');
const strict  = args.includes('--strict');
const files = args.filter(a => !a.startsWith('--'));

if (!files.length) {
  console.error('Usage: node scripts/quality-score.mjs [--json] [--strict] <bundle.prompt.md>');
  process.exit(2);
}

const RED = '\x1b[31m', GREEN = '\x1b[32m', YELLOW = '\x1b[33m', DIM = '\x1b[2m', RESET = '\x1b[0m';

const results = [];
let fileErrors = 0;
for (const rel of files) {
  const abs = resolve(process.cwd(), rel);
  if (!existsSync(abs)) {
    if (jsonOut) results.push({ file: rel, error: 'not found' });
    else console.error(`${RED}✗${RESET} not found: ${abs}`);
    fileErrors++;
    continue;
  }
  const raw = await readFile(abs, 'utf8');
  const score = scoreBundle(raw);
  results.push({ file: rel, ...score });
}

if (jsonOut) {
  process.stdout.write(JSON.stringify(results, null, 2) + '\n');
  if (fileErrors > 0) process.exit(2);
  if (strict && results.some(r => (r.total ?? 0) < 80)) process.exit(1);
  process.exit(0);
}

let belowThreshold = 0;
for (const r of results) {
  if (r.error) continue;
  const colour = r.total >= 90 ? GREEN : r.total >= 80 ? YELLOW : RED;
  console.log(`\n${colour}${r.total}/100${RESET}  ${r.stats.templateId || '?'}  ${DIM}${basename(r.file)}${RESET}`);
  for (const a of r.axes) {
    const mark = a.ok ? `${GREEN}✓${RESET}` : `${RED}✗${RESET}`;
    const hint = a.ok ? '' : `  ${DIM}← ${a.hint}${RESET}`;
    console.log(`  ${mark} ${a.name.padEnd(22)} ${a.points}/10${hint}`);
  }
  if (r.bonus) console.log(`  ${DIM}+ bonus (scaffold/contract): +${r.bonus}${RESET}`);
  if (r.total < 80) belowThreshold++;
}

if (fileErrors > 0) {
  console.log(`\n${RED}✗ ${fileErrors} file(s) could not be read${RESET}`);
  process.exit(2);
}

if (strict && belowThreshold > 0) {
  console.log(`\n${RED}✗ ${belowThreshold} bundle(s) below 80${RESET}`);
  process.exit(1);
}
process.exit(0);
