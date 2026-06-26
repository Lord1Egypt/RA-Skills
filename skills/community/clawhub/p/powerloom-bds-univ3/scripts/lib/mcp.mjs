import { powerloomApiKey, mcpDebugEnabled } from "./powerloom-env.mjs";

/**
 * Powerloom BDS MCP over HTTP+SSE (same wire as Claude / OpenClaw remote MCP).
 * Env: POWERLOOM_API_KEY (required), POWERLOOM_MCP_URL (default https://bds-mcp.powerloom.io/sse),
 * POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS (default 60000; raise for large `bds_mpp_snapshot_allTrades` responses under backlog).
 *
 * Naming (do not confuse):
 * - **ClawHub skill slug:** `powerloom-bds-univ3` (folder + SKILL.md) — not an MCP tool.
 * - **MCP tool names:** `bds_mpp_*`, `get_credit_balance`, `verify_data_provenance` — from `tools/list` on the server.
 * - There is **no** tool called `bds_univ3` or `bds_univ3_*`.
 */

export function getMcpSseUrl() {
  const raw = process.env.POWERLOOM_MCP_URL || "https://bds-mcp.powerloom.io/sse";
  const trimmed = raw.replace(/\/$/, "");
  return trimmed.endsWith("/sse") ? trimmed : `${trimmed}/sse`;
}

export function getCallTimeoutMs() {
  const n = Number((process.env.POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS || "").trim());
  return Number.isFinite(n) && n > 0 ? n : 60000;
}

/**
 * Extract session id from MCP SSE bootstrap bytes.
 * The official transport sends an endpoint URL (often in `event: endpoint` / `data:`).
 * Session tokens may be hex, UUID (with hyphens), or URL-encoded — the old `[a-f0-9]+`-only
 * pattern failed for UUIDs and broke OpenClaw/Docker setups.
 */
