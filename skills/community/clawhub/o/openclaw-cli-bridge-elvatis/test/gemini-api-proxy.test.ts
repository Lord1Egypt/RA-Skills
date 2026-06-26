/**
 * test/gemini-api-proxy.test.ts
 *
 * Integration tests for Gemini API routing in the cli-bridge proxy.
 * Uses _geminiApiComplete/_geminiApiCompleteStream DI overrides (no real API calls).
 */

import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import http from "node:http";
import type { AddressInfo } from "node:net";
import { startProxyServer, CLI_MODELS } from "../src/proxy-server.js";
import type { GeminiApiResult, GeminiApiOptions, ContentPart } from "../src/gemini-api-runner.js";
import type { ChatMessage } from "../src/cli-runner.js";

const stubComplete = vi.fn(async (
  messages: ChatMessage[],
  opts: GeminiApiOptions
): Promise<GeminiApiResult> => ({
  content: `api mock: ${typeof messages[messages.length - 1]?.content === "string" ? messages[messages.length - 1].content : "multipart"}`,
  finishReason: "stop",
  promptTokens: 10,
  completionTokens: 5,
}));

const stubCompleteMultimodal = vi.fn(async (
  _messages: ChatMessage[],
  _opts: GeminiApiOptions
): Promise<GeminiApiResult> => ({
  content: [
    { type: "text", text: "Here is the image:" },
    { type: "image_url", image_url: { url: "data:image/png;base64,iVBOR..." } },
  ] as ContentPart[],
  finishReason: "stop",
  promptTokens: 15,
  completionTokens: 100,
}));

const stubCompleteStream = vi.fn(async (
  messages: ChatMessage[],
  opts: GeminiApiOptions,
  onToken: (t: string) => void
): Promise<GeminiApiResult> => {
  const tokens = ["api ", "stream ", "response"];
  for (const t of tokens) onToken(t);
  return { content: tokens.join(""), finishReason: "stop", promptTokens: 10, completionTokens: 8 };
});

const stubCompleteToolCalls = vi.fn(async (
  _messages: ChatMessage[],
  _opts: GeminiApiOptions
): Promise<GeminiApiResult> => ({
  content: "",
  finishReason: "stop",
  tool_calls: [
    { id: "call_abc123", type: "function", function: { name: "search", arguments: '{"q":"test"}' } },
  ],
}));

async function httpPost(url: string, body: unknown): Promise<{ status: number; body: unknown; raw: string }> {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u = new URL(url);
    const req = http.request(
      { hostname: u.hostname, port: Number(u.port), path: u.pathname, method: "POST",
        headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(data) } },
      (res) => { let raw = ""; res.on("data", c => raw += c); res.on("end", () => { try { resolve({ status: res.statusCode ?? 0, body: JSON.parse(raw), raw }); } catch { resolve({ status: res.statusCode ?? 0, body: raw, raw }); } }); }
    );
    req.on("error", reject); req.write(data); req.end();
  });
}
async function httpGet(url: string): Promise<{ status: number; body: unknown }> {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = http.request({ hostname: u.hostname, port: Number(u.port), path: u.pathname, method: "GET" },
      (res) => { let raw = ""; res.on("data", c => raw += c); res.on("end", () => { try { resolve({ status: res.statusCode ?? 0, body: JSON.parse(raw) }); } catch { resolve({ status: res.statusCode ?? 0, body: raw }); } }); }
    );
    req.on("error", reject); req.end();
  });
}
async function httpPostRaw(url: string, body: unknown): Promise<{ status: number; raw: string }> {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u = new URL(url);
    const req = http.request(
      { hostname: u.hostname, port: Number(u.port), path: u.pathname, method: "POST",
        headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(data) } },
      (res) => { let raw = ""; res.on("data", c => raw += c); res.on("end", () => resolve({ status: res.statusCode ?? 0, raw })); }
    );
    req.on("error", reject); req.write(data); req.end();
  });
}

let server: http.Server;
let baseUrl: string;

beforeAll(async () => {
  server = await startProxyServer({
    port: 0, log: () => {}, warn: () => {},
    // @ts-expect-error — stub types close enough for testing
    _geminiApiComplete: stubComplete,
    // @ts-expect-error — stub types close enough for testing
    _geminiApiCompleteStream: stubCompleteStream,
  });
  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(() => server.close());

describe("Gemini API routing — model list", () => {
  it("includes gemini-api/* models in /v1/models", async () => {
    const res = await httpGet(`${baseUrl}/v1/models`);
    expect(res.status).toBe(200);
    const data = res.body as { data: Array<{ id: string }> };
    const ids = data.data.map(m => m.id);
    expect(ids).toContain("gemini-api/gemini-2.5-flash");
    expect(ids).toContain("gemini-api/gemini-2.5-pro");
  });

  it("gemini-api models exist in CLI_MODELS constant", () => {
    const ids = CLI_MODELS.map(m => m.id);
    expect(ids).toContain("gemini-api/gemini-2.5-flash");
    expect(ids).toContain("gemini-api/gemini-2.5-pro");
  });
});

describe("Gemini API routing — non-streaming", () => {
  it("returns text response for gemini-api model", async () => {
    const res = await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "gemini-api/gemini-2.5-flash",
      messages: [{ role: "user", content: "Hello" }],
    });
    expect(res.status).toBe(200);
    const data = res.body as { choices: Array<{ message: { content: string } }> };
    expect(data.choices[0].message.content).toContain("api mock");
  });

  it("returns usage with real token counts from API", async () => {
    const res = await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "gemini-api/gemini-2.5-flash",
      messages: [{ role: "user", content: "test" }],
    });
    const data = res.body as { usage: { prompt_tokens: number; completion_tokens: number } };
    expect(data.usage.prompt_tokens).toBe(10);
    expect(data.usage.completion_tokens).toBe(5);
  });

  it("returns correct model in response", async () => {
    const res = await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "gemini-api/gemini-2.5-pro",
      messages: [{ role: "user", content: "pro model" }],
    });
    expect(res.status).toBe(200);
    const data = res.body as { model: string };
    expect(data.model).toBe("gemini-api/gemini-2.5-pro");
  });

  it("accepts vllm/ prefix and routes correctly", async () => {
    const res = await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "vllm/gemini-api/gemini-2.5-flash",
      messages: [{ role: "user", content: "with prefix" }],
    });
    expect(res.status).toBe(200);
    const data = res.body as { choices: Array<{ message: { content: string } }> };
    expect(data.choices[0].message.content).toContain("api mock");
  });
});

describe("Gemini API routing — streaming", () => {
  it("returns SSE stream with text tokens", async () => {
    const res = await httpPostRaw(`${baseUrl}/v1/chat/completions`, {
      model: "gemini-api/gemini-2.5-flash",
      messages: [{ role: "user", content: "stream test" }],
      stream: true,
    });
    expect(res.status).toBe(200);
    expect(res.raw).toContain("data: ");
    expect(res.raw).toContain("[DONE]");
    // Should contain the streamed tokens
    expect(res.raw).toContain("api ");
    expect(res.raw).toContain("stream ");
  });
});
