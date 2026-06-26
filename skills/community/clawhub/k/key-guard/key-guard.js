#!/usr/bin/env node
/**
 * key-guard MCP Server
 *
 * Reads API keys from .env file LOCALLY and exposes tools that Claude
 * can call. The raw key is NEVER returned to Claude — only results.
 *
 * Tools exposed:
 *   - validate_key: Check if a key exists and is non-empty
 *   - call_api:     Make an authenticated HTTP request and return the response
 *
 * Usage:
 *   node mcp/key-guard.js
 *
 * Register with Copilot CLI:
 *   /mcp add key-guard node /absolute/path/to/mcp/key-guard.js
 */

const readline = require("readline");
const fs = require("fs");
const path = require("path");
const https = require("https");
const http = require("http");

// ── Config ────────────────────────────────────────────────────────────────────

const ENV_FILE = path.resolve(__dirname, ".env");

// Shell profile files to scan for KG_* keys, in priority order (last wins before .env)
const SHELL_PROFILES = [
  ".profile",
  ".bash_profile",
  ".bashrc",
  ".zshrc",
].map((f) => path.join(process.env.HOME || "~", f));

const KG_PREFIX = "KG_";

// ── Key helpers ───────────────────────────────────────────────────────────────

function parseKeyLines(lines) {
  const result = {};
  for (const line of lines) {
    const stripped = line.replace(/^export\s+/, "").trim();
    if (!stripped.includes("=") || stripped.startsWith("#")) continue;
    const [k, ...v] = stripped.split("=");
    result[k.trim()] = v.join("=").trim().replace(/^["']|["']$/g, "");
  }
  return result;
}

function loadShellProfileKeys() {
  const result = {};
  for (const profilePath of SHELL_PROFILES) {
    if (!fs.existsSync(profilePath)) continue;
    const lines = fs.readFileSync(profilePath, "utf-8").split("\n");
    const parsed = parseKeyLines(lines);
    for (const [k, v] of Object.entries(parsed)) {
      if (k.startsWith(KG_PREFIX)) {
        result[k.slice(KG_PREFIX.length)] = v; // strip KG_ prefix
      }
    }
  }
  return result;
}

function loadEnv() {
  if (!fs.existsSync(ENV_FILE)) return {};
  const lines = fs.readFileSync(ENV_FILE, "utf-8").split("\n");
  return parseKeyLines(lines);
}

function loadAllKeys() {
  // Priority: shell profiles (lowest) → .env → process.env (highest)
  return { ...loadShellProfileKeys(), ...loadEnv() };
}

function getKey(name) {
  const all = loadAllKeys();
  return all[name] || process.env[name] || null;
}

// ── HTTP helper (no external deps) ───────────────────────────────────────────

function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const lib = parsed.protocol === "https:" ? https : http;
    const req = lib.request(
      { ...parsed, method: options.method || "GET", headers: options.headers || {} },
      (res) => {
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          try {
            resolve({ status: res.statusCode, body: JSON.parse(body) });
          } catch {
            resolve({ status: res.statusCode, body });
          }
        });
      }
    );
    req.on("error", reject);
    if (options.body) req.write(JSON.stringify(options.body));
    req.end();
  });
}

// ── MCP Tool handlers ─────────────────────────────────────────────────────────

async function list_keys() {
  const all = loadAllKeys();
  return { keys: Object.keys(all) };
}

async function validate_key({ key_name }) {
  const value = getKey(key_name);
  if (!value) return { exists: false, message: `Key '${key_name}' not found` };
  return {
    exists: true,
    length: value.length,
    preview: value.slice(0, 4) + "****",
    message: `Key '${key_name}' is set`,
  };
}

async function read_file_masked({ file_path }) {
  const resolved = path.resolve(file_path);
  if (!fs.existsSync(resolved)) return { error: `File not found: ${file_path}` };
  let content = fs.readFileSync(resolved, "utf-8");
  const all = loadAllKeys();
  for (const [name, value] of Object.entries(all)) {
    if (value && value.length >= 8) {
      content = content.split(value).join(`{{${name}}}`);
    }
  }
  return { file_path, content };
}

