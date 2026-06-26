/**
 * mcp-client.js — PredicTradar MCP HTTP client
 *
 * Provides shared access to prediction market data over the MCP protocol.
 *
 * Benefits:
 * - No direct database connection management
 * - Shared HTTP entry point with quota handling
 * - High-level tools plus preview SQL queries and stream exports
 * - Automatic session handshake, retries, and error handling
 *
 * Usage:
 *   const mcp = require('../../polymarket-data-layer/scripts/mcp-client');
 *
 *   // High-level tools
 *   const traders = await mcp.callTool('get_traders', { sortBy: 'pnl_7d', limit: 10 });
 *   const stats = await mcp.callTool('get_market_stats', { period: '24h' });
 *
 *   // Preview SQL query
 *   const rows = await mcp.query('SELECT count(*) FROM trades WHERE traded_at >= now() - INTERVAL 1 DAY');
 *
 *   // Health check
 *   const ok = await mcp.ping();
 */

"use strict";

// Configuration
const MCP_BASE_URL = process.env.MCP_URL || "https://api.predictradar.ai";
const MCP_API_KEY = process.env.MCP_API_KEY || "pr_public_predictradar";
const MCP_SESSION_HEADER = "mcp-session-id";
const MCP_NETWORK_RETRIES = 2;

let requestId = 0;
let sessionState = {
  sessionId: null,
  initialized: false,
  serverInfo: null,
  initializeResult: null,
};

// HTTP helpers
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function getRetryDelayMs(attempt) {
  return 500 * attempt;
}

function isTransientNetworkError(error) {
  const message = String(error?.message || "").toLowerCase();
  const causeCode = String(error?.cause?.code || "").toUpperCase();

  if (causeCode) {
    return [
      "ECONNRESET",
      "ECONNREFUSED",
      "ETIMEDOUT",
      "ECONNABORTED",
      "EPIPE",
      "EAI_AGAIN",
      "ENETUNREACH",
      "UND_ERR_CONNECT_TIMEOUT",
      "UND_ERR_SOCKET",
    ].includes(causeCode);
  }

  return (
    message.includes("fetch failed") ||
    message.includes("socket disconnected") ||
    message.includes("networkerror") ||
    message.includes("network error")
  );
}

async function withNetworkRetry(fn, { retries = MCP_NETWORK_RETRIES } = {}) {
  let lastError;

  for (let attempt = 1; attempt <= retries + 1; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (attempt > retries || !isTransientNetworkError(error)) {
        throw error;
      }
      await sleep(getRetryDelayMs(attempt));
    }
  }

  throw lastError;
}

async function httpPost(
  endpoint,
  body,
  { timeout = 60_000, headers = {} } = {},
) {
  const url = `${MCP_BASE_URL}${endpoint}`;

  return withNetworkRetry(async () => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": MCP_API_KEY,
          ...headers,
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(
          `MCP HTTP ${response.status}: ${errorBody.slice(0, 200)}`,
        );
      }

      const text = await response.text();

      return {
        status: response.status,
        headers: response.headers,
        body: text ? JSON.parse(text) : null,
      };
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === "AbortError") {
        throw new Error(`MCP request timeout (${timeout}ms)`);
      }
      throw error;
    }
  });
}

// MCP JSON-RPC helpers

function resetSession() {
  sessionState = {
    sessionId: null,
    initialized: false,
    serverInfo: null,
    initializeResult: null,
  };
}

function getSessionHeaders() {
  return sessionState.sessionId
    ? { [MCP_SESSION_HEADER]: sessionState.sessionId }
    : {};
}

function shouldRetryWithFreshSession(error) {
  const message = error?.message || "";
  return (
    message.includes("session is required") ||
    message.includes("session not found") ||
    message.includes("handshake incomplete")
  );
}

async function sendRpc(
  method,
  params = {},
  { timeout = 60_000, headers = {} } = {},
) {
  const response = await httpPost(
    "/api/mcp/v2",
    {
      jsonrpc: "2.0",
      id: ++requestId,
      method,
      params,
    },
    { timeout, headers },
  );

  return response;
}