export function extractMcpSseSessionId(text) {
  if (!text || typeof text !== "string") return null;
  const candidates = [
    /session_id=([^&\s"'<>]+)/i,
    /session_id%3D([^&\s"'<>%]+)/i,
    /\/messages\/\?session_id=([^&\s"'<>]+)/i,
  ];
  for (const re of candidates) {
    const m = text.match(re);
    if (!m?.[1]) continue;
    let raw = m[1].trim();
    try {
      raw = decodeURIComponent(raw);
    } catch {
      /* use raw */
    }
    if (raw.length > 0) return raw;
  }
  return null;
}

/**
 * Open GET /sse, read until session_id, POST initialize + notifications/initialized.
 * Caller must eventually cancel `reader` or call teardown.
 */
async function connectMcpSession(apiKey) {
  const sseUrl = getMcpSseUrl();
  const baseOrigin = sseUrl.replace(/\/sse\/?$/, "");
  const timeoutMs = getCallTimeoutMs();
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), timeoutMs);

  let sseResp;
  try {
    sseResp = await fetch(sseUrl, {
      headers: { Authorization: `Bearer ${apiKey}` },
      signal: ac.signal,
    });
  } catch (e) {
    clearTimeout(timer);
    if (e.name === "AbortError") {
      const err = new Error(
        `MCP SSE connection timed out after ${timeoutMs}ms (POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS).`
      );
      err.code = "TIMEOUT";
      throw err;
    }
    const err = new Error(`MCP SSE connection failed: ${e.message || e}`);
    err.code = "NETWORK";
    throw err;
  }

  if (sseResp.status === 401) {
    clearTimeout(timer);
    const err = new Error(
      "HTTP 401 — invalid or missing API key. Fix POWERLOOM_API_KEY (get a key via CLI at https://bds-metering.powerloom.io or browser at https://bds-metering.powerloom.io/metering)."
    );
    err.code = "HTTP_401";
    err.httpStatus = 401;
    throw err;
  }
  if (sseResp.status === 402) {
    clearTimeout(timer);
    const err = new Error(
      "HTTP 402 — credits exhausted. Top up at https://bds-metering.powerloom.io/metering"
    );
    err.code = "HTTP_402";
    err.httpStatus = 402;
    throw err;
  }
  if (sseResp.status === 429) {
    clearTimeout(timer);
    const err = new Error("HTTP 429 — rate limited. Back off and retry.");
    err.code = "HTTP_429";
    err.httpStatus = 429;
    throw err;
  }
  if (!sseResp.ok || !sseResp.body) {
    clearTimeout(timer);
    const txt = await sseResp.text().catch(() => "");
    const err = new Error(`MCP SSE HTTP ${sseResp.status}: ${txt.slice(0, 400)}`);
    err.code = "HTTP_ERROR";
    err.httpStatus = sseResp.status;
    throw err;
  }

  const reader = sseResp.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  const bootstrapMaxChunks = 500;

  let sessionId = null;
  for (let chunk = 0; chunk < bootstrapMaxChunks && !sessionId; chunk += 1) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    sessionId = extractMcpSseSessionId(buf);
  }

  if (!sessionId) {
    clearTimeout(timer);
    await reader.cancel().catch(() => {});
    const hint = mcpDebugEnabled()
        ? ` First bytes (debug): ${buf.slice(0, 800).replace(/\s+/g, " ")}`
        : "";
    const err = new Error(
      "MCP session_id never arrived on SSE — check POWERLOOM_MCP_URL, Authorization, and proxy. " +
        "If the server emits a non-URL session line, set POWERLOOM_BDS_MCP_DEBUG=1 and inspect hint in this message." +
        hint
    );
    err.code = "NO_SESSION";
    throw err;
  }

  const msgUrl = `${baseOrigin}/messages/?session_id=${sessionId}`;
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  };

  const rpc = async (id, method, params_) => {
    const r = await fetch(msgUrl, {
      method: "POST",
      headers,
      body: JSON.stringify({
        jsonrpc: "2.0",
        id,
        method,
        params: params_,
      }),
    });
    if (r.status === 401 || r.status === 402 || r.status === 429) {
      const txt = await r.text().catch(() => "");
      const err = new Error(`MCP POST HTTP ${r.status}: ${txt.slice(0, 300)}`);
      err.code = `HTTP_${r.status}`;
      err.httpStatus = r.status;
      throw err;
    }
    if (!r.ok) {
      const txt = await r.text().catch(() => "");
      const err = new Error(`MCP POST HTTP ${r.status}: ${txt.slice(0, 400)}`);
      err.code = "HTTP_ERROR";
      throw err;
    }
  };

  await rpc(1, "initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "powerloom-bds-univ3", version: "0.1.0" },
  });
  await new Promise((r) => setTimeout(r, 50));
  await fetch(msgUrl, {
    method: "POST",
    headers,
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "notifications/initialized",
    }),
  });
  await new Promise((r) => setTimeout(r, 50));

  async function teardown() {
    clearTimeout(timer);
    await reader.cancel().catch(() => {});
  }

  return { reader, decoder, buf, msgUrl, headers, rpc, timeoutMs, timer, teardown };
}

/**
 * Read SSE `data:` JSON lines until a JSON-RPC response with matching id (or timeout).
 */
async function readJsonRpcById(reader, decoder, bufRef, expectedId, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  let buf = bufRef;

  while (Date.now() < deadline) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const lines = buf.split("\n");
    buf = lines.pop() || "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const raw = line.slice(6).trim();
      if (!raw || raw === "[DONE]") continue;
      let j;
      try {
        j = JSON.parse(raw);
      } catch {
        continue;
      }
      if (j.id == null) continue;
      if (j.id !== expectedId) continue;
      if (j.error) {
        const err = new Error(
          typeof j.error.message === "string"
            ? j.error.message
            : JSON.stringify(j.error)
        );
        err.code = "JSONRPC_ERROR";
        err.jsonRpc = j.error;
        throw err;
      }
      return { result: j.result, buf };
    }
  }
  return { result: null, buf };
}

