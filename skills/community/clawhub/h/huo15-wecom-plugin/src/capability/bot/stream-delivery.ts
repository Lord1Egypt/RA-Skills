import crypto from "node:crypto";

import type { PluginRuntime } from "openclaw/plugin-sdk";

import { wecomFetch } from "../../http.js";
import { LIMITS, type StreamStore } from "../../monitor/state.js";
import { getActiveReplyUrl, useActiveReplyOnce } from "../../transport/bot-webhook/active-reply.js";
import type { WecomWebhookTarget } from "../../types/runtime-context.js";
import { extractLocalImagePathsFromText } from "./fallback-delivery.js";
import {
  appendDmContent,
  buildFallbackPrompt,
  resolveAgentAccountOrUndefined,
  sendAgentDmMedia,
  sendBotFallbackPromptNow,
} from "./fallback-delivery.js";
import type { BotRuntimeLogger, RecordBotOperationalEvent } from "./types.js";

const STREAM_MAX_BYTES = LIMITS.STREAM_MAX_BYTES;
// 企微群机器人 response_url 实际有效期约 5 分钟。把窗口收紧到 4.5 分钟（switchAt = 4 分钟），
// 让 nearTimeout 在 response_url 还活着时触发，用户能在 4 分钟时看到 "转私信" 提示，
// 而不是等到企微已拒绝后才发现 prompt 推不出去。
const BOT_WINDOW_MS = 4.5 * 60 * 1000;
const BOT_SWITCH_MARGIN_MS = 30 * 1000;

