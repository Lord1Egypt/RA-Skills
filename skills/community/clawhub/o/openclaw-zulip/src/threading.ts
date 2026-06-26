/**
 * Zulip threading — topic ↔ OpenClaw thread mapping.
 *
 * In Zulip, topics ARE threads. Every message in a stream belongs to a topic,
 * making the mapping straightforward: thread = stream#topic.
 */

import { formatStreamTopic, parseStreamTopic } from "./normalize.js";

/**
 * Build a canonical thread identifier from stream + topic.
 */
export function formatThreadId(stream: string, topic: string): string {
  return formatStreamTopic(stream, topic);
}

/**
 * Parse a thread identifier back into stream + topic.
 * Returns undefined if the threadId doesn't contain a valid stream#topic.
 */
export function parseThreadId(threadId: string): { stream: string; topic: string } | undefined {
  const parsed = parseStreamTopic(threadId);
  if (!parsed || !parsed.topic) {
    return undefined;
  }
  return { stream: parsed.stream, topic: parsed.topic };
}

/**
 * Extract the topic name from a thread identifier.
 */
export function getThreadTopic(threadId: string): string | undefined {
  const parsed = parseThreadId(threadId);
  return parsed?.topic;
}

/**
 * In Zulip, every stream message is part of a topic (thread).
 * Returns true for all group/stream messages.
 */
export function isThreadMessage(msg: { isGroup: boolean; topic?: string }): boolean {
  return msg.isGroup && typeof msg.topic === "string" && msg.topic.length > 0;
}
