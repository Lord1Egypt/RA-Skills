#!/usr/bin/env node
/**
 * write_skill.js
 * --------------
 * 将草稿 skill 文件夹复制到目标 OpenClaw skills 目录。
 *
 * 用法:
 *   node write_skill.js --source <草稿目录> --dest <目标目录> [--if-exists error|replace] [--dry-run]
 *
 * 参数:
 *   --source      草稿 skill 文件夹路径（必须包含 SKILL.md）
 *   --dest        目标路径
 *   --if-exists   目标已存在时的策略：error | replace（默认 error）
 *   --dry-run     只打印计划，不实际写文件
 */

"use strict";

const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const args = { ifExists: "error" };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--source")    { args.source = argv[++i]; continue; }
    if (argv[i] === "--dest")      { args.dest = argv[++i]; continue; }
    if (argv[i] === "--if-exists") { args.ifExists = argv[++i]; continue; }
    if (argv[i] === "--dry-run")   { args.dryRun = true; continue; }
  }
  return args;
}

function validate(args) {
  if (!args.source) {
    return { code: "MISSING_ARG", message: "缺少 --source 参数，请提供草稿文件夹路径。" };
  }
  if (!args.dest) {
    return { code: "MISSING_ARG", message: "缺少 --dest 参数，请提供目标安装路径。" };
  }
  if (!["error", "replace"].includes(args.ifExists)) {
    return { code: "INVALID_ARGS", message: `--if-exists 只支持 error 或 replace，当前值为：${args.ifExists}` };
  }

  // 安全边界校验
  const destPath = path.resolve(args.dest);
  if (!destPath.replace(/\\/g, '/').includes('/.openclaw/')) {
    return { code: "PATH_TRAVERSAL_BLOCKED", message: `拒绝访问：目标路径不在 .openclaw 边界内 (${destPath})` };
  }

  if (!fs.existsSync(args.source)) {
    return {
      code: "SOURCE_MISSING",
      message: `草稿目录不存在：${args.source}`,
      suggestion: "请确认草稿是否已经写入。若刚发生跨 session 跳转，请回到 Phase 4 重新创建草稿文件。",
    };
  }

  if (!fs.statSync(args.source).isDirectory()) {
    return { code: "INVALID_SOURCE", message: `--source 指向的不是目录：${args.source}` };
  }

  return null;
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function listFiles(baseDir, currentDir = baseDir, acc = []) {
  for (const entry of fs.readdirSync(currentDir, { withFileTypes: true })) {
    const fullPath = path.join(currentDir, entry.name);
    if (entry.isDirectory()) {
      listFiles(baseDir, fullPath, acc);
    } else {
      acc.push(path.relative(baseDir, fullPath));
    }
  }
  return acc.sort();
}

function removeDirIfExists(target) {
  if (fs.existsSync(target)) {
    fs.rmSync(target, { recursive: true, force: true });
  }
}

function main() {
  const args = parseArgs(process.argv);
  const validation = validate(args);

  if (validation) {
    print({ status: "error", ...validation });
    process.exit(1);
  }

  const source = path.resolve(args.source);
  const dest = path.resolve(args.dest);
  const destParent = path.dirname(dest);
  const destExists = fs.existsSync(dest);

  if (destExists && args.ifExists === "error") {
    print({
      status: "error",
      code: "TARGET_EXISTS",
      message: `目标目录已存在：${dest}`,
      suggestion: "如需覆盖，请重新执行并传入 --if-exists replace，或先备份后再覆盖。",
      dest,
    });
    process.exit(1);
  }

  const relativeFiles = listFiles(source).map(rel => path.join(dest, rel));

  if (args.dryRun) {
    print({
      status: "dry-run",
      mode: destExists ? "replace" : "create",
      dest,
      filesWritten: relativeFiles.length,
      files: relativeFiles,
    });
    process.exit(0);
  }

  const stamp = `${Date.now()}-${process.pid}`;
  const stageDir = path.join(destParent, `.${path.basename(dest)}.staging-${stamp}`);
  const rollbackDir = path.join(destParent, `.${path.basename(dest)}.rollback-${stamp}`);
  let renamedOldDest = false;

  try {
    fs.mkdirSync(destParent, { recursive: true });
    removeDirIfExists(stageDir);
    removeDirIfExists(rollbackDir);

    copyDir(source, stageDir);

    if (destExists) {
      fs.renameSync(dest, rollbackDir);
      renamedOldDest = true;
    }

    fs.renameSync(stageDir, dest);

    if (renamedOldDest) {
      removeDirIfExists(rollbackDir);
    }
    
    // 部署成功后清理源草稿目录 (Garbage Collection)
    if (source !== dest && fs.existsSync(source)) {
      removeDirIfExists(source);
    }
  } catch (err) {
    try {
      if (!fs.existsSync(dest) && renamedOldDest && fs.existsSync(rollbackDir)) {
        fs.renameSync(rollbackDir, dest);
      }
    } catch {}

    removeDirIfExists(stageDir);

    print({
      status: "error",
      code: "WRITE_FAILED",
      message: `写入文件失败：${err.message}`,
      dest,
      suggestion: "请检查目标目录权限、磁盘空间，以及是否有其他进程占用该目录。",
      file: __filename
    });
    process.exit(1);
  }

  print({
    status: "success",
    mode: destExists ? "replace" : "create",
    dest,
    filesWritten: relativeFiles.length,
    files: relativeFiles,
  });
}

function print(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
}

main();
