/**
 * Unit tests for SessionManager.
 *
 * Mocks child_process.spawn so no real CLIs are executed.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { EventEmitter } from "node:events";
import type { ChildProcess } from "node:child_process";

// ── Mock child_process.spawn ────────────────────────────────────────────────

/** Minimal fake ChildProcess for testing. */
function makeFakeProc(): ChildProcess & {
  _stdout: EventEmitter;
  _stderr: EventEmitter;
  _emit: (event: string, ...args: unknown[]) => void;
} {
  const proc = new EventEmitter() as any;
  proc._stdout = new EventEmitter();
  proc._stderr = new EventEmitter();
  proc.stdout = proc._stdout;
  proc.stderr = proc._stderr;
  proc.stdin = {
    write: vi.fn((_data: string, _enc: string, cb?: () => void) => { cb?.(); }),
    end: vi.fn(),
  };
  proc.kill = vi.fn(() => true);
  proc.pid = 12345;
  proc._emit = (event: string, ...args: unknown[]) => proc.emit(event, ...args);
  return proc;
}

// vi.hoisted variables are available inside vi.mock factories
const { mockSpawn, mockExecSync, latestProcRef, mockCreateIsolatedWorkdir, mockCleanupWorkdir, mockSweepOrphanedWorkdirs } = vi.hoisted(() => ({
  mockSpawn: vi.fn(),
  mockExecSync: vi.fn(),
  latestProcRef: { current: null as any },
  mockCreateIsolatedWorkdir: vi.fn(() => "/tmp/cli-bridge-fake123"),
  mockCleanupWorkdir: vi.fn(() => true),
  mockSweepOrphanedWorkdirs: vi.fn(() => 0),
}));

vi.mock("node:child_process", async (importOriginal) => {
  const orig = await importOriginal<typeof import("node:child_process")>();
  return { ...orig, spawn: mockSpawn, execSync: mockExecSync };
});

// Mock claude-auth to prevent real token operations
vi.mock("../src/claude-auth.js", () => ({
  ensureClaudeToken: vi.fn(async () => {}),
  refreshClaudeToken: vi.fn(async () => {}),
  scheduleTokenRefresh: vi.fn(async () => {}),
  stopTokenRefresh: vi.fn(),
  setAuthLogger: vi.fn(),
}));

// Mock workdir module to prevent real FS operations in unit tests
vi.mock("../src/workdir.js", () => ({
  createIsolatedWorkdir: mockCreateIsolatedWorkdir,
  cleanupWorkdir: mockCleanupWorkdir,
  sweepOrphanedWorkdirs: mockSweepOrphanedWorkdirs,
}));

// Mock config module — provide all constants needed by session-manager.ts and cli-runner.ts
vi.mock("../src/config.js", async () => {
  return {
    SESSION_TTL_MS: 30 * 60 * 1000,
    CLEANUP_INTERVAL_MS: 5 * 60 * 1000,
    SESSION_KILL_GRACE_MS: 5_000,
    DEFAULT_CLI_TIMEOUT_MS: 120_000,
    TIMEOUT_GRACE_MS: 5_000,
    MAX_MESSAGES: 20,
    MAX_MSG_CHARS: 4_000,
    MEDIA_TMP_DIR: "/tmp/cli-bridge-media",
  };
});

// Now import SessionManager (uses the mocked spawn)
import { SessionManager } from "../src/session-manager.js";

// ──────────────────────────────────────────────────────────────────────────────

