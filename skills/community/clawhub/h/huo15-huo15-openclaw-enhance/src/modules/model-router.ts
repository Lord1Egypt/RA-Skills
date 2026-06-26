/**
 * 模块: 模型路由器（Model Router）v5.7.12 / 接入 v5.8.3 / v6.1.2 重写 PROVIDER_REGISTRY
 *
 * Hook: before_model_resolve
 * 时机: Agent 解析模型之前
 * 作用: 检测多模态 + 任务复杂度，在已注册 provider 间自动路由
 *
 * v6.1.2 修复（2026-05-04）:
 *   - 之前 PROVIDER_REGISTRY 硬编码 deepseek/google-ai-studio/custom-sidus-ai 三个不存在
 *     的 provider，导致路由器选了它们后 runtime 把 model id 整串塞给 sidus，sidus 拒 400
 *     ("model deepseek/deepseek-v4-pro is not supported")。
 *   - 现在只用实际注册的 sidus（priority 1）+ minimax（priority 2）。
 *   - 同步替换 getBestModel(...) || "..." 兜底字符串里的旧 id。
 *
 * 供应商注册表（PROVIDER_REGISTRY）
 * ─────────────────────────────────────
 * priority 数值越小优先级越高。每个 tier 选第一个可用的供应商。
 *
 * | 供应商   | priority | 定位                | tier 支持                  |
 * |---------|----------|--------------------|---------------------------|
 * | sidus   | 1        | DeepSeek/GLM 全家   | flash / pro / reasoner     |
 * | minimax | 2        | 极速兜底             | fast / flash               |
 *
 * 新增供应商：只需在 PROVIDER_REGISTRY 添加一行，且 provider id 必须与
 * openclaw.json `models.providers.<id>` 完全一致；model id 必须与
 * 该 provider 的 `models[].id` 完全一致。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import {
  loadModelRouteConfig,
  saveModelRouteConfig,
  selectProvider,
  patchProvider,
  listAllProviders,
  getModelRouteConfigPath,
  type ModelRouteConfig,
  type RouteMode,
} from "../utils/model-route-config.js";
import {
  recordSample,
  recordError,
  schedulePersist,
  snapshotStats,
  getProviderSpeedSample,
  isModelBanned,
  unbanModel,
  listBannedModels,
} from "../utils/latency-tracker.js";
import {
  readHistory,
  sparkLine,
  getHistoryPath,
} from "../utils/route-history.js";

// ── 类型定义 ───────────────────────────────────────────────

type TaskTier = "fast" | "flash" | "pro" | "reasoner" | "vl" | "hailuo" | "unknown";

interface RouteDecision {
  provider: string;
  model: string;
  taskTier: TaskTier;
  reason: string;
}

// ── 路由缓存 ──────────────────────────────────────────────

const CACHE_TTL_MS = 30_000; // 30 秒

interface CacheEntry {
  decision: RouteDecision;
  expiresAt: number;
}

const routeCache = new Map<string, CacheEntry>();

function cacheKey(prompt: string, mediaTypes: Set<string>): string {
  // 用 prompt 前 200 字符 + 媒体类型做 key（完整 prompt 太长不适合做 key）
  const mediaKey = [...mediaTypes].sort().join(",");
  return `${prompt.slice(0, 200)}|${mediaKey}`;
}

function cacheGet(key: string): RouteDecision | null {
  const entry = routeCache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expiresAt) {
    routeCache.delete(key);
    return null;
  }
  return entry.decision;
}

function cacheSet(key: string, decision: RouteDecision): void {
  // 定期清理过期条目（简单策略：超过 500 条时全量清理）
  if (routeCache.size > 500) {
    const now = Date.now();
    for (const [k, v] of routeCache) {
      if (now > v.expiresAt) routeCache.delete(k);
    }
  }
  routeCache.set(key, { decision, expiresAt: Date.now() + CACHE_TTL_MS });
}

// ── 供应商注册表（可扩展）──────────────────────────────────

// v6.1.2: 重排为只用实际注册的 provider
//         之前的 deepseek/google-ai-studio/custom-sidus-ai 都是不存在的 provider id，
//         路由器选了它们后 runtime 找不到 provider，把 model id 整串发给 sidus，
//         sidus 拒 400（"model deepseek/deepseek-v4-pro is not supported"）。
//         现在只用 sidus（priority 1） + minimax（priority 2）。
// v6.1.4 ⭐ 动态 capability matrix — **启动期扫 ~/.openclaw/openclaw.json**
// `models.providers.<id>.models[]` 自动构建。用户加新 provider/model 不用改代码。
//
// 之前 v6.1.2 硬编码 sidus 是错的；这次彻底"不死"——读 OpenClaw 标准 schema：
//   { id, name, reasoning, input: ["text","image",...], cost: {input,output},
//     contextWindow, maxTokens }
//
// 红线：read 在 register() 启动期做一次（IO），hook 路径只查内存表（O(1)）。
// read 失败 fallback 到空数组——hook 不死，让 OpenClaw 走原生 fallback。
//
// 未来加 model：用户只需在 openclaw.json `models.providers.<provider>.models` 里
// 加一项，重启 OpenClaw 即自动被路由器看见——无需 enhance 升级。
interface ModelCapability {
  /** "<providerId>/<modelId>"，跟 openclaw.json 完全对齐，model_call_ended event 的 key */
  id: string;
  /** 显示名（log 用）*/
  label: string;
  /** 输入模态：image/video/audio 是否支持（text 永远 true）*/
  modalities: { text: true; image?: boolean; video?: boolean; audio?: boolean };
  /** 是否原生支持推理（reasoning content）*/
  reasoning: boolean;
  /** ctx 窗口大小（token 数）*/
  contextWindow: number;
  /** 单次输出 token 上限 */
  maxTokens: number;
  /** $/百万输入 token */
  costInPerM: number;
  /** $/百万输出 token */
  costOutPerM: number;
  /** 综合"快速分"（按 cost 反推：越便宜假设越快，1-10）*/
  speedScore: number;
}

// 启动期 build，hook 内只读
let MODEL_CAPABILITIES: ModelCapability[] = [];
let CAPABILITY_BY_ID: Map<string, ModelCapability> = new Map();
let IMAGE_CAPABLE_MODELS: ModelCapability[] = [];
let VIDEO_CAPABLE_MODELS: ModelCapability[] = [];
let AUDIO_CAPABLE_MODELS: ModelCapability[] = [];
let REASONING_CAPABLE_MODELS: ModelCapability[] = [];
let LONG_CONTEXT_MODELS: ModelCapability[] = []; // ≥ 500K ctx，按 cost 升序
let CHEAP_FAST_MODELS: ModelCapability[] = []; // 非 reasoning 的便宜 model，按 cost 升序

/** speedScore 启发式：根据 cost 反推（便宜的 model 通常更快）。 */
function inferSpeedScore(cap: { costInPerM: number; reasoning: boolean }): number {
  if (cap.costInPerM <= 0.2) return 9;
  if (cap.costInPerM <= 0.5) return cap.reasoning ? 7 : 8;
  if (cap.costInPerM <= 1.0) return 6;
  return cap.reasoning ? 5 : 6;
}

