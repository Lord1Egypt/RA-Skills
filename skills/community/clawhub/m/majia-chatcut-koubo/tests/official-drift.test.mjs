import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import test from "node:test";
import {auditOfficialSnapshot, ROOT} from "../scripts/check-official-drift.mjs";

test("来源快照检查不会伪造上游连接或真实媒体验证", () => {
  const snapshot = JSON.parse(fs.readFileSync(path.join(ROOT, "reports/official-source-current.json")));
  const result = auditOfficialSnapshot(snapshot);
  assert.equal(result.ok, true);
  assert.equal(result.upstreamChecked, false);
  assert.equal(result.mediaVerified, false);
  assert.equal(auditOfficialSnapshot({...snapshot, mediaVerified: true}).ok, false);
  assert.equal(auditOfficialSnapshot({...snapshot, reviewedFiles: [{path: "codex/../private", sha256: "a".repeat(64)}]}).ok, false);
});

test("参数文档变化、插件版本变化和新增 Skill 都需重新审查", (t) => {
  const checkout = fs.mkdtempSync(path.join(os.tmpdir(), "koubo-official-drift-"));
  t.after(() => fs.rmSync(checkout, {recursive: true, force: true}));
  const files = {"codex/.codex-plugin/plugin.json": '{"version":"1.0.0"}', "chatcut-desktop-codex-plugin/.codex-plugin/plugin.json": '{"version":"1.0.0"}', "codex/skills/example/SKILL.md": "# Synthetic skill\n"};
  for (const [file, body] of Object.entries(files)) {
    fs.mkdirSync(path.dirname(path.join(checkout, file)), {recursive: true});
    fs.writeFileSync(path.join(checkout, file), body);
  }
  const baseline = JSON.parse(fs.readFileSync(path.join(ROOT, "reports/official-source-current.json")));
  const snapshot = {...baseline, hostedPluginVersion: "1.0.0", desktopConnectorVersion: "1.0.0", hostedSkills: ["example"], reviewedFiles: Object.entries(files).map(([file, body]) => ({path: file, sha256: crypto.createHash("sha256").update(body).digest("hex")}))};
  assert.equal(auditOfficialSnapshot(snapshot, {checkout}).ok, true);
  fs.writeFileSync(path.join(checkout, "codex/skills/example/SKILL.md"), "# Changed synthetic instruction\n");
  fs.writeFileSync(path.join(checkout, "codex/.codex-plugin/plugin.json"), '{"version":"2.0.0"}');
  fs.mkdirSync(path.join(checkout, "codex/skills/new-skill"));
  fs.writeFileSync(path.join(checkout, "codex/skills/new-skill/SKILL.md"), "# New synthetic skill\n");
  const result = auditOfficialSnapshot(snapshot, {checkout});
  const codes = result.findings.map((item) => item.code);
  for (const code of ["OFFICIAL_CONTENT_DRIFT", "OFFICIAL_VERSION_DRIFT", "OFFICIAL_SKILL_INVENTORY_DRIFT"]) assert.ok(codes.includes(code), code);
  assert.equal(result.ok, false);
});
