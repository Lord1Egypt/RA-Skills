import type { PluginRuntime } from "openclaw/plugin-sdk";

import { getActiveReplyUrl } from "../../transport/bot-webhook/active-reply.js";
import { type StreamStore } from "../../monitor/state.js";
import type { WecomWebhookTarget } from "../../types/runtime-context.js";
import { pushFinalStreamReplyNow, resolveAgentAccountOrUndefined, sendAgentDmText } from "./fallback-delivery.js";
import type { BotRuntimeLogger, RecordBotOperationalEvent } from "./types.js";

export async function finalizeBotStream(params: {
  streamStore: StreamStore;
  target: WecomWebhookTarget;
  streamId: string;
  chatType: "group" | "direct";
  core: PluginRuntime;
  config: WecomWebhookTarget["config"];
  accountId: string;
  isResetCommand: boolean;
  resetCommandKind: string | null;
  logInfo: BotRuntimeLogger;
  logVerbose: BotRuntimeLogger;
  recordBotOperationalEvent: RecordBotOperationalEvent;
}): Promise<void> {
  const {
    streamStore,
    target,
    streamId,
    chatType,
    core,
    config,
    accountId,
    isResetCommand,
    resetCommandKind,
    logInfo,
    logVerbose,
    recordBotOperationalEvent,
  } = params;

  if (isResetCommand) {
    const current = streamStore.getStream(streamId);
    const hasAnyContent = Boolean(current?.content?.trim());
    if (current && !hasAnyContent) {
      const ackText = resetCommandKind === "reset" ? "✅ 已重置会话。" : "✅ 已开启新会话。";
      streamStore.updateStream(streamId, (s) => {
        s.content = ackText;
        s.finished = true;
      });
    }
  }

  streamStore.updateStream(streamId, (s) => {
    if (!s.content.trim() && !(s.images?.length ?? 0)) {
      s.content = "✅ 已处理完成。";
    }
  });

  streamStore.markFinished(streamId);

  const stateAfterFinish = streamStore.getStream(streamId);
  const responseUrl = getActiveReplyUrl(streamId);

  let responseUrlPushSucceeded = false;
  if (stateAfterFinish && responseUrl) {
    try {
      await pushFinalStreamReplyNow({ streamId, state: stateAfterFinish });
      responseUrlPushSucceeded = true;
      logVerbose(
        target,
        `final stream pushed via response_url streamId=${streamId}, chatType=${chatType}, images=${stateAfterFinish.images?.length ?? 0}`,
      );
    } catch (err) {
      target.runtime.error?.(`final stream push via response_url failed streamId=${streamId}: ${String(err)}`);
      recordBotOperationalEvent(target, {
        category: "fallback-delivery-failed",
        summary: `final stream push failed streamId=${streamId}`,
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }

  // Agent DM 兜底：当 response_url 推送失败、不可用，或已切到 fallback("timeout") 模式时，
  // 通过自建应用私信把完整内容发给触发用户。修复：长任务期间 deliver 沉默时
  // fallbackMode 不会被旁路触发，response_url 静默过期会让结果彻底丢失。
  const stateForDm = streamStore.getStream(streamId);
  const fallbackTriggered = stateForDm?.fallbackMode === "timeout";
  const needsDmFallback =
    !!stateForDm && !stateForDm.finalDeliveredAt && (!responseUrlPushSucceeded || fallbackTriggered);

  if (needsDmFallback && stateForDm) {
    const agentCfg = resolveAgentAccountOrUndefined(config, accountId);
    const dmText = (stateForDm.dmContent ?? stateForDm.content ?? "").trim();
    const dmReason = !responseUrlPushSucceeded ? "response-url-unavailable" : "fallback-timeout";

    if (agentCfg && stateForDm.userId && dmText) {
      try {
        logVerbose(
          target,
          `fallback(final-dm): 通过 Agent 私信发送完整内容 user=${stateForDm.userId} len=${dmText.length} reason=${dmReason}`,
        );
        await sendAgentDmText({ agent: agentCfg, userId: stateForDm.userId, text: dmText, core });
        logInfo(target, `fallback(final-dm): Agent 私信发送完成 user=${stateForDm.userId} reason=${dmReason}`);
      } catch (err) {
        target.runtime.error?.(`fallback(final-dm): Agent 私信发送失败 reason=${dmReason}: ${String(err)}`);
        recordBotOperationalEvent(target, {
          category: "fallback-delivery-failed",
          summary: `final dm fallback failed streamId=${streamId} user=${stateForDm.userId} reason=${dmReason}`,
          error: err instanceof Error ? err.message : String(err),
        });
      }
      streamStore.updateStream(streamId, (s) => {
        s.finalDeliveredAt = Date.now();
      });
    } else if (!responseUrlPushSucceeded) {
      const reasons: string[] = [];
      if (!agentCfg) reasons.push("agent-not-configured");
      if (!stateForDm.userId) reasons.push("user-id-missing");
      if (!dmText) reasons.push("empty-content");
      logInfo(
        target,
        `fallback(final-dm): 无法降级 Agent 私信 streamId=${streamId} reasons=${reasons.join(",")}`,
      );
      recordBotOperationalEvent(target, {
        category: "fallback-delivery-failed",
        summary: `final delivery dropped streamId=${streamId} reasons=${reasons.join(",")}`,
      });
      streamStore.updateStream(streamId, (s) => {
        s.finalDeliveredAt = Date.now();
      });
    }
  }

  logInfo(target, `queue: 当前批次结束，尝试推进下一批 streamId=${streamId}`);
  const ackStreamIds = streamStore.drainAckStreamsForBatch(streamId);
  if (ackStreamIds.length > 0) {
    const mergedDoneHint = "✅ 已合并处理完成，请查看上一条回复。";
    for (const ackId of ackStreamIds) {
      streamStore.updateStream(ackId, (s) => {
        s.content = mergedDoneHint;
        s.finished = true;
      });
    }
    logInfo(target, `queue: 已更新回执流 count=${ackStreamIds.length} batchStreamId=${streamId}`);
  }

  streamStore.onStreamFinished(streamId);
}
