/**
 * session-manager.ts
 *
 * Manages long-running CLI sessions as background processes.
 * Each session spawns a CLI subprocess, buffers stdout/stderr, and allows
 * polling, log streaming, stdin writes, and graceful termination.
 *
 * Singleton pattern — import and use the shared `sessionManager` instance.
 */

import { spawn, type ChildProcess } from "node:child_process";
import { randomBytes } from "node:crypto";
import { tmpdir, homedir } from "node:os";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { execSync } from "node:child_process";
import { formatPrompt, type ChatMessage } from "./cli-runner.js";
import { createIsolatedWorkdir, cleanupWorkdir, sweepOrphanedWorkdirs } from "./workdir.js";
import {
  SESSION_TTL_MS,
  CLEANUP_INTERVAL_MS,
  SESSION_KILL_GRACE_MS,
} from "./config.js";

// ──────────────────────────────────────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────────────────────────────────────

export type SessionStatus = "running" | "exited" | "killed";

export interface SessionEntry {
  proc: ChildProcess;
  stdout: string;
  stderr: string;
  startTime: number;
  exitCode: number | null;
  model: string;
  status: SessionStatus;
  /** Isolated workdir created for this session (null if caller provided explicit workdir). */
  isolatedWorkdir: string | null;
}

export interface SessionInfo {
  sessionId: string;
  model: string;
  status: SessionStatus;
  startTime: number;
  exitCode: number | null;
  /** Isolated workdir path (null if not using workdir isolation). */
  isolatedWorkdir: string | null;
}

export interface SpawnOptions {
  workdir?: string;
  timeout?: number;
  /**
   * If true, create an isolated temp directory for this session.
   * The directory is automatically cleaned up when the session exits or is killed.
   * Ignored if `workdir` is explicitly set.
   * Default: false (uses per-runner defaults: tmpdir for gemini, homedir for others).
   */
  isolateWorkdir?: boolean;
}

// ──────────────────────────────────────────────────────────────────────────────
// Minimal env (mirrors cli-runner.ts buildMinimalEnv)
// ──────────────────────────────────────────────────────────────────────────────

function buildMinimalEnv(): Record<string, string> {
  const pick = (key: string) => process.env[key];
  const env: Record<string, string> = { NO_COLOR: "1", TERM: "dumb" };

  for (const key of ["HOME", "PATH", "USER", "LOGNAME", "SHELL", "TMPDIR", "TMP", "TEMP"]) {
    const v = pick(key);
    if (v) env[key] = v;
  }
  for (const key of [
    "GOOGLE_APPLICATION_CREDENTIALS",
    "ANTHROPIC_API_KEY",
    "CLAUDE_API_KEY",
    "CODEX_API_KEY",
    "OPENAI_API_KEY",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "XDG_CACHE_HOME",
    "XDG_RUNTIME_DIR",
    "DBUS_SESSION_BUS_ADDRESS",
  ]) {
    const v = pick(key);
    if (v) env[key] = v;
  }

  return env;
}

// ──────────────────────────────────────────────────────────────────────────────
// Session Manager
// ──────────────────────────────────────────────────────────────────────────────

// SESSION_TTL_MS, CLEANUP_INTERVAL_MS, SESSION_KILL_GRACE_MS imported from config.ts

export class SessionManager {
  private sessions = new Map<string, SessionEntry>();
  private cleanupTimer: ReturnType<typeof setInterval> | null = null;

  constructor() {
    this.cleanupTimer = setInterval(() => this.cleanup(), CLEANUP_INTERVAL_MS);
    // Don't keep the process alive just for cleanup
    if (this.cleanupTimer.unref) this.cleanupTimer.unref();
  }

