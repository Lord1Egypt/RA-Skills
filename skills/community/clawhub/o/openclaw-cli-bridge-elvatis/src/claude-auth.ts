/**
 * claude-auth.ts
 *
 * Proactive OAuth token management for the Claude Code CLI.
 *
 * Problem: Claude Code stores its claude.ai OAuth token in
 * ~/.claude/.credentials.json. The access token expires every ~8-12 hours.
 * When the gateway runs as a systemd service without a browser, the normal
 * interactive refresh flow never triggers — the token silently expires and
 * every CLI call returns 401.
 *
 * Solution: This module reads the credentials file, tracks expiry, and
 * proactively refreshes the token by running `claude -p "ping"` before it
 * expires. It also retries once on 401 errors.
 *
 * Design:
 *   - scheduleTokenRefresh()  — call once at proxy startup; sets an internal
 *                               timer that fires 30 min before expiry
 *   - ensureClaudeToken()     — call before every claude CLI invocation;
 *                               triggers an immediate refresh if token is
 *                               expired or expires within the next 5 minutes
 *   - refreshClaudeToken()    — runs `claude -p "ping"` to force token refresh
 *                               (Claude Code auto-refreshes on any API call)
 */

import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { spawn } from "node:child_process";

// ──────────────────────────────────────────────────────────────────────────────
// Config
// ──────────────────────────────────────────────────────────────────────────────

/** Refresh this many ms before the token actually expires. */
const REFRESH_BEFORE_EXPIRY_MS = 30 * 60 * 1000; // 30 min

/** If token expires within this window, refresh synchronously before the call. */
const REFRESH_SYNC_WINDOW_MS = 5 * 60 * 1000; // 5 min

/** Max time to wait for a refresh ping. */
const REFRESH_TIMEOUT_MS = 30_000;

const CREDENTIALS_PATH = join(homedir(), ".claude", ".credentials.json");

// ──────────────────────────────────────────────────────────────────────────────
// State
// ──────────────────────────────────────────────────────────────────────────────

let refreshTimer: ReturnType<typeof setInterval> | null = null;
let nextRefreshAt = 0; // epoch ms when the next refresh is due
let refreshInProgress: Promise<void> | null = null;
let log: (msg: string) => void = () => {};

// ──────────────────────────────────────────────────────────────────────────────
// Public API
// ──────────────────────────────────────────────────────────────────────────────

/** Configure the logger (call once at startup). */
export function setAuthLogger(logger: (msg: string) => void): void {
  log = logger;
}

/**
 * Stop the background token refresh interval.
 * Call in plugin deactivate / proxy server close to avoid timer leaks.
 */
export function stopTokenRefresh(): void {
  if (refreshTimer) {
    clearInterval(refreshTimer);
    refreshTimer = null;
    nextRefreshAt = 0;
    log("[cli-bridge:auth] Token refresh scheduler stopped");
  }
}

/**
 * Read the current token expiry from ~/.claude/.credentials.json.
 * Returns null if the file doesn't exist or has no OAuth credentials
 * (e.g. API-key users — they don't need token management).
 */
export async function readTokenExpiry(): Promise<number | null> {
  try {
    const raw = await readFile(CREDENTIALS_PATH, "utf8");
    const creds = JSON.parse(raw) as {
      claudeAiOauth?: { expiresAt?: number };
    };
    const expiresAt = creds?.claudeAiOauth?.expiresAt;
    return typeof expiresAt === "number" ? expiresAt : null;
  } catch {
    return null;
  }
}

/**
 * Schedule a proactive token refresh 30 minutes before expiry.
 * Call once at proxy startup. Safe to call multiple times (restarts the interval).
 *
 * Uses a 10-minute polling interval instead of a single long setTimeout so that
 * the scheduler survives system sleep/resume without missing its window.
 */
