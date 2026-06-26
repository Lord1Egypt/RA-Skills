import type { ReplyContext } from "../../types/index.js";

export function createAgentCallbackReplyContext(params: {
  accountId: string;
  raw: ReplyContext["raw"];
}): ReplyContext {
  return {
    transport: "agent-callback",
    accountId: params.accountId,
    passiveWindowMs: 5_000,
    raw: params.raw,
  };
}
