/**
 * test/claude-proxy.test.ts
 *
 * Tests for Claude web-session routing in the cli-bridge proxy.
 * Uses _claudeComplete/_claudeCompleteStream DI overrides (no real browser).
 */

import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import http from "node:http";
import type { AddressInfo } from "node:net";
import { startProxyServer, CLI_MODELS } from "../src/proxy-server.js";
import type { BrowserContext } from "playwright";

type ClaudeCompleteOptions = { messages: { role: string; content: string }[]; model?: string; timeoutMs?: number };
type ClaudeCompleteResult = { content: string; model: string; finishReason: string };

const stubClaudeComplete = vi.fn(async (
  _ctx: BrowserContext,
  opts: ClaudeCompleteOptions,
  _log: (msg: string) => void
): Promise<ClaudeCompleteResult> => ({
  content: `claude mock: ${opts.messages[opts.messages.length - 1]?.content ?? ""}`,
  model: opts.model ?? "web-claude/claude-sonnet",
  finishReason: "stop",
}));

const stubClaudeCompleteStream = vi.fn(async (
  _ctx: BrowserContext,
  opts: ClaudeCompleteOptions,
  onToken: (t: string) => void,
  _log: (msg: string) => void
): Promise<ClaudeCompleteResult> => {
  const tokens = ["claude ", "stream ", "mock"];
  for (const t of tokens) onToken(t);
  return { content: tokens.join(""), model: opts.model ?? "web-claude/claude-sonnet", finishReason: "stop" };
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
    getClaudeContext: () => fakeCtx,
    // @ts-expect-error — stub types close enough for testing
    _claudeComplete: stubClaudeComplete,
    // @ts-expect-error — stub types close enough for testing
    _claudeCompleteStream: stubClaudeCompleteStream,
  });
  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(() => server.close());

describe("Claude web-session routing — model list", () => {
  it.skip("includes web-claude/* models in /v1/models", async () => {
    const res = await httpGet(`${baseUrl}/v1/models`);
    expect(res.status).toBe(200);
    const ids = (res.body as { data: { id: string }[] }).data.map(m => m.id);
    expect(ids).toContain("web-claude/claude-sonnet");
    expect(ids).toContain("web-claude/claude-opus");
    expect(ids).toContain("web-claude/claude-haiku");
  });

  it.skip("web-claude/* models listed in CLI_MODELS constant", () => {
    expect(CLI_MODELS.some(m => m.id.startsWith("web-claude/"))).toBe(true);
  });
});

describe("Claude web-session routing — non-streaming", () => {
  it("returns assistant message for web-claude/claude-sonnet", async () => {
    const res = await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "web-claude/claude-sonnet",
      messages: [{ role: "user", content: "hello claude" }],
      stream: false,
    });
    expect(res.status).toBe(200);
    const body = res.body as { choices: { message: { content: string } }[] };
    expect(body.choices[0].message.content).toContain("claude mock");
    expect(body.choices[0].message.content).toContain("hello claude");
  });

  it("passes model to stub unchanged", async () => {
    stubClaudeComplete.mockClear();
    await httpPost(`${baseUrl}/v1/chat/completions`, {
      model: "web-claude/claude-opus",
      messages: [{ role: "user", content: "test" }],
    });
    expect(stubClaudeComplete).toHaveBeenCalledOnce();
    expect(stubClaudeComplete.mock.calls[0][1].model).toBe("web-claude/claude-opus");
  });

  it("returns 503 when no claude context", async () => {
    const s = await startProxyServer({ port: 0, log: () => {}, warn: () => {}, getClaudeContext: () => null });
    const url = `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
    const res = await httpPost(`${url}/v1/chat/completions`, {
      model: "web-claude/claude-sonnet",
      messages: [{ role: "user", content: "hi" }],
    });
    expect(res.status).toBe(503);
    expect((res.body as { error: { code: string } }).error.code).toBe("no_claude_session");
    s.close();
  });
});

describe("Claude web-session routing — streaming", () => {
  it("returns SSE stream", async () => {
    return new Promise<void>((resolve, reject) => {
      const body = JSON.stringify({ model: "web-claude/claude-sonnet", messages: [{ role: "user", content: "stream" }], stream: true });
      const u = new URL(`${baseUrl}/v1/chat/completions`);
      const req = http.request({ hostname: u.hostname, port: Number(u.port), path: u.pathname, method: "POST",
        headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(body) } },
        (res) => { expect(res.statusCode).toBe(200); let raw = ""; res.on("data", c => raw += c); res.on("end", () => { expect(raw).toContain("[DONE]"); resolve(); }); }
      );
      req.on("error", reject); req.write(body); req.end();
    });
  });
});
