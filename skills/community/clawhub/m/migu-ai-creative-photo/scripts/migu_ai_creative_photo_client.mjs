#!/usr/bin/env node

import https from "node:https";
import process from "node:process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, extname, resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";

const SKILL_DIR = dirname(dirname(fileURLToPath(import.meta.url)));
const TOKEN_FILE = resolve(SKILL_DIR, "secrets", "plan_multi_token.txt");
const SESSION_FILE = resolve(SKILL_DIR, "creative_photo_session.txt");
const HOST = "gulangyu.migudm.cn";
const ORIGIN = "https://gulangyu.migudm.cn";
const REFERER = "https://gulangyu.migudm.cn/multi-city-trip-agent/";
const UPLOAD_PATH = "/trip-agent-api/v1/file/upload";
const GENERATE_PATH = "/trip-agent-api/ai/creative/photo/generate";
const QUERY_PATH = "/trip-agent-api/ai/creative/photo/query";
const USER_AGENT = "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36";

class TokenError extends Error {}
const readText = (path) => path && existsSync(path) ? readFileSync(path, "utf8") : "";

function cleanToken(value) {
  let text = String(value || "").replace(/[\u0000\x00]/g, "").trim();
  const flags = { hadBearer: /\bBearer\s+/i.test(text), hadCodeFence: /```/.test(text), hadInvisible: /[\uFEFF\u200B-\u200D\u2060\u00A0]/.test(text) };
  text = text.replace(/^\uFEFF/, "").replace(/[\u200B-\u200D\u2060]/g, "").replace(/\u00A0/g, " ").replace(/```(?:text|txt|jwt|json)?/gi, "").replace(/```/g, "").replace(/^[\s"'`>]+|[\s"'`>]+$/g, "").replace(/^Bearer\s+/i, "").trim();
  const compact = text.replace(/\s+/g, "");
  const match = compact.match(/eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/);
  const token = match ? match[0] : compact;
  return { token, diagnostics: { sanitizedLength: token.length, dotCount: (token.match(/\./g) || []).length, startsWithJwtPrefix: token.startsWith("eyJ"), ...flags } };
}

function jwtMeta(token) {
  try {
    const data = JSON.parse(Buffer.from(token.split(".")[1], "base64url").toString("utf8"));
    const exp = Number(data.exp);
    return { exp, expIso: Number.isFinite(exp) ? new Date(exp * 1000).toISOString() : "", expired: Number.isFinite(exp) && exp <= Math.floor(Date.now() / 1000) };
  } catch { return null; }
}

function fingerprint(token) {
  const parts = token.split(".");
  return parts.length === 3 ? `${parts[0].slice(0, 8)}...${parts[2].slice(-8)}` : "";
}

function assertToken(args) {
  const d = args.tokenDiagnostics;
  if (!d.startsWithJwtPrefix || d.dotCount !== 2 || d.sanitizedLength <= 20) throw new TokenError(`Token is not a valid JWT shape. source=${args.tokenSource || "(none)"}`);
  if (jwtMeta(args.token)?.expired) throw new TokenError("Token is expired");
}

function parseArgs(argv) {
  const args = { token: "", tokenFile: "", tokenSource: "", checkToken: false, tokenDiagnosticsRequested: false, saveToken: false, saveTokenFile: "", imagePath: "", imageUrl: "", fieldName: "file", uploadOnly: false, gender: "", category: "", scenicName: "", sessionId: "", sessionFile: SESSION_FILE, resume: false, generateOnly: false, pollIntervalMs: 3000, pollTimeoutMs: 180000, json: false, verbose: false };
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i]; const next = () => { if (++i >= argv.length) throw new Error(`Missing value for ${key}`); return argv[i]; };
    if (key === "--token") { args.token = next(); args.tokenSource = "--token"; }
    else if (key === "--token-file") args.tokenFile = next();
    else if (key === "--check-token") args.checkToken = true;
    else if (key === "--token-diagnostics") args.tokenDiagnosticsRequested = true;
    else if (key === "--save-token-stdin") args.saveToken = true;
    else if (key === "--save-token-file") args.saveTokenFile = next();
    else if (key === "--image") args.imagePath = next();
    else if (key === "--image-url") args.imageUrl = next();
    else if (key === "--field-name") args.fieldName = next();
    else if (key === "--upload-only") args.uploadOnly = true;
    else if (key === "--gender") args.gender = next();
    else if (key === "--category") args.category = next();
    else if (key === "--scenic-name") args.scenicName = next();
    else if (key === "--session-id") args.sessionId = next();
    else if (key === "--session-file") args.sessionFile = next();
    else if (key === "--resume") args.resume = true;
    else if (key === "--generate-only") args.generateOnly = true;
    else if (key === "--poll-interval-ms") args.pollIntervalMs = Number.parseInt(next(), 10);
    else if (key === "--poll-timeout-ms") args.pollTimeoutMs = Number.parseInt(next(), 10);
    else if (key === "--json") args.json = true;
    else if (key === "--verbose") args.verbose = true;
    else if (key === "--help" || key === "-h") { console.log("Use --image <path> --gender male|female --scenic-name <name>, or --session-id <id>."); process.exit(0); }
    else throw new Error(`Unknown option: ${key}`);
  }
  if (!args.tokenFile && process.env.MIGU_AI_CREATIVE_PHOTO_TOKEN_FILE) args.tokenFile = process.env.MIGU_AI_CREATIVE_PHOTO_TOKEN_FILE;
  if (!args.tokenFile && process.env.PLAN_MULTI_TOKEN_FILE) args.tokenFile = process.env.PLAN_MULTI_TOKEN_FILE;
  if (!args.token && args.tokenFile) { args.token = readText(args.tokenFile); args.tokenSource = args.token ? args.tokenFile : ""; }
  if (!args.token && process.env.MIGU_AI_CREATIVE_PHOTO_TOKEN) { args.token = process.env.MIGU_AI_CREATIVE_PHOTO_TOKEN; args.tokenSource = "MIGU_AI_CREATIVE_PHOTO_TOKEN"; }
  if (!args.token && process.env.PLAN_MULTI_TOKEN) { args.token = process.env.PLAN_MULTI_TOKEN; args.tokenSource = "PLAN_MULTI_TOKEN"; }
  if (!args.token) { args.token = readText(TOKEN_FILE); args.tokenSource = args.token ? TOKEN_FILE : ""; }
  const cleaned = cleanToken(args.token); args.token = cleaned.token; args.tokenDiagnostics = cleaned.diagnostics;
  if (args.resume && !args.sessionId) args.sessionId = readText(args.sessionFile).trim();
  if (args.imagePath && args.imageUrl) throw new Error("Use only one of --image or --image-url");
  if (!Number.isFinite(args.pollIntervalMs) || args.pollIntervalMs <= 0) throw new Error("--poll-interval-ms must be positive");
  if (!Number.isFinite(args.pollTimeoutMs) || args.pollTimeoutMs <= 0) throw new Error("--poll-timeout-ms must be positive");
  return args;
}

