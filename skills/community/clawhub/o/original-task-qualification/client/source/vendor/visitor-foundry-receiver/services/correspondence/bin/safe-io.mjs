import {
  closeSync,
  existsSync,
  fsyncSync,
  lstatSync,
  mkdirSync,
  openSync,
  readFileSync,
  renameSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname, parse, resolve } from "node:path";

export const RESPONSE_MAX_BYTES = 64 * 1024;
export const REQUEST_MAX_BYTES = 32 * 1024;
export const REQUEST_TIMEOUT_MS = 10_000;

function assertNoSymlinkComponents(inputPath) {
  const absolute = resolve(inputPath);
  const { root } = parse(absolute);
  const parts = absolute.slice(root.length).split(/[\\/]+/).filter(Boolean);
  let current = root;
  for (const part of parts) {
    current = resolve(current, part);
    let stat;
    try {
      stat = lstatSync(current);
    } catch (error) {
      if (error?.code === "ENOENT") break;
      throw error;
    }
    if (stat.isSymbolicLink()) {
      throw new Error(`refusing symlink path: ${absolute}`);
    }
  }
  return absolute;
}

function assertPrivateRegularFile(inputPath) {
  const absolute = assertNoSymlinkComponents(inputPath);
  const stat = lstatSync(absolute);
  if (!stat.isFile()) throw new Error(`refusing non-regular private file: ${absolute}`);
  if ((stat.mode & 0o077) !== 0) throw new Error(`private file permissions must be 0600: ${absolute}`);
  return absolute;
}

function preparePrivateParent(inputPath) {
  const absolute = resolve(inputPath);
  assertNoSymlinkComponents(dirname(absolute));
  mkdirSync(dirname(absolute), { recursive: true, mode: 0o700 });
  assertNoSymlinkComponents(dirname(absolute));
  return absolute;
}

export function inspectPrivateDestination(inputPath) {
  const absolute = preparePrivateParent(inputPath);
  assertNoSymlinkComponents(absolute);
  try {
    assertPrivateRegularFile(absolute);
    return { path: absolute, exists: true };
  } catch (error) {
    if (error?.code === "ENOENT") return { path: absolute, exists: false };
    throw error;
  }
}

function exclusiveWrite(inputPath, contents) {
  const absolute = preparePrivateParent(inputPath);
  assertNoSymlinkComponents(absolute);
  let fd;
  try {
    fd = openSync(absolute, "wx", 0o600);
    writeFileSync(fd, contents, { encoding: "utf8" });
    fsyncSync(fd);
  } catch (error) {
    if (fd !== undefined) {
      closeSync(fd);
      try {
        unlinkSync(absolute);
      } catch {
        // Preserve the original write error.
      }
    }
    throw error;
  }
  closeSync(fd);
  assertPrivateRegularFile(absolute);
  return absolute;
}

export function readPrivateSecret(inputPath, minimumLength = 16) {
  if (!inputPath) throw new Error("token file path required");
  const absolute = assertPrivateRegularFile(inputPath);
  const value = readFileSync(absolute, "utf8").trim();
  if (!value || value.length < minimumLength) throw new Error(`refusing empty/short secret file: ${absolute}`);
  return value;
}

export function writeSecretNoClobber(inputPath, value) {
  const destination = inspectPrivateDestination(inputPath);
  const absolute = destination.path;
  if (destination.exists) {
    const current = readPrivateSecret(absolute);
    if (current !== value) throw new Error(`refusing to overwrite existing secret file: ${absolute}`);
    return absolute;
  }
  return exclusiveWrite(absolute, `${value}\n`);
}

export function readPrivateJson(inputPath) {
  const absolute = resolve(inputPath);
  if (!existsSync(absolute)) return null;
  assertPrivateRegularFile(absolute);
  return JSON.parse(readFileSync(absolute, "utf8"));
}

export function writeJsonNoClobber(inputPath, value) {
  return exclusiveWrite(inputPath, `${JSON.stringify(value, null, 2)}\n`);
}

