import type { UnifiedInboundEvent } from "./runtime.js";

export type BotWsFrameHeaders = {
  req_id: string;
  [key: string]: unknown;
};

export type BotWsFrame<T = unknown> = {
  cmd?: string;
  headers: BotWsFrameHeaders;
  body?: T;
  errcode?: number;
  errmsg?: string;
};

export type AgentCallbackEnvelope = {
  xml: string;
  decrypted: Record<string, unknown>;
};

export type InboundEventMapper<T = unknown> = (payload: T) => UnifiedInboundEvent;
