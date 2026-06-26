/**
 * WechatServiceAccountRuntime 状态机回归测试。
 *
 * 关键不变量：
 *  1. lifecycle 方法（markStart/markStop/markInbound/markOutbound/markError）
 *     更新对应字段；不改其他字段
 *  2. getStatusSnapshot() 返回纯快照（不暴露 log / 不依赖 class 引用）
 *  3. 旧 plain-object AccountRuntime 字段访问仍可用（backward-compat）
 *  4. registerAccountRuntime/getAccountRuntime/updateAccountRuntime 整套接口完整保留
 */
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  WechatServiceAccountRuntime,
  type AccountRuntimeStatusSnapshot,
} from "./account-runtime.js";
import {
  getAccountRuntime,
  listAccountRuntimeIds,
  registerAccountRuntime,
  unregisterAccountRuntime,
  updateAccountRuntime,
} from "./index.js";

describe("WechatServiceAccountRuntime class", () => {
  it("starts with empty status", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    expect(r.accountId).toBe("main");
    expect(r.running).toBe(false);
    expect(r.lastStartAt).toBe(null);
    expect(r.lastStopAt).toBe(null);
    expect(r.lastInboundAt).toBe(null);
    expect(r.lastOutboundAt).toBe(null);
    expect(r.lastError).toBe(null);
  });

  it("markStart sets running=true + lastStartAt + clears lastError", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    r.lastError = "stale error";
    r.markStart(1000);
    expect(r.running).toBe(true);
    expect(r.lastStartAt).toBe(1000);
    expect(r.lastStopAt).toBe(null);
    expect(r.lastError).toBe(null);
  });

  it("markStop sets running=false + lastStopAt", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    r.markStart(1000);
    r.markStop(2000);
    expect(r.running).toBe(false);
    expect(r.lastStopAt).toBe(2000);
    // lastStartAt 不被覆盖
    expect(r.lastStartAt).toBe(1000);
  });

  it("markInbound / markOutbound only touch corresponding field", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    r.markInbound(100);
    expect(r.lastInboundAt).toBe(100);
    expect(r.lastOutboundAt).toBe(null);
    r.markOutbound(200);
    expect(r.lastInboundAt).toBe(100);
    expect(r.lastOutboundAt).toBe(200);
  });

  it("markError stores message string (not raw error object)", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    r.markError(new Error("connection refused"));
    expect(r.lastError).toBe("connection refused");
    r.markError("plain string err");
    expect(r.lastError).toBe("plain string err");
    r.markError({ weird: true });
    // 非 Error 对象走 String() 转换
    expect(typeof r.lastError).toBe("string");
  });

  it("clearError resets lastError to null without touching others", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    r.markStart(100);
    r.markInbound(150);
    r.markError("boom");
    r.clearError();
    expect(r.lastError).toBe(null);
    expect(r.running).toBe(true);
    expect(r.lastInboundAt).toBe(150);
  });

  it("getStatusSnapshot returns pure data (no method refs)", () => {
    const r = new WechatServiceAccountRuntime({
      accountId: "main",
      log: { info: vi.fn() },
    });
    r.markStart(1000);
    r.markInbound(1500);
    r.markOutbound(1800);
    const snap: AccountRuntimeStatusSnapshot = r.getStatusSnapshot();
    expect(snap).toEqual({
      accountId: "main",
      running: true,
      lastStartAt: 1000,
      lastStopAt: null,
      lastInboundAt: 1500,
      lastOutboundAt: 1800,
      lastError: null,
    });
    // snapshot 不应该暴露 log
    expect((snap as unknown as { log?: unknown }).log).toBeUndefined();
  });

  it("backward-compat: plain-object field access (runtime.lastInboundAt) still works", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    r.lastInboundAt = 999;
    expect(r.lastInboundAt).toBe(999);
    expect(r.getStatusSnapshot().lastInboundAt).toBe(999);
  });
});

describe("app/index.ts registry", () => {
  beforeEach(() => {
    // 清理之前测试可能留下的 runtime
    for (const id of listAccountRuntimeIds()) {
      unregisterAccountRuntime(id);
    }
  });

  afterEach(() => {
    for (const id of listAccountRuntimeIds()) {
      unregisterAccountRuntime(id);
    }
  });

  it("registerAccountRuntime accepts class instance directly", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    const stored = registerAccountRuntime("main", r);
    expect(stored).toBe(r);
    expect(getAccountRuntime("main")).toBe(r);
  });

  it("registerAccountRuntime promotes plain-object init to class instance (backward-compat)", () => {
    const stored = registerAccountRuntime("acc1", {
      accountId: "acc1",
      running: true,
      lastStartAt: 5000,
      log: { info: vi.fn() },
    });
    expect(stored).toBeInstanceOf(WechatServiceAccountRuntime);
    expect(stored.running).toBe(true);
    expect(stored.lastStartAt).toBe(5000);
  });

  it("updateAccountRuntime patches existing runtime in place", () => {
    const r = new WechatServiceAccountRuntime({ accountId: "main" });
    registerAccountRuntime("main", r);
    updateAccountRuntime("main", { lastInboundAt: 7000, lastOutboundAt: 8000 });
    expect(r.lastInboundAt).toBe(7000);
    expect(r.lastOutboundAt).toBe(8000);
  });

  it("updateAccountRuntime auto-creates runtime if not registered (defensive)", () => {
    updateAccountRuntime("ghost", { lastInboundAt: 100 });
    const r = getAccountRuntime("ghost");
    expect(r).toBeDefined();
    expect(r?.lastInboundAt).toBe(100);
  });

  it("listAccountRuntimeIds reflects registered runtimes", () => {
    registerAccountRuntime("a", { accountId: "a" });
    registerAccountRuntime("b", { accountId: "b" });
    expect(listAccountRuntimeIds().sort()).toEqual(["a", "b"]);
    unregisterAccountRuntime("a");
    expect(listAccountRuntimeIds()).toEqual(["b"]);
  });
});
