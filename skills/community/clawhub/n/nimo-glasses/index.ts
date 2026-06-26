/**
 * @nimo/openclaw-glasses
 *
 * OpenClaw plugin for Nimo AI Smart Glasses.
 * Allows the Nimo Companion App to connect directly to the user's OpenClaw
 * Gateway for private, on-device AI voice conversations.
 *
 * Data flow: Glasses → Companion App → OpenClaw Gateway (this plugin) → AI Agent
 * Data does NOT pass through Nimo servers.
 */

import crypto from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";

// ─── Types ───────────────────────────────────────────────────────────────────

interface SessionEntry {
  token: string;
  expiresAt: number; // ms timestamp
}

interface SseClient {
  res: ServerResponse;
  createdAt: number;
}

interface PluginConfig {
  maxResponseLength?: number;
  systemPrompt?: string;
}

// ─── State ───────────────────────────────────────────────────────────────────

const DEFAULT_SESSION_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours
const DEFAULT_MAX_RESPONSE_LENGTH = 300;
const DEFAULT_GATEWAY_PORT = 18789;

let currentLinkCode = generateLinkCode();
const sessions = new Map<string, SessionEntry>(); // token → session
const sseClients = new Map<string, SseClient>();   // token → SSE client

// ─── Helpers ─────────────────────────────────────────────────────────────────

/** Generate a random 6-character alphanumeric link code (uppercase). */
function generateLinkCode(): string {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; // Exclude confusable chars
  let code = "";
  const bytes = crypto.randomBytes(6);
  for (let i = 0; i < 6; i++) {
    code += chars[bytes[i]! % chars.length];
  }
  return code;
}

/** Issue a new session token and rotate the link code. */
function issueSessonToken(): SessionEntry {
  const token = crypto.randomUUID();
  const expiresAt = Date.now() + DEFAULT_SESSION_TTL_MS;
  sessions.set(token, { token, expiresAt });

  // Rotate link code
  currentLinkCode = generateLinkCode();
  console.log(`[nimo-glasses] 🔗 New link code: ${currentLinkCode}`);

  return { token, expiresAt };
}

/** Validate a bearer token from an Authorization header. Returns the session or null. */
function resolveSession(authHeader: string | undefined): SessionEntry | null {
  if (!authHeader?.startsWith("Bearer ")) return null;
  const token = authHeader.slice(7).trim();
  const session = sessions.get(token);
  if (!session) return null;
  if (Date.now() > session.expiresAt) {
    sessions.delete(token);
    return null;
  }
  return session;
}

/** Read the full request body as a string. */
function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on("data", (chunk: Buffer) => chunks.push(chunk));
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf-8")));
    req.on("error", reject);
  });
}

/** Send a JSON response. */
function jsonResponse(res: ServerResponse, status: number, body: unknown): void {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  });
  res.end(payload);
}

/** Push an SSE event to a connected client. */
function pushSseEvent(token: string, event: Record<string, unknown>): boolean {
  const client = sseClients.get(token);
  if (!client) return false;
  try {
    client.res.write(`data: ${JSON.stringify(event)}\n\n`);
    return true;
  } catch {
    sseClients.delete(token);
    return false;
  }
}

/** Resolve gateway port from config or env. */
function resolveGatewayPort(cfg: Record<string, unknown>): number {
  const envPort = parseInt(
    process.env.OPENCLAW_GATEWAY_PORT ?? process.env.CLAWDBOT_GATEWAY_PORT ?? "",
    10,
  );
  if (Number.isFinite(envPort) && envPort > 0) return envPort;
  const configPort = (cfg as { gateway?: { port?: number } }).gateway?.port;
  if (typeof configPort === "number" && configPort > 0) return configPort;
  return DEFAULT_GATEWAY_PORT;
}

/**
 * Call the OpenClaw gateway's /v1/chat/completions endpoint internally.
 * This is the clean way to route messages through the AI agent without
 * needing deep internal API access.
 */
