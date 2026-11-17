import assert from "node:assert/strict";
import test from "node:test";

import {latestCheckpoint, registerFailure} from "../src/orchestration/checkpoint-manager.mjs";
import {createSampleFingerprint} from "../src/orchestration/preview-selector.mjs";
import {selectProfile} from "../src/orchestration/profile-selector.mjs";
import {
  approvalIsCurrent,
  approveSample,
  authorizeExport,
  authorizeEnhancements,
  blockRun,
  createRunManifest,
  createSampleBinding,
  invalidateApprovals,
  requestSampleRevision,
  resumeRun,
  RunStateError,
  transitionRun,
} from "../src/orchestration/run-state.mjs";

const NOW = "2026-08-10T00:00:00Z";

function manifestAtSample() {
  let manifest = createRunManifest({
    runId: "run-state-test",
    profile: selectProfile(),
    projectRef: "logical:project-current",
    timelineRef: "logical:timeline-current",
    timelineRevision: "rev-current",
    now: NOW,
  });
  for (const stage of ["brief_ready", "project_ready", "transcript_ready", "edit_plan_ready", "sample_ready"]) {
    manifest = transitionRun(manifest, stage, {
      now: NOW,
      ...(stage === "sample_ready"
        ? {sampleBinding: createSampleBinding({fingerprints: fingerprints(), scope: ["logical:sample-opening"], now: NOW})}
        : {}),
    });
  }
  return manifest;
}

function fingerprints(revision = "rev-current") {
  return createSampleFingerprint({
    plan: [{action: "remove-false-start"}],
    style: {profile: "balanced-stable"},
    layout: {states: ["A"]},
    captions: {enabled: true},
    timelineRevision: revision,
    windows: [{windowRef: "logical:sample-opening", startSec: 0, endSec: 30}],
  });
}

test("状态机允许顺序推进并阻止非法跳阶段", () => {
  const manifest = createRunManifest({runId: "run-transition", profile: selectProfile(), now: NOW});
  assert.equal(transitionRun(manifest, "brief_ready", {now: NOW}).stage, "brief_ready");
  assert.throws(
    () => transitionRun(manifest, "project_ready", {now: NOW}),
    (error) => error instanceof RunStateError && error.code === "RUN_TRANSITION_INVALID",
  );
});

test("代表样片确认持久化完整六维绑定", () => {
  const allFingerprints = fingerprints();
  const approved = approveSample(manifestAtSample(), {
    fingerprints: allFingerprints,
    scope: ["logical:sample-opening"],
    now: NOW,
  });
  assert.equal(approved.stage, "sample_approved");
  assert.deepEqual(
    Object.keys(approved.approvals[0].fingerprints).sort(),
    ["captions", "layout", "plan", "sample", "style", "timelineRevision"].sort(),
  );
  assert.equal(approved.approvals[0].approvalRef, "logical:sample-approval-state-test");
  assert.equal(approvalIsCurrent(approved, allFingerprints), true);
  assert.equal(approvalIsCurrent(approved, {...allFingerprints, style: "sha256:" + "0".repeat(64)}), false);
});

test("样片未确认不能整片扩展", () => {
  const sample = manifestAtSample();
  assert.throws(
    () => transitionRun(sample, "sample_approved", {now: NOW}),
    (error) => error.code === "RUN_SAMPLE_APPROVAL_REQUIRED",
  );
});

test("用户可要求样片更自然或更紧，并使旧绑定失效", () => {
  const revised = requestSampleRevision(manifestAtSample(), {direction: "natural", now: NOW});
  assert.equal(revised.stage, "revision_requested");
  assert.equal(revised.sampleBinding, null);
  assert.equal(revised.lastSafeAction, "replan_sample_natural");
});

test("时间线漂移使审批 stale 并保持 blocked", () => {
  const approved = approveSample(manifestAtSample(), {
    fingerprints: fingerprints(),
    scope: ["logical:sample-opening"],
    now: NOW,
  });
  const stale = invalidateApprovals(approved, {currentRevision: "rev-manual", now: NOW});
  assert.equal(stale.status, "blocked");
  assert.equal(stale.project.timelineRevision, "rev-manual");
  assert.equal(stale.approvals[0].status, "stale");
  assert.equal(approvalIsCurrent(stale, fingerprints("rev-manual")), false);
});

test("样片审批拒绝 blocked、旧 revision 与不完整 scope", () => {
  const sample = manifestAtSample();
  const blocked = blockRun(sample, {code: "PRIVACY_UNVERIFIED", message: "privacy pending", now: NOW});
  assert.throws(
    () => approveSample(blocked, {fingerprints: fingerprints(), scope: ["logical:sample-opening"], now: NOW}),
    (error) => error.code === "RUN_SAMPLE_APPROVAL_BLOCKED",
  );
  assert.throws(
    () => approveSample(sample, {fingerprints: fingerprints("rev-old"), scope: ["logical:sample-opening"], now: NOW}),
    (error) => error.code === "RUN_SAMPLE_REVISION_MISMATCH",
  );
  assert.throws(
    () => approveSample(sample, {fingerprints: fingerprints(), scope: ["logical:other-window"], now: NOW}),
    (error) => error.code === "RUN_SAMPLE_BINDING_MISMATCH",
  );
});

