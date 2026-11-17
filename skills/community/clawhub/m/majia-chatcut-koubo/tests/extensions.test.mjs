import assert from "node:assert/strict";
import {execFileSync, spawnSync} from "node:child_process";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("extension registry and bundled snapshots pass governance validation", () => {
  const output = execFileSync(process.execPath, ["scripts/validate-extensions.mjs"], {
    cwd: root,
    encoding: "utf8",
  });
  assert.match(output, /extension validation passed/u);
  assert.match(output, /cuttips=198 sources\/48 cards\/14 rules/u);
  assert.match(output, /shotcraft=8 adapters/u);
});

test("cuttips query returns machine-readable knowledge candidates", () => {
  const output = execFileSync(process.execPath, [
    "extensions/cuttips-kb/scripts/query.mjs",
    "--text", "字幕",
    "--type", "knowledge",
    "--limit", "2",
    "--json",
  ], {cwd: root, encoding: "utf8"});
  const result = JSON.parse(output);
  assert.ok(result.counts.knowledge >= 1);
  assert.ok(result.result.knowledge.length >= 1);
  assert.ok(result.result.knowledge.every((item) => item.id.startsWith("KB-")));
});

test("shotcraft inspector fails closed without a provider checkout", () => {
  const result = spawnSync(process.execPath, [
    "extensions/video-shotcraft/scripts/inspect-provider.mjs",
    "--checkout", path.join(root, "fixtures", "not-a-shotcraft-checkout"),
  ], {cwd: root, encoding: "utf8"});
  assert.equal(result.status, 2);
  assert.match(result.stderr, /existing directory/u);
});
