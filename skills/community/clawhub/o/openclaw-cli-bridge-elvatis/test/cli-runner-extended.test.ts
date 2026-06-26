/**
 * Extended CLI runner tests for new runners: Codex, OpenCode, Pi.
 *
 * Mocks child_process.spawn so no real CLIs are executed.
 * Tests argument construction, routing, and workdir handling.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { EventEmitter } from "node:events";
import { spawn, execSync } from "node:child_process";

// ── Mock child_process ──────────────────────────────────────────────────────

function makeFakeProc(stdoutData = "", exitCode = 0) {
  const proc = new EventEmitter() as any;
  const stdout = new EventEmitter();
  const stderr = new EventEmitter();
  proc.stdout = stdout;
  proc.stderr = stderr;
  proc.stdin = {
    write: vi.fn((_data: string, _enc: string, cb?: () => void) => { cb?.(); }),
    end: vi.fn(),
  };
  proc.kill = vi.fn();
  proc.pid = 99999;

  // Auto-emit data + close on next tick (simulates CLI finishing)
  setTimeout(() => {
    if (stdoutData) stdout.emit("data", Buffer.from(stdoutData));
    proc.emit("close", exitCode);
  }, 5);

  return proc;
}

// Use vi.hoisted to declare mock variables that can be referenced in vi.mock factories
const { mockSpawn, mockExecSync, existsSyncRef } = vi.hoisted(() => ({
  mockSpawn: vi.fn(),
  mockExecSync: vi.fn(),
  existsSyncRef: { value: true },
}));

vi.mock("node:child_process", async (importOriginal) => {
  const orig = await importOriginal<typeof import("node:child_process")>();
  return { ...orig, spawn: mockSpawn, execSync: mockExecSync };
});

vi.mock("node:fs", async (importOriginal) => {
  const orig = await importOriginal<typeof import("node:fs")>();
  return {
    ...orig,
    existsSync: vi.fn((...args: unknown[]) => {
      const path = args[0] as string;
      if (path.endsWith(".git")) return existsSyncRef.value;
      return orig.existsSync(path);
    }),
  };
});

// Mock claude-auth
vi.mock("../src/claude-auth.js", () => ({
  ensureClaudeToken: vi.fn(async () => {}),
  refreshClaudeToken: vi.fn(async () => {}),
  scheduleTokenRefresh: vi.fn(async () => {}),
  stopTokenRefresh: vi.fn(),
  setAuthLogger: vi.fn(),
}));

import {
  runCodex,
  runOpenCode,
  runPi,
  routeToCliRunner,
} from "../src/cli-runner.js";

// ──────────────────────────────────────────────────────────────────────────────

describe("runCodex()", () => {
  beforeEach(() => {
    mockSpawn.mockImplementation(() => makeFakeProc("codex result", 0));
    existsSyncRef.value = true;
    mockExecSync.mockClear();
  });

  it("constructs correct args and returns output", async () => {
    const result = await runCodex("hello", "openai-codex/gpt-5.3-codex", 5000);
    expect(result).toBe("codex result");
    expect(mockSpawn).toHaveBeenCalledWith(
      "codex",
      ["exec", "--model", "gpt-5.3-codex", "--full-auto"],
      expect.any(Object)
    );
  });

  it("strips model prefix correctly", async () => {
    await runCodex("test", "openai-codex/gpt-5.4", 5000);
    expect(mockSpawn).toHaveBeenCalledWith(
      "codex",
      expect.arrayContaining(["--model", "gpt-5.4"]),
      expect.any(Object)
    );
  });

  it("passes workdir as cwd", async () => {
    await runCodex("test", "openai-codex/gpt-5.3-codex", 5000, "/my/workdir");
    expect(mockSpawn).toHaveBeenCalledWith(
      "codex",
      expect.any(Array),
      expect.objectContaining({ cwd: "/my/workdir" })
    );
  });

  it("auto-initializes git when workdir has no .git", async () => {
    existsSyncRef.value = false;
    await runCodex("test", "openai-codex/gpt-5.3-codex", 5000, "/no-git");
    expect(mockExecSync).toHaveBeenCalledWith("git init", expect.objectContaining({ cwd: "/no-git" }));
  });

  it("does not run git init when .git exists", async () => {
    existsSyncRef.value = true;
    await runCodex("test", "openai-codex/gpt-5.3-codex", 5000, "/has-git");
    expect(mockExecSync).not.toHaveBeenCalled();
  });
});

describe("runOpenCode()", () => {
  beforeEach(() => {
    mockSpawn.mockImplementation(() => makeFakeProc("opencode result", 0));
  });

  it("constructs correct args with prompt as CLI argument", async () => {
    const result = await runOpenCode("hello world", "opencode/default", 5000);
    expect(result).toBe("opencode result");
    expect(mockSpawn).toHaveBeenCalledWith(
      "opencode",
      ["run", "hello world"],
      expect.any(Object)
    );
  });

  it("passes workdir as cwd", async () => {
    await runOpenCode("test", "opencode/default", 5000, "/my/dir");
    expect(mockSpawn).toHaveBeenCalledWith(
      "opencode",
      expect.any(Array),
      expect.objectContaining({ cwd: "/my/dir" })
    );
  });
});

describe("runPi()", () => {
  beforeEach(() => {
    mockSpawn.mockImplementation(() => makeFakeProc("pi result", 0));
  });

  it("constructs correct args with prompt as -p flag", async () => {
    const result = await runPi("hello world", "pi/default", 5000);
    expect(result).toBe("pi result");
    expect(mockSpawn).toHaveBeenCalledWith(
      "pi",
      ["-p", "hello world"],
      expect.any(Object)
    );
  });

  it("passes workdir as cwd", async () => {
    await runPi("test", "pi/default", 5000, "/pi/workdir");
    expect(mockSpawn).toHaveBeenCalledWith(
      "pi",
      expect.any(Array),
      expect.objectContaining({ cwd: "/pi/workdir" })
    );
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// routeToCliRunner — new model prefix routing
// ──────────────────────────────────────────────────────────────────────────────

describe("routeToCliRunner — new model prefixes", () => {
  beforeEach(() => {
    mockSpawn.mockImplementation(() => makeFakeProc("routed output", 0));
    existsSyncRef.value = true;
  });

  it("routes openai-codex/* to runCodex", async () => {
    const result = await routeToCliRunner(
      "openai-codex/gpt-5.3-codex",
      [{ role: "user", content: "hi" }],
      5000
    );
    expect(result).toEqual({ content: "routed output" });
    expect(mockSpawn).toHaveBeenCalledWith("codex", expect.any(Array), expect.any(Object));
  });

  it("routes vllm/openai-codex/* to runCodex (strips vllm prefix)", async () => {
    const result = await routeToCliRunner(
      "vllm/openai-codex/gpt-5.3-codex",
      [{ role: "user", content: "hi" }],
      5000,
      { allowedModels: null }
    );
    expect(result).toEqual({ content: "routed output" });
    expect(mockSpawn).toHaveBeenCalledWith("codex", expect.any(Array), expect.any(Object));
  });

  it("routes opencode/* to runOpenCode", async () => {
    const result = await routeToCliRunner(
      "opencode/default",
      [{ role: "user", content: "hi" }],
      5000
    );
    expect(result).toEqual({ content: "routed output" });
    expect(mockSpawn).toHaveBeenCalledWith("opencode", expect.any(Array), expect.any(Object));
  });

  it("routes pi/* to runPi", async () => {
    const result = await routeToCliRunner(
      "pi/default",
      [{ role: "user", content: "hi" }],
      5000
    );
    expect(result).toEqual({ content: "routed output" });
    expect(mockSpawn).toHaveBeenCalledWith("pi", expect.any(Array), expect.any(Object));
  });

  it("passes workdir option through to the runner cwd", async () => {
    await routeToCliRunner(
      "openai-codex/gpt-5.3-codex",
      [{ role: "user", content: "hi" }],
      5000,
      { workdir: "/custom/dir" }
    );
    expect(mockSpawn).toHaveBeenCalledWith(
      "codex",
      expect.any(Array),
      expect.objectContaining({ cwd: "/custom/dir" })
    );
  });

  it("rejects unknown model prefix", async () => {
    await expect(
      routeToCliRunner("unknown/model", [{ role: "user", content: "hi" }], 5000, { allowedModels: null })
    ).rejects.toThrow("Unknown CLI bridge model");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Codex auto-git-init via routeToCliRunner
// ──────────────────────────────────────────────────────────────────────────────

describe("Codex auto-git-init via routeToCliRunner", () => {
  it("calls git init when workdir has no .git directory", async () => {
    existsSyncRef.value = false;
    mockSpawn.mockImplementation(() => makeFakeProc("codex output", 0));
    mockExecSync.mockClear();

    await routeToCliRunner(
      "openai-codex/gpt-5.3-codex",
      [{ role: "user", content: "hi" }],
      5000,
      { workdir: "/no-git-dir" }
    );

    expect(mockExecSync).toHaveBeenCalledWith("git init", expect.objectContaining({ cwd: "/no-git-dir" }));
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Timeout handling: graceful SIGTERM → SIGKILL and exit 143 annotation
// ──────────────────────────────────────────────────────────────────────────────

import { runCli, annotateExitError } from "../src/cli-runner.js";

describe("runCli() timeout handling", () => {
  it("does NOT pass timeout to spawn options (manual timer instead)", async () => {
    mockSpawn.mockImplementation(() => makeFakeProc("ok", 0));
    await runCli("echo", [], "hello", 60_000);
    const spawnOpts = mockSpawn.mock.calls[0][2];
    expect(spawnOpts.timeout).toBeUndefined();
  });

  it("sends SIGTERM after timeout fires", async () => {
    vi.useFakeTimers();
    const proc = new EventEmitter() as any;
    proc.stdout = new EventEmitter();
    proc.stderr = new EventEmitter();
    proc.stdin = { write: vi.fn((_d: string, _e: string, cb?: () => void) => { cb?.(); }), end: vi.fn() };
    proc.kill = vi.fn(() => { proc.emit("close", 143); });
    proc.killed = false;
    mockSpawn.mockImplementation(() => proc);

    const logMessages: string[] = [];
    const promise = runCli("claude", [], "prompt", 100, { log: (m) => logMessages.push(m) });

    // Advance past the timeout
    vi.advanceTimersByTime(101);

    const result = await promise;
    expect(proc.kill).toHaveBeenCalledWith("SIGTERM");
    expect(result.timedOut).toBe(true);
    expect(result.exitCode).toBe(143);
    expect(logMessages.some(m => m.includes("timeout") && m.includes("SIGTERM"))).toBe(true);
    vi.useRealTimers();
  });

  it("sets timedOut=false for normal exits", async () => {
    mockSpawn.mockImplementation(() => makeFakeProc("output", 0));
    const result = await runCli("echo", [], "hello", 60_000);
    expect(result.timedOut).toBe(false);
    expect(result.exitCode).toBe(0);
  });
});

describe("annotateExitError()", () => {
  it("annotates exit 143 as timeout", () => {
    const msg = annotateExitError(143, "(no output)", false, "cli-claude/claude-sonnet-4-6");
    expect(msg).toContain("timeout");
    expect(msg).toContain("supervisor");
    expect(msg).toContain("cli-claude/claude-sonnet-4-6");
  });

  it("annotates when timedOut is true regardless of exit code", () => {
    const msg = annotateExitError(1, "some error", true, "cli-claude/claude-sonnet-4-6");
    expect(msg).toContain("timeout");
    expect(msg).toContain("supervisor");
  });

  it("returns plain error when not a timeout", () => {
    const msg = annotateExitError(1, "auth error", false, "cli-claude/claude-sonnet-4-6");
    expect(msg).toBe("auth error");
    expect(msg).not.toContain("timeout");
  });

  it("returns (no output) placeholder when stderr is empty and not a timeout", () => {
    const msg = annotateExitError(1, "", false, "cli-claude/claude-sonnet-4-6");
    expect(msg).toBe("(no output)");
  });
});
