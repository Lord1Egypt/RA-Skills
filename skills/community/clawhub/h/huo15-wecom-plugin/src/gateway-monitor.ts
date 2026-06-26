import type {
  ChannelGatewayContext,
  OpenClawConfig,
} from "openclaw/plugin-sdk";

import {
  listWecomAccountIds,
  resolveDerivedPathSummary,
  resolveWecomAccount,
  resolveWecomAccountConflict,
} from "./config/index.js";
import { createAccountRuntime } from "./app/bootstrap.js";
import { registerAccountRuntime, unregisterAccountRuntime } from "./app/index.js";
import type { ResolvedWecomAccount, WecomConfig } from "./types/index.js";
import { WecomBotCapabilityService } from "./capability/bot/index.js";
import { WecomAgentIngressService } from "./capability/agent/index.js";
import { WecomKefuCapabilityService } from "./capability/kefu/index.js";
import type { WecomRuntimeEnv } from "./types/runtime-context.js";

type AccountRouteRegistryItem = {
  botPaths: string[];
  agentPaths: string[];
  kefuPaths: string[];
};

const accountRouteRegistry = new Map<string, AccountRouteRegistryItem>();

function logRegisteredRouteSummary(
  ctx: ChannelGatewayContext<ResolvedWecomAccount>,
  preferredOrder: string[],
): void {
  const seen = new Set<string>();
  const orderedAccountIds = [
    ...preferredOrder.filter((accountId) => accountRouteRegistry.has(accountId)),
    ...Array.from(accountRouteRegistry.keys())
      .filter((accountId) => !seen.has(accountId))
      .sort((a, b) => a.localeCompare(b)),
  ].filter((accountId) => {
    if (seen.has(accountId)) return false;
    seen.add(accountId);
    return true;
  });

  const entries = orderedAccountIds
    .map((accountId) => {
      const routes = accountRouteRegistry.get(accountId);
      if (!routes) return undefined;
      const botText = routes.botPaths.length > 0 ? routes.botPaths.join(", ") : "未启用";
      const agentText = routes.agentPaths.length > 0 ? routes.agentPaths.join(", ") : "未启用";
      const kefuText = routes.kefuPaths.length > 0 ? routes.kefuPaths.join(", ") : "未启用";
      return `accountId=${accountId}（Bot: ${botText}；Agent: ${agentText}；Kefu: ${kefuText}）`;
    })
    .filter((entry): entry is string => Boolean(entry));
  const summary = entries.length > 0 ? entries.join("； ") : "无";
  ctx.log?.info(`[${ctx.account.accountId}] 已注册账号路由汇总：${summary}`);
}

function resolveExpectedRouteSummaryAccountIds(cfg: OpenClawConfig): string[] {
  return listWecomAccountIds(cfg)
    .filter((accountId) => {
      const conflict = resolveWecomAccountConflict({ cfg, accountId });
      if (conflict) return false;
      const account = resolveWecomAccount({ cfg, accountId });
      if (!account.enabled || !account.configured) return false;
      return Boolean(account.bot?.configured || account.agent?.configured || account.kefu?.configured);
    })
    .sort((a, b) => a.localeCompare(b));
}

function waitForAbortSignal(abortSignal: AbortSignal): Promise<void> {
  if (abortSignal.aborted) {
    return Promise.resolve();
  }
  return new Promise<void>((resolve) => {
    const onAbort = () => {
      abortSignal.removeEventListener("abort", onAbort);
      resolve();
    };
    abortSignal.addEventListener("abort", onAbort, { once: true });
  });
}

/**
 * Keeps WeCom webhook targets registered for the account lifecycle.
 * The promise only settles after gateway abort/reload signals shutdown.
 */
