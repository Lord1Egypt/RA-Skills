/**
 * 模块: 上下文守护 (Context Watchdog) v6.5.3
 *
 * 解决场景：长会话不知不觉吃满 ctx 窗口 → 龙虾原生在 overflow **错误发生后**才
 * 走 model-fallback；用户体验是"突然报错"或"突然丢上下文"，没有预警。
 *
 * 龙虾原生已有（不复制，红线 #2）：
 *   - isContextOverflowError / isLikelyContextOverflowError 错误检测
 *   - model-fallback.ts ctx overflow 触发后做 model fallback
 *   - /compact 命令 + before_compaction / after_compaction hook
 *
 * 龙虾原生没有的（本模块补）：
 *   1. **会话级 token 累加追踪**：hook llm_output 拿 usage 实时累加到 sessionKey
 *   2. **三阶预警**（70%/85%/95%）：在 overflow **之前** 注入 prependContext，
 *      让 LLM 主动收尾 / 走 /compact / 切大 ctx 模型
 *   3. **after_compaction 自动归零**：龙虾刚 compact 完，session 重置 token 计数
 *   4. **enhance_ctx_status 工具**：LLM 主动查当前用量
 *
 * 非侵入式保证：
 *   - 零 child_process / 零新 npm 依赖
 *   - 不修龙虾核心 / 不复制 model-fallback / 不抢龙虾 routing 决策
 *   - 仅观察 + 提醒（通过 prompt supplement）；切模型让 model-router 自己决定
 *
 * 实测痛点（2026-05-11）：
 *   用户长会话 + 跨日续接 + 多轮工具调用，token 累计到 180K+ 还没主动 /compact，
 *   突然遇到 200K 上限报错。三阶预警让 LLM 在 70% 就开始 awareness，
 *   85% 强烈建议收尾，95% 命令式停手。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { DEFAULT_AGENT_ID } from "../types.js";
import type { ContextWatchdogConfig, ChannelThresholds } from "../types.js";
import { isModelBanned } from "../utils/latency-tracker.js";
import { getDb } from "../utils/sqlite-store.js";
import {
  loadCtxUsage,
  batchSaveCtxUsage,
  getAgentCtxProfile,
  getMonthlyCostEstimate,
  purgeOldCtxUsage,
  type CtxUsageRow,
} from "../utils/ctx-usage-db.js";

// ── 已知 model contextWindow 表（fallback；优先用 openclaw.json 实际值） ──
//
// 数据来源：各 provider 官网 + 实测 OpenClaw 4.29 capability scan
// 未列入的 model 默认走 DEFAULT_CTX_MAX 保守值。
const KNOWN_MODEL_CTX_MAX: Record<string, number> = {
  // Anthropic
  "claude-opus-4.7": 200_000,
  "claude-opus-4.7-1m": 1_000_000,
  "claude-sonnet-4.5": 200_000,
  "claude-haiku-4.5": 200_000,
  // OpenAI
  "gpt-5.4": 200_000,
  "gpt-5.4-codex": 200_000,
  "gpt-5.4-mini": 128_000,
  "o1": 200_000,
  // Google
  "gemini-2.5-pro": 2_000_000,
  "gemini-2.5-flash": 1_000_000,
  // 智谱
  "glm-4.6": 200_000,
  "glm-4.6-airx": 128_000,
  "glm-4-flash": 128_000,
  "glm-4-air": 128_000,
  // DeepSeek
  "deepseek-v3.2": 128_000,
  "deepseek-r1": 128_000,
  "deepseek-coder": 128_000,
  // Moonshot
  "kimi-k2": 256_000,
  "kimi-k2-200k": 256_000,
  "kimi-k2-128k": 128_000,
  // Minimax
  "minimax-m2": 200_000,
  "abab7-chat-preview": 245_000,
};

const DEFAULT_CTX_MAX = 128_000; // 未知 model 保守值
const DEFAULT_HINT_AT = 0.70;
const DEFAULT_WARN_AT = 0.85;
const DEFAULT_CRITICAL_AT = 0.95;
const DEFAULT_ESCALATE_AT = 0.80; // 80% 起触发"建议切大 ctx 模型"
const DEFAULT_FORCE_ESCALATE_AT = 0.95; // v6.5.5：强切阈值（critical 同位）
const MAX_TRACKED_SESSIONS = 500;
const HOOK_PRIORITY_FORCE_ESCALATE = 100; // 比 model-router 默认（无 priority）高，确保抢先

/**
 * v6.5.5：long-ctx 候选 model id 列表（按优先级降序）。
 * ctx-watchdog 在 95% 强切时按此顺序选第一个非 banned 且 ctx≥256K 的。
 * 用户可通过 ContextWatchdogConfig.longCtxCandidates 覆盖。
 *
 * v6.6.4: 同时维护 MODEL_TO_PROVIDER_MAP，强切时返回 { modelOverride, providerOverride }
 *   双字段（before）只返 modelOverride 不返 providerOverride，OpenClaw 核心拿到错配 provider+model
 *   组合 → API 拒 400 mismatch → fallback chain_exhausted → 用户看到通用错误页。
 */
const LONG_CTX_CANDIDATES_DEFAULT: string[] = [
  "claude-opus-4.7-1m",   // 1M ctx
  "gemini-2.5-pro",        // 2M ctx
  "gemini-2.5-flash",      // 1M ctx
  "kimi-k2",               // 256K ctx
  "kimi-k2-200k",          // 256K ctx
  "claude-opus-4.7",       // 200K（最后兜底；与当前 200K 持平但起码不更小）
  "claude-sonnet-4.5",     // 200K
  "minimax-m2",            // 200K
];

/**
 * v6.6.4: 裸 model id → provider 映射。
 *
 * Why：candidates 是裸 model id（无 provider prefix），但 OpenClaw 核心 hook 强切时需要
 * 同时知道 provider 才能正确路由到对应 provider client，否则把 model id 整串塞给当前
 * session 的 provider client → API 拒 400 "passed <wrong-model>"。
 *
 * 添加新 model 时同步加这里 + KNOWN_MODEL_CTX_MAX + KNOWN_MODEL_COST。
 */
const MODEL_TO_PROVIDER_MAP: Record<string, string> = {
  // Anthropic
  "claude-opus-4.7-1m": "anthropic",
  "claude-opus-4.7": "anthropic",
  "claude-sonnet-4.5": "anthropic",
  "claude-haiku-4.5": "anthropic",
  // Google AI Studio
  "gemini-2.5-pro": "google-ai-studio",
  "gemini-2.5-flash": "google-ai-studio",
  // Moonshot
  "kimi-k2": "moonshot",
  "kimi-k2-200k": "moonshot",
  "kimi-k2-128k": "moonshot",
  // Minimax
  "minimax-m2": "minimax",
  "abab7-chat-preview": "minimax",
  // DeepSeek
  "deepseek-v3.2": "deepseek",
  "deepseek-r1": "deepseek",
  "deepseek-coder": "deepseek",
  // OpenAI
  "gpt-5.4": "openai",
  "gpt-5.4-codex": "openai",
  "gpt-5.4-mini": "openai",
  "o1": "openai",
  // 智谱
  "glm-4.6": "zhipu",
  "glm-4.6-airx": "zhipu",
  "glm-4-flash": "zhipu",
  "glm-4-air": "zhipu",
};

/**
 * v6.5.5：每张图片估算 token（OpenAI/Anthropic 实测平均）。
 * 视频/音频按帧数 × 1500 累加（粗估，provider 实际可能差距大；以 llm_output usage 为准）。
 */
const TOKENS_PER_IMAGE = 1500;
const TOKENS_PER_VIDEO_FRAME = 1500;
const TOKENS_PER_AUDIO_SECOND = 100;

/**
 * v6.6.0 P1-6：按 model 细分图片 token 成本（默认 1500 兜底）。
 * 数据来源：各 provider 官方文档实测平均。
 */
const KNOWN_MODEL_IMAGE_TOKEN_COST: Record<string, number> = {
  // Anthropic — Claude vision 文档：单图大致 ~1568 token
  "claude-opus-4.7-1m": 1500,
  "claude-opus-4.7": 1500,
  "claude-sonnet-4.5": 1500,
  "claude-haiku-4.5": 1500,
  // OpenAI — GPT-5 vision low ~85，high ~1500，default high
  "gpt-5.4": 1200,
  "gpt-5.4-codex": 1200,
  "gpt-5.4-mini": 1200,
  // Google Gemini — 按 tile（768×768）每 tile ~258 token，单图通常 1-3 tile
  "gemini-2.5-pro": 800,
  "gemini-2.5-flash": 800,
  // 智谱 GLM-4V
  "glm-4.6": 1500,
  // Moonshot Kimi-VL
  "kimi-k2": 1500,
  // DeepSeek 大部分 model 不支持图片，给保守默认
};

/**
 * v6.6.0 P1-4：按 model 单价（USD per 1M token；input / output）。
 * 数据来源：各 provider 2026 官方定价（仅热门 model；未列表用 openclaw.json 注册值兜底）。
 */
const KNOWN_MODEL_COST: Record<string, { in: number; out: number }> = {
  "claude-opus-4.7-1m": { in: 15, out: 75 }, // 1M ctx 单独定价
  "claude-opus-4.7": { in: 15, out: 75 },
  "claude-sonnet-4.5": { in: 3, out: 15 },
  "claude-haiku-4.5": { in: 1, out: 5 },
  "gpt-5.4": { in: 5, out: 15 },
  "gpt-5.4-codex": { in: 5, out: 15 },
  "gpt-5.4-mini": { in: 0.15, out: 0.6 },
  "o1": { in: 15, out: 60 },
  "gemini-2.5-pro": { in: 1.25, out: 5 },
  "gemini-2.5-flash": { in: 0.1, out: 0.4 },
  "glm-4.6": { in: 1, out: 2 },
  "glm-4-flash": { in: 0, out: 0 },
  "deepseek-v3.2": { in: 0.14, out: 0.28 },
  "deepseek-r1": { in: 0.55, out: 2.19 },
  "deepseek-coder": { in: 0.14, out: 0.28 },
  "kimi-k2": { in: 0.6, out: 2.5 },
  "kimi-k2-200k": { in: 0.6, out: 2.5 },
  "kimi-k2-128k": { in: 0.6, out: 2.5 },
  "minimax-m2": { in: 1, out: 3 },
  "abab7-chat-preview": { in: 0.8, out: 0.8 },
};

