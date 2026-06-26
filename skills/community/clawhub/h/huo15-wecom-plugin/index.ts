/**
 * Author: YanHaidao / 火一五定制版
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
// import { emptyPluginConfigSchema } from "openclaw/plugin-sdk";
import { registerWecomCalendarTools } from "./src/capability/calendar/tool.js";
import { registerWecomDocTools } from "./src/capability/doc/tool.js";
import { createWeComMcpToolFactory } from "./src/capability/mcp/index.js";
import { wecomPlugin } from "./src/channel.js";
import { handleWecomWebhookRequest } from "./src/monitor.js";
import { setWecomRuntime } from "./src/runtime.js";
import { isWecomBotWsSource } from "./src/runtime/source-registry.js";

const WECOM_BOT_WS_MEDIA_GUIDANCE = [
  "【WeCom 文件发送（v2.8.25 — 优先 MEDIA: 直发，仅大文件走链接）】",
  "",
  "用户偏好：群里能直接收到附件 > 收到下载链接。**默认优先 MEDIA: 字面量直发**，",
  "仅当文件超过企微 size 上限时再调 `enhance_share_file` 走链接。",
  "",
  "═══ 路径选择决策表 ═══",
  "",
  "| 文件类型/大小 | 路径 | 用户体验 |",
  "|---|---|---|",
  "| 图片 ≤ 10MB | **MEDIA: 直发** ← 默认 | 群里直接收到图片 |",
  "| 视频 ≤ 10MB | **MEDIA: 直发** ← 默认 | 群里直接收到视频 |",
  "| 语音 ≤ 2MB | **MEDIA: 直发** ← 默认 | 群里直接收到语音 |",
  "| 其他文件 ≤ 20MB | **MEDIA: 直发** ← 默认 | 群里直接收到附件 |",
  "| 超过上面阈值 | `enhance_share_file` 链接 ← fallback | 群里收到 markdown 链接 |",
  "| 用户**明确说**「不要发链接」/「直接发文件」 | **强制 MEDIA: 直发** | 即使大文件也尝试 MEDIA:，企微拒了再降级链接 |",
  "",
  "═══ 默认路径：MEDIA: 直发 ═══",
  "",
  "v2.8.23 已修群聊场景（群聊走 sendMediaMessage 主动推送通道，不撞 86008）；",
  "v2.8.24 已修 placeholder timeout 解锁 UI；MEDIA: 路径现在**稳定可用**。",
  "",
  "✅ 正确格式（MEDIA: 必须独立成行）：",
  "```",
  "你要的文件已经准备好。",
  "",
  "MEDIA: ~/.openclaw/media/outbound/report.pdf",
  "```",
  "",
  "❌ 错误（parser 抽不出来 → 文件发不出）：",
  "- `📎 MEDIA: ~/foo.zip` ← 行首有 emoji",
  "- `请查收 MEDIA: ~/foo.zip` ← 行首有正文",
  "- `MEDIA: ~/foo.zip 已准备` ← 路径后有正文",
  "- `> MEDIA: ~/foo.zip` ← markdown 引用 / 列表前缀",
  "- 整体被引号包住（应只在路径上加引号，不是包整行）",
  "",
  "硬性要求：",
  "- 必须**整行单独**出现，前后只有空白",
  "- 路径必须**绝对路径**或 `~/` 开头（自动展开 home），相对路径会失败",
  "- 一次回复可以叠多行 MEDIA:（每行独立），按序发送、单个失败不影响后续",
  "- 媒体行抽出后，剩下的正文按普通文本同时发出（如有）",
  "",
  "═══ Fallback：enhance_share_file 链接（仅大文件用）═══",
  "",
  "当文件超过企微 size 上限（图/视频 > 10MB / 语音 > 2MB / 文件 > 20MB）：",
  "1. 调 `enhance_share_file({ filePath: '<绝对路径>' })` 工具",
  "2. 拿 `structuredContent.url`",
  "3. 用 markdown 链接形式发：`📎 [文件名](url)`",
  "",
  "链接路径优势：大小无硬限制（≤ 500MB）、24h 自动过期、跨群跨企业通用。",
  "",
  "═══ 用户偏好覆盖 ═══",
  "",
  "如果用户**明确**说「不要发链接」/「直接发文件给我」/「以后都直接发文件」：",
  "**即使文件超出企微上限**也先尝试 MEDIA: 直发——企微 server 会拒（errcode），",
  "wecom 自动 share-fallback 走链接。这样用户至少看到了你的努力。",
].join("\n");

// ── 插件配置 Schema（tips/pet 已移除）──
const wecomPluginConfigSchema = {
  type: "object" as const,
  properties: {},
};

const plugin = {
  id: "wecom",
  name: "WeCom (企业微信)",
  description: "企业微信官方推荐三方插件，默认 Bot WS，支持主动发消息与统一运行时能力，火一五定制版",
  configSchema: wecomPluginConfigSchema,
  /**
   * **register (注册插件)**
   *
   * OpenClaw 插件入口点。
   * 1. 注入统一 runtime compatibility layer。
   * 2. 注册 capability-first WeCom 渠道插件。
   * 3. 注册统一 HTTP 入口（所有 webhook 请求都走共享路由器）。
   */
  register(api: OpenClawPluginApi) {
    setWecomRuntime(api.runtime);
    api.registerChannel({ plugin: wecomPlugin });
    const routes = ["/plugins/wecom", "/wecom"];
    for (const path of routes) {
      api.registerHttpRoute({
        path,
        handler: handleWecomWebhookRequest,
        auth: "plugin",
        match: "prefix",
      });
    }

    // Register WeCom Doc Tools
    registerWecomDocTools(api);
    registerWecomCalendarTools(api);
    api.registerTool(createWeComMcpToolFactory(), { name: "wecom_mcp" });

    api.on("before_prompt_build", (_event, ctx) => {
      if (ctx.channelId !== "wecom") {
        return;
      }
      if (
        !isWecomBotWsSource({
          sessionKey: ctx.sessionKey,
          sessionId: ctx.sessionId,
        })
      ) {
        return;
      }
      return {
        appendSystemContext: WECOM_BOT_WS_MEDIA_GUIDANCE,
      };
    });

    // [已移除] 小贴士+火苗宠物模块 — 导致企微不回复
  },
};

export default plugin;
