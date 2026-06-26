#!/usr/bin/env node
// verify-lite — zero-dep static scan for `*.prompt.md` build bundles.
// Usage:
//   node scripts/verify-lite.mjs <bundle.prompt.md> [more.prompt.md ...]
//   node scripts/verify-lite.mjs --template assets/templates/pc-tauri.prompt.md
// Exit codes: 0 clean, 1 findings, 2 file error.

import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { scanBundle } from './lib/bundle-scanner.mjs';

const args = process.argv.slice(2);
const templateMode = args.includes('--template');
const files = args.filter(a => !a.startsWith('--'));

if (!files.length) {
  console.error('Usage: node scripts/verify-lite.mjs [--template] <bundle.prompt.md> [more.prompt.md ...]');
  process.exit(2);
}

const RED = '\x1b[31m', GREEN = '\x1b[32m', YELLOW = '\x1b[33m', DIM = '\x1b[2m', RESET = '\x1b[0m';
let totalErrors = 0;
let totalWarns = 0;
let fileErrors = 0;

for (const rel of files) {
  const abs = resolve(process.cwd(), rel);
  if (!existsSync(abs)) {
    console.error(`${RED}✗${RESET} file not found: ${abs}`);
    fileErrors++;
    continue;
  }
  const raw = await readFile(abs, 'utf8');
  const { findings, stats } = scanBundle(raw, { templateMode });

  const errors = findings.filter(f => f.level === 'error');
  const warns  = findings.filter(f => f.level === 'warn');
  totalErrors += errors.length;
  totalWarns  += warns.length;

  console.log(`\n${DIM}→${RESET} ${basename(abs)}  ${DIM}[${stats.mode || '?'} · ${stats.templateId || '?'}]${RESET}`);
  if (!findings.length) {
    console.log(`  ${GREEN}✓${RESET} clean${templateMode ? ' (template mode)' : ''}`);
    continue;
  }
  for (const f of errors) console.log(`  ${RED}✗${RESET} [${f.code}] ${f.message}`);
  for (const f of warns)  console.log(`  ${YELLOW}!${RESET} [${f.code}] ${f.message}`);
}

console.log('');
if (fileErrors > 0) {
  console.log(`${RED}✗ ${fileErrors} file(s) could not be read${RESET}`);
  process.exit(2);
}
if (totalErrors > 0) {
  console.log(`${RED}✗ verify-lite: ${totalErrors} error(s)${totalWarns ? `, ${totalWarns} warning(s)` : ''} — fix before shipping${RESET}`);
  process.exit(1);
}
console.log(`${GREEN}✓ verify-lite: all clean${totalWarns ? ` (${totalWarns} warning(s))` : ''}${RESET}`);
process.exit(0);
