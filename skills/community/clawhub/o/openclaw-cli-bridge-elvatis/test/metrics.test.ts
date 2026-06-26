import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { readFileSync, unlinkSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

// We test estimateTokens directly and the MetricsCollector via the singleton
// after resetting. For persistence tests we mock METRICS_FILE.

describe("estimateTokens", () => {
  it("returns 0 for empty string", async () => {
    const { estimateTokens } = await import("../src/metrics.js");
    expect(estimateTokens("")).toBe(0);
  });

  it("returns 0 for undefined/null-ish input", async () => {
    const { estimateTokens } = await import("../src/metrics.js");
    expect(estimateTokens(undefined as unknown as string)).toBe(0);
    expect(estimateTokens(null as unknown as string)).toBe(0);
  });

  it("estimates ~1 token per 4 characters", async () => {
    const { estimateTokens } = await import("../src/metrics.js");
    // 100 chars → ceil(100/4) = 25 tokens
    const text = "a".repeat(100);
    expect(estimateTokens(text)).toBe(25);
  });

  it("rounds up partial tokens", async () => {
    const { estimateTokens } = await import("../src/metrics.js");
    // 5 chars → ceil(5/4) = 2
    expect(estimateTokens("hello")).toBe(2);
  });

  it("handles realistic prompt sizes", async () => {
    const { estimateTokens } = await import("../src/metrics.js");
    // ~400 chars of English text → ~100 tokens
    const text = "The quick brown fox jumps over the lazy dog. ".repeat(9); // 405 chars
    const tokens = estimateTokens(text);
    expect(tokens).toBeGreaterThan(90);
    expect(tokens).toBeLessThan(110);
  });
});

describe("MetricsCollector", () => {
  it("records requests and tracks per-model stats", async () => {
    const { metrics } = await import("../src/metrics.js");
    metrics.reset();

    metrics.recordRequest("test/model-a", 100, true, 50, 25);
    metrics.recordRequest("test/model-a", 200, true, 60, 30);
    metrics.recordRequest("test/model-b", 150, false, 40, 0);

    const snap = metrics.getMetrics();
    expect(snap.totalRequests).toBe(3);
    expect(snap.totalErrors).toBe(1);

    const modelA = snap.models.find(m => m.model === "test/model-a");
    expect(modelA).toBeDefined();
    expect(modelA!.requests).toBe(2);
    expect(modelA!.errors).toBe(0);
    expect(modelA!.promptTokens).toBe(110);
    expect(modelA!.completionTokens).toBe(55);
    expect(modelA!.totalLatencyMs).toBe(300);

    const modelB = snap.models.find(m => m.model === "test/model-b");
    expect(modelB).toBeDefined();
    expect(modelB!.requests).toBe(1);
    expect(modelB!.errors).toBe(1);
    expect(modelB!.promptTokens).toBe(40);
  });

  it("sorts models by request count descending", async () => {
    const { metrics } = await import("../src/metrics.js");
    metrics.reset();

    metrics.recordRequest("low", 10, true);
    metrics.recordRequest("high", 10, true);
    metrics.recordRequest("high", 10, true);
    metrics.recordRequest("high", 10, true);
    metrics.recordRequest("mid", 10, true);
    metrics.recordRequest("mid", 10, true);

    const snap = metrics.getMetrics();
    expect(snap.models[0].model).toBe("high");
    expect(snap.models[1].model).toBe("mid");
    expect(snap.models[2].model).toBe("low");
  });

  it("reset clears all data", async () => {
    const { metrics } = await import("../src/metrics.js");
    metrics.recordRequest("test/x", 10, true, 5, 5);
    metrics.reset();

    const snap = metrics.getMetrics();
    expect(snap.totalRequests).toBe(0);
    expect(snap.models).toHaveLength(0);
  });

  it("handles missing token counts gracefully", async () => {
    const { metrics } = await import("../src/metrics.js");
    metrics.reset();

    // No token args — should not crash, tokens stay 0
    metrics.recordRequest("test/no-tokens", 50, true);
    const snap = metrics.getMetrics();
    const m = snap.models[0];
    expect(m.promptTokens).toBe(0);
    expect(m.completionTokens).toBe(0);
  });
});