async function sendNotification(
  method,
  params = {},
  { timeout = 60_000, headers = {} } = {},
) {
  return httpPost(
    "/api/mcp/v2",
    {
      jsonrpc: "2.0",
      method,
      params,
    },
    { timeout, headers },
  );
}

async function ensureSession({ force = false, timeout = 60_000 } = {}) {
  if (!force && sessionState.sessionId && sessionState.initialized) {
    return sessionState;
  }

  if (force) {
    resetSession();
  }

  const initResponse = await sendRpc(
    "initialize",
    {
      protocolVersion: "2025-03-26",
      capabilities: { batch: { enabled: true } },
      clientInfo: { name: "polymarket-data-layer-skill", version: "1.0.0" },
    },
    { timeout },
  );

  const sessionId = initResponse.headers.get(MCP_SESSION_HEADER);
  if (!sessionId) {
    throw new Error("MCP initialize did not return mcp-session-id");
  }

  if (initResponse.body?.error) {
    const err = new Error(
      initResponse.body.error.message || "MCP initialize failed",
    );
    err.code = initResponse.body.error.code;
    err.data = initResponse.body.error.data;
    throw err;
  }

  sessionState.sessionId = sessionId;
  sessionState.serverInfo = initResponse.body?.result?.serverInfo || null;
  sessionState.initializeResult = initResponse.body?.result || null;

  await sendNotification(
    "notifications/initialized",
    {},
    {
      timeout,
      headers: getSessionHeaders(),
    },
  );

  sessionState.initialized = true;
  return sessionState;
}

/**
 * Send MCP JSON-RPC request
 * @param {string} method - JSON-RPC method name
 * @param {object} params - Method parameters
 * @param {object} options - Request options
 * @returns {Promise<any>} - Response result
 */
async function rpc(method, params = {}, { timeout = 60_000 } = {}) {
  const sessionRequired = ![
    "initialize",
    "notifications/initialized",
    "ping",
  ].includes(method);

  if (sessionRequired) {
    await ensureSession({ timeout });
  }

  let response = await sendRpc(method, params, {
    timeout,
    headers: sessionRequired ? getSessionHeaders() : {},
  });

  if (response.body?.error) {
    const err = new Error(response.body.error.message || "MCP RPC Error");
    err.code = response.body.error.code;
    err.data = response.body.error.data;

    if (sessionRequired && shouldRetryWithFreshSession(err)) {
      await ensureSession({ force: true, timeout });
      response = await sendRpc(method, params, {
        timeout,
        headers: getSessionHeaders(),
      });
    }
  }

  if (response.body?.error) {
    const err = new Error(response.body.error.message || "MCP RPC Error");
    err.code = response.body.error.code;
    err.data = response.body.error.data;
    throw err;
  }

  return response.body.result;
}

// Core API

/**
 * Initialize an MCP session and complete the required handshake.
 * @returns {Promise<object>} Server capabilities plus the session id
 */
async function initialize() {
  const session = await ensureSession({ force: true });
  return {
    ...session.initializeResult,
    sessionId: session.sessionId,
  };
}

/**
 * List available MCP tools.
 * @returns {Promise<object[]>} Tool definitions
 */
async function listTools() {
  const result = await rpc("tools/list");
  return result.tools || [];
}

/**
 * Call an MCP tool.
 * @param {string} name Tool name
 * @param {object} args Tool arguments
 * @param {object} options Request options
 * @returns {Promise<any>} Parsed tool result
 */
async function callTool(
  name,
  args = {},
  { timeout = 60_000, raw = false } = {},
) {
  const result = await rpc(
    "tools/call",
    { name, arguments: args },
    { timeout },
  );

  if (result.isError) {
    const content = result.content?.[0]?.text || "Unknown error";
    throw new Error(`Tool "${name}" failed: ${content}`);
  }

  // Parse the first text content as JSON by default
  if (!raw && result.content?.[0]?.type === "text") {
    try {
      return JSON.parse(result.content[0].text);
    } catch (_) {
      return result.content[0].text;
    }
  }

  return result;
}

