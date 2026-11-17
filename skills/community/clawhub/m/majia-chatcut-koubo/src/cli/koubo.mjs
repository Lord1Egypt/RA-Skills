#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import {assertEvidenceClaims, buildHandoffReport, renderHandoffMarkdown} from "../orchestration/handoff-reporter.mjs";
import {inferIntent} from "../orchestration/intent-router.mjs";
import {runFakeOneClickSession} from "../orchestration/orchestrator.mjs";
import {createProjectBrief, selectProfile} from "../orchestration/profile-selector.mjs";
import {sampleApprovalCard} from "../orchestration/preview-selector.mjs";
import {auditDecisionLog, decisionSummaryForUser} from "../orchestration/risk-classifier.mjs";
import {assertSourceInventoryBindings} from "../orchestration/source-inventory.mjs";
import {preflightSession} from "../orchestration/session-preflight.mjs";
import {contentHash} from "../planning/preview-approval.mjs";
import {
  approvalIsCurrent,
  approveSample,
  authorizeDecisions,
  createRunManifest,
  requestSampleRevision,
  resumeRun,
  RunStateError,
  transitionRun,
} from "../orchestration/run-state.mjs";

const MODULE_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const REPOSITORY_ROOT = path.resolve(MODULE_DIRECTORY, "../..");
const DEFAULT_STATE_ROOT = path.resolve(process.cwd(), ".majia-koubo");
const DEFAULT_SCENARIO_FILE = path.join(REPOSITORY_ROOT, "fixtures/runtime/scenarios.json");
const COMMANDS = new Set(["preflight", "run", "status", "review", "approve-decisions", "approve-sample", "request-revision", "resume", "report"]);
const RUN_ID_PATTERN = /^run-[a-z0-9-]+$/u;
const REVISION_PATTERN = /^rev[-_][A-Za-z0-9._-]+$/u;
const MAX_JSON_BYTES = 5 * 1024 * 1024;
const RUNTIME_SCHEMA_FILES = Object.freeze([
  "project-brief.schema.json",
  "source-inventory.schema.json",
  "orchestration-profile.schema.json",
  "run-manifest.schema.json",
  "decision-log.schema.json",
  "checkpoint.schema.json",
  "handoff-report.schema.json",
  "fake-session.schema.json",
  "fake-session-suite.schema.json",
  "sample-context.schema.json",
]);
const runtimeAjv = new Ajv2020({allErrors: true, strict: true, allowUnionTypes: true, logger: false});
addFormats(runtimeAjv);
const runtimeValidators = new Map();
for (const schemaFile of RUNTIME_SCHEMA_FILES) {
  const schema = JSON.parse(fs.readFileSync(path.join(REPOSITORY_ROOT, "schemas/runtime", schemaFile), "utf8"));
  runtimeAjv.addSchema(schema);
  runtimeValidators.set(schemaFile, schema.$id);
}

const SCHEMA_BY_BASENAME = Object.freeze({
  "run-manifest.json": "run-manifest.schema.json",
  "project-brief.json": "project-brief.schema.json",
  "source-inventory.json": "source-inventory.schema.json",
  "decision-log.json": "decision-log.schema.json",
  "sample-context.json": "sample-context.schema.json",
  "handoff-report.json": "handoff-report.schema.json",
});

function assertRuntimeSchema(document, schemaFile, code = "RUNTIME_SCHEMA") {
  const validator = runtimeAjv.getSchema(runtimeValidators.get(schemaFile));
  if (!validator?.(document)) {
    throw new CliError(code, "runtime state does not satisfy its schema", 2);
  }
  if (schemaFile === "source-inventory.schema.json") {
    try {
      assertSourceInventoryBindings(document);
    } catch {
      throw new CliError(code, "source inventory bindings are invalid", 2);
    }
  }
  return document;
}

const USAGE = `Usage:
  majia-koubo preflight [--session <observation.json>] [--surface auto|hosted|desktop]
  majia-koubo run [intent] [--mode stable|fast|pro] [--run-id <id>] [--dry-run]
  majia-koubo run --scenario <file> [--scenario-id <id>] [--dry-run]
  majia-koubo status <run-id>
  majia-koubo review <run-id>
  majia-koubo approve-decisions <run-id> --decision-id <dec-id[,dec-id]> [--dry-run]
  majia-koubo approve-sample <run-id> [--dry-run]
  majia-koubo request-revision <run-id> --direction natural|tight [--dry-run]
  majia-koubo resume <run-id> --timeline-revision <revision> --reconcile-outcome <outcome> --evidence-ref <logical:ref> [--checkpoint-id <id>] [--dry-run]
  majia-koubo report <run-id> [--json]

Options:
  --session <observation.json>     Current tool/skill observation (not media proof)
  --surface auto|hosted|desktop    Bind to the selected ChatCut environment
  --root, --state-dir <directory>  Runtime state directory
  --json                          Emit machine-readable JSON
  --format text|markdown|json     Select output format
  --help                          Show this help
`;

