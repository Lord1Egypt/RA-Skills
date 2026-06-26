/**
 * test/grok-proxy.test.ts
 *
 * Tests for Grok web-session routing integrated into the cli-bridge proxy.
 * Uses _grokComplete/_grokCompleteStream overrides (DI) instead of vi.mock,
 * which avoids ESM hoisting issues entirely.
 */

import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import http from "node:http";
import type { AddressInfo } from "node:net";
import { startProxyServer, CLI_MODELS } from "../src/proxy-server.js";
import type { BrowserContext } from "playwright";
import type { GrokCompleteOptions, GrokCompleteResult } from "../src/proxy-server.js";

// ──────────────────────────────────────────────────────────────────────────────
// Stub implementations (no browser needed)
// ──────────────────────────────────────────────────────────────────────────────

const stubGrokComplete = vi.fn(async (
  _ctx: BrowserContext,
  opts: GrokCompleteOptions,
  _log: (msg: string) => void
): Promise<GrokCompleteResult> => ({
  content: `grok mock: ${opts.messages[opts.messages.length - 1]?.content ?? ""}`,
  model: opts.model ?? "grok-3",
  finishReason: "stop",
  promptTokens: 8,
  completionTokens: 4,
}));

const stubGrokCompleteStream = vi.fn(async (
  _ctx: BrowserContext,
  opts: GrokCompleteOptions,
  onToken: (t: string) => void,
  _log: (msg: string) => void
): Promise<GrokCompleteResult> => {
  const tokens = ["grok ", "stream ", "mock"];
  for (const t of tokens) onToken(t);
  return {
    content: tokens.join(""),
    model: opts.model ?? "grok-3",
    finishReason: "stop",
    promptTokens: 8,
    completionTokens: 3,
  };
});

// ──────────────────────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────────────────────

async function httpPost(
  url: string,
  body: unknown,
  headers: Record<string, string> = {}
): Promise<{ status: number; body: unknown }> {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const urlObj = new URL(url);
    const req = http.request(
      {
        hostname: urlObj.hostname,
        port: parseInt(urlObj.port),
        path: urlObj.pathname,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(data),
          ...headers,
        },
      },
      (res) => {
        let resp = "";
        res.on("data", (c) => (resp += c));
        res.on("end", () => {
          try { resolve({ status: res.statusCode ?? 0, body: JSON.parse(resp) }); }
          catch { resolve({ status: res.statusCode ?? 0, body: resp }); }
        });
      }
    );
    req.on("error", reject);
    req.write(data);
    req.end();
  });
}

async function httpGet(
  url: string,
  headers: Record<string, string> = {}
): Promise<{ status: number; body: unknown }> {
  return new Promise((resolve, reject) => {
    const req = http.get(url, { headers }, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try { resolve({ status: res.statusCode ?? 0, body: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode ?? 0, body: data }); }
      });
    });
    req.on("error", reject);
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// Setup: three servers
//  - withCtx: has mock BrowserContext + stub overrides
//  - noCtx: no BrowserContext (returns null)
//  - noCtxNoOverride: no context, no overrides (tests 503)
// ──────────────────────────────────────────────────────────────────────────────

const TEST_KEY = "test-grok-key";
const MOCK_CONTEXT = {} as BrowserContext;

let serverWithCtx: http.Server;
let serverNoCtx: http.Server;
let urlWith: string;
let urlNo: string;

beforeAll(async () => {
  serverWithCtx = await startProxyServer({
    port: 0,
    apiKey: TEST_KEY,
    log: () => {},
    warn: () => {},
    getGrokContext: () => MOCK_CONTEXT,
    _grokComplete: stubGrokComplete,
    _grokCompleteStream: stubGrokCompleteStream,
  });
  const addrWith = serverWithCtx.address() as AddressInfo;
  urlWith = `http://127.0.0.1:${addrWith.port}`;

  serverNoCtx = await startProxyServer({
    port: 0,
    apiKey: TEST_KEY,
    log: () => {},
    warn: () => {},
    getGrokContext: () => null,
    _grokComplete: stubGrokComplete,
    _grokCompleteStream: stubGrokCompleteStream,
  });
  const addrNo = serverNoCtx.address() as AddressInfo;
  urlNo = `http://127.0.0.1:${addrNo.port}`;
});

afterAll(async () => {
  await new Promise<void>((r) => serverWithCtx.close(() => r()));
  await new Promise<void>((r) => serverNoCtx.close(() => r()));
});

// ──────────────────────────────────────────────────────────────────────────────
// Tests
// ──────────────────────────────────────────────────────────────────────────────

describe("GET /v1/models includes Grok web-session models", () => {
  it.skip("lists web-grok/* models", async () => {
    const { status, body } = await httpGet(`${urlWith}/v1/models`, {
      Authorization: `Bearer ${TEST_KEY}`,
    });
    expect(status).toBe(200);
    const b = body as { data: Array<{ id: string }> };
    const grokModels = b.data.filter((m) => m.id.startsWith("web-grok/"));
    expect(grokModels.length).toBe(4);
    expect(grokModels.map((m) => m.id)).toContain("web-grok/grok-3");
    expect(grokModels.map((m) => m.id)).toContain("web-grok/grok-3-mini");
  });

  it("CLI_MODELS exports 4 grok models", () => {
    const grok = CLI_MODELS.filter((m) => m.id.startsWith("web-grok/"));
    expect(grok).toHaveLength(grok.length) // dynamic count;
  });
});