async function callAgentChat(
  port: number,
  userText: string,
  pluginCfg: PluginConfig,
  onChunk: (text: string, done: boolean) => void,
  stream: boolean,
  gatewayToken?: string,
): Promise<void> {
  const maxTokens = pluginCfg.maxResponseLength ?? DEFAULT_MAX_RESPONSE_LENGTH;

  const systemPrompt =
    pluginCfg.systemPrompt ??
    `你是 Nimo 智能眼镜中的 AI 助手。回复要求：1) 简洁（${maxTokens}字内）2) 不换行不列表 3) 匹配用户语言 4) 直接回答不废话。You are an AI assistant in Nimo smart glasses. Keep responses concise (under ${maxTokens} chars), no line breaks, no lists, match user language.`;

  const agentId = process.env.OPENCLAW_AGENT_ID || "main";
  const body = JSON.stringify({
    model: `openclaw:${agentId}`,
    stream,
    max_tokens: maxTokens,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userText },
    ],
  });

  const resp = await fetch(`http://localhost:${port}/v1/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // Internal calls use gateway auth token
    ...(gatewayToken ? { Authorization: `Bearer ${gatewayToken}` } : {}),
    },
    body,
    // @ts-ignore — Node 18+ fetch signal
    signal: AbortSignal.timeout(60_000),
  });

  if (!resp.ok) {
    const errText = await resp.text().catch(() => "");
    throw new Error(`Agent responded ${resp.status}: ${errText}`);
  }

  if (!stream) {
    const data = (await resp.json()) as {
      choices?: Array<{ message?: { content?: string } }>;
    };
    const content = data.choices?.[0]?.message?.content ?? "";
    onChunk(content, true);
    return;
  }

  // Stream mode: parse SSE from the completions endpoint
  const reader = resp.body?.getReader();
  if (!reader) throw new Error("No response body");

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const raw = line.slice(6).trim();
      if (raw === "[DONE]") {
        onChunk("", true);
        return;
      }
      try {
        const parsed = JSON.parse(raw) as {
          choices?: Array<{ delta?: { content?: string } }>;
        };
        const delta = parsed.choices?.[0]?.delta?.content ?? "";
        if (delta) onChunk(delta, false);
      } catch {
        // ignore malformed lines
      }
    }
  }

  onChunk("", true);
}

// ─── Route Handlers ──────────────────────────────────────────────────────────

function handleHealth(res: ServerResponse): boolean {
  jsonResponse(res, 200, {
    status: "ok",
    plugin: "nimo-glasses",
    linkCode: currentLinkCode,
  });
  return true;
}

async function handlePair(req: IncomingMessage, res: ServerResponse): Promise<boolean> {
  const raw = await readBody(req);
  let body: { linkCode?: string };
  try {
    body = JSON.parse(raw);
  } catch {
    jsonResponse(res, 400, { error: "Invalid JSON" });
    return true;
  }

  if (!body.linkCode || body.linkCode !== currentLinkCode) {
    jsonResponse(res, 401, { error: "Invalid link code" });
    return true;
  }

  const session = issueSessonToken();
  jsonResponse(res, 200, {
    token: session.token,
    expiresAt: new Date(session.expiresAt).toISOString(),
  });
  return true;
}

async function handleChat(
  req: IncomingMessage,
  res: ServerResponse,
  cfg: Record<string, unknown>,
  pluginCfg: PluginConfig,
  gatewayToken?: string,
): Promise<boolean> {
  const session = resolveSession(req.headers["authorization"] as string | undefined);
  if (!session) {
    jsonResponse(res, 401, { error: "Unauthorized — invalid or expired token" });
    return true;
  }

  const raw = await readBody(req);
  let body: { text?: string; stream?: boolean };
  try {
    body = JSON.parse(raw);
  } catch {
    jsonResponse(res, 400, { error: "Invalid JSON" });
    return true;
  }

  if (!body.text?.trim()) {
    jsonResponse(res, 400, { error: "Missing text field" });
    return true;
  }

  const port = resolveGatewayPort(cfg);
  const useStream = body.stream === true;

  // Non-stream: collect full reply then respond
  if (!useStream) {
    try {
      let reply = "";
      await callAgentChat(
        port,
        body.text.trim(),
        pluginCfg,
        (chunk) => { reply += chunk; },
        false,
        gatewayToken,
      );
      jsonResponse(res, 200, { text: reply });
    } catch (err) {
      console.error("[nimo-glasses] Chat error:", err);
      jsonResponse(res, 500, { error: "Agent call failed" });
    }
    return true;
  }

  // Stream mode: push chunks via SSE to the /nimo/events client
  jsonResponse(res, 202, { status: "streaming" });

  callAgentChat(
    port,
    body.text.trim(),
    pluginCfg,
    (chunk, done) => {
      pushSseEvent(session.token, { type: "text", content: chunk, done });
    },
    true,
    gatewayToken,
  ).catch((err) => {
    console.error("[nimo-glasses] Stream chat error:", err);
    pushSseEvent(session.token, {
      type: "error",
      content: "Agent call failed",
      done: true,
    });
  });

  return true;
}

function handleEvents(
  req: IncomingMessage,
  res: ServerResponse,
): boolean {
  const session = resolveSession(req.headers["authorization"] as string | undefined);
  if (!session) {
    jsonResponse(res, 401, { error: "Unauthorized — invalid or expired token" });
    return true;
  }

  // Set up SSE
  res.writeHead(200, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Access-Control-Allow-Origin": "*",
    "X-Accel-Buffering": "no",
  });

  // Send initial heartbeat
  res.write(`data: ${JSON.stringify({ type: "connected", done: false })}\n\n`);

  sseClients.set(session.token, { res, createdAt: Date.now() });

  // Clean up on client disconnect
  req.on("close", () => {
    sseClients.delete(session.token);
  });

  // Keep connection alive with periodic pings
  const pingInterval = setInterval(() => {
    try {
      res.write(": ping\n\n");
    } catch {
      clearInterval(pingInterval);
      sseClients.delete(session.token);
    }
  }, 25_000);

  req.on("close", () => clearInterval(pingInterval));

  return true;
}

// ─── Plugin Registration ──────────────────────────────────────────────────────

export default function register(api: {
  config: Record<string, unknown>;
  pluginConfig?: PluginConfig & { config?: PluginConfig };
  logger: { info: (...a: unknown[]) => void; error: (...a: unknown[]) => void };
  registerHttpRoute: (opts: {
    path: string;
    auth: "plugin" | "gateway";
    match?: "exact" | "prefix";
    handler: (req: IncomingMessage, res: ServerResponse) => Promise<boolean> | boolean;
  }) => void;
}): void {
  // Config can come as api.pluginConfig directly or nested under .config
  const pluginCfg: PluginConfig = api.pluginConfig?.config ?? api.pluginConfig ?? {};

  // Extract gateway auth token for internal API calls
  const gatewayToken: string | undefined =
    (api.config as any)?.gateway?.auth?.token ||
    process.env.OPENCLAW_GATEWAY_TOKEN;

  api.logger.info(`[nimo-glasses] Plugin loaded. Initial link code: ${currentLinkCode}`);
  console.log(`\n[nimo-glasses] 🥽 Nimo AI Glasses plugin ready`);
  console.log(`[nimo-glasses] 🔗 Link code: ${currentLinkCode}`);
  console.log(`[nimo-glasses] 📱 Open Nimo Companion App → Connect → enter the code above\n`);

  // GET /nimo/health — Healthcheck + link code
  api.registerHttpRoute({
    path: "/nimo/health",
    auth: "plugin",
    match: "exact",
    handler: (_req, res) => handleHealth(res),
  });

  // POST /nimo/pair — Exchange link code for session token
  api.registerHttpRoute({
    path: "/nimo/pair",
    auth: "plugin",
    match: "exact",
    handler: (req, res) => handlePair(req, res),
  });

  // POST /nimo/chat — Send a message to the AI agent
  api.registerHttpRoute({
    path: "/nimo/chat",
    auth: "plugin",
    match: "exact",
    handler: (req, res) => handleChat(req, res, api.config, pluginCfg, gatewayToken),
  });

  // GET /nimo/events — SSE stream for AI replies
  api.registerHttpRoute({
    path: "/nimo/events",
    auth: "plugin",
    match: "exact",
    handler: (req, res) => handleEvents(req, res),
  });
}