class CliError extends Error {
  constructor(code, message, exitCode = 1) {
    super(message);
    this.name = "CliError";
    this.code = code;
    this.exitCode = exitCode;
  }
}

function usageError(message) {
  return new CliError("CLI_USAGE", message, 2);
}

function parseArguments(argv) {
  if (argv.length === 0) return {help: true, format: "text", provided: new Set(), positionals: []};
  const command = argv[0];
  if (command === "help" || command === "--help" || command === "-h") {
    return {help: true, format: "text", provided: new Set(), positionals: []};
  }
  if (!COMMANDS.has(command)) throw usageError("unknown command");

  const values = {
    "--root": "stateRoot",
    "--state-dir": "stateRoot",
    "--format": "format",
    "--intent": "intent",
    "--run-id": "runId",
    "--mode": "mode",
    "--goal": "goal",
    "--duration": "duration",
    "--platform": "platform",
    "--scenario": "scenarioFile",
    "--scenario-file": "scenarioFile",
    "--fixture": "scenarioFile",
    "--scenario-id": "scenarioId",
    "--timeline-revision": "timelineRevision",
    "--reconcile-outcome": "reconcileOutcome",
    "--evidence-ref": "evidenceRef",
    "--checkpoint-id": "checkpointId",
    "--decision-id": "decisionId",
    "--direction": "direction",
    "--now": "now",
    "--session": "sessionFile",
    "--surface": "surface",
  };
  const booleans = {
    "--json": "json",
    "--dry-run": "dryRun",
    "--screen": "screen",
    "--help": "help",
    "-h": "help",
  };
  const options = {command, format: "text", provided: new Set(), positionals: []};
  for (let index = 1; index < argv.length; index += 1) {
    const token = argv[index];
    if (token in booleans) {
      const key = booleans[token];
      if (options.provided.has(key)) throw usageError(`duplicate option: ${token}`);
      options[key] = true;
      options.provided.add(key);
      continue;
    }
    if (token in values) {
      const key = values[token];
      if (options.provided.has(key)) throw usageError(`duplicate option: ${token}`);
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw usageError(`${token} requires a value`);
      options[key] = value;
      options.provided.add(key);
      index += 1;
      continue;
    }
    if (token.startsWith("-")) throw usageError("unknown option");
    options.positionals.push(token);
  }
  if (options.help) return options;
  if (options.json && options.provided.has("format")) {
    throw usageError("choose either --json or --format, not both");
  }
  if (options.json) options.format = "json";
  if (!["text", "markdown", "json"].includes(options.format)) {
    throw usageError("--format must be text, markdown, or json");
  }
  options.stateRoot = path.resolve(options.stateRoot ?? DEFAULT_STATE_ROOT);
  assignPositionals(options);
  validateCommandOptions(options);
  return options;
}

function assignPositionals(options) {
  if (options.command === "preflight") {
    if (options.positionals.length > 0) throw usageError("preflight does not accept positional arguments");
    return;
  }
  if (options.command === "run") {
    if (options.positionals.length > 0) {
      if (options.intent !== undefined) throw usageError("intent was provided twice");
      options.intent = options.positionals.join(" ");
    }
    return;
  }
  if (options.positionals.length > 1) throw usageError("too many positional arguments");
  if (options.positionals.length === 1) {
    if (options.runId !== undefined) throw usageError("run ID was provided twice");
    options.runId = options.positionals[0];
  }
}

