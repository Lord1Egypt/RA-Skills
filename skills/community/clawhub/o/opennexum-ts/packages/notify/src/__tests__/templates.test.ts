import assert from "node:assert/strict";
import { mock } from "node:test";
import test from "node:test";

import { formatBatchDone, formatComplete, formatDispatch, formatFail } from "../templates.js";
import { sendMessage } from "../telegram.js";

// ─── formatDispatch ───────────────────────────────────────────────────────────

test("formatDispatch contains taskId, agentId, scopeCount, progress", () => {
  const result = formatDispatch("NX-004", "Telegram Notify", "agent-1", 7, 4, "2/10");
  assert.ok(result.includes("NX-004"), "should contain taskId");
  assert.ok(result.includes("agent-1"), "should contain agentId");
  assert.ok(result.includes("7"), "should contain scopeCount");
  assert.ok(result.includes("2/10"), "should contain progress");
  assert.ok(typeof result === "string", "should return a string");
});

test("formatDispatch contains taskName and deliverablesCount", () => {
  const result = formatDispatch("NX-004", "Telegram Notify", "agent-1", 7, 4, "2/10");
  assert.ok(result.includes("Telegram Notify"), "should contain taskName");
  assert.ok(result.includes("4"), "should contain deliverablesCount");
});

// ─── formatComplete ───────────────────────────────────────────────────────────

test("formatComplete contains taskName, elapsed, passCount, unlockedTasks", () => {
  const result = formatComplete("NX-004", "Telegram Notify", 12500, 1, 5, 5, ["NX-005", "NX-006"], "3/10");
  assert.ok(result.includes("Telegram Notify"), "should contain taskName");
  assert.ok(result.includes("5/5"), "should contain passCount/totalCount");
  assert.ok(result.includes("NX-005"), "should contain unlocked task NX-005");
  assert.ok(result.includes("NX-006"), "should contain unlocked task NX-006");
  assert.ok(result.includes("3/10"), "should contain progress");
});

test("formatComplete shows elapsed time", () => {
  const result = formatComplete("NX-004", "Telegram Notify", 65000, 1, 5, 5, [], "3/10");
  assert.ok(result.includes("1m5s"), "should contain elapsed in minutes");
});

test("formatComplete with no unlocked tasks says none", () => {
  const result = formatComplete("NX-004", "Telegram Notify", 1000, 1, 5, 5, [], "3/10");
  assert.ok(result.includes("无") || result.includes("none"), "should say none when no unlocked tasks");
});

// ─── formatFail ───────────────────────────────────────────────────────────────

test("formatFail contains failCount and feedbackExcerpt", () => {
  const result = formatFail(
    "NX-004",
    "Telegram Notify",
    2,
    3,
    5,
    2,
    ["C3 - missing field", "C5 - build failed"],
    "Build error on line 42"
  );
  assert.ok(result.includes("2"), "should contain failCount");
  assert.ok(result.includes("Build error on line 42"), "should contain feedbackExcerpt");
  assert.ok(result.includes("C3 - missing field"), "should contain failed criteria");
  assert.ok(result.includes("C5 - build failed"), "should contain failed criteria");
});

test("formatFail contains taskId and iteration", () => {
  const result = formatFail("NX-004", "Telegram Notify", 2, 3, 5, 2, [], "some feedback");
  assert.ok(result.includes("NX-004"), "should contain taskId");
  assert.ok(result.includes("2"), "should contain iteration");
});

// ─── formatBatchDone ──────────────────────────────────────────────────────────

test("formatBatchDone contains projectName and task statuses", () => {
  const result = formatBatchDone("nexum-ts", [
    { taskId: "NX-001", taskName: "Foundation", status: "done", elapsedMs: 5000 },
    { taskId: "NX-002", taskName: "Notify", status: "fail", elapsedMs: 3000 },
  ]);
  assert.ok(result.includes("nexum-ts"), "should contain projectName");
  assert.ok(result.includes("NX-001"), "should contain first task id");
  assert.ok(result.includes("NX-002"), "should contain second task id");
  assert.ok(result.includes("Foundation"), "should contain task name");
});

// ─── sendMessage error handling ───────────────────────────────────────────────

test("sendMessage does not throw when fetch throws", async () => {
  const originalFetch = global.fetch;
  // @ts-ignore — intentionally replacing fetch for this test
  global.fetch = async () => {
    throw new Error("network error");
  };

  try {
    // Should resolve without throwing
    await assert.doesNotReject(async () => {
      await sendMessage("chat123", "hello", "fake-token");
    });
  } finally {
    global.fetch = originalFetch;
  }
});

test("sendMessage does not throw when fetch returns non-ok", async () => {
  const originalFetch = global.fetch;
  // @ts-ignore — intentionally replacing fetch for this test
  global.fetch = async () => ({
    ok: false,
    status: 400,
    text: async () => "Bad Request",
  });

  try {
    await assert.doesNotReject(async () => {
      await sendMessage("chat123", "hello", "fake-token");
    });
  } finally {
    global.fetch = originalFetch;
  }
});
