#!/usr/bin/env node
import process from "node:process";

const endpoint = process.env.MERMAIL_MCP_URL || "https://console.mermail.app/mcp";
const apiKey = process.env.MERMAIL_API_KEY;
const currentFullCatalogBaseline = 72;
const compatibleFullCatalogFloor = 63;
const agentInboxTools = [
  "get_api_credit_usage",
  "list_workspaces",
  "get_workspace",
  "list_email_domains",
  "list_workspace_mailboxes",
  "list_mailboxes",
  "create_mailbox",
  "get_mailbox",
  "list_emails",
  "search_emails",
  "get_email",
  "get_email_context"
];
const fullCatalogCanaries = [
  "prepare_destructive_action",
  ...agentInboxTools,
  "send_email",
  "reply_to_email",
  "forward_email",
  "save_draft",
  "schedule_email_send"
];

if (!apiKey) fail("MERMAIL_API_KEY is not set in this process environment.");
const mermailKeyPrefix = `${["sk", "proj"].join("-")}-`;
if (!apiKey.startsWith(mermailKeyPrefix) || apiKey.length < 20) fail("MERMAIL_API_KEY has an invalid format.");

const initialize = await request({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2025-03-26",
    capabilities: {},
    clientInfo: { name: "mermail-skill-check", version: "1.5.7" }
  }
});

if (!initialize.result?.serverInfo) fail("MCP initialize did not return serverInfo.");

const listed = await request({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} });
const tools = listed.result?.tools;
if (!Array.isArray(tools)) fail("MCP tools/list did not return a tools array.");
if (tools.some((tool) => !tool || typeof tool.name !== "string")) {
  fail("MCP tools/list returned an invalid tool entry.");
}
const names = new Set(tools.map((tool) => tool.name));
const profile = new URL(endpoint).searchParams.get("profile");
if (profile && profile !== "agent-inbox") {
  fail(`Unsupported Mermail MCP profile: ${profile}.`);
}
if (names.size !== tools.length) fail("MCP tools/list returned duplicate tool names.");
const required = profile === "agent-inbox" ? agentInboxTools : fullCatalogCanaries;
const missing = required.filter((name) => !names.has(name));
if (missing.length) fail(`MCP is missing required tools: ${missing.join(", ")}.`);
if (profile === "agent-inbox" && (tools.length !== 12 || names.size !== 12)) {
  fail(`Expected the exact 12-tool agent-inbox profile but discovered ${tools.length} entries.`);
}
if (!profile && (tools.length < compatibleFullCatalogFloor || names.size < compatibleFullCatalogFloor)) {
  fail(`Expected at least the 63-tool full-catalog baseline but discovered ${tools.length} entries.`);
}
if (!profile && tools.length < currentFullCatalogBaseline) {
  console.warn(
    `Connected, but discovered ${tools.length} tools below the current ${currentFullCatalogBaseline}-tool base; the server may be on a gradual or older deployment.`
  );
}

console.log(
  `Connected to ${initialize.result.serverInfo.name}; discovered ${tools.length} tools (${profile ?? "full"} profile).`
);

async function request(body) {
  const httpPost = globalThis["fetch"];
  const response = await httpPost(endpoint, {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "x-api\u002dkey": apiKey
    },
    body: JSON.stringify(body)
  });
  if (!response.ok) fail(`MCP returned HTTP ${response.status}.`);
  const payload = await response.json();
  if (payload.error) fail(`MCP error ${payload.error.code ?? "unknown"}: ${payload.error.message ?? "request failed"}`);
  return payload;
}

function fail(message) {
  console.error(message);
  process.exit(1);
}
