#!/usr/bin/env node

import {spawnSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {LIVE_CANARY_REPORT} from "../src/config/release-files.mjs";

const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const REQUIRED_PATHS = Object.freeze([
  "SKILL.md",
  "profiles/balanced-stable.json",
  "profiles/tight-short.json",
  "profiles/trust-longform.json",
  "profiles/screen-demo.json",
  "schemas/runtime/run-manifest.schema.json",
  "schemas/runtime/decision-log.schema.json",
  "schemas/runtime/checkpoint.schema.json",
  "schemas/runtime/handoff-report.schema.json",
  LIVE_CANARY_REPORT,
  "src/orchestration/orchestrator.mjs",
  "src/cli/koubo.mjs",
  "scripts/validate-live-canary-claim.mjs",
]);
const SOURCE_AUDIT_PATHS = Object.freeze([
  "fixtures/runtime/scenarios.json",
  "scripts/validate-runtime-fixtures.mjs",
]);

function usage(message) {
  process.stderr.write("Usage: node scripts/doctor.mjs [--root <repository-root>] [--json]\n");
  if (message) process.stderr.write(`${message}\n`);
  process.exit(2);
}

function parseArguments(argv) {
  let root = DEFAULT_ROOT;
  let json = false;
  let rootSeen = false;
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (option === "--json") {
      if (json) usage("duplicate option: --json");
      json = true;
      continue;
    }
    if (option === "--root") {
      if (rootSeen) usage("duplicate option: --root");
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) usage("--root requires a value");
      root = path.resolve(value);
      rootSeen = true;
      index += 1;
      continue;
    }
    usage("unknown option");
  }
  return {root, json};
}

function readText(root, relativePath) {
  const absolute = path.resolve(root, relativePath);
  const relative = path.relative(root, absolute);
  if (!relative || relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error("DOCTOR_PATH_OUTSIDE_ROOT");
  }
  return fs.readFileSync(absolute, "utf8");
}

function parseVersion(value) {
  const match = String(value).trim().replace(/^v/u, "").match(/^(\d+)\.(\d+)\.(\d+)$/u);
  return match ? match.slice(1).map(Number) : null;
}

function compareVersion(left, right) {
  for (let index = 0; index < 3; index += 1) {
    if (left[index] !== right[index]) return left[index] - right[index];
  }
  return 0;
}

function checkNode(root) {
  let pinnedText;
  let source;
  try {
    pinnedText = readText(root, ".node-version").trim();
    source = ".node-version";
  } catch {
    const manifest = JSON.parse(readText(root, "package.json"));
    const match = String(manifest.engines?.node ?? "").match(/>=\s*(\d+\.\d+\.\d+)\s+<\s*(\d+)/u);
    if (!match || Number(match[2]) !== Number(match[1].split(".")[0]) + 1) {
      return {supported: false, current: process.version.replace(/^v/u, ""), pinned: null, source: "unavailable"};
    }
    pinnedText = match[1];
    source = "package.json#engines.node";
  }
  const pinned = parseVersion(pinnedText);
  const current = parseVersion(process.version);
  const supported = Boolean(
    pinned
      && current
      && current[0] === pinned[0]
      && compareVersion(current, pinned) >= 0,
  );
  return {supported, current: process.version.replace(/^v/u, ""), pinned: pinnedText, source};
}

function checkPaths(root) {
  const missing = [];
  const unsafe = [];
  for (const relativePath of REQUIRED_PATHS) {
    try {
      const stat = fs.lstatSync(path.join(root, relativePath));
      if (!stat.isFile() || stat.isSymbolicLink()) unsafe.push(relativePath);
    } catch {
      missing.push(relativePath);
    }
  }
  return {ok: missing.length === 0 && unsafe.length === 0, missing, unsafe};
}

function runRuntimeAudit(root) {
  const result = spawnSync(
    process.execPath,
    [path.join(root, "scripts/validate-runtime-fixtures.mjs"), "--root", root, "--json"],
    {cwd: root, encoding: "utf8", env: {...process.env, MAJIA_RUNTIME_DEBUG: "0"}},
  );
  return {
    ok: result.status === 0,
    code: result.status ?? 1,
    status: result.status === 0 ? "passed" : "failed",
  };
}

