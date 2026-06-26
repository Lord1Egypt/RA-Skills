/**
 * 微信服务号 gateway lifecycle (startAccount)
 *
 * 每个 account 启动时：
 *  1. 把 webhook target 注册到内存里 (registry.ts)
 *  2. 同时把 runtime 记录到 account runtime map，供 outbound / 日志使用
 *  3. 阻塞在 abortSignal 上，直到 reload/stop 解除
 */

import type { ChannelGatewayContext, OpenClawConfig } from "openclaw/plugin-sdk";

import {
  listWechatServiceAccountIds,
  resolveWechatServiceAccount,
  resolveWechatServiceAccountConflict,
  resolveDerivedPathSummary,
} from "./config/index.js";
import {
  registerAccountRuntime,
  unregisterAccountRuntime,
  tryGetWechatServiceRuntime,
  updateAccountRuntime,
  WechatServiceAccountRuntime,
} from "./app/index.js";
import { registerWebhookTarget } from "./transport/webhook/registry.js";
import type { ResolvedWechatServiceAccount } from "./types.js";

function waitForAbort(abortSignal: AbortSignal): Promise<void> {
  if (abortSignal.aborted) return Promise.resolve();
  return new Promise((resolve) => {
    const onAbort = () => {
      abortSignal.removeEventListener("abort", onAbort);
      resolve();
    };
    abortSignal.addEventListener("abort", onAbort, { once: true });
  });
}

function buildAccountRuntime(
  ctx: ChannelGatewayContext<ResolvedWechatServiceAccount>,
): WechatServiceAccountRuntime {
  const runtime = WechatServiceAccountRuntime.fromGatewayContext(ctx);
  runtime.markStart();
  return runtime;
}

export async function monitorWechatServiceProvider(
  ctx: ChannelGatewayContext<ResolvedWechatServiceAccount>,
): Promise<void> {
  const account = ctx.account;
  const cfg = ctx.cfg as OpenClawConfig;
  const conflict = resolveWechatServiceAccountConflict({
    cfg,
    accountId: account.accountId,
  });
  if (conflict) {
    ctx.setStatus({
      accountId: account.accountId,
      running: false,
      configured: false,
      lastError: conflict.message,
    });
    throw new Error(conflict.message);
  }
  if (!account.configured) {
    ctx.log?.warn(
      `[${account.accountId}] wechat-service not fully configured; channel is idle (appId=${account.appId || "∅"} token=${account.token ? "set" : "∅"} encodingAESKey=${account.encodingAESKey ? "set" : "∅"})`,
    );
    ctx.setStatus({ accountId: account.accountId, running: false, configured: false });
    await waitForAbort(ctx.abortSignal);
    return;
  }

  const runtime = buildAccountRuntime(ctx);
  registerAccountRuntime(account.accountId, runtime);

  const paths = resolveDerivedPathSummary(account.accountId);
  const unregisters: Array<() => void> = [];
  for (const path of paths.inbound) {
    const off = registerWebhookTarget({
      account,
      path,
      encryptMode: account.encryptMode,
      runtime: {
        log: (msg) => ctx.log?.info(msg),
        error: (msg) => ctx.log?.error(msg),
      },
      core: tryGetWechatServiceRuntime(),
      touchTransportSession: (patch) => {
        if (patch.lastInboundAt != null) {
          updateAccountRuntime(account.accountId, {
            lastInboundAt: patch.lastInboundAt,
          });
        }
        if (patch.running != null) {
          updateAccountRuntime(account.accountId, { running: patch.running });
        }
      },
    });
    unregisters.push(off);
  }

  ctx.log?.info(
    `[${account.accountId}] wechat-service webhook registered: ${paths.inbound.join(", ")} (encryptMode=${account.encryptMode})`,
  );

  try {
    ctx.setStatus({
      accountId: account.accountId,
      running: true,
      configured: true,
      webhookPath: paths.primary,
      lastStartAt: Date.now(),
    });
    await waitForAbort(ctx.abortSignal);
  } finally {
    for (const off of unregisters) {
      try {
        off();
      } catch {
        /* ignore */
      }
    }
    unregisterAccountRuntime(account.accountId);
    ctx.setStatus({
      accountId: account.accountId,
      running: false,
      lastStopAt: Date.now(),
    });
    ctx.log?.info(`[${account.accountId}] wechat-service runtime stopped`);
  }
}

export function listExpectedAccountIds(cfg: OpenClawConfig): string[] {
  return listWechatServiceAccountIds(cfg).filter((id) => {
    const account = resolveWechatServiceAccount({ cfg, accountId: id });
    return account.enabled && account.configured;
  });
}
