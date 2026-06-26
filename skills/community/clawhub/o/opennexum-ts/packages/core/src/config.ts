import { readFile } from "node:fs/promises";
import path from "node:path";

export type AgentCli = "codex" | "claude";

export interface AgentConfig {
  cli: AgentCli;
  model?: string;
}

export interface NotifyConfig {
  target?: string;
  botToken?: string;
}

export interface NexumConfig {
  notify?: NotifyConfig;
  agents?: Record<string, AgentConfig>;
}

export async function loadConfig(projectDir: string): Promise<NexumConfig> {
  const configPath = path.join(projectDir, "nexum", "config.json");

  try {
    const contents = await readFile(configPath, "utf8");
    return JSON.parse(contents) as NexumConfig;
  } catch (error) {
    if (isNodeError(error) && error.code === "ENOENT") {
      return {};
    }
    throw error;
  }
}

export function resolveAgentCli(config: NexumConfig, agentId: string): AgentCli {
  return config.agents?.[agentId]?.cli ?? "codex";
}

function isNodeError(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error;
}
