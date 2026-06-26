#!/usr/bin/env node
/**
 * KeyAPI MCP Tool Runner
 *
 * Calls any KeyAPI MCP tool with built-in caching, auto-pagination,
 * and automatic cover-image URL conversion.
 *
 * Usage:
 *   node scripts/run.js --tool <tool_name> [options]
 *   node scripts/run.js --list-tools
 *   node scripts/run.js --schema <tool_name>
 *
 * Options:
 *   --tool <name>       MCP tool name to call  (required for tool calls)
 *   --platform <name>   Platform to target  (default: tiktok)
 *   --params <json>     Tool parameters as JSON string  (default: {})
 *   --page-num <n>      Page number for paginated endpoints  (default: 1)
 *   --page-size <n>     Items per page — max 10  (default: 10)
 *   --all-pages         Auto-fetch ALL pages and merge list results
 *   --no-cache          Skip cache lookup, force a fresh API call
 *   --no-images         Skip automatic cover-image URL conversion
 *   --cache-dir <path>  Cache directory  (default: .keyapi-cache)
 *   --output <path>     Also save result to this file path
 *   --pretty            Pretty-print JSON output to stdout
 *   --list-tools        List all available tools on the MCP server
 *   --schema <name>     Show the input schema for a specific tool
 *   --help              Show this help
 *
 * Environment variables:
 *   KEYAPI_TOKEN        Required. Get yours at https://keyapi.ai/
 *   KEYAPI_SERVER_URL   Optional MCP base URL override  (default: https://mcp.keyapi.ai)
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { createHash } from "crypto";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { join, resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { parseArgs } from "util";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

// ── .env loader ───────────────────────────────────────────────────────────────

(function loadDotenv() {
  const envPath = join(ROOT, ".env");
  if (!existsSync(envPath)) return;
  for (const line of readFileSync(envPath, "utf8").split("\n")) {
    const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$/);
    if (m && !process.env[m[1]])
      process.env[m[1]] = m[2].replace(/^["']|["']$/g, "").trim();
  }
})();

// ── Config ────────────────────────────────────────────────────────────────────

const SERVER_BASE = process.env.KEYAPI_SERVER_URL ?? "https://mcp.keyapi.ai";
const PAGE_SIZE_MAX = 10;

/**
 * Platforms that require cover-image URL conversion.
 * Only TikTok serves images via the echosell CDN host that needs proxying.
 * Other platforms serve images directly — no conversion needed.
 */
const COVER_IMAGE_HOSTS = {
  tiktok: ["echosell-images.tos-ap-southeast-1.volces.com"],
};

function getCoverImageHosts(platform) {
  return COVER_IMAGE_HOSTS[platform] ?? [];
}

// ── Help text ─────────────────────────────────────────────────────────────────

const HELP = `KeyAPI MCP Tool Runner
======================

Calls KeyAPI MCP tools with caching, auto-pagination, and cover-image conversion.

Usage:
  node scripts/run.js --tool <tool_name> [options]
  node scripts/run.js --list-tools
  node scripts/run.js --schema <tool_name>

Options:
  --tool <name>       MCP tool name to call  (required for tool calls)
  --platform <name>   Platform to target  (default: tiktok)
  --params <json>     Tool parameters as JSON string  (default: {})
  --page-num <n>      Page number for paginated endpoints  (default: 1)
  --page-size <n>     Items per page — max 10  (default: 10)
  --all-pages         Auto-fetch ALL pages and merge list results
  --no-cache          Skip cache lookup, force a fresh API call
  --no-images         Skip automatic cover-image URL conversion
  --cache-dir <path>  Cache directory  (default: .keyapi-cache)
  --output <path>     Also save result to this file path
  --pretty            Pretty-print JSON output to stdout
  --list-tools        List all available tools on the MCP server
  --schema <name>     Show the input schema for a specific tool
  --help              Show this help

Environment:
  KEYAPI_TOKEN        Required. Get yours at https://keyapi.ai/
                      Set via: export KEYAPI_TOKEN=your_token
                      Or save to a .env file in the skill directory.
  KEYAPI_SERVER_URL   Optional MCP base URL override
                      (default: https://mcp.keyapi.ai)

Examples:
  # List all tools on a platform
  node scripts/run.js --list-tools
  node scripts/run.js --platform youtube --list-tools

  # Inspect a tool's input schema
  node scripts/run.js --schema search_influencers

  # Call a tool (platform defaults to tiktok)
  node scripts/run.js --tool search_influencers \\
    --params '{"keyword":"fitness","region":"US"}' --pretty

  # Explicit platform
  node scripts/run.js --platform tiktok --tool get_influencer_detail \\
    --params '{"unique_id":"charlidamelio"}' --pretty

  # Another platform
  node scripts/run.js --platform youtube --tool search_channels \\
    --params '{"keyword":"fitness"}' --pretty
`;

