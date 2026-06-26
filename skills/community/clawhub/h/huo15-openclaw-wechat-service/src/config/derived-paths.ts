import { DEFAULT_ACCOUNT_ID } from "./accounts.js";

export const WECHAT_SERVICE_ROUTE_PREFIX = "/plugins/wechat-service";
export const WECHAT_SERVICE_LEGACY_PREFIX = "/wechat-service";

export type DerivedPathSummary = {
  inbound: string[];
  primary: string;
};

export function resolveWebhookPath(accountId: string): string {
  const id = accountId.trim() || DEFAULT_ACCOUNT_ID;
  return `${WECHAT_SERVICE_ROUTE_PREFIX}/${id}`;
}

export function resolveDerivedPathSummary(accountId: string): DerivedPathSummary {
  const id = accountId.trim() || DEFAULT_ACCOUNT_ID;
  const primary = `${WECHAT_SERVICE_ROUTE_PREFIX}/${id}`;
  return {
    primary,
    inbound: [primary, `${WECHAT_SERVICE_LEGACY_PREFIX}/${id}`],
  };
}
