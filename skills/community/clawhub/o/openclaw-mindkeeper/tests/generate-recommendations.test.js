import test from "node:test";
import assert from "node:assert/strict";
import { generateRecommendations } from "../src/pipeline/generate-recommendations.js";

test("generateRecommendations derives actions from highlights and decisions", () => {
  const recommendations = generateRecommendations({
    highlights: [
      "Mindkeeper emails should use the same visual family as the IMM-Romania MSP GitHub checker email template.",
      "prompt-to-pr v1.5.0 work: repo registry, bounded discovery, PR/merge, local sync cleanup",
    ],
    decisions: ["IMM-Romania PR #3 was merged to main after iterative live review by Alex."],
    openLoops: [],
    recommendations: [],
  });

  assert.ok(recommendations.some((line) => /template, branding, and copy consistent/i.test(line)));
  assert.ok(recommendations.some((line) => /recent shipped work/i.test(line)));
  assert.ok(recommendations.length <= 3);
});

test("generateRecommendations falls back when a day has signal but no obvious open loop", () => {
  const recommendations = generateRecommendations({
    highlights: ["Mindkeeper should be a clarity / sensemaking tool, not just a generic daily summary bot."],
    decisions: [],
    openLoops: [],
    recommendations: [],
  });

  assert.equal(recommendations.length, 1);
  assert.match(recommendations[0], /Review the day’s strongest signal/i);
});
