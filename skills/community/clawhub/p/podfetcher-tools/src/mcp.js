#!/usr/bin/env node

import { parseArgs } from "node:util";
import { randomUUID } from "node:crypto";
import {
  createPodfetcherClient,
  isTranscriptReadyResponse,
  PodfetcherApiError,
} from "./sdk.js";

const TOOL_DEFINITIONS = [
  {
    name: "search_shows",
    description: "Search podcast shows by query.",
    inputSchema: {
      type: "object",
      properties: {
        q: { type: "string", description: "Search query string." },
        limit: { type: "integer", minimum: 1, maximum: 100 },
        cursor: { type: "string" },
      },
      required: ["q"],
      additionalProperties: false,
    },
  },
  {
    name: "list_episodes",
    description: "List episodes for a show with optional timeframe and paging filters.",
    inputSchema: {
      type: "object",
      properties: {
        showId: { type: "string" },
        since: { type: "string", description: "ISO-8601 timestamp." },
        from: { type: "string", description: "ISO-8601 start timestamp." },
        to: { type: "string", description: "ISO-8601 end timestamp." },
        orderBy: { type: "string", enum: ["publishedAt"] },
        order: { type: "string", enum: ["asc", "desc"] },
        limit: { type: "integer", minimum: 1, maximum: 100 },
        cursor: { type: "string" },
      },
      required: ["showId"],
      additionalProperties: false,
    },
  },
  {
    name: "fetch_transcript",
    description: "Fetch transcript for an episode. Can optionally wait for async processing.",
    inputSchema: {
      type: "object",
      properties: {
        episodeId: { type: "string" },
        wait: { type: "boolean", default: false },
        pollIntervalMs: { type: "integer", minimum: 100 },
        waitTimeoutMs: { type: "integer", minimum: 1000 },
        idempotencyKey: { type: "string" },
      },
      required: ["episodeId"],
      additionalProperties: false,
    },
  },
];

const parsed = parseArgs({
  args: process.argv.slice(2),
  options: {
    "base-url": { type: "string" },
    "api-key": { type: "string" },
    "api-key-header": { type: "string" },
    "timeout-ms": { type: "string" },
    help: { type: "boolean", short: "h", default: false },
  },
  allowPositionals: false,
});

if (parsed.values.help) {
  process.stdout.write(
    "Usage: podfetcher-mcp [--base-url URL] [--api-key KEY] [--api-key-header H] [--timeout-ms MS]\n",
  );
  process.exit(0);
}

const client = createPodfetcherClient({
  baseUrl: parsed.values["base-url"],
  apiKey: parsed.values["api-key"],
  apiKeyHeader: parsed.values["api-key-header"],
  timeoutMs: parsed.values["timeout-ms"] ? Number(parsed.values["timeout-ms"]) : undefined,
});

const PROTOCOL_VERSION = "2024-11-05";
let inputBuffer = Buffer.alloc(0);

process.stdin.on("data", (chunk) => {
  inputBuffer = Buffer.concat([inputBuffer, chunk]);
  drainIncomingMessages().catch((error) => {
    writeToStderr(`Failed to process message: ${error.stack || error.message}`);
  });
});

process.stdin.on("end", () => {
  process.exit(0);
});

async function drainIncomingMessages() {
  while (true) {
    const headerEndIndex = inputBuffer.indexOf("\r\n\r\n");
    if (headerEndIndex === -1) {
      return;
    }

    const headers = inputBuffer.subarray(0, headerEndIndex).toString("utf8");
    const lengthMatch = headers.match(/Content-Length:\s*(\d+)/i);
    if (!lengthMatch) {
      writeToStderr("Missing Content-Length header");
      inputBuffer = Buffer.alloc(0);
      return;
    }

    const contentLength = Number(lengthMatch[1]);
    const totalLength = headerEndIndex + 4 + contentLength;
    if (inputBuffer.length < totalLength) {
      return;
    }

    const payloadBuffer = inputBuffer.subarray(headerEndIndex + 4, totalLength);
    inputBuffer = inputBuffer.subarray(totalLength);

    let payload;
    try {
      payload = JSON.parse(payloadBuffer.toString("utf8"));
    } catch {
      writeToStderr("Invalid JSON payload");
      continue;
    }

    await handleMessage(payload);
  }
}

async function handleMessage(message) {
  if (!message || typeof message !== "object") {
    return;
  }
  if (typeof message.method !== "string") {
    return;
  }

  const { id, method, params } = message;
  const isRequest = id !== undefined && id !== null;

  if (!isRequest) {
    return;
  }

  try {
    const result = await handleRequest(method, params);
    sendJsonRpcResponse(id, result);
  } catch (error) {
    sendJsonRpcError(id, mapError(error));
  }
}

