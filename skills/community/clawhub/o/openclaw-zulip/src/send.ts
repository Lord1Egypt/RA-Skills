/**
 * Zulip message sending — maps OpenClaw outbound calls to ZulipClient.
 */

import { ZulipClient } from "./client.js";
import { DEFAULT_TOPIC } from "./constants.js";
import { normalizeZulipMessagingTarget, parseStreamTopic } from "./normalize.js";
import { getZulipRuntime } from "./runtime.js";
import type { ZulipClientConfig } from "./types.js";

export type SendZulipOptions = {
  accountId?: string;
  replyTo?: string;
  client?: ZulipClient;
  clientConfig?: ZulipClientConfig;
};

export type SendZulipResult = {
  messageId: number;
  target: string;
};

function resolveTarget(to: string): string {
  const normalized = normalizeZulipMessagingTarget(to);
  if (normalized) {
    return normalized;
  }
  throw new Error(`Invalid Zulip target: ${to}`);
}

function resolveClient(opts: SendZulipOptions): ZulipClient {
  if (opts.client) {
    return opts.client;
  }
  if (opts.clientConfig) {
    return new ZulipClient(opts.clientConfig);
  }
  // Fallback: try runtime
  const runtime = getZulipRuntime();
  const client = (runtime as Record<string, unknown>).client;
  if (client instanceof ZulipClient) {
    return client;
  }
  throw new Error("No ZulipClient available — provide client or clientConfig");
}

/**
 * Send a text message to a Zulip stream#topic or DM target.
 */
export async function sendMessageZulip(
  to: string,
  text: string,
  opts: SendZulipOptions = {},
): Promise<SendZulipResult> {
  const target = resolveTarget(to);
  const client = resolveClient(opts);

  const payload = text.trim();
  if (!payload) {
    throw new Error("Message must be non-empty for Zulip sends");
  }

  const streamTopic = parseStreamTopic(target);

  if (streamTopic) {
    // Channel (stream) message
    const res = await client.sendMessage({
      type: "channel",
      to: streamTopic.stream,
      topic: streamTopic.topic ?? DEFAULT_TOPIC,
      content: payload,
    });
    return { messageId: res.id, target };
  }

  // DM — target should be a numeric user ID
  const userId = Number(target);
  if (!Number.isFinite(userId)) {
    throw new Error(`Invalid DM target (expected numeric user ID): ${target}`);
  }
  const res = await client.sendMessage({
    type: "direct",
    to: [userId],
    content: payload,
  });
  return { messageId: res.id, target };
}

/**
 * Send a media file to a Zulip target.
 * Uploads the file first, then sends a message with the embedded link.
 */
export async function sendMediaZulip(
  to: string,
  filename: string,
  data: Blob,
  contentType: string,
  opts: SendZulipOptions & { caption?: string } = {},
): Promise<SendZulipResult> {
  const client = resolveClient(opts);
  const upload = await client.uploadFile(filename, data, contentType);
  const url = upload.url ?? upload.uri;
  const text = opts.caption ? `${opts.caption}\n[${filename}](${url})` : `[${filename}](${url})`;
  return sendMessageZulip(to, text, opts);
}
