const LOW_RISK_TYPES = new Set([
  "head-tail-silence",
  "hesitation",
  "false-start",
  "covered-restart",
  "duplicate-dialogue",
  "smooth-audio",
]);
const MEDIUM_RISK_TYPES = new Set([
  "filler",
  "partial-retake",
  "caption-display",
  "transcript-repair",
  "intro",
  "pause",
]);
const HIGH_RISK_TYPES = new Set([
  "whole-sentence",
  "numeric-content",
  "proper-noun",
  "negation",
  "restructure",
  "hook-forward",
  "take-selection",
  "portrait-reframe",
  "privacy",
  "protected-baseline",
  "generated-content",
  "spoken-replacement",
  "export",
  "publish",
]);
const KNOWN_RISK_TYPES = new Set([
  ...LOW_RISK_TYPES,
  ...MEDIUM_RISK_TYPES,
  ...HIGH_RISK_TYPES,
]);

export class RiskPolicyError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "RiskPolicyError";
    this.code = code;
  }
}

export function classifyRisk(candidate = {}) {
  const type = candidate.type ?? candidate.category;
  if (!KNOWN_RISK_TYPES.has(type)) {
    throw new RiskPolicyError("RISK_TYPE_UNKNOWN", "decision type is not recognized");
  }
  if (HIGH_RISK_TYPES.has(type) || candidate.affectsNumber || candidate.affectsProperNoun || candidate.affectsNegation || candidate.removesWholeSentence || candidate.affectsPrivacy || candidate.changesProtectedBaseline) {
    return "high";
  }
  if (LOW_RISK_TYPES.has(type) && candidate.evidenceRefs?.length > 0) {
    return "low";
  }
  if (LOW_RISK_TYPES.has(type)) return "medium";
  if (MEDIUM_RISK_TYPES.has(type)) return "medium";
  throw new RiskPolicyError("RISK_TYPE_UNKNOWN", "decision type is not recognized");
}

export function normalizeDecision(candidate, index = 0) {
  const risk = classifyRisk(candidate);
  return {
    decisionId: candidate.decisionId ?? `dec-${String(index + 1).padStart(3, "0")}`,
    type: candidate.type ?? candidate.category,
    risk,
    action: candidate.action,
    spokenExcerpt: candidate.spokenExcerpt,
    resultExcerpt: candidate.resultExcerpt,
    reason: candidate.reason,
    evidenceRefs: [...(candidate.evidenceRefs ?? [])],
    status: candidate.status ?? "proposed",
    approvalRequired: risk !== "low",
    approvalRef: candidate.approvalRef ?? null,
  };
}

function approvalFor(decision, {approvals = [], timelineRevision = null} = {}) {
  if (!decision.approvalRef) return null;
  const approval = approvals.find((item) => item.approvalRef === decision.approvalRef);
  if (!approval || approval.status !== "approved") return null;
  if (timelineRevision && approval.fingerprints?.timelineRevision !== timelineRevision) return null;
  const expectedKind = decision.risk === "high" ? "decision" : "sample";
  if (approval.kind !== expectedKind) return null;
  const decisionScope = `logical:decision-${decision.decisionId}`;
  if (!approval.scope?.includes(decisionScope)) return null;
  return approval;
}

export function assertDecisionCanApply(decision, context = {}) {
  if (!decision.reason || decision.evidenceRefs?.length === 0) {
    throw new RiskPolicyError("RISK_EVIDENCE_MISSING", "applied decisions require a reason and evidence");
  }
  if (decision.risk === "high" && !approvalFor(decision, context)) {
    throw new RiskPolicyError("RISK_HIGH_APPROVAL_REQUIRED", "high-risk decisions require explicit approval");
  }
  if (decision.risk === "medium" && !approvalFor(decision, context)) {
    throw new RiskPolicyError("RISK_SAMPLE_APPROVAL_REQUIRED", "medium-risk decisions require sample approval");
  }
  return true;
}

export function auditDecisionLog(log, context = {}) {
  const findings = [];
  for (const [index, decision] of (log?.decisions ?? []).entries()) {
    let expected;
    try {
      expected = classifyRisk(decision);
    } catch (error) {
      findings.push({code: error.code ?? "RISK_TYPE_UNKNOWN", index});
      continue;
    }
    if (decision.risk !== expected || decision.approvalRequired !== (expected !== "low")) {
      findings.push({code: "RISK_CLASSIFICATION_DRIFT", index});
    }
    if (decision.status === "applied") {
      try {
        assertDecisionCanApply(decision, context);
      } catch (error) {
        findings.push({code: error.code ?? "RISK_APPLY_BLOCKED", index});
      }
    }
  }
  return findings;
}

export function decisionSummaryForUser(decision) {
  return {
    before: decision.spokenExcerpt,
    after: decision.resultExcerpt,
    reason: decision.reason,
    state: decision.status,
    needsApproval: decision.approvalRequired,
  };
}