/**
 * Run a preview-only SQL query.
 * Uses the current `run_query_preview` tool and returns a limited row set.
 * @param {string} sql Read-only SQL query
 * @param {object} options Query options
 * @returns {Promise<object[]>} Result rows
 */
async function query(sql, { maxRows = 100, timeout = 60_000, metadata } = {}) {
  const result = await callTool(
    "run_query_preview",
    { query: sql, maxRows, metadata },
    { timeout },
  );
  return result.rows || [];
}

/**
 * Retry wrapper for preview SQL queries.
 * @param {string} sql Read-only SQL query
 * @param {object} options Query options
 * @returns {Promise<object[]>} Result rows
 */
async function queryWithRetry(
  sql,
  { maxRows = 100, timeout = 60_000, retries = 3, metadata } = {},
) {
  for (let i = 0; i < retries; i++) {
    try {
      return await query(sql, { maxRows, timeout, metadata });
    } catch (e) {
      if (i < retries - 1) {
        await new Promise((r) => setTimeout(r, 2000 * (i + 1)));
      } else {
        throw e;
      }
    }
  }
}

function extractStreamToken(streamUrl) {
  const parts = String(streamUrl || "")
    .split("/")
    .filter(Boolean);
  return parts[parts.length - 1] || null;
}

function parseNdjson(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

async function openQueryStream(
  sql,
  {
    format = "ndjson",
    previewRows = 5,
    timeoutMs,
    timeout = 60_000,
    metadata,
  } = {},
) {
  return callTool(
    "open_query_stream",
    {
      query: sql,
      format,
      previewRows,
      timeoutMs,
      metadata,
    },
    { timeout },
  );
}

async function consumeQueryStream(
  streamUrl,
  { timeout = 60_000, raw = false } = {},
) {
  return withNetworkRetry(async () => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(streamUrl, {
        method: "GET",
        headers: {
          "X-API-Key": MCP_API_KEY,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(
          `MCP stream HTTP ${response.status}: ${errorBody.slice(0, 200)}`,
        );
      }

      const contentType = response.headers.get("content-type") || "";
      const text = await response.text();

      if (raw) {
        return { contentType, raw: text };
      }

      if (contentType.includes("application/x-ndjson")) {
        return {
          contentType,
          rows: parseNdjson(text),
        };
      }

      return {
        contentType,
        raw: text,
      };
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === "AbortError") {
        throw new Error(`MCP stream timeout (${timeout}ms)`);
      }
      throw error;
    }
  });
}

async function cancelQueryStream(streamUrl, { timeout = 30_000 } = {}) {
  const token = extractStreamToken(streamUrl);
  if (!token) {
    throw new Error("Invalid streamUrl: missing token");
  }

  return withNetworkRetry(async () => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(`${MCP_BASE_URL}/api/query/streams/${token}`, {
        method: "DELETE",
        headers: {
          "X-API-Key": MCP_API_KEY,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(
          `MCP cancel stream HTTP ${response.status}: ${errorBody.slice(0, 200)}`,
        );
      }

      return true;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === "AbortError") {
        throw new Error(`MCP cancel stream timeout (${timeout}ms)`);
      }
      throw error;
    }
  });
}

async function queryStream(
  sql,
  {
    format = "ndjson",
    previewRows = 5,
    timeoutMs,
    timeout = 60_000,
    raw = false,
    metadata,
  } = {},
) {
  const opened = await openQueryStream(sql, {
    format,
    previewRows,
    timeoutMs,
    timeout,
    metadata,
  });

  const consumed = await consumeQueryStream(opened.streamUrl, {
    timeout,
    raw,
  });

  return {
    ...opened,
    ...consumed,
  };
}

