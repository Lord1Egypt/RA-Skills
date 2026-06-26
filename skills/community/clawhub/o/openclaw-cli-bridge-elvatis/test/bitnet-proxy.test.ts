/**
 * test/bitnet-proxy.test.ts
 *
 * Tests for BitNet local inference routing in the cli-bridge proxy.
 * Spins up a mock llama-server and validates:
 *   - 503 when BitNet server is unreachable
 *   - Successful forward (non-streaming)
 *   - Tools rejection (400)
 */

import { describe, it, expect, beforeAll, afterAll } from "vitest";
import http from "node:http";
import type { AddressInfo } from "node:net";
import { startProxyServer, CLI_MODELS } from "../src/proxy-server.js";

// ──────────────────────────────────────────────────────────────────────────────
// Mock llama-server — responds to POST /v1/chat/completions
// ──────────────────────────────────────────────────────────────────────────────

let mockLlamaServer: http.Server;
let mockLlamaPort: number;

function startMockLlamaServer(): Promise<void> {
  return new Promise((resolve) => {
    mockLlamaServer = http.createServer((req, res) => {
      if (req.url === "/v1/models" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ data: [{ id: "bitnet-2b" }] }));
        return;
      }
      if (req.url === "/v1/chat/completions" && req.method === "POST") {
        const chunks: Buffer[] = [];
        req.on("data", (d: Buffer) => chunks.push(d));
        req.on("end", () => {
          const body = JSON.parse(Buffer.concat(chunks).toString("utf8"));
          const lastMsg = body.messages?.[body.messages.length - 1]?.content ?? "";
          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify({
            id: "chatcmpl-bitnet-mock",
            object: "chat.completion",
            created: Math.floor(Date.now() / 1000),
            model: "bitnet-2b",
            choices: [{ index: 0, message: { role: "assistant", content: `bitnet echo: ${lastMsg}` }, finish_reason: "stop" }],
            usage: { prompt_tokens: 4, completion_tokens: 6, total_tokens: 10 },
          }));
        });
        return;
      }
      res.writeHead(404);
      res.end();
    });
    mockLlamaServer.listen(0, "127.0.0.1", () => {
      mockLlamaPort = (mockLlamaServer.address() as AddressInfo).port;
      resolve();
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// HTTP helpers
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

// ──────────────────────────────────────────────────────────────────────────────
// Setup: two proxy servers
//   - withBitNet: points to mock llama-server
//   - noBitNet: points to unreachable port (503 expected)
// ──────────────────────────────────────────────────────────────────────────────

const TEST_KEY = "test-bitnet-key";
let serverWith: http.Server;
let serverNo: http.Server;
let urlWith: string;
let urlNo: string;

beforeAll(async () => {
  await startMockLlamaServer();

  serverWith = await startProxyServer({
    port: 0,
    apiKey: TEST_KEY,
    log: () => {},
    warn: () => {},
    getBitNetServerUrl: () => `http://127.0.0.1:${mockLlamaPort}`,
  });
  const addrWith = serverWith.address() as AddressInfo;
  urlWith = `http://127.0.0.1:${addrWith.port}`;

  serverNo = await startProxyServer({
    port: 0,
    apiKey: TEST_KEY,
    log: () => {},
    warn: () => {},
    getBitNetServerUrl: () => `http://127.0.0.1:1`, // unreachable
  });
  const addrNo = serverNo.address() as AddressInfo;
  urlNo = `http://127.0.0.1:${addrNo.port}`;
});

afterAll(async () => {
  await new Promise<void>((r) => serverWith.close(() => r()));
  await new Promise<void>((r) => serverNo.close(() => r()));
  await new Promise<void>((r) => mockLlamaServer.close(() => r()));
});

// ──────────────────────────────────────────────────────────────────────────────
// Tests
// ──────────────────────────────────────────────────────────────────────────────

describe("CLI_MODELS includes BitNet", () => {
  it("has local-bitnet/bitnet-2b in the model list", () => {
    const bitnet = CLI_MODELS.filter((m) => m.id.startsWith("local-bitnet/"));
    expect(bitnet).toHaveLength(1);
    expect(bitnet[0].id).toBe("local-bitnet/bitnet-2b");
  });
});

describe("POST /v1/chat/completions — BitNet routing", () => {
  const auth = { Authorization: `Bearer ${TEST_KEY}` };

  it("returns 503 when BitNet server is unreachable", async () => {
    const { status, body } = await httpPost(
      `${urlNo}/v1/chat/completions`,
      { model: "local-bitnet/bitnet-2b", messages: [{ role: "user", content: "Hi" }] },
      auth
    );
    expect(status).toBe(503);
    const b = body as { error: { code: string; message: string } };
    expect(b.error.code).toBe("bitnet_unavailable");
    expect(b.error.message).toContain("BitNet server not running");
  });

  it("forwards request to mock llama-server (non-streaming)", async () => {
    const { status, body } = await httpPost(
      `${urlWith}/v1/chat/completions`,
      { model: "local-bitnet/bitnet-2b", messages: [{ role: "user", content: "Hello BitNet" }], stream: false },
      auth
    );
    expect(status).toBe(200);
    const b = body as {
      choices: Array<{ message: { content: string }; finish_reason: string }>;
    };
    expect(b.choices[0].message.content).toContain("Hello BitNet");
    expect(b.choices[0].finish_reason).toBe("stop");
  });

  it("accepts tool calls (llama-server ignores tools silently)", async () => {
    // local-bitnet/* is exempt from tool rejection — llama-server ignores tool schemas
    // and responds normally. OpenClaw always sends tools with every request.
    const { status } = await httpPost(
      `${urlWith}/v1/chat/completions`,
      {
        model: "local-bitnet/bitnet-2b",
        messages: [{ role: "user", content: "use tools" }],
        tools: [{ type: "function", function: { name: "test", parameters: {} } }],
      },
      auth
    );
    // Should NOT return 400 tools_not_supported — reaches BitNet routing (503 = server not running in test)
    expect(status).not.toBe(400);
  });
});
