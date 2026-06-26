/**
 * Tests for the centralized config module.
 * No mocks — tests the real exported values.
 */

import { describe, it, expect } from "vitest";
import {
  DEFAULT_PROXY_PORT,
  DEFAULT_PROXY_API_KEY,
  DEFAULT_PROXY_TIMEOUT_MS,
  DEFAULT_CLI_TIMEOUT_MS,
  TIMEOUT_GRACE_MS,
  MAX_MESSAGES,
  MAX_MSG_CHARS,
  SESSION_TTL_MS,
  CLEANUP_INTERVAL_MS,
  SESSION_KILL_GRACE_MS,
  DEFAULT_MODEL_TIMEOUTS,
  DEFAULT_MODEL_FALLBACKS,
  OPENCLAW_DIR,
  CLI_TEST_DEFAULT_MODEL,
  MAX_EFFECTIVE_TIMEOUT_MS,
  TIMEOUT_PER_EXTRA_MSG_MS,
  TIMEOUT_PER_TOOL_MS,
  PROVIDER_SESSION_TTL_MS,
  MEDIA_TMP_DIR,
  PROFILE_DIRS,
  STATE_FILE,
  PENDING_FILE,
  PROVIDER_SESSIONS_FILE,
  DEFAULT_BITNET_SERVER_URL,
  BITNET_MAX_MESSAGES,
  BITNET_SYSTEM_PROMPT,
} from "../src/config.js";

describe("config.ts exports", () => {
  it("exports sensible timeout defaults", () => {
    expect(DEFAULT_PROXY_TIMEOUT_MS).toBe(300_000);
    expect(DEFAULT_CLI_TIMEOUT_MS).toBe(120_000);
    expect(TIMEOUT_GRACE_MS).toBe(5_000);
    expect(MAX_EFFECTIVE_TIMEOUT_MS).toBe(900_000);
    expect(SESSION_TTL_MS).toBe(30 * 60 * 1000);
    expect(CLEANUP_INTERVAL_MS).toBe(5 * 60 * 1000);
    expect(SESSION_KILL_GRACE_MS).toBe(5_000);
    expect(PROVIDER_SESSION_TTL_MS).toBe(2 * 60 * 60 * 1000);
  });

  it("exports dynamic timeout scaling factors", () => {
    expect(TIMEOUT_PER_EXTRA_MSG_MS).toBe(2_000);
    expect(TIMEOUT_PER_TOOL_MS).toBe(7_000);
  });

  it("exports message limits", () => {
    expect(MAX_MESSAGES).toBe(20);
    expect(MAX_MSG_CHARS).toBe(4_000);
  });

  it("exports proxy defaults", () => {
    expect(DEFAULT_PROXY_PORT).toBe(31337);
    expect(DEFAULT_PROXY_API_KEY).toBe("cli-bridge");
  });

  it("exports per-model timeouts for all major models", () => {
    expect(DEFAULT_MODEL_TIMEOUTS["cli-claude/claude-opus-4-6"]).toBe(300_000);
    expect(DEFAULT_MODEL_TIMEOUTS["cli-claude/claude-sonnet-4-6"]).toBe(300_000);
    expect(DEFAULT_MODEL_TIMEOUTS["cli-claude/claude-haiku-4-5"]).toBe(90_000);
    expect(DEFAULT_MODEL_TIMEOUTS["cli-gemini/gemini-2.5-pro"]).toBe(300_000);
    expect(DEFAULT_MODEL_TIMEOUTS["cli-gemini/gemini-2.5-flash"]).toBe(180_000);
    expect(DEFAULT_MODEL_TIMEOUTS["openai-codex/gpt-5.4"]).toBe(300_000);
    expect(DEFAULT_MODEL_TIMEOUTS["gemini-api/gemini-2.5-pro"]).toBe(300_000);
    expect(DEFAULT_MODEL_TIMEOUTS["gemini-api/gemini-2.5-flash"]).toBe(180_000);
  });

  it("exports model fallback chains", () => {
    expect(DEFAULT_MODEL_FALLBACKS["cli-claude/claude-sonnet-4-6"]).toBe("cli-claude/claude-haiku-4-5");
    expect(DEFAULT_MODEL_FALLBACKS["cli-claude/claude-opus-4-6"]).toBe("cli-claude/claude-sonnet-4-6");
    expect(DEFAULT_MODEL_FALLBACKS["cli-gemini/gemini-2.5-pro"]).toBe("cli-gemini/gemini-2.5-flash");
    expect(DEFAULT_MODEL_FALLBACKS["gemini-api/gemini-2.5-pro"]).toBe("gemini-api/gemini-2.5-flash");
  });

  it("exports path constants rooted in ~/.openclaw", () => {
    expect(OPENCLAW_DIR).toContain(".openclaw");
    expect(STATE_FILE).toContain("cli-bridge-state.json");
    expect(PENDING_FILE).toContain("cli-bridge-pending.json");
    expect(PROVIDER_SESSIONS_FILE).toContain("sessions.json");
    expect(MEDIA_TMP_DIR).toContain("cli-bridge-media");
  });

  it("exports browser profile directories", () => {
    expect(PROFILE_DIRS.grok).toContain("grok-profile");
    expect(PROFILE_DIRS.gemini).toContain("gemini-profile");
    expect(PROFILE_DIRS.claude).toContain("claude-profile");
    expect(PROFILE_DIRS.chatgpt).toContain("chatgpt-profile");
  });

  it("exports BitNet defaults", () => {
    expect(DEFAULT_BITNET_SERVER_URL).toBe("http://127.0.0.1:8082");
    expect(BITNET_MAX_MESSAGES).toBe(6);
    expect(BITNET_SYSTEM_PROMPT).toContain("Akido");
  });

  it("exports CLI test default model", () => {
    expect(CLI_TEST_DEFAULT_MODEL).toBe("cli-claude/claude-sonnet-4-6");
  });
});
