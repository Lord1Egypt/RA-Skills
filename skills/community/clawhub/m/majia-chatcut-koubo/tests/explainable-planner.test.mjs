import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  auditExplainableScorecard,
  buildExplainableScorecard,
} from "../src/planning/explainable-planner.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(
  ROOT,
  "scripts/validate-explainable-planner.mjs",
);

function fixture(relativePath) {
  return JSON.parse(fs.readFileSync(
    path.join(ROOT, relativePath),
    "utf8",
  ));
}

function inputs() {
  return {
    transcript: fixture(
      "fixtures/plan-bundles/valid/transcript.json",
    ),
    editPlan: fixture(
      "fixtures/plan-bundles/valid/edit-plan.json",
    ),
  };
}

test("canonical scorecard is fully reproducible from IR references", () => {
  const {transcript, editPlan} = inputs();
  const expected = fixture(
    "fixtures/planning/valid/content-scorecard.json",
  );
  const generated = buildExplainableScorecard(
    transcript,
    editPlan,
    {scorecardId: expected.scorecardId},
  );
  assert.deepEqual(generated, expected);
  assert.equal(
    auditExplainableScorecard(expected, transcript, editPlan).status,
    "passed",
  );
});

test("planner reports structural signals without a black-box score", () => {
  const {transcript, editPlan} = inputs();
  const scorecard = buildExplainableScorecard(transcript, editPlan);
  const byKind = new Map(
    scorecard.signals.map((item) => [item.kind, item]),
  );
  assert.equal(byKind.get("opening-density").value, 1);
  assert.equal(byKind.get("evidence-coverage").value, 1);
  assert.equal(scorecard.predictionPolicy.viralityProbability, "not-produced");
  assert.equal(scorecard.predictionPolicy.generatedText, false);
  assert.equal("score" in scorecard, false);
  assert.equal("probability" in scorecard, false);
});

test("narrative suggestions reuse source references and stay pending", () => {
  const {transcript, editPlan} = inputs();
  const scorecard = buildExplainableScorecard(transcript, editPlan);
  const sourceTexts = new Set(
    transcript.words.map((word) => word.sourceText),
  );
  for (const candidate of scorecard.narrativeCandidates) {
    assert.equal(candidate.inventedContent, false);
    assert.equal(candidate.approval.status, "pending");
    assert.equal(candidate.approval.required, true);
    assert.equal("text" in candidate, false);
    assert.ok(candidate.sourceWordIds.every(
      (wordId) => transcript.words.some((word) => word.wordId === wordId),
    ));
  }
  assert.ok(sourceTexts.size > 0);
});

test("low confidence, content risk, and destructive edits enter decisions", () => {
  const {transcript, editPlan} = inputs();
  transcript.words[0].confidence = 0.5;
  transcript.words[0].riskFlags = ["number"];
  editPlan.segments[0].action = "remove";
  editPlan.segments[0].risk = "high";
  editPlan.segments[0].approval = {
    required: true,
    status: "pending",
  };
  const scorecard = buildExplainableScorecard(transcript, editPlan);
  const kinds = new Set(scorecard.decisionQueue.map((item) => item.kind));
  assert.ok(kinds.has("low-confidence"));
  assert.ok(kinds.has("content-risk"));
  assert.ok(kinds.has("destructive-edit"));
  assert.equal(scorecard.narrativeCandidates.length, 0);
});

test("revision drift stops planning before producing suggestions", () => {
  const {transcript, editPlan} = inputs();
  editPlan.transcriptRevision = `sha256:${"f".repeat(64)}`;
  assert.throws(
    () => buildExplainableScorecard(transcript, editPlan),
    /revisions do not match/u,
  );
});

test("scorecard drift is a stable machine finding", () => {
  const {transcript, editPlan} = inputs();
  const scorecard = buildExplainableScorecard(transcript, editPlan);
  scorecard.signals[0].value = 999;
  const report = auditExplainableScorecard(
    scorecard,
    transcript,
    editPlan,
  );
  assert.equal(report.status, "failed");
  assert.equal(report.findings[0].code, "PLANNER_SCORECARD_DRIFT");
});

test("planner CLI validates explicit root-bounded fixtures", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--transcript",
    "fixtures/plan-bundles/valid/transcript.json",
    "--edit-plan",
    "fixtures/plan-bundles/valid/edit-plan.json",
    "--expected",
    "fixtures/planning/valid/content-scorecard.json",
    "--format",
    "json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).status, "passed");

  const unsafe = spawnSync(process.execPath, [
    CLI,
    "--transcript=fixtures/plan-bundles/valid/transcript.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(unsafe.status, 2);
  assert.doesNotMatch(unsafe.stderr, new RegExp(
    ROOT.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});
