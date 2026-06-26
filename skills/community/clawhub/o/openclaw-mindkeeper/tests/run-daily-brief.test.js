import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runDailyBrief } from "../src/pipeline/run-daily-brief.js";
import { createLcmFixtureDb } from "./helpers/create-lcm-fixture.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fixture = path.join(__dirname, "fixtures", "2026-04-09.md");

test("runDailyBrief builds a structured brief from a memory file", async () => {
  const result = await runDailyBrief({
    date: "2026-04-09",
    title: "Mindkeeper Daily Brief",
    memoryFile: fixture,
  });

  assert.equal(result.diagnostics.sources[0], "daily-memory-file");
  assert.ok(result.brief.summary.decisions.some((line) => line.includes("Mindkeeper")));
  assert.ok(result.brief.summary.openLoops.some((line) => line.includes("day-context collector")));
  assert.ok(result.brief.summary.recommendations.length >= 1);
});

test("runDailyBrief rejects empty runs with no sources", async () => {
  await assert.rejects(
    () => runDailyBrief({
      date: "2026-04-09",
      title: "Mindkeeper Daily Brief",
    }),
    /at least one source/,
  );
});

test("runDailyBrief can focus a brief to specific terms", async () => {
  const result = await runDailyBrief({
    date: "2026-04-09",
    title: "Mindkeeper Daily Brief",
    memoryFile: fixture,
    focusTerms: ["Mindkeeper", "lossless-claw"],
  });

  assert.ok(result.diagnostics.focusedLineCount >= 3);
  assert.ok(result.brief.summary.decisions.some((line) => line.includes("Mindkeeper")));
  assert.ok(result.brief.summary.openLoops.some((line) => line.includes("lossless-claw")));
});

test("runDailyBrief lossless-only mode ignores daily memory file and uses LCM only", async () => {
  const dbPath = await createLcmFixtureDb();
  const result = await runDailyBrief({
    date: "2026-04-09",
    title: "Mindkeeper Lossless-Only Brief",
    briefMode: "lossless-only",
    memoryFile: fixture,
    lcm: {
      enabled: true,
      dbPath,
      sessionKey: "agent:main:main",
      includeTools: false,
      includeSummaries: true,
      conversationLimit: 1,
      rawConversationLimit: 1,
      messageTail: 10,
      summaryLimit: 1,
      limit: 200,
    },
  });

  assert.equal(result.diagnostics.briefMode, "lossless-only");
  assert.deepEqual(result.diagnostics.sources, ["lcm"]);
  assert.ok(result.brief.summary.decisions.some((line) => line.includes("Mindkeeper")));
  assert.ok(!result.brief.summary.decisions.some((line) => line.includes("openclaw-mindkeeper")));
  assert.ok(result.brief.summary.recommendations.length >= 1);
});

test("runDailyBrief lossless-only mode requires LCM", async () => {
  await assert.rejects(
    () => runDailyBrief({
      date: "2026-04-09",
      title: "Mindkeeper Lossless-Only Brief",
      briefMode: "lossless-only",
      memoryFile: fixture,
    }),
    /lossless-only mode requires --use-lcm/,
  );
});
