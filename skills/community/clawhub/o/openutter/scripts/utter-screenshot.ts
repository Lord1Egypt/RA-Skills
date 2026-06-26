#!/usr/bin/env npx tsx
/**
 * utter-screenshot.ts — Request an on-demand screenshot from a running OpenUtter bot
 *
 * Usage:
 *   npx tsx skills/openutter/scripts/utter-screenshot.ts
 *
 * Sends SIGUSR1 to the running utter-join process, waits for
 * the screenshot to be saved, and prints the path.
 */

import { existsSync, readFileSync, unlinkSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const OPENUTTER_DIR = join(homedir(), ".openutter");
const OPENUTTER_WORKSPACE_DIR = join(homedir(), ".openclaw", "workspace", "openutter");
const PID_FILE = join(OPENUTTER_DIR, "otter.pid");
const SCREENSHOT_READY_FILE = join(OPENUTTER_WORKSPACE_DIR, "screenshot-ready.json");

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  // 1. Read PID file
  if (!existsSync(PID_FILE)) {
    console.error("No running OpenUtter bot found (missing PID file).");
    console.error("Start a meeting first with utter-join.ts.");
    process.exit(1);
  }

  const pid = Number.parseInt(readFileSync(PID_FILE, "utf-8").trim(), 10);
  if (Number.isNaN(pid)) {
    console.error("Invalid PID file contents.");
    process.exit(1);
  }

  // 2. Check process is alive
  try {
    process.kill(pid, 0);
  } catch {
    console.error(`OpenUtter process (PID ${pid}) is not running.`);
    try { unlinkSync(PID_FILE); } catch { /* ignore */ }
    process.exit(1);
  }

  // 3. Remove stale screenshot-ready file
  try {
    if (existsSync(SCREENSHOT_READY_FILE)) unlinkSync(SCREENSHOT_READY_FILE);
  } catch { /* ignore */ }

  // 4. Send SIGUSR1
  console.log(`Requesting screenshot from OpenUtter (PID ${pid})...`);
  process.kill(pid, "SIGUSR1");

  // 5. Poll for screenshot-ready.json
  const timeoutMs = 10_000;
  const pollMs = 500;
  const start = Date.now();

  while (Date.now() - start < timeoutMs) {
    if (existsSync(SCREENSHOT_READY_FILE)) {
      try {
        const data = JSON.parse(readFileSync(SCREENSHOT_READY_FILE, "utf-8")) as {
          path: string;
          timestamp: number;
        };
        console.log(`[OPENUTTER_SCREENSHOT] ${data.path}`);
        return;
      } catch {
        // File might be partially written, retry
      }
    }
    await sleep(pollMs);
  }

  console.error("Timed out waiting for screenshot (10s).");
  process.exit(1);
}

main().catch((err) => {
  console.error("Fatal:", err instanceof Error ? err.message : String(err));
  process.exit(1);
});
