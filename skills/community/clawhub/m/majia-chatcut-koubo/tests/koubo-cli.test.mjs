import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import test from "node:test";
import {fileURLToPath} from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CLI = path.join(ROOT, "src/cli/koubo.mjs");
const SCENARIOS = JSON.parse(fs.readFileSync(path.join(ROOT, "fixtures/runtime/scenarios.json"), "utf8"));
const NOW = "2026-08-10T00:00:00Z";

function invoke(args) {
  return spawnSync(process.execPath, [CLI, ...args], {
    cwd: ROOT,
    encoding: "utf8",
    env: {...process.env, NO_COLOR: "1"},
  });
}

function successJson(args) {
  const result = invoke([...args, "--json"]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  return JSON.parse(result.stdout);
}

function workspace(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-cli-test-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  return directory;
}

function fixture(id) {
  return structuredClone(SCENARIOS.scenarios.find((item) => item.scenarioId === id));
}

function hash(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

test("help 暴露完整用户主流程", () => {
  const result = invoke(["--help"]);
  assert.equal(result.status, 0);
  for (const command of ["run", "status", "review", "approve-sample", "resume", "report"]) {
    assert.match(result.stdout, new RegExp(`\\b${command}\\b`, "u"));
  }
});

test("preflight 无会话时退出非零且不创建状态文件", (t) => {
  const stateRoot = path.join(workspace(t), "untouched");
  const result = invoke(["preflight", "--root", stateRoot, "--json"]);
  assert.equal(result.status, 1, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.equal(report.contractReady, false);
  assert.equal(report.surface, "unknown");
  assert.equal(fs.existsSync(stateRoot), false);
});

test("普通文字 run 保存目标与环境检查，但不伪造剪辑结果", (t) => {
  const stateRoot = workspace(t);
  const result = successJson(["run", "只改字幕，别剪原声", "--run-id", "run-caption-only", "--root", stateRoot]);
  assert.equal(result.brief.textEdit.target, "caption-display");
  assert.equal(result.brief.treatments.arollCleanup, false);
  assert.equal(result.sessionPreflight.contractReady, false);
  assert.equal(result.manifest.capability.status, "unverified");
  assert.equal(result.nextAction, "refresh_session_contract");
  assert.equal(result.recovery, null);
  assert.equal(fs.existsSync(path.join(stateRoot, result.runId, "session-preflight.json")), true);
});

test("模拟文字请求不得调用普通稳剪批量写入", (t) => {
  const directory = workspace(t);
  const scenario = fixture("scenario-happy-path");
  scenario.intent = "只改字幕，别剪原声";
  const file = path.join(directory, "caption-only.json");
  fs.writeFileSync(file, JSON.stringify(scenario));
  const result = successJson(["run", "--scenario", file, "--root", directory, "--dry-run", "--now", NOW]);
  assert.equal(result.recovery.objectCount, 0);
  assert.equal(result.stage, "edit_plan_ready");
  const mixed = invoke(["run", "--scenario", file, "--surface", "desktop", "--json"]);
  assert.equal(mixed.status, 2);
});

test("preflight 从已声明的 Desktop 合同读取能力，并拒绝环境不匹配", (t) => {
  const directory = workspace(t);
  const file = path.join(directory, "session.json");
  fs.writeFileSync(file, JSON.stringify({
    surface: "desktop", skillSource: "managed-desktop", skills: [], provenance: "live",
    capabilities: ["project-read", "timeline-read", "timeline-write", "transcript-read", "speech-edit", "caption-read", "caption-write", "composed-preview"],
    observedAt: "2026-08-09T23:59:00Z", expiresAt: "2026-08-10T00:59:00Z", toolSchemaFingerprint: `sha256:${"a".repeat(64)}`,
  }));
  const result = successJson(["preflight", "--session", file, "--now", NOW]);
  assert.equal(result.contractReady, true);
  assert.equal(result.mediaVerified, false);
  assert.equal(result.surface, "desktop");
  const mismatch = invoke(["preflight", "--session", file, "--surface", "hosted", "--now", NOW, "--json"]);
  assert.equal(mismatch.status, 1);
  assert.ok(JSON.parse(mismatch.stdout).findings.some((item) => item.code === "SESSION_SURFACE_MISMATCH"));
});

test("普通 run --dry-run 解析意图与 Profile 且零落盘", (t) => {
  const directory = workspace(t);
  const stateRoot = path.join(directory, "state-does-not-exist");
  const result = successJson([
    "run",
    "稳剪当前口播",
    "--root", stateRoot,
    "--run-id", "run-cli-dry",
    "--dry-run",
    "--now", NOW,
  ]);
  assert.equal(result.dryRun, true);
  assert.equal(result.stage, "brief_ready");
  assert.equal(result.profile, "balanced-stable");
  assert.equal(result.brief.treatments.music, false);
  assert.equal(result.brief.treatments.export, false);
  assert.equal(fs.existsSync(stateRoot), false);
});

test("fixture run 原子落盘完整状态，status/review/report 可回读", (t) => {
  const stateRoot = workspace(t);
  const created = successJson([
    "run",
    "--root", stateRoot,
    "--scenario-id", "scenario-happy-path",
    "--now", NOW,
  ]);
  assert.equal(created.runId, "run-happy-path");
  assert.equal(created.stage, "review_ready");
  assert.equal(created.recovery.objectCount, 1);
  assert.equal(created.recovery.duplicateWrites, false);

  const runDir = path.join(stateRoot, created.runId);
  for (const relative of [
    "run-manifest.json",
    "project-brief.json",
    "source-inventory.json",
    "decision-log.json",
    "sample-context.json",
    "handoff-report.json",
    "recovery-report.json",
    "checkpoints/cp-sample-ready-001.json",
    "checkpoints/cp-review-ready-002.json",
  ]) {
    const file = path.join(runDir, relative);
    assert.equal(fs.statSync(file).mode & 0o777, 0o600, relative);
  }

  const status = successJson(["status", created.runId, "--root", stateRoot]);
  assert.equal(status.status, "review_ready");
  assert.equal(status.sampleApproval, "approved");
  assert.equal(status.nextAction, "review_editable_timeline");

  const review = successJson(["review", created.runId, "--root", stateRoot]);
  assert.equal(review.sampleApprovalCurrent, true);
  assert.equal(review.decisions.length, 1);
  assert.deepEqual(Object.keys(review.decisions[0]), ["before", "after", "reason", "state", "needsApproval"]);
  assert.equal(JSON.stringify(review).includes("logical:word-range"), false);
  assert.equal(JSON.stringify(review).includes("decisionId"), false);

  const report = successJson(["report", created.runId, "--root", stateRoot]);
  assert.equal(report.deliveryState, "review_ready");
  assert.equal(report.verification.visual, "pass");
  assert.equal(report.verification.humanListening, "unverified");
  assert.ok(report.notPerformed.includes("export"));
});

test("approve-sample 支持预演、六维绑定和重复批准保护", (t) => {
  const directory = workspace(t);
  const stateRoot = path.join(directory, "state");
  fs.mkdirSync(stateRoot);
  const scenario = fixture("scenario-happy-path");
  scenario.scenarioId = "scenario-cli-approval";
  scenario.sampleApproved = false;
  scenario.expectedStage = "sample_ready";
  const scenarioFile = path.join(directory, "approval.json");
  fs.writeFileSync(scenarioFile, JSON.stringify(scenario), {mode: 0o600});

  const created = successJson([
    "run",
    "--root", stateRoot,
    "--scenario", scenarioFile,
    "--run-id", "run-cli-approval",
    "--now", NOW,
  ]);
  assert.equal(created.stage, "sample_ready");
  const manifestFile = path.join(stateRoot, created.runId, "run-manifest.json");
  const before = hash(manifestFile);

  const dryRun = successJson([
    "approve-sample", created.runId,
    "--root", stateRoot,
    "--dry-run",
    "--now", NOW,
  ]);
  assert.equal(dryRun.stage, "sample_approved");
  assert.equal(hash(manifestFile), before);

  const approved = successJson([
    "approve-sample", created.runId,
    "--root", stateRoot,
    "--now", NOW,
  ]);
  assert.equal(approved.stage, "sample_approved");
  const manifest = JSON.parse(fs.readFileSync(manifestFile, "utf8"));
  assert.deepEqual(
    Object.keys(manifest.approvals[0].fingerprints).sort(),
    ["plan", "style", "layout", "captions", "timelineRevision", "sample"].sort(),
  );

  const review = successJson(["review", created.runId, "--root", stateRoot]);
  assert.equal(review.sampleApprovalCurrent, true);

  const duplicate = invoke(["approve-sample", created.runId, "--root", stateRoot, "--json"]);
  assert.equal(duplicate.status, 1);
  assert.equal(JSON.parse(duplicate.stderr).error.code, "RUN_SAMPLE_NOT_READY");
});

test("高风险决定必须通过当前样片的独立批准账本", (t) => {
  const directory = workspace(t);
  const stateRoot = path.join(directory, "state");
  fs.mkdirSync(stateRoot);
  const scenario = fixture("scenario-happy-path");
  scenario.scenarioId = "scenario-cli-high-risk";
  scenario.sampleApproved = false;
  scenario.expectedStage = "sample_ready";
  scenario.decisions = [{
    decisionId: "dec-high-risk",
    type: "whole-sentence",
    action: "remove",
    spokenExcerpt: "完整观点",
    resultExcerpt: "待用户确认",
    reason: "候选整句删除",
    evidenceRefs: ["logical:word-range-high"],
    status: "proposed",
  }];
  const scenarioFile = path.join(directory, "high-risk.json");
  fs.writeFileSync(scenarioFile, JSON.stringify(scenario), {mode: 0o600});
  const created = successJson([
    "run", "--root", stateRoot, "--scenario", scenarioFile,
    "--run-id", "run-cli-high-risk", "--now", NOW,
  ]);
  const approved = successJson([
    "approve-decisions", created.runId,
    "--root", stateRoot,
    "--decision-id", "dec-high-risk",
    "--now", NOW,
  ]);
  assert.equal(approved.approvalRef, "logical:decision-approval-cli-high-risk");
  const manifest = JSON.parse(fs.readFileSync(path.join(stateRoot, created.runId, "run-manifest.json"), "utf8"));
  const ledger = manifest.approvals.find((item) => item.kind === "decision");
  assert.deepEqual(ledger.scope, ["logical:decision-dec-high-risk"]);
  const log = JSON.parse(fs.readFileSync(path.join(stateRoot, created.runId, "decision-log.json"), "utf8"));
  assert.equal(log.decisions[0].status, "approved");
  assert.equal(log.decisions[0].approvalRef, ledger.approvalRef);

  log.decisions[0].status = "applied";
  log.decisions[0].approvalRef = "logical:invented-approval";
  fs.writeFileSync(path.join(stateRoot, created.runId, "decision-log.json"), `${JSON.stringify(log, null, 2)}\n`);
  const forged = invoke(["review", created.runId, "--root", stateRoot, "--json"]);
  assert.equal(forged.status, 2);
  assert.equal(JSON.parse(forged.stderr).error.code, "DECISION_LOG_POLICY_INVALID");
});

test("request-revision 把样片退回重规划且不复用旧绑定", (t) => {
  const directory = workspace(t);
  const stateRoot = path.join(directory, "state");
  fs.mkdirSync(stateRoot);
  const scenario = fixture("scenario-happy-path");
  scenario.scenarioId = "scenario-cli-revision";
  scenario.sampleApproved = false;
  scenario.expectedStage = "sample_ready";
  const scenarioFile = path.join(directory, "revision.json");
  fs.writeFileSync(scenarioFile, JSON.stringify(scenario), {mode: 0o600});
  const created = successJson([
    "run", "--root", stateRoot, "--scenario", scenarioFile,
    "--run-id", "run-cli-revision", "--now", NOW,
  ]);
  const revised = successJson([
    "request-revision", created.runId,
    "--root", stateRoot,
    "--direction", "natural",
    "--now", NOW,
  ]);
  assert.equal(revised.stage, "revision_requested");
  const manifest = JSON.parse(fs.readFileSync(path.join(stateRoot, created.runId, "run-manifest.json"), "utf8"));
  assert.equal(manifest.sampleBinding, null);
});

test("partial-write 补偿后的 run 仅可凭 checkpoint 和对账证据安全恢复", (t) => {
  const stateRoot = workspace(t);
  const created = successJson([
    "run",
    "--root", stateRoot,
    "--scenario-id", "scenario-partial-write",
    "--now", NOW,
  ]);
  assert.equal(created.status, "blocked");
  assert.equal(created.recovery.objectCount, 1);
  assert.equal(created.recovery.reconciliations.includes("compensated"), true);

  const resumed = successJson([
    "resume", created.runId,
    "--root", stateRoot,
    "--timeline-revision", created.manifest.project.timelineRevision,
    "--reconcile-outcome", "compensated",
    "--evidence-ref", "logical:partial-write-readback",
    "--checkpoint-id", "cp-sample-ready-001",
    "--now", NOW,
  ]);
  assert.equal(resumed.stage, "edit_plan_ready");
  assert.equal(resumed.status, "active");
  assert.equal(resumed.sampleApproval, "stale");
  assert.equal(resumed.blocker, null);

  const report = successJson(["report", created.runId, "--root", stateRoot]);
  assert.equal(report.deliveryState, "in_progress");
  assert.equal(report.verification.sampleApproval, "stale");
});

test("resume 发现新 revision 时审批 stale 且仍 blocked", (t) => {
  const stateRoot = workspace(t);
  const created = successJson([
    "run",
    "--root", stateRoot,
    "--scenario-id", "scenario-partial-write",
    "--run-id", "run-cli-drift",
    "--now", NOW,
  ]);
  const resumed = successJson([
    "resume", created.runId,
    "--root", stateRoot,
    "--timeline-revision", "rev-new",
    "--now", NOW,
  ]);
  assert.equal(resumed.status, "blocked");
  assert.equal(resumed.timelineRevision, "rev-new");
  assert.equal(resumed.sampleApproval, "stale");
  assert.equal(resumed.blocker.code, "TIMELINE_REVISION_DRIFT");

  const status = successJson(["status", created.runId, "--root", stateRoot]);
  assert.equal(status.sampleApproval, "stale");
  assert.equal(status.status, "blocked");
});

test("重复 run ID 被拒绝且已有 manifest 不变", (t) => {
  const stateRoot = workspace(t);
  successJson(["run", "--root", stateRoot, "--run-id", "run-duplicate", "--now", NOW]);
  const manifest = path.join(stateRoot, "run-duplicate", "run-manifest.json");
  const before = hash(manifest);
  const duplicate = invoke(["run", "--root", stateRoot, "--run-id", "run-duplicate", "--json", "--now", NOW]);
  assert.equal(duplicate.status, 1);
  assert.equal(JSON.parse(duplicate.stderr).error.code, "RUN_ALREADY_EXISTS");
  assert.equal(hash(manifest), before);
});

test("不安全路径、重复参数和 traversal run ID 都产生脱敏错误", (t) => {
  const directory = workspace(t);
  const realState = path.join(directory, "real-state");
  const linkedState = path.join(directory, "linked-state");
  fs.mkdirSync(realState);
  fs.symlinkSync(realState, linkedState);

  const unsafe = invoke(["run", "--root", linkedState, "--run-id", "run-unsafe", "--json"]);
  assert.equal(unsafe.status, 2);
  const unsafeError = JSON.parse(unsafe.stderr);
  assert.equal(unsafeError.error.code, "STATE_DIRECTORY_UNSAFE");
  assert.equal(unsafe.stderr.includes(directory), false);

  const duplicate = invoke(["status", "run-safe", "--root", realState, "--root", realState, "--json"]);
  assert.equal(duplicate.status, 2);
  assert.equal(JSON.parse(duplicate.stderr).error.code, "CLI_USAGE");

  const ambiguousOutput = invoke(["status", "run-safe", "--root", realState, "--json", "--format", "json"]);
  assert.equal(ambiguousOutput.status, 2);
  assert.equal(JSON.parse(ambiguousOutput.stderr).error.code, "CLI_USAGE");

  const traversal = invoke(["status", "../secret", "--root", realState, "--json"]);
  assert.equal(traversal.status, 1);
  assert.equal(JSON.parse(traversal.stderr).error.code, "RUN_ID_INVALID");
  assert.equal(traversal.stderr.includes(directory), false);
});
