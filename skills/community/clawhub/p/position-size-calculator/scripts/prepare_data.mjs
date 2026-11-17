#!/usr/bin/env node
//
// prepare_data.mjs: fetch everything the position size template needs, in one command.
//
//   SENTISENSE_API_KEY=... node scripts/prepare_data.mjs TSLA
//   SENTISENSE_API_KEY=... node scripts/prepare_data.mjs TSLA --out size_TSLA.html
//
// With no --out it emits one JSON object on stdout, shaped exactly for the template's data
// slot, and the caller binds it. With --out it does the binding too, writing the finished
// self-contained file in one step. Both paths produce the same artifact.
//
// No position is sized here. The sizing arithmetic, the refusal rules and the ladder all live
// in the template, written once and reviewed once, so two renders of the same snapshot cannot
// disagree about how many shares a risk budget buys. This script fetches and reshapes; the one
// number it computes is the average true range, and it is computed here rather than in the
// template only because it needs the daily bars, which are not worth inlining.
//
// Zero dependencies on purpose. Plain fetch, Node 18+, no install step, nothing to audit but
// this file.

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const API_ORIGIN = "https://app.sentisense.ai";
const KEY = process.env.SENTISENSE_API_KEY;

const SKILL_SLUG = "position-size-calculator";
const MAX_IDENTITY = 32;

/**
 * Reduce a volunteered name to a single safe token, matching the official CLI's rule so the
 * same agent identifies the same way whichever path it takes.
 *
 * Order matters. Whitespace collapses to hyphens BEFORE the strip, so "research desk" stays
 * "research-desk" instead of becoming "researchdesk"; the length cap is applied BEFORE the
 * edge trim, so a truncation that lands on a hyphen does not leave one dangling. The strip is
 * a positive allowlist, which is what stops anything user-supplied from reshaping the header:
 * a value carrying a newline, a quote, a semicolon or a parenthesis cannot close the comment
 * or start a second header line, because none of those characters survive.
 */
function sanitizeIdentity(value) {
  return String(value || "")
    .trim()
    .replace(/\s+/g, "-")
    .replace(/[^A-Za-z0-9._-]/g, "")
    .replace(/-{2,}/g, "-")
    .slice(0, MAX_IDENTITY)
    .replace(/^-+|-+$/g, "");
}

// The skill slug leads as a bare token, and a volunteered agent name follows it inside the
// same parenthesized comment, exactly as the CLI composes it. Both are optional to the server
// and nothing is inferred when the name is absent, so with no SENTISENSE_AGENT_NAME set the
// comment carries the slug alone rather than an empty agent token.
const AGENT_NAME = sanitizeIdentity(process.env.SENTISENSE_AGENT_NAME);
const UA = "node/prepare_data (" + SKILL_SLUG + (AGENT_NAME ? "; agent/" + AGENT_NAME : "") + ")";

function die(message, hint) {
  process.stderr.write(`prepare_data: ${message}\n`);
  if (hint) process.stderr.write(`  ${hint}\n`);
  process.exit(1);
}

export function sentisenseApiUrl(path) {
  const url = new URL(path, API_ORIGIN);
  if (url.protocol !== "https:" || url.hostname !== "app.sentisense.ai"
      || url.port !== "" || url.username !== "" || url.password !== ""
      || url.origin !== API_ORIGIN) {
    throw new Error("API URL must use https://app.sentisense.ai with no credentials or port");
  }
  return url;
}

