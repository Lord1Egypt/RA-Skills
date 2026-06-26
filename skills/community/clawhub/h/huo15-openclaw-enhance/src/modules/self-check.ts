/**
 * 模块: 输出自检（Self-Check）
 *
 * Hook: before_agent_reply
 * 时机: AI 回复发送前，拦截检查
 * 作用: 检测空输出、错误关键词、格式异常，记录问题但不阻断正常输出
 *
 * 来源: 对标 Claude Code "评估与观测" 能力（Agent Harness 六层第5层）
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { getDb, logSafetyEvent } from "../utils/sqlite-store.js";
import { DEFAULT_AGENT_ID } from "../types.js";

// ── 配置 ──
export interface SelfCheckConfig {
  /** 是否启用 */
  enabled?: boolean;
  /** 检查空输出 */
  checkEmpty?: boolean;
  /** 检查 NO_REPLY 标记 */
  checkNoReply?: boolean;
  /** 检查错误关键词 */
  checkErrorKeywords?: boolean;
  /** 检查超长输出 */
  checkExcessiveLength?: boolean;
  /** 超长阈值（字符），默认 10000 */
  maxLength?: number;
  /** 错误关键词列表 */
  errorKeywords?: string[];
  /** 是否阻断（true=拦截，false=仅记录） */
  blockOnEmpty?: boolean;
}

const DEFAULT_ERROR_KEYWORDS = [
  "cannot",
  "unable to",
  "failed to",
  "error occurred",
  "sorry",
  "apologi",
  "something went wrong",
  "unexpected error",
];

function scoreKeywordMatch(text: string, keywords: string[]): number {
  const lower = text.toLowerCase();
  return keywords.filter((k) => lower.includes(k.toLowerCase())).length;
}

export function registerSelfCheck(api: OpenClawPluginApi, config?: SelfCheckConfig) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();

  const enabled = config?.enabled !== false;
  if (!enabled) return;

  const checkEmpty = config?.checkEmpty !== false;
  const checkNoReply = config?.checkNoReply !== false;
  const checkErrorKeywords = config?.checkErrorKeywords !== false;
  const checkExcessiveLength = config?.checkExcessiveLength !== false;
  const maxLength = config?.maxLength ?? 10000;
  const errorKeywords = config?.errorKeywords ?? DEFAULT_ERROR_KEYWORDS;
  const blockOnEmpty = config?.blockOnEmpty ?? false;

  // ── Hook: before_agent_reply ──（v5.7.8: typed via openclaw 4.24 SDK）
  api.on("before_agent_reply", (event, ctx) => {
    const agentId = (ctx?.agentId ?? DEFAULT_AGENT_ID).trim();
    const body: string = event?.cleanedBody ?? "";
    const issues: string[] = [];

    // 1. 检查空输出
    if (checkEmpty && body.trim().length === 0) {
      issues.push("empty_output");
      api.logger.warn(`[enhance-selfcheck] 检测到空输出 (agent: ${agentId})`);
    }

    // 2. 检查 NO_REPLY 标记（正常，静默放行）
    if (checkNoReply) {
      const trimmed = body.trim().toUpperCase();
      if (trimmed === "NO_REPLY" || trimmed === "HEARTBEAT_OK") {
        return; // void = 不接管
      }
    }

    // 3. 检查超长输出
    if (checkExcessiveLength && body.length > maxLength) {
      issues.push(`excessive_length:${body.length}`);
      api.logger.warn(
        `[enhance-selfcheck] 检测到超长输出 ${body.length} chars (agent: ${agentId})，超过阈值 ${maxLength}`,
      );
    }

    // 4. 检查错误关键词（只记录，不阻断）
    if (checkErrorKeywords && body.trim().length > 0) {
      const errorScore = scoreKeywordMatch(body, errorKeywords);
      if (errorScore >= 2) {
        issues.push(`error_keywords:${errorScore}`);
        api.logger.warn(
          `[enhance-selfcheck] 检测到 ${errorScore} 个错误关键词 (agent: ${agentId}): ${body.slice(0, 100)}`,
        );
      }
    }

    // 5. 记录到 safety_log
    if (issues.length > 0) {
      logSafetyEvent(
        db,
        agentId,
        "self_check",
        issues.join(" | "),
        "log",
        JSON.stringify({ issues, bodyLength: body.length }),
        "self_check_output_issue",
      );
    }

    // 6. 空输出阻断（可选）
    if (blockOnEmpty && issues.includes("empty_output")) {
      return {
        handled: true,
        reply: {
          text: "⚠️ 未能生成有效回复，请重试。",
          isError: true,
        },
        reason: "self_check: empty output blocked",
      };
    }

    // void = 不接管，让原回复正常发送
    return;
  });

  api.logger.info("[enhance] 输出自检模块已加载（before_agent_reply hook，非阻断式）");
}
