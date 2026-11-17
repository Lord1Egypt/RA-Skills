#!/usr/bin/env node

import { createHash, randomUUID } from "node:crypto";
import {
  chmodSync,
  closeSync,
  constants,
  existsSync,
  lstatSync,
  mkdirSync,
  openSync,
  readFileSync,
  readdirSync,
  renameSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { homedir } from "node:os";
import { basename, dirname, isAbsolute, join, resolve } from "node:path";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const SHA256 = /^[0-9a-f]{64}$/;
const SAFE_TOKEN = /^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,255}$/;
const RESOURCE_TYPES = new Set(["example", "scenario", "pattern", "template", "theme"]);

const STEP_RULES = {
  createProject: {
    references: ["artifactKind", "projectSlug", "requestedVisibility"],
    required: ["artifactKind", "projectSlug", "requestedVisibility"],
    receipt: ["projectId", "projectSlug", "rowVersion", "artifactKind", "visibility"],
    receiptRequired: ["projectId", "rowVersion"],
    retry: "same-mutation-and-request",
  },
  acquireResource: {
    references: [
      "projectId",
      "resourceType",
      "resourceKey",
      "resourceVersion",
      "locale",
      "themeKey",
      "themeVersion",
    ],
    receiptRequired: ["resourceType", "resourceKey", "resourceVersion", "sha256"],
    required: ["resourceType", "resourceKey", "resourceVersion", "locale"],
    receipt: [
      "resourceType",
      "resourceKey",
      "resourceVersion",
      "locale",
      "themeKey",
      "themeVersion",
      "sha256",
      "bytes",
    ],
    retry: "safe-read",
    readOnly: true,
  },
  saveDraft: {
    references: ["projectId", "expectedRevision", "sourceSha256", "manifestSha256"],
    required: ["projectId", "expectedRevision"],
    receipt: ["projectId", "revisionId", "revision", "sourceSha256"],
    receiptRequired: ["projectId", "revisionId", "revision", "sourceSha256"],
    retry: "same-mutation-and-request",
  },
  configureParticipation: {
    references: [
      "projectId",
      "expectedVersion",
      "mode",
      "identityPolicy",
      "ownerVisibility",
      "manifestSha256",
      "collectionKey",
      "batchKey",
      "formVersion",
    ],
    required: ["projectId", "expectedVersion", "mode", "identityPolicy", "ownerVisibility", "manifestSha256"],
    receipt: [
      "projectId",
      "configId",
      "version",
      "manifestSha256",
      "latestVersion",
      "activeVersion",
    ],
    receiptRequired: ["projectId", "configId", "version", "manifestSha256"],
    retry: "same-mutation-and-request",
  },
  setParticipationLifecycle: {
    references: ["projectId", "configVersion", "writeState", "externalAccess"],
    required: ["projectId", "configVersion", "writeState", "externalAccess"],
    receipt: ["projectId", "version", "writeState", "externalAccess", "operationalVersion"],
    receiptRequired: ["projectId", "version", "writeState", "externalAccess"],
    retry: "same-mutation-and-request",
  },
  createGrant: {
    references: [
      "projectId",
      "participationConfigVersion",
      "deliveryKind",
      "role",
      "identityMode",
      "expiresAt",
    ],
    required: ["projectId", "participationConfigVersion", "deliveryKind", "role", "identityMode"],
    receipt: ["projectId", "grantId", "grantVersion", "status", "expiresAt"],
    receiptRequired: ["projectId", "grantId", "grantVersion"],
    retry: "same-mutation-and-request",
  },
  publishHtml: {
    references: ["projectId", "projectSlug", "filename", "htmlSha256"],
    required: ["projectId", "filename", "htmlSha256"],
    receipt: ["projectId", "publicationId", "releaseId", "version", "status", "sourceSha256"],
    receiptRequired: ["projectId", "status"],
    retry: "same-mutation-and-request",
  },
  preparePublication: {
    references: [
      "projectId",
      "sourceDraftRevisionId",
      "sourceSha256",
      "expectedPolicyEpoch",
      "expectedActiveReleaseId",
      "participationConfigVersion",
    ],
    receiptRequired: ["projectId", "publicationId", "status", "sourceDraftRevisionId", "sourceSha256"],
    required: [
      "projectId",
      "sourceDraftRevisionId",
      "sourceSha256",
      "expectedPolicyEpoch",
      "expectedActiveReleaseId",
    ],
    receipt: [
      "projectId",
      "publicationId",
      "status",
      "sourceDraftRevisionId",
      "sourceSha256",
      "policyEpoch",
      "participationConfigVersion",
    ],
    retry: "same-mutation-and-request",
  },
  activatePublication: {
    references: ["projectId", "publicationId", "expectedActiveReleaseId"],
    required: ["projectId", "publicationId", "expectedActiveReleaseId"],
    receipt: ["projectId", "publicationId", "releaseId", "activeReleaseId", "status", "version"],
    receiptRequired: ["projectId", "publicationId", "status"],
    retry: "same-mutation-and-request",
  },
  setVisibility: {
    references: ["projectId", "visibility", "expectedRowVersion", "expectedVisibility"],
    required: ["projectId", "visibility", "expectedRowVersion", "expectedVisibility"],
    receipt: ["projectId", "visibility", "rowVersion"],
    receiptRequired: ["projectId", "visibility", "rowVersion"],
    retry: "same-mutation-and-request",
  },
};

