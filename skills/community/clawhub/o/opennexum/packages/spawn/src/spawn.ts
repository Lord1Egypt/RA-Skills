import type { SessionRecord, SpawnOptions } from "./types.js";

type AgentCliName = "claude" | "codex";

/**
 * Resolve CLI name from agentId prefix.
 * codex-* -> codex, claude-* -> claude, default -> codex
 */
export function resolveCliName(agentId: string, explicitCli?: string): AgentCliName {
  if (explicitCli === "claude" || explicitCli === "codex") {
    return explicitCli;
  }
  if (agentId.startsWith("claude-")) {
    return "claude";
  }
  return "codex";
}

/**
 * OpenClaw webhook dispatch happens in the CLI callback flow.
 * Keep this stub to preserve the package API for existing imports.
 */
export async function spawnAcpSession(options: SpawnOptions): Promise<SessionRecord> {
  const startedAt = new Date().toISOString();

  return {
    taskId: options.taskId,
    sessionKey: options.agentId,
    agentId: options.agentId,
    startedAt,
    status: "running",
  };
}
