import { randomUUID } from "node:crypto";
import { pathToFileURL } from "node:url";

export const EXIT_HTTP = 1;
export const EXIT_ARGUMENT = 2;
export const DEFAULT_TIMEOUT_MS = 90_000;
export const LONG_TIMEOUT_MS = 120_000;
export const DEFAULT_MAX_ATTEMPTS = 3;
export const SOURCE = `${process.platform}-openclaw-paper-schema`;
export const MAX_INPUT_BYTES = 1_000_000;
export const MAX_RESPONSE_BYTES = 16 * 1024 * 1024;
export const MAX_ERROR_BYTES = 64 * 1024;

const RETRYABLE_STATUS = new Set([429, 502, 503, 504]);
const PUBLIC_PATHS = [
  /^\/paper-schema$/,
  /^\/paper-schema\/(search|entities\/related-papers|entities\/search|relations\/search|evidence\/search|resolve-provenance|search-in-schema|hydrate-items|materials)$/,
  /^\/paper-schema\/schemas\/[^/]+\/(related-papers|entities|citation-summary|citations|citation-graph)$/,
  /^\/paper-schema\/schemas\/[^/]+\/(entities|relations|evidence)\/[^/]+$/,
];

export class ToolError extends Error {
  constructor(message, options = {}) {
    super(message);
    this.name = "ToolError";
    this.code = options.code ?? "TOOL_ERROR";
    this.exitCode = options.exitCode ?? EXIT_ARGUMENT;
    this.status = options.status;
    this.requestId = options.requestId;
    this.retryable = options.retryable ?? false;
    this.attempt = options.attempt;
    this.details = options.details;
  }
}

export function isMain(importMetaUrl) {
  return Boolean(process.argv[1]) && importMetaUrl === pathToFileURL(process.argv[1]).href;
}

export function failArgument(message, details) {
  throw new ToolError(message, { code: "INVALID_ARGUMENT", exitCode: EXIT_ARGUMENT, details });
}

export function readJsonArg(argv = process.argv) {
  const raw = argv[2] ?? "{}";
  if (new TextEncoder().encode(raw).byteLength > MAX_INPUT_BYTES) {
    failArgument(`Input JSON must be at most ${MAX_INPUT_BYTES} bytes.`);
  }
  let value;
  try {
    value = JSON.parse(raw);
  } catch {
    failArgument("Input must be valid JSON.");
  }
  return requireObject(value, "input");
}

export function requireObject(value, name) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    failArgument(`${name} must be an object.`);
  }
  return value;
}

export function requireString(value, name, { max = 600 } = {}) {
  if (typeof value !== "string" || value.trim().length === 0) {
    failArgument(`${name} must be a non-empty string.`);
  }
  if (value.length > max) failArgument(`${name} must be at most ${max} characters.`);
  return value;
}

export function optionalString(value, name, options) {
  return value === undefined || value === null ? undefined : requireString(value, name, options);
}

export function requireEnum(value, name, allowed) {
  if (!allowed.includes(value)) {
    failArgument(`${name} must be one of: ${allowed.join(", ")}.`);
  }
  return value;
}

export function optionalBoolean(value, name) {
  if (value === undefined || value === null) return undefined;
  if (typeof value !== "boolean") failArgument(`${name} must be a boolean.`);
  return value;
}

export function optionalInteger(value, name, { min, max } = {}) {
  if (value === undefined || value === null) return undefined;
  if (!Number.isInteger(value)) failArgument(`${name} must be an integer.`);
  if (min !== undefined && value < min) failArgument(`${name} must be at least ${min}.`);
  if (max !== undefined && value > max) failArgument(`${name} must be at most ${max}.`);
  return value;
}

export function optionalStringArray(value, name, { max = 100 } = {}) {
  if (value === undefined || value === null) return undefined;
  if (!Array.isArray(value) || value.some((item) => typeof item !== "string" || !item.trim())) {
    failArgument(`${name} must be an array of non-empty strings.`);
  }
  if (value.length > max) failArgument(`${name} must contain at most ${max} items.`);
  return value;
}

export function ensureAllowedKeys(value, allowed, name = "input") {
  const unknown = Object.keys(requireObject(value, name)).filter((key) => !allowed.includes(key));
  if (unknown.length) failArgument(`${name} contains unsupported fields: ${unknown.join(", ")}.`);
}