function validateCommandOptions(options) {
  const global = new Set(["stateRoot", "format", "json", "help"]);
  const perCommand = {
    preflight: new Set(["sessionFile", "surface", "now"]),
    run: new Set(["intent", "runId", "mode", "goal", "duration", "platform", "scenarioFile", "scenarioId", "dryRun", "screen", "now", "sessionFile", "surface"]),
    status: new Set(["runId"]),
    review: new Set(["runId"]),
    "approve-decisions": new Set(["runId", "decisionId", "dryRun", "now"]),
    "approve-sample": new Set(["runId", "dryRun", "now"]),
    "request-revision": new Set(["runId", "direction", "dryRun", "now"]),
    resume: new Set(["runId", "timelineRevision", "reconcileOutcome", "evidenceRef", "checkpointId", "dryRun", "now"]),
    report: new Set(["runId"]),
  };
  for (const key of options.provided) {
    if (!global.has(key) && !perCommand[options.command].has(key)) {
      throw usageError(`option is not valid for ${options.command}`);
    }
  }
  if (options.surface && !["auto", "hosted", "desktop"].includes(options.surface)) throw usageError("--surface must be auto, hosted, or desktop");
  if ((options.scenarioFile || options.scenarioId) && (options.sessionFile || options.surface)) throw usageError("simulation scenarios cannot use a live session observation");
  if (!["run", "preflight"].includes(options.command) && !options.runId) throw usageError(`${options.command} requires a run ID`);
  if (options.runId && !RUN_ID_PATTERN.test(options.runId)) {
    throw new CliError("RUN_ID_INVALID", "run ID must use the run- prefix and lowercase safe characters");
  }
  if (options.mode && !["stable", "fast", "pro"].includes(options.mode)) {
    throw usageError("--mode must be stable, fast, or pro");
  }
  if (options.goal && !["daily-publish", "short-draft", "trust-longform", "screen-demo", "internal-material"].includes(options.goal)) {
    throw usageError("--goal is invalid");
  }
  if (options.duration !== undefined) {
    const duration = Number(options.duration);
    if (!Number.isInteger(duration) || duration <= 0 || duration > 21600) {
      throw usageError("--duration must be an integer between 1 and 21600");
    }
    options.duration = duration;
  }
  if (options.timelineRevision && !REVISION_PATTERN.test(options.timelineRevision)) {
    throw new CliError("TIMELINE_REVISION_INVALID", "timeline revision is not valid");
  }
  if (options.checkpointId && !/^cp-[a-z0-9-]+$/u.test(options.checkpointId)) {
    throw usageError("--checkpoint-id is invalid");
  }
  if (options.decisionId) {
    options.decisionIds = options.decisionId.split(",").map((item) => item.trim()).filter(Boolean);
    if (options.decisionIds.length === 0 || options.decisionIds.some((item) => !/^dec-[a-z0-9-]+$/u.test(item))) {
      throw usageError("--decision-id must contain comma-separated decision IDs");
    }
  }
  if (options.command === "approve-decisions" && !options.decisionIds?.length) {
    throw usageError("approve-decisions requires --decision-id");
  }
  if (options.direction && !["natural", "tight"].includes(options.direction)) {
    throw usageError("--direction must be natural or tight");
  }
  if (options.command === "request-revision" && !options.direction) {
    throw usageError("request-revision requires --direction");
  }
  if (options.evidenceRef) {
    options.evidenceRefs = options.evidenceRef.split(",").map((item) => item.trim()).filter(Boolean);
    if (options.evidenceRefs.length === 0 || options.evidenceRefs.some((item) => !/^logical:[a-z0-9-]+$/u.test(item))) {
      throw usageError("--evidence-ref must contain comma-separated logical references");
    }
  }
  if (options.platform && options.platform.length > 64) throw usageError("--platform must be 64 characters or fewer");
  if (options.now && (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/u.test(options.now) || !Number.isFinite(Date.parse(options.now)))) {
    throw usageError("--now must be an ISO UTC date-time");
  }
  if (options.scenarioId && !/^scenario-[a-z0-9-]+$/u.test(options.scenarioId)) {
    throw usageError("--scenario-id is invalid");
  }
}

function lstatOrNull(target) {
  try {
    return fs.lstatSync(target);
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw new CliError("STATE_ACCESS_FAILED", "runtime state could not be accessed", 2);
  }
}

function assertSafeDirectory(directory, {allowMissing = false} = {}) {
  const stat = lstatOrNull(directory);
  if (!stat && allowMissing) return false;
  if (!stat) throw new CliError("STATE_NOT_FOUND", "runtime state was not found");
  if (stat.isSymbolicLink() || !stat.isDirectory()) {
    throw new CliError("STATE_DIRECTORY_UNSAFE", "runtime state directory is unsafe", 2);
  }
  return true;
}

function ensureStateRoot(root) {
  if (assertSafeDirectory(root, {allowMissing: true})) return;
  try {
    fs.mkdirSync(root, {recursive: true, mode: 0o700});
  } catch {
    throw new CliError("STATE_CREATE_FAILED", "runtime state directory could not be created", 2);
  }
  assertSafeDirectory(root);
}

function runDirectory(options) {
  assertRunId(options.runId);
  return path.join(options.stateRoot, options.runId);
}

function assertRunId(runId) {
  if (!RUN_ID_PATTERN.test(runId ?? "")) {
    throw new CliError("RUN_ID_INVALID", "run ID must use the run- prefix and lowercase safe characters");
  }
}

function safeReadJson(file, {code = "STATE_FILE", schemaFile = null} = {}) {
  const stat = lstatOrNull(file);
  if (!stat) throw new CliError(`${code}_MISSING`, "required runtime state is missing");
  if (stat.isSymbolicLink() || !stat.isFile()) {
    throw new CliError(`${code}_UNSAFE`, "runtime state file is unsafe", 2);
  }
  if (stat.size > MAX_JSON_BYTES) throw new CliError(`${code}_TOO_LARGE`, "runtime state file is too large", 2);
  try {
    const document = JSON.parse(fs.readFileSync(file, "utf8"));
    return schemaFile ? assertRuntimeSchema(document, schemaFile, `${code}_SCHEMA_INVALID`) : document;
  } catch (error) {
    if (error instanceof CliError) throw error;
    throw new CliError(`${code}_INVALID`, "runtime state JSON is invalid", 2);
  }
}

function readOptionalJson(file, schemaFile = null) {
  if (!lstatOrNull(file)) return null;
  return safeReadJson(file, {schemaFile});
}

