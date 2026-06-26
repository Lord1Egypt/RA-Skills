import type { OpenClawConfig } from "openclaw/plugin-sdk";

import type { WecomRuntimeEnv } from "../../types/runtime-context.js";
import type { ResolvedAgentAccount } from "../../types/index.js";
import type { WecomAccountRuntime } from "../../app/account-runtime.js";
import { resolveAgentCallbackPaths } from "./inbound.js";
import { createAgentCallbackSessionSnapshot } from "./session.js";
import { registerAgentWebhookTarget } from "../http/registry.js";

export function startAgentCallbackTransport(params: {
  account: ResolvedAgentAccount;
  cfg: OpenClawConfig;
  runtime: WecomAccountRuntime;
  runtimeEnv: WecomRuntimeEnv;
}): { paths: string[]; stop: () => void } {
  const paths = resolveAgentCallbackPaths(params.account.accountId);
  params.runtime.updateTransportSession(
    createAgentCallbackSessionSnapshot({
      accountId: params.account.accountId,
      running: true,
    }),
  );
  const unregisters = paths.map((path) =>
    registerAgentWebhookTarget({
      agent: params.account,
      config: params.cfg,
      runtimeEnv: params.runtimeEnv,
      touchTransportSession: (patch) => params.runtime.touchTransportSession("agent-callback", patch),
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
        createAgentCallbackSessionSnapshot({
          accountId: params.account.accountId,
          running: false,
        }),
      );
    },
  };
}