export function replacePrivateJson(inputPath, value) {
  const absolute = preparePrivateParent(inputPath);
  if (existsSync(absolute)) assertPrivateRegularFile(absolute);
  const temporary = `${absolute}.tmp-${process.pid}-${Date.now()}`;
  exclusiveWrite(temporary, `${JSON.stringify(value, null, 2)}\n`);
  try {
    renameSync(temporary, absolute);
  } catch (error) {
    try {
      unlinkSync(temporary);
    } catch {
      // Preserve the original rename error.
    }
    throw error;
  }
  assertPrivateRegularFile(absolute);
  return absolute;
}

export async function withPrivateLock(inputPath, operation) {
  const lockPath = `${resolve(inputPath)}.lock`;
  try {
    exclusiveWrite(lockPath, `${process.pid}\n`);
  } catch (error) {
    if (error?.code === "EEXIST") throw new Error(`another operator command holds the lock: ${lockPath}`);
    throw error;
  }
  try {
    return await operation();
  } finally {
    unlinkSync(lockPath);
  }
}

const PATH_SEGMENT = /^[A-Za-z0-9._~-]+$/;

export function canonicalOperatorOrigin(baseUrl, label = "base-url") {
  let url;
  try {
    url = new URL(baseUrl);
  } catch {
    throw new Error(`${label} must be a canonical origin without userinfo, query, or fragment`);
  }
  if (url.username || url.password || url.search || url.hash) {
    throw new Error(`${label} must be a canonical origin without userinfo, query, or fragment`);
  }
  const https = url.protocol === "https:";
  const loopbackHttp =
    url.protocol === "http:" && (url.hostname === "127.0.0.1" || url.hostname === "localhost");
  if (!https && !loopbackHttp) {
    throw new Error(`${label} must be https://… or http://127.0.0.1|localhost`);
  }
  const pathname = url.pathname || "/";
  if (pathname === "/") return url.origin;
  const trimmed = pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;
  const segments = trimmed.startsWith("/") ? trimmed.slice(1).split("/") : [trimmed];
  if (segments.length === 0 || segments.some((segment) => !PATH_SEGMENT.test(segment))) {
    throw new Error(
      `${label} must be a canonical origin without userinfo, query, fragment, or invalid path segments`,
    );
  }
  return `${url.origin}${trimmed}`;
}

async function boundedResponseText(response, maximumBytes) {
  if (!response.body) return "";
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let bytes = 0;
  let output = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    bytes += value.byteLength;
    if (bytes > maximumBytes) {
      await reader.cancel();
      throw new Error(`server response exceeded ${maximumBytes} bytes`);
    }
    output += decoder.decode(value, { stream: true });
  }
  return output + decoder.decode();
}

export async function boundedApi(
  baseUrl,
  method,
  path,
  { token, body, idempotencyKey, timeoutMs = REQUEST_TIMEOUT_MS, fetchImpl = globalThis.fetch } = {},
) {
  const headers = { accept: "application/json" };
  if (token) headers.authorization = `Bearer ${token}`;
  let payload;
  if (body !== undefined) {
    headers["content-type"] = "application/json";
    payload = JSON.stringify(body);
    if (Buffer.byteLength(payload) > REQUEST_MAX_BYTES) {
      throw new Error(`request body exceeded ${REQUEST_MAX_BYTES} bytes`);
    }
  }
  if (idempotencyKey) headers["idempotency-key"] = idempotencyKey;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let response;
  try {
    response = await fetchImpl(`${baseUrl}${path}`, {
      method,
      headers,
      body: payload,
      signal: controller.signal,
    });
    const text = await boundedResponseText(response, RESPONSE_MAX_BYTES);
    let json = null;
    if (text) {
      try {
        json = JSON.parse(text);
      } catch {
        json = { error: { code: "invalid_response", message: "server returned a non-JSON response" } };
      }
    }
    return { status: response.status, json };
  } catch (error) {
    if (controller.signal.aborted) throw new Error(`request timed out after ${timeoutMs}ms`);
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

export function publicApiError(result) {
  const suppliedCode = result?.json?.error?.code;
  const code =
    typeof suppliedCode === "string" && /^[a-z][a-z0-9_]{0,79}$/.test(suppliedCode)
      ? suppliedCode
      : "request_failed";
  return {
    code,
    message:
      code === "invalid_response"
        ? "server returned a non-JSON response"
        : "server rejected the request; inspect server logs using the HTTP status and request time",
  };
}