// ── File / cache utilities ────────────────────────────────────────────────────

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function readJSON(path) {
  try {
    if (existsSync(path)) return JSON.parse(readFileSync(path, "utf8"));
  } catch { /* ignore */ }
  return null;
}

function writeJSON(path, data) {
  ensureDir(dirname(path));
  writeFileSync(path, JSON.stringify(data, null, 2), "utf8");
}

/** Deterministic cache path: .keyapi-cache/YYYY-MM-DD/<tool>/<hash>.json */
function cacheKey(tool, params, cacheDir) {
  const hash = createHash("md5")
    .update(JSON.stringify(params, Object.keys(params).sort()))
    .digest("hex")
    .slice(0, 16);
  const date = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  return join(cacheDir, date, tool, `${hash}.json`);
}

// ── Cover-image helpers ───────────────────────────────────────────────────────

function collectImageUrls(obj, hosts, acc = []) {
  if (!obj || typeof obj !== "object") return acc;
  if (Array.isArray(obj)) {
    for (const item of obj) collectImageUrls(item, hosts, acc);
  } else {
    for (const v of Object.values(obj)) {
      if (typeof v === "string" && hosts.some(h => v.includes(h))) acc.push(v);
      else collectImageUrls(v, hosts, acc);
    }
  }
  return acc;
}

function replaceImageUrls(obj, map) {
  if (!obj || typeof obj !== "object") return obj;
  if (Array.isArray(obj)) return obj.map(i => replaceImageUrls(i, map));
  return Object.fromEntries(
    Object.entries(obj).map(([k, v]) =>
      typeof v === "string" && map.has(v) ? [k, map.get(v)] : [k, replaceImageUrls(v, map)]
    )
  );
}

/** Split array into chunks of n */
function chunk(arr, n) {
  const out = [];
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
  return out;
}

// ── Heuristic list extractor for --all-pages ─────────────────────────────────

const LIST_KEYS = [
  "list", "items", "results", "videos", "products", "creators",
  "shops", "influencers", "hashtags", "music", "ads", "data",
  "channels", "posts", "comments", "reviews", "users",
];

function extractList(data) {
  const d = data?.data ?? data;
  for (const k of LIST_KEYS) {
    if (Array.isArray(d?.[k])) return d[k];
  }
  return Array.isArray(d) ? d : [];
}

// ── Schema cache & pagination detection ──────────────────────────────────────

/** Session-level tool schema cache — loaded once per process. */
let _toolSchemas = null;

async function getToolSchemas(client) {
  if (!_toolSchemas) {
    const { tools } = await client.listTools();
    _toolSchemas = new Map(tools.map(t => [t.name, t]));
  }
  return _toolSchemas;
}

/**
 * Inspect a tool's input schema to determine its pagination style.
 *
 * Returns:
 *   "analytics"  → tool accepts page_num / page_size
 *   "trending"   → tool accepts page / limit
 *   null         → tool has no recognised pagination fields
 */
async function detectPagination(client, toolName) {
  const schemas = await getToolSchemas(client);
  const tool = schemas.get(toolName);
  if (!tool?.inputSchema?.properties) return null;
  const props = tool.inputSchema.properties;
  if ("page_num" in props && "page_size" in props) return "analytics";
  if ("page" in props && "limit" in props) return "trending";
  return null;
}

// ── MCP client ────────────────────────────────────────────────────────────────

/** Prompt for KEYAPI_TOKEN interactively and persist it to .env */
async function promptToken() {
  if (!process.stdin.isTTY) {
    throw new Error(
      "KEYAPI_TOKEN is not set.\n" +
      "  → Register at https://keyapi.ai/ to obtain a free token, then either:\n" +
      "    export KEYAPI_TOKEN=your_token_here\n" +
      "  → Or create a .env file in the skill directory:\n" +
      "    echo \"KEYAPI_TOKEN=your_token_here\" > .env"
    );
  }
  const { createInterface } = await import("readline");
  const rl = createInterface({ input: process.stdin, output: process.stderr });
  return new Promise((resolve, reject) => {
    process.stderr.write("\nKEYAPI_TOKEN is required. Get yours at https://keyapi.ai/\n\n");
    rl.question("Enter your token: ", (answer) => {
      rl.close();
      const token = answer.trim();
      if (!token) {
        reject(new Error("No token entered. Set KEYAPI_TOKEN and try again."));
        return;
      }
      const envPath = join(ROOT, ".env");
      writeFileSync(envPath, `KEYAPI_TOKEN=${token}\n`, "utf8");
      log(`[token] Saved to ${envPath} — future runs will load it automatically`);
      process.env.KEYAPI_TOKEN = token;
      resolve(token);
    });
  });
}

