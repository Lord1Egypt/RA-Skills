import assert from "node:assert/strict";
import test from "node:test";

import {
  assertEvidenceClaims,
  buildHandoffReport,
  renderHandoffMarkdown,
} from "../src/orchestration/handoff-reporter.mjs";
import {createSampleFingerprint} from "../src/orchestration/preview-selector.mjs";
import {selectProfile} from "../src/orchestration/profile-selector.mjs";
import {contentHash} from "../src/planning/preview-approval.mjs";
import {
  approveSample,
  authorizeExport,
  blockRun,
  createRunManifest,
  createSampleBinding,
  transitionRun,
} from "../src/orchestration/run-state.mjs";

const NOW = "2026-08-10T00:00:00Z";

function fingerprints(revision = "rev-current") {
  return createSampleFingerprint({
    plan: [],
    style: {},
    layout: {},
    captions: {},
    timelineRevision: revision,
    windows: [{windowRef: "logical:sample-opening", startSec: 0, endSec: 30}],
  });
}

function evidence(kind, ref, revision = "rev-current") {
  return {
    ref,
    kind,
    hash: contentHash({kind, ref, revision}),
    revision,
    provenance: "simulation",
    capturedAt: NOW,
  };
}

function manifestAt(stage = "preflight") {
  let manifest = createRunManifest({
    runId: `run-handoff-${stage.replaceAll("_", "-")}`,
    profile: selectProfile(),
    projectRef: "logical:project-current",
    timelineRef: "logical:timeline-current",
    timelineRevision: "rev-current",
    now: NOW,
  });
  if (stage === "preflight") return manifest;
  const order = ["brief_ready", "project_ready", "transcript_ready", "edit_plan_ready", "sample_ready"];
  for (const next of order) {
    manifest = transitionRun(manifest, next, {
      now: NOW,
      ...(next === "sample_ready"
        ? {sampleBinding: createSampleBinding({fingerprints: fingerprints(), scope: ["logical:sample-opening"], now: NOW})}
        : {}),
    });
    if (next === stage) return manifest;
  }
  if (stage === "sample_ready") return manifest;
  const sampleFingerprints = fingerprints();
  manifest = approveSample(manifest, {fingerprints: sampleFingerprints, scope: ["logical:sample-opening"], now: NOW});
  if (stage === "sample_approved") return manifest;
  for (const next of ["full_aroll_applied", "captions_audio_ready", "verified", "review_ready"]) {
    manifest = transitionRun(manifest, next, {now: NOW});
    if (next === stage) return manifest;
  }
  if (stage === "exported") {
    manifest = authorizeExport(manifest, {fingerprints: sampleFingerprints, scope: ["logical:timeline-current"], now: NOW});
    return transitionRun(manifest, "exported", {now: NOW});
  }
  return manifest;
}

test("未到交付阶段的 report 明确为 in_progress", () => {
  assert.equal(buildHandoffReport({manifest: manifestAt(), now: NOW}).deliveryState, "in_progress");
  assert.equal(buildHandoffReport({manifest: manifestAt("sample_approved"), now: NOW}).deliveryState, "in_progress");
});

test("sample、review、blocked 和 exported 映射为对应交付态", () => {
  assert.equal(buildHandoffReport({manifest: manifestAt("sample_ready"), now: NOW}).deliveryState, "sample_ready");
  assert.equal(buildHandoffReport({manifest: manifestAt("review_ready"), now: NOW}).deliveryState, "review_ready");
  const blocked = blockRun(manifestAt("project_ready"), {code: "TRANSCRIPT_PENDING", message: "still pending", now: NOW});
  assert.equal(buildHandoffReport({manifest: blocked, now: NOW}).deliveryState, "blocked");
  assert.equal(buildHandoffReport({manifest: manifestAt("exported"), now: NOW}).deliveryState, "exported");
});

test("结构、画面、测量、试听和批准状态不会互相冒充", () => {
  const report = buildHandoffReport({
    manifest: manifestAt("review_ready"),
    verification: {
      structure: "pass",
      visual: "unverified",
      audioMeasurement: "pass",
      humanListening: "unverified",
      sampleApproval: "pass",
      finalReviewApproval: "pending",
      privacy: "pass",
    },
    evidence: [
      evidence("structure-readback", "logical:structure-readback"),
      evidence("audio-measurement", "logical:audio-measurement"),
      evidence("sample-approval", "logical:sample-approval"),
      evidence("privacy-review", "logical:privacy-review"),
    ],
    now: NOW,
  });
  assert.equal(assertEvidenceClaims(report), true);
  assert.equal(report.verification.structure, "pass");
  assert.equal(report.verification.visual, "unverified");
  assert.equal(report.verification.humanListening, "unverified");
});

test("visual PASS 必须有结构化 composed-frame evidence", () => {
  const report = buildHandoffReport({
    manifest: manifestAt("review_ready"),
    verification: {visual: "pass"},
    evidence: [{...evidence("structure-readback", "logical:not-a-frame-proof")}],
    now: NOW,
  });
  assert.throws(() => assertEvidenceClaims(report), /HANDOFF_VISUAL_EVIDENCE_MISSING/u);
  const valid = buildHandoffReport({
    manifest: manifestAt("review_ready"),
    verification: {visual: "pass"},
    evidence: [evidence("composed-frame", "logical:frame-final")],
    now: NOW,
  });
  assert.equal(assertEvidenceClaims(valid), true);
});

test("human listening PASS 必须有 listening evidence", () => {
  const report = buildHandoffReport({
    manifest: manifestAt("review_ready"),
    verification: {humanListening: "pass"},
    evidence: [evidence("audio-measurement", "logical:audio-measurement")],
    now: NOW,
  });
  assert.throws(() => assertEvidenceClaims(report), /HANDOFF_HUMAN_LISTENING_EVIDENCE_MISSING/u);
  const valid = buildHandoffReport({
    manifest: manifestAt("review_ready"),
    verification: {humanListening: "pass"},
    evidence: [evidence("human-listening", "logical:listening-review")],
    now: NOW,
  });
  assert.equal(assertEvidenceClaims(valid), true);
});

test("Markdown 交付报告列出未执行与 UNVERIFIED", () => {
  const report = buildHandoffReport({manifest: manifestAt("review_ready"), now: NOW});
  const markdown = renderHandoffMarkdown(report);
  assert.match(markdown, /^# 稳剪交付报告/mu);
  assert.match(markdown, /export/u);
  assert.match(markdown, /UNVERIFIED/u);
  assert.match(markdown, /PENDING/u);
});
