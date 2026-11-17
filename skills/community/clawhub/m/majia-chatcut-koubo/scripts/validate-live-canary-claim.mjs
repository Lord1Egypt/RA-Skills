#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import {LIVE_CANARY_REPORT} from "../src/config/release-files.mjs";

const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DEFAULT_REPORT = LIVE_CANARY_REPORT;
const CLAIM_FILES = Object.freeze(["README.md", "SKILL.md"]);
const QUALIFIER = /(?:UNVERIFIED|unverified|未验证|尚未|仍需|需要.{0,12}证据|须另有.{0,12}证据|离线|fake|模拟|目标|不宣称|不代表|不得|不能|待验证|当前边界|canary)/iu;
const STRONG_CLAIMS = Object.freeze([
  /(?:真实|线上|生产环境).{0,28}(?:已验证|验证通过|稳定可用|生产可用|端到端.{0,8}通过|完整闭环)/iu,
  /(?:一键稳定剪辑|稳定一键剪辑|一键稳剪).{0,28}(?:已实现|已完成|已验证|稳定可用|生产可用|全自动|端到端)/iu,
  /(?:real|live|production).{0,28}(?:verified|production-ready|stable|end-to-end\s+passed)/iu,
]);
const REQUIRED_LIVE_CHECKS = Object.freeze([
  "timeout-before",
  "timeout-after",
  "partial-write",
  "manual-edit-protected",
  "no-unapproved-high-risk",
  "no-duplicate-write",
  "evidence-separated",
  "starter-prompt-routed",
]);

function usage(message) {
  process.stderr.write("Usage: node scripts/validate-live-canary-claim.mjs [--root <repository-root>] [--report <relative-json>] [--json]\n");
  if (message) process.stderr.write(`${message}\n`);
  process.exit(2);
}

function parseArguments(argv) {
  let root = DEFAULT_ROOT;
  let report = DEFAULT_REPORT;
  let json = false;
  const seen = new Set();
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (option === "--json") {
      if (seen.has(option)) usage("duplicate option: --json");
      seen.add(option);
      json = true;
      continue;
    }
    if (option === "--root" || option === "--report") {
      if (seen.has(option)) usage(`duplicate option: ${option}`);
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) usage(`${option} requires a value`);
      seen.add(option);
      if (option === "--root") root = path.resolve(value);
      else report = value;
      index += 1;
      continue;
    }
    usage("unknown option");
  }
  return {root, report, json};
}

function resolveInside(root, relativePath) {
  const absolute = path.resolve(root, relativePath);
  const relative = path.relative(root, absolute);
  if (!relative || relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error("LIVE_CLAIM_PATH_OUTSIDE_ROOT");
  }
  return absolute;
}

function readText(root, relativePath) {
  const absolute = resolveInside(root, relativePath);
  try {
    const stat = fs.lstatSync(absolute);
    if (!stat.isFile() || stat.isSymbolicLink()) throw new Error();
    return fs.readFileSync(absolute, "utf8");
  } catch {
    throw new Error(`LIVE_CLAIM_FILE_UNAVAILABLE:${relativePath}`);
  }
}

function readJson(root, relativePath) {
  try {
    return JSON.parse(readText(root, relativePath));
  } catch (error) {
    if (error?.message?.startsWith("LIVE_CLAIM_")) throw error;
    throw new Error(`LIVE_CLAIM_JSON_INVALID:${relativePath}`);
  }
}

function requireCondition(condition, code) {
  if (!condition) throw new Error(code);
}

