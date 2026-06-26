import { randomBytes } from "node:crypto";
import { keccak256, stringToHex } from "viem";

export const DEFAULT_BASE_URL = "https://ghostprotocol.cc";
export const DEFAULT_CHAIN_ID = 8453;
export const DEFAULT_X402_SCHEME = "exact";
export const DEFAULT_TIMEOUT_MS = 15000;

export function parseCliArgs(argv = process.argv.slice(2)) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token || !token.startsWith("--")) continue;
    const body = token.slice(2);
    if (!body) continue;

    const separator = body.indexOf("=");
    if (separator > 0) {
      const key = body.slice(0, separator);
      const value = body.slice(separator + 1);
      args[key] = value;
      continue;
    }

    const maybeValue = argv[i + 1];
    if (!maybeValue || maybeValue.startsWith("--")) {
      args[body] = "true";
      continue;
    }

    args[body] = maybeValue;
    i += 1;
  }
  return args;
}

export function normalizeBaseUrl(value) {
  return String(value || DEFAULT_BASE_URL).trim().replace(/\/+$/, "");
}

export function normalizeOptionalString(value) {
  const normalized = String(value || "").trim();
  return normalized || null;
}

export function parsePositiveInt(raw, fallback) {
  if (raw == null || raw === "") return fallback;
  const parsed = Number.parseInt(String(raw), 10);
  if (!Number.isFinite(parsed) || parsed <= 0) return fallback;
  return parsed;
}

export function parsePositiveBigIntString(raw, fallback) {
  if (raw == null || raw === "") return fallback;
  const normalized = String(raw).trim();
  if (!/^\d+$/.test(normalized)) return fallback;
  return normalized;
}

export function toBool(raw, fallback = false) {
  if (raw == null || raw === "") return fallback;
  const value = String(raw).trim().toLowerCase();
  if (value === "true" || value === "1" || value === "yes") return true;
  if (value === "false" || value === "0" || value === "no") return false;
  return fallback;
}

export function parseJson(raw, fallback = null) {
  if (!raw) return fallback;
  try {
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
}

function sortJsonValue(value) {
  if (Array.isArray(value)) return value.map(sortJsonValue);
  if (value && typeof value === "object") {
    return Object.keys(value)
      .sort()
      .reduce((result, key) => {
        result[key] = sortJsonValue(value[key]);
        return result;
      }, {});
  }
  return value;
}

export function normalizeGhostWireRequestPayload(value) {
  if (value == null) return null;
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("GhostWire request must be a JSON object.");
  }

  const prompt = normalizeOptionalString(value.prompt);
  if (!prompt) {
    throw new Error("GhostWire request.prompt must be a non-empty string.");
  }

  return {
    version: 1,
    prompt,
    ...(normalizeOptionalString(value.walletAddress) ? { walletAddress: normalizeOptionalString(value.walletAddress) } : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "metadata")
      ? { metadata: sortJsonValue(value.metadata ?? null) }
      : {}),
  };
}

export function buildGhostWireRequestSpecHash(value) {
  const normalized = normalizeGhostWireRequestPayload(value);
  if (!normalized) {
    throw new Error("GhostWire request payload is required.");
  }
  return keccak256(stringToHex(JSON.stringify(sortJsonValue(normalized))));
}

export function createNonce(bytes = 16) {
  return randomBytes(bytes).toString("hex");
}

export function printJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

export async function fetchWithTimeout(url, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }
}
