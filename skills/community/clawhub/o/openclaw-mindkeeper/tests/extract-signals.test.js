import test from "node:test";
import assert from "node:assert/strict";
import { extractSignals } from "../src/pipeline/extract-signals.js";
import { normalizeLine } from "../src/utils/text.js";

test("extractSignals groups decisions, open loops, and recommendations", () => {
  const signals = extractSignals([
    "We decided the final product name is Mindkeeper.",
    "Remaining open loop: implement the real day-context collector for lossless-claw.",
    "Recommendation: validate the brief manually for a few days before sending it daily.",
    "The GitHub repo should follow the convention openclaw-mindkeeper.",
  ]);

  assert.equal(signals.decisions.length, 1);
  assert.equal(signals.openLoops.length, 1);
  assert.equal(signals.recommendations.length, 1);
  assert.ok(signals.highlights.some((line) => line.includes("openclaw-mindkeeper")));
});

test("normalizeLine strips reply tags and timestamp wrappers", () => {
  const normalized = normalizeLine("[[reply_to_current]] [Thu 2026-04-09 23:04 UTC] We decided the final product name is Mindkeeper.");
  assert.equal(normalized, "We decided the final product name is Mindkeeper.");
});

test("extractSignals drops noisy metadata lines", () => {
  const signals = extractSignals([
    "Sender (untrusted metadata):",
    '"label": "openclaw-control-ui"',
    "{",
    "}",
    "We decided the final product name is Mindkeeper.",
  ]);

  assert.equal(signals.decisions.length, 1);
  assert.equal(signals.highlights.length, 0);
});

test("extractSignals prefers product lines over housekeeping noise", () => {
  const signals = extractSignals([
    "Let me update tasks/todo.md:",
    "See: tasks/todo.md for full session log.",
    "The GitHub repo should follow the convention openclaw-mindkeeper.",
    "Use lossless-claw as the memory engine and keep the owner-facing product separate.",
    "What feature vrei să construim?",
  ]);

  assert.ok(signals.highlights.some((line) => line.includes("openclaw-mindkeeper")));
  assert.ok(signals.highlights.some((line) => line.includes("lossless-claw")));
  assert.ok(!signals.highlights.some((line) => line.includes("tasks/todo.md")));
  assert.ok(!signals.highlights.some((line) => line.includes("What feature vrei")));
});

test("extractSignals drops chatty delivery/status phrases from decisions and open loops", () => {
  const signals = extractSignals([
    "Perfect. Îți trimit acum un first real send prin IMM-Romania.",
    "Dacă vrei, următorul pas e să facem cronul.",
    "IMM-Romania PR #3 was merged to main today and the branded GitHub digest direction was finalized.",
    "Remaining open loop: improve LCM scoping for the real day brief.",
  ]);

  assert.ok(signals.decisions.some((line) => line.includes("IMM-Romania PR #3")));
  assert.ok(signals.openLoops.some((line) => line.includes("improve LCM scoping")));
  assert.ok(!signals.highlights.some((line) => line.includes("Îți trimit")));
  assert.ok(!signals.openLoops.some((line) => line.includes("Dacă vrei")));
});
