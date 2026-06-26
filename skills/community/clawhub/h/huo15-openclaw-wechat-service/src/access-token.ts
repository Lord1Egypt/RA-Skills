/**
 * access_token 管理器
 *
 * 微信服务号 access_token 有效期 7200s，每账号独立缓存。
 * - 提前 120s 刷新，避免 expires_in 边界
 * - 失败时短暂缓存失败结果，避免雪崩
 * - 并发调用复用同一个 in-flight 请求
 */

import type { ResolvedWechatServiceAccount } from "./types.js";
import { jsonRequest } from "./http-client.js";

export const ACCESS_TOKEN_EARLY_REFRESH_MS = 120_000;
export const ACCESS_TOKEN_FAILURE_COOLDOWN_MS = 5_000;

type TokenCacheEntry = {
  accountId: string;
  appId: string;
  accessToken: string;
  expiresAt: number;
  fetchedAt: number;
};

export type AccessTokenHandle = {
  getAccessToken(options?: { forceRefresh?: boolean }): Promise<string>;
  invalidate(): void;
  snapshot(): TokenCacheEntry | undefined;
};

type FetchFn = (params: {
  appId: string;
  appSecret: string;
  account: ResolvedWechatServiceAccount;
}) => Promise<{ accessToken: string; expiresIn: number }>;

const defaultFetch: FetchFn = async ({ appId, appSecret, account }) => {
  const data = await jsonRequest<{ access_token?: string; expires_in?: number }>({
    method: "GET",
    endpoint: "cgi-bin/token",
    query: {
      grant_type: "client_credential",
      appid: appId,
      secret: appSecret,
    },
    network: account.network,
  });
  if (!data.access_token) {
    throw new Error("[wechat-service] access_token missing in response");
  }
  return {
    accessToken: data.access_token,
    expiresIn: typeof data.expires_in === "number" ? data.expires_in : 7200,
  };
};

type ManagerOptions = {
  now?: () => number;
  fetcher?: FetchFn;
};

export class AccessTokenManager {
  private readonly cache = new Map<string, TokenCacheEntry>();
  private readonly inflight = new Map<string, Promise<TokenCacheEntry>>();
  private readonly now: () => number;
  private readonly fetcher: FetchFn;

  constructor(options: ManagerOptions = {}) {
    this.now = options.now ?? (() => Date.now());
    this.fetcher = options.fetcher ?? defaultFetch;
  }

  handle(account: ResolvedWechatServiceAccount): AccessTokenHandle {
    return {
      getAccessToken: (opts) => this.ensure(account, opts ?? {}),
      invalidate: () => this.invalidate(account.accountId),
      snapshot: () => this.cache.get(account.accountId),
    };
  }

  invalidate(accountId: string): void {
    this.cache.delete(accountId);
  }

  snapshot(accountId: string): TokenCacheEntry | undefined {
    return this.cache.get(accountId);
  }

  private async ensure(
    account: ResolvedWechatServiceAccount,
    opts: { forceRefresh?: boolean },
  ): Promise<string> {
    const { accountId, appId, appSecret } = account;
    if (!appId || !appSecret) {
      throw new Error(
        `[wechat-service] access_token requires appId/appSecret for account=${accountId}`,
      );
    }
    const existing = this.cache.get(accountId);
    const now = this.now();
    if (
      !opts.forceRefresh &&
      existing &&
      existing.appId === appId &&
      existing.expiresAt - now > ACCESS_TOKEN_EARLY_REFRESH_MS
    ) {
      return existing.accessToken;
    }
    const pending = this.inflight.get(accountId);
    if (pending) return (await pending).accessToken;

    const task = (async () => {
      try {
        const { accessToken, expiresIn } = await this.fetcher({
          appId,
          appSecret,
          account,
        });
        const entry: TokenCacheEntry = {
          accountId,
          appId,
          accessToken,
          expiresAt: now + Math.max(60, expiresIn) * 1000,
          fetchedAt: now,
        };
        this.cache.set(accountId, entry);
        return entry;
      } catch (err) {
        this.cache.delete(accountId);
        setTimeout(() => this.inflight.delete(accountId), ACCESS_TOKEN_FAILURE_COOLDOWN_MS).unref?.();
        throw err;
      } finally {
        this.inflight.delete(accountId);
      }
    })();

    this.inflight.set(accountId, task);
    const entry = await task;
    return entry.accessToken;
  }
}

const globalManager = new AccessTokenManager();

export function getGlobalAccessTokenManager(): AccessTokenManager {
  return globalManager;
}

export function accessTokenHandleFor(
  account: ResolvedWechatServiceAccount,
): AccessTokenHandle {
  return globalManager.handle(account);
}
