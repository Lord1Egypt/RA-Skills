#!/usr/bin/env node
/*
Trace From Session
- Reads OpenClaw session transcript JSONL
- Extracts tool calls + tool results
- Outputs normalized trace JSON for the compiler
*/

const fs = require("node:fs");
const path = require("node:path");

function usage() {
  console.log(`Usage:
  node scripts/trace-from-session.js --session <file.jsonl> --out <trace.json> [--name <skill-name>] [--description <text>]
  node scripts/trace-from-session.js --latest [--agent <agentId>] --out <trace.json> [--name <skill-name>] [--description <text>]
  node scripts/trace-from-session.js --latest --since "2026-03-12T00:00:00Z" --out <trace.json>
`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const token = argv[i];
    if (token.startsWith("--")) {
      const key = token.slice(2);
      const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
      args[key] = value;
    } else {
      args._.push(token);
    }
  }
  return args;
}

function getTimestampMs(entry) {
  if (typeof entry.timestamp === "number") return entry.timestamp;
  if (typeof entry.timestamp === "string") {
    const ms = Date.parse(entry.timestamp);
    if (!Number.isNaN(ms)) return ms;
  }
  if (entry.message && typeof entry.message.timestamp === "number") return entry.message.timestamp;
  if (entry.message && typeof entry.message.timestamp === "string") {
    const ms = Date.parse(entry.message.timestamp);
    if (!Number.isNaN(ms)) return ms;
  }
  return null;
}

function readJsonl(filePath) {
  return fs
    .readFileSync(filePath, "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function findLatestSession(agentId) {
  const dir = path.join(process.env.HOME || "~", ".openclaw", "agents", agentId, "sessions");
  const files = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".jsonl") && !f.includes(".reset") && !f.includes(".deleted") && !f.endsWith(".lock"))
    .map((f) => ({ file: f, full: path.join(dir, f), stat: fs.statSync(path.join(dir, f)) }))
    .sort((a, b) => b.stat.mtimeMs - a.stat.mtimeMs);
  if (!files.length) throw new Error(`No session jsonl found in ${dir}`);
  return files[0].full;
}

function normalizeToolOutput(content) {
  if (!content) return null;
  if (Array.isArray(content) && content.length === 1 && content[0].type === "text") {
    const text = content[0].text;
    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  }
  return content;
}

function extractTrace(entries, options) {
  const steps = new Map();
  let order = 0;

  function ensureStep(id) {
    if (!steps.has(id)) {
      steps.set(id, { id, tool: undefined, input: undefined, output: undefined, order: order++ });
    }
    return steps.get(id);
  }

  for (const entry of entries) {
    if (entry.type !== "message") continue;
    const msg = entry.message || {};

    if (msg.role === "assistant" && Array.isArray(msg.content)) {
      for (const part of msg.content) {
        if (part.type === "toolCall") {
          const step = ensureStep(part.id || `step${order + 1}`);
          step.tool = part.name;
          step.input = part.arguments || {};
        }
      }
    }

    if (msg.role === "tool") {
      const callId = msg.toolCallId || entry.toolCallId || entry.toolCallID;
      const step = ensureStep(callId || `step${order + 1}`);
      step.tool = step.tool || msg.toolName || msg.name;
      step.output = normalizeToolOutput(msg.content);
    }
  }

  return {
    expected_skill_name: options.name,
    description_override: options.description,
    steps: Array.from(steps.values())
      .filter((s) => s.tool)
      .sort((a, b) => a.order - b.order)
      .map((s) => ({ id: s.id, tool: s.tool, input: s.input || {}, output: s.output }))
  };
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.out || (!args.session && !args.latest)) {
    usage();
    process.exit(1);
  }

  const agentId = args.agent || "main";
  const sessionPath = args.session || findLatestSession(agentId);
  const entries = readJsonl(sessionPath);

  const sinceMs = args.since ? Date.parse(args.since) : null;
  const untilMs = args.until ? Date.parse(args.until) : null;

  const filtered = entries.filter((entry) => {
    const ts = getTimestampMs(entry);
    if (ts === null) return true;
    if (sinceMs && ts < sinceMs) return false;
    if (untilMs && ts > untilMs) return false;
    return true;
  });

  const trace = extractTrace(filtered, { name: args.name, description: args.description });
  fs.writeFileSync(args.out, JSON.stringify(trace, null, 2), "utf8");
  console.log(`Trace written to: ${args.out}`);
}

try {
  main();
} catch (err) {
  console.error(`Failed: ${err.message}`);
  process.exit(1);
}
