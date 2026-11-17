import crypto from "node:crypto";

import {
  ratesEqual,
  validateTimeRange,
} from "../time/rational-time.mjs";

const INVALIDATION_FIELDS = Object.freeze([
  "planHash",
  "previewBundleId",
  "styleFingerprint",
  "timelineRevision",
]);

export class PreviewApprovalError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "PreviewApprovalError";
    this.code = code;
  }
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalize(value[key])]),
    );
  }
  return value;
}

export function contentHash(value) {
  return `sha256:${crypto
    .createHash("sha256")
    .update(JSON.stringify(canonicalize(value)))
    .digest("hex")}`;
}

function secondsInUnitsFloor(seconds, rate) {
  return Number(
    BigInt(seconds) * BigInt(rate.numerator) / BigInt(rate.denominator),
  );
}

function overlaps(left, right) {
  return left.start < right.end && left.end > right.start;
}

function rangeWithin(range, boundary) {
  return range.start >= boundary.start && range.end <= boundary.end;
}

function window(windowId, reason, range, subjectRefs) {
  return {
    windowId,
    reason,
    range: structuredClone(range),
    subjectRefs: [...subjectRefs],
  };
}

export function createPreviewBundle({
  project,
  statePlan,
  planHash,
  styleFingerprint,
}) {
  const timeline = project?.timeline;
  if (
    !timeline
    || project.projectId !== statePlan?.projectId
    || timeline.timelineId !== statePlan.timelineId
    || timeline.revision !== statePlan.timelineRevision
  ) {
    throw new PreviewApprovalError(
      "PREVIEW_PLAN_MISMATCH",
      "preview inputs do not target one project timeline",
    );
  }
  validateTimeRange(timeline.duration, "timeline");
  const duration = timeline.duration;
  const openingLength = secondsInUnitsFloor(60, duration.rate);
  const endingLength = secondsInUnitsFloor(10, duration.rate);
  const openingRange = {
    ...structuredClone(duration),
    end: Math.min(duration.end, duration.start + openingLength),
  };
  const endingRange = {
    ...structuredClone(duration),
    start: Math.max(duration.start, duration.end - endingLength),
  };
  const rankedStates = [...statePlan.compositionStates].sort((left, right) => {
    const score = (state) =>
      (state.stateType === "A" ? 0 : 10)
      + statePlan.privacyOverlays.filter(
        (overlay) => overlaps(overlay.range, state.range),
      ).length * 100;
    return score(right) - score(left)
      || left.range.start - right.range.start
      || left.stateInstanceId.localeCompare(right.stateInstanceId);
  });
  const complexState = rankedStates[0];
  if (!complexState) {
    throw new PreviewApprovalError(
      "PREVIEW_COMPLEX_WINDOW_MISSING",
      "preview requires at least one composition state",
    );
  }
  const windows = [
    window(
      "preview_opening",
      "opening-60s",
      openingRange,
      [timeline.timelineId],
    ),
    window(
      "preview_complex",
      "complex-operation",
      complexState.range,
      [complexState.stateInstanceId],
    ),
    ...statePlan.privacyOverlays.map((overlay, index) => window(
      `preview_privacy_${String(index + 1).padStart(3, "0")}`,
      "privacy-risk",
      overlay.range,
      [overlay.privacyInstanceId],
    )),
    window(
      "preview_ending",
      "ending",
      endingRange,
      [timeline.timelineId],
    ),
  ];
  const requiredReasons = [
    "opening-60s",
    "complex-operation",
    ...(statePlan.privacyOverlays.length > 0 ? ["privacy-risk"] : []),
    "ending",
  ];
  const identity = contentHash({
    planHash,
    projectId: project.projectId,
    styleFingerprint,
    timelineRevision: timeline.revision,
    windows,
  }).slice(7, 19);
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/preview-bundle.schema.json",
    schemaVersion: "1.0.0",
    previewBundleId: `preview_bundle_${identity}`,
    projectId: project.projectId,
    runId: project.runId,
    timelineId: timeline.timelineId,
    timelineRevision: timeline.revision,
    timelineRange: structuredClone(duration),
    planHash,
    styleFingerprint,
    requiredReasons,
    windows,
    status: "ready",
  };
}

