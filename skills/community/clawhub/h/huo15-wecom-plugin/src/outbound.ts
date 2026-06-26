import { homedir } from "node:os";
import type { ChannelOutboundAdapter } from "openclaw/plugin-sdk/channel-send-result";
import { WecomAgentDeliveryService } from "./capability/agent/index.js";
import {
  resolveWecomMergedMediaLocalRoots,
  resolveWecomMediaMaxBytes,
  resolveWecomAccount,
  resolveWecomAccountConflict,
  resolveWecomAccounts,
} from "./config/index.js";
import {
  getAccountRuntime,
  getActiveBotWsReplyHandle,
  getBotWsPushHandle,
  getWecomRuntime,
} from "./runtime.js";
import { resolveWecomSourceSnapshot } from "./runtime/source-registry.js";
import { parseKefuScopedTarget, resolveScopedWecomTarget } from "./target.js";
import {
  deliverKefuMediaUrl,
  deliverKefuText,
  type KefuDeliveryTarget,
} from "./transport/kefu/outbound.js";
import { extractMarkdownImages } from "./wecom_msg_adapter/image_extractor.js";
import { loadImageAsPayload } from "./wecom_msg_adapter/image_fetcher.js";
import { toKefuText } from "./wecom_msg_adapter/kefu_text_adapter.js";
import { toWeComMarkdownV2 } from "./wecom_msg_adapter/markdown_adapter.js";

type WecomOutboundBaseContext = Parameters<NonNullable<ChannelOutboundAdapter["sendText"]>>[0];
type WecomOutboundContext = WecomOutboundBaseContext & {
  sessionKey?: string | null;
};
type WecomOutboundConfig = WecomOutboundContext["cfg"];

/**
 * v2.8.19 — 解析 LLM 在文本里 emit 的 "MEDIA: <path>" 单行指令。
 *
 * 背景：index.ts 的 WECOM_BOT_WS_MEDIA_GUIDANCE 通过 before_prompt_build hook 注入到
 * system context，告诉 LLM 「当你需要发送图片、文件、视频或语音时，必须在回复中单独
 * 一行使用 MEDIA: 指令」。但 v2.8.19 之前 outbound 完全没有解析这个字面量——LLM 老老
 * 实实按 GUIDANCE emit 的 "MEDIA: ~/.openclaw/.../foo.zip" 行就当成普通文本发了出去，
 * 用户根本没收到附件。
 *
 * 本函数把 LLM 输出按行扫描，命中 `MEDIA: <path>` 的行抽出来作为媒体路径返回；
 * 剩下的文字保持原样组装回 `residualText`。会自动：
 *   - trim 前后空格
 *   - 去掉成对的引号（`"..."` / `'...'`）
 *   - 把 `~/` 展开到当前用户 home（与 sendMedia 内部 `mediaUrl.startsWith("~")` 行为一致）
 *   - 大小写不敏感（`media:` / `Media:` 也接受）
 *
 * 多行同时存在多个 `MEDIA:` 时按出现顺序全部抽出，sendText 入口循环逐个调
 * sendMediaInternal 发送（每一个失败不影响后续，避免单次失败吞掉整批回复）。
 */
export function extractMediaDirectives(text: string | undefined | null): {
  residualText: string;
  mediaPaths: string[];
} {
  if (!text) return { residualText: "", mediaPaths: [] };
  const lines = String(text).split(/\r?\n/);
  const mediaPaths: string[] = [];
  const remaining: string[] = [];
  // 整行模式（前后允许空白）：MEDIA: <path> 单独成一行
  const re = /^\s*MEDIA:\s*(.+?)\s*$/i;
  for (const line of lines) {
    const m = line.match(re);
    if (m) {
      let p = m[1].trim();
      // 去掉成对引号
      if (
        (p.startsWith('"') && p.endsWith('"')) ||
        (p.startsWith("'") && p.endsWith("'"))
      ) {
        p = p.slice(1, -1).trim();
      }
      // 展开 ~/ 到 home dir
      if (p === "~" || p.startsWith("~/")) {
        p = p.replace(/^~/, homedir());
      }
      if (p) mediaPaths.push(p);
    } else {
      remaining.push(line);
    }
  }
  return { residualText: remaining.join("\n").trim(), mediaPaths };
}

