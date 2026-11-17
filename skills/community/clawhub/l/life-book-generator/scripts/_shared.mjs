import fs from "node:fs/promises";

function readArgValue(args, index) {
  const value = args[index + 1];
  if (!value || value.startsWith("--")) throw new Error(`MISSING_VALUE:${args[index]}`);
  return value;
}

export function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith("--")) continue;
    const key = item.slice(2);
    if (key === "help") {
      args.help = true;
      continue;
    }
    args[key] = readArgValue(argv, index);
    index += 1;
  }
  return args;
}

export function resolveBaseUrl(args) {
  const raw = String(args["base-url"] ?? process.env.LIFE_BOOK_BASE_URL ?? "").trim();
  if (!raw) throw new Error("LIFE_BOOK_BASE_URL_REQUIRED");
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new Error("LIFE_BOOK_BASE_URL_INVALID");
  }
  if (url.protocol !== "http:" && url.protocol !== "https:") throw new Error("LIFE_BOOK_BASE_URL_INVALID");
  url.pathname = url.pathname.replace(/\/+$/, "");
  url.search = "";
  url.hash = "";
  return url.toString().replace(/\/$/, "");
}

export function resolveTimeoutMs(args) {
  const raw = String(args["timeout-ms"] ?? process.env.LIFE_BOOK_TIMEOUT_MS ?? "15000").trim();
  const value = Number(raw);
  if (!Number.isFinite(value) || value <= 0) throw new Error("LIFE_BOOK_TIMEOUT_MS_INVALID");
  return value;
}

export function resolveAgentApiKey(args) {
  return String(args["agent-api-key"] ?? process.env.LIFE_BOOK_AGENT_API_KEY ?? "").trim();
}

export function resolveTaskToken(args) {
  return String(args["task-token"] ?? process.env.LIFE_BOOK_TASK_TOKEN ?? "").trim();
}

export async function readJsonInput(args) {
  if (args.input) return JSON.parse(String(args.input));
  if (args["input-file"]) return JSON.parse(await fs.readFile(String(args["input-file"]), "utf8"));
  if (!process.stdin.isTTY) {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const text = Buffer.concat(chunks).toString("utf8").trim();
    if (text) return JSON.parse(text);
  }
  throw new Error("INPUT_REQUIRED");
}

export async function requestJson(baseUrl, path, init, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`${baseUrl}${path}`, { ...init, signal: controller.signal });
    const text = await response.text();
    const body = text ? JSON.parse(text) : null;
    if (!response.ok) {
      const error = new Error(body?.error ?? `HTTP_${response.status}`);
      error.status = response.status;
      error.body = body;
      throw error;
    }
    return body;
  } finally {
    clearTimeout(timer);
  }
}

export async function requestMaybeJson(baseUrl, path, init, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`${baseUrl}${path}`, { ...init, signal: controller.signal });
    const text = await response.text();
    const body = text ? JSON.parse(text) : null;
    return { response, body };
  } finally {
    clearTimeout(timer);
  }
}

export function printJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

export function exitWithHelp(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}
