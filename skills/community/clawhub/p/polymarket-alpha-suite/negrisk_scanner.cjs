#!/usr/bin/env node
/**
 * NegRisk Rebalancing Scanner — risk-free arbitrage on Polymarket multi-outcome events.
 *
 * If the sum of best-ask prices across ALL outcomes of an event < $1.00,
 * buying one share of every outcome guarantees $1.00 on resolution.
 *
 * Usage:
 *   node negrisk_scanner.cjs scan
 *   node negrisk_scanner.cjs watch
 *   node negrisk_scanner.cjs detail <event-slug>
 */

const GAMMA_BASE = "https://gamma-api.polymarket.com";
const CLOB_BASE = "https://clob.polymarket.com";
const EDGE_THRESHOLD = 0.98; // sum must be < this to flag
const POLL_INTERVAL = 60_000;

// ── Helpers ──────────────────────────────────────────────────────────────────

async function fetchJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r.json();
}

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Fetch order book and return best ask price + liquidity at that level
async function bestAsk(tokenId) {
  try {
    const book = await fetchJSON(`${CLOB_BASE}/book?token_id=${tokenId}`);
    const asks = (book.asks || []).sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
    if (!asks.length) return null;
    const price = parseFloat(asks[0].price);
    const size = parseFloat(asks[0].size);
    // sum liquidity at levels within 2c of best
    let liq = 0;
    for (const a of asks) {
      if (parseFloat(a.price) <= price + 0.02) liq += parseFloat(a.size);
      else break;
    }
    return { price, size, liq };
  } catch {
    return null;
  }
}

// ── Fetch events with multiple outcomes ──────────────────────────────────────

async function fetchEvents(limit = 100, offset = 0) {
  const url = `${GAMMA_BASE}/events?closed=false&active=true&limit=${limit}&offset=${offset}`;
  return fetchJSON(url);
}

// ── Analyze a single event ───────────────────────────────────────────────────

async function analyzeEvent(event, useBooks = true) {
  const markets = event.markets || [];
  if (markets.length < 3) return null; // need 3+ outcomes to be interesting

  // Each market in a multi-outcome event represents one outcome.
  // The YES token of each market is what we'd buy.
  const outcomes = [];
  for (const m of markets) {
    const tokens = JSON.parse(m.clobTokenIds || "[]");
    const prices = JSON.parse(m.outcomePrices || "[]");
    if (!tokens.length) continue;

    const yesToken = tokens[0]; // first token is YES
    const midPrice = parseFloat(prices[0] || "0");

    let askData = null;
    if (useBooks) {
      askData = await bestAsk(yesToken);
      // Small rate-limit courtesy (only between sequential calls within one event)
      await sleep(20);
    }

    outcomes.push({
      question: m.question || m.groupItemTitle || "?",
      token: yesToken,
      midPrice,
      askPrice: askData ? askData.price : midPrice,
      askSize: askData ? askData.size : 0,
      askLiq: askData ? askData.liq : 0,
      hasBook: !!askData,
    });
  }

  if (outcomes.length < 3) return null;

  const sumAsk = outcomes.reduce((s, o) => s + o.askPrice, 0);
  const sumMid = outcomes.reduce((s, o) => s + o.midPrice, 0);
  const minLiq = outcomes.reduce((m, o) => Math.min(m, o.askLiq), Infinity);
  const profitPct = ((1 - sumAsk) / sumAsk) * 100;

  return {
    title: event.title || event.slug,
    slug: event.slug,
    numOutcomes: outcomes.length,
    sumAsk: Math.round(sumAsk * 10000) / 10000,
    sumMid: Math.round(sumMid * 10000) / 10000,
    profitPct: Math.round(profitPct * 100) / 100,
    minLiq: Math.round(minLiq),
    outcomes,
  };
}

// ── Commands ─────────────────────────────────────────────────────────────────