/**
 * 图片下发失败时的纯文字占位。
 *
 * 为什么不把原 URL 内联回 markdown：Agent 回复里常见的 `![](cos_url)` 是**短 TTL 的预签名 URL**
 * （Tencent COS / 阿里 OSS 等），插件这侧 fetch 拉不动时，把同一 URL 发给企微客户端，
 * 客户端同样会失败，只会让用户看到"COS链接已过期 / 图片打不开"。
 *
 * 纯文字占位更诚实，用户能判断出是哪张图丢了，并能要求重新生成。
 */
export function buildImageFailurePlaceholder(alt: string, reason?: string): string {
  const label = alt?.trim() || "图片";
  const reasonSuffix = reason ? `（${summarizeImageFailure(reason)}）` : "";
  return `⚠️ 图片发送失败：${label}${reasonSuffix}`;
}

function summarizeImageFailure(reason: string): string {
  const msg = reason.trim();
  if (!msg) return "未知错误";
  // 常见预签名过期错误里会带 "expired" / "403" / "SignatureDoesNotMatch" —— 归一成一句提示。
  if (/expired|403|SignatureDoesNotMatch/i.test(msg)) return "下载链接已过期，请重试";
  if (/timeout|ETIMEDOUT|AbortError/i.test(msg)) return "下载超时，请重试";
  if (/exceeds max|超过/i.test(msg)) return "超出大小限制";
  // 兜底时截断，避免把多行 stack 塞进用户可见的文本里
  const short = msg.split(/\r?\n/)[0].slice(0, 80);
  return short || "未知错误";
}

/**
 * 发送前最后一道兜底：如果 residualText 里仍然残留 `![...](...)` 语法，
 * 说明上一轮 `extractMarkdownImages` 正则漏掉了（URL 含 `)`、换行打断等边缘场景）。
 *
 * 漏网的原因我们已经知道：插件侧都没能 upload，那等这段 markdown 被发到企微客户端时，
 * 客户端同样拉不动那条 URL，最终用户看到的只有 "COS 链接已过期"。
 *
 * 这里兜底把所有残留的 `![alt](whatever)` 统一替换成明文占位，行为与上层 upload 失败时一致。
 * 用更宽松的正则（不限制 URL 内的 `)` / `\s`），宁可误伤也不放行。
 */
export function sanitizeResidualImageMarkdown(text: string): string {
  if (!text) return text;
  return text.replace(/!\[([^\]\n]*)\]\(([^\n]*?)\)/g, (_full, altRaw: string) => {
    const alt = String(altRaw ?? "").trim() || "图片";
    return buildImageFailurePlaceholder(alt);
  });
}

function resolveOutboundAccountOrThrow(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
}) {
  const resolvedAccounts = resolveWecomAccounts(params.cfg);
  const conflictAccountId = params.accountId?.trim() || resolvedAccounts.defaultAccountId;
  const conflict = resolveWecomAccountConflict({
    cfg: params.cfg,
    accountId: conflictAccountId,
  });
  if (conflict) {
    throw new Error(conflict.message);
  }

  const requestedAccountId = params.accountId?.trim();
  if (requestedAccountId) {
    if (!resolvedAccounts.accounts[requestedAccountId]) {
      throw new Error(
        `WeCom outbound account "${requestedAccountId}" not found. Configure channels.wecom.accounts.${requestedAccountId} or use an existing accountId.`,
      );
    }
  }
  return resolveWecomAccount({
    cfg: params.cfg,
    accountId: params.accountId,
  });
}

function resolveAgentConfigOrThrow(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
}) {
  const account = resolveOutboundAccountOrThrow(params).agent;
  if (!account?.apiConfigured) {
    throw new Error(
      `WeCom outbound requires Agent mode for account=${params.accountId ?? "default"}. Configure channels.wecom.accounts.<accountId>.agent (or legacy channels.wecom.agent).`,
    );
  }
  if (typeof account.agentId !== "number" || !Number.isFinite(account.agentId)) {
    throw new Error(
      `WeCom outbound requires channels.wecom.accounts.<accountId>.agent.agentId (or legacy channels.wecom.agent.agentId) for account=${params.accountId ?? account.accountId}.`,
    );
  }
  // 注意：不要在日志里输出 corpSecret 等敏感信息
  getAccountRuntime(account.accountId)?.log.info?.(
    `[wecom-outbound] Using agent config: accountId=${account.accountId}, corpId=${account.corpId}, agentId=${account.agentId}`,
  );
  return account;
}

