import {
  contentHash,
} from "../planning/preview-approval.mjs";

export class ExecutionError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "ExecutionError";
    this.code = code;
  }
}

export class AmbiguousWriteError extends ExecutionError {
  constructor(message = "write outcome is ambiguous") {
    super("EXEC_WRITE_AMBIGUOUS", message);
    this.name = "AmbiguousWriteError";
  }
}

function clone(value) {
  return structuredClone(value);
}

function entryFor(operation, attempt) {
  return {
    entryId: `entry_${operation.operationId.replace(/^operation_/u, "")}_${attempt}`,
    operationId: operation.operationId,
    sceneId: operation.sceneId,
    idempotencyKey: operation.idempotencyKey,
    logicalId: operation.logicalId,
    attempt,
    result: "started",
    expectedHash: operation.desiredHash,
    observedHash: null,
    reconciliation: "none",
    evidenceRef: null,
    errorCode: null,
  };
}

function evidenceFor(operation, observedHash) {
  return {
    evidenceId: `evidence_${operation.operationId}`,
    kind: "timeline-readback",
    targetRef: operation.logicalId,
    path: null,
    sha256: observedHash,
    result: "passed",
    sensitive: false,
    checks: [
      "READBACK_MATCH",
      "REVISION_LOCK",
    ],
    dependencies: [
      operation.operationId,
    ],
    invalidatedBy: [],
  };
}

function checkpointFor(operation, revision, evidenceRefs) {
  return {
    checkpointId: `checkpoint_${operation.sceneId}`,
    sceneId: operation.sceneId,
    lastOperationId: operation.operationId,
    timelineRevision: revision,
    evidenceRefs,
  };
}

function createJournal(plan) {
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/operation-journal.schema.json",
    schemaVersion: "1.0.0",
    journalId: `journal_${plan.runId.replace(/^run_/u, "")}`,
    projectId: plan.projectId,
    runId: plan.runId,
    planHash: plan.planHash,
    baseTimelineRevision: plan.timelineRevision,
    currentTimelineRevision: plan.timelineRevision,
    status: "planned",
    entries: [],
    checkpoints: [],
  };
}

function createEvidenceManifest(plan) {
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/evidence-manifest.schema.json",
    schemaVersion: "1.0.0",
    projectId: plan.projectId,
    runId: plan.runId,
    timelineRevision: plan.timelineRevision,
    artifacts: [],
  };
}

function unique(items) {
  return new Set(items).size === items.length;
}

function auditExecutionPlan(plan) {
  if (!plan || !Array.isArray(plan.operations) || plan.operations.length === 0) {
    throw new ExecutionError(
      "EXEC_PLAN_INVALID",
      "execution plan must contain operations",
    );
  }
  if (!unique(plan.operations.map((item) => item.operationId))) {
    throw new ExecutionError(
      "EXEC_OPERATION_DUPLICATE",
      "operation IDs must be unique",
    );
  }
  if (!unique(plan.operations.map((item) => item.idempotencyKey))) {
    throw new ExecutionError(
      "EXEC_IDEMPOTENCY_DUPLICATE",
      "idempotency keys must be unique",
    );
  }
  for (const operation of plan.operations) {
    if (contentHash(operation.desiredState) !== operation.desiredHash) {
      throw new ExecutionError(
        "EXEC_DESIRED_HASH_MISMATCH",
        "operation desired state differs from its hash",
      );
    }
  }
}

function auditExecutionGate(executionPlan, approvalReport, executionGate) {
  if (approvalReport?.canExecute) return;
  if (
    executionGate?.kind !== "bounded-sample"
    || executionGate.canExecute !== true
    || executionGate.planHash !== executionPlan.planHash
    || executionGate.timelineRevision !== executionPlan.timelineRevision
    || !Array.isArray(executionGate.scope)
    || executionGate.scope.length === 0
  ) {
    throw new ExecutionError(
      "EXEC_PREVIEW_NOT_APPROVED",
      "execution requires either current preview approval or a bounded sample gate",
    );
  }
  const allowedScope = new Set(executionGate.scope);
  for (const operation of executionPlan.operations) {
    if (
      !["low", "medium"].includes(operation.risk)
      || !operation.scopeRef
      || !allowedScope.has(operation.scopeRef)
    ) {
      throw new ExecutionError(
        "EXEC_SAMPLE_GATE_SCOPE_INVALID",
        "bounded sample execution cannot include high-risk or out-of-scope operations",
      );
    }
  }
}

