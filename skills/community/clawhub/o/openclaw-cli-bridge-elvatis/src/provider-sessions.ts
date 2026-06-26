/**
 * provider-sessions.ts
 *
 * Persistent session registry for CLI bridge provider sessions.
 *
 * A "provider session" represents a long-lived context with a CLI provider
 * (Claude, Gemini, Codex, etc.). Sessions survive across individual runs:
 * when a run times out, the session persists so that follow-up runs can
 * resume in the same context.
 *
 * Session vs Run:
 *   - Session: long-lived unit (provider context, profile, remote session ID)
 *   - Run: single request within a session (messages, tools, timeout)
 *
 * Storage: in-memory Map + periodic flush to ~/.openclaw/cli-bridge/sessions.json.
 */

import { randomBytes } from "node:crypto";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import {
  PROVIDER_SESSIONS_FILE,
  PROVIDER_SESSION_TTL_MS,
  PROVIDER_SESSION_SWEEP_MS,
} from "./config.js";

// ──────────────────────────────────────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────────────────────────────────────

export type ProviderAlias = "claude" | "gemini" | "grok" | "codex" | "opencode" | "pi" | "bitnet" | string;

export type SessionState = "active" | "idle" | "expired";

export interface ProviderSession {
  /** Unique session ID, e.g. "claude:session-a1b2c3d4". */
  id: string;
  /** Provider type. */
  provider: ProviderAlias;
  /** Full model alias, e.g. "cli-claude/claude-sonnet-4-6". */
  modelAlias: string;
  /** Unix timestamp when the session was created. */
  createdAt: number;
  /** Unix timestamp of the last activity (run start, touch). */
  updatedAt: number;
  /** Current session state. */
  state: SessionState;
  /** Total runs executed in this session. */
  runCount: number;
  /** Number of runs that timed out. */
  timeoutCount: number;
  /** Provider-specific state (profile path, remote session ID, etc.). */
  meta: Record<string, unknown>;
}

export interface CreateSessionOptions {
  /** Provider-specific metadata. */
  meta?: Record<string, unknown>;
}

// ──────────────────────────────────────────────────────────────────────────────
// Registry
// ──────────────────────────────────────────────────────────────────────────────

/** Serialized format of the sessions file. */
interface SessionStore {
  version: 1;
  sessions: ProviderSession[];
}

export class ProviderSessionRegistry {
  private sessions = new Map<string, ProviderSession>();
  private sweepTimer: ReturnType<typeof setInterval> | null = null;
  private dirty = false;

  constructor() {
    this.load();
    this.sweepTimer = setInterval(() => this.sweep(), PROVIDER_SESSION_SWEEP_MS);
    if (this.sweepTimer.unref) this.sweepTimer.unref();
  }

  // ── CRUD ─────────────────────────────────────────────────────────────────

  /**
   * Create a new provider session.
   * Returns the session with a unique ID.
   */
  createSession(
    provider: ProviderAlias,
    modelAlias: string,
    opts: CreateSessionOptions = {}
  ): ProviderSession {
    const now = Date.now();
    const id = `${provider}:session-${randomBytes(6).toString("hex")}`;
    const session: ProviderSession = {
      id,
      provider,
      modelAlias,
      createdAt: now,
      updatedAt: now,
      state: "active",
      runCount: 0,
      timeoutCount: 0,
      meta: opts.meta ?? {},
    };
    this.sessions.set(id, session);
    this.dirty = true;
    this.flush();
    return session;
  }

  /** Get a session by ID. Returns undefined if not found. */
  getSession(id: string): ProviderSession | undefined {
    return this.sessions.get(id);
  }

  /**
   * Find an existing active session for the given provider+model.
   * Returns the most recently updated match, or undefined.
   */
  findSession(provider: ProviderAlias, modelAlias: string): ProviderSession | undefined {
    let best: ProviderSession | undefined;
    for (const s of this.sessions.values()) {
      if (s.provider !== provider || s.modelAlias !== modelAlias) continue;
      if (s.state === "expired") continue;
      if (!best || s.updatedAt > best.updatedAt) best = s;
    }
    return best;
  }

