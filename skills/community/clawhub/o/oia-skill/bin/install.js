#!/usr/bin/env node
/**
 * oia-skill 安装脚本
 * 用法：npx @oia-ai/oia-skill          安装到当前项目 .claude/skills/oia-skill
 *       npx @oia-ai/oia-skill --global 安装到用户目录 ~/.claude/skills/oia-skill
 */
"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

// 包安装后的根目录（bin/ 的上一级）
const PKG_ROOT = path.join(__dirname, "..");
const FILES = ["SKILL.md", "README.md"];

const isGlobal = process.argv.includes("--global") || process.argv.includes("-g");
const targetDir = path.join(
  isGlobal ? os.homedir() : process.cwd(),
  ".claude",
  "skills",
  "oia-skill",
);

fs.mkdirSync(targetDir, { recursive: true });
for (const file of FILES) {
  fs.copyFileSync(path.join(PKG_ROOT, file), path.join(targetDir, file));
}

console.log("");
console.log("✅ oia-skill 已安装到：" + targetDir);
console.log('   在 Claude Code 里说「初始化一个 oia 项目」或输入 /oia-skill 即可触发。');
console.log("");
