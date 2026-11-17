#!/usr/bin/env node
/**
 * One-command Polymarket desk setup:
 * - arms dry-run stops
 * - wires place + guard MCP
 * - prints YOU ARE PROTECTED / PLACE THROUGH THIS DESK loop
 */
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { existsSync } from 'node:fs';

const require = createRequire(import.meta.url);
const scriptsDir = dirname(fileURLToPath(import.meta.url));

function resolveBin(pkgName, binRel) {
  try {
    const pkgJson = require.resolve(`${pkgName}/package.json`);
    return join(dirname(pkgJson), binRel);
  } catch {
    return null;
  }
}

const placePkg = resolveBin('@hypelens/polymarket-place', 'package.json');
const guardEntry =
  resolveBin('@hypelens/hypelens-agent-guard', 'bin/agent-guard.js') ||
  join(scriptsDir, '..', '..', 'agent-guard', 'bin', 'agent-guard.js');

if (!placePkg) {
  console.error('Missing @hypelens/polymarket-place. Run: npm install (in this scripts/ folder)');
  process.exit(1);
}
if (!existsSync(guardEntry)) {
  console.error('Missing @hypelens/hypelens-agent-guard. Run: npm install (in this scripts/ folder)');
  process.exit(1);
}

console.log('');
console.log('========================================');
console.log(' pm-desk — daily driver');
console.log(' YOU ARE PROTECTED / PLACE THROUGH THIS DESK');
console.log('========================================');
console.log(' place OK @', dirname(placePkg));
console.log(' running agent-guard setup (arms dry-run stops)…');
console.log('');

process.argv = [process.argv[0], guardEntry, 'setup', '--scripts-dir', scriptsDir, ...process.argv.slice(2)];
await import(pathToFileURL(guardEntry).href);
