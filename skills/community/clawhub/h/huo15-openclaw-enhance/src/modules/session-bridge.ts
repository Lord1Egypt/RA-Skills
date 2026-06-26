/**
 * 模块: Session Bridge — 跨 reset 把上次会话尾段的 user/assistant 对话拉回来当 prependContext
 *
 * 触发场景（issue #1 5/2 早晨 zhaobo 失忆事故复盘）：
 *   - 5/1 23:13:26 openclaw runtime 把 wecom:direct:zhaobo 的活跃 session 硬 reset
 *     （.jsonl 改名 .jsonl.reset.<ts>，新 session 起空白上下文）
 *   - enhance 已有的 before_reset hook 当时未触发（动作不是 reset 事件而是 hard wipe），
 *     lifecycle 抢救 = 0，session-recap 又只读 chapters/todos/decisions 这些结构化元数据
 *   - 用户次日感知到"openclaw 忘了昨天下午聊的内容"
 *
 * 本模块的策略：
 *   - 不依赖 hook 抢救（避免上面那种"reset 没发 before_reset"的盲区）
 *   - before_prompt_build 时主动扫 sessions/ 找 .jsonl.reset.* 文件
 *   - 用 chat_id (case-insensitive) 匹配同一会话伙伴 — 比 sessionKey 更鲁棒
 *     （sessionKey 大小写归一化跟原始 wecom userid 大小写偶尔不一致）
 *   - 拉末 N 条 message 拼成 prependContext 注入
 *
 * 红线：
 *   - 完全只读，不动龙虾任何状态（红线 #1）
 *   - 只读自己 + 龙虾 sessions/ 目录（红线 #2）
 *   - 不在插件代码里嵌 cli 命令（红线 #4 #5）
 *   - prependContext 只追加，绝不覆盖原 system prompt
 *   - 进程内 6h dedup 防止反复注入污染同一 session
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { DEFAULT_AGENT_ID } from "../types.js";

export interface SessionBridgeConfig {
  enabled?: boolean;
  /** prior 文件 mtime 距今需 ≥ 多少分钟才桥接（防止活跃流被自己重复注入），默认 75 */
  bridgeIdleMinutes?: number;
  /** 检索 prior session 文件的最大年龄（小时），默认 72（v6.1.9 起从 48 → 72，跨周末 OK） */
  priorMaxAgeHours?: number;
  /** 桥接的末 N 条 message，默认 20（v6.1.9 起从 8 → 20，跨夜大半天会话覆盖） */
  tailMessages?: number;
  /** 桥接文本字符上限（含模板），默认 12000（v6.1.9 起从 4000 → 12000，3x 容量） */
  maxChars?: number;
  /** 当前 session jsonl ≥ 多少字节就视为非 fresh、不再桥接，默认 200KB */
  freshSessionMaxBytes?: number;
  /** 调试日志 */
  debug?: boolean;
}

/** 同 (agentId,sessionId) 组合 6 小时内只桥接一次，防止重复污染同一会话上下文 */
const DEDUP_WINDOW_MS = 6 * 3600 * 1000;
const MAX_DEDUP_ENTRIES = 500;
const recentBridges = new Map<string, number>();

function shouldBridge(key: string): boolean {
  const now = Date.now();
  const last = recentBridges.get(key) ?? 0;
  if (now - last < DEDUP_WINDOW_MS) return false;
  if (recentBridges.has(key)) recentBridges.delete(key);
  while (recentBridges.size >= MAX_DEDUP_ENTRIES) {
    const oldest = recentBridges.keys().next().value;
    if (oldest === undefined) break;
    recentBridges.delete(oldest);
  }
  recentBridges.set(key, now);
  return true;
}

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return ((ctx?.agentId ?? DEFAULT_AGENT_ID) + "").trim() || DEFAULT_AGENT_ID;
}
function pickSessionKey(ctx: { sessionKey?: string } | undefined): string {
  return ((ctx?.sessionKey ?? "") + "").trim();
}
function pickSessionId(ctx: { sessionId?: string } | undefined): string {
  return ((ctx?.sessionId ?? "") + "").trim();
}

interface MessageEvent {
  role: string;
  text: string;
  timestamp?: string;
}

