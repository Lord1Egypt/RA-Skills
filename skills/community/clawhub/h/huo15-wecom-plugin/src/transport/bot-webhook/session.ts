import type { TransportSessionSnapshot } from "../../types/index.js";

export function createBotWebhookSessionSnapshot(params: {
  accountId: string;
  running: boolean;
  lastInboundAt?: number;
  lastOutboundAt?: number;
  lastError?: string;
}): TransportSessionSnapshot {
  return {
    accountId: params.accountId,
    transport: "bot-webhook",
    running: params.running,
    ownerId: `${params.accountId}:bot-webhook`,
    connected: params.running,
    authenticated: true,
    lastConnectedAt: params.running ? Date.now() : undefined,
    lastDisconnectedAt: params.running ? undefined : Date.now(),
    lastInboundAt: params.lastInboundAt,
    lastOutboundAt: params.lastOutboundAt,
    lastError: params.lastError,
  };
}
