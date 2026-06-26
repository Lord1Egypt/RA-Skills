import { readFile, writeFile, unlink } from "fs/promises";
import { join } from "path";

const LOCK_FILE = ".memory-dream.lock";

interface LockData {
  pid: number;
  timestamp: string;
}

/**
 * Check if a process is alive by sending signal 0 (no-op liveness probe).
 * Signal 0 does not kill or interrupt the process — it only checks existence.
 * See: https://man7.org/linux/man-pages/man2/kill.2.html
 */
function isProcessRunning(pid: number): boolean {
  try {
    // POSIX signal 0 = liveness check only, no side effects
    const LIVENESS_PROBE = 0 as unknown as NodeJS.Signals;
    process.kill(pid, LIVENESS_PROBE);
    return true;
  } catch {
    return false;
  }
}

export async function acquireLock(agentDir: string): Promise<boolean> {
  const lockPath = join(agentDir, LOCK_FILE);

  // Check if lock already exists
  try {
    const raw = await readFile(lockPath, "utf-8");
    const existing: LockData = JSON.parse(raw);
    if (isProcessRunning(existing.pid)) {
      return false; // Lock held by a running process
    }
    // Stale lock — process is dead, we can overwrite
  } catch {
    // No lock file exists, proceed
  }

  const lockData: LockData = {
    pid: process.pid,
    timestamp: new Date().toISOString(),
  };

  await writeFile(lockPath, JSON.stringify(lockData, null, 2), "utf-8");
  return true;
}

export async function releaseLock(agentDir: string): Promise<void> {
  const lockPath = join(agentDir, LOCK_FILE);
  try {
    await unlink(lockPath);
  } catch {
    // Already gone — that's fine
  }
}

export async function isLocked(agentDir: string): Promise<boolean> {
  const lockPath = join(agentDir, LOCK_FILE);
  try {
    const raw = await readFile(lockPath, "utf-8");
    const existing: LockData = JSON.parse(raw);
    return isProcessRunning(existing.pid);
  } catch {
    return false;
  }
}