function fail(message) {
  throw new Error(message);
}

function args() {
  const [command, ...rest] = process.argv.slice(2);
  const options = {};
  for (let index = 0; index < rest.length; index += 2) {
    const key = rest[index];
    const value = rest[index + 1];
    if (!key?.startsWith("--") || value === undefined) fail("Options must use --name value pairs.");
    options[key.slice(2)] = value;
  }
  return { command, options };
}

function strictObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) fail(`${label} must be an object.`);
  return value;
}

function onlyKeys(value, allowed, label) {
  const object = strictObject(value, label);
  const unknown = Object.keys(object).filter((key) => !allowed.includes(key));
  if (unknown.length) fail(`${label} has unsupported fields: ${unknown.join(", ")}.`);
  return object;
}

function readJson(path, label) {
  if (!path || !isAbsolute(path)) fail(`${label} path must be absolute.`);
  const stat = lstatSync(path);
  if (!stat.isFile() || stat.isSymbolicLink()) fail(`${label} must be a regular file, not a symlink.`);
  const descriptor = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
  try {
    const bytes = readFileSync(descriptor);
    if (bytes.length > 32_768) fail(`${label} is too large.`);
    return JSON.parse(bytes.toString("utf8"));
  } finally {
    closeSync(descriptor);
  }
}

function stateDirectory(override) {
  if (override && !isAbsolute(override)) fail("State directory must be absolute.");
  const base = override
    ? resolve(override)
    : join(process.env.XDG_STATE_HOME || join(homedir(), ".local", "state"), "onimi-pages", "tasks");
  if (!isAbsolute(base)) fail("State directory must be absolute.");
  mkdirSync(base, { recursive: true, mode: 0o700 });
  chmodSync(base, 0o700);
  return base;
}

function statePath(taskId, stateDir) {
  if (!UUID.test(taskId || "")) fail("taskId must be a UUID.");
  return join(stateDirectory(stateDir), `${taskId}.json`);
}

function readState(path) {
  const state = readJson(path, "Task state");
  if (state.schemaVersion !== 1 || !UUID.test(state.taskId || "")) fail("Task state is invalid.");
  chmodSync(path, 0o600);
  return state;
}

