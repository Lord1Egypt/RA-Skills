export type SpawnMode = "run" | "session";

export type SessionStatus = "running" | "done" | "failed" | "unknown";

export interface SpawnOptions {
  taskId: string;
  agentId: string;
  promptFile: string;
  cwd: string;
  mode: SpawnMode;
  label: string;
}

export interface SessionRecord {
  taskId: string;
  sessionKey: string;
  agentId: string;
  startedAt: string;
  status: SessionStatus;
}
