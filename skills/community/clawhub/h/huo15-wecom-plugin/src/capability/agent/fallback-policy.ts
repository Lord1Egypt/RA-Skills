import type { ResolvedAgentAccount } from "../../types/index.js";

export function canUseAgentApiDelivery(agent: ResolvedAgentAccount | undefined): boolean {
  return Boolean(agent?.apiConfigured && typeof agent.agentId === "number");
}

export function shouldFallbackToAgentApi(params: {
  agent: ResolvedAgentAccount | undefined;
  hasText?: boolean;
  hasMedia?: boolean;
}): boolean {
  return canUseAgentApiDelivery(params.agent) && Boolean(params.hasText || params.hasMedia);
}