async function scan({ verbose = false } = {}) {
  console.log("🔍 Fetching active events from Gamma API...\n");

  let allEvents = [];
  for (let offset = 0; ; offset += 100) {
    const batch = await fetchEvents(100, offset);
    if (!batch.length) break;
    allEvents = allEvents.concat(batch);
    if (batch.length < 100) break;
    process.stdout.write(`  fetched ${allEvents.length} events...\r`);
  }

  // Filter to multi-outcome only
  const multi = allEvents.filter(e => (e.markets || []).length >= 3);
  console.log(`Found ${allEvents.length} events, ${multi.length} with 3+ outcomes.\n`);

  // PHASE 1: Fast pre-filter using mid prices (no API calls)
  console.log("Phase 1: Pre-filtering by mid prices...");
  const candidates = [];
  for (const ev of multi) {
    const r = await analyzeEvent(ev, false); // no book checks
    if (r && r.sumMid < 0.995) candidates.push(ev); // tight filter — asks are usually ≥ mid
  }
  console.log(`${candidates.length} candidates with mid-price sum < $0.995.\n`);

  // PHASE 2: Check order books only for candidates (5 concurrent)
  console.log(`Phase 2: Checking order books for ${candidates.length} events...\n`);
  const results = [];
  const CONCURRENCY = 10;
  for (let i = 0; i < candidates.length; i += CONCURRENCY) {
    const batch = candidates.slice(i, i + CONCURRENCY);
    process.stdout.write(`  [${i+1}-${Math.min(i+CONCURRENCY, candidates.length)}/${candidates.length}] checking books...\r`);
    const batchResults = await Promise.all(batch.map(ev => analyzeEvent(ev, true)));
    for (const r of batchResults) {
      if (r && r.sumAsk < 1.0) results.push(r);
    }
  }
  console.log();

  results.sort((a, b) => b.profitPct - a.profitPct);

  const opps = results.filter(r => r.sumAsk < EDGE_THRESHOLD);

  if (!results.length) {
    console.log("No multi-outcome events with sum < $1.00 found.");
    return results;
  }

  console.log("═══════════════════════════════════════════════════════════════");
  console.log(" NegRisk Arbitrage Opportunities (sum of asks < $1.00)");
  console.log("═══════════════════════════════════════════════════════════════\n");

  for (const r of results) {
    const flag = r.sumAsk < EDGE_THRESHOLD ? "🟢" : "⚪";
    console.log(`${flag} ${r.title}`);
    console.log(`   Outcomes: ${r.numOutcomes} | Sum(ask): $${r.sumAsk.toFixed(4)} | Sum(mid): $${r.sumMid.toFixed(4)}`);
    console.log(`   Profit: ${r.profitPct.toFixed(2)}% | Min liq: ${r.minLiq} shares | Slug: ${r.slug}`);
    console.log();
  }

  console.log(`\n${opps.length} opportunities with ≥2% edge (sum < $${EDGE_THRESHOLD}).`);
  console.log(`${results.length} total with any positive edge.\n`);
  return results;
}

async function watch() {
  console.log("👁️  NegRisk Watch Mode — polling every 60s. Ctrl+C to stop.\n");
  while (true) {
    const ts = new Date().toLocaleTimeString();
    console.log(`\n── Scan at ${ts} ──────────────────────────────────`);
    await scan();
    await sleep(POLL_INTERVAL);
  }
}

async function detail(slug) {
  console.log(`🔎 Fetching event: ${slug}\n`);
  const events = await fetchJSON(`${GAMMA_BASE}/events?slug=${slug}`);
  if (!events.length) {
    console.log("Event not found. Try the URL slug from polymarket.com/event/<slug>");
    return;
  }
  const ev = events[0];
  const r = await analyzeEvent(ev, true);
  if (!r) {
    console.log("Not a multi-outcome event or no book data.");
    return;
  }

  console.log(`Event: ${r.title}`);
  console.log(`Outcomes: ${r.numOutcomes} | Sum(ask): $${r.sumAsk.toFixed(4)} | Profit: ${r.profitPct.toFixed(2)}%\n`);
  console.log("Outcome Breakdown:");
  console.log("─".repeat(80));

  for (const o of r.outcomes) {
    const bookTag = o.hasBook ? "📗" : "📕";
    console.log(`  ${bookTag} ${o.question}`);
    console.log(`     Mid: $${o.midPrice.toFixed(4)} | Ask: $${o.askPrice.toFixed(4)} | Liq: ${Math.round(o.askLiq)} shares`);
    console.log(`     Token: ${o.token.slice(0, 20)}...`);
  }

  console.log("\n─".repeat(80));
  console.log(`Total cost (1 share each): $${r.sumAsk.toFixed(4)}`);
  console.log(`Guaranteed payout:         $1.0000`);
  console.log(`Profit per set:            $${(1 - r.sumAsk).toFixed(4)} (${r.profitPct.toFixed(2)}%)`);
  console.log(`Max sets at min liq:       ${r.minLiq}`);
  console.log(`Max profit at min liq:     $${(r.minLiq * (1 - r.sumAsk)).toFixed(2)}`);
}

// ── Main ─────────────────────────────────────────────────────────────────────

const [cmd, ...args] = process.argv.slice(2);

switch (cmd) {
  case "scan":
    scan().catch(console.error);
    break;
  case "watch":
    watch().catch(console.error);
    break;
  case "detail":
    if (!args[0]) { console.log("Usage: node negrisk_scanner.cjs detail <slug>"); process.exit(1); }
    detail(args[0]).catch(console.error);
    break;
  default:
    console.log("NegRisk Rebalancing Scanner");
    console.log("  node negrisk_scanner.cjs scan           — Find arbitrage opportunities");
    console.log("  node negrisk_scanner.cjs watch          — Continuous monitoring (60s)");
    console.log("  node negrisk_scanner.cjs detail <slug>  — Breakdown for specific event");
}