import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {assertEvidenceClaims} from "../src/orchestration/handoff-reporter.mjs";
import {runFakeOneClickSession} from "../src/orchestration/orchestrator.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SUITE = JSON.parse(fs.readFileSync(path.join(ROOT, "fixtures/runtime/scenarios.json"), "utf8"));
const BY_ID = new Map(SUITE.scenarios.map((scenario) => [scenario.scenarioId, scenario]));

function run(id) {
  const scenario = BY_ID.get(id);
  assert.ok(scenario, `fixture missing: ${id}`);
  return runFakeOneClickSession(scenario);
}

test("全部离线场景到达声明阶段且 handoff 证据不过度声称", () => {
  assert.ok(SUITE.scenarios.length >= 10);
  for (const scenario of SUITE.scenarios) {
    const result = runFakeOneClickSession(scenario);
    assert.equal(result.manifest.stage, scenario.expectedStage, scenario.scenarioId);
    assert.equal(assertEvidenceClaims(result.handoff), true, scenario.scenarioId);
  }
});

test("happy path 默认停在可编辑时间线 review_ready，不做增强、导出或发布", () => {
  const result = run("scenario-happy-path");
  assert.equal(result.manifest.stage, "review_ready");
  assert.equal(result.manifest.status, "review_ready");
  assert.equal(result.handoff.deliveryState, "review_ready");
  assert.equal(result.handoff.verification.structure, "pass");
  assert.equal(result.handoff.verification.visual, "pass");
  assert.equal(result.handoff.verification.humanListening, "unverified");
  for (const item of ["restructure", "music", "motion-graphics", "broll", "generated-media", "export", "publish"]) {
    assert.ok(result.handoff.notPerformed.includes(item), item);
  }
  assert.equal(result.brief.treatments.export, false);
  assert.equal(result.brief.treatments.music, false);
});

test("缺项目时创建一次逻辑项目且不重复导入主素材", () => {
  const result = run("scenario-project-created");
  assert.equal(result.manifest.project.projectRef, "logical:project-new");
  assert.deepEqual(result.manifest.sourceAssets, ["logical:aroll-main"]);
  assert.equal(result.manifest.stage, "review_ready");
});

test("转写 pending 与 failed 都停在 project checkpoint", () => {
  const pending = run("scenario-transcript-pending");
  assert.equal(pending.manifest.status, "blocked");
  assert.equal(pending.manifest.blockedReason.code, "TRANSCRIPT_PENDING");
  assert.equal(pending.decisionLog, null);

  const failed = run("scenario-transcript-failed");
  assert.equal(failed.manifest.status, "blocked");
  assert.equal(failed.manifest.blockedReason.code, "TRANSCRIPT_FAILED");
  assert.equal(failed.decisionLog, null);
});

test("timeout-before 仅在 readback 证明未提交后 retry 且不重复写", () => {
  const result = run("scenario-timeout-before");
  assert.equal(result.recovery.status, "completed");
  assert.ok(result.recovery.reconciliations.includes("retry"));
  assert.equal(result.recovery.objectCount, 1);
  assert.equal(result.recovery.duplicateWrites, false);
  assert.equal(result.manifest.stage, "review_ready");
});

test("timeout-after 由 readback 认领已提交写入且不重复写", () => {
  const result = run("scenario-timeout-after");
  assert.equal(result.recovery.status, "completed");
  assert.ok(result.recovery.reconciliations.includes("readback"));
  assert.equal(result.recovery.objectCount, 1);
  assert.equal(result.recovery.duplicateWrites, false);
  assert.equal(result.manifest.stage, "review_ready");
});

test("partial write 实际补偿后进入 blocked", () => {
  const result = run("scenario-partial-write");
  assert.equal(result.recovery.status, "failed");
  assert.ok(result.recovery.reconciliations.includes("compensated"));
  assert.equal(result.recovery.objectCount, 1);
  assert.equal(result.recovery.duplicateWrites, false);
  assert.equal(result.manifest.status, "blocked");
  assert.equal(result.manifest.blockedReason.code, "PARTIAL_WRITE");
  assert.equal(result.manifest.blockedReason.resumeStage, "edit_plan_ready");
  assert.equal(result.manifest.approvals[0].status, "stale");
});

test("手工改动与 stale timeline 都使样片批准失效且不会覆盖", () => {
  for (const id of ["scenario-manual-edit", "scenario-stale-timeline"]) {
    const result = run(id);
    assert.equal(result.manifest.status, "blocked", id);
    assert.equal(result.manifest.blockedReason.code, "TIMELINE_REVISION_DRIFT", id);
    assert.equal(result.manifest.approvals[0].status, "stale", id);
    assert.equal(result.handoff.verification.sampleApproval, "stale", id);
    assert.equal(result.recovery, null, id);
  }
});

test("无 renderer 时只把 visual 标为 unverified", () => {
  const result = run("scenario-renderer-unavailable");
  assert.equal(result.manifest.stage, "review_ready");
  assert.equal(result.handoff.verification.structure, "pass");
  assert.equal(result.handoff.verification.visual, "unverified");
  assert.ok(result.handoff.openRisks.length > 0);
});

test("未授权导出时始终停在 review_ready", () => {
  const result = run("scenario-export-not-authorized");
  assert.equal(result.manifest.stage, "review_ready");
  assert.equal(result.manifest.status, "review_ready");
  assert.equal(result.handoff.completed.includes("export"), false);
  assert.ok(result.handoff.notPerformed.includes("export"));
});

test("只审核、先不要改时间线时执行器保持零写入", () => {
  const scenario = structuredClone(BY_ID.get("scenario-happy-path"));
  scenario.intent = "只给我审核方案，先不要改时间线";
  const result = runFakeOneClickSession(scenario);
  assert.equal(result.route.action, "review");
  assert.equal(result.manifest.stage, "edit_plan_ready");
  assert.equal(result.recovery.status, "not-run");
  assert.equal(result.recovery.objectCount, 0);
  assert.ok(result.decisionLog.decisions.every((item) => item.status === "proposed"));
  assert.equal(result.handoff.completed.includes("sample"), false);
});

test("继续意图不能创建一条新的运行", () => {
  const scenario = structuredClone(BY_ID.get("scenario-happy-path"));
  scenario.intent = "继续上次剪辑";
  const result = runFakeOneClickSession(scenario);
  assert.equal(result.route.action, "resume");
  assert.equal(result.manifest.stage, "preflight");
  assert.equal(result.manifest.status, "blocked");
  assert.equal(result.manifest.blockedReason.code, "RUN_CONTEXT_REQUIRED");
  assert.equal(result.recovery, null);
});
