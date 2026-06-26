import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

export const PRODUCT_SLUG = "propai-live";
export const DEFAULT_OFFLINE_GRACE_HOURS = 72;
export const DEFAULT_NEXT_CHECK_HOURS = 6;
export const DEFAULT_TIMEOUT_MS = 10000;
export const ACTIVE_STATUSES = new Set(["active", "trial", "grace"]);

const EXIT_CODES = {
  ok: 0,
  missing: 2,
  expired: 3,
  invalid_status: 4,
  entitlement_missing: 5,
  bad_state: 6,
  network: 7,
  unknown: 1,
};

export function getExitCode(reason) {
  return EXIT_CODES[reason] ?? EXIT_CODES.unknown;
}

export function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      continue;
    }
    const body = token.slice(2);
    if (!body) {
      continue;
    }
    const eqIndex = body.indexOf("=");
    if (eqIndex >= 0) {
      const key = body.slice(0, eqIndex);
      const value = body.slice(eqIndex + 1);
      args[key] = value === "" ? true : value;
      continue;
    }
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[body] = true;
      continue;
    }
    args[body] = next;
    i += 1;
  }
  return args;
}

export function printJson(payload) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

export function printError(message, detail) {
  const out = {
    ok: false,
    error: message,
  };
  if (detail) {
    out.detail = detail;
  }
  printJson(out);
}

export function normalizeApiBaseUrl(value) {
  if (!value || typeof value !== "string") {
    return "";
  }
  return value.replace(/\/+$/, "");
}

export function toIsoNow() {
  return new Date().toISOString();
}

export function hoursFromNow(hours) {
  return new Date(Date.now() + hours * 60 * 60 * 1000).toISOString();
}

export function safeDateMs(value) {
  if (!value) {
    return NaN;
  }
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? ms : NaN;
}

export function resolveMachineId(explicitMachineId) {
  if (explicitMachineId && typeof explicitMachineId === "string") {
    return explicitMachineId;
  }
  const seed = [
    os.hostname(),
    os.platform(),
    os.arch(),
    os.userInfo().username,
  ].join("|");
  const hash = crypto.createHash("sha256").update(seed).digest("hex");
  return `mid_${hash.slice(0, 24)}`;
}

export function resolveStateFilePath(stateDirFlag) {
  const stateDir =
    (typeof stateDirFlag === "string" && stateDirFlag) ||
    process.env.PROPAI_LIVE_STATE_DIR ||
    path.join(os.homedir(), ".propai-live");
  return path.join(stateDir, "license-state.json");
}

export async function loadState(stateFile) {
  try {
    const raw = await fs.readFile(stateFile, "utf8");
    return JSON.parse(raw);
  } catch (error) {
    if (error && error.code === "ENOENT") {
      return null;
    }
    throw error;
  }
}

