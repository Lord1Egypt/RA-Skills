import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  auditFeedbackEvent,
  auditSuggestedUpdateQueue,
  createSuggestedUpdate,
} from "../src/governance/feedback-governance.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts/validate-feedback-governance.mjs");

function fixture(relativePath) {
  return JSON.parse(fs.readFileSync(
    path.join(ROOT, relativePath),
    "utf8",
  ));
}

function registry() {
  return fixture("rules/registry.json");
}

function event() {
  return fixture("fixtures/feedback/valid/event.json");
}

function queue() {
  return fixture(
    "fixtures/feedback/valid/suggestion-queue.json",
  );
}

test("anonymous feedback event and governed queue pass", () => {
  assert.equal(
    auditFeedbackEvent(event(), registry()).status,
    "passed",
  );
  const report = auditSuggestedUpdateQueue(queue(), registry());
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
  assert.deepEqual(report.summary, {
    suggestions: 1,
    released: 0,
    errors: 0,
  });
});

test("feedback event rejects content-bearing fields and user paths", () => {
  const document = event();
  document.captionText = "private words";
  document.debug = "/Users/example/private/project";
  const codes = new Set(
    auditFeedbackEvent(document, registry()).findings.map(
      (item) => item.code,
    ),
  );
  assert.ok(codes.has("FEEDBACK_CONTENT_FIELD_FORBIDDEN"));
  assert.ok(codes.has("FEEDBACK_ABSOLUTE_PATH_FORBIDDEN"));
});

test("failure events require stable signatures", () => {
  const document = event();
  document.eventType = "failure";
  assert.ok(
    auditFeedbackEvent(document, registry()).findings.some(
      (item) =>
        item.code === "FEEDBACK_FAILURE_SIGNATURE_REQUIRED",
    ),
  );
});

test("promotion requires repeated samples, evidence, and counterexamples", () => {
  const document = queue();
  const suggestion = document.suggestions[0];
  suggestion.status = "approved";
  suggestion.sampleCount = 1;
  suggestion.sampleRefs = suggestion.sampleRefs.slice(0, 1);
  suggestion.evidenceRefs = [];
  suggestion.counterexampleRefs = [];
  delete suggestion.reviewerId;
  const codes = new Set(
    auditSuggestedUpdateQueue(document, registry()).findings.map(
      (item) => item.code,
    ),
  );
  assert.ok(codes.has("FEEDBACK_REPEATED_SAMPLES_REQUIRED"));
  assert.ok(codes.has("FEEDBACK_REVIEW_EVIDENCE_REQUIRED"));
});

test("released hard policy requires a human release and version increase", () => {
  const document = queue();
  const suggestion = document.suggestions[0];
  suggestion.targetType = "rule";
  suggestion.targetRef = "CAPTION-MIN-DURATION";
  suggestion.status = "released";
  suggestion.reviewerId = "reviewer_policy_owner";
  let report = auditSuggestedUpdateQueue(document, registry());
  assert.ok(report.findings.some(
    (item) => item.code === "FEEDBACK_RELEASE_RECORD_INVALID",
  ));
  assert.ok(report.findings.some(
    (item) => item.code === "FEEDBACK_HARD_POLICY_RELEASE_FORBIDDEN",
  ));

  suggestion.releaseRecord = {
    releasedAt: "2026-07-24T10:00:00Z",
    reviewerId: "reviewer_policy_owner",
    versionBefore: "1.1.0",
    versionAfter: "1.2.0",
    changeRef: "CHANGELOG.md#unreleased",
  };
  report = auditSuggestedUpdateQueue(document, registry());
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
});

test("a release record cannot appear before release", () => {
  const document = queue();
  document.suggestions[0].releaseRecord = {
    releasedAt: "2026-07-24T10:00:00Z",
    reviewerId: "reviewer_policy_owner",
    versionBefore: "1.1.0",
    versionAfter: "1.2.0",
    changeRef: "CHANGELOG.md#unreleased",
  };
  assert.ok(
    auditSuggestedUpdateQueue(document, registry()).findings.some(
      (item) => item.code === "FEEDBACK_RELEASE_RECORD_PREMATURE",
    ),
  );
});

test("suggestion creation is deterministic and never mutates a registry", () => {
  const policyRegistry = registry();
  const before = JSON.stringify(policyRegistry);
  const events = [
    event(),
    {
      ...event(),
      eventRefHash: `sha256:${"2".repeat(64)}`,
    },
    event(),
  ];
  const suggestion = createSuggestedUpdate({
    suggestionId: "suggestion_caption_001",
    targetType: "rule",
    targetRef: "CAPTION-MIN-DURATION",
    proposedAdjustment: {
      field: "canonical.value",
      operation: "increase",
      value: 500,
    },
    events,
    ownerId: "owner_caption_policy",
    rollback: {
      strategy: "previous-version",
      reference: "rules/policy.json",
    },
  });
  assert.equal(suggestion.status, "suggested");
  assert.equal(suggestion.sampleCount, 2);
  assert.deepEqual(suggestion.evidenceRefs, []);
  assert.equal(JSON.stringify(policyRegistry), before);
});

test("feedback CLI validates only root-bounded explicit inputs", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--event",
    "fixtures/feedback/valid/event.json",
    "--queue",
    "fixtures/feedback/valid/suggestion-queue.json",
    "--format",
    "json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).status, "passed");

  const unsafe = spawnSync(process.execPath, [
    CLI,
    "--event",
    "../event.json",
    "--queue",
    "fixtures/feedback/valid/suggestion-queue.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(unsafe.status, 1);
  assert.match(unsafe.stderr, /^FEEDBACK_PATH_UNSAFE:/u);
  assert.doesNotMatch(unsafe.stderr, new RegExp(
    ROOT.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});
