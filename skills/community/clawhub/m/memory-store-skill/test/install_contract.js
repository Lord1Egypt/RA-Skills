#!/usr/bin/env node
"use strict";

const assert = require("assert");
const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const INSTALLER = path.join(ROOT, "scripts", "install.js");
const UPDATER = path.join(ROOT, "scripts", "update.js");
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "memory-store-install-contract-"));
const tempHome = path.join(tempRoot, "home");
const claudeConfig = path.join(tempRoot, "claude-config");
const codexConfig = path.join(tempRoot, "codex-config");
const manualTarget = path.join(tempRoot, "manual-target");
const dryRunTarget = path.join(tempRoot, "dry-run-target");
const policyTarget = path.join(tempRoot, "policy-target");

fs.mkdirSync(tempHome, { recursive: true });

const isolatedEnv = {
  ...process.env,
  HOME: tempHome,
  USERPROFILE: tempHome,
  CLAUDE_CONFIG_DIR: claudeConfig,
  CODEX_CONFIG_DIR: codexConfig,
};

function runNode(args, expectedStatus = 0) {
  const result = spawnSync(process.execPath, args, {
    cwd: ROOT,
    env: isolatedEnv,
    encoding: "utf8",
  });
  const output = `${result.stdout || ""}${result.stderr || ""}`;
  assert.strictEqual(
    result.status,
    expectedStatus,
    `Expected exit ${expectedStatus}, got ${result.status}:\n${output}`
  );
  return output;
}

function hash(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function assertSame(relative, installedRoot) {
  const source = path.join(ROOT, relative);
  const installed = path.join(installedRoot, relative);
  assert.ok(fs.existsSync(installed), `Expected installed artifact: ${installed}`);
  assert.strictEqual(hash(installed), hash(source), `Artifact differs: ${relative}`);
}

try {
  assert.match(runNode([INSTALLER, "--unknown"], 1), /Unknown option/);
  assert.match(runNode([INSTALLER, "--target"], 1), /Missing value/);
  assert.match(runNode([INSTALLER, "--all", "--agent", "claude"], 1), /mutually exclusive/);
  assert.match(runNode([INSTALLER, "--check", "--dry-run", "--target", dryRunTarget], 1), /cannot be combined/);
  assert.match(runNode([INSTALLER, "--check", "--update", "--agent", "claude"], 1), /cannot be combined/);

  const dryRunOutput = runNode([INSTALLER, "--target", dryRunTarget, "--memory-profile", "proactive", "--dry-run"]);
  assert.match(dryRunOutput, /Would copy and verify/);
  assert.match(dryRunOutput, /Would set memory profile 'proactive'/);
  assert.ok(!fs.existsSync(dryRunTarget), "--dry-run must not create the target directory");
  assert.ok(!fs.existsSync(path.join(tempHome, ".memory-store")), "--dry-run must not initialize a memory store");
  assert.match(runNode([INSTALLER, "--target", dryRunTarget, "--memory-profile", "invalid"], 1), /Invalid memory profile/);

  const installOutput = runNode([INSTALLER, "--agent", "claude,codex"]);
  const claudeSkill = path.join(claudeConfig, "skills", "memory-store");
  const codexSkill = path.join(codexConfig, "skills", "memory-store");
  assert.match(installOutput, /Verified \d+ artifact\(s\)/);
  assert.ok(installOutput.includes(claudeSkill), "CLAUDE_CONFIG_DIR must determine the install target");
  assert.ok(installOutput.includes(codexSkill), "CODEX_CONFIG_DIR must determine the install target");

  for (const installedRoot of [claudeSkill, codexSkill]) {
    assertSame("SKILL.md", installedRoot);
    assertSame(path.join("scripts", "memory_cli.js"), installedRoot);
    assertSame(path.join("agents", "openai.yaml"), installedRoot);
    assertSame(path.join("references", "memory_schema.json"), installedRoot);
  }

  runNode([INSTALLER, "--check", "--agent", "claude,codex"]);
  assert.ok(!fs.existsSync(path.join(tempHome, ".memory-store")), "installation without a profile must not create a global store");

  runNode([INSTALLER, "--target", policyTarget, "--memory-profile", "balanced"]);
  const policy = JSON.parse(fs.readFileSync(path.join(tempHome, ".memory-store", "config.json"), "utf8"));
  assert.strictEqual(policy.profile, "balanced");
  assert.ok(!fs.existsSync(path.join(tempHome, ".memory-store", "memories.json")), "policy setup must not initialize memory data");

  fs.appendFileSync(path.join(claudeSkill, "SKILL.md"), "\ncontract-test-stale-copy\n", "utf8");
  const staleOutput = runNode([INSTALLER, "--check", "--agent", "claude"], 1);
  assert.match(staleOutput, /Changed: SKILL\.md/);
  const updateOutput = runNode([INSTALLER, "--update", "--agent", "claude"]);
  assert.match(updateOutput, /Updating 1 existing target/);
  assert.match(updateOutput, /1 target\(s\) changed/);
  runNode([INSTALLER, "--check", "--agent", "claude"]);

  const currentOutput = runNode([INSTALLER, "--update", "--agent", "claude"]);
  assert.match(currentOutput, /Already current/);
  assert.match(currentOutput, /0 target\(s\) changed/);

  const missingUpdateTarget = path.join(tempRoot, "missing-update-target");
  assert.match(runNode([INSTALLER, "--update", "--target", missingUpdateTarget], 1), /no existing installation/);
  assert.ok(!fs.existsSync(missingUpdateTarget), "--update must not create a new installation");

  fs.appendFileSync(path.join(codexSkill, "SKILL.md"), "\ncontract-test-updater-copy\n", "utf8");
  const updaterPreview = runNode([UPDATER, "--agent", "codex", "--dry-run"]);
  assert.match(updaterPreview, /1 target\(s\) need update/);
  assert.notStrictEqual(
    hash(path.join(codexSkill, "SKILL.md")),
    hash(path.join(ROOT, "SKILL.md")),
    "updater --dry-run must not change installed files"
  );
  const updaterOutput = runNode([UPDATER, "--agent", "codex"]);
  assert.match(updaterOutput, /Syncing from the currently installed memory-store-skill package/);
  runNode([INSTALLER, "--check", "--agent", "codex"]);

  runNode([INSTALLER, "--target", manualTarget]);
  runNode([INSTALLER, "--check", "--target", manualTarget]);
  assertSame("SKILL.md", manualTarget);
  assertSame(path.join("scripts", "memory_cli.js"), manualTarget);

  const pkg = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8"));
  assert.strictEqual(pkg.bin["memory-store-update"], "scripts/update.js");
  assert.ok(pkg.files.includes("scripts/update.js"), "package files must include scripts/update.js");
  for (const directory of ["agents", "examples", "references"]) {
    assert.ok(pkg.files.includes(directory), `package files must include ${directory}/`);
  }
  assert.match(pkg.scripts.test, /install_contract\.js/);

  assert.ok(!Object.prototype.hasOwnProperty.call(pkg.scripts, "postinstall"));
  assert.ok(!pkg.files.includes("scripts/postinstall.js"));
  assert.ok(!fs.existsSync(path.join(ROOT, "scripts", "postinstall.js")));

  const versionOutput = runNode([path.join(manualTarget, "scripts", "memory_cli.js"), "version"]);
  assert.ok(versionOutput.includes(`v${pkg.version}`), "installed CLI version must match package.json");

  console.log("Install contract tests passed.");
} finally {
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
