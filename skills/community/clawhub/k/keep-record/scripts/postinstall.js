#!/usr/bin/env node

/**
 * keep-record 的 postinstall：三件事，任一失败都不能阻塞 npm install。
 *   1. 同步 MCP URL 到 ~/.keepai/.env（syncMcpUrl）——写入 KEEP_MCP_URL
 *   2. 上报安装遥测（reportInstall）——帮助服务端度量分发情况
 *   3. 把整包 cp 到 runner 的 skills 目录：
 *        - OpenClaw：`~/.openclaw/workspace/skills/keep-record/`
 *        - Hermes：  `~/.hermes/skills/keep-record/`
 *      若 npm 把 `@keepclaw/skill-sdk` hoist 到上层而未嵌入包内 node_modules，
 *      会主动用 `require.resolve` 定位后补拷入目标，确保 `require(..)` 自洽。
 *
 * 部署只在 **全局安装**（`npm i -g`，`npm_config_global=true`）时触发。
 * 覆盖策略：always overwrite（先 `rm -rf` 再 cp），不读不判断已有内容。
 * 这个目录归本脚本管理，不建议手改（改请改上游 npm 包）。
 */

const path = require("node:path");

const { reportInstall } = require("@keepclaw/skill-sdk/telemetry");
const { deploySkillToRunners } = require("@keepclaw/skill-sdk/install");
const { syncMcpUrl } = require("@keepclaw/skill-sdk/auth");
const { DEFAULT_MCP_URL } = require("@keepclaw/skill-sdk/mcp");
const pkg = require("../package.json");
const meta = require("../_meta.json");

async function main() {
  runSyncUrl();
  await runTelemetry();
  runDeploy();
}

/**
 * 将 MCP URL 写入 ~/.keepai/.env（KEEP_MCP_URL）。
 *
 * 切换 MCP 环境：
 *   export KEEP_MCP_URL=https://mcp.example.com/... && npm install -g @keepclaw/keep-record
 *
 * 正式用户直接安装，写入默认线上地址：
 *   npm install -g @keepclaw/keep-record
 *
 * 若 URL 与本地已存储值相同则幂等，不做任何修改。
 * 若 URL 发生变化（切换环境）则同时清空旧 token，需要重新 keep login。
 */
function runSyncUrl() {
  try {
    const url = process.env.KEEP_MCP_URL || DEFAULT_MCP_URL;
    const { changed, tokenCleared } = syncMcpUrl({ url });
    if (changed) {
      console.log(`mcp-url: updated → ${url}${tokenCleared ? " (credentials cleared, please re-login)" : ""}`);
    } else {
      console.log(`mcp-url: unchanged (${url})`);
    }
  } catch (err) {
    console.error("mcp-url sync failed:", err && err.message ? err.message : err);
  }
}

async function runTelemetry() {
  try {
    const sourceArg = process.argv.find((a) => a.startsWith("--source="))?.split("=")[1];
    const result = await reportInstall({
      skillName: meta.name,
      version: pkg.version,
      source: sourceArg,
    });
    if (result.ok) {
      console.log("report status:", result.status, "success:", true);
    } else {
      console.error("report request failed");
    }
  } catch (err) {
    console.error("report request failed:", err && err.message ? err.message : err);
  }
}

function runDeploy() {
  try {
    const skillDir = path.resolve(__dirname, "..");
    const { enabled, results } = deploySkillToRunners({
      skillDir,
      skillName: meta.name,
      bundleDeps: ["@keepclaw/skill-sdk"],
    });
    if (!enabled) {
      console.log("skill deploy: skipped (not a global install).");
      return;
    }
    for (const r of results) {
      const suffix = r.reason ? ` (${r.reason})` : "";
      const bundled =
        r.bundled && r.bundled.length
          ? ` [bundled: ${r.bundled.join(", ")}]`
          : "";
      const line = `skill deploy [${r.runner}]: ${r.status} → ${r.target}${suffix}${bundled}`;
      if (r.status === "failed") {
        console.error(line);
      } else {
        console.log(line);
      }
    }
  } catch (err) {
    console.error("skill deploy failed:", err && err.message ? err.message : err);
  }
}

main();
