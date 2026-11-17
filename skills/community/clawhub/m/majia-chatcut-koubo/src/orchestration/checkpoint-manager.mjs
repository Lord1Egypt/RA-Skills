export function createCheckpoint({
  manifest,
  planFingerprint = null,
  styleFingerprint = null,
  verifiedEvidence = [],
  completedOperations = [],
  nextSafeAction = manifest.lastSafeAction,
  blockedReason = null,
  now = new Date().toISOString(),
} = {}) {
  const suffix = String(manifest.checkpoints.length + 1).padStart(3, "0");
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/checkpoint.schema.json",
    schemaVersion: "majia.koubo.checkpoint.v1",
    checkpointId: `cp-${manifest.stage.replaceAll("_", "-")}-${suffix}`,
    runId: manifest.runId,
    stage: manifest.stage,
    projectRevision: manifest.project.timelineRevision,
    planFingerprint,
    styleFingerprint,
    verifiedEvidence: [...verifiedEvidence],
    completedOperations: [...completedOperations],
    nextSafeAction,
    blockedReason,
    createdAt: now,
  };
}

export function attachCheckpoint(manifest, checkpoint, now = new Date().toISOString()) {
  if (checkpoint.runId !== manifest.runId || checkpoint.stage !== manifest.stage) {
    throw new Error("CHECKPOINT_RUN_MISMATCH");
  }
  const next = structuredClone(manifest);
  if (!next.checkpoints.includes(checkpoint.checkpointId)) next.checkpoints.push(checkpoint.checkpointId);
  next.lastSafeStage = checkpoint.stage;
  next.lastSafeAction = checkpoint.nextSafeAction;
  next.updatedAt = now;
  return next;
}

export function registerFailure(manifest, signature, now = new Date().toISOString()) {
  if (!/^[A-Z0-9_]+$/u.test(signature)) throw new Error("FAILURE_SIGNATURE_INVALID");
  const next = structuredClone(manifest);
  const count = Math.min(3, (next.failureCounts[signature] ?? 0) + 1);
  next.failureCounts[signature] = count;
  next.updatedAt = now;
  return {
    manifest: next,
    count,
    stop: count >= 3,
    action: count >= 3 ? "return_to_last_checkpoint" : "retry_only_after_new_evidence",
  };
}

export function latestCheckpoint(checkpoints) {
  return [...checkpoints].sort((left, right) => {
    const byTime = Date.parse(right.createdAt) - Date.parse(left.createdAt);
    if (byTime !== 0) return byTime;
    const leftSequence = Number(/-(\d+)$/u.exec(left.checkpointId)?.[1] ?? -1);
    const rightSequence = Number(/-(\d+)$/u.exec(right.checkpointId)?.[1] ?? -1);
    if (rightSequence !== leftSequence) return rightSequence - leftSequence;
    return right.checkpointId.localeCompare(left.checkpointId);
  })[0] ?? null;
}