export function encodePathSegment(value, name) {
  return encodeURIComponent(requireString(value, name));
}

export function pickDefined(value, keys) {
  return Object.fromEntries(keys.filter((key) => value[key] !== undefined).map((key) => [key, value[key]]));
}

export function validateBaseUrl(raw = process.env.SCIVERSE_BASE_URL ?? "https://api.sciverse.space") {
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new ToolError("SCIVERSE_BASE_URL must be a valid URL.", { code: "INVALID_BASE_URL", exitCode: EXIT_ARGUMENT });
  }
  const hostname = url.hostname.toLowerCase();
  if (url.protocol !== "https:" || (hostname !== "sciverse.space" && !hostname.endsWith(".sciverse.space"))) {
    throw new ToolError("SCIVERSE_BASE_URL must use HTTPS and point to sciverse.space or a subdomain.", { code: "INVALID_BASE_URL", exitCode: EXIT_ARGUMENT });
  }
  if (url.username || url.password || (url.port && url.port !== "443") || (url.pathname && url.pathname !== "/") || url.search || url.hash) {
    throw new ToolError("SCIVERSE_BASE_URL must not include credentials, a custom port, a path, a query, or a fragment.", { code: "INVALID_BASE_URL", exitCode: EXIT_ARGUMENT });
  }
  return `${url.protocol}//${url.hostname}`;
}

export function buildUrl(baseUrl, path, query = {}) {
  if (typeof path !== "string" || path.includes("..") || !PUBLIC_PATHS.some((pattern) => pattern.test(path))) {
    failArgument("The requested path is not part of the public Paper Schema contract.");
  }
  const url = new URL(`${baseUrl}${path}`);
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null) continue;
    if (Array.isArray(value)) {
      for (const item of value) url.searchParams.append(key, String(item));
    } else {
      url.searchParams.set(key, String(value));
    }
  }
  return url;
}

function parseRetryAfter(value, now = Date.now()) {
  if (!value) return undefined;
  const seconds = Number(value);
  if (Number.isFinite(seconds) && seconds >= 0) return seconds * 1000;
  const date = Date.parse(value);
  return Number.isFinite(date) ? Math.max(0, date - now) : undefined;
}

function retryDelay(attempt, retryAfter, random = Math.random) {
  if (retryAfter !== undefined) return Math.min(retryAfter, 30_000);
  const base = Math.min(500 * 2 ** (attempt - 1), 8_000);
  return Math.round(base * (0.75 + random() * 0.5));
}

const defaultSleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function readResponseText(response, maxBytes) {
  const contentLength = Number(response.headers.get("content-length"));
  if (Number.isFinite(contentLength) && contentLength > maxBytes) {
    throw new ToolError("Sciverse API response exceeded the client size limit.", {
      code: "RESPONSE_TOO_LARGE",
      exitCode: EXIT_HTTP,
      status: response.status,
    });
  }
  if (!response.body) return "";
  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    total += value.byteLength;
    if (total > maxBytes) {
      await reader.cancel();
      throw new ToolError("Sciverse API response exceeded the client size limit.", {
        code: "RESPONSE_TOO_LARGE",
        exitCode: EXIT_HTTP,
        status: response.status,
      });
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return new TextDecoder().decode(bytes);
}

function safeErrorDetails(text) {
  try {
    const parsed = JSON.parse(text);
    const source = parsed?.detail && typeof parsed.detail === "object" ? parsed.detail : parsed;
    const details = {};
    if (typeof source?.code === "string" && /^[A-Z0-9_.-]{1,100}$/i.test(source.code)) details.upstream_code = source.code;
    if (typeof source?.retry_after === "number" && Number.isFinite(source.retry_after)) details.retry_after = source.retry_after;
    if (typeof source?.retry_after === "string" && /^\d{1,6}$/.test(source.retry_after)) details.retry_after = source.retry_after;
    return Object.keys(details).length ? details : undefined;
  } catch {
    return undefined;
  }
}

export async function callSciverse(method, path, options = {}) {
  if (!["GET", "POST"].includes(method)) failArgument("Only GET and POST are supported.");
  const token = options.token ?? process.env.SCIVERSE_API_TOKEN;
  if (!token) {
    throw new ToolError("SCIVERSE_API_TOKEN is not set.", { code: "TOKEN_MISSING", exitCode: EXIT_ARGUMENT });
  }
  const baseUrl = validateBaseUrl(options.baseUrl);
  const fetchImpl = options.fetchImpl ?? globalThis.fetch;
  const sleep = options.sleep ?? defaultSleep;
  const random = options.random ?? Math.random;
  const maxAttempts = options.maxAttempts ?? DEFAULT_MAX_ATTEMPTS;
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const url = buildUrl(baseUrl, path, options.query);

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    const requestId = randomUUID();
    let response;
    try {
      const headers = {
        accept: "application/json",
        authorization: `Bearer ${token}`,
        "x-request-id": requestId,
        "x-sciverse-source": SOURCE,
      };
      const init = { method, headers, signal: controller.signal, redirect: "error" };
      if (options.body !== undefined) {
        headers["content-type"] = "application/json";
        init.body = JSON.stringify(options.body);
      }
      response = await fetchImpl(url, init);
    } catch (error) {
      clearTimeout(timer);
      const timedOut = error?.name === "AbortError";
      if (attempt < maxAttempts) {
        await sleep(retryDelay(attempt, undefined, random));
        continue;
      }
      throw new ToolError(timedOut ? "Sciverse request timed out." : "Sciverse request failed.", {
        code: timedOut ? "REQUEST_TIMEOUT" : "NETWORK_ERROR",
        exitCode: EXIT_HTTP,
        retryable: true,
        attempt,
        requestId,
      });
    }

    const responseRequestId = response.headers.get("x-request-id") ?? requestId;
    let responseText;
    try {
      responseText = await readResponseText(response, response.ok ? MAX_RESPONSE_BYTES : MAX_ERROR_BYTES);
    } catch (error) {
      clearTimeout(timer);
      if (error instanceof ToolError) throw error;
      const timedOut = error?.name === "AbortError";
      if (attempt < maxAttempts) {
        await sleep(retryDelay(attempt, undefined, random));
        continue;
      }
      throw new ToolError(timedOut ? "Sciverse response timed out." : "Sciverse response stream failed.", {
        code: timedOut ? "REQUEST_TIMEOUT" : "NETWORK_ERROR",
        exitCode: EXIT_HTTP,
        retryable: true,
        attempt,
        requestId: responseRequestId,
      });
    }
    clearTimeout(timer);
    if (!response.ok) {
      const retryable = RETRYABLE_STATUS.has(response.status);
      if (retryable && attempt < maxAttempts) {
        const retryAfter = parseRetryAfter(response.headers.get("retry-after"));
        await sleep(retryDelay(attempt, retryAfter, random));
        continue;
      }
      throw new ToolError(`Sciverse API returned HTTP ${response.status}.`, {
        code: "HTTP_ERROR",
        exitCode: EXIT_HTTP,
        status: response.status,
        retryable,
        attempt,
        requestId: responseRequestId,
        details: safeErrorDetails(responseText),
      });
    }

    try {
      return JSON.parse(responseText);
    } catch {
      throw new ToolError("Sciverse API returned invalid JSON.", {
        code: "INVALID_RESPONSE",
        exitCode: EXIT_HTTP,
        status: response.status,
        requestId: responseRequestId,
      });
    }
  }
  throw new ToolError("Sciverse request exhausted retries.", { code: "RETRY_EXHAUSTED", exitCode: EXIT_HTTP });
}

export async function runTool(handler) {
  try {
    const result = await handler();
    process.stdout.write(`${JSON.stringify(result)}\n`);
  } catch (error) {
    const toolError = error instanceof ToolError
      ? error
      : new ToolError("Unexpected tool failure.", { code: "UNEXPECTED_ERROR", exitCode: EXIT_HTTP });
    const payload = {
      error: {
        code: toolError.code,
        message: toolError.message,
        ...(toolError.status !== undefined ? { status: toolError.status } : {}),
        ...(toolError.requestId ? { request_id: toolError.requestId } : {}),
        retryable: toolError.retryable,
        ...(toolError.attempt !== undefined ? { attempt: toolError.attempt } : {}),
        ...(toolError.details !== undefined ? { details: toolError.details } : {}),
      },
    };
    process.stderr.write(`${JSON.stringify(payload)}\n`);
    process.exitCode = toolError.exitCode;
  }
}
