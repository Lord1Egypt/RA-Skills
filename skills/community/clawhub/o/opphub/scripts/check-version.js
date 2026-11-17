#!/usr/bin/env node
//
// P2-3 版本单一源 CI 检查
//   单一源 = package.json version
//   同步: SKILL.md / _meta.json / skill-card.md / bin/opphub 头
//   用法: node scripts/check-version.js
//
// 任何不一致 exit 1, CI 阻止 commit / push

import { readFileSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const PKG_PATH = join(ROOT, "package.json");

function readVersion(path) {
  const raw = readFileSync(path, "utf8");
  // package.json / _meta.json: JSON.parse
  if (path.endsWith(".json")) {
    const j = JSON.parse(raw);
    return j.version;
  }
  // SKILL.md: 找 frontmatter 里的 `version: x.y.z`
  if (path.endsWith("SKILL.md")) {
    const m = raw.match(/^---\n([\s\S]*?)\n---/);
    if (!m) return null;
    const v = m[1].match(/^version:\s*(.+)$/m);
    return v ? v[1].trim() : null;
  }
  // skill-card.md: 找 "## Skill Version(s):" 段的 "X.Y.Z" 行
  if (path.endsWith("skill-card.md")) {
    const m = raw.match(/^## Skill Version\(s\): <br>\n([\d.a-z-]+)/m);
    return m ? m[1].trim() : null;
  }
  if (path.endsWith("opphub") || path.endsWith(".sh")) {
    const m = raw.match(/^# bin\/opphub · (.+)$/m);
    return m ? m[1].trim().replace(/^v/, "") : null;
  }
  return null;
}

const checks = [
  { path: "package.json", file: PKG_PATH },
  { path: "_meta.json", file: join(ROOT, "_meta.json") },
  { path: "SKILL.md", file: join(ROOT, "SKILL.md") },
  { path: "skill-card.md", file: join(ROOT, "skill-card.md") },
  { path: "bin/opphub", file: join(ROOT, "bin/opphub") },
];

let canonical = null;
const failures = [];
const seen = [];

for (const c of checks) {
  let v;
  try {
    v = readVersion(c.file);
  } catch (e) {
    failures.push(`${c.path}: 读取失败 - ${e.message}`);
    continue;
  }
  if (!v) {
    failures.push(`${c.path}: 未找到 version 字段`);
    continue;
  }
  seen.push({ path: c.path, version: v });
  if (canonical === null) {
    canonical = v;
  } else if (v !== canonical) {
    failures.push(`${c.path}: version = "${v}", 不匹配 canonical = "${canonical}"`);
  }
}

console.log("📦 版本一致性检查 (canonical = package.json)");
console.log("─".repeat(60));
for (const s of seen) {
  const marker = s.version === canonical ? "✅" : "❌";
  console.log(`${marker}  ${s.path.padEnd(20)} → ${s.version}`);
}
console.log("─".repeat(60));

if (failures.length > 0) {
  console.log("\n❌ 失败:");
  for (const f of failures) console.log(`   ${f}`);
  console.log(`\n修法: 改 package.json version 后, 同步 SKILL.md / _meta.json / skill-card.md / bin/opphub`);
  process.exit(1);
}

console.log(`\n✅ 所有位置版本一致 = ${canonical}`);
process.exit(0);
