#!/usr/bin/env node
/**
 * 通用 MCP 工具调用
 * 用法: node mcp_tool.mjs <tool_name> [args_json] [base_url]
 */
import { print, print_error } from "./stdio_utf8.mjs";

const [toolName, argsRaw = "{}", baseUrl = process.env.BIL_CRAWL_URL || "http://127.0.0.1:39002"] = process.argv.slice(2);

if (!toolName) {
  print_error("Usage: node mcp_tool.mjs <tool_name> [args_json] [base_url]");
  print_error(
    'Example: node mcp_tool.mjs list_archives \'{"platform":"bilibili","limit":10}\''
  );
  process.exit(2);
}

let args;
try {
  args = JSON.parse(argsRaw);
  if (typeof args !== "object" || Array.isArray(args) || args === null) throw new Error();
} catch {
  print_error("args_json must be a valid JSON object");
  process.exit(2);
}

const mcpUrl = `${baseUrl}/mcp`;

try {
  await fetch(`${baseUrl}/`, { signal: AbortSignal.timeout(3000) });
} catch {
  print_error(`Service not reachable at ${baseUrl}`);
  process.exit(1);
}

const headers = { "Content-Type": "application/json", Accept: "application/json, text/event-stream" };

const initPayload = {
  jsonrpc: "2.0", id: 1, method: "initialize",
  params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "media-crawler-local", version: "1.0.0" } },
};

const callPayload = {
  jsonrpc: "2.0", id: 2, method: "tools/call",
  params: { name: toolName, arguments: args },
};

// Initialize session (best-effort)
try {
  await fetch(mcpUrl, { method: "POST", headers, body: JSON.stringify(initPayload), signal: AbortSignal.timeout(5000) });
} catch {}

const res = await fetch(mcpUrl, {
  method: "POST",
  headers,
  body: JSON.stringify(callPayload),
  signal: AbortSignal.timeout(30000),
});

const text = await res.text();
try {
  print(JSON.stringify(JSON.parse(text), null, 2));
} catch {
  print(text);
}
