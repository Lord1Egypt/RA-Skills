export const AUTOMATIC_SELECTION_MINIMUM = 7;

const GENERATED_ASSET_KINDS = new Set([
  "generated-illustration",
  "motion-graphic",
]);

const EVIDENCE_TASKS = new Set(["evidence", "data"]);

function finding(code, pointer) {
  return {code, pointer, severity: "error"};
}

function approvalIsValid(approval) {
  return approval?.required === true
    && approval.status === "approved"
    && typeof approval.approvalId === "string";
}

export function scoreVisualCandidate(candidate) {
  return Object.values(candidate.scores).reduce(
    (total, value) => total + value,
    0,
  );
}

function requireUnique(findings, items, key, pointer, code) {
  const seen = new Set();
  for (const [index, item] of items.entries()) {
    if (seen.has(item[key])) {
      findings.push(finding(code, `${pointer}/${index}/${key}`));
    }
    seen.add(item[key]);
  }
}

function auditCandidate(candidate, pointer, findings) {
  if (candidate.total !== scoreVisualCandidate(candidate)) {
    findings.push(finding(
      "VISUAL_SCORE_TOTAL_MISMATCH",
      `${pointer}/total`,
    ));
  }
  if (
    candidate.decision === "eligible"
    && candidate.total < AUTOMATIC_SELECTION_MINIMUM
  ) {
    findings.push(finding(
      "VISUAL_ELIGIBLE_SCORE_BELOW_THRESHOLD",
      `${pointer}/decision`,
    ));
  }
}

function auditAutomaticSelection(segment, pointer, selected, findings) {
  if (!selected) {
    findings.push(finding(
      "VISUAL_AUTOMATIC_SELECTION_MISSING",
      `${pointer}/selection/selectedCandidateId`,
    ));
    return;
  }
  if (selected.decision !== "eligible") {
    findings.push(finding(
      "VISUAL_SELECTED_CANDIDATE_NOT_ELIGIBLE",
      `${pointer}/selection/selectedCandidateId`,
    ));
  }
  if (selected.total < AUTOMATIC_SELECTION_MINIMUM) {
    findings.push(finding(
      "VISUAL_AUTOMATIC_SCORE_BELOW_THRESHOLD",
      `${pointer}/selection/selectedCandidateId`,
    ));
  }
  if (
    selected.sourceVerified !== true
    || selected.sourceEvidenceRefs.length === 0
  ) {
    findings.push(finding(
      "VISUAL_SOURCE_EVIDENCE_REQUIRED",
      `${pointer}/selection/selectedCandidateId`,
    ));
  }
  if (
    selected.scores.rightsConfidence < 1
    || selected.rightsEvidenceRefs.length === 0
  ) {
    findings.push(finding(
      "VISUAL_RIGHTS_EVIDENCE_REQUIRED",
      `${pointer}/selection/selectedCandidateId`,
    ));
  }
  if (
    EVIDENCE_TASKS.has(segment.primaryTask)
    && GENERATED_ASSET_KINDS.has(selected.assetKind)
  ) {
    findings.push(finding(
      "VISUAL_GENERATED_EVIDENCE_FORBIDDEN",
      `${pointer}/selection/selectedCandidateId`,
    ));
  }
  if (!approvalIsValid(segment.selection.approval)) {
    findings.push(finding(
      "VISUAL_APPROVAL_REQUIRED",
      `${pointer}/selection/approval`,
    ));
  }
}

export function auditVisualDecisionPlan(plan) {
  const findings = [];
  requireUnique(
    findings,
    plan.segments,
    "segmentId",
    "/segments",
    "VISUAL_SEGMENT_ID_DUPLICATE",
  );

  let candidateCount = 0;
  let automaticSelections = 0;
  let manualReviews = 0;

  for (const [segmentIndex, segment] of plan.segments.entries()) {
    const pointer = `/segments/${segmentIndex}`;
    if (segment.range.end <= segment.range.start) {
      findings.push(finding(
        "VISUAL_RANGE_EMPTY",
        `${pointer}/range`,
      ));
    }
    if (
      segment.primaryTask !== "none"
      && segment.evidenceRefs.length === 0
    ) {
      findings.push(finding(
        "VISUAL_SEMANTIC_EVIDENCE_REQUIRED",
        `${pointer}/evidenceRefs`,
      ));
    }
    requireUnique(
      findings,
      segment.candidates,
      "candidateId",
      `${pointer}/candidates`,
      "VISUAL_CANDIDATE_ID_DUPLICATE",
    );
    candidateCount += segment.candidates.length;
    for (const [candidateIndex, candidate] of segment.candidates.entries()) {
      auditCandidate(
        candidate,
        `${pointer}/candidates/${candidateIndex}`,
        findings,
      );
    }

    const selected = segment.candidates.find(
      (candidate) =>
        candidate.candidateId === segment.selection.selectedCandidateId,
    );
    if (
      segment.selection.selectedCandidateId !== null
      && !selected
    ) {
      findings.push(finding(
        "VISUAL_SELECTED_CANDIDATE_UNKNOWN",
        `${pointer}/selection/selectedCandidateId`,
      ));
    }
    if (segment.detectedAntiPatterns.length > 0) {
      findings.push(finding(
        "VISUAL_ANTI_PATTERN_DETECTED",
        `${pointer}/detectedAntiPatterns`,
      ));
    }

    if (segment.selection.mode === "automatic") {
      automaticSelections += 1;
      auditAutomaticSelection(segment, pointer, selected, findings);
    } else {
      manualReviews += 1;
      if (
        segment.selection.mode === "no-selection"
        && segment.selection.selectedCandidateId !== null
      ) {
        findings.push(finding(
          "VISUAL_NO_SELECTION_MUST_BE_EMPTY",
          `${pointer}/selection/selectedCandidateId`,
        ));
      }
    }
  }

  const executionAllowed =
    findings.length === 0
    && manualReviews === 0
    && automaticSelections === plan.segments.length;

  return {
    status: findings.length === 0 ? "passed" : "failed",
    planId: plan.planId,
    executionAllowed,
    summary: {
      segments: plan.segments.length,
      candidates: candidateCount,
      automaticSelections,
      manualReviews,
      errors: findings.length,
    },
    findings,
  };
}