function isExplicitAgentTarget(raw: string | undefined): boolean {
  return /^wecom-agent:/i.test(String(raw ?? "").trim());
}

function isExplicitKefuTarget(raw: string | undefined): boolean {
  return /^wecom-kefu:/i.test(String(raw ?? "").trim());
}

function resolveKefuDeliveryTarget(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
  to: string | undefined;
  sessionKey?: string | null;
}): { target: KefuDeliveryTarget; accountId: string } | undefined {
  const explicit = params.to ? parseKefuScopedTarget(params.to) : undefined;
  const explicitAccountId = explicit?.accountId?.trim();
  const account = resolveOutboundAccountOrThrow({
    cfg: params.cfg,
    accountId: explicitAccountId || params.accountId,
  });
  if (!account.kefu?.apiConfigured) {
    if (explicit) {
      throw new Error(
        `WeCom outbound account="${account.accountId}" is missing kefu credentials (corpId + corpSecret).`,
      );
    }
    return undefined;
  }
  if (explicit) {
    return {
      accountId: account.accountId,
      target: {
        kefu: account.kefu,
        openKfId: explicit.openKfId,
        externalUserId: explicit.externalUserId,
      },
    };
  }
  const scoped = resolveScopedWecomTarget(params.to, account.accountId);
  const externalUserId = scoped?.target.touser?.trim() || scoped?.target.kefu?.externalUserId?.trim();
  if (!externalUserId) return undefined;
  const snapshot = resolveWecomSourceSnapshot({
    accountId: account.accountId,
    sessionKey: params.sessionKey,
    peerKind: "direct",
    peerId: externalUserId,
  });
  if (snapshot?.source !== "kefu" || !snapshot.kefuOpenKfId) return undefined;
  return {
    accountId: account.accountId,
    target: {
      kefu: account.kefu,
      openKfId: snapshot.kefuOpenKfId,
      externalUserId,
    },
  };
}

async function sendTextViaKefu(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
  to: string | undefined;
  text: string;
  sessionKey?: string | null;
}): Promise<boolean> {
  if (isExplicitAgentTarget(params.to)) return false;
  const resolved = resolveKefuDeliveryTarget(params);
  if (!resolved) return false;
  const { images, residualText } = extractMarkdownImages(params.text);
  let textToSend = residualText;
  for (const image of images) {
    try {
      await deliverKefuMediaUrl(resolved.target, image.url);
      getAccountRuntime(resolved.accountId)?.log.info?.(
        `[wecom-outbound] Sent kefu inline image to openKfId=${resolved.target.openKfId} externalUserId=${resolved.target.externalUserId} src=${image.url}`,
      );
    } catch (err) {
      getAccountRuntime(resolved.accountId)?.log.warn?.(
        `[wecom-outbound] kefu inline image failed (src=${image.url}): ${err instanceof Error ? err.message : String(err)}, embedding back into text`,
      );
      textToSend = textToSend
        ? `${textToSend}\n\n![${image.alt}](${image.url})`
        : `![${image.alt}](${image.url})`;
    }
  }
  const plain = toKefuText(textToSend);
  if (plain.trim()) {
    await deliverKefuText(resolved.target, plain);
    getAccountRuntime(resolved.accountId)?.log.info?.(
      `[wecom-outbound] Sent kefu text to openKfId=${resolved.target.openKfId} externalUserId=${resolved.target.externalUserId} (len=${plain.length})`,
    );
  } else if (images.length === 0) {
    getAccountRuntime(resolved.accountId)?.log.info?.(
      `[wecom-outbound] Empty kefu message to openKfId=${resolved.target.openKfId}, skipped`,
    );
    return false;
  }
  return true;
}

async function sendMediaViaKefu(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
  to: string | undefined;
  mediaUrl: string;
  sessionKey?: string | null;
}): Promise<boolean> {
  if (isExplicitAgentTarget(params.to)) return false;
  const resolved = resolveKefuDeliveryTarget(params);
  if (!resolved) return false;
  await deliverKefuMediaUrl(resolved.target, params.mediaUrl);
  getAccountRuntime(resolved.accountId)?.log.info?.(
    `[wecom-outbound] Sent kefu media to openKfId=${resolved.target.openKfId} externalUserId=${resolved.target.externalUserId} url=${params.mediaUrl}`,
  );
  return true;
}


