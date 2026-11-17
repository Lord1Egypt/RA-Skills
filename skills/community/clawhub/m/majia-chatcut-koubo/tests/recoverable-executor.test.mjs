import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  ExecutionError,
  FakeTimelineAdapter,
  RecoverableExecutor,
  invalidateEvidence,
} from "../src/execution/recoverable-executor.mjs";
import {contentHash} from "../src/planning/preview-approval.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

function plan() {
  return JSON.parse(fs.readFileSync(
    path.join(ROOT, "fixtures/execution/valid/execution-plan.json"),
    "utf8",
  ));
}

const APPROVED = Object.freeze({canExecute: true});

test("successful scenes create readback evidence and a checkpoint", () => {
  const adapter = new FakeTimelineAdapter();
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  assert.equal(result.status, "completed");
  assert.equal(result.journal.status, "completed");
  assert.equal(adapter.objectCount(), 2);
  assert.equal(result.journal.entries.length, 2);
  assert.ok(result.journal.entries.every(
    (entry) => entry.result === "verified",
  ));
  assert.equal(result.evidenceManifest.artifacts.length, 2);
  assert.ok(result.evidenceManifest.artifacts.every(
    (artifact) => artifact.result === "passed",
  ));
  assert.equal(result.journal.checkpoints.length, 1);
  assert.deepEqual(
    result.journal.checkpoints[0].evidenceRefs.sort(),
    ["evidence_operation_001", "evidence_operation_002"],
  );
});

test("bounded sample gate 只允许低中风险且限定 scope", () => {
  const samplePlan = plan();
  for (const [index, operation] of samplePlan.operations.entries()) {
    operation.risk = index === 0 ? "low" : "medium";
    operation.scopeRef = `logical:sample-${index + 1}`;
  }
  const adapter = new FakeTimelineAdapter();
  const completed = new RecoverableExecutor(adapter).execute({
    executionPlan: samplePlan,
    executionGate: {
      kind: "bounded-sample",
      canExecute: true,
      planHash: samplePlan.planHash,
      timelineRevision: samplePlan.timelineRevision,
      scope: samplePlan.operations.map((item) => item.scopeRef),
    },
  });
  assert.equal(completed.status, "completed");

  const unsafePlan = plan();
  unsafePlan.operations[0].risk = "high";
  unsafePlan.operations[0].scopeRef = "logical:sample-1";
  assert.throws(
    () => new RecoverableExecutor(new FakeTimelineAdapter()).execute({
      executionPlan: unsafePlan,
      executionGate: {
        kind: "bounded-sample",
        canExecute: true,
        planHash: unsafePlan.planHash,
        timelineRevision: unsafePlan.timelineRevision,
        scope: ["logical:sample-1"],
      },
    }),
    (error) => error.code === "EXEC_SAMPLE_GATE_SCOPE_INVALID",
  );
});

test("replaying a completed journal is idempotent", () => {
  const adapter = new FakeTimelineAdapter();
  const executor = new RecoverableExecutor(adapter);
  const first = executor.execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  const revision = adapter.getRevision();
  const second = executor.execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
    journal: first.journal,
    evidenceManifest: first.evidenceManifest,
  });
  assert.equal(second.status, "completed");
  assert.equal(adapter.objectCount(), 2);
  assert.equal(adapter.getRevision(), revision);
  assert.equal(second.journal.entries.length, 2);
});

test("ambiguous timeout before commit reads then retries once", () => {
  const adapter = new FakeTimelineAdapter();
  adapter.injectFailure("operation_001", "timeout-before-commit");
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  assert.equal(result.status, "completed");
  assert.equal(result.journal.entries[0].reconciliation, "retry");
  assert.equal(adapter.objectCount(), 2);
});

test("ambiguous timeout after commit is proven by readback", () => {
  const adapter = new FakeTimelineAdapter();
  adapter.injectFailure("operation_001", "timeout-after-commit");
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  assert.equal(result.status, "completed");
  assert.equal(result.journal.entries[0].reconciliation, "readback");
  assert.equal(adapter.objectCount(), 2);
});