async function handleRequest(method, params) {
  switch (method) {
    case "initialize":
      return {
        protocolVersion: PROTOCOL_VERSION,
        capabilities: {
          tools: {},
        },
        serverInfo: {
          name: "podfetcher-mcp",
          version: "0.1.0",
        },
      };

    case "tools/list":
      return { tools: TOOL_DEFINITIONS };

    case "tools/call":
      return callTool(params);

    default:
      throw {
        jsonrpcError: {
          code: -32601,
          message: `Method not found: ${method}`,
        },
      };
  }
}

async function callTool(params) {
  const name = params?.name;
  const args = params?.arguments || {};

  try {
    switch (name) {
      case "search_shows": {
        const result = await client.searchShows({
          q: requireString(args.q, "q"),
          limit: optionalInt(args.limit, "limit"),
          cursor: optionalString(args.cursor),
        });
        return toToolResult(result);
      }

      case "list_episodes": {
        const result = await client.listEpisodes({
          showId: requireString(args.showId, "showId"),
          since: optionalString(args.since),
          from: optionalString(args.from),
          to: optionalString(args.to),
          orderBy: optionalString(args.orderBy),
          order: optionalString(args.order),
          limit: optionalInt(args.limit, "limit"),
          cursor: optionalString(args.cursor),
        });
        return toToolResult(result);
      }

      case "fetch_transcript": {
        const episodeId = requireString(args.episodeId, "episodeId");
        const wait = optionalBoolean(args.wait, false);
        const idempotencyKey = optionalString(args.idempotencyKey) || randomUUID();

        const result = wait
          ? await client.fetchTranscriptAndWait({
              episodeId,
              idempotencyKey,
              pollIntervalMs: optionalInt(args.pollIntervalMs, "pollIntervalMs", 1_000),
              waitTimeoutMs: optionalInt(args.waitTimeoutMs, "waitTimeoutMs", 60_000),
            })
          : await client.fetchTranscript({
              episodeId,
              idempotencyKey,
            });

        return toToolResult({
          ...result,
          ready: isTranscriptReadyResponse(result),
        });
      }

      default:
        return toToolErrorResult(`Unknown tool: ${String(name)}`);
    }
  } catch (error) {
    return toToolErrorResult(formatError(error), error);
  }
}

function toToolResult(payload) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(payload, null, 2),
      },
    ],
    structuredContent: payload,
    isError: false,
  };
}

function toToolErrorResult(message, error) {
  const structuredContent = {
    error: {
      message,
    },
  };

  if (error instanceof PodfetcherApiError) {
    structuredContent.error.status = error.status;
    structuredContent.error.code = error.code;
    structuredContent.error.details = error.details;
  }

  return {
    content: [
      {
        type: "text",
        text: message,
      },
    ],
    structuredContent,
    isError: true,
  };
}

function sendJsonRpcResponse(id, result) {
  writeFramedJson({
    jsonrpc: "2.0",
    id,
    result,
  });
}

function sendJsonRpcError(id, error) {
  writeFramedJson({
    jsonrpc: "2.0",
    id,
    error,
  });
}

function writeFramedJson(payload) {
  const body = JSON.stringify(payload);
  const header = `Content-Length: ${Buffer.byteLength(body, "utf8")}\r\n\r\n`;
  process.stdout.write(header);
  process.stdout.write(body);
}

function mapError(error) {
  if (error?.jsonrpcError) {
    return error.jsonrpcError;
  }
  return {
    code: -32603,
    message: error?.message || "Internal error",
  };
}

function formatError(error) {
  if (error instanceof PodfetcherApiError) {
    const base = `[HTTP ${error.status}] ${error.code || "API_ERROR"}: ${error.message}`;
    if (!error.details) {
      return base;
    }
    const details = Object.entries(error.details)
      .map(([k, v]) => `${k}=${v}`)
      .join(", ");
    return `${base} (${details})`;
  }
  return error?.message || String(error);
}

function requireString(value, name) {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`Argument '${name}' must be a non-empty string`);
  }
  return value;
}

function optionalString(value) {
  if (value === undefined || value === null) {
    return undefined;
  }
  if (typeof value !== "string") {
    throw new Error("Expected string value");
  }
  return value;
}

function optionalInt(value, name, fallback) {
  if (value === undefined || value === null) {
    return fallback;
  }
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`Argument '${name}' must be a positive integer`);
  }
  return parsed;
}

function optionalBoolean(value, fallback) {
  if (value === undefined || value === null) {
    return fallback;
  }
  if (typeof value === "boolean") {
    return value;
  }
  if (value === "true") {
    return true;
  }
  if (value === "false") {
    return false;
  }
  throw new Error("Expected boolean value");
}

function writeToStderr(message) {
  process.stderr.write(`${message}\n`);
}
