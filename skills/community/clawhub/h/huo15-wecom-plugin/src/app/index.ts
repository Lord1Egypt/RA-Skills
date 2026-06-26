import type { PluginRuntime } from "openclaw/plugin-sdk";
import { clearWecomSourceAccount } from "../runtime/source-registry.js";
import type { ReplyHandle } from "../types/index.js";
import { WecomAccountRuntime } from "./account-runtime.js";

let runtime: PluginRuntime | null = null;
const runtimes = new Map<string, WecomAccountRuntime>();
const botWsPushHandles = new Map<string, BotWsPushHandle>();
const activeBotWsReplyHandlesBySession = new Map<string, ReplyHandle>();
const activeBotWsReplyHandlesByPeer = new Map<string, ReplyHandle>();

export type BotWsPushHandle = {
  isConnected: () => boolean;
  sendMarkdown: (chatId: string, content: string) => Promise<void>;
  replyCommand: (params: {
    cmd: string;
    body?: Record<string, unknown>;
    headers?: ({ req_id?: string } & Record<string, string>) | undefined;
  }) => Promise<Record<string, unknown>>;
  sendMedia: (params: {
    chatId: string;
    mediaUrl: string;
    text?: string;
    mediaLocalRoots?: readonly string[];
    maxBytes?: number;
  }) => Promise<{
    ok: boolean;
    messageId?: string;
    rejected?: boolean;
    rejectReason?: string;
    error?: string;
  }>;
};

function normalizeOptional(value: string | null | undefined): string | undefined {
  const trimmed = String(value ?? "").trim();
  return trimmed || undefined;
}

function normalizePeerId(value: string | null | undefined): string | undefined {
  const trimmed = normalizeOptional(value);
  return trimmed ? trimmed.toLowerCase() : undefined;
}

function buildSessionHandleKey(accountId: string, sessionKey: string): string {
  return `${accountId}::session::${sessionKey}`;
}

function buildPeerHandleKey(
  accountId: string,
  peerKind: "direct" | "group",
  peerId: string,
): string {
  return `${accountId}::peer::${peerKind}::${peerId}`;
}

export function setWecomRuntime(next: PluginRuntime): void {
  runtime = next;
}

export function getWecomRuntime(): PluginRuntime {
  if (!runtime) {
    throw new Error("WeCom runtime not initialized");
  }
  return runtime;
}

export function registerAccountRuntime(accountRuntime: WecomAccountRuntime): void {
  runtimes.set(accountRuntime.account.accountId, accountRuntime);
  console.log(`[wecom-runtime] register account=${accountRuntime.account.accountId}`);
}

export function getAccountRuntime(accountId: string): WecomAccountRuntime | undefined {
  return runtimes.get(accountId);
}

export function getAccountRuntimeSnapshot(accountId: string) {
  return runtimes.get(accountId)?.buildRuntimeStatus();
}

export function registerBotWsPushHandle(accountId: string, handle: BotWsPushHandle): void {
  botWsPushHandles.set(accountId, handle);
}

export function getBotWsPushHandle(accountId: string): BotWsPushHandle | undefined {
  return botWsPushHandles.get(accountId);
}

export function registerActiveBotWsReplyHandle(params: {
  accountId: string;
  sessionKey?: string | null;
  peerKind?: "direct" | "group" | null;
  peerId?: string | null;
  handle: ReplyHandle;
}): void {
  const accountId = normalizeOptional(params.accountId);
  const sessionKey = normalizeOptional(params.sessionKey);
  const peerId = normalizePeerId(params.peerId);
  if (!accountId) {
    return;
  }
  if (sessionKey) {
    activeBotWsReplyHandlesBySession.set(
      buildSessionHandleKey(accountId, sessionKey),
      params.handle,
    );
  }
  if ((params.peerKind === "direct" || params.peerKind === "group") && peerId) {
    activeBotWsReplyHandlesByPeer.set(
      buildPeerHandleKey(accountId, params.peerKind, peerId),
      params.handle,
    );
  }
}

export function getActiveBotWsReplyHandle(params: {
  accountId: string;
  sessionKey?: string | null;
  peerKind?: "direct" | "group" | null;
  peerId?: string | null;
}): ReplyHandle | undefined {
  const accountId = normalizeOptional(params.accountId);
  const sessionKey = normalizeOptional(params.sessionKey);
  const peerId = normalizePeerId(params.peerId);
  if (!accountId) {
    return undefined;
  }
  if (sessionKey) {
    const handle = activeBotWsReplyHandlesBySession.get(
      buildSessionHandleKey(accountId, sessionKey),
    );
    if (handle) {
      return handle;
    }
  }
  if ((params.peerKind === "direct" || params.peerKind === "group") && peerId) {
    return activeBotWsReplyHandlesByPeer.get(
      buildPeerHandleKey(accountId, params.peerKind, peerId),
    );
  }
  return undefined;
}

export function unregisterActiveBotWsReplyHandle(params: {
  accountId: string;
  sessionKey?: string | null;
  peerKind?: "direct" | "group" | null;
  peerId?: string | null;
  handle?: ReplyHandle;
}): void {
  const accountId = normalizeOptional(params.accountId);
  const sessionKey = normalizeOptional(params.sessionKey);
  const peerId = normalizePeerId(params.peerId);
  if (!accountId) {
    return;
  }
  if (sessionKey) {
    const key = buildSessionHandleKey(accountId, sessionKey);
    const current = activeBotWsReplyHandlesBySession.get(key);
    if (!params.handle || current === params.handle) {
      activeBotWsReplyHandlesBySession.delete(key);
    }
  }
  if ((params.peerKind === "direct" || params.peerKind === "group") && peerId) {
    const key = buildPeerHandleKey(accountId, params.peerKind, peerId);
    const current = activeBotWsReplyHandlesByPeer.get(key);
    if (!params.handle || current === params.handle) {
      activeBotWsReplyHandlesByPeer.delete(key);
    }
  }
}

export function unregisterBotWsPushHandle(accountId: string): void {
  botWsPushHandles.delete(accountId);
}

export function unregisterAccountRuntime(accountId: string): void {
  runtimes.delete(accountId);
  botWsPushHandles.delete(accountId);
  for (const key of activeBotWsReplyHandlesBySession.keys()) {
    if (key.startsWith(`${accountId}::`)) {
      activeBotWsReplyHandlesBySession.delete(key);
    }
  }
  for (const key of activeBotWsReplyHandlesByPeer.keys()) {
    if (key.startsWith(`${accountId}::`)) {
      activeBotWsReplyHandlesByPeer.delete(key);
    }
  }
  clearWecomSourceAccount(accountId);
  console.log(`[wecom-runtime] unregister account=${accountId}`);
}
