import {createCheckpoint, attachCheckpoint, registerFailure} from "./checkpoint-manager.mjs";
import {buildHandoffReport} from "./handoff-reporter.mjs";
import {inferIntent} from "./intent-router.mjs";
import {createProjectBrief, selectProfile} from "./profile-selector.mjs";
import {createSampleFingerprint, selectRepresentativeWindows} from "./preview-selector.mjs";
import {auditDecisionLog, normalizeDecision} from "./risk-classifier.mjs";
import {approveSample, blockRun, createRunManifest, createSampleBinding, invalidateApprovals, transitionRun} from "./run-state.mjs";
import {contentHash} from "../planning/preview-approval.mjs";
import {FakeTimelineAdapter, RecoverableExecutor} from "../execution/recoverable-executor.mjs";

function makeRunId(scenarioId) {
  return `run-${scenarioId.replace(/^scenario-/u, "")}`;
}

function checkpoint(manifest, fingerprints, now) {
  const value = createCheckpoint({
    manifest,
    planFingerprint: fingerprints?.plan ?? null,
    styleFingerprint: fingerprints?.style ?? null,
    verifiedEvidence: [],
    completedOperations: [],
    nextSafeAction: manifest.lastSafeAction,
    now,
  });
  return {manifest: attachCheckpoint(manifest, value, now), checkpoint: value};
}

function simulatedEvidence({ref, kind, revision, payload, now}) {
  return {
    ref,
    kind,
    hash: typeof payload === "string" && /^sha256:[0-9a-f]{64}$/u.test(payload)
      ? payload
      : contentHash(payload),
    revision,
    provenance: "simulation",
    capturedAt: now,
  };
}

function sampleApprovalEvidence(manifest, now) {
  const approval = [...manifest.approvals].reverse().find((item) => item.kind === "sample" && item.status === "approved");
  if (!approval) return null;
  return simulatedEvidence({
    ref: "logical:sample-approval-evidence",
    kind: "sample-approval",
    revision: approval.fingerprints.timelineRevision,
    payload: approval,
    now,
  });
}

function sampleOperation(manifest, windows) {
  const operation = {
    operationId: "operation_sample_aroll",
    sceneId: "scene_sample",
    idempotencyKey: `idem_sample_${manifest.runId}`,
    logicalId: "logical_aroll_batch",
    risk: "low",
    scopeRef: windows[0].windowRef,
    desiredState: {
      kind: "bounded-sample",
      runId: manifest.runId,
      windowRefs: windows.map((item) => item.windowRef),
    },
  };
  operation.desiredHash = contentHash(operation.desiredState);
  return operation;
}

function executeBoundedFakeSample(manifest, windows) {
  const operation = sampleOperation(manifest, windows);
  const executionPlan = {
    projectId: manifest.project.projectRef,
    runId: manifest.runId,
    timelineRevision: manifest.project.timelineRevision,
    planHash: contentHash({runId: manifest.runId, sample: operation.desiredHash}),
    operations: [operation],
  };
  const adapter = new FakeTimelineAdapter({revision: manifest.project.timelineRevision});
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan,
    executionGate: {
      kind: "bounded-sample",
      canExecute: true,
      planHash: executionPlan.planHash,
      timelineRevision: executionPlan.timelineRevision,
      scope: windows.map((item) => item.windowRef),
    },
  });
  return {adapter, result};
}

function executeApprovedFakeBatch(manifest, injectedFailures, adapter) {
  const operation = {
    operationId: "operation_aroll_batch",
    sceneId: "scene_aroll",
    idempotencyKey: `idem_${manifest.runId}`,
    logicalId: "logical_aroll_batch",
    desiredState: {kind: "approved-aroll-cleanup", runId: manifest.runId},
  };
  operation.desiredHash = contentHash(operation.desiredState);
  const executionPlan = {
    projectId: manifest.project.projectRef,
    runId: manifest.runId,
    timelineRevision: manifest.project.timelineRevision,
    planHash: contentHash({runId: manifest.runId, operation: operation.desiredHash}),
    operations: [operation],
  };
  for (const failure of ["timeout-before-commit", "timeout-after-commit", "partial-write"]) {
    if (injectedFailures.includes(failure)) adapter.injectFailure(operation.operationId, failure);
  }
  const result = new RecoverableExecutor(adapter).execute({
    executionPlan,
    approvalReport: {canExecute: true},
  });
  return {
    status: result.status,
    errorCode: result.errorCode,
    objectCount: adapter.objectCount(),
    duplicateWrites: adapter.objectCount() > 1,
    reconciliations: result.journal.entries.map((entry) => entry.reconciliation),
    currentTimelineRevision: result.journal.currentTimelineRevision,
    journal: result.journal,
  };
}