  /**
   * Spawn a new CLI session for the given model + messages.
   * Returns a unique sessionId (random hex).
   */
  spawn(model: string, messages: ChatMessage[], opts: SpawnOptions = {}): string {
    // Validate model ID before it reaches spawn() args to prevent command injection
    // (CodeQL js/command-line-injection). Allow only safe chars: letters, digits,
    // dots, hyphens, underscores, and forward slashes (for provider prefixes).
    if (!/^[a-zA-Z0-9._\-\/]+$/.test(model)) {
      throw new Error(`Invalid model ID: "${model}". Only alphanumeric characters, dots, hyphens, underscores, and slashes are allowed.`);
    }

    const sessionId = randomBytes(8).toString("hex");
    const prompt = formatPrompt(messages);

    // Workdir isolation: create a temp dir if requested and no explicit workdir given
    let isolatedDir: string | null = null;
    const effectiveOpts = { ...opts };
    if (opts.isolateWorkdir && !opts.workdir) {
      isolatedDir = createIsolatedWorkdir();
      effectiveOpts.workdir = isolatedDir;
    }

    const { cmd, args, cwd, useStdin } = this.resolveCliCommand(model, prompt, effectiveOpts);

    const proc = spawn(cmd, args, {
      env: buildMinimalEnv(),
      cwd,
      timeout: opts.timeout,
    });

    const entry: SessionEntry = {
      proc,
      stdout: "",
      stderr: "",
      startTime: Date.now(),
      exitCode: null,
      model,
      status: "running",
      isolatedWorkdir: isolatedDir,
    };

    if (useStdin) {
      proc.stdin.write(prompt, "utf8", () => {
        proc.stdin.end();
      });
    }

    proc.stdout?.on("data", (d: Buffer) => { entry.stdout += d.toString(); });
    proc.stderr?.on("data", (d: Buffer) => { entry.stderr += d.toString(); });

    proc.on("close", (code) => {
      entry.exitCode = code ?? 0;
      if (entry.status === "running") entry.status = "exited";
      // Auto-cleanup isolated workdir on process exit
      if (entry.isolatedWorkdir) {
        cleanupWorkdir(entry.isolatedWorkdir);
      }
    });

    proc.on("error", () => {
      if (entry.status === "running") entry.status = "exited";
      entry.exitCode = entry.exitCode ?? 1;
      // Auto-cleanup isolated workdir on error too
      if (entry.isolatedWorkdir) {
        cleanupWorkdir(entry.isolatedWorkdir);
      }
    });

    this.sessions.set(sessionId, entry);
    return sessionId;
  }

  /** Check if a session is still running. */
  poll(sessionId: string): { running: boolean; exitCode: number | null; status: SessionStatus } | null {
    const entry = this.sessions.get(sessionId);
    if (!entry) return null;
    return {
      running: entry.status === "running",
      exitCode: entry.exitCode,
      status: entry.status,
    };
  }

  /** Get buffered stdout/stderr from offset. */
  log(sessionId: string, offset = 0): { stdout: string; stderr: string; offset: number } | null {
    const entry = this.sessions.get(sessionId);
    if (!entry) return null;
    return {
      stdout: entry.stdout.slice(offset),
      stderr: entry.stderr.slice(offset),
      offset: entry.stdout.length,
    };
  }

