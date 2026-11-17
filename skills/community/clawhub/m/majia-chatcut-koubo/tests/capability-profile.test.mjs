import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  auditCapabilityProfile,
} from "../src/execution/capability-profile.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts/validate-capability-profile.mjs");
const AS_OF = "2026-07-24T12:00:00Z";

function profile() {
  return JSON.parse(fs.readFileSync(
    path.join(
      ROOT,
      "fixtures/capabilities/valid/unverified-profile.json",
    ),
    "utf8",
  ));
}

function validatedProfile() {
  const document = profile();
  document.status = "validated";
  document.hostBuild = "2026.07.24";
  document.toolSchemaHash = `sha256:${"a".repeat(64)}`;
  document.observedAt = "2026-07-24T08:00:00Z";
  document.expiresAt = "2026-08-24T08:00:00Z";
  document.liveRouteRequested = true;
  document.capabilities.forEach((capability, index) => {
    capability.status = "validated";
    capability.probeRefs = [
      `sha256:${String(index + 1).repeat(64)}`,
    ];
  });
  document.canary.status = "passed";
  document.canary.evidenceRefs = [`sha256:${"f".repeat(64)}`];
  return document;
}

test("missing live evidence routes every capability to a fallback", () => {
  const report = auditCapabilityProfile(profile(), {asOf: AS_OF});
  assert.equal(report.status, "passed");
  assert.equal(report.effectiveStatus, "unverified");
  assert.equal(report.liveAllowed, false);
  assert.deepEqual(
    report.routes.map((route) => route.route),
    ["fake-adapter", "fake-adapter", "manual", "manual", "blocked"],
  );
});

test("requesting live without a current canary fails closed", () => {
  const document = profile();
  document.liveRouteRequested = true;
  const report = auditCapabilityProfile(document, {asOf: AS_OF});
  assert.equal(report.status, "failed");
  assert.ok(report.findings.some(
    (item) => item.code === "CAPABILITY_LIVE_ROUTE_BLOCKED",
  ));
});

test("validated build, schema, probes, and canary enable live routing", () => {
  const report = auditCapabilityProfile(
    validatedProfile(),
    {asOf: AS_OF},
  );
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
  assert.equal(report.effectiveStatus, "validated");
  assert.equal(report.liveAllowed, true);
  assert.ok(report.routes.every((route) => route.route === "live"));
});

test("expired evidence degrades to stale and blocks live", () => {
  const document = validatedProfile();
  document.expiresAt = "2026-07-24T11:59:59Z";
  const report = auditCapabilityProfile(document, {asOf: AS_OF});
  assert.equal(report.liveAllowed, false);
  assert.equal(report.effectiveStatus, "stale");
  assert.ok(report.findings.some(
    (item) =>
      item.code === "CAPABILITY_PROFILE_STALE"
      && item.severity === "warning",
  ));
  assert.ok(report.findings.some(
    (item) => item.code === "CAPABILITY_LIVE_ROUTE_BLOCKED",
  ));
});

test("a failed canary blocks routing even with complete probes", () => {
  const document = validatedProfile();
  document.canary.status = "failed";
  const report = auditCapabilityProfile(document, {asOf: AS_OF});
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("CAPABILITY_CANARY_FAILED"));
  assert.ok(codes.has("CAPABILITY_LIVE_ROUTE_BLOCKED"));
});

test("duplicate and missing mandatory capabilities fail", () => {
  const document = profile();
  document.capabilities[4] = structuredClone(document.capabilities[0]);
  const codes = new Set(
    auditCapabilityProfile(document, {asOf: AS_OF}).findings.map(
      (item) => item.code,
    ),
  );
  assert.ok(codes.has("CAPABILITY_ID_DUPLICATE"));
  assert.ok(codes.has("CAPABILITY_MANDATORY_MISSING"));
});

test("capability CLI reports unverified as a safe successful audit", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--profile",
    "fixtures/capabilities/valid/unverified-profile.json",
    "--as-of",
    AS_OF,
    "--format",
    "json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 0, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.equal(report.effectiveStatus, "unverified");
  assert.equal(report.liveAllowed, false);
});

test("capability CLI rejects ambiguous options without path disclosure", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--profile=fixtures/capabilities/valid/unverified-profile.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 2);
  assert.doesNotMatch(result.stderr, new RegExp(
    ROOT.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});