export function runFakeOneClickSession(scenario, {now = "2026-08-10T00:00:00Z"} = {}) {
  const route = inferIntent(scenario.intent);
  const goal = scenario.hasScreenCapture
    ? "screen-demo"
    : scenario.durationSec >= 300
      ? "trust-longform"
      : route.mode === "fast"
        ? "short-draft"
        : "daily-publish";
  const profile = selectProfile({mode: route.mode, goal, durationSec: scenario.durationSec, hasScreenCapture: scenario.hasScreenCapture});
  const brief = createProjectBrief({route, profile, goal, targetDurationSec: null, createdAt: now});
  let manifest = createRunManifest({
    runId: makeRunId(scenario.scenarioId),
    profile,
    projectRef: scenario.projectExists ? "logical:project-current" : null,
    timelineRef: scenario.projectExists ? "logical:timeline-current" : null,
    timelineRevision: scenario.projectExists ? scenario.timelineRevision : null,
    now,
  });
  const checkpoints = [];

  if (route.action === "resume") {
    manifest = blockRun(manifest, {
      code: "RUN_CONTEXT_REQUIRED",
      message: "恢复请求必须绑定已有运行记录，不能创建新的剪辑任务。",
      now,
    });
    return {
      route,
      profile,
      brief,
      manifest,
      checkpoints,
      decisionLog: null,
      windows: [],
      fingerprints: null,
      recovery: null,
      handoff: buildHandoffReport({manifest, openRisks: [manifest.blockedReason.message], now}),
    };
  }

  if (!scenario.authenticated) {
    manifest = blockRun(manifest, {code: "CHATCUT_LOGIN_REQUIRED", message: "请先按 ChatCut 官方指引完成登录。", now});
    return {route, profile, brief, manifest, checkpoints, decisionLog: null, windows: [], fingerprints: null, handoff: buildHandoffReport({manifest, openRisks: ["ChatCut 尚未登录"], now})};
  }

  manifest = transitionRun(manifest, "brief_ready", {now, nextSafeAction: "resolve_project_and_source"});
  if (!manifest.project.projectRef && route.automationLevel === "audit") {
    manifest = blockRun(manifest, {
      code: "RUN_CONTEXT_REQUIRED",
      message: "只读审核需要现有项目上下文；未创建新项目。",
      now,
    });
    return {route, profile, brief, manifest, checkpoints, decisionLog: null, windows: [], fingerprints: null, recovery: null, handoff: buildHandoffReport({manifest, openRisks: [manifest.blockedReason.message], now})};
  }
  if (!manifest.project.projectRef) {
    manifest.project = {projectRef: "logical:project-new", timelineRef: "logical:timeline-new", timelineRevision: scenario.timelineRevision};
  }
  manifest.sourceAssets = ["logical:aroll-main"];
  manifest.sourceInventoryRef = "source-inventory.json";
  manifest = transitionRun(manifest, "project_ready", {now, nextSafeAction: "ensure_transcript"});
  if (scenario.transcriptStatus !== "ready") {
    manifest = blockRun(manifest, {
      code: scenario.transcriptStatus === "failed" ? "TRANSCRIPT_FAILED" : "TRANSCRIPT_PENDING",
      message: scenario.transcriptStatus === "failed" ? "转写失败，先按官方恢复指引处理。" : "转写仍在处理中。",
      now,
    });
    return {route, profile, brief, manifest, checkpoints, decisionLog: null, windows: [], fingerprints: null, handoff: buildHandoffReport({manifest, openRisks: [manifest.blockedReason.message], now})};
  }
  manifest = transitionRun(manifest, "transcript_ready", {now, nextSafeAction: "classify_aroll_decisions"});

  const decisions = scenario.decisions.map((candidate, index) => normalizeDecision(
    route.automationLevel === "audit" || (brief.textEdit && brief.textEdit.target !== "speech-cut")
      ? {...candidate, status: "proposed", approvalRef: null}
      : candidate,
    index,
  ));
  const decisionLog = {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/decision-log.schema.json",
    schemaVersion: "majia.koubo.decisions.v1",
    runId: manifest.runId,
    decisions,
  };
  const findings = auditDecisionLog(decisionLog, {
    approvals: manifest.approvals,
    timelineRevision: manifest.project.timelineRevision,
  });
  if (findings.length > 0) {
    manifest = blockRun(manifest, {code: "RISK_POLICY_FAILED", message: "剪辑决定未通过风险检查。", now});
    return {route, profile, brief, manifest, checkpoints, decisionLog, windows: [], fingerprints: null, handoff: buildHandoffReport({manifest, openRisks: ["风险规则未通过"], now})};
  }
  manifest = transitionRun(manifest, "edit_plan_ready", {now, nextSafeAction: "build_representative_sample"});
  if (brief.textEdit && brief.textEdit.target !== "speech-cut") {
    manifest.lastSafeAction = "route_text_edit_without_aroll_cleanup";
    return {
      route, profile, brief, manifest, checkpoints, decisionLog,
      windows: [], fingerprints: null,
      recovery: {status: "not-run", objectCount: 0, duplicateWrites: false, reconciliations: []},
      handoff: buildHandoffReport({manifest, nextActions: ["按当前官方指令处理指定文字对象；不执行口播清理。"], now}),
    };
  }
  if (route.automationLevel === "audit" || route.action === "review") {
    return {
      route,
      profile,
      brief,
      manifest,
      checkpoints,
      decisionLog,
      windows: [],
      fingerprints: null,
      recovery: {status: "not-run", objectCount: 0, duplicateWrites: false, reconciliations: []},
      handoff: buildHandoffReport({
        manifest,
        completed: ["project", "source-inventory", "transcript"],
        openRisks: decisions.filter((item) => item.approvalRequired).map((item) => `待确认：${item.type}`),
        nextActions: ["确认审核方案后再决定是否制作代表样片"],
        now,
      }),
    };
  }
  const windows = selectRepresentativeWindows({
    durationSec: scenario.durationSec,
    candidates: scenario.sampleCandidates ?? [],
    hasScreenCapture: scenario.hasScreenCapture,
    samplePolicy: profile.defaults.sample,
  });
  const sampleExecution = executeBoundedFakeSample(manifest, windows);
  if (sampleExecution.result.status !== "completed") {
    manifest = blockRun(manifest, {code: "SAMPLE_WRITE_FAILED", message: "代表样片写入后未通过回读。", resumeStage: "edit_plan_ready", now});
    return {route, profile, brief, manifest, checkpoints, decisionLog, windows, fingerprints: null, recovery: sampleExecution.result, handoff: buildHandoffReport({manifest, openRisks: [manifest.blockedReason.message], now})};
  }
  manifest.project.timelineRevision = sampleExecution.result.journal.currentTimelineRevision;
  const fingerprints = createSampleFingerprint({
    plan: decisions,
    style: {profile: profile.id},
    layout: {states: profile.defaults.visualStates},
    captions: {profile: profile.defaults.captions, provisional: true},
    timelineRevision: manifest.project.timelineRevision,
    windows,
  });
  manifest = transitionRun(manifest, "sample_ready", {
    now,
    nextSafeAction: "request_sample_approval",
    sampleBinding: createSampleBinding({
      fingerprints,
      scope: windows.map((item) => item.windowRef),
      now,
    }),
  });
  let saved = checkpoint(manifest, fingerprints, now);
  manifest = saved.manifest;
  checkpoints.push(saved.checkpoint);

  const sampleEvidence = [simulatedEvidence({
    ref: "logical:sample-structure-readback",
    kind: "structure-readback",
    revision: manifest.project.timelineRevision,
    payload: sampleExecution.result.evidenceManifest.artifacts[0]?.sha256
      ?? {runId: manifest.runId, stage: "sample"},
    now,
  })];
  if (scenario.rendererAvailable) {
    sampleEvidence.push(simulatedEvidence({
      ref: "logical:sample-composed-frame",
      kind: "composed-frame",
      revision: manifest.project.timelineRevision,
      payload: {runId: manifest.runId, revision: manifest.project.timelineRevision, frame: "sample"},
      now,
    }));
  }

  if (!scenario.sampleApproved) {
    return {route, profile, brief, manifest, checkpoints, decisionLog, windows, fingerprints, handoff: buildHandoffReport({manifest, completed: ["project", "source-inventory", "transcript", "sample"], verification: {structure: "pass", visual: scenario.rendererAvailable ? "pass" : "unverified", sampleApproval: "pending"}, evidence: sampleEvidence, nextActions: ["播放代表样片并选择是否继续整片"], now})};
  }

  manifest = approveSample(manifest, {fingerprints, scope: windows.map((item) => item.windowRef), now});
  if (scenario.injectedFailures.includes("manual-edit") || scenario.injectedFailures.includes("stale-timeline-id")) {
    manifest = invalidateApprovals(manifest, {
      reason: "TIMELINE_REVISION_DRIFT",
      currentRevision: scenario.injectedFailures.includes("manual-edit") ? "rev-after-manual-edit" : "rev-new-timeline",
      now,
    });
    return {route, profile, brief, manifest, checkpoints, decisionLog, windows, fingerprints, recovery: null, handoff: buildHandoffReport({manifest, completed: ["project", "source-inventory", "transcript", "sample"], verification: {sampleApproval: "stale"}, openRisks: ["需回读用户手工修改"], now})};
  }
  const recovery = executeApprovedFakeBatch(manifest, scenario.injectedFailures, sampleExecution.adapter);
  if (recovery.status !== "completed") {
    manifest = registerFailure(manifest, "PARTIAL_WRITE", now).manifest;
    manifest = invalidateApprovals(manifest, {
      reason: "PARTIAL_WRITE",
      message: "整片写入不完整且已补偿；样片批准失效，必须从检查点回读后重新规划。",
      currentRevision: recovery.currentTimelineRevision,
      now,
    });
    return {route, profile, brief, manifest, checkpoints, decisionLog, windows, fingerprints, recovery, handoff: buildHandoffReport({manifest, verification: {sampleApproval: "stale"}, openRisks: ["部分写入需要人工核对"], now})};
  }

  manifest = transitionRun(manifest, "full_aroll_applied", {now, nextSafeAction: "smooth_audio_then_captions"});
  manifest.project.timelineRevision = recovery.currentTimelineRevision;
  manifest = transitionRun(manifest, "captions_audio_ready", {now, nextSafeAction: "verify_timeline"});
  manifest = transitionRun(manifest, "verified", {now, nextSafeAction: "handoff_editable_timeline"});
  manifest = transitionRun(manifest, "review_ready", {now, nextSafeAction: "wait_for_user_review"});
  saved = checkpoint(manifest, fingerprints, now);
  manifest = saved.manifest;
  checkpoints.push(saved.checkpoint);

  const evidence = [simulatedEvidence({
    ref: "logical:final-structure-readback",
    kind: "structure-readback",
    revision: manifest.project.timelineRevision,
    payload: recovery.journal.entries.at(-1)?.observedHash
      ?? {runId: manifest.runId, stage: "final"},
    now,
  })];
  const approvalEvidence = sampleApprovalEvidence(manifest, now);
  if (approvalEvidence) evidence.push(approvalEvidence);
  if (scenario.rendererAvailable) evidence.push(simulatedEvidence({
    ref: "logical:final-composed-frame",
    kind: "composed-frame",
    revision: manifest.project.timelineRevision,
    payload: {runId: manifest.runId, revision: manifest.project.timelineRevision, frame: "final"},
    now,
  }));
  if (scenario.audioMeasured) evidence.push(simulatedEvidence({
    ref: "logical:audio-measurement-evidence",
    kind: "audio-measurement",
    revision: manifest.project.timelineRevision,
    payload: {runId: manifest.runId, revision: manifest.project.timelineRevision, measurement: "simulated"},
    now,
  }));
  if (scenario.humanListening) evidence.push(simulatedEvidence({
    ref: "logical:human-listening-evidence",
    kind: "human-listening",
    revision: manifest.project.timelineRevision,
    payload: {runId: manifest.runId, revision: manifest.project.timelineRevision, listening: "simulated"},
    now,
  }));
  const privacyStatus = scenario.hasScreenCapture
    ? "unverified"
    : "not_applicable";
  const handoff = buildHandoffReport({
    manifest,
    completed: ["project", "source-inventory", "transcript", "aroll", "sample", "smooth-audio", "captions", "verification"],
    verification: {
      structure: "pass",
      visual: scenario.rendererAvailable ? "pass" : "unverified",
      audioMeasurement: scenario.audioMeasured ? "pass" : "unverified",
      humanListening: scenario.humanListening ? "pass" : "unverified",
      sampleApproval: "pass",
      finalReviewApproval: "pending",
      privacy: privacyStatus,
    },
    evidence,
    openRisks: [
      ...(scenario.rendererAvailable ? [] : ["当前环境没有可用合成帧，画面仍未验证"]),
      ...(scenario.hasScreenCapture ? ["录屏隐私仍需独立逐区复核，普通合成帧不能替代隐私证据"] : []),
      ...decisions
        .filter((item) => item.approvalRequired && item.status !== "applied")
        .map((item) => `高风险或审美决定仍未应用：${item.type}`),
      ...(brief.treatments.broll || brief.treatments.motionGraphics || brief.treatments.music || brief.treatments.generatedMedia
        ? ["增强项尚未获得分项批准，因此未执行"]
        : []),
    ],
    now,
  });
  return {route, profile, brief, manifest, checkpoints, decisionLog, windows, fingerprints, recovery, handoff};
}