function headers(args) {
  return { Accept: "application/json, text/plain, */*", Authorization: `Bearer ${args.token}`, Origin: ORIGIN, Referer: REFERER, "User-Agent": USER_AGENT, "X-APP-From": "10", "X-App-Version": "0.6.0" };
}

function request(args, method, path, body) {
  const payload = body === undefined ? null : Buffer.from(JSON.stringify(body), "utf8");
  const requestHeaders = headers(args);
  if (payload) { requestHeaders["Content-Type"] = "application/json"; requestHeaders["Content-Length"] = payload.length; }
  return new Promise((resolvePromise, rejectPromise) => {
    const req = https.request({ hostname: HOST, port: 443, path, method, headers: requestHeaders, rejectUnauthorized: true, timeout: args.pollTimeoutMs }, (res) => {
      let raw = ""; res.on("data", (part) => { raw += part.toString("utf8"); }); res.on("end", () => {
        let json; try { json = JSON.parse(raw); } catch { rejectPromise(new Error(`${method} ${path} returned invalid JSON: ${raw.slice(0, 400)}`)); return; }
        if (res.statusCode !== 200 || json.code !== 0) { rejectPromise(new Error(`${method} ${path} failed: ${json.msg || `HTTP ${res.statusCode}`}`)); return; }
        resolvePromise(json);
      });
    });
    req.on("timeout", () => req.destroy(new Error(`${method} ${path} timed out`))); req.on("error", rejectPromise); if (payload) req.write(payload); req.end();
  });
}

