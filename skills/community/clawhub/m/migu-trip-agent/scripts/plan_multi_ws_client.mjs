#!/usr/bin/env node

import process from "node:process";
import { appendFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { createInterface } from "node:readline";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";
import WebSocket from "ws";

const SKILL_DIR = dirname(dirname(fileURLToPath(import.meta.url)));
const DEFAULT_TOKEN_FILE = resolve(SKILL_DIR, "secrets", "plan_multi_token.txt");
/** Legacy path; Feishu/OpenClaw sometimes writes here and corrupts JWT. Do not prefer over skill secrets. */
const LEGACY_TOKEN_FILE = resolve(SKILL_DIR, "..", "..", "secrets", "plan_multi_token.txt");
const DEFAULT_ENDPOINT = "wss://gulangyu.migudm.cn/trip-agent/ws/api/ws";
const DEFAULT_ORIGIN = "https://gulangyu.migudm.cn";
const DEFAULT_APP_VERSION = "0.6.4";
const DEFAULT_VERSION = "v0.6.4";
const DEFAULT_TENANT = "hmxt";
const DEFAULT_HEARTBEAT_MS = 30_000;
const DEFAULT_TIMEOUT_MS = 120_000;

function stripNullBytes(value) {
  if (typeof value !== "string") {
    return value;
  }
  // Remove all types of null bytes: \u0000, \x00, etc.
  return value.replace(/[\u0000\x00]/g, "").trim();
}

function sanitizeTokenInput(value) {
  let text = stripNullBytes(String(value || ""));
  const hadBearer = /\bBearer\s+/i.test(text);
  const hadCodeFence = /```/.test(text);
  const hadInvisible = /[\uFEFF\u200B-\u200D\u2060\u00A0]/.test(text);

  text = text
    .replace(/^\uFEFF/, "")
    .replace(/[\u200B-\u200D\u2060]/g, "")
    .replace(/\u00A0/g, " ")
    .replace(/```(?:text|txt|jwt|json)?/gi, "")
    .replace(/```/g, "")
    .replace(/^[\s"'`“”‘’<>]+|[\s"'`“”‘’<>]+$/g, "")
    .replace(/^Bearer\s+/i, "")
    .trim();

  // Feishu rich text may wrap a JWT with labels, quotes, or line breaks.
  // JWT is base64url segments separated by dots, so extract the first candidate.
  const compact = text.replace(/\s+/g, "");
  const candidate = compact.match(/eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/);
  const token = candidate ? candidate[0] : compact;

  return {
    token,
    diagnostics: {
      rawLength: String(value || "").length,
      sanitizedLength: token.length,
      dotCount: (token.match(/\./g) || []).length,
      startsWithJwtPrefix: token.startsWith("eyJ"),
      hadBearer,
      hadCodeFence,
      hadInvisible,
    },
  };
}

class TokenError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "TokenError";
    this.code = code;
  }
}

function getTokenPathHints() {
  return {
    primary: DEFAULT_TOKEN_FILE,
    windowsExample: "C:\\Users\\ll\\.openclaw\\workspace\\skills\\migu-trip-agent\\secrets\\plan_multi_token.txt",
    unixExample: "~/.openclaw/workspace/skills/migu-trip-agent/secrets/plan_multi_token.txt",
  };
}

function isTokenAuthError(error) {
  const text = `${error?.message || ""} ${error?.code || ""}`.toLowerCase();
  return (
    text.includes("401") ||
    text.includes("unauthorized") ||
    text.includes("invalid token") ||
    text.includes("token expired") ||
    text.includes("jwt expired")
  );
}

/** User-facing setup guide on stderr (never prints the JWT). */
function printTokenSetupGuide(reason = "missing", extra = {}) {
  const paths = getTokenPathHints();
  const src = extra.tokenSource || "(none)";
  console.error("");
  console.error("[token-help] ==================================================");
  if (reason === "missing") {
    console.error("[token-help] 未配置咪咕旅游登录 token，无法调用行程 WebSocket。");
  } else if (reason === "invalid_format") {
    console.error("[token-help] token 已读取，但内容不是合法 JWT（应以 eyJ 开头，且包含两个英文句点 . ）。");
  } else if (reason === "corrupted_file") {
    console.error("[token-help] 检测到 token 文件内容与另一路径不一致，或 JWT 在保存时被飞书/富文本损坏。");
    console.error("[token-help]   典型现象：payload 段字符被改写（如 2c→2b、MTl9→MTP09），签名校验失败 → 401。");
    console.error("[token-help]   JWT 的 exp 可能仍显示未过期，但服务端会拒绝——这不是“日期过期”，是“文件内容损坏”。");
  } else if (reason === "auth_rejected") {
    console.error("[token-help] 服务端返回 401，但 JWT 的 exp 尚未到期。");
    console.error("[token-help]   优先检查：token 文件是否在粘贴/保存时被改了一个字符；请用 --save-token-stdin 重新写入。");
    console.error("[token-help]   若原样 token 可用、文件不可用，即可确认是保存损坏。");
  } else if (reason === "expired") {
    console.error("[token-help] JWT 已过期（exp <= 当前时间），请重新登录 H5 获取新 token。");
  } else {
    console.error("[token-help] token 无效（连接返回 401 / Unauthorized）。");
  }
  if (extra.expIso) {
    console.error(`[token-help] JWT exp=${extra.expIso} expired=${extra.expired === true}`);
  }
  if (src && src !== "(none)") {
    console.error(`[token-help] 当前读取位置: ${src}`);
  }
  console.error("[token-help]");
  console.error("[token-help] 【一】如何获取 token（浏览器登录咪咕旅游 H5 后）");
  console.error("[token-help]   1. 打开 https://gulangyu.migudm.cn ，用手机号登录");
  console.error("[token-help]   2. F12 → Network（网络），在页面里随便问一句行程问题");
  console.error("[token-help]   3. 找到 WebSocket 连接，在请求 URL 的 token= 或 Header 的 Authorization 中复制 JWT");
  console.error("[token-help]   4. JWT 特征：以 eyJ 开头，中间有两个 . ，整段一行、无换行");
  console.error("[token-help]   （也可：Application → Local Storage，搜索 token / authorization）");
  console.error("[token-help]");
  console.error("[token-help] 【二】保存到本地文件（推荐，UTF-8 单行纯文本，不要加引号）");
  console.error(`[token-help]   Windows: ${paths.windowsExample}`);
  console.error(`[token-help]   Linux/Mac: ${paths.unixExample}`);
  console.error(`[token-help]   本 skill 默认: ${paths.primary}`);
  console.error("[token-help]   也可用环境变量: PLAN_MULTI_TOKEN_FILE=<上述路径>");
  console.error("[token-help]");
  console.error("[token-help] 【三】配置到本地（仅用户本人在本机操作；请勿把 token 发到对话里）");
  console.error("[token-help]   推荐：由用户本人执行 --save-token-stdin，把 JWT 从 stdin 原样写入（勿经 Markdown 再编辑）。");
  console.error("[token-help]   Agent 不应向用户索取 token 明文，也不得在回复或日志中回显 token。");
  console.error("[token-help]   不要保存到 workspace/secrets/（旧路径易与 skill 目录混淆）。");
  console.error("[token-help]");
  console.error("[token-help] 【四】保存后预检");
  console.error("[token-help]   node scripts/plan_multi_ws_client.mjs --check-token --token-diagnostics");
  console.error("[token-help]   node scripts/plan_multi_ws_client.mjs --check-token --probe-auth --user-id <手机号>");
  console.error("[token-help]   若仍 401：重新登录 H5，在 Network 里复制最新 WS 的 token=，并确认命令带 --bearer --user-id");
  console.error("[token-help] ==================================================");
  console.error("");
}

function tokenFingerprint(token) {
  const parts = String(token || "").split(".");
  if (parts.length !== 3) return "";
  return `${parts[0].slice(0, 8)}…${parts[2].slice(-8)}`;
}

