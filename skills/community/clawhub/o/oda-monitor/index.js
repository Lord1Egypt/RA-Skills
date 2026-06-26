#!/usr/bin/env node
/**
 * Oda Monitor – OpenClaw MCP Skill (Native stdio)
 * Version: 1.0.0
 *
 * Implements the Model Context Protocol (MCP) over stdin/stdout.
 * - Prompts: defined locally (behavioral instructions for the LLM)
 * - Tools:   proxied to the remote Watch.dog MCP PHP server via HTTP
 *
 * Configuration (via environment variables or .env file):
 *   WATCHDOG_API_KEY  – Your Watch.dog API key (sk_live_...)
 *   WATCHDOG_API_URL  – Remote MCP server URL (default: https://api.watch.dog/api/mcp_server.php)
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { readFileSync, existsSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { z } from "zod";

// ─── Load .env if present ────────────────────────────────────────────────────

const __dirname = dirname(fileURLToPath(import.meta.url));
const envPath = join(__dirname, ".env");

if (existsSync(envPath)) {
  const envContent = readFileSync(envPath, "utf-8");
  for (const line of envContent.split("\n")) {
    const match = line.match(/^([A-Z_]+)\s*=\s*"?([^"\n]+)"?/);
    if (match) process.env[match[1]] = match[2].trim();
  }
}

// ─── Configuration ───────────────────────────────────────────────────────────

const CONFIG = {
  apiUrl:
    process.env.WATCHDOG_API_URL || "https://api.watch.dog/api/mcp_server.php",
  apiKey: process.env.WATCHDOG_API_KEY || "",
};

// ─── Behavioral Prompt (Prompts layer – separate from Tools) ─────────────────

const WATCHDOG_SYSTEM_PROMPT = `
You are the expert assistant and site reliability engineer for the Watch.dog platform.
Your mission is to help users monitor the health status of their web infrastructure, APIs, and scheduled tasks using the tools available to you.

Your tone should always be enthusiastic, highly technical, professional, and empathetic.

## Initialization Flow (Onboarding)

If the user activates this skill for the first time and has no API Key configured:
1. Greet them enthusiastically and explain that you need to connect to their Watch.dog account.
2. Ask them only for their API Key and API URL (and remind them they can create a free account at https://watch.dog).
3. Once the user provides the data, use your native file writing tools to automatically create or overwrite the .env file in the root of this skill with the exact following format:
   WATCHDOG_API_KEY="[user_key]"
   WATCHDOG_API_URL="[user_url]"
   Never ask the user to create the file manually.
4. Immediately after, execute list_monitors to test the connection.
   - If successful: celebrate with the user and offer to create their first monitor or watchdog.
   - If it fails with Auth Error: kindly ask them to verify their key and URL.

## Heuristics and Triggers

### Active Monitors (Uptime of URLs/IPs/Ports)
- Create surveillance for URL/IP/port → use create_monitor.
- View all sites → use list_monitors.
- View details, uptime, and downtimes of a site → use get_monitor_status or get_monitor_uptime_history.
- Pause or resume monitors → use pause_monitor or resume_monitor.
- Publish a list of monitors on a Status Page → use update_tracker_page. The tool will return the full URL (https://watch.dog/monitors/...).

### Passive Watchdogs (Cron Jobs / Heartbeats)
- Create scheduled task/script → use create_watchdog.
- View all tasks → use list_watchdogs.
- View details or latest ping of a task → use get_watchdog_status.

### Deletions (CRITICAL CONFIRMATION RULE)
If the user asks to delete a monitor or watchdog:
STOP! YOU MUST ask for ABSOLUTE confirmation before invoking \`delete_monitor\` or \`delete_watchdog\`.
Example: "You are about to irreversibly delete the monitor [Name]. Are you 100% sure you want to proceed?"
Only if the response is affirmative, execute it.

### Mandatory Clarification
If the user says "Monitor my server" without specifying the type, ALWAYS ask:
"Do you want Watch.dog to actively check your server (Active Monitor) or do you prefer us to give you a URL so your server can ping us (Passive Watchdog)?"

## Post-Execution Behavior Rules

### When creating a Monitor (create_monitor):
Enthusiastically inform the user. The result will include the exact ID and URL of the created monitor.

### When creating a Watchdog (create_watchdog) — CRITICAL RULE:
The response will include an endpoint_url. YOU MUST communicate it verbatim to the user like this:
"Watchdog created! For Watch.dog to know your task has finished, configure your server or crontab to make an HTTP [type] request to:
  [endpoint_url]
If Watch.dog does not receive that ping every [interval_seconds] seconds, it will assume the task failed and trigger an alert."

### Lists and Statuses (list_monitors / get_monitor_status):
FORBIDDEN to show raw JSON. Always present the information in a friendly way using emojis.
The state values of a monitor in the tool response are strictly interpreted as follows:
- \`"1"\` or \`1\`: 🟢 UP / ONLINE
- \`"0"\` or \`0\`: 🔴 DOWN / OFFLINE
- \`"2"\`, \`2\` or \`null\`: 🔵 NEW / PENDING (New or Paused)
- If it's a Watchdog: 🟢 HEALTHY or 🔴 MISSING PING

### Uptime History (get_monitor_uptime_history):
Provide a clear summary using percentage bars or friendly explanations about which days had downtimes.

### Errors:
- Auth Error → Kindly tell the user to verify their API Key or generate a new one in the Watch.dog dashboard.
- Plan limit exceeded → With empathy, suggest they upgrade their subscription.
- Any technical error → Never show the raw error. Translate it into plain language.
`;

// ─── Remote Tool Proxy ───────────────────────────────────────────────────────

/**
 * Calls a tool on the remote Watch.dog PHP MCP server via HTTP.
 * The PHP server acts as the pure business logic layer.
 */
