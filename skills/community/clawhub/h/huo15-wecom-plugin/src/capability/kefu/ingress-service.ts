import type { OpenClawConfig } from "openclaw/plugin-sdk";

import type { WecomRuntimeEnv } from "../../types/runtime-context.js";
import type { WecomAccountRuntime } from "../../app/account-runtime.js";
import { startKefuTransport } from "../../transport/kefu/http-handler.js";

export class WecomKefuCapabilityService {
  private stopTransport?: () => void;

  constructor(
    private readonly runtime: WecomAccountRuntime,
    private readonly cfg: OpenClawConfig,
    private readonly runtimeEnv: WecomRuntimeEnv,
  ) {}

  start(): { transport: "kefu"; descriptors: string[] } | undefined {
    const kefu = this.runtime.account.kefu;
    if (!kefu?.configured) {
      return undefined;
    }
    const callback = startKefuTransport({
      account: kefu,
      cfg: this.cfg,
      runtime: this.runtime,
      runtimeEnv: this.runtimeEnv,
    });
    this.stopTransport = callback.stop;
    return {
      transport: "kefu",
      descriptors: callback.paths,
    };
  }

  stop(): void {
    this.stopTransport?.();
    this.stopTransport = undefined;
  }
}
