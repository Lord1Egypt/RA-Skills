import type { OpenClawConfig } from "openclaw/plugin-sdk";

import { resolveDerivedPathSummary } from "./derived-paths.js";
import { DEFAULT_ACCOUNT_ID, resolveWecomAccount, resolveWecomAccounts } from "./accounts.js";
import type { ResolvedWecomAccount, WecomConfig } from "../types/index.js";

export type ResolvedRuntimeAccount = {
  account: ResolvedWecomAccount;
  derivedPaths: ReturnType<typeof resolveDerivedPathSummary>;
};

export type ResolvedRuntimeConfig = {
  raw: WecomConfig | undefined;
  defaultAccountId: string;
  accounts: Record<string, ResolvedRuntimeAccount>;
};

export function resolveWecomRuntimeConfig(cfg: OpenClawConfig): ResolvedRuntimeConfig {
  const raw = cfg.channels?.wecom as WecomConfig | undefined;
  const resolved = resolveWecomAccounts(cfg);
  const accounts = Object.fromEntries(
    Object.entries(resolved.accounts).map(([accountId, account]) => [
      accountId,
      {
        account,
        derivedPaths: resolveDerivedPathSummary(accountId),
      },
    ]),
  );
  return {
    raw,
    defaultAccountId: resolved.defaultAccountId || DEFAULT_ACCOUNT_ID,
    accounts,
  };
}

export function resolveWecomRuntimeAccount(params: {
  cfg: OpenClawConfig;
  accountId?: string | null;
}): ResolvedRuntimeAccount {
  const account = resolveWecomAccount(params);
  return {
    account,
    derivedPaths: resolveDerivedPathSummary(account.accountId),
  };
}
