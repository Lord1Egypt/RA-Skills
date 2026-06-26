import type { TransportSessionSnapshot } from "../../types/index.js";

export function createBotWsSessionSnapshot(params: {
  accountId: string;
  ownerId: string;
  connected?: boolean;
  authenticated?: boolean;
  lastError?: string;
  running?: boolean;
  lastConnectedAt?: number;
  lastDisconnectedAt?: number;
  lastInboundAt?: number;
  lastOutboundAt?: number;
}): TransportSessionSnapshot {
  return {
    accountId: params.accountId,
    transport: "bot-ws",
    running: params.running ?? true,
    ownerId: params.ownerId,
    connected: params.connected,
    authenticated: params.authenticated,
    lastConnectedAt: params.lastConnectedAt ?? (params.connected ? Date.now() : undefined),
    lastDisconnectedAt: params.lastDisconnectedAt,
    lastInboundAt: params.lastInboundAt,
    lastOutboundAt: params.lastOutboundAt,
    lastError: params.lastError,
  };
}