function requireUniqueBinding(objects) {
  if (objects.length > 1) {
    throw new ExecutionError(
      "EXEC_BINDING_AMBIGUOUS",
      "logical ID resolves to multiple host objects",
    );
  }
}

function stateMatches(objects, desiredHash) {
  return objects.length === 1 && objects[0].hash === desiredHash;
}

function stateMatchesSnapshot(objects, snapshot) {
  if (objects.length !== snapshot.length) return false;
  const current = objects.map((item) => `${item.hostId}:${item.hash}`).sort();
  const before = snapshot.map((item) => `${item.hostId}:${item.hash}`).sort();
  return current.every((value, index) => value === before[index]);
}

export class FakeTimelineAdapter {
  constructor({revision = "rev_demo", objects = []} = {}) {
    this.revision = revision;
    this.revisionCounter = 0;
    this.hostCounter = 0;
    this.objects = new Map();
    this.idempotency = new Map();
    this.failures = new Map();
    for (const item of objects) this.#store(item);
  }

  #store(item) {
    this.objects.set(item.hostId, clone(item));
    const match = /^host_(\d+)$/u.exec(item.hostId);
    if (match) this.hostCounter = Math.max(this.hostCounter, Number(match[1]));
  }

  #bumpRevision() {
    this.revisionCounter += 1;
    this.revision = `rev_host_${this.revisionCounter}`;
  }

  #takeFailure(operationId, type) {
    const configured = this.failures.get(operationId) ?? [];
    const index = configured.indexOf(type);
    if (index === -1) return false;
    configured.splice(index, 1);
    return true;
  }

  injectFailure(operationId, type) {
    const configured = this.failures.get(operationId) ?? [];
    configured.push(type);
    this.failures.set(operationId, configured);
  }

  getRevision() {
    return this.revision;
  }

  beforeOperation(operation) {
    if (this.#takeFailure(operation.operationId, "revision-drift")) {
      this.#bumpRevision();
    }
  }

  readLogical(logicalId) {
    return [...this.objects.values()]
      .filter((item) => item.logicalId === logicalId)
      .map(clone);
  }

  apply(operation) {
    if (this.#takeFailure(operation.operationId, "timeout-before-commit")) {
      throw new AmbiguousWriteError();
    }
    const rememberedHostId = this.idempotency.get(operation.idempotencyKey);
    if (rememberedHostId && this.objects.has(rememberedHostId)) {
      return clone(this.objects.get(rememberedHostId));
    }
    if (rememberedHostId) this.idempotency.delete(operation.idempotencyKey);

    const existing = this.readLogical(operation.logicalId);
    requireUniqueBinding(existing);
    let hostId = existing[0]?.hostId;
    if (!hostId || this.#takeFailure(operation.operationId, "id-change")) {
      if (hostId) this.objects.delete(hostId);
      this.hostCounter += 1;
      hostId = `host_${this.hostCounter}`;
    }
    const partial = this.#takeFailure(operation.operationId, "partial-write");
    const state = partial
      ? {partial: true}
      : clone(operation.desiredState);
    const stored = {
      hostId,
      logicalId: operation.logicalId,
      state,
      hash: contentHash(state),
    };
    this.#store(stored);
    this.idempotency.set(operation.idempotencyKey, hostId);
    this.#bumpRevision();
    if (this.#takeFailure(operation.operationId, "timeout-after-commit")) {
      throw new AmbiguousWriteError();
    }
    return clone(stored);
  }

  compensate(logicalId, snapshot) {
    for (const item of this.readLogical(logicalId)) {
      this.objects.delete(item.hostId);
    }
    for (const item of snapshot) this.#store(item);
    for (const [key, hostId] of this.idempotency.entries()) {
      if (!this.objects.has(hostId)) this.idempotency.delete(key);
    }
    this.#bumpRevision();
  }

  objectCount() {
    return this.objects.size;
  }
}

