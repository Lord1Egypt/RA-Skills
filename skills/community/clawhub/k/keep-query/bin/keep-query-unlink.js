#!/usr/bin/env node

/**
 * 从 OpenClaw / Hermes 的 skills 目录移除本 skill 的投递（rm -rf 目录）。
 *
 * 典型使用场景（建议在 `npm uninstall` **之前**执行）：
 *   # 全局安装场景：
 *   npx -p @keepclaw/keep-query keep-query-unlink
 *   npm uninstall -g @keepclaw/keep-query
 *
 * npm v7+ 不再触发任何 uninstall 钩子，所以这一步是手动 opt-in。不清理也
 * 只是在 runner skills 目录留一个旧版本的 keep-query/ 目录而已，不会产生
 * 悬空 symlink。
 *
 * 退出码：
 *   0  全部处理（含 "skipped"）
 *   1  有 failed 条目
 */

"use strict";

const { undeploySkillFromRunners } = require("@keepclaw/skill-sdk/install");
const meta = require("../_meta.json");

function main() {
  const results = undeploySkillFromRunners({ skillName: meta.name });

  if (results.length === 0) {
    console.log("skill undeploy: no runner targets configured.");
    return 0;
  }
  for (const r of results) {
    const suffix = r.reason ? ` (${r.reason})` : "";
    const line = `skill undeploy [${r.runner}]: ${r.status} → ${r.target}${suffix}`;
    if (r.status === "failed") {
      console.error(line);
    } else {
      console.log(line);
    }
  }
  return results.some((r) => r.status === "failed") ? 1 : 0;
}

process.exit(main());
