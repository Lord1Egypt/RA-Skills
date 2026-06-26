import assert from "node:assert/strict";
import test from "node:test";

import {
  formatBatchDone,
  formatDispatch,
  formatGeneratorDone,
  formatReviewFailed,
  formatReviewPassed,
} from "../templates.js";

test("formatDispatch includes task details and optional batch progress", () => {
  const result = formatDispatch({
    taskId: "NX-004",
    taskName: "Message Notify",
    agent: "codex-gen-01 (NX-004)",
    model: "gpt-5.4",
    scopeCount: 7,
    deliverablesCount: 4,
    progress: "2/10",
    batchProgress: "batch-a: 1/3",
  });

  assert.ok(result.includes("NX-004"));
  assert.ok(result.includes("Message Notify"));
  assert.ok(result.includes("codex-gen-01"));
  assert.ok(result.includes("gpt-5.4"));
  assert.ok(result.includes("7"));
  assert.ok(result.includes("4"));
  assert.ok(result.includes("batch-a: 1/3"));
  assert.ok(result.includes("2/10"));
});

test("formatGeneratorDone includes commit and elapsed fields", () => {
  const result = formatGeneratorDone({
    taskId: "NX-004",
    taskName: "Message Notify",
    agent: "codex-gen-01",
    model: "gpt-5.4",
    inputTokens: 1200,
    outputTokens: 345,
    scopeFiles: ["a.ts", "b.ts"],
    commitHash: "1234567890abcdef",
    commitMessage: "feat(nx-004): add notify flow",
    iteration: 1,
    elapsedMs: 65_000,
  });

  assert.ok(result.includes("1234567"));
  assert.ok(result.includes("feat(nx-004): add notify flow"));
  assert.ok(result.includes("1m5s"));
  assert.ok(result.includes("第2次"));
  assert.ok(result.includes("1,200 in / 345 out"));
});

test("formatReviewPassed includes unlocked tasks and progress", () => {
  const result = formatReviewPassed({
    taskId: "NX-004",
    taskName: "Message Notify",
    evaluator: "claude-eval-01",
    model: "sonnet-4-6",
    elapsedMs: 12_500,
    iteration: 1,
    passCount: 5,
    totalCount: 5,
    unlockedTasks: ["NX-005", "NX-006"],
    progress: "3/10",
    batchProgress: "batch-a: 2/4",
  });

  assert.ok(result.includes("Message Notify"));
  assert.ok(result.includes("claude-eval-01"));
  assert.ok(result.includes("5/5"));
  assert.ok(result.includes("NX-005"));
  assert.ok(result.includes("NX-006"));
  assert.ok(result.includes("12s"));
  assert.ok(result.includes("batch-a: 2/4"));
  assert.ok(result.includes("3/10"));
});

test("formatReviewFailed expands failed criteria and retry hint", () => {
  const result = formatReviewFailed({
    taskId: "NX-004",
    taskName: "Message Notify",
    evaluator: "claude-eval-01",
    model: "sonnet-4-6",
    iteration: 2,
    passCount: 3,
    totalCount: 5,
    criteriaResults: [
      { id: "C1", passed: true, reason: "looks good" },
      { id: "C3", passed: false, reason: "missing field" },
      { id: "C5", passed: false, reason: "build failed" },
    ],
    feedback: "Build error on line 42",
    autoRetryHint: "自动重试中",
  });

  assert.ok(result.includes("NX-004"));
  assert.ok(result.includes("第3次"));
  assert.ok(result.includes("3/5"));
  assert.ok(result.includes("C3"));
  assert.ok(result.includes("missing field"));
  assert.ok(result.includes("C5"));
  assert.ok(result.includes("build failed"));
  assert.ok(result.includes("Build error on line 42"));
  assert.ok(result.includes("自动重试中"));
});

test("formatBatchDone includes project summary and task rows", () => {
  const result = formatBatchDone({
    batchName: "nexum-ts",
    totalElapsedMs: 8_000,
    tasks: [
      { taskId: "NX-001", taskName: "Foundation", status: "done", elapsedMs: 5_000 },
      { taskId: "NX-002", taskName: "Notify", status: "fail", elapsedMs: 3_000 },
    ],
  });

  assert.ok(result.includes("nexum-ts"));
  assert.ok(result.includes("1/2"));
  assert.ok(result.includes("NX-001"));
  assert.ok(result.includes("Foundation"));
  assert.ok(result.includes("NX-002"));
  assert.ok(result.includes("Notify"));
  assert.ok(result.includes("8s"));
});