/**
 * List tool names from the live MCP server (same handshake as `callTool`).
 * Use this to prove which `bds_mpp_*` names the endpoint exposes — not guess `bds_univ3`.
 */
export async function listMcpTools() {
  const apiKey = powerloomApiKey();
  if (!apiKey) {
    const err = new Error(
      "POWERLOOM_API_KEY is not set. Sign up at https://bds-metering.powerloom.io (CLI) or https://bds-metering.powerloom.io/metering (browser) and export your API key."
    );
    err.code = "NO_API_KEY";
    throw err;
  }

  const { reader, decoder, buf: buf0, rpc, timeoutMs, teardown } =
    await connectMcpSession(apiKey);
  const listId = 2;
  await rpc(listId, "tools/list", {});

  try {
    const { result, buf } = await readJsonRpcById(
      reader,
      decoder,
      buf0,
      listId,
      timeoutMs
    );
    if (!result) {
      const err = new Error(
        "tools/list timed out — no JSON-RPC response with id 2 (check POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS)."
      );
      err.code = "TOOLS_LIST_TIMEOUT";
      throw err;
    }
    if (!Array.isArray(result.tools)) {
      const err = new Error(
        "tools/list returned unexpected shape — expected result.tools[]"
      );
      err.code = "TOOLS_LIST_SHAPE";
      throw err;
    }
    return result.tools.map((t) => (typeof t.name === "string" ? t.name : String(t?.name ?? "")));
  } finally {
    await teardown();
  }
}

/**
 * One MCP tools/call round-trip. Returns parsed JSON from tool result text (object).
 */
export async function callTool(toolName, params = {}) {
  const apiKey = powerloomApiKey();
  if (!apiKey) {
    const err = new Error(
      "POWERLOOM_API_KEY is not set. Sign up at https://bds-metering.powerloom.io (CLI) or https://bds-metering.powerloom.io/metering (browser) and export your API key."
    );
    err.code = "NO_API_KEY";
    throw err;
  }

  const { reader, decoder, buf: buf0, rpc, timeoutMs, timer, teardown } =
    await connectMcpSession(apiKey);
  const callId = 2;
  await rpc(callId, "tools/call", {
    name: toolName,
    arguments: params,
  });

  const deadline = Date.now() + timeoutMs;
  let buf = buf0;

  try {
    while (Date.now() < deadline) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split("\n");
      buf = lines.pop() || "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const raw = line.slice(6).trim();
        if (!raw || raw === "[DONE]") continue;
        let j;
        try {
          j = JSON.parse(raw);
        } catch {
          continue;
        }
        if (j.id == null) continue;
        if (j.id !== callId) continue;
        if (j.error) {
          const err = new Error(
            typeof j.error.message === "string"
              ? j.error.message
              : JSON.stringify(j.error)
          );
          err.code = "JSONRPC_ERROR";
          err.jsonRpc = j.error;
          throw err;
        }
        if (!j.result) continue;
        const r = j.result;
        if (r.isError && r.content && r.content[0]) {
          const err = new Error(String(r.content[0].text || "Tool error"));
          err.code = "TOOL_ERROR";
          err.isError = true;
          throw err;
        }
        const content = r.content;
        if (Array.isArray(content) && content[0]?.type === "text" && content[0].text) {
          const text = content[0].text.trim();
          try {
            clearTimeout(timer);
            return JSON.parse(text);
          } catch {
            clearTimeout(timer);
            return { _rawText: text };
          }
        }
        clearTimeout(timer);
        return r;
      }
    }
  } finally {
    clearTimeout(timer);
    await teardown();
  }

  const err = new Error(
    `Timeout waiting for MCP tools/call response after ${timeoutMs}ms (tool=${toolName}).`
  );
  err.code = "TOOL_TIMEOUT";
  throw err;
}