function decodeJwtMeta(token) {
  try {
    const payloadB64 = String(token || "").split(".")[1];
    if (!payloadB64) return null;
    const json = JSON.parse(Buffer.from(payloadB64, "base64url").toString("utf8"));
    const exp = Number(json.exp);
    const iat = Number(json.iat);
    const now = Math.floor(Date.now() / 1000);
    return {
      exp,
      iat,
      expired: Number.isFinite(exp) && exp <= now,
      expIso: Number.isFinite(exp) ? new Date(exp * 1000).toISOString() : "",
      iatIso: Number.isFinite(iat) ? new Date(iat * 1000).toISOString() : "",
    };
  } catch {
    return null;
  }
}

function warnIfLegacyTokenMismatch(activeToken, activeSource) {
  if (!existsSync(LEGACY_TOKEN_FILE) || activeSource === LEGACY_TOKEN_FILE) return;
  const legacyClean = sanitizeTokenInput(readTextFileIfExists(LEGACY_TOKEN_FILE));
  if (!legacyClean.token || legacyClean.token === activeToken) return;
  console.error(
    `[token-warn] ${LEGACY_TOKEN_FILE} differs from active token (${tokenFingerprint(legacyClean.token)} vs ${tokenFingerprint(activeToken)}).`,
  );
  console.error("[token-warn] OpenClaw 可能写入了损坏的旧路径 token；请只使用 skill secrets 或执行 --save-token-stdin 覆盖。");
}

function saveTokenToFile(targetPath, rawToken) {
  const clean = sanitizeTokenInput(rawToken);
  if (!clean.token.startsWith("eyJ") || clean.diagnostics.dotCount !== 2) {
    throw new TokenError("TOKEN_INVALID_FORMAT", "Refusing to save: not a valid JWT after sanitization");
  }
  writeFileSync(targetPath, `${clean.token}\n`, { encoding: "utf8" });
  return { path: targetPath, token: clean.token, ...clean.diagnostics };
}

function resolveAuthFailureReason(meta) {
  if (meta?.expired) return "expired";
  return "auth_rejected";
}

function probeWsAuth(args) {
  return new Promise((resolve) => {
    const url = buildUrl(args);
    const ws = new WebSocket(url, {
      perMessageDeflate: true,
      handshakeTimeout: 12_000,
      rejectUnauthorized: true,
      headers: buildWsHeaders(args),
    });
    let settled = false;
    const done = (ok, message) => {
      if (settled) return;
      settled = true;
      try {
        ws.close();
      } catch {
        /* ignore */
      }
      resolve({ ok, message });
    };
    ws.on("open", () => done(true, "websocket_open"));
    ws.on("error", (err) => done(false, err.message));
    ws.on("close", (code) => {
      if (!settled) done(false, `closed_${code}`);
    });
    setTimeout(() => done(false, "probe_timeout"), 12_000);
  });
}

function assertTokenFormat(args) {
  const d = args.tokenDiagnosticsData;
  if (d.startsWithJwtPrefix && d.dotCount === 2 && d.sanitizedLength > 20) {
    return;
  }
  printTokenSetupGuide("invalid_format", { tokenSource: args.tokenSource });
  throw new TokenError("TOKEN_INVALID_FORMAT", "Token is not a valid JWT shape after sanitization");
}

async function runTokenCheck(args) {
  if (!args.token) {
    printTokenSetupGuide("missing", { tokenSource: args.tokenSource });
    return 2;
  }
  try {
    assertTokenFormat(args);
  } catch {
    return 2;
  }
  warnIfLegacyTokenMismatch(args.token, args.tokenSource);
  const meta = decodeJwtMeta(args.token);
  console.error("[token-check] OK: JWT format looks valid.");
  console.error(`[token-check] source=${args.tokenSource || DEFAULT_TOKEN_FILE}`);
  console.error(`[token-check] fingerprint=${tokenFingerprint(args.token)}`);
  const d = args.tokenDiagnosticsData;
  console.error(`[token-check] length=${d.sanitizedLength} dots=${d.dotCount} starts_eyJ=${d.startsWithJwtPrefix}`);
  if (meta) {
    console.error(`[token-check] exp=${meta.expIso} expired=${meta.expired}`);
  }
  if (args.probeAuth) {
    if (!args.bearerAuth) {
      console.error("[token-check] probe: enabling --bearer for handshake (same as run_plan.bat)");
      args.bearerAuth = true;
    }
    const probe = await probeWsAuth(args);
    if (probe.ok) {
      console.error("[token-check] probe: WebSocket auth OK");
      return 0;
    }
    console.error(`[token-check] probe: WebSocket auth FAILED (${probe.message})`);
    const reason =
      args.tokenSource === LEGACY_TOKEN_FILE
        ? "corrupted_file"
        : resolveAuthFailureReason(meta);
    printTokenSetupGuide(reason, {
      tokenSource: args.tokenSource,
      expIso: meta?.expIso,
      expired: meta?.expired,
    });
    return 3;
  }
  return 0;
}

function readTextFileIfExists(filePath) {
  if (!filePath || !existsSync(filePath)) return "";
  return readFileSync(filePath, "utf8");
}

