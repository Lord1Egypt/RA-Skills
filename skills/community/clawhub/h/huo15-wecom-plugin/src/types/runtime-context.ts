import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";

import type { ResolvedBotAccount } from "./account.js";
import type { RawFrameReference, TransportSessionPatch, WecomAuditCategory, WecomTransportKind } from "./runtime.js";

export type WecomRuntimeEnv = {
  log?: (message: string) => void;
  error?: (message: string) => void;
};

export type WecomRuntimeAuditEvent = {
  transport: WecomTransportKind;
  category: WecomAuditCategory;
  summary: string;
  messageId?: string;
  raw?: RawFrameReference;
  error?: string;
};

export type WecomWebhookTarget = {
  account: ResolvedBotAccount;
  config: OpenClawConfig;
  runtime: WecomRuntimeEnv;
  core: PluginRuntime;
  path: string;
  touchTransportSession?: (patch: TransportSessionPatch) => void;
  auditSink?: (event: WecomRuntimeAuditEvent) => void;
};
