import { randomUUID } from "node:crypto";
import { accessSync, constants, lstatSync } from "node:fs";
import { isAbsolute, join } from "node:path";
import { performance } from "node:perf_hooks";

const MAX_MS = 86_400_000;
const KINDS = new Set(["install", "page", "slides", "update"]);
const ARTIFACTS = new Set(["page", "slides"]);
const REASONS = new Set(["first", "expired", "revoked", "account_changed", "scope_changed"]);
const MODULE_FILES = {
  creator: ["SKILL.md", "scripts/validate-html.mjs"],
  publish: ["SKILL.md", "scripts/task-state.mjs"],
};

function exact(value, keys) {
  return value && typeof value === "object" && !Array.isArray(value)
    && Object.keys(value).length === keys.length && keys.every((key) => Object.hasOwn(value, key));
}

function safeDuration(value) {
  const integer = Math.floor(value);
  return Number.isSafeInteger(integer) && integer >= 0 && integer <= MAX_MS ? integer : null;
}

function available(root, module) {
  try {
    const base = join(root, `onimi-pages-${module}`);
    if (!lstatSync(base).isDirectory()) return false;
    if (!lstatSync(join(base, "scripts")).isDirectory()) return false;
    for (const relative of MODULE_FILES[module]) {
      const file = join(base, relative);
      if (!lstatSync(file).isFile()) return false;
      accessSync(file, constants.R_OK);
    }
    return true;
  } catch {
    return false;
  }
}

/**
 * Ephemeral, optional client observer. A host supplies the observed MCP results and a
 * report callback which calls onimi_report_agent_event through its existing connection.
 * This module never acquires credentials or makes a network request.
 */