export function auditPreviewBundle(previewBundle) {
  const findings = [];
  const windowIds = new Set();
  for (const [index, item] of previewBundle.windows.entries()) {
    if (windowIds.has(item.windowId)) {
      findings.push({
        code: "PREVIEW_WINDOW_DUPLICATE",
        pointer: `/windows/${index}/windowId`,
      });
    }
    windowIds.add(item.windowId);
    try {
      validateTimeRange(item.range, "timeline");
      if (
        !ratesEqual(item.range.rate, previewBundle.timelineRange.rate)
        || !rangeWithin(item.range, previewBundle.timelineRange)
      ) {
        findings.push({
          code: "PREVIEW_WINDOW_OUTSIDE_TIMELINE",
          pointer: `/windows/${index}/range`,
        });
      }
    } catch {
      findings.push({
        code: "PREVIEW_WINDOW_RANGE_INVALID",
        pointer: `/windows/${index}/range`,
      });
    }
  }
  for (const reason of previewBundle.requiredReasons) {
    if (!previewBundle.windows.some((item) => item.reason === reason)) {
      findings.push({
        code: "PREVIEW_REQUIRED_REASON_MISSING",
        pointer: "/requiredReasons",
        reason,
      });
    }
  }
  return findings;
}

function sameSet(left, right) {
  return left.length === right.length
    && [...left].sort().every((value, index) => value === [...right].sort()[index]);
}

export function evaluatePreviewApproval({
  previewBundle,
  approvalLog,
  currentPlanHash,
  currentStyleFingerprint,
  currentTimelineRevision,
}) {
  const reasons = auditPreviewBundle(previewBundle)
    .map((item) => item.code);
  if (previewBundle.status !== "ready") reasons.push("PREVIEW_NOT_READY");
  if (approvalLog.projectId !== previewBundle.projectId) {
    reasons.push("PREVIEW_APPROVAL_PROJECT_MISMATCH");
  }
  if (currentPlanHash !== previewBundle.planHash) {
    reasons.push("PREVIEW_PLAN_CHANGED");
  }
  if (currentStyleFingerprint !== previewBundle.styleFingerprint) {
    reasons.push("PREVIEW_STYLE_CHANGED");
  }
  if (currentTimelineRevision !== previewBundle.timelineRevision) {
    reasons.push("PREVIEW_TIMELINE_CHANGED");
  }
  const events = approvalLog.events
    .filter((event) =>
      event.previewBundleId === previewBundle.previewBundleId,
    )
    .sort((left, right) =>
      Date.parse(left.recordedAt) - Date.parse(right.recordedAt),
    );
  const latest = events.at(-1);
  if (!latest) {
    reasons.push("PREVIEW_APPROVAL_MISSING");
  } else if (latest.decision !== "approved") {
    reasons.push(
      latest.decision === "revoked"
        ? "PREVIEW_APPROVAL_REVOKED"
        : "PREVIEW_APPROVAL_REJECTED",
    );
  } else {
    const scope = latest.scope;
    const exactScope =
      scope.projectId === previewBundle.projectId
      && scope.runId === previewBundle.runId
      && scope.timelineId === previewBundle.timelineId
      && scope.timelineRevision === previewBundle.timelineRevision
      && scope.planHash === previewBundle.planHash
      && scope.styleFingerprint === previewBundle.styleFingerprint
      && sameSet(
        scope.windowIds,
        previewBundle.windows.map((item) => item.windowId),
      )
      && sameSet(latest.invalidatesOn, INVALIDATION_FIELDS);
    if (!exactScope) reasons.push("PREVIEW_APPROVAL_SCOPE_MISMATCH");
  }
  const uniqueReasons = [...new Set(reasons)];
  return {
    status: uniqueReasons.length === 0 ? "open" : "closed",
    canExecute: uniqueReasons.length === 0,
    previewBundleId: previewBundle.previewBundleId,
    approvalId: latest?.approvalId ?? null,
    reasons: uniqueReasons,
  };
}

export const PREVIEW_INVALIDATION_FIELDS = INVALIDATION_FIELDS;