/**
 * v6.6.0 P2-8：按 channel 内置阈值（用户可通过 ContextWatchdogConfig.thresholdsByChannel 覆盖）。
 * 群聊每条消息进上下文涨得快 → 更激进；单聊/服务号居中；terminal 用户能 /compact → 宽松。
 *
 * channel 来源：ctx.channelId / ctx.originatingChannel；wecom 进一步按 agentId 含 "group" 拆分。
 */
const CHANNEL_THRESHOLDS_DEFAULT: Record<string, ChannelThresholds> = {
  "wecom-group": {
    hintAt: 0.60,
    warnAt: 0.75,
    criticalAt: 0.90,
    escalateToLongCtxAt: 0.65,
    forceEscalateAt: 0.90,
  },
  "wecom-direct": {
    hintAt: 0.65,
    warnAt: 0.80,
    criticalAt: 0.92,
    escalateToLongCtxAt: 0.70,
    forceEscalateAt: 0.92,
  },
  "wechat-service": {
    hintAt: 0.65,
    warnAt: 0.80,
    criticalAt: 0.92,
    escalateToLongCtxAt: 0.70,
    forceEscalateAt: 0.92,
  },
  "dingtalk": {
    hintAt: 0.65,
    warnAt: 0.80,
    criticalAt: 0.92,
    escalateToLongCtxAt: 0.70,
    forceEscalateAt: 0.92,
  },
  // terminal / default：不指定 → 沿用全局配置（默认 0.70/0.85/0.95/0.80/0.95）
};

interface SessionUsage {
  sessionKey: string;
  agentId: string;
  /** llm_output 累加来的真实 token 用量 */
  totalTokens: number;
  /** v6.5.5：本轮 prompt 事前估算（before_prompt_build / before_model_resolve 用），LLM 调用后清零 */
  pendingTokens: number;
  lastModel?: string;
  lastModelCtxMax: number;
  /**
   * v6.5.5：首次因 ctx 压力被切走前的"原始 model"。
   * 用于 P1-5（ctx 降下来后建议切回原模型）和日志溯源。
   */
  originalModel?: string;
  /** 已发出过的最高阈值（防抖：同 session 同阈值不重复警告）*/
  lastWarnedThreshold: number;
  /**
   * v6.5.7 P2-9：最近 N 轮 llm_output 的 token 增量（最多 PREDICTION_HISTORY_LEN 个，FIFO）。
   * 用于算 avgTokensPerTurn → 预测 turnsToWarn / turnsToCritical。
   */
  tokensPerTurnHistory: number[];
  /** v6.5.7 P2-9：是否已发出过预测式提醒（一次性，防抖；until threshold 真到了再重置）*/
  predictionEmittedFor?: number;
  /**
   * v6.6.0 P1-4：会话级累计估算成本（USD）。
   * llm_output 时按 KNOWN_MODEL_COST 累加：cost = (input × in + output × out) / 1_000_000
   */
  estimatedCostUSD: number;
  /** v6.6.0 P1-4：是否已发出过预算警告 banner（防抖；月度预算 ≥80% 时一次性） */
  budgetWarnedAt?: number;
  /**
   * v6.6.1 P3-13：最近见过的 runId 集合（bounded，最多 SEEN_RUNIDS_LIMIT 个 FIFO）。
   * 防止龙虾 model-fallback retry 时 llm_output 同 runId 来两次导致 token/cost 重复累加。
   * 仅内存（重启后置空 — retry 风险也消失）。
   */
  seenRunIds: Set<string>;
  /**
   * v6.6.1 P2-10：mute 截止时间戳（ms）。在此之前 before_prompt_build 不发任何 banner
   * （revert / threshold / prediction / budget 都跳过）。仅内存，重启自动解除。
   */
  mutedUntilMs?: number;
  lastUpdatedAt: number;
}

const SEEN_RUNIDS_LIMIT = 20;

const PREDICTION_HISTORY_LEN = 5;
const PREDICTION_LOOKAHEAD_TURNS = 3;

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return (ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID;
}

