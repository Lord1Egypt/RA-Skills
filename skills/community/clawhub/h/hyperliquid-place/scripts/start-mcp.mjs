#!/usr/bin/env node
/** Start pinned hypelens agent-rail MCP from local node_modules (no child_process).
 *  REFUSES until post-install setup.mjs wrote .setup-ok (conversion gate).
 *  If .setup-ok exists but placeAllowed=false, WARN and print ApproveBuilderFee recovery
 *  (MCP still starts so agent-only can call hl_approve_payloads — place stays refuse-closed). */
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { existsSync, readFileSync } from 'node:fs';

const scriptsDir = dirname(fileURLToPath(import.meta.url));
const marker = join(scriptsDir, '.setup-ok');
if (!existsSync(marker) && process.env.HYPELENS_ALLOW_BARE_START !== '1') {
  console.error('REFUSED: post-install setup required before place tools work.');
  console.error('Run: npm install && node setup.mjs');
  console.error('(wires MCP + ApproveBuilderFee; writes .setup-ok). Bare start-mcp skips conversion — downloads alone pay $0.');
  console.error('Then: fund → hl_place_order(..., confirmTrade:true) → poll until fillStatus=FILLED (RESTING≠paid).');
  process.exit(2);
}

if (existsSync(marker)) {
  try {
    const ok = JSON.parse(readFileSync(marker, 'utf8'));
    if (ok && ok.placeAllowed === false) {
      console.error('WARNING: setup ran but placeAllowed=false (maxBuilderFee not approved).');
      console.error('Place is REFUSED until ApproveBuilderFee — no silent $0.');
      console.error('Recovery: export HYPERLIQUID_PRIVATE_KEY=<master> && node setup.mjs');
      console.error('Or call hl_approve_payloads then MASTER-sign ApproveBuilderFee, then hl_balances → place.');
      console.error('Funnel: setup → maxBuilderFee>=10 → equity>0 → hl_place_order(..., confirmTrade:true) → FILLED.');
    }
  } catch (_) { /* ignore corrupt marker */ }
}

const require = createRequire(import.meta.url);
try {
  const pkgJson = require.resolve('@hypelens/hypelens-agent-rail/package.json');
  const pkg = require(pkgJson);
  const binRel = (pkg.bin && (pkg.bin['hypelens-rail-mcp'] || pkg.bin['hypelens-agent-rail'])) || 'bin/hypelens-rail-mcp.js';
  const entry = join(dirname(pkgJson), binRel);
  await import(pathToFileURL(entry).href);
} catch (e) {
  console.error('Missing dependency. Run: npm install && node setup.mjs (in this scripts/ folder)');
  console.error(String(e && e.message ? e.message : e));
  process.exit(1);
}
