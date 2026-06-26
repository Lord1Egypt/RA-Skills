/**
 * 模块: 蓝火 / cc-media-bridge 派活 harness — 真原生 CC 会话强制（v6.x）
 *
 * 痛点：用户在 wecom 群说「蓝火 修 X」/「蓝火 做 PPT」时，LLM 会本能选错路：
 *   - sessions_spawn(agentId="claude", runtime="acp") — ACP 子 agent，不是真原生 CC
 *   - Task tool / mcp__ccd_session__spawn_task — Claude Code Task 子 agent
 *   - Bash "claude -p ..." / "claude --resume ..." — 直接 exec，绕开 cc-media-task
 *   - 或自己用 Write+Bash 把活做了 — 截胡，用户明明指名让蓝火干
 *
 * SKILL 命令式（v2.10.5+）+ 反模式列表 + harness 思想 L4 (cc-bridge-pre-fetch
 * for query) 都治不住 dispatch — 因为 query 是"读"，dispatch 是"写"，写路径
 * 没人钉死。
 *
 * 这模块就是 dispatch 路径的 hook 级钉死：
 *   1. before_prompt_build：检测"蓝火+动词"模式 → 标记 session 进入 dispatch
 *      lockdown 窗口（默认 90s），同时 prependContext 注入硬约束："必须 Bash
 *      cc-media-task --owner ... --desc ... ，禁止 sessions_spawn / Task /
 *      exec claude / Write+Bash 干"
 *   2. before_tool_call：会话在 lockdown 窗口里时，凡是 toolName 在 blocklist
 *      就直接 block（return { block:true, blockReason }），并在 reason 里告诉
 *      LLM 怎么改对——下一轮 LLM 会读到 blockReason 然后走 Bash cc-media-task
 *   3. 一旦看到正确路径（Bash 命令含 "cc-media-task"）就清掉 lockdown 标记
 *
 * 红线：
 *   - capability detection: ~/.openclaw-media-bridge 不存在则跳过整个模块
 *   - 零 child_process / 零 fs 写
 *   - lockdown 只对 dispatch 触发后短窗口生效（默认 90s 或正确派活立解），
 *     避免 false positive 拦其他工具调用
 *   - blocklist 只拦"明显错路"，留 Bash / Write / Read 等正常路径
 */

import { existsSync } from "node:fs";
import { join } from "node:path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

const BRIDGE_STATE_DIR = ".openclaw-media-bridge";

// 触发派活意图的正则 —— 三种命中路径任一即触发：
//   1. EXPLICIT: 显式"蓝火/虾任务/龙任务/..." + 派活动词
//   2. AT_BOT: 群聊 @bot 名（@贾维斯/@Jarvis/...）+ 派活动词 — 用户实际最常用的模式
//   3. PURE_DISPATCH: 长任务关键词（创建/新建/拆分/重构/做一份/帮我.../写一个...）
// （v6.4.2 扩大）
const TRIGGER_NOUN = /(蓝火|虾任务|龙任务|发给龙虾|cc[\s-]?task|媒桥)/i;
const AT_BOT = /@(贾维斯|Jarvis|jarvis|机器人|bot|huo15|蓝火)/i;
const DISPATCH_VERB =
  /(帮我|帮你|做一|做下|做个|做份|写一|写个|写份|改一|改下|改个|继续|优化|创建|新建|拆分|生成|制作|分析|修复|修一下|修个|搞一|搞下|搞个|搭建|实现|完善|整理|发给我|发我|debug|fix|implement|build|create|让.{1,5}做|跑一下|跑一个|跑个|来一|来个)/;

// 被拦截的"错路"工具名清单（精确匹配，可加 prefix）
const BLOCKED_TOOLS = new Set<string>([
  "sessions_spawn",       // OpenClaw 原生 subagent 派发
  "Task",                 // Claude Code Task tool（在 CC 内不会走到 OpenClaw hook，但保险）
  "spawn_task",           // 直接命名
]);
const BLOCKED_TOOL_PREFIXES = [
  "mcp__ccd_session__spawn_task",  // Claude Code session manager 的 spawn_task
];
// Bash 命令体白名单 inverse —— Bash 是允许的，但命令里不能直接 exec claude CLI
const BASH_DENIED_RE = /\b(?:claude(?:\s+-p|\s+--resume|\s+chat|\s+code)|npx\s+@anthropic-ai\/claude-code)\b/;

