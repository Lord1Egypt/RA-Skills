/**
 * Unit tests for Codex auth import (Issue #2).
 *
 * Uses real temp files instead of mocks for reliable FS testing.
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { writeFileSync, mkdirSync, readFileSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { importCodexAuth } from "../src/codex-auth-import.js";

const TEST_BASE = join(tmpdir(), `codex-import-test-${process.pid}`);
const CODEX_AUTH_PATH = join(TEST_BASE, "codex", "auth.json");
const AUTH_STORE_PATH = join(TEST_BASE, "openclaw", "auth-profiles.json");

function writeCodexAuth(data: Record<string, unknown>) {
  mkdirSync(join(TEST_BASE, "codex"), { recursive: true });
  writeFileSync(CODEX_AUTH_PATH, JSON.stringify(data));
}

function writeAuthStore(data: Record<string, unknown>) {
  mkdirSync(join(TEST_BASE, "openclaw"), { recursive: true });
  writeFileSync(AUTH_STORE_PATH, JSON.stringify(data, null, 4));
}

function readAuthStore(): Record<string, unknown> {
  return JSON.parse(readFileSync(AUTH_STORE_PATH, "utf8"));
}

beforeEach(() => {
  mkdirSync(TEST_BASE, { recursive: true });
});

afterEach(() => {
  try {
    rmSync(TEST_BASE, { recursive: true, force: true });
  } catch { /* ignore */ }
});

describe("importCodexAuth()", () => {
  it("imports Codex OAuth tokens into auth store", async () => {
    writeCodexAuth({
      auth_mode: "oauth",
      tokens: {
        access_token: "test-access-token",
        refresh_token: "test-refresh-token",
      },
      last_refresh: new Date().toISOString(),
    });

    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(true);
    expect(result.skipped).toBe(false);
    expect(result.error).toBeUndefined();

    const store = readAuthStore() as { profiles: Record<string, { access: string; refresh: string }> };
    expect(store.profiles["openai-codex:default"]).toBeDefined();
    expect(store.profiles["openai-codex:default"].access).toBe("test-access-token");
    expect(store.profiles["openai-codex:default"].refresh).toBe("test-refresh-token");
  });

  it("imports API key when OAuth tokens are not available", async () => {
    writeCodexAuth({
      auth_mode: "api-key",
      OPENAI_API_KEY: "sk-test-key-123",
    });

    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(true);
    const store = readAuthStore() as { profiles: Record<string, { access: string }> };
    expect(store.profiles["openai-codex:default"].access).toBe("sk-test-key-123");
  });

  it("creates auth store directory if it does not exist", async () => {
    writeCodexAuth({
      auth_mode: "oauth",
      tokens: { access_token: "new-token" },
    });

    const deepStorePath = join(TEST_BASE, "deep", "nested", "auth-profiles.json");
    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: deepStorePath,
    });

    expect(result.imported).toBe(true);
    expect(existsSync(deepStorePath)).toBe(true);
  });

  it("preserves existing profiles in auth store", async () => {
    writeCodexAuth({
      auth_mode: "oauth",
      tokens: { access_token: "codex-token" },
    });
    writeAuthStore({
      version: 1,
      profiles: {
        "anthropic:default": {
          type: "token",
          provider: "anthropic",
          token: "sk-ant-test",
        },
      },
    });

    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(true);
    const store = readAuthStore() as { profiles: Record<string, { token?: string; access?: string }> };
    // Codex profile added
    expect(store.profiles["openai-codex:default"].access).toBe("codex-token");
    // Anthropic profile preserved
    expect(store.profiles["anthropic:default"].token).toBe("sk-ant-test");
  });

  it("skips import when tokens are already up-to-date", async () => {
    writeCodexAuth({
      auth_mode: "oauth",
      tokens: { access_token: "same-token", refresh_token: "same-refresh" },
    });
    writeAuthStore({
      version: 1,
      profiles: {
        "openai-codex:default": {
          type: "oauth",
          provider: "openai-codex",
          access: "same-token",
          refresh: "same-refresh",
        },
      },
    });

    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(false);
    expect(result.skipped).toBe(true);
  });

  it("updates when access token has changed", async () => {
    writeCodexAuth({
      auth_mode: "oauth",
      tokens: { access_token: "new-token", refresh_token: "new-refresh" },
    });
    writeAuthStore({
      version: 1,
      profiles: {
        "openai-codex:default": {
          type: "oauth",
          provider: "openai-codex",
          access: "old-token",
          refresh: "old-refresh",
        },
      },
    });

    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(true);
    const store = readAuthStore() as { profiles: Record<string, { access: string }> };
    expect(store.profiles["openai-codex:default"].access).toBe("new-token");
  });

  it("returns error when codex auth file does not exist", async () => {
    const result = await importCodexAuth({
      codexAuthPath: join(TEST_BASE, "nonexistent", "auth.json"),
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(false);
    expect(result.skipped).toBe(false);
    expect(result.error).toContain("Cannot read Codex auth file");
  });

  it("returns error when codex auth has no token", async () => {
    writeCodexAuth({
      auth_mode: "oauth",
      // No tokens, no API key
    });

    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(false);
    expect(result.error).toContain("No access token found");
  });

  it("includes expiry when last_refresh is present", async () => {
    const now = new Date();
    writeCodexAuth({
      auth_mode: "oauth",
      tokens: { access_token: "token-with-expiry" },
      last_refresh: now.toISOString(),
    });

    const result = await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
    });

    expect(result.imported).toBe(true);
    const store = readAuthStore() as { profiles: Record<string, { expires: number }> };
    const profile = store.profiles["openai-codex:default"];
    // Expiry should be ~1h after last_refresh
    expect(profile.expires).toBeGreaterThan(now.getTime());
    expect(profile.expires).toBeLessThanOrEqual(now.getTime() + 3600 * 1000 + 1000);
  });

  it("calls log function when provided", async () => {
    writeCodexAuth({
      auth_mode: "oauth",
      tokens: { access_token: "logged-token" },
    });

    const logs: string[] = [];
    await importCodexAuth({
      codexAuthPath: CODEX_AUTH_PATH,
      authStorePath: AUTH_STORE_PATH,
      log: (msg) => logs.push(msg),
    });

    expect(logs.length).toBeGreaterThan(0);
    expect(logs.some(l => l.includes("imported"))).toBe(true);
  });
});
