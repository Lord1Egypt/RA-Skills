import { resolveDerivedPathSummary } from "../../config/index.js";

export function resolveKefuPaths(accountId: string): string[] {
  return resolveDerivedPathSummary(accountId).kefu;
}
