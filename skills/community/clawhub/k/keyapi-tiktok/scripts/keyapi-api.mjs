import { existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const platform = "tiktok";
const defaultBaseUrl = "https://api.keyapi.ai";
const defaultTimeoutMs = 30000;
const defaultMaxStdoutBytes = 100000;
const defaultPreviewItems = 5;
const minNodeMajor = 18;
const managedBlockStart = "# >>> keyapi-skills >>>";
const managedBlockEnd = "# <<< keyapi-skills <<<";
const valueArgKeys = new Set([
  "path",
  "endpoint",
  "method",
  "query",
  "query-file",
  "query-param",
  "param",
  "body",
  "body-file",
  "image-file",
  "image-field",
  "timeout-ms",
  "max-stdout-bytes",
  "preview-items",
  "stdout",
  "output-file"
]);

function requireSupportedNodeVersion() {
  const major = Number(process.versions.node.split(".")[0]);
  if (Number.isNaN(major) || major < minNodeMajor) {
    throw new Error(`Node.js >= ${minNodeMajor} is required. Current version: ${process.versions.node}`);
  }
}

function parseArgs(argv) {
  const args = {
    method: "GET",
    queryParams: [],
    timeoutMs: defaultTimeoutMs,
    maxStdoutBytes: defaultMaxStdoutBytes,
    previewItems: defaultPreviewItems,
    stdout: "auto"
  };

  for (let index = 2; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }

    const equalsIndex = token.indexOf("=");
    const rawKey = equalsIndex === -1 ? token : token.slice(0, equalsIndex);
    const inlineValue = equalsIndex === -1 ? undefined : token.slice(equalsIndex + 1);
    const key = rawKey.slice(2);
    if (!valueArgKeys.has(key)) {
      throw new Error(`Unsupported argument: --${key}`);
    }

    const nextValue = inlineValue ?? argv[index + 1];
    if (!nextValue || nextValue.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    if (inlineValue === undefined) {
      index += 1;
    }

    if (key === "path") args.path = nextValue;
    else if (key === "endpoint") args.endpoint = nextValue;
    else if (key === "method") args.method = nextValue.toUpperCase();
    else if (key === "query") args.query = nextValue;
    else if (key === "query-file") args.queryFile = nextValue;
    else if (key === "query-param" || key === "param") args.queryParams.push(nextValue);
    else if (key === "body") args.body = nextValue;
    else if (key === "body-file") args.bodyFile = nextValue;
    else if (key === "image-file") args.imageFile = nextValue;
    else if (key === "image-field") args.imageField = nextValue;
    else if (key === "timeout-ms") args.timeoutMs = Number(nextValue);
    else if (key === "max-stdout-bytes") args.maxStdoutBytes = Number(nextValue);
    else if (key === "preview-items") args.previewItems = Number(nextValue);
    else if (key === "stdout") args.stdout = nextValue;
    else if (key === "output-file") args.outputFile = nextValue;
  }

  validateArgs(args);
  return args;
}

function validateArgs(args) {
  if (!Number.isFinite(args.timeoutMs)) {
    throw new Error("--timeout-ms must be a number");
  }
  if (!Number.isInteger(args.maxStdoutBytes) || args.maxStdoutBytes < 0) {
    throw new Error("--max-stdout-bytes must be a non-negative integer");
  }
  if (!Number.isInteger(args.previewItems) || args.previewItems < 0) {
    throw new Error("--preview-items must be a non-negative integer");
  }
  if (!["auto", "full", "preview", "none"].includes(args.stdout)) {
    throw new Error("--stdout must be one of: auto, full, preview, none");
  }
}

function isPlaceholder(value) {
  if (!value) {
    return true;
  }
  return new Set([
    "",
    "your_token",
    "your_token_here",
    "your_keyapi_token",
    "keyapi_token",
    "changeme",
    "replace_me",
    "todo"
  ]).has(String(value).trim().toLowerCase());
}

function detectProfilePath() {
  const homeDir = os.homedir();
  const shell = process.env.SHELL || "";

  if (process.platform === "win32") {
    return path.join(homeDir, "Documents", "PowerShell", "Microsoft.PowerShell_profile.ps1");
  }
  if (shell.includes("zsh")) {
    return path.join(homeDir, ".zshrc");
  }
  if (shell.includes("bash")) {
    const bashrc = path.join(homeDir, ".bashrc");
    return existsSync(bashrc) ? bashrc : path.join(homeDir, ".bash_profile");
  }

  return path.join(homeDir, ".profile");
}

function extractManagedBlock(contents) {
  const startIndex = contents.indexOf(managedBlockStart);
  if (startIndex === -1) {
    return undefined;
  }
  const endIndex = contents.indexOf(managedBlockEnd, startIndex + managedBlockStart.length);
  if (endIndex === -1) {
    return undefined;
  }
  return contents.slice(startIndex + managedBlockStart.length, endIndex);
}

function parseManagedValue(rawValue, profilePath) {
  const value = rawValue.trim();
  if (value.startsWith("'") && value.endsWith("'")) {
    const inner = value.slice(1, -1);
    if (profilePath.toLowerCase().endsWith(".ps1")) {
      return inner.replace(/''/g, "'");
    }
    return inner.split("'\\''").join("'");
  }
  if (value.startsWith('"') && value.endsWith('"')) {
    return value.slice(1, -1);
  }
  return value;
}

async function readTokenFromManagedProfile() {
  const profilePath = detectProfilePath();
  if (!existsSync(profilePath)) {
    return undefined;
  }

  const block = extractManagedBlock(await readFile(profilePath, "utf8"));
  if (!block) {
    return undefined;
  }

  const powershellMatch = block.match(/^\s*\$env:KEYAPI_TOKEN\s*=\s*(.+?)\s*$/m);
  const posixMatch = block.match(/^\s*export\s+KEYAPI_TOKEN=(.+?)\s*$/m);
  const rawValue = powershellMatch?.[1] ?? posixMatch?.[1];
  if (!rawValue) {
    return undefined;
  }

  const token = parseManagedValue(rawValue, profilePath).trim();
  return isPlaceholder(token) ? undefined : token;
}

async function buildAuthHeader() {
  if (!isPlaceholder(process.env.KEYAPI_TOKEN)) {
    return "Bearer " + String(process.env.KEYAPI_TOKEN).trim();
  }

  const profileToken = await readTokenFromManagedProfile();
  if (!isPlaceholder(profileToken)) {
    return "Bearer " + profileToken;
  }

  throw new Error(
    "KEYAPI_TOKEN is not configured in the current session or managed shell profile. Run node scripts/configure-keyapi-auth.mjs, then retry. Restart Codex only if needed."
  );
}

function parseJsonFlag(label, value) {
  if (!value) {
    return undefined;
  }
  try {
    return JSON.parse(String(value).replace(/^\uFEFF/, ""));
  } catch (error) {
    throw new Error(`Invalid JSON for ${label}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function appendQuery(url, query) {
  if (!query || typeof query !== "object" || Array.isArray(query)) {
    return;
  }

  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === "") {
      continue;
    }
    if (Array.isArray(value)) {
      url.searchParams.set(key, value.join(","));
    } else if (typeof value === "object") {
      url.searchParams.set(key, JSON.stringify(value));
    } else {
      url.searchParams.set(key, String(value));
    }
  }
}

async function loadQuery(args) {
  const merged = {};

  if (args.query) {
    Object.assign(merged, parseQueryObject("--query", args.query));
  }
  if (args.queryFile) {
    Object.assign(merged, parseQueryObject("--query-file", await readFile(args.queryFile, "utf8")));
  }
  for (const entry of args.queryParams) {
    const [key, value] = parseQueryParam(entry);
    if (value === "") {
      continue;
    }
    merged[key] = value;
  }

  return Object.keys(merged).length > 0 ? merged : undefined;
}

function parseQueryObject(label, value) {
  const parsed = parseJsonFlag(label, value);
  if (parsed === undefined) {
    return {};
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error(`${label} must be a JSON object.`);
  }
  return parsed;
}

function parseQueryParam(value) {
  const equalsIndex = String(value).indexOf("=");
  if (equalsIndex <= 0) {
    throw new Error("--query-param must use key=value.");
  }

  const key = String(value).slice(0, equalsIndex).trim();
  if (!key) {
    throw new Error("--query-param key cannot be empty.");
  }

  return [key, String(value).slice(equalsIndex + 1)];
}

function resolvePath(args) {
  if (args.path && args.endpoint) {
    throw new Error("Use either --path or --endpoint, not both.");
  }
  if (args.endpoint) {
    const endpoint = args.endpoint.startsWith("/") ? args.endpoint : `/${args.endpoint}`;
    return `/v1/${platform}${endpoint}`;
  }
  if (!args.path) {
    throw new Error("Missing required argument: --path or --endpoint");
  }
  if (!args.path.startsWith("/v1/")) {
    throw new Error("--path must start with /v1/; use --endpoint for platform-relative paths.");
  }
  if (!args.path.startsWith(`/v1/${platform}/`) && args.path !== `/v1/${platform}`) {
    throw new Error(`This skill can only call /v1/${platform}/... paths. Use the matching KeyAPI platform skill for other platforms.`);
  }
  return args.path;
}

function stripDataUrlPrefix(value) {
  return typeof value === "string" ? value.replace(/^data:[^,]*;base64,/, "") : value;
}

function hasKeyApiEnvelopeFailure(value) {
  return Boolean(
    value &&
      typeof value === "object" &&
      !Array.isArray(value) &&
      typeof value.code === "number" &&
      value.code !== 0
  );
}

async function loadBody(args) {
  if (args.body && args.bodyFile) {
    throw new Error("Use either --body or --body-file, not both.");
  }

  let body;
  if (args.bodyFile) {
    body = parseJsonFlag("--body-file", await readFile(args.bodyFile, "utf8"));
  } else {
    body = parseJsonFlag("--body", args.body);
  }

  if (args.imageFile) {
    const imageField = args.imageField || "image_base64";
    if (body === undefined) {
      body = {};
    }
    if (!body || typeof body !== "object" || Array.isArray(body)) {
      throw new Error("--image-file can only be merged into a JSON object body.");
    }
    body[imageField] = (await readFile(args.imageFile)).toString("base64");
  }

  const imageField = args.imageField || "image_base64";
  if (body && typeof body === "object" && !Array.isArray(body) && typeof body[imageField] === "string") {
    body[imageField] = stripDataUrlPrefix(body[imageField]);
  }

  return body;
}

async function writeResultFile(result, explicitOutputFile) {
  const outputPath = path.resolve(explicitOutputFile);
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(result, null, 2)}\n`, "utf8");
  return outputPath;
}

function byteLength(value) {
  return Buffer.byteLength(value, "utf8");
}

function summarizeResult(result, { savedTo, fullResultBytes, args }) {
  const data = result.data;
  const envelope = data && typeof data === "object" && !Array.isArray(data) ? data : undefined;
  const summary = {
    ok: result.ok,
    status: result.status,
    code: typeof envelope?.code === "number" ? envelope.code : undefined,
    message: typeof envelope?.message === "string" ? envelope.message : undefined,
    url: result.url,
    method: result.method,
    platform: result.platform,
    savedTo,
    fullResultBytes,
    stdoutMode: result.stdoutMode,
    note: savedTo
      ? "Full JSON was written to --output-file."
      : "Full JSON omitted from stdout. Re-run with --output-file <path> to save the complete response.",
    preview: makePreview(data, args.previewItems)
  };
  if (!savedTo) {
    delete summary.savedTo;
  }
  return summary;
}

function makePreview(value, maxItems, depth = 0) {
  if (depth >= 5) {
    return summarizeScalar(value);
  }
  if (Array.isArray(value)) {
    const items = value.slice(0, maxItems).map((item) => makePreview(item, maxItems, depth + 1));
    if (value.length > maxItems) {
      items.push({ truncated: value.length - maxItems });
    }
    return items;
  }
  if (value && typeof value === "object") {
    const entries = Object.entries(value);
    const preview = {};
    for (const [key, item] of entries.slice(0, 30)) {
      preview[key] = makePreview(item, maxItems, depth + 1);
    }
    if (entries.length > 30) {
      preview.__truncatedKeys = entries.length - 30;
    }
    return preview;
  }
  return summarizeScalar(value);
}

function summarizeScalar(value) {
  if (typeof value === "string" && value.length > 500) {
    return `${value.slice(0, 500)}... [truncated ${value.length - 500} chars]`;
  }
  return value;
}

async function emitSuccess(result, args) {
  const fullText = JSON.stringify(result, null, 2);
  const fullResultBytes = byteLength(fullText);

  let savedTo;
  if (args.outputFile) {
    savedTo = await writeResultFile(result, args.outputFile);
  }

  if (args.stdout === "none") {
    return;
  }

  if (
    args.stdout === "full" ||
    (args.stdout === "auto" &&
      fullResultBytes <= args.maxStdoutBytes &&
      !args.outputFile)
  ) {
    process.stdout.write(`${fullText}\n`);
    return;
  }

  result.stdoutMode = savedTo ? "preview-with-saved-result" : "preview";
  const summary = summarizeResult(result, {
    savedTo,
    fullResultBytes,
    args
  });
  process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
}

async function main() {
  requireSupportedNodeVersion();
  const args = parseArgs(process.argv);
  const requestPath = resolvePath(args);
  const baseUrl = defaultBaseUrl;
  const authHeader = await buildAuthHeader();
  const query = await loadQuery(args);
  const body = await loadBody(args);

  const url = new URL(requestPath, baseUrl);
  appendQuery(url, query);

  const headers = {
    Accept: "application/json",
    Authorization: authHeader
  };

  const options = {
    method: args.method,
    headers,
    signal: args.timeoutMs > 0 ? AbortSignal.timeout(args.timeoutMs) : undefined
  };

  if (body !== undefined && args.method !== "GET") {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  const text = await response.text();

  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = text;
  }

  const result = {
    ok: response.ok,
    status: response.status,
    url: url.toString(),
    method: args.method,
    platform,
    data: parsed
  };

  if (!response.ok || hasKeyApiEnvelopeFailure(parsed)) {
    process.stderr.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exitCode = 1;
    return;
  }

  await emitSuccess(result, args);
}

try {
  await main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
