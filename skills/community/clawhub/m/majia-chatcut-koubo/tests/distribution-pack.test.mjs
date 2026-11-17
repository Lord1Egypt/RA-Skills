import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  auditDistributionPack,
} from "../src/distribution/distribution-pack.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts/validate-distribution-pack.mjs");

function pack() {
  return JSON.parse(fs.readFileSync(
    path.join(
      ROOT,
      "fixtures/distribution/valid/distribution-pack.json",
    ),
    "utf8",
  ));
}

test("distribution pack binds every artifact to the verified master", () => {
  const report = auditDistributionPack(pack(), {asOf: "2026-07-24"});
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
  assert.deepEqual(report.summary, {
    deliverables: 4,
    profiles: 2,
    errors: 0,
    warnings: 1,
  });
});

test("expired platform rules degrade to advisory", () => {
  const report = auditDistributionPack(pack(), {asOf: "2026-07-24"});
  const xiaohongshu = report.effectiveProfiles.find(
    (profile) => profile.platformId === "xiaohongshu",
  );
  assert.equal(xiaohongshu.stale, true);
  assert.ok(xiaohongshu.rules.every(
    (rule) => rule.effectiveLevel === "advisory",
  ));
  assert.ok(report.findings.some(
    (item) =>
      item.code === "DISTRIBUTION_PROFILE_STALE"
      && item.severity === "warning",
  ));
});

test("master hash, revision, and content truth drift block a deliverable", () => {
  const document = pack();
  document.deliverables[0].parentArtifactHash =
    `sha256:${"a".repeat(64)}`;
  document.deliverables[0].masterTimelineRevision = "rev_other";
  document.deliverables[0].contentTruthHash =
    `sha256:${"b".repeat(64)}`;
  const codes = new Set(
    auditDistributionPack(document, {asOf: "2026-07-24"})
      .findings.map((item) => item.code),
  );
  assert.ok(codes.has("DISTRIBUTION_MASTER_HASH_MISMATCH"));
  assert.ok(codes.has("DISTRIBUTION_MASTER_REVISION_MISMATCH"));
  assert.ok(codes.has("DISTRIBUTION_CONTENT_TRUTH_MISMATCH"));
});

test("deliverables cannot target an unprofiled platform", () => {
  const document = pack();
  document.deliverables[0].platformId = "bilibili";
  assert.ok(
    auditDistributionPack(document, {asOf: "2026-07-24"})
      .findings.some((item) => item.code === "DISTRIBUTION_PROFILE_MISSING"),
  );
});

test("distribution CLI passes with stale-profile warnings", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--pack",
    "fixtures/distribution/valid/distribution-pack.json",
    "--as-of",
    "2026-07-24",
    "--format",
    "json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 0, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.equal(report.status, "passed");
  assert.equal(report.summary.warnings, 1);
});

test("distribution CLI rejects implicit dates and ambiguous options", () => {
  const result = spawnSync(process.execPath, [
    CLI,
    "--pack=fixtures/distribution/valid/distribution-pack.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(result.status, 2);
  assert.doesNotMatch(result.stderr, new RegExp(
    ROOT.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});
