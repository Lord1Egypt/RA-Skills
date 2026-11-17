#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import {
  FakeTimelineAdapter,
  RecoverableExecutor,
} from "../src/execution/recoverable-executor.mjs";
import {assertEvidenceClaims} from "../src/orchestration/handoff-reporter.mjs";
import {runFakeOneClickSession} from "../src/orchestration/orchestrator.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const REQUIRED = Object.freeze([
  "scenario-happy-path",
  "scenario-timeout-before",
  "scenario-timeout-after",
  "scenario-partial-write",
  "scenario-manual-edit",
]);

function parseArguments(argv) {
  if (argv.length === 0) return {json: false};
  if (argv.length === 1 && argv[0] === "--json") return {json: true};
  process.stderr.write("Usage: node scripts/smoke-one-click.mjs [--json]\n");
  process.exit(2);
}

function readJson(relativePath) {
  try {
    return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
  } catch {
    throw new Error("SMOKE_FIXTURE_READ_FAILED");
  }
}

function requireCondition(condition, code) {
  if (!condition) throw new Error(code);
}

function exerciseRecovery(plan, failure) {
  const adapter = new FakeTimelineAdapter();
  adapter.injectFailure("operation_001", failure);
  const executor = new RecoverableExecutor(adapter);
  const result = executor.execute({
    executionPlan: plan,
    approvalReport: {canExecute: true},
  });
  return {result, adapter};
}

function runSmoke() {
  const suite = readJson("fixtures/runtime/scenarios.json");
  const executionPlan = readJson("fixtures/execution/valid/execution-plan.json");
  const byId = new Map(suite.scenarios.map((scenario) => [scenario.scenarioId, scenario]));
  requireCondition(REQUIRED.every((id) => byId.has(id)), "SMOKE_REQUIRED_SCENARIO_MISSING");

  const results = Object.fromEntries(
    REQUIRED.map((id) => {
      const scenario = byId.get(id);
      const result = runFakeOneClickSession(scenario);
      requireCondition(result.manifest.stage === scenario.expectedStage, "SMOKE_STAGE_MISMATCH");
      assertEvidenceClaims(result.handoff);
      return [id, result];
    }),
  );

  const happy = results["scenario-happy-path"];
  requireCondition(happy.manifest.status === "review_ready", "SMOKE_HAPPY_NOT_REVIEW_READY");
  requireCondition(happy.handoff.verification.structure === "pass", "SMOKE_STRUCTURE_NOT_PROVEN");
  requireCondition(happy.handoff.verification.visual === "pass", "SMOKE_VISUAL_NOT_PROVEN");
  requireCondition(happy.handoff.verification.humanListening === "unverified", "SMOKE_LISTENING_OVERCLAIM");
  requireCondition(happy.handoff.notPerformed.includes("export"), "SMOKE_EXPORT_BOUNDARY_MISSING");
  requireCondition(happy.handoff.notPerformed.includes("publish"), "SMOKE_PUBLISH_BOUNDARY_MISSING");

  const timeoutBefore = exerciseRecovery(executionPlan, "timeout-before-commit");
  requireCondition(timeoutBefore.result.status === "completed", "SMOKE_TIMEOUT_BEFORE_FAILED");
  requireCondition(
    timeoutBefore.result.journal.entries[0]?.reconciliation === "retry",
    "SMOKE_TIMEOUT_BEFORE_RETRY_MISSING",
  );
  requireCondition(
    timeoutBefore.adapter.objectCount() === executionPlan.operations.length,
    "SMOKE_TIMEOUT_BEFORE_DUPLICATE_WRITE",
  );

  const timeoutAfter = exerciseRecovery(executionPlan, "timeout-after-commit");
  requireCondition(timeoutAfter.result.status === "completed", "SMOKE_TIMEOUT_AFTER_FAILED");
  requireCondition(
    timeoutAfter.result.journal.entries[0]?.reconciliation === "readback",
    "SMOKE_TIMEOUT_AFTER_READBACK_MISSING",
  );
  requireCondition(
    timeoutAfter.adapter.objectCount() === executionPlan.operations.length,
    "SMOKE_TIMEOUT_AFTER_DUPLICATE_WRITE",
  );

  const partial = results["scenario-partial-write"];
  const partialRecovery = exerciseRecovery(executionPlan, "partial-write");
  requireCondition(partial.manifest.status === "blocked", "SMOKE_PARTIAL_NOT_BLOCKED");
  requireCondition(partial.manifest.blockedReason?.code === "PARTIAL_WRITE", "SMOKE_PARTIAL_REASON_MISSING");
  requireCondition(partialRecovery.result.status === "failed", "SMOKE_PARTIAL_EXECUTOR_NOT_FAILED");
  requireCondition(partialRecovery.adapter.objectCount() === 0, "SMOKE_PARTIAL_NOT_COMPENSATED");

  const manual = results["scenario-manual-edit"];
  requireCondition(manual.manifest.status === "blocked", "SMOKE_MANUAL_EDIT_NOT_BLOCKED");
  requireCondition(
    manual.manifest.blockedReason?.code === "TIMELINE_REVISION_DRIFT",
    "SMOKE_MANUAL_EDIT_REASON_MISSING",
  );
  requireCondition(
    manual.handoff.verification.sampleApproval === "stale",
    "SMOKE_MANUAL_EDIT_APPROVAL_NOT_STALE",
  );

  return {
    ok: true,
    scenarios: {
      happy: {stage: happy.manifest.stage, status: happy.manifest.status},
      timeoutBefore: {stage: results["scenario-timeout-before"].manifest.stage, reconciliation: "retry"},
      timeoutAfter: {stage: results["scenario-timeout-after"].manifest.stage, reconciliation: "readback"},
      partialWrite: {stage: partial.manifest.stage, status: partial.manifest.status, compensated: true},
      manualEdit: {stage: manual.manifest.stage, status: manual.manifest.status, preserved: true},
    },
    evidence: {
      class: "offline-simulation",
      structure: "pass",
      fakeRecovery: "pass",
      liveChatCut: "unverified",
      realMedia: "unverified",
      humanListening: "unverified",
      stableClaimEligible: false,
    },
  };
}

const options = parseArguments(process.argv.slice(2));
try {
  const result = runSmoke();
  if (options.json) {
    process.stdout.write(`${JSON.stringify(result)}\n`);
  } else {
    process.stdout.write(
      "one-click fake smoke passed: happy + timeout-before(retry) + timeout-after(readback) + partial-write(compensated) + manual-edit(preserved); evidence=offline-simulation, live=UNVERIFIED\n",
    );
  }
} catch (error) {
  const code = typeof error?.message === "string" && /^SMOKE_[A-Z0-9_]+$/u.test(error.message)
    ? error.message
    : "SMOKE_ONE_CLICK_FAILED";
  process.stderr.write(`${code}: one-click fake smoke failed\n`);
  process.exitCode = 1;
}
