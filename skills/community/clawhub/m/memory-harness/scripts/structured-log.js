#!/usr/bin/env node

function main() {
  const input = process.argv.slice(2).join(" ").trim();

  let parsed = {};
  try {
    parsed = input ? JSON.parse(input) : {};
  } catch {
    parsed = { message: input };
  }

  const payload = {
    ts: new Date().toISOString(),
    intent: parsed.intent || null,
    recall_trigger: parsed.recall_trigger || null,
    recall_mode: parsed.recall_mode || null,
    recall_status: parsed.recall_status || null,
    recall_item_count: parsed.recall_item_count ?? null,
    injected_item_count: parsed.injected_item_count ?? null,
    pre_execution_gate: parsed.pre_execution_gate ?? false,
    message: parsed.message || null
  };

  process.stdout.write("[memory-harness] " + JSON.stringify(payload) + "\n");
}

main();
