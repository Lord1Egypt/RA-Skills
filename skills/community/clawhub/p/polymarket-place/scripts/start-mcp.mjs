#!/usr/bin/env node
/** Start pinned @hypelens/polymarket-place MCP from local node_modules (no child_process). */
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);

try {
  const pkgJson = require.resolve('@hypelens/polymarket-place/package.json');
  const pkg = require(pkgJson);
  const binRel =
    (pkg.bin && (pkg.bin['polymarket-place-mcp'] || pkg.bin['polymarket-place'])) ||
    'bin/polymarket-place-mcp.js';
  const entry = join(dirname(pkgJson), binRel);
  await import(pathToFileURL(entry).href);
} catch (e) {
  // Fallback: repo checkout before npm link/publish
  try {
    const localEntry = join(dirname(fileURLToPath(import.meta.url)), '..', '..', 'bin', 'polymarket-place-mcp.js');
    await import(pathToFileURL(localEntry).href);
  } catch {
    console.error('Missing dependency. Run: npm install (in this scripts/ folder)');
    console.error('Or from repo root: npm install && npm run mcp');
    console.error(String(e && e.message ? e.message : e));
    process.exit(1);
  }
}