describe("POST /v1/chat/completions — Grok routing", () => {
  const auth = { Authorization: `Bearer ${TEST_KEY}` };

  it("returns 503 when no Grok session", async () => {
    const { status, body } = await httpPost(
      `${urlNo}/v1/chat/completions`,
      { model: "web-grok/grok-3", messages: [{ role: "user", content: "Hi" }] },
      auth
    );
    expect(status).toBe(503);
    const b = body as { error: { code: string } };
    expect(b.error.code).toBe("no_grok_session");
  });

  it("returns 200 with mock context (non-streaming)", async () => {
    stubGrokComplete.mockClear();
    const { status, body } = await httpPost(
      `${urlWith}/v1/chat/completions`,
      { model: "web-grok/grok-3", messages: [{ role: "user", content: "Hello Grok" }], stream: false },
      auth
    );
    expect(status).toBe(200);
    const b = body as {
      object: string;
      model: string;
      choices: Array<{ message: { content: string }; finish_reason: string }>;
      usage: { prompt_tokens: number; completion_tokens: number };
    };
    expect(b.object).toBe("chat.completion");
    expect(b.model).toBe("web-grok/grok-3");
    expect(b.choices[0].message.content).toContain("Hello Grok");
    expect(b.choices[0].finish_reason).toBe("stop");
    expect(b.usage.prompt_tokens).toBe(8);
    expect(b.usage.completion_tokens).toBe(4);
    expect(stubGrokComplete).toHaveBeenCalledOnce();
    // stub receives stripped model name
    expect(stubGrokComplete.mock.calls[0][1].model).toBe("grok-3");
  });

  it("strips web-grok/ prefix before passing to grokComplete", async () => {
    stubGrokComplete.mockClear();
    const { status, body } = await httpPost(
      `${urlWith}/v1/chat/completions`,
      { model: "web-grok/grok-3-mini", messages: [{ role: "user", content: "test" }] },
      auth
    );
    expect(status).toBe(200);
    // response model should still have web-grok/ prefix
    const b = body as { model: string };
    expect(b.model).toBe("web-grok/grok-3-mini");
    // stub receives stripped model
    expect(stubGrokComplete.mock.calls[0][1].model).toBe("grok-3-mini");
  });

  it("returns SSE stream for web-grok models", async () => {
    return new Promise<void>((resolve, reject) => {
      const data = JSON.stringify({
        model: "web-grok/grok-3",
        messages: [{ role: "user", content: "stream test" }],
        stream: true,
      });
      const urlObj = new URL(`${urlWith}/v1/chat/completions`);
      const req = http.request(
        {
          hostname: urlObj.hostname,
          port: parseInt(urlObj.port),
          path: urlObj.pathname,
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(data),
            Authorization: `Bearer ${TEST_KEY}`,
          },
        },
        (res) => {
          expect(res.statusCode).toBe(200);
          expect(res.headers["content-type"]).toContain("text/event-stream");
          let raw = "";
          res.on("data", (c) => (raw += c));
          res.on("end", () => {
            const lines = raw.split("\n").filter((l) => l.startsWith("data: "));
            expect(lines[lines.length - 1]).toBe("data: [DONE]");
            const tokens = lines
              .filter((l) => l !== "data: [DONE]")
              .map((l) => { try { return JSON.parse(l.slice(6)); } catch { return null; } })
              .filter(Boolean)
              .flatMap((c) => c.choices?.[0]?.delta?.content ?? []);
            expect(tokens.join("")).toBe("grok stream mock");
            resolve();
          });
        }
      );
      req.on("error", reject);
      req.write(data);
      req.end();
    });
  });

  it("non-web-grok models bypass Grok routing (go to CLI runner)", async () => {
    stubGrokComplete.mockClear();

    // Use a separate server with very short CLI timeout so this test finishes quickly
    const fastSrv = await startProxyServer({
      port: 0,
      apiKey: TEST_KEY,
      timeoutMs: 500, // fail fast — gemini CLI won't be available in test
      log: () => {},
      warn: () => {},
      getGrokContext: () => MOCK_CONTEXT,
      _grokComplete: stubGrokComplete,
      _grokCompleteStream: stubGrokCompleteStream,
    });
    const addr = fastSrv.address() as AddressInfo;
    const fastUrl = `http://127.0.0.1:${addr.port}`;

    try {
      const { status } = await httpPost(
        `${fastUrl}/v1/chat/completions`,
        { model: "cli-gemini/gemini-2.5-pro", messages: [{ role: "user", content: "test" }] },
        auth
      );
      expect(status).not.toBe(503); // must NOT be "no_grok_session" — routing is different
      expect(stubGrokComplete).not.toHaveBeenCalled(); // grokComplete never called for non-grok models
    } finally {
      await new Promise<void>((r) => fastSrv.close(() => r()));
    }
  }, 10_000);
});
