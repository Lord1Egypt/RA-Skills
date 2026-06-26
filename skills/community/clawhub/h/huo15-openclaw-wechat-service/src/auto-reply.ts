/**
 * **自动回复模块（v2.2.0+）**
 *
 * 在 agent dispatch 之前执行的关键词匹配 & 业务时间检查。
 *
 * 配置路径：`channels["wechat-service"].autoReply`
 *
 * 功能：
 *  1. **关键词匹配**：用户消息完全匹配关键词 → 直接回复（不经 agent，节省 token）
 *  2. **业务时间检查**：非工作时间 → 自动回复提示
 *  3. **欢迎语模板**：subscribe 事件 → 渲染模板后下发
 *
 * 处理流程：
 *  webhook handler → checkAutoReply() → 命中则直接发送客服消息并返回 true
 *  → 未命中则正常走 agent dispatch
 */

import type { OpenClawConfig } from "openclaw/plugin-sdk";

import { CONFIG_SECTION_KEY, LEGACY_CONFIG_SECTION_KEY } from "./config/index.js";
import type {
  WechatServiceAutoReplyConfig,
  WechatServiceBusinessHoursSchedule,
  WechatServiceInboundMessage,
} from "./types.js";

// ============================================================================
// 配置读取
// ============================================================================

function readAutoReplyConfig(cfg: OpenClawConfig): WechatServiceAutoReplyConfig | undefined {
  const channels = (cfg as { channels?: Record<string, unknown> })?.channels;
  const section =
    (channels?.[CONFIG_SECTION_KEY] as { autoReply?: WechatServiceAutoReplyConfig } | undefined) ??
    (channels?.[LEGACY_CONFIG_SECTION_KEY] as { autoReply?: WechatServiceAutoReplyConfig } | undefined);
  return section?.autoReply;
}

// ============================================================================
// 关键词匹配
// ============================================================================

export type KeywordMatchResult =
  | { matched: true; reply: string }
  | { matched: false };

/**
 * **关键词匹配模式（v2.3.3+）**
 *
 * 旧版仅支持完全匹配（`content === keyword`），导致"Odoo 怎么学？"无法命中
 * "Odoo" 关键词，运营每个变体都要手工列举一遍。v2.3.3 引入 glob 通配：
 *
 *  - `"你好"` → **exact**（完全匹配）：`content === "你好"`
 *  - `"*Odoo*"` → **contains**：`content.includes("Odoo")`（大小写不敏感）
 *  - `"价格*"` → **prefix**：`content.startsWith("价格")`
 *  - `"*多少钱"` → **suffix**：`content.endsWith("多少钱")`
 *
 * 匹配优先级：先 exact 全扫一遍，未命中再扫通配。这样运营写
 *   `{ "价格": "...固定问候...", "*价格*": "...含价格的通用引导..." }`
 * 时，"价格" 走前者，"我想问下价格多少" 走后者。
 *
 * 大小写不敏感：中文不受影响；英文 keyword "Odoo" 能命中 "odoo 怎么学"。
 */
type MatchMode = "exact" | "contains" | "prefix" | "suffix";

function classifyKeyword(raw: string): { pattern: string; mode: MatchMode } {
  const trimmed = raw.trim();
  if (trimmed.length >= 2 && trimmed.startsWith("*") && trimmed.endsWith("*")) {
    return { pattern: trimmed.slice(1, -1), mode: "contains" };
  }
  if (trimmed.startsWith("*")) {
    return { pattern: trimmed.slice(1), mode: "suffix" };
  }
  if (trimmed.endsWith("*")) {
    return { pattern: trimmed.slice(0, -1), mode: "prefix" };
  }
  return { pattern: trimmed, mode: "exact" };
}

function matches(content: string, pattern: string, mode: MatchMode): boolean {
  if (!pattern) return false;
  const c = content.toLowerCase();
  const p = pattern.toLowerCase();
  switch (mode) {
    case "exact": return content === pattern || c === p;
    case "contains": return c.includes(p);
    case "prefix": return c.startsWith(p);
    case "suffix": return c.endsWith(p);
  }
}

/**
 * 检查用户消息是否命中配置的关键词。
 * 仅对 text 类型消息生效。
 *
 * 匹配规则：
 *  1. 先按 keys 顺序扫所有 **exact** 关键词（保留旧版精确匹配的语义 + 优先级）
 *  2. 都未命中，再按 keys 顺序扫 **通配** 关键词（contains / prefix / suffix）
 *  3. 第一个命中即返回；后续关键词不再尝试
 */
