/**
 * Zulip inbound — normalize ZulipMessageEvent into OpenClaw inbound context.
 */

import { formatStreamTopic } from "./normalize.js";
import type { MessageEvent } from "./types.js";

export interface ZulipInboundMessage {
  /** Raw message text (Zulip content is HTML; we use the plain text source). */
  text: string;
  /** Sender user ID */
  senderId: number;
  /** Sender email */
  senderEmail: string;
  /** Sender display name */
  senderName: string;
  /** Is this a group (stream/channel) message? */
  isGroup: boolean;
  /** For group messages: stream name */
  stream?: string;
  /** For group messages: topic name */
  topic?: string;
  /** For DMs: list of recipient user IDs (excluding self) */
  dmRecipientIds?: number[];
  /** Zulip message ID */
  messageId: number;
  /** Unix timestamp */
  timestamp: number;
  /** Was the bot mentioned? */
  wasMentioned: boolean;
  /** Stream ID (for group messages) */
  streamId?: number;
}

/**
 * Convert a raw Zulip message event into a normalized inbound message.
 */
export function normalizeZulipEvent(event: MessageEvent, ownUserId?: number): ZulipInboundMessage {
  const msg = event.message;
  const isGroup = msg.type === "stream";
  const wasMentioned =
    event.flags?.includes("mentioned") || event.flags?.includes("wildcard_mentioned") || false;

  const result: ZulipInboundMessage = {
    text: msg.content,
    senderId: msg.sender_id,
    senderEmail: msg.sender_email,
    senderName: msg.sender_full_name,
    isGroup,
    messageId: msg.id,
    timestamp: msg.timestamp,
    wasMentioned,
  };

  if (isGroup) {
    result.stream = typeof msg.display_recipient === "string" ? msg.display_recipient : undefined;
    result.topic = msg.subject;
    result.streamId = msg.stream_id;
  } else {
    // DM — display_recipient is an array of user objects
    if (Array.isArray(msg.display_recipient)) {
      result.dmRecipientIds = msg.display_recipient
        .map((r: { id: number }) => r.id)
        .filter((id: number) => id !== ownUserId);
    }
  }

  return result;
}

/**
 * Build the OpenClaw target string for routing.
 */
export function buildInboundTarget(msg: ZulipInboundMessage, accountId: string): string {
  if (msg.isGroup && msg.stream) {
    const streamTopic = formatStreamTopic(msg.stream, msg.topic);
    return `zulip:${accountId}:group:${streamTopic}`;
  }
  return `zulip:${accountId}:direct:${msg.senderId}`;
}
