#!/usr/bin/env node
// OpenClaw C1/C2 Usage Dashboard
// Usage: node server.mjs
// Opens at http://localhost:18800

import { createServer } from "http";
import { randomBytes } from "crypto";
import { execSync } from "child_process";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PORT = 18800;
const CSRF_TOKEN = randomBytes(32).toString("hex");
const CACHE_TTL_MS = 30_000;

let usageCache = null;
let cacheTimestamp = 0;
let inflightPromise = null;

const ACCOUNTS = {
  c1: { label: "C1", opItemId: "your-c1-item-id" },
  c2: { label: "C2", opItemId: "your-c2-item-id" },
};

function getTokenFrom1Password(itemId) {
  try {
    const raw = execSync(
      `op item get ${itemId} --reveal --format=json 2>/dev/null`,
      { encoding: "utf-8", timeout: 10000 }
    );
    const data = JSON.parse(raw);
    const field = data.fields?.find((f) => f.value?.startsWith("sk-ant"));
    return field?.value || null;
  } catch {
    return null;
  }
}

async function fetchUsage(token) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "anthropic-version": "2023-06-01",
      "anthropic-beta": "claude-code-20250219,oauth-2025-04-20",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1,
      messages: [{ role: "user", content: "." }],
    }),
  });

  if (!res.ok) {
    return { error: true, status: res.status };
  }

  const headers = {};
  for (const [k, v] of res.headers.entries()) {
    if (k.startsWith("anthropic-ratelimit")) headers[k] = v;
  }
  return { error: false, headers };
}

function parseUsage(headers) {
  const get = (key) => headers[`anthropic-ratelimit-unified-${key}`];
  const ts = (v) => (v ? new Date(Number(v) * 1000).toISOString() : null);
  return {
    status: get("status"),
    session: {
      utilization: parseFloat(get("5h-utilization") || "0"),
      resetAt: ts(get("5h-reset")),
      status: get("5h-status"),
    },
    weekly: {
      utilization: parseFloat(get("7d-utilization") || "0"),
      resetAt: ts(get("7d-reset")),
      status: get("7d-status"),
    },
    sonnet: {
      utilization: parseFloat(get("7d_sonnet-utilization") || "0"),
      resetAt: ts(get("7d_sonnet-reset")),
      status: get("7d_sonnet-status"),
    },
    overage: {
      utilization: parseFloat(get("overage-utilization") || "0"),
      status: get("overage-status"),
      disabledReason: get("overage-disabled-reason") || null,
    },
    fallbackPct: parseFloat(get("fallback-percentage") || "0"),
  };
}

const LOOPBACK_HOSTS = new Set([`localhost:${PORT}`, `127.0.0.1:${PORT}`]);

function isAllowedHost(host) {
  return typeof host === "string" && LOOPBACK_HOSTS.has(host.toLowerCase());
}

function isAllowedOrigin(origin) {
  if (!origin) return true;
  try {
    const u = new URL(origin);
    return (u.protocol === "http:" || u.protocol === "https:")
      && LOOPBACK_HOSTS.has(u.host.toLowerCase());
  } catch {
    return false;
  }
}

function verifyRequest(req) {
  if (!isAllowedHost(req.headers["host"])) return false;
  if (req.headers["x-dashboard-csrf"] !== CSRF_TOKEN) return false;
  return isAllowedOrigin(req.headers["origin"]);
}

async function getUsageData() {
  if (usageCache && Date.now() - cacheTimestamp < CACHE_TTL_MS) {
    return usageCache;
  }

  if (inflightPromise) return inflightPromise;

  inflightPromise = (async () => {
    const results = {};
    for (const [key, acc] of Object.entries(ACCOUNTS)) {
      const token = getTokenFrom1Password(acc.opItemId);
      if (!token) {
        results[key] = { error: "Token not found in 1Password", label: acc.label };
        continue;
      }
      const raw = await fetchUsage(token);
      if (raw.error) {
        results[key] = { error: `API error (status ${raw.status})`, label: acc.label };
      } else {
        results[key] = { ...parseUsage(raw.headers), label: acc.label };
      }
    }

    usageCache = results;
    cacheTimestamp = Date.now();
    return results;
  })().finally(() => { inflightPromise = null; });

  return inflightPromise;
}

const server = createServer(async (req, res) => {
  if (req.url === "/api/usage") {
    res.setHeader("Content-Type", "application/json");
    res.setHeader("Cache-Control", "no-store");

    if (req.method !== "POST") {
      res.statusCode = 405;
      res.end(JSON.stringify({ error: "Method not allowed" }));
      return;
    }
    if (!verifyRequest(req)) {
      res.statusCode = 403;
      res.end(JSON.stringify({ error: "Forbidden" }));
      return;
    }

    try {
      const data = await getUsageData();
      res.end(JSON.stringify(data));
    } catch (e) {
      res.statusCode = 500;
      res.end(JSON.stringify({ error: "Internal server error" }));
    }
    return;
  }

  if (req.url !== "/" && req.url !== "/index.html") {
    res.statusCode = 404;
    res.end("Not found");
    return;
  }
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  const html = readFileSync(join(__dirname, "index.html"), "utf-8")
    .replace("__CSRF_TOKEN__", CSRF_TOKEN);
  res.end(html);
});

server.headersTimeout = 10_000;
server.requestTimeout = 15_000;
server.keepAliveTimeout = 5_000;
server.maxRequestsPerSocket = 100;

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(`Port ${PORT} is already in use. Killing existing process...`);
    try {
      execSync(`lsof -ti:${PORT} | xargs kill 2>/dev/null`);
    } catch {}
    setTimeout(() => {
      server.listen(PORT, "127.0.0.1");
    }, 500);
  } else {
    console.error(err);
    process.exit(1);
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`Usage Dashboard: http://localhost:${PORT}`);
});
