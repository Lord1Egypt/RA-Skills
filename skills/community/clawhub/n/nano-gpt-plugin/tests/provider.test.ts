/**
 * NanoGPT Provider Plugin — Unit tests
 *
 * Tests the exported functions directly (no live OpenClaw instance needed).
 * Run: pnpm test
 */

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import plugin, {
  buildProvider,
  resolveDynamicModel,
  resolveUsageAuth,
  fetchUsageSnapshot,
  prepareExtraParams,
} from "../src/provider";

// ---------------------------------------------------------------------------
// Plugin export shape
// ---------------------------------------------------------------------------

describe("nano-gpt provider plugin", () => {
  it("should export a plugin object", () => {
    expect(plugin).toBeDefined();
    expect(typeof plugin).toBe("object");
  });

  it("should have id 'nano-gpt'", () => {
    expect(plugin.id).toBe("nano-gpt");
  });
});

// ---------------------------------------------------------------------------
// Static catalog — buildProvider
// ---------------------------------------------------------------------------

describe("buildProvider (Phase 1 — static catalog)", () => {
  it("returns a provider object with api and baseUrl", () => {
    const result = buildProvider();
    expect(result.api).toBe("openai-completions");
    expect(result.baseUrl).toBe("https://nano-gpt.com/api/v1");
  });

  it("returns 2 hardcoded models", () => {
    const result = buildProvider();
    expect(result.models).toHaveLength(2);
  });

  it("includes gpt-5.2 model with vision", () => {
    const result = buildProvider();
    const gpt = result.models.find((m) => m.id === "nano-gpt/openai/gpt-5.2");
    expect(gpt).toBeDefined();
    expect(gpt!.reasoning).toBe(false);
    expect(gpt!.input).toContain("image");
  });

  it("includes claude-opus-4.6 model with reasoning", () => {
    const result = buildProvider();
    const claude = result.models.find((m) => m.id === "nano-gpt/anthropic/claude-opus-4.6");
    expect(claude).toBeDefined();
    expect(claude!.reasoning).toBe(true);
    expect(claude!.input).toContain("image");
  });

  it("both models have correct cost and contextWindow", () => {
    const result = buildProvider();
    const gpt = result.models.find((m) => m.id === "nano-gpt/openai/gpt-5.2");
    expect(gpt!.cost.input).toBe(1.25);
    expect(gpt!.cost.output).toBe(10);
    expect(gpt!.contextWindow).toBe(128_000);
    expect(gpt!.maxTokens).toBe(32_768);
  });
});

// ---------------------------------------------------------------------------
// Dynamic model resolution — resolveDynamicModel
// ---------------------------------------------------------------------------

