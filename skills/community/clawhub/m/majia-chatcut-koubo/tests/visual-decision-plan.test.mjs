import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {
  auditVisualDecisionPlan,
  scoreVisualCandidate,
} from "../src/planning/visual-decision-plan.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts", "validate-visual-decision-plan.mjs");

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

function canonicalPlan() {
  return readJson("fixtures/visual-decisions/valid/plan.json");
}

function runCli(...arguments_) {
  return spawnSync(process.execPath, [CLI, ...arguments_], {
    cwd: ROOT,
    encoding: "utf8",
  });
}

test("canonical visual decision plan satisfies its release schema", () => {
  const ajv = new Ajv2020({
    allErrors: true,
    strict: true,
    strictRequired: false,
  });
  addFormats(ajv);
  ajv.addSchema(readJson("schemas/creator-os-common.schema.json"));
  const validate = ajv.compile(
    readJson("schemas/visual-decision-plan.schema.json"),
  );
  const plan = canonicalPlan();
  assert.equal(validate(plan), true, JSON.stringify(validate.errors));
});

test("canonical visual decisions are explainable and execution-safe", () => {
  const plan = canonicalPlan();
  const report = auditVisualDecisionPlan(plan);
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
  assert.equal(report.executionAllowed, true);
  assert.deepEqual(report.summary, {
    segments: 2,
    candidates: 3,
    automaticSelections: 2,
    manualReviews: 0,
    errors: 0,
  });
  assert.equal(scoreVisualCandidate(plan.segments[0].candidates[0]), 10);
});

test("automatic selection fails closed below the transparent score threshold", () => {
  const plan = canonicalPlan();
  const selected = plan.segments[0].candidates[0];
  selected.scores = {
    semanticMatch: 2,
    authenticity: 1,
    timingMatch: 1,
    visualClarity: 1,
    rightsConfidence: 1,
    notRecentlyRepeated: 0,
  };
  selected.total = 6;

  const report = auditVisualDecisionPlan(plan);
  assert.equal(report.executionAllowed, false);
  assert.deepEqual(
    report.findings.map((item) => item.code),
    [
      "VISUAL_ELIGIBLE_SCORE_BELOW_THRESHOLD",
      "VISUAL_AUTOMATIC_SCORE_BELOW_THRESHOLD",
    ],
  );
});

test("below-threshold candidates may be routed to manual review without lying", () => {
  const plan = canonicalPlan();
  const segment = plan.segments[0];
  const selected = segment.candidates[0];
  selected.scores = {
    semanticMatch: 2,
    authenticity: 1,
    timingMatch: 1,
    visualClarity: 1,
    rightsConfidence: 1,
    notRecentlyRepeated: 0,
  };
  selected.total = 6;
  selected.decision = "manual-review";
  segment.selection.mode = "manual-review";
  segment.selection.approval = {
    required: true,
    status: "pending",
    approvalId: null,
  };

  const report = auditVisualDecisionPlan(plan);
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
  assert.equal(report.executionAllowed, false);
  assert.equal(report.summary.manualReviews, 1);
});

test("generated visuals cannot impersonate evidence or data", () => {
  const plan = canonicalPlan();
  plan.segments[0].candidates[0].assetKind = "generated-illustration";
  const report = auditVisualDecisionPlan(plan);
  assert.ok(report.findings.some(
    (item) => item.code === "VISUAL_GENERATED_EVIDENCE_FORBIDDEN",
  ));
});

test("automatic selection requires source, rights, approval, and clean patterns", () => {
  const plan = canonicalPlan();
  const segment = plan.segments[0];
  const selected = segment.candidates[0];
  selected.sourceVerified = false;
  selected.sourceEvidenceRefs = [];
  selected.scores.rightsConfidence = 0;
  selected.rightsEvidenceRefs = [];
  selected.total = 9;
  segment.selection.approval.status = "pending";
  segment.selection.approval.approvalId = null;
  segment.detectedAntiPatterns = ["unrelated-broll"];

  const report = auditVisualDecisionPlan(plan);
  assert.deepEqual(
    report.findings.map((item) => item.code),
    [
      "VISUAL_ANTI_PATTERN_DETECTED",
      "VISUAL_SOURCE_EVIDENCE_REQUIRED",
      "VISUAL_RIGHTS_EVIDENCE_REQUIRED",
      "VISUAL_APPROVAL_REQUIRED",
    ],
  );
});

test("stored totals cannot drift from their auditable dimensions", () => {
  const plan = canonicalPlan();
  plan.segments[0].candidates[0].total = 9;
  const report = auditVisualDecisionPlan(plan);
  assert.equal(
    report.findings[0].code,
    "VISUAL_SCORE_TOTAL_MISMATCH",
  );
});

test("visual decision CLI validates canonical input without leaking paths", () => {
  const result = runCli(
    "--plan",
    "fixtures/visual-decisions/valid/plan.json",
    "--format",
    "json",
  );
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = JSON.parse(result.stdout);
  assert.equal(report.executionAllowed, true);
  assert.doesNotMatch(result.stdout, /\/Users\/|Obsidian/u);

  const unsafe = runCli(
    "--plan=fixtures/visual-decisions/valid/plan.json",
  );
  assert.equal(unsafe.status, 2);
  assert.match(unsafe.stderr, /^VISUAL_DECISION_USAGE:/u);
  assert.doesNotMatch(unsafe.stderr, /\/Users\/|Obsidian/u);
});