function writeState(path, state) {
  const lock = `${path}.lock`;
  try {
    mkdirSync(lock, { mode: 0o700 });
  } catch (error) {
    if (error.code === "EEXIST") fail("Task state is locked by another process; retry after it finishes.");
    throw error;
  }
  const temporary = join(dirname(path), `.${basename(path)}.${process.pid}.${randomUUID()}.tmp`);
  try {
    state.updatedAt = new Date().toISOString();
    writeFileSync(temporary, `${JSON.stringify(state, null, 2)}\n`, { mode: 0o600, flag: "wx" });
    chmodSync(temporary, 0o600);
    renameSync(temporary, path);
    chmodSync(path, 0o600);
  } finally {
    rmSync(temporary, { force: true });
    rmSync(lock, { recursive: true, force: true });
  }
}

function withActivationPlanLock(directory, action) {
  const lock = join(directory, ".activate-publication-plan.lock");
  try {
    mkdirSync(lock, { mode: 0o700 });
  } catch (error) {
    if (error.code === "EEXIST") fail("Activation planning is locked by another process; retry this plan.");
    throw error;
  }
  try {
    return action();
  } finally {
    rmSync(lock, { recursive: true, force: true });
  }
}

function assertActivationNotJournaled(directory, taskId, references) {
  const matches = [];
  for (const name of readdirSync(directory)) {
    if (!UUID.test(name.slice(0, -5)) || !name.endsWith(".json")) continue;
    const otherTaskId = name.slice(0, -5);
    if (otherTaskId === taskId) continue;
    const other = readJson(join(directory, name), "Activation journal");
    if (other.schemaVersion !== 1 || other.taskId !== otherTaskId ||
        !other.operations || typeof other.operations !== "object") {
      fail("An activation journal is invalid; resolve it before planning another activation.");
    }
    const existing = other.operations.activatePublication;
    if (existing?.references?.projectId === references.projectId &&
        existing.references.publicationId === references.publicationId) {
      matches.push(otherTaskId);
    }
  }
  if (matches.length) {
    fail(`Activation is already journaled in task(s) ${matches.slice(0, 8).join(", ")}${matches.length > 8 ? ` and ${matches.length - 8} more` : ""}; reconcile the original mutation IDs before another activation.`);
  }
}

function safeScalar(value, label) {
  if (value === null || typeof value === "boolean") return value;
  if (typeof value === "number" && Number.isSafeInteger(value)) return value;
  if (typeof value === "string" && value.length <= 256 && SAFE_TOKEN.test(value)) return value;
  fail(`${label} must be a short identifier, enum, integer or null.`);
}

function safeSummary(value) {
  if (typeof value !== "string" || value.length < 1 || value.length > 80 || /[\r\n]/.test(value)) {
    fail("summary must be one short line of at most 80 characters.");
  }
  if (/https?:\/\/|(?:bearer|token|secret|password)\s*[:=]/i.test(value)) {
    fail("summary cannot contain a URL or credential-like material.");
  }
  return value;
}

function sanitizedRecord(value, allowed, required, label) {
  const object = onlyKeys(value, allowed, label);
  for (const key of required) if (!(key in object)) fail(`${label}.${key} is required.`);
  const result = {};
  for (const key of allowed) {
    if (!(key in object)) continue;
    result[key] = safeScalar(object[key], `${label}.${key}`);
  }
  return result;
}

function validateSelection(value) {
  if (value === undefined) return undefined;
  const selection = sanitizedRecord(
    value,
    ["resourceType", "resourceKey", "resourceVersion", "locale", "themeKey", "themeVersion"],
    ["resourceType", "resourceKey", "resourceVersion", "locale"],
    "selection",
  );
  if (!RESOURCE_TYPES.has(selection.resourceType)) fail("selection.resourceType is unsupported.");
  if ((selection.themeKey === undefined) !== (selection.themeVersion === undefined)) {
    fail("selection.themeKey and selection.themeVersion must be supplied together.");
  }
  return selection;
}

