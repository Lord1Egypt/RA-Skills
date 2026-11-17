import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {
  SrtBridgeError,
  diffSrtBridge,
  exportSrtBridge,
  parseSrt,
  validateSrtSidecar,
} from "../src/planning/srt-bridge.mjs";

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const CLI = path.join(ROOT, "scripts/srt-bridge.mjs");

function captionPlan() {
  return JSON.parse(fs.readFileSync(
    path.join(ROOT, "fixtures/plan-bundles/valid/caption-plan.json"),
    "utf8",
  ));
}

function replaceTimestamp(srt, before, after) {
  return srt.replace(before, after);
}

test("SRT export retains stable cue identity and exact rational ranges", () => {
  const exported = exportSrtBridge(captionPlan());
  assert.equal(parseSrt(exported.srt).length, 2);
  assert.deepEqual(
    exported.sidecar.cues.map((cue) => cue.range),
    captionPlan().pages.map((page) => page.range),
  );
  assert.equal(diffSrtBridge({
    srt: exported.srt,
    sidecar: exported.sidecar,
  }).status, "unchanged");
  const exactRanges = structuredClone(
    exported.sidecar.cues.map((cue) => cue.range),
  );
  for (let cycle = 0; cycle < 20; cycle += 1) {
    assert.equal(diffSrtBridge({
      srt: exported.srt,
      sidecar: exported.sidecar,
    }).status, "unchanged");
  }
  assert.deepEqual(
    exported.sidecar.cues.map((cue) => cue.range),
    exactRanges,
  );
});

test("SRT cue renumbering does not change sidecar identity", () => {
  const exported = exportSrtBridge(captionPlan());
  const renumbered = exported.srt
    .replace(/^1$/mu, "101")
    .replace(/^2$/mu, "202");
  const report = diffSrtBridge({
    srt: renumbered,
    sidecar: exported.sidecar,
  });
  assert.equal(report.status, "unchanged");
  assert.equal(report.summary.matchedCues, 2);
});

test("SRT edits become candidate decisions without mutating the plan", () => {
  const plan = captionPlan();
  const before = structuredClone(plan);
  const exported = exportSrtBridge(plan);
  const edited = replaceTimestamp(
    exported.srt.replace("\n先\n", "\n首先\n"),
    "00:00:00,000 --> 00:00:01,500",
    "00:00:00,100 --> 00:00:01,400",
  );
  const report = diffSrtBridge({srt: edited, sidecar: exported.sidecar});
  assert.deepEqual(
    new Set(report.decisions.map((item) => item.type)),
    new Set(["correction", "retime"]),
  );
  assert.deepEqual(plan, before);
  assert.ok(report.decisions.every((item) => item.status === "candidate"));
});

test("deletion and reorder are high-risk approval candidates", () => {
  const exported = exportSrtBridge(captionPlan());
  const blocks = exported.srt.trim().split("\n\n");
  const deleted = diffSrtBridge({
    srt: `${blocks[0]}\n`,
    sidecar: exported.sidecar,
  });
  assert.equal(deleted.decisions[0].type, "delete");
  assert.equal(deleted.decisions[0].requiresApproval, true);

  const reordered = diffSrtBridge({
    srt: `${blocks.reverse().join("\n\n")}\n`,
    sidecar: exported.sidecar,
  });
  const decision = reordered.decisions.find(
    (item) => item.type === "reorder",
  );
  assert.equal(decision.requiresApproval, true);
});

test("split and merge are classified as high-risk candidates", () => {
  const exported = exportSrtBridge(captionPlan());
  const splitSrt = [
    "1",
    "00:00:00,000 --> 00:00:00,700",
    "先",
    "",
    "2",
    "00:00:00,700 --> 00:00:01,500",
    "再",
    "",
    "3",
    "00:00:01,500 --> 00:00:03,000",
    "验证",
    "",
  ].join("\n");
  const split = diffSrtBridge({
    srt: splitSrt,
    sidecar: exported.sidecar,
  }).decisions.find((item) => item.type === "split");
  assert.ok(split.subjectRefs.includes("cue_001"));

  const mergeSrt = [
    "1",
    "00:00:00,000 --> 00:00:03,000",
    "先验证",
    "",
  ].join("\n");
  assert.ok(diffSrtBridge({
    srt: mergeSrt,
    sidecar: exported.sidecar,
  }).decisions.some((item) => item.type === "merge"));
});

test("ambiguous repeated text fails closed", () => {
  const plan = captionPlan();
  plan.pages[1].displayText = plan.pages[0].displayText;
  plan.pages[1].sourceText = plan.pages[0].sourceText;
  const exported = exportSrtBridge(plan);
  const moved = [
    "1",
    "00:00:04,000 --> 00:00:05,000",
    "先",
    "",
  ].join("\n");
  assert.throws(
    () => diffSrtBridge({srt: moved, sidecar: exported.sidecar}),
    (error) =>
      error instanceof SrtBridgeError
      && error.code === "SRT_MATCH_AMBIGUOUS",
  );
});

test("sidecar quantization drift fails closed before matching", () => {
  const exported = exportSrtBridge(captionPlan());
  exported.sidecar.cues[0].quantization.startResidual = 1;
  assert.throws(
    () => validateSrtSidecar(exported.sidecar),
    (error) =>
      error instanceof SrtBridgeError
      && error.code === "SRT_SIDECAR_QUANTIZATION_DRIFT",
  );
});

test("SRT CLI exports and diffs inside an explicit root", (t) => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-srt-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  fs.mkdirSync(path.join(directory, "schemas"));
  fs.mkdirSync(path.join(directory, "work"));
  for (const name of [
    "creator-os-common.schema.json",
    "caption-plan.schema.json",
    "srt-sidecar.schema.json",
  ]) {
    fs.copyFileSync(
      path.join(ROOT, "schemas", name),
      path.join(directory, "schemas", name),
    );
  }
  fs.copyFileSync(
    path.join(ROOT, "fixtures/plan-bundles/valid/caption-plan.json"),
    path.join(directory, "work/caption-plan.json"),
  );
  const exported = spawnSync(process.execPath, [
    CLI,
    "export",
    "--root",
    directory,
    "--caption-plan",
    "work/caption-plan.json",
    "--srt-out",
    "work/captions.srt",
    "--sidecar-out",
    "work/captions.sidecar.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(exported.status, 0, exported.stderr);

  const diffed = spawnSync(process.execPath, [
    CLI,
    "diff",
    "--root",
    directory,
    "--srt",
    "work/captions.srt",
    "--sidecar",
    "work/captions.sidecar.json",
    "--format",
    "json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(diffed.status, 0, diffed.stderr);
  assert.equal(JSON.parse(diffed.stdout).status, "unchanged");
});

test("SRT CLI rejects traversal, symlinks, and ambiguous options", (t) => {
  const directory = fs.mkdtempSync(
    path.join(os.tmpdir(), "koubo-srt-private-"),
  );
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  const usage = spawnSync(process.execPath, [
    CLI,
    "diff",
    "--root",
    directory,
    "--srt=outside.srt",
    "--sidecar",
    "../outside.json",
  ], {cwd: ROOT, encoding: "utf8"});
  assert.equal(usage.status, 2);
  assert.doesNotMatch(usage.stderr, new RegExp(
    directory.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
  ));
});
