/**
 * 模块: 大文件上传桥接 (v6.x)
 *
 * 作用: 企微有 100MB 文件传输上限，用户发 >100MB 文件时企微系统返回纯文本错误
 *       "视频/文件超过100M，无法下载"。本模块检测该错误 + 用户主动提大文件上传的意图，
 *       通过 before_prompt_build 注入上传链接引导，并提供 enhance_upload_large_file 工具。
 *
 * 非侵入式保证:
 * - 纯 hook 观察 (before_prompt_build) + 按需工具
 * - 只在 wecom 渠道激活，不影响 terminal 等其他渠道
 * - 不修改 wecom 插件的任何逻辑
 * - 上传端点通过 dashboard HTTP route 暴露，不新增进程
 *
 * 与 bot-share-link 的边界：
 * - bot-share-link: 把本地文件投递到 share 目录 → 生成下载 URL（agent 主动调用）
 * - large-file-bridge: 检测 >100MB 错误/大文件意图 → 注入上传链接引导（自动 hook）+ 提供上传表单
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { getChannel } from "../utils/channel-detect.js";
import { DEFAULT_AGENT_ID } from "../types.js";
import { resolveBaseUrl as resolveBaseUrlFromBridge } from "../utils/http-route-bridge.js";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { randomBytes } from "node:crypto";

export interface LargeFileBridgeConfig {
  enabled?: boolean;
  /**
   * 自定义上传页面 URL；不填则自动生成为 `${baseUrl}/upload`（v6.7.6 起最短 URL）。
   *
   * 历程：
   *   v6.7.4: 改 /lanhuo/upload 避免 LLM 把 /lanhuo 当上传链接误用
   *   v6.7.6: cc-media-bridge v2.18.9 已 native 支持 /upload 短 URL（_lanhuo_strip 让 /upload 直命中）
   *           用户原话："能不能换成 https://keepermac.huo15.com/upload" → 改最短 URL
   *           /lanhuo/upload 仍兼容（等价 alias）
   */
  uploadUrl?: string;
  /** 上传页面基础 URL（企微分享场景需显式填公网地址） */
  baseUrl?: string;
  /** 检测企微 >100M 错误文本，默认 true */
  detectWecomError?: boolean;
  /** 用户提大文件/上传相关关键词时主动提供上传链接，默认 true */
  proactiveOffer?: boolean;
}

const MAX_DEDUP_ENTRIES = 200;

/** 企微系统大文件错误提示的关键词匹配模式 */
const WECOM_LARGE_FILE_ERROR = /视频.*文件.*超过.*100.*[Mm].*无法下载|文件超过.*[Mm].*无法下载|视频超过.*[Mm].*无法下载|100.*[Mm].*无法下载/;

/** 用户主动提及大文件/上传的关键词 */
const LARGE_FILE_INTENT = /(大文件|超大文件|超过\s*\d{2,}\s*[Mm]|\d{3,}\s*[Mm]|发.*大文件|文件太大|怎么传.*文件|上传.*大|大文件.*怎么|send.*large.*file|upload.*large)/i;