function loadRun(options) {
  const directory = runDirectory(options);
  assertSafeDirectory(options.stateRoot);
  assertSafeDirectory(directory);
  const manifest = safeReadJson(path.join(directory, "run-manifest.json"), {code: "RUN_MANIFEST", schemaFile: "run-manifest.schema.json"});
  if (manifest.runId !== options.runId) throw new CliError("RUN_MANIFEST_MISMATCH", "run manifest does not match the requested run", 2);
  return {directory, manifest};
}

function writeJsonAtomic(file, value) {
  const directory = path.dirname(file);
  const schemaFile = path.basename(directory) === "checkpoints"
    ? "checkpoint.schema.json"
    : SCHEMA_BY_BASENAME[path.basename(file)];
  if (schemaFile) assertRuntimeSchema(value, schemaFile, "STATE_WRITE_SCHEMA_INVALID");
  assertSafeDirectory(directory);
  const existing = lstatOrNull(file);
  if (existing?.isSymbolicLink() || (existing && !existing.isFile())) {
    throw new CliError("STATE_FILE_UNSAFE", "runtime state file is unsafe", 2);
  }
  const temporary = path.join(directory, `.tmp-${path.basename(file)}-${crypto.randomBytes(6).toString("hex")}`);
  let descriptor;
  try {
    descriptor = fs.openSync(temporary, "wx", 0o600);
    fs.writeFileSync(descriptor, `${JSON.stringify(value, null, 2)}\n`, "utf8");
    fs.fsyncSync(descriptor);
    fs.closeSync(descriptor);
    descriptor = undefined;
    fs.renameSync(temporary, file);
    fs.chmodSync(file, 0o600);
  } catch {
    if (descriptor !== undefined) fs.closeSync(descriptor);
    try {
      fs.unlinkSync(temporary);
    } catch {
      // The temporary file may already have been renamed or never created.
    }
    throw new CliError("STATE_WRITE_FAILED", "runtime state could not be written", 2);
  }
}

function createRunId(now = new Date().toISOString()) {
  const day = now.slice(0, 10).replaceAll("-", "");
  return `run-${day}-${crypto.randomBytes(4).toString("hex")}`;
}

function deriveGoal({mode, durationSec, hasScreenCapture}) {
  if (hasScreenCapture) return "screen-demo";
  if (durationSec !== null && durationSec >= 300) return "trust-longform";
  if (mode === "fast") return "short-draft";
  return "daily-publish";
}

function loadScenario(options) {
  const file = path.resolve(options.scenarioFile ?? DEFAULT_SCENARIO_FILE);
  const document = safeReadJson(file, {code: "SCENARIO"});
  if (Array.isArray(document.scenarios)) {
    assertRuntimeSchema(document, "fake-session-suite.schema.json", "SCENARIO_SCHEMA_INVALID");
    if (!options.scenarioId && document.scenarios.length !== 1) {
      throw new CliError("SCENARIO_ID_REQUIRED", "a scenario ID is required for a scenario suite", 2);
    }
    const scenario = options.scenarioId
      ? document.scenarios.find((item) => item.scenarioId === options.scenarioId)
      : document.scenarios[0];
    if (!scenario) throw new CliError("SCENARIO_NOT_FOUND", "the requested scenario was not found", 2);
    return structuredClone(scenario);
  }
  assertRuntimeSchema(document, "fake-session.schema.json", "SCENARIO_SCHEMA_INVALID");
  if (!document || typeof document !== "object" || !document.scenarioId) {
    throw new CliError("SCENARIO_INVALID", "scenario JSON is invalid", 2);
  }
  if (options.scenarioId && document.scenarioId !== options.scenarioId) {
    throw new CliError("SCENARIO_NOT_FOUND", "the requested scenario was not found", 2);
  }
  return structuredClone(document);
}

function sourceInventoryFor(scenario, result, now) {
  if (!result.manifest.sourceInventoryRef || !result.manifest.project.projectRef || !result.manifest.project.timelineRef) return null;
  const assets = [{
    logicalRef: "logical:aroll-main",
    role: "aroll",
    mediaType: "video",
    durationSec: scenario.durationSec,
    alreadyImported: Boolean(scenario.assetAlreadyImported),
    transcriptStatus: scenario.transcriptStatus,
  }];
  if (scenario.hasScreenCapture) {
    assets.push({
      logicalRef: "logical:screen-main",
      role: "screen",
      mediaType: "video",
      durationSec: scenario.durationSec,
      alreadyImported: Boolean(scenario.assetAlreadyImported),
      transcriptStatus: "not-applicable",
    });
  }
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/source-inventory.schema.json",
    schemaVersion: "majia.koubo.sources.v1",
    runId: result.manifest.runId,
    projectRef: result.manifest.project.projectRef,
    timelineRef: result.manifest.project.timelineRef,
    mainSourceRef: "logical:aroll-main",
    assets,
    capturedAt: now,
  };
}

