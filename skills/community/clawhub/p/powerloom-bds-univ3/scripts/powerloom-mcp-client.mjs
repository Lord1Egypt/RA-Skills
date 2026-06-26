#!/usr/bin/env node
/**
 * Generic MCP tool invocation (for ad-hoc prompts and debugging).
 * Usage: POWERLOOM_API_KEY=... node scripts/powerloom-mcp-client.mjs <tool_name> '[json_params]'
 */

import { callTool } from "./lib/mcp.mjs";

const toolName = process.argv[2];
const params = process.argv[3] ? JSON.parse(process.argv[3]) : {};

if (!toolName) {
  console.error(
    'Usage: node scripts/powerloom-mcp-client.mjs <tool_name> \'{"k":"v"}\''
  );
  process.exit(1);
}

try {
  const out = await callTool(toolName, params);
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  console.error(e.message || e);
  process.exit(1);
}
