import fs from "node:fs/promises";
import path from "node:path";

type PluginLogger = {
  warn: (message: string) => void;
  error: (message: string) => void;
};

export type AuditFinding = {
  category: string;
  severity: "low" | "medium" | "high" | "critical";
  message: string;
};

export type AuditEvent = {
  type: string;
  severity: "low" | "medium" | "high" | "critical";
  sessionKey?: string;
  agentId?: string;
  runId?: string;
  toolName?: string;
  blocked?: boolean;
  preview?: string;
  findings: AuditFinding[];
};

export function createAuditLogger(logPath: string, logger: PluginLogger) {
  return {
    async write(event: AuditEvent) {
      try {
        await fs.mkdir(path.dirname(logPath), { recursive: true });
        await fs.appendFile(
          logPath,
          `${JSON.stringify({ ts: new Date().toISOString(), ...event })}\n`,
          "utf8",
        );
      } catch (error) {
        logger.warn(`[ironclaw-security-guard] failed to write audit log: ${String(error)}`);
      }
    },
  };
}