async function connect(serverUrl) {
  let token = process.env.KEYAPI_TOKEN;
  if (!token) token = await promptToken();

  const client = new Client({ name: "keyapi-runner", version: "1.0.0" });
  const transport = new StreamableHTTPClientTransport(
    new URL(serverUrl),
    { requestInit: { headers: { Authorization: `Bearer ${token}` } } }
  );
  await client.connect(transport);
  return client;
}

/** Call a tool, parse the text/JSON response, retry once on code=500 */
async function callTool(client, tool, args) {
  for (let attempt = 0; attempt <= 1; attempt++) {
    const raw = await client.callTool({ name: tool, arguments: args });
    const textBlock = raw?.content?.find(c => c.type === "text");
    let data;
    try { data = textBlock ? JSON.parse(textBlock.text) : raw; }
    catch { data = { raw: textBlock?.text ?? raw }; }

    if (data?.code === 500 && attempt === 0) {
      log(`[retry] ${tool} returned code=500, retrying in 2s…`);
      await sleep(2000);
      continue;
    }
    return data;
  }
}

/**
 * Batch-convert platform cover image URLs.
 * Hosts are resolved from PLATFORM_CONFIG; skipped entirely if the platform
 * has no configured image hosts.
 * API accepts max 10 URLs per call as a comma-separated string (cover_urls).
 */
async function convertImages(client, data, platform) {
  const hosts = getCoverImageHosts(platform);
  if (hosts.length === 0) return data;

  const urls = [...new Set(collectImageUrls(data, hosts))];
  if (urls.length === 0) return data;

  const urlMap = new Map();

  for (const batch of chunk(urls, 10)) {
    try {
      const result = await callTool(client, "batch_download_cover_images", {
        cover_urls: batch.join(","),
      });
      if (result?.code === 0 && result?.data) {
        if (Array.isArray(result.data)) {
          for (const { original_url, converted_url } of result.data) {
            if (original_url && converted_url) urlMap.set(original_url, converted_url);
          }
        } else if (typeof result.data === "object") {
          for (const [k, v] of Object.entries(result.data)) urlMap.set(k, v);
        }
      }
    } catch (e) {
      log(`[images] Warning: batch conversion failed — ${e.message}`);
    }
  }

  if (urlMap.size > 0) {
    log(`[images] Converted ${urlMap.size} cover image URL(s)`);
    return replaceImageUrls(data, urlMap);
  }
  return data;
}

// ── Commands ──────────────────────────────────────────────────────────────────

async function cmdListTools(client) {
  const { tools } = await client.listTools();
  const out = tools.map(t => ({
    name: t.name,
    description: (t.description ?? "").slice(0, 100),
  }));
  emit(out, null, true);
}

async function cmdSchema(client, toolName) {
  const schemas = await getToolSchemas(client);
  const tool = schemas.get(toolName);
  if (!tool) {
    throw new Error(
      `Tool "${toolName}" not found on the server.\n` +
      "  Run --list-tools to see all available tools."
    );
  }
  emit(tool, null, true);
}

