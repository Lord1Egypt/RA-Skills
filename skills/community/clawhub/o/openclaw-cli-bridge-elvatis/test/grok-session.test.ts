/**
 * test/session.test.ts
 *
 * Unit tests for grok-session.ts — persistence, age check, cookie handling.
 * No browser needed (mocked).
 */

import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { existsSync, unlinkSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  loadSession,
  saveSession,
  isSessionExpiredByAge,
  type GrokSession,
} from "../src/grok-session.js";

const TMP_SESSION = join(tmpdir(), `grok-test-session-${process.pid}.json`);

const MOCK_SESSION: GrokSession = {
  cookies: [
    {
      name: "auth_token",
      value: "test-token-123",
      domain: ".grok.com",
      path: "/",
      expires: Date.now() / 1000 + 86400,
      httpOnly: true,
      secure: true,
      sameSite: "Lax",
    },
    {
      name: "ct0",
      value: "csrf-token-abc",
      domain: ".x.com",
      path: "/",
      expires: Date.now() / 1000 + 86400,
      httpOnly: false,
      secure: true,
      sameSite: "Lax",
    },
  ],
  savedAt: Date.now(),
  userAgent: "Mozilla/5.0 (test)",
};

describe("grok-session persistence", () => {
  afterEach(() => {
    if (existsSync(TMP_SESSION)) unlinkSync(TMP_SESSION);
  });

  it("returns null when file does not exist", () => {
    const result = loadSession(TMP_SESSION);
    expect(result).toBeNull();
  });

  it("saves and loads a session round-trip", () => {
    saveSession(TMP_SESSION, MOCK_SESSION);
    expect(existsSync(TMP_SESSION)).toBe(true);

    const loaded = loadSession(TMP_SESSION);
    expect(loaded).not.toBeNull();
    expect(loaded!.cookies).toHaveLength(2);
    expect(loaded!.cookies[0].name).toBe("auth_token");
    expect(loaded!.cookies[0].value).toBe("test-token-123");
    expect(loaded!.userAgent).toBe("Mozilla/5.0 (test)");
  });

  it("returns null for corrupted JSON", () => {
    const { writeFileSync } = require("node:fs");
    writeFileSync(TMP_SESSION, "{ bad json }", "utf-8");
    const result = loadSession(TMP_SESSION);
    expect(result).toBeNull();
  });

  it("returns null for missing cookies field", () => {
    const { writeFileSync } = require("node:fs");
    writeFileSync(TMP_SESSION, JSON.stringify({ savedAt: Date.now() }), "utf-8");
    const result = loadSession(TMP_SESSION);
    expect(result).toBeNull();
  });

  it("returns null for cookies field not being array", () => {
    const { writeFileSync } = require("node:fs");
    writeFileSync(TMP_SESSION, JSON.stringify({ cookies: "not-array", savedAt: Date.now() }), "utf-8");
    const result = loadSession(TMP_SESSION);
    expect(result).toBeNull();
  });

  it("saves valid JSON that can be parsed independently", () => {
    saveSession(TMP_SESSION, MOCK_SESSION);
    const raw = readFileSync(TMP_SESSION, "utf-8");
    expect(() => JSON.parse(raw)).not.toThrow();
    const parsed = JSON.parse(raw);
    expect(parsed.savedAt).toBeTypeOf("number");
  });

  it("overwrites existing session file", () => {
    saveSession(TMP_SESSION, MOCK_SESSION);

    const updated: GrokSession = { ...MOCK_SESSION, userAgent: "updated-ua", savedAt: Date.now() };
    saveSession(TMP_SESSION, updated);

    const loaded = loadSession(TMP_SESSION);
    expect(loaded!.userAgent).toBe("updated-ua");
  });
});

describe("session age check", () => {
  it("fresh session is not expired", () => {
    const session: GrokSession = { ...MOCK_SESSION, savedAt: Date.now() };
    expect(isSessionExpiredByAge(session)).toBe(false);
  });

  it("session saved 6 days ago is not expired", () => {
    const sixDaysAgo = Date.now() - 6 * 24 * 60 * 60 * 1000;
    const session: GrokSession = { ...MOCK_SESSION, savedAt: sixDaysAgo };
    expect(isSessionExpiredByAge(session)).toBe(false);
  });

  it("session saved 8 days ago is expired", () => {
    const eightDaysAgo = Date.now() - 8 * 24 * 60 * 60 * 1000;
    const session: GrokSession = { ...MOCK_SESSION, savedAt: eightDaysAgo };
    expect(isSessionExpiredByAge(session)).toBe(true);
  });

  it("session saved exactly 7 days ago is expired", () => {
    const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000 - 1;
    const session: GrokSession = { ...MOCK_SESSION, savedAt: sevenDaysAgo };
    expect(isSessionExpiredByAge(session)).toBe(true);
  });
});