async function get(path, {
  allowNullData = false, tolerate400 = false, tolerate404 = false, optional = false,
} = {}) {
  // A load-bearing call exits the process with a message. An optional context call THROWS
  // instead, so the caller's try/catch can soften the artifact rather than losing it: dying
  // inside a try block that exists to degrade gracefully would make the catch unreachable.
  // Auth failures always exit, optional or not, because a rejected key dooms every call and
  // the fix lives outside this script.
  const fail = (msg, hint) => {
    if (optional) throw new Error(hint ? `${msg} (${hint})` : msg);
    die(msg, hint);
  };
  let response;
  try {
    const url = sentisenseApiUrl(path);
    response = await fetch(url, {
      redirect: "error",
      headers: { "X-SentiSense-API-Key": KEY, Accept: "application/json", "User-Agent": UA },
    });
  } catch (cause) {
    fail(`network error calling ${path}`, String(cause && cause.message ? cause.message : cause));
  }

  if (response.status === 401 || response.status === 403) {
    die(
      "the API rejected the key",
      "Check SENTISENSE_API_KEY. A free key comes from https://app.sentisense.ai/get-api-key",
    );
  }
  if (response.status === 429) {
    const wait = response.headers.get("Retry-After");
    fail("rate limited", wait ? `Retry after ${wait}s.` : "Wait a minute and retry.");
  }
  // A 400 is sometimes routing advice rather than a failure: the quote endpoints are split by
  // instrument type and the stock one names the ETF path in its error. Hand the body back so the
  // caller can act on it instead of dying on a recoverable answer.
  if (response.status === 400 && tolerate400) {
    let err = {};
    try { err = await response.json(); } catch { /* not JSON, treat as opaque */ }
    return { data: null, isPreview: false, error: err };
  }
  // A 404 on a context call means "we do not cover this for that ticker", which softens the
  // artifact rather than failing it.
  if (response.status === 404 && tolerate404) {
    return { data: null, isPreview: false, notFound: true };
  }
  if (!response.ok) {
    fail(`${path} answered HTTP ${response.status}`);
  }

  const body = await response.json();
  // The preview envelope wraps some endpoints and not others. Unwrap when it is there, so the
  // rest of this script reads one shape.
  const enveloped = body && typeof body === "object" && !Array.isArray(body)
    && "isPreview" in body && "data" in body;
  const data = enveloped ? body.data : body;
  if (!allowNullData && (data === null || data === undefined)) {
    fail(`${path} returned no data`);
  }
  return { data, isPreview: enveloped ? body.isPreview === true : false };
}

function num(v) {
  return typeof v === "number" && isFinite(v) ? v : null;
}

/**
 * The New York calendar date of an epoch-millisecond stamp, as YYYY-MM-DD.
 *
 * Every timestamp this script converts is a US market one, and a session date is a New York
 * date: a stamp from late in the US evening already belongs to the next day in UTC, so slicing
 * an ISO string would label it with a session that has not traded. It is a label for the
 * reader, not an input to any arithmetic.
 */
function isoDate(ms) {
  const t = Number(ms);
  if (!isFinite(t) || t <= 0) return null;
  const d = new Date(t);
  if (isNaN(d.getTime())) return null;
  return d.toLocaleDateString("en-CA", { timeZone: "America/New_York" });
}

/**
 * Average true range over the most recent completed sessions.
 *
 * True range is the widest of today's own range and the two gaps against yesterday's close, so
 * it counts an overnight gap that a plain high-minus-low would miss. That is exactly what makes
 * it the right yardstick for a stop: a stop is reached by the gap as readily as by the drift.
 *
 * Two deliberate choices, both stated on the artifact's face:
 *   - The LAST bar is dropped. The chart endpoint serves the current session too, and a session
 *     still in progress has an incomplete range that would drag the average down. Dropping it
 *     costs at most one stale day and never reports a partial day as a full one.
 *   - The average is a plain mean of the true ranges, not Wilder's smoothing. Over a 14 session
 *     window the two are close, and a plain mean is a figure a reader can reproduce by hand from
 *     the same bars, which a recursively smoothed one is not.
 *
 * Returns null rather than a thin average when there are not enough bars to say anything.
 */
