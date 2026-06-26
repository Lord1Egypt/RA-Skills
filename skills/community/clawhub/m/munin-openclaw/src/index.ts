import { MuninClient } from "@kalera/munin-sdk";

export function createOpenClawMuninAdapter(config: {
  baseUrl: string;
  apiKey?: string;
  
  timeoutMs?: number;
}) {
  const client = new MuninClient(config);

  return {
    execute: (projectId: string, action: string, payload: Record<string, unknown>) =>
      client.invoke(projectId, action as any, payload, { ensureCapability: true }),
    capabilities: () => client.capabilities(),
  };
}