function validateReport(root, reportPath) {
  const schema = readJson(root, "schemas/runtime/live-canary-report.schema.json");
  const report = readJson(root, reportPath);
  const ajv = new Ajv2020({allErrors: true, logger: false, strict: true});
  addFormats(ajv);
  const validate = ajv.compile(schema);
  requireCondition(validate(report), "LIVE_CLAIM_REPORT_SCHEMA_INVALID");

  const passed = report.canaries.filter((canary) => canary.status === "pass");
  requireCondition(
    report.metrics.passedCanaries === passed.length,
    "LIVE_CLAIM_PASSED_COUNT_DRIFT",
  );

  const zeroRisk = [
    report.metrics.unapprovedHighRiskEdits,
    report.metrics.duplicateWrites,
    report.metrics.manualEditsOverwritten,
    report.metrics.evidenceStateConfusions,
  ].every((value) => value === 0);
  const shapes = new Set(passed.map((canary) => canary.shape));
  const durations = new Set(
    passed
      .map((canary) => canary.durationClass)
      .filter((value) => ["short", "medium", "long"].includes(value)),
  );
  const checks = new Set(passed.flatMap((canary) => canary.checks));
  const caseIds = report.canaries.map((canary) => canary.caseId);
  const now = Date.now();
  const observedAt = Date.parse(report.capabilityObservedAt ?? "");
  const expiresAt = Date.parse(report.capabilityExpiresAt ?? "");
  const capabilityFresh = Number.isFinite(observedAt)
    && Number.isFinite(expiresAt)
    && observedAt <= now
    && expiresAt > now;
  const evidenceSufficient = passed.every((canary) => ["E2", "E3"].includes(canary.evidenceLevel));
  requireCondition(new Set(caseIds).size === caseIds.length, "LIVE_CLAIM_CASE_ID_DUPLICATE");
  const computedEligible = report.capabilityStatus === "current"
    && capabilityFresh
    && typeof report.capabilityBuildFingerprint === "string"
    && report.capabilityBuildFingerprint.length > 0
    && typeof report.toolSchemaFingerprint === "string"
    && passed.length >= 5
    && shapes.size >= 3
    && durations.size >= 3
    && REQUIRED_LIVE_CHECKS.every((check) => checks.has(check))
    && zeroRisk
    && (report.metrics.recoveryObservedRate ?? 0) >= 0.95
    && evidenceSufficient;

  if (report.stableClaimEligible) {
    requireCondition(computedEligible, "LIVE_CLAIM_ELIGIBILITY_UNSUPPORTED");
  }
  return {report, passed: passed.length, computedEligible};
}

function auditClaims(root, stableClaimEligible) {
  const findings = [];
  for (const file of CLAIM_FILES) {
    const text = readText(root, file);
    if (!stableClaimEligible) {
      requireCondition(
        /(?:UNVERIFIED|unverified|未验证|尚不宣称真实|须另有.{0,12}证据|真实.{0,20}仍.{0,8}验证)/iu.test(text),
        `LIVE_CLAIM_BOUNDARY_MISSING:${file}`,
      );
      for (const [index, line] of text.split(/\r?\n/u).entries()) {
        if (STRONG_CLAIMS.some((pattern) => pattern.test(line)) && !QUALIFIER.test(line)) {
          findings.push({file, line: index + 1});
        }
      }
    }
  }
  requireCondition(findings.length === 0, "LIVE_CLAIM_UNQUALIFIED_PRODUCTION_CLAIM");
  return findings;
}

const options = parseArguments(process.argv.slice(2));
try {
  const {report, passed, computedEligible} = validateReport(options.root, options.report);
  auditClaims(options.root, report.stableClaimEligible);
  const result = {
    ok: true,
    report: options.report,
    capabilityStatus: report.capabilityStatus,
    passedCanaries: passed,
    stableClaimEligible: report.stableClaimEligible,
    computedEligible,
    documentsQualified: !report.stableClaimEligible,
  };
  if (options.json) process.stdout.write(`${JSON.stringify(result)}\n`);
  else process.stdout.write(
    `live canary claim audit passed: capability=${result.capabilityStatus}, passed=${result.passedCanaries}, stableClaimEligible=${result.stableClaimEligible}; public claims remain qualified\n`,
  );
} catch (error) {
  const message = typeof error?.message === "string" ? error.message : "LIVE_CLAIM_AUDIT_FAILED";
  const safe = /^LIVE_CLAIM_[A-Z0-9_]+(?::[A-Za-z0-9._/-]+)?$/u.test(message)
    ? message
    : "LIVE_CLAIM_AUDIT_FAILED";
  process.stderr.write(`${safe}: live canary claim audit failed\n`);
  process.exitCode = 1;
}