function sampleContextFor(result) {
  if (!result.fingerprints) return null;
  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/runtime/sample-context.schema.json",
    schemaVersion: "majia.koubo.sample-context.v1",
    runId: result.manifest.runId,
    fingerprints: structuredClone(result.fingerprints),
    windows: structuredClone(result.windows),
    approvalCard: sampleApprovalCard({
      decisions: result.decisionLog?.decisions ?? [],
      treatments: result.brief.treatments,
    }),
    treatments: structuredClone(result.brief.treatments),
  };
}

function persistNewRun(options, artifacts) {
  ensureStateRoot(options.stateRoot);
  const target = runDirectory(options);
  if (lstatOrNull(target)) throw new CliError("RUN_ALREADY_EXISTS", "a run with this ID already exists");
  const staging = path.join(options.stateRoot, `.tmp-${options.runId}-${crypto.randomBytes(6).toString("hex")}`);
  try {
    fs.mkdirSync(staging, {mode: 0o700});
    for (const [relative, value] of Object.entries(artifacts)) {
      if (value === null || value === undefined) continue;
      const file = path.join(staging, relative);
      const parent = path.dirname(file);
      if (!lstatOrNull(parent)) fs.mkdirSync(parent, {recursive: true, mode: 0o700});
      writeJsonAtomic(file, value);
    }
    fs.renameSync(staging, target);
  } catch (error) {
    try {
      fs.rmSync(staging, {recursive: true, force: true});
    } catch {
      // Best-effort cleanup is limited to this uniquely named staging directory.
    }
    if (error instanceof CliError) throw error;
    throw new CliError("STATE_WRITE_FAILED", "runtime state could not be written", 2);
  }
}

function artifactsForScenario(scenario, result, now) {
  const artifacts = {
    "run-manifest.json": result.manifest,
    "project-brief.json": result.brief,
    "source-inventory.json": sourceInventoryFor(scenario, result, now),
    "decision-log.json": result.decisionLog,
    "sample-context.json": sampleContextFor(result),
    "recovery-report.json": result.recovery ?? null,
    "handoff-report.json": result.handoff,
  };
  for (const checkpoint of result.checkpoints) {
    artifacts[`checkpoints/${checkpoint.checkpointId}.json`] = checkpoint;
  }
  return artifacts;
}

function refreshHandoff(manifest, previous, {
  sampleApproval,
  nextActions,
  now = new Date().toISOString(),
} = {}) {
  const evidence = structuredClone(previous?.evidence ?? []);
  if (sampleApproval === "pass" && !evidence.some((item) => item.kind === "sample-approval")) {
    const approval = [...manifest.approvals].reverse().find((item) => item.kind === "sample" && item.status === "approved");
    if (approval) {
      evidence.push({
        ref: "logical:sample-approval-evidence",
        kind: "sample-approval",
        hash: contentHash(approval),
        revision: approval.fingerprints.timelineRevision,
        provenance: evidence[0]?.provenance ?? "live",
        capturedAt: now,
      });
    }
  }
  return buildHandoffReport({
    manifest,
    completed: previous?.completed ?? [],
    notPerformed: previous?.notPerformed,
    verification: {
      ...(previous?.verification ?? {}),
      ...(sampleApproval ? {sampleApproval} : {}),
    },
    evidence,
    openRisks: manifest.blockedReason
      ? [manifest.blockedReason.message]
      : previous?.openRisks ?? [],
    nextActions: nextActions ?? previous?.nextActions,
    now,
  });
}

function sessionPreflight(options, brief = null) {
  const observation = options.sessionFile
    ? safeReadJson(path.resolve(options.sessionFile), {code: "SESSION_OBSERVATION"})
    : null;
  return preflightSession({
    observation,
    surface: options.surface ?? "auto",
    treatments: brief?.treatments ?? {arollCleanup: true, smoothAudio: true, captions: true},
    textTarget: brief?.textEdit?.target ?? null,
    now: options.now ?? new Date().toISOString(),
  });
}

function preflightCommand(options) {
  const report = sessionPreflight(options);
  if (!report.contractReady) process.exitCode = 1;
  return {ok: report.contractReady, command: "preflight", ...report};
}

