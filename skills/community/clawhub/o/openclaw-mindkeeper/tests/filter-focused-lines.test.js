import test from "node:test";
import assert from "node:assert/strict";
import { filterFocusedLines } from "../src/pipeline/filter-focused-lines.js";

test("filterFocusedLines keeps only lines matching focus terms", () => {
  const lines = [
    "We decided the final product name is Mindkeeper.",
    "Use lossless-claw as the memory engine.",
    "Completely unrelated project conversation.",
  ];

  const filtered = filterFocusedLines(lines, ["mindkeeper", "lossless"]);
  assert.equal(filtered.length, 2);
  assert.ok(filtered.every((line) => /mindkeeper|lossless/i.test(line)));
});

test("filterFocusedLines returns all lines when no focus terms are provided", () => {
  const lines = ["a", "b"];
  assert.deepEqual(filterFocusedLines(lines, []), lines);
});
