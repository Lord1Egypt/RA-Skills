/**
 * Tests for cookie expiry formatting helpers.
 */

import { describe, it, expect, vi, afterEach } from "vitest";
import {
  formatExpiryInfo,
  formatGeminiExpiry,
  formatClaudeExpiry,
  formatChatGPTExpiry,
  type ExpiryInfo,
} from "../src/expiry-helpers.js";

// Fix Date.now() for deterministic tests
const NOW = new Date("2026-03-13T12:00:00Z").getTime();

afterEach(() => {
  vi.restoreAllMocks();
});

function makeExpiry(daysFromNow: number): ExpiryInfo {
  return {
    expiresAt: NOW + daysFromNow * 86_400_000,
    loginAt: NOW - 86_400_000,
    cookieName: "test-cookie",
  };
}

// ──────────────────────────────────────────────────────────────────────────────
// formatExpiryInfo (Grok)
// ──────────────────────────────────────────────────────────────────────────────

describe("formatExpiryInfo (Grok)", () => {
  it("expired → contains EXPIRED", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatExpiryInfo(makeExpiry(-5));
    expect(result).toContain("EXPIRED");
  });

  it("3 days → contains 🚨", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatExpiryInfo(makeExpiry(3));
    expect(result).toContain("🚨");
    expect(result).toContain("3d");
  });

  it("20 days → contains ✅", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatExpiryInfo(makeExpiry(20));
    expect(result).toContain("✅");
    expect(result).toContain("20");
  });

  it("10 days → contains ⚠️ (warning zone 7-14d)", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatExpiryInfo(makeExpiry(10));
    expect(result).toContain("⚠️");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// formatGeminiExpiry
// ──────────────────────────────────────────────────────────────────────────────

describe("formatGeminiExpiry", () => {
  it("expired → contains EXPIRED", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatGeminiExpiry(makeExpiry(-2));
    expect(result).toContain("EXPIRED");
    expect(result).toContain("/gemini-login");
  });

  it("3 days → contains 🚨", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatGeminiExpiry(makeExpiry(3));
    expect(result).toContain("🚨");
  });

  it("20 days → contains ✅", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatGeminiExpiry(makeExpiry(20));
    expect(result).toContain("✅");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// formatClaudeExpiry
// ──────────────────────────────────────────────────────────────────────────────

describe("formatClaudeExpiry", () => {
  it("expired → contains EXPIRED", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatClaudeExpiry(makeExpiry(-1));
    expect(result).toContain("EXPIRED");
    expect(result).toContain("/claude-login");
  });

  it("3 days → contains 🚨", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatClaudeExpiry(makeExpiry(3));
    expect(result).toContain("🚨");
  });

  it("20 days → contains ✅", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatClaudeExpiry(makeExpiry(20));
    expect(result).toContain("✅");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// formatChatGPTExpiry
// ──────────────────────────────────────────────────────────────────────────────

describe("formatChatGPTExpiry", () => {
  it("expired → contains EXPIRED", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatChatGPTExpiry(makeExpiry(-3));
    expect(result).toContain("EXPIRED");
    expect(result).toContain("/chatgpt-login");
  });

  it("3 days → contains 🚨", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatChatGPTExpiry(makeExpiry(3));
    expect(result).toContain("🚨");
  });

  it("20 days → contains ✅", () => {
    vi.spyOn(Date, "now").mockReturnValue(NOW);
    const result = formatChatGPTExpiry(makeExpiry(20));
    expect(result).toContain("✅");
  });
});
