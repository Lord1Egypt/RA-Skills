import { resolveDerivedPathSummary } from "../../config/index.js";

export function resolveAgentCallbackPaths(accountId: string): string[] {
  return resolveDerivedPathSummary(accountId).agentCallback;
}
