import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  PREVIEW_INVALIDATION_FIELDS,
  auditPreviewBundle,
  contentHash,
  createPreviewBundle,
  evaluatePreviewApproval,
} from "../src/planning/preview-approval.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts/validate-preview-approval.mjs");

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

function fixture() {
  return {
    previewBundle: readJson(
      "fixtures/preview/valid/preview-bundle.json",
    ),
    approvalLog: readJson("fixtures/preview/valid/approval-log.json"),
  };
}

function evaluate(previewBundle, approvalLog, overrides = {}) {
  return evaluatePreviewApproval({
    previewBundle,
    approvalLog,
    currentPlanHash:
      overrides.currentPlanHash ?? previewBundle.planHash,
    currentStyleFingerprint:
      overrides.currentStyleFingerprint ?? previewBundle.styleFingerprint,
    currentTimelineRevision:
      overrides.currentTimelineRevision ?? previewBundle.timelineRevision,
  });
}

test("preview selector covers opening, complex, privacy, and ending windows", () => {
  const project = readJson("fixtures/plan-bundles/valid/project.json");
  const statePlan = readJson("fixtures/plan-bundles/valid/state-plan.json");
  const previewBundle = createPreviewBundle({
    project,
    statePlan,
    planHash: contentHash({project, statePlan}),
    styleFingerprint: contentHash({
      themeId: "theme_demo",
      layoutRevision: "rev_demo",
    }),
  });
  assert.deepEqual(
    new Set(previewBundle.windows.map((item) => item.reason)),
    new Set([
      "opening-60s",
      "complex-operation",
      "privacy-risk",
      "ending",
    ]),
  );
  assert.equal(
    previewBundle.windows.find(
      (item) => item.reason === "complex-operation",
    ).subjectRefs[0],
    "state_002",
  );
  assert.deepEqual(auditPreviewBundle(previewBundle), []);
});

test("an exact approved scope opens the execution gate", () => {
  const {previewBundle, approvalLog} = fixture();
  const report = evaluate(previewBundle, approvalLog);
  assert.equal(report.status, "open");
  assert.equal(report.canExecute, true);
  assert.equal(report.approvalId, "approval_preview_001");
});

test("missing approval keeps execution closed", () => {
  const {previewBundle, approvalLog} = fixture();
  approvalLog.events = [];
  const report = evaluate(previewBundle, approvalLog);
  assert.equal(report.canExecute, false);
  assert.deepEqual(report.reasons, ["PREVIEW_APPROVAL_MISSING"]);
});

test("plan, style, and timeline changes invalidate approval independently", () => {
  const {previewBundle, approvalLog} = fixture();
  const cases = [
    ["currentPlanHash", `sha256:${"1".repeat(64)}`, "PREVIEW_PLAN_CHANGED"],
    [
      "currentStyleFingerprint",
      `sha256:${"2".repeat(64)}`,
      "PREVIEW_STYLE_CHANGED",
    ],
    ["currentTimelineRevision", "rev_changed", "PREVIEW_TIMELINE_CHANGED"],
  ];
  for (const [field, value, code] of cases) {
    const report = evaluate(previewBundle, approvalLog, {[field]: value});
    assert.equal(report.canExecute, false);
    assert.ok(report.reasons.includes(code));
  }
});

test("partial approval scope and missing invalidators fail closed", () => {
  const {previewBundle, approvalLog} = fixture();
  approvalLog.events[0].scope.windowIds.pop();
  approvalLog.events[0].invalidatesOn = PREVIEW_INVALIDATION_FIELDS.slice(1);
  const report = evaluate(previewBundle, approvalLog);
  assert.equal(report.canExecute, false);
  assert.ok(report.reasons.includes("PREVIEW_APPROVAL_SCOPE_MISMATCH"));
});

test("a later rejection or revocation supersedes an approval", () => {
  const {previewBundle, approvalLog} = fixture();
  for (const decision of ["rejected", "revoked"]) {
    const event = structuredClone(approvalLog.events[0]);
    event.eventId = `event_preview_${decision}`;
    event.approvalId = `approval_preview_${decision}`;
    event.decision = decision;
    event.recordedAt = "2026-07-24T12:01:00Z";
    const report = evaluate(
      previewBundle,
      {...approvalLog, events: [...approvalLog.events, event]},
    );
    assert.equal(report.canExecute, false);
    assert.ok(report.reasons.includes(
      decision === "revoked"
        ? "PREVIEW_APPROVAL_REVOKED"
        : "PREVIEW_APPROVAL_REJECTED",
    ));
  }
});

test("missing representative windows and out-of-range windows are audited", () => {
  const {previewBundle} = fixture();
  previewBundle.windows = previewBundle.windows.filter(
    (item) => item.reason !== "privacy-risk",
  );
  previewBundle.windows[0].range.end =
    previewBundle.timelineRange.end + 1;
  const codes = new Set(
    auditPreviewBundle(previewBundle).map((item) => item.code),
  );
  assert.ok(codes.has("PREVIEW_REQUIRED_REASON_MISSING"));
  assert.ok(codes.has("PREVIEW_WINDOW_OUTSIDE_TIMELINE"));
});

test("preview approval CLI opens only for the current exact fingerprints", () => {
  const {previewBundle} = fixture();
  const baseArguments = [
    CLI,
    "--preview",
    "fixtures/preview/valid/preview-bundle.json",
    "--approval-log",
    "fixtures/preview/valid/approval-log.json",
    "--plan-hash",
    previewBundle.planHash,
    "--style-fingerprint",
    previewBundle.styleFingerprint,
    "--timeline-revision",
    previewBundle.timelineRevision,
    "--format",
    "json",
  ];
  const open = spawnSync(process.execPath, baseArguments, {
    cwd: ROOT,
    encoding: "utf8",
  });
  assert.equal(open.status, 0, open.stderr);
  assert.equal(JSON.parse(open.stdout).status, "open");

  const changed = [...baseArguments];
  changed[changed.indexOf("--style-fingerprint") + 1] =
    `sha256:${"9".repeat(64)}`;
  const closed = spawnSync(process.execPath, changed, {
    cwd: ROOT,
    encoding: "utf8",
  });
  assert.equal(closed.status, 1);
  assert.ok(
    JSON.parse(closed.stdout).reasons.includes("PREVIEW_STYLE_CHANGED"),
  );
});

test("preview approval CLI rejects ambiguous paths without disclosure", (t) => {
  const directory = fs.mkdtempSync(
    path.join(os.tmpdir(), "koubo-preview-private-"),
  );
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  const result = spawnSync(process.execPath, [
    CLI,
    "--root",
    directory,
    "--preview=preview.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 2);
  assert.doesNotMatch(result.stderr, new RegExp(
    directory.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});