/**
 * List available data tables.
 * @param {string} category Optional category filter
 * @returns {Promise<object[]>} Table metadata
 */
async function listTables(category = "all") {
  const result = await callTool("list_tables", { category });
  return result.tables || [];
}

/**
 * Describe a table schema.
 * @param {string} tableName Table name
 * @param {boolean} includeExample Whether to include sample rows
 * @returns {Promise<object>} Table schema metadata
 */
async function describeTable(tableName, includeExample = false) {
  return callTool("describe_table", { tableName, includeExample });
}

/**
 * Lightweight ping check.
 * @param {number} timeoutMs Timeout in milliseconds
 * @returns {Promise<boolean>} Whether the server is reachable
 */
async function ping(timeoutMs = 5000) {
  try {
    await rpc("ping", {}, { timeout: timeoutMs });
    return true;
  } catch (_) {
    return false;
  }
}

/**
 * Read the REST health endpoint.
 * @returns {Promise<object|null>} Health payload or null
 */
async function health() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${MCP_BASE_URL}/api/mcp/health`, {
      headers: { "X-API-Key": MCP_API_KEY },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    return response.ok ? await response.json() : null;
  } catch (_) {
    return null;
  }
}

// High-level tool wrappers

/**
 * Get traders with sorting and pagination.
 * @param {object} options Query options
 * @returns {Promise<object>} Trader list payload
 */
async function getTraders({
  sortBy = "pnl_7d",
  order = "desc",
  limit = 20,
  offset = 0,
} = {}) {
  return callTool("get_traders", { sortBy, order, limit, offset });
}

/**
 * Get trader detail for a wallet.
 * @param {string} address Wallet address
 * @returns {Promise<object>} Trader detail payload
 */
async function getTraderDetail(address) {
  return callTool("get_trader_detail", { address });
}

/**
 * Get a leaderboard.
 * @param {object} options Query options
 * @returns {Promise<object>} Leaderboard payload
 */
async function getLeaderboard({
  period = "7d",
  rankBy = "pnl",
  limit = 20,
} = {}) {
  return callTool("get_leaderboard", { period, rankBy, limit });
}

/**
 * Get aggregate market statistics.
 * @param {string} period Statistics period
 * @returns {Promise<object>} Market statistics
 */
async function getMarketStats(period = "24h") {
  return callTool("get_market_stats", { period });
}

/**
 * Get markets with filtering and search.
 * @param {object} options Query options
 * @returns {Promise<object>} Market list payload
 */
async function getMarkets({
  status = "active",
  search,
  limit = 20,
  offset = 0,
} = {}) {
  const args = { status, limit, offset };
  if (search) args.search = search;
  return callTool("get_markets", args);
}

/**
 * Get detailed market information for a single condition id.
 * @param {string} conditionId Market condition id
 * @returns {Promise<object>} Market detail payload
 */
async function getMarketDetail(conditionId) {
  return callTool("get_market_detail", { conditionId });
}

/**
 * Search events.
 * @param {object} options Search options
 * @returns {Promise<object>} Event search payload
 */
async function searchEvents({
  query: q,
  category,
  status = "active",
  limit = 10,
} = {}) {
  const args = { status, limit };
  if (q) args.query = q;
  if (category) args.category = category;
  return callTool("search_events", args);
}

// Exports
module.exports = {
  // Core methods
  rpc,
  initialize,
  listTools,
  callTool,

  // SQL queries
  query,
  queryWithRetry,
  openQueryStream,
  consumeQueryStream,
  cancelQueryStream,
  queryStream,
  listTables,
  describeTable,

  // Health check
  ping,
  health,

  // High-level tool shortcuts
  getTraders,
  getTraderDetail,
  getLeaderboard,
  getMarketStats,
  getMarkets,
  getMarketDetail,
  searchEvents,

  // Configuration
  MCP_BASE_URL,
  MCP_API_KEY,
  MCP_SESSION_HEADER,
  resetSession,
};