function validateTarget(value) {
  const target = sanitizedRecord(
    value,
    ["mode", "projectId", "projectSlug", "requestedVisibility"],
    ["mode"],
    "target",
  );
  if (!new Set(["create", "update"]).has(target.mode)) fail("target.mode must be create or update.");
  if (target.mode === "update" && !UUID.test(target.projectId || "")) {
    fail("An update target requires an exact projectId UUID.");
  }
  if (target.mode === "create" && target.projectId !== undefined) fail("A create target cannot start with projectId.");
  if (target.mode === "create") {
    if (typeof target.projectSlug !== "string" || !target.projectSlug) {
      fail("A create target requires the confirmed projectSlug.");
    }
    if (!["private", "unlisted", "public"].includes(target.requestedVisibility)) {
      fail("A create target requires the confirmed requestedVisibility.");
    }
  }
  return target;
}

function plan(state, input) {
  onlyKeys(input, ["step", "requestSha256", "references", "mutationId"], "Plan input");
  const rule = STEP_RULES[input.step];
  if (!rule) fail("Plan input.step is unsupported.");
  if (input.step === "createProject" && state.target.mode !== "create") {
    fail("createProject is allowed only for a confirmed create target.");
  }
  if (!SHA256.test(input.requestSha256 || "")) fail("Plan input.requestSha256 must be lowercase SHA-256.");
  const references = sanitizedRecord(input.references, rule.references, rule.required, "Plan references");
  if (input.step === "createProject") {
    if (
      references.artifactKind !== state.artifactKind ||
      references.projectSlug !== state.target.projectSlug ||
      references.requestedVisibility !== state.target.requestedVisibility
    ) {
      fail("Project creation does not match the confirmed task target.");
    }
  } else if (references.projectId) {
    if (!state.target.projectId || references.projectId !== state.target.projectId) {
      fail("Plan references a project other than this task target.");
    }
  } else if (input.step !== "acquireResource") {
    fail("Plan requires the confirmed projectId for this task.");
  }
  const existing = state.operations[input.step];
  if (existing) {
    if (
      input.step === "preparePublication" &&
      existing.status === "failed" &&
      existing.failure?.code === "PARTICIPATION_CONFIG_CONFLICT"
    ) {
      fail("A definite participation configuration conflict cannot be replayed; use replan.");
    }
    const same =
      existing.requestSha256 === input.requestSha256 &&
      JSON.stringify(existing.references) === JSON.stringify(references);
    if (!same) fail("This step already has a different durable request; start a new task for changed bytes or references.");
    return existing;
  }
  const mutationId = rule.readOnly ? null : input.mutationId || randomUUID();
  if (mutationId !== null && !UUID.test(mutationId)) fail("Plan input.mutationId must be a UUID.");
  const operation = {
    status: "planned",
    mutationId,
    requestSha256: input.requestSha256,
    references,
    retry: rule.retry,
    plannedAt: new Date().toISOString(),
  };
  state.operations[input.step] = operation;
  return operation;
}

