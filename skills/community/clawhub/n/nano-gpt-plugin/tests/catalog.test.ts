import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mapNanoModelToOpenClaw, fetchDynamicCatalog, type DynamicCatalogResult } from "../src/catalog";

// ---------------------------------------------------------------------------
// Model mapping tests
// ---------------------------------------------------------------------------

describe("mapNanoModelToOpenClaw", () => {
  it("maps a complete NanoGPT model correctly", () => {
    const raw = {
      id: "openai/gpt-5.2",
      name: "GPT-5.2",
      context_length: 128000,
      max_output_tokens: 32768,
      pricing: { prompt: 1.25, completion: 10 },
      capabilities: { vision: true, reasoning: false },
    };
    const mapped = mapNanoModelToOpenClaw(raw);
    expect(mapped.id).toBe("nano-gpt/openai/gpt-5.2");
    expect(mapped.name).toBe("GPT-5.2");
    expect(mapped.reasoning).toBe(false);
    expect(mapped.input).toEqual(["text", "image"]);
    expect(mapped.cost.input).toBe(1.25 / 1_000_000);
    expect(mapped.cost.output).toBe(10 / 1_000_000);
    expect(mapped.contextWindow).toBe(128_000);
    expect(mapped.maxTokens).toBe(32_768);
  });

  it("handles missing name (falls back to id)", () => {
    const raw = {
      id: "openai/gpt-5.2",
      context_length: 128000,
      max_output_tokens: 32768,
      pricing: { prompt: 1.25, completion: 10 },
      capabilities: { vision: false, reasoning: true },
    };
    const mapped = mapNanoModelToOpenClaw(raw);
    expect(mapped.name).toBe("openai/gpt-5.2");
    expect(mapped.reasoning).toBe(true);
    expect(mapped.input).toEqual(["text"]);
  });

  it("handles null context_length and max_output_tokens (uses defaults)", () => {
    const raw = {
      id: "openai/gpt-5.2",
      name: "GPT-5.2",
      context_length: null,
      max_output_tokens: null,
      pricing: { prompt: 0, completion: 0 },
      capabilities: { vision: false, reasoning: false },
    };
    const mapped = mapNanoModelToOpenClaw(raw);
    expect(mapped.contextWindow).toBe(128_000);
    expect(mapped.maxTokens).toBe(8_192);
  });

  it("handles null pricing (sets cost to 0)", () => {
    const raw = {
      id: "openai/gpt-5.2",
      name: "GPT-5.2",
      context_length: 128000,
      max_output_tokens: 32768,
      pricing: null,
      capabilities: { vision: false, reasoning: false },
    };
    const mapped = mapNanoModelToOpenClaw(raw);
    expect(mapped.cost.input).toBe(0);
    expect(mapped.cost.output).toBe(0);
  });

  it("handles missing capabilities (defaults to text-only, no reasoning)", () => {
    const raw = {
      id: "openai/gpt-5.2",
      name: "GPT-5.2",
      context_length: 128000,
      max_output_tokens: 32768,
      pricing: { prompt: 1.25, completion: 10 },
    };
    const mapped = mapNanoModelToOpenClaw(raw);
    expect(mapped.reasoning).toBe(false);
    expect(mapped.input).toEqual(["text"]);
  });
});

// ---------------------------------------------------------------------------
// Catalog fetcher tests (mocked network)
// ---------------------------------------------------------------------------

describe("fetchDynamicCatalog", () => {
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

  it("returns null when no API key is available", async () => {
    const result = await fetchDynamicCatalog({
      resolveProviderApiKey: () => ({ apiKey: undefined }),
    } as any);
    expect(result).toBeNull();
  });

  it("returns catalog when API key is available", async () => {
    const mockResponse = {
      models: [
        {
          id: "openai/gpt-5.2",
          name: "GPT-5.2",
          context_length: 128000,
          max_output_tokens: 32768,
          pricing: { prompt: 1.25, completion: 10 },
          capabilities: { vision: true, reasoning: false },
        },
        {
          id: "anthropic/claude-opus-4.6",
          name: "Claude Opus 4.6",
          context_length: 200000,
          max_output_tokens: 32768,
          pricing: { prompt: 6, completion: 30 },
          capabilities: { vision: true, reasoning: true },
        },
      ],
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const result = await fetchDynamicCatalog({
      resolveProviderApiKey: () => ({ apiKey: "test-key" }),
    } as any);

    expect(result).not.toBeNull();
    expect(result?.api).toBe("openai-completions");
    expect(result?.baseUrl).toBe("https://nano-gpt.com/api/v1");
    expect(result?.models).toHaveLength(2);

    // Check first model
    const model1 = result?.models[0];
    expect(model1.id).toBe("nano-gpt/openai/gpt-5.2");
    expect(model1.reasoning).toBe(false);
    expect(model1.input).toEqual(["text", "image"]);
    expect(model1.contextWindow).toBe(128_000);
    expect(model1.maxTokens).toBe(32_768);

    // Check second model
    const model2 = result?.models[1];
    expect(model2.id).toBe("nano-gpt/anthropic/claude-opus-4.6");
    expect(model2.reasoning).toBe(true);
    expect(model2.input).toEqual(["text", "image"]);
    expect(model2.contextWindow).toBe(200_000);
    expect(model2.maxTokens).toBe(32_768);
  });

  it("throws on non-ok response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
    });

    await expect(
      fetchDynamicCatalog({
        resolveProviderApiKey: () => ({ apiKey: "bad-key" }),
      } as any)
    ).rejects.toThrow("NanoGPT catalog fetch failed: 401 Unauthorized");
  });

  it("handles missing/null fields in API response", async () => {
    const mockResponse = {
      models: [
        {
          id: "openai/gpt-5.2",
          // missing name
          context_length: null, // null
          max_output_tokens: 32768,
          pricing: { prompt: null, completion: 10 }, // null prompt
          capabilities: { vision: false, reasoning: null }, // null reasoning
        },
      ],
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const result = await fetchDynamicCatalog({
      resolveProviderApiKey: () => ({ apiKey: "test-key" }),
    } as any);

    expect(result?.models).toHaveLength(1);
    const model = result?.models[0];
    expect(model.id).toBe("nano-gpt/openai/gpt-5.2");
    expect(model.name).toBe("openai/gpt-5.2"); // falls back to id
    expect(model.contextWindow).toBe(128_000); // default for null
    expect(model.maxTokens).toBe(32_768);
    expect(model.cost.input).toBe(0); // null pricing -> 0
    expect(model.cost.output).toBe(10 / 1_000_000);
    expect(model.reasoning).toBe(false); // null reasoning -> false
    expect(model.input).toEqual(["text"]); // no vision -> text-only
  });
});