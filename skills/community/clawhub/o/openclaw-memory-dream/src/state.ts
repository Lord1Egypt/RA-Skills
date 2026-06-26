import { readFile, writeFile, mkdir } from "fs/promises";
import { join } from "path";

async function ensureDir(dir: string): Promise<void> {
  await mkdir(dir, { recursive: true });
}

export interface DreamState {
  sessionCount: number;
  lastRunAt: string | null;
  lastRunStatus: "success" | "failed" | "running" | null;
  lastRunSummary: string | null;
  lastMessageAt: string | null;  // Tracks last turn timestamp for session-gap detection
}

const STATE_FILE = ".memory-dream-state.json";

const defaultState = (): DreamState => ({
  sessionCount: 0,
  lastRunAt: null,
  lastRunStatus: null,
  lastRunSummary: null,
  lastMessageAt: null,
});

export async function loadState(agentDir: string): Promise<DreamState> {
  const statePath = join(agentDir, STATE_FILE);
  try {
    const raw = await readFile(statePath, "utf-8");
    return { ...defaultState(), ...JSON.parse(raw) };
  } catch {
    return defaultState();
  }
}

export async function saveState(agentDir: string, state: DreamState): Promise<void> {
  await ensureDir(agentDir);
  const statePath = join(agentDir, STATE_FILE);
  await writeFile(statePath, JSON.stringify(state, null, 2), "utf-8");
}

export async function incrementSession(agentDir: string): Promise<DreamState> {
  const state = await loadState(agentDir);
  state.sessionCount += 1;
  await saveState(agentDir, state);
  return state;
}

/**
 * Detects a session boundary by checking if the gap since the last message
 * exceeds `sessionGapMinutes` (default 30). If so, increments session count.
 * Always updates lastMessageAt to now.
 * Returns { state, newSessionDetected }.
 */
export async function detectAndCountSession(
  agentDir: string,
  sessionGapMinutes = 30
): Promise<{ state: DreamState; newSessionDetected: boolean }> {
  const state = await loadState(agentDir);
  const now = Date.now();
  const gapMs = sessionGapMinutes * 60 * 1000;

  let newSessionDetected = false;

  if (state.lastMessageAt === null) {
    // First ever message — counts as first session
    newSessionDetected = true;
    state.sessionCount += 1;
  } else {
    const lastMs = new Date(state.lastMessageAt).getTime();
    if (now - lastMs > gapMs) {
      // Gap exceeded — this is a new session
      newSessionDetected = true;
      state.sessionCount += 1;
    }
  }

  state.lastMessageAt = new Date(now).toISOString();
  await saveState(agentDir, state);
  return { state, newSessionDetected };
}

export async function resetCounter(agentDir: string): Promise<DreamState> {
  const state = await loadState(agentDir);
  state.sessionCount = 0;
  state.lastRunAt = new Date().toISOString();
  await saveState(agentDir, state);
  return state;
}
