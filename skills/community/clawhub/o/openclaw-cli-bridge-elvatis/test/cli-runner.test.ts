import { describe, it, expect } from "vitest";
import {
  formatPrompt,
  routeToCliRunner,
  DEFAULT_ALLOWED_CLI_MODELS,
} from "../src/cli-runner.js";

// ──────────────────────────────────────────────────────────────────────────────
// formatPrompt
// ──────────────────────────────────────────────────────────────────────────────

describe("formatPrompt", () => {
  it("returns empty string for empty messages", () => {
    expect(formatPrompt([])).toBe("");
  });

  it("returns bare user text for a single short user message", () => {
    const result = formatPrompt([{ role: "user", content: "hello" }]);
    expect(result).toBe("hello");
  });

  it("truncates to MAX_MESSAGES (20) non-system messages", () => {
    const messages = Array.from({ length: 30 }, (_, i) => ({
      role: "user" as const,
      content: `msg ${i}`,
    }));
    const result = formatPrompt(messages);
    expect(result).toContain("msg 29");
    expect(result).not.toContain("msg 0\n");
    expect(result).toContain("[User]");
  });

  it("keeps system message + last 20 non-system messages", () => {
    const sys = { role: "system" as const, content: "You are helpful" };
    const msgs = Array.from({ length: 25 }, (_, i) => ({
      role: "user" as const,
      content: `msg ${i}`,
    }));
    const result = formatPrompt([sys, ...msgs]);
    expect(result).toContain("[System]");
    expect(result).toContain("You are helpful");
    expect(result).toContain("msg 24");
    expect(result).not.toContain("msg 0\n");
  });

  it("truncates individual message content at MAX_MSG_CHARS (4000)", () => {
    const longContent = "x".repeat(5000);
    const result = formatPrompt([{ role: "user", content: longContent }]);
    expect(result.length).toBeLessThan(5000);
    expect(result).toContain("truncated");
  });

  // T-101: additional formatPrompt cases

  it("formats a multi-turn user/assistant conversation with role labels", () => {
    const messages = [
      { role: "user" as const, content: "What is 2+2?" },
      { role: "assistant" as const, content: "4" },
      { role: "user" as const, content: "And 3+3?" },
    ];
    const result = formatPrompt(messages);
    expect(result).toContain("[User]\nWhat is 2+2?");
    expect(result).toContain("[Assistant]\n4");
    expect(result).toContain("[User]\nAnd 3+3?");
  });

  it("single assistant message gets role label (not bare)", () => {
    const result = formatPrompt([{ role: "assistant", content: "I am an assistant" }]);
    expect(result).toContain("[Assistant]");
  });

  it("content exactly at MAX_MSG_CHARS (4000) is NOT truncated", () => {
    const exact = "a".repeat(4000);
    const result = formatPrompt([{ role: "user", content: exact }]);
    expect(result).toBe(exact);
    expect(result).not.toContain("truncated");
  });

  it("content well above MAX_MSG_CHARS is truncated to a shorter result", () => {
    // Use 6000 chars — truncation suffix (~23 chars) + 4000 body = 4023, well below 6000
    const over = "a".repeat(6000);
    const result = formatPrompt([{ role: "user", content: over }]);
    expect(result).toContain("truncated");
    expect(result.length).toBeLessThan(over.length);
    expect(result.startsWith("a".repeat(4000))).toBe(true);
  });

  it("system-only message uses role label (not bare)", () => {
    const result = formatPrompt([{ role: "system", content: "Be concise" }]);
    expect(result).toContain("[System]");
    expect(result).toContain("Be concise");
  });

  it("system + single user message uses role labels (not bare)", () => {
    const result = formatPrompt([
      { role: "system", content: "Be concise" },
      { role: "user", content: "Hi" },
    ]);
    expect(result).toContain("[System]");
    expect(result).toContain("[User]");
  });

  // contentToString coercion tests (fix: [object Object] in WhatsApp group messages)
  it("coerces ContentPart array to plain text", () => {
    const result = formatPrompt([
      { role: "user", content: [{ type: "text", text: "Hello from WA group" }] },
    ]);
    expect(result).toBe("Hello from WA group");
    expect(result).not.toContain("[object Object]");
  });

  it("joins multiple text ContentParts with newline", () => {
    const result = formatPrompt([
      {
        role: "user",
        content: [
          { type: "text", text: "Part one" },
          { type: "text", text: "Part two" },
        ],
      },
    ]);
    expect(result).toContain("Part one");
    expect(result).toContain("Part two");
  });

  it("includes placeholder for non-text ContentParts (e.g. image)", () => {
    const result = formatPrompt([
      {
        role: "user",
        content: [
          { type: "image_url", url: "https://example.com/img.png" },
          { type: "text", text: "describe this" },
        ],
      },
    ]);
    expect(result).toContain("describe this");
    expect(result).toContain("[Attached image");
  });

  it("coerces plain object content to JSON string (not [object Object])", () => {
    const result = formatPrompt([
      { role: "user", content: { text: "structured", extra: 42 } as any },
    ]);
    expect(result).not.toBe("[object Object]");
    expect(result).toContain("structured");
  });

  it("handles null content gracefully", () => {
    const result = formatPrompt([{ role: "user", content: null as any }]);
    expect(result).toBe("");
  });

  it("handles undefined content gracefully", () => {
    const result = formatPrompt([{ role: "user", content: undefined as any }]);
    expect(result).toBe("");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// routeToCliRunner — model normalization + routing (T-101)
// ──────────────────────────────────────────────────────────────────────────────

describe("routeToCliRunner — model normalization", () => {
  it("rejects unknown model without vllm prefix", async () => {
    await expect(
      routeToCliRunner("unknown/model", [], 1000, { allowedModels: null })
    ).rejects.toThrow("Unknown CLI bridge model");
  });

  it("rejects unknown model with vllm prefix", async () => {
    await expect(
      routeToCliRunner("vllm/unknown/model", [], 1000, { allowedModels: null })
    ).rejects.toThrow("Unknown CLI bridge model");
  });

  it("accepts cli-claude/ without vllm prefix (calls runClaude path)", async () => {
    // Claude CLI may resolve (empty) or reject — what matters is it doesn't throw "Unknown CLI bridge model"
    let errorMsg = "";
    try {
      await routeToCliRunner("cli-claude/claude-sonnet-4-6", [{ role: "user", content: "hi" }], 500);
    } catch (e: any) {
      errorMsg = (e as Error).message ?? String(e);
    }
    expect(errorMsg).not.toContain("Unknown CLI bridge model");
    expect(errorMsg).not.toContain("CLI bridge model not allowed");
  });

  it("accepts vllm/cli-claude/ — strips vllm prefix before routing", async () => {
    let errorMsg = "";
    try {
      await routeToCliRunner("vllm/cli-claude/claude-sonnet-4-6", [{ role: "user", content: "hi" }], 500);
    } catch (e: any) {
      errorMsg = (e as Error).message ?? String(e);
    }
    expect(errorMsg).not.toContain("Unknown CLI bridge model");
    expect(errorMsg).not.toContain("CLI bridge model not allowed");
  });

  // T-101: gemini routing paths

  it("accepts cli-gemini/ without vllm prefix (routes to gemini, not 'unknown')", async () => {
    // gemini CLI may resolve or reject — what matters is it doesn't throw "Unknown CLI bridge model"
    let errorMsg = "";
    try {
      await routeToCliRunner("cli-gemini/gemini-2.5-pro", [{ role: "user", content: "hi" }], 500);
    } catch (e: any) {
      errorMsg = e?.message ?? "";
    }
    expect(errorMsg).not.toContain("Unknown CLI bridge model");
  });

  it("accepts vllm/cli-gemini/ — strips vllm prefix before routing", async () => {
    let errorMsg = "";
    try {
      await routeToCliRunner("vllm/cli-gemini/gemini-2.5-flash", [{ role: "user", content: "hi" }], 500);
    } catch (e: any) {
      errorMsg = e?.message ?? "";
    }
    expect(errorMsg).not.toContain("Unknown CLI bridge model");
  });

  it("rejects bare 'vllm/' with no type segment", async () => {
    await expect(
      routeToCliRunner("vllm/", [], 1000, { allowedModels: null })
    ).rejects.toThrow("Unknown CLI bridge model");
  });

  it("rejects empty model string", async () => {
    await expect(
      routeToCliRunner("", [], 1000, { allowedModels: null })
    ).rejects.toThrow("Unknown CLI bridge model");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// routeToCliRunner — model allowlist (T-103)
// ──────────────────────────────────────────────────────────────────────────────

describe("routeToCliRunner — model allowlist (T-103)", () => {
  it("DEFAULT_ALLOWED_CLI_MODELS includes all registered claude models", () => {
    expect(DEFAULT_ALLOWED_CLI_MODELS.has("cli-claude/claude-sonnet-4-6")).toBe(true);
    expect(DEFAULT_ALLOWED_CLI_MODELS.has("cli-claude/claude-opus-4-6")).toBe(true);
    expect(DEFAULT_ALLOWED_CLI_MODELS.has("cli-claude/claude-haiku-4-5")).toBe(true);
  });

  it("DEFAULT_ALLOWED_CLI_MODELS includes all registered gemini models", () => {
    expect(DEFAULT_ALLOWED_CLI_MODELS.has("cli-gemini/gemini-2.5-pro")).toBe(true);
    expect(DEFAULT_ALLOWED_CLI_MODELS.has("cli-gemini/gemini-2.5-flash")).toBe(true);
    expect(DEFAULT_ALLOWED_CLI_MODELS.has("cli-gemini/gemini-3-pro-preview")).toBe(true);
  });

  it("rejects a model not in the default allowlist", async () => {
    await expect(
      routeToCliRunner("vllm/cli-claude/claude-unknown-99", [{ role: "user", content: "hi" }], 500)
    ).rejects.toThrow("CLI bridge model not allowed");
  });

  it("rejects an unregistered gemini model", async () => {
    await expect(
      routeToCliRunner("vllm/cli-gemini/gemini-1.0-pro", [{ role: "user", content: "hi" }], 500)
    ).rejects.toThrow("CLI bridge model not allowed");
  });

  it("error message lists allowed models", async () => {
    try {
      await routeToCliRunner("vllm/cli-claude/bad-model", [{ role: "user", content: "hi" }], 500);
    } catch (e: any) {
      expect(e.message).toContain("cli-claude/claude-sonnet-4-6");
    }
  });

  it("allowedModels: null disables the check — only routing matters", async () => {
    // With null allowlist, the allowlist check is skipped — routing still happens
    // Claude CLI may resolve (empty) or reject for other reasons — should NOT throw "CLI bridge model not allowed"
    let errorMsg = "";
    try {
      await routeToCliRunner("vllm/cli-claude/any-model", [{ role: "user", content: "hi" }], 500, {
        allowedModels: null,
      });
    } catch (e: any) {
      errorMsg = (e as Error).message ?? String(e);
    }
    expect(errorMsg).not.toContain("CLI bridge model not allowed");
  });

  it("custom allowlist overrides defaults", async () => {
    const custom = new Set(["cli-claude/claude-sonnet-4-6"]);
    // claude-opus is in defaults but NOT in custom — should be rejected
    await expect(
      routeToCliRunner("vllm/cli-claude/claude-opus-4-6", [{ role: "user", content: "hi" }], 500, {
        allowedModels: custom,
      })
    ).rejects.toThrow("CLI bridge model not allowed");
  });
});