test("resume 需要 blocker 对账与 checkpoint，revision 变化时继续阻断", () => {
  const sample = manifestAtSample();
  const blocked = blockRun(sample, {
    code: "TRANSIENT_FAILURE",
    message: "temporary failure",
    resumeStage: "sample_ready",
    now: NOW,
  });
  blocked.checkpoints = ["cp-sample-ready-001"];
  const checkpoint = {
    checkpointId: "cp-sample-ready-001",
    runId: blocked.runId,
    stage: "sample_ready",
  };
  assert.throws(
    () => resumeRun(blocked, {currentTimelineRevision: "rev-current", now: NOW}),
    (error) => error.code === "RUN_RECONCILIATION_REQUIRED",
  );
  const resumed = resumeRun(blocked, {
    currentTimelineRevision: "rev-current",
    checkpoint,
    reconciliation: {
      blockerCode: "TRANSIENT_FAILURE",
      outcome: "unchanged",
      evidenceRefs: ["logical:timeline-readback"],
      checkpointId: checkpoint.checkpointId,
      observedRevision: "rev-current",
    },
    now: NOW,
  });
  assert.equal(resumed.stage, "sample_ready");
  assert.equal(resumed.status, "waiting_user_approval");
  assert.equal(resumed.blockedReason, null);

  const drifted = resumeRun(blocked, {currentTimelineRevision: "rev-new", now: NOW});
  assert.equal(drifted.status, "blocked");
  assert.equal(drifted.blockedReason.code, "TIMELINE_REVISION_DRIFT");
});

test("导出既要样片确认也要单独导出授权", () => {
  let manifest = approveSample(manifestAtSample(), {
    fingerprints: fingerprints(),
    scope: ["logical:sample-opening"],
    now: NOW,
  });
  for (const stage of ["full_aroll_applied", "captions_audio_ready", "verified", "review_ready"]) {
    manifest = transitionRun(manifest, stage, {now: NOW});
  }
  assert.throws(
    () => transitionRun(manifest, "exported", {now: NOW}),
    (error) => error.code === "RUN_EXPORT_APPROVAL_REQUIRED",
  );
  manifest = authorizeExport(manifest, {
    fingerprints: fingerprints(manifest.project.timelineRevision),
    scope: ["logical:timeline-current"],
    now: NOW,
  });
  assert.equal(transitionRun(manifest, "exported", {now: NOW}).status, "exported");
});

test("增强项需要当前 revision 的分项批准", () => {
  let manifest = approveSample(manifestAtSample(), {
    fingerprints: fingerprints(),
    scope: ["logical:sample-opening"],
    now: NOW,
  });
  for (const stage of ["full_aroll_applied", "captions_audio_ready"]) {
    manifest = transitionRun(manifest, stage, {now: NOW});
  }
  assert.throws(
    () => transitionRun(manifest, "enhancements_ready", {now: NOW}),
    (error) => error.code === "RUN_ENHANCEMENT_APPROVAL_REQUIRED",
  );
  manifest = authorizeEnhancements(manifest, {
    fingerprints: fingerprints(manifest.project.timelineRevision),
    scope: ["logical:music"],
    now: NOW,
  });
  assert.equal(transitionRun(manifest, "enhancements_ready", {now: NOW}).stage, "enhancements_ready");
});

test("同类失败第三次触发止损且计数封顶", () => {
  let manifest = manifestAtSample();
  let outcome;
  for (let attempt = 1; attempt <= 4; attempt += 1) {
    outcome = registerFailure(manifest, "WRITE_TIMEOUT", NOW);
    manifest = outcome.manifest;
    assert.equal(outcome.stop, attempt >= 3);
  }
  assert.equal(outcome.count, 3);
  assert.equal(outcome.action, "return_to_last_checkpoint");
});

test("相同时间戳的 checkpoint 仍按序号确定性选择最新一项", () => {
  const latest = latestCheckpoint([
    {checkpointId: "cp-sample-ready-001", createdAt: NOW},
    {checkpointId: "cp-review-ready-002", createdAt: NOW},
  ]);
  assert.equal(latest.checkpointId, "cp-review-ready-002");
});

test("三轮同类失败后 resume 强制人工交接", () => {
  const blocked = blockRun(manifestAtSample(), {
    code: "TRANSIENT_FAILURE",
    message: "still failing",
    now: NOW,
  });
  blocked.failureCounts.WRITE_TIMEOUT = 3;
  assert.throws(
    () => resumeRun(blocked, {currentTimelineRevision: "rev-current", now: NOW}),
    (error) => error.code === "RUN_RETRY_LIMIT_REACHED",
  );
});