export function createBotReplyDispatcher(params: {
  streamStore: StreamStore;
  target: WecomWebhookTarget;
  accountId: string;
  config: WecomWebhookTarget["config"];
  msg: any;
  streamId: string;
  rawBody: string;
  chatType: "group" | "direct";
  userId: string;
  core: PluginRuntime;
  tableMode: unknown;
  logVerbose: BotRuntimeLogger;
  truncateUtf8Bytes: (text: string, maxBytes: number) => string;
  recordBotOperationalEvent: RecordBotOperationalEvent;
}) {
  const {
    streamStore,
    target,
    accountId,
    config,
    msg,
    streamId,
    rawBody,
    chatType,
    userId,
    core,
    tableMode,
    logVerbose,
    truncateUtf8Bytes,
    recordBotOperationalEvent,
  } = params;

  return {
    deliver: async (payload: any, info: { kind?: string }) => {
      let text = payload.text ?? "";
      const thinkRegex = /<think>([\s\S]*?)<\/think>/g;
      const thinks: string[] = [];
      text = text.replace(thinkRegex, (match: string) => {
        thinks.push(match);
        return `__THINK_PLACEHOLDER_${thinks.length - 1}__`;
      });

      const trimmedText = text.trim();
      if (trimmedText.startsWith("{") && trimmedText.includes('"template_card"')) {
        try {
          const parsed = JSON.parse(trimmedText);
          if (parsed.template_card) {
            const isSingleChat = msg.chattype !== "group";
            const responseUrl = getActiveReplyUrl(streamId);

            if (responseUrl && isSingleChat) {
              await useActiveReplyOnce(streamId, async ({ responseUrl, proxyUrl }) => {
                const res = await wecomFetch(
                  responseUrl,
                  {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      msgtype: "template_card",
                      template_card: parsed.template_card,
                    }),
                  },
                  { proxyUrl, timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
                );
                if (!res.ok) {
                  throw new Error(`template_card send failed: ${res.status}`);
                }
              });
              logVerbose(target, `sent template_card: task_id=${parsed.template_card.task_id}`);
              streamStore.updateStream(streamId, (s) => {
                s.finished = true;
                s.content = "[已发送交互卡片]";
              });
              target.touchTransportSession?.({ lastOutboundAt: Date.now(), running: true });
              return;
            }

            logVerbose(target, `template_card fallback to text (group=${!isSingleChat}, hasUrl=${!!responseUrl})`);
            const cardTitle = parsed.template_card.main_title?.title || "交互卡片";
            const cardDesc = parsed.template_card.main_title?.desc || "";
            const buttons = parsed.template_card.button_list?.map((b: any) => b.text).join(" / ") || "";
            text = `📋 **${cardTitle}**${cardDesc ? `\n${cardDesc}` : ""}${buttons ? `\n\n选项: ${buttons}` : ""}`;
          }
        } catch {
          // keep normal text path
        }
      }

      text = core.channel.text.convertMarkdownTables(text, tableMode as any);
      thinks.forEach((think, i) => {
        text = text.replace(`__THINK_PLACEHOLDER_${i}__`, think);
      });

      const current = streamStore.getStream(streamId);
      if (!current) return;

      if (!current.images) current.images = [];
      if (!current.agentMediaKeys) current.agentMediaKeys = [];

      const deliverKind = info?.kind ?? "block";
      logVerbose(
        target,
        `deliver: kind=${deliverKind} chatType=${current.chatType ?? chatType} user=${current.userId ?? userId} textLen=${text.length} mediaCount=${(payload.mediaUrls?.length ?? 0) + (payload.mediaUrl ? 1 : 0)}`,
      );

      if (!payload.mediaUrl && !(payload.mediaUrls?.length ?? 0) && text.includes("/")) {
        const candidates = extractLocalImagePathsFromText({ text, mustAlsoAppearIn: rawBody });
        if (candidates.length > 0) {
          logVerbose(target, `media: 从输出文本推断到本机图片路径（来自用户原消息）count=${candidates.length}`);
          for (const p of candidates) {
            try {
              const fs = await import("node:fs/promises");
              const pathModule = await import("node:path");
              const buf = await fs.readFile(p);
              const ext = pathModule.extname(p).slice(1).toLowerCase();
              const imageExts: Record<string, string> = {
                jpg: "image/jpeg",
                jpeg: "image/jpeg",
                png: "image/png",
                gif: "image/gif",
                webp: "image/webp",
                bmp: "image/bmp",
              };
              const contentType = imageExts[ext] ?? "application/octet-stream";
              if (!contentType.startsWith("image/")) continue;
              const base64 = buf.toString("base64");
              const md5 = crypto.createHash("md5").update(buf).digest("hex");
              current.images.push({ base64, md5 });
              logVerbose(target, `media: 已加载本机图片用于 Bot 交付 path=${p}`);
            } catch (err) {
              target.runtime.error?.(`media: 读取本机图片失败 path=${p}: ${String(err)}`);
            }
          }
        }
      }

      if (text.trim()) {
        streamStore.updateStream(streamId, (s) => {
          appendDmContent(s, text);
        });
      }

      const now = Date.now();
      const deadline = current.createdAt + BOT_WINDOW_MS;
      const switchAt = deadline - BOT_SWITCH_MARGIN_MS;
      const nearTimeout = !current.fallbackMode && !current.finished && now >= switchAt;
      if (nearTimeout) {
        const agentCfg = resolveAgentAccountOrUndefined(config, accountId);
        const agentOk = Boolean(agentCfg);
        const prompt = buildFallbackPrompt({
          kind: "timeout",
          agentConfigured: agentOk,
          userId: current.userId,
          chatType: current.chatType,
        });
        logVerbose(
          target,
          `fallback(timeout): 触发切换（接近 6 分钟）chatType=${current.chatType} agentConfigured=${agentOk} hasResponseUrl=${Boolean(getActiveReplyUrl(streamId))}`,
        );
        streamStore.updateStream(streamId, (s) => {
          s.fallbackMode = "timeout";
          s.finished = true;
          s.content = prompt;
          s.fallbackPromptSentAt = s.fallbackPromptSentAt ?? Date.now();
        });
        try {
          await sendBotFallbackPromptNow({ streamId, text: prompt });
          logVerbose(target, "fallback(timeout): 群内提示已推送");
        } catch (err) {
          target.runtime.error?.(`wecom bot fallback prompt push failed (timeout) streamId=${streamId}: ${String(err)}`);
          recordBotOperationalEvent(target, {
            category: "fallback-delivery-failed",
            summary: `timeout prompt push failed streamId=${streamId}`,
            error: err instanceof Error ? err.message : String(err),
          });
        }
        return;
      }

      const mediaUrls = payload.mediaUrls || (payload.mediaUrl ? [payload.mediaUrl] : []);
      for (const mediaPath of mediaUrls) {
        let contentType: string | undefined;
        let filename = mediaPath.split("/").pop() || "attachment";
        try {
          let buf: Buffer;
          const looksLikeUrl = /^https?:\/\//i.test(mediaPath);

          if (looksLikeUrl) {
            const loaded = await core.channel.media.fetchRemoteMedia({ url: mediaPath });
            buf = loaded.buffer;
            contentType = loaded.contentType;
            filename = loaded.fileName ?? "attachment";
          } else {
            const fs = await import("node:fs/promises");
            const pathModule = await import("node:path");
            buf = await fs.readFile(mediaPath);
            filename = pathModule.basename(mediaPath);
            const ext = pathModule.extname(mediaPath).slice(1).toLowerCase();
            const imageExts: Record<string, string> = {
              jpg: "image/jpeg",
              jpeg: "image/jpeg",
              png: "image/png",
              gif: "image/gif",
              webp: "image/webp",
              bmp: "image/bmp",
            };
            contentType = imageExts[ext] ?? "application/octet-stream";
          }

          if (contentType?.startsWith("image/")) {
            const base64 = buf.toString("base64");
            const md5 = crypto.createHash("md5").update(buf).digest("hex");
            current.images.push({ base64, md5 });
            logVerbose(target, `media: 识别为图片 contentType=${contentType} filename=${filename}`);
          } else {
            const agentCfg = resolveAgentAccountOrUndefined(config, accountId);
            const agentOk = Boolean(agentCfg);
            const alreadySent = current.agentMediaKeys.includes(mediaPath);
            logVerbose(
              target,
              `fallback(media): 检测到非图片文件 chatType=${current.chatType} contentType=${contentType ?? "unknown"} filename=${filename} agentConfigured=${agentOk} alreadySent=${alreadySent} hasResponseUrl=${Boolean(getActiveReplyUrl(streamId))}`,
            );

            if (agentCfg && !alreadySent && current.userId) {
              try {
                await sendAgentDmMedia({
                  agent: agentCfg,
                  userId: current.userId,
                  mediaUrlOrPath: mediaPath,
                  contentType,
                  filename,
                });
                logVerbose(target, `fallback(media): 文件已通过 Agent 私信发送 user=${current.userId}`);
                streamStore.updateStream(streamId, (s) => {
                  s.agentMediaKeys = Array.from(new Set([...(s.agentMediaKeys ?? []), mediaPath]));
                });
              } catch (err) {
                target.runtime.error?.(`wecom agent dm media failed: ${String(err)}`);
                recordBotOperationalEvent(target, {
                  category: "fallback-delivery-failed",
                  summary: `agent media dm failed streamId=${streamId} filename=${filename}`,
                  error: err instanceof Error ? err.message : String(err),
                });
              }
            }

            if (!current.fallbackMode) {
              const prompt = buildFallbackPrompt({
                kind: "media",
                agentConfigured: agentOk,
                userId: current.userId,
                filename,
                chatType: current.chatType,
              });
              streamStore.updateStream(streamId, (s) => {
                s.fallbackMode = "media";
                s.finished = true;
                s.content = prompt;
                s.fallbackPromptSentAt = s.fallbackPromptSentAt ?? Date.now();
              });
              try {
                await sendBotFallbackPromptNow({ streamId, text: prompt });
                logVerbose(target, "fallback(media): 群内提示已推送");
              } catch (err) {
                target.runtime.error?.(`wecom bot fallback prompt push failed (media) streamId=${streamId}: ${String(err)}`);
                recordBotOperationalEvent(target, {
                  category: "fallback-delivery-failed",
                  summary: `media prompt push failed streamId=${streamId} filename=${filename}`,
                  error: err instanceof Error ? err.message : String(err),
                });
              }
            }
            return;
          }
        } catch (err) {
          target.runtime.error?.(`Failed to process outbound media: ${mediaPath}: ${String(err)}`);
          recordBotOperationalEvent(target, {
            category: "fallback-delivery-failed",
            summary: `outbound media processing failed streamId=${streamId} media=${mediaPath}`,
            error: err instanceof Error ? err.message : String(err),
          });
          const agentCfg = resolveAgentAccountOrUndefined(config, accountId);
          const agentOk = Boolean(agentCfg);
          const fallbackFilename = filename || mediaPath.split("/").pop() || "attachment";
          if (agentCfg && current.userId && !current.agentMediaKeys.includes(mediaPath)) {
            try {
              await sendAgentDmMedia({
                agent: agentCfg,
                userId: current.userId,
                mediaUrlOrPath: mediaPath,
                contentType,
                filename: fallbackFilename,
              });
              streamStore.updateStream(streamId, (s) => {
                s.agentMediaKeys = Array.from(new Set([...(s.agentMediaKeys ?? []), mediaPath]));
              });
              logVerbose(target, `fallback(error): 媒体处理失败后已通过 Agent 私信发送 user=${current.userId}`);
            } catch (sendErr) {
              target.runtime.error?.(`fallback(error): 媒体处理失败后的 Agent 私信发送也失败: ${String(sendErr)}`);
              recordBotOperationalEvent(target, {
                category: "fallback-delivery-failed",
                summary: `fallback error dm failed streamId=${streamId} filename=${fallbackFilename}`,
                error: sendErr instanceof Error ? sendErr.message : String(sendErr),
              });
            }
          }
          if (!current.fallbackMode) {
            const prompt = buildFallbackPrompt({
              kind: "error",
              agentConfigured: agentOk,
              userId: current.userId,
              filename: fallbackFilename,
              chatType: current.chatType,
            });
            streamStore.updateStream(streamId, (s) => {
              s.fallbackMode = "error";
              s.finished = true;
              s.content = prompt;
              s.fallbackPromptSentAt = s.fallbackPromptSentAt ?? Date.now();
            });
            try {
              await sendBotFallbackPromptNow({ streamId, text: prompt });
              logVerbose(target, "fallback(error): 群内提示已推送");
            } catch (pushErr) {
              target.runtime.error?.(`wecom bot fallback prompt push failed (error) streamId=${streamId}: ${String(pushErr)}`);
              recordBotOperationalEvent(target, {
                category: "fallback-delivery-failed",
                summary: `fallback error prompt push failed streamId=${streamId} filename=${fallbackFilename}`,
                error: pushErr instanceof Error ? pushErr.message : String(pushErr),
              });
            }
          }
          return;
        }
      }

      const mode = streamStore.getStream(streamId)?.fallbackMode;
      if (mode) return;

      const nextText = current.content ? `${current.content}\n\n${text}`.trim() : text.trim();
      streamStore.updateStream(streamId, (s) => {
        s.content = truncateUtf8Bytes(nextText, STREAM_MAX_BYTES);
        if (current.images?.length) s.images = current.images;
      });
      target.touchTransportSession?.({ lastOutboundAt: Date.now(), running: true });
    },
    onError: (err: unknown, info: { kind: string }) => {
      target.runtime.error?.(`[${accountId}] wecom ${info.kind} reply failed: ${String(err)}`);
      recordBotOperationalEvent(target, {
        category: "fallback-delivery-failed",
        summary: `reply dispatcher failed kind=${info.kind} streamId=${streamId}`,
        error: err instanceof Error ? err.message : String(err),
      });
    },
  };
}