function extractText(content: unknown): string {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    let out = "";
    for (const block of content) {
      if (block && typeof block === "object") {
        const b = block as { type?: unknown; text?: unknown };
        if (b.type === "text" && typeof b.text === "string") out += b.text + " ";
      }
    }
    return out.trim();
  }
  if (content && typeof content === "object") {
    const b = content as { type?: unknown; text?: unknown };
    if (b.type === "text" && typeof b.text === "string") return b.text;
  }
  return "";
}

/**
 * 从 session jsonl 头部 64KB 内抽 chat_id 标识（用于跨 .jsonl.reset.* 找同会话伙伴）。
 *
 * v6.4.2: 多字段 fallback——OpenClaw runtime 不同版本 + 不同 channel 的 chat_id 命名不一：
 *   - `chat_id`（v5.x wecom direct，snake_case）
 *   - `chatid`（4.29+ wecom 群聊去掉下划线）
 *   - `chatId`（钉钉/微信服务号 camelCase）
 *   - cwd 兜底（最稳：cwd 里包含 wecom-default-group-XXX / wecom-direct-XXX 等动态 agent
 *     workspace 标识，跨版本/跨渠道都稳定；从 `"cwd":"..."` 字段抽末段路径名）
 *
 * 全 lowercase 归一化，匹配时大小写不敏感。
 */
function readChatId(filePath: string): string | null {
  try {
    const buf = readFileSync(filePath);
    const head = buf.slice(0, Math.min(buf.length, 64 * 1024)).toString("utf-8");
    // 优先 chat_id / chatid / chatId
    const m =
      head.match(/"chat_id"\s*:\s*"([^"]+)"/) ||
      head.match(/"chatid"\s*:\s*"([^"]+)"/) ||
      head.match(/"chatId"\s*:\s*"([^"]+)"/);
    if (m?.[1]) return m[1].toLowerCase();
    // fallback: cwd 里的 workspace 标识（wecom-default-group-XXX / wecom-direct-XXX 等）
    const cwdMatch = head.match(/"cwd"\s*:\s*"([^"]+)"/);
    if (cwdMatch?.[1]) {
      // 取 cwd 末段作为 key（如 ~/.openclaw/workspace-wecom-default-group-XXX → workspace-...）
      const tail = cwdMatch[1].split("/").filter(Boolean).pop();
      if (tail && tail.length > 0) return `cwd:${tail.toLowerCase()}`;
    }
    return null;
  } catch {
    return null;
  }
}

interface PriorCandidate {
  filePath: string;
  sessionId: string;
  mtimeMs: number;
  matchedChatId: string;
}

function findPriorBridgeSource(
  sessionsDir: string,
  currentChatId: string | null,
  currentSessionId: string,
  maxAgeMs: number,
): PriorCandidate | null {
  let entries: string[];
  try {
    entries = readdirSync(sessionsDir);
  } catch {
    return null;
  }

  type Cand = { path: string; sessionId: string; mtime: number };
  const cands: Cand[] = [];
  const now = Date.now();
  for (const e of entries) {
    if (!e.includes(".jsonl.reset.")) continue;
    const sessionId = e.split(".")[0];
    if (!sessionId || sessionId === currentSessionId) continue;
    const filePath = join(sessionsDir, e);
    let mtime = 0;
    try {
      mtime = statSync(filePath).mtimeMs;
    } catch {
      continue;
    }
    if (now - mtime > maxAgeMs) continue;
    cands.push({ path: filePath, sessionId, mtime });
  }
  cands.sort((a, b) => b.mtime - a.mtime);

  // v6.4.2: chat_id 严格匹配 → 命中优先（保留 v5.7.26 wecom direct 行为）
  if (currentChatId) {
    for (const c of cands) {
      const chatId = readChatId(c.path);
      if (!chatId) continue;
      if (chatId === currentChatId) {
        return {
          filePath: c.path,
          sessionId: c.sessionId,
          mtimeMs: c.mtime,
          matchedChatId: chatId,
        };
      }
    }
  }
  // v6.4.2: fallback 到 mtime 最新策略——agent 目录已 per-agent 隔离（动态派生
  // wecom-* / wechat-service-* / dingtalk-*）天然属于同一会话伙伴；chat_id 仅在
  // 多渠道 main agent 共用 sessions 时才有区分意义。当 chat_id null（OpenClaw 4.29+
  // 群聊场景常见）→ 直接选最新的 .jsonl.reset.*。
  if (cands.length > 0) {
    const c = cands[0];
    return {
      filePath: c.path,
      sessionId: c.sessionId,
      mtimeMs: c.mtime,
      matchedChatId: currentChatId ?? "(per-agent fallback)",
    };
  }
  return null;
}