describe("SessionManager", () => {
  let mgr: SessionManager;

  beforeEach(() => {
    mgr = new SessionManager();
    mockSpawn.mockImplementation(() => {
      const proc = makeFakeProc();
      latestProcRef.current = proc;
      return proc;
    });
  });

  afterEach(() => {
    mgr.stop();
  });

  // ── spawn() ──────────────────────────────────────────────────────────────

  describe("spawn()", () => {
    it("returns a hex sessionId", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      expect(id).toMatch(/^[a-f0-9]{16}$/);
    });

    it("returns unique sessionIds on repeated calls", () => {
      const id1 = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "a" }]);
      const id2 = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "b" }]);
      expect(id1).not.toBe(id2);
    });
  });

  // ── poll() ─────────────────────────────────────────────────────────────

  describe("poll()", () => {
    it("returns running status for an active session", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      const result = mgr.poll(id);
      expect(result).not.toBeNull();
      expect(result!.running).toBe(true);
      expect(result!.status).toBe("running");
      expect(result!.exitCode).toBeNull();
    });

    it("returns exited status after process closes", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      // Simulate process exit
      latestProcRef.current._emit("close", 0);
      const result = mgr.poll(id);
      expect(result!.running).toBe(false);
      expect(result!.status).toBe("exited");
      expect(result!.exitCode).toBe(0);
    });

    it("returns null for unknown sessionId", () => {
      expect(mgr.poll("0000000000000000")).toBeNull();
    });
  });

  // ── log() ──────────────────────────────────────────────────────────────

  describe("log()", () => {
    it("returns buffered stdout output", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      latestProcRef.current._stdout.emit("data", Buffer.from("Hello "));
      latestProcRef.current._stdout.emit("data", Buffer.from("World"));
      const result = mgr.log(id);
      expect(result).not.toBeNull();
      expect(result!.stdout).toBe("Hello World");
      expect(result!.offset).toBe(11);
    });

    it("returns buffered stderr output", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      latestProcRef.current._stderr.emit("data", Buffer.from("warning"));
      const result = mgr.log(id);
      expect(result!.stderr).toBe("warning");
    });

    it("supports offset to get incremental output", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      latestProcRef.current._stdout.emit("data", Buffer.from("ABCDE"));
      const result = mgr.log(id, 3);
      expect(result!.stdout).toBe("DE");
      expect(result!.offset).toBe(5);
    });

    it("returns null for unknown sessionId", () => {
      expect(mgr.log("0000000000000000")).toBeNull();
    });
  });

  // ── write() ────────────────────────────────────────────────────────────

  describe("write()", () => {
    it("writes data to stdin of a running session", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      const proc = latestProcRef.current;
      const ok = mgr.write(id, "input data");
      expect(ok).toBe(true);
      expect(proc.stdin.write).toHaveBeenCalledWith("input data", "utf8");
    });

    it("returns false for unknown sessionId", () => {
      expect(mgr.write("0000000000000000", "data")).toBe(false);
    });

    it("returns false for an exited session", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      latestProcRef.current._emit("close", 0);
      expect(mgr.write(id, "data")).toBe(false);
    });
  });

  // ── kill() ─────────────────────────────────────────────────────────────

  describe("kill()", () => {
    it("sends SIGTERM to a running session", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      const proc = latestProcRef.current;
      const ok = mgr.kill(id);
      expect(ok).toBe(true);
      expect(proc.kill).toHaveBeenCalledWith("SIGTERM");
      // Status should be "killed"
      const poll = mgr.poll(id);
      expect(poll!.status).toBe("killed");
    });

    it("returns false for unknown sessionId", () => {
      expect(mgr.kill("0000000000000000")).toBe(false);
    });

    it("returns false for an already-exited session", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      latestProcRef.current._emit("close", 0);
      expect(mgr.kill(id)).toBe(false);
    });
  });

  // ── list() ─────────────────────────────────────────────────────────────

  describe("list()", () => {
    it("returns all sessions", () => {
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "a" }]);
      mgr.spawn("cli-claude/claude-sonnet-4-6", [{ role: "user", content: "b" }]);
      const list = mgr.list();
      expect(list).toHaveLength(2);
      expect(list[0].sessionId).toMatch(/^[a-f0-9]{16}$/);
      expect(list[0].model).toBe("cli-gemini/gemini-2.5-pro");
      expect(list[0].status).toBe("running");
      expect(list[1].model).toBe("cli-claude/claude-sonnet-4-6");
    });

    it("returns empty array when no sessions exist", () => {
      expect(mgr.list()).toHaveLength(0);
    });
  });

  // ── cleanup() ──────────────────────────────────────────────────────────

  describe("cleanup()", () => {
    it("removes sessions older than TTL", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);

      // Manually set startTime to far in the past
      const sessions = (mgr as any).sessions as Map<string, any>;
      const entry = sessions.get(id)!;
      entry.startTime = Date.now() - 31 * 60 * 1000; // 31 minutes ago

      mgr.cleanup();

      expect(mgr.poll(id)).toBeNull();
      expect(mgr.list()).toHaveLength(0);
    });

    it("kills running sessions before removing them", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      const proc = latestProcRef.current;

      const sessions = (mgr as any).sessions as Map<string, any>;
      sessions.get(id)!.startTime = Date.now() - 31 * 60 * 1000;

      mgr.cleanup();

      expect(proc.kill).toHaveBeenCalledWith("SIGTERM");
    });

    it("does not remove recent sessions", () => {
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      mgr.cleanup();
      expect(mgr.list()).toHaveLength(1);
    });
  });

  // ── resolveCliCommand (via spawn behavior) ─────────────────────────────

  describe("resolveCliCommand routing", () => {
    it("routes cli-gemini/ to 'gemini' command", () => {
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "test" }]);
      expect(mockSpawn).toHaveBeenCalledWith(
        "gemini",
        expect.arrayContaining(["-m", "gemini-2.5-pro"]),
        expect.any(Object)
      );
    });

    it("routes cli-claude/ to 'claude' command", () => {
      mgr.spawn("cli-claude/claude-sonnet-4-6", [{ role: "user", content: "test" }]);
      expect(mockSpawn).toHaveBeenCalledWith(
        "claude",
        expect.arrayContaining(["--model", "claude-sonnet-4-6"]),
        expect.any(Object)
      );
    });

    it("routes openai-codex/ to 'codex' command", () => {
      mgr.spawn("openai-codex/gpt-5.3-codex", [{ role: "user", content: "test" }]);
      expect(mockSpawn).toHaveBeenCalledWith(
        "codex",
        expect.arrayContaining(["--model", "gpt-5.3-codex"]),
        expect.any(Object)
      );
    });

    it("routes opencode/ to 'opencode' command", () => {
      mgr.spawn("opencode/default", [{ role: "user", content: "test" }]);
      expect(mockSpawn).toHaveBeenCalledWith(
        "opencode",
        expect.arrayContaining(["run"]),
        expect.any(Object)
      );
    });

    it("routes pi/ to 'pi' command", () => {
      mgr.spawn("pi/default", [{ role: "user", content: "test" }]);
      expect(mockSpawn).toHaveBeenCalledWith(
        "pi",
        expect.arrayContaining(["-p"]),
        expect.any(Object)
      );
    });

    it("passes workdir option as cwd", () => {
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "test" }], { workdir: "/tmp/test" });
      expect(mockSpawn).toHaveBeenCalledWith(
        "gemini",
        expect.any(Array),
        expect.objectContaining({ cwd: "/tmp/test" })
      );
    });
  });

  // ── process error handling ─────────────────────────────────────────────

  describe("process error handling", () => {
    it("marks session as exited on process error", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      latestProcRef.current._emit("error", new Error("spawn ENOENT"));
      const result = mgr.poll(id);
      expect(result!.running).toBe(false);
      expect(result!.status).toBe("exited");
      expect(result!.exitCode).toBe(1);
    });
  });

  // ── stop() ─────────────────────────────────────────────────────────────

  describe("stop()", () => {
    it("kills all running sessions", () => {
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "a" }]);
      const proc1 = latestProcRef.current;
      mgr.spawn("cli-claude/claude-sonnet-4-6", [{ role: "user", content: "b" }]);
      const proc2 = latestProcRef.current;

      mgr.stop();

      expect(proc1.kill).toHaveBeenCalledWith("SIGTERM");
      expect(proc2.kill).toHaveBeenCalledWith("SIGTERM");
    });

    it("cleans up isolated workdirs on stop", () => {
      mockCleanupWorkdir.mockClear();
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "a" }], { isolateWorkdir: true });

      mgr.stop();

      expect(mockCleanupWorkdir).toHaveBeenCalledWith("/tmp/cli-bridge-fake123");
    });
  });

  // ── workdir isolation (Issue #6) ───────────────────────────────────────

  describe("workdir isolation", () => {
    beforeEach(() => {
      mockCreateIsolatedWorkdir.mockClear();
      mockCleanupWorkdir.mockClear();
      mockSweepOrphanedWorkdirs.mockClear();
    });

    it("creates an isolated workdir when isolateWorkdir is true", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }], { isolateWorkdir: true });
      expect(mockCreateIsolatedWorkdir).toHaveBeenCalledTimes(1);

      // The session should use the created workdir as cwd
      expect(mockSpawn).toHaveBeenCalledWith(
        "gemini",
        expect.any(Array),
        expect.objectContaining({ cwd: "/tmp/cli-bridge-fake123" })
      );

      // Session info should include the isolated workdir
      const list = mgr.list();
      const session = list.find(s => s.sessionId === id);
      expect(session?.isolatedWorkdir).toBe("/tmp/cli-bridge-fake123");
    });

    it("does not create isolated workdir when isolateWorkdir is false", () => {
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      expect(mockCreateIsolatedWorkdir).not.toHaveBeenCalled();
    });

    it("does not create isolated workdir when explicit workdir is provided", () => {
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }], {
        isolateWorkdir: true,
        workdir: "/explicit/dir",
      });
      expect(mockCreateIsolatedWorkdir).not.toHaveBeenCalled();

      // Should use the explicit workdir
      expect(mockSpawn).toHaveBeenCalledWith(
        "gemini",
        expect.any(Array),
        expect.objectContaining({ cwd: "/explicit/dir" })
      );
    });

    it("cleans up isolated workdir when process exits", () => {
      mockCleanupWorkdir.mockClear();
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }], { isolateWorkdir: true });

      // Simulate process exit
      latestProcRef.current._emit("close", 0);

      expect(mockCleanupWorkdir).toHaveBeenCalledWith("/tmp/cli-bridge-fake123");
    });

    it("cleans up isolated workdir on process error", () => {
      mockCleanupWorkdir.mockClear();
      mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }], { isolateWorkdir: true });

      // Simulate process error
      latestProcRef.current._emit("error", new Error("spawn ENOENT"));

      expect(mockCleanupWorkdir).toHaveBeenCalledWith("/tmp/cli-bridge-fake123");
    });

    it("cleans up isolated workdir during cleanup sweep", () => {
      mockCleanupWorkdir.mockClear();
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }], { isolateWorkdir: true });

      // Make the session old enough for cleanup
      const sessions = (mgr as any).sessions as Map<string, any>;
      sessions.get(id)!.startTime = Date.now() - 31 * 60 * 1000;

      mgr.cleanup();

      expect(mockCleanupWorkdir).toHaveBeenCalledWith("/tmp/cli-bridge-fake123");
      expect(mockSweepOrphanedWorkdirs).toHaveBeenCalled();
    });

    it("session without isolation has null isolatedWorkdir", () => {
      const id = mgr.spawn("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }]);
      const list = mgr.list();
      const session = list.find(s => s.sessionId === id);
      expect(session?.isolatedWorkdir).toBeNull();
    });
  });
});