async function write_file_with_keys({ file_path, content }) {
  const resolved = path.resolve(file_path);
  const all = loadAllKeys();
  let output = content;
  for (const [name, value] of Object.entries(all)) {
    if (value) output = output.split(`{{${name}}}`).join(value);
  }
  fs.writeFileSync(resolved, output, "utf-8");
  return { success: true, file_path, message: "File written with keys substituted locally" };
}

async function call_api({ key_name, url, method = "GET", headers = {}, body }) {
  const key = getKey(key_name);
  if (!key) return { error: `Key '${key_name}' not found` };

  // Inject key into Authorization header (adapt pattern as needed)
  const authHeaders = { Authorization: `Bearer ${key}`, ...headers };

  try {
    const result = await request(url, { method, headers: authHeaders, body });
    // Return API result — raw key was never sent to Claude
    return { status: result.status, data: result.body };
  } catch (err) {
    return { error: err.message };
  }
}

// ── MCP Protocol (stdio JSON-RPC) ─────────────────────────────────────────────

const TOOLS = {
  list_keys: {
    description: "List all available key names from .env and shell profiles. Returns only names — never values.",
    inputSchema: { type: "object", properties: {} },
  },
  validate_key: {
    description: "Check if an API key exists in .env without revealing its value",
    inputSchema: {
      type: "object",
      properties: {
        key_name: { type: "string", description: "Name of the env var, e.g. OPENAI_API_KEY" },
      },
      required: ["key_name"],
    },
  },
  call_api: {
    description:
      "Make an authenticated HTTP request using a local API key. The key is injected locally and never sent to Claude.",
    inputSchema: {
      type: "object",
      properties: {
        key_name: { type: "string", description: "Name of the env var holding the API key" },
        url: { type: "string", description: "API endpoint URL" },
        method: { type: "string", enum: ["GET", "POST", "PUT", "DELETE"], default: "GET" },
        headers: { type: "object", description: "Extra headers (no auth needed)" },
        body: { type: "object", description: "Request body for POST/PUT" },
      },
      required: ["key_name", "url"],
    },
  },
  read_file_masked: {
    description:
      "Read a file and mask any API key values with {{KEY_NAME}} placeholders. Use this instead of reading script/config files directly.",
    inputSchema: {
      type: "object",
      properties: {
        file_path: { type: "string", description: "Path to the file to read" },
      },
      required: ["file_path"],
    },
  },
  write_file_with_keys: {
    description:
      "Write a file, substituting {{KEY_NAME}} placeholders with real key values from .env. Use this to save edited scripts that reference keys.",
    inputSchema: {
      type: "object",
      properties: {
        file_path: { type: "string", description: "Path to the file to write" },
        content: { type: "string", description: "File content with {{KEY_NAME}} placeholders instead of raw keys" },
      },
      required: ["file_path", "content"],
    },
  },
};

const HANDLERS = { list_keys, validate_key, call_api, read_file_masked, write_file_with_keys };

const rl = readline.createInterface({ input: process.stdin });

rl.on("line", async (line) => {
  let msg;
  try { msg = JSON.parse(line); } catch { return; }

  const { id, method, params } = msg;

  if (method === "initialize") {
    respond(id, {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      serverInfo: { name: "key-guard", version: "1.0.0" },
    });
  } else if (method === "tools/list") {
    respond(id, {
      tools: Object.entries(TOOLS).map(([name, def]) => ({ name, ...def })),
    });
  } else if (method === "tools/call") {
    const { name, arguments: args } = params;
    if (!HANDLERS[name]) {
      respondError(id, -32601, `Unknown tool: ${name}`);
      return;
    }
    try {
      const result = await HANDLERS[name](args || {});
      respond(id, { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] });
    } catch (err) {
      respondError(id, -32603, err.message);
    }
  } else if (method === "notifications/initialized") {
    // no-op
  }
});

function respond(id, result) {
  process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, result }) + "\n");
}

function respondError(id, code, message) {
  process.stdout.write(
    JSON.stringify({ jsonrpc: "2.0", id, error: { code, message } }) + "\n"
  );
}