function parseArgs(argv) {
  const args = {
    endpoint: DEFAULT_ENDPOINT,
    appVersion: DEFAULT_APP_VERSION,
    version: DEFAULT_VERSION,
    tenant: DEFAULT_TENANT,
    clientType: "web",
    sessionId: "",
    question: "你好",
    heartbeatMs: DEFAULT_HEARTBEAT_MS,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    recommendContent: [],
    json: false,
    verbose: false,
    interactive: false,
    questionFromCli: false,
    logFile: "",
    tokenFile: "",
    tokenSource: "",
    tokenDiagnostics: false,
    checkTokenOnly: false,
    probeAuth: false,
    saveTokenStdin: false,
    saveTokenFile: "",
    bearerAuth: false,
    fallbackTripPlan: false,
    noPromptPlanForm: false,
    tripPlanDirect: false,
    planFormFile: "",
    sessionFile: "",
    departure: "",
    destination: "",
    adults: 0,
    children: 0,
    startDate: "",
    returnDate: "",
    minBudget: "",
    maxBudget: "",
    travelMode: "",
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      i += 1;
      if (i >= argv.length) {
        throw new Error(`Missing value for ${arg}`);
      }
      return argv[i];
    };

    switch (arg) {
      case "--token":
        args.token = next();
        args.tokenSource = "--token";
        break;
      case "--token-file":
        args.tokenFile = next();
        break;
      case "--user-id":
        args.userId = next();
        break;
      case "--question":
        args.question = next();
        args.questionFromCli = true;
        break;
      case "--session-id":
        args.sessionId = next();
        break;
      case "--recommend-content":
        args.recommendContent.push(next());
        break;
      case "--endpoint":
        args.endpoint = next();
        break;
      case "--timeout-ms":
        args.timeoutMs = Number.parseInt(next(), 10);
        break;
      case "--heartbeat-ms":
        args.heartbeatMs = Number.parseInt(next(), 10);
        break;
      case "--json":
        args.json = true;
        break;
      case "--verbose":
        args.verbose = true;
        break;
      case "--log-file":
        args.logFile = next();
        break;
      case "--bearer":
        args.bearerAuth = true;
        break;
      case "--token-diagnostics":
        args.tokenDiagnostics = true;
        break;
      case "--check-token":
        args.checkTokenOnly = true;
        break;
      case "--probe-auth":
        args.probeAuth = true;
        args.checkTokenOnly = true;
        break;
      case "--save-token-stdin":
        args.saveTokenStdin = true;
        break;
      case "--save-token-file":
        args.saveTokenFile = next();
        break;
      case "--fallback-trip-plan":
        args.fallbackTripPlan = true;
        break;
      case "--no-prompt-plan-form":
        args.noPromptPlanForm = true;
        break;
      case "--trip-plan-direct":
        args.tripPlanDirect = true;
        break;
      case "--plan-form-file":
        args.planFormFile = next();
        break;
      case "--session-file":
        args.sessionFile = next();
        break;
      case "--departure":
        args.departure = next();
        break;
      case "--destination":
        args.destination = next();
        break;
      case "--adults":
        args.adults = Number.parseInt(next(), 10);
        break;
      case "--children":
        args.children = Number.parseInt(next(), 10);
        break;
      case "--start-date":
        args.startDate = next();
        break;
      case "--return-date":
        args.returnDate = next();
        break;
      case "--min-budget":
        args.minBudget = next();
        break;
      case "--max-budget":
        args.maxBudget = next();
        break;
      case "--travel-mode":
        args.travelMode = next();
        break;
      case "--interactive":
      case "-i":
        args.interactive = true;
        break;
      case "--help":
      case "-h":
        printHelp();
        process.exit(0);
        break;
      default:
        throw new Error(`Unknown option: ${arg}`);
    }
  }

  if (!args.userId && process.env.PLAN_MULTI_USER_ID) {
    args.userId = process.env.PLAN_MULTI_USER_ID;
  }
  if (!args.tokenFile && process.env.PLAN_MULTI_TOKEN_FILE) {
    args.tokenFile = process.env.PLAN_MULTI_TOKEN_FILE;
  }
  if (!args.token && args.tokenFile) {
    args.token = readTextFileIfExists(args.tokenFile);
    args.tokenSource = args.token ? args.tokenFile : "";
  }
  if (!args.token && process.env.PLAN_MULTI_TOKEN) {
    args.token = process.env.PLAN_MULTI_TOKEN;
    args.tokenSource = "PLAN_MULTI_TOKEN";
  }
  if (!args.token) {
    args.token = readTextFileIfExists(DEFAULT_TOKEN_FILE);
    if (args.token) {
      args.tokenSource = DEFAULT_TOKEN_FILE;
    }
  }
  const tokenClean = sanitizeTokenInput(args.token || "");
  args.token = tokenClean.token;
  args.tokenDiagnosticsData = tokenClean.diagnostics;
  if (args.tokenDiagnostics || args.verbose) {
    console.error(`[token] source=${args.tokenSource || "(none)"}`);
    console.error(
      `[token] sanitized_length=${tokenClean.diagnostics.sanitizedLength} dots=${tokenClean.diagnostics.dotCount} starts_eyJ=${tokenClean.diagnostics.startsWithJwtPrefix}`,
    );
    if (tokenClean.diagnostics.hadBearer || tokenClean.diagnostics.hadCodeFence || tokenClean.diagnostics.hadInvisible) {
      console.error(
        `[token] cleaned bearer=${tokenClean.diagnostics.hadBearer} code_fence=${tokenClean.diagnostics.hadCodeFence} invisible_chars=${tokenClean.diagnostics.hadInvisible}`,
      );
    }
  }
  if (!args.bearerAuth && (process.env.PLAN_MULTI_BEARER === "1" || process.env.PLAN_MULTI_BEARER === "true")) {
    args.bearerAuth = true;
  }
  if (!args.fallbackTripPlan && (process.env.PLAN_MULTI_FALLBACK_TRIP_PLAN === "1" || process.env.PLAN_MULTI_FALLBACK_TRIP_PLAN === "true")) {
    args.fallbackTripPlan = true;
  }
  if (!args.interactive && (process.env.PLAN_MULTI_INTERACTIVE === "1" || process.env.PLAN_MULTI_INTERACTIVE === "true")) {
    args.interactive = true;
  }
  if (!args.sessionFile && process.env.PLAN_MULTI_SESSION_FILE) {
    args.sessionFile = process.env.PLAN_MULTI_SESSION_FILE;
  }
  if (!args.planFormFile && process.env.PLAN_MULTI_PLAN_FORM_FILE) {
    args.planFormFile = process.env.PLAN_MULTI_PLAN_FORM_FILE;
  }
  if (!args.sessionId && args.sessionFile && existsSync(args.sessionFile)) {
    args.sessionId = stripNullBytes(readFileSync(args.sessionFile, "utf8")).trim();
  }
  if (!args.token && !args.saveTokenStdin) {
    printTokenSetupGuide("missing", { tokenSource: args.tokenSource });
    throw new TokenError(
      "TOKEN_MISSING",
      "Missing token: use --token, --token-file, PLAN_MULTI_TOKEN, or PLAN_MULTI_TOKEN_FILE",
    );
  }
  if (args.token && !args.saveTokenStdin && !args.checkTokenOnly) {
    assertTokenFormat(args);
  }
  if (args.token && !args.saveTokenStdin) {
    warnIfLegacyTokenMismatch(args.token, args.tokenSource);
  }
  if (!Number.isFinite(args.timeoutMs) || args.timeoutMs <= 0) {
    throw new Error("--timeout-ms must be a positive integer");
  }
  if (!Number.isFinite(args.heartbeatMs) || args.heartbeatMs <= 0) {
    throw new Error("--heartbeat-ms must be a positive integer");
  }

  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/plan_multi_ws_client.mjs --token "<jwt-token>" [options]

Alternatives to --token (recommended for OpenClaw and wrappers):
  --token-file "<path>"            Read JWT from a UTF-8 one-line file.
  env PLAN_MULTI_TOKEN              Read JWT from environment.
  env PLAN_MULTI_TOKEN_FILE         Path to a token file.

Single-shot mode (default):
  --question "<text>"            Question to ask. Default: "你好".

Interactive multi-turn mode:
  --interactive, -i              Keep connection alive, read questions from stdin.
                                 Use with --question to send the first turn, then continue at Q>.
  env PLAN_MULTI_INTERACTIVE=1     Same as -i.

Options:
  --user-id "<id>"               Optional H5 user_id query parameter.
  --session-id "<uuid>"          Optional session id (auto-tracked in interactive mode).
  --recommend-content "<text>"   Add a recommend_content item. Repeatable.
  --endpoint "<wss-url>"         Override the real H5 WebSocket endpoint.
  --timeout-ms <ms>             Per-question timeout. Default: ${DEFAULT_TIMEOUT_MS}.
  --heartbeat-ms <ms>            Heartbeat interval. Default: ${DEFAULT_HEARTBEAT_MS}.
  --json                         Print structured JSON per response.
  --verbose                      Print all frames and state changes to stderr.
  --log-file "<path>"            Write raw WebSocket traffic as JSONL.
  --bearer                       Add Authorization: Bearer <token> on WS handshake (some gateways need this).
  --token-diagnostics            Print safe token diagnostics (never prints token).
  --check-token                  Preflight: JWT shape (+ optional --probe-auth).
  --probe-auth                   With --check-token: open WebSocket to verify server accepts token.
  --save-token-stdin             Read one JWT line from stdin, save to DEFAULT_TOKEN_FILE, exit.
  --save-token-file <path>       With --save-token-stdin: override output path.
  env PLAN_MULTI_USER_ID         Default --user-id (e.g. login phone).
  --fallback-trip-plan           Auto-fallback to structured trip_plan when backend returns summary_plan error.
  --no-prompt-plan-form          Use default plan_form (no stdin prompts). Auto when stdin is not a TTY.
  --trip-plan-direct             Send structured trip_plan immediately (OpenClaw/H5-style). Requires plan form.
  --plan-form-file "<path>"      JSON plan_form file (recommended for OpenClaw).
  --session-file "<path>"        Read/write session_id for multi-turn OpenClaw conversations.
  --departure / --destination    Inline plan_form fields (alternative to --plan-form-file).
  --adults / --children          Passenger counts.
  --start-date / --return-date   Dates as YYYY/MM/DD.
  --min-budget / --max-budget    Budget strings (empty = no limit).
  --travel-mode                  e.g. 飞机, 高铁.
  env PLAN_MULTI_SESSION_FILE      Session persistence path.
  env PLAN_MULTI_PLAN_FORM_FILE    Default plan_form JSON path.
