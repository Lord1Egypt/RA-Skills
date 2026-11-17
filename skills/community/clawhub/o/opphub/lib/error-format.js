//
// P1-8 错误结构化: 所有 bin 返统一错误格式
//   旧: { ok:false, error:"code", message:"..." } (零散, 无法分类)
//   新: { ok:false, stage, code, retryable, hint, traceId }
//
// 字段语义:
//   stage     - 错误发生的阶段 (auth/token/server/parse/io)
//   code      - 错误码 (snake_case, 机器可读)
//   retryable - 是否可重试 (true/false, 决定 bot 是否自动重试)
//   hint      - 给 user 看的提示 (中文, 简洁, 含 action)
//   traceId   - 本次请求 ID (UUID), 关联 server log / OpenClaw log
//
// 用法:
//   import { formatError, formatOk, ERR_STAGES, ERR_CODES, isRetryable } from "../lib/error-format.js";
//   out(formatError({ stage: "token", code: "no_token", retryable: false, hint: "先偶合登录" }));
//   out(formatOk({ userId: "user_xxx" }));

import { randomUUID } from "node:crypto";

// === 阶段枚举 ===
export const ERR_STAGES = {
  AUTH: "auth",        // OAuth / Keychain / token 鉴权
  TOKEN: "token",      // token 读取/刷新/写入
  PLUGIN: "plugin",    // plugin 缺失/不可用
  CHANNEL: "channel",  // 通道读取/写入
  CRON: "cron",        // cron 读取/写入
  SERVER: "server",    // server HTTP 调用
  PARSE: "parse",      // 输入解析 (JSON / xls / rawText)
  IO: "io",            // 文件读写
  VALIDATE: "validate",// 字段校验
  INTERNAL: "internal",// 内部错误 (uncaught)
};

// === 错误码 (按 stage 分组) ===
export const ERR_CODES = {
  // auth
  no_token: { stage: "auth", retryable: false },
  device_code_failed: { stage: "auth", retryable: true },
  device_flow_expired: { stage: "auth", retryable: false },
  device_flow_denied: { stage: "auth", retryable: false },
  invalid_credentials: { stage: "auth", retryable: false },
  // token
  keychain_unavailable: { stage: "token", retryable: true },
  token_refresh_failed: { stage: "token", retryable: true },
  token_expired: { stage: "token", retryable: true },
  // plugin
  plugin_missing: { stage: "plugin", retryable: false },
  plugin_offline: { stage: "plugin", retryable: true },
  plugin_install_failed: { stage: "plugin", retryable: true },
  // channel
  channels_unavailable: { stage: "channel", retryable: true },
  no_default_channel: { stage: "channel", retryable: false },
  // cron
  cron_create_failed: { stage: "cron", retryable: true },
  cron_read_failed: { stage: "cron", retryable: true },
  // server
  network_failed: { stage: "server", retryable: true },
  server_error: { stage: "server", retryable: true },
  rate_limit: { stage: "server", retryable: true },
  // parse
  invalid_json: { stage: "parse", retryable: false },
  invalid_cards: { stage: "parse", retryable: false },
  binary_xls_not_supported: { stage: "parse", retryable: false },
  missing_columns: { stage: "parse", retryable: false },
  // io
  file_not_found: { stage: "io", retryable: false },
  file_read_failed: { stage: "io", retryable: true },
  // validate
  missing_name: { stage: "validate", retryable: false },
  missing_cards: { stage: "validate", retryable: false },
  missing_raw_text: { stage: "validate", retryable: false },
  missing_columns_validation: { stage: "validate", retryable: false },
  industry_ambiguous: { stage: "validate", retryable: false },
  industry_weak_evidence: { stage: "validate", retryable: false },
  no_evidence_cards: { stage: "validate", retryable: false },
  // internal
  internal_error: { stage: "internal", retryable: false },
};

// === 格式化函数 ===

/**
 * 格式化错误
 * @param {Object} opts
 * @param {string} opts.stage - 阶段 (或用 code 推断)
 * @param {string} opts.code - 错误码
 * @param {string} [opts.message] - 详细消息 (技术细节, 给 dev 看)
 * @param {string} [opts.hint] - 给 user 看的提示
 * @param {boolean} [opts.retryable] - 可否重试
 * @param {string} [opts.traceId] - trace ID
 * @param {Object} [opts.extra] - 其他字段
 * @returns {Object}
 */
export function formatError({ stage, code, message, hint, retryable, traceId, ...extra }) {
  // 1. 从 ERR_CODES 推断 stage + retryable (用户没显式传时)
  const def = ERR_CODES[code] || {};
  const finalStage = stage || def.stage || ERR_STAGES.INTERNAL;
  const finalRetryable = retryable ?? def.retryable ?? false;
  const finalTraceId = traceId || randomUUID();

  return {
    ok: false,
    error: code,
    stage: finalStage,
    retryable: finalRetryable,
    traceId: finalTraceId,
    ...(message ? { message } : {}),
    ...(hint ? { hint } : {}),
    ...extra,
  };
}

/**
 * 格式化成功响应
 * @param {Object} data - 业务字段
 * @param {string} [data.traceId]
 * @returns {Object}
 */
export function formatOk({ traceId, ...data } = {}) {
  return {
    ok: true,
    ...data,
    ...(traceId ? { traceId } : { traceId: randomUUID() }),
  };
}

/**
 * 判断错误是否可重试
 * @param {Object} errResult - formatError() 返的对象
 * @returns {boolean}
 */
export function isRetryable(errResult) {
  return errResult?.retryable === true;
}

// === 兼容旧 API ===

/**
 * 旧 errorOut 风格: 返错误 + 输 stdout + exit 1
 * 用法: errorOutAndExit({ code, hint, ... })
 */
export function errorOutAndExit({ code, message, hint, stage, retryable, ...extra }) {
  const err = formatError({ code, message, hint, stage, retryable, ...extra });
  console.log(JSON.stringify(err, null, 2));
  process.exit(1);
}