function resolveBotWsChatTarget(params: {
  to: string | undefined;
  accountId: string;
}): string | undefined {
  const scoped = resolveScopedWecomTarget(params.to, params.accountId);
  if (!scoped) {
    return undefined;
  }
  if (scoped.accountId && scoped.accountId !== params.accountId) {
    throw new Error(
      `WeCom outbound account mismatch: target belongs to account=${scoped.accountId}, current account=${params.accountId}.`,
    );
  }
  if (scoped.target.chatid) {
    return scoped.target.chatid;
  }
  if (scoped.target.touser) {
    return scoped.target.touser;
  }
  return undefined;
}

function resolveOutboundPeer(params: {
  to: string | undefined;
  accountId: string;
}): { peerKind: "direct" | "group"; peerId: string } | undefined {
  const scoped = resolveScopedWecomTarget(params.to, params.accountId);
  if (!scoped) {
    return undefined;
  }
  if (scoped.accountId && scoped.accountId !== params.accountId) {
    return undefined;
  }
  if (scoped.target.chatid) {
    return { peerKind: "group", peerId: scoped.target.chatid };
  }
  if (scoped.target.touser) {
    return { peerKind: "direct", peerId: scoped.target.touser };
  }
  return undefined;
}

function shouldPreferBotWsOutbound(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
  to: string | undefined;
  sessionKey?: string | null;
}): { preferred: boolean; accountId: string } {
  const account = resolveOutboundAccountOrThrow({
    cfg: params.cfg,
    accountId: params.accountId,
  });
  const peer = resolveOutboundPeer({
    to: params.to,
    accountId: account.accountId,
  });
  const source = resolveWecomSourceSnapshot({
    accountId: account.accountId,
    sessionKey: params.sessionKey,
    peerKind: peer?.peerKind,
    peerId: peer?.peerId,
  });
  const pinnedToAgent = source?.source === "agent-callback";
  const pinnedToBotWs = source?.source === "bot-ws";
  return {
    preferred:
      !isExplicitAgentTarget(params.to) &&
      !pinnedToAgent &&
      Boolean(
        account.bot?.configured &&
        account.bot.wsConfigured &&
        (pinnedToBotWs || account.bot.primaryTransport === "ws"),
      ),
    accountId: account.accountId,
  };
}

function markActiveBotWsReplyHandleActivity(params: {
  accountId: string;
  sessionKey?: string | null;
  to: string | undefined;
}): void {
  const peer = resolveOutboundPeer({
    to: params.to,
    accountId: params.accountId,
  });
  const handle = getActiveBotWsReplyHandle({
    accountId: params.accountId,
    sessionKey: params.sessionKey,
    peerKind: peer?.peerKind,
    peerId: peer?.peerId,
  });
  handle?.markExternalActivity?.();
}