export async function scheduleTokenRefresh(): Promise<void> {
  // Clear any existing interval before (re-)starting
  stopTokenRefresh();

  const expiresAt = await readTokenExpiry();
  if (expiresAt === null) {
    log("[cli-bridge:auth] No OAuth credentials found — skipping token scheduling (API key auth?)");
    return;
  }

  const now = Date.now();
  const msUntilExpiry = expiresAt - now;

  if (msUntilExpiry <= 0) {
    log("[cli-bridge:auth] Token already expired — refreshing now");
    await refreshClaudeToken();
    return;
  }

  if (msUntilExpiry <= REFRESH_BEFORE_EXPIRY_MS) {
    // Expires within the next 30 min — refresh immediately
    log(`[cli-bridge:auth] Token expires in ${Math.round(msUntilExpiry / 60000)}min — refreshing now`);
    await refreshClaudeToken();
    return;
  }

  // Set the target time for the first scheduled refresh (30 min before expiry)
  nextRefreshAt = expiresAt - REFRESH_BEFORE_EXPIRY_MS;
  const refreshInMin = Math.round((nextRefreshAt - now) / 60000);
  log(`[cli-bridge:auth] Token valid for ${Math.round(msUntilExpiry / 60000)}min — refresh scheduled in ${refreshInMin}min`);

  // Poll every 10 minutes instead of a single long setTimeout.
  // This survives laptop sleep/resume without missing the refresh window.
  const POLL_INTERVAL_MS = 10 * 60 * 1000;
  refreshTimer = setInterval(async () => {
    if (Date.now() < nextRefreshAt) return; // not yet due
    log("[cli-bridge:auth] Scheduled token refresh triggered");
    await refreshClaudeToken();
    // Recompute next refresh target from the freshly written credentials
    const newExpiry = await readTokenExpiry();
    if (newExpiry) {
      nextRefreshAt = newExpiry - REFRESH_BEFORE_EXPIRY_MS;
      const nextInMin = Math.round((nextRefreshAt - Date.now()) / 60000);
      log(`[cli-bridge:auth] Next refresh in ${nextInMin}min`);
    }
  }, POLL_INTERVAL_MS);

  // Don't block process exit
  if (refreshTimer.unref) refreshTimer.unref();
}

/**
 * Ensure the Claude OAuth token is valid before making a CLI call.
 * If the token expires within REFRESH_SYNC_WINDOW_MS, refreshes synchronously.
 * No-op for API-key users (no credentials file).
 */
export async function ensureClaudeToken(): Promise<void> {
  const expiresAt = await readTokenExpiry();
  if (expiresAt === null) return; // API key user, nothing to do

  const msUntilExpiry = expiresAt - Date.now();

  if (msUntilExpiry > REFRESH_SYNC_WINDOW_MS) return; // still valid, nothing to do

  if (msUntilExpiry <= 0) {
    log("[cli-bridge:auth] Token expired — refreshing before call");
  } else {
    log(`[cli-bridge:auth] Token expires in ${Math.round(msUntilExpiry / 1000)}s — refreshing before call`);
  }

  await refreshClaudeToken();
}

/**
 * Run `claude -p "ping"` to force Claude Code to refresh its OAuth token.
 * Claude Code automatically refreshes the access token on any API call.
 * Deduplicates concurrent refresh attempts.
 */
export async function refreshClaudeToken(): Promise<void> {
  // Deduplicate concurrent refresh calls
  if (refreshInProgress) {
    await refreshInProgress;
    return;
  }

  refreshInProgress = doRefresh();
  try {
    await refreshInProgress;
  } finally {
    refreshInProgress = null;
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Internal
// ──────────────────────────────────────────────────────────────────────────────

async function doRefresh(): Promise<void> {
  log("[cli-bridge:auth] Refreshing Claude OAuth token...");

  const result = await runRefreshPing();

  if (result.exitCode !== 0) {
    const stderr = result.stderr || "(no output)";
    if (stderr.includes("401") || stderr.includes("authentication_error") || stderr.includes("Invalid authentication credentials")) {
      throw new Error(
        "Claude CLI OAuth token refresh failed (401). " +
        "Re-login required: run `claude auth logout && claude auth login` in a terminal."
      );
    }
    // Non-auth errors (network blip etc.) — log but don't throw, let the actual call fail naturally
    log(`[cli-bridge:auth] Token refresh exited ${result.exitCode}: ${stderr.slice(0, 200)}`);
    return;
  }

  // Re-read expiry and update the next refresh target for the running interval
  const newExpiry = await readTokenExpiry();
  if (newExpiry) {
    const validForMin = Math.round((newExpiry - Date.now()) / 60000);
    log(`[cli-bridge:auth] Token refreshed — valid for ${validForMin}min`);
    nextRefreshAt = newExpiry - REFRESH_BEFORE_EXPIRY_MS;
  }
}

function runRefreshPing(): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  return new Promise((resolve) => {
    const env: Record<string, string> = { NO_COLOR: "1", TERM: "dumb" };
    for (const key of ["HOME", "PATH", "USER", "XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"]) {
      const v = process.env[key];
      if (v) env[key] = v;
    }

    const proc = spawn(
      "claude",
      ["-p", "ping", "--output-format", "text", "--permission-mode", "plan", "--tools", ""],
      { timeout: REFRESH_TIMEOUT_MS, env }
    );

    let stdout = "";
    let stderr = "";
    proc.stdout.on("data", (d: Buffer) => { stdout += d.toString(); });
    proc.stderr.on("data", (d: Buffer) => { stderr += d.toString(); });
    proc.on("close", (code) => resolve({ stdout: stdout.trim(), stderr: stderr.trim(), exitCode: code ?? 0 }));
    proc.on("error", (err) => resolve({ stdout: "", stderr: err.message, exitCode: 1 }));
  });
}