function runCommand(options) {
  const now = options.now ?? new Date().toISOString();
  let result;
  let artifacts;
  let session = null;
  if (options.scenarioFile || options.scenarioId) {
    const scenario = loadScenario(options);
    const runId = options.runId ?? `run-${scenario.scenarioId.replace(/^scenario-/u, "")}`;
    assertRunId(runId);
    scenario.scenarioId = `scenario-${runId.replace(/^run-/u, "")}`;
    result = runFakeOneClickSession(scenario, {now});
    options.runId = runId;
    artifacts = artifactsForScenario(scenario, result, now);
  } else {
    const route = inferIntent(options.intent ?? "稳剪当前口播");
    if (options.mode) {
      route.mode = options.mode;
      route.action = "run";
      route.reason = "explicit-mode";
    }
    if (route.action === "resume") {
      throw new CliError("RUN_USE_RESUME", "continue requests must use the resume command with an existing run ID", 2);
    }
    const durationSec = options.duration ?? null;
    const goal = options.goal ?? deriveGoal({mode: route.mode, durationSec, hasScreenCapture: Boolean(options.screen)});
    const profile = selectProfile({mode: route.mode, goal, durationSec, hasScreenCapture: Boolean(options.screen)});
    const brief = createProjectBrief({
      route,
      profile,
      goal,
      platform: options.platform ?? "unspecified",
      targetDurationSec: durationSec,
      createdAt: now,
    });
    const runId = options.runId ?? createRunId(now);
    options.runId = runId;
    session = sessionPreflight({...options, now}, brief);
    let manifest = createRunManifest({runId, profile, now});
    manifest = transitionRun(manifest, "brief_ready", {now, nextSafeAction: session.contractReady ? "resolve_project_and_source" : "refresh_session_contract"});
    const handoff = buildHandoffReport({
      manifest,
      nextActions: !session.contractReady ? [session.nextAction] : route.automationLevel === "audit"
        ? ["连接现有 ChatCut 项目并只读生成审核方案"]
        : ["连接 ChatCut 并自动读取目标项目与主素材"],
      now,
    });
    result = {route, profile, brief, manifest, handoff, checkpoints: [], decisionLog: null, windows: [], fingerprints: null};
    artifacts = {
      "run-manifest.json": manifest,
      "project-brief.json": brief,
      "handoff-report.json": handoff,
      "session-preflight.json": session,
    };
  }
  if (!options.dryRun) persistNewRun(options, artifacts);
  return {
    ok: true,
    command: "run",
    dryRun: Boolean(options.dryRun),
    runId: result.manifest.runId,
    stage: result.manifest.stage,
    status: result.manifest.status,
    profile: result.profile.id,
    nextAction: result.manifest.lastSafeAction,
    blockedReason: result.manifest.blockedReason,
    manifest: result.manifest,
    brief: result.brief,
    handoff: result.handoff,
    recovery: result.recovery ?? null,
    sessionPreflight: session,
  };
}

function statusFor(manifest) {
  const sample = [...manifest.approvals].reverse().find((item) => item.kind === "sample") ?? null;
  const nextAction = manifest.status === "blocked"
    ? "reconcile_before_resume"
    : manifest.stage === "sample_ready"
      ? "approve_sample_or_request_revision"
      : manifest.stage === "review_ready"
        ? "review_editable_timeline"
        : manifest.lastSafeAction;
  return {
    ok: true,
    command: "status",
    runId: manifest.runId,
    stage: manifest.stage,
    status: manifest.status,
    profile: manifest.profile.id,
    timelineRevision: manifest.project.timelineRevision,
    sampleApproval: sample?.status ?? "pending",
    nextAction,
    blocker: manifest.blockedReason,
    updatedAt: manifest.updatedAt,
  };
}

function statusCommand(options) {
  return statusFor(loadRun(options).manifest);
}

function reviewCommand(options) {
  const {directory, manifest} = loadRun(options);
  const decisionLog = readOptionalJson(path.join(directory, "decision-log.json"), "decision-log.schema.json");
  const context = readOptionalJson(path.join(directory, "sample-context.json"), "sample-context.schema.json");
  const previous = readOptionalJson(path.join(directory, "handoff-report.json"), "handoff-report.schema.json");
  if (decisionLog && auditDecisionLog(decisionLog, {approvals: manifest.approvals}).length > 0) {
    throw new CliError("DECISION_LOG_POLICY_INVALID", "decision log approval or risk bindings are invalid", 2);
  }
  const handoff = refreshHandoff(manifest, previous);
  assertEvidenceClaims(handoff);
  return {
    ok: true,
    command: "review",
    runId: manifest.runId,
    stage: manifest.stage,
    status: manifest.status,
    sampleApprovalCurrent: context?.fingerprints
      ? approvalIsCurrent(manifest, context.fingerprints)
      : false,
    sample: context
      ? {
          windows: context.windows.map(({reason, startSec, endSec}) => ({reason, startSec, endSec})),
          approvalCard: context.approvalCard,
        }
      : null,
    decisions: (decisionLog?.decisions ?? []).map(decisionSummaryForUser),
    verification: handoff.verification,
    openRisks: handoff.openRisks,
    nextActions: handoff.nextActions,
  };
}