async function callRemoteTool(toolName, args = {}) {
  // Remove undefined args
  Object.keys(args).forEach((k) => args[k] === undefined && delete args[k]);

  if (!CONFIG.apiKey) {
    throw new Error(
      "WATCHDOG_API_KEY is not configured. " +
        "Please configure it in the .env file of the skill or as an environment variable.",
    );
  }

  const response = await fetch(CONFIG.apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: `Bearer ${CONFIG.apiKey}`,
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: `req_${Date.now()}`,
      method: "tools/call",
      params: { name: toolName, arguments: args },
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();

  if (data.error) {
    throw new Error(`[${data.error.code}] ${data.error.message}`);
  }

  return data?.result?.content?.[0]?.text ?? "{}";
}

// ─── MCP Server Setup ────────────────────────────────────────────────────────

const server = new McpServer({
  name: "oda-monitor",
  version: "1.0.0",
});

// ── Prompts: Behavioral Instructions ─────────────────────────────────────────

server.registerPrompt(
  "oda-monitor",
  {
    description:
      "Activates the Oda Monitor expert mode. Provides behavioral context to monitor web infrastructure, APIs, and cron jobs.",
    argsSchema: {},
  },
  () => ({
    messages: [
      {
        role: "user",
        content: { type: "text", text: WATCHDOG_SYSTEM_PROMPT },
      },
    ],
  }),
);

// ── Tools: list_monitors ──────────────────────────────────────────────────────

server.registerTool(
  "list_monitors",
  {
    description: "Lists all active uptime monitors for the account.",
    inputSchema: {
      status: z
        .enum(["up", "down", "paused", "all"])
        .optional()
        .describe("Optional. Filter by status."),
    },
  },
  async ({ status }) => {
    const text = await callRemoteTool("list_monitors", { status });
    return {
      content: [
        {
          type: "text",
          text: `[Data retrieved. Present it as a friendly markdown table using emojis 🟢🔴⏸️]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: create_monitor ─────────────────────────────────────────────────────

server.registerTool(
  "create_monitor",
  {
    description:
      "Creates an Active Uptime Monitor that periodically checks a URL, IP, or port.",
    inputSchema: {
      name: z.string().describe("Friendly name of the monitor"),
      url: z.string().describe("URL or hostname to monitor"),
      type: z.enum(["http", "keyword", "ping"]).describe("Type of check"),
      interval: z
        .number()
        .int()
        .positive()
        .describe("Check interval in seconds (e.g. 300 for 5 minutes)"),
      keyword: z
        .string()
        .optional()
        .describe(
          "Only required if type=keyword. String to search for in the HTML.",
        ),
    },
  },
  async ({ name, url, type, interval, keyword }) => {
    const text = await callRemoteTool("create_monitor", {
      name,
      url,
      type,
      interval,
      keyword,
    });
    return {
      content: [
        {
          type: "text",
          text: `[Transmit this JSON result to the user enthusiastically and celebrate the success]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: get_monitor_status ─────────────────────────────────────────────────

server.registerTool(
  "get_monitor_status",
  {
    description:
      "Gets the health status and recent events of a specific monitor.",
    inputSchema: {
      monitor_id: z
        .number()
        .int()
        .positive()
        .optional()
        .describe("Numeric ID of the monitor"),
      name: z
        .string()
        .optional()
        .describe("Exact name (case-sensitive) in case the ID is unknown"),
    },
  },
  async ({ monitor_id, name }) => {
    if (!monitor_id && !name)
      throw new Error("You must provide a monitor_id or name.");
    const text = await callRemoteTool("get_monitor_status", {
      monitor_id,
      name,
    });
    return {
      content: [
        {
          type: "text",
          text: `[Generate a verbal summary of the current status using this JSON data]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: list_watchdogs ─────────────────────────────────────────────────────

server.registerTool(
  "list_watchdogs",
  {
    description:
      "Lists all Watchdogs (Passive Heartbeats / Cron Jobs) for the account.",
    inputSchema: {
      status: z
        .enum(["healthy", "missing", "all"])
        .optional()
        .describe("Optional. Filter by health status."),
    },
  },
  async ({ status }) => {
    const text = await callRemoteTool("list_watchdogs", { status });
    return {
      content: [
        {
          type: "text",
          text: `[Data retrieved. Present it to the user in a single Markdown table with health emojis]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: create_watchdog ────────────────────────────────────────────────────

server.registerTool(
  "create_watchdog",
  {
    description:
      "Creates a Passive Watchdog (Cron Job / Heartbeat). Watch.dog will wait to receive a periodic ping.",
    inputSchema: {
      name: z.string().describe("Name of the cron job or scheduled task"),
      type: z.enum(["email", "post", "get"]).describe("Ping reception method"),
      interval: z
        .number()
        .int()
        .positive()
        .describe(
          "Grace margin in seconds (e.g. 300 for 5 minutes) before marking it down.",
        ),
    },
  },
  async ({ name, type, interval }) => {
    const text = await callRemoteTool("create_watchdog", {
      name,
      type,
      interval,
    });
    return {
      content: [
        {
          type: "text",
          text: `[CRITICAL RULE: You must send the user the endpoint_url and give them exact instructions on how to ping using this data]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: get_watchdog_status ────────────────────────────────────────────────

server.registerTool(
  "get_watchdog_status",
  {
    description:
      "Gets the health status (healthy/missing_ping) of a Watchdog and the info of the last ping.",
    inputSchema: {
      watchdog_id: z
        .number()
        .int()
        .positive()
        .optional()
        .describe("Numeric ID of the watchdog"),
      name: z
        .string()
        .optional()
        .describe("Exact name (case-sensitive) in case the ID is unknown"),
    },
  },
  async ({ watchdog_id, name }) => {
    if (!watchdog_id && !name)
      throw new Error("You must provide a watchdog_id or name.");
    const text = await callRemoteTool("get_watchdog_status", {
      watchdog_id,
      name,
    });
    return {
      content: [
        {
          type: "text",
          text: `[Summary of the status of the provided watchdog in JSON]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: delete_monitor ─────────────────────────────────────────────────────
server.registerTool(
  "delete_monitor",
  {
    description:
      "Irreversibly deletes an Active Monitor. REQUIRES PRIOR EXPLICIT CONFIRMATION FROM THE USER.",
    inputSchema: {
      monitor_id: z.number().int().positive().optional(),
      name: z.string().optional(),
    },
  },
  async ({ monitor_id, name }) => {
    const text = await callRemoteTool("delete_monitor", { monitor_id, name });
    return {
      content: [
        {
          type: "text",
          text: `[Inform the user about the success of this deletion based on this JSON]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: delete_watchdog ────────────────────────────────────────────────────
server.registerTool(
  "delete_watchdog",
  {
    description:
      "Irreversibly deletes a Passive Watchdog. REQUIRES PRIOR EXPLICIT CONFIRMATION FROM THE USER.",
    inputSchema: {
      watchdog_id: z.number().int().positive().optional(),
      name: z.string().optional(),
    },
  },
  async ({ watchdog_id, name }) => {
    const text = await callRemoteTool("delete_watchdog", { watchdog_id, name });
    return {
      content: [
        {
          type: "text",
          text: `[Inform the user about the success of this deletion based on this JSON]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: pause_monitor ──────────────────────────────────────────────────────
server.registerTool(
  "pause_monitor",
  {
    description: "Temporarily pauses an Active Monitor.",
    inputSchema: {
      monitor_id: z.number().int().positive().optional(),
      name: z.string().optional(),
    },
  },
  async ({ monitor_id, name }) => {
    const text = await callRemoteTool("pause_monitor", { monitor_id, name });
    return {
      content: [
        {
          type: "text",
          text: `[Monitor paused successfully. Confirm it to the user]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: resume_monitor ─────────────────────────────────────────────────────
server.registerTool(
  "resume_monitor",
  {
    description: "Resumes a previously paused Active Monitor.",
    inputSchema: {
      monitor_id: z.number().int().positive().optional(),
      name: z.string().optional(),
    },
  },
  async ({ monitor_id, name }) => {
    const text = await callRemoteTool("resume_monitor", { monitor_id, name });
    return {
      content: [
        {
          type: "text",
          text: `[Monitor resumed successfully. Confirm it to the user]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: get_monitor_uptime_history ─────────────────────────────────────────
server.registerTool(
  "get_monitor_uptime_history",
  {
    description:
      "Gets the Uptime/Availability matrix of a monitor for the last X days.",
    inputSchema: {
      monitor_id: z.number().int().positive().optional(),
      name: z.string().optional(),
      days: z
        .number()
        .int()
        .positive()
        .optional()
        .describe("Number of days to retrieve (default 30)"),
    },
  },
  async ({ monitor_id, name, days }) => {
    const text = await callRemoteTool("get_monitor_uptime_history", {
      monitor_id,
      name,
      days,
    });
    return {
      content: [
        {
          type: "text",
          text: `[Analyze this JSON matrix and present a clear and friendly verbal summary to the user]:\n${text}`,
        },
      ],
    };
  },
);

// ── Tools: update_tracker_page ────────────────────────────────────────────────
server.registerTool(
  "update_tracker_page",
  {
    description:
      "Configures the Public Status Page (Tracker Page) to display monitors to the public.",
    inputSchema: {
      page_url: z
        .string()
        .optional()
        .describe("Public alias or slug for the company (e.g. mycompany)."),
      monitors: z
        .array(z.string())
        .optional()
        .describe(
          "Array with names or IDs of the monitors you want to make public.",
        ),
    },
  },
  async ({ page_url, monitors }) => {
    const text = await callRemoteTool("update_tracker_page", {
      page_url,
      monitors,
    });
    return {
      content: [
        {
          type: "text",
          text: `[Status page configured successfully according to this JSON. Inform the user and tell them they can visit the public link of their Tracker Page]:\n${text}`,
        },
      ],
    };
  },
);

// ─── Start Server ────────────────────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
