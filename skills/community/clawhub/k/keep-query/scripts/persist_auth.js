#!/usr/bin/env node

/**
 * 最小本地持久化脚本：把扫码登录得到的 token 写入 ~/.keepai/.env，
 * 或按 --clear 清除已有凭证。
 *
 * 推荐主路径：
 * 1. 运行器原生调用 get_qrcode / check_login（或 revoke_auth）
 * 2. 登录成功后 exec 本脚本持久化 token；退出登录时 exec 本脚本 --clear
 *
 * 用法：
 *   node scripts/persist_auth.js --token=<jwt> [--username=<name>]
 *   node scripts/persist_auth.js --clear
 */

const {
  decodeJwtExp,
  persistCredentials,
  clearCredentials,
} = require("@keepclaw/skill-sdk/auth");

function emit(type, data) {
  console.log(JSON.stringify({ type, ...data }));
}

function readArg(name) {
  const inline = process.argv.find((a) => a.startsWith(`--${name}=`));
  if (inline) return inline.slice(name.length + 3);

  const idx = process.argv.findIndex((a) => a === `--${name}`);
  if (idx >= 0) return process.argv[idx + 1] || "";
  return "";
}

function hasFlag(name) {
  return process.argv.includes(`--${name}`);
}

function main() {
  if (hasFlag("clear")) {
    const { cleared } = clearCredentials();
    emit("auth_cleared", { cleared });
    return;
  }

  const token = String(readArg("token") || "").trim();
  const username = String(readArg("username") || "").trim();

  if (!token) {
    emit("error", { message: "缺少 --token 参数（或使用 --clear 清除凭证）" });
    process.exitCode = 1;
    return;
  }

  const exp = decodeJwtExp(token);
  const { username: persistedUsername } = persistCredentials({ token, exp, username });
  emit("auth_persisted", { exp, username: persistedUsername || username });
}

main();
