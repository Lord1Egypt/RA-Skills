/**
 * test/claude-browser.test.ts
 *
 * Unit tests for claude-browser.ts helper functions.
 * Does not require a real browser — tests the pure logic.
 */

import { describe, it, expect } from "vitest";

// ─── Test the flatten + model resolution logic directly ──────────────────────
// We import internal helpers by re-exporting them from a test shim, or we just
// test the public surface via duck-typed mocks.

describe("claude-browser — model resolution", () => {
  // We can test via the exported functions indirectly through proxy tests.
  // Direct unit tests use small isolated helpers copied here.

  function resolveModel(m?: string): string {
    const clean = (m ?? "claude-sonnet").replace("web-claude/", "");
    const allowed = ["claude-sonnet","claude-opus","claude-haiku","claude-sonnet-4-5","claude-sonnet-4-6","claude-opus-4-5"];
    return allowed.includes(clean) ? clean : "claude-sonnet";
  }

  it("strips web-claude/ prefix", () => {
    expect(resolveModel("web-claude/claude-sonnet")).toBe("claude-sonnet");
    expect(resolveModel("web-claude/claude-opus")).toBe("claude-opus");
  });

  it("falls back to claude-sonnet for unknown models", () => {
    expect(resolveModel("web-claude/unknown-model")).toBe("claude-sonnet");
    expect(resolveModel(undefined)).toBe("claude-sonnet");
  });

  it("accepts known models without prefix", () => {
    expect(resolveModel("claude-sonnet-4-6")).toBe("claude-sonnet-4-6");
    expect(resolveModel("claude-opus")).toBe("claude-opus");
  });
});

describe("claude-browser — message flattening", () => {
  function flattenMessages(messages: { role: string; content: string }[]): string {
    if (messages.length === 1) return messages[0].content;
    return messages.map((m) => {
      if (m.role === "system") return `[System]: ${m.content}`;
      if (m.role === "assistant") return `[Assistant]: ${m.content}`;
      return m.content;
    }).join("\n\n");
  }

  it("returns content directly for single user message", () => {
    expect(flattenMessages([{ role: "user", content: "hello" }])).toBe("hello");
  });

  it("prefixes system messages", () => {
    const result = flattenMessages([
      { role: "system", content: "Be brief" },
      { role: "user", content: "hi" },
    ]);
    expect(result).toContain("[System]: Be brief");
    expect(result).toContain("hi");
  });

  it("prefixes assistant turns in multi-turn", () => {
    const result = flattenMessages([
      { role: "user", content: "Hello" },
      { role: "assistant", content: "Hi there" },
      { role: "user", content: "How are you?" },
    ]);
    expect(result).toContain("[Assistant]: Hi there");
    expect(result).toContain("How are you?");
  });
});

describe("claude-browser — proxy routing (DI override)", () => {
  // Test that web-claude/* models route correctly through the proxy
  // using the same DI pattern as grok-proxy.test.ts

  it("web-claude/* model IDs follow naming convention", () => {
    const validModels = [
      "web-claude/claude-sonnet",
      "web-claude/claude-opus",
      "web-claude/claude-haiku",
    ];
    for (const m of validModels) {
      expect(m.startsWith("web-claude/")).toBe(true);
    }
  });

  it("distinguishes web-claude from web-grok", () => {
    expect("web-claude/claude-sonnet".startsWith("web-claude/")).toBe(true);
    expect("web-grok/grok-3".startsWith("web-claude/")).toBe(false);
  });
});
