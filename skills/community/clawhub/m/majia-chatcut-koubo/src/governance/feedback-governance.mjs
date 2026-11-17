const FORBIDDEN_KEY = /(?:caption(?:text|body)?|transcript|text|body|frame|image|audio|video|(?:file)?path|terminology|terms|user(?:name|id)?|media)/iu;
const ABSOLUTE_PATH = /^(?:\/(?:Users|home|private|tmp)\/|[A-Za-z]:[\\/]|file:\/\/)/u;

function finding(code, pointer) {
  return {code, pointer, severity: "error"};
}

function walkPrivacy(value, pointer, findings) {
  if (typeof value === "string" && ABSOLUTE_PATH.test(value)) {
    findings.push(finding("FEEDBACK_ABSOLUTE_PATH_FORBIDDEN", pointer));
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => {
      walkPrivacy(item, `${pointer}/${index}`, findings);
    });
    return;
  }
  if (!value || typeof value !== "object") return;
  for (const [key, item] of Object.entries(value)) {
    if (FORBIDDEN_KEY.test(key)) {
      findings.push(finding(
        "FEEDBACK_CONTENT_FIELD_FORBIDDEN",
        `${pointer}/${key}`,
      ));
    }
    walkPrivacy(item, `${pointer}/${key}`, findings);
  }
}

export function auditFeedbackEvent(event, registry) {
  const findings = [];
  walkPrivacy(event, "", findings);
  const knownRules = new Set(registry.rules.map((rule) => rule.ruleId));
  event.ruleRefs.forEach((ruleId, index) => {
    if (!knownRules.has(ruleId)) {
      findings.push(finding(
        "FEEDBACK_RULE_UNKNOWN",
        `/ruleRefs/${index}`,
      ));
    }
  });
  if (
    event.eventType === "failure"
    && typeof event.failureSignature !== "string"
  ) {
    findings.push(finding(
      "FEEDBACK_FAILURE_SIGNATURE_REQUIRED",
      "/failureSignature",
    ));
  }
  return {
    status: findings.length === 0 ? "passed" : "failed",
    eventId: event.eventId,
    findings,
  };
}

function requireUnique(findings, items, key, pointer, code) {
  const seen = new Set();
  items.forEach((item, index) => {
    if (seen.has(item[key])) {
      findings.push(finding(code, `${pointer}/${index}/${key}`));
    }
    seen.add(item[key]);
  });
}

function semverParts(version) {
  const match = /^(\d+)\.(\d+)\.(\d+)$/u.exec(version ?? "");
  return match ? match.slice(1).map(Number) : null;
}

function isVersionIncrease(before, after) {
  const left = semverParts(before);
  const right = semverParts(after);
  if (!left || !right) return false;
  for (let index = 0; index < left.length; index += 1) {
    if (right[index] > left[index]) return true;
    if (right[index] < left[index]) return false;
  }
  return false;
}

export function auditSuggestedUpdateQueue(queue, registry) {
  const findings = [];
  if (
    queue.executionPolicy.autoApply !== false
    || queue.executionPolicy.mutationRoute !== "human-reviewed-release"
  ) {
    findings.push(finding(
      "FEEDBACK_AUTO_APPLY_FORBIDDEN",
      "/executionPolicy",
    ));
  }
  requireUnique(
    findings,
    queue.suggestions,
    "suggestionId",
    "/suggestions",
    "FEEDBACK_SUGGESTION_ID_DUPLICATE",
  );
  const ruleById = new Map(
    registry.rules.map((rule) => [rule.ruleId, rule]),
  );
  for (const [index, suggestion] of queue.suggestions.entries()) {
    const pointer = `/suggestions/${index}`;
    const uniqueSamples = new Set(suggestion.sampleRefs);
    if (
      uniqueSamples.size !== suggestion.sampleRefs.length
      || suggestion.sampleCount !== uniqueSamples.size
    ) {
      findings.push(finding(
        "FEEDBACK_SAMPLE_COUNT_MISMATCH",
        `${pointer}/sampleCount`,
      ));
    }
    const promoted = [
      "under-review",
      "approved",
      "released",
    ].includes(suggestion.status);
    if (promoted && suggestion.sampleCount < suggestion.minimumSamples) {
      findings.push(finding(
        "FEEDBACK_REPEATED_SAMPLES_REQUIRED",
        `${pointer}/sampleRefs`,
      ));
    }
    if (
      ["approved", "released"].includes(suggestion.status)
      && (
        !suggestion.reviewerId
        || suggestion.evidenceRefs.length === 0
        || suggestion.counterexampleRefs.length === 0
      )
    ) {
      findings.push(finding(
        "FEEDBACK_REVIEW_EVIDENCE_REQUIRED",
        pointer,
      ));
    }
    if (
      suggestion.targetType === "rule"
      && !ruleById.has(suggestion.targetRef)
    ) {
      findings.push(finding(
        "FEEDBACK_RULE_UNKNOWN",
        `${pointer}/targetRef`,
      ));
    }
    if (suggestion.status === "released") {
      const record = suggestion.releaseRecord;
      if (
        !record
        || record.reviewerId !== suggestion.reviewerId
        || !isVersionIncrease(record.versionBefore, record.versionAfter)
      ) {
        findings.push(finding(
          "FEEDBACK_RELEASE_RECORD_INVALID",
          `${pointer}/releaseRecord`,
        ));
      }
      if (
        ruleById.get(suggestion.targetRef)?.kind === "hard-policy"
        && !record
      ) {
        findings.push(finding(
          "FEEDBACK_HARD_POLICY_RELEASE_FORBIDDEN",
          pointer,
        ));
      }
    } else if (suggestion.releaseRecord) {
      findings.push(finding(
        "FEEDBACK_RELEASE_RECORD_PREMATURE",
        `${pointer}/releaseRecord`,
      ));
    }
  }
  return {
    status: findings.length === 0 ? "passed" : "failed",
    queueId: queue.queueId,
    summary: {
      suggestions: queue.suggestions.length,
      released: queue.suggestions.filter(
        (item) => item.status === "released",
      ).length,
      errors: findings.length,
    },
    findings,
  };
}

export function createSuggestedUpdate({
  suggestionId,
  targetType,
  targetRef,
  proposedAdjustment,
  events,
  minimumSamples = 3,
  ownerId,
  rollback,
}) {
  const sampleRefs = [...new Set(
    events.map((event) => event.eventRefHash),
  )].sort();
  return {
    suggestionId,
    targetType,
    targetRef,
    proposedAdjustment: structuredClone(proposedAdjustment),
    sampleRefs,
    sampleCount: sampleRefs.length,
    minimumSamples,
    evidenceRefs: [],
    counterexampleRefs: [],
    ownerId,
    status: "suggested",
    rollback: structuredClone(rollback),
  };
}
