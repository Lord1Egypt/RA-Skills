// The compiled bundle that ships in the package must carry the same gate as the
// source it was built from — a fix in extension/index.ts alone proves nothing
// about extension/dist/index.js.
//
//   node --test --test-force-exit tests/*.test.mjs

import { test } from "node:test";
import assert from "node:assert/strict";

import * as source from "../extension/index.ts";
import * as bundle from "../extension/dist/index.js";

const GATE_EXPORTS = [
  "classifyTool",
  "destructiveOperationsEnabled",
  "evaluateDestructiveGate",
  "projectChangingTools",
];

test("the compiled bundle exports the gate", () => {
  for (const name of GATE_EXPORTS) {
    assert.equal(typeof bundle[name], "function", name);
  }
  assert.equal(bundle.default.id, "unity");
});

test("the compiled bundle refuses a project-changing call by default", () => {
  const decision = bundle.evaluateDestructiveGate({
    tool: "asset.delete",
    confirm: true,
    env: {},
  });
  assert.equal(decision.allowed, false);
  assert.equal(decision.reason, "operator-opt-in-missing");
});

test("the compiled bundle classifies exactly like the source", () => {
  const samples = [
    "asset.delete",
    "debug.hierarchy",
    "debug.screenshot",
    "transform.setPosition",
    "batch.execute",
    "mygame.getScore",
    "",
  ];
  for (const tool of samples) {
    assert.equal(bundle.classifyTool(tool), source.classifyTool(tool), tool);
  }
});