function readLastMessages(
  filePath: string,
  count: number,
  perMsgCharCap: number,
): MessageEvent[] {
  let raw: string;
  try {
    raw = readFileSync(filePath, "utf-8");
  } catch {
    return [];
  }
  const lines = raw.split("\n");
  const out: MessageEvent[] = [];
  for (let i = lines.length - 1; i >= 0 && out.length < count; i--) {
    const line = lines[i];
    if (!line) continue;
    let d: any;
    try {
      d = JSON.parse(line);
    } catch {
      continue;
    }
    if (d?.type !== "message") continue;
    const role = typeof d?.message?.role === "string" ? d.message.role : "?";
    const text = extractText(d?.message?.content).trim();
    if (!text) continue;
    const timestamp = typeof d?.timestamp === "string" ? d.timestamp : undefined;
    out.unshift({
      role,
      text: text.replace(/\s+/g, " ").slice(0, perMsgCharCap),
      timestamp,
    });
  }
  return out;
}

function fmtAge(ms: number): string {
  const h = ms / 3600 / 1000;
  if (h < 24) return `${h.toFixed(1)} 小时前`;
  return `${(h / 24).toFixed(1)} 天前`;
}

function fmtTimestamp(ts?: string): string {
  if (!ts) return "";
  return ts.slice(0, 19).replace("T", " ");
}

function buildBridgeText(
  prior: PriorCandidate,
  msgs: MessageEvent[],
  totalCharCap: number,
): string {
  if (msgs.length === 0) return "";
  const ageStr = fmtAge(Date.now() - prior.mtimeMs);
  const lastMsgTime = msgs[msgs.length - 1]?.timestamp
    ? fmtTimestamp(msgs[msgs.length - 1].timestamp)
    : "";
  // v6.2.0 ⭐ PRIOR_SESSION_CHECKPOINT banner：明确告诉 LLM 这是"延续"，不是"当下要回应的新内容"。
  // 实测痛点：v5.7.26 + v6.1.9 注入了 prependContext 但 LLM 不知是历史 → 被动用、不主动检索。
  // 给清晰 banner + 完整 jsonl 路径，让 LLM 知道：① 这是上一段的尾段 ② 需要更多上下文可以 Read 整个文件。
  const lines: string[] = [
    "🔄 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    `   PRIOR_SESSION_CHECKPOINT —— 上一段会话的尾段（${ageStr}）`,
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "",
    `当前 session 因 OpenClaw runtime 硬 reset / compact 跟上文断了。enhance session-bridge 自动从前一个 session 文件拉回最后 ${msgs.length} 条 user/assistant 原始对话——**这是历史延续，不是用户当下的新请求**。`,
    "",
    `**前 session 完整文件**（需要中段/决策/tool result 时 Read 这个）：\`${prior.filePath}\``,
    lastMsgTime ? `**最后一条消息时间**：${lastMsgTime}` : "",
    "",
    "**使用建议**：",
    "1. 用户没明示『延续昨天的话题』时，先把这段当作背景理解，不要主动 echo / 复述",
    "2. 需要更多上下文 → 主动 Read 上面那个完整 jsonl 文件（或 enhance_transcript_search）",
    "3. 重要决策 / 进展 / 用户偏好 → 调 `enhance_memory_store` 记到分类记忆，避免下次 reset 又得重新拉",
    "",
    "──── 历史尾段 message ────",
    "",
  ];
  let acc = lines.join("\n").length;
  for (const m of msgs) {
    const head = `· [${m.role}${m.timestamp ? `@${fmtTimestamp(m.timestamp)}` : ""}]`;
    const piece = `${head} ${m.text}`;
    if (acc + piece.length + 1 > totalCharCap) {
      lines.push("");
      lines.push("…（后续被字数上限截断；需要全文请 Read 上面那个完整 jsonl 文件，或调 enhance_transcript_search）");
      break;
    }
    lines.push(piece);
    acc += piece.length + 1;
  }
  lines.push("");
  lines.push("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  lines.push(
    "(由 @huo15/openclaw-enhance session-bridge 自动注入；可在 enhance.sessionBridge.enabled=false 关闭)",
  );
  return lines.join("\n");
}

