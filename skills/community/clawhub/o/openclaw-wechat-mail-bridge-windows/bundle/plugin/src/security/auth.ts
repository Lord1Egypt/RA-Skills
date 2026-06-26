import crypto from "node:crypto";
import type { IncomingHttpHeaders } from "node:http";

const seenNonces = new Map<string, number>();
const maxNonceEntries = 20_000;

function getBearerToken(headers: IncomingHttpHeaders): string | null {
  const auth = headers.authorization;
  if (!auth) {
    return null;
  }

  const [kind, token] = auth.split(" ");
  if (!kind || !token) {
    return null;
  }
  if (kind.toLowerCase() !== "bearer") {
    return null;
  }
  return token.trim();
}

function getBridgeSignature(headers: IncomingHttpHeaders): string | null {
  const signature = headers["x-bridge-signature"];
  if (!signature) {
    return null;
  }
  return Array.isArray(signature) ? signature[0] : signature;
}

function safeEquals(a: string, b: string): boolean {
  const left = Buffer.from(a, "utf8");
  const right = Buffer.from(b, "utf8");
  if (left.length !== right.length) {
    return false;
  }
  return crypto.timingSafeEqual(left, right);
}

export function assertAuthenticated(
  headers: IncomingHttpHeaders,
  secret: string,
  authWindowSec: number,
  payload?: unknown
): void {
  const token = getBearerToken(headers);
  const signature = getBridgeSignature(headers);
  if ((!token || !safeEquals(token, secret)) && !verifyHmacSignature(headers, secret, signature, payload)) {
    throw new Error("unauthorized");
  }

  const timestampHeader = headers["x-bridge-ts"];
  if (!timestampHeader || authWindowSec <= 0) {
    return;
  }

  const timestampValue = Array.isArray(timestampHeader) ? timestampHeader[0] : timestampHeader;
  const requestTime = Number(timestampValue);
  if (Number.isNaN(requestTime)) {
    throw new Error("invalid_timestamp");
  }

  const nowSec = Math.floor(Date.now() / 1000);
  if (Math.abs(nowSec - requestTime) > authWindowSec) {
    throw new Error("expired_timestamp");
  }

  registerNonce(headers, secret, nowSec, Math.max(5, authWindowSec));
}

function verifyHmacSignature(
  headers: IncomingHttpHeaders,
  secret: string,
  signature: string | null,
  payload?: unknown
): boolean {
  if (!signature) {
    return false;
  }
  const timestampHeader = headers["x-bridge-ts"];
  if (!timestampHeader) {
    return false;
  }
  const timestamp = Array.isArray(timestampHeader) ? timestampHeader[0] : timestampHeader;
  if (!timestamp) {
    return false;
  }
  const payloadText =
    payload === undefined || payload === null ? "" : stableStringify(payload);
  const mac = crypto.createHmac("sha256", secret);
  mac.update(`${timestamp}.${payloadText}`);
  const expected = mac.digest("hex");
  return safeEquals(expected, signature);
}

function stableStringify(value: unknown): string {
  if (value === null || value === undefined) {
    return "";
  }
  if (typeof value !== "object") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableStringify(item)).join(",")}]`;
  }

  const obj = value as Record<string, unknown>;
  const keys = Object.keys(obj).sort((a, b) => a.localeCompare(b));
  const serialized = keys.map((key) => `${JSON.stringify(key)}:${stableStringify(obj[key])}`);
  return `{${serialized.join(",")}}`;
}

function registerNonce(
  headers: IncomingHttpHeaders,
  secret: string,
  nowSec: number,
  ttlSec: number
): void {
  const nonceHeader = headers["x-bridge-nonce"];
  if (!nonceHeader) {
    return;
  }

  const rawNonce = Array.isArray(nonceHeader) ? nonceHeader[0] : nonceHeader;
  const nonce = rawNonce?.trim();
  if (!nonce) {
    throw new Error("invalid_nonce");
  }

  pruneSeenNonces(nowSec, ttlSec);
  const key = `${secret}:${nonce}`;
  if (seenNonces.has(key)) {
    throw new Error("replayed_nonce");
  }
  seenNonces.set(key, nowSec);
  if (seenNonces.size > maxNonceEntries) {
    pruneSeenNonces(nowSec, ttlSec);
  }
}

function pruneSeenNonces(nowSec: number, ttlSec: number): void {
  const expiry = nowSec - ttlSec;
  for (const [key, seenAt] of seenNonces.entries()) {
    if (seenAt <= expiry) {
      seenNonces.delete(key);
    }
  }
}
