#!/usr/bin/env node

function hasContinuation(text) {
  return /(続き|前回|再開|引き継ぎ|continue|resume|previous work)/i.test(text);
}

function hasExecutionIntent(text) {
  return /(実装|修正|変更|設計|追加|削除|edit|modify|implement|design|change)/i.test(text);
}

function hasKnownEntity(entities) {
  return Array.isArray(entities) && entities.length > 0;
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
  const entities = parsed.entities || [];
  const intent = parsed.intent || "generic_qa";

  let needed = false;
  let mode = null;
  let reason = "generic";

  if (hasContinuation(text)) {
    needed = true;
    mode = "continuation_query";
    reason = "continuation";
  } else if (intent === "implementation_request" || hasExecutionIntent(text)) {
    needed = true;
    mode = "constraint_query";
    reason = "execution_like";
  } else if (hasKnownEntity(entities)) {
    needed = true;
    mode = "entity_query";
    reason = "known_entity";
  }

  const out = {
    needed,
    status: needed ? "needed" : "not_needed",
    mode,
    reason
  };

  process.stdout.write(JSON.stringify(out, null, 2) + "\n");
}

main();
