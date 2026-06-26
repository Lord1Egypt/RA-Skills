#!/usr/bin/env node
"use strict";

/**
 * Keep MCP 调用桥（exec fallback）
 *
 * 本脚本是 @keepclaw/skill-sdk/mcp-cli 的 shim：实际实现住在 SDK 里，
 * 所有 skill 共用同一份退出码映射、envelope 格式和 argv 约定。
 *
 * 保留这个脚本路径（packages/keep-query/scripts/mcp-call.js）是为了
 * 兼容运行器里既有的 exec 命令模板：
 *   node {baseDir}/scripts/mcp-call.js <tool> '<json_args>'
 *
 * 详细用法、退出码、环境变量见 @keepclaw/skill-sdk 的 src/mcp-cli.js 注释。
 *
 * 埋点：为与 keep-record / keep CLI 区分，exec 桥默认
 * KEEP_INVOKE_SOURCE=keep-query（见 skill-sdk reportInvoke source）。
 */

if (!process.env.KEEP_INVOKE_SOURCE) {
  process.env.KEEP_INVOKE_SOURCE = "keep-query";
}
require("@keepclaw/skill-sdk/mcp-cli").runCli();
