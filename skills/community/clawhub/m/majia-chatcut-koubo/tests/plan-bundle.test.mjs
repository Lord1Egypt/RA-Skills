import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  validatePlanBundle,
} from "../src/planning/plan-bundle-validator.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts", "validate-plan-bundle.mjs");

function createFixtureRoot(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-plan-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  fs.cpSync(path.join(ROOT, "schemas"), path.join(directory, "schemas"), {
    recursive: true,
  });
  fs.mkdirSync(path.join(directory, "rules"), {recursive: true});
  for (const file of ["policy.json", "registry.json"]) {
    fs.copyFileSync(
      path.join(ROOT, "rules", file),
      path.join(directory, "rules", file),
    );
  }
  fs.cpSync(
    path.join(ROOT, "fixtures/plan-bundles/valid"),
    path.join(directory, "bundle"),
    {recursive: true},
  );
  return directory;
}

function mutateJson(directory, relativePath, mutate) {
  const absolutePath = path.join(directory, relativePath);
  const document = JSON.parse(fs.readFileSync(absolutePath, "utf8"));
  mutate(document);
  fs.writeFileSync(absolutePath, `${JSON.stringify(document, null, 2)}\n`);
}

function validate(directory) {
  return validatePlanBundle({
    root: directory,
    bundlePath: "bundle/bundle.json",
  });
}

test("anonymous Creator OS IR fixture passes the plan bundle validator", (t) => {
  const directory = createFixtureRoot(t);
  const report = validate(directory);
  assert.equal(report.status, "passed", JSON.stringify(report.findings));
  assert.deepEqual(report.summary, {documents: 7, errors: 0});
});

test("composition state coverage rejects gaps and overlaps", async (t) => {
  await t.test("gap", (t2) => {
    const directory = createFixtureRoot(t2);
    mutateJson(directory, "bundle/state-plan.json", (document) => {
      document.compositionStates[0].range.end = 80;
    });
    const report = validate(directory);
    assert.ok(report.findings.some(
      (item) => item.code === "PLAN_COVERAGE_GAP",
    ));
  });
  await t.test("overlap", (t2) => {
    const directory = createFixtureRoot(t2);
    mutateJson(directory, "bundle/state-plan.json", (document) => {
      document.compositionStates[1].range.start = 80;
    });
    const report = validate(directory);
    assert.ok(report.findings.some(
      (item) => item.code === "PLAN_COVERAGE_OVERLAP",
    ));
  });
});

test("visual and privacy owners must match their exact orthogonal lanes", (t) => {
  const directory = createFixtureRoot(t);
  mutateJson(directory, "bundle/owner-ledger.json", (document) => {
    document.owners[0].range.end = 89;
    document.owners = document.owners.filter(
      (owner) => owner.domain !== "privacy",
    );
  });
  const report = validate(directory);
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("PLAN_VISUAL_OWNER_MISMATCH"));
  assert.ok(codes.has("PLAN_PRIVACY_OWNER_MISMATCH"));
});

test("source-bound edits and privacy overlays cannot drift from assets", (t) => {
  const directory = createFixtureRoot(t);
  mutateJson(directory, "bundle/edit-plan.json", (document) => {
    document.segments[0].sourceAssetId = "asset_other";
  });
  mutateJson(directory, "bundle/state-plan.json", (document) => {
    document.privacyOverlays[0].sourceAssetId = "asset_other";
  });
  const report = validate(directory);
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("PLAN_EDIT_SOURCE_MISMATCH"));
  assert.ok(codes.has("PLAN_PRIVACY_SOURCE_UNKNOWN"));
});

test("visual and privacy owner subjects are one-to-one", (t) => {
  const directory = createFixtureRoot(t);
  mutateJson(directory, "bundle/owner-ledger.json", (document) => {
    const visualClone = structuredClone(document.owners[0]);
    visualClone.ownerId = "owner_visual_duplicate";
    const privacyClone = structuredClone(
      document.owners.find((owner) => owner.domain === "privacy"),
    );
    privacyClone.ownerId = "owner_privacy_orphan";
    privacyClone.subjectRef = "privacy_missing";
    document.owners.push(visualClone, privacyClone);
  });
  const report = validate(directory);
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("PLAN_VISUAL_OWNER_MISMATCH"));
  assert.ok(codes.has("PLAN_PRIVACY_OWNER_ORPHAN"));
});

