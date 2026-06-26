#!/usr/bin/env node

function main() {
  const input = process.argv.slice(2).join(" ").trim();

  let parsed = {};
  try {
    parsed = input ? JSON.parse(input) : {};
  } catch {
    parsed = { text: input };
  }

  const mode = parsed.mode || "entity_query";
  const text = parsed.text || "";
  const entities = Array.isArray(parsed.entities) ? parsed.entities : [];

  const items = [];

  if (mode === "continuation_query") {
    items.push({ text: "Previous work continuation context exists" });
  }

  if (mode === "entity_query" && entities.length > 0) {
    items.push({ text: `Entity context exists for ${entities[0]}` });
  }

  if (mode === "constraint_query") {
    items.push({ text: "Execution-like request should check prior constraints" });
  }

  if (items.length === 0 && text) {
    items.push({ text: `Recall placeholder for: ${text}` });
  }

  const out = {
    status: items.length > 0 ? "queried_success" : "queried_no_hits",
    mode,
    items
  };

  process.stdout.write(JSON.stringify(out, null, 2) + "\n");
}

main();
