import type { RawFrameReference, UnifiedInboundEvent } from "../types/index.js";

function summarizeRawHeaders(raw: RawFrameReference): string | undefined {
  const reqId = typeof raw.headers?.req_id === "string" ? raw.headers.req_id : undefined;
  const eventId = typeof raw.headers?.event_id === "string" ? raw.headers.event_id : undefined;
  return [reqId ? `req_id=${reqId}` : undefined, eventId ? `event_id=${eventId}` : undefined]
    .filter((part): part is string => Boolean(part))
    .join(" ");
}

export function buildRawFrameReferenceSummary(raw: RawFrameReference): string {
  const parts = [
    `envelope=${raw.envelopeType}`,
    raw.command ? `cmd=${raw.command}` : undefined,
    summarizeRawHeaders(raw),
  ].filter((part): part is string => Boolean(part));
  return parts.join(" ");
}

export function buildRawEnvelopeSummary(event: UnifiedInboundEvent): string {
  return [
    `transport=${event.transport}`,
    `kind=${event.inboundKind}`,
    `messageId=${event.messageId}`,
    `peer=${event.conversation.peerKind}:${event.conversation.peerId}`,
    buildRawFrameReferenceSummary(event.raw),
  ].join(" ");
}