`);
}

function buildWsHeaders(args) {
  const headers = { Origin: DEFAULT_ORIGIN };
  if (args.bearerAuth) {
    headers.Authorization = `Bearer ${args.token}`;
  }
  return headers;
}

function buildUrl(args) {
  const url = new URL(args.endpoint);
  // encodeURIComponent avoids rare gateway issues with base64url in query strings
  url.searchParams.set("token", args.token);
  if (args.userId) {
    url.searchParams.set("user_id", args.userId);
  }
  url.searchParams.set("client_type", args.clientType);
  url.searchParams.set("X-App-Version", args.appVersion);
  url.searchParams.set("tenant", args.tenant);
  url.searchParams.set("version", args.version);
  return url.toString();
}

function buildHeartbeat(sessionId) {
  return {
    header: {
      task_type: "heartbeat",
      biz_type: "heartbeat",
      session_id: sessionId || "",
      timestamp: Date.now(),
      mode: 2,
    },
    body: {},
  };
}

function buildPlanMultiRequest(question, sessionId, recommendContent, extraBody = {}) {
  const body = {
    session_id: sessionId || "",
    question,
    ...extraBody,
  };

  if (recommendContent && recommendContent.length > 0) {
    body.recommend_content = recommendContent;
  }

  return {
    header: {
      task_type: "text_to_llm",
      biz_type: "plan_multi",
      session_id: sessionId || "",
      mode: 2,
      status: 3,
    },
    body,
  };
}

function buildTripPlanRequest(planForm, sessionId) {
  const question = buildTripPlanQuestion(planForm);
  return {
    header: {
      task_type: "text_to_llm",
      biz_type: "plan_multi",
      session_id: sessionId || "",
    },
    body: {
      question,
      mode: "prefer",
      plan_form: planForm,
      preference: {
        scenic: [],
        food: [],
        accommodation: [],
        transportation: "",
      },
    },
  };
}

function buildTripPlanQuestion(planForm) {
  const departure = planForm.departure || planForm.departure_city || "";
  const destination = planForm.destinations?.[0] || "未明确目的地";
  const peopleType = planForm.people_type || `${planForm.people || 1}人`;
  const days = planForm.days || "";
  const daysText = days ? `${days}日游` : "旅行";
  const budgetText = planForm.min_budget || planForm.max_budget
    ? `预算${planForm.min_budget || "不限"}至${planForm.max_budget || "不限"}`
    : "无明确预算";
  const travelHint = planForm.travel_mode ? `，交通方式${planForm.travel_mode}` : "";
  const departText = departure ? `计划从${departure}出发，` : "计划";
  const stageHint =
    "请先只生成简约行程，包含每日主题、核心景点、美食/住宿概览，不要一次性生成详细行程或路书。";

  return `${departText}${peopleType}结伴进行${destination}${daysText}，行程规划${budgetText}${travelHint}。${stageHint}`;
}

function tryParseJsonText(value) {
  if (typeof value !== "string") return null;
  const text = value.trim();
  if (!text.startsWith("{") && !text.startsWith("[")) return null;
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function extractIntentCategory(frame) {
  const parsedContent = tryParseJsonText(frame.content);
  return parsedContent?.intent_category || frame.intent_category || "";
}

function parseLlmJsonContent(frame) {
  if (frame?.content_type !== "json") return null;
  if (typeof frame.content === "object" && frame.content !== null) return frame.content;
  return tryParseJsonText(frame.content);
}

function applyLlmContentToResult(frame, result, streamOutput) {
  const jsonContent = parseLlmJsonContent(frame);
  if (jsonContent) {
    result.rawJsonContent = jsonContent;
    if (typeof jsonContent.answer === "string" && jsonContent.answer) {
      result.answer = jsonContent.answer;
      result.content += jsonContent.answer;
      if (streamOutput) process.stdout.write(jsonContent.answer);
    }
    if (jsonContent.summary_plan) {
      result.summaryPlan = jsonContent.summary_plan;
      if (!result.answer) {
        const fallback = "已收到结构化行程结果（summary_plan）。";
        result.content += fallback;
        if (streamOutput) process.stdout.write(fallback);
      }
    }
    if (jsonContent.detailed_plan || jsonContent.detailedPlan) {
      result.detailedPlan = jsonContent.detailed_plan || jsonContent.detailedPlan;
    }
    if (jsonContent.travel_guide || jsonContent.travelGuide) {
      result.travelGuide = jsonContent.travel_guide || jsonContent.travelGuide;
    }
    return true;
  }

  const chunk = asText(frame.content);
  result.content += chunk;
  if (streamOutput) process.stdout.write(chunk);
  return true;
}

function parseFrame(raw) {
  const text = raw.toString().trim();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch (error) {
    return { parse_error: error.message, raw: text };
  }
}

function asText(content) {
  if (content === undefined || content === null) return "";
  if (typeof content === "string") return content;
  return JSON.stringify(content);
}

function hasSummaryPlanError(frame) {
  if (!frame || frame.status !== "error") return false;
  const errText = `${asText(frame.error)} ${asText(frame.content)}`.toLowerCase();
  return errText.includes("summary_plan");
}

function inferFallbackDestination(question) {
  const text = question || "";
  if (text.includes("贵州")) return "贵州省";
  if (text.includes("重庆")) return "重庆市";
  if (text.includes("成都")) return "成都市";
  return "重庆市";
}

function buildFallbackPlanForm(question = "") {
  const destination = inferFallbackDestination(question);
  return normalizePlanForm({
    departure: "成都市",
    destinations: [destination],
    people: 1,
    people_type: "1成人、0儿童",
    travel_mode: "飞机",
    start_date: "2026/05/10",
    return_date: "2026/05/12",
  });
}

function hasRequiredCliPlanFields(args) {
  return Boolean(args.destination && args.startDate && args.returnDate);
}

function validatePlanFormRequired(raw) {
  const destination = raw.destinations?.[0] || raw.destination || raw.cities?.[0];
  if (!destination || !String(destination).trim()) {
    throw new Error("必填：目的地 (destination / destinations[0])");
  }
  const startDate = raw.start_date || raw.startDate;
  const returnDate = raw.return_date || raw.returnDate;
  if (!startDate || !String(startDate).trim()) {
    throw new Error("必填：开始日期 start_date (YYYY/MM/DD)");
  }
  if (!returnDate || !String(returnDate).trim()) {
    throw new Error("必填：返回日期 return_date (YYYY/MM/DD)");
  }
  let adults = raw.adults;
  let children = raw.children;
  if (raw.people_type) {
    const adultMatch = String(raw.people_type).match(/(\d+)\s*成人/);
    const childMatch = String(raw.people_type).match(/(\d+)\s*儿童/);
    if (adultMatch) adults = Number.parseInt(adultMatch[1], 10);
    if (childMatch) children = Number.parseInt(childMatch[1], 10);
  }
  const people = Number.parseInt(raw.people, 10);
  const total =
    (Number.isFinite(adults) && adults > 0 ? adults : 0) +
    (Number.isFinite(children) && children > 0 ? children : 0) +
    (Number.isFinite(people) && people > 0 ? people : 0);
  if (total <= 0 && !(Number.isFinite(adults) && adults > 0)) {
    throw new Error("必填：人数 (people 或 adults/children 或 people_type 如 2成人、0儿童)");
  }
}

function buildPlanFormFromCliArgs(args) {
  const adults = args.adults > 0 ? args.adults : 1;
  const children = args.children >= 0 ? args.children : 0;
  return normalizePlanForm({
    departure: args.departure,
    destination: args.destination,
    adults,
    children,
    start_date: args.startDate,
    return_date: args.returnDate,
    min_budget: args.minBudget,
    max_budget: args.maxBudget,
    travel_mode: args.travelMode,
    people: adults + children,
    people_type: `${adults}成人、${children}儿童`,
  });
}

function normalizePlanForm(raw = {}, { applyDefaults = true } = {}) {
  const destination =
    raw.destinations?.[0] ||
    raw.destination ||
    raw.cities?.[0] ||
    (applyDefaults ? inferFallbackDestination(raw.question || "") : "");
  const departure = raw.departure || raw.departure_city || "";
  const startDate = raw.start_date || raw.startDate || (applyDefaults ? "2026/05/10" : "");
  const returnDate = raw.return_date || raw.returnDate || (applyDefaults ? "2026/05/12" : "");
  let adults = raw.adults;
  let children = raw.children;
  if (!Number.isFinite(adults) || adults <= 0) {
    const people = Number.parseInt(raw.people, 10);
    adults = Number.isFinite(people) && people > 0 ? people : 1;
  }
  if (!Number.isFinite(children) || children < 0) children = 0;
  if (raw.people_type) {
    const match = String(raw.people_type).match(/(\d+)\s*成人/);
    if (match) adults = Number.parseInt(match[1], 10);
    const childMatch = String(raw.people_type).match(/(\d+)\s*儿童/);
    if (childMatch) children = Number.parseInt(childMatch[1], 10);
  }
  const people = adults + children;
  return {
    departure,
    departure_city: raw.departure_city || departure,
    destinations: Array.isArray(raw.destinations) && raw.destinations.length > 0 ? raw.destinations : [destination],
    cities: Array.isArray(raw.cities) && raw.cities.length > 0 ? raw.cities : [destination],
    people,
    people_type: raw.people_type || `${adults}成人、${children}儿童`,
    max_budget: raw.max_budget ?? raw.maxBudget ?? "",
    min_budget: raw.min_budget ?? raw.minBudget ?? "",
    travel_mode: raw.travel_mode || raw.travelMode || (applyDefaults ? "飞机" : ""),
    start_date: startDate,
    return_date: returnDate,
    days: raw.days || countTripDays(startDate, returnDate),
    city_days: raw.city_days || {},
    plan_type: raw.plan_type || "summary",
  };
}

function assertNotDetailedViaWebSocket(planForm) {
  if (planForm?.plan_type === "detailed") {
    console.error(
      "[error] plan_type=detailed 不能通过 plan_multi WebSocket 生成详细行程。",
    );
    console.error(
      "[error] 请改用: node scripts/create_detail.mjs --session-file <plan_multi_session.txt> --json",
    );
    throw new Error("Use scripts/create_detail.mjs for detailed itinerary (POST /api/plan/create_detail)");
  }
}

function loadPlanFormForArgs(args, { optional = false } = {}) {
  if (args.planFormFile) {
    if (!existsSync(args.planFormFile)) {
      throw new Error(`plan-form file not found: ${args.planFormFile}`);
    }
    const raw = JSON.parse(readFileSync(args.planFormFile, "utf8"));
    if (!optional) validatePlanFormRequired(raw);
    return normalizePlanForm(raw, { applyDefaults: optional });
  }
  if (hasRequiredCliPlanFields(args)) {
    const raw = {
      departure: args.departure,
      destination: args.destination,
      adults: args.adults,
      children: args.children,
      start_date: args.startDate,
      return_date: args.returnDate,
      min_budget: args.minBudget,
      max_budget: args.maxBudget,
      travel_mode: args.travelMode,
    };
    if (!optional) validatePlanFormRequired(raw);
    return buildPlanFormFromCliArgs(args);
  }
  if (args.tripPlanDirect && !optional) {
    throw new Error(
      "trip-plan-direct requires --plan-form-file or required CLI fields: --destination, --start-date, --return-date, --adults (optional: --departure, --children, budgets, --travel-mode)",
    );
  }
  return null;
}

function persistSessionId(args, sessionId) {
  if (!sessionId || !args.sessionFile) return;
  writeFileSync(args.sessionFile, `${sessionId}\n`, "utf8");
  if (args.verbose) console.error(`[session] saved to ${args.sessionFile}`);
}

function warnOpenClawInteractive(args) {
  if (!args.interactive) return;
  if (!process.stdin.isTTY) {
    console.error(
      "[warn] -i on non-TTY stdin is for local debugging only. OpenClaw must use single-shot + --trip-plan-direct + --plan-form-file.",
    );
  }
}

function processLlmFrame(frame, result, streamOutput) {
  const intentCategory = extractIntentCategory(frame);
  if (intentCategory) result.intentCategory = intentCategory;

  if (frame.category !== "llm") return false;

  if (frame.status === "middle" || (frame.status === "stop" && frame.content_type === "json")) {
    applyLlmContentToResult(frame, result, streamOutput);
    return false;
  }

  if (frame.status === "stop" && frame.content_type === "markdown") {
    return true;
  }

  return false;
}

function shouldFinishAfterTaskNotify(frame, result) {
  if (frame.category !== "task_notify" || frame.task_status !== "finished") return false;
  return Boolean(result.content || result.answer || result.summaryPlan);
}

class SummaryPlanFallbackError extends Error {
  constructor(frame, result = {}) {
    super(`Task failed: ${asText(frame.content) || JSON.stringify(frame)}`);
    this.name = "SummaryPlanFallbackError";
    this.frame = frame;
    this.sessionId = frame.session_id || result.sessionId || "";
    this.taskId = frame.task_id || result.taskId || "";
    this.rawError = asText(frame.error);
    this.rawContent = asText(frame.content);
    this.fallbackReason = "summary_plan_error";
  }
}

function logTraffic(args, direction, raw, extra = {}) {
  if (!args?.logFile) return;
  const line = JSON.stringify({
    ts: new Date().toISOString(),
    direction,
    raw,
    ...extra,
  });
  appendFileSync(args.logFile, `${line}\n`, "utf8");
}

function sendJson(ws, payload, argsOrVerbose) {
  const data = JSON.stringify(payload);
  const verbose = typeof argsOrVerbose === "object" ? argsOrVerbose.verbose : argsOrVerbose;
  if (verbose) console.error(`[send] ${data}`);
  if (typeof argsOrVerbose === "object") logTraffic(argsOrVerbose, "send", data, { payload });
  ws.send(data);
}

// --- Single-shot mode (unchanged behavior) ---

async function callPlanMultiOnce(args) {
  const result = {
    endpoint: args.endpoint,
    sessionId: args.sessionId,
    taskId: "",
    status: "",
    taskStatus: "",
    content: "",
    answer: "",
    summaryPlan: null,
    detailedPlan: null,
    travelGuide: null,
    rawJsonContent: null,
    llmCosts: "",
    intentCategory: "",
    frames: 0,
    heartbeatAcks: 0,
    fallbackTriggered: false,
    fallbackReason: "",
    firstTaskId: "",
    retryTaskId: "",
  };

  const url = buildUrl(args);
  const ws = new WebSocket(url, {
    perMessageDeflate: true,
    handshakeTimeout: 15_000,
    rejectUnauthorized: true,
    headers: buildWsHeaders(args),
  });

  let heartbeatTimer;
  let timeoutTimer;
  let settled = false;
  let fallbackRetryUsed = false;
  let fallbackPending = false;
  let fallbackRetryLogged = false;
  const upfrontPlanForm = args.tripPlanDirect ? loadPlanFormForArgs(args) : loadPlanFormForArgs(args, { optional: true });
  if (upfrontPlanForm) assertNotDetailedViaWebSocket(upfrontPlanForm);

  const cleanup = () => {
    if (heartbeatTimer) clearInterval(heartbeatTimer);
    if (timeoutTimer) clearTimeout(timeoutTimer);
  };

  return new Promise((resolve, reject) => {
    const finish = (error) => {
      if (settled) return;
      settled = true;
      cleanup();
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close(1000, "plan_multi_done");
      }
      if (error) reject(error);
      else resolve(result);
    };

    timeoutTimer = setTimeout(() => {
      finish(new Error(`Timed out after ${args.timeoutMs} ms`));
    }, args.timeoutMs);

    ws.on("open", () => {
      if (args.verbose) console.error("[state] websocket opened");
      sendJson(ws, buildHeartbeat(args.sessionId), args);
      heartbeatTimer = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          sendJson(ws, buildHeartbeat(result.sessionId || args.sessionId), args);
        }
      }, args.heartbeatMs);

      void delay(40).then(() => {
        if (ws.readyState === WebSocket.OPEN && !settled) {
          if (upfrontPlanForm) {
            if (args.verbose) console.error("[trip_plan] sending structured plan_form (trip-plan-direct)");
            sendJson(ws, buildTripPlanRequest(upfrontPlanForm, result.sessionId || args.sessionId), args);
          } else {
            sendJson(ws, buildPlanMultiRequest(args.question, args.sessionId, args.recommendContent), args);
          }
        }
      });
    });

    ws.on("message", (raw) => {
      logTraffic(args, "recv", raw.toString());
      const frame = parseFrame(raw);
      if (!frame) return;
      result.frames += 1;

      if (frame.parse_error) {
        if (args.verbose) console.error(`[ignore] non-json: ${frame.raw}`);
        return;
      }
      if (args.verbose) console.error(`[recv] ${JSON.stringify(frame)}`);

      if (frame.session_id) result.sessionId = frame.session_id;
      if (frame.task_id) result.taskId = frame.task_id;
      if (frame.status) result.status = frame.status;
      if (frame.task_status) result.taskStatus = frame.task_status;
      if (frame.llm_costs) result.llmCosts = frame.llm_costs;
      const intentCategory = extractIntentCategory(frame);
      if (intentCategory) result.intentCategory = intentCategory;

      if (frame.task_status === "created" && fallbackPending && frame.task_id && frame.task_id !== result.firstTaskId) {
        result.retryTaskId = frame.task_id;
        if (!fallbackRetryLogged) {
          fallbackRetryLogged = true;
          if (args.verbose) {
            console.error(
              `[fallback] retry task created session_id=${result.sessionId || args.sessionId || ""} first_task_id=${result.firstTaskId} retry_task_id=${result.retryTaskId}`,
            );
          }
          logTraffic(args, "fallback_retry", JSON.stringify({
            fallback_triggered: true,
            fallback_reason: result.fallbackReason,
            session_id: result.sessionId || args.sessionId || "",
            first_task_id: result.firstTaskId,
            retry_task_id: result.retryTaskId,
          }));
        }
      }

      if (frame.status === "error" || frame.task_status === "failed") {
        if (args.fallbackTripPlan && hasSummaryPlanError(frame) && !fallbackRetryUsed) {
          fallbackRetryUsed = true;
          fallbackPending = true;
          result.fallbackTriggered = true;
          result.fallbackReason = "summary_plan_error";
          result.firstTaskId = result.taskId || frame.task_id || "";
          const fallbackPlanForm = upfrontPlanForm || buildFallbackPlanForm(args.question);
          if (args.verbose) {
            console.error("[fallback] summary_plan error detected, retrying with trip_plan form");
          }
          logTraffic(args, "fallback", JSON.stringify({
            fallback_triggered: true,
            fallback_reason: result.fallbackReason,
            session_id: result.sessionId || args.sessionId || "",
            first_task_id: result.firstTaskId,
            retry_task_id: "",
            fallback_plan_form: fallbackPlanForm,
          }));
          result.status = "";
          result.taskStatus = "";
          result.content = "";
          result.answer = "";
          result.summaryPlan = null;
          result.detailedPlan = null;
          result.travelGuide = null;
          result.rawJsonContent = null;
          result.llmCosts = "";
          sendJson(ws, buildTripPlanRequest(fallbackPlanForm, result.sessionId || args.sessionId), args);
          return;
        }
        finish(new Error(`Task failed: ${asText(frame.content) || JSON.stringify(frame)}`));
        return;
      }
      if (frame.category === "system_notify") {
        if (frame.content === "heartbeat") result.heartbeatAcks += 1;
        return;
      }
      if (frame.category === "task_notify") {
        if (shouldFinishAfterTaskNotify(frame, result)) finish();
        return;
      }
      if (frame.category === "tts_notify") return;
      if (processLlmFrame(frame, result, false)) {
        finish();
        return;
      }
      if (frame.status === "stop" && frame.content_type === "markdown" && frame.category !== "task_notify") {
        if (result.content || result.summaryPlan || !args.tripPlanDirect) finish();
      }
    });

    ws.on("error", (error) => {
      logTraffic(args, "error", error.message);
      finish(error);
    });
    ws.on("close", (code, reason) => {
      logTraffic(args, "close", reason.toString(), { code });
      if (!settled) finish(new Error(`WebSocket closed: ${code} ${reason.toString()}`));
    });
  });
}

// --- Interactive multi-turn mode ---

class InteractiveSession {
  constructor(args) {
    this.args = args;
    this.sessionId = args.sessionId || "";
    /** Last structured plan_form sent; reused on summary_plan fallback without re-prompting. */
    this.lastPlanForm = null;
    this.ws = null;
    this.heartbeatTimer = null;
    this.connected = false;
    this.pendingResolve = null;
    this.pendingReject = null;
    this.pendingTimeout = null;
    this.currentResult = null;
    this.turnCount = 0;
  }

  async connect() {
    const url = buildUrl(this.args);
    this.ws = new WebSocket(url, {
      perMessageDeflate: true,
      handshakeTimeout: 15_000,
      rejectUnauthorized: true,
      headers: buildWsHeaders(this.args),
    });

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error("Connection timeout (15s)"));
      }, 15_000);

      this.ws.on("open", () => {
        clearTimeout(timeout);
        this.connected = true;
        if (this.args.verbose) console.error("[state] websocket opened");

        sendJson(this.ws, buildHeartbeat(this.sessionId), this.args);
        this.heartbeatTimer = setInterval(() => {
          if (this.ws.readyState === WebSocket.OPEN) {
            sendJson(this.ws, buildHeartbeat(this.sessionId), this.args);
          }
        }, this.args.heartbeatMs);

        resolve();
      });

      this.ws.on("message", (raw) => this._onMessage(raw));

      this.ws.on("error", (err) => {
        logTraffic(this.args, "error", err.message);
        if (!this.connected) {
          clearTimeout(timeout);
          reject(err);
        } else {
          this._finishTurn(err);
        }
      });

      this.ws.on("close", (code, reason) => {
        logTraffic(this.args, "close", reason?.toString() || "", { code });
        this.connected = false;
        if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
        this._finishTurn(new Error(`WebSocket closed: ${code} ${reason?.toString() || ""}`));
      });
    });
  }

  _onMessage(raw) {
    logTraffic(this.args, "recv", raw.toString());
    const frame = parseFrame(raw);
    if (!frame) return;

    if (frame.parse_error) {
      if (this.args.verbose) console.error(`[ignore] non-json: ${frame.raw}`);
      return;
    }
    if (this.args.verbose) console.error(`[recv] ${JSON.stringify(frame)}`);

    if (frame.session_id && frame.session_id !== this.sessionId) {
      this.sessionId = frame.session_id;
      if (this.currentResult) this.currentResult.sessionId = this.sessionId;
      if (this.args.verbose) console.error(`[session] updated to ${this.sessionId}`);
    }

    if (frame.status === "error" || frame.task_status === "failed") {
      if (hasSummaryPlanError(frame)) {
        this._finishTurn(new SummaryPlanFallbackError(frame, this.currentResult || {}));
      } else {
        this._finishTurn(new Error(`Task failed: ${asText(frame.content) || JSON.stringify(frame)}`));
      }
      return;
    }

    if (frame.category === "system_notify") {
      if (frame.content === "heartbeat") {
        if (this.currentResult) this.currentResult.heartbeatAcks += 1;
      } else if (typeof frame.content === "object" && frame.content?.msg) {
        console.error(`[system] ${frame.content.msg} (conn: ${frame.content.connectionId})`);
      }
      return;
    }

    if (!this.currentResult) return;

    if (frame.task_id) this.currentResult.taskId = frame.task_id;
    if (frame.status) this.currentResult.status = frame.status;
    if (frame.task_status) this.currentResult.taskStatus = frame.task_status;
    if (frame.llm_costs) this.currentResult.llmCosts = frame.llm_costs;
    const intentCategory = extractIntentCategory(frame);
    if (intentCategory) this.currentResult.intentCategory = intentCategory;

    if (frame.category === "task_notify") {
      if (shouldFinishAfterTaskNotify(frame, this.currentResult)) {
        this._finishTurn(null);
      }
      return;
    }

    if (frame.category === "tts_notify") return;

    if (processLlmFrame(frame, this.currentResult, true)) {
      this._finishTurn(null);
      return;
    }

    if (frame.status === "stop" && frame.content_type === "markdown" && frame.category !== "task_notify") {
      if (this.currentResult.content || this.currentResult.summaryPlan) {
        this._finishTurn(null);
      }
    }
  }

  _finishTurn(error) {
    if (!this.pendingResolve) return;
    if (this.pendingTimeout) {
      clearTimeout(this.pendingTimeout);
      this.pendingTimeout = null;
    }
    const resolve = this.pendingResolve;
    const reject = this.pendingReject;
    this.pendingResolve = null;
    this.pendingReject = null;

    if (error) reject(error);
    else resolve(this.currentResult);
  }

  async ask(question, recommendContent) {
    if (!this.connected || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error("WebSocket not connected");
    }

    this.turnCount += 1;
    this.currentResult = {
      turn: this.turnCount,
      sessionId: this.sessionId,
      taskId: "",
      status: "",
      taskStatus: "",
      content: "",
      answer: "",
      summaryPlan: null,
      detailedPlan: null,
      travelGuide: null,
      rawJsonContent: null,
      llmCosts: "",
      intentCategory: "",
      heartbeatAcks: 0,
      fallbackTriggered: false,
      fallbackReason: "",
      firstTaskId: "",
      retryTaskId: "",
    };

    return new Promise((resolve, reject) => {
      this.pendingResolve = resolve;
      this.pendingReject = reject;
      this.pendingTimeout = setTimeout(() => {
        this._finishTurn(new Error(`Turn ${this.turnCount} timed out after ${this.args.timeoutMs} ms`));
      }, this.args.timeoutMs);

      sendJson(this.ws, buildPlanMultiRequest(question, this.sessionId, recommendContent), this.args);
    });
  }

  async askTripPlan(planForm) {
    if (!this.connected || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error("WebSocket not connected");
    }

    this.turnCount += 1;
    this.currentResult = {
      turn: this.turnCount,
      sessionId: this.sessionId,
      taskId: "",
      status: "",
      taskStatus: "",
      content: "",
      answer: "",
      summaryPlan: null,
      detailedPlan: null,
      travelGuide: null,
      rawJsonContent: null,
      llmCosts: "",
      intentCategory: "",
      heartbeatAcks: 0,
      fallbackTriggered: false,
      fallbackReason: "",
      firstTaskId: "",
      retryTaskId: "",
    };

    return new Promise((resolve, reject) => {
      this.pendingResolve = resolve;
      this.pendingReject = reject;
      this.pendingTimeout = setTimeout(() => {
        this._finishTurn(new Error(`Turn ${this.turnCount} timed out after ${this.args.timeoutMs} ms`));
      }, this.args.timeoutMs);

      sendJson(this.ws, buildTripPlanRequest(planForm, this.sessionId), this.args);
    });
  }

  close() {
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      this.ws.close(1000, "session_end");
    }
  }
}

function promptLine(rl, label, defaultValue = "") {
  const suffix = defaultValue ? ` (${defaultValue})` : "";
  return new Promise((resolve) => {
    rl.question(`${label}${suffix}: `, (answer) => {
      const value = answer.trim();
      resolve(value || defaultValue);
    });
  });
}

function parsePositiveInt(value, fallback) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function countTripDays(startDate, returnDate) {
  const start = Date.parse(startDate.replaceAll("/", "-"));
  const end = Date.parse(returnDate.replaceAll("/", "-"));
  if (!Number.isFinite(start) || !Number.isFinite(end) || end < start) {
    return 1;
  }
  return Math.floor((end - start) / 86_400_000) + 1;
}

function shouldPromptPlanForm(args) {
  if (args.noPromptPlanForm) return false;
  return Boolean(process.stdin.isTTY);
}

async function resolvePlanForm(session, rl, args, question) {
  if (session.lastPlanForm) {
    if (args.verbose) {
      console.error("[trip_plan] reusing last plan_form from this session.");
    }
    return session.lastPlanForm;
  }
  const fromFileOrCli = loadPlanFormForArgs(args, { optional: true });
  if (fromFileOrCli) {
    if (args.verbose) console.error("[trip_plan] using plan_form from file/CLI args.");
    return fromFileOrCli;
  }
  const defaults = buildFallbackPlanForm(question);
  if (!shouldPromptPlanForm(args)) {
    if (args.verbose) {
      console.error("[trip_plan] stdin is not interactive; using default plan_form from question.");
    }
    return defaults;
  }
  return collectTripPlanForm(rl, {
    departure: defaults.departure,
    destination: defaults.destinations[0],
    adults: 1,
    children: 0,
    startDate: defaults.start_date,
    returnDate: defaults.return_date,
    minBudget: defaults.min_budget,
    maxBudget: defaults.max_budget,
    travelMode: defaults.travel_mode,
  });
}

async function collectTripPlanForm(rl, defaults = {}) {
  console.error("[trip_plan] 必填：目的地、日期、人数。可选：出发地、预算、交通。直接回车可用括号内默认值。");

  const destination = await promptLine(rl, "目的地（必填）", defaults.destination || defaults.destinations?.[0] || "成都市");
  const startDate = await promptLine(rl, "开始日期 YYYY/MM/DD（必填）", defaults.startDate || defaults.start_date || "2026/05/10");
  const returnDate = await promptLine(rl, "返回日期 YYYY/MM/DD（必填）", defaults.returnDate || defaults.return_date || "2026/05/12");
  const adults = parsePositiveInt(await promptLine(rl, "成人数（必填）", String(defaults.adults || 1)), 1);
  const children = Math.max(0, Number.parseInt(await promptLine(rl, "儿童数", String(defaults.children || 0)), 10) || 0);
  const departure = await promptLine(rl, "出发地（可选）", defaults.departure || "");
  const minBudget = await promptLine(rl, "最低预算（可选，留空=不限）", defaults.minBudget || defaults.min_budget || "");
  const maxBudget = await promptLine(rl, "最高预算（可选，留空=不限）", defaults.maxBudget || defaults.max_budget || "");
  const travelMode = await promptLine(rl, "交通方式（可选）", defaults.travelMode || defaults.travel_mode || "");
  const people = adults + children;
  validatePlanFormRequired({
    destination,
    start_date: startDate,
    return_date: returnDate,
    adults,
    children,
    people,
  });

  return {
    departure,
    departure_city: departure || destination,
    destinations: [destination],
    cities: [destination],
    people,
    people_type: `${adults}成人、${children}儿童`,
    max_budget: maxBudget,
    min_budget: minBudget,
    travel_mode: travelMode,
    start_date: startDate,
    return_date: returnDate,
    days: countTripDays(startDate, returnDate),
    city_days: {},
  };
}

function printTurnMetadata(result) {
  console.error(`[session_id] ${result.sessionId || ""}`);
  if (result.taskId) console.error(`[task_id] ${result.taskId}`);
  if (result.intentCategory) console.error(`[intent_category] ${result.intentCategory}`);
  if (result.answer) console.error(`[answer] ${result.answer}`);
  if (result.summaryPlan) {
    const overviewRows = Array.isArray(result.summaryPlan["行程概览表"]) ? result.summaryPlan["行程概览表"].length : 0;
    const days = result.summaryPlan["行程总结"]?.["天数"] || "";
    console.error(`[summary_plan] overview_rows=${overviewRows}, days=${days}`);
  }
  if (result.detailedPlan) {
    const dayRows = Array.isArray(result.detailedPlan.days) ? result.detailedPlan.days.length : "";
    console.error(`[detailed_plan] days=${dayRows}`);
  }
  if (result.travelGuide) {
    console.error(`[travel_guide] present=true`);
  }
  if (result.fallbackTriggered) {
    console.error(
      `[fallback] triggered reason=${result.fallbackReason || "summary_plan_error"} first_task_id=${result.firstTaskId || ""} retry_task_id=${result.retryTaskId || ""}`,
    );
  }
  console.error(`[content_chars] ${result.content.length}`);
  if (result.llmCosts) console.error(`[llm_costs] ${result.llmCosts}s`);
  if (!result.content) {
    console.error("[notice] This turn returned no llm text. Use --verbose or --log-file to inspect raw frames.");
  }
}

async function runInteractiveTurn(session, rl, args, question, { isFirstTurn, firstRecommend }) {
  const recommend = isFirstTurn ? firstRecommend : undefined;

  try {
    process.stdout.write("\nA> ");
    const result = await session.ask(question, recommend);
    process.stdout.write("\n");

    if (args.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      printTurnMetadata(result);
    }

    if (result.intentCategory === "trip_plan") {
      const planForm = await resolvePlanForm(session, rl, args, question);
      session.lastPlanForm = planForm;
      process.stdout.write("\nA> ");
      const planResult = await session.askTripPlan(planForm);
      process.stdout.write("\n");
      if (args.json) {
        console.log(JSON.stringify(planResult, null, 2));
      } else {
        printTurnMetadata(planResult);
      }
    }
  } catch (err) {
    if (args.fallbackTripPlan && err instanceof SummaryPlanFallbackError) {
      console.error("[fallback] summary_plan error detected, retrying with trip_plan form.");
      logTraffic(args, "fallback", JSON.stringify({
        fallback_triggered: true,
        fallback_reason: err.fallbackReason || "summary_plan_error",
        session_id: session.sessionId || "",
        first_task_id: err.taskId || "",
        retry_task_id: "",
      }));
      try {
        const planForm = await resolvePlanForm(session, rl, args, question);
        session.lastPlanForm = planForm;
        process.stdout.write("\nA> ");
        const planResult = await session.askTripPlan(planForm);
        planResult.fallbackTriggered = true;
        planResult.fallbackReason = err.fallbackReason || "summary_plan_error";
        planResult.firstTaskId = err.taskId || "";
        planResult.retryTaskId = planResult.taskId || "";
        logTraffic(args, "fallback_retry", JSON.stringify({
          fallback_triggered: true,
          fallback_reason: planResult.fallbackReason,
          session_id: session.sessionId || "",
          first_task_id: planResult.firstTaskId,
          retry_task_id: planResult.retryTaskId,
        }));
        process.stdout.write("\n");
        if (args.json) {
          console.log(JSON.stringify(planResult, null, 2));
        } else {
          printTurnMetadata(planResult);
        }
      } catch (fallbackErr) {
        console.error(`[fallback-error] ${fallbackErr.message}`);
      }
    } else {
      console.error(`[error] ${err.message}`);
    }
    if (!session.connected) {
      console.error("[interactive] Connection lost. Attempting reconnect...");
      try {
        await delay(1000);
        await session.connect();
        console.error("[interactive] Reconnected.");
      } catch (reconnErr) {
        throw reconnErr;
      }
    }
  }
}

async function runInteractive(args) {
  warnOpenClawInteractive(args);
  const session = new InteractiveSession(args);

  console.error("[interactive] Connecting... (local debugging; OpenClaw should use --trip-plan-direct)");
  await session.connect();
  console.error("[interactive] Connected. Type your questions (empty line or Ctrl+D to quit).");
  if (session.sessionId) {
    console.error(`[interactive] session_id: ${session.sessionId}`);
  }
  console.error("---");

  const rl = createInterface({ input: process.stdin, output: process.stderr, prompt: "Q> " });

  const firstRecommend = args.recommendContent.length > 0 ? args.recommendContent : undefined;
  let isFirstTurn = true;

  if (args.questionFromCli && args.question) {
    console.error(`[interactive] first question from --question: ${args.question}`);
    await runInteractiveTurn(session, rl, args, args.question, { isFirstTurn, firstRecommend });
    isFirstTurn = false;
    console.error("---");
  }

  rl.prompt();

  for await (const line of rl) {
    const question = line.trim();
    if (!question) {
      rl.prompt();
      continue;
    }

    if (question === "/quit" || question === "/exit") break;

    if (question === "/session") {
      console.error(`[session] ${session.sessionId || "(none)"}`);
      rl.prompt();
      continue;
    }

    if (question === "/plan") {
      try {
        const planForm = await resolvePlanForm(session, rl, args, args.question || "成都三日游");
        session.lastPlanForm = planForm;
        process.stdout.write("\nA> ");
        const result = await session.askTripPlan(planForm);
        process.stdout.write("\n");
        if (args.json) console.log(JSON.stringify(result, null, 2));
        else printTurnMetadata(result);
      } catch (err) {
        console.error(`[error] ${err.message}`);
      }
      console.error("---");
      rl.prompt();
      continue;
    }

    if (question === "/reconnect") {
      console.error("[interactive] Reconnecting...");
      session.close();
      await delay(500);
      await session.connect();
      console.error("[interactive] Reconnected.");
      rl.prompt();
      continue;
    }

    try {
      await runInteractiveTurn(session, rl, args, question, { isFirstTurn, firstRecommend });
    } catch (reconnErr) {
      console.error(`[fatal] Reconnect failed: ${reconnErr.message}`);
      break;
    }
    isFirstTurn = false;

    console.error("---");
    rl.prompt();
  }

  console.error("\n[interactive] Closing session.");
  session.close();
}

// --- Main entry ---

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
    warnOpenClawInteractive(args);

    if (args.saveTokenStdin) {
      const chunks = [];
      for await (const chunk of process.stdin) chunks.push(chunk);
      const raw = Buffer.concat(chunks).toString("utf8");
      const target = args.saveTokenFile || DEFAULT_TOKEN_FILE;
      const saved = saveTokenToFile(target, raw);
      const meta = decodeJwtMeta(saved.token);
      console.error(
        `[token-save] wrote ${saved.path} length=${saved.sanitizedLength} fingerprint=${tokenFingerprint(saved.token)}`,
      );
      if (meta) {
        console.error(`[token-save] exp=${meta.expIso} expired=${meta.expired}`);
      }
      if (args.userId || args.probeAuth) {
        args.token = saved.token;
        args.tokenSource = target;
        args.tokenDiagnosticsData = {
          sanitizedLength: saved.sanitizedLength,
          dotCount: 2,
          startsWithJwtPrefix: true,
        };
        args.probeAuth = true;
        if (!args.bearerAuth) args.bearerAuth = true;
        process.exitCode = await runTokenCheck(args);
      }
      return;
    }

    if (args.checkTokenOnly) {
      process.exitCode = await runTokenCheck(args);
      return;
    }

    if (args.interactive) {
      if (args.verbose) console.error("[mode] interactive multi-turn (-i, local terminal only)");
      await runInteractive(args);
    } else {
      if (args.verbose) {
        const mode = args.tripPlanDirect ? "single-shot trip-plan-direct (OpenClaw recommended)" : "single-shot plan_multi";
        console.error(`[mode] ${mode}`);
      }
      const result = await callPlanMultiOnce(args);
      persistSessionId(args, result.sessionId);
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log(result.content);
        printTurnMetadata(result);
      }
    }
  } catch (error) {
    if (error instanceof TokenError) {
      if (error.code !== "TOKEN_MISSING" && error.code !== "TOKEN_INVALID_FORMAT") {
        console.error(error.message);
      }
      process.exitCode = 2;
    } else if (isTokenAuthError(error)) {
      const meta = decodeJwtMeta(args?.token || "");
      printTokenSetupGuide(resolveAuthFailureReason(meta), {
        tokenSource: args?.tokenSource,
        expIso: meta?.expIso,
        expired: meta?.expired,
      });
      console.error(error.message);
      process.exitCode = 3;
    } else {
      console.error(error.message);
      process.exitCode = 1;
    }
  }
}

await main();