function sourceAuditAvailable(root) {
  return SOURCE_AUDIT_PATHS.every((relativePath) => {
    try {
      const stat = fs.lstatSync(path.join(root, relativePath));
      return stat.isFile() && !stat.isSymbolicLink();
    } catch {
      return false;
    }
  });
}

function runLiveClaimAudit(root) {
  const result = spawnSync(
    process.execPath,
    [path.join(root, "scripts/validate-live-canary-claim.mjs"), "--root", root, "--json"],
    {cwd: root, encoding: "utf8"},
  );
  if (result.status !== 0) return {ok: false, computedEligible: false, code: result.status ?? 1};
  try {
    const report = JSON.parse(result.stdout);
    return {
      ok: report.ok === true,
      computedEligible: report.computedEligible === true,
      stableClaimEligible: report.stableClaimEligible === true,
      capabilityStatus: report.capabilityStatus,
      code: 0,
    };
  } catch {
    return {ok: false, computedEligible: false, code: 1};
  }
}

function readCapability(root) {
  let report;
  try {
    report = JSON.parse(readText(root, LIVE_CANARY_REPORT));
  } catch {
    return {status: "unverified", stableClaimEligible: false, reason: "report-unavailable"};
  }
  const status = ["unverified", "current", "stale", "blocked"].includes(report.capabilityStatus)
    ? report.capabilityStatus
    : "unverified";
  return {
    status,
    stableClaimEligible: report.stableClaimEligible === true,
    reason: report.stableClaimEligible === true ? "report-claims-eligible" : "live-evidence-not-established",
  };
}

function gitSnapshot(root) {
  const result = spawnSync("git", ["status", "--short", "--branch"], {
    cwd: root,
    encoding: "utf8",
  });
  if (result.status !== 0) return {available: false, clean: null};
  const lines = result.stdout.trim().split(/\r?\n/u).filter(Boolean);
  return {available: true, clean: lines.slice(1).length === 0};
}

const options = parseArguments(process.argv.slice(2));
try {
  const node = checkNode(options.root);
  const files = checkPaths(options.root);
  const hasSourceAudit = sourceAuditAvailable(options.root);
  const runtimeContracts = hasSourceAudit
    ? runRuntimeAudit(options.root)
    : {ok: true, code: null, status: "not_packaged", evidence: "release-gates-not-bundled"};
  const capability = readCapability(options.root);
  const liveClaimAudit = runLiveClaimAudit(options.root);
  const git = gitSnapshot(options.root);
  const offlineReady = node.supported && files.ok && runtimeContracts.ok;
  const liveReady = liveClaimAudit.ok
    && liveClaimAudit.computedEligible
    && liveClaimAudit.stableClaimEligible
    && liveClaimAudit.capabilityStatus === "current";
  const result = {
    ok: offlineReady,
    mode: "read-only",
    node,
    files,
    runtimeContracts,
    verificationScope: hasSourceAudit ? "source-checkout" : "distribution-package",
    liveClaimAudit,
    git,
    capability: {
      ...capability,
      liveReady,
      promotedByDoctor: false,
    },
    offlineReady,
    liveReady,
  };
  if (options.json) process.stdout.write(`${JSON.stringify(result)}\n`);
  else {
    process.stdout.write(`doctor: offline=${offlineReady ? "READY" : "NOT_READY"}, live=${liveReady ? "READY" : capability.status.toUpperCase()}, mode=read-only\n`);
    if (files.missing.length > 0) process.stdout.write(`missing: ${files.missing.join(", ")}\n`);
    if (!node.supported) process.stdout.write(`node: current ${node.current}, expected ${node.pinned}.x-compatible runtime\n`);
  }
  if (!offlineReady) process.exitCode = 1;
} catch {
  process.stderr.write("DOCTOR_AUDIT_UNAVAILABLE: read-only doctor failed\n");
  process.exitCode = 2;
}