async function sendTextViaBotWs(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
  to: string | undefined;
  text: string;
  sessionKey?: string | null;
}): Promise<boolean> {
  const { preferred, accountId } = shouldPreferBotWsOutbound(params);
  if (!preferred) {
    return false;
  }
  const chatId = resolveBotWsChatTarget({
    to: params.to,
    accountId,
  });
  if (!chatId) {
    return false;
  }
  const handle = getBotWsPushHandle(accountId);
  if (!handle) {
    throw new Error(
      `WeCom outbound account=${accountId} is configured for Bot WS active push, but no live WS runtime is registered.`,
    );
  }
  if (!handle.isConnected()) {
    throw new Error(
      `WeCom outbound account=${accountId} is configured for Bot WS active push, but the WS transport is not connected.`,
    );
  }

  // 先把 markdown 内的 ![](url) 抽成独立图片消息,失败回退为内嵌 markdown
  const { images, residualText } = extractMarkdownImages(params.text);
  const mediaLocalRoots = resolveWecomMergedMediaLocalRoots({ cfg: params.cfg });
  const maxBytes = resolveWecomMediaMaxBytes(params.cfg, accountId);
  let textToSend = residualText;

  for (const image of images) {
    let failureReason: string | undefined;
    try {
      const result = await handle.sendMedia({
        chatId,
        mediaUrl: image.url,
        mediaLocalRoots,
        maxBytes,
      });
      if (result.ok) {
        console.log(
          `[wecom-outbound] Sent Bot WS inline image to ${chatId} (src=${image.url})`,
        );
        continue;
      }
      failureReason = result.rejectReason || result.error || "unknown";
      console.warn(
        `[wecom-outbound] Bot WS inline image failed (src=${image.url}): ${failureReason}`,
      );
    } catch (imgErr) {
      failureReason = imgErr instanceof Error ? imgErr.message : String(imgErr);
      console.warn(
        `[wecom-outbound] Bot WS inline image threw (src=${image.url}): ${failureReason}`,
      );
    }
    // 下载/上传失败时不要把原 URL 再写回 markdown —— 预签名 URL（COS/OSS）插件拉不动，
    // 企微客户端同样拉不动，只会让用户看到 "链接已过期"。改用纯文字占位。
    const placeholder = buildImageFailurePlaceholder(image.alt, failureReason);
    textToSend = textToSend ? `${textToSend}\n\n${placeholder}` : placeholder;
  }

  if (textToSend.trim()) {
    // 兜底：如果 extractMarkdownImages 正则漏了某些 `![](url)`（URL 含 `)` / 换行 / 等），
    // 发到客户端后只会触发 "链接已过期"。统一替换为占位文本。
    const sanitized = sanitizeResidualImageMarkdown(textToSend);
    const markdownText = toWeComMarkdownV2(sanitized);
    console.log(
      `[wecom-outbound] Sending Bot WS active message to target=${String(params.to ?? "")} chatId=${chatId} (len=${markdownText.length})`,
    );
    await handle.sendMarkdown(chatId, markdownText);
    console.log(`[wecom-outbound] Successfully sent Bot WS active message to ${chatId}`);
  } else if (images.length === 0) {
    console.log(`[wecom-outbound] Empty Bot WS message to ${chatId}, skipped`);
    return false;
  }

  markActiveBotWsReplyHandleActivity({
    accountId,
    sessionKey: params.sessionKey,
    to: params.to,
  });
  return true;
}

async function sendMediaViaBotWs(params: {
  cfg: WecomOutboundConfig;
  accountId?: string | null;
  to: string | undefined;
  mediaUrl: string;
  text?: string;
  mediaLocalRoots?: readonly string[];
  sessionKey?: string | null;
}): Promise<{
  attempted: boolean;
  sent: boolean;
  reason?: string;
}> {
  const { preferred, accountId } = shouldPreferBotWsOutbound(params);
  if (!preferred) {
    return { attempted: false, sent: false };
  }
  const chatId = resolveBotWsChatTarget({
    to: params.to,
    accountId,
  });
  if (!chatId) {
    return { attempted: false, sent: false };
  }
  const handle = getBotWsPushHandle(accountId);
  if (!handle) {
    throw new Error(
      `WeCom outbound account=${accountId} is configured for Bot WS active push, but no live WS runtime is registered.`,
    );
  }
  if (!handle.isConnected()) {
    throw new Error(
      `WeCom outbound account=${accountId} is configured for Bot WS active push, but the WS transport is not connected.`,
    );
  }
  console.log(
    `[wecom-outbound] Sending Bot WS media to target=${String(params.to ?? "")} chatId=${chatId} media=${params.mediaUrl}`,
  );
  const effectiveMediaLocalRoots = resolveWecomMergedMediaLocalRoots({
    cfg: params.cfg,
    baseRoots: params.mediaLocalRoots,
  });
  const result = await handle.sendMedia({
    chatId,
    mediaUrl: params.mediaUrl,
    text: params.text,
    mediaLocalRoots: effectiveMediaLocalRoots,
    maxBytes: resolveWecomMediaMaxBytes(params.cfg, accountId),
  });
  if (result.ok) {
    markActiveBotWsReplyHandleActivity({
      accountId,
      sessionKey: params.sessionKey,
      to: params.to,
    });
    console.log(`[wecom-outbound] Successfully sent Bot WS media to ${chatId}`);
    return { attempted: true, sent: true };
  }
  const reason = result.rejectReason || result.error || "unknown";
  console.warn(`[wecom-outbound] Bot WS media failed for ${chatId}: ${reason}`);
  return { attempted: true, sent: false, reason };
}

/**
 * v2.8.19 — 内部 sendMedia 实现（从原 wecomOutbound.sendMedia body 抽出来）。
 * sendText 的 MEDIA: 字面量解析路径会复用它（KISS：不重复实现 kefu/botWs/agent 三层 fallback）。
 */
