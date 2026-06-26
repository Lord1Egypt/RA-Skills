import type { OpenClawConfig } from "openclaw/plugin-sdk";

import type { WecomRuntimeEnv } from "../../types/runtime-context.js";
import type { ResolvedBotAccount } from "../../types/index.js";
import type { WecomAccountRuntime } from "../../app/account-runtime.js";
import { resolveBotWebhookPaths } from "./inbound.js";
import { createBotWebhookSessionSnapshot } from "./session.js";
import { registerWecomWebhookTarget } from "../http/registry.js";

export function startBotWebhookTransport(params: {
  account: ResolvedBotAccount;
  cfg: OpenClawConfig;
  runtime: WecomAccountRuntime;
  runtimeEnv: WecomRuntimeEnv;
}): { paths: string[]; stop: () => void } {
  const paths = resolveBotWebhookPaths(params.account.accountId);
  params.runtime.updateTransportSession(
    createBotWebhookSessionSnapshot({
      accountId: params.account.accountId,
      running: true,
    }),
  );
  const unregisters = paths.map((path) =>
    registerWecomWebhookTarget({
      account: params.account,
      config: params.cfg,
      runtime: params.runtimeEnv,
      core: params.runtime.core,
      path,
      touchTransportSession: (patch) => params.runtime.touchTransportSession("bot-webhook", patch),
      auditSink: (event) => params.runtime.recordOperationalIssue(event),
    }),
  );
  return {
    paths,
    stop: () => {
      for (const unregister of unregisters) {
        unregister();
      }
      params.runtime.updateTransportSession(
        createBotWebhookSessionSnapshot({
          accountId: params.account.accountId,
          running: false,
        }),
      );
    },
  };
}
