import type { OpenClawConfig } from "openclaw/plugin-sdk";

import type { WecomRuntimeEnv } from "../../types/runtime-context.js";
import type { WecomAccountRuntime } from "../../app/account-runtime.js";
import { startAgentCallbackTransport } from "../../transport/agent-callback/http-handler.js";

export class WecomAgentIngressService {
  private stopTransport?: () => void;

  constructor(
    private readonly runtime: WecomAccountRuntime,
    private readonly cfg: OpenClawConfig,
    private readonly runtimeEnv: WecomRuntimeEnv,
  ) {}

  start(): { transport: "agent-callback"; descriptors: string[] } | undefined {
    const agent = this.runtime.account.agent;
    if (!agent?.callbackConfigured) {
      return undefined;
    }
    const callback = startAgentCallbackTransport({
      account: agent,
      cfg: this.cfg,
      runtime: this.runtime,
      runtimeEnv: this.runtimeEnv,
    });
    this.stopTransport = callback.stop;
    return {
      transport: "agent-callback",
      descriptors: callback.paths,
    };
  }

  stop(): void {
    this.stopTransport?.();
    this.stopTransport = undefined;
  }
}
