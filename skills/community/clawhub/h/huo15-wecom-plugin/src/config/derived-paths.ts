import { DEFAULT_ACCOUNT_ID } from "./accounts.js";
import type { WecomTransportKind } from "../types/runtime.js";
import { WEBHOOK_PATHS } from "../types/constants.js";

export function resolveDerivedPath(params: {
  accountId: string;
  transport: Extract<WecomTransportKind, "bot-webhook" | "agent-callback" | "kefu">;
  includeLegacy?: boolean;
}): string[] {
  const accountId = params.accountId.trim() || DEFAULT_ACCOUNT_ID;
  const isDefault = accountId === DEFAULT_ACCOUNT_ID;
  if (params.transport === "bot-webhook") {
    return isDefault
      ? [
          `${WEBHOOK_PATHS.BOT_PLUGIN}/${accountId}`,
          `${WEBHOOK_PATHS.BOT}/${accountId}`,
          WEBHOOK_PATHS.BOT_PLUGIN,
          WEBHOOK_PATHS.BOT_ALT,
          WEBHOOK_PATHS.BOT,
        ]
      : [`${WEBHOOK_PATHS.BOT_PLUGIN}/${accountId}`];
  }
  if (params.transport === "kefu") {
    return isDefault
      ? [
          `${WEBHOOK_PATHS.KEFU_PLUGIN}/${accountId}`,
          `${WEBHOOK_PATHS.KEFU}/${accountId}`,
          WEBHOOK_PATHS.KEFU_PLUGIN,
          WEBHOOK_PATHS.KEFU,
        ]
      : [`${WEBHOOK_PATHS.KEFU_PLUGIN}/${accountId}`];
  }
  return isDefault
    ? [
        `${WEBHOOK_PATHS.AGENT_PLUGIN}/${accountId}`,
        `${WEBHOOK_PATHS.AGENT}/${accountId}`,
        WEBHOOK_PATHS.AGENT_PLUGIN,
        WEBHOOK_PATHS.AGENT,
      ]
    : [`${WEBHOOK_PATHS.AGENT_PLUGIN}/${accountId}`];
}

export function resolveDerivedPathSummary(accountId: string): {
  botWebhook: string[];
  agentCallback: string[];
  kefu: string[];
} {
  return {
    botWebhook: resolveDerivedPath({ accountId, transport: "bot-webhook" }),
    agentCallback: resolveDerivedPath({ accountId, transport: "agent-callback" }),
    kefu: resolveDerivedPath({ accountId, transport: "kefu" }),
  };
}
