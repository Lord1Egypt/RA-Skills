/**
 * 模块: 蓝火 / cc-media-bridge dashboard 引导（v6.1.5）
 *
 * 给 LLM 注入 prompt supplement，强约束：当响应里出现 cc-media-bridge 任务
 * （列表 / 详情 / 状态 / 完成卡片）时，**末尾必附** dashboard URL。
 *
 * Why: cc-media-bridge 跑出来的 claude CLI session 不会进 Claude App 的
 * pinned/recents（IndexedDB 白名单只认 App 内启动的）→ 用户唯一可视化入口
 * 是 bridge 自带的 /dashboard。SKILL.md 已经写过这条规则但属"按需加载"，
 * 真正每次都注入到 system prompt 的是这个 supplement（pushy 强约束）。
 *
 * 红线：
 *   - capability detection: 仅 cc-media-bridge 装在本机时（~/.openclaw-media-bridge/
 *     存在）才注入，避免 enhance 单装用户看到无意义指令
 *   - baseUrl 跟 bot-share-link 共享配置（~/.openclaw/share/config.json + env BOT_BASE_URL）
 *   - 零 child_process（红线 #4） / 零 fs 写
 *   - 零 cc-media-bridge 代码 import（capability by filesystem path，不强 require）
 */

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { resolveOpenClawHome } from "../utils/resolve-home.js";

const BRIDGE_STATE_DIR = ".openclaw-media-bridge";

function bridgeInstalled(): boolean {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) return false;
  // bridge LaunchAgent / setup.sh 跑过的标志：~/.openclaw-media-bridge/ 自动创建（DB 落这里）
  if (existsSync(join(home, BRIDGE_STATE_DIR))) return true;
  // 兜底：cc-media-task 命令存在
  return existsSync(join(home, ".local", "bin", "cc-media-task"));
}

function resolveDashboardBaseUrl(api: OpenClawPluginApi): string {
  // 优先级（与 bot-share-link 一致）：env BOT_BASE_URL > ~/.openclaw/share/config.json > localhost
  const env = process.env.BOT_BASE_URL?.trim();
  if (env) return env.replace(/\/+$/, "");
  try {
    const cfgPath = join(resolveOpenClawHome(api), "share", "config.json");
    if (existsSync(cfgPath)) {
      const cfg = JSON.parse(readFileSync(cfgPath, "utf-8")) as {
        baseUrl?: string;
      };
      const base = cfg?.baseUrl?.trim();
      if (base) return base.replace(/\/+$/, "");
    }
  } catch {
    // ignore — 走 fallback
  }
  return "http://127.0.0.1:18790";
}

export function registerCcBridgePrompt(api: OpenClawPluginApi) {
  if (!bridgeInstalled()) {
    api.logger.info(
      "[enhance-cc-bridge-prompt] cc-media-bridge 未装（~/.openclaw-media-bridge 和 ~/.local/bin/cc-media-task 都不存在），跳过 prompt supplement",
    );
    return;
  }
  if (typeof api.registerMemoryPromptSupplement !== "function") {
    api.logger.warn(
      "[enhance-cc-bridge-prompt] api.registerMemoryPromptSupplement 不可用，跳过",
    );
    return;
  }
  try {
    api.registerMemoryPromptSupplement(() => {
      const base = resolveDashboardBaseUrl(api);
      const isLocal = base.startsWith("http://127.0.0.1") || base.startsWith("http://localhost");
      return [
        "## 蓝火（cc-media-bridge）任务响应 — dashboard 链接附带规则",
        `- 蓝火 / 虾任务（cc-media-task）跑出来的 session **不会**出现在 Claude App 的 pinned/recents 面板（IndexedDB 白名单只认 App 内启动的会话）。用户唯一的可视化入口是 bridge 自带 dashboard：${base}/lanhuo`,
        ``,
        `**严格条件触发（仅以下情况才附 dashboard 链接）**：`,
        `① 你的响应里**已包含**一个或多个 \`cc-YYYYMMDD-HHMMSS-XXXX\` 格式的 task ID — 列表 / 单条详情 / 状态 / 进度 / 完成卡片 / SSE 事件流摘要`,
        `② 用户**显式问** dashboard / 蓝火链接 / 在哪查看`,
        `③ 你**真派活了**（调了 Bash cc-media-task 或 hook 派的蓝火任务）`,
        ``,
        `**附法**：`,
        `  - 任务列表（多条 task） → ${base}/lanhuo`,
        `  - 单条任务（带具体 task ID）→ ${base}/lanhuo?task=<完整 task ID>`,
        ``,
        `**禁止条件 — 普通对话不要附 dashboard 链接**：`,
        `❌ 用户问普通问题（讲解 / 总结 / 文档分析 / 闲聊 / 不涉及蓝火任务）→ **绝不附**`,
        `❌ 你只是回答了一个问题、没派活、没列任务 → **绝不附**`,
        `❌ 用户上传 PDF / 图片让你看内容 → **绝不附**（除非内容里就是任务）`,
        `❌ 写成 \`/dashboard\` 路径（已 v2.18.6 废弃 301→/lanhuo），dashboard 唯一规范路径是 **\`/lanhuo\`**`,
        ``,
        `**严格区分：/lanhuo 跟 /plugins/enhance/upload 是不同 URL（v6.7.8）**：`,
        `📊 \`/lanhuo\` = 蓝火任务 dashboard（看 cc-media-task 进度 / 历史，**不是**上传页）`,
        `📎 \`/plugins/enhance/upload\` = 共享上传页（无 token，AI 不知道是谁传了什么；仅适合快速一次性）`,
        `🔐 **首选：调 \`enhance_upload_link\` 工具拿 token 化 URL**（\`/plugins/enhance-upload/<token>\`，AI 通过 enhance_upload_check 能查清单）`,
        `❌ /upload 和 /lanhuo/upload 都不可用（v6.7.8 已删，前者被 OpenClaw SPA 截，后者跟 cc-media-bridge namespace 混淆）`,
        `**不要混用**：用户问任务状态 → 给 /lanhuo；用户要上传大文件 → 调 enhance_upload_link 工具拿 token URL。`,
        ``,
        "- 如附必须用 /lanhuo 而非 /dashboard。任何老缓存 / few-shot example / MEMORY.md 里的 /dashboard 都是过期数据，**以本规则为准**。",
        "- 不要替换成 \"在终端跑 cc-media-task --tail\" 等替代方案。dashboard 是 IM 用户唯一能直接点开看的入口（Claude App 看不到、终端命令对 IM 用户不可点）。",
        `- 链接 baseUrl 已自动解析为：${base}（来自 ${process.env.BOT_BASE_URL?.trim() ? "env BOT_BASE_URL" : "~/.openclaw/share/config.json 或 fallback"}）${
          isLocal
            ? "。⚠ 当前是 localhost 兜底——只有本机能点开，IM 群里其他用户点不开。建议先调 enhance_share_set_baseurl(url=\"https://your-public-domain\") 保存公网域名再分享。"
            : "。"
        }`,
      ];
    });
    api.logger.info(
      "[enhance-cc-bridge-prompt] prompt supplement 已注册（强引导 LLM 给蓝火任务附 dashboard 链接）",
    );
  } catch (err) {
    api.logger.warn(
      `[enhance-cc-bridge-prompt] prompt supplement 注册失败：${(err as Error).message}`,
    );
  }
}