export function registerSessionBridge(
  api: OpenClawPluginApi,
  config?: SessionBridgeConfig,
) {
  if (config?.enabled === false) return;

  const home = resolveOpenClawHome(api);
  const idleMinutes = config?.bridgeIdleMinutes ?? 75;
  // v6.1.9: 默认值 3x 扩容（48h→72h, 8msg→20msg, 4000字→12000字）
  // 触发：用户报"第二天失忆严重"。诊断：session-bridge 在跑但 4KB 窗口太小，
  // 跨夜的项目背景/决策/上下文全在窗口外丢失。3x 扩容覆盖大半天会话。
  // 实测验证：v6.1.0 实测一个会话 jsonl tail 20msg ≈ 8-10KB 中文文本，给 12000 字
  // 上限留 20-50% buffer 不会截断到信息丢失。
  const priorMaxAgeMs = (config?.priorMaxAgeHours ?? 72) * 3600_000;
  const tailN = config?.tailMessages ?? 20;
  const maxChars = config?.maxChars ?? 12000;
  const freshMaxBytes = config?.freshSessionMaxBytes ?? 200 * 1024;
  const debug = config?.debug === true;
  const perMsgCap = Math.max(120, Math.floor(maxChars / Math.max(1, tailN)));

  api.on("before_prompt_build", (_event: unknown, ctx: any) => {
    try {
      const agentId = pickAgentId(ctx);
      const sessionKey = pickSessionKey(ctx);
      const sessionId = pickSessionId(ctx);
      if (!sessionKey || !sessionId) return undefined;

      const dedupKey = `${agentId}::${sessionId}`;
      // 不立刻 mark — 只有真正注入了内容才 mark（早返回不消耗冷却）
      const cooldownActive = (() => {
        const last = recentBridges.get(dedupKey) ?? 0;
        return Date.now() - last < DEDUP_WINDOW_MS;
      })();
      if (cooldownActive) return undefined;

      const sessionsDir = join(home, "agents", agentId, "sessions");

      // 仅对"fresh session"桥接：当前 jsonl 体量低（说明刚起没几轮）
      const currentJsonl = join(sessionsDir, `${sessionId}.jsonl`);
      let currentSize = 0;
      try {
        currentSize = statSync(currentJsonl).size;
      } catch {
        return undefined; // 当前 session 文件还没建 — 太早了
      }
      if (currentSize > freshMaxBytes) return undefined;

      // v6.4.2: chat_id 允许 null。当前 jsonl 头扫到 chat_id（wecom direct 等）→ 严格匹配；
      // 没扫到（OpenClaw 4.29+ 群聊场景，chat_id 不在 jsonl 头里）→ findPriorBridgeSource
      // 走 mtime 最新策略（agent 目录已 per-agent 隔离，足够稳）。
      const currentChatId = readChatId(currentJsonl);

      const prior = findPriorBridgeSource(sessionsDir, currentChatId, sessionId, priorMaxAgeMs);
      if (!prior) return undefined;

      // idle 阈值：prior 文件 mtime 距今足够久（避免活跃同步流被自己注入）
      const idleMs = Date.now() - prior.mtimeMs;
      if (idleMs < idleMinutes * 60_000) return undefined;

      const msgs = readLastMessages(prior.filePath, tailN, perMsgCap);
      if (msgs.length === 0) return undefined;

      const text = buildBridgeText(prior, msgs, maxChars);
      if (!text) return undefined;

      shouldBridge(dedupKey); // 真正注入后才 mark 冷却
      if (debug) {
        api.logger.info(
          `[enhance-session-bridge] 桥接 prior=${prior.sessionId.slice(0, 8)}…(${msgs.length} msg, ${text.length} 字符), idle=${(idleMs / 60000).toFixed(0)}min, sessionKey=${sessionKey}`,
        );
      }
      return { prependContext: text };
    } catch (err) {
      api.logger.error(`[enhance-session-bridge] 错误: ${(err as Error).message}`);
      return undefined;
    }
  });

  api.logger.info(
    `[enhance] session-bridge 已加载（fresh<${(freshMaxBytes / 1024).toFixed(0)}KB & idle≥${idleMinutes}min & prior≤${(priorMaxAgeMs / 3600_000).toFixed(0)}h → tail ${tailN}msg/${maxChars}字 注入 prependContext）`,
  );
}