function approveDecisionsCommand(options) {
  const {directory, manifest} = loadRun(options);
  const context = safeReadJson(path.join(directory, "sample-context.json"), {code: "SAMPLE_CONTEXT", schemaFile: "sample-context.schema.json"});
  const decisionLog = safeReadJson(path.join(directory, "decision-log.json"), {code: "DECISION_LOG", schemaFile: "decision-log.schema.json"});
  if (context.runId !== manifest.runId || decisionLog.runId !== manifest.runId) {
    throw new CliError("DECISION_CONTEXT_MISMATCH", "decision approval artifacts belong to another run", 2);
  }
  const selected = decisionLog.decisions.filter((item) => options.decisionIds.includes(item.decisionId));
  if (selected.length !== options.decisionIds.length || selected.some((item) => item.risk !== "high" || !["proposed", "approved"].includes(item.status))) {
    throw new CliError("DECISION_APPROVAL_SCOPE_INVALID", "only existing proposed high-risk decisions can be approved", 2);
  }
  const now = options.now ?? new Date().toISOString();
  const next = authorizeDecisions(manifest, {
    fingerprints: context.fingerprints,
    decisionIds: options.decisionIds,
    now,
  });
  const approval = [...next.approvals].reverse().find((item) => item.kind === "decision");
  const nextLog = structuredClone(decisionLog);
  nextLog.decisions = nextLog.decisions.map((item) => options.decisionIds.includes(item.decisionId)
    ? {...item, status: "approved", approvalRef: approval.approvalRef}
    : item);
  if (!options.dryRun) {
    writeJsonAtomic(path.join(directory, "decision-log.json"), nextLog);
    writeJsonAtomic(path.join(directory, "run-manifest.json"), next);
  }
  return {
    ok: true,
    command: "approve-decisions",
    dryRun: Boolean(options.dryRun),
    runId: next.runId,
    approvedDecisionIds: [...options.decisionIds],
    approvalRef: approval.approvalRef,
    stage: next.stage,
    status: next.status,
    nextAction: "approve_sample_or_review_more_decisions",
  };
}

function approveSampleCommand(options) {
  const {directory, manifest} = loadRun(options);
  const context = safeReadJson(path.join(directory, "sample-context.json"), {code: "SAMPLE_CONTEXT", schemaFile: "sample-context.schema.json"});
  if (context.runId !== manifest.runId) throw new CliError("SAMPLE_CONTEXT_MISMATCH", "sample context belongs to a different run", 2);
  const scope = (context.windows ?? []).map((item) => item.windowRef).filter(Boolean);
  const now = options.now ?? new Date().toISOString();
  const next = approveSample(manifest, {fingerprints: context.fingerprints, scope, now});
  const previous = readOptionalJson(path.join(directory, "handoff-report.json"), "handoff-report.schema.json");
  const handoff = refreshHandoff(next, previous, {
    sampleApproval: "pass",
    nextActions: ["按已确认样片策略继续整片处理"],
    now,
  });
  assertEvidenceClaims(handoff);
  if (!options.dryRun) {
    writeJsonAtomic(path.join(directory, "handoff-report.json"), handoff);
    writeJsonAtomic(path.join(directory, "run-manifest.json"), next);
  }
  return {
    ok: true,
    command: "approve-sample",
    dryRun: Boolean(options.dryRun),
    runId: next.runId,
    stage: next.stage,
    status: next.status,
    sampleApproval: "approved",
    nextAction: next.lastSafeAction,
  };
}

function requestRevisionCommand(options) {
  const {directory, manifest} = loadRun(options);
  const now = options.now ?? new Date().toISOString();
  const next = requestSampleRevision(manifest, {direction: options.direction, now});
  const previous = readOptionalJson(path.join(directory, "handoff-report.json"), "handoff-report.schema.json");
  const handoff = refreshHandoff(next, previous, {
    sampleApproval: "pending",
    nextActions: [`按“${options.direction === "natural" ? "再自然一点" : "再紧一点"}”重做受影响样片窗口`],
    now,
  });
  if (!options.dryRun) {
    writeJsonAtomic(path.join(directory, "handoff-report.json"), handoff);
    writeJsonAtomic(path.join(directory, "run-manifest.json"), next);
  }
  return {
    ok: true,
    command: "request-revision",
    dryRun: Boolean(options.dryRun),
    runId: next.runId,
    stage: next.stage,
    status: next.status,
    direction: options.direction,
    nextAction: next.lastSafeAction,
  };
}

function resumeCommand(options) {
  const {directory, manifest} = loadRun(options);
  const currentTimelineRevision = options.timelineRevision ?? null;
  if (manifest.project.timelineRevision && !currentTimelineRevision) {
    throw new CliError("RUN_CURRENT_REVISION_REQUIRED", "resume requires --timeline-revision from a fresh ChatCut readback", 2);
  }
  if (
    manifest.status === "blocked"
    && currentTimelineRevision === manifest.project.timelineRevision
    && (!options.reconcileOutcome || !options.evidenceRefs?.length)
  ) {
    throw new CliError("RUN_RECONCILIATION_REQUIRED", "blocked runs require --reconcile-outcome and --evidence-ref", 2);
  }
  const checkpointId = options.checkpointId ?? manifest.checkpoints.at(-1) ?? null;
  const checkpoint = checkpointId
    ? safeReadJson(path.join(directory, "checkpoints", `${checkpointId}.json`), {
        code: "CHECKPOINT",
        schemaFile: "checkpoint.schema.json",
      })
    : null;
  const now = options.now ?? new Date().toISOString();
  const next = resumeRun(manifest, {
    currentTimelineRevision,
    checkpoint,
    reconciliation: manifest.status === "blocked"
      ? {
          blockerCode: manifest.blockedReason.code,
          outcome: options.reconcileOutcome,
          evidenceRefs: options.evidenceRefs,
          checkpointId,
          observedRevision: currentTimelineRevision,
        }
      : null,
    now,
  });
  const previous = readOptionalJson(path.join(directory, "handoff-report.json"), "handoff-report.schema.json");
  const sample = [...next.approvals].reverse().find((item) => item.kind === "sample");
  const sampleApproval = sample?.status === "approved" ? "pass" : sample?.status ?? "pending";
  const handoff = refreshHandoff(next, previous, {
    sampleApproval,
    nextActions: next.status === "blocked"
      ? ["回读时间线差异并重新确认代表样片"]
      : ["从最近安全检查点继续"],
    now,
  });
  assertEvidenceClaims(handoff);
  if (!options.dryRun) {
    writeJsonAtomic(path.join(directory, "handoff-report.json"), handoff);
    writeJsonAtomic(path.join(directory, "run-manifest.json"), next);
  }
  return {
    ok: true,
    command: "resume",
    dryRun: Boolean(options.dryRun),
    runId: next.runId,
    stage: next.stage,
    status: next.status,
    timelineRevision: next.project.timelineRevision,
    sampleApproval,
    blocker: next.blockedReason,
    nextAction: next.lastSafeAction,
  };
}

