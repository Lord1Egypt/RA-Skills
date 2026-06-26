/**
 * Unit tests for ProviderSessionRegistry.
 *
 * Mocks the filesystem to prevent real file I/O.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

// Mock config module — provide constants used by provider-sessions.ts
vi.mock("../src/config.js", async () => {
  return {
    PROVIDER_SESSIONS_FILE: "/tmp/test-sessions.json",
    PROVIDER_SESSION_TTL_MS: 2 * 60 * 60 * 1000, // 2 hours
    PROVIDER_SESSION_SWEEP_MS: 10 * 60 * 1000,
  };
});

// Mock fs to prevent real file operations
const { mockReadFileSync, mockWriteFileSync, mockMkdirSync } = vi.hoisted(() => ({
  mockReadFileSync: vi.fn(() => { throw new Error("ENOENT"); }),
  mockWriteFileSync: vi.fn(),
  mockMkdirSync: vi.fn(),
}));

vi.mock("node:fs", async (importOriginal) => {
  const orig = await importOriginal<typeof import("node:fs")>();
  return {
    ...orig,
    readFileSync: mockReadFileSync,
    writeFileSync: mockWriteFileSync,
    mkdirSync: mockMkdirSync,
  };
});

import { ProviderSessionRegistry } from "../src/provider-sessions.js";

// ──────────────────────────────────────────────────────────────────────────────

describe("ProviderSessionRegistry", () => {
  let registry: ProviderSessionRegistry;

  beforeEach(() => {
    mockReadFileSync.mockImplementation(() => { throw new Error("ENOENT"); });
    mockWriteFileSync.mockClear();
    mockMkdirSync.mockClear();
    registry = new ProviderSessionRegistry();
  });

  afterEach(() => {
    registry.stop();
  });

  // ── createSession ──────────────────────────────────────────────────────

  describe("createSession()", () => {
    it("creates a session with correct fields", () => {
      const session = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(session.id).toMatch(/^claude:session-[a-f0-9]+$/);
      expect(session.provider).toBe("claude");
      expect(session.modelAlias).toBe("cli-claude/claude-sonnet-4-6");
      expect(session.state).toBe("active");
      expect(session.runCount).toBe(0);
      expect(session.timeoutCount).toBe(0);
      expect(session.createdAt).toBeGreaterThan(0);
      expect(session.updatedAt).toBe(session.createdAt);
    });

    it("creates unique session IDs", () => {
      const s1 = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      const s2 = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(s1.id).not.toBe(s2.id);
    });

    it("accepts optional metadata", () => {
      const session = registry.createSession("claude", "cli-claude/claude-sonnet-4-6", {
        meta: { profilePath: "/tmp/test" },
      });
      expect(session.meta.profilePath).toBe("/tmp/test");
    });

    it("flushes to disk after creation", () => {
      registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(mockWriteFileSync).toHaveBeenCalled();
    });
  });

  // ── getSession ─────────────────────────────────────────────────────────

  describe("getSession()", () => {
    it("returns the session by ID", () => {
      const created = registry.createSession("gemini", "cli-gemini/gemini-2.5-pro");
      const found = registry.getSession(created.id);
      expect(found).toBe(created);
    });

    it("returns undefined for unknown ID", () => {
      expect(registry.getSession("nonexistent")).toBeUndefined();
    });
  });

  // ── findSession ────────────────────────────────────────────────────────

  describe("findSession()", () => {
    it("finds most recently updated matching session", () => {
      const s1 = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      const s2 = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      // Force s2 to be newer so the comparison is deterministic
      s2.updatedAt = s1.updatedAt + 1000;
      const found = registry.findSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(found?.id).toBe(s2.id);
    });

    it("returns undefined when no match", () => {
      registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(registry.findSession("gemini", "cli-gemini/gemini-2.5-pro")).toBeUndefined();
    });

    it("skips expired sessions", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      s.state = "expired";
      expect(registry.findSession("claude", "cli-claude/claude-sonnet-4-6")).toBeUndefined();
    });
  });

  // ── ensureSession ──────────────────────────────────────────────────────

  describe("ensureSession()", () => {
    it("reuses existing active session", () => {
      const s1 = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      const s2 = registry.ensureSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(s2.id).toBe(s1.id);
    });

    it("creates new session when none exists", () => {
      const s = registry.ensureSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(s.id).toMatch(/^claude:session-/);
    });

    it("touches the existing session", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      const originalUpdated = s.updatedAt;
      // Small delay to ensure timestamp changes
      s.updatedAt = originalUpdated - 1000;
      registry.ensureSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(s.updatedAt).toBeGreaterThan(originalUpdated - 1000);
    });
  });

  // ── touchSession ───────────────────────────────────────────────────────

  describe("touchSession()", () => {
    it("updates the timestamp", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      const before = s.updatedAt;
      s.updatedAt = before - 5000;
      registry.touchSession(s.id);
      expect(s.updatedAt).toBeGreaterThanOrEqual(before);
    });

    it("returns false for unknown session", () => {
      expect(registry.touchSession("nonexistent")).toBe(false);
    });

    it("reactivates idle sessions", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      s.state = "idle";
      registry.touchSession(s.id);
      expect(s.state).toBe("active");
    });
  });

  // ── recordRun ──────────────────────────────────────────────────────────

  describe("recordRun()", () => {
    it("increments run count", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      registry.recordRun(s.id, false);
      expect(s.runCount).toBe(1);
      expect(s.timeoutCount).toBe(0);
      expect(s.state).toBe("idle");
    });

    it("increments timeout count when timedOut is true", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      registry.recordRun(s.id, true);
      expect(s.runCount).toBe(1);
      expect(s.timeoutCount).toBe(1);
    });

    it("sets state to idle after run", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(s.state).toBe("active");
      registry.recordRun(s.id, false);
      expect(s.state).toBe("idle");
    });
  });

  // ── deleteSession ──────────────────────────────────────────────────────

  describe("deleteSession()", () => {
    it("removes the session", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      expect(registry.deleteSession(s.id)).toBe(true);
      expect(registry.getSession(s.id)).toBeUndefined();
    });

    it("returns false for unknown ID", () => {
      expect(registry.deleteSession("nonexistent")).toBe(false);
    });
  });

  // ── stats ──────────────────────────────────────────────────────────────

  describe("stats()", () => {
    it("returns correct counts", () => {
      const s1 = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      const s2 = registry.createSession("gemini", "cli-gemini/gemini-2.5-pro");
      registry.recordRun(s2.id, false); // s2 → idle
      const stats = registry.stats();
      expect(stats.total).toBe(2);
      expect(stats.active).toBe(1);
      expect(stats.idle).toBe(1);
      expect(stats.expired).toBe(0);
    });
  });

  // ── sweep ──────────────────────────────────────────────────────────────

  describe("sweep()", () => {
    it("removes stale sessions", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      // Make the session very old
      s.updatedAt = Date.now() - 3 * 60 * 60 * 1000; // 3 hours ago
      registry.sweep();
      expect(registry.getSession(s.id)).toBeUndefined();
    });

    it("keeps recent sessions", () => {
      const s = registry.createSession("claude", "cli-claude/claude-sonnet-4-6");
      registry.sweep();
      expect(registry.getSession(s.id)).toBeDefined();
    });
  });

  // ── persistence ────────────────────────────────────────────────────────

  describe("persistence", () => {
    it("loads sessions from disk on construction", () => {
      const stored = {
        version: 1,
        sessions: [{
          id: "claude:session-abc123",
          provider: "claude",
          modelAlias: "cli-claude/claude-sonnet-4-6",
          createdAt: Date.now() - 1000,
          updatedAt: Date.now() - 500,
          state: "idle" as const,
          runCount: 3,
          timeoutCount: 1,
          meta: {},
        }],
      };
      mockReadFileSync.mockReturnValue(JSON.stringify(stored));
      const freshRegistry = new ProviderSessionRegistry();
      const loaded = freshRegistry.getSession("claude:session-abc123");
      expect(loaded).toBeDefined();
      expect(loaded!.runCount).toBe(3);
      freshRegistry.stop();
    });

    it("skips expired sessions on load", () => {
      const stored = {
        version: 1,
        sessions: [{
          id: "claude:session-old",
          provider: "claude",
          modelAlias: "cli-claude/claude-sonnet-4-6",
          createdAt: Date.now() - 5 * 60 * 60 * 1000,
          updatedAt: Date.now() - 5 * 60 * 60 * 1000, // 5 hours ago
          state: "idle" as const,
          runCount: 1,
          timeoutCount: 0,
          meta: {},
        }],
      };
      mockReadFileSync.mockReturnValue(JSON.stringify(stored));
      const freshRegistry = new ProviderSessionRegistry();
      expect(freshRegistry.getSession("claude:session-old")).toBeUndefined();
      freshRegistry.stop();
    });
  });
});

// Config module tests are in a separate file (config.test.ts) without mocks.
