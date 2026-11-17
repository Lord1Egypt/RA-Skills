#!/usr/bin/env node
// bin/opphub-plugin-check.js · v4.0
// status: implemented (plugin 探测, v3.1)
//
//
// 用法: bot 调 `opphub plugin-check --json`
// 返 { ok, installed, version, path, hint, install_cmd }
// skill 拿到这个 JSON 后:
//   - installed=false → 走 bot.skillApi.askInteractive 强引导装 plugin
//   - installed=true  → 走 bot.skillApi.send 验链路 (不念装命令)

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const CANDIDATE_PATHS = [
  join(homedir(), ".openclaw/extensions/opphub/package.json"),
  // 老版本 / 简化安装
  join(homedir(), "openclaw/plugins/opphub/package.json"),
  // K8s / Docker WORKDIR
  "/app/extensions/opphub/package.json",
  "/workspace/extensions/opphub/package.json",
];

const INSTALL_CMD = "openclaw plugins install clawhub:@mtty-ai/opphub";

function findPackageJson() {
  for (const p of CANDIDATE_PATHS) {
    if (existsSync(p)) return p;
  }
  return null;
}

function main() {
  const args = process.argv.slice(2);
  const wantJson = args.includes("--json");

  const path = findPackageJson();
  if (!path) {
    const result = {
      ok: true,
      installed: false,
      version: null,
      path: null,
      hint: "⚠️ 还没装 opphub-plugin, 推送过来没人接 = 收不到撮合",
      install_cmd: INSTALL_CMD,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else {
      console.error("⚠️  opphub-plugin 未装");
      console.error(`装: ${INSTALL_CMD}`);
    }
    process.exit(0);
  }

  let version = null;
  try {
    const pkg = JSON.parse(readFileSync(path, "utf8"));
    version = pkg.version ?? null;
  } catch (e) {
    const result = {
      ok: false,
      installed: null,
      error: "package_json_parse_failed",
      path,
      message: e?.message ?? String(e),
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else console.error(`✗ ${path} 解析失败: ${e.message}`);
    process.exit(1);
  }

  const result = {
    ok: true,
    installed: true,
    version,
    path,
    hint: "✅ opphub-plugin 已装, 推送链路通",
  };
  if (wantJson) console.log(JSON.stringify(result, null, 2));
  else {
    console.log(`✅ opphub-plugin v${version}`);
    console.log(`   ${path}`);
  }
}

main();