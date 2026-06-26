#!/usr/bin/env node
// postinstall - hint about BOT_BASE_URL after npm install.
// 零 require 外部包；只用 fs/path（node 内置），不算 §6.2 禁的 child_process。
// 不动用户文件，纯写 stderr。已配置 / CI / silent 自动跳过。

"use strict";

var fs = require("fs");
var path = require("path");

// Skip 1: CI / silent npm
if (process.env.CI || process.env.npm_config_loglevel === "silent") {
  process.exit(0);
}

// Skip 2: env BOT_BASE_URL set
if (process.env.BOT_BASE_URL && process.env.BOT_BASE_URL.trim()) {
  process.exit(0);
}

// Skip 3: ~/.openclaw/share/config.json baseUrl set (升级安装不重复唠叨)
try {
  var home = process.env.HOME || process.env.USERPROFILE;
  if (home) {
    var cfg = path.join(home, ".openclaw", "share", "config.json");
    if (fs.existsSync(cfg)) {
      var data = JSON.parse(fs.readFileSync(cfg, "utf8"));
      if (data && typeof data.baseUrl === "string" && data.baseUrl.trim()) {
        process.exit(0);
      }
    }
  }
} catch (_e) {
  // 读不到/解析失败不影响主流程，继续往下打提示
}

// ---- 提示文案 ----
var pkgVersion = "?";
try {
  pkgVersion = require("../package.json").version || "?";
} catch (_e) {
  /* ignore */
}

var tty = process.stderr && process.stderr.isTTY;
var c = tty
  ? {
      reset: "\x1b[0m",
      bold: "\x1b[1m",
      dim: "\x1b[2m",
      cyan: "\x1b[36m",
      yellow: "\x1b[33m",
      green: "\x1b[32m",
    }
  : { reset: "", bold: "", dim: "", cyan: "", yellow: "", green: "" };

var msg =
  "\n" +
  c.bold + c.cyan + "@huo15/openclaw-enhance v" + pkgVersion + " 装好了" + c.reset + "\n" +
  "\n" +
  c.yellow + "推荐配置：" + c.bold + "BOT_BASE_URL" + c.reset + c.yellow + "（公网下载域名）" + c.reset + "\n" +
  "\n" +
  "如果你打算用 " + c.bold + "enhance_share_file" + c.reset + " 工具给企微 / 飞书 / 钉钉群发大文件下载链接\n" +
  "（>20-50MB IM 直传不了的场景），enhance 必须知道你的" + c.bold + "公网 base URL" + c.reset + "才能生成\n" +
  "群成员点得开的链接。不配置的副作用：链接会落 LAN IP / localhost，群里其他人点开 404。\n" +
  "\n" +
  c.bold + "三种配置方式（任选其一，优先级从高到低）：" + c.reset + "\n" +
  "\n" +
  "  " + c.cyan + "1." + c.reset + " shell 环境变量（最简单，OpenClaw 重启即生效）\n" +
  "       " + c.dim + "echo 'export BOT_BASE_URL=https://your-domain.com' >> ~/.zshrc" + c.reset + "\n" +
  "       " + c.dim + "source ~/.zshrc" + c.reset + "\n" +
  "\n" +
  "  " + c.cyan + "2." + c.reset + " openclaw.json 显式配（per-account 隔离）\n" +
  "       " + c.dim + 'plugins.entries.enhance.config.botShare.baseUrl = "https://your-domain.com"' + c.reset + "\n" +
  "\n" +
  "  " + c.cyan + "3." + c.reset + " 让 LLM 一次性持久化（" + c.green + "最自然" + c.reset + "——OpenClaw 启动后跟它说话即可）\n" +
  "       " + c.dim + '你："把 baseUrl 设成 https://your-domain.com"' + c.reset + "\n" +
  "       " + c.dim + "LLM 自动调 enhance_share_set_baseurl 工具，写到 ~/.openclaw/share/config.json" + c.reset + "\n" +
  "\n" +
  c.dim + "文档：https://cnb.cool/huo15/ai/huo15-openclaw-enhance" + c.reset + "\n" +
  c.dim + "（已配置 / CI 环境会自动跳过此提示）" + c.reset + "\n" +
  "\n";

process.stderr.write(msg);
