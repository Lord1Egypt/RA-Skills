import test from "node:test";
import assert from "node:assert/strict";
import { extractFocusTerms } from "../src/pipeline/extract-focus-terms.js";

test("extractFocusTerms prefers explicit terms", () => {
  assert.deepEqual(extractFocusTerms({ explicitTerms: ["mindkeeper", "lossless"] }), ["mindkeeper", "lossless"]);
});

test("extractFocusTerms derives terms from title and prompt", () => {
  const terms = extractFocusTerms({
    title: "Mindkeeper daily brief",
    prompt: "Focus on lossless-claw integration and openclaw-mindkeeper naming",
  });

  assert.ok(terms.includes("lossless-claw") || terms.includes("lossless"));
  assert.ok(terms.includes("openclaw-mindkeeper"));
});

test("extractFocusTerms drops generic meta words", () => {
  const terms = extractFocusTerms({
    prompt: "Focus on today's real work and the remaining open loops for NexLink",
  });

  assert.ok(!terms.includes("focus"));
  assert.ok(!terms.includes("today"));
  assert.ok(!terms.includes("real"));
  assert.ok(terms.includes("nexlink"));
});