// session-key → dispatch lockdown 解锁时间（毫秒）
const _lockdown = new Map<string, number>();
const LOCKDOWN_MS = 90_000;

function bridgeInstalled(): boolean {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) return false;
  return existsSync(join(home, BRIDGE_STATE_DIR));
}

function isInLockdown(sessionKey: string | undefined): boolean {
  if (!sessionKey) return false;
  const exp = _lockdown.get(sessionKey);
  if (!exp) return false;
  if (Date.now() > exp) {
    _lockdown.delete(sessionKey);
    return false;
  }
  return true;
}

function setLockdown(sessionKey: string | undefined) {
  if (!sessionKey) return;
  _lockdown.set(sessionKey, Date.now() + LOCKDOWN_MS);
}

function clearLockdown(sessionKey: string | undefined) {
  if (!sessionKey) return;
  _lockdown.delete(sessionKey);
}

function renderHarnessPrompt(matchKind: "explicit" | "at_bot"): string {
  const intro = matchKind === "explicit"
    ? "用户消息显式含「蓝火 / 虾任务 / 龙任务」+ 派活动词。"
    : "用户在 IM 群聊 @<bot 名>（贾维斯/Jarvis/...）+ 派活动词——这是**派活意图**，不是闲聊。";
  return [
    "## 🔒 [蓝火 dispatch harness — enhance plugin 自动钉死，不是 LLM 编造]",
    "",
    intro,
    "**这是 DISPATCH 派活模式**：必须真原生 CC 会话产出，进 dashboard 列表，owner_id 可追踪。",
    "",
    "**唯一允许的路径**：调用 Bash 工具，命令为：",
    "```bash",
    "cc-media-task --owner \"wecom:<sender_id>\" --desc \"<把用户原话+上下文整理成清晰任务描述>\" --background",
    "# --background：父进程秒返回 task_id，群里不阻塞，dashboard 实时看进度",
    "# 有附件：--image /path  --file /path  --audio /path",
    "```",
    "",
    "**enhance plugin 已经在 hook 层钉死了以下错路 — 你调它们会被 block，next-turn 看到 blockReason 才回头**：",
    "- ❌ `sessions_spawn(agentId=\"claude\", runtime=\"acp\")` — ACP 子 agent 不是真原生 CC，绕过 dashboard",
    "- ❌ `mcp__ccd_session__spawn_task(...)` / 任何 spawn_task 工具 — 同上",
    "- ❌ Bash `claude -p ...` / `claude --resume ...` / `npx @anthropic-ai/claude-code ...` — 直接 exec 绕过 wrapper",
    "- ❌ 用 Write+Bash/Edit/MultiEdit 自己把任务做了 — 用户在 IM 群里下任务，你不能截胡，必须派给蓝火",
    "- ❌ 用其它 skill (PPT / 文档 / 报表 等内置 skill) 替代蓝火 — 派活类一律走 cc-media-task",
    "",
    "**判定捷径**：用户在群里 @你 + 任何动词意图（帮我/做/写/改/创建/新建/拆分/优化/...） → **唯一动作是 Bash `cc-media-task`**。",
    "",
    "**怎么拿 sender_id**：从 user message 前缀的 `Conversation info` JSON 块取 `sender_id`，channel 从 system prompt `Inbound Context` 取。",
    "",
    "**例外（仅这些情况可以你自己直接答）**：",
    "- 纯查询：列任务 / 查状态 / 看历史（这些走 cc_session_list 等 MCP 工具，不派 cc-media-task）",
    "- 明确陈述/疑问：「下周要干的事情...」、「fork 哪个仓库」（无派活动词的咨询/陈述）",
    "- 用户明确说「你直接做」/「不用蓝火」",
  ].join("\n");
}

