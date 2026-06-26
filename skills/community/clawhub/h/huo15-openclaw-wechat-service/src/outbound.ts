/**
 * 微信服务号 outbound adapter
 *
 * 支持两条发送路径：
 * 1. **客服消息**（默认）：48 小时会话窗口内可主动下发文字/图片/图文等
 * 2. **图片上传后发送**：用 media/upload 拿 media_id，再发 customer-service 图片消息
 *
 * 无法直接主动推送陌生用户（微信平台限制），只能在用户与公众号交互过的 48h 窗口内发。
 */

import type { ChannelOutboundAdapter } from "openclaw/plugin-sdk/channel-send-result";

import { accessTokenHandleFor } from "./access-token.js";
import {
  sendCustomerServiceMessage,
  type CustomerServiceMessage,
} from "./api/customer-service.js";
import {
  resolveWechatServiceAccount,
  resolveWechatServiceAccountConflict,
  resolveWechatServiceAccounts,
} from "./config/accounts.js";
import { uploadTemporaryMedia } from "./api/material.js";
import { getAccountRuntime, updateAccountRuntime } from "./app/index.js";
import type { WechatServiceConfig } from "./types.js";

type WechatServiceOutboundContext = Parameters<
  NonNullable<ChannelOutboundAdapter["sendText"]>
>[0];
type WechatServiceOutboundCfg = WechatServiceOutboundContext["cfg"];

const TARGET_PREFIX = /^(wechat-service|wechat|mp|offiaccount|服务号|公众号):(user|direct):/i;

function resolveOutboundAccount(params: {
  cfg: WechatServiceOutboundCfg;
  accountId?: string | null;
}) {
  const resolvedAccounts = resolveWechatServiceAccounts(params.cfg);
  const conflictAccountId =
    params.accountId?.trim() || resolvedAccounts.defaultAccountId;
  const conflict = resolveWechatServiceAccountConflict({
    cfg: params.cfg,
    accountId: conflictAccountId,
  });
  if (conflict) {
    throw new Error(conflict.message);
  }
  const requestedAccountId = params.accountId?.trim();
  if (requestedAccountId && !resolvedAccounts.accounts[requestedAccountId]) {
    throw new Error(
      `WeChat Service outbound account "${requestedAccountId}" not found. Configure channels["wechat-service"].accounts.${requestedAccountId}.`,
    );
  }
  const account = resolveWechatServiceAccount({
    cfg: params.cfg,
    accountId: params.accountId,
  });
  if (!account.configured) {
    throw new Error(
      `WeChat Service outbound account "${account.accountId}" is not configured (missing appId/appSecret/token).`,
    );
  }
  return account;
}

function normalizeWechatServiceTarget(raw: string | undefined): string {
  const trimmed = String(raw ?? "").trim();
  if (!trimmed) {
    throw new Error("WeChat Service outbound requires a target openid.");
  }
  const stripped = trimmed.replace(TARGET_PREFIX, "").trim();
  return stripped || trimmed;
}

function sliceCsText(input: string): string {
  // 客服消息文本最大长度约 2000 字符（官方未严格给字节数）
  return input.slice(0, 2000);
}

async function sendTextMessage(ctx: WechatServiceOutboundContext): Promise<{
  messageId: string;
  timestamp: number;
}> {
  const account = resolveOutboundAccount({
    cfg: ctx.cfg,
    accountId: ctx.accountId,
  });
  const openid = normalizeWechatServiceTarget(ctx.to);
  const tokenHandle = accessTokenHandleFor(account);
  const message: CustomerServiceMessage = {
    touser: openid,
    msgtype: "text",
    text: { content: sliceCsText(ctx.text ?? "") },
  };
  await sendCustomerServiceMessage({ account, tokenHandle, message });
  updateAccountRuntime(account.accountId, { lastOutboundAt: Date.now() });
  getAccountRuntime(account.accountId)?.log.info?.(
    `[wechat-service-outbound] sent text to openid=${openid} accountId=${account.accountId} (len=${(ctx.text ?? "").length})`,
  );
  return {
    messageId: `wechat-service-cs-text-${Date.now()}`,
    timestamp: Date.now(),
  };
}

