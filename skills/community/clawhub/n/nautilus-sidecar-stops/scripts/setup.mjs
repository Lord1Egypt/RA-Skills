#!/usr/bin/env node
/** Sticky setup: wire MCP + watcher hints via package setup. */
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { existsSync } from 'node:fs';

const require = createRequire(import.meta.url);
const scriptsDir = dirname(fileURLToPath(import.meta.url));

let entry;
try {
  const pkgJson = require.resolve('@hypelens/hypelens-agent-guard/package.json');
  entry = join(dirname(pkgJson), 'bin', 'agent-guard.js');
} catch {
  entry = join(scriptsDir, '..', '..', 'bin', 'agent-guard.js');
}
if (!existsSync(entry)) {
  console.error('Missing @hypelens/hypelens-agent-guard. Run: npm install');
  process.exit(1);
}
process.argv = [process.argv[0], entry, 'setup', '--scripts-dir', scriptsDir, ...process.argv.slice(2)];
await import(pathToFileURL(entry).href);
