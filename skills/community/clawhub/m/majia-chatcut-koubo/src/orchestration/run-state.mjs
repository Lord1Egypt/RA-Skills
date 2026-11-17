import {contentHash} from "../planning/preview-approval.mjs";

export const RUN_STAGES = Object.freeze([
  "preflight",
  "brief_ready",
  "project_ready",
  "transcript_ready",
  "edit_plan_ready",
  "sample_ready",
  "revision_requested",
  "sample_approved",
  "full_aroll_applied",
  "captions_audio_ready",
  "enhancements_ready",
  "verified",
  "review_ready",
  "exported",
]);

const TRANSITIONS = new Map([
  ["preflight", new Set(["brief_ready"])],
  ["brief_ready", new Set(["project_ready"])],
  ["project_ready", new Set(["transcript_ready"])],
  ["transcript_ready", new Set(["edit_plan_ready"])],
  ["edit_plan_ready", new Set(["sample_ready"])],
  ["sample_ready", new Set(["sample_approved", "revision_requested"])],
  ["revision_requested", new Set(["edit_plan_ready"])],
  ["sample_approved", new Set(["full_aroll_applied"])],
  ["full_aroll_applied", new Set(["captions_audio_ready"])],
  ["captions_audio_ready", new Set(["enhancements_ready", "verified"])],
  ["enhancements_ready", new Set(["verified"])],
  ["verified", new Set(["review_ready"])],
  ["review_ready", new Set(["exported"])],
  ["exported", new Set()],
]);

const FINGERPRINT_KEYS = Object.freeze([
  "plan",
  "style",
  "layout",
  "captions",
  "timelineRevision",
  "sample",
]);

const RECONCILIATION_OUTCOMES = Object.freeze({
  CHATCUT_LOGIN_REQUIRED: new Set(["authenticated"]),
  RUN_CONTEXT_REQUIRED: new Set(["context-resolved"]),
  TRANSCRIPT_PENDING: new Set(["transcript-ready"]),
  TRANSCRIPT_FAILED: new Set(["transcript-ready"]),
  RISK_POLICY_FAILED: new Set(["risk-reviewed"]),
  PRIVACY_UNVERIFIED: new Set(["privacy-verified"]),
  PARTIAL_WRITE: new Set(["compensated"]),
  TIMELINE_REVISION_DRIFT: new Set(["changes-reviewed"]),
  TRANSIENT_FAILURE: new Set(["unchanged", "committed"]),
  WRITE_TIMEOUT: new Set(["unchanged", "committed"]),
});

const CHECKPOINT_REQUIRED_BLOCKERS = new Set([
  "PARTIAL_WRITE",
  "TIMELINE_REVISION_DRIFT",
  "TRANSIENT_FAILURE",
  "WRITE_TIMEOUT",
]);

export class RunStateError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "RunStateError";
    this.code = code;
  }
}

function clone(value) {
  return structuredClone(value);
}

function sameSet(left, right) {
  if (!Array.isArray(left) || !Array.isArray(right)) return false;
  const normalizedLeft = [...new Set(left)].sort();
  const normalizedRight = [...new Set(right)].sort();
  return normalizedLeft.length === left.length
    && normalizedRight.length === right.length
    && normalizedLeft.length === normalizedRight.length
    && normalizedLeft.every((value, index) => value === normalizedRight[index]);
}

function normalizeFingerprints(fingerprints) {
  const normalized = Object.fromEntries(
    FINGERPRINT_KEYS.map((key) => [key, fingerprints?.[key]]),
  );
  if (Object.values(normalized).some((value) => !value)) {
    throw new RunStateError(
      "RUN_SAMPLE_FINGERPRINTS_INVALID",
      "approval must bind plan, style, layout, captions, timeline revision, and sample scope",
    );
  }
  for (const key of ["plan", "style", "layout", "captions", "sample"]) {
    if (!/^sha256:[0-9a-f]{64}$/u.test(normalized[key])) {
      throw new RunStateError("RUN_SAMPLE_FINGERPRINTS_INVALID", "approval fingerprints must be SHA-256 values");
    }
  }
  if (!/^rev[-_][A-Za-z0-9._-]+$/u.test(normalized.timelineRevision)) {
    throw new RunStateError("RUN_SAMPLE_FINGERPRINTS_INVALID", "approval timeline revision is invalid");
  }
  return normalized;
}

function approvedRecordIsCurrent(manifest, approval) {
  return Boolean(
    approval
    && approval.status === "approved"
    && approval.fingerprints?.timelineRevision === manifest.project.timelineRevision,
  );
}