function replanPublication(state, input) {
  onlyKeys(
    input,
    ["step", "supersedesMutationId", "mutationId", "requestSha256", "references", "readback"],
    "Replan input",
  );
  if (input.step !== "preparePublication") fail("Only a failed publication preparation can be replanned.");
  const rule = STEP_RULES.preparePublication;
  const previous = state.operations.preparePublication;
  if (!previous) fail("Publication preparation has not been planned.");
  if (!UUID.test(input.supersedesMutationId || "") || !UUID.test(input.mutationId || "")) {
    fail("Replan requires the previous and a new mutationId UUID.");
  }
  if (!SHA256.test(input.requestSha256 || "")) fail("Replan requestSha256 must be lowercase SHA-256.");
  const references = sanitizedRecord(input.references, rule.references, rule.required, "Replan references");
  const readback = sanitizedRecord(
    input.readback,
    ["latestConfigVersion", "activeReleaseId", "publicationCountBefore", "publicationCountAfter"],
    ["latestConfigVersion", "activeReleaseId", "publicationCountBefore", "publicationCountAfter"],
    "Replan readback",
  );
  const sameReplan =
    previous.supersedesMutationId === input.supersedesMutationId &&
    previous.mutationId === input.mutationId &&
    previous.requestSha256 === input.requestSha256 &&
    JSON.stringify(previous.references) === JSON.stringify(references) &&
    JSON.stringify(previous.reconciliation?.readback) === JSON.stringify(readback);
  if (sameReplan) {
    if (previous.status === "failed" && previous.failure?.code === "PARTICIPATION_CONFIG_CONFLICT") {
      fail("A definite participation configuration conflict cannot be replayed; use replan for the next version.");
    }
    return previous;
  }
  if (previous.mutationId !== input.supersedesMutationId) {
    fail("Replan must supersede the current publication mutationId.");
  }
  if (
    previous.status !== "failed" ||
    previous.failure?.code !== "PARTICIPATION_CONFIG_CONFLICT" ||
    previous.failure.retryable !== false
  ) {
    fail("Replan requires a definite, non-retryable participation configuration conflict.");
  }
  const old = previous.references;
  if (
    references.projectId !== state.target.projectId ||
    references.projectId !== old.projectId ||
    references.sourceDraftRevisionId !== old.sourceDraftRevisionId ||
    references.sourceSha256 !== old.sourceSha256 ||
    references.expectedPolicyEpoch !== old.expectedPolicyEpoch ||
    references.expectedActiveReleaseId !== old.expectedActiveReleaseId
  ) {
    fail("Replan must keep the exact project, saved draft, policy epoch and active release.");
  }
  if (
    !Number.isSafeInteger(old.participationConfigVersion) ||
    !Number.isSafeInteger(references.participationConfigVersion) ||
    references.participationConfigVersion <= old.participationConfigVersion ||
    readback.latestConfigVersion !== references.participationConfigVersion
  ) {
    fail("Replan requires a newer participation version matching the server readback.");
  }
  if (input.requestSha256 === previous.requestSha256) {
    fail("Replan requires the digest of a new complete publication request.");
  }
  if (
    readback.activeReleaseId !== references.expectedActiveReleaseId ||
    !Number.isSafeInteger(readback.publicationCountBefore) ||
    readback.publicationCountBefore < 0 ||
    readback.publicationCountAfter !== readback.publicationCountBefore
  ) {
    fail("Replan requires an unchanged active release and publication count readback.");
  }
  if (
    input.mutationId === previous.mutationId ||
    Object.values(state.operations).some((operation) => operation.mutationId === input.mutationId) ||
    previous.priorAttempts?.some((operation) => operation.mutationId === input.mutationId)
  ) {
    fail("Replan requires a fresh mutationId that has never been used in this task.");
  }
  const priorAttempts = previous.priorAttempts ?? [];
  if (priorAttempts.length >= 8) fail("Too many publication conflict attempts; review this task before continuing.");
  const { priorAttempts: _priorAttempts, ...frozenPrevious } = previous;
  const operation = {
    status: "planned",
    mutationId: input.mutationId,
    requestSha256: input.requestSha256,
    references,
    retry: rule.retry,
    plannedAt: new Date().toISOString(),
    supersedesMutationId: previous.mutationId,
    reconciliation: { readback, at: new Date().toISOString() },
    priorAttempts: [...priorAttempts, frozenPrevious],
  };
  state.operations.preparePublication = operation;
  return operation;
}

