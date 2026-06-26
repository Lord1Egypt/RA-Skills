import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";

import { prepareInboundSession } from "./session-manager.js";
import { dispatchRuntimeReply } from "./reply-orchestrator.js";
import type { RuntimeStore } from "../store/interfaces.js";
import type { WecomAuditLog } from "../observability/audit-log.js";
import { buildRawEnvelopeSummary } from "../observability/raw-envelope-log.js";
import type { ReplyHandle, UnifiedInboundEvent } from "../types/index.js";
import type { WecomMediaService } from "../shared/media-service.js";
import { registerActiveBotWsReplyHandle, unregisterActiveBotWsReplyHandle } from "../runtime.js";

export async function dispatchInboundEvent(params: {
  core: PluginRuntime;
  cfg: OpenClawConfig;
  store: RuntimeStore;
  auditLog: WecomAuditLog;
  mediaService: WecomMediaService;
  event: UnifiedInboundEvent;
  replyHandle: ReplyHandle;
}): Promise<void> {
  const { core, cfg, store, auditLog, mediaService, event, replyHandle } = params;
  if (!store.markInboundSeen(event)) {
    auditLog.appendOperational({
      accountId: event.accountId,
      transport: event.transport,
      category: "duplicate-inbound",
      messageId: event.messageId,
      summary: buildRawEnvelopeSummary(event),
      raw: event.raw,
    });
    return;
  }
  auditLog.appendInbound({
    accountId: event.accountId,
    transport: event.transport,
    messageId: event.messageId,
    summary: buildRawEnvelopeSummary(event),
    raw: event.raw,
  });
  store.writeReplyContext(event.messageId, event.replyContext);
  const session = await prepareInboundSession({
    core,
    cfg,
    event,
    mediaService,
  });
  const sessionKey = session.ctx.SessionKey ?? session.route.sessionKey;
  registerActiveBotWsReplyHandle({
    accountId: event.accountId,
    sessionKey,
    peerKind: event.conversation.peerKind,
    peerId: event.conversation.peerId,
    handle: replyHandle,
  });
  try {
    await dispatchRuntimeReply({
      core,
      cfg,
      session,
      replyHandle,
    });
  } finally {
    unregisterActiveBotWsReplyHandle({
      accountId: event.accountId,
      sessionKey,
      peerKind: event.conversation.peerKind,
      peerId: event.conversation.peerId,
      handle: replyHandle,
    });
  }
}