/** 文件类型关键词（进一步确认用户在讨论文件上传） */
const FILE_UPLOAD_KEYWORDS = /(上传|upload|传文件|发文件|分享文件|share.*file|send.*file)/i;

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return (ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID;
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

function buildUploadContext(url: string, token: string | null): string {
  const tokenChecklist = token
    ? `

# 本次会话已预生成 token（AI 追踪用）

**token = \`${token}\`**（已写入 ~/.openclaw/upload/manifest.json，24h 有效）

## 用户上传后的处理流程（关键！LLM 必须严格按此顺序执行）

用户上传文件后会发"传完了" / "上传好了" / "已传完" / 类似确认消息。**此时你必须**：

1. 立即调用 \`enhance_upload_check({token: "${token}"})\` 工具
2. 工具返 \`{files: [{path, size, name}, ...]}\` 数组
3. 用 Read 工具读 \`files[i].path\` 拿到文件内容
4. 按用户原始任务继续处理（如"转会议纪要" / "分析内容" / "提取信息"）

**严禁的反模式**（用户上传后你回复时不要做这些）：
❌ 再次发上传链接（用户已上传，再发链接 = 死循环！）
❌ 反问"你确定上传了吗 / 请截图" / "我没收到"（请你**先调 enhance_upload_check** 再说，绝大多数情况文件就在）
❌ 跳过 enhance_upload_check 直接 ls 或 grep \`~/.openclaw/upload/\` 全盘扫（隐私 + 性能差，token 才是精确入口）`
    : "\n\n# 本次未生成 token（兜底共享 URL，AI 不能精确追踪）";

  return `【大文件上传 — 强制规则，禁止违反】

用户上一条消息是「视频/文件超过100M，无法下载」。这是企微官方对 bot 接收文件的硬上限拦截，**你不需要查任何源码、不需要问任何诊断问题、不需要解释技术原因**。

# 你的回复必须是下面这一段，一字不改：

文件超过 100MB 无法在企微直接传输，请通过下面这个链接上传（支持 2GB 以内，浏览器拖拽即可）：

${url}

上传完成后告诉我，我来处理。
${tokenChecklist}

# 严禁的行为（违反 = 用户卡死）

❌ 不要 exec/grep wecom / openclaw 源码查"limit / maxBytes / MAX_DOCUMENT_BYTES"等 — 已知是企微平台 100MB 上限，**结论已确定**
❌ 不要反问用户"请把完整错误消息截图发给我" / "你是哪个场景" / "需要更多信息才能定位"
❌ 不要建议用户 \`openclaw config set\` 或修改任何配置 — 用户**就是想传文件给你**，不是改配置
❌ 不要叙述性提到 "large-file-bridge 模块" / "增强包 hook" / "插件内置限制" — 用户不关心实现
❌ 不要给 \`/plugins/enhance/upload\` 这种**裸路径**（缺 https:// 前缀），用户点不开
${token ? `❌ 不要再调 enhance_upload_link 工具生成新 token — token \`${token}\` 已预备好,直接发给用户即可` : ""}

(由 enhance large-file-bridge 触发；关闭: config.largeFileBridge.enabled = false)`;
}

export function registerLargeFileBridge(
  api: OpenClawPluginApi,
  config?: LargeFileBridgeConfig,
) {
  if (config?.enabled === false) return;

  const detectWecomError = config?.detectWecomError !== false;
  const proactiveOffer = config?.proactiveOffer !== false;

  // v6.7.12: 每个 session 关联一个 token，让 prompt 引导 + 兜底 hook 都给同一个 token URL
  // → AI 之后能调 enhance_upload_check({token}) 拿清单（精确追踪谁传了什么）
  // v6.7.13: 加 replyAppendUsed 标记 — 每次 inject 只兜底一次，避免后续 reply（用户说
  // "传完了" / "继续帮我处理" 等）都被 hook 强制覆盖回上传链接（用户卡死循环）
  const injectedSessions = new Map<
    string,
    { token: string; createdAt: number; replyAppendUsed: boolean }
  >();

  // v6.7.12: token 自动生成 + manifest 写入（跟 bot-upload-link 同一份 ~/.openclaw/upload/）
  // 这样 LLM 不调 enhance_upload_link 工具,我们 hook 兜底也能给 token URL,enhance_upload_check 仍能查清单
  const UPLOAD_ROOT = join(homedir(), ".openclaw", "upload");
  const MANIFEST_PATH = join(UPLOAD_ROOT, "manifest.json");
  const URL_PREFIX = "/plugins/enhance-upload";

  function createUploadToken(label: string | undefined, ownerAgent: string | undefined): string | null {
    try {
      const token = randomBytes(6).toString("hex");  // 12 hex chars,与 bot-upload-link 一致
      const tokenDir = join(UPLOAD_ROOT, token, "files");
      mkdirSync(tokenDir, { recursive: true });

      // 读取或新建 manifest（跟 bot-upload-link 同一份,所以 enhance_upload_check 能查到）
      let manifest: { version: 1; entries: any[] } = { version: 1, entries: [] };
      if (existsSync(MANIFEST_PATH)) {
        try {
          const parsed = JSON.parse(readFileSync(MANIFEST_PATH, "utf-8"));
          if (parsed && Array.isArray(parsed.entries)) manifest = parsed;
        } catch { /* ignore corrupt manifest, start fresh */ }
      }

      const now = new Date();
      const expireAt = new Date(now.getTime() + 24 * 3600 * 1000);  // 24h TTL（跟 bot-upload-link 默认一致）
      manifest.entries.push({
        token,
        label,
        ownerAgent,
        createdAt: now.toISOString(),
        expireAt: expireAt.toISOString(),
        files: [],
      });

      writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), "utf-8");
      return token;
    } catch (err) {
      api.logger.warn(`[enhance-large-file] createUploadToken 失败,fallback 到无 token URL: ${(err as Error).message}`);
      return null;
    }
  }

  function buildTokenUrl(baseUrl: string, token: string): string {
    return `${baseUrl.replace(/\/+$/, "")}${URL_PREFIX}/${token}`;
  }

  /**
   * v6.7.9: baseUrl 优先级（跟 bot-share-link / bot-upload-link 同款）:
   *   env BOT_BASE_URL > config.baseUrl > ~/.openclaw/share/config.json
   *   > bridge 检测到的外网 URL > internal fallback
   *
   * 修 v6.7.8- bug：默认推 `/plugins/enhance/upload` 时没拼公网域名，
   * LLM 给用户的回复变成 `👉 /plugins/enhance/upload`（没 https://...），用户根本点不开。
   */
  function readSharedBaseUrl(): string | undefined {
    try {
      const sharePath = join(homedir(), ".openclaw", "share", "config.json");
      if (!existsSync(sharePath)) return undefined;
      const j = JSON.parse(readFileSync(sharePath, "utf-8")) as { baseUrl?: string };
      return j?.baseUrl?.trim() || undefined;
    } catch {
      return undefined;
    }
  }

  function resolveUploadUrl(): string {
    if (config?.uploadUrl?.trim()) return config.uploadUrl.trim();
    // 多源 baseUrl: env > config > shared share/config.json > bridge detected
    const base = resolveBaseUrlFromBridge({
      configBaseUrl: config?.baseUrl?.trim() || readSharedBaseUrl(),
      envName: "BOT_BASE_URL",
      fallback: "http://localhost:18789",
    });
    return `${base.replace(/\/+$/, "")}/plugins/enhance/upload`;
  }

  api.on("before_prompt_build", (_event, ctx) => {
    const agentId = pickAgentId(ctx);
    const sessionId = pickSessionId(ctx);
    const key = `${agentId}::${sessionId}`;

    const promptText = (() => {
      try {
        return String((_event as any).prompt ?? (_event as any).promptText ?? "");
      } catch {
        return "";
      }
    })();

    if (!promptText) return;

    let reason = "";

    // v6.7.10: 触发条件**不再卡 agentId**——「视频/文件超过 100M，无法下载」
    // 是企微独家错误文本，命中即必定是企微大文件场景，**不管 channel 是什么**都该引导。
    // 之前 v6.7.0 加 agentId.startsWith("wecom-") 是为了"避免 terminal 误触"，但实际
    // terminal 用户也可能粘贴这句错误文本来问 AI 怎么处理——同样应该给上传链接。
    if (detectWecomError && WECOM_LARGE_FILE_ERROR.test(promptText)) {
      reason = "detected-wecom-large-file-error";
    } else if (
      proactiveOffer &&
      LARGE_FILE_INTENT.test(promptText) &&
      FILE_UPLOAD_KEYWORDS.test(promptText) &&
      // 主动引导仍卡 wecom-（这种泛泛的「想传大文件」表达 terminal 用户其实有别的路径）
      agentId.startsWith("wecom-")
    ) {
      reason = "detected-large-file-intent";
    }

    if (!reason) return;

    if (injectedSessions.has(key)) return;

    // v6.7.12: 自动生成 token + 拼 token URL（让 AI 通过 enhance_upload_check 能追踪）
    const baseUrl = resolveBaseUrlFromBridge({
      configBaseUrl: config?.baseUrl?.trim() || readSharedBaseUrl(),
      envName: "BOT_BASE_URL",
      fallback: "http://localhost:18789",
    });
    const token = createUploadToken(`session:${sessionId.slice(0, 12)}`, agentId);
    const url = token
      ? buildTokenUrl(baseUrl, token)
      : resolveUploadUrl();  // token 生成失败兜底用共享 URL

    const text = buildUploadContext(url, token);

    if (injectedSessions.size >= MAX_DEDUP_ENTRIES) {
      const oldest = injectedSessions.keys().next().value;
      if (oldest !== undefined) injectedSessions.delete(oldest);
    }
    injectedSessions.set(key, {
      token: token ?? "",
      createdAt: Date.now(),
      replyAppendUsed: false,
    });

    api.logger.info(
      `[enhance-large-file] ${reason} | token=${token ?? "<fallback-no-token>"} | url=${url} (agent=${agentId}, session=${sessionId.slice(0, 12)})`,
    );

    return { prependContext: text };
  });

  // before_agent_reply 第三层防御：如果 LLM 回复里没含上传链接关键词，hook 接管整个 reply，
  // 把原 body 拼上上传链接 suffix 一起作为最终回复返回。
  //
  // v6.7.4 修正：v6.7.3 用了 `{appendText: suffix}` —— 但 PluginHookBeforeAgentReplyResult 类型
  // 实际是 `{handled, reply, reason}`，`appendText` 字段不被 OpenClaw runtime 识别！v6.7.3 那个
  // hook 实际上**没起作用**（runtime 拿到 unknown field 就 silent ignore）。
  // 正确做法：return `{ handled: true, reply: { text: body + suffix } }` 接管 reply 并自己拼。
  api.on("before_agent_reply", (event, ctx) => {
    const agentId = pickAgentId(ctx);
    const sessionId = pickSessionId(ctx);
    const key = `${agentId}::${sessionId}`;

    const entry = injectedSessions.get(key);
    if (!entry) return;
    // v6.7.13: 每次 inject 兜底只 fire 一次。后续 user 消息（如"传完了" / "继续处理"）
    // LLM 应该正常调 enhance_upload_check 工具，hook 不再强行 appendText 上传链接覆盖。
    if (entry.replyAppendUsed) return;

    try {
      const body: string = (event as any)?.cleanedBody ?? (event as any)?.body ?? "";
      if (!body) return;

      // v6.7.12: 用 before_prompt_build 时记下的 token 拼 URL（前后一致）
      const baseUrl = resolveBaseUrlFromBridge({
        configBaseUrl: config?.baseUrl?.trim() || readSharedBaseUrl(),
        envName: "BOT_BASE_URL",
        fallback: "http://localhost:18789",
      });
      const url = entry.token
        ? buildTokenUrl(baseUrl, entry.token)
        : resolveUploadUrl();
      // v6.7.11: 收紧"已含上传链接"判断 — 只在含**真实可点 URL**时跳过。
      // 之前用 body.includes("upload") 太宽泛 — LLM 叙述性提到 "large-file-bridge"
      // 或 "上传相关问题" 也会误判为"已给链接"。MiniMax M2.7 等弱模型反向操作
      // (问诊断 + 自己 grep source code) 时回复里有 "upload" 字符串但**没真给 URL**，
      // 兜底 hook 不接管 = 用户什么都拿不到。
      const hasRealUrl =
        body.includes(url) ||                                       // 完整匹配本次 url
        /https?:\/\/[^\s)]+\/plugins\/enhance(-upload)?\//.test(body) ||  // 任何 enhance 上传 URL
        body.includes("enhance_upload_link") ||                     // LLM 调过工具会留下 marker
        body.includes("enhance_upload_check");
      if (hasRealUrl) {
        // LLM 已经按引导给链接（或调过工具）→ 标记本轮 inject 已完成，后续 reply 不再兜底
        entry.replyAppendUsed = true;
        return;
      }

      // 只在 final/block 类型 reply 接管（流式片段不接管）
      const kind: string = (event as any)?.kind ?? "";
      if (kind && kind !== "block" && kind !== "final") return;

      const suffix = `\n\n---\n📎 **大文件上传**：文件超过 100MB 无法在企微直接传输，请通过以下链接上传：\n👉 ${url}\n上传完成后告诉我，我来处理文件。`;

      api.logger.info(
        `[enhance-large-file] before_agent_reply 强制接管 reply 拼上传链接 (agent=${agentId}, token=${entry.token || "<no-token>"})`,
      );

      // v6.7.13: 标记本轮 inject 兜底已用，后续不再 fire
      entry.replyAppendUsed = true;

      // v6.7.4: return PluginHookBeforeAgentReplyResult shape: {handled, reply, reason}
      return {
        handled: true,
        reply: { text: body + suffix },
        reason: "large-file-bridge: 强制把上传链接拼到 LLM 回复末尾",
      };
    } catch {
      return;
    }
  });

  api.registerTool(
    (ctx) => ({
      name: "enhance_upload_large_file",
      description: "获取大文件上传链接（企微文件上限 100MB 时使用）返回 uploadUrl 及使用说明",
      inputSchema: {
        type: "object",
        properties: {
          filename: {
            type: "string",
            description: "可选，建议用户使用的文件名",
          },
        },
      },
      async execute(_params: unknown) {
        const url = resolveUploadUrl();
        const agentId = pickAgentId(ctx);
        try {
          api.logger.info(
            `[enhance-large-file] tool called by agent=${agentId}`,
          );
        } catch { /* silent */ }
        return {
          uploadUrl: url,
          instructions:
            "用户点击链接后选择文件上传。上传完成后系统会返回分享链接。" +
            "如果辉火云 Odoo 文档引擎可用，文件会自动同步到 documents.document。" +
            "本地上传的文件也可通过 enhance_share_file 转为分享链接。",
          note: "企微Bot API 文件上传上限为 20MB，聊天传输上限为 100MB。超出请走此上传通道。",
        };
      },
    }) as any,
    { tier: "tools" } as any,
  );

  api.logger.info("[enhance] 大文件上传桥接模块已加载 (large-file-bridge)");
}
