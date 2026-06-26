#!/usr/bin/env node
/**
 * backup_skill.js
 * ---------------
 * 在修改 skill 之前，把当前版本备份到系统根目录下的 skill-backups 文件夹，
 * 或写入用户显式提供的备份根目录。
 *
 * 用法:
 *   node backup_skill.js --skill-path <skill目录> [--backup-root <备份根目录>]
 */

"use strict";

const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--skill-path")  { args.skillPath = argv[++i]; continue; }
    if (argv[i] === "--backup-root") { args.backupRoot = argv[++i]; continue; }
  }
  return args;
}

function timestamp() {
  const d = new Date();
  const p = n => String(n).padStart(2, "0");
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}

function defaultBackupRoot(skillPath) {
  const resolved = path.resolve(skillPath);
  const parsed = path.parse(resolved);

  if (process.platform === "win32") {
    return path.join(parsed.root || "C:\\", "skill-backups");
  }

  return path.join(parsed.root || path.sep, "skill-backups");
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    entry.isDirectory() ? copyDir(srcPath, destPath) : fs.copyFileSync(srcPath, destPath);
  }
}

function main() {
  const args = parseArgs(process.argv);

  if (!args.skillPath) {
    print({ status: "error", code: "MISSING_ARG", message: "缺少 --skill-path 参数，请提供要备份的 skill 目录路径。" });
    process.exit(1);
  }

  const skillPath = path.resolve(args.skillPath);
  if (!fs.existsSync(skillPath)) {
    print({ status: "error", code: "NOT_FOUND", message: `要备份的 skill 目录不存在：${skillPath}` });
    process.exit(1);
  }

  if (!fs.statSync(skillPath).isDirectory()) {
    print({ status: "error", code: "INVALID_PATH", message: `--skill-path 指向的不是目录：${skillPath}` });
    process.exit(1);
  }

  const skillName = path.basename(skillPath);
  const backupRoot = path.resolve(args.backupRoot || defaultBackupRoot(skillPath));
  const backupDest = path.join(backupRoot, skillName, timestamp());

  try {
    copyDir(skillPath, backupDest);
  } catch (err) {
    print({
      status: "error",
      code: "BACKUP_FAILED",
      message: `备份失败：${err.message}`,
      backupDest,
      suggestion: "请检查备份根目录是否可写，或改用 --backup-root 指定其他路径。",
      file: __filename
    });
    process.exit(1);
  }

  print({
    status: "success",
    skillName,
    backupRoot,
    backupPath: backupDest,
    message: `备份已创建：${backupDest}`,
  });
}

function print(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
}

main();