export function matchKeyword(
  cfg: OpenClawConfig,
  inbound: WechatServiceInboundMessage,
): KeywordMatchResult {
  if (inbound.msgType !== "text" || !inbound.content) {
    return { matched: false };
  }

  const autoReply = readAutoReplyConfig(cfg);
  const keywords = autoReply?.keywords;
  if (!keywords || typeof keywords !== "object") {
    return { matched: false };
  }

  const content = inbound.content.trim();
  const entries = Object.entries(keywords).filter(
    (e): e is [string, string] => typeof e[1] === "string",
  );

  // 第一轮：exact 优先（向后兼容 v2.3.2 之前的语义）
  for (const [keyword, reply] of entries) {
    const { pattern, mode } = classifyKeyword(keyword);
    if (mode === "exact" && matches(content, pattern, mode)) {
      return { matched: true, reply };
    }
  }

  // 第二轮：通配（contains / prefix / suffix）
  for (const [keyword, reply] of entries) {
    const { pattern, mode } = classifyKeyword(keyword);
    if (mode !== "exact" && matches(content, pattern, mode)) {
      return { matched: true, reply };
    }
  }

  return { matched: false };
}

// ============================================================================
// 业务时间检查
// ============================================================================

/**
 * 检查当前时间是否在业务时间内。
 *
 * schedule 示例：`{ days: [1,2,3,4,5], start: "09:00", end: "18:00" }`
 * days: 0=周日, 1=周一 ... 6=周六
 */
export function isBusinessHours(
  cfg: OpenClawConfig,
  now?: Date,
): boolean {
  const autoReply = readAutoReplyConfig(cfg);
  const bh = autoReply?.businessHours;
  if (!bh?.schedule || bh.schedule.length === 0) {
    return true; // 未配置业务时间 → 始终视为工作时间
  }

  const current = now ?? new Date();
  const dayOfWeek = current.getDay(); // 0=Sun, 1=Mon ...
  const currentMinutes = current.getHours() * 60 + current.getMinutes();

  for (const entry of bh.schedule) {
    if (!entry.days || !Array.isArray(entry.days)) continue;
    if (!entry.days.includes(dayOfWeek)) continue;

    const startMinutes = parseTimeToMinutes(entry.start);
    const endMinutes = parseTimeToMinutes(entry.end);
    if (startMinutes == null || endMinutes == null) continue;

    if (currentMinutes >= startMinutes && currentMinutes < endMinutes) {
      return true;
    }
  }

  return false;
}

function parseTimeToMinutes(time: string): number | null {
  const parts = time.trim().split(":");
  if (parts.length !== 2) return null;
  const h = Number(parts[0]);
  const m = Number(parts[1]);
  if (!Number.isFinite(h) || !Number.isFinite(m)) return null;
  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
  return h * 60 + m;
}

/**
 * 获取非工作时间提示消息。
 */
export function getOffHoursMessage(cfg: OpenClawConfig): string | undefined {
  const autoReply = readAutoReplyConfig(cfg);
  const msg = autoReply?.businessHours?.offHoursMessage?.trim();
  return msg || undefined;
}

// ============================================================================
// 欢迎语模板
// ============================================================================

/**
 * 渲染欢迎语模板。
 *
 * 支持变量：
 *  - `{{nickname}}` → 用户昵称（如果有）
 *  - `{{date}}` → 当前日期（YYYY-MM-DD）
 */
export function renderWelcomeText(
  cfg: OpenClawConfig,
  nickname?: string,
): string | undefined {
  const autoReply = readAutoReplyConfig(cfg);
  const template = autoReply?.welcomeText?.trim();
  if (!template) return undefined;

  const now = new Date();
  const dateStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;

  return template
    .replace(/\{\{nickname\}\}/g, nickname || "用户")
    .replace(/\{\{date\}\}/g, dateStr);
}

// ============================================================================
// 统一入口
// ============================================================================

export type AutoReplyResult =
  | { handled: true; reply: string }
  | { handled: false };

/**
 * **checkAutoReply** —— 统一自动回复入口。
 *
 * 由 webhook handler 在 agent dispatch 之前调用。
 * 命中则直接通过客服消息回复（不经过 agent），返回 `{ handled: true }`。
 *
 * 检查顺序：
 *  1. 关键词匹配（优先级最高）
 *  2. 业务时间检查
 */
export function checkAutoReply(
  cfg: OpenClawConfig,
  inbound: WechatServiceInboundMessage,
): AutoReplyResult {
  // 仅对用户主动发的文本消息做关键词匹配
  const keywordResult = matchKeyword(cfg, inbound);
  if (keywordResult.matched) {
    return { handled: true, reply: keywordResult.reply };
  }

  // 业务时间检查：对文本消息检查是否非工作时间
  if (inbound.msgType === "text" && !isBusinessHours(cfg)) {
    const offMsg = getOffHoursMessage(cfg);
    if (offMsg) {
      return { handled: true, reply: offMsg };
    }
  }

  return { handled: false };
}
