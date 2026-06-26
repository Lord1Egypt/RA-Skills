#!/usr/bin/env node
// Resolve an HTML file to a file:// URL without launching a browser.
// Zero dependencies, zero child processes, zero network I/O.

import { existsSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const arg = process.argv[2];
if (!arg || arg === '--help' || arg === '-h') {
  console.error('Usage: node scripts/preview.mjs <file.html | url>');
  console.error('Prints a file:// URL that humans or agent browser tools can open.');
  process.exit(arg ? 0 : 1);
}

const isUrl = /^[a-z][a-z0-9+.-]*:\/\//i.test(arg);
let target = arg;

if (!isUrl) {
  const abs = resolve(process.cwd(), arg);
  if (!existsSync(abs)) {
    console.error(`ERROR: file not found: ${abs}`);
    process.exit(1);
  }
  if (!statSync(abs).isFile()) {
    console.error(`ERROR: not a regular file: ${abs}`);
    process.exit(1);
  }
  target = pathToFileURL(abs).href;
}

console.log('');
console.log('  Preview URL:');
console.log(`    ${target}`);
console.log('');
console.log('  Agents: open this URL with your browser tool.');
console.log('  Humans: click or paste the URL into a browser tab.');
console.log('');
