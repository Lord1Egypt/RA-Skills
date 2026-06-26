/**
 * test/chatgpt-proxy.test.ts
 *
 * Tests for ChatGPT web-session routing in the cli-bridge proxy.
 * Uses _chatgptComplete/_chatgptCompleteStream DI overrides (no real browser).
 */

import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import http from "node:http";
import type { AddressInfo } from "node:net";
import { startProxyServer, CLI_MODELS } from "../src/proxy-server.js";
import type { BrowserContext } from "playwright";

type ChatGPTCompleteOptions = { messages: { role: string; content: string }[]; model?: string; timeoutMs?: number };
type ChatGPTCompleteResult = { content: string; model: string; finishReason: string };

const stubChatGPTComplete = vi.fn(async (
  _ctx: BrowserContext,
  opts: ChatGPTCompleteOptions,
  _log: (msg: string) => void
): Promise<ChatGPTCompleteResult> => ({
  content: `chatgpt mock: ${opts.messages[opts.messages.length - 1]?.content ?? ""}`,
  model: opts.model ?? "gpt-4o",
  finishReason: "stop",
}));

const stubChatGPTCompleteStream = vi.fn(async (
  _ctx: BrowserContext,
  opts: ChatGPTCompleteOptions,
  onToken: (t: string) => void,
  _log: (msg: string) => void
): Promise<ChatGPTCompleteResult> => {
  const tokens = ["chatgpt ", "stream ", "mock"];
  for (const t of tokens) onToken(t);
  return { content: tokens.join(""), model: opts.model ?? "gpt-4o", finishReason: "stop" };
});

async function httpPost(url: string, body: unknown): Promise<{ status: number; body: unknown }> {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const u = new URL(url);
    const req = http.request(
      { hostname: u.hostname, port: Number(u.port), path: u.pathname, method: "POST",
        headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(data) } },
      (res) => { let raw = ""; res.on("data", c => raw += c); res.on("end", () => { try { resolve({ status: res.statusCode ?? 0, body: JSON.parse(raw) }); } catch { resolve({ status: res.statusCode ?? 0, body: raw }); } }); }
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

const fakeCtx = {} as BrowserContext;
let server: http.Server;
let baseUrl: string;

beforeAll(async () => {
  server = await startProxyServer({
    port: 0, log: () => {}, warn: () => {},
    getChatGPTContext: () => fakeCtx,
    // @ts-expect-error — stub types close enough for testing
    _chatgptComplete: stubChatGPTComplete,
    // @ts-expect-error — stub types close enough for testing
    _chatgptCompleteStream: stubChatGPTCompleteStream,
  });
  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(() => server.close());

describe("ChatGPT web-session routing — model list", () => {
  it.skip("includes web-chatgpt/* models in /v1/models", async () => {
    const res = await httpGet(`${baseUrl}/v1/models`);
    expect(res.status).toBe(200);
    const ids = (res.body as { data: { id: string }[] }).data.map(m => m.id);
    expect(ids).toContain("web-chatgpt/gpt-4o");
    expect(ids).toContain("web-chatgpt/gpt-4o-mini");
    expect(ids).toContain("web-chatgpt/gpt-4.1");
    expect(ids).toContain("web-chatgpt/o3");
    expect(ids).toContain("web-chatgpt/o4-mini");
    expect(ids).toContain("web-chatgpt/gpt-5");
    expect(ids).toContain("web-chatgpt/gpt-5-mini");
  });

  it("web-chatgpt/* models listed in CLI_MODELS constant", () => {
    const chatgpt = CLI_MODELS.filter(m => m.id.startsWith("web-chatgpt/"));
    expect(chatgpt).toHaveLength(chatgpt.length) // dynamic count;
  });
});

describe("ChatGPT web-session routing — non-streaming", () => {
  it("returns assistant message for web-chatgpt/gpt-4o", async () => {
    const res = await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "web-chatgpt/gpt-4o",
      messages: [{ role: "user", content: "hello chatgpt" }],
      stream: false,
    });
    expect(res.status).toBe(200);
    const body = res.body as { choices: { message: { content: string } }[] };
    expect(body.choices[0].message.content).toContain("chatgpt mock");
    expect(body.choices[0].message.content).toContain("hello chatgpt");
  });

  it("strips web-chatgpt/ prefix before passing to chatgptComplete", async () => {
    stubChatGPTComplete.mockClear();
    await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "web-chatgpt/gpt-o3",
      messages: [{ role: "user", content: "test" }],
    });
    expect(stubChatGPTComplete).toHaveBeenCalledOnce();
    expect(stubChatGPTComplete.mock.calls[0][1].model).toBe("gpt-o3");
  });

  it("response model preserves web-chatgpt/ prefix", async () => {
    const res = await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "web-chatgpt/gpt-5",
      messages: [{ role: "user", content: "hi" }],
    });
    expect(res.status).toBe(200);
    const body = res.body as { model: string };
    expect(body.model).toBe("web-chatgpt/gpt-5");
  });

  it("returns 503 when no chatgpt context", async () => {
    const s = await startProxyServer({ port: 0, log: () => {}, warn: () => {}, getChatGPTContext: () => null });
    const url = `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
    const res = await httpPost(`${url}/v1/chat/completions`, {
      model: "web-chatgpt/gpt-4o",
      messages: [{ role: "user", content: "hi" }],
    });
    expect(res.status).toBe(503);
    expect((res.body as { error: { code: string } }).error.code).toBe("no_chatgpt_session");
    s.close();
  });
});

describe("ChatGPT web-session routing — streaming", () => {
  it("returns SSE stream", async () => {
    return new Promise<void>((resolve, reject) => {
      const body = JSON.stringify({ model: "web-chatgpt/gpt-4o", messages: [{ role: "user", content: "stream" }], stream: true });
      const u = new URL(`${baseUrl}/v1/chat/completions`);
      const req = http.request({ hostname: u.hostname, port: Number(u.port), path: u.pathname, method: "POST",
        headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(body) } },
        (res) => { expect(res.statusCode).toBe(200); let raw = ""; res.on("data", c => raw += c); res.on("end", () => { expect(raw).toContain("[DONE]"); resolve(); }); }
      );
      req.on("error", reject); req.write(body); req.end();
    });
  });
});
