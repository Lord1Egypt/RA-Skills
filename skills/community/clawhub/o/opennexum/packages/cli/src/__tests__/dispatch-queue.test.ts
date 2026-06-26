import assert from "node:assert/strict";
import { mkdir, readFile } from "node:fs/promises";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import {
  acknowledgeDispatchEntries,
  enqueueDispatchEntry,
  readDispatchQueueEntries
} from "../lib/dispatch-queue.js";

async function setupProject(): Promise<string> {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-dispatch-queue-"));
  await mkdir(path.join(projectDir, "nexum"), { recursive: true });
  return projectDir;
}

test("enqueueDispatchEntry preserves concurrent entries", async () => {
  const projectDir = await setupProject();

  await Promise.all([
    enqueueDispatchEntry(projectDir, {
      taskId: "TASK-001",
      action: "spawn-next",
      role: "generator",
      projectDir,
      sessionName: "codex-gen-01"
    }),
    enqueueDispatchEntry(projectDir, {
      taskId: "TASK-002",
      action: "spawn-next",
      role: "generator",
      projectDir,
      sessionName: "codex-gen-02"
    })
  ]);

  const entries = await readDispatchQueueEntries(projectDir);
  assert.equal(entries.length, 2);
  assert.deepEqual(
    entries.map((entry) => entry.taskId).sort(),
    ["TASK-001", "TASK-002"]
  );
});

test("enqueueDispatchEntry deduplicates taskId + action and acknowledgeDispatchEntries removes entries", async () => {
  const projectDir = await setupProject();

  await enqueueDispatchEntry(projectDir, {
    taskId: "TASK-001",
    action: "spawn-evaluator",
    role: "evaluator",
    projectDir,
    sessionName: "claude-eval-01"
  });
  await enqueueDispatchEntry(projectDir, {
    taskId: "TASK-001",
    action: "spawn-evaluator",
    role: "evaluator",
    projectDir,
    sessionName: "claude-eval-99"
  });

  let entries = await readDispatchQueueEntries(projectDir);
  assert.equal(entries.length, 1);
  assert.equal(entries[0]?.sessionName, "claude-eval-01");

  await acknowledgeDispatchEntries(
    projectDir,
    (entry) => entry.taskId === "TASK-001" && entry.action === "spawn-evaluator"
  );

  entries = await readDispatchQueueEntries(projectDir);
  assert.equal(entries.length, 0);
  const rawQueue = await readFile(path.join(projectDir, "nexum", "dispatch-queue.jsonl"), "utf8");
  assert.equal(rawQueue, "");
});