function averageTrueRange(bars, want = 14) {
  if (!Array.isArray(bars) || bars.length < 3) return null;
  const clean = bars
    .filter((b) => b && num(b.high) !== null && num(b.low) !== null && num(b.close) !== null)
    .sort((a, b) => Number(a.timestamp) - Number(b.timestamp));
  // Drop the session in progress. With only a handful of bars there is nothing to spare, so the
  // drop is skipped and the shorter window is reported instead of refusing outright.
  const usable = clean.length > 6 ? clean.slice(0, -1) : clean;
  if (usable.length < 6) return null;

  const trueRanges = [];
  for (let i = 1; i < usable.length; i++) {
    const prevClose = usable[i - 1].close;
    trueRanges.push(Math.max(
      usable[i].high - usable[i].low,
      Math.abs(usable[i].high - prevClose),
      Math.abs(usable[i].low - prevClose),
    ));
  }
  const window = trueRanges.slice(-want);
  if (!window.length) return null;
  const mean = window.reduce((a, b) => a + b, 0) / window.length;
  if (!(mean > 0)) return null;

  return {
    value: Math.round(mean * 10000) / 10000,
    sessions: window.length,
    asOf: isoDate(usable[usable.length - 1].timestamp),
  };
}

const DATA_TOKEN = "/*__SENTISENSE_" + "DATA__*/";
const META_TOKEN = "/*__SENTISENSE_" + "META__*/";

/**
 * Bind a snapshot into the shipped template and return the finished document.
 *
 * The JSON lands inside a <script type="application/json"> block, where the parser ends the
 * block at the first literal `</script`, so `<` is escaped to its JSON unicode form. Nothing in
 * a market-data snapshot carries one today, and relying on that is exactly the assumption that
 * stops being true once a field starts carrying free text.
 */
function bind(template, payload, meta) {
  const json = (v) => JSON.stringify(v, null, 2).replace(/</g, "\\u003c");
  for (const [token, value] of [[DATA_TOKEN, payload], [META_TOKEN, meta]]) {
    const first = template.indexOf(token);
    if (first === -1 || template.indexOf(token, first + 1) !== -1) {
      die(
        `the template does not hold exactly one ${token} slot`,
        "Use the shipped scripts/template.html unmodified.",
      );
    }
    template = template.replace(token, json(value));
  }
  return template;
}