function reportCommand(options) {
  const {directory, manifest} = loadRun(options);
  const previous = readOptionalJson(path.join(directory, "handoff-report.json"), "handoff-report.schema.json");
  const report = refreshHandoff(manifest, previous);
  assertEvidenceClaims(report);
  return report;
}

function execute(options) {
  switch (options.command) {
    case "preflight": return preflightCommand(options);
    case "run": return runCommand(options);
    case "status": return statusCommand(options);
    case "review": return reviewCommand(options);
    case "approve-decisions": return approveDecisionsCommand(options);
    case "approve-sample": return approveSampleCommand(options);
    case "request-revision": return requestRevisionCommand(options);
    case "resume": return resumeCommand(options);
    case "report": return reportCommand(options);
    default: throw usageError("unknown command");
  }
}

function renderText(command, result) {
  if (command === "preflight") return `环境：${result.surface}\n会话合同：${result.contractReady ? "可继续核对项目" : "需补齐"}\n${result.nextAction}\n`;
  if (command === "report") return renderHandoffMarkdown(result);
  if (command === "status") {
    return [
      `运行：${result.runId}`,
      `阶段：${result.stage}`,
      `状态：${result.status}`,
      `样片确认：${result.sampleApproval}`,
      `下一步：${result.nextAction}`,
      ...(result.blocker ? [`阻断：${result.blocker.message}`] : []),
    ].join("\n") + "\n";
  }
  if (command === "review") {
    return [
      `运行：${result.runId}`,
      `阶段：${result.stage}`,
      `样片确认仍有效：${result.sampleApprovalCurrent ? "是" : "否"}`,
      `决策项：${result.decisions.length}`,
      ...result.nextActions.map((item) => `下一步：${item}`),
    ].join("\n") + "\n";
  }
  return [
    `运行：${result.runId}`,
    `阶段：${result.stage}`,
    `状态：${result.status}`,
    ...(result.dryRun ? ["模式：仅预演，未写入状态"] : []),
    ...(result.blockedReason ? [`阻断：${result.blockedReason.message}`] : []),
    ...(result.blocker ? [`阻断：${result.blocker.message}`] : []),
    `下一步：${result.nextAction}`,
  ].join("\n") + "\n";
}

function safeError(error) {
  if (error instanceof CliError || error instanceof RunStateError) {
    return {
      code: error.code ?? "KOUBO_FAILED",
      message: String(error.message).replace(/[\r\n]+/gu, " ").slice(0, 240),
      exitCode: error.exitCode ?? 1,
    };
  }
  const knownCode = typeof error?.message === "string" && /^[A-Z][A-Z0-9_]+$/u.test(error.message)
    ? error.message
    : "KOUBO_FAILED";
  return {code: knownCode, message: "the command could not be completed safely", exitCode: 1};
}

function main(argv) {
  let options;
  const wantsJson = argv.includes("--json") || argv.some((value, index) => argv[index - 1] === "--format" && value === "json");
  try {
    options = parseArguments(argv);
    if (options.help) {
      process.stdout.write(USAGE);
      return;
    }
    const result = execute(options);
    if (options.format === "json") {
      process.stdout.write(`${JSON.stringify(result)}\n`);
    } else {
      process.stdout.write(renderText(options.command, result));
    }
  } catch (error) {
    const failure = safeError(error);
    if (wantsJson || options?.format === "json") {
      process.stderr.write(`${JSON.stringify({ok: false, error: {code: failure.code, message: failure.message}})}\n`);
    } else {
      process.stderr.write(`${failure.code}: ${failure.message}\n`);
      if (failure.code === "CLI_USAGE") process.stderr.write(USAGE);
    }
    process.exitCode = failure.exitCode;
  }
}

main(process.argv.slice(2));
