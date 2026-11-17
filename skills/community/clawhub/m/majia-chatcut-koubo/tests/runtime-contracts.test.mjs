import assert from "node:assert/strict";
import {LIVE_CANARY_REPORT} from "../src/config/release-files.mjs";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";
import {assertSourceInventoryBindings} from "../src/orchestration/source-inventory.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("source inventory 的 mainSourceRef 与 logicalRef 必须一一绑定", () => {
  const base = {
    mainSourceRef: "logical:aroll-main",
    assets: [{logicalRef: "logical:aroll-main"}],
  };
  assert.equal(assertSourceInventoryBindings(base), true);
  assert.throws(
    () => assertSourceInventoryBindings({...base, assets: [...base.assets, {logicalRef: "logical:aroll-main"}]}),
    (error) => error.code === "SOURCE_LOGICAL_REF_DUPLICATE",
  );
  assert.throws(
    () => assertSourceInventoryBindings({...base, mainSourceRef: "logical:missing"}),
    (error) => error.code === "SOURCE_MAIN_REF_UNRESOLVED",
  );
});

function run(script, args = []) {
  return spawnSync(process.execPath, [script, ...args], {
    cwd: root,
    encoding: "utf8",
  });
}

function outputJson(result) {
  assert.equal(result.stdout.trim().startsWith("{"), true, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}

test("runtime schemas, profiles, templates, fixtures and generated documents agree", () => {
  const result = run("scripts/validate-runtime-fixtures.mjs", ["--json"]);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = outputJson(result);
  assert.equal(report.ok, true);
  assert.equal(report.scenarios >= 10, true);
  assert.equal(report.generatedDocuments > report.scenarios, true);
  assert.equal(report.evidenceBoundary, "offline-contracts-only");
  assert.equal(report.liveChatCutVerified, false);
});

test("one-click smoke proves recovery without pretending to be live evidence", () => {
  const result = run("scripts/smoke-one-click.mjs", ["--json"]);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = outputJson(result);
  assert.equal(report.scenarios.happy.status, "review_ready");
  assert.equal(report.scenarios.timeoutBefore.reconciliation, "retry");
  assert.equal(report.scenarios.timeoutAfter.reconciliation, "readback");
  assert.equal(report.scenarios.partialWrite.compensated, true);
  assert.equal(report.scenarios.manualEdit.preserved, true);
  assert.equal(report.evidence.class, "offline-simulation");
  assert.equal(report.evidence.liveChatCut, "unverified");
  assert.equal(report.evidence.humanListening, "unverified");
  assert.equal(report.evidence.stableClaimEligible, false);
});

test("current live canary report is allowed to remain explicitly ineligible", () => {
  const result = run("scripts/validate-live-canary-claim.mjs", ["--json"]);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = outputJson(result);
  assert.equal(report.capabilityStatus, "unverified");
  assert.equal(report.passedCanaries, 0);
  assert.equal(report.stableClaimEligible, false);
  assert.equal(report.computedEligible, false);
});

test("live claim eligibility requires fresh capability fingerprints and every recovery check", (t) => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-live-eligible-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  fs.mkdirSync(path.join(directory, "schemas/runtime"), {recursive: true});
  fs.mkdirSync(path.join(directory, "reports"), {recursive: true});
  fs.copyFileSync(
    path.join(root, "schemas/runtime/live-canary-report.schema.json"),
    path.join(directory, "schemas/runtime/live-canary-report.schema.json"),
  );
  const report = JSON.parse(fs.readFileSync(path.join(root, LIVE_CANARY_REPORT), "utf8"));
  const now = Date.now();
  report.capabilityStatus = "current";
  report.capabilityObservedAt = new Date(now - 60_000).toISOString();
  report.capabilityExpiresAt = new Date(now + 86_400_000).toISOString();
  report.capabilityBuildFingerprint = "chatcut-build-current";
  report.toolSchemaFingerprint = `sha256:${"a".repeat(64)}`;
  const requiredChecks = [
    "timeout-before",
    "timeout-after",
    "partial-write",
    "manual-edit-protected",
    "no-unapproved-high-risk",
    "no-duplicate-write",
    "evidence-separated",
    "starter-prompt-routed",
  ];
  for (const [index, canary] of report.canaries.entries()) {
    canary.status = index < 5 ? "pass" : "not_run";
    canary.evidenceLevel = index < 5 ? "E2" : "none";
    canary.checks = index < 5 ? requiredChecks.filter((_, checkIndex) => checkIndex % 5 === index) : [];
  }
  report.metrics = {
    passedCanaries: 5,
    unapprovedHighRiskEdits: 0,
    duplicateWrites: 0,
    manualEditsOverwritten: 0,
    evidenceStateConfusions: 0,
    recoveryObservedRate: 0.95,
  };
  report.stableClaimEligible = true;
  fs.writeFileSync(path.join(directory, LIVE_CANARY_REPORT), `${JSON.stringify(report, null, 2)}\n`);
  fs.writeFileSync(path.join(directory, "README.md"), "# Eligible live report\n");
  fs.writeFileSync(path.join(directory, "SKILL.md"), "# Eligible live report\n");

  const eligible = run("scripts/validate-live-canary-claim.mjs", ["--root", directory, "--json"]);
  assert.equal(eligible.status, 0, eligible.stderr || eligible.stdout);
  assert.equal(outputJson(eligible).computedEligible, true);

  report.canaries[0].checks = report.canaries[0].checks.filter((check) => check !== "timeout-before");
  fs.writeFileSync(path.join(directory, LIVE_CANARY_REPORT), `${JSON.stringify(report, null, 2)}\n`);
  const incomplete = run("scripts/validate-live-canary-claim.mjs", ["--root", directory]);
  assert.equal(incomplete.status, 1);
  assert.match(incomplete.stderr, /LIVE_CLAIM_ELIGIBILITY_UNSUPPORTED/);
});

