import type { WecomRuntimeAuditEvent, WecomWebhookTarget } from "../../types/runtime-context.js";

export type BotRuntimeLogger = (target: WecomWebhookTarget, message: string) => void;

export type RecordBotOperationalEvent = (
  target: Pick<WecomWebhookTarget, "account" | "auditSink">,
  event: Omit<WecomRuntimeAuditEvent, "transport">,
) => void;