/**
 * 启动期扫描 ~/.openclaw/openclaw.json 的 models.providers，把所有声明的 model
 * 转成 ModelCapability 内存表。失败时返回空数组（让 hook 路径走 OpenClaw 原生 fallback）。
 *
 * Schema（OpenClaw 4.x 标准）：
 *   models.providers.<providerId>.models[] = {
 *     id: string,           // model 短 id，如 "MiniMax-M2.7"
 *     name?: string,        // 显示名
 *     reasoning?: boolean,
 *     input?: ("text"|"image"|"video"|"audio")[],
 *     cost?: { input?: number, output?: number, ... },
 *     contextWindow?: number,
 *     maxTokens?: number,
 *   }
 */
function scanAvailableModels(api: OpenClawPluginApi): ModelCapability[] {
  // 用 dynamic require 避免顶层 import fs 失败时整个 module 拒载
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const fs = require("node:fs") as typeof import("node:fs");
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const pathMod = require("node:path") as typeof import("node:path");
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const homeMod = require("node:os") as typeof import("node:os");

  const openclawHome =
    process.env.OPENCLAW_HOME?.trim() ||
    pathMod.join(homeMod.homedir(), ".openclaw");
  const cfgPath = pathMod.join(openclawHome, "openclaw.json");

  if (!fs.existsSync(cfgPath)) {
    api.logger.warn(
      `[model-router] openclaw.json 不存在 ${cfgPath}，capability 表为空——所有路由走 OpenClaw 原生 fallback`,
    );
    return [];
  }

  let cfg: unknown;
  try {
    cfg = JSON.parse(fs.readFileSync(cfgPath, "utf-8"));
  } catch (err) {
    api.logger.warn(
      `[model-router] openclaw.json 解析失败：${(err as Error).message}——capability 表为空`,
    );
    return [];
  }

  const providers = (cfg as {
    models?: { providers?: Record<string, unknown> };
  })?.models?.providers;
  if (!providers || typeof providers !== "object") return [];

  const out: ModelCapability[] = [];
  for (const [providerId, raw] of Object.entries(providers)) {
    const p = raw as { models?: unknown[] };
    if (!Array.isArray(p?.models)) continue;
    for (const mRaw of p.models) {
      const m = mRaw as {
        id?: string;
        name?: string;
        reasoning?: boolean;
        input?: string[];
        cost?: { input?: number; output?: number };
        contextWindow?: number;
        maxTokens?: number;
      };
      if (!m?.id || typeof m.id !== "string") continue;

      const inputs = Array.isArray(m.input) ? m.input.map((s) => String(s).toLowerCase()) : ["text"];
      const cap: ModelCapability = {
        id: `${providerId}/${m.id}`,
        label: m.name || `${providerId}/${m.id}`,
        modalities: {
          text: true,
          ...(inputs.includes("image") ? { image: true } : {}),
          ...(inputs.includes("video") ? { video: true } : {}),
          ...(inputs.includes("audio") ? { audio: true } : {}),
        },
        reasoning: m.reasoning === true,
        contextWindow: typeof m.contextWindow === "number" ? m.contextWindow : 32768,
        maxTokens: typeof m.maxTokens === "number" ? m.maxTokens : 4096,
        costInPerM: typeof m.cost?.input === "number" ? m.cost.input : 1.0,
        costOutPerM: typeof m.cost?.output === "number" ? m.cost.output : 2.0,
        speedScore: 0, // 下面填
      };
      cap.speedScore = inferSpeedScore(cap);
      out.push(cap);
    }
  }

  return out;
}

/**
 * 用扫描出来的 capabilities 重建所有 hook 路径需要的派生索引。
 * 启动期 + 用户调 enhance_model_route_reload 时跑。
 */
function rebuildCapabilityIndices(caps: ModelCapability[], api: OpenClawPluginApi): void {
  MODEL_CAPABILITIES = caps;
  CAPABILITY_BY_ID = new Map(caps.map((c) => [c.id, c]));
  IMAGE_CAPABLE_MODELS = caps
    .filter((c) => c.modalities.image === true)
    .sort((a, b) => a.costInPerM - b.costInPerM);
  VIDEO_CAPABLE_MODELS = caps
    .filter((c) => c.modalities.video === true)
    .sort((a, b) => a.costInPerM - b.costInPerM);
  AUDIO_CAPABLE_MODELS = caps
    .filter((c) => c.modalities.audio === true)
    .sort((a, b) => a.costInPerM - b.costInPerM);
  REASONING_CAPABLE_MODELS = caps
    .filter((c) => c.reasoning)
    .sort((a, b) => a.costInPerM - b.costInPerM);
  LONG_CONTEXT_MODELS = caps
    .filter((c) => c.contextWindow >= 500_000)
    .sort((a, b) => a.costInPerM - b.costInPerM);
  CHEAP_FAST_MODELS = caps
    .filter((c) => !c.reasoning) // 非 reasoning 的视为"快速档"
    .sort((a, b) => a.costInPerM - b.costInPerM);

  api.logger.info(
    `[model-router] capability 索引已重建：${caps.length} models | image=${IMAGE_CAPABLE_MODELS.length} | video=${VIDEO_CAPABLE_MODELS.length} | audio=${AUDIO_CAPABLE_MODELS.length} | reasoning=${REASONING_CAPABLE_MODELS.length} | longCtx≥500K=${LONG_CONTEXT_MODELS.length}`,
  );
  if (caps.length === 0) {
    api.logger.warn(
      `[model-router] 当前 0 model 可用——所有路由会走 OpenClaw 原生 fallback。检查 ~/.openclaw/openclaw.json 的 models.providers 配置`,
    );
  }
}

// 兼容老代码：从 capability 表派生 PROVIDER_REGISTRY 风格映射（getBestModel 还在用）。
// 启动期 build 一次，hook 路径只读。
let DERIVED_TIER_MAP: Record<string, string> = {};

function rebuildDerivedTierMap(): void {
  DERIVED_TIER_MAP = {};
  // flash/fast tier：选最便宜的非 reasoning text model（速度+成本最优）
  if (CHEAP_FAST_MODELS.length > 0) {
    DERIVED_TIER_MAP.flash = CHEAP_FAST_MODELS[0].id;
    DERIVED_TIER_MAP.fast = CHEAP_FAST_MODELS[0].id;
  }
  // pro/reasoner tier：选最便宜的 reasoning model（性价比）
  if (REASONING_CAPABLE_MODELS.length > 0) {
    DERIVED_TIER_MAP.pro = REASONING_CAPABLE_MODELS[0].id;
    DERIVED_TIER_MAP.reasoner = REASONING_CAPABLE_MODELS[0].id;
  }
  // vl tier：image-capable 第一个
  if (IMAGE_CAPABLE_MODELS.length > 0) {
    DERIVED_TIER_MAP.vl = IMAGE_CAPABLE_MODELS[0].id;
    DERIVED_TIER_MAP.hailuo = IMAGE_CAPABLE_MODELS[0].id;
  }
}

// ── getBestModel 缓存 ─────────────────────────────────────
const bestModelCache = new Map<TaskTier, string>();

/**
 * v6.1.4: 从动态 DERIVED_TIER_MAP 取（启动期由 capability 扫描结果派生）。
 * 兼容旧调用：tier 没命中返回 null，调用方有 hardcoded fallback string 兜底。
 */
function getBestModel(taskTier: TaskTier): string | null {
  const cached = bestModelCache.get(taskTier);
  if (cached) return cached;
  const id = DERIVED_TIER_MAP[taskTier];
  if (id) {
    bestModelCache.set(taskTier, id);
    return id;
  }
  return null;
}

