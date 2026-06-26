import type { OpenClawConfig } from "openclaw/plugin-sdk";

import type { WecomRuntimeEnv } from "../../types/runtime-context.js";
import type { ResolvedKefuAccount } from "../../types/index.js";
import type { WecomAccountRuntime } from "../../app/account-runtime.js";
import { resolveKefuPaths } from "./inbound.js";
import { createKefuSessionSnapshot } from "./session.js";
import { registerKefuWebhookTarget } from "../http/registry.js";

export function startKefuTransport(params: {
  account: ResolvedKefuAccount;
  cfg: OpenClawConfig;
  runtime: WecomAccountRuntime;
  runtimeEnv: WecomRuntimeEnv;
}): { paths: string[]; stop: () => void } {
  const paths = resolveKefuPaths(params.account.accountId);
  params.runtime.updateTransportSession(
    createKefuSessionSnapshot({
      accountId: params.account.accountId,
      running: true,
    }),
  );
  const unregisters = paths.map((path) =>
    registerKefuWebhookTarget({
      kefu: params.account,
      config: params.cfg,
      runtimeEnv: params.runtimeEnv,
      runtime: params.runtime,
      core: params.runtime.core,
      touchTransportSession: (patch) => params.runtime.touchTransportSession("kefu", patch),
      auditSink: (event) => params.runtime.recordOperationalIssue(event),
      path,
    }),
  );
  return {
    paths,
    stop: () => {
      for (const unregister of unregisters) {
        unregister();
      }
      params.runtime.updateTransportSession(
        createKefuSessionSnapshot({
          accountId: params.account.accountId,
          running: false,
        }),
      );
    },
  };
}
