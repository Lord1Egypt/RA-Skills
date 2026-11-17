import assert from "node:assert/strict";
import test from "node:test";

import {
  assertDecisionCanApply,
  auditDecisionLog,
  classifyRisk,
  decisionSummaryForUser,
  normalizeDecision,
  RiskPolicyError,
} from "../src/orchestration/risk-classifier.mjs";

function candidate(overrides = {}) {
  return {
    type: "false-start",
    action: "remove-false-start",
    spokenExcerpt: "数、数据",
    resultExcerpt: "数据",
    reason: "词头卡壳，后接完整词",
    evidenceRefs: ["logical:word-range-001"],
    status: "applied",
    ...overrides,
  };
}

test("低风险自动化必须有 evidence，否则降为中风险", () => {
  assert.equal(classifyRisk(candidate()), "low");
  assert.equal(classifyRisk(candidate({evidenceRefs: []})), "medium");
});

test("数字、专名、否定、整句、重排和隐私始终高风险", () => {
  for (const type of ["numeric-content", "proper-noun", "negation", "whole-sentence", "restructure", "privacy"] ) {
    assert.equal(classifyRisk(candidate({type})), "high", type);
  }
  assert.equal(classifyRisk(candidate({type: "false-start", affectsNumber: true})), "high");
});

test("未知类型不会被静默自动执行", () => {
  assert.throws(
    () => classifyRisk({type: "delete-everything"}),
    (error) => error instanceof RiskPolicyError && error.code === "RISK_TYPE_UNKNOWN",
  );
});

test("applied 决策必须有理由和证据", () => {
  const decision = normalizeDecision(candidate());
  assert.equal(assertDecisionCanApply(decision), true);
  assert.throws(
    () => assertDecisionCanApply({...decision, evidenceRefs: []}),
    (error) => error.code === "RISK_EVIDENCE_MISSING",
  );
});

test("中高风险 applied 决策必须绑定相应批准", () => {
  const medium = normalizeDecision(candidate({type: "pause"}));
  assert.throws(
    () => assertDecisionCanApply(medium),
    (error) => error.code === "RISK_SAMPLE_APPROVAL_REQUIRED",
  );
  const mediumApproved = {...medium, approvalRef: "logical:sample-approval"};
  assert.equal(assertDecisionCanApply(mediumApproved, {
    timelineRevision: "rev-current",
    approvals: [{
      approvalRef: "logical:sample-approval",
      kind: "sample",
      status: "approved",
      fingerprints: {timelineRevision: "rev-current"},
      scope: [`logical:decision-${medium.decisionId}`],
    }],
  }), true);

  const high = normalizeDecision(candidate({type: "numeric-content"}));
  assert.throws(
    () => assertDecisionCanApply(high),
    (error) => error.code === "RISK_HIGH_APPROVAL_REQUIRED",
  );
  const highApproved = {...high, approvalRef: "logical:explicit-approval"};
  assert.throws(
    () => assertDecisionCanApply(highApproved, {approvals: []}),
    (error) => error.code === "RISK_HIGH_APPROVAL_REQUIRED",
  );
  assert.equal(assertDecisionCanApply(highApproved, {
    timelineRevision: "rev-current",
    approvals: [{
      approvalRef: "logical:explicit-approval",
      kind: "decision",
      status: "approved",
      fingerprints: {timelineRevision: "rev-current"},
      scope: [`logical:decision-${high.decisionId}`],
    }],
  }), true);
});

test("审计能发现分类漂移和无批准应用", () => {
  const low = normalizeDecision(candidate());
  const high = normalizeDecision(candidate({type: "whole-sentence"}), 1);
  const findings = auditDecisionLog({decisions: [{...low, risk: "medium", status: "proposed"}, high]});
  assert.deepEqual(findings.map((item) => item.code), [
    "RISK_CLASSIFICATION_DRIFT",
    "RISK_HIGH_APPROVAL_REQUIRED",
  ]);
});

test("用户摘要不暴露 decision ID、evidence 或内部引用", () => {
  const normalized = normalizeDecision(candidate({decisionId: "dec-private"}));
  const summary = decisionSummaryForUser(normalized);
  assert.deepEqual(Object.keys(summary), ["before", "after", "reason", "state", "needsApproval"]);
  const serialized = JSON.stringify(summary);
  assert.equal(serialized.includes("dec-private"), false);
  assert.equal(serialized.includes("logical:"), false);
});
