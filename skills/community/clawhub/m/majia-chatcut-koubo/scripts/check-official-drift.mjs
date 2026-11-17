#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import {fileURLToPath} from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export function auditOfficialSnapshot(snapshot, {checkout = null} = {}) {
  const findings = [];
  const add = (code, file = null) => findings.push({code, file});
  const valid = snapshot?.repository === "https://github.com/ChatCut-Inc/agent-plugin"
    && /^[a-f0-9]{40}$/u.test(snapshot.commit ?? "")
    && Number.isFinite(Date.parse(snapshot.observedAt))
    && /^\d+\.\d+\.\d+$/u.test(snapshot.hostedPluginVersion ?? "")
    && /^\d+\.\d+\.\d+$/u.test(snapshot.desktopConnectorVersion ?? "")
    && Array.isArray(snapshot.hostedSkills) && snapshot.hostedSkills.length > 0
    && new Set(snapshot.hostedSkills).size === snapshot.hostedSkills.length
    && snapshot.hostedSkills.every((name) => /^[a-z][a-z0-9-]{0,79}$/u.test(name))
    && Array.isArray(snapshot.reviewedFiles) && snapshot.reviewedFiles.length > 0
    && new Set(snapshot.reviewedFiles.map((item) => item?.path)).size === snapshot.reviewedFiles.length
    && snapshot.reviewedFiles.every((item) => /^(?:codex|chatcut-desktop-codex-plugin)\/[a-zA-Z0-9._/-]+$/u.test(item.path ?? "") && !item.path.split("/").includes("..") && /^[a-f0-9]{64}$/u.test(item.sha256 ?? ""))
    && snapshot.verificationScope === "official-source-review"
    && snapshot.liveToolsObserved === false && snapshot.mediaVerified === false;
  if (!valid) add("OFFICIAL_SNAPSHOT_INVALID");
  if (valid && checkout) {
    try {
      for (const item of snapshot.reviewedFiles) {
        const bytes = fs.readFileSync(path.join(checkout, item.path));
        if (crypto.createHash("sha256").update(bytes).digest("hex") !== item.sha256) add("OFFICIAL_CONTENT_DRIFT", item.path);
      }
      const skills = fs.readdirSync(path.join(checkout, "codex/skills"))
        .filter((name) => fs.existsSync(path.join(checkout, "codex/skills", name, "SKILL.md"))).sort();
      if (JSON.stringify(skills) !== JSON.stringify([...snapshot.hostedSkills].sort())) add("OFFICIAL_SKILL_INVENTORY_DRIFT");
      for (const [file, version] of [["codex/.codex-plugin/plugin.json", snapshot.hostedPluginVersion], ["chatcut-desktop-codex-plugin/.codex-plugin/plugin.json", snapshot.desktopConnectorVersion]]) {
        if (JSON.parse(fs.readFileSync(path.join(checkout, file), "utf8")).version !== version) add("OFFICIAL_VERSION_DRIFT", file);
      }
    } catch {
      add("OFFICIAL_CHECKOUT_UNAVAILABLE");
    }
  }
  return {ok: findings.length === 0, findings, upstreamChecked: Boolean(checkout), verificationScope: checkout ? "supplied-official-checkout" : "recorded-official-snapshot", mediaVerified: false};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    let checkout = null;
    let json = false;
    for (let index = 2; index < process.argv.length; index += 1) {
      const flag = process.argv[index];
      if (flag === "--json" && !json) json = true;
      else if (flag === "--checkout" && !checkout && process.argv[index + 1] && !process.argv[index + 1].startsWith("--")) checkout = path.resolve(process.argv[++index]);
      else throw new Error("usage");
    }
    const snapshot = JSON.parse(fs.readFileSync(path.join(ROOT, "reports/official-source-current.json"), "utf8"));
    const report = auditOfficialSnapshot(snapshot, {checkout});
    if (json) process.stdout.write(`${JSON.stringify(report)}\n`);
    else process.stdout.write(`official source: ${report.ok ? "PASS" : "DRIFT"}, scope=${report.verificationScope}\n${report.findings.map((item) => item.code).join("\n")}\n`);
    if (!report.ok) process.exitCode = 1;
  } catch {
    process.stderr.write("OFFICIAL_AUDIT_UNAVAILABLE: use --checkout <official-checkout> [--json]\n");
    process.exitCode = 2;
  }
}
