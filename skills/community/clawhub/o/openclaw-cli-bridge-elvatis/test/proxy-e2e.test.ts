/**
 * End-to-end tests for the CLI bridge proxy server.
 *
 * Starts a real HTTP server on a random port and validates all endpoints:
 *   - GET /health, /v1/health
 *   - GET /v1/models
 *   - POST /v1/chat/completions (non-streaming + streaming)
 *   - Auth enforcement
 *   - Error handling (bad JSON, missing fields, unknown model, 404)
 *   - vllm/ prefix stripping through the full stack
 *
 * routeToCliRunner is mocked so we don't need real CLIs installed.
 */

import { describe, it, expect, beforeAll, afterAll, vi, beforeEach } from "vitest";
import http from "node:http";
import { startProxyServer, CLI_MODELS } from "../src/proxy-server.js";

// Mock session-manager so we don't spawn real CLIs for session endpoints
const mockSessions = new Map<string, { model: string; status: string; stdout: string; stderr: string; exitCode: number | null; startTime: number }>();
let nextSessionId = "aabbccdd11223344";

vi.mock("../src/session-manager.js", () => ({
  sessionManager: {
    spawn: vi.fn((model: string, _messages: unknown[]) => {
      const id = nextSessionId;
      mockSessions.set(id, { model, status: "running", stdout: "", stderr: "", exitCode: null, startTime: Date.now() });
      // Generate a different ID next time
      nextSessionId = Math.random().toString(16).slice(2, 18).padEnd(16, "0");
      return id;
    }),
    poll: vi.fn((sessionId: string) => {
      const entry = mockSessions.get(sessionId);
      if (!entry) return null;
      return { running: entry.status === "running", exitCode: entry.exitCode, status: entry.status };
    }),
    log: vi.fn((sessionId: string, offset = 0) => {
      const entry = mockSessions.get(sessionId);
      if (!entry) return null;
      return { stdout: entry.stdout.slice(offset), stderr: entry.stderr.slice(offset), offset: entry.stdout.length };
    }),
    write: vi.fn((sessionId: string) => {
      return mockSessions.has(sessionId);
    }),
    kill: vi.fn((sessionId: string) => {
      const entry = mockSessions.get(sessionId);
      if (!entry || entry.status !== "running") return false;
      entry.status = "killed";
      return true;
    }),
    list: vi.fn(() => {
      const result: { sessionId: string; model: string; status: string; startTime: number; exitCode: number | null }[] = [];
      for (const [sessionId, entry] of mockSessions) {
        result.push({ sessionId, model: entry.model, status: entry.status, startTime: entry.startTime, exitCode: entry.exitCode });
      }
      return result;
    }),
    stop: vi.fn(),
    cleanup: vi.fn(),
  },
}));

// Mock cli-runner so we don't spawn real CLIs
vi.mock("../src/cli-runner.js", async (importOriginal) => {
  const orig = await importOriginal<typeof import("../src/cli-runner.js")>();
  return {
    ...orig,
    routeToCliRunner: vi.fn(async (model: string, _messages: unknown[], _timeout: number) => {
      // Simulate the real router: strip vllm/ prefix, validate model
      const normalized = model.startsWith("vllm/") ? model.slice(5) : model;
      if (!normalized.startsWith("cli-gemini/") && !normalized.startsWith("cli-claude/") && !normalized.startsWith("openai-codex/") && !normalized.startsWith("opencode/") && !normalized.startsWith("pi/")) {
        throw new Error(`Unknown CLI bridge model: "${model}"`);
      }
      // Returns CliToolResult (content + optional tool_calls)
      return { content: `Mock response from ${normalized}` };
    }),
    extractMultimodalParts: vi.fn((messages: unknown[]) => ({ cleanMessages: messages, mediaFiles: [] })),
    cleanupMediaFiles: vi.fn(),
  };
});

const API_KEY = "test-key-e2e";
let server: http.Server;
let port: number;
const baseUrl = () => `http://127.0.0.1:${port}`;

// ──────────────────────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────────────────────

function fetch(path: string, opts: {
  method?: string;
  headers?: Record<string, string>;
  body?: string;
} = {}): Promise<{ status: number; headers: http.IncomingHttpHeaders; body: string }> {
  return new Promise((resolve, reject) => {
    const url = new URL(path, baseUrl());
    const req = http.request(url, {
      method: opts.method ?? "GET",
      headers: opts.headers,
    }, (res) => {
      const chunks: Buffer[] = [];
      res.on("data", (d: Buffer) => chunks.push(d));
      res.on("end", () => {
        resolve({
          status: res.statusCode ?? 0,
          headers: res.headers,
          body: Buffer.concat(chunks).toString("utf8"),
        });
      });
    });
    req.on("error", reject);
    if (opts.body) req.write(opts.body);
    req.end();
  });
}

