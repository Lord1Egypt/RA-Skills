import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";
import type { ReplyHandle } from "../types/index.js";
import type { PreparedSession } from "./session-manager.js";

export async function dispatchReplyPayload(params: {
  replyHandle: ReplyHandle;
  payload: {
    text?: string;
    mediaUrl?: string;
    mediaUrls?: string[];
    replyToId?: string;
    replyToTag?: boolean;
    replyToCurrent?: boolean;
    audioAsVoice?: boolean;
    isError?: boolean;
    isReasoning?: boolean;
    channelData?: Record<string, unknown>;
  };
  kind: "block" | "final";
}): Promise<void> {
  await params.replyHandle.deliver(params.payload, { kind: params.kind });
}

export async function dispatchRuntimeReply(params: {
  core: PluginRuntime;
  cfg: OpenClawConfig;
  session: PreparedSession;
  replyHandle: ReplyHandle;
}): Promise<void> {
  const { core, cfg, session, replyHandle } = params;
  const result = await core.channel.reply.dispatchReplyWithBufferedBlockDispatcher({
    ctx: session.ctx,
    cfg,
    // sourceReplyDeliveryMode 在某次 openclaw SDK 升级里从 GetReplyOptions 类型签名移除了，
    // 但 runtime 仍消费此字段（覆盖 2026.4.27 群聊默认 message_tool_only 导致 reply blocks
    // 被丢弃的问题）。as cast 绕过 EPC，等 SDK 类型补回再清理。
    replyOptions: {
      disableBlockStreaming: replyHandle.context.transport === "bot-ws" ? false : undefined,
      sourceReplyDeliveryMode: "automatic",
    } as Parameters<
      typeof core.channel.reply.dispatchReplyWithBufferedBlockDispatcher
    >[0]["replyOptions"],
    dispatcherOptions: {
      deliver: async (payload, info) => {
        await dispatchReplyPayload({
          replyHandle,
          payload,
          kind: info?.kind === "final" ? "final" : "block",
        });
      },
      onError: async (error) => {
        await replyHandle.fail?.(error);
      },
    },
  });


  if (
    replyHandle.context.transport === "bot-ws" &&
    result &&
    result.queuedFinal !== true &&
    (result.counts?.block ?? 0) > 0
  ) {
    await dispatchReplyPayload({
      replyHandle,
      payload: { text: "" },
      kind: "final",
    });
  }
}