  /**
   * Get or create a session for the given provider+model.
   * Reuses existing active session if available.
   */
  ensureSession(
    provider: ProviderAlias,
    modelAlias: string,
    opts: CreateSessionOptions = {}
  ): ProviderSession {
    const existing = this.findSession(provider, modelAlias);
    if (existing) {
      this.touchSession(existing.id);
      return existing;
    }
    return this.createSession(provider, modelAlias, opts);
  }

  /**
   * Update the session's last-activity timestamp and set state to active.
   * Call this at the start of every run.
   */
  touchSession(id: string): boolean {
    const session = this.sessions.get(id);
    if (!session) return false;
    session.updatedAt = Date.now();
    if (session.state === "idle") session.state = "active";
    this.dirty = true;
    return true;
  }

  /** Record that a run completed in this session. */
  recordRun(id: string, timedOut: boolean): void {
    const session = this.sessions.get(id);
    if (!session) return;
    session.runCount++;
    if (timedOut) session.timeoutCount++;
    session.updatedAt = Date.now();
    session.state = "idle"; // run finished, session stays alive
    this.dirty = true;
    this.flush();
  }

  /** Delete a session by ID. */
  deleteSession(id: string): boolean {
    const deleted = this.sessions.delete(id);
    if (deleted) {
      this.dirty = true;
      this.flush();
    }
    return deleted;
  }

  /** List all sessions. */
  listSessions(): ProviderSession[] {
    return [...this.sessions.values()];
  }

  /** Get summary stats for logging/status. */
  stats(): { total: number; active: number; idle: number; expired: number } {
    let active = 0, idle = 0, expired = 0;
    for (const s of this.sessions.values()) {
      if (s.state === "active") active++;
      else if (s.state === "idle") idle++;
      else expired++;
    }
    return { total: this.sessions.size, active, idle, expired };
  }

  // ── Lifecycle ────────────────────────────────────────────────────────────

  /** Sweep stale sessions (older than PROVIDER_SESSION_TTL_MS without activity). */
  sweep(): void {
    const now = Date.now();
    let changed = false;
    for (const [id, session] of this.sessions) {
      if (now - session.updatedAt > PROVIDER_SESSION_TTL_MS) {
        session.state = "expired";
        this.sessions.delete(id);
        changed = true;
      }
    }
    if (changed) {
      this.dirty = true;
      this.flush();
    }
  }

  /** Stop the sweep timer (for graceful shutdown). */
  stop(): void {
    if (this.sweepTimer) {
      clearInterval(this.sweepTimer);
      this.sweepTimer = null;
    }
    this.flush();
  }

  // ── Persistence ──────────────────────────────────────────────────────────

  /** Load sessions from disk. */
  private load(): void {
    try {
      const raw = readFileSync(PROVIDER_SESSIONS_FILE, "utf-8");
      const store = JSON.parse(raw) as SessionStore;
      if (store.version === 1 && Array.isArray(store.sessions)) {
        for (const s of store.sessions) {
          // Skip expired sessions on load
          if (Date.now() - s.updatedAt > PROVIDER_SESSION_TTL_MS) continue;
          this.sessions.set(s.id, s);
        }
      }
    } catch {
      // No file yet or corrupt — start fresh
    }
  }

  /** Flush dirty sessions to disk. */
  private flush(): void {
    if (!this.dirty) return;
    try {
      mkdirSync(dirname(PROVIDER_SESSIONS_FILE), { recursive: true });
      const store: SessionStore = {
        version: 1,
        sessions: [...this.sessions.values()],
      };
      writeFileSync(PROVIDER_SESSIONS_FILE, JSON.stringify(store, null, 2) + "\n", "utf-8");
      this.dirty = false;
    } catch {
      // Non-fatal — sessions are still in memory
    }
  }
}

/** Shared singleton instance. */
export const providerSessions = new ProviderSessionRegistry();