function currentSampleApproval(manifest) {
  const approval = [...manifest.approvals]
    .reverse()
    .find((item) => item.kind === "sample");
  return approvedRecordIsCurrent(manifest, approval)
    && manifest.sampleBinding
    && approval.fingerprints.sample === manifest.sampleBinding.fingerprint
    && approval.fingerprints.timelineRevision === manifest.sampleBinding.timelineRevision
    && sameSet(approval.scope, manifest.sampleBinding.scope);
}

function currentApproval(manifest, kind) {
  const approval = [...manifest.approvals].reverse().find((item) => item.kind === kind);
  return approvedRecordIsCurrent(manifest, approval);
}

export function createSampleBinding({fingerprints, scope, now = new Date().toISOString()} = {}) {
  const normalized = normalizeFingerprints(fingerprints);
  if (
    !Array.isArray(scope)
    || scope.length === 0
    || !sameSet(scope, scope)
    || scope.some((item) => !/^logical:[a-z0-9-]+$/u.test(item))
  ) {
    throw new RunStateError("RUN_SAMPLE_SCOPE_INVALID", "sample scope must be non-empty and unique");
  }
  return {
    fingerprint: normalized.sample,
    timelineRevision: normalized.timelineRevision,
    scope: [...scope].sort(),
    createdAt: now,
  };
}

export function createRunManifest({
  runId,
  profile,
  projectRef = null,
  timelineRef = null,
  timelineRevision = null,
  capability = {},
  now = new Date().toISOString(),
} = {}) {
  if (!/^run-[a-z0-9-]+$/u.test(runId ?? "")) {
    throw new RunStateError("RUN_ID_INVALID", "run ID must be privacy-safe and stable");
  }
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/run-manifest.schema.json",
    schemaVersion: "majia.koubo.run.v1",
    runId,
    stage: "preflight",
    status: "active",
    lastSafeStage: "preflight",
    project: {projectRef, timelineRef, timelineRevision},
    profile: {
      id: profile.id,
      version: profile.version,
      fingerprint: contentHash(profile),
    },
    briefRef: "project-brief.json",
    sourceInventoryRef: null,
    sourceAssets: [],
    sampleBinding: null,
    approvals: [],
    checkpoints: [],
    reconciliations: [],
    lastSafeAction: "check_chatcut_session",
    blockedReason: null,
    failureCounts: {},
    capability: {
      status: capability.status ?? "unverified",
      buildFingerprint: capability.buildFingerprint ?? null,
      toolSchemaFingerprint: capability.toolSchemaFingerprint ?? null,
      observedAt: capability.observedAt ?? null,
    },
    createdAt: now,
    updatedAt: now,
  };
}

function hasApproval(manifest, kind) {
  return manifest.approvals.some((item) => item.kind === kind && item.status === "approved");
}

export function transitionRun(manifest, nextStage, {
  now = new Date().toISOString(),
  nextSafeAction = `continue_${nextStage}`,
  sampleBinding = null,
} = {}) {
  const next = clone(manifest);
  if (next.status === "blocked") {
    throw new RunStateError("RUN_BLOCKED", "blocked runs must be reconciled before transition");
  }
  if (!TRANSITIONS.get(next.stage)?.has(nextStage)) {
    throw new RunStateError("RUN_TRANSITION_INVALID", `cannot move from ${next.stage} to ${nextStage}`);
  }
  if (nextStage === "sample_ready") {
    if (!sampleBinding || sampleBinding.timelineRevision !== next.project.timelineRevision) {
      throw new RunStateError(
        "RUN_SAMPLE_BINDING_INVALID",
        "sample_ready requires a scope fingerprint bound to the current timeline revision",
      );
    }
    next.sampleBinding = clone(sampleBinding);
  }
  if (nextStage === "sample_approved" && !currentSampleApproval(next)) {
    throw new RunStateError("RUN_SAMPLE_APPROVAL_REQUIRED", "full-timeline work requires current sample approval");
  }
  if (["full_aroll_applied", "captions_audio_ready", "enhancements_ready", "verified", "review_ready", "exported"].includes(nextStage) && !hasApproval(next, "sample")) {
    throw new RunStateError("RUN_SAMPLE_APPROVAL_REQUIRED", "full-timeline work requires sample approval");
  }
  if (nextStage === "enhancements_ready" && !currentApproval(next, "enhancement")) {
    throw new RunStateError("RUN_ENHANCEMENT_APPROVAL_REQUIRED", "enhancements require a current explicit approval");
  }
  if (nextStage === "exported" && !currentApproval(next, "export")) {
    throw new RunStateError("RUN_EXPORT_APPROVAL_REQUIRED", "export requires explicit approval");
  }
  next.stage = nextStage;
  if (nextStage === "edit_plan_ready" && manifest.stage === "revision_requested") {
    next.sampleBinding = null;
  }
  next.lastSafeStage = nextStage;
  next.status = nextStage === "sample_ready"
    ? "waiting_user_approval"
    : nextStage === "review_ready"
      ? "review_ready"
      : nextStage === "exported"
        ? "exported"
        : "active";
  next.lastSafeAction = nextSafeAction;
  next.blockedReason = null;
  next.updatedAt = now;
  return next;
}