describe("resolveDynamicModel (Phase 3)", () => {
  it("returns correct shape for arbitrary model ID", () => {
    const model = resolveDynamicModel({ modelId: "nano-gpt/qwen/qwen3-coder" });
    expect(model.id).toBe("nano-gpt/qwen/qwen3-coder");
    expect(model.provider).toBe("nano-gpt");
    expect(model.api).toBe("openai-completions");
    expect(model.baseUrl).toBe("https://nano-gpt.com/api/v1");
  });

  it("strips leading nano-gpt/ prefix from name", () => {
    const model = resolveDynamicModel({ modelId: "nano-gpt/qwen/qwen3-coder" });
    expect(model.name).toBe("qwen/qwen3-coder");
  });

  it("defaults to text-only input", () => {
    const model = resolveDynamicModel({ modelId: "nano-gpt/qwen/qwen3-coder" });
    expect(model.input).toEqual(["text"]);
  });

  it("defaults reasoning to false for unknown models", () => {
    const model = resolveDynamicModel({ modelId: "nano-gpt/qwen/qwen3-coder" });
    expect(model.reasoning).toBe(false);
  });

  it("defaults to safe context window and maxTokens", () => {
    const model = resolveDynamicModel({ modelId: "nano-gpt/qwen/qwen3-coder" });
    expect(model.contextWindow).toBe(128_000);
    expect(model.maxTokens).toBe(8_192);
  });

  it("defaults cost to zero for unknown models", () => {
    const model = resolveDynamicModel({ modelId: "nano-gpt/qwen/qwen3-coder" });
    expect(model.cost.input).toBe(0);
    expect(model.cost.output).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// Usage auth — resolveUsageAuth
// ---------------------------------------------------------------------------

describe("resolveUsageAuth (Phase 4)", () => {
  it("returns token when API key is available", async () => {
    const result = await resolveUsageAuth({
      resolveApiKeyFromConfigAndStore: () => "test-key-123",
    });
    expect(result).toEqual({ token: "test-key-123" });
  });

  it("returns null when no API key", async () => {
    const result = await resolveUsageAuth({
      resolveApiKeyFromConfigAndStore: () => undefined,
    });
    expect(result).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// Usage snapshot — fetchUsageSnapshot (mocked network)
// ---------------------------------------------------------------------------

describe("fetchUsageSnapshot (mocked)", () => {
  const realFetch = globalThis.fetch;
  let mockFetch: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockFetch = vi.fn();
    globalThis.fetch = mockFetch;
  });

  afterEach(() => {
    globalThis.fetch = realFetch;
    vi.restoreAllMocks();
  });

  it("parses daily usage correctly", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          dailyInputTokens: { used: 1_000_000, limit: 10_000_000 },
        }),
    });
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ balance: 12.5 }),
    });

    const result = await fetchUsageSnapshot({ token: "test-key" });

    expect(result.period).toBe("daily");
    expect(result.used).toBe(1_000_000);
    expect(result.limit).toBe(10_000_000);
    expect(result.balanceUsd).toBe(12.5);
  });

  it("falls back to weekly when daily is absent", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          weeklyInputTokens: { used: 5_000_000, limit: 60_000_000 },
        }),
    });
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ balance: 0 }),
    });

    const result = await fetchUsageSnapshot({ token: "test-key" });

    expect(result.period).toBe("monthly");
    expect(result.used).toBe(5_000_000);
    expect(result.limit).toBe(60_000_000);
  });

  it("throws when usage API returns non-ok", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
    });
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ balance: 0 }),
    });

    await expect(fetchUsageSnapshot({ token: "bad-key" })).rejects.toThrow(
      "Usage API 401"
    );
  });

  it("aborts on timeout", async () => {
    // Simulate a real fetch: rejects if signal already aborted, otherwise hangs.
    // When the timeout fires and aborts the controller, the pending fetch rejects.
    mockFetch.mockImplementation((_url: string, opts?: { signal?: AbortSignal }) => {
      if (opts?.signal?.aborted) {
        return Promise.reject(new DOMException("Aborted", "AbortError"));
      }
      return new Promise((_, reject) => {
        opts?.signal?.addEventListener("abort", () => {
          reject(new DOMException("Aborted", "AbortError"));
        });
      });
    });

    const promise = fetchUsageSnapshot({ token: "test-key", timeoutMs: 20 });
    await expect(promise).rejects.toThrow();
  }, 10_000);
});

// ---------------------------------------------------------------------------
// prepareExtraParams
// ---------------------------------------------------------------------------

describe("prepareExtraParams", () => {
  it("adds stream_options with include_usage: true to extraParams", () => {
    const ctx = { extraParams: { foo: "bar" } };
    const result = prepareExtraParams(ctx);
    expect(result).toEqual({ foo: "bar", stream_options: { include_usage: true } });
  });

  it("returns { stream_options: { include_usage: true } } when extraParams is undefined", () => {
    const ctx = { extraParams: undefined };
    const result = prepareExtraParams(ctx);
    expect(result).toEqual({ stream_options: { include_usage: true } });
  });

  it("returns { stream_options: { include_usage: true } } when extraParams is null", () => {
    const ctx = { extraParams: null };
    const result = prepareExtraParams(ctx);
    expect(result).toEqual({ stream_options: { include_usage: true } });
  });
});