async function sendMediaMessage(ctx: WechatServiceOutboundContext): Promise<{
  messageId: string;
  timestamp: number;
}> {
  if (!ctx.mediaUrl) {
    throw new Error("WeChat Service outbound requires mediaUrl.");
  }
  const account = resolveOutboundAccount({
    cfg: ctx.cfg,
    accountId: ctx.accountId,
  });
  const openid = normalizeWechatServiceTarget(ctx.to);
  const tokenHandle = accessTokenHandleFor(account);

  const fetched = await fetchMediaBuffer(ctx.mediaUrl);
  const mediaType = guessMediaType(fetched.contentType, ctx.mediaUrl);
  const upload = await uploadTemporaryMedia({
    account,
    tokenHandle,
    type: mediaType,
    buffer: fetched.buffer,
    filename: fetched.filename,
    contentType: fetched.contentType,
  });
  const message = buildMediaMessage({
    type: mediaType,
    openid,
    mediaId: upload.mediaId,
  });
  await sendCustomerServiceMessage({ account, tokenHandle, message });

  if (ctx.text && ctx.text.trim()) {
    await sendCustomerServiceMessage({
      account,
      tokenHandle,
      message: {
        touser: openid,
        msgtype: "text",
        text: { content: sliceCsText(ctx.text) },
      },
    });
  }

  updateAccountRuntime(account.accountId, { lastOutboundAt: Date.now() });
  getAccountRuntime(account.accountId)?.log.info?.(
    `[wechat-service-outbound] sent ${mediaType} to openid=${openid} accountId=${account.accountId} mediaUrl=${ctx.mediaUrl}`,
  );
  return {
    messageId: `wechat-service-cs-${mediaType}-${Date.now()}`,
    timestamp: Date.now(),
  };
}

type MediaType = "image" | "voice" | "video";

function buildMediaMessage(params: {
  type: MediaType;
  openid: string;
  mediaId: string;
}): CustomerServiceMessage {
  switch (params.type) {
    case "image":
      return {
        touser: params.openid,
        msgtype: "image",
        image: { media_id: params.mediaId },
      };
    case "voice":
      return {
        touser: params.openid,
        msgtype: "voice",
        voice: { media_id: params.mediaId },
      };
    case "video":
      return {
        touser: params.openid,
        msgtype: "video",
        video: {
          media_id: params.mediaId,
          thumb_media_id: params.mediaId,
        },
      };
  }
}

function guessMediaType(
  contentType: string | undefined,
  url: string,
): MediaType {
  const lower = (contentType ?? "").toLowerCase();
  if (lower.startsWith("image/")) return "image";
  if (lower.startsWith("audio/")) return "voice";
  if (lower.startsWith("video/")) return "video";
  const ext = url.split("?")[0]?.split(".").pop()?.toLowerCase() ?? "";
  if (["jpg", "jpeg", "png", "gif", "webp", "bmp"].includes(ext)) return "image";
  if (["mp3", "amr", "wav", "m4a"].includes(ext)) return "voice";
  if (["mp4", "mov", "webm", "mkv"].includes(ext)) return "video";
  return "image";
}

async function fetchMediaBuffer(mediaUrl: string): Promise<{
  buffer: Buffer;
  contentType: string;
  filename: string;
}> {
  const isRemote = /^https?:\/\//i.test(mediaUrl);
  if (isRemote) {
    const res = await fetch(mediaUrl, { signal: AbortSignal.timeout(30_000) });
    if (!res.ok) {
      throw new Error(
        `Failed to fetch media ${mediaUrl}: HTTP ${res.status}`,
      );
    }
    const buffer = Buffer.from(await res.arrayBuffer());
    const contentType =
      res.headers.get("content-type") ?? "application/octet-stream";
    const filename =
      new URL(mediaUrl).pathname.split("/").pop() || "media.bin";
    return { buffer, contentType, filename };
  }
  const fs = await import("node:fs/promises");
  const path = await import("node:path");
  const buffer = await fs.readFile(mediaUrl);
  const filename = path.basename(mediaUrl);
  const ext = path.extname(mediaUrl).slice(1).toLowerCase();
  const MIME: Record<string, string> = {
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    gif: "image/gif",
    webp: "image/webp",
    mp3: "audio/mpeg",
    amr: "audio/amr",
    wav: "audio/wav",
    mp4: "video/mp4",
  };
  const contentType = MIME[ext] ?? "application/octet-stream";
  return { buffer, contentType, filename };
}

export const wechatServiceOutbound: ChannelOutboundAdapter = {
  deliveryMode: "direct",
  chunkerMode: "text",
  textChunkLimit: 2000,
  sendText: async (ctx) => {
    const result = await sendTextMessage(ctx);
    return {
      channel: "wechat-service",
      messageId: result.messageId,
      timestamp: result.timestamp,
    };
  },
  sendMedia: async (ctx) => {
    const result = await sendMediaMessage(ctx);
    return {
      channel: "wechat-service",
      messageId: result.messageId,
      timestamp: result.timestamp,
    };
  },
};

void (undefined as unknown as WechatServiceConfig | undefined);