test("unqualified production stability claims fail while live evidence is absent", (t) => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-live-claim-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  fs.mkdirSync(path.join(directory, "schemas/runtime"), {recursive: true});
  fs.mkdirSync(path.join(directory, "reports"), {recursive: true});
  fs.copyFileSync(
    path.join(root, "schemas/runtime/live-canary-report.schema.json"),
    path.join(directory, "schemas/runtime/live-canary-report.schema.json"),
  );
  fs.copyFileSync(
    path.join(root, LIVE_CANARY_REPORT),
    path.join(directory, LIVE_CANARY_REPORT),
  );
  fs.writeFileSync(
    path.join(directory, "README.md"),
    "# Demo\n\n真实 ChatCut 端到端已经验证通过并稳定可用。\n\n其他实验仍为 UNVERIFIED。\n",
  );
  fs.writeFileSync(
    path.join(directory, "SKILL.md"),
    "# Demo\n\n真实 ChatCut 仍未验证（UNVERIFIED）。\n",
  );

  const result = run("scripts/validate-live-canary-claim.mjs", [
    "--root",
    directory,
  ]);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /LIVE_CLAIM_UNQUALIFIED_PRODUCTION_CLAIM/);
  assert.doesNotMatch(result.stderr, new RegExp(directory.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
});

test("doctor is read-only and cannot promote UNVERIFIED capability", () => {
  const result = run("scripts/doctor.mjs", ["--json"]);
  assert.equal([0, 1].includes(result.status), true, result.stderr || result.stdout);
  const report = outputJson(result);
  assert.equal(report.mode, "read-only");
  assert.equal(report.capability.status, "unverified");
  assert.equal(report.capability.promotedByDoctor, false);
  assert.equal(report.liveClaimAudit.ok, true);
  assert.equal(report.liveClaimAudit.computedEligible, false);
  assert.equal(report.liveReady, false);
  assert.equal(report.verificationScope, "source-checkout");
  assert.doesNotMatch(result.stdout, new RegExp(root.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
});

test("doctor degrades honestly in a registry package without fixtures or dotfiles", (t) => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-doctor-package-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  fs.cpSync(root, directory, {
    recursive: true,
    filter: (source) => {
      const relative = path.relative(root, source);
      if (!relative) return true;
      const first = relative.split(path.sep)[0];
      return ![".git", ".github", ".node-version", "node_modules", "fixtures", "tests"].includes(first);
    },
  });
  const result = run(path.join(directory, "scripts/doctor.mjs"), ["--root", directory, "--json"]);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = outputJson(result);
  assert.equal(report.offlineReady, true);
  assert.equal(report.runtimeContracts.status, "not_packaged");
  assert.equal(report.runtimeContracts.evidence, "release-gates-not-bundled");
  assert.equal(report.verificationScope, "distribution-package");
  assert.equal(report.node.source, "package.json#engines.node");
  assert.equal(report.liveReady, false);
});

test("user-facing docs route starter prompts, official skills and maintainer commands", () => {
  const result = run("scripts/validate-docs-routing.mjs", ["--json"]);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const report = outputJson(result);
  assert.equal(report.ok, true);
  const official = JSON.parse(fs.readFileSync(path.join(root, "reports/official-source-current.json"), "utf8"));
  assert.equal(report.officialSkills, official.hostedSkills.length);
  assert.equal(report.starterPrompts, 4);
  assert.deepEqual(report.findings, []);
});
