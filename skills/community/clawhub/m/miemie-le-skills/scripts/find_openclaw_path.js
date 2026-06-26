#!/usr/bin/env node
/**
 * find_openclaw_path.js
 * ---------------------
 * 在本地文件系统中自动定位 OpenClaw 的 .openclaw/skills 目录。
 *
 * 输出（stdout）：
 *   成功: { "status": "success", "skillsPath": "/absolute/path/to/skills" }
 *   失败: { "status": "error",   "code": "NOT_FOUND", "message": "...", "searched": [...] }
 *
 * 退出码:
 *   0 — 找到路径（或成功创建了 skills 子目录）
 *   1 — 未找到 .openclaw 根目录，需要用户手动提供
 */

"use strict";

const fs   = require("fs");
const path = require("path");
const os   = require("os");

const HOME = os.homedir();

// 按优先级排列的候选 .openclaw 根目录
const OPENCLAW_ROOTS = [
  path.join(HOME, ".openclaw"),
  path.join(HOME, ".config", "openclaw"),
  path.join(HOME, "Library", "Application Support", "openclaw"),
  ...(process.env.APPDATA ? [path.join(process.env.APPDATA, "openclaw")] : []),
  path.join(process.cwd(), ".openclaw"),
];

function isDir(p) {
  try { return fs.statSync(p).isDirectory(); } catch { return false; }
}

function ensureDir(p) {
  if (!isDir(p)) fs.mkdirSync(p, { recursive: true });
}

function main() {
  const searched = [];

  for (const root of OPENCLAW_ROOTS) {
    searched.push(root);
    if (!isDir(root)) continue;

    // 找到了 .openclaw 根目录
    const skillsPath = path.join(root, "skills");

    // 如果 skills/ 子目录不存在，自动创建它
    try {
      ensureDir(skillsPath);
    } catch (err) {
      print({ status: "error", code: "MKDIR_FAILED", message: `无法创建 skills 目录：${err.message}`, path: skillsPath, file: __filename });
      process.exit(1);
    }

    print({ status: "success", skillsPath });
    process.exit(0);
  }

  // 所有候选路径都不存在
  print({
    status: "error",
    code: "NOT_FOUND",
    message: "在常见位置均未找到 .openclaw 目录，请手动提供 skill 存放路径。",
    searched,
    file: __filename
  });
  process.exit(1);
}

function print(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
}

main();