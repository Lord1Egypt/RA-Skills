import { describe, expect, it, vi } from "vitest";
import { AccessTokenManager } from "./access-token.js";
import type { ResolvedWechatServiceAccount } from "./types.js";

function mockAccount(accountId = "main"): ResolvedWechatServiceAccount {
  return {
    accountId,
    enabled: true,
    configured: true,
    appId: "wx_app",
    appSecret: "secret",
    token: "token",
    encodingAESKey: "",
    encryptMode: "plain",
    originalId: "",
    replyMode: "async",
    replyPlaceholderText: "",
    welcomeText: "",
    routing: {},
    config: { appId: "wx_app", appSecret: "secret", token: "token" },
  };
}

describe("AccessTokenManager", () => {
  it("caches token and reuses across calls", async () => {
    const fetcher = vi.fn(async () => ({ accessToken: "tok1", expiresIn: 7200 }));
    const mgr = new AccessTokenManager({ fetcher, now: () => 1_000_000 });
    const handle = mgr.handle(mockAccount());
    expect(await handle.getAccessToken()).toBe("tok1");
    expect(await handle.getAccessToken()).toBe("tok1");
    expect(fetcher).toHaveBeenCalledTimes(1);
  });

  it("refreshes when close to expiry", async () => {
    let currentNow = 1_000_000;
    const fetcher = vi
      .fn()
      .mockResolvedValueOnce({ accessToken: "tok1", expiresIn: 60 })
      .mockResolvedValueOnce({ accessToken: "tok2", expiresIn: 60 });
    const mgr = new AccessTokenManager({ fetcher, now: () => currentNow });
    const handle = mgr.handle(mockAccount());
    expect(await handle.getAccessToken()).toBe("tok1");
    currentNow += 61_000;
    expect(await handle.getAccessToken()).toBe("tok2");
    expect(fetcher).toHaveBeenCalledTimes(2);
  });

  it("forceRefresh bypasses cache", async () => {
    const fetcher = vi
      .fn()
      .mockResolvedValueOnce({ accessToken: "tok1", expiresIn: 7200 })
      .mockResolvedValueOnce({ accessToken: "tok2", expiresIn: 7200 });
    const mgr = new AccessTokenManager({ fetcher, now: () => 1_000_000 });
    const handle = mgr.handle(mockAccount());
    expect(await handle.getAccessToken()).toBe("tok1");
    expect(await handle.getAccessToken({ forceRefresh: true })).toBe("tok2");
  });

  it("de-duplicates concurrent in-flight requests", async () => {
    let resolveFirst: ((value: { accessToken: string; expiresIn: number }) => void) | null = null;
    const fetcher = vi.fn(
      () =>
        new Promise<{ accessToken: string; expiresIn: number }>((resolve) => {
          resolveFirst = resolve;
        }),
    );
    const mgr = new AccessTokenManager({ fetcher, now: () => 1_000_000 });
    const handle = mgr.handle(mockAccount());
    const p1 = handle.getAccessToken();
    const p2 = handle.getAccessToken();
    resolveFirst!({ accessToken: "same", expiresIn: 7200 });
    await expect(p1).resolves.toBe("same");
    await expect(p2).resolves.toBe("same");
    expect(fetcher).toHaveBeenCalledTimes(1);
  });

  it("invalidate clears cache", async () => {
    const fetcher = vi
      .fn()
      .mockResolvedValueOnce({ accessToken: "tok1", expiresIn: 7200 })
      .mockResolvedValueOnce({ accessToken: "tok2", expiresIn: 7200 });
    const mgr = new AccessTokenManager({ fetcher, now: () => 1_000_000 });
    const handle = mgr.handle(mockAccount());
    await handle.getAccessToken();
    handle.invalidate();
    expect(await handle.getAccessToken()).toBe("tok2");
  });
});
