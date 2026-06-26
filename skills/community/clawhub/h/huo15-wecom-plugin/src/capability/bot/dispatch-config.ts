import type { OpenClawConfig } from "openclaw/plugin-sdk";

export function buildWecomBotDispatchConfig(config: OpenClawConfig): OpenClawConfig {
  const baseAgents = (config as any)?.agents ?? {};
  const baseAgentDefaults = (baseAgents as any)?.defaults ?? {};
  const baseBlockChunk = (baseAgentDefaults as any)?.blockStreamingChunk ?? {};
  const baseBlockCoalesce = (baseAgentDefaults as any)?.blockStreamingCoalesce ?? {};
  const baseTools = (config as any)?.tools ?? {};
  const baseSandbox = (baseTools as any)?.sandbox ?? {};
  const baseSandboxTools = (baseSandbox as any)?.tools ?? {};
  const existingTopLevelDeny = Array.isArray((baseTools as any).deny) ? ((baseTools as any).deny as string[]) : [];
  const existingSandboxDeny = Array.isArray((baseSandboxTools as any).deny) ? ((baseSandboxTools as any).deny as string[]) : [];
  const topLevelDeny = Array.from(new Set([...existingTopLevelDeny, "message"]));
  const sandboxDeny = Array.from(new Set([...existingSandboxDeny, "message"]));
  return {
    ...(config as any),
    agents: {
      ...baseAgents,
      defaults: {
        ...baseAgentDefaults,
        blockStreamingChunk: {
          ...baseBlockChunk,
          minChars: baseBlockChunk.minChars ?? 120,
          maxChars: baseBlockChunk.maxChars ?? 360,
          breakPreference: baseBlockChunk.breakPreference ?? "sentence",
        },
        blockStreamingCoalesce: {
          ...baseBlockCoalesce,
          minChars: baseBlockCoalesce.minChars ?? 120,
          maxChars: baseBlockCoalesce.maxChars ?? 360,
          idleMs: baseBlockCoalesce.idleMs ?? 250,
        },
      },
    },
    tools: {
      ...baseTools,
      deny: topLevelDeny,
      sandbox: {
        ...baseSandbox,
        tools: {
          ...baseSandboxTools,
          deny: sandboxDeny,
        },
      },
    },
  } as OpenClawConfig;
}
