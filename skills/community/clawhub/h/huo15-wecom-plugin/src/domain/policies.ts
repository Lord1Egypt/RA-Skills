import type { ResolvedBotAccount, UnifiedInboundEvent } from "../types/index.js";

export function assertBotPrimaryTransport(account: ResolvedBotAccount): void {
  if (account.primaryTransport === "ws" && !account.wsConfigured) {
    throw new Error(`WeCom bot account "${account.accountId}" is missing bot.ws credentials.`);
  }
  if (account.primaryTransport === "webhook" && !account.webhookConfigured) {
    throw new Error(`WeCom bot account "${account.accountId}" is missing bot.webhook credentials.`);
  }
}

export function buildDedupKey(event: UnifiedInboundEvent): string {
  return `${event.accountId}:${event.transport}:${event.messageId}`;
}

export function resolveConversationKey(event: UnifiedInboundEvent): string {
  const conversation = event.conversation;
  return [event.accountId, conversation.peerKind, conversation.peerId, conversation.senderId].join(":");
}

export function normalizeWecomAllowFromEntry(raw: string): string {
  return raw
    .trim()
    .toLowerCase()
    .replace(/^wecom:/, "")
    .replace(/^user:/, "")
    .replace(/^userid:/, "");
}

export function isWecomSenderAllowed(senderUserId: string, allowFrom: string[]): boolean {
  const list = allowFrom.map((entry) => normalizeWecomAllowFromEntry(entry)).filter(Boolean);
  if (list.includes("*")) return true;
  const normalizedSender = normalizeWecomAllowFromEntry(senderUserId);
  if (!normalizedSender) return false;
  return list.includes(normalizedSender);
}
