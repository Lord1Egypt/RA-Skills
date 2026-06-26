import type { ChannelGatewayContext } from "openclaw/plugin-sdk";

import { resolveWecomRuntimeAccount } from "../config/runtime-config.js";
import type { ResolvedWecomAccount } from "../types/index.js";
import { WecomAccountRuntime } from "./account-runtime.js";
import { getWecomRuntime } from "./index.js";

export function createAccountRuntime(ctx: ChannelGatewayContext<ResolvedWecomAccount>): WecomAccountRuntime {
  const resolved = resolveWecomRuntimeAccount({
    cfg: ctx.cfg,
    accountId: ctx.accountId,
  });
  return new WecomAccountRuntime(
    getWecomRuntime(),
    ctx.cfg,
    resolved,
    {
      info: (message) => ctx.log?.info(message),
      warn: (message) => ctx.log?.warn(message),
      error: (message) => ctx.log?.error(message),
    },
    (snapshot) => {
      ctx.setStatus({
        accountId: ctx.accountId,
        ...snapshot,
      });
    },
  );
}
