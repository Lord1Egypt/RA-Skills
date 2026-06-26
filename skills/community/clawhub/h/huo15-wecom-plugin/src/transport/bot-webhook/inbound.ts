import { resolveDerivedPathSummary } from "../../config/index.js";

export function resolveBotWebhookPaths(accountId: string): string[] {
  return resolveDerivedPathSummary(accountId).botWebhook;
}