export function approveSample(manifest, {
  fingerprints,
  scope,
  now = new Date().toISOString(),
} = {}) {
  if (manifest.stage !== "sample_ready") {
    throw new RunStateError("RUN_SAMPLE_NOT_READY", "sample approval is only valid at sample_ready");
  }
  if (manifest.status !== "waiting_user_approval" || manifest.blockedReason !== null) {
    throw new RunStateError("RUN_SAMPLE_APPROVAL_BLOCKED", "blocked or inactive samples must be reconciled before approval");
  }
  const next = clone(manifest);
  const approvalFingerprints = normalizeFingerprints(fingerprints);
  if (approvalFingerprints.timelineRevision !== next.project.timelineRevision) {
    throw new RunStateError("RUN_SAMPLE_REVISION_MISMATCH", "sample approval revision does not match the current timeline");
  }
  if (
    !next.sampleBinding
    || next.sampleBinding.timelineRevision !== approvalFingerprints.timelineRevision
    || next.sampleBinding.fingerprint !== approvalFingerprints.sample
    || !sameSet(scope, next.sampleBinding.scope)
  ) {
    throw new RunStateError("RUN_SAMPLE_BINDING_MISMATCH", "sample approval scope or fingerprint differs from the prepared sample");
  }
  const approvalScope = [...scope].sort();
  next.approvals = next.approvals.filter((item) => item.kind !== "sample");
  next.approvals.push({
    approvalRef: `logical:sample-approval-${next.runId.replace(/^run-/u, "")}`,
    kind: "sample",
    status: "approved",
    fingerprints: approvalFingerprints,
    scope: approvalScope,
    recordedAt: now,
  });
  next.status = "active";
  next.updatedAt = now;
  return transitionRun(next, "sample_approved", {now, nextSafeAction: "expand_approved_sample"});
}

export function authorizeDecisions(manifest, {
  fingerprints,
  decisionIds,
  now = new Date().toISOString(),
} = {}) {
  if (manifest.stage !== "sample_ready" || manifest.status !== "waiting_user_approval" || manifest.blockedReason !== null) {
    throw new RunStateError("RUN_DECISION_APPROVAL_NOT_READY", "decision approval is only valid on the current representative sample");
  }
  const approvalFingerprints = normalizeFingerprints(fingerprints);
  if (
    approvalFingerprints.timelineRevision !== manifest.project.timelineRevision
    || !manifest.sampleBinding
    || approvalFingerprints.sample !== manifest.sampleBinding.fingerprint
  ) {
    throw new RunStateError("RUN_DECISION_APPROVAL_STALE", "decision approval does not match the current sample");
  }
  if (
    !Array.isArray(decisionIds)
    || decisionIds.length === 0
    || decisionIds.length !== new Set(decisionIds).size
    || decisionIds.some((id) => !/^dec-[a-z0-9-]+$/u.test(id))
  ) {
    throw new RunStateError("RUN_DECISION_SCOPE_INVALID", "decision approval requires unique safe decision IDs");
  }
  const next = clone(manifest);
  const approvalRef = `logical:decision-approval-${next.runId.replace(/^run-/u, "")}`;
  next.approvals = next.approvals.filter((item) => item.kind !== "decision");
  next.approvals.push({
    approvalRef,
    kind: "decision",
    status: "approved",
    fingerprints: approvalFingerprints,
    scope: decisionIds.map((id) => `logical:decision-${id}`).sort(),
    recordedAt: now,
  });
  next.updatedAt = now;
  return next;
}

