#!/usr/bin/env node

import https from "node:https";
import process from "node:process";
import {
  appendFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { basename, dirname, extname, resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";
import WebSocket from "ws";

const SKILL_DIR = dirname(dirname(fileURLToPath(import.meta.url)));
const DEFAULT_TOKEN_FILE = resolve(SKILL_DIR, "secrets", "plan_multi_token.txt");
const DEFAULT_SESSION_FILE = resolve(SKILL_DIR, "guide_session.txt");
const HOST = "gulangyu.migudm.cn";
const UPLOAD_PATH = "/trip-agent-api/v1/file/upload";
const DEFAULT_ENDPOINT = "wss://gulangyu.migudm.cn/trip-agent/ws/api/ws";
const DEFAULT_ORIGIN = "https://gulangyu.migudm.cn";
const DEFAULT_REFERER = "https://gulangyu.migudm.cn/multi-city-trip-agent/";
const DEFAULT_WS_APP_VERSION = "0.6.4";
const DEFAULT_WS_VERSION = "v0.6.4";
const DEFAULT_UPLOAD_APP_VERSION = "0.6.0";
const DEFAULT_TENANT = "hmxt";
const DEFAULT_HEARTBEAT_MS = 30_000;
const DEFAULT_TIMEOUT_MS = 120_000;

class TokenError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "TokenError";
    this.code = code;
  }
}

function readTextFileIfExists(filePath) {
  if (!filePath || !existsSync(filePath)) return "";
  return readFileSync(filePath, "utf8");
}

function stripNullBytes(value) {
  return String(value || "").replace(/[\u0000\x00]/g, "").trim();
}