test("validated high-risk edit decisions require named approval", (t) => {
  const directory = createFixtureRoot(t);
  mutateJson(directory, "bundle/edit-plan.json", (document) => {
    document.segments[0].action = "reorder";
    document.segments[0].risk = "high";
    document.segments[0].approval = {
      required: false,
      status: "not-required",
    };
  });
  const report = validate(directory);
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("PLAN_EDIT_APPROVAL_REQUIRED"));
  assert.ok(codes.has("PLAN_EDIT_APPROVAL_PENDING"));
});

test("project, timeline, transcript, and evidence revisions cannot drift", (t) => {
  const directory = createFixtureRoot(t);
  mutateJson(directory, "bundle/transcript.json", (document) => {
    document.projectId = "proj_other";
    document.sourceRevision =
      "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc";
    document.words[0].evidenceRefs = ["evidence_missing"];
  });
  mutateJson(directory, "bundle/caption-plan.json", (document) => {
    document.timelineRevision = "rev_other";
  });
  const report = validate(directory);
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("PLAN_PROJECT_ID_MISMATCH"));
  assert.ok(codes.has("PLAN_TRANSCRIPT_SOURCE_REVISION"));
  assert.ok(codes.has("PLAN_EVIDENCE_UNKNOWN"));
  assert.ok(codes.has("PLAN_TIMELINE_REVISION_MISMATCH"));
});

test("caption pages cannot invent corrections or unknown words", (t) => {
  const directory = createFixtureRoot(t);
  mutateJson(directory, "bundle/caption-plan.json", (document) => {
    document.pages[0].displayText = "新增";
    document.pages[0].sourceWordIds = ["word_missing"];
    document.pages[1].range.start = 40;
  });
  const report = validate(directory);
  const codes = new Set(report.findings.map((item) => item.code));
  assert.ok(codes.has("PLAN_CAPTION_CORRECTION_UNMODELED"));
  assert.ok(codes.has("PLAN_CAPTION_WORD_UNKNOWN"));
  assert.ok(codes.has("PLAN_CAPTION_OVERLAP"));
});

test("bundle document paths fail closed on traversal and symlinks", async (t) => {
  await t.test("traversal", (t2) => {
    const directory = createFixtureRoot(t2);
    mutateJson(directory, "bundle/bundle.json", (document) => {
      document.documents.project = "../rules/policy.json";
    });
    const report = validate(directory);
    assert.ok(report.findings.some(
      (item) =>
        item.code === "PLAN_SCHEMA_PATTERN"
        || item.code === "PLAN_UNSAFE_PATH",
    ));
  });
  await t.test("symlink", (t2) => {
    const directory = createFixtureRoot(t2);
    fs.renameSync(
      path.join(directory, "bundle/project.json"),
      path.join(directory, "bundle/project.real.json"),
    );
    fs.symlinkSync(
      "project.real.json",
      path.join(directory, "bundle/project.json"),
    );
    const report = validate(directory);
    assert.ok(report.findings.some(
      (item) => item.code === "PLAN_SYMLINK_NOT_ALLOWED",
    ));
  });
});

test("plan bundle CLI returns stable machine output", (t) => {
  const directory = createFixtureRoot(t);
  const result = spawnSync(
    process.execPath,
    [
      CLI,
      "--root",
      directory,
      "--bundle",
      "bundle/bundle.json",
      "--format",
      "json",
    ],
    {cwd: ROOT, encoding: "utf8"},
  );
  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(JSON.parse(result.stdout).status, "passed");
});

test("plan bundle CLI rejects ambiguous options and hides root paths", (t) => {
  const unknown = spawnSync(
    process.execPath,
    [CLI, "--bundle", "bundle.json", "--unknown", "x"],
    {cwd: ROOT, encoding: "utf8"},
  );
  assert.equal(unknown.status, 2);
  assert.match(unknown.stderr, /unknown or unsupported option/u);

  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-plan-private-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  const missing = spawnSync(
    process.execPath,
    [CLI, "--root", directory, "--bundle", "missing.json"],
    {cwd: ROOT, encoding: "utf8"},
  );
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /PLAN_BUNDLE_UNREADABLE/u);
  assert.doesNotMatch(
    missing.stderr,
    new RegExp(directory.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
  );
});
