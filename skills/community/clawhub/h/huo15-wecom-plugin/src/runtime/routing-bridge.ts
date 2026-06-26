import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";

import {
  ensureDynamicAgentListed,
  generateAgentId,
  shouldUseDynamicAgent,
} from "../dynamic-agent.js";
import type { UnifiedInboundEvent } from "../types/index.js";

export function resolveRuntimeRoute(params: {
  core: PluginRuntime;
  cfg: OpenClawConfig;
  event: UnifiedInboundEvent;
}) {
  const route = params.core.channel.routing.resolveAgentRoute({
    cfg: params.cfg,
    channel: "wecom",
    accountId: params.event.accountId,
    peer: {
      kind: params.event.conversation.peerKind,
      id: params.event.conversation.peerId,
    },
  });

  const chatType = params.event.conversation.peerKind === "group" ? "group" : "dm";
  const useDynamicAgent = shouldUseDynamicAgent({
    chatType,
    senderId: params.event.conversation.senderId,
    config: params.cfg,
  });
  if (!useDynamicAgent) {
    return route;
  }

  const targetAgentId = generateAgentId(
    chatType,
    params.event.conversation.peerId,
    params.event.accountId,
  );
  route.agentId = targetAgentId;
  route.sessionKey = `agent:${targetAgentId}:wecom:${params.event.accountId}:${chatType}:${params.event.conversation.peerId}`;
  ensureDynamicAgentListed({
    agentId: targetAgentId,
    chatType,
    peerId: params.event.conversation.peerId,
    accountId: params.event.accountId,
    runtime: params.core,
  }).catch(() => {});
  return route;
}