export class RecoverableExecutor {
  constructor(adapter) {
    this.adapter = adapter;
  }

  execute({
    executionPlan,
    approvalReport,
    executionGate,
    journal: suppliedJournal,
    evidenceManifest: suppliedEvidence,
  }) {
    auditExecutionPlan(executionPlan);
    auditExecutionGate(executionPlan, approvalReport, executionGate);
    const journal = suppliedJournal
      ? clone(suppliedJournal)
      : createJournal(executionPlan);
    const evidenceManifest = suppliedEvidence
      ? clone(suppliedEvidence)
      : createEvidenceManifest(executionPlan);
    if (
      journal.planHash !== executionPlan.planHash
      || journal.projectId !== executionPlan.projectId
      || journal.runId !== executionPlan.runId
    ) {
      throw new ExecutionError(
        "EXEC_JOURNAL_PLAN_MISMATCH",
        "journal cannot resume a different execution plan",
      );
    }
    const expectedRevision = suppliedJournal
      ? journal.currentTimelineRevision
      : executionPlan.timelineRevision;
    if (this.adapter.getRevision() !== expectedRevision) {
      throw new ExecutionError(
        "EXEC_REVISION_DRIFT",
        "timeline revision changed outside the executor",
      );
    }
    journal.status = "running";
    let activeSceneId = null;
    let sceneSnapshots = new Map();

    for (const [index, operation] of executionPlan.operations.entries()) {
      if (operation.sceneId !== activeSceneId) {
        activeSceneId = operation.sceneId;
        sceneSnapshots = new Map();
        for (const sceneOperation of executionPlan.operations.filter(
          (candidate) => candidate.sceneId === activeSceneId,
        )) {
          if (!sceneSnapshots.has(sceneOperation.logicalId)) {
            const snapshot = this.adapter.readLogical(sceneOperation.logicalId);
            requireUniqueBinding(snapshot);
            sceneSnapshots.set(sceneOperation.logicalId, clone(snapshot));
          }
        }
      }
      const verified = [...journal.entries]
        .reverse()
        .find((item) =>
          item.operationId === operation.operationId
          && item.result === "verified",
        );
      const current = this.adapter.readLogical(operation.logicalId);
      requireUniqueBinding(current);
      if (verified && stateMatches(current, operation.desiredHash)) continue;

      const attempt =
        journal.entries.filter(
          (item) => item.operationId === operation.operationId,
        ).length + 1;
      const entry = entryFor(operation, attempt);
      journal.entries.push(entry);
      const before = clone(current);
      try {
        this.adapter.beforeOperation(operation);
        if (this.adapter.getRevision() !== journal.currentTimelineRevision) {
          throw new ExecutionError(
            "EXEC_REVISION_DRIFT",
            "timeline revision changed outside the executor",
          );
        }
        let reconciliation = "none";
        try {
          this.adapter.apply(operation);
        } catch (error) {
          if (!(error instanceof AmbiguousWriteError)) throw error;
          let observed = this.adapter.readLogical(operation.logicalId);
          requireUniqueBinding(observed);
          if (stateMatches(observed, operation.desiredHash)) {
            reconciliation = "readback";
          } else if (stateMatchesSnapshot(observed, before)) {
            reconciliation = "retry";
            this.adapter.apply(operation);
          } else {
            throw new ExecutionError(
              "EXEC_AMBIGUOUS_PARTIAL_WRITE",
              "ambiguous write produced an unrecognized partial state",
            );
          }
        }
        const observed = this.adapter.readLogical(operation.logicalId);
        requireUniqueBinding(observed);
        if (!stateMatches(observed, operation.desiredHash)) {
          throw new ExecutionError(
            "EXEC_POSTCONDITION_FAILED",
            "timeline readback does not match the planned state",
          );
        }
        entry.result = "verified";
        entry.observedHash = observed[0].hash;
        entry.reconciliation = reconciliation;
        entry.evidenceRef = `evidence_${operation.operationId}`;
        journal.currentTimelineRevision = this.adapter.getRevision();
        const artifact = evidenceFor(operation, observed[0].hash);
        evidenceManifest.artifacts = evidenceManifest.artifacts.filter(
          (item) => item.evidenceId !== artifact.evidenceId,
        );
        evidenceManifest.artifacts.push(artifact);
        evidenceManifest.timelineRevision = journal.currentTimelineRevision;

        const next = executionPlan.operations[index + 1];
        if (!next || next.sceneId !== operation.sceneId) {
          const sceneEvidence = evidenceManifest.artifacts
            .filter((item) => executionPlan.operations.some(
              (candidate) =>
                candidate.sceneId === operation.sceneId
                && item.dependencies?.includes(candidate.operationId),
            ))
            .map((item) => item.evidenceId);
          journal.checkpoints = journal.checkpoints.filter(
            (item) => item.sceneId !== operation.sceneId,
          );
          journal.checkpoints.push(checkpointFor(
            operation,
            journal.currentTimelineRevision,
            sceneEvidence,
          ));
        }
      } catch (error) {
        const code = error instanceof ExecutionError
          ? error.code
          : "EXEC_ADAPTER_FAILED";
        const observed = this.adapter.readLogical(operation.logicalId);
        entry.observedHash = observed[0]?.hash ?? null;
        let compensated = false;
        for (const [logicalId, snapshot] of sceneSnapshots.entries()) {
          const currentState = this.adapter.readLogical(logicalId);
          if (!stateMatchesSnapshot(currentState, snapshot)) {
            this.adapter.compensate(logicalId, snapshot);
            compensated = true;
          }
        }
        if (compensated) {
          const sceneOperationIds = new Set(
            executionPlan.operations
              .filter((candidate) => candidate.sceneId === operation.sceneId)
              .map((candidate) => candidate.operationId),
          );
          for (const sceneEntry of journal.entries) {
            if (
              sceneEntry.sceneId === operation.sceneId
              && sceneEntry.result === "verified"
            ) {
              sceneEntry.result = "compensated";
              sceneEntry.reconciliation = "compensated";
              sceneEntry.errorCode = "EXEC_SCENE_COMPENSATED";
            }
          }
          entry.result = "compensated";
          entry.reconciliation = "compensated";
          journal.currentTimelineRevision = this.adapter.getRevision();
          evidenceManifest.artifacts = evidenceManifest.artifacts.filter(
            (artifact) => !(artifact.dependencies ?? []).some(
              (dependency) => sceneOperationIds.has(dependency),
            ),
          );
        } else {
          entry.result = "failed";
        }
        entry.errorCode = code;
        journal.status = "failed";
        evidenceManifest.timelineRevision = journal.currentTimelineRevision;
        return {
          status: "failed",
          errorCode: code,
          journal,
          evidenceManifest,
        };
      }
    }
    journal.status = "completed";
    return {
      status: "completed",
      errorCode: null,
      journal,
      evidenceManifest,
    };
  }
}

export function invalidateEvidence(evidenceManifest, changedDependencies) {
  const result = clone(evidenceManifest);
  const invalid = new Set(changedDependencies);
  let changed = true;
  while (changed) {
    changed = false;
    for (const artifact of result.artifacts) {
      if (
        artifact.result === "passed"
        && (artifact.dependencies ?? []).some(
          (dependency) => invalid.has(dependency),
        )
      ) {
        artifact.result = "unverified";
        artifact.invalidatedBy = [...new Set([
          ...(artifact.invalidatedBy ?? []),
          ...(artifact.dependencies ?? []).filter(
            (dependency) => invalid.has(dependency),
          ),
        ])];
        invalid.add(artifact.evidenceId);
        changed = true;
      }
    }
  }
  return result;
}