function json(path: string, body: unknown, extraHeaders: Record<string, string> = {}) {
  return fetch(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
      ...extraHeaders,
    },
    body: JSON.stringify(body),
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// Setup / Teardown
// ──────────────────────────────────────────────────────────────────────────────

beforeAll(async () => {
  // Use port 0 to let the OS pick a free port
  server = await startProxyServer({
    port: 0,
    apiKey: API_KEY,
    timeoutMs: 5_000,
    log: () => {},
    warn: () => {},
  });
  const addr = server.address();
  port = typeof addr === "object" && addr ? addr.port : 0;
});

afterAll(async () => {
  await new Promise<void>((resolve) => {
    server.closeAllConnections();
    server.close(() => resolve());
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Health checks
// ──────────────────────────────────────────────────────────────────────────────

describe("GET /health", () => {
  it("returns {status: ok}", async () => {
    const res = await fetch("/health");
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.status).toBe("ok");
    expect(body.service).toBe("openclaw-cli-bridge");
  });
});

describe("GET /v1/health", () => {
  it("returns {status: ok}", async () => {
    const res = await fetch("/v1/health");
    expect(res.status).toBe(200);
    expect(JSON.parse(res.body).status).toBe("ok");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// CORS preflight
// ──────────────────────────────────────────────────────────────────────────────

describe("OPTIONS (CORS preflight)", () => {
  it("returns 204 with CORS headers", async () => {
    const res = await fetch("/v1/chat/completions", { method: "OPTIONS" });
    expect(res.status).toBe(204);
    expect(res.headers["access-control-allow-origin"]).toBe("*");
    expect(res.headers["access-control-allow-methods"]).toContain("POST");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Model listing
// ──────────────────────────────────────────────────────────────────────────────

describe("GET /v1/models", () => {
  it("returns all CLI bridge models in OpenAI format", async () => {
    const res = await fetch("/v1/models");
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.object).toBe("list");
    expect(body.data).toHaveLength(CLI_MODELS.length);

    const ids = body.data.map((m: { id: string }) => m.id);
    for (const model of CLI_MODELS) {
      expect(ids).toContain(model.id);
    }

    // Each model has the correct OpenAI shape
    for (const m of body.data) {
      expect(m.object).toBe("model");
      expect(m.owned_by).toBe("openclaw-cli-bridge");
      expect(typeof m.created).toBe("number");
    }
  });

  it("includes CORS headers", async () => {
    const res = await fetch("/v1/models");
    expect(res.headers["access-control-allow-origin"]).toBe("*");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Chat completions — non-streaming
// ──────────────────────────────────────────────────────────────────────────────

describe("POST /v1/chat/completions (non-streaming)", () => {
  it("returns valid OpenAI completion for cli-claude model", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-claude/claude-sonnet-4-6",
      messages: [{ role: "user", content: "hello" }],
      stream: false,
    });

    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.object).toBe("chat.completion");
    expect(body.id).toMatch(/^chatcmpl-cli-/);
    expect(body.model).toBe("cli-claude/claude-sonnet-4-6");
    expect(body.choices).toHaveLength(1);
    expect(body.choices[0].message.role).toBe("assistant");
    expect(body.choices[0].message.content).toBe("Mock response from cli-claude/claude-sonnet-4-6");
    expect(body.choices[0].finish_reason).toBe("stop");
    expect(body.usage).toBeDefined();
  });

  it("returns valid completion for cli-gemini model", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hi" }],
    });

    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toBe("Mock response from cli-gemini/gemini-2.5-pro");
  });

  it("handles vllm/ prefix (OpenClaw sends full provider path)", async () => {
    const res = await json("/v1/chat/completions", {
      model: "vllm/cli-claude/claude-haiku-4-5",
      messages: [{ role: "user", content: "test" }],
    });

    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    // Model in response should be the requested model (vllm/ prefix preserved in response)
    expect(body.model).toBe("vllm/cli-claude/claude-haiku-4-5");
    // But the mock receives the model and strips vllm/ internally
    expect(body.choices[0].message.content).toBe("Mock response from cli-claude/claude-haiku-4-5");
  });

  it("handles vllm/ prefix for gemini models", async () => {
    const res = await json("/v1/chat/completions", {
      model: "vllm/cli-gemini/gemini-2.5-flash",
      messages: [{ role: "user", content: "test" }],
    });

    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toBe("Mock response from cli-gemini/gemini-2.5-flash");
  });

  it("passes multi-turn conversation", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-claude/claude-sonnet-4-6",
      messages: [
        { role: "system", content: "You are helpful" },
        { role: "user", content: "What is 2+2?" },
        { role: "assistant", content: "4" },
        { role: "user", content: "And 3+3?" },
      ],
    });

    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toContain("Mock response");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Chat completions — streaming (SSE)
// ──────────────────────────────────────────────────────────────────────────────

describe("POST /v1/chat/completions (streaming)", () => {
  it("returns SSE stream with correct chunks", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-claude/claude-sonnet-4-6",
      messages: [{ role: "user", content: "hello" }],
      stream: true,
    });

    expect(res.status).toBe(200);
    expect(res.headers["content-type"]).toBe("text/event-stream");

    // Parse SSE events
    const events = res.body
      .split("\n\n")
      .filter((e) => e.startsWith("data: "))
      .map((e) => e.replace("data: ", ""));

    // Should end with [DONE]
    expect(events[events.length - 1]).toBe("[DONE]");

    // Parse JSON chunks (all except [DONE])
    const chunks = events
      .filter((e) => e !== "[DONE]")
      .map((e) => JSON.parse(e));

    // First chunk should have role delta
    expect(chunks[0].choices[0].delta.role).toBe("assistant");
    expect(chunks[0].object).toBe("chat.completion.chunk");

    // Last JSON chunk should have finish_reason: "stop"
    const lastChunk = chunks[chunks.length - 1];
    expect(lastChunk.choices[0].finish_reason).toBe("stop");

    // Content chunks should reassemble to the full response
    const fullContent = chunks
      .map((c) => c.choices[0].delta.content ?? "")
      .join("");
    expect(fullContent).toBe("Mock response from cli-claude/claude-sonnet-4-6");

    // All chunks should have consistent id
    const ids = new Set(chunks.map((c) => c.id));
    expect(ids.size).toBe(1);
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Auth enforcement
// ──────────────────────────────────────────────────────────────────────────────

describe("Auth enforcement", () => {
  it("rejects request without Authorization header", async () => {
    const res = await fetch("/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "cli-claude/claude-sonnet-4-6",
        messages: [{ role: "user", content: "hi" }],
      }),
    });

    expect(res.status).toBe(401);
    expect(JSON.parse(res.body).error.type).toBe("auth_error");
  });

  it("rejects request with wrong API key", async () => {
    const res = await fetch("/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer wrong-key",
      },
      body: JSON.stringify({
        model: "cli-claude/claude-sonnet-4-6",
        messages: [{ role: "user", content: "hi" }],
      }),
    });

    expect(res.status).toBe(401);
  });

  it("accepts request with correct API key", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-claude/claude-sonnet-4-6",
      messages: [{ role: "user", content: "hi" }],
    });

    expect(res.status).toBe(200);
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Error handling
// ──────────────────────────────────────────────────────────────────────────────

describe("Error handling", () => {
  it("returns 400 for invalid JSON body", async () => {
    const res = await fetch("/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
      body: "not json",
    });

    expect(res.status).toBe(400);
    expect(JSON.parse(res.body).error.type).toBe("invalid_request_error");
  });

  it("returns 400 when model is missing", async () => {
    const res = await json("/v1/chat/completions", {
      messages: [{ role: "user", content: "hi" }],
    });

    expect(res.status).toBe(400);
    expect(JSON.parse(res.body).error.message).toContain("model and messages are required");
  });

  it("returns 400 when messages is empty", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-claude/claude-sonnet-4-6",
      messages: [],
    });

    expect(res.status).toBe(400);
  });

  it("returns 500 for unknown model", async () => {
    const res = await json("/v1/chat/completions", {
      model: "unknown/model",
      messages: [{ role: "user", content: "hi" }],
    });

    expect(res.status).toBe(500);
    expect(JSON.parse(res.body).error.type).toBe("cli_error");
    expect(JSON.parse(res.body).error.message).toContain("Unknown CLI bridge model");
  });

  it("returns 404 for unknown routes", async () => {
    const res = await fetch("/v1/nonexistent");
    expect(res.status).toBe(404);
    expect(JSON.parse(res.body).error.type).toBe("not_found");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Tool/function call rejection for CLI-proxy models
// ──────────────────────────────────────────────────────────────────────────────

describe("Tool call support", () => {
  it("accepts tools for cli-gemini models (200)", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hi" }],
      tools: [{ type: "function", function: { name: "test", parameters: {} } }],
    });

    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toBeDefined();
  });

  it("accepts tools for cli-claude models (200)", async () => {
    const res = await json("/v1/chat/completions", {
      model: "cli-claude/claude-sonnet-4-6",
      messages: [{ role: "user", content: "hi" }],
      tools: [{ type: "function", function: { name: "test", parameters: {} } }],
    });

    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toBeDefined();
  });

  it("does NOT reject tools for web-grok models (returns 503 no session)", async () => {
    const res = await json("/v1/chat/completions", {
      model: "web-grok/grok-3",
      messages: [{ role: "user", content: "hi" }],
      tools: [{ type: "function", function: { name: "test", parameters: {} } }],
    });

    // Reaches provider logic, gets 503 (no session)
    expect(res.status).not.toBe(400);
    expect(res.status).toBe(503);
    const body = JSON.parse(res.body);
    expect(body.error.code).toBe("no_grok_session");
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Model capabilities
// ──────────────────────────────────────────────────────────────────────────────

describe("Model capabilities", () => {
  it("cli-gemini models have capabilities.tools===true", async () => {
    const res = await fetch("/v1/models");
    const body = JSON.parse(res.body);
    const cliGeminiModels = body.data.filter((m: { id: string }) => m.id.startsWith("cli-gemini/"));
    expect(cliGeminiModels.length).toBeGreaterThan(0);
    for (const m of cliGeminiModels) {
      expect(m.capabilities.tools).toBe(true);
    }
  });

  it("cli-claude models have capabilities.tools===true", async () => {
    const res = await fetch("/v1/models");
    const body = JSON.parse(res.body);
    const cliClaudeModels = body.data.filter((m: { id: string }) => m.id.startsWith("cli-claude/"));
    expect(cliClaudeModels.length).toBeGreaterThan(0);
    for (const m of cliClaudeModels) {
      expect(m.capabilities.tools).toBe(true);
    }
  });

  it("web-grok models have capabilities.tools===true", async () => {
    const res = await fetch("/v1/models");
    const body = JSON.parse(res.body);
    const webGrokModels = body.data.filter((m: { id: string }) => m.id.startsWith("web-grok/"));
    expect(webGrokModels.length).toBeGreaterThan(0);
    for (const m of webGrokModels) {
      expect(m.capabilities.tools).toBe(true);
    }
  });

  it("openai-codex models have capabilities.tools===true", async () => {
    const res = await fetch("/v1/models");
    const body = JSON.parse(res.body);
    const codexModels = body.data.filter((m: { id: string }) => m.id.startsWith("openai-codex/"));
    expect(codexModels.length).toBeGreaterThan(0);
    for (const m of codexModels) {
      expect(m.capabilities.tools).toBe(true);
    }
  });

  it("opencode models have capabilities.tools===true", async () => {
    const res = await fetch("/v1/models");
    const body = JSON.parse(res.body);
    const ocModels = body.data.filter((m: { id: string }) => m.id.startsWith("opencode/"));
    expect(ocModels.length).toBeGreaterThan(0);
    for (const m of ocModels) {
      expect(m.capabilities.tools).toBe(true);
    }
  });

  it("pi models have capabilities.tools===true", async () => {
    const res = await fetch("/v1/models");
    const body = JSON.parse(res.body);
    const piModels = body.data.filter((m: { id: string }) => m.id.startsWith("pi/"));
    expect(piModels.length).toBeGreaterThan(0);
    for (const m of piModels) {
      expect(m.capabilities.tools).toBe(true);
    }
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Chat completions — new model prefixes (codex, opencode, pi)
// ──────────────────────────────────────────────────────────────────────────────

describe("POST /v1/chat/completions — new model prefixes", () => {
  it("returns completion for openai-codex model", async () => {
    const res = await json("/v1/chat/completions", {
      model: "openai-codex/gpt-5.3-codex",
      messages: [{ role: "user", content: "hello" }],
    });
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toBe("Mock response from openai-codex/gpt-5.3-codex");
  });

  it("returns completion for opencode model", async () => {
    const res = await json("/v1/chat/completions", {
      model: "opencode/default",
      messages: [{ role: "user", content: "hello" }],
    });
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toBe("Mock response from opencode/default");
  });

  it("returns completion for pi model", async () => {
    const res = await json("/v1/chat/completions", {
      model: "pi/default",
      messages: [{ role: "user", content: "hello" }],
    });
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.choices[0].message.content).toBe("Mock response from pi/default");
  });

  it("accepts tools for openai-codex models", async () => {
    const res = await json("/v1/chat/completions", {
      model: "openai-codex/gpt-5.3-codex",
      messages: [{ role: "user", content: "hi" }],
      tools: [{ type: "function", function: { name: "test", parameters: {} } }],
    });
    expect(res.status).toBe(200);
    expect(JSON.parse(res.body).choices[0].message.content).toBeDefined();
  });

  it("accepts tools for opencode models", async () => {
    const res = await json("/v1/chat/completions", {
      model: "opencode/default",
      messages: [{ role: "user", content: "hi" }],
      tools: [{ type: "function", function: { name: "test", parameters: {} } }],
    });
    expect(res.status).toBe(200);
    expect(JSON.parse(res.body).choices[0].message.content).toBeDefined();
  });

  it("accepts tools for pi models", async () => {
    const res = await json("/v1/chat/completions", {
      model: "pi/default",
      messages: [{ role: "user", content: "hi" }],
      tools: [{ type: "function", function: { name: "test", parameters: {} } }],
    });
    expect(res.status).toBe(200);
    expect(JSON.parse(res.body).choices[0].message.content).toBeDefined();
  });
});

// ──────────────────────────────────────────────────────────────────────────────
// Session Manager endpoints
// ──────────────────────────────────────────────────────────────────────────────

describe("Session Manager endpoints", () => {
  beforeEach(() => {
    mockSessions.clear();
    nextSessionId = "aabbccdd11223344";
  });

  it("POST /v1/sessions/spawn returns sessionId", async () => {
    const res = await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hello" }],
    });
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.sessionId).toBe("aabbccdd11223344");
  });

  it("POST /v1/sessions/spawn rejects missing model", async () => {
    const res = await json("/v1/sessions/spawn", {
      messages: [{ role: "user", content: "hello" }],
    });
    expect(res.status).toBe(400);
    expect(JSON.parse(res.body).error.message).toContain("model and messages are required");
  });

  it("POST /v1/sessions/spawn rejects missing messages", async () => {
    const res = await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [],
    });
    expect(res.status).toBe(400);
  });

  it("GET /v1/sessions lists sessions", async () => {
    // Spawn one session first
    await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hello" }],
    });

    const res = await fetch("/v1/sessions");
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.sessions).toHaveLength(1);
    expect(body.sessions[0].model).toBe("cli-gemini/gemini-2.5-pro");
    expect(body.sessions[0].status).toBe("running");
  });

  it("GET /v1/sessions/:id/poll returns status", async () => {
    const spawnRes = await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hello" }],
    });
    const { sessionId } = JSON.parse(spawnRes.body);

    const res = await fetch(`/v1/sessions/${sessionId}/poll`);
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.running).toBe(true);
    expect(body.status).toBe("running");
  });

  it("GET /v1/sessions/:id/poll returns 404 for unknown session", async () => {
    const res = await fetch("/v1/sessions/0000000000000000/poll");
    expect(res.status).toBe(404);
  });

  it("GET /v1/sessions/:id/log returns output", async () => {
    const spawnRes = await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hello" }],
    });
    const { sessionId } = JSON.parse(spawnRes.body);

    const res = await fetch(`/v1/sessions/${sessionId}/log`);
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(typeof body.stdout).toBe("string");
    expect(typeof body.stderr).toBe("string");
    expect(typeof body.offset).toBe("number");
  });

  it("GET /v1/sessions/:id/log returns 404 for unknown session", async () => {
    const res = await fetch("/v1/sessions/0000000000000000/log");
    expect(res.status).toBe(404);
  });

  it("POST /v1/sessions/:id/write sends data", async () => {
    const spawnRes = await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hello" }],
    });
    const { sessionId } = JSON.parse(spawnRes.body);

    const res = await json(`/v1/sessions/${sessionId}/write`, { data: "input" });
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.ok).toBe(true);
  });

  it("POST /v1/sessions/:id/kill terminates session", async () => {
    const spawnRes = await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hello" }],
    });
    const { sessionId } = JSON.parse(spawnRes.body);

    const res = await json(`/v1/sessions/${sessionId}/kill`, {});
    expect(res.status).toBe(200);
    const body = JSON.parse(res.body);
    expect(body.ok).toBe(true);
  });

  it("POST /v1/sessions/:id/kill returns false for already-killed session", async () => {
    const spawnRes = await json("/v1/sessions/spawn", {
      model: "cli-gemini/gemini-2.5-pro",
      messages: [{ role: "user", content: "hello" }],
    });
    const { sessionId } = JSON.parse(spawnRes.body);

    // Kill once
    await json(`/v1/sessions/${sessionId}/kill`, {});
    // Kill again
    const res = await json(`/v1/sessions/${sessionId}/kill`, {});
    expect(res.status).toBe(404);
    expect(JSON.parse(res.body).ok).toBe(false);
  });
});
