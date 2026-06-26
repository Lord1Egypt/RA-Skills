import type { SessionStatus } from "./types.js";

const DEFAULT_TIMEOUT_MS = 5 * 60 * 1000;
const DEFAULT_INTERVAL_MS = 1_000;
type ExecaResult = {
  stdout: string;
  stderr: string;
  exitCode: number;
};
type ExecaRunner = (
  command: string,
  args: string[],
  options: { reject: false }
) => Promise<ExecaResult>;
const testingGlobals = globalThis as typeof globalThis & {
  __nexumStatusExeca?: ExecaRunner;
};
let cachedExecaRunner: ExecaRunner | undefined;
const loadExecaModule = new Function("return import('execa')") as () => Promise<{ execa: ExecaRunner }>;

export class TimeoutError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "TimeoutError";
  }
}

export async function getSessionStatus(sessionKey: string): Promise<SessionStatus> {
  const result = await (await getExecaRunner())("openclaw", ["sessions", "list", "--json"], {
    reject: false
  });

  if (result.exitCode !== 0) {
    throw new Error(result.stderr || result.stdout || "Failed to list OpenClaw sessions.");
  }

  const payload = JSON.parse(result.stdout) as
    | { sessions?: unknown[] }
    | unknown[];
  const sessions = Array.isArray(payload) ? payload : payload.sessions ?? [];
  const match = sessions.find((entry) => hasSessionKey(entry, sessionKey));

  if (!match) {
    return "unknown";
  }

  return normalizeSessionStatus(match);
}

export async function pollUntilDone(
  sessionKey: string,
  opts: { timeoutMs?: number; intervalMs?: number } = {}
): Promise<void> {
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const intervalMs = opts.intervalMs ?? DEFAULT_INTERVAL_MS;
  const deadline = Date.now() + timeoutMs;

  while (true) {
    const status = await getSessionStatus(sessionKey);

    if (status === "done") {
      return;
    }

    if (status === "failed") {
      throw new Error(`ACP session failed: ${sessionKey}`);
    }

    if (Date.now() >= deadline) {
      throw new TimeoutError(`Timed out waiting for ACP session: ${sessionKey}`);
    }

    await sleep(intervalMs);
  }
}

function hasSessionKey(entry: unknown, sessionKey: string): boolean {
  if (!entry || typeof entry !== "object") {
    return false;
  }

  const record = entry as Record<string, unknown>;

  return ["key", "sessionKey", "childSessionKey"].some((field) => record[field] === sessionKey);
}

function normalizeSessionStatus(entry: unknown): SessionStatus {
  if (!entry || typeof entry !== "object") {
    return "unknown";
  }

  const record = entry as Record<string, unknown>;
  const rawStatus = record.status;

  if (rawStatus === "running" || rawStatus === "done" || rawStatus === "failed") {
    return rawStatus;
  }

  if (typeof rawStatus === "string") {
    const normalized = rawStatus.trim().toLowerCase();

    if (normalized === "completed" || normalized === "complete" || normalized === "succeeded") {
      return "done";
    }

    if (normalized === "error" || normalized === "aborted") {
      return "failed";
    }
  }

  if (record.endedAt || record.completedAt) {
    return record.error || record.failedAt ? "failed" : "done";
  }

  if (record.error || record.failedAt || record.abortedLastRun === true) {
    return "failed";
  }

  return "running";
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function getExecaRunner(): Promise<ExecaRunner> {
  if (testingGlobals.__nexumStatusExeca) {
    return testingGlobals.__nexumStatusExeca;
  }

  if (cachedExecaRunner) {
    return cachedExecaRunner;
  }

  const { execa } = await loadExecaModule();
  cachedExecaRunner = execa;
  return execa;
}
