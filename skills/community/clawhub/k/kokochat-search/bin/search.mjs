#!/usr/bin/env node
/**
 * kokochat-search
 *
 * Tiny local OpenClaw exec tool that calls KokoChat's hosted search proxy
 * (default: https://deeply.plus/deeply/search — server path is currently
 * Deeply-namespaced for legacy reasons but the wrapper itself is shared
 * across mini-apps). The Brave API key stays on KokoChat's server; user
 * OpenClaw installs only this wrapper.
 *
 * Input via argv[2] or stdin:
 *   { "query": "AI investor outlook 2026", "count": 5 }
 *
 * Output:
 *   { "ok": true, "provider": "brave", "query": "...",
 *     "results": [{ "title": "...", "url": "https://...", "snippet": "..." }] }
 */

import { argv, env, stdin } from "node:process";

const DEFAULT_BASE = "https://deeply.plus";
const DEFAULT_TIMEOUT_MS = 15_000;
const MAX_QUERY_CHARS = 500;

async function main() {
  let input;
  try {
    input = await readInput();
  } catch (error) {
    return fail(`could not parse input: ${describeError(error)}`);
  }

  const query = typeof input.query === "string" ? cleanText(input.query).slice(0, MAX_QUERY_CHARS) : "";
  const count = clampInt(input.count ?? input.limit, 1, 10, 5);
  if (query.length === 0) {
    return fail("query is required and must be a non-empty string");
  }

  const base = (
    env.KOKO_SEARCH_API_BASE ??
    env.KOKO_DEEPLY_SEARCH_BASE ?? // legacy alias
    DEFAULT_BASE
  ).replace(/\/+$/, "");
  const token = (env.KOKO_SEARCH_TOKEN ?? env.KOKO_DEEPLY_SEARCH_TOKEN ?? "").trim();
  const timeoutMs = clampInt(
    env.KOKO_SEARCH_TIMEOUT_MS ?? env.KOKO_DEEPLY_SEARCH_TIMEOUT_MS,
    1_000,
    60_000,
    DEFAULT_TIMEOUT_MS
  );

  try {
    const payload = await fetchSearch({
      endpoint: `${base}/deeply/search`,
      token,
      timeoutMs,
      query,
      count
    });
    if (payload?.ok !== true) {
      return fail(`koko search failed: ${payload?.error ?? "unknown_error"}`);
    }
    const results = Array.isArray(payload.results)
      ? payload.results.map(normalizeResult).filter((item) => item !== null)
      : [];
    process.stdout.write(
      `${JSON.stringify({
        ok: true,
        provider: typeof payload.provider === "string" ? payload.provider : "kokochat",
        query,
        requestedCount: count,
        count: results.length,
        results
      })}\n`
    );
  } catch (error) {
    return fail(`koko search request failed: ${describeError(error)}`);
  }
}

async function readInput() {
  if (argv[2] !== undefined && argv[2].trim().length > 0) {
    return JSON.parse(argv[2]);
  }
  const chunks = [];
  for await (const chunk of stdin) chunks.push(Buffer.from(chunk));
  const text = Buffer.concat(chunks).toString("utf8").trim();
  if (text.length === 0) return {};
  return JSON.parse(text);
}

async function fetchSearch({ endpoint, token, timeoutMs, query, count }) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const headers = {
      "Content-Type": "application/json",
      Accept: "application/json"
    };
    if (token.length > 0) headers.Authorization = `Bearer ${token}`;
    const response = await fetch(endpoint, {
      method: "POST",
      signal: controller.signal,
      headers,
      body: JSON.stringify({ query, count })
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      return {
        ok: false,
        error: payload?.error ?? `http_${response.status}`,
        message: payload?.message
      };
    }
    return payload;
  } finally {
    clearTimeout(timer);
  }
}

function normalizeResult(item) {
  if (item === null || typeof item !== "object") return null;
  const title = typeof item.title === "string" ? cleanText(item.title) : "";
  const url = typeof item.url === "string" ? item.url.trim() : "";
  const snippet = typeof item.snippet === "string" ? cleanText(item.snippet) : "";
  if (title.length === 0 || !/^https?:\/\//i.test(url)) return null;
  return { title, url, snippet };
}

function clampInt(value, min, max, fallback) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(min, Math.min(max, Math.trunc(n)));
}

function cleanText(value) {
  return value.replace(/\s+/g, " ").trim();
}

function fail(error) {
  process.stdout.write(`${JSON.stringify({ ok: false, error })}\n`);
  process.exitCode = 1;
}

function describeError(error) {
  return error instanceof Error ? error.message : String(error);
}

void main();
