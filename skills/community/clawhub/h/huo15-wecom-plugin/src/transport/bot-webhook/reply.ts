import type { ReplyContext } from "../../types/index.js";

export function createBotWebhookReplyContext(params: {
  accountId: string;
  responseUrl?: string;
  raw: ReplyContext["raw"];
}): ReplyContext {
  return {
    transport: "bot-webhook",
    accountId: params.accountId,
    responseUrl: params.responseUrl,
    passiveWindowMs: 5_000,
    raw: params.raw,
  };
}
