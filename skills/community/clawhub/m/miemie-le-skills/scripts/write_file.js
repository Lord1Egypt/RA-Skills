#!/usr/bin/env node
/**
 * write_file.js
 * -------------
 * 跨平台通用文件写入脚本，支持自动创建父目录。
 * 
 * 用法:
 *   node write_file.js --file "<文件路径>" --content "<文件内容>"
 * 或者从 stdin 读取内容:
 *   echo "content" | node write_file.js --file "<文件路径>"
 */

"use strict";

const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--file") { args.file = argv[++i]; continue; }
    if (argv[i] === "--content") { args.content = argv[++i]; continue; }
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv);
  
  if (!args.file) {
    console.error(JSON.stringify({ status: "error", code: "MISSING_ARG", message: "缺少 --file 参数", file: __filename }));
    process.exit(1);
  }

  const filePath = path.resolve(args.file);
  
  // 安全边界校验：必须写入到 .openclaw 目录下
  if (!filePath.replace(/\\/g, '/').includes('/.openclaw/')) {
    console.error(JSON.stringify({ status: "error", code: "PATH_TRAVERSAL_BLOCKED", message: `拒绝访问：目标路径不在 .openclaw 边界内 (${filePath})`, file: __filename }));
    process.exit(1);
  }

  const dirPath = path.dirname(filePath);

  try {
    fs.mkdirSync(dirPath, { recursive: true });
    
    if (args.content !== undefined) {
      // Content provided via argument
      fs.writeFileSync(filePath, args.content, "utf8");
      console.log(JSON.stringify({ status: "success", file: filePath }));
      process.exit(0);
    } else {
      // Content provided via stdin
      let data = "";
      process.stdin.setEncoding("utf8");
      process.stdin.on("data", chunk => { data += chunk; });
      process.stdin.on("end", () => {
        fs.writeFileSync(filePath, data, "utf8");
        console.log(JSON.stringify({ status: "success", file: filePath }));
        process.exit(0);
      });
    }
  } catch (err) {
    console.error(JSON.stringify({ status: "error", code: "WRITE_FAILED", message: err.message, file: __filename }));
    process.exit(1);
  }
}

main();