export function createH08StageObserver({
  locale,
  skillParent,
  report,
  canReport = () => false,
  privacySignals = () => null,
  now = () => performance.now(),
  uuid = randomUUID,
} = {}) {
  if (!["en", "zh-CN"].includes(locale) || typeof skillParent !== "string" || !isAbsolute(skillParent)
    || typeof report !== "function" || typeof canReport !== "function"
    || typeof privacySignals !== "function" || typeof now !== "function") {
    throw new TypeError("Observer requires locale, skillParent and host callbacks.");
  }
  const taskId = uuid();
  const initialModules = Object.fromEntries(Object.keys(MODULE_FILES)
    .map((module) => [module, available(skillParent, module)]));
  const deliveries = new Map();
  const publications = new Map();
  const observedStages = new Set();
  let started = false;
  let agentSince = null;
  let agentElapsed = 0;
  let waitSince = null;
  let waitKind = null;
  let waitElapsed = 0;
  let firstPreview = false;
  let authOpened = false;
  let connected = false;

  function clock() {
    try {
      const value = now();
      return Number.isFinite(value) && value >= 0 ? value : null;
    } catch { return null; }
  }
  function durations() {
    const current = clock();
    if (current === null) return null;
    const agent = safeDuration(agentElapsed + (agentSince === null ? 0 : current - agentSince));
    const waiting = safeDuration(waitElapsed + (waitSince === null ? 0 : current - waitSince));
    return agent === null || waiting === null ? null : { agent, waiting };
  }
  function beginWait(kind) {
    const current = clock();
    if (!started || current === null || agentSince === null || waitSince !== null) return false;
    agentElapsed += current - agentSince;
    agentSince = null;
    waitSince = current;
    waitKind = kind;
    return true;
  }
  function endWait(kind) {
    const current = clock();
    if (waitSince === null || waitKind !== kind || current === null) return false;
    waitElapsed += current - waitSince;
    waitSince = null;
    waitKind = null;
    agentSince = current;
    return true;
  }
  function permitted() {
    try {
      const signals = privacySignals();
      return canReport() === true && signals?.dnt === false && signals?.gpc === false;
    } catch { return false; }
  }
  async function send(eventName, fields, operationId = uuid()) {
    if (!permitted()) return null;
    const payload = { locale, taskId, operationId, reportId: uuid(), eventName, fields };
    deliveries.set(payload.reportId, { payload, attempted: false, uncertain: false });
    await deliver(payload.reportId);
    return payload;
  }
  async function deliver(reportId) {
    const entry = deliveries.get(reportId);
    if (!entry || (entry.attempted && !entry.uncertain) || !permitted()) return false;
    entry.attempted = true;
    entry.uncertain = false;
    try {
      const receipt = await report(entry.payload);
      entry.uncertain = receipt?.deliveryUncertain === true
        || (receipt?.recorded !== true && receipt?.duplicate !== true
          && receipt?.deliveryUncertain !== false);
      return receipt?.recorded === true || receipt?.duplicate === true;
    } catch {
      entry.uncertain = true;
      return false;
    }
  }
  return {
    taskId,
    retryDelivery: deliver,
    async startTask(taskKind) {
      if (started || !KINDS.has(taskKind)) return null;
      const current = clock();
      if (current === null) return null;
      started = true;
      agentSince = current;
      return send("onimi.task.started", { task_kind: taskKind });
    },
    async capabilityReady(module) {
      if (!started || !["creator", "publish", "suite"].includes(module)) return null;
      const members = module === "suite" ? ["creator", "publish"] : [module];
      if (!members.every((name) => available(skillParent, name))) return null;
      if (observedStages.has(`capability:${module}`)) return null;
      observedStages.add(`capability:${module}`);
      return send("onimi.capability.ready", {
        module, reused: members.every((name) => initialModules[name]),
      });
    },
    async authorizationOpened(reason) {
      if (!started || authOpened || !REASONS.has(reason)) return null;
      if (!beginWait("authorization")) return null;
      authOpened = true;
      // First authorization normally has no bearer. Never queue it for later.
      return send("onimi.authorization.waiting", { reason });
    },
    async connectionResult({ response, expectedActor, requiredScopes, state } = {}) {
      if (!started || connected || !["reused", "after_authorization"].includes(state)
        || (state === "after_authorization") !== authOpened
        || !exact(expectedActor, ["userId", "accountId"])
        || !Object.values(expectedActor).every((value) => typeof value === "string" && value.length > 0)
        || !Array.isArray(requiredScopes) || !requiredScopes.every((scope) => typeof scope === "string")
        || response?.connected !== true || !exact(response.actor, ["userId", "accountId"])
        || response.actor.userId !== expectedActor.userId
        || response.actor.accountId !== expectedActor.accountId
        || !Array.isArray(response.scopes)
        || !requiredScopes.every((scope) => response.scopes.includes(scope))) return null;
      if (authOpened && !endWait("authorization")) return null;
      connected = true;
      return send("onimi.connection.result", { result: "ready", reused: state === "reused" });
    },
    userWaitStarted() { return beginWait("user"); },
    userWaitEnded() { return endWait("user"); },
    async firstVisiblePreview(receipt) {
      if (!started || firstPreview || !exact(receipt, ["visible", "firstForTask", "artifactKind"])
        || receipt.visible !== true || receipt.firstForTask !== true
        || !ARTIFACTS.has(receipt.artifactKind)) return null;
      const elapsed = durations();
      if (!elapsed || waitSince !== null) return null;
      firstPreview = true;
      return send("onimi.preview.first", {
        artifact_kind: receipt.artifactKind,
        agent_ms: elapsed.agent,
        user_wait_ms: elapsed.waiting,
      });
    },
    beginPublication({ businessMutationId, kind, projectId, publicationId } = {}) {
      if (!started || !connected || !["prepare", "activate"].includes(kind)
        || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(businessMutationId ?? "")
        || typeof projectId !== "string" || !projectId
        || (kind === "activate" && (typeof publicationId !== "string" || !publicationId))
        || [...publications.values()].some((item) => item.businessMutationId === businessMutationId)) return null;
      const current = clock();
      if (current === null || waitSince !== null) return null;
      let operationId = uuid();
      for (let attempt = 0; attempt < 3 && (operationId === businessMutationId || publications.has(operationId)); attempt += 1) {
        operationId = uuid();
      }
      if (operationId === businessMutationId || publications.has(operationId)) return null;
      publications.set(operationId, {
        kind, projectId, publicationId, businessMutationId, since: current, initialWait: waitElapsed,
        attempts: 0, definite: false,
      });
      return operationId;
    },
    publicationAttempt(operationId, businessMutationId) {
      const operation = publications.get(operationId);
      if (!operation || operation.definite || operation.attempts >= 16
        || operation.businessMutationId !== businessMutationId) return false;
      operation.attempts += 1;
      return true;
    },
    async publicationResponse({ operationId, response } = {}) {
      const operation = publications.get(operationId);
      if (!operation || operation.definite || operation.attempts === 0) return null;
      // Only the exact operation's parsed business response is accepted. Transport errors,
      // timeouts, 202 wrappers and status reads are not definite publication results.
      if (!response || typeof response !== "object" || Array.isArray(response)
        || Object.keys(response).some((key) => /^(?:token|cookie|authorization|secret|email|prompt|source|body)$/i.test(key))
        || response.idempotencyKey !== operation.businessMutationId
        || typeof response.idempotentReplay !== "boolean"
        || response.projectId !== operation.projectId
        || typeof response.publicationId !== "string" || !response.publicationId
        || (operation.publicationId && response.publicationId !== operation.publicationId)) return null;
      const result = operation.kind === "prepare" && response.status === "pending-review" ? "pending"
        : operation.kind === "activate" && response.status === "active" ? "active" : null;
      if (result === null) return null;
      const current = clock();
      const currentWait = waitElapsed + (waitSince === null || current === null ? 0 : current - waitSince);
      const agentMs = current === null ? null
        : safeDuration(current - operation.since - (currentWait - operation.initialWait));
      if (agentMs === null) return null;
      operation.definite = true;
      return send("onimi.publication.result", {
        result, retry: operation.attempts > 1, agent_ms: agentMs,
      }, operationId);
    },
  };
}