async function sendMediaInternal({
  cfg,
  to,
  text,
  mediaUrl,
  accountId,
  mediaLocalRoots,
  sessionKey,
}: WecomOutboundContext): Promise<{
  channel: "wecom";
  messageId: string;
  timestamp: number;
}> {
  if (!mediaUrl) {
    throw new Error("WeCom outbound requires mediaUrl.");
  }

  const sentViaKefu = await sendMediaViaKefu({
    cfg,
    accountId,
    to,
    mediaUrl,
    sessionKey,
  });
  if (sentViaKefu) {
    return {
      channel: "wecom",
      messageId: `kefu-media-${Date.now()}`,
      timestamp: Date.now(),
    };
  }

  const botWs = await sendMediaViaBotWs({
    cfg,
    accountId,
    to,
    text,
    mediaUrl,
    mediaLocalRoots,
    sessionKey,
  });
  if (botWs.sent) {
    return {
      channel: "wecom",
      messageId: `bot-ws-media-${Date.now()}`,
      timestamp: Date.now(),
    };
  }
  if (botWs.attempted) {
    throw new Error(
      `WeCom Bot WS media delivery failed for ${String(to ?? "")}: ${botWs.reason ?? "unknown"}`,
    );
  }

  const agent = resolveAgentConfigOrThrow({ cfg, accountId });
  const deliveryService = new WecomAgentDeliveryService(agent);

  let buffer: Buffer;
  let contentType: string;
  let filename: string;

  // 判断是 URL 还是本地文件路径
  const isRemoteUrl = /^https?:\/\//i.test(mediaUrl);

  if (isRemoteUrl) {
    // 不走裸 fetch：复用 fetchRemoteMedia 拿到 SSRF 防护 / redirect / readIdleTimeout，
    // 并显式带 desktop UA 避免部分 CDN（COS/OSS）拒绝 Node 默认 UA。
    const fetched = await loadImageAsPayload(mediaUrl, {
      maxBytes: resolveWecomMediaMaxBytes(cfg, accountId),
    });
    buffer = fetched.buffer;
    contentType = fetched.contentType;
    filename = fetched.filename;
  } else {
    // 本地文件路径
    const fs = await import("node:fs/promises");
    const path = await import("node:path");
    const os = await import("node:os");

    const resolvedPath = mediaUrl.startsWith("~")
      ? path.join(os.homedir(), mediaUrl.slice(1))
      : mediaUrl;
    buffer = await fs.readFile(resolvedPath);
    filename = path.basename(resolvedPath);

    // 根据扩展名推断 content-type
    const ext = path.extname(mediaUrl).slice(1).toLowerCase();
    const mimeTypes: Record<string, string> = {
      jpg: "image/jpeg",
      jpeg: "image/jpeg",
      png: "image/png",
      gif: "image/gif",
      webp: "image/webp",
      bmp: "image/bmp",
      mp3: "audio/mpeg",
      wav: "audio/wav",
      amr: "audio/amr",
      mp4: "video/mp4",
      pdf: "application/pdf",
      doc: "application/msword",
      docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      xls: "application/vnd.ms-excel",
      xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ppt: "application/vnd.ms-powerpoint",
      pptx: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      txt: "text/plain",
      csv: "text/csv",
      tsv: "text/tab-separated-values",
      md: "text/markdown",
      json: "application/json",
      xml: "application/xml",
      yaml: "application/yaml",
      yml: "application/yaml",
      zip: "application/zip",
      rar: "application/vnd.rar",
      "7z": "application/x-7z-compressed",
      tar: "application/x-tar",
      gz: "application/gzip",
      tgz: "application/gzip",
      rtf: "application/rtf",
      odt: "application/vnd.oasis.opendocument.text",
    };
    contentType = mimeTypes[ext] || "application/octet-stream";
    console.log(
      `[wecom-outbound] Reading local file: ${mediaUrl}, ext=${ext}, contentType=${contentType}`,
    );
  }

  console.log(
    `[wecom-outbound] Sending media to ${String(to ?? "")} (filename=${filename}, contentType=${contentType})`,
  );

  try {
    await deliveryService.sendMedia({
      to,
      text,
      buffer,
      filename,
      contentType,
    });
    console.log(`[wecom-outbound] Successfully sent media to ${String(to ?? "")}`);
  } catch (err) {
    console.error(`[wecom-outbound] Failed to send media to ${String(to ?? "")}:`, err);
    throw err;
  }

  return {
    channel: "wecom",
    messageId: `${botWs.attempted ? "agent-fallback-media" : "agent-media"}-${Date.now()}`,
    timestamp: Date.now(),
  };
}

