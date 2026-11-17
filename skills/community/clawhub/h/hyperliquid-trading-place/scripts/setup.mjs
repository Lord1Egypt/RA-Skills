#!/usr/bin/env node
/** Post-install one-shot: wire MCP + ApproveBuilderFee (OpenBroker). */
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { existsSync } from 'node:fs';

const require = createRequire(import.meta.url);
const scriptsDir = dirname(fileURLToPath(import.meta.url));

async function main() {
  let entry;
  try {
    const pkgJson = require.resolve('@hypelens/hypelens-agent-rail/package.json');
    entry = join(dirname(pkgJson), 'bin', 'hypelens-setup.js');
  } catch {
    entry = null;
  }
  if (!entry || !existsSync(entry)) {
    console.error('Missing @hypelens/hypelens-agent-rail. Run: npm install (in this scripts/ folder)');
    process.exit(1);
  }
  // Pass --scripts-dir so MCP entry points at local start-mcp.mjs
  process.argv.push('--scripts-dir', scriptsDir);
  await import(pathToFileURL(entry).href);
}

main().catch((e) => {
  console.error(String(e && e.message ? e.message : e));
  process.exit(1);
});
