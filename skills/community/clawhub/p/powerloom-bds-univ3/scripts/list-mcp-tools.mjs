#!/usr/bin/env node
/**
 * Print MCP tool names from the live server (tools/list).
 * Proves valid names are bds_mpp_* / get_credit_balance / verify_data_provenance — not the ClawHub slug.
 *
 * Usage: POWERLOOM_API_KEY=sk_live_... node scripts/list-mcp-tools.mjs
 */

import { listMcpTools } from "./lib/mcp.mjs";

try {
  const names = await listMcpTools();
  for (const n of names.sort()) {
    console.log(n);
  }
} catch (e) {
  console.error(e.message || e);
  process.exit(1);
}
