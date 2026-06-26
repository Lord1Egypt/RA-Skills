#!/usr/bin/env npx tsx
// =============================================================
// Komandr Bridge for OpenClaw
// =============================================================
//
// A CLI bridge that lets OpenClaw agents interact with Komandr
// by invoking individual commands for each task lifecycle action.
//
// Usage:
//   npx tsx scripts/komandr-bridge.ts <command> [args...]
//
// Commands:
//   me                                    — Show agent profile
//   heartbeat                             — Send heartbeat (status: online)
//   poll [capabilities]                   — Poll for next task
//   accept <task-id>                      — Accept a queued task
//   progress <task-id> <percent> [message] — Report progress
//   submit <task-id> <summary> [result-json] — Submit completed work
//   fail <task-id> <message>              — Report task failure
//
// Environment:
//   KOMANDR_API_KEY  — Required. Agent API key (km_...)
//   KOMANDR_URL      — Optional. Defaults to https://komandr.vercel.app
// =============================================================

const API_KEY = process.env.KOMANDR_API_KEY;
const BASE_URL = (process.env.KOMANDR_URL || "https://komandr.vercel.app").replace(/\/$/, "");

if (!API_KEY) {
  console.error(JSON.stringify({
    error: "KOMANDR_API_KEY environment variable is not set",
    hint: "Set it to your agent API key (starts with km_...)",
  }));
  process.exit(1);
}

// --------------- HTTP helpers ---------------

async function request(method: string, path: string, body?: unknown): Promise<unknown> {
  const url = `${BASE_URL}${path}`;

  const headers: Record<string, string> = {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  };

  const init: RequestInit = { method, headers };

  if (body !== undefined && method !== "GET") {
    init.body = JSON.stringify(body);
  }

  let response: Response;
  try {
    response = await fetch(url, init);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(JSON.stringify({ error: "Network error", message, url }));
    process.exit(1);
  }

  let data: unknown;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    console.error(JSON.stringify({
      error: "API error",
      status: response.status,
      body: data,
    }));
    process.exit(1);
  }

  return data;
}

async function get(path: string): Promise<unknown> {
  return request("GET", path);
}

async function post(path: string, body?: unknown): Promise<unknown> {
  return request("POST", path, body);
}

// --------------- Commands ---------------

async function cmdMe(): Promise<void> {
  const profile = await get("/api/v1/agent/me");
  console.log(JSON.stringify(profile, null, 2));
}

async function cmdHeartbeat(): Promise<void> {
  const result = await post("/api/v1/agent/heartbeat", { status: "online" });
  console.log(JSON.stringify(result, null, 2));
}

async function cmdPoll(capabilities?: string): Promise<void> {
  let path = "/api/v1/agent/tasks/next";
  if (capabilities) {
    path += `?capabilities=${encodeURIComponent(capabilities)}`;
  }
  const result = await get(path);
  console.log(JSON.stringify(result, null, 2));
}

async function cmdAccept(taskId: string): Promise<void> {
  const result = await post(`/api/v1/agent/tasks/${taskId}/accept`);
  console.log(JSON.stringify(result, null, 2));
}

async function cmdProgress(taskId: string, percent: number, message?: string): Promise<void> {
  const body: Record<string, unknown> = { progress: percent };
  if (message) {
    body.message = message;
  }
  const result = await post(`/api/v1/agent/tasks/${taskId}/progress`, body);
  console.log(JSON.stringify(result, null, 2));
}

async function cmdSubmit(taskId: string, summary: string, resultJson?: string): Promise<void> {
  let resultData: Record<string, unknown> = {};
  if (resultJson) {
    try {
      resultData = JSON.parse(resultJson);
    } catch {
      console.error(JSON.stringify({ error: "Invalid JSON in result argument", input: resultJson }));
      process.exit(1);
    }
  }

  const body = {
    summary,
    result: resultData,
  };

  const result = await post(`/api/v1/agent/tasks/${taskId}/submit`, body);
  console.log(JSON.stringify(result, null, 2));
}

async function cmdFail(taskId: string, message: string): Promise<void> {
  const body = {
    error_type: "agent_reported_error",
    message,
    recoverable: true,
  };

  const result = await post(`/api/v1/agent/tasks/${taskId}/fail`, body);
  console.log(JSON.stringify(result, null, 2));
}

// --------------- CLI router ---------------

function printUsage(): void {
  console.log(`Komandr Bridge for OpenClaw

Usage: npx tsx scripts/komandr-bridge.ts <command> [args...]

Commands:
  me                                      Show agent profile
  heartbeat                               Send heartbeat (online)
  poll [capabilities]                     Poll for next task
  accept <task-id>                        Accept a queued task
  progress <task-id> <percent> [message]  Report progress (0-100)
  submit <task-id> <summary> [result-json] Submit completed work
  fail <task-id> <message>                Report task failure

Environment:
  KOMANDR_API_KEY   Agent API key (required, starts with km_...)
  KOMANDR_URL       Server URL (default: https://komandr.vercel.app)`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === "--help" || command === "-h") {
    printUsage();
    process.exit(0);
  }

  switch (command) {
    case "me":
      await cmdMe();
      break;

    case "heartbeat":
      await cmdHeartbeat();
      break;

    case "poll":
      await cmdPoll(args[1]);
      break;

    case "accept":
      if (!args[1]) {
        console.error(JSON.stringify({ error: "Missing task-id argument" }));
        process.exit(1);
      }
      await cmdAccept(args[1]);
      break;

    case "progress":
      if (!args[1] || !args[2]) {
        console.error(JSON.stringify({ error: "Usage: progress <task-id> <percent> [message]" }));
        process.exit(1);
      }
      await cmdProgress(args[1], parseInt(args[2], 10), args[3]);
      break;

    case "submit":
      if (!args[1] || !args[2]) {
        console.error(JSON.stringify({ error: "Usage: submit <task-id> <summary> [result-json]" }));
        process.exit(1);
      }
      await cmdSubmit(args[1], args[2], args[3]);
      break;

    case "fail":
      if (!args[1] || !args[2]) {
        console.error(JSON.stringify({ error: "Usage: fail <task-id> <message>" }));
        process.exit(1);
      }
      await cmdFail(args[1], args[2]);
      break;

    default:
      console.error(JSON.stringify({ error: `Unknown command: ${command}` }));
      printUsage();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(JSON.stringify({ error: "Unexpected error", message: String(err) }));
  process.exit(1);
});