function sanitizeTokenInput(value) {
  let text = stripNullBytes(value);
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

function tokenFingerprint(token) {
  const parts = String(token || "").split(".");
  if (parts.length !== 3) return "";
  return `${parts[0].slice(0, 8)}...${parts[2].slice(-8)}`;
}

function assertTokenFormat(args) {
  const d = args.tokenDiagnosticsData;
  if (d.startsWithJwtPrefix && d.dotCount === 2 && d.sanitizedLength > 20) return;
  throw new TokenError(
    "TOKEN_INVALID_FORMAT",
    `Token is not a valid JWT shape after sanitization. source=${args.tokenSource || "(none)"}`,
  );
}

function saveTokenToFile(targetPath, rawToken) {
  const clean = sanitizeTokenInput(rawToken);
  if (!clean.token.startsWith("eyJ") || clean.diagnostics.dotCount !== 2) {
    throw new TokenError("TOKEN_INVALID_FORMAT", "Refusing to save: not a valid JWT after sanitization");
  }
  mkdirSync(dirname(targetPath), { recursive: true });
  writeFileSync(targetPath, `${clean.token}\n`, "utf8");
  return { path: targetPath, token: clean.token, ...clean.diagnostics };
}

function parseArgs(argv) {
  const args = {
    endpoint: DEFAULT_ENDPOINT,
    token: "",
    tokenFile: "",
    tokenSource: "",
    tokenDiagnostics: false,
    checkTokenOnly: false,
    probeAuth: false,
    saveTokenStdin: false,
    saveTokenFile: "",
    bearerAuth: true,
    insecure: false,
    userId: "",
    clientType: "web",
    wsAppVersion: DEFAULT_WS_APP_VERSION,
    wsVersion: DEFAULT_WS_VERSION,
    tenant: DEFAULT_TENANT,
    uploadAppVersion: DEFAULT_UPLOAD_APP_VERSION,
    question: "",
    prompt: "",
    title: "【图片】",
    imagePath: "",
    imageUrl: "",
    fieldName: "file",
    uploadOnly: false,
    sessionId: "",
    sessionFile: DEFAULT_SESSION_FILE,
    heartbeatMs: DEFAULT_HEARTBEAT_MS,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    json: false,
    verbose: false,
    logFile: "",
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      i += 1;
      if (i >= argv.length) throw new Error(`Missing value for ${arg}`);
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
      case "--no-bearer":
        args.bearerAuth = false;
        break;
      case "--bearer":
        args.bearerAuth = true;
        break;
      case "--insecure":
        args.insecure = true;
        break;
      case "--user-id":
        args.userId = next();
        break;
      case "--question":
        args.question = next();
        break;
      case "--prompt":
        args.prompt = next();
        break;
      case "--title":
        args.title = next();
        break;
      case "--image":
        args.imagePath = next();
        break;
      case "--image-url":
        args.imageUrl = next();
        break;
      case "--field-name":
        args.fieldName = next();
        break;
      case "--upload-only":
        args.uploadOnly = true;
        break;
      case "--session-id":
        args.sessionId = next();
        break;
      case "--session-file":
        args.sessionFile = next();
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
      case "--ws-app-version":
        args.wsAppVersion = next();
        break;
      case "--upload-app-version":
        args.uploadAppVersion = next();
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
      case "--help":
      case "-h":
        printHelp();
        process.exit(0);
        break;
      default:
        throw new Error(`Unknown option: ${arg}`);
    }
  }

  if (!args.userId && process.env.PLAN_MULTI_USER_ID) args.userId = process.env.PLAN_MULTI_USER_ID;
  if (!args.tokenFile && process.env.MIGU_AI_GUIDE_TOKEN_FILE) args.tokenFile = process.env.MIGU_AI_GUIDE_TOKEN_FILE;
  if (!args.tokenFile && process.env.PLAN_MULTI_TOKEN_FILE) args.tokenFile = process.env.PLAN_MULTI_TOKEN_FILE;
  if (!args.token && args.tokenFile) {
    args.token = readTextFileIfExists(args.tokenFile);
    args.tokenSource = args.token ? args.tokenFile : "";
  }
  if (!args.token && process.env.MIGU_AI_GUIDE_TOKEN) {
    args.token = process.env.MIGU_AI_GUIDE_TOKEN;
    args.tokenSource = "MIGU_AI_GUIDE_TOKEN";
  }
  if (!args.token && process.env.PLAN_MULTI_TOKEN) {
    args.token = process.env.PLAN_MULTI_TOKEN;
    args.tokenSource = "PLAN_MULTI_TOKEN";
  }
  if (!args.token) {
    args.token = readTextFileIfExists(DEFAULT_TOKEN_FILE);
    if (args.token) args.tokenSource = DEFAULT_TOKEN_FILE;
  }

  const tokenClean = sanitizeTokenInput(args.token || "");
  args.token = tokenClean.token;
  args.tokenDiagnosticsData = tokenClean.diagnostics;

  if (!args.sessionId && args.sessionFile && existsSync(args.sessionFile)) {
    args.sessionId = stripNullBytes(readFileSync(args.sessionFile, "utf8"));
  }

  if (!Number.isFinite(args.timeoutMs) || args.timeoutMs <= 0) {
    throw new Error("--timeout-ms must be a positive integer");
  }
  if (!Number.isFinite(args.heartbeatMs) || args.heartbeatMs <= 0) {
    throw new Error("--heartbeat-ms must be a positive integer");
  }
  if (args.imagePath && args.imageUrl) {
    throw new Error("Use only one of --image or --image-url");
  }

  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/migu_ai_guide_client.mjs --question "介绍成都" [options]
  node scripts/migu_ai_guide_client.mjs --image "photo.jpg" --prompt "讲解图片中的内容" [options]

Token:
  --token-file <path>             Default: this skill's secrets/plan_multi_token.txt.
  env MIGU_AI_GUIDE_TOKEN_FILE    Override token file.
  env PLAN_MULTI_TOKEN_FILE       Compatibility override using original env name.
  --save-token-stdin              Save a JWT from stdin to this skill's token file.
  --check-token [--probe-auth]    Check JWT shape and optionally WebSocket auth.

Guide:
  --question <text>               Text guide question.
  --image <path>                  Upload local image, then ask guide_chat.
  --image-url <url>               Use an already uploaded image URL.
  --prompt <text>                 Image prompt. Default: question or 讲解图片中的内容.
  --title <text>                  Image title. Default: 【图片】.
  --session-file <path>           Read/write session_id. Default: guide_session.txt.
  --json                          Print structured JSON result.
  --verbose                       Print request/frame logs to stderr.
  --insecure                      Disable TLS verification.
`);
}

function buildWsHeaders(args) {
  const headers = { Origin: DEFAULT_ORIGIN };
  if (args.bearerAuth) headers.Authorization = `Bearer ${args.token}`;
  return headers;
}

function buildUrl(args) {
  const url = new URL(args.endpoint);
  url.searchParams.set("token", args.token);
  if (args.userId) url.searchParams.set("user_id", args.userId);
  url.searchParams.set("client_type", args.clientType);
  url.searchParams.set("X-App-Version", args.wsAppVersion);
  url.searchParams.set("tenant", args.tenant);
  url.searchParams.set("version", args.wsVersion);
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

function buildTextGuideRequest(question, sessionId) {
  return {
    header: {
      task_type: "text_to_llm",
      biz_type: "guide_chat",
      session_id: sessionId || "",
    },
    body: {
      session_id: sessionId || "",
      question,
    },
  };
}

function buildImageGuideRequest(imageUrl, sessionId, prompt, title) {
  const imageList = [imageUrl];
  return {
    header: {
      task_type: "text_to_llm",
      biz_type: "guide_chat",
      session_id: sessionId || "",
      image_list: imageList,
    },
    body: {
      session_id: sessionId || "",
      question: "",
      prompt: prompt || "讲解图片中的内容",
      title: title || "【图片】",
      image_list: imageList,
    },
  };
}

function mimeTypeFor(filePath) {
  switch (extname(filePath).toLowerCase()) {
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    case ".png":
      return "image/png";
    case ".gif":
      return "image/gif";
    case ".webp":
      return "image/webp";
    case ".bmp":
      return "image/bmp";
    default:
      return "application/octet-stream";
  }
}

function postMultipartUpload(args) {
  if (!existsSync(args.imagePath)) {
    throw new Error(`Image file not found: ${args.imagePath}`);
  }

  const fileBuffer = readFileSync(args.imagePath);
  const filename = basename(args.imagePath);
  const boundary = `----OpenClawMiguGuide${Date.now().toString(16)}${Math.random().toString(16).slice(2)}`;
  const before = Buffer.from(
    `--${boundary}\r\n` +
      `Content-Disposition: form-data; name="${args.fieldName}"; filename="${filename}"\r\n` +
      `Content-Type: ${mimeTypeFor(args.imagePath)}\r\n\r\n`,
    "utf8",
  );
  const after = Buffer.from(`\r\n--${boundary}--\r\n`, "utf8");
  const payload = Buffer.concat([before, fileBuffer, after]);

  return new Promise((resolvePromise, rejectPromise) => {
    const req = https.request(
      {
        hostname: HOST,
        port: 443,
        path: UPLOAD_PATH,
        method: "POST",
        rejectUnauthorized: !args.insecure,
        timeout: args.timeoutMs,
        headers: {
          Accept: "application/json, text/plain, */*",
          Authorization: `Bearer ${args.token}`,
          "Content-Type": `multipart/form-data; boundary=${boundary}`,
          "Content-Length": payload.length,
          Origin: DEFAULT_ORIGIN,
          Referer: DEFAULT_REFERER,
          "User-Agent":
            "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
          "X-APP-From": "10",
          "X-App-Version": args.uploadAppVersion,
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => {
          raw += chunk.toString("utf8");
        });
        res.on("end", () => {
          let json = null;
          try {
            json = JSON.parse(raw);
          } catch {
            // Keep raw body in the thrown error below.
          }
          if (res.statusCode !== 200) {
            rejectPromise(new Error(`Upload HTTP ${res.statusCode}: ${raw.slice(0, 400)}`));
            return;
          }
          if (!json || json.code !== 0 || !json.data?.filePath) {
            rejectPromise(new Error(`Upload failed: ${raw.slice(0, 400)}`));
            return;
          }
          resolvePromise({
            statusCode: res.statusCode,
            fileName: json.data.fileName || "",
            filePath: json.data.filePath,
            raw: json,
          });
        });
      },
    );

    req.on("timeout", () => req.destroy(new Error(`Upload timeout after ${args.timeoutMs} ms`)));
    req.on("error", rejectPromise);
    req.write(payload);
    req.end();
  });
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

function applyLlmFrame(frame, result) {
  if (frame.content_type === "json") {
    const jsonContent = typeof frame.content === "object" ? frame.content : tryParseJsonText(frame.content);
    if (jsonContent) {
      result.rawJsonContent = jsonContent;
      if (typeof jsonContent.answer === "string") {
        result.content += jsonContent.answer;
      }
      return;
    }
  }
  result.content += asText(frame.content);
}

function logTraffic(args, direction, raw, extra = {}) {
  if (!args.logFile) return;
  appendFileSync(
    args.logFile,
    `${JSON.stringify({ ts: new Date().toISOString(), direction, raw, ...extra })}\n`,
    "utf8",
  );
}

function sendJson(ws, payload, args) {
  const data = JSON.stringify(payload);
  if (args.verbose) console.error(`[send] ${data}`);
  logTraffic(args, "send", data, { payload });
  ws.send(data);
}

function persistSessionId(args, sessionId) {
  if (!sessionId || !args.sessionFile) return;
  writeFileSync(args.sessionFile, `${sessionId}\n`, "utf8");
  if (args.verbose) console.error(`[session] saved to ${args.sessionFile}`);
}

function probeWsAuth(args) {
  return new Promise((resolveProbe) => {
    const ws = new WebSocket(buildUrl(args), {
      perMessageDeflate: true,
      handshakeTimeout: 12_000,
      rejectUnauthorized: !args.insecure,
      headers: buildWsHeaders(args),
    });
    let settled = false;
    const done = (ok, message) => {
      if (settled) return;
      settled = true;
      try {
        ws.close();
      } catch {
        // ignore
      }
      resolveProbe({ ok, message });
    };
    ws.on("open", () => done(true, "websocket_open"));
    ws.on("error", (err) => done(false, err.message));
    ws.on("close", (code) => {
      if (!settled) done(false, `closed_${code}`);
    });
    setTimeout(() => done(false, "probe_timeout"), 12_000);
  });
}

async function runTokenCheck(args) {
  if (!args.token) {
    console.error(`[token-check] missing token. expected file: ${DEFAULT_TOKEN_FILE}`);
    return 2;
  }
  try {
    assertTokenFormat(args);
  } catch (error) {
    console.error(`[token-check] ${error.message}`);
    return 2;
  }
  const meta = decodeJwtMeta(args.token);
  console.error("[token-check] OK: JWT format looks valid.");
  console.error(`[token-check] source=${args.tokenSource || DEFAULT_TOKEN_FILE}`);
  console.error(`[token-check] fingerprint=${tokenFingerprint(args.token)}`);
  const d = args.tokenDiagnosticsData;
  console.error(`[token-check] length=${d.sanitizedLength} dots=${d.dotCount} starts_eyJ=${d.startsWithJwtPrefix}`);
  if (meta) console.error(`[token-check] exp=${meta.expIso} expired=${meta.expired}`);
  if (!args.probeAuth) return 0;

  const probe = await probeWsAuth(args);
  if (probe.ok) {
    console.error("[token-check] probe: WebSocket auth OK");
    return 0;
  }
  console.error(`[token-check] probe: WebSocket auth FAILED (${probe.message})`);
  return 3;
}

async function callGuideOnce(args, uploaded) {
  const imageUrl = args.imageUrl || uploaded?.filePath || "";
  if (!imageUrl && !args.question) {
    throw new Error("Missing guide input: pass --question, --image, or --image-url");
  }

  const result = {
    endpoint: args.endpoint,
    sessionId: args.sessionId || "",
    status: "",
    taskStatus: "",
    contentType: "",
    content: "",
    rawJsonContent: null,
    frames: 0,
    heartbeatAcks: 0,
    uploaded: uploaded || null,
  };

  const requestPayload = imageUrl
    ? buildImageGuideRequest(imageUrl, args.sessionId, args.prompt || args.question || "讲解图片中的内容", args.title)
    : buildTextGuideRequest(args.question, args.sessionId);

  const ws = new WebSocket(buildUrl(args), {
    perMessageDeflate: true,
    handshakeTimeout: 15_000,
    rejectUnauthorized: !args.insecure,
    headers: buildWsHeaders(args),
  });

  let heartbeatTimer;
  let timeoutTimer;
  let settled = false;

  const cleanup = () => {
    if (heartbeatTimer) clearInterval(heartbeatTimer);
    if (timeoutTimer) clearTimeout(timeoutTimer);
  };

  return new Promise((resolveGuide, rejectGuide) => {
    const finish = (error) => {
      if (settled) return;
      settled = true;
      cleanup();
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close(1000, "guide_chat_done");
      }
      if (!error) persistSessionId(args, result.sessionId);
      if (error) rejectGuide(error);
      else resolveGuide({ ...result, request: requestPayload });
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
          sendJson(ws, requestPayload, args);
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
      if (frame.status) result.status = frame.status;
      if (frame.task_status) result.taskStatus = frame.task_status;
      if (frame.content_type) result.contentType = frame.content_type;

      if (frame.status === "error" || frame.task_status === "failed") {
        finish(new Error(`Task failed: ${asText(frame.content) || JSON.stringify(frame)}`));
        return;
      }

      if (frame.category === "system_notify") {
        if (frame.content === "heartbeat") result.heartbeatAcks += 1;
        return;
      }

      if (frame.category === "llm") {
        if (frame.content !== undefined && frame.content !== null) {
          applyLlmFrame(frame, result);
          if (!args.json) process.stdout.write(asText(frame.content));
        }
        if (frame.status === "stop") finish();
        return;
      }

      if (frame.category === "task_notify" && frame.task_status === "finished" && result.content) {
        finish();
      }
    });

    ws.on("error", (error) => {
      logTraffic(args, "error", error.message);
      finish(error);
    });
    ws.on("close", (code, reason) => {
      logTraffic(args, "close", reason.toString(), { code });
      if (!settled) {
        if (result.content) finish();
        else finish(new Error(`WebSocket closed: ${code} ${reason.toString()}`));
      }
    });
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.tokenDiagnostics || args.verbose) {
    const d = args.tokenDiagnosticsData;
    console.error(`[token] source=${args.tokenSource || "(none)"}`);
    console.error(`[token] sanitized_length=${d.sanitizedLength} dots=${d.dotCount} starts_eyJ=${d.startsWithJwtPrefix}`);
    if (d.hadBearer || d.hadCodeFence || d.hadInvisible) {
      console.error(`[token] cleaned bearer=${d.hadBearer} code_fence=${d.hadCodeFence} invisible_chars=${d.hadInvisible}`);
    }
  }

  if (args.saveTokenStdin) {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const target = args.saveTokenFile || args.tokenFile || DEFAULT_TOKEN_FILE;
    const saved = saveTokenToFile(target, Buffer.concat(chunks).toString("utf8"));
    const meta = decodeJwtMeta(saved.token);
    console.error(`[token-save] wrote ${saved.path} length=${saved.sanitizedLength} fingerprint=${tokenFingerprint(saved.token)}`);
    if (meta) console.error(`[token-save] exp=${meta.expIso} expired=${meta.expired}`);
    return;
  }

  if (args.checkTokenOnly) {
    process.exitCode = await runTokenCheck(args);
    return;
  }

  if (!args.token) {
    throw new TokenError(
      "TOKEN_MISSING",
      `Missing token. Configure ${DEFAULT_TOKEN_FILE}, --token-file, MIGU_AI_GUIDE_TOKEN, or PLAN_MULTI_TOKEN.`,
    );
  }
  assertTokenFormat(args);

  let uploaded = null;
  if (args.imagePath) {
    uploaded = await postMultipartUpload(args);
    if (args.verbose) console.error(`[upload] ${uploaded.filePath}`);
  }

  if (args.uploadOnly) {
    console.log(JSON.stringify({ uploaded }, null, 2));
    return;
  }

  const result = await callGuideOnce(args, uploaded);
  if (args.json) {
    console.log(JSON.stringify(result, null, 2));
  } else if (!result.content.endsWith("\n")) {
    process.stdout.write("\n");
  }
}

main().catch((error) => {
  if (error instanceof TokenError) {
    console.error(`[token-error] ${error.message}`);
    process.exitCode = 2;
    return;
  }
  console.error(`[error] ${error.message}`);
  process.exitCode = 1;
});
