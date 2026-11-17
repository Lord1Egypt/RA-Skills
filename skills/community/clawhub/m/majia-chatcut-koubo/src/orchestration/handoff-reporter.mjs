const DISPLAY_STATUS = Object.freeze({
  pass: "PASS",
  fail: "FAIL",
  unverified: "UNVERIFIED",
  stale: "STALE",
  waived: "WAIVED",
  not_applicable: "NOT_APPLICABLE",
  pending: "PENDING",
});

const REQUIRED_EVIDENCE_KIND = Object.freeze({
  structure: "structure-readback",
  visual: "composed-frame",
  audioMeasurement: "audio-measurement",
  humanListening: "human-listening",
  sampleApproval: "sample-approval",
  finalReviewApproval: "final-review-approval",
  privacy: "privacy-review",
});

function uniqueEvidence(evidence) {
  const byRef = new Map();
  for (const item of evidence) {
    if (byRef.has(item.ref) && JSON.stringify(byRef.get(item.ref)) !== JSON.stringify(item)) {
      throw new Error("HANDOFF_EVIDENCE_REF_CONFLICT");
    }
    byRef.set(item.ref, structuredClone(item));
  }
  return [...byRef.values()];
}

function sameSet(left, right) {
  const a = [...new Set(left)].sort();
  const b = [...new Set(right)].sort();
  return a.length === left.length
    && b.length === right.length
    && a.length === b.length
    && a.every((value, index) => value === b[index]);
}

export function buildHandoffReport({
  manifest,
  completed = [],
  notPerformed = ["restructure", "music", "motion-graphics", "broll", "generated-media", "export", "publish"],
  verification = {},
  evidence = [],
  evidenceRefs = [],
  openRisks = [],
  nextActions = ["在 ChatCut 中播放时间线并继续微调"],
  now = new Date().toISOString(),
} = {}) {
  const projectReady = Boolean(manifest.project.projectRef && manifest.project.timelineRef);
  const normalizedEvidence = uniqueEvidence(evidence);
  const derivedEvidenceRefs = normalizedEvidence.map((item) => item.ref);
  if (evidenceRefs.length > 0 && !sameSet(evidenceRefs, derivedEvidenceRefs)) {
    throw new Error("HANDOFF_EVIDENCE_REF_MISMATCH");
  }
  const normalizedCompleted = [...new Set([
    ...completed,
    ...(manifest.stage === "enhancements_ready" ? ["visual-enhancements"] : []),
    ...(manifest.stage === "exported" ? ["export"] : []),
  ])];
  const normalizedNotPerformed = [...new Set(notPerformed)].filter((item) => {
    if (item === "export" && (normalizedCompleted.includes("export") || manifest.stage === "exported")) return false;
    if (["music", "motion-graphics", "broll", "generated-media"].includes(item) && normalizedCompleted.includes("visual-enhancements")) return false;
    return true;
  });
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/handoff-report.schema.json",
    schemaVersion: "majia.koubo.handoff.v1",
    runId: manifest.runId,
    timelineRevision: manifest.project.timelineRevision,
    deliveryState: manifest.status === "blocked"
      ? "blocked"
      : manifest.stage === "sample_ready"
        ? "sample_ready"
        : manifest.stage === "review_ready"
          ? "review_ready"
          : manifest.stage === "exported"
            ? "exported"
            : "in_progress",
    completed: normalizedCompleted,
    notPerformed: normalizedNotPerformed,
    verification: {
      structure: verification.structure ?? "unverified",
      visual: verification.visual ?? "unverified",
      audioMeasurement: verification.audioMeasurement ?? "unverified",
      humanListening: verification.humanListening ?? "unverified",
      sampleApproval: verification.sampleApproval ?? "pending",
      finalReviewApproval: verification.finalReviewApproval ?? "pending",
      privacy: verification.privacy ?? "unverified",
    },
    evidence: normalizedEvidence,
    evidenceRefs: derivedEvidenceRefs,
    openRisks: [...openRisks],
    nextActions: [...nextActions],
    editorHandoff: projectReady
      ? {projectRef: manifest.project.projectRef, timelineRef: manifest.project.timelineRef}
      : null,
    generatedAt: now,
  };
}

function list(items, fallback = "- 无") {
  return items.length > 0 ? items.map((item) => `- ${item}`).join("\n") : fallback;
}

export function renderHandoffMarkdown(report) {
  const verification = Object.entries(report.verification)
    .map(([name, state]) => `- ${name}：${DISPLAY_STATUS[state] ?? state}`)
    .join("\n");
  const provenance = [...new Set(report.evidence.map((item) => item.provenance))];
  return `# 稳剪交付报告\n\n## 已完成\n${list(report.completed)}\n\n## 保护与未执行\n${list(report.notPerformed)}\n\n## 验证\n${verification}\n\n证据来源：${provenance.length > 0 ? provenance.join(", ") : "none"}\n\n## 仍需留意\n${list(report.openRisks)}\n\n## 下一步\n${list(report.nextActions)}\n`;
}

export function assertEvidenceClaims(report) {
  if (!sameSet(report.evidenceRefs ?? [], (report.evidence ?? []).map((item) => item.ref))) {
    throw new Error("HANDOFF_EVIDENCE_REF_MISMATCH");
  }
  for (const item of report.evidence ?? []) {
    if (
      !/^logical:[a-z0-9-]+$/u.test(item.ref ?? "")
      || !/^sha256:[0-9a-f]{64}$/u.test(item.hash ?? "")
      || !["simulation", "live"].includes(item.provenance)
      || !Number.isFinite(Date.parse(item.capturedAt ?? ""))
    ) {
      throw new Error("HANDOFF_EVIDENCE_INVALID");
    }
  }
  for (const [field, kind] of Object.entries(REQUIRED_EVIDENCE_KIND)) {
    if (report.verification[field] !== "pass") continue;
    const candidates = (report.evidence ?? []).filter((item) => item.kind === kind);
    if (candidates.length === 0) {
      throw new Error(`HANDOFF_${field.replace(/([A-Z])/gu, "_$1").toUpperCase()}_EVIDENCE_MISSING`);
    }
    if (!["sample-approval", "final-review-approval"].includes(kind)
      && candidates.every((item) => item.revision !== report.timelineRevision)) {
      throw new Error("HANDOFF_EVIDENCE_REVISION_MISMATCH");
    }
  }
  return true;
}
