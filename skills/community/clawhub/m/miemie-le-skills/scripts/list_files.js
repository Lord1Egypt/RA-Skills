#!/usr/bin/env node
/**
 * list_files.js
 * -------------
 * 以跨平台方式列出目标目录中的所有文件，并按相对路径排序输出。
 *
 * 用法:
 *   node list_files.js --target <目录>
 */

"use strict";

const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--target") {
      args.target = argv[++i];
    }
  }
  return args;
}

function walk(baseDir, currentDir = baseDir, acc = []) {
  for (const entry of fs.readdirSync(currentDir, { withFileTypes: true })) {
    const fullPath = path.join(currentDir, entry.name);
    if (entry.isDirectory()) {
      walk(baseDir, fullPath, acc);
    } else {
      acc.push(path.relative(baseDir, fullPath));
    }
  }
  return acc;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.target) {
    print({ status: "error", code: "MISSING_ARG", message: "缺少 --target 参数，请提供要列出文件的目录路径。", file: __filename });
    process.exit(1);
  }

  const target = path.resolve(args.target);
  if (!fs.existsSync(target)) {
    print({ status: "error", code: "NOT_FOUND", message: `目标目录不存在：${target}`, file: __filename });
    process.exit(1);
  }

  if (!fs.statSync(target).isDirectory()) {
    print({ status: "error", code: "INVALID_PATH", message: `--target 指向的不是目录：${target}`, file: __filename });
    process.exit(1);
  }

  const files = walk(target).sort();
  print({ status: "success", target, filesCount: files.length, files });
}

function print(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
}

main();
