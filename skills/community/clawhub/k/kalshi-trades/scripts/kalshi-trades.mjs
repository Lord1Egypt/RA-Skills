#!/usr/bin/env node

/**
 * Minimal Kalshi OpenAPI reader.
 * Read-only endpoints only.
 */

const BASE_URL = process.env.KALSHI_BASE_URL || "https://api.elections.kalshi.com/trade-api/v2";

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      out._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      out[key] = true;
    } else {
      out[key] = next;
      i += 1;
    }
  }
  return out;
}

function toInt(v, fallback) {
  if (v == null) return fallback;
  const n = Number(v);
  return Number.isFinite(n) ? Math.trunc(n) : fallback;
}

function buildQuery(params) {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v == null || v === "") continue;
    q.set(k, String(v));
  }
  const s = q.toString();
  return s ? `?${s}` : "";
}

async function request(path, query = {}) {
  const url = `${BASE_URL}${path}${buildQuery(query)}`;
  const res = await fetch(url, {
    method: "GET",
    headers: {
      accept: "application/json",
      "user-agent": "openclaw-skills-kalshi-openapi-reader/1.0",
    },
  });
  const text = await res.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    // keep raw fallback
  }

  if (!res.ok) {
    const err = new Error(`HTTP ${res.status} for ${url}`);
    err.status = res.status;
    err.url = url;
    err.body = json ?? text;
    throw err;
  }
  return { url, data: json ?? { raw: text } };
}

function printJson(obj, pretty = false) {
  process.stdout.write(`${JSON.stringify(obj, null, pretty ? 2 : 0)}\n`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];
  const pretty = Boolean(args.pretty);

  if (!cmd || cmd === "help" || cmd === "--help") {
    process.stdout.write(
      [
        "kalshi-trades.mjs",
        "",
        "Usage:",
        "  node kalshi-trades.mjs status [--pretty]",
        "  node kalshi-trades.mjs markets --limit 500 [--status open] [--series KXBTC] [--event <ticker>] [--cursor <c>] [--pretty]",
        "  node kalshi-trades.mjs market --ticker <market_ticker> [--pretty]",
        "  node kalshi-trades.mjs orderbook --ticker <market_ticker> [--depth 50] [--pretty]",
        "  node kalshi-trades.mjs trades [--ticker <market_ticker>] [--limit 100] [--cursor <c>] [--min_ts <unix>] [--max_ts <unix>] [--pretty]",
        "  node kalshi-trades.mjs events [--limit 100] [--status open] [--series <series_ticker>] [--cursor <c>] [--pretty]",
        "  node kalshi-trades.mjs event --event <event_ticker> [--pretty]",
        "  node kalshi-trades.mjs series [--limit 400] [--category Economics] [--cursor <c>] [--pretty]",
      ].join("\n"),
    );
    return;
  }

  try {
    if (cmd === "status") {
      const { url, data } = await request("/exchange/status");
      return printJson({ endpoint: url, data }, pretty);
    }

    if (cmd === "markets") {
      const query = {
        limit: toInt(args.limit, 100),
        status: args.status,
        series_ticker: args.series,
        event_ticker: args.event,
        cursor: args.cursor,
      };
      const { url, data } = await request("/markets", query);
      return printJson({ endpoint: url, data }, pretty);
    }

    if (cmd === "market") {
      const ticker = args.ticker;
      if (!ticker) throw new Error("--ticker is required");
      const { url, data } = await request(`/markets/${encodeURIComponent(ticker)}`);
      return printJson({ endpoint: url, data }, pretty);
    }

    if (cmd === "orderbook") {
      const ticker = args.ticker;
      if (!ticker) throw new Error("--ticker is required");
      const query = { depth: toInt(args.depth, 0) };
      const { url, data } = await request(`/markets/${encodeURIComponent(ticker)}/orderbook`, query);
      return printJson({ endpoint: url, data }, pretty);
    }

    if (cmd === "trades") {
      const query = {
        ticker: args.ticker,
        limit: toInt(args.limit, 100),
        cursor: args.cursor,
        min_ts: toInt(args.min_ts, null),
        max_ts: toInt(args.max_ts, null),
      };
      const { url, data } = await request("/markets/trades", query);
      return printJson({ endpoint: url, data }, pretty);
    }

    if (cmd === "events") {
      const query = {
        limit: toInt(args.limit, 100),
        status: args.status,
        series_ticker: args.series,
        cursor: args.cursor,
      };
      const { url, data } = await request("/events", query);
      return printJson({ endpoint: url, data }, pretty);
    }

    if (cmd === "event") {
      const eventTicker = args.event;
      if (!eventTicker) throw new Error("--event is required");
      const { url, data } = await request(`/events/${encodeURIComponent(eventTicker)}`);
      return printJson({ endpoint: url, data }, pretty);
    }

    if (cmd === "series") {
      const query = {
        limit: toInt(args.limit, 400),
        category: args.category,
        cursor: args.cursor,
      };
      const { url, data } = await request("/series", query);
      return printJson({ endpoint: url, data }, pretty);
    }

    throw new Error(`unknown command: ${cmd}`);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    printJson(
      {
        error: message,
        status: error?.status ?? null,
        url: error?.url ?? null,
        body: error?.body ?? null,
      },
      true,
    );
    process.exitCode = 1;
  }
}

main();
