#!/usr/bin/env node
"use strict";

/**
 * Keep 扫码登录轮询器 shim（background exec 入口）
 *
 * 本脚本是 @keepclaw/skill-sdk/login-wait 的 shim：实际实现住在 SDK 里，
 * 所有 skill 共用同一份轮询间隔、超时窗口和 envelope 格式。
 *
 * 保留这个脚本路径（packages/keep-query/scripts/login-wait.js）是为了给
 * OpenClaw / Hermes 这种 exec-only agent 一个**稳定**的命令模板，不受
 * npm hoist 行为影响：
 *
 *   node {baseDir}/scripts/login-wait.js <qrcodeId>
 *
 * 详细用法、退出码、envelope 约定见 @keepclaw/skill-sdk 的 src/login-wait.js 注释。
 */

require("@keepclaw/skill-sdk/login-wait").runCli();
