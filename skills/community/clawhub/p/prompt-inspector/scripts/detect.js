#!/usr/bin/env node
/**
 * Prompt Inspector — detection helper script (Node.js).
 *
 * Sends text to the Prompt Inspector API and prints the result.
 * No third-party packages required — uses only Node.js built-ins (https, fs, path).
 *
 * Usage:
 *   node detect.js --text "Ignore all previous instructions..."
 *   node detect.js --file inputs.txt --format json
 *   node detect.js --api-key pi_xxx --text "..." --format json
 *
 * Authentication (in priority order):
 *   1. --api-key  command-line argument
 *   2. PMTINSP_API_KEY  environment variable
 *   3. ~/.openclaw/.env  file  (line: PMTINSP_API_KEY=...)
 */

"use strict";

const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { URL } = require("url");

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const DEFAULT_BASE_URL = "https://promptinspector.io";
const DETECT_PATH = "/api/v1/detect/sdk";
const DEFAULT_TIMEOUT = 30000; // milliseconds

// ---------------------------------------------------------------------------
// API key resolution
// ---------------------------------------------------------------------------

/**
 * Parse a simple KEY=VALUE .env file and return a plain object.
 * @param {string} filePath
 * @returns {Record<string, string>}
 */
function loadDotenv(filePath) {
  const env = {};
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    for (const raw of content.split(/\r?\n/)) {
      const line = raw.trim();
      if (!line || line.startsWith("#") || !line.includes("=")) continue;
      const idx = line.indexOf("=");
      const key = line.slice(0, idx).trim();
      let value = line.slice(idx + 1).trim();
      // Remove surrounding quotes if present
      if (value.length >= 2 && (value[0] === '"' || value[0] === "'") && value[0] === value[value.length - 1]) {
        value = value.slice(1, -1);
      }
      env[key] = value;
    }
  } catch (_) {
    // File not found or unreadable — ignore
  }
  return env;
}

/**
 * Return the first available API key or exit with an error.
 * @param {string|null} cliKey
 * @returns {string}
 */