async function cmdRun(client, opts) {
  const { tool, platform, params, pageNum, pageSize, allPages, noCache, noImages, cacheDir, output, pretty } = opts;

  // Clamp page_size to max allowed by the API
  const safePageSize = Math.min(pageSize, PAGE_SIZE_MAX);

  // ── Single page ────────────────────────────────────────────────────────────
  if (!allPages) {
    const finalParams = { ...params };

    const paginationType = await detectPagination(client, tool);
    if (paginationType === "analytics") {
      if (!("page_num"  in finalParams)) finalParams.page_num  = pageNum;
      if (!("page_size" in finalParams)) finalParams.page_size = safePageSize;
    } else if (paginationType === "trending") {
      if (!("page"  in finalParams)) finalParams.page  = pageNum;
      if (!("limit" in finalParams)) finalParams.limit = safePageSize;
    }

    const cachePath = cacheKey(tool, finalParams, cacheDir);
    if (!noCache) {
      const cached = readJSON(cachePath);
      if (cached) {
        log(`[cache] Loaded from ${cachePath}`);
        emit(cached, output, pretty);
        return;
      }
    }

    let data = await callTool(client, tool, finalParams);
    assertSuccess(data, tool);
    if (!noImages) data = await convertImages(client, data, platform);
    writeJSON(cachePath, data);
    emit(data, output, pretty);
    return;
  }

  // ── All pages ──────────────────────────────────────────────────────────────
  const paginationType = await detectPagination(client, tool);
  const isTrending = paginationType === "trending";
  let page = 1;
  let allItems = [];
  let lastData = null;

  while (true) {
    const pageParams = isTrending
      ? { ...params, page: page, limit: safePageSize }
      : { ...params, page_num: page, page_size: safePageSize };

    const cachePath = cacheKey(tool, pageParams, cacheDir);

    let data = noCache ? null : readJSON(cachePath);
    if (data) {
      log(`[cache] Page ${page} loaded from ${cachePath}`);
    } else {
      data = await callTool(client, tool, pageParams);
      if (data?.code !== undefined && data.code !== 0) {
        log(`[warn] API error on page ${page}: code=${data.code} — ${data.message ?? ""}`);
        break;
      }
      if (!noImages) data = await convertImages(client, data, platform);
      writeJSON(cachePath, data);
    }

    const items = extractList(data);
    if (items.length === 0) break;

    allItems = allItems.concat(items);
    lastData = data;
    log(`[page ${page}] ${items.length} items  (total so far: ${allItems.length})`);

    const hasMore = data?.data?.has_more ?? data?.has_more;
    if (hasMore === false || items.length < safePageSize) break;
    page++;
  }

  const merged = {
    ...lastData,
    _merged: { total_pages: page, total_items: allItems.length },
    items: allItems,
  };
  writeJSON(cacheKey(tool, { ...params, _all_pages: true }, cacheDir), merged);
  emit(merged, output, pretty);
}

// ── Output / logging ──────────────────────────────────────────────────────────

function emit(data, filePath, pretty) {
  console.log(pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data));
  if (filePath) {
    const abs = resolve(filePath);
    ensureDir(dirname(abs));
    writeFileSync(abs, JSON.stringify(data, null, 2), "utf8");
    log(`[output] Saved to ${abs}`);
  }
}

function log(msg) { process.stderr.write(msg + "\n"); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function assertSuccess(data, tool) {
  if (data?.code !== undefined && data.code !== 0) {
    throw new Error(`API error from "${tool}": code=${data.code} — ${data.message ?? "(no message)"}`);
  }
}

// ── Entry point ───────────────────────────────────────────────────────────────

async function main() {
  const { values } = parseArgs({
    options: {
      tool:          { type: "string"  },
      platform:      { type: "string",  default: "tiktok" },
      schema:        { type: "string"  },
      params:        { type: "string",  default: "{}" },
      "page-num":    { type: "string",  default: "1"  },
      "page-size":   { type: "string",  default: "10" },
      "all-pages":   { type: "boolean", default: false },
      "no-cache":    { type: "boolean", default: false },
      "no-images":   { type: "boolean", default: false },
      "cache-dir":   { type: "string"  },
      output:        { type: "string"  },
      pretty:        { type: "boolean", default: false },
      "list-tools":  { type: "boolean", default: false },
      help:          { type: "boolean", default: false },
    },
    strict: false,
  });

  const needsHelp = values.help || (!values.tool && !values["list-tools"] && !values.schema);
  if (needsHelp) {
    process.stdout.write(HELP);
    process.exit(0);
  }

  let params;
  try { params = JSON.parse(values.params); }
  catch { throw new Error(`--params is not valid JSON: ${values.params}`); }

  const cacheDir = values["cache-dir"]
    ? resolve(values["cache-dir"])
    : join(ROOT, ".keyapi-cache");

  const serverUrl = `${SERVER_BASE}/${values.platform}/mcp`;
  const client = await connect(serverUrl);

  try {
    if (values["list-tools"]) {
      await cmdListTools(client);
    } else if (values.schema) {
      await cmdSchema(client, values.schema);
    } else {
      await cmdRun(client, {
        tool:     values.tool,
        platform: values.platform,
        params,
        pageNum:  parseInt(values["page-num"],  10),
        pageSize: parseInt(values["page-size"], 10),
        allPages: values["all-pages"],
        noCache:  values["no-cache"],
        noImages: values["no-images"],
        cacheDir,
        output:   values.output,
        pretty:   values.pretty,
      });
    }
  } finally {
    await client.close().catch(() => {});
  }
}

main().catch(err => {
  process.stderr.write(`Error: ${err.message ?? String(err)}\n`);
  process.exit(1);
});
