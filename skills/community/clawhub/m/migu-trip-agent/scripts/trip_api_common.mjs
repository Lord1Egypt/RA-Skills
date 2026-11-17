import https from "node:https";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const HOST = "gulangyu.migudm.cn";
export const DETAIL_PATH = "/trip-agent-api/api/plan/create_detail";
export const ROADBOOK_PATH = "/trip-agent-api/road/book/pic/make";

const SKILL_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
export const DEFAULT_TOKEN_FILE = path.join(SKILL_DIR, "secrets", "plan_multi_token.txt");

export function redact(text) {
  return String(text ?? "")
    .replace(/Bearer\s+[A-Za-z0-9._-]+/gi, "Bearer [REDACTED]")
    .replace(/eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g, "[REDACTED_JWT]");
}

export function sanitizeToken(value) {
  const compact = String(value || "")
    .replace(/[\u0000\x00]/g, "")
    .replace(/^\uFEFF/, "")
    .replace(/[\u200B-\u200D\u2060]/g, "")
    .replace(/\u00A0/g, " ")
    .replace(/```(?:text|txt|jwt|json)?/gi, "")
    .replace(/```/g, "")
    .replace(/^[\s"'`“”‘’<>]+|[\s"'`“”‘’<>]+$/g, "")
    .replace(/^Bearer\s+/i, "")
    .replace(/\s+/g, "");
  const match = compact.match(/eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/);
  return match ? match[0] : compact;
}

export function parseBaseArgs(argv, defaults = {}) {
  const args = {
    tokenFile: process.env.PLAN_MULTI_TOKEN_FILE || DEFAULT_TOKEN_FILE,
    sessionFile: process.env.PLAN_MULTI_SESSION_FILE || path.join(SKILL_DIR, "plan_multi_session.txt"),
    sessionId: "",
    json: false,
    verbose: false,
    ...defaults,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      i += 1;
      if (i >= argv.length) throw new Error(`Missing value for ${arg}`);
      return argv[i];
    };
    if (arg === "--token-file") args.tokenFile = next();
    else if (arg === "--session-file") args.sessionFile = next();
    else if (arg === "--session-id") args.sessionId = next();
    else if (arg === "--json") args.json = true;
    else if (arg === "--verbose") args.verbose = true;
    else if (arg === "--skip-create-detail") args.skipCreateDetail = true;
    else throw new Error(`Unknown option: ${arg}`);
  }
  return args;
}

export function resolveSessionId(args) {
  const sessionId = (args.sessionId || fs.readFileSync(args.sessionFile, "utf8")).trim();
  if (!sessionId) {
    throw new Error(`Missing session_id. Pass --session-id or write ${args.sessionFile}`);
  }
  return sessionId;
}

export function loadToken(tokenFile) {
  return sanitizeToken(fs.readFileSync(tokenFile, "utf8"));
}

export function postRequest(pathname, token, body, { timeoutMs = 180_000 } = {}) {
  const payload = JSON.stringify(body);
  return new Promise((resolve, reject) => {
    const req = https.request(
      {
        hostname: HOST,
        port: 443,
        path: pathname,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(payload),
          Authorization: `Bearer ${token}`,
        },
        timeout: timeoutMs,
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => {
          raw += chunk.toString("utf8");
        });
        res.on("end", () => {
          resolve({ statusCode: res.statusCode, raw });
        });
      },
    );
    req.on("timeout", () => req.destroy(new Error(`Request timeout: ${pathname}`)));
    req.on("error", reject);
    req.write(payload);
    req.end();
  });
}

export function postJson(pathname, token, body, options) {
  return postRequest(pathname, token, body, options).then(({ statusCode, raw }) => {
    try {
      return { statusCode, json: JSON.parse(raw), raw };
    } catch {
      return { statusCode, json: null, raw };
    }
  });
}

export function parseSseEvents(raw) {
  const events = [];
  for (const line of raw.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed.startsWith("data:")) continue;
    const payload = trimmed.slice(5).trim();
    if (!payload) continue;
    try {
      events.push(JSON.parse(payload));
    } catch {
      /* ignore partial json lines */
    }
  }
  return events;
}

export function extractDetailPlanFromSse(events) {
  let detailPlan = null;
  let error = null;
  let progress = [];

  for (const ev of events) {
    const h = ev.h || {};
    const b = ev.b || {};
    if (typeof b.answer === "string" && h.status === "status" && b.answer && !b.answer.startsWith("<")) {
      progress.push(b.answer);
    }
    if (h.hasTrip === "2" || b.type === "error") {
      error = b.answer || "详细行程生成失败，请重试";
    }
    if (h.status === "content_blocked" || b.type === "output_blocked") {
      error = b.answer || "详细行程未通过内容审核";
    }
    if (b.type === "trip" && b.trip_answer && typeof b.trip_answer === "object") {
      const keys = Object.keys(b.trip_answer);
      if (keys.length > 0) {
        detailPlan = b.trip_answer;
        error = null;
      }
    }
  }

  if (!detailPlan && !error) {
    error = "详细行程流结束但未返回 trip_answer，请确认该 session 已先完成简约行程（summary_plan 已入库）";
  }

  return { detailPlan, error, progress };
}

export async function callCreateDetail(token, sessionId, verbose) {
  const body = { session_id: sessionId };
  if (verbose) {
    console.error(`[create_detail] POST ${DETAIL_PATH}`);
    console.error(`[create_detail] body=${JSON.stringify(body)}`);
  }
  const { statusCode, raw } = await postRequest(DETAIL_PATH, token, body);
  if (statusCode !== 200) {
    throw new Error(`create_detail HTTP ${statusCode}: ${redact(raw).slice(0, 400)}`);
  }
  const events = parseSseEvents(raw);
  const result = extractDetailPlanFromSse(events);
  if (verbose) {
    console.error(`[create_detail] events=${events.length} progress_steps=${result.progress.length}`);
  }
  return { ...result, sessionId, requestBody: body, events };
}
