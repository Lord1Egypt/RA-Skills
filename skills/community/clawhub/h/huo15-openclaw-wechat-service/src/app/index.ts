/**
 * Plugin runtime registry —— 多账号 WechatServiceAccountRuntime 注册表 + plugin-level runtime ref。
 *
 * v2.0.0 起 AccountRuntime 改为 class（参 `./account-runtime.ts`），但本文件
 * 保留全部 v0.1.0 的导出 API（`registerAccountRuntime` / `getAccountRuntime` /
 * `updateAccountRuntime` / ...），调用方代码无需改动。
 */

import type { PluginRuntime } from "openclaw/plugin-sdk";

import {
  WechatServiceAccountRuntime,
  type AccountRuntime,
  type AccountRuntimeLogger,
  type AccountRuntimeStatusSnapshot,
} from "./account-runtime.js";

export type { AccountRuntime, AccountRuntimeLogger, AccountRuntimeStatusSnapshot };
export { WechatServiceAccountRuntime };

let runtimeRef: PluginRuntime | undefined;
const accountRuntimes = new Map<string, WechatServiceAccountRuntime>();

export function setWechatServiceRuntime(runtime: PluginRuntime): void {
  runtimeRef = runtime;
}

export function getWechatServiceRuntime(): PluginRuntime {
  if (!runtimeRef) {
    throw new Error(
      "[wechat-service] plugin runtime has not been initialized. Call setWechatServiceRuntime(api.runtime) from the plugin register() first.",
    );
  }
  return runtimeRef;
}

export function tryGetWechatServiceRuntime(): PluginRuntime | undefined {
  return runtimeRef;
}

/**
 * 注册一个账号 runtime。接受 class 实例或 plain-object（后者会被自动包成 class）。
 */
export function registerAccountRuntime(
  accountId: string,
  runtime: WechatServiceAccountRuntime | AccountRuntimeInitArgs,
): WechatServiceAccountRuntime {
  const wrapped =
    runtime instanceof WechatServiceAccountRuntime
      ? runtime
      : promotePlainObjectToClass(accountId, runtime);
  accountRuntimes.set(accountId, wrapped);
  return wrapped;
}

export function getAccountRuntime(accountId: string): WechatServiceAccountRuntime | undefined {
  return accountRuntimes.get(accountId);
}

export function unregisterAccountRuntime(accountId: string): void {
  accountRuntimes.delete(accountId);
}

export function listAccountRuntimeIds(): string[] {
  return Array.from(accountRuntimes.keys());
}

/**
 * **updateAccountRuntime** —— 增量更新账号状态。保留作 backward-compat 入口，
 * 推荐新代码直接用 `runtime.markInbound()` / `markOutbound()` / `markError()` 等方法。
 */
export function updateAccountRuntime(
  accountId: string,
  patch: Partial<AccountRuntimeInitArgs>,
): void {
  const current = accountRuntimes.get(accountId);
  if (!current) {
    // 兜底：没注册过就先注册一个最小版
    const fresh = promotePlainObjectToClass(accountId, patch);
    accountRuntimes.set(accountId, fresh);
    return;
  }
  if (patch.log) current.log.info = patch.log.info ?? current.log.info;
  if (patch.running != null) current.running = Boolean(patch.running);
  if (patch.lastStartAt != null) current.lastStartAt = patch.lastStartAt ?? null;
  if (patch.lastStopAt != null) current.lastStopAt = patch.lastStopAt ?? null;
  if (patch.lastInboundAt != null) current.lastInboundAt = patch.lastInboundAt ?? null;
  if (patch.lastOutboundAt != null) current.lastOutboundAt = patch.lastOutboundAt ?? null;
  if (patch.lastError !== undefined) current.lastError = patch.lastError ?? null;
}

// ---- internal helpers ----

type AccountRuntimeInitArgs = {
  accountId?: string;
  log?: AccountRuntimeLogger;
  running?: boolean;
  lastStartAt?: number | null;
  lastStopAt?: number | null;
  lastInboundAt?: number | null;
  lastOutboundAt?: number | null;
  lastError?: string | null;
};

function promotePlainObjectToClass(
  accountId: string,
  init: AccountRuntimeInitArgs,
): WechatServiceAccountRuntime {
  const r = new WechatServiceAccountRuntime({
    accountId: init.accountId ?? accountId,
    log: init.log,
  });
  r.running = Boolean(init.running);
  r.lastStartAt = init.lastStartAt ?? null;
  r.lastStopAt = init.lastStopAt ?? null;
  r.lastInboundAt = init.lastInboundAt ?? null;
  r.lastOutboundAt = init.lastOutboundAt ?? null;
  r.lastError = init.lastError ?? null;
  return r;
}