export function requestSampleRevision(manifest, {
  direction = "natural",
  now = new Date().toISOString(),
} = {}) {
  if (manifest.stage !== "sample_ready" || manifest.status !== "waiting_user_approval" || manifest.blockedReason !== null) {
    throw new RunStateError("RUN_SAMPLE_REVISION_NOT_READY", "sample revision can only be requested for the current reviewable sample");
  }
  if (!["natural", "tight"].includes(direction)) {
    throw new RunStateError("RUN_SAMPLE_REVISION_DIRECTION_INVALID", "sample revision direction must be natural or tight");
  }
  const next = transitionRun(manifest, "revision_requested", {
    now,
    nextSafeAction: `replan_sample_${direction}`,
  });
  next.sampleBinding = null;
  next.approvals = next.approvals.map((item) => ({...item, status: item.status === "approved" ? "stale" : item.status}));
  return next;
}

export function authorizeExport(manifest, {fingerprints, scope, now = new Date().toISOString()} = {}) {
  if (manifest.stage !== "review_ready" || manifest.status !== "review_ready" || manifest.blockedReason !== null) {
    throw new RunStateError("RUN_EXPORT_NOT_READY", "export can only be authorized from an unblocked review_ready run");
  }
  const next = clone(manifest);
  const approvalFingerprints = normalizeFingerprints(fingerprints);
  if (approvalFingerprints.timelineRevision !== next.project.timelineRevision) {
    throw new RunStateError("RUN_EXPORT_REVISION_MISMATCH", "export approval must bind the current timeline revision");
  }
  if (!Array.isArray(scope) || !sameSet(scope, [next.project.timelineRef])) {
    throw new RunStateError("RUN_EXPORT_SCOPE_INVALID", "export approval must cover exactly the current timeline");
  }
  next.approvals = next.approvals.filter((item) => item.kind !== "export");
  next.approvals.push({
    approvalRef: `logical:export-approval-${next.runId.replace(/^run-/u, "")}`,
    kind: "export",
    status: "approved",
    fingerprints: approvalFingerprints,
    scope: [...scope],
    recordedAt: now,
  });
  next.updatedAt = now;
  return next;
}

export function authorizeEnhancements(manifest, {fingerprints, scope, now = new Date().toISOString()} = {}) {
  if (manifest.stage !== "captions_audio_ready" || manifest.status !== "active" || manifest.blockedReason !== null) {
    throw new RunStateError("RUN_ENHANCEMENT_NOT_READY", "enhancements can only be authorized after A-roll, audio, and captions are ready");
  }
  const allowed = new Set(["logical:music", "logical:motion-graphics", "logical:broll", "logical:generated-media", "logical:restructure"]);
  if (!Array.isArray(scope) || scope.length === 0 || !sameSet(scope, scope) || scope.some((item) => !allowed.has(item))) {
    throw new RunStateError("RUN_ENHANCEMENT_SCOPE_INVALID", "enhancement approval must name explicit supported treatments");
  }
  const approvalFingerprints = normalizeFingerprints(fingerprints);
  if (approvalFingerprints.timelineRevision !== manifest.project.timelineRevision) {
    throw new RunStateError("RUN_ENHANCEMENT_REVISION_MISMATCH", "enhancement approval must bind the current timeline revision");
  }
  const next = clone(manifest);
  next.approvals = next.approvals.filter((item) => item.kind !== "enhancement");
  next.approvals.push({
    approvalRef: `logical:enhancement-approval-${next.runId.replace(/^run-/u, "")}`,
    kind: "enhancement",
    status: "approved",
    fingerprints: approvalFingerprints,
    scope: [...scope].sort(),
    recordedAt: now,
  });
  next.updatedAt = now;
  return next;
}

export function blockRun(manifest, {
  code,
  message,
  resumeStage = manifest.lastSafeStage,
  now = new Date().toISOString(),
} = {}) {
  if (!/^[A-Z0-9_]+$/u.test(code ?? "") || typeof message !== "string" || message.length === 0 || message.length > 240) {
    throw new RunStateError("RUN_BLOCK_REASON_INVALID", "blocked runs require a safe code and user-facing message");
  }
  if (!RUN_STAGES.includes(resumeStage)) {
    throw new RunStateError("RUN_BLOCK_RESUME_STAGE_INVALID", "blocked resume stage is invalid");
  }
  const next = clone(manifest);
  next.status = "blocked";
  next.blockedReason = {code, message, resumeStage};
  next.lastSafeAction = "reconcile_before_resume";
  next.updatedAt = now;
  return next;
}

export function invalidateApprovals(manifest, {
  reason = "TIMELINE_REVISION_DRIFT",
  message = "时间线已变化，旧样片确认失效；先回读差异再继续。",
  currentRevision = null,
  now = new Date().toISOString(),
} = {}) {
  const next = clone(manifest);
  next.approvals = next.approvals.map((item) => ({...item, status: item.status === "approved" ? "stale" : item.status}));
  if (currentRevision) next.project.timelineRevision = currentRevision;
  next.sampleBinding = null;
  return blockRun(next, {
    code: reason,
    message,
    resumeStage: RUN_STAGES.indexOf(next.stage) >= RUN_STAGES.indexOf("sample_ready")
      ? "edit_plan_ready"
      : next.lastSafeStage,
    now,
  });
}