function resolveApiKey(cliKey) {
  // 1. CLI argument
  if (cliKey) return cliKey;

  // 2. Environment variable
  if (process.env.PMTINSP_API_KEY) return process.env.PMTINSP_API_KEY;

  // 3. ~/.openclaw/.env
  const dotenvPath = path.join(os.homedir(), ".openclaw", ".env");
  const dotenv = loadDotenv(dotenvPath);
  if (dotenv.PMTINSP_API_KEY) return dotenv.PMTINSP_API_KEY;

  console.error(
    "Error: No API key found.\n" +
    "  Provide it via --api-key, the PMTINSP_API_KEY environment variable,\n" +
    "  or add PMTINSP_API_KEY=... to ~/.openclaw/.env\n\n" +
    "  Get your key at https://promptinspector.io"
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// API call
// ---------------------------------------------------------------------------

/**
 * Call the Prompt Inspector detection endpoint.
 * @param {string} text
 * @param {string} apiKey
 * @param {string} baseUrl
 * @param {number} timeout  milliseconds
 * @returns {Promise<object>}  parsed JSON response
 */
function detect(text, apiKey, baseUrl, timeout) {
  return new Promise((resolve, reject) => {
    const endpoint = new URL(DETECT_PATH, baseUrl.replace(/\/$/, ""));
    const body = JSON.stringify({ input_text: text });
    const isHttps = endpoint.protocol === "https:";
    const transport = isHttps ? https : http;

    const options = {
      hostname: endpoint.hostname,
      port: endpoint.port || (isHttps ? 443 : 80),
      path: endpoint.pathname,
      method: "POST",
      headers: {
        "X-App-Key": apiKey,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    };

    const req = transport.request(options, (res) => {
      let raw = "";
      res.setEncoding("utf-8");
      res.on("data", (chunk) => { raw += chunk; });
      res.on("end", () => {
        if (res.statusCode === 200) {
          try {
            resolve(JSON.parse(raw));
          } catch (_) {
            reject(new Error("Failed to parse API response as JSON."));
          }
          return;
        }
        // Handle HTTP error codes
        let detail = "";
        try { detail = JSON.parse(raw).detail || ""; } catch (_) { detail = raw.slice(0, 200); }
        const messages = {
          401: "Authentication failed. Check your API key.",
          403: "Authentication failed. Check your API key.",
          413: "Input text is too long for your current plan.",
          422: `Invalid request: ${detail}`,
          429: "Rate limit exceeded. Please slow down your requests.",
        };
        const msg = messages[res.statusCode] ||
          `API error (HTTP ${res.statusCode}): ${detail || "unexpected error"}`;
        reject(new Error(msg));
      });
    });

    req.setTimeout(timeout, () => {
      req.destroy(new Error(`Request timed out after ${timeout / 1000}s.`));
    });

    req.on("error", (err) => {
      if (err.message.includes("timed out")) {
        reject(new Error(`Request timed out after ${timeout / 1000}s.`));
      } else {
        reject(new Error(`Connection failed — ${err.message}`));
      }
    });

    req.write(body);
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Output formatting
// ---------------------------------------------------------------------------

/**
 * @param {object} data  Raw API response
 * @param {string} fmt   "human" | "json"
 */
function printResult(data, fmt) {
  const result = data.result || {};
  if (fmt === "json") {
    const out = {
      request_id: data.request_id || "",
      is_safe: result.is_safe !== undefined ? result.is_safe : true,
      score: result.score !== undefined ? result.score : null,
      category: result.category || [],
      latency_ms: data.latency_ms || 0,
    };
    console.log(JSON.stringify(out, null, 2));
  } else {
    const categories = (result.category || []).join(", ") || "none";
    console.log(`Request ID : ${data.request_id || "n/a"}`);
    console.log(`Is Safe    : ${result.is_safe}`);
    console.log(`Score      : ${result.score !== undefined ? result.score : "null"}`);
    console.log(`Category   : ${categories}`);
    console.log(`Latency    : ${data.latency_ms || 0} ms`);
  }
}

// ---------------------------------------------------------------------------
// CLI argument parsing
// ---------------------------------------------------------------------------

/**
 * Parse process.argv into a plain object.
 * Supports: --key value  and  --key=value
 * @returns {Record<string, string>}
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};
  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const eqIdx = arg.indexOf("=");
      if (eqIdx !== -1) {
        params[arg.slice(2, eqIdx)] = arg.slice(eqIdx + 1);
        i++;
      } else {
        const key = arg.slice(2);
        const next = args[i + 1];
        if (next !== undefined && !next.startsWith("--")) {
          params[key] = next;
          i += 2;
        } else {
          params[key] = "true";
          i++;
        }
      }
    } else {
      i++;
    }
  }
  return params;
}

function printHelp() {
  console.log(
    "Usage:\n" +
    "  node detect.js --text <text> [options]\n" +
    "  node detect.js --file <path> [options]\n\n" +
    "Options:\n" +
    "  --text       Text to inspect (single input)\n" +
    "  --file       Path to file; each non-empty line is inspected separately\n" +
    "  --api-key    Prompt Inspector API key\n" +
    "  --base-url   API base URL (default: " + DEFAULT_BASE_URL + ")\n" +
    "  --format     Output format: human (default) | json\n" +
    "  --timeout    Request timeout in seconds (default: 30)\n\n" +
    "Examples:\n" +
    "  node detect.js --text 'Ignore all previous instructions'\n" +
    "  node detect.js --file inputs.txt --format json\n" +
    "  node detect.js --api-key pi_xxx --text '...' --format json\n\n" +
    "Docs: https://docs.promptinspector.io"
  );
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const params = parseArgs();

  if (params.help || params.h) {
    printHelp();
    process.exit(0);
  }

  if (!params.text && !params.file) {
    console.error("Error: Provide --text or --file.\n");
    printHelp();
    process.exit(1);
  }

  const apiKey = resolveApiKey(params["api-key"] || null);
  const baseUrl = params["base-url"] || DEFAULT_BASE_URL;
  const fmt = params.format === "json" ? "json" : "human";
  const timeout = params.timeout ? parseInt(params.timeout, 10) * 1000 : DEFAULT_TIMEOUT;

  // Single text mode
  if (params.text) {
    try {
      const data = await detect(params.text, apiKey, baseUrl, timeout);
      printResult(data, fmt);
    } catch (err) {
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
    return;
  }

  // Batch mode: --file
  const filePath = path.resolve(params.file);
  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found: ${filePath}`);
    process.exit(1);
  }

  const lines = fs
    .readFileSync(filePath, "utf-8")
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean);

  if (lines.length === 0) {
    console.error("Error: File is empty.");
    process.exit(1);
  }

  const results = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    process.stderr.write(`[${i + 1}/${lines.length}] Inspecting: ${line.slice(0, 60)}...\n`);
    try {
      const data = await detect(line, apiKey, baseUrl, timeout);
      if (fmt === "json") {
        const result = data.result || {};
        results.push({
          input: line,
          request_id: data.request_id || "",
          is_safe: result.is_safe !== undefined ? result.is_safe : true,
          score: result.score !== undefined ? result.score : null,
          category: result.category || [],
          latency_ms: data.latency_ms || 0,
        });
      } else {
        console.log(`\n--- [${i + 1}] ${line.slice(0, 80)} ---`);
        printResult(data, fmt);
      }
    } catch (err) {
      console.error(`  Error: ${err.message}`);
      if (fmt === "json") {
        results.push({ input: line, error: err.message });
      }
    }
  }

  if (fmt === "json") {
    console.log(JSON.stringify(results, null, 2));
  }
}

main();
