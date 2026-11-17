import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  auditMediaRelease,
  buildInspectionSchedule,
} from "../src/qa/media-release-audit.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts/validate-media-release.mjs");

function report() {
  return JSON.parse(fs.readFileSync(
    path.join(ROOT, "fixtures/media-qa/valid/release-report.json"),
    "utf8",
  ));
}

function codes(result) {
  return new Set(result.findings.map((item) => item.code));
}

test("canonical final artifact release report passes", () => {
  const result = auditMediaRelease(report());
  assert.equal(result.status, "passed", JSON.stringify(result.findings));
  assert.deepEqual(result.summary, {
    samples: 7,
    privacyRisks: 1,
    errors: 0,
  });
});

test("inspection schedule is deterministic around boundaries and risks", () => {
  const document = report();
  const first = buildInspectionSchedule({
    duration: document.actualProbe.duration,
    boundaries: document.inspection.boundaries,
    privacyRisks: document.privacy.risks,
  });
  const second = buildInspectionSchedule({
    duration: document.actualProbe.duration,
    boundaries: [...document.inspection.boundaries].reverse(),
    privacyRisks: [...document.privacy.risks].reverse(),
  });
  assert.deepEqual(first, second);
  assert.deepEqual(
    first.map((item) => item.position),
    [0, 89, 90, 91, 104, 119, 179],
  );
});

test("probe, loudness, true peak, and anomaly limits fail closed", () => {
  const document = report();
  document.actualProbe.width = 720;
  document.audioAnalysis.integratedLufs = -20;
  document.audioAnalysis.truePeakDbtp = 0;
  document.audioAnalysis.silenceSegments[0].end = 100;
  document.visualAnalysis.blackSegments.push({
    ...structuredClone(document.actualProbe.duration),
    start: 10,
    end: 20,
  });
  document.visualAnalysis.freezeSegments.push({
    ...structuredClone(document.actualProbe.duration),
    start: 20,
    end: 100,
  });
  document.status = "failed";
  const resultCodes = codes(auditMediaRelease(document));
  for (const code of [
    "MEDIA_PROBE_MISMATCH",
    "MEDIA_LOUDNESS_OUT_OF_RANGE",
    "MEDIA_TRUE_PEAK_EXCEEDED",
    "MEDIA_SILENCE_TOO_LONG",
    "MEDIA_BLACK_TOO_LONG",
    "MEDIA_FREEZE_TOO_LONG",
  ]) {
    assert.ok(resultCodes.has(code), code);
  }
});

test("critical privacy ranges require complete treatment coverage", () => {
  const document = report();
  document.privacy.treatments[0].range.end = 110;
  document.status = "failed";
  assert.ok(codes(auditMediaRelease(document)).has(
    "MEDIA_PRIVACY_COVERAGE_MISSING",
  ));
});

test("inspection drift and export authorization mismatch block release", () => {
  const document = report();
  document.inspection.samples[0].position = 1;
  document.exportAuthorization.artifactHash =
    `sha256:${"d".repeat(64)}`;
  document.status = "failed";
  const resultCodes = codes(auditMediaRelease(document));
  assert.ok(resultCodes.has("MEDIA_INSPECTION_SCHEDULE_DRIFT"));
  assert.ok(resultCodes.has("MEDIA_EXPORT_AUTHORIZATION_MISMATCH"));
});

test("a false passed claim is itself a release failure", () => {
  const document = report();
  document.audioAnalysis.integratedLufs = -30;
  const resultCodes = codes(auditMediaRelease(document));
  assert.ok(resultCodes.has("MEDIA_LOUDNESS_OUT_OF_RANGE"));
  assert.ok(resultCodes.has("MEDIA_STATUS_CLAIM_MISMATCH"));
});

test("media release CLI validates the canonical fixture", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--report",
    "fixtures/media-qa/valid/release-report.json",
    "--format",
    "json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).status, "passed");
});

test("media release CLI rejects ambiguous options without path disclosure", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--report=fixtures/media-qa/valid/release-report.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 2);
  assert.doesNotMatch(result.stderr, new RegExp(
    ROOT.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});
