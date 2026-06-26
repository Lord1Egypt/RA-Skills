import test from "node:test";
import assert from "node:assert/strict";
import { readLcmDayContext } from "../src/sources/lcm-source.js";
import { createLcmFixtureDb } from "./helpers/create-lcm-fixture.js";

test("readLcmDayContext loads recent same-session context and summaries from SQLite", async () => {
  const dbPath = await createLcmFixtureDb();
  const result = await readLcmDayContext({
    date: "2026-04-09",
    dbPath,
    sessionKey: "agent:main:main",
    conversationLimit: 1,
  });

  assert.equal(result.source, "lcm");
  assert.deepEqual(result.conversationIds, [2]);
  assert.ok(result.lines.some((line) => line.includes("Mindkeeper summary context")));
  assert.ok(result.lines.some((line) => line.includes("Mindkeeper")));
  assert.ok(!result.lines.some((line) => line.includes("OldProject")));
  assert.ok(!result.lines.some((line) => line.includes("Different session")));
  assert.ok(!result.lines.some((line) => line.includes("Noisy tool output")));
});

test("readLcmDayContext can include tool messages when explicitly enabled", async () => {
  const dbPath = await createLcmFixtureDb();
  const result = await readLcmDayContext({
    date: "2026-04-09",
    dbPath,
    sessionKey: "agent:main:main",
    includeTools: true,
    includeSummaries: false,
    conversationLimit: 1,
  });

  assert.ok(result.lines.some((line) => line.includes("Noisy tool output")));
});
