import crypto from "node:crypto";

import { wecomFetch } from "../../http.js";
import { LIMITS, type StreamStore } from "../../monitor/state.js";
import { getActiveReplyUrl, useActiveReplyOnce } from "../../transport/bot-webhook/active-reply.js";
import type { WecomWebhookTarget } from "../../types/runtime-context.js";
import { buildStreamReplyFromState } from "../../transport/bot-webhook/protocol.js";
import {
  buildFallbackPrompt,
  extractLocalFilePathsFromText,
  guessLocalPathContentType,
  resolveAgentAccountOrUndefined,
  sendAgentDmMedia,
  sendBotFallbackPromptNow,
} from "./fallback-delivery.js";
import type { BotRuntimeLogger } from "./types.js";

export async function handleDirectLocalPathIntent(params: {
  streamStore: StreamStore;
  target: WecomWebhookTarget;
  streamId: string;
  rawBody: string;
  userId: string;
  chatType: "group" | "direct";
  logVerbose: BotRuntimeLogger;
  looksLikeSendLocalFileIntent: (rawBody: string) => boolean;
}): Promise<boolean> {
  const { streamStore, target, streamId, rawBody, userId, chatType, logVerbose, looksLikeSendLocalFileIntent } = params;
  const directLocalPaths = extractLocalFilePathsFromText(rawBody);
  if (directLocalPaths.length) {
    logVerbose(
      target,
      `local-path: 检测到用户消息包含本机路径 count=${directLocalPaths.length} intent=${looksLikeSendLocalFileIntent(rawBody)}`,
    );
  }
  if (!directLocalPaths.length || !looksLikeSendLocalFileIntent(rawBody)) {
    return false;
  }

  const fs = await import("node:fs/promises");
  const pathModule = await import("node:path");
  const imageExts = new Set(["png", "jpg", "jpeg", "gif", "webp", "bmp"]);

  const imagePaths: string[] = [];
  const otherPaths: string[] = [];
  for (const p of directLocalPaths) {
    const ext = pathModule.extname(p).slice(1).toLowerCase();
    if (imageExts.has(ext)) imagePaths.push(p);
    else otherPaths.push(p);
  }

  if (imagePaths.length > 0 && otherPaths.length === 0) {
    const loaded: Array<{ base64: string; md5: string; path: string }> = [];
    for (const p of imagePaths) {
      try {
        const buf = await fs.readFile(p);
        const base64 = buf.toString("base64");
        const md5 = crypto.createHash("md5").update(buf).digest("hex");
        loaded.push({ base64, md5, path: p });
      } catch (err) {
        target.runtime.error?.(`local-path: 读取图片失败 path=${p}: ${String(err)}`);
      }
    }

    if (loaded.length > 0) {
      streamStore.updateStream(streamId, (s) => {
        s.images = loaded.map(({ base64, md5 }) => ({ base64, md5 }));
        s.content = loaded.length === 1 ? `已发送图片（${pathModule.basename(loaded[0]!.path)}）` : `已发送 ${loaded.length} 张图片`;
        s.finished = true;
      });

      const responseUrl = getActiveReplyUrl(streamId);
      if (responseUrl) {
        try {
          const finalReply = buildStreamReplyFromState(streamStore.getStream(streamId)!) as unknown as Record<string, unknown>;
          await useActiveReplyOnce(streamId, async ({ responseUrl, proxyUrl }) => {
            const res = await wecomFetch(
              responseUrl,
              {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(finalReply),
              },
              { proxyUrl, timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
            );
            if (!res.ok) throw new Error(`local-path image push failed: ${res.status}`);
          });
          logVerbose(target, `local-path: 已通过 Bot response_url 推送图片 frames=final images=${loaded.length}`);
        } catch (err) {
          target.runtime.error?.(`local-path: Bot 主动推送图片失败（将依赖 stream_refresh 拉取）: ${String(err)}`);
        }
      } else {
        logVerbose(target, "local-path: 无 response_url，等待 stream_refresh 拉取最终图片");
      }
      streamStore.onStreamFinished(streamId);
      return true;
    }

    const agentCfg = resolveAgentAccountOrUndefined(target.config, target.account.accountId);
    const agentOk = Boolean(agentCfg);
    const fallbackName = imagePaths.length === 1 ? (imagePaths[0]!.split("/").pop() || "image") : `${imagePaths.length} 张图片`;
    const prompt = buildFallbackPrompt({
      kind: "media",
      agentConfigured: agentOk,
      userId,
      filename: fallbackName,
      chatType,
    });

    streamStore.updateStream(streamId, (s) => {
      s.fallbackMode = "error";
      s.finished = true;
      s.content = prompt;
      s.fallbackPromptSentAt = s.fallbackPromptSentAt ?? Date.now();
    });

    try {
      await sendBotFallbackPromptNow({ streamId, text: prompt });
      logVerbose(target, "local-path: 图片读取失败后已推送兜底提示");
    } catch (err) {
      target.runtime.error?.(`local-path: 图片读取失败后的兜底提示推送失败: ${String(err)}`);
    }

    if (agentCfg && userId && userId !== "unknown") {
      for (const p of imagePaths) {
        const guessedType = guessLocalPathContentType(p);
        try {
          await sendAgentDmMedia({
            agent: agentCfg,
            userId,
            mediaUrlOrPath: p,
            contentType: guessedType,
            filename: p.split("/").pop() || "image",
          });
          streamStore.updateStream(streamId, (s) => {
            s.agentMediaKeys = Array.from(new Set([...(s.agentMediaKeys ?? []), p]));
          });
          logVerbose(
            target,
            `local-path: 图片已通过 Agent 私信发送 user=${userId} path=${p} contentType=${guessedType ?? "unknown"}`,
          );
        } catch (err) {
          target.runtime.error?.(`local-path: 图片 Agent 私信兜底失败 path=${p}: ${String(err)}`);
        }
      }
    }
    streamStore.onStreamFinished(streamId);
    return true;
  }

  if (otherPaths.length > 0) {
    const agentCfg = resolveAgentAccountOrUndefined(target.config, target.account.accountId);
    const agentOk = Boolean(agentCfg);
    const filename = otherPaths.length === 1 ? otherPaths[0]!.split("/").pop()! : `${otherPaths.length} 个文件`;
    const prompt = buildFallbackPrompt({
      kind: "media",
      agentConfigured: agentOk,
      userId,
      filename,
      chatType,
    });

    streamStore.updateStream(streamId, (s) => {
      s.fallbackMode = "media";
      s.finished = true;
      s.content = prompt;
      s.fallbackPromptSentAt = s.fallbackPromptSentAt ?? Date.now();
    });

    try {
      await sendBotFallbackPromptNow({ streamId, text: prompt });
      logVerbose(target, "local-path: 文件兜底提示已推送");
    } catch (err) {
      target.runtime.error?.(`local-path: 文件兜底提示推送失败: ${String(err)}`);
    }

    if (!agentCfg) {
      streamStore.onStreamFinished(streamId);
      return true;
    }
    if (!userId || userId === "unknown") {
      target.runtime.error?.("local-path: 无法识别触发者 userId，无法 Agent 私信发送文件");
      streamStore.onStreamFinished(streamId);
      return true;
    }

    for (const p of otherPaths) {
      const alreadySent = streamStore.getStream(streamId)?.agentMediaKeys?.includes(p);
      if (alreadySent) continue;
      const guessedType = guessLocalPathContentType(p);
      try {
        await sendAgentDmMedia({
          agent: agentCfg,
          userId,
          mediaUrlOrPath: p,
          contentType: guessedType,
          filename: p.split("/").pop() || "file",
        });
        streamStore.updateStream(streamId, (s) => {
          s.agentMediaKeys = Array.from(new Set([...(s.agentMediaKeys ?? []), p]));
        });
        logVerbose(
          target,
          `local-path: 文件已通过 Agent 私信发送 user=${userId} path=${p} contentType=${guessedType ?? "unknown"}`,
        );
      } catch (err) {
        target.runtime.error?.(`local-path: Agent 私信发送文件失败 path=${p}: ${String(err)}`);
      }
    }
    streamStore.onStreamFinished(streamId);
    return true;
  }

  return false;
}
