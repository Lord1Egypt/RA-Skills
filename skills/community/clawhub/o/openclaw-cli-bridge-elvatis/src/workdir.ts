/**
 * workdir.ts
 *
 * Workdir isolation for CLI agent spawns (Issue #6).
 *
 * Creates a unique temporary directory per agent session and cleans it up
 * after the session completes. This prevents agents from interfering with
 * each other or polluting the user's home directory.
 *
 * Each isolated workdir is created under a base directory:
 *   <base>/cli-bridge-<randomHex>/
 *
 * Default base: os.tmpdir() (e.g. /tmp/)
 * Override via OPENCLAW_CLI_BRIDGE_WORKDIR_BASE env var.
 *
 * Cleanup is best-effort: directories are removed when the session ends,
 * and a periodic sweep removes any orphaned dirs older than 1 hour.
 */

import { mkdtempSync, rmSync, readdirSync, statSync, existsSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

/** Prefix for all isolated workdir directories. */
const WORKDIR_PREFIX = "cli-bridge-";

/** Max age for orphaned workdirs before cleanup sweep removes them (ms). */
const ORPHAN_MAX_AGE_MS = 60 * 60 * 1000; // 1 hour

/** Get the base directory for isolated workdirs. */
export function getWorkdirBase(): string {
  return process.env.OPENCLAW_CLI_BRIDGE_WORKDIR_BASE ?? tmpdir();
}

/**
 * Create an isolated temporary directory for an agent session.
 * Returns the absolute path to the new directory.
 *
 * The directory is created with a random suffix to ensure uniqueness:
 *   /tmp/cli-bridge-a1b2c3d4/
 */
export function createIsolatedWorkdir(base?: string): string {
  const dir = mkdtempSync(join(base ?? getWorkdirBase(), WORKDIR_PREFIX));
  return dir;
}

/**
 * Clean up an isolated workdir by removing it and all contents.
 * Returns true if removed successfully, false if it didn't exist or failed.
 *
 * Safety: only removes directories that match the cli-bridge- prefix.
 */
export function cleanupWorkdir(dirPath: string): boolean {
  if (!dirPath || !dirPath.includes(WORKDIR_PREFIX)) {
    return false; // safety: refuse to remove dirs that don't match our prefix
  }
  try {
    rmSync(dirPath, { recursive: true, force: true });
    return true;
  } catch {
    return false;
  }
}

/**
 * Sweep orphaned workdirs older than ORPHAN_MAX_AGE_MS.
 * Scans the base directory for cli-bridge-* dirs and removes stale ones.
 * Returns the number of dirs removed.
 */
export function sweepOrphanedWorkdirs(base?: string): number {
  const baseDir = base ?? getWorkdirBase();
  let removed = 0;

  try {
    const entries = readdirSync(baseDir);
    const now = Date.now();

    for (const entry of entries) {
      if (!entry.startsWith(WORKDIR_PREFIX)) continue;

      const fullPath = join(baseDir, entry);
      try {
        const stat = statSync(fullPath);
        if (stat.isDirectory() && (now - stat.mtimeMs) > ORPHAN_MAX_AGE_MS) {
          rmSync(fullPath, { recursive: true, force: true });
          removed++;
        }
      } catch {
        // Skip entries we can't stat (race condition, permissions)
      }
    }
  } catch {
    // Base dir doesn't exist or not readable
  }

  return removed;
}

/**
 * Ensure a directory exists, creating it if needed.
 * Returns the path.
 */
export function ensureDir(dirPath: string): string {
  if (!existsSync(dirPath)) {
    mkdirSync(dirPath, { recursive: true });
  }
  return dirPath;
}