export function registerCcBridgeDispatchHarness(api: OpenClawPluginApi) {
  if (!bridgeInstalled()) {
    api.logger.info(
      "[enhance-cc-dispatch-harness] cc-media-bridge 未装（~/.openclaw-media-bridge 不存在），跳过 dispatch harness",
    );
    return;
  }

  // ── Hook 1: before_prompt_build —— 检测 dispatch 模式 + 注入硬约束 + 设 lockdown ──
  // v6.4.2 三路命中（任一即触发）：
  //   1. EXPLICIT: 用户显式说「蓝火/虾任务/...」+ 派活动词（最严格）
  //   2. AT_BOT: 用户 @<bot 名>（贾维斯/Jarvis/...）+ 派活动词（群聊里最常见）
  //   3. （未来）按 chattype 区分群/单独
  api.on("before_prompt_build", (event: any, ctx: any) => {
    const userMessage: string = (event as any)?.prompt ?? "";
    if (!userMessage || userMessage.length > 2000) return {};

    if (!DISPATCH_VERB.test(userMessage)) return {}; // 没动词意图 = 闲聊/陈述/查询，不触发
    const explicit = TRIGGER_NOUN.test(userMessage);
    const atBot = AT_BOT.test(userMessage);
    if (!explicit && !atBot) return {};

    // 命中：标记本 session 进入 dispatch lockdown 窗口
    const sessionKey: string | undefined =
      ctx?.sessionKey ?? ctx?.sessionId ?? ctx?.agentId ?? undefined;
    setLockdown(sessionKey);

    const matchKind: "explicit" | "at_bot" = explicit ? "explicit" : "at_bot";
    api.logger.info?.(
      `[enhance-cc-dispatch-harness] 命中 dispatch 模式 [${matchKind}]（session=${(sessionKey || "?").slice(-12)}）："${userMessage.slice(0, 60)}..."；注入硬约束 + 90s lockdown`,
    );

    return {
      prependContext: renderHarnessPrompt(matchKind),
    };
  });

  // ── Hook 2: before_tool_call —— lockdown 窗口里拦"错路"工具调用 ──
  api.on("before_tool_call", (event: any, ctx: any) => {
    const sessionKey: string | undefined =
      ctx?.sessionKey ?? ctx?.sessionId ?? ctx?.agentId ?? undefined;
    if (!isInLockdown(sessionKey)) return {};

    const toolName: string = event?.toolName ?? ctx?.toolName ?? "";
    const params: Record<string, unknown> = event?.params ?? {};

    // 正确路径：Bash + 命令含 "cc-media-task" → 解锁 + 放行
    if (toolName === "Bash") {
      const cmd = String((params as any)?.command ?? "").trim();
      if (cmd.includes("cc-media-task")) {
        clearLockdown(sessionKey);
        api.logger.info?.(
          `[enhance-cc-dispatch-harness] 检测到 Bash cc-media-task 调用，dispatch 已正确派出，清 lockdown`,
        );
        return {};
      }
      // Bash 但命令是直接 exec claude CLI → block
      if (BASH_DENIED_RE.test(cmd)) {
        api.logger.warn?.(
          `[enhance-cc-dispatch-harness] BLOCK Bash 直跑 claude："${cmd.slice(0, 100)}"`,
        );
        return {
          block: true,
          blockReason:
            "蓝火 dispatch 模式禁止直接 exec claude CLI（绕开 cc-media-task wrapper 会丢 dashboard 记录 / owner 隔离 / 实时进度回写）。立刻改为：Bash `cc-media-task --owner \"wecom:<sender_id>\" --desc \"...\"`",
        };
      }
      // 其它 Bash 放行（用户可能在做附件预处理 / 检查文件等）
      return {};
    }

    // sessions_spawn / spawn_task / Task → block
    if (BLOCKED_TOOLS.has(toolName)) {
      api.logger.warn?.(
        `[enhance-cc-dispatch-harness] BLOCK ${toolName}（dispatch 模式禁 spawn 子 agent）`,
      );
      return {
        block: true,
        blockReason: `蓝火 dispatch 模式禁止 ${toolName}（spawn 子 agent 不是真原生 CC 会话——会丢 dashboard 记录 / owner 隔离 / 实时进度）。立刻改为：Bash \`cc-media-task --owner "wecom:<sender_id>" --desc "<任务描述>"\``,
      };
    }
    for (const prefix of BLOCKED_TOOL_PREFIXES) {
      if (toolName.startsWith(prefix)) {
        api.logger.warn?.(
          `[enhance-cc-dispatch-harness] BLOCK ${toolName}（前缀 ${prefix}）`,
        );
        return {
          block: true,
          blockReason: `蓝火 dispatch 模式禁止 ${toolName}（spawn 类工具）。立刻改为：Bash \`cc-media-task --owner "wecom:<sender_id>" --desc "..."\``,
        };
      }
    }

    return {};
  }, { priority: 950 } as any);

  api.logger.info(
    "[enhance-cc-dispatch-harness] dispatch harness 已注册（蓝火+动词触发 90s lockdown，期间禁 sessions_spawn/Task/spawn_task/exec claude）",
  );
}