function mime(path) {
  return ({ ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp" })[extname(path).toLowerCase()] || "application/octet-stream";
}

function upload(args) {
  if (!existsSync(args.imagePath)) throw new Error(`Image file not found: ${args.imagePath}`);
  const boundary = `----OpenClawMiguPhoto${Date.now().toString(16)}`;
  const before = Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="${args.fieldName}"; filename="${basename(args.imagePath)}"\r\nContent-Type: ${mime(args.imagePath)}\r\n\r\n`);
  const payload = Buffer.concat([before, readFileSync(args.imagePath), Buffer.from(`\r\n--${boundary}--\r\n`)]);
  const requestHeaders = headers(args); requestHeaders["Content-Type"] = `multipart/form-data; boundary=${boundary}`; requestHeaders["Content-Length"] = payload.length;
  return new Promise((resolvePromise, rejectPromise) => {
    const req = https.request({ hostname: HOST, port: 443, path: UPLOAD_PATH, method: "POST", headers: requestHeaders, rejectUnauthorized: true, timeout: args.pollTimeoutMs }, (res) => {
      let raw = ""; res.on("data", (part) => { raw += part.toString("utf8"); }); res.on("end", () => {
        let json; try { json = JSON.parse(raw); } catch { rejectPromise(new Error(`Upload returned invalid JSON: ${raw.slice(0, 400)}`)); return; }
        if (res.statusCode !== 200 || json.code !== 0 || !json.data?.filePath) { rejectPromise(new Error(`Upload failed: ${raw.slice(0, 400)}`)); return; }
        resolvePromise({ fileName: json.data.fileName || "", filePath: json.data.filePath });
      });
    });
    req.on("timeout", () => req.destroy(new Error("Upload timed out"))); req.on("error", rejectPromise); req.write(payload); req.end();
  });
}

function category(args) {
  if (args.category) { const value = Number.parseInt(args.category, 10); if (value === 1 || value === 2) return value; throw new Error("--category must be 1 or 2"); }
  if (["male", "man"].includes(args.gender.toLowerCase())) return 1;
  if (["female", "woman"].includes(args.gender.toLowerCase())) return 2;
  throw new Error("Missing or invalid gender. Ask the user to choose male or female, or pass --category 1|2");
}

function saveSession(path, id) { mkdirSync(dirname(path), { recursive: true }); writeFileSync(path, `${id}\n`, "utf8"); }

async function poll(args, sessionId) {
  const deadline = Date.now() + args.pollTimeoutMs; let attempts = 0; let lastStatus = "unknown";
  while (Date.now() <= deadline) {
    attempts += 1; const data = (await request(args, "GET", `${QUERY_PATH}?${new URLSearchParams({ sessionId })}`)).data || {}; lastStatus = data.status;
    if (data.status === 2) return { sessionId, attempts, status: 2, photoUrls: data.photoUrls || [], tphotoUrls: data.tphotoUrls || [] };
    if (data.status !== 1) throw new Error(`Creative photo task returned unexpected status: ${data.status}`);
    if (args.verbose) console.error(`[poll] session=${sessionId} status=1 attempt=${attempts}`); await delay(args.pollIntervalMs);
  }
  throw new Error(`Creative photo polling timed out after ${args.pollTimeoutMs} ms. sessionId=${sessionId} lastStatus=${lastStatus}`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2)); const d = args.tokenDiagnostics;
  if (args.tokenDiagnosticsRequested || args.verbose) console.error(`[token] source=${args.tokenSource || "(none)"} sanitized_length=${d.sanitizedLength} dots=${d.dotCount} starts_eyJ=${d.startsWithJwtPrefix}`);
  if (args.saveToken) {
    const chunks = []; for await (const chunk of process.stdin) chunks.push(chunk); const clean = cleanToken(Buffer.concat(chunks).toString("utf8"));
    if (!clean.token.startsWith("eyJ") || clean.diagnostics.dotCount !== 2) throw new TokenError("Refusing to save: not a valid JWT after sanitization");
    const target = args.saveTokenFile || args.tokenFile || TOKEN_FILE; mkdirSync(dirname(target), { recursive: true }); writeFileSync(target, `${clean.token}\n`, "utf8");
    const meta = jwtMeta(clean.token); console.error(`[token-save] wrote ${target} length=${clean.diagnostics.sanitizedLength} fingerprint=${fingerprint(clean.token)}`); if (meta) console.error(`[token-save] exp=${meta.expIso} expired=${meta.expired}`); return;
  }
  if (args.checkToken) { assertToken(args); const meta = jwtMeta(args.token); console.error(`[token-check] OK source=${args.tokenSource || TOKEN_FILE} fingerprint=${fingerprint(args.token)} exp=${meta?.expIso || "unknown"} expired=${meta?.expired || false}`); return; }
  if (!args.token) throw new TokenError(`Missing token. Configure ${TOKEN_FILE}, --token-file, or MIGU_AI_CREATIVE_PHOTO_TOKEN.`); assertToken(args);
  const uploaded = args.imagePath ? await upload(args) : null;
  if (args.uploadOnly) { console.log(JSON.stringify({ uploaded }, null, 2)); return; }
  if (args.sessionId) { console.log(JSON.stringify({ result: await poll(args, args.sessionId) }, null, 2)); return; }
  const fileUrl = args.imageUrl || uploaded?.filePath; if (!fileUrl) throw new Error("Missing image. Ask the user for a local photo or uploaded image URL");
  if (!args.scenicName.trim()) throw new Error("Missing scenic name. Ask the user which scenic spot they want for the photo");
  const usedCategory = category(args); const generated = await request(args, "POST", GENERATE_PATH, { fileUrl, category: usedCategory, content: args.scenicName });
  if (typeof generated.data !== "string" || !generated.data) throw new Error("Generate response did not include a session ID");
  const generation = { sessionId: generated.data, category: usedCategory, scenicName: args.scenicName }; saveSession(args.sessionFile, generation.sessionId);
  const result = args.generateOnly ? null : await poll(args, generation.sessionId); console.log(JSON.stringify({ uploaded, generation, result }, null, 2));
}

main().catch((error) => { console.error(error instanceof TokenError ? `[token-error] ${error.message}` : `[error] ${error.message}`); process.exitCode = error instanceof TokenError ? 2 : 1; });