export function resumeRun(manifest, {
  currentTimelineRevision,
  reconciliation = null,
  checkpoint = null,
  now = new Date().toISOString(),
} = {}) {
  if (manifest.status !== "blocked") return clone(manifest);
  if (manifest.project.timelineRevision && !currentTimelineRevision) {
    throw new RunStateError("RUN_CURRENT_REVISION_REQUIRED", "resume requires a fresh timeline revision readback");
  }
  if (manifest.project.timelineRevision && currentTimelineRevision !== manifest.project.timelineRevision) {
    return invalidateApprovals(manifest, {currentRevision: currentTimelineRevision, now});
  }
  const blockerCode = manifest.blockedReason?.code;
  if (Object.values(manifest.failureCounts ?? {}).some((count) => count >= 3)) {
    throw new RunStateError("RUN_RETRY_LIMIT_REACHED", "three repeated failures require manual handoff");
  }
  const allowedOutcomes = RECONCILIATION_OUTCOMES[blockerCode];
  if (!allowedOutcomes) {
    throw new RunStateError("RUN_RECONCILIATION_POLICY_MISSING", "this blocker cannot be cleared by generic resume");
  }
  if (
    !reconciliation
    || reconciliation.blockerCode !== blockerCode
    || !allowedOutcomes.has(reconciliation.outcome)
    || reconciliation.observedRevision !== currentTimelineRevision
    || !Array.isArray(reconciliation.evidenceRefs)
    || reconciliation.evidenceRefs.length === 0
    || reconciliation.evidenceRefs.length !== new Set(reconciliation.evidenceRefs).size
    || reconciliation.evidenceRefs.some((item) => !/^logical:[a-z0-9-]+$/u.test(item))
  ) {
    throw new RunStateError("RUN_RECONCILIATION_REQUIRED", "resume requires blocker-specific readback evidence");
  }
  if (CHECKPOINT_REQUIRED_BLOCKERS.has(blockerCode)) {
    if (
      !checkpoint
      || checkpoint.runId !== manifest.runId
      || !manifest.checkpoints.includes(checkpoint.checkpointId)
      || reconciliation.checkpointId !== checkpoint.checkpointId
    ) {
      throw new RunStateError("RUN_CHECKPOINT_REQUIRED", "this blocker must resume from a persisted checkpoint");
    }
  }
  const next = clone(manifest);
  const safeStageByBlocker = {
    CHATCUT_LOGIN_REQUIRED: "preflight",
    RUN_CONTEXT_REQUIRED: "preflight",
    TRANSCRIPT_PENDING: "project_ready",
    TRANSCRIPT_FAILED: "project_ready",
    RISK_POLICY_FAILED: "transcript_ready",
    PRIVACY_UNVERIFIED: "edit_plan_ready",
    PARTIAL_WRITE: "edit_plan_ready",
    TIMELINE_REVISION_DRIFT: "edit_plan_ready",
  };
  next.stage = safeStageByBlocker[blockerCode]
    ?? checkpoint?.stage
    ?? next.blockedReason?.resumeStage
    ?? next.lastSafeStage;
  if (["PARTIAL_WRITE", "TIMELINE_REVISION_DRIFT", "PRIVACY_UNVERIFIED"].includes(blockerCode)) {
    next.approvals = next.approvals.map((item) => ({...item, status: item.status === "approved" ? "stale" : item.status}));
    next.sampleBinding = null;
  }
  next.status = next.stage === "sample_ready" ? "waiting_user_approval" : "active";
  next.reconciliations.push({
    blockerCode,
    outcome: reconciliation.outcome,
    evidenceRefs: [...new Set(reconciliation.evidenceRefs)].sort(),
    checkpointId: reconciliation.checkpointId ?? null,
    observedRevision: currentTimelineRevision ?? null,
    recordedAt: now,
  });
  next.blockedReason = null;
  next.lastSafeAction = "continue_from_checkpoint";
  next.updatedAt = now;
  return next;
}

export function approvalIsCurrent(manifest, fingerprints) {
  const approval = [...manifest.approvals].reverse().find((item) => item.kind === "sample");
  if (!approval || approval.status !== "approved") return false;
  return FINGERPRINT_KEYS
    .every((key) => approval.fingerprints[key] === fingerprints[key]);
}