export async function saveState(stateFile, value) {
  const dir = path.dirname(stateFile);
  await fs.mkdir(dir, { recursive: true });
  const tempFile = `${stateFile}.${Date.now()}.tmp`;
  await fs.writeFile(tempFile, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  await fs.rename(tempFile, stateFile);
}

export async function clearState(stateFile) {
  await fs.rm(stateFile, { force: true });
}

function numOrDefault(value, fallback) {
  const num = Number(value);
  return Number.isFinite(num) && num >= 0 ? num : fallback;
}

export function normalizeEntitlements(value) {
  if (!Array.isArray(value)) {
    return [];
  }
  return value
    .map((item) => String(item).trim().toLowerCase())
    .filter((item) => item.length > 0);
}

export function normalizeActivationPayload(apiData) {
  const entitlements = normalizeEntitlements(apiData.entitlements);
  return {
    licenseToken: apiData.licenseToken || apiData.token || apiData.accessToken || "",
    licenseId: apiData.licenseId || apiData.id || "",
    status: String(apiData.status || "active").toLowerCase(),
    plan: String(apiData.plan || apiData.tier || "unknown"),
    expiresAt: apiData.expiresAt || apiData.expiry || "",
    entitlements,
    offlineGraceUntil:
      apiData.offlineGraceUntil ||
      hoursFromNow(numOrDefault(apiData.offlineGraceHours, DEFAULT_OFFLINE_GRACE_HOURS)),
    nextRemoteCheckAt:
      apiData.nextRemoteCheckAt ||
      hoursFromNow(numOrDefault(apiData.nextCheckHours, DEFAULT_NEXT_CHECK_HOURS)),
  };
}

export function mergeValidationIntoState(state, apiData) {
  const next = { ...state };
  if (apiData.licenseToken || apiData.token || apiData.accessToken) {
    next.licenseToken = apiData.licenseToken || apiData.token || apiData.accessToken;
  }
  if (apiData.licenseId || apiData.id) {
    next.licenseId = apiData.licenseId || apiData.id;
  }
  if (apiData.status) {
    next.status = String(apiData.status).toLowerCase();
  }
  if (apiData.plan) {
    next.plan = String(apiData.plan);
  }
  if (Array.isArray(apiData.entitlements)) {
    next.entitlements = normalizeEntitlements(apiData.entitlements);
  }
  if (apiData.expiresAt || apiData.expiry) {
    next.expiresAt = apiData.expiresAt || apiData.expiry;
  }
  if (apiData.offlineGraceUntil) {
    next.offlineGraceUntil = apiData.offlineGraceUntil;
  } else if (apiData.offlineGraceHours != null) {
    next.offlineGraceUntil = hoursFromNow(
      numOrDefault(apiData.offlineGraceHours, DEFAULT_OFFLINE_GRACE_HOURS),
    );
  }
  if (apiData.nextRemoteCheckAt) {
    next.nextRemoteCheckAt = apiData.nextRemoteCheckAt;
  } else if (apiData.nextCheckHours != null) {
    next.nextRemoteCheckAt = hoursFromNow(
      numOrDefault(apiData.nextCheckHours, DEFAULT_NEXT_CHECK_HOURS),
    );
  }
  next.lastValidatedAt = toIsoNow();
  return next;
}

export function shouldRunRemoteValidation(state, nowMs) {
  const due = safeDateMs(state.nextRemoteCheckAt);
  if (!Number.isFinite(due)) {
    return true;
  }
  return nowMs >= due;
}

export function withinOfflineGrace(state, nowMs) {
  const graceMs = safeDateMs(state.offlineGraceUntil);
  if (!Number.isFinite(graceMs)) {
    return false;
  }
  return nowMs <= graceMs;
}

function includesEntitlement(entitlements, expected) {
  const wanted = String(expected || "").toLowerCase();
  if (!wanted) {
    return true;
  }
  return entitlements.some(
    (entitlement) =>
      entitlement === wanted ||
      entitlement === "all" ||
      entitlement === "full-access" ||
      entitlement === "*",
  );
}

export function evaluateState(state, mode, requiredEntitlement) {
  if (!state || typeof state !== "object") {
    return { ok: false, reason: "missing", message: "License is not activated." };
  }

  const status = String(state.status || "").toLowerCase();
  if (!ACTIVE_STATUSES.has(status)) {
    return {
      ok: false,
      reason: "invalid_status",
      message: `License status is '${status || "unknown"}'.`,
    };
  }

  const nowMs = Date.now();
  const expiryMs = safeDateMs(state.expiresAt);
  if (Number.isFinite(expiryMs) && nowMs > expiryMs) {
    return { ok: false, reason: "expired", message: "License has expired." };
  }

  const entitlements = normalizeEntitlements(state.entitlements);
  if (mode === "write" && !includesEntitlement(entitlements, "write")) {
    return {
      ok: false,
      reason: "entitlement_missing",
      message: "Missing required entitlement: write.",
    };
  }

  if (!includesEntitlement(entitlements, requiredEntitlement)) {
    return {
      ok: false,
      reason: "entitlement_missing",
      message: `Missing required entitlement: ${requiredEntitlement}.`,
    };
  }

  return { ok: true, reason: "ok", message: "License is locally valid." };
}

export function maskLicenseKey(key) {
  if (!key) {
    return "";
  }
  const asText = String(key);
  if (asText.length <= 4) {
    return `****${asText}`;
  }
  return `****${asText.slice(-4)}`;
}

export async function postJson(url, payload, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        accept: "application/json",
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    const text = await response.text();
    let data = null;
    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = null;
      }
    }
    return { ok: response.ok, status: response.status, data, text };
  } finally {
    clearTimeout(timer);
  }
}

export function safeApiError(result) {
  if (!result) {
    return "No response from license service.";
  }
  if (result.data && typeof result.data.error === "string") {
    return result.data.error;
  }
  if (typeof result.text === "string" && result.text.trim()) {
    return result.text.trim();
  }
  return `License service returned status ${result.status}.`;
}