export const wecomOutbound: ChannelOutboundAdapter = {
  deliveryMode: "direct",
  chunkerMode: "text",
  textChunkLimit: 20480,
  chunker: (text: string, limit: number) => {
    try {
      return getWecomRuntime().channel.text.chunkText(text, limit);
    } catch {
      return [text];
    }
  },
  sendText: async (ctx: WecomOutboundContext) => {
    const { cfg, to, accountId, sessionKey } = ctx;
    let { text } = ctx;

    // ── v2.8.19 ⭐ MEDIA: 指令解析（修群里发 zip 失败事故）─────────────────────
    // index.ts 的 WECOM_BOT_WS_MEDIA_GUIDANCE 通过 system context 引导 LLM 用
    // "MEDIA: <path>" 单独一行发文件，但之前没 outbound 解析。这里抽出每一条
    // MEDIA: 行作为媒体路径，复用 sendMediaInternal 的三层（kefu/botWs/agent）发送链。
    const { residualText, mediaPaths } = extractMediaDirectives(text);
    let lastMediaResult:
      | { channel: "wecom"; messageId: string; timestamp: number }
      | null = null;
    if (mediaPaths.length > 0) {
      console.log(
        `[wecom-outbound] MEDIA directive(s) detected (count=${mediaPaths.length}) for target=${String(to ?? "")}`,
      );
      for (const mediaUrl of mediaPaths) {
        try {
          lastMediaResult = await sendMediaInternal({
            ...ctx,
            mediaUrl,
            text: "", // MEDIA: 行不带 caption，纯文件
          });
          console.log(`[wecom-outbound] MEDIA directive sent ok: ${mediaUrl}`);
        } catch (err) {
          // 单个 media 失败不吞整批：记 warn，继续发剩下的 + residualText
          console.warn(
            `[wecom-outbound] MEDIA directive failed (${mediaUrl}): ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      }
      // 把后续逻辑用的 text 替换为去掉 MEDIA: 行的残余
      text = residualText;
    }
    // 残余文字为空且确实发了 media → 直接返回最后一次 media 的结果
    if (!String(text ?? "").trim() && lastMediaResult) {
      return lastMediaResult;
    }
    // ──────────────────────────────────────────────────────────────────────────

    // signal removed - not supported in current SDK
    // Defer Agent resolution until the Agent fallback path
    // sendTextViaBotWs() can already deliver without Agent mode

    // 体验优化：/new /reset 的“New session started”回执在 OpenClaw 核心里是英文固定文案，
    // 且通过 routeReply 走 wecom outbound（Agent 主动发送）。
    // 在 WeCom“双模式”场景下，这会造成：
    // - 用户在 Bot 会话发 /new，但却收到一条 Agent 私信回执（双重回复/错会话）。
    // 因此：
    // - Bot 会话目标：抑制该回执（Bot 会话里由 wecom 插件补中文回执）。
    // - Agent 会话目标（wecom-agent:）：允许发送，但改写成中文。
    let outgoingText = text;
    const trimmed = String(outgoingText ?? "").trim();
    const rawTo = typeof to === "string" ? to.trim().toLowerCase() : "";
    const isAgentSessionTarget = rawTo.startsWith("wecom-agent:");
    const looksLikeNewSessionAck = /new session started/i.test(trimmed) && /model:/i.test(trimmed);

    if (looksLikeNewSessionAck) {
      if (!isAgentSessionTarget) {
        // Suppress ack without agent resolution
        return { channel: "wecom", messageId: `suppressed-${Date.now()}`, timestamp: Date.now() };
      }

      const modelLabel = (() => {
        const m = trimmed.match(/model:\s*([^\n()]+)\s*/i);
        return m?.[1]?.trim();
      })();
      const rewritten = modelLabel ? `✅ 已开启新会话（模型：${modelLabel}）` : "✅ 已开启新会话。";
      outgoingText = rewritten;
    }

    let sentViaBotWs = false;
    let sentViaKefu = false;
    let agent: ReturnType<typeof resolveAgentConfigOrThrow> | null = null;

    try {
      sentViaKefu = await sendTextViaKefu({
        cfg,
        accountId,
        to,
        text: outgoingText,
        sessionKey,
      });
      if (!sentViaKefu) {
        sentViaBotWs = await sendTextViaBotWs({
          cfg,
          accountId,
          to,
          text: outgoingText,
          sessionKey,
        });
      }
      if (!sentViaKefu && !sentViaBotWs) {
        // Defer Agent resolution until needed for fallback
        agent = resolveAgentConfigOrThrow({ cfg, accountId });
        getAccountRuntime(agent.accountId)?.log.info?.(
          `[wecom-outbound] Sending text to target=${String(to ?? "")} (len=${outgoingText.length})`,
        );
        const deliveryService = new WecomAgentDeliveryService(agent);

        // 先把 markdown 中的 ![alt](url) 抽出来,单独作为 image 消息下发。
        // 企微 markdown_v2 虽然声称支持 ![](url),实际 CDN/外链图片经常渲染失败,
        // 用 uploadMedia + image 消息可靠性更高。失败时回退为内嵌 markdown 图片。
        const { images, residualText } = extractMarkdownImages(outgoingText);
        let textToSend = residualText;

        for (const image of images) {
          try {
            const payload = await loadImageAsPayload(image.url);
            await deliveryService.sendMedia({
              to,
              buffer: payload.buffer,
              filename: payload.filename,
              contentType: payload.contentType,
            });
            console.log(
              `[wecom-outbound] Sent inline image to ${String(to ?? "")} (src=${image.url}, ${payload.buffer.length}B)`,
            );
          } catch (imgErr) {
            const failureReason = imgErr instanceof Error ? imgErr.message : String(imgErr);
            console.warn(
              `[wecom-outbound] Inline image upload failed (src=${image.url}): ${failureReason}`,
            );
            // 预签名 URL 插件下载失败，企微客户端同样会失败。用纯文字占位，不写回 markdown。
            const placeholder = buildImageFailurePlaceholder(image.alt, failureReason);
            textToSend = textToSend ? `${textToSend}\n\n${placeholder}` : placeholder;
          }
        }

        // markdown_v2 原生支持表格/链接/标题/粗体/代码块,不再需要 textcard 降级
        const MARKDOWN_PATTERNS = /^#{1,6}\s|\*\*[^*\n]+\*\*|\[[^\]\n]+\]\([^)\s]+\)|`[^`\n]+`|```|^>\s|^\s*[-*+]\s|\|.*\||!\[[^\]\n]*\]\(/m;
        // 兜底：同 Bot WS 路径，消除任何漏网的 `![](url)`，避免客户端再去拉不可达 URL。
        textToSend = sanitizeResidualImageMarkdown(textToSend);
        if (textToSend.trim()) {
          if (MARKDOWN_PATTERNS.test(textToSend)) {
            const markdownText = toWeComMarkdownV2(textToSend);
            console.log(
              `[wecom-outbound] Markdown features detected, sending as markdown_v2 to target=${String(to ?? "")} (len=${markdownText.length})`,
            );
            await deliveryService.sendMarkdown({ to, text: markdownText });
            console.log(`[wecom-outbound] Successfully sent Agent markdown_v2 to ${String(to ?? "")}`);
          } else {
            await deliveryService.sendText({
              to,
              text: textToSend,
            });
            console.log(`[wecom-outbound] Successfully sent Agent text to ${String(to ?? "")}`);
          }
        } else if (images.length === 0) {
          console.log(`[wecom-outbound] Empty text, nothing to send to ${String(to ?? "")}`);
        }
      }
    } catch (err) {
      if (agent) {
        getAccountRuntime(agent.accountId)?.log.error?.(
          `[wecom-outbound] Failed to send text to ${String(to ?? "")}: ${err instanceof Error ? err.message : String(err)}`,
        );
      }
      throw err;
    }

    const transport = sentViaKefu ? "kefu" : sentViaBotWs ? "bot-ws" : "agent";
    return {
      channel: "wecom",
      messageId: `${transport}-${Date.now()}`,
      timestamp: Date.now(),
    };
  },
  // v2.8.19 — sendMedia 公开入口直接复用 sendMediaInternal（与 sendText 的 MEDIA: 解析路径同源）
  sendMedia: sendMediaInternal,
};