// ── 阈值常量 ──────────────────────────────────────────────

const SHORT_CIRCUIT_THRESHOLD = 50;   // 极短 prompt 直接快速模型
const COMPLEX_LENGTH_THRESHOLD = 2000; // 超长 prompt 视为复杂任务

// ── 任务特征库（按优先级排列）──────────────────────────────

// 极速任务：极短文本或用户表示急迫（最先检查）
const FAST_PATTERNS: RegExp[] = [
  /\b(快点|赶紧|马上|立刻|迅速|急|赶时间)\b/i,
  /\b(在吗|在不|在不啦|嗨|喂)\b/i,
];

// 多模态检测（最高优先，紧随其后）
// 代码任务 — 特征明确，优先检测避免被其他模式误吞
const CODE_PATTERNS: RegExp[] = [
  /```/,
  /\b(code|coding|编程|代码|编码|写代码|写个)\b/i,
  /\b(debug|调试|traceback|报错|修复|排查|定位|bug)\b/i,
  /\b(重构|refactor|优化性能|性能优化)\b/i,
  /\b(function|class|import|def |const |let |var |async|await|export|interface|type |enum)\b/i,
  /\b(python|javascript|typescript|java|go|rust|c\+\+|sql|bash|shell|php|ruby)\b/i,
  /\b(api|endpoint|middleware|hook|plugin|component|module|package)\b/i,
  /\b(git commit|git push|git merge|pull request|PR)\b/i,
];

// Debug / 报错分析 — 代码相关但更紧急
const DEBUG_PATTERNS: RegExp[] = [
  /\b(报错|错误|error|exception|crash|崩溃|异常)\b/i,
  /\b(not found|cannot find|undefined is not|typeerror|syntaxerror|referenceerror)\b/i,
  /\b(怎么.*不行|为什么.*报错|哪里.*错了|修.*bug)\b/i,
];

// 文档生成任务
const DOC_PATTERNS: RegExp[] = [
  /\b(写.*word|写.*文档|生成.*word|写.*合同|写.*报告)\b/i,
  /\b(写.*PPT|做.*PPT|生成.*PPT|生成.*演示)\b/i,
  /\b(生成.*PDF|PDF|写.*方案)\b/i,
];

// 报告生成（合同/方案/正式文档）
const REPORT_PATTERNS: RegExp[] = [
  /\b(合同|协议|标书|投标|方案书|需求文档|技术方案|项目计划)\b/i,
  /\b(生成.*报告|写.*报告|出具.*报告)\b/i,
];

// 数据分析/统计
const DATA_ANALYSIS_PATTERNS: RegExp[] = [
  /\b(数据.*分析|统计|报表|图表|可视化|dashboard)\b/i,
  /\b(excel|csv|json.*分析|数据.*处理|数据.*清洗)\b/i,
  /\b(同比|环比|趋势|增长.*率|占比|平均值|中位数)\b/i,
];

// 数学计算/公式推导
const MATH_PATTERNS: RegExp[] = [
  /\b(计算|算一下|推导|证明|公式|方程|求解|积分|微分)\b/i,
  /\b(数学|代数|几何|微积分|概率|统计.*题)\b/i,
  /[+\-*/^]=/,
  /\b(sqrt|log|sin|cos|tan|lim|∑|∫)\b/i,
];

// 分析/架构/深度任务
const ANALYSIS_PATTERNS: RegExp[] = [
  /\b(架构|设计|方案|规划|技术选型|系统设计|数据库设计)\b/i,
  /\b(architecture|design pattern|system design)\b/i,
  /\b(分析|深入|详细|为什么|原因|原理|机制|底层|源码)\b/i,
  /\b(compare|对比|区别|优缺点|利弊|权衡|比较)\b/i,
  /\b(配置|config|setup|部署|deploy|迁移|migration|安装)\b/i,
  /(?:^|\n)[ ]*[{[]/,
  /\b(odoo|erp|crm|进销存|库存|财务|会计)\b/i,
  /\b(订单|采购|销售|报价|发票)\b/i,
  /\b(生成|create|build|implement|develop)\b/i,
];

// 推理任务（需要深度思考）
const REASONER_PATTERNS: RegExp[] = [
  /\b(推理|reason|think deeply|深入思考|复杂问题)\b/i,
  /\b(证明|推导)\b/i,
  /\b(为什么.*为什么.*为什么)\b/i,
];

// 多步骤复杂推理
const MULTI_STEP_PATTERNS: RegExp[] = [
  /\b(步骤|step.*step|多步|chain.*thought|逐步|一步一步)\b/i,
  /\b(先.*再.*然后|first.*then.*finally)\b/i,
  /\b(plan|规划.*执行|拆分|分解|流程.*设计)\b/i,
];

// 写作/文案/创作 — 短文案用 flash，长文用 pro（由长度判断兜底）
const WRITING_PATTERNS: RegExp[] = [
  /\b(写.*文章|写.*文案|写.*脚本|写.*故事|写.*小说)\b/i,
  /\b(创作|创意|灵感|改写|润色|扩写|缩写|改写)\b/i,
  /\b(写.*标题|写.*slogan|写.*广告语|写.*宣传)\b/i,
  /\b(写.*邮件|写.*通知|写.*公告|写.*邀请函)\b/i,
];

// 长文本摘要/总结
const SUMMARIZATION_PATTERNS: RegExp[] = [
  /\b(总结|摘要|概括|归纳|提炼|梳理.*要点|汇总)\b/i,
  /\b(summarize|summary|tldr|key points|要点)\b/i,
];

// 翻译任务 — flash 足够
const TRANSLATION_PATTERNS: RegExp[] = [
  /\b(翻译|translate|译成|翻成|译成中文|译成英文|中译英|英译中)\b/i,
  /\b(用.*说|用.*写|换成.*语言)\b/i,
];

// 信息检索/查找 — flash 足够
const RETRIEVAL_PATTERNS: RegExp[] = [
  /\b(搜索|搜一下|查一下|帮我查|帮我找|找一下|检索)\b/i,
  /\b(什么是|是什么|是谁|在哪里|什么时候|多少钱)\b/i,
  /\b(定义|含义|意思|解释|百科|wiki)\b/i,
];

// 情绪识别/情感分析 — flash 足够
const SENTIMENT_PATTERNS: RegExp[] = [
  /\b(情绪|情感|心情|态度|语气|口吻|正面|负面|中性)\b/i,
  /\b(sentiment|emotion|tone|mood|polarity)\b/i,
];

// 客服对话/闲聊 — flash 足够
const CHAT_PATTERNS: RegExp[] = [
  /\b(你好|hi|hello|hey|嗨|早上好|下午好|晚上好|晚安|再见|拜拜|谢谢|多谢|ok|好的)\b/i,
  /^(hi|hello|hey|哟|嗯|哦|好|行|对|是)\b/i,
  /\b(怎么样|如何|好不好|行不行|可以吗|能.*吗|会.*吗)\b/i,
  /\b(天气|温度|下雨|多少度|热不热|冷不冷)\b/i,
  /\b(在吗|在不|在不啦)\b/i,
];

// 快速问答（一句话回答）— flash 足够
const QUICK_QA_PATTERNS: RegExp[] = [
  /\b(几点|今天星期几|日期|时间|现在.*时间)\b/i,
  /\b(多少|几个|哪些|哪个|谁|哪里|什么)\b/i,
];

// 简单常识查询
const SIMPLE_PATTERNS: RegExp[] = [
  /\b(解释一下|简单.*说一下)\b/i,
  /\b(多少钱|价格|报价|费用)\b/i,
  /\b(计算|算一下|加.*减.*乘.*除)\b/i,
];

// ── 工具函数 ──────────────────────────────────────────────

const IMAGE_MIME_PREFIX = "image/";
const VIDEO_MIME_PREFIX = "video/";
const AUDIO_MIME_PREFIX = "audio/";

function detectAttachmentMediaTypes(
  attachments?: Array<{ kind?: string; mimeType?: string }>
): Set<string> {
  const types = new Set<string>();
  if (!attachments?.length) return types;
  for (const att of attachments) {
    const mime = (att.mimeType || "").toLowerCase();
    const kind = (att.kind || "").toLowerCase();
    if (mime.startsWith(IMAGE_MIME_PREFIX) || kind === "image") types.add("image");
    else if (mime.startsWith(VIDEO_MIME_PREFIX) || kind === "video") types.add("video");
    else if (mime.startsWith(AUDIO_MIME_PREFIX) || kind === "audio") types.add("audio");
  }
  return types;
}

function detectPromptInlineMedia(prompt?: string): Set<string> {
  const types = new Set<string>();
  if (!prompt) return types;
  if (prompt.includes("[media attached") || prompt.includes("[image]")) types.add("image");
  if (/\.openclaw\/media\/inbound\/[^\s]+\.(png|jpg|jpeg|gif|webp|bmp)/i.test(prompt)) types.add("image");
  if (prompt.includes("[video]")) types.add("video");
  if (prompt.includes("[audio]") || prompt.includes("[voice]")) types.add("audio");
  return types;
}

/** 匹配任意一个 pattern */
function matchAny(patterns: readonly RegExp[], text: string): boolean {
  for (const pat of patterns) {
    if (pat.test(text)) return true;
  }
  return false;
}

/** 路由主逻辑 */
function routeTask(prompt: string, mediaTypes: Set<string>): RouteDecision {
  const p = prompt.trim();
  const len = p.length;

  // ── 0. 极短 prompt 短路（无媒体，<50 字符）─────────
  // v6.1.4: minimax M2.7 → deepseek-v4-flash（speedScore 9 vs 7、$0.14 vs $0.3、1M ctx vs 200K）
  if (len <= SHORT_CIRCUIT_THRESHOLD && mediaTypes.size === 0) {
    return {
      provider: "deepseek",
      model: "deepseek/deepseek-v4-flash",
      taskTier: "fast",
      reason: `极短文本短路（${len}字符）→ DeepSeek V4 Flash`,
    };
  }

  // ── 1. 多模态硬路由（v6.1.4 修对）─────────────────────
  // image → 强制 minimax M2.7（capability table 唯一支持 image 的）。
  // 之前 v6.1.2 "用 sidus pro 兜底"是错的——文本 model 收到 image 引用会 400。
  // video/audio → 用户机器没装支持的 model，让 deepseek-v4-pro 文本兜底（不会 400，但理解会丢）。
  if (mediaTypes.has("image")) {
    const imgModel = IMAGE_CAPABLE_MODELS[0];
    if (imgModel) {
      return {
        provider: imgModel.id.split("/")[0]!,
        model: imgModel.id,
        taskTier: "vl",
        reason: `image 输入 → 硬路由到 ${imgModel.label}（capability table 唯一支持 image）`,
      };
    }
  }
  if (mediaTypes.has("video") || mediaTypes.has("audio")) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return {
      provider: "deepseek",
      model,
      taskTier: "pro",
      reason: `${[...mediaTypes].join(",")} 输入但无 capable model → 文本兜底 ${model}（用户机器未装 video/audio model）`,
    };
  }

  // ── 2. ctx-aware 长文本路由（v6.1.4 新增）──
  // 中文 token 估算：length * 0.6（中文 1 字 ≈ 0.6 token，英文 1 word ≈ 1.3 token，混合粗估 0.6）。
  // > 50K token（约 80K 字符）→ 强制走 1M ctx model（deepseek-v4-pro 或 v4-flash）
  // 200K-1M ctx 段：优先 deepseek-v4-flash（便宜 12x 比 pro，快 1.8x）。
  const estimatedTokens = Math.round(len * 0.6);
  if (estimatedTokens >= 50_000) {
    // 找最便宜的长 ctx model
    const longCtx = LONG_CONTEXT_MODELS[0]; // 已按 cost 升序排
    if (longCtx) {
      return {
        provider: longCtx.id.split("/")[0]!,
        model: longCtx.id,
        taskTier: "pro",
        reason: `超长 ctx 估 ${estimatedTokens} tokens（${len}字符）→ 长 ctx model ${longCtx.label}`,
      };
    }
  }

  // ── 3. 超长 prompt（>2000 字符但 ctx 还在 200K 内）→ 复杂任务 pro ──
  if (len > COMPLEX_LENGTH_THRESHOLD) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return {
      provider: "deepseek", model, taskTier: "pro",
      reason: `超长文本（${len}字符 / ${estimatedTokens} tokens）→ pro tier`,
    };
  }

  // ── 3. 文本任务分类（按优先级）──────────────────

  // 代码任务 — 特征明确，先检查
  if (matchAny(CODE_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "代码任务 → pro tier" };
  }

  // Debug / 报错分析
  if (matchAny(DEBUG_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "Debug/报错分析 → pro tier" };
  }

  // 推理任务
  if (matchAny(REASONER_PATTERNS, p)) {
    const model = getBestModel("reasoner") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "reasoner", reason: "推理任务 → reasoner tier" };
  }

  // 数学计算
  if (matchAny(MATH_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "数学计算 → pro tier" };
  }

  // 数据分析
  if (matchAny(DATA_ANALYSIS_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "数据分析 → pro tier" };
  }

  // 分析/架构/深度任务
  if (matchAny(ANALYSIS_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "分析/架构 → pro tier" };
  }

  // 多步骤复杂推理
  if (matchAny(MULTI_STEP_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "多步骤推理 → pro tier" };
  }

  // 文档生成 → pro
  if (matchAny(DOC_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "文档生成 → pro tier" };
  }

  // 报告生成 → pro
  if (matchAny(REPORT_PATTERNS, p)) {
    const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
    return { provider: "deepseek", model, taskTier: "pro", reason: "报告生成 → pro tier" };
  }

  // 写作/文案/创作 — 按长度判断：长文 → pro，短文 → flash
  if (matchAny(WRITING_PATTERNS, p)) {
    if (len > 300) {
      const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
      return { provider: "deepseek", model, taskTier: "pro", reason: `写作创作（${len}字符，长文）→ pro tier` };
    }
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: `写作创作（${len}字符，短文）→ flash tier` };
  }

  // 长文本摘要 → pro（>500 字）
  if (matchAny(SUMMARIZATION_PATTERNS, p)) {
    if (len > 500) {
      const model = getBestModel("pro") || "deepseek/deepseek-v4-pro";
      return { provider: "deepseek", model, taskTier: "pro", reason: `长文本摘要（${len}字符）→ pro tier` };
    }
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: `简短摘要 → flash tier` };
  }

  // ── 以下为 flash-tier 任务 ──

  // 翻译任务
  if (matchAny(TRANSLATION_PATTERNS, p)) {
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: "翻译任务 → flash tier" };
  }

  // 信息检索
  if (matchAny(RETRIEVAL_PATTERNS, p)) {
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: "信息检索 → flash tier" };
  }

  // 情绪/情感分析
  if (matchAny(SENTIMENT_PATTERNS, p)) {
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: "情感分析 → flash tier" };
  }

  // 客服/闲聊
  if (matchAny(CHAT_PATTERNS, p)) {
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: "闲聊对话 → flash tier" };
  }

  // 快速问答
  if (matchAny(QUICK_QA_PATTERNS, p)) {
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: "快速问答 → flash tier" };
  }

  // 简单任务兜底
  if (matchAny(SIMPLE_PATTERNS, p)) {
    const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
    return { provider: "deepseek", model, taskTier: "flash", reason: "简单任务 → flash tier" };
  }

  // 急迫关键词兜底（用户催）
  if (matchAny(FAST_PATTERNS, p)) {
    return {
      provider: "minimax",
      model: "minimax/MiniMax-M2.7",
      taskTier: "fast",
      reason: `急迫关键词（${len}字符）→ MiniMax M2.7`,
    };
  }

  // ── 4. 默认：deepseek-v4-flash ──────────────────────────
  // v6.5.6: 之前硬编码 "sidus/DeepSeek-V4-Flash" 兜底，但 sidus provider 不再注册
  // → fallback 找不到 provider → 返回 model id 给 LLM → LLM 自己 session_status 调用
  // 时复用旧 model id 撞 "Model not allowed"。改成 deepseek 与 OpenClaw 默认一致。
  const model = getBestModel("flash") || "deepseek/deepseek-v4-flash";
  return {
    provider: "deepseek", model, taskTier: "flash",
    reason: `默认 → deepseek-v4-flash（${len}字符）`,
  };
}

// ── v5.8.4 配置驱动路由 ──────────────────────────────────

/**
 * 启动期 load 一次到内存；工具修改后 in-place 更新这个 ref。
 * 单进程读写，无并发风险。
 */
let runtimeConfig: ModelRouteConfig = loadModelRouteConfig();

function reloadConfig(): void {
  runtimeConfig = loadModelRouteConfig();
  bestModelCache.clear();
  routeCache.clear();
}

function persistConfig(): void {
  saveModelRouteConfig(runtimeConfig);
  bestModelCache.clear();
  routeCache.clear();
}

/**
 * v6.1.4: channel 偏好——路由 tier 提升/降级。仅在 task tier 是默认 flash/fast 时生效，
 * 显式 task 关键词（CODE/REASONER 等）已经命中的不动。
 *
 * 不写死硬规则，**只调 tier preference**——具体 model 仍由 capability 表 + selectProvider 决定。
 *
 * 内置启发式：
 *   - wecom:group / wecom:direct（IM 短消息）→ flash 偏好（速度优先）
 *   - dingtalk / wechat-service → flash 偏好
 *   - cli / api / web（开发场景）→ pro 偏好（精度优先）
 *   - 其他 → 不动
 */
function applyChannelPreference(
  baseDecision: RouteDecision,
  channelId: string | undefined,
): RouteDecision {
  if (!channelId) return baseDecision;
  const tier = baseDecision.taskTier;
  // 只调"默认级别"的 tier，避免覆盖明确意图（pro/reasoner 命中后不降级）
  if (tier !== "flash" && tier !== "fast") return baseDecision;

  const lower = channelId.toLowerCase();
  // IM 渠道：偏 flash（已经是 flash/fast 不变；只是 reason 标注）
  if (lower.startsWith("wecom") || lower.startsWith("dingtalk") || lower.startsWith("wechat")) {
    return { ...baseDecision, reason: `${baseDecision.reason} | channel=${channelId} (IM,速度优先)` };
  }
  return baseDecision;
}

/**
 * v6.1.4: circuit breaker —— 选定 model 后查 latency tracker 的 errRate，
 * > 0.5 within 1h 时跳过该 model，找下一个同 tier 内 cost 最接近的备选。
 * 数据完全在 latency-tracker 内存里，零 IO。
 */
/**
 * v6.1.5: 对给定 decision 检查并切换。两个独立的"切换条件"：
 *   1. quota-ban（来自 recordError 的硬错检测，即时切，不等累积）
 *   2. circuit-breaker（基于 errRate window 累积式判断 > 50%）
 *
 * 共用同一个候选选择逻辑（同模态/同 reasoning，按 errRate + cost 排）。
 */
function applyCircuitBreaker(
  decision: RouteDecision,
  api: OpenClawPluginApi,
): RouteDecision {
  // 检查 1: quota ban（v6.1.5 新增）—— 优先级最高，单次硬错就切
  const banEntry = isModelBanned(decision.model);
  if (banEntry) {
    const winner = pickFallbackCandidate(decision.model);
    if (winner) {
      const remainMin = Math.round((banEntry.expireAt - Date.now()) / 60_000);
      api.logger.warn(
        `[model-router] quota-ban active on ${decision.model} (${banEntry.trigger}, 剩 ${remainMin}min) → 切到 ${winner.id}`,
      );
      return {
        provider: winner.id.split("/")[0]!,
        model: winner.id,
        taskTier: decision.taskTier,
        reason: `${decision.reason} | quota-ban(${decision.model} 剩${remainMin}min)→${winner.label}`,
      };
    }
    // 没备选——只能让原 model 继续（OpenClaw 会再失败一次，但路由器尽力了）
    api.logger.warn(
      `[model-router] quota-ban active on ${decision.model} 但无同类备选，继续用原 model`,
    );
  }

  // 检查 2: circuit breaker（v6.1.4，errRate 累积式）
  const sample = getProviderSpeedSample(decision.model);
  if (!sample || sample.samples < 5 || sample.errRate <= 0.5) return decision;

  const winner = pickFallbackCandidate(decision.model);
  if (!winner) return decision;
  api.logger.warn(
    `[model-router] circuit-breaker: ${decision.model} errRate=${(sample.errRate * 100).toFixed(0)}% (${sample.samples} samples) → 切到 ${winner.id}`,
  );
  return {
    provider: winner.id.split("/")[0]!,
    model: winner.id,
    taskTier: decision.taskTier,
    reason: `${decision.reason} | circuit-breaker(${decision.model} err=${(sample.errRate * 100).toFixed(0)}%)→${winner.label}`,
  };
}

/**
 * v6.1.5: 给定一个失败 model，选同模态+同 reasoning 能力的备选。
 * 跳过当前 banned 的，按 errRate 升序 + cost 升序排。
 */
function pickFallbackCandidate(failedModelId: string): ModelCapability | null {
  const failed = CAPABILITY_BY_ID.get(failedModelId);
  if (!failed) return null;
  const candidates = MODEL_CAPABILITIES.filter(
    (c) =>
      c.id !== failedModelId &&
      !isModelBanned(c.id) && // 跳过同样在 ban 期的
      (failed.modalities.image ? c.modalities.image === true : true) &&
      c.reasoning === failed.reasoning,
  );
  if (candidates.length === 0) return null;
  const ranked = candidates.sort((a, b) => {
    const sa = getProviderSpeedSample(a.id);
    const sb = getProviderSpeedSample(b.id);
    const errA = sa && sa.samples >= 5 ? sa.errRate : 0;
    const errB = sb && sb.samples >= 5 ? sb.errRate : 0;
    if (errA !== errB) return errA - errB;
    return a.costInPerM - b.costInPerM;
  });
  return ranked[0];
}

/**
 * 主路由：先用 routeTask 选 tier（auto-task 模式的 task-aware 部分），
 * 再用 selectProvider 按 mode 选 provider，
 * 再走 channel preference + circuit breaker 调整。
 */
function pickModel(
  prompt: string,
  mediaTypes: Set<string>,
  channelId?: string,
  api?: OpenClawPluginApi,
): RouteDecision | null {
  const taskDecision = routeTask(prompt, mediaTypes);
  const tier = taskDecision.taskTier;
  const picked = selectProvider(runtimeConfig, tier);

  let decision: RouteDecision;
  if (!picked) {
    // selectProvider 没命中（用户 model-route.json 删空了某个 tier）
    // → 直接用 routeTask 的硬选（基于 capability 表 + DERIVED_TIER_MAP）
    decision = taskDecision;
  } else if (!CAPABILITY_BY_ID.has(picked.id)) {
    // v6.1.7 ⭐ capability 验证：picked.id 不在 ~/.openclaw/openclaw.json 实际注册
    // 的 model 列表里——是用户 model-route.json 残留的死 entry（典型如 minimax/MiniMax-VL-01
    // 实际未注册，但老配置写着）。这种情况覆盖硬路由会把不存在的 model 发给 OpenClaw runtime
    // → fallback 到默认 model → image 任务收不到 image。
    //
    // 修：picked 不在 capability 表 → 抛弃 picked，回退到 routeTask 给的硬路由
    // （routeTask 是从 IMAGE_CAPABLE_MODELS / LONG_CONTEXT_MODELS 等动态扫描出来的，
    // 一定是用户实际可用的 model）。
    api?.logger.warn(
      `[model-router] selectProvider 返回 ${picked.id} 但不在 capability 表（model-route.json 残留死 entry，可能是历史配置漂移），回退到硬路由 ${taskDecision.model}`,
    );
    decision = {
      ...taskDecision,
      reason: `${taskDecision.reason} | ⚠ ${picked.id} 不存在，回退硬路由`,
    };
  } else {
    decision = {
      provider: picked.id.split("/")[0] ?? "?",
      model: picked.id,
      taskTier: tier,
      reason: `${runtimeConfig.mode} | ${taskDecision.reason} | ${picked.reason}`,
    };
  }

  // channel 偏好（轻量调整）
  decision = applyChannelPreference(decision, channelId);

  // circuit breaker（基于历史 errRate）
  if (api) {
    decision = applyCircuitBreaker(decision, api);
  }

  return decision;
}

// ── Hook 注册 ─────────────────────────────────────────────

export function registerModelRouter(api: OpenClawPluginApi) {
  // v6.1.4: 启动期扫 ~/.openclaw/openclaw.json 自动构建 capability 表
  // —— 用户加新 provider/model 不用改代码，重启 OpenClaw 即生效。
  // 这里是 IO 但发生在 register() 阶段（plugin 加载期），不在 hook 路径，无延迟成本。
  try {
    const caps = scanAvailableModels(api);
    rebuildCapabilityIndices(caps, api);
    rebuildDerivedTierMap();
    bestModelCache.clear();
    routeCache.clear();
  } catch (err) {
    api.logger.warn(
      `[model-router] capability 启动期扫描失败：${(err as Error).message}——hook 路径仍可工作（走原生 fallback）`,
    );
  }

  api.on("before_model_resolve", (event, ctx) => {
    // 检测媒体类型
    let mediaTypes: Set<string>;
    if (event?.attachments?.length) {
      mediaTypes = detectAttachmentMediaTypes(event.attachments);
    } else {
      mediaTypes = detectPromptInlineMedia(event?.prompt);
    }

    // v6.1.4: ctx 透传给 pickModel 做 channel-aware 路由（channel/agent 偏好）
    const channelId = (ctx as { channelId?: string } | undefined)?.channelId;

    // 缓存查找（mode=weighted/speed 时跳缓存——每次都要重新抽样/调权）
    // cache key 加 channelId 防止跨渠道污染（wecom 群偏 flash vs odoo 偏 pro）
    if (runtimeConfig.mode === "priority" || runtimeConfig.mode === "auto-task" || runtimeConfig.mode === "cost-budget") {
      const ck = `${channelId ?? ""}|${cacheKey(event?.prompt || "", mediaTypes)}`;
      const cached = cacheGet(ck);
      if (cached) {
        api.logger.info(`[model-router] CACHE HIT: ${cached.reason} | → ${cached.model}`);
        return { modelOverride: cached.model };
      }
    }

    // 执行路由决策（带 channelId 做偏好调整 + circuit breaker 接 errRate）
    const decision = pickModel(event?.prompt || "", mediaTypes, channelId, api);
    if (!decision) return undefined;

    if (runtimeConfig.mode === "priority" || runtimeConfig.mode === "auto-task" || runtimeConfig.mode === "cost-budget") {
      const ck = `${channelId ?? ""}|${cacheKey(event?.prompt || "", mediaTypes)}`;
      cacheSet(ck, decision);
    }

    api.logger.info(
      `[model-router] ${decision.reason} | tier=${decision.taskTier} | → ${decision.model}`
    );

    return { modelOverride: decision.model };
  });

  // ── v5.8.5 latency tracker：监听 model_call_ended 收集 P50/P95/errRate ──
  // openclaw 2026.4.29 dist 确认 emit 这个 hook（hook-types.d.ts 含 PluginHookModelCallEndedEvent
  // 与 durationMs / outcome / timeToFirstByteMs 字段），但 enhance 项目锁定的 plugin-sdk
  // 类型 union 还没及时更新含 "model_call_ended"——用 (api.on as any) cast 绕过类型不齐。
  // runtime 行为完全依赖 dist 实现，cast 不影响功能。
  (api.on as any)("model_call_ended", (event: any, _ctx: any) => {
    try {
      const provider = event?.provider;
      const model = event?.model;
      if (!provider || !model) return;
      const providerId = `${provider}/${model}`;
      // 优先 TTFB（更接近"用户体感速度"），缺失 fallback 到 totalDurationMs
      const ttfb = event?.timeToFirstByteMs;
      const dur = event?.durationMs;
      const latencyMs = typeof ttfb === "number" ? ttfb : (typeof dur === "number" ? dur : 0);
      const errored = event?.outcome === "error";
      recordSample(providerId, latencyMs, errored);

      // v6.1.5 ⭐ quota-aware 即时切换：检测"配额耗尽/超限/限流"类硬错 → 立刻 ban
      // 不等 errRate 累积（5 样本 50%）—— 这种错后续请求一定也失败，越早切越好。
      // event 字段命名各 OpenClaw 版本不一，全部尝试一遍。
      if (errored) {
        const errorMessage =
          event?.errorMessage ??
          event?.error?.message ??
          event?.error ??
          event?.outcomeReason ??
          (typeof event?.body === "string" ? event.body : "") ??
          "";
        const httpStatus =
          (typeof event?.httpStatus === "number" ? event.httpStatus : null) ??
          (typeof event?.error?.status === "number" ? event.error.status : null) ??
          (typeof event?.statusCode === "number" ? event.statusCode : null) ??
          null;
        const result = recordError(providerId, String(errorMessage), httpStatus);
        if (result.banned) {
          api.logger.warn(
            `[model-router] ⛔ quota-ban: ${providerId} 触发 ${result.trigger} → 1h 内不再路由到此 model（其他备选自动接管）。手动恢复：enhance_model_route_unban("${providerId}")`,
          );
          // 立刻清缓存——下次 prompt 不命中老 model 缓存
          routeCache.clear();
        }
      }

      schedulePersist(runtimeConfig);
    } catch {
      // hook 内永不抛 —— 防止把 openclaw 主流程拖坏
    }
  });

  // ── v5.8.4 工具：4 个对话式配置入口 ─────────────────────

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_model_route_status",
      description:
        "查看当前模型路由配置：mode + 各 tier × provider 的 priority / weight / enabled / 最近延迟。" +
        "对话式配置入口（v5.8.4）。",
      parameters: Type.Object({}),
      async execute() {
        const cfg = runtimeConfig;
        const lines: string[] = [];
        lines.push(`# 模型路由当前状态`);
        lines.push(``);
        lines.push(`**模式**: \`${cfg.mode}\``);
        lines.push(`  - priority: 严格按 priority 排序`);
        lines.push(`  - weighted: 按 weight 加权随机`);
        lines.push(`  - speed: 按最近 P50 + errRate 自动调权（v5.8.5+ 才有数据）`);
        lines.push(`  - auto-task: 按任务复杂度选 tier，tier 内按 priority`);
        lines.push(``);
        lines.push(`**配置文件**: \`${getModelRouteConfigPath()}\``);
        lines.push(``);
        const memSnap = snapshotStats();
        for (const [tier, t] of Object.entries(cfg.models)) {
          lines.push(`## tier = \`${tier}\``);
          lines.push(``);
          lines.push(`| provider | priority | weight | enabled | p50ms | p95ms | errRate | samples | pending |`);
          lines.push(`|---|---|---|---|---|---|---|---|---|`);
          for (const p of t.providers) {
            const speed = cfg.speedTracking?.[p.id];
            const mem = memSnap[p.id];
            lines.push(
              `| \`${p.id}\` | ${p.priority} | ${p.weight} | ${p.enabled ? "✓" : "✗"} | ${speed?.p50Ms ?? "-"} | ${speed?.p95Ms ?? "-"} | ${speed?.errRate?.toFixed(2) ?? "-"} | ${speed?.samples ?? mem?.samples ?? 0} | ${mem?.pending ?? 0} |`,
            );
          }
          lines.push(``);
        }
        if (Object.keys(memSnap).length > 0) {
          lines.push(`> v5.8.5 latency tracker 在线：每次 model_call_ended 收集 P50/P95/errRate，1h 滑动窗口，节流 60s 落盘。`);
          lines.push(`> "pending" 列 = 上次落盘后新增样本数，攒够 10 或满 60s 自动 persist 到 ${getModelRouteConfigPath()}。`);
        }
        return { content: [{ type: "text" as const, text: lines.join("\n") }] };
      },
    })) as any,
    { name: "enhance_model_route_status" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_model_route_set",
      description:
        "改某个 tier 下某个 provider 的 priority / weight / enabled 字段。" +
        "示例：tier='flash', providerId='minimax/MiniMax-M2.7', priority=10 把 minimax 降权到几乎不选。" +
        "weight 0-100，priority 越小越优先；任一字段可省略不改。",
      parameters: Type.Object({
        tier: Type.String({ description: "task tier 名（flash / pro / reasoner / fast / vl / hailuo）" }),
        providerId: Type.String({ description: "完整 provider/model id，如 deepseek/deepseek-v4-flash" }),
        priority: Type.Optional(Type.Number({ description: "新优先级（数值越小越优先）" })),
        weight: Type.Optional(Type.Number({ description: "新权重 0-100" })),
        enabled: Type.Optional(Type.Boolean({ description: "是否启用" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const tier = String(params.tier ?? "").trim();
        const providerId = String(params.providerId ?? "").trim();
        if (!tier || !providerId) {
          return { content: [{ type: "text" as const, text: "tier / providerId 必填。" }] };
        }
        const patch: Record<string, unknown> = {};
        if (typeof params.priority === "number") patch.priority = params.priority;
        if (typeof params.weight === "number") patch.weight = Math.max(0, Math.min(100, params.weight));
        if (typeof params.enabled === "boolean") patch.enabled = params.enabled;
        if (Object.keys(patch).length === 0) {
          return { content: [{ type: "text" as const, text: "需要至少一个字段（priority / weight / enabled）" }] };
        }
        const ok = patchProvider(runtimeConfig, tier, providerId, patch as any);
        if (!ok) {
          return {
            content: [{
              type: "text" as const,
              text: `未找到 tier='${tier}' / providerId='${providerId}'。运行 enhance_model_route_status 查现有列表。`,
            }],
          };
        }
        persistConfig();
        return {
          content: [{
            type: "text" as const,
            text: `✅ 已更新 ${tier} → ${providerId}：${JSON.stringify(patch)}\n配置文件：${getModelRouteConfigPath()}`,
          }],
        };
      },
    })) as any,
    { name: "enhance_model_route_set" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_model_route_mode",
      description:
        "切换路由模式。priority=严格按优先级 / weighted=按权重抽样 / speed=按最近延迟自动调权（v5.8.5+） / auto-task=按任务自动选 tier 内首选（默认） / cost-budget=优先成本最低（v6.1.4+，priority 升序选第一个，用户把便宜 model 放高 priority）。",
      parameters: Type.Object({
        mode: Type.Union(
          [
            Type.Literal("priority"),
            Type.Literal("weighted"),
            Type.Literal("speed"),
            Type.Literal("auto-task"),
          ],
          { description: "新模式" },
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const mode = String(params.mode ?? "").trim() as RouteMode;
        if (!["priority", "weighted", "speed", "auto-task", "cost-budget"].includes(mode)) {
          return { content: [{ type: "text" as const, text: `mode 必须是 priority / weighted / speed / auto-task / cost-budget` }] };
        }
        const old = runtimeConfig.mode;
        runtimeConfig.mode = mode;
        persistConfig();
        const note = mode === "speed"
          ? "（speed 模式 v5.8.5 才能收集 latency 数据；当前回退到 priority 兜底）"
          : "";
        return {
          content: [{
            type: "text" as const,
            text: `✅ 模式切换：\`${old}\` → \`${mode}\`${note}\n下次 LLM 调用立即生效。`,
          }],
        };
      },
    })) as any,
    { name: "enhance_model_route_mode" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_model_route_history",
      description:
        "查模型路由的历史延迟趋势（v5.8.6）。每次 latency tracker flush 同步 append 一条快照，" +
        "可看 P50/errRate 随时间变化（用 ASCII spark line 展示，便于判断 deepseek 是否在恢复 / minimax 高峰是否变慢）。",
      parameters: Type.Object({
        windowHours: Type.Optional(Type.Number({ description: "查最近多少小时（默认 24）" })),
        providerFilter: Type.Optional(Type.String({ description: "provider 子串过滤（如 'deepseek' / 'minimax'）" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const windowHours = typeof params.windowHours === "number" ? params.windowHours : 24;
        const filter = typeof params.providerFilter === "string" ? params.providerFilter : "";
        const snaps = readHistory({ windowHours, providerFilter: filter });
        if (snaps.length === 0) {
          return {
            content: [{
              type: "text" as const,
              text:
                `📭 history 暂无数据。\n` +
                `条件: 最近 ${windowHours}h${filter ? `, providerFilter='${filter}'` : ""}\n` +
                `文件: ${getHistoryPath()}\n` +
                `提示: latency tracker 至少要 5 样本/provider + 触发 flush 后才会写入 history。等几次 LLM 调用后再查。`,
            }],
          };
        }

        // 按 providerId 聚合时间序列
        const byProvider = new Map<string, Array<{ ts: string; p50: number; errRate: number; samples: number }>>();
        for (const snap of snaps) {
          for (const [pid, s] of Object.entries(snap.providers || {})) {
            if (filter && !pid.includes(filter)) continue;
            if (!byProvider.has(pid)) byProvider.set(pid, []);
            byProvider.get(pid)!.push({ ts: snap.ts, p50: s.p50Ms, errRate: s.errRate, samples: s.samples });
          }
        }

        const lines: string[] = [];
        lines.push(`# 模型路由历史 — 最近 ${windowHours}h${filter ? `（filter: \`${filter}\`）` : ""}`);
        lines.push(``);
        lines.push(`快照数: **${snaps.length}**　file: \`${getHistoryPath()}\``);
        lines.push(``);
        for (const [pid, series] of byProvider) {
          const p50s = series.map((s) => s.p50);
          const errs = series.map((s) => s.errRate);
          const latest = series[series.length - 1];
          const oldest = series[0];
          const p50Min = Math.min(...p50s);
          const p50Max = Math.max(...p50s);
          const avgErr = errs.reduce((a, b) => a + b, 0) / errs.length;
          lines.push(`## \`${pid}\``);
          lines.push(``);
          lines.push(`- **P50** spark: \`${sparkLine(p50s)}\`  范围 ${p50Min}-${p50Max}ms  最新 ${latest.p50}ms`);
          lines.push(`- **errRate** spark: \`${sparkLine(errs)}\`  平均 ${avgErr.toFixed(2)}  最新 ${latest.errRate.toFixed(2)}`);
          lines.push(`- 时间窗: ${oldest.ts} ~ ${latest.ts} (${series.length} 个采样点)`);
          lines.push(``);
        }
        return { content: [{ type: "text" as const, text: lines.join("\n") }] };
      },
    })) as any,
    { name: "enhance_model_route_history" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_model_route_disable",
      description:
        "批量禁用某个 provider（在所有 tier 中），或恢复某个 provider。" +
        "示例：providerPrefix='minimax' enabled=false 一刀禁掉所有 minimax。",
      parameters: Type.Object({
        providerPrefix: Type.String({ description: "provider 前缀（如 deepseek / minimax）或完整 id" }),
        enabled: Type.Boolean({ description: "true=启用 / false=禁用" }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const prefix = String(params.providerPrefix ?? "").trim();
        const enabled = params.enabled === true;
        if (!prefix) {
          return { content: [{ type: "text" as const, text: "providerPrefix 必填。" }] };
        }
        let touched = 0;
        const matched: string[] = [];
        for (const [, t] of Object.entries(runtimeConfig.models)) {
          for (const p of t.providers) {
            if (p.id === prefix || p.id.startsWith(prefix + "/")) {
              if (p.enabled !== enabled) {
                p.enabled = enabled;
                touched += 1;
              }
              matched.push(p.id);
            }
          }
        }
        if (touched === 0 && matched.length === 0) {
          return {
            content: [{
              type: "text" as const,
              text: `未匹配到 providerPrefix='${prefix}'。运行 enhance_model_route_status 查现有 provider id。`,
            }],
          };
        }
        persistConfig();
        const verb = enabled ? "启用" : "禁用";
        return {
          content: [{
            type: "text" as const,
            text: `✅ 已${verb} ${touched} 处（共匹配 ${matched.length} 处）\n匹配项: ${matched.join(", ")}`,
          }],
        };
      },
    })) as any,
    { name: "enhance_model_route_disable" },
  );

  // ── v6.1.5 ⭐ quota-aware ban 管理工具（2 个）─────────────────

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_model_route_ban_status",
      description:
        "查看当前因 quota-exhausted（HTTP 422/429/402 或'额度超限'类错误）被自动 ban 的 model 列表。" +
        "v6.1.5 新增：model_call_ended hook 检测到硬错时立刻 ban 1h，下次路由自动跳过该 model 选同模态/同 reasoning 备选。",
      parameters: Type.Object({}),
      async execute() {
        const banned = listBannedModels();
        if (banned.length === 0) {
          return {
            content: [{ type: "text" as const, text: "✅ 当前无 model 处于 quota-ban 期" }],
          };
        }
        const now = Date.now();
        const lines = ["⛔ 当前 quota-ban 列表：", ""];
        for (const e of banned) {
          const remainMin = Math.round((e.expireAt - now) / 60_000);
          lines.push(
            `  · ${e.providerId}`,
            `    触发: ${e.trigger}`,
            `    原因: ${e.reason.slice(0, 100)}${e.reason.length > 100 ? "..." : ""}`,
            `    剩余: ${remainMin} 分钟（自动恢复）`,
            `    手动解除: enhance_model_route_unban("${e.providerId}")`,
            "",
          );
        }
        return {
          content: [{ type: "text" as const, text: lines.join("\n") }],
          structuredContent: { banned },
        };
      },
    })) as any,
    { name: "enhance_model_route_ban_status" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_model_route_unban",
      description:
        "手动解除某个 model 的 quota-ban（默认 1h 自动恢复，但用户额度立刻补了的话可提前解）。" +
        "传 providerId 形如 'minimax/MiniMax-M2.7' 或 'deepseek/deepseek-v4-pro'。",
      parameters: Type.Object({
        providerId: Type.String({
          description: "<provider>/<model> 格式，如 minimax/MiniMax-M2.7",
        }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const id = String(params?.providerId ?? "").trim();
        if (!id) {
          return { content: [{ type: "text" as const, text: "❌ providerId 必填" }] };
        }
        const removed = unbanModel(id);
        if (!removed) {
          return {
            content: [{ type: "text" as const, text: `ℹ️ ${id} 不在 ban 列表（可能已自动过期或从未被 ban）` }],
          };
        }
        // 顺手清缓存让下次路由立刻能选回这个 model
        routeCache.clear();
        bestModelCache.clear();
        return {
          content: [{ type: "text" as const, text: `✅ 已解除 ${id} 的 quota-ban，路由器下次决策起可重新选它` }],
        };
      },
    })) as any,
    { name: "enhance_model_route_unban" },
  );

  // 暴露 reload，方便未来 enhance_loop 触发
  void reloadConfig;

  api.logger.info(
    `[enhance] 模型路由器 v6.1.5 已加载（before_model_resolve + model_call_ended hooks + 7 工具）| mode=${runtimeConfig.mode} | tiers=${Object.keys(runtimeConfig.models).join(",")} | latency tracker 在线（P50/P95/errRate 1h 滑窗）+ history 自动归档 + quota-aware ban（HTTP 422/429/402 + '额度超限' 关键词立即切）`,
  );
}
