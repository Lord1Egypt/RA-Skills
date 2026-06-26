import type { IncomingMessage, ServerResponse } from "node:http";

import type { ResolvedBotAccount, WecomBotInboundMessage as WecomInboundMessage } from "../../types/index.js";
import { LIMITS } from "../../monitor/state.js";
import { computeWecomMsgSignature, encryptWecomPlaintext } from "../../crypto.js";
import type { StreamState } from "../../types/legacy-stream.js";
import type { WecomWebhookTarget } from "../../types/runtime-context.js";

function truncateUtf8Bytes(text: string, maxBytes: number): string {
  const buf = Buffer.from(text, "utf8");
  if (buf.length <= maxBytes) return text;
  const slice = buf.subarray(buf.length - maxBytes);
  return slice.toString("utf8");
}

export function jsonOk(res: ServerResponse, body: unknown): void {
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.end(JSON.stringify(body));
}

export async function readBotWebhookJsonBody(req: IncomingMessage, maxBytes: number) {
  const chunks: Buffer[] = [];
  let total = 0;
  return await new Promise<{ ok: boolean; value?: unknown; error?: string }>((resolve) => {
    req.on("data", (chunk: Buffer) => {
      total += chunk.length;
      if (total > maxBytes) {
        resolve({ ok: false, error: "payload too large" });
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => {
      try {
        const raw = Buffer.concat(chunks).toString("utf8");
        if (!raw.trim()) {
          resolve({ ok: false, error: "empty payload" });
          return;
        }
        resolve({ ok: true, value: JSON.parse(raw) as unknown });
      } catch (err) {
        resolve({ ok: false, error: err instanceof Error ? err.message : String(err) });
      }
    });
    req.on("error", (err) => {
      resolve({ ok: false, error: err instanceof Error ? err.message : String(err) });
    });
  });
}

export function buildEncryptedBotWebhookReply(params: {
  account: ResolvedBotAccount;
  plaintextJson: unknown;
  nonce: string;
  timestamp: string;
}): { encrypt: string; msgsignature: string; timestamp: string; nonce: string } {
  const plaintext = JSON.stringify(params.plaintextJson ?? {});
  const encrypt = encryptWecomPlaintext({
    encodingAESKey: params.account.encodingAESKey ?? "",
    receiveId: params.account.receiveId ?? "",
    plaintext,
  });
  const msgsignature = computeWecomMsgSignature({
    token: params.account.token ?? "",
    timestamp: params.timestamp,
    nonce: params.nonce,
    encrypt,
  });
  return {
    encrypt,
    msgsignature,
    timestamp: params.timestamp,
    nonce: params.nonce,
  };
}

export function resolveBotIdentitySet(target: WecomWebhookTarget): Set<string> {
  const ids = new Set<string>();
  const single = target.account.config.aibotid?.trim();
  if (single) ids.add(single);
  for (const botId of target.account.config.botIds ?? []) {
    const normalized = String(botId ?? "").trim();
    if (normalized) ids.add(normalized);
  }
  return ids;
}

export function buildStreamPlaceholderReply(params: {
  streamId: string;
  placeholderContent?: string;
}): { msgtype: "stream"; stream: { id: string; finish: boolean; content: string } } {
  const content = params.placeholderContent?.trim() || "1";
  return {
    msgtype: "stream",
    stream: {
      id: params.streamId,
      finish: false,
      content,
    },
  };
}

export function buildStreamTextPlaceholderReply(params: {
  streamId: string;
  content: string;
}): { msgtype: "stream"; stream: { id: string; finish: boolean; content: string } } {
  return {
    msgtype: "stream",
    stream: {
      id: params.streamId,
      finish: false,
      content: params.content.trim() || "1",
    },
  };
}

export function buildStreamReplyFromState(state: StreamState): {
  msgtype: "stream";
  stream: { id: string; finish: boolean; content: string; msg_item?: Array<{ msgtype: string; image: { base64: string; md5: string } }> };
} {
  const content = truncateUtf8Bytes(state.content, LIMITS.STREAM_MAX_BYTES);
  return {
    msgtype: "stream",
    stream: {
      id: state.streamId,
      finish: state.finished,
      content,
      ...(state.finished && state.images?.length
        ? {
            msg_item: state.images.map((img) => ({
              msgtype: "image",
              image: { base64: img.base64, md5: img.md5 },
            })),
          }
        : {}),
    },
  };
}

export function parseWecomPlainMessage(raw: string): WecomInboundMessage {
  const parsed = JSON.parse(raw) as unknown;
  if (!parsed || typeof parsed !== "object") {
    return {};
  }
  return parsed as WecomInboundMessage;
}