function sameRecord(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function verifyParticipationReadback(state, operation, receipt, readback, directory) {
  const references = operation.references;
  if (!UUID.test(receipt.configId || "") || !SHA256.test(receipt.manifestSha256 || "") ||
      !Number.isSafeInteger(references.expectedVersion) ||
      receipt.version !== references.expectedVersion + 1) {
    fail("Participation receipt is not the planned next configuration.");
  }
  const siblingReferences = { ...references, manifestSha256: receipt.manifestSha256 };
  let siblingFound = false;
  for (const name of readdirSync(directory)) {
    if (!name.endsWith(".json") || !UUID.test(name.slice(0, -5)) ||
        name === `${state.taskId}.json`) continue;
    const sibling = readJson(join(directory, name), "Participation journal");
    const other = sibling.operations?.configureParticipation;
    if (sibling.schemaVersion !== 1 || sibling.taskId !== name.slice(0, -5) ||
        sibling.target?.projectId !== state.target.projectId ||
        other?.status !== "succeeded" || other.mutationId !== operation.mutationId ||
        other.requestSha256 !== operation.requestSha256 ||
        !sameRecord(other.references, siblingReferences) || !sameRecord(other.receipt, receipt)) continue;
    siblingFound = true;
    break;
  }
  if (!siblingFound) fail("Participation normalization needs the completed same-request journal.");
  onlyKeys(readback, ["mutation", "configuration"], "Participation readback");
  const mutation = sanitizedRecord(readback.mutation,
    ["accountId", "projectId", "principalKey", "operation", "mutationKey", "state", "configId", "version", "requestSha256"],
    ["accountId", "projectId", "principalKey", "operation", "mutationKey", "state", "configId", "version", "requestSha256"],
    "Participation mutation readback");
  const config = sanitizedRecord(readback.configuration,
    ["accountId", "projectId", "createdByUserId", "id", "version", "mode", "identityPolicy", "ownerVisibility", "manifestSha256", "configSha256"],
    ["accountId", "projectId", "createdByUserId", "id", "version", "mode", "identityPolicy", "ownerVisibility", "manifestSha256", "configSha256"],
    "Participation configuration readback");
  if (!UUID.test(mutation.accountId || "") || !UUID.test(mutation.principalKey || "") ||
      !SHA256.test(mutation.requestSha256 || "") || !SHA256.test(config.configSha256 || "") ||
      mutation.operation !== "participation.config.save" || mutation.state !== "accepted" ||
      mutation.mutationKey !== operation.mutationId ||
      mutation.projectId !== references.projectId ||
      mutation.configId !== receipt.configId || mutation.version !== receipt.version ||
      config.accountId !== mutation.accountId || config.createdByUserId !== mutation.principalKey ||
      config.projectId !== references.projectId || config.id !== receipt.configId ||
      config.version !== receipt.version || config.manifestSha256 !== receipt.manifestSha256 ||
      config.mode !== references.mode || config.identityPolicy !== references.identityPolicy ||
      config.ownerVisibility !== references.ownerVisibility) {
    fail("Participation server mutation and exact configuration readback disagree with the journal.");
  }
  return { kind: "server-participation-mutation-readback", configId: receipt.configId,
    version: receipt.version, manifestSha256: receipt.manifestSha256 };
}

function finish(state, input, directory) {
  onlyKeys(input, ["step", "mutationId", "receipt", "readback"], "Finish input");
  const rule = STEP_RULES[input.step];
  const operation = state.operations[input.step];
  if (!rule || !operation) fail("Finish input.step has not been planned.");
  if (operation.mutationId !== (input.mutationId ?? null)) fail("Finish mutationId does not match the durable plan.");
  if (
    input.step === "preparePublication" &&
    operation.status === "failed" &&
    operation.failure?.code === "PARTICIPATION_CONFIG_CONFLICT"
  ) {
    fail("A definite participation configuration conflict cannot be finished as success; use replan.");
  }
  const receipt = sanitizedRecord(input.receipt, rule.receipt, rule.receiptRequired, "Receipt");
  let verifiedReadback;
  const participationDigestDiffers = input.step === "configureParticipation" &&
    receipt.manifestSha256 !== operation.references.manifestSha256;
  if (participationDigestDiffers) {
    verifiedReadback = verifyParticipationReadback(state, operation, receipt, input.readback, directory);
  }
  for (const [key, value] of Object.entries(receipt)) {
    if (key in operation.references && operation.references[key] !== value) {
      if (participationDigestDiffers && key === "manifestSha256") continue;
      if (input.step !== "saveDraft" || key !== "sourceSha256") {
        fail(`Receipt.${key} does not match the durable plan.`);
      }
      verifiedReadback = sanitizedRecord(
        input.readback,
        ["projectId", "revisionId", "revision", "sourceSha256"],
        ["projectId", "revisionId", "revision", "sourceSha256"],
        "Readback",
      );
      if (
        !UUID.test(verifiedReadback.revisionId) ||
        !SHA256.test(verifiedReadback.sourceSha256) ||
        receipt.revision !== operation.references.expectedRevision + 1 ||
        Object.entries(verifiedReadback).some(([field, observed]) => receipt[field] !== observed)
      ) {
        fail("Save-draft source digest differs without an exact server revision readback.");
      }
    }
  }
  if (input.readback && !verifiedReadback) fail("Readback is only for a normalized save-draft or participation digest.");
  if (operation.status === "succeeded") {
    if (JSON.stringify(operation.receipt) !== JSON.stringify(receipt)) {
      fail("A succeeded step cannot be overwritten with a different receipt.");
    }
    return operation;
  }
  operation.receipt = receipt;
  if (verifiedReadback) operation.verification = verifiedReadback.kind
    ? verifiedReadback : { kind: "server-revision-readback", ...verifiedReadback };
  operation.status = "succeeded";
  operation.finishedAt = new Date().toISOString();
  delete operation.failure;
  if (input.step === "createProject") state.target.projectId = receipt.projectId;
  return operation;
}

function mark(state, input) {
  onlyKeys(input, ["step", "mutationId", "status", "code", "retryable"], "Mark input");
  const operation = state.operations[input.step];
  if (!operation) fail("Mark input.step has not been planned.");
  if (operation.mutationId !== (input.mutationId ?? null)) fail("Mark mutationId does not match the durable plan.");
  if (operation.status === "succeeded") fail("A succeeded step cannot be marked incomplete.");
  if (
    input.step === "preparePublication" &&
    operation.status === "failed" &&
    operation.failure?.code === "PARTICIPATION_CONFIG_CONFLICT"
  ) {
    fail("A definite participation configuration conflict cannot be overwritten; use replan.");
  }
  if (!new Set(["uncertain", "failed", "waiting"]).has(input.status)) fail("Mark status is unsupported.");
  if (typeof input.code !== "string" || !SAFE_TOKEN.test(input.code)) fail("Mark code must be a short safe token.");
  if (typeof input.retryable !== "boolean") fail("Mark retryable must be boolean.");
  if (
    input.step === "preparePublication" &&
    input.code === "PARTICIPATION_CONFIG_CONFLICT" &&
    (input.status !== "failed" || input.retryable !== false)
  ) {
    fail("A definite participation configuration conflict must be marked failed and non-retryable.");
  }
  operation.status = input.status;
  operation.failure = { code: input.code, retryable: input.retryable, at: new Date().toISOString() };
  return operation;
}

function unresolvedWrite(state) {
  return Object.entries(state.operations).find(([step, operation]) =>
    !STEP_RULES[step]?.readOnly &&
    (operation.status === "planned" || operation.status === "uncertain" ||
      operation.status === "waiting" ||
      (operation.status === "failed" && operation.failure?.retryable !== false))
  );
}

function print(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function main() {
  const { command, options } = args();
  if (command === "digest") {
    if (!options.file || !isAbsolute(options.file)) fail("digest requires an absolute --file path.");
    const stat = lstatSync(options.file);
    if (!stat.isFile() || stat.isSymbolicLink()) fail("Digest input must be a regular file, not a symlink.");
    const descriptor = openSync(options.file, constants.O_RDONLY | constants.O_NOFOLLOW);
    try {
      print({ sha256: createHash("sha256").update(readFileSync(descriptor)).digest("hex") });
    } finally {
      closeSync(descriptor);
    }
    return;
  }

  const input = options.input ? readJson(options.input, "Input") : undefined;
  if (command === "init") {
    onlyKeys(input, ["taskId", "artifactKind", "target", "selection", "summary"], "Init input");
    const taskId = input.taskId || randomUUID();
    const path = statePath(taskId, options["state-dir"]);
    if (existsSync(path)) fail("Task state already exists; use show or resume it.");
    if (!new Set(["page", "slides"]).has(input.artifactKind)) fail("artifactKind must be page or slides.");
    const summary = input.summary === undefined ? undefined : safeSummary(input.summary);
    const now = new Date().toISOString();
    const state = {
      schemaVersion: 1,
      taskId,
      artifactKind: input.artifactKind,
      target: validateTarget(input.target),
      selection: validateSelection(input.selection),
      summary,
      status: "active",
      operations: {},
      createdAt: now,
      updatedAt: now,
    };
    writeState(path, state);
    print({ path, state });
    return;
  }

  const path = statePath(options["task-id"], options["state-dir"]);
  let state = readState(path);
  if (command === "show") return print({ path, state });
  if (command === "next") {
    const pending = Object.entries(state.operations).find(([, operation]) => operation.status !== "succeeded");
    return print({
      path,
      taskId: state.taskId,
      status: state.status,
      next: pending ? { step: pending[0], ...pending[1] } : null,
    });
  }
  if (command === "pause") {
    if (state.status === "canceled") fail("Canceled task state is read-only; use recover for an unresolved write.");
    if (state.status === "active") {
      state.status = "paused";
      state.pausedAt = new Date().toISOString();
      writeState(path, state);
    }
    return print({ path, taskId: state.taskId, status: state.status });
  }
  if (command === "resume") {
    if (state.status === "canceled") fail("Canceled task state is read-only; use recover for an unresolved write.");
    if (state.status === "paused") {
      state.status = "active";
      state.resumedAt = new Date().toISOString();
      writeState(path, state);
    }
    return print({ path, taskId: state.taskId, status: state.status });
  }
  if (command === "recover") {
    if (state.status !== "canceled") fail("Only a canceled task can be recovered.");
    const pending = unresolvedWrite(state);
    if (!pending) fail("Canceled task has no unresolved write to recover.");
    state.status = "paused";
    state.recoveredAt = new Date().toISOString();
    writeState(path, state);
    return print({ path, taskId: state.taskId, status: state.status,
      next: { step: pending[0], ...pending[1] } });
  }
  if (command === "cancel") {
    if (state.status === "canceled") return print({ path, taskId: state.taskId, status: state.status });
    const pending = unresolvedWrite(state);
    if (pending) {
      fail(`Cannot cancel an unresolved ${pending[0]} write; pause and reconcile its original mutationId first.`);
    }
    state.status = "canceled";
    state.canceledAt = new Date().toISOString();
    writeState(path, state);
    return print({ path, taskId: state.taskId, status: state.status });
  }
  if (state.status === "paused") fail("Paused task state is read-only; verify the connection and resume before cloud work.");
  if (state.status !== "active") fail("Canceled task state is read-only; use recover for an unresolved write.");
  if (command === "plan" && input?.step === "activatePublication") {
    return withActivationPlanLock(dirname(path), () => {
      state = readState(path);
      if (state.status !== "active") fail("Task is no longer active; inspect its journal before planning activation.");
      if (!state.operations.activatePublication) {
        assertActivationNotJournaled(dirname(path), state.taskId, input.references ?? {});
      }
      const operation = plan(state, input);
      writeState(path, state);
      print({ path, taskId: state.taskId, operation });
    });
  }
  let operation;
  if (command === "plan") operation = plan(state, input);
  else if (command === "replan") operation = replanPublication(state, input);
  else if (command === "finish") operation = finish(state, input, dirname(path));
  else if (command === "mark") operation = mark(state, input);
  else fail("Usage: task-state.mjs <init|digest|plan|replan|finish|mark|next|show|pause|resume|recover|cancel> [options].");
  writeState(path, state);
  print({ path, taskId: state.taskId, operation });
}

try {
  main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