test("partial writes are compensated and never reported complete", () => {
  const adapter = new FakeTimelineAdapter();
  adapter.injectFailure("operation_001", "partial-write");
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  assert.equal(result.status, "failed");
  assert.equal(result.errorCode, "EXEC_POSTCONDITION_FAILED");
  assert.equal(result.journal.entries[0].result, "compensated");
  assert.equal(result.journal.entries[0].reconciliation, "compensated");
  assert.equal(adapter.objectCount(), 0);
});

test("logical IDs resolving to multiple host IDs stop execution", () => {
  const logicalId = "logical_state_001";
  const state = {kind: "state", value: "old"};
  const adapter = new FakeTimelineAdapter({
    objects: [
      {hostId: "host_1", logicalId, state, hash: contentHash(state)},
      {hostId: "host_2", logicalId, state, hash: contentHash(state)},
    ],
  });
  assert.throws(
    () => new RecoverableExecutor(adapter).execute({
      executionPlan: plan(),
      approvalReport: APPROVED,
    }),
    (error) =>
      error instanceof ExecutionError
      && error.code === "EXEC_BINDING_AMBIGUOUS",
  );
});

test("host ID changes remain safe when the logical binding stays unique", () => {
  const state = {kind: "state", value: "old"};
  const adapter = new FakeTimelineAdapter({
    objects: [{
      hostId: "host_1",
      logicalId: "logical_state_001",
      state,
      hash: contentHash(state),
    }],
  });
  adapter.injectFailure("operation_001", "id-change");
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  assert.equal(result.status, "completed");
  assert.equal(
    adapter.readLogical("logical_state_001")[0].hostId,
    "host_2",
  );
});

test("revision drift stops before mutation", () => {
  const adapter = new FakeTimelineAdapter();
  adapter.injectFailure("operation_001", "revision-drift");
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  assert.equal(result.status, "failed");
  assert.equal(result.errorCode, "EXEC_REVISION_DRIFT");
  assert.equal(adapter.objectCount(), 0);
});

test("resume skips proven work and continues after compensation", () => {
  const adapter = new FakeTimelineAdapter();
  const executor = new RecoverableExecutor(adapter);
  adapter.injectFailure("operation_002", "partial-write");
  const first = executor.execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  assert.equal(first.status, "failed");
  assert.equal(adapter.objectCount(), 0);
  assert.equal(first.journal.entries[0].result, "compensated");
  assert.equal(first.evidenceManifest.artifacts.length, 0);

  const resumed = executor.execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
    journal: first.journal,
    evidenceManifest: first.evidenceManifest,
  });
  assert.equal(resumed.status, "completed");
  assert.equal(adapter.objectCount(), 2);
  assert.equal(resumed.journal.entries.filter(
    (entry) => entry.operationId === "operation_001",
  ).length, 2);
  assert.equal(resumed.journal.entries.filter(
    (entry) => entry.operationId === "operation_002",
  ).length, 2);
});

test("evidence invalidation propagates through evidence dependencies", () => {
  const adapter = new FakeTimelineAdapter();
  const completed = new RecoverableExecutor(adapter).execute({
    executionPlan: plan(),
    approvalReport: APPROVED,
  });
  completed.evidenceManifest.artifacts.push({
    evidenceId: "evidence_release_001",
    kind: "export-probe",
    targetRef: "export_demo",
    path: null,
    sha256: `sha256:${"a".repeat(64)}`,
    result: "passed",
    sensitive: false,
    checks: ["EXPORT_MATCH"],
    dependencies: ["evidence_operation_001"],
    invalidatedBy: [],
  });
  const invalidated = invalidateEvidence(
    completed.evidenceManifest,
    ["operation_001"],
  );
  assert.equal(
    invalidated.artifacts.find(
      (item) => item.evidenceId === "evidence_operation_001",
    ).result,
    "unverified",
  );
  assert.equal(
    invalidated.artifacts.find(
      (item) => item.evidenceId === "evidence_release_001",
    ).result,
    "unverified",
  );
});

test("closed preview approval blocks all mutations", () => {
  const adapter = new FakeTimelineAdapter();
  assert.throws(
    () => new RecoverableExecutor(adapter).execute({
      executionPlan: plan(),
      approvalReport: {canExecute: false},
    }),
    (error) =>
      error instanceof ExecutionError
      && error.code === "EXEC_PREVIEW_NOT_APPROVED",
  );
  assert.equal(adapter.objectCount(), 0);
});
