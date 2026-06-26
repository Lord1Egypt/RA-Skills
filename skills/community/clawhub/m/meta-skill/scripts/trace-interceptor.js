#!/usr/bin/env node
/*
Trace Interceptor
- Reads JSONL tool-call events
- Aggregates into a normalized trace
- Outputs trace JSON for the compiler
*/

const fs = require("node:fs");

function usage() {
  console.log(`Usage:
  node scripts/trace-interceptor.js --in <file.jsonl> --out <trace.json> [--name <skill-name>] [--description <text>]
  node scripts/trace-interceptor.js --stdin --out <trace.json> [--name <skill-name>] [--description <text>]
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

function readJsonlFromFile(filePath) {
  return fs
    .readFileSync(filePath, "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function readJsonlFromStdin() {
  return new Promise((resolve, reject) => {
    let buf = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (buf += chunk));
    process.stdin.on("end", () => {
      try {
        const events = buf
          .split(/\r?\n/)
          .map((line) => line.trim())
          .filter(Boolean)
          .map((line) => JSON.parse(line));
        resolve(events);
      } catch (err) {
        reject(err);
      }
    });
    process.stdin.on("error", reject);
  });
}

function normalizeEvents(events) {
  const steps = new Map();
  let counter = 0;

  function getStep(id) {
    if (!steps.has(id)) {
      steps.set(id, { id, tool: undefined, input: undefined, output: undefined, order: counter++ });
    }
    return steps.get(id);
  }

  for (const evt of events) {
    const type = String(evt.type || evt.event || "").toLowerCase();
    const id = evt.id || evt.call_id || evt.span_id || evt.request_id || `step${counter + 1}`;
    const tool = evt.tool || evt.toolName || evt.tool_name || evt.name;
    const input = evt.input || evt.args || evt.request || evt.params;
    const output = evt.output || evt.result || evt.response;

    const step = getStep(String(id));
    if (tool) step.tool = tool;

    const isInput = type.includes("call") || type.includes("request") || type.includes("input");
    const isOutput = type.includes("result") || type.includes("response") || type.includes("output");

    if (input !== undefined && output !== undefined) {
      step.input = input;
      step.output = output;
      continue;
    }

    if (input !== undefined || isInput) {
      step.input = input;
      continue;
    }

    if (output !== undefined || isOutput) {
      step.output = output;
    }
  }

  return Array.from(steps.values())
    .filter((s) => s.tool)
    .sort((a, b) => a.order - b.order)
    .map((s) => ({
      id: s.id,
      tool: s.tool,
      input: s.input || {},
      output: s.output
    }));
}

async function main() {
  const args = parseArgs(process.argv);
  if ((!args.in && !args.stdin) || !args.out) {
    usage();
    process.exit(1);
  }

  const events = args.stdin ? await readJsonlFromStdin() : readJsonlFromFile(args.in);
  const steps = normalizeEvents(events);

  const trace = {
    expected_skill_name: args.name || undefined,
    description_override: args.description || undefined,
    steps
  };

  fs.writeFileSync(args.out, JSON.stringify(trace, null, 2), "utf8");
  console.log(`Trace written to: ${args.out}`);
}

main().catch((err) => {
  console.error(`Failed: ${err.message}`);
  process.exit(1);
});