export async function monitorWecomProvider(
  ctx: ChannelGatewayContext<ResolvedWecomAccount>,
): Promise<void> {
  const account = ctx.account;
  const cfg = ctx.cfg as OpenClawConfig;
  const expectedRouteSummaryAccountIds = resolveExpectedRouteSummaryAccountIds(cfg);
  const conflict = resolveWecomAccountConflict({
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
  const bot = account.bot;
  const agent = account.agent;
  const kefu = account.kefu;
  const botConfigured = Boolean(bot?.configured);
  const agentConfigured = Boolean(agent?.configured);
  const kefuConfigured = Boolean(kefu?.configured);

  if (!botConfigured && !agentConfigured && !kefuConfigured) {
    ctx.log?.warn(`[${account.accountId}] wecom not configured; channel is idle`);
    ctx.setStatus({ accountId: account.accountId, running: false, configured: false });
    await waitForAbortSignal(ctx.abortSignal);
    return;
  }

  const accountRuntime = createAccountRuntime(ctx);
  registerAccountRuntime(accountRuntime);
  const botPaths: string[] = [];
  const agentPaths: string[] = [];
  const kefuPaths: string[] = [];
  const runtimeEnv: WecomRuntimeEnv = {
    log: (message) => ctx.log?.info(message),
    error: (message) => ctx.log?.error(message),
  };
  const botService = new WecomBotCapabilityService(
    accountRuntime,
    cfg,
    runtimeEnv,
  );
  const agentIngress = new WecomAgentIngressService(accountRuntime, cfg, runtimeEnv);
  const kefuService = new WecomKefuCapabilityService(accountRuntime, cfg, runtimeEnv);
  try {
    ctx.log?.info(
      `[${account.accountId}] wecom runtime start bot=${bot?.primaryTransport ?? "disabled"} agent=${agentConfigured ? "callback/api" : "disabled"} kefu=${kefuConfigured ? "callback" : "disabled"}`,
    );
    const botRegistration = botService.start();
    if (botRegistration) {
      botPaths.push(...botRegistration.descriptors);
      ctx.log?.info(
        `[${account.accountId}] wecom bot ${botRegistration.transport} started: ${botRegistration.descriptors.join(", ")}`,
      );
    }

    const agentRegistration = agentIngress.start();
    if (agentRegistration) {
      agentPaths.push(...agentRegistration.descriptors);
      ctx.log?.info(
        `[${account.accountId}] wecom agent ${agentRegistration.transport} started: ${agentRegistration.descriptors.join(", ")}`,
      );
    }

    const kefuRegistration = kefuService.start();
    if (kefuRegistration) {
      kefuPaths.push(...kefuRegistration.descriptors);
      ctx.log?.info(
        `[${account.accountId}] wecom kefu ${kefuRegistration.transport} started: ${kefuRegistration.descriptors.join(", ")}`,
      );
    }

    accountRouteRegistry.set(account.accountId, { botPaths, agentPaths, kefuPaths });
    const shouldLogSummary =
      expectedRouteSummaryAccountIds.length <= 1 ||
      expectedRouteSummaryAccountIds.every((accountId) => accountRouteRegistry.has(accountId));
    if (shouldLogSummary) {
      logRegisteredRouteSummary(ctx, expectedRouteSummaryAccountIds);
    }

    ctx.setStatus({
      running: true,
      configured: true,
      webhookPath: botPaths[0] ?? agentPaths[0] ?? kefuPaths[0] ?? null,
      lastStartAt: Date.now(),
      ...accountRuntime.buildRuntimeStatus(),
    });
    ctx.log?.info(
      `[${account.accountId}] runtime status health=${accountRuntime.buildRuntimeStatus().health} transports=${(accountRuntime.buildRuntimeStatus().transportSessions ?? []).join(" | ") || "none"}`,
    );

    await waitForAbortSignal(ctx.abortSignal);
  } finally {
    botService.stop();
    agentIngress.stop();
    kefuService.stop();
    accountRouteRegistry.delete(account.accountId);
    unregisterAccountRuntime(account.accountId);
    ctx.setStatus({
      running: false,
      lastStopAt: Date.now(),
      ...accountRuntime.buildRuntimeStatus(),
    });
    ctx.log?.info(`[${account.accountId}] wecom runtime stopped`);
  }
}
