#!/usr/bin/env node
//
// Setup script for ClawAgent MCP Skill — Node.js edition
//
// 功能：
//   1. 安装 mcporter（已安装则跳过）
//   2. 检查/保存/验证 Token
//
// 用法（供 AI Agent 调用）：
//   node setup.mjs                    → 交互式安装向导
//   node setup.mjs check_auth         → 检查授权状态
//   node setup.mjs save_token <token> → 保存 Token
//   node setup.mjs verify_token       → 验证 Token
//
// 输出约定（AI Agent 依赖这些字符串判断状态）：
//   READY / NOT_CONFIGURED / TOKEN_SAVED / TOKEN_VALID
//   ERROR:xxx - 错误信息
//

import { execSync } from "node:child_process";

// ── 常量 ──────────────────────────────────────────────────────────────
const MCP_URL = "https://mcp.jiadouai.com/mcp";
const SERVICE_NAME = "JIADOUAI";
const MCPORTER_VERSION = "^0.12.0";

// ── Shell 工具 ────────────────────────────────────────────────────────
function sh(cmd) {
  try {
    return execSync(cmd, {
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
    }).trim();
  } catch {
    return null;
  }
}

function which(bin) {
  const cmd = process.platform === "win32" ? `where ${bin}` : `which ${bin}`;
  return sh(cmd) !== null;
}

// ── mcporter 检测 & 安装 ──────────────────────────────────────────────
function checkMcporter() {
  if (which("mcporter")) {
    console.log("✅ mcporter 已安装");
    return true;
  }

  console.log("⚠️  未找到 mcporter，正在安装...");
  if (!which("npm")) {
    console.log("❌ ERROR: no_npm - 请先安装 Node.js 和 npm 后重试");
    return false;
  }

  try {
    execSync(`npm install -g mcporter@${MCPORTER_VERSION}`, {
      encoding: "utf-8",
      stdio: "pipe",
    });
  } catch (e) {
    // 打印 npm 最后几行错误方便排查
    const stderr = e.stderr?.trim() || "";
    const tail = stderr.split("\n").slice(-3).join("\n");
    if (tail) console.log(tail);
    console.log(
      "❌ ERROR: install_failed - mcporter 安装失败，请检查网络或 npm 配置",
    );
    return false;
  }

  console.log("✅ mcporter 安装完成");
  return true;
}

// ── Token 操作 ────────────────────────────────────────────────────────
function getToken() {
  const out = sh(`mcporter config get ${SERVICE_NAME}`);
  if (!out) return null;
  const m = out.match(/^\s*Authorization:\s*(\S+)/im);
  return m ? m[1] : null;
}

function validateToken(token) {
  if (!token) return false;
  // 只允许安全字符，拒绝命令注入
  return !/[`$();|&<>\\ \n\r\t]/.test(token);
}

function saveToken(token) {
  if (!validateToken(token)) return false;

  const ok = sh(
    `mcporter config add ${SERVICE_NAME} ${MCP_URL} --header Authorization=${token} --transport http --scope home`,
  );
  return ok !== null;
}

// ── 服务状态 ──────────────────────────────────────────────────────────
function checkService() {
  const list = sh("mcporter list");
  if (!list || !list.includes(SERVICE_NAME)) return "not_registered";

  const token = getToken();
  if (!token) return "no_token";
  if (!token.trim()) return "empty_token";
  return "ready";
}

// ── 子命令 ────────────────────────────────────────────────────────────
function cmdCheckAuth() {
  if (!checkMcporter()) {
    console.log("ERROR:mcporter_not_found");
    process.exit(1);
  }

  if (checkService() === "ready") {
    console.log("READY");
  } else {
    console.log("NOT_CONFIGURED");
  }
}

function cmdSaveToken(token) {
  if (!token) {
    console.log("ERROR:no_token - 请提供 Token");
    process.exit(1);
  }
  if (!checkMcporter()) {
    console.log("ERROR:mcporter_not_found");
    process.exit(1);
  }

  console.log("🔧 正在保存 Token...");
  if (saveToken(token)) {
    console.log("TOKEN_SAVED");
  } else {
    console.log("ERROR:save_failed");
  }
}

function cmdVerifyToken() {
  if (!checkMcporter()) {
    console.log("ERROR:mcporter_not_found");
    process.exit(1);
  }

  const out = sh(`mcporter list ${SERVICE_NAME}`);
  if (out) {
    console.log("TOKEN_VALID");
  } else {
    console.log("ERROR:token_invalid");
  }
}

function cmdInteractive() {
  console.log("");
  console.log("╔══════════════════════════════════════════════╗");
  console.log("║     ClawAgent 配置向导                       ║");
  console.log("╚══════════════════════════════════════════════╝");
  console.log("");

  console.log("🔍 检查 mcporter...");
  if (!checkMcporter()) {
    console.log(
      "❌ mcporter 安装失败，请先安装 Node.js (https://nodejs.org) 后重试",
    );
    process.exit(1);
  }
  console.log("✅ mcporter 已就绪");
  console.log("");

  console.log("🔍 检查 ClawAgent 服务配置...");
  const status = checkService();

  if (status === "ready") {
    console.log("✅ ClawAgent 服务已配置且运行正常！");
    console.log("");
    console.log("🎉 无需重新配置，您可以直接使用 ClawAgent 功能。");
    console.log("");
    console.log("📖 使用示例：");
    console.log("   mcporter list ClawAgent");
    return;
  }
  if (
    status === "not_registered" ||
    status === "no_token" ||
    status === "empty_token"
  ) {
    console.log("⚠️  Token 未配置，需要授权...");
  }

  console.log("");
  console.log("─────────────────────────────────────────────");
  console.log("🎉 基础设置完成！");
  console.log("");
  console.log("📖 下一步：配置 ClawAgent Token");
  console.log("   详见 SKILL.md 中快速配置说明");
  console.log("");
  console.log("   更多信息请查看 SKILL.md");
  console.log("");
}

// ── 主入口 ────────────────────────────────────────────────────────────
const cmd = process.argv[2];

if (!cmd) {
  cmdInteractive();
} else if (cmd === "check_auth") {
  cmdCheckAuth();
} else if (cmd === "save_token") {
  const token = process.argv.slice(3).join(" ");
  cmdSaveToken(token);
} else if (cmd === "verify_token") {
  cmdVerifyToken();
} else {
  cmdInteractive();
}