  /** Write data to the session's stdin. */
  write(sessionId: string, data: string): boolean {
    const entry = this.sessions.get(sessionId);
    if (!entry || entry.status !== "running") return false;
    try {
      entry.proc.stdin?.write(data, "utf8");
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Gracefully terminate a session: SIGTERM first, then SIGKILL after grace period.
   * This prevents the ambiguous "exit 143 (no output)" pattern.
   */
  kill(sessionId: string): boolean {
    const entry = this.sessions.get(sessionId);
    if (!entry || entry.status !== "running") return false;
    entry.status = "killed";
    entry.proc.kill("SIGTERM");
    // If the process doesn't exit within the grace period, force-kill it
    setTimeout(() => {
      try { if (!entry.proc.killed) entry.proc.kill("SIGKILL"); } catch { /* already dead */ }
    }, SESSION_KILL_GRACE_MS);
    return true;
  }

  /** List all sessions with their status. */
  list(): SessionInfo[] {
    const result: SessionInfo[] = [];
    for (const [sessionId, entry] of this.sessions) {
      result.push({
        sessionId,
        model: entry.model,
        status: entry.status,
        startTime: entry.startTime,
        exitCode: entry.exitCode,
        isolatedWorkdir: entry.isolatedWorkdir,
      });
    }
    return result;
  }

  /** Remove sessions older than SESSION_TTL_MS. Kill running ones with graceful SIGTERM→SIGKILL. */
  cleanup(): void {
    const now = Date.now();
    for (const [sessionId, entry] of this.sessions) {
      if (now - entry.startTime > SESSION_TTL_MS) {
        if (entry.status === "running") {
          entry.proc.kill("SIGTERM");
          entry.status = "killed";
          // Escalate to SIGKILL after grace period
          setTimeout(() => {
            try { if (!entry.proc.killed) entry.proc.kill("SIGKILL"); } catch { /* already dead */ }
          }, SESSION_KILL_GRACE_MS);
        }
        // Clean up isolated workdir if it wasn't cleaned on exit
        if (entry.isolatedWorkdir) {
          cleanupWorkdir(entry.isolatedWorkdir);
        }
        this.sessions.delete(sessionId);
      }
    }
    // Sweep orphaned workdirs from crashed sessions
    sweepOrphanedWorkdirs();
  }

  /** Stop the cleanup timer (for graceful shutdown). SIGTERM all sessions, SIGKILL after grace. */
  stop(): void {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
      this.cleanupTimer = null;
    }
    // Kill all running sessions with graceful SIGTERM → SIGKILL escalation
    for (const [, entry] of this.sessions) {
      if (entry.status === "running") {
        entry.proc.kill("SIGTERM");
        entry.status = "killed";
        setTimeout(() => {
          try { if (!entry.proc.killed) entry.proc.kill("SIGKILL"); } catch { /* already dead */ }
        }, SESSION_KILL_GRACE_MS);
      }
      if (entry.isolatedWorkdir) {
        cleanupWorkdir(entry.isolatedWorkdir);
      }
    }
  }

  // ────────────────────────────────────────────────────────────────────────────
  // Internal: resolve CLI command + args for a model
  // ────────────────────────────────────────────────────────────────────────────

  private resolveCliCommand(
    model: string,
    prompt: string,
    opts: SpawnOptions
  ): { cmd: string; args: string[]; cwd: string; useStdin: boolean } {
    const normalized = model.startsWith("vllm/") ? model.slice(5) : model;
    const stripPfx = (id: string) => { const s = id.indexOf("/"); return s === -1 ? id : id.slice(s + 1); };
    const modelName = stripPfx(normalized);

    if (normalized.startsWith("cli-gemini/")) {
      return {
        cmd: "gemini",
        args: ["-m", modelName, "-p", ""],
        cwd: opts.workdir ?? tmpdir(),
        useStdin: true,
      };
    }

    if (normalized.startsWith("cli-claude/")) {
      return {
        cmd: "claude",
        args: ["-p", "--output-format", "text", "--permission-mode", "plan", "--tools", "", "--model", modelName],
        cwd: opts.workdir ?? homedir(),
        useStdin: true,
      };
    }

    if (normalized.startsWith("openai-codex/")) {
      const cwd = opts.workdir ?? homedir();
      // Ensure git repo for Codex
      if (!existsSync(join(cwd, ".git"))) {
        try { execSync("git init", { cwd, stdio: "ignore" }); } catch { /* best effort */ }
      }
      return {
        cmd: "codex",
        args: ["exec", "--model", modelName, "--full-auto"],
        cwd,
        useStdin: true,
      };
    }

    if (normalized.startsWith("opencode/")) {
      return {
        cmd: "opencode",
        args: ["run", prompt],
        cwd: opts.workdir ?? homedir(),
        useStdin: false,
      };
    }

    if (normalized.startsWith("pi/")) {
      return {
        cmd: "pi",
        args: ["-p", prompt],
        cwd: opts.workdir ?? homedir(),
        useStdin: false,
      };
    }

    // Fallback: try as a generic CLI (stdin-based)
    return {
      cmd: modelName,
      args: [],
      cwd: opts.workdir ?? homedir(),
      useStdin: true,
    };
  }
}

/** Shared singleton instance. */
export const sessionManager = new SessionManager();