async function main() {
  const args = process.argv.slice(2);
  const outIndex = args.indexOf("--out");
  const outPath = outIndex === -1 ? null : args[outIndex + 1];
  if (outIndex !== -1 && !outPath) {
    die("--out needs a file path", "Usage: node scripts/prepare_data.mjs TSLA --out size.html");
  }
  // Drop the flag and its value before reading the ticker, but only when the flag is actually
  // present: with outIndex at -1, `outIndex + 1` is 0 and a naive filter would discard the
  // ticker itself on every run that does not pass --out.
  const rest = outIndex === -1 ? args : args.filter((a, i) => i !== outIndex && i !== outIndex + 1);
  const ticker = (rest[0] || "").trim().toUpperCase();
  if (!ticker) {
    die("no ticker given", "Usage: node scripts/prepare_data.mjs TSLA [--out size.html]");
  }
  if (!/^[A-Z][A-Z0-9.\-]{0,9}$/.test(ticker)) {
    die(`"${ticker}" does not look like a ticker`, "Use a symbol such as TSLA, SPY or BRK.B");
  }
  if (!KEY) {
    die(
      "SENTISENSE_API_KEY is not set",
      "Get a free key at https://app.sentisense.ai/get-api-key, then export SENTISENSE_API_KEY",
    );
  }
  const enc = encodeURIComponent(ticker);

  // The quote is the only load-bearing call: with no last price there is no entry to pre-fill
  // and the artifact has nothing to open on. Everything after it is context that softens the
  // page rather than failing it.
  //
  // Quotes are split by instrument type. The stock endpoint answers 400 `ticker_is_etf` for a
  // fund and names the ETF path in the message, so an ETF is one redirect away rather than a
  // failure: both return the same `currentPrice`.
  let quote = await get(`/api/v1/stocks/${enc}/quote`, { tolerate400: true });
  if (!quote.data) {
    if (quote.error && quote.error.error === "ticker_is_etf") {
      quote = await get(`/api/v1/etfs/${enc}/quote`);
    } else {
      die(
        `${ticker} has no quote`,
        quote.error && quote.error.message ? String(quote.error.message) : undefined,
      );
    }
  }
  const price = num(quote.data.currentPrice);
  if (!(price > 0)) {
    die(`${ticker} has no usable current price`);
  }

  // Daily bars, for the average true range the artifact reads a stop distance against. This
  // endpoint takes the ticker as a query parameter and is NOT split by instrument type, so one
  // call covers stocks and funds alike.
  //
  // 3M is chosen deliberately: `1M` and shorter return INTRADAY bars, whose ranges are a
  // fraction of a session's and would understate the daily range several fold. A 3M window is
  // about 63 daily bars, comfortably more than the 15 an average true range needs.
  let atr = null;
  try {
    const bars = (await get(`/api/v1/stocks/chart?ticker=${enc}&timeframe=3M`, {
      allowNullData: true,
      tolerate404: true,
      optional: true,
    })).data;
    atr = Array.isArray(bars) ? averageTrueRange(bars) : null;
  } catch {
    atr = null;
  }

  // The Score. Free on every tier and never truncated to a preview, but legitimately absent in
  // two ways: `sentisenseScore` is null until the day's first analytics run lands, and the
  // endpoint answers 404 for a ticker with no sentiment coverage at all. Both soften the page.
  let score = null;
  let scoreNote = null;
  try {
    const sent = await get(`/api/v1/stocks/${enc}/sentiment`, {
      allowNullData: true,
      tolerate404: true,
      optional: true,
    });
    const d = sent.data;
    if (!d) {
      scoreNote = `No SentiSense Score is published for ${ticker}, so the artifact carries no ` +
        "sentiment context. Nothing in the sizing arithmetic depends on it.";
    } else {
      // A measured zero is a real reading and is served as `0.0`, so it is passed through as a
      // number. Coercing it to null here would report a genuinely neutral stock as uncovered.
      score = {
        value: num(d.sentisenseScore),
        avg30d: num(d.sentisenseScoreAvg30d),
        label: typeof d.scoreLabel === "string" ? d.scoreLabel : null,
        direction: typeof d.direction === "string" ? d.direction : null,
        asOf: typeof d.asOf === "string" ? d.asOf : null,
      };
      if (score.value === null && score.avg30d === null) {
        score = null;
        scoreNote = `The SentiSense Score for ${ticker} has no reading yet today and no 30 day ` +
          "average to stand in for it, so the artifact carries no sentiment context.";
      }
    }
  } catch {
    score = null;
  }

  const payload = {
    ticker,
    generatedAt: new Date().toISOString(),
    price,
    // The quote's `timestamp` field is when the response was served, not when the price is
    // from, so it is deliberately not a fallback here: without a price stamp the artifact says
    // "delayed, not live" rather than dressing the clock up as a session date.
    priceAsOf: isoDate(quote.data.priceAsOf),
    previousClose: num(quote.data.previousClose),
    week52High: num(quote.data.week52High),
    week52Low: num(quote.data.week52Low),
    // The average true range in dollars per share, over completed sessions only. This is the
    // yardstick the artifact reads a stop distance against, and it is a measured figure from
    // past bars rather than anything implied or forecast.
    atr: atr ? atr.value : null,
    atrSessions: atr ? atr.sessions : null,
    atrAsOf: atr ? atr.asOf : null,
    score,
    scoreNote,
    isPreview: false,
  };

  if (!outPath) {
    process.stdout.write(JSON.stringify(payload, null, 2) + "\n");
    return;
  }

  const templatePath = resolve(dirname(fileURLToPath(import.meta.url)), "template.html");
  let template;
  try {
    template = readFileSync(templatePath, "utf8");
  } catch {
    die(`could not read the template at ${templatePath}`, "It ships beside this script.");
  }
  const meta = {
    title: `Position size: ${ticker}`,
    subtitle:
      "Share count, position value and dollar risk, worked out from the account size and the " +
      "risk you set. Pre-filled with the last price so nothing starts empty.",
  };
  try {
    writeFileSync(outPath, bind(template, payload, meta));
  } catch (cause) {
    die(`could not write ${outPath}`, String(cause && cause.message ? cause.message : cause));
  }
  process.stdout.write(outPath + "\n");
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