function pickSessionKey(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

/**
 * 从 modelId 推断 ctx 上限。
 * 支持 "<provider>/<model>" 全 ref 或裸 modelId；先 strip provider 前缀再查表。
 */
function resolveCtxMax(modelId: string | undefined): number {
  if (!modelId) return DEFAULT_CTX_MAX;
  const bare = modelId.includes("/") ? modelId.split("/").pop()! : modelId;
  // 完全匹配
  if (KNOWN_MODEL_CTX_MAX[bare]) return KNOWN_MODEL_CTX_MAX[bare];
  // 前缀匹配（kimi-k2-anything → kimi-k2）
  for (const known of Object.keys(KNOWN_MODEL_CTX_MAX)) {
    if (bare.startsWith(known)) return KNOWN_MODEL_CTX_MAX[known];
  }
  // 启发式：含 1m / 1000k → 1M，含 256k → 256K，含 200k → 200K，含 128k → 128K
  if (/[-_](1m|1000k)/i.test(bare)) return 1_000_000;
  if (/[-_]256k/i.test(bare)) return 256_000;
  if (/[-_]200k/i.test(bare)) return 200_000;
  if (/[-_]128k/i.test(bare)) return 128_000;
  if (/[-_]32k/i.test(bare)) return 32_000;
  return DEFAULT_CTX_MAX;
}

/** 累加 usage：input + output + cacheRead（cacheRead 也占用 ctx） */
function sumUsage(usage: { input?: number; output?: number; cacheRead?: number; cacheWrite?: number; total?: number } | undefined): number {
  if (!usage) return 0;
  if (typeof usage.total === "number" && usage.total > 0) return usage.total;
  return (usage.input ?? 0) + (usage.output ?? 0) + (usage.cacheRead ?? 0);
}

/** v6.6.0 P1-6：按 model 返单张图片 token 成本（默认 TOKENS_PER_IMAGE） */
function resolveImageTokens(modelId: string | undefined): number {
  if (!modelId) return TOKENS_PER_IMAGE;
  const bare = modelId.includes("/") ? modelId.split("/").pop()! : modelId;
  if (KNOWN_MODEL_IMAGE_TOKEN_COST[bare] !== undefined) return KNOWN_MODEL_IMAGE_TOKEN_COST[bare];
  for (const known of Object.keys(KNOWN_MODEL_IMAGE_TOKEN_COST)) {
    if (bare.startsWith(known)) return KNOWN_MODEL_IMAGE_TOKEN_COST[known];
  }
  return TOKENS_PER_IMAGE;
}

/** v6.6.0 P1-4：按 model 算单轮 cost (USD)；返 0 表示未知 model */
function estimateTurnCostUSD(modelId: string | undefined, usage: { input?: number; output?: number; cacheRead?: number; cacheWrite?: number } | undefined): number {
  if (!modelId || !usage) return 0;
  const bare = modelId.includes("/") ? modelId.split("/").pop()! : modelId;
  let prices = KNOWN_MODEL_COST[bare];
  if (!prices) {
    for (const known of Object.keys(KNOWN_MODEL_COST)) {
      if (bare.startsWith(known)) {
        prices = KNOWN_MODEL_COST[known];
        break;
      }
    }
  }
  if (!prices) return 0;
  // cacheRead 通常按 input × 0.1（90% 折扣，Anthropic/OpenAI 定价）；cacheWrite 按 input × 1.25
  const inputTokens = (usage.input ?? 0) + (usage.cacheRead ?? 0) * 0.1 + (usage.cacheWrite ?? 0) * 1.25;
  const outputTokens = usage.output ?? 0;
  return (inputTokens * prices.in + outputTokens * prices.out) / 1_000_000;
}

/**
 * v6.6.0 P2-8：从 hook ctx 解析 channel 标识。
 * wecom 渠道再按 agentId 含 'group' 拆分成 wecom-group / wecom-direct。
 */
function resolveChannel(ctx: any): string {
  const raw = (ctx?.channelId ?? ctx?.originatingChannel ?? (ctx as any)?.channel ?? "")
    .toString()
    .toLowerCase()
    .trim();
  if (!raw || raw === "terminal") return "default";
  if (raw === "wecom") {
    const agentId = String(ctx?.agentId ?? "").toLowerCase();
    return agentId.includes("group") ? "wecom-group" : "wecom-direct";
  }
  return raw;
}

function buildHintBanner(percent: number, used: number, max: number, modelId: string): string {
  const pct = Math.round(percent * 100);
  return `【上下文用量提示 - ${pct}%】当前会话已累计使用 ~${used.toLocaleString()} / ${max.toLocaleString()} token（model=${modelId}）。
建议告一段落或在合适节点主动调用 \`/compact\` 总结当前会话，避免接近上限时被动截断。
(由 enhance context-watchdog 监测；阈值 ≥${pct}%。关闭：config.contextWatchdog.enabled=false)`;
}

function buildWarnBanner(percent: number, used: number, max: number, modelId: string): string {
  const pct = Math.round(percent * 100);
  return `⚠️ 【上下文警告 - ${pct}%】当前会话已使用 ~${used.toLocaleString()} / ${max.toLocaleString()} token，**强烈建议**立即采取行动：
  1. 优先：当前任务到达自然 checkpoint 时调用 \`/compact\` 让龙虾压缩历史
  2. 备选：完成手头任务后总结当前进度，提示用户开新会话续接
  3. 切模型：如果有更大 ctx 的模型可用（如 kimi-k2 256K / claude-opus-4.7-1m），可直接切换
继续大幅累积 token 会触发 ctx overflow 错误或丢失更早期的上下文。`;
}

function buildCriticalBanner(percent: number, used: number, max: number, modelId: string): string {
  const pct = Math.round(percent * 100);
  return `🚨 【上下文临界 - ${pct}%】**立即停止新任务**！当前会话已用 ~${used.toLocaleString()} / ${max.toLocaleString()} token，距离 ctx 上限不足 ${100 - pct}%。
**必须立刻**：
  1. 总结当前进度（一句话）+ 用 enhance_memory_store 持久化 key 决策
  2. 调用 \`/compact\` 或告知用户『上下文将满，请新开会话续接』
  3. 不要再读新文件 / 不要再调长 prompt 工具
继续走极易触发龙虾 model-fallback overflow handler，丢失最关键的近期上下文。`;
}

function buildEscalateHint(currentModel: string, currentMax: number, used: number, percent: number): string {
  const pct = Math.round(percent * 100);
  return `【建议切大 ctx 模型 - ${pct}%】当前 model=${currentModel}（ctx ${currentMax.toLocaleString()}），用量已达 ${pct}%。
**主动调用 \`enhance_route_to_long_ctx\` 工具立即切换**（推荐）；或继续 /compact / 让 model-router 自选 LONG_CONTEXT_MODELS。
长 ctx 候选（≥256K）：claude-opus-4.7-1m (1M) / gemini-2.5-pro (2M) / kimi-k2 (256K)`;
}

/**
 * v6.5.5：本轮 prompt 事前估算（在 LLM 调用之前，比 llm_output 累加器更早一步）。
 *
 * 输入信号（按可用性优先级）：
 *   1. event.prompt（before_prompt_build / before_model_resolve / llm_input 都有）
 *   2. event.systemPrompt（仅 llm_input 有）
 *   3. event.imagesCount / event.attachments（多模态附件）
 *   4. event.messages / event.historyMessages（已有的历史消息——通常已被 llm_output usage 算过，
 *      只有"刚拼装完未发出"这一窗口该补；保守不重复算）
 *
 * 估算规则：
 *   - 文本：4 chars/token（英文标准；中文实测 1.5-2 chars/token，所以这里偏保守=高估，
 *     宁可早预警也别迟）
 *   - 图片：每张 1500 token
 *   - 视频帧：每帧 1500 token（按 attachments[].frames 估）
 *   - 音频秒：每秒 100 token
 */
function estimatePromptTokens(event: any, modelHint?: string): number {
  const prompt = String(event?.prompt ?? "");
  const sys = String(event?.systemPrompt ?? "");
  const textChars = prompt.length + sys.length;
  let tokens = Math.ceil(textChars / 4);

  // v6.6.0 P1-6: 按 model 取图片 token 成本（gemini 800 / claude 1500 / gpt 1200）
  const modelId = modelHint ?? (event as any)?.model ?? (event as any)?.resolvedRef;
  const imagePerToken = resolveImageTokens(modelId);

  const imagesCount = Number(event?.imagesCount ?? 0);
  if (imagesCount > 0) tokens += imagesCount * imagePerToken;

  const attachments: Array<{ kind?: string; frames?: number; durationSec?: number }> =
    Array.isArray(event?.attachments) ? event.attachments : [];
  for (const att of attachments) {
    const kind = String(att?.kind ?? "").toLowerCase();
    if (kind.includes("image")) tokens += imagePerToken;
    else if (kind.includes("video")) {
      const frames = Number(att?.frames ?? 1);
      tokens += frames * TOKENS_PER_VIDEO_FRAME;
    } else if (kind.includes("audio")) {
      const sec = Number(att?.durationSec ?? 1);
      tokens += sec * TOKENS_PER_AUDIO_SECOND;
    }
  }
  return tokens;
}

/**
 * v6.5.5：从 long-ctx 候选清单选第一个非 banned 且 ctx ≥ 256K 的 model。
 * 跳过当前 model（避免"切到自己"），跳过已在 latency-tracker 黑名单的 model。
 *
 * 返 model 的 bare id（如 "kimi-k2"）；调用方自己拼 provider 前缀（OpenClaw runtime
 * 会把 modelOverride 转成 "<provider>/<model>"）。
 *
 * 如果所有候选都 banned 或 ctx 不够 → 返 null（调用方应降级到 banner 提示，让用户/compact）。
 */
/**
 * v6.6.4: 从 cfg 读已注册 providers（cfg.agents.defaults.models keys 取 split('/')[0]）。
 * 强切候选必须命中已注册 provider，避免选了用户没装的 model（claude/gemini 等）。
 */
function readInstalledProviders(cfg: unknown): Set<string> {
  const models = (cfg as { agents?: { defaults?: { models?: Record<string, unknown> } } })
    ?.agents?.defaults?.models;
  if (!models || typeof models !== "object") return new Set();
  const providers = new Set<string>();
  for (const key of Object.keys(models)) {
    const slash = key.indexOf("/");
    if (slash > 0) providers.add(key.slice(0, slash));
  }
  return providers;
}

/**
 * v6.6.7: 用户配置驱动的候选 model — 修 v6.6.x 强切硬编码 LONG_CTX_CANDIDATES 的设计错误。
 *
 * 用户截图明确指出："你应该看 openclaw.json 里面配置的几个模型，按照这个里面的配置切换"
 *
 * 之前问题：LONG_CTX_CANDIDATES_DEFAULT 硬编码 claude/gemini/kimi——用户机器上没装
 * 这些 provider（实际是 deepseek + minimax），三重过滤后返 null 不强切（v6.6.4 已修
 * 错切的 bug，但还是没真正切——浪费"P0-1 真实切换"的设计）。
 *
 * 新设计：从 cfg.agents.defaults.model.{primary, fallbacks} 读用户配置的 model 列表 →
 * cfg.models.providers[<provider>].models[<bareId>] join 拿 contextWindow + cost →
 * 按 ctx 降序（或 cost 升序）选第一个 ctx 比当前大的。
 */
export interface UserModelCandidate {
  fullId: string;       // "deepseek/DeepSeek-V4-Pro"
  bareId: string;       // "DeepSeek-V4-Pro"
  provider: string;     // "deepseek"
  contextWindow: number;
  costInPerM?: number;
  costOutPerM?: number;
}

function readUserAgentModels(cfg: unknown): UserModelCandidate[] {
  if (!cfg || typeof cfg !== "object") return [];
  const root = cfg as {
    agents?: { defaults?: { model?: { primary?: string; fallbacks?: unknown[] } } };
    models?: { providers?: Record<string, { models?: Array<{ id?: string; contextWindow?: number; cost?: { input?: number; output?: number } }> }> };
  };

  // 1. 拿用户配置的 model 列表（primary + fallbacks，按出现顺序去重）
  const modelSpec = root?.agents?.defaults?.model;
  if (!modelSpec) return [];
  const seen = new Set<string>();
  const fullIds: string[] = [];
  if (typeof modelSpec.primary === "string" && modelSpec.primary.trim()) {
    const id = modelSpec.primary.trim();
    seen.add(id);
    fullIds.push(id);
  }
  if (Array.isArray(modelSpec.fallbacks)) {
    for (const f of modelSpec.fallbacks) {
      if (typeof f === "string" && f.trim() && !seen.has(f.trim())) {
        seen.add(f.trim());
        fullIds.push(f.trim());
      }
    }
  }
  if (fullIds.length === 0) return [];

  // 2. 拿 providers 表（看每个 model 的真实 contextWindow + cost）
  const providers = root?.models?.providers ?? {};

  const out: UserModelCandidate[] = [];
  for (const fullId of fullIds) {
    const slash = fullId.indexOf("/");
    if (slash <= 0) continue;
    const provider = fullId.slice(0, slash);
    const bareId = fullId.slice(slash + 1);

    const providerSpec = providers[provider];
    if (!providerSpec || !Array.isArray(providerSpec.models)) {
      // provider 未注册 — 跳过（用户配置自相矛盾）
      continue;
    }
    const modelInfo = providerSpec.models.find((m) => m?.id === bareId);
    if (!modelInfo) continue;

    out.push({
      fullId,
      bareId,
      provider,
      contextWindow: typeof modelInfo.contextWindow === "number" ? modelInfo.contextWindow : 32_768,
      costInPerM: typeof modelInfo.cost?.input === "number" ? modelInfo.cost.input : undefined,
      costOutPerM: typeof modelInfo.cost?.output === "number" ? modelInfo.cost.output : undefined,
    });
  }
  return out;
}

/**
 * v6.6.7: 从用户配置中选 ctx 严格更大的 model 作强切 target。
 * 跳过：当前 model / ctx ≤ current.ctxMax（切去更小没意义）/ isModelBanned 命中。
 * 排序：默认 ctx 降序（最大优先），preferCheap=true 时改 costIn 升序。
 *
 * 返 null 时表示用户配置中没有比当前更大的 model — ctx-watchdog 不强切，
 * banner 提示用户主动 /compact（已经在 user fallback chain 里走到了最优）。
 */
function pickEscalateTargetFromUserConfig(
  current: { model?: string; ctxMax: number },
  candidates: UserModelCandidate[],
  preferCheap = false,
): UserModelCandidate | null {
  const excludeFullId = current.model;
  const excludeBareId = current.model?.includes("/") ? current.model.split("/").pop() : current.model;

  const available = candidates.filter((c) => {
    if (c.fullId === excludeFullId) return false;
    if (c.bareId === excludeBareId) return false;
    // 必须严格 > 当前 ctxMax（不切去同等大小或更小的）
    if (c.contextWindow <= current.ctxMax) return false;
    if (isModelBanned(c.fullId)) return false;
    if (isModelBanned(c.bareId)) return false;
    return true;
  });
  if (available.length === 0) return null;

  if (preferCheap) {
    available.sort((a, b) => (a.costInPerM ?? 999) - (b.costInPerM ?? 999));
  } else {
    available.sort((a, b) => b.contextWindow - a.contextWindow);
  }
  return available[0];
}

function pickLongCtxModel(
  candidates: string[],
  currentModel: string | undefined,
  installedProviders: Set<string>,
  options?: { preferCheap?: boolean },
): string | null {
  const exclude = currentModel?.includes("/") ? currentModel.split("/").pop() : currentModel;

  // 过滤可用候选
  const available = candidates.filter((c) => {
    if (c === exclude) return false;
    const ctxMax = KNOWN_MODEL_CTX_MAX[c] ?? 0;
    if (ctxMax < 256_000) return false;
    // v6.6.4: 必须是用户 cfg 已注册 provider（防止选了 claude/gemini 而用户没装该 provider）
    const provider = MODEL_TO_PROVIDER_MAP[c];
    if (!provider) return false; // 未知 provider 的 candidate 跳
    if (installedProviders.size > 0 && !installedProviders.has(provider)) return false;
    if (isModelBanned(c)) return false;
    if (isModelBanned(`${provider}/${c}`)) return false;
    return true;
  });

  if (available.length === 0) return null;

  // v6.6.0 P1-4: preferCheap=true 时按 cost.in 升序（月度预算紧时省钱）
  if (options?.preferCheap) {
    const sorted = [...available].sort((a, b) => {
      const costA = KNOWN_MODEL_COST[a]?.in ?? 999;
      const costB = KNOWN_MODEL_COST[b]?.in ?? 999;
      return costA - costB;
    });
    return sorted[0];
  }
  // 默认：按 longCtxCandidates 顺序（用户/默认按 quality 排）
  return available[0];
}

export function registerContextWatchdog(
  api: OpenClawPluginApi,
  config?: ContextWatchdogConfig,
) {
  if (config?.enabled === false) return;

  const hintAt = config?.hintAt ?? DEFAULT_HINT_AT;
  const warnAt = config?.warnAt ?? DEFAULT_WARN_AT;
  const criticalAt = config?.criticalAt ?? DEFAULT_CRITICAL_AT;
  const escalateAt = config?.escalateToLongCtxAt ?? DEFAULT_ESCALATE_AT;
  const forceEscalateAt = config?.forceEscalateAt ?? DEFAULT_FORCE_ESCALATE_AT;
  const longCtxCandidates =
    config?.longCtxCandidates && config.longCtxCandidates.length > 0
      ? config.longCtxCandidates
      : LONG_CTX_CANDIDATES_DEFAULT;
  const monthlyBudgetUSD = config?.monthlyBudgetUSD;
  const debug = config?.debug === true;

  /**
   * v6.6.0 P2-8: 按 channel 取阈值（覆盖全局；未覆盖的字段 fallback 全局）
   * 优先级：用户配置 thresholdsByChannel[ch] > 内置 CHANNEL_THRESHOLDS_DEFAULT[ch] > 全局
   */
  function resolveThresholds(channel: string): {
    hintAt: number;
    warnAt: number;
    criticalAt: number;
    escalateAt: number;
    forceEscalateAt: number;
  } {
    const userOverride = config?.thresholdsByChannel?.[channel];
    const builtin = CHANNEL_THRESHOLDS_DEFAULT[channel];
    const specific: ChannelThresholds = { ...builtin, ...userOverride };
    return {
      hintAt: specific.hintAt ?? hintAt,
      warnAt: specific.warnAt ?? warnAt,
      criticalAt: specific.criticalAt ?? criticalAt,
      escalateAt: specific.escalateToLongCtxAt ?? escalateAt,
      forceEscalateAt: specific.forceEscalateAt ?? forceEscalateAt,
    };
  }

  // v6.5.6: 会话级累加器（in-memory）+ dirty 集合（节流 flush 到 sqlite）+ peak 画像
  const sessions = new Map<string, SessionUsage>();
  const dirtySessionKeys = new Set<string>();
  const sessionPeakPercent = new Map<string, number>();
  let flushTimer: NodeJS.Timeout | null = null;
  const FLUSH_INTERVAL_MS = 10_000;

  function scheduleFlush() {
    if (flushTimer) return;
    flushTimer = setTimeout(() => {
      flushTimer = null;
      flushDirtySessions();
    }, FLUSH_INTERVAL_MS);
    flushTimer.unref?.();
  }

  function flushDirtySessions() {
    if (dirtySessionKeys.size === 0) return;
    let db;
    try {
      db = getDb();
    } catch {
      dirtySessionKeys.clear();
      return;
    }
    const rows: CtxUsageRow[] = [];
    for (const sk of dirtySessionKeys) {
      const s = sessions.get(sk);
      if (!s) continue;
      const used = s.totalTokens + s.pendingTokens;
      const percent = used / s.lastModelCtxMax;
      const peak = Math.max(sessionPeakPercent.get(sk) ?? 0, percent);
      sessionPeakPercent.set(sk, peak);
      rows.push({
        session_key: sk,
        agent_id: s.agentId,
        total_tokens: s.totalTokens,
        last_model: s.lastModel ?? null,
        last_model_ctx_max: s.lastModelCtxMax,
        original_model: s.originalModel ?? null,
        last_warned_threshold: s.lastWarnedThreshold,
        peak_percent: peak,
        estimated_cost_usd: s.estimatedCostUSD,
        last_updated_at: s.lastUpdatedAt,
        created_at: s.lastUpdatedAt,
      });
    }
    batchSaveCtxUsage(db, rows);
    if (debug) api.logger.info(`[ctx-watchdog] flushed ${rows.length} sessions to sqlite`);
    dirtySessionKeys.clear();
  }

  function markDirty(sessionKey: string) {
    dirtySessionKeys.add(sessionKey);
    scheduleFlush();
  }

  function getOrCreate(sessionKey: string, agentId: string, modelId?: string): SessionUsage {
    let s = sessions.get(sessionKey);
    if (!s) {
      // v6.5.6: lazy hydrate from sqlite（首次见到此 sessionKey 才查一次）
      let hydrated: SessionUsage | undefined;
      try {
        const db = getDb();
        const row = loadCtxUsage(db, sessionKey);
        if (row) {
          hydrated = {
            sessionKey,
            agentId: row.agent_id || agentId,
            totalTokens: row.total_tokens,
            pendingTokens: 0,
            lastModel: row.last_model ?? undefined,
            lastModelCtxMax: row.last_model_ctx_max || resolveCtxMax(modelId),
            originalModel: row.original_model ?? undefined,
            lastWarnedThreshold: row.last_warned_threshold,
            tokensPerTurnHistory: [], // hydrate 后从 0 重建（不持久化轮次历史避免 schema 复杂化）
            estimatedCostUSD: row.estimated_cost_usd ?? 0,
            seenRunIds: new Set(),
            lastUpdatedAt: row.last_updated_at,
          };
          sessionPeakPercent.set(sessionKey, row.peak_percent);
          if (debug) {
            api.logger.info(
              `[ctx-watchdog] hydrated from sqlite | session=${sessionKey.slice(0, 12)} | tokens=${row.total_tokens} | peak=${(row.peak_percent * 100).toFixed(1)}%`,
            );
          }
        }
      } catch {
        /* sqlite 不可用，跳过 hydrate */
      }

      // LRU eviction（不删 sqlite 行，保留作画像）
      if (sessions.size >= MAX_TRACKED_SESSIONS) {
        const oldest = [...sessions.entries()].sort((a, b) => a[1].lastUpdatedAt - b[1].lastUpdatedAt)[0];
        if (oldest) {
          dirtySessionKeys.add(oldest[0]);
          flushDirtySessions();
          sessions.delete(oldest[0]);
        }
      }
      s = hydrated ?? {
        sessionKey,
        agentId,
        totalTokens: 0,
        pendingTokens: 0,
        lastModelCtxMax: resolveCtxMax(modelId),
        lastWarnedThreshold: 0,
        tokensPerTurnHistory: [],
        estimatedCostUSD: 0,
        seenRunIds: new Set(),
        lastUpdatedAt: Date.now(),
      };
      sessions.set(sessionKey, s);
    }
    if (modelId && modelId !== s.lastModel) {
      s.lastModel = modelId;
      s.lastModelCtxMax = resolveCtxMax(modelId);
    }
    return s;
  }

  /** 当前评估用的"有效 token 数"= 真实累加 + 本轮事前估算（pending） */
  function effectiveTokens(s: SessionUsage): number {
    return s.totalTokens + s.pendingTokens;
  }

  // v6.5.6 P1-5: 会话级"建议切回原模型" 标记
  const revertSuggestPending = new Map<string, string>();

  // v6.6.6 hotfix: 所有 hook 包 try/catch — 防御性「不影响主流程」
  // 触发原因：用户实测 v6.6.5 升级后『麻将观战可行性报告』仍撞 "Something went wrong"，
  // 说明某个 enhance hook 在 edge case 抛了 unhandled exception → OpenClaw 报通用错误页。
  // 修法：每个 hook handler 顶层包 try/catch，错误 log + return undefined，不影响主流程。
  const safeHook = <T>(hookName: string, body: () => T | undefined): T | undefined => {
    try {
      return body();
    } catch (err) {
      api.logger.error(
        `[ctx-watchdog] ${hookName} hook 异常已捕获（不影响主流程）: ${(err as Error)?.message ?? err}`,
      );
      return undefined;
    }
  };

  // ── hook 1: llm_output 累加 token usage（事后真实值）──
  api.on("llm_output", (event, ctx) => safeHook("llm_output", () => {
    const sessionKey = pickSessionKey(ctx);
    if (!sessionKey) return;
    const agentId = pickAgentId(ctx);
    const modelId = (event as any)?.resolvedRef ?? (event as any)?.model;
    const usageDelta = sumUsage((event as any)?.usage);
    const runId = String((event as any)?.runId ?? "").trim();

    const s = getOrCreate(sessionKey, agentId, modelId);

    // v6.6.1 P3-13: runId 去重防 retry 重复累加
    if (runId) {
      if (s.seenRunIds.has(runId)) {
        if (debug) {
          api.logger.info(
            `[ctx-watchdog] retry detected runId=${runId} | session=${sessionKey.slice(0, 12)} — skipping (dedup)`,
          );
        }
        return;
      }
      s.seenRunIds.add(runId);
      if (s.seenRunIds.size > SEEN_RUNIDS_LIMIT) {
        const first = s.seenRunIds.values().next().value;
        if (first !== undefined) s.seenRunIds.delete(first);
      }
    }

    s.pendingTokens = 0;
    if (usageDelta <= 0) {
      if (debug) {
        api.logger.info(
          `[ctx-watchdog] llm_output 没拿到 usage（provider 没报）| session=${sessionKey.slice(0, 12)} | model=${modelId}`,
        );
      }
      return;
    }

    s.totalTokens += usageDelta;
    s.lastUpdatedAt = Date.now();
    s.tokensPerTurnHistory.push(usageDelta);
    if (s.tokensPerTurnHistory.length > PREDICTION_HISTORY_LEN) {
      s.tokensPerTurnHistory.shift();
    }
    const turnCost = estimateTurnCostUSD(modelId, (event as any)?.usage);
    if (turnCost > 0) {
      s.estimatedCostUSD += turnCost;
    }
    markDirty(sessionKey);

    if (debug) {
      const pct = Math.round((s.totalTokens / s.lastModelCtxMax) * 100);
      api.logger.info(
        `[ctx-watchdog] +${usageDelta.toLocaleString()} → ${s.totalTokens.toLocaleString()}/${s.lastModelCtxMax.toLocaleString()} (${pct}%) | session=${sessionKey.slice(0, 12)} | model=${modelId}`,
      );
    }
  }));

  // ── hook 1b: llm_input 累加事前估算（v6.5.5 P0-2）──
  // 比 before_model_resolve / before_prompt_build 信息更全（含 systemPrompt + historyMessages + imagesCount），
  // 但顺序在 before_model_resolve 之后——所以 before_model_resolve 自己也要 estimate 一次（用 event.prompt）。
  api.on("llm_input", (event, ctx) => safeHook("llm_input", () => {
    const sessionKey = pickSessionKey(ctx);
    if (!sessionKey) return;
    const agentId = pickAgentId(ctx);
    const modelId = (event as any)?.model;
    const s = getOrCreate(sessionKey, agentId, modelId);
    const est = estimatePromptTokens(event, modelId);
    s.pendingTokens = est;
    s.lastUpdatedAt = Date.now();
    if (debug) {
      api.logger.info(
        `[ctx-watchdog] llm_input estimate=${est.toLocaleString()} | session=${sessionKey.slice(0, 12)}`,
      );
    }
  }));

  // ── hook 1c: subagent_spawned / subagent_ended（v6.5.7 P1-7）──
  // 解决 subagent token 累加盲区：child agent 调 LLM 的 token 走 child sessionKey，
  // main agent 看 ctx 用量永远是"自己的部分"，但实际后端 ctx 已经被 child 吃掉一截。
  // 修法：spawn 时记 child→parent 映射，end 时把 child.totalTokens 加到 parent。
  const childToParent = new Map<string, string>();
  const MAX_SUBAGENT_LINKS = 500;

  api.on("subagent_spawned", (event, ctx) => safeHook("subagent_spawned", () => {
    const childKey = (event as any)?.childSessionKey ?? (ctx as any)?.childSessionKey;
    const parentKey = (ctx as any)?.requesterSessionKey;
    if (!childKey || !parentKey || childKey === parentKey) return;
    if (childToParent.size >= MAX_SUBAGENT_LINKS) {
      const oldest = childToParent.keys().next().value;
      if (oldest) childToParent.delete(oldest);
    }
    childToParent.set(childKey, parentKey);
    if (debug) {
      api.logger.info(
        `[ctx-watchdog] subagent linked: child=${childKey.slice(0, 12)} → parent=${parentKey.slice(0, 12)}`,
      );
    }
  }));

  api.on("subagent_ended", (event, ctx) => safeHook("subagent_ended", () => {
    const childKey =
      (event as any)?.targetSessionKey ??
      (ctx as any)?.childSessionKey ??
      "";
    if (!childKey) return;
    const parentKey = childToParent.get(childKey) ?? (ctx as any)?.requesterSessionKey;
    if (!parentKey || parentKey === childKey) return;

    const child = sessions.get(childKey);
    if (!child || child.totalTokens <= 0) {
      childToParent.delete(childKey);
      return;
    }
    const parent = sessions.get(parentKey);
    if (!parent) {
      childToParent.delete(childKey);
      return;
    }
    parent.totalTokens += child.totalTokens;
    parent.lastUpdatedAt = Date.now();
    markDirty(parentKey);
    api.logger.info(
      `[ctx-watchdog] subagent rolled up: child=${childKey.slice(0, 12)} (+${child.totalTokens.toLocaleString()}) → parent=${parentKey.slice(0, 12)} | parent total=${parent.totalTokens.toLocaleString()}`,
    );
    childToParent.delete(childKey);
  }));

  // ── hook 2: after_compaction 重置（龙虾刚 compact 完，token 大幅下降）──
  // openclaw 2026.4.x dist 实际 emit after_compaction 但 SDK 类型 union 可能落后；
  // 跟 model_call_ended 一样用 cast 绕过类型检查
  // v6.5.6: 加 P1-5 切回原模型逻辑 + dirty 标记
  (api.on as any)("after_compaction", (_event: any, ctx: any) => safeHook("after_compaction", () => {
    const sessionKey = pickSessionKey(ctx);
    if (!sessionKey) return;
    const s = sessions.get(sessionKey);
    if (!s) return;
    const before = s.totalTokens;
    s.totalTokens = Math.round(s.totalTokens * 0.3);
    s.lastWarnedThreshold = 0;
    s.lastUpdatedAt = Date.now();
    markDirty(sessionKey);

    const afterPercent = s.totalTokens / s.lastModelCtxMax;
    if (s.originalModel && s.lastModel !== s.originalModel) {
      const originalCtxMax = resolveCtxMax(s.originalModel);
      const projectedInOriginal = s.totalTokens / originalCtxMax;
      if (projectedInOriginal < 0.6) {
        revertSuggestPending.set(sessionKey, s.originalModel);
        if (debug) {
          api.logger.info(
            `[ctx-watchdog] revert hint queued: ${s.lastModel} → ${s.originalModel} | session=${sessionKey.slice(0, 12)} | projectedInOriginal=${Math.round(projectedInOriginal * 100)}%`,
          );
        }
      }
    }

    if (debug) {
      api.logger.info(
        `[ctx-watchdog] after_compaction: ${before.toLocaleString()} → ${s.totalTokens.toLocaleString()} (${Math.round(afterPercent * 100)}%) | session=${sessionKey.slice(0, 12)}`,
      );
    }
  }));

  /**
   * v6.5.7 P2-9: 预测式提醒。
   * 当用量未到 warnAt 但按当前速率 PREDICTION_LOOKAHEAD_TURNS 轮内会撞 warnAt → 提早注 banner
   * 防抖：同一 session 同一目标阈值只警告一次（predictionEmittedFor）
   */
  function evalPredictionBanner(s: SessionUsage, event: any, ctx: any): string | null {
    if (s.tokensPerTurnHistory.length < 2) return null;
    const liveEstimate = s.pendingTokens > 0
      ? s.pendingTokens
      : estimatePromptTokens(event, s.lastModel);
    const used = s.totalTokens + liveEstimate;
    const percent = used / s.lastModelCtxMax;

    // v6.6.0 P2-8: channel-aware warnAt
    const channel = resolveChannel(ctx);
    const T = resolveThresholds(channel);
    if (percent >= T.warnAt) return null;

    const avgPerTurn = s.tokensPerTurnHistory.reduce((a, b) => a + b, 0) / s.tokensPerTurnHistory.length;
    if (avgPerTurn <= 0) return null;

    const warnTarget = T.warnAt * s.lastModelCtxMax;
    const turnsToWarn = Math.ceil((warnTarget - used) / avgPerTurn);
    if (turnsToWarn > PREDICTION_LOOKAHEAD_TURNS) return null;
    if (turnsToWarn <= 0) return null;

    if (s.predictionEmittedFor === Math.round(T.warnAt * 100)) return null;
    s.predictionEmittedFor = Math.round(T.warnAt * 100);
    markDirty(s.sessionKey);

    const pctNow = Math.round(percent * 100);
    const pctWarn = Math.round(T.warnAt * 100);
    const avgK = Math.round(avgPerTurn / 1000);
    api.logger.info(
      `[ctx-watchdog] prediction (channel=${channel}) | session=${s.sessionKey.slice(0, 12)} | now=${pctNow}% → ${pctWarn}% in ~${turnsToWarn} turns (avgPerTurn=${avgK}k)`,
    );
    return `【上下文用量趋势预警 - channel=${channel}】当前 ${pctNow}%，按最近 ${s.tokensPerTurnHistory.length} 轮平均每轮 +${avgK}k token 速率，预计 **~${turnsToWarn} 轮内**撞 ${pctWarn}%（${channel} 阈值）。建议：现在就在合适节点收尾或主动 /compact。`;
  }

  /** v6.5.6+v6.6.0: 阈值评估 + banner 构造（按 channel 取差异化阈值） */
  function evalThresholdBanner(s: SessionUsage, event: any, ctx: any): string | null {
    const liveEstimate = s.pendingTokens > 0
      ? s.pendingTokens
      : estimatePromptTokens(event, s.lastModel);
    const used = s.totalTokens + liveEstimate;
    if (used === 0) return null;

    const percent = used / s.lastModelCtxMax;
    const modelId = s.lastModel ?? "<unknown>";

    // v6.6.0 P2-8: 按 channel 取阈值
    const channel = resolveChannel(ctx);
    const T = resolveThresholds(channel);

    let triggeredThreshold = 0;
    let banner = "";
    if (percent >= T.criticalAt) {
      triggeredThreshold = T.criticalAt;
      banner = buildCriticalBanner(percent, used, s.lastModelCtxMax, modelId);
    } else if (percent >= T.warnAt) {
      triggeredThreshold = T.warnAt;
      banner = buildWarnBanner(percent, used, s.lastModelCtxMax, modelId);
    } else if (percent >= T.hintAt) {
      triggeredThreshold = T.hintAt;
      banner = buildHintBanner(percent, used, s.lastModelCtxMax, modelId);
    } else {
      return null;
    }

    if (s.lastWarnedThreshold >= triggeredThreshold) return null;
    s.lastWarnedThreshold = triggeredThreshold;
    s.predictionEmittedFor = undefined;
    markDirty(s.sessionKey);

    let final = banner;
    if (percent >= T.escalateAt && s.lastModelCtxMax < 256_000) {
      final = banner + "\n\n" + buildEscalateHint(modelId, s.lastModelCtxMax, used, percent);
    }

    // v6.6.0 P1-4: 预算告警附加
    if (monthlyBudgetUSD && monthlyBudgetUSD > 0 && s.estimatedCostUSD > 0) {
      const budgetUsage = s.estimatedCostUSD / monthlyBudgetUSD;
      if (budgetUsage >= 0.8 && s.budgetWarnedAt !== Math.round(budgetUsage * 100)) {
        s.budgetWarnedAt = Math.round(budgetUsage * 100);
        final += `\n\n【💰 预算告警】本会话已消耗 $${s.estimatedCostUSD.toFixed(3)}（月度预算 $${monthlyBudgetUSD.toFixed(2)} 的 ${Math.round(budgetUsage * 100)}%）。escalate 时优先选低成本 long-ctx 候选。`;
      }
    }

    api.logger.info(
      `[ctx-watchdog] threshold=${Math.round(triggeredThreshold * 100)}% (channel=${channel}) triggered | session=${s.sessionKey.slice(0, 12)} | usage=${used}/${s.lastModelCtxMax}`,
    );
    return final;
  }

  // ── hook 3: before_prompt_build 注入预警 banner（v6.5.6 含 revert hint 消费）──
  api.on("before_prompt_build", (event, ctx) => safeHook("before_prompt_build", () => {
    const sessionKey = pickSessionKey(ctx);
    if (!sessionKey) return undefined;
    const s = sessions.get(sessionKey);
    if (!s) return undefined;

    if (s.mutedUntilMs && Date.now() < s.mutedUntilMs) {
      return undefined;
    }
    if (s.mutedUntilMs && Date.now() >= s.mutedUntilMs) {
      s.mutedUntilMs = undefined;
    }

    const revertTarget = revertSuggestPending.get(sessionKey);
    if (revertTarget) {
      revertSuggestPending.delete(sessionKey);
      const originalCtxMax = resolveCtxMax(revertTarget);
      const revertBanner = `【建议切回原模型】会话已通过 /compact 降低用量，可调 \`enhance_route_revert_to_original\` 工具切回 ${revertTarget}（ctx ${originalCtxMax.toLocaleString()}）以节省成本。当前正用 ${s.lastModel ?? "<unknown>"}（ctx ${s.lastModelCtxMax.toLocaleString()}）。`;
      api.logger.info(
        `[ctx-watchdog] revert hint emitted | session=${sessionKey.slice(0, 12)} | suggest=${revertTarget}`,
      );
      const thresholdBanner = evalThresholdBanner(s, event, ctx);
      const final = thresholdBanner ? revertBanner + "\n\n" + thresholdBanner : revertBanner;
      return { prependContext: final };
    }

    const thresholdBanner = evalThresholdBanner(s, event, ctx);
    if (thresholdBanner) return { prependContext: thresholdBanner };

    const predictionBanner = evalPredictionBanner(s, event, ctx);
    if (predictionBanner) return { prependContext: predictionBanner };

    return undefined;
  }));

  // ── hook 4: before_model_resolve 强切到 long-ctx model（v6.5.5 P0-1）──
  // priority=100 比 model-router（默认 0）高，让 ctx-watchdog 先跑。
  // OpenClaw mergeBeforeModelResolve 用 firstDefined：高 priority 返的 modelOverride 赢，
  // 即使 model-router 后跑也返 modelOverride，firstDefined 保留 ctx-watchdog 的。
  api.on(
    "before_model_resolve",
    (event, ctx) => safeHook("before_model_resolve", () => {
      const sessionKey = pickSessionKey(ctx);
      if (!sessionKey) return undefined;
      const s = sessions.get(sessionKey);
      if (!s) return undefined;

      const liveEstimate = estimatePromptTokens(event, s.lastModel);
      const projected = s.totalTokens + liveEstimate;
      const percent = projected / s.lastModelCtxMax;

      const channel = resolveChannel(ctx);
      const T = resolveThresholds(channel);

      if (percent < T.forceEscalateAt) return undefined;
      // v6.6.7: 不再硬截"已是 long ctx (≥256K) 就不切"——用户机器实际 ctx 范围 128-200K，
      // 只要找到比当前更大的就有意义切（minimax 200K > deepseek 128K 也值得切）

      const budgetTight =
        monthlyBudgetUSD !== undefined &&
        monthlyBudgetUSD > 0 &&
        s.estimatedCostUSD > monthlyBudgetUSD * 0.8;

      // v6.6.7: 优先从用户配置 (cfg.agents.defaults.model.{primary,fallbacks}) 选 ctx 更大的
      // 用户截图配置：primary=deepseek/DeepSeek-V4-Pro + fallbacks=[minimax/MiniMax-M2.7, deepseek/DeepSeek-V4-Flash]
      // 当前 deepseek-v4-pro 128K 撞 95% → 切到 minimax-m2.7 200K（用户实际装的）
      let cfg: unknown;
      try {
        cfg = api.runtime?.config?.loadConfig?.();
      } catch (err) {
        api.logger.warn(`[ctx-watchdog] loadConfig 失败（忽略，退回硬编码 fallback）: ${(err as Error)?.message}`);
      }
      const userCandidates = readUserAgentModels(cfg);

      if (userCandidates.length > 0) {
        const target = pickEscalateTargetFromUserConfig(
          { model: s.lastModel, ctxMax: s.lastModelCtxMax },
          userCandidates,
          budgetTight,
        );
        if (target) {
          if (!s.originalModel) s.originalModel = s.lastModel;
          const fromModel = s.lastModel ?? "<unknown>";
          api.logger.warn(
            `[ctx-watchdog] FORCE-escalate (user-config): ${fromModel} (${s.lastModelCtxMax}) → ${target.fullId} (${target.contextWindow}) | session=${sessionKey.slice(0, 12)} | percent=${Math.round(percent * 100)}% | channel=${channel} | budgetTight=${budgetTight}`,
          );
          return {
            modelOverride: target.fullId,
            providerOverride: target.provider,
          };
        }
        // 用户配置里没有更大的 model — banner 提示已在 prompt build 出过，这里不再强切
        api.logger.info(
          `[ctx-watchdog] FORCE-escalate skipped: user-config 中没有 ctx > ${s.lastModelCtxMax} 的可用 model（已是 fallback chain 最大）| session=${sessionKey.slice(0, 12)} | candidates=[${userCandidates.map((c) => `${c.bareId}(${c.contextWindow})`).join(',')}]`,
        );
        return undefined;
      }

      // 用户配置完全没读到（极端兜底）→ 退回 v6.6.4 硬编码 LONG_CTX_CANDIDATES 路径
      if (s.lastModelCtxMax >= 256_000) return undefined; // 硬编码路径才保留此截断
      let installedProviders: Set<string> = new Set();
      try {
        installedProviders = readInstalledProviders(cfg);
      } catch (err) {
        api.logger.warn(`[ctx-watchdog] readInstalledProviders 失败（忽略，退回默认）: ${(err as Error)?.message}`);
      }
      const target = pickLongCtxModel(longCtxCandidates, s.lastModel, installedProviders, { preferCheap: budgetTight });
      if (!target) {
        api.logger.warn(
          `[ctx-watchdog] FORCE-escalate skipped: 无 user-config 且 hardcoded 候选不可用 | session=${sessionKey.slice(0, 12)} | percent=${Math.round(percent * 100)}%`,
        );
        return undefined;
      }
      if (!s.originalModel) s.originalModel = s.lastModel;
      const fromModel = s.lastModel ?? "<unknown>";
      const targetProvider = MODEL_TO_PROVIDER_MAP[target];
      const targetFullId = targetProvider ? `${targetProvider}/${target}` : target;
      api.logger.warn(
        `[ctx-watchdog] FORCE-escalate (hardcoded fallback): ${fromModel} → ${targetFullId} | session=${sessionKey.slice(0, 12)} | percent=${Math.round(percent * 100)}% | channel=${channel}`,
      );
      return targetProvider
        ? { modelOverride: targetFullId, providerOverride: targetProvider }
        : { modelOverride: target };
    }),
    { priority: HOOK_PRIORITY_FORCE_ESCALATE },
  );

  // ── prompt supplement: 让 LLM 知道两个核心工具 ──
  api.registerMemoryPromptSupplement(() => {
    return [
      `【上下文用量】enhance_ctx_status 查当前会话 token 累计与百分比；用量 ≥80% 时调 enhance_route_to_long_ctx 立即切大 ctx 模型（≥256K）。70/85/95% 三阶 banner 自动提醒；95% 时 ctx-watchdog 在 before_model_resolve 强制切走（绕开 LLM）。`,
    ];
  });

  // ── tool 1: enhance_ctx_status 让 LLM 主动查 ──
  api.registerTool(
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_ctx_status",
      description: "查询当前会话的上下文 token 用量、距离 ctx 上限百分比与建议",
      inputSchema: Type.Object({}),
      async execute() {
        const sessionKey = pickSessionKey(ctx);
        if (!sessionKey) {
          return { ok: false, reason: "no session key in ctx" };
        }
        const s = sessions.get(sessionKey);
        const used = s ? effectiveTokens(s) : 0;
        if (!s || used === 0) {
          return {
            ok: true,
            sessionKey: sessionKey.slice(0, 16) + "…",
            tokensUsed: 0,
            ctxMax: s?.lastModelCtxMax ?? DEFAULT_CTX_MAX,
            percent: 0,
            severity: "fresh",
            recommendation: "会话刚开始或未捕获到 llm_output usage（可能模型没返 usage 字段）",
          };
        }
        const percent = used / s.lastModelCtxMax;
        const pctRound = Math.round(percent * 100);
        let severity: "ok" | "hint" | "warn" | "critical";
        let recommendation: string;
        if (percent >= criticalAt) {
          severity = "critical";
          recommendation = "🚨 立即停止新任务，先 /compact 或调 enhance_route_to_long_ctx 切大 ctx 模型";
        } else if (percent >= warnAt) {
          severity = "warn";
          recommendation = "⚠️ 强烈建议调 enhance_route_to_long_ctx 切大 ctx 模型，或 /compact";
        } else if (percent >= hintAt) {
          severity = "hint";
          recommendation = "💡 建议在合适 checkpoint /compact，或继续注意累积";
        } else {
          severity = "ok";
          recommendation = "上下文用量健康，继续即可";
        }
        const channel = resolveChannel(ctx);
        const T = resolveThresholds(channel);
        let cfg2: unknown;
        try { cfg2 = api.runtime?.config?.loadConfig?.(); } catch { /* ignore */ }
        const userCandidates = readUserAgentModels(cfg2);
        // v6.6.7: 优先从用户配置中找比当前 ctx 更大的
        const userTarget = pickEscalateTargetFromUserConfig(
          { model: s.lastModel, ctxMax: s.lastModelCtxMax },
          userCandidates,
        );
        const availableLongCtx = userTarget?.fullId ?? null;
        return {
          ok: true,
          sessionKey: sessionKey.slice(0, 16) + "…",
          model: s.lastModel,
          originalModel: s.originalModel,
          tokensUsed: s.totalTokens,
          tokensPending: s.pendingTokens,
          tokensEffective: used,
          ctxMax: s.lastModelCtxMax,
          percent: pctRound,
          severity,
          recommendation,
          shouldEscalate: percent >= T.escalateAt && !!userTarget,
          // v6.6.7: 暴露用户配置候选 + 当前会被强切的 target
          availableLongCtxModel: availableLongCtx,
          userConfigCandidates: userCandidates.map((c) => ({
            fullId: c.fullId,
            ctxMax: c.contextWindow,
            costInPerM: c.costInPerM,
          })),
          // v6.6.0 新字段
          channel,
          channelThresholds: { hint: T.hintAt, warn: T.warnAt, critical: T.criticalAt, escalate: T.escalateAt, force: T.forceEscalateAt },
          estimatedCostUSD: Math.round(s.estimatedCostUSD * 10000) / 10000,
          monthlyBudgetUSD: monthlyBudgetUSD,
          budgetUsedPercent: monthlyBudgetUSD
            ? Math.round((s.estimatedCostUSD / monthlyBudgetUSD) * 100)
            : undefined,
          avgTokensPerTurn: s.tokensPerTurnHistory.length > 0
            ? Math.round(s.tokensPerTurnHistory.reduce((a, b) => a + b, 0) / s.tokensPerTurnHistory.length)
            : undefined,
          // v6.6.1 新字段
          mutedUntilMs: s.mutedUntilMs && Date.now() < s.mutedUntilMs ? s.mutedUntilMs : undefined,
          seenRunIdsCount: s.seenRunIds.size,
        };
      },
    }) as any,
    { tier: "tools" } as any,
  );

  // ── tool 2: enhance_route_to_long_ctx（v6.5.5 P0-1）让 LLM ≥80% 时主动调 ──
  // 实际"切"由 ctx-watchdog 自己的 before_model_resolve hook 接管：
  //   - 调本工具会立刻把 sessions[].lastModel 标到目标 long-ctx，并把 lastWarnedThreshold 重置
  //     （让 banner 不再喷同阈值），但**本轮 LLM 调用已经发出了**——LLM 收到工具返回后，
  //     **下一轮** LLM 调用 ctx-watchdog 会在 before_model_resolve 直接返 modelOverride 切到 target
  //   - 如果当前 percent 已 ≥ forceEscalateAt，本工具就是冗余路径——hook 会自动接管；本工具兜底
  //     给 LLM 一个"我已经主动决定切了"的明确入口
  api.registerTool(
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_route_to_long_ctx",
      description: "立即切到更大 ctx 的 model（从 openclaw.json agents.defaults.model.{primary,fallbacks} 中选 ctx 比当前更大的）。当 enhance_ctx_status 显示 percent>=80 时主动调；返目标 model fullId + 原 model 备份；下一轮 LLM 调用 ctx-watchdog 会强制路由过去（不需要再调 enhance_route_set 持久化）",
      inputSchema: Type.Object({
        reason: Type.Optional(Type.String({ description: "切换原因（如 'ctx 已 85%' / '用户主动要求'）" })),
        target: Type.Optional(Type.String({ description: "目标 model fullId（如 'minimax/MiniMax-M2.7'）；不填则从用户 openclaw.json primary+fallbacks 中按 ctx 降序选第一个比当前大的" })),
      }),
      async execute(params: any) {
        const sessionKey = pickSessionKey(ctx);
        if (!sessionKey) {
          return { ok: false, reason: "no session key in ctx" };
        }
        const s = sessions.get(sessionKey);
        if (!s) {
          return { ok: false, reason: "session 还没开始累加 usage（llm_output 没 fire 过），无法切换" };
        }

        // v6.6.7: 优先用用户 openclaw.json 配置的 model 列表
        let cfg: unknown;
        try {
          cfg = api.runtime?.config?.loadConfig?.();
        } catch {
          // ignore — fallback 到硬编码
        }
        const userCandidates = readUserAgentModels(cfg);

        // 用户指定 target → 验证后用
        let targetFullId: string | null = null;
        let targetProvider: string | null = null;
        let targetCtxMax: number | null = null;

        if (params?.target && typeof params.target === "string") {
          const requested = params.target.trim();
          // 优先从 user-config 中匹配（fullId 完全相等或 bareId 相等）
          const match = userCandidates.find(
            (c) => c.fullId === requested || c.bareId === requested,
          );
          if (match) {
            if (isModelBanned(match.fullId) || isModelBanned(match.bareId)) {
              return { ok: false, reason: `${match.fullId} 当前被 latency-tracker ban`, hint: "等解禁或选别的" };
            }
            if (match.contextWindow <= s.lastModelCtxMax) {
              return {
                ok: false,
                reason: `${match.fullId} ctx=${match.contextWindow} 不大于当前 ${s.lastModelCtxMax}，切了等于没切`,
                hint: "选 ctx 更大的 model",
              };
            }
            targetFullId = match.fullId;
            targetProvider = match.provider;
            targetCtxMax = match.contextWindow;
          } else {
            return {
              ok: false,
              reason: `指定的 ${requested} 不在 openclaw.json agents.defaults.model.{primary,fallbacks} 注册`,
              hint: `用户配置 candidates: [${userCandidates.map((c) => c.fullId).join(', ')}]`,
            };
          }
        } else if (userCandidates.length > 0) {
          // 自动从用户配置选 ctx 最大的（不大于当前的会被过滤掉）
          const auto = pickEscalateTargetFromUserConfig(
            { model: s.lastModel, ctxMax: s.lastModelCtxMax },
            userCandidates,
          );
          if (auto) {
            targetFullId = auto.fullId;
            targetProvider = auto.provider;
            targetCtxMax = auto.contextWindow;
          }
        }

        // 用户配置完全没读到 → 退回硬编码 fallback（极端兜底）
        if (!targetFullId) {
          const installedProviders = readInstalledProviders(cfg);
          const fallbackBare = pickLongCtxModel(longCtxCandidates, s.lastModel, installedProviders);
          if (fallbackBare) {
            const fbProvider = MODEL_TO_PROVIDER_MAP[fallbackBare];
            targetFullId = fbProvider ? `${fbProvider}/${fallbackBare}` : fallbackBare;
            targetProvider = fbProvider ?? null;
            targetCtxMax = KNOWN_MODEL_CTX_MAX[fallbackBare] ?? null;
          }
        }

        if (!targetFullId) {
          return {
            ok: false,
            reason: userCandidates.length > 0
              ? `用户配置中没有 ctx > ${s.lastModelCtxMax} 的可用 model（已是 fallback chain 最大）`
              : "openclaw.json 未读到任何 model 配置且硬编码 fallback 也不可用",
            hint: "建议立即 /compact 或告知用户开新会话续接",
            userConfigCandidates: userCandidates.map((c) => ({
              fullId: c.fullId,
              ctxMax: c.contextWindow,
            })),
          };
        }

        // 记 originalModel（首次切才记）
        if (!s.originalModel) s.originalModel = s.lastModel;
        const fromModel = s.lastModel;
        s.lastWarnedThreshold = 0;
        const used = effectiveTokens(s);
        const percent = Math.round((used / s.lastModelCtxMax) * 100);
        api.logger.warn(
          `[ctx-watchdog] LLM-triggered escalate: ${fromModel} (${s.lastModelCtxMax}) → ${targetFullId} (${targetCtxMax}) | reason="${params?.reason ?? '-'}" | session=${sessionKey.slice(0, 12)} | percent=${percent}%`,
        );
        return {
          ok: true,
          from: fromModel,
          to: targetFullId,
          newCtxMax: targetCtxMax ?? DEFAULT_CTX_MAX,
          provider: targetProvider,
          currentPercent: percent,
          reason: params?.reason ?? "no reason given",
          message: `已切到 ${targetFullId}（ctx ${(targetCtxMax ?? DEFAULT_CTX_MAX).toLocaleString()}）。**下一轮** LLM 调用 ctx-watchdog 会在 before_model_resolve 强制路由过去；当 ctx 降下来后 model-router 重新评估自动选回最优。`,
          note: fromModel ? `已记录 originalModel=${s.originalModel}，将来 ctx 降到 60% 以下后会建议切回` : undefined,
        };
      },
    }) as any,
    { tier: "tools" } as any,
  );

  // ── tool 3: enhance_route_revert_to_original（v6.5.6 P1-5）切回原模型，省成本 ──
  api.registerTool(
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_route_revert_to_original",
      description: "切回原模型（compact 后 ctx 降下来时省成本用）。本工具清掉 ctx-watchdog 的强切意愿，让 model-router 重新走任务路由自然回到原 tier。仅在 enhance_ctx_status 显示 originalModel 不等于 model 且 percent<60% 时调",
      inputSchema: Type.Object({
        reason: Type.Optional(Type.String({ description: "切回原因（如 'compact 后 ctx 降到 40%'）" })),
      }),
      async execute(params: any) {
        const sessionKey = pickSessionKey(ctx);
        if (!sessionKey) return { ok: false, reason: "no session key in ctx" };
        const s = sessions.get(sessionKey);
        if (!s) return { ok: false, reason: "session 没在追踪" };
        if (!s.originalModel) {
          return { ok: false, reason: "本会话没切过模型（originalModel 为空），无需 revert" };
        }
        if (s.lastModel === s.originalModel) {
          return { ok: false, reason: `当前已是 originalModel=${s.originalModel}，无需 revert` };
        }
        const used = effectiveTokens(s);
        const originalCtxMax = resolveCtxMax(s.originalModel);
        const projectedPercent = used / originalCtxMax;
        if (projectedPercent >= 0.7) {
          return {
            ok: false,
            reason: `切回 ${s.originalModel} 后 percent=${Math.round(projectedPercent * 100)}% 仍超过 70%，不建议 revert`,
            hint: "继续用 long-ctx 模型或先 /compact 再考虑",
          };
        }
        const fromModel = s.lastModel;
        const targetModel = s.originalModel;
        s.originalModel = undefined;
        s.lastWarnedThreshold = 0;
        markDirty(sessionKey);
        api.logger.warn(
          `[ctx-watchdog] revert to original: ${fromModel} → ${targetModel} | reason="${params?.reason ?? '-'}" | session=${sessionKey.slice(0, 12)} | projectedPercent=${Math.round(projectedPercent * 100)}%`,
        );
        return {
          ok: true,
          from: fromModel,
          to: targetModel,
          newCtxMax: originalCtxMax,
          projectedPercent: Math.round(projectedPercent * 100),
          reason: params?.reason ?? "no reason given",
          message: `已清掉 ctx-watchdog 的强切意愿，下一轮 model-router 会重新走任务路由——预期切回到 ${targetModel} 或同 tier 最优。`,
        };
      },
    }) as any,
    { tier: "tools" } as any,
  );

  // ── tool 4: enhance_ctx_profile（v6.5.6 P0-3）查 agent 历史 ctx 画像 ──
  api.registerTool(
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_ctx_profile",
      description: "查询当前 agent 的历史会话 ctx 用量画像（peak / avg / sessions count）。基于 sqlite 持久化的 peak_percent，可用于了解'我这个 agent 平均会涨多高'",
      inputSchema: Type.Object({
        agentId: Type.Optional(Type.String({ description: "可选；默认取当前 ctx 的 agentId" })),
      }),
      async execute(params: any) {
        const targetAgentId = params?.agentId?.trim() || pickAgentId(ctx);
        try {
          const db = getDb();
          const profile = getAgentCtxProfile(db, targetAgentId);
          const monthly = getMonthlyCostEstimate(db, targetAgentId);
          return {
            ok: true,
            agentId: targetAgentId,
            sessions: profile.sessions,
            avgPeakPercent: Math.round(profile.avgPeak * 100),
            maxPeakPercent: Math.round(profile.maxPeak * 100),
            // v6.6.0 P1-4: 成本画像
            totalCostUSD: Math.round(profile.totalCostUSD * 10000) / 10000,
            monthly30dSessions: monthly.sessions,
            monthly30dCostUSD: Math.round(monthly.totalCostUSD * 10000) / 10000,
            monthlyBudgetUSD: monthlyBudgetUSD,
            monthlyBudgetUsedPercent: monthlyBudgetUSD && monthly.totalCostUSD > 0
              ? Math.round((monthly.totalCostUSD / monthlyBudgetUSD) * 100)
              : undefined,
            note: profile.maxPeak > 0.95
              ? "⚠️ 历史峰值 > 95%，建议设置更激进的 hintAt/warnAt 阈值或主动用 enhance_route_to_long_ctx"
              : profile.maxPeak > 0.8
              ? "💡 历史峰值 80-95%，处于上限敏感区"
              : "上下文用量历史健康",
          };
        } catch (err) {
          return { ok: false, reason: `sqlite 不可用: ${(err as Error).message}` };
        }
      },
    }) as any,
    { tier: "tools" } as any,
  );

  // ── tool 5: enhance_ctx_silence（v6.6.1 P2-10）静音 ctx 提醒 N 分钟 ──
  // 用户嫌 70%-85% 阶段反复提醒烦时调；mute 期间所有 banner（revert / threshold /
  // prediction / budget）都跳过。仅内存（重启自动解除，避免持久化静音错过真正风险）。
  api.registerTool(
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_ctx_silence",
      description: "静音上下文守护的 banner 提醒 N 分钟。mute 期间所有 banner（revert/threshold/prediction/budget）都跳过；过期自动解除；重启也自动解除。仅在用户明确表示烦提醒时调",
      inputSchema: Type.Object({
        minutes: Type.Number({
          description: "静音分钟数，1-60；默认 15",
          minimum: 1,
          maximum: 60,
        }),
        reason: Type.Optional(Type.String({ description: "静音原因（log 友好）" })),
      }),
      async execute(params: any) {
        const sessionKey = pickSessionKey(ctx);
        if (!sessionKey) return { ok: false, reason: "no session key in ctx" };
        const minutes = Math.max(1, Math.min(60, Number(params?.minutes) || 15));
        const s = getOrCreate(sessionKey, pickAgentId(ctx));
        s.mutedUntilMs = Date.now() + minutes * 60 * 1000;
        const untilStr = new Date(s.mutedUntilMs).toLocaleTimeString("zh-CN");
        api.logger.info(
          `[ctx-watchdog] silenced for ${minutes}min until ${untilStr} | reason="${params?.reason ?? '-'}" | session=${sessionKey.slice(0, 12)}`,
        );
        return {
          ok: true,
          mutedUntilMs: s.mutedUntilMs,
          mutedUntilLocal: untilStr,
          minutes,
          message: `已静音 ${minutes} 分钟（到 ${untilStr} 自动解除）。期间不会有 ctx-watchdog banner。重启后立即解除。`,
        };
      },
    }) as any,
    { tier: "tools" } as any,
  );

  // ── v6.5.6: 启动期清理 30 天前的 ctx_usage 行（防止 sqlite 无限增长）──
  try {
    const db = getDb();
    const purged = purgeOldCtxUsage(db, 30);
    if (purged.deleted > 0) {
      api.logger.info(`[ctx-watchdog] purged ${purged.deleted} stale ctx_usage rows (>30d)`);
    }
  } catch {
    /* silent: sqlite 不可用 */
  }

  // ── v6.5.6: 进程退出前 finalFlush dirty sessions ──
  const finalFlush = () => {
    if (flushTimer) {
      clearTimeout(flushTimer);
      flushTimer = null;
    }
    flushDirtySessions();
  };
  try {
    process.on("beforeExit", finalFlush);
    process.on("SIGTERM", finalFlush);
  } catch {
    /* silent: 某些 runtime 限制 process.on */
  }

  api.logger.info(
    `[enhance] context-watchdog v6.6.7 已加载（default thresholds=${Math.round(hintAt * 100)}/${Math.round(warnAt * 100)}/${Math.round(criticalAt * 100)}%, force=${Math.round(forceEscalateAt * 100)}% | userConfig-priority escalate + hardcoded fallback | channelAware=${Object.keys({ ...CHANNEL_THRESHOLDS_DEFAULT, ...(config?.thresholdsByChannel ?? {}) }).length} | budget=${monthlyBudgetUSD ? "$" + monthlyBudgetUSD : "off"} | safeHook + runId-dedup + silence + cost+image+subagent+prediction+sqlite）`,
  );
}
