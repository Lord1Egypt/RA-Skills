#!/usr/bin/env node

const { execFileSync } = require("node:child_process");
const path = require("node:path");

const DIR = __dirname;

function run(script, payload) {
  const p = path.join(DIR, script);
  const out = execFileSync("node", [p, JSON.stringify(payload)], { encoding: "utf-8" });
  return JSON.parse(out);
}

function main() {
  const input = process.argv.slice(2).join(" ").trim();

  let parsed = {};
  try {
    parsed = input ? JSON.parse(input) : {};
  } catch {
    parsed = { text: input };
  }

  const text = parsed.text || "";
  const intent = parsed.intent || "generic_qa";
  const entities = Array.isArray(parsed.entities) ? parsed.entities : [];
  const preExecution = !!parsed.pre_execution;

  const recallDecision = run("should-recall.js", { text, intent, entities });

  let recallResult = { status: "not_needed", mode: null, items: [] };
  let compressed = { totalCount: 0, compressedCount: 0, items: [] };

  if (recallDecision.needed) {
    recallResult = run("targeted-recall.js", {
      mode: recallDecision.mode,
      text,
      entities
    });

    compressed = run("memory-compress.js", {
      items: recallResult.items || []
    });
  }

  const logLine = execFileSync(
    "node",
    [
      path.join(DIR, "structured-log.js"),
      JSON.stringify({
        intent,
        recall_trigger: recallDecision.reason,
        recall_mode: recallDecision.mode,
        recall_status: recallResult.status,
        recall_item_count: (recallResult.items || []).length,
        injected_item_count: (compressed.items || []).length,
        pre_execution_gate: preExecution,
        message: text
      })
    ],
    { encoding: "utf-8" }
  ).trim();

  const out = {
    input: { text, intent, entities, pre_execution: preExecution },
    recallDecision,
    recallResult,
    compressed,
    log: logLine
  };

  process.stdout.write(JSON.stringify(out, null, 2) + "\n");
}

main();
