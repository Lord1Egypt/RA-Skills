#!/usr/bin/env -S npx tsx
/**
 * Expiry Arbitrage Scanner for Polymarket
 *
 * Strategy: For same-event markets with different expiry dates,
 * probability MUST be monotonically increasing with time:
 *   P("by Feb 28") ≤ P("by Mar 31") ≤ P("by Jun 30") ≤ P("by Dec 31")
 *
 * Any violation = risk-free arbitrage:
 *   - If P(early) > P(later): BUY YES on later, BUY NO on earlier
 *   - The later expiry MUST resolve YES if the earlier one does
 *
 * Usage: npx tsx expiry-arb.ts "US strikes Iran" [--threshold 0.5]
 */

import { execSync } from "node:child_process";

interface Market {
  question: string;
  id: string;
  slug: string;
  yes_price: number;
  no_price: number;
  volume: number;
  liquidity: number;
  active: boolean;
  closed: boolean;
  clob_token_ids?: string[];
  condition_id?: string;
}

interface DatedMarket extends Market {
  expiryDate: Date;
  expiryStr: string;
}

interface ArbOpportunity {
  earlier: DatedMarket;
  later: DatedMarket;
  spread: number; // earlier.yes - later.yes (should be negative)
  profitBps: number;
  action: string;
}

// ─── Parse CLI args ──────────────────────────────────────────────

const args = process.argv.slice(2);
let query = "US strikes Iran";
let threshold = 0.5; // cents
let showAll = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--threshold" && args[i + 1]) {
    threshold = parseFloat(args[i + 1]);
    i++;
  } else if (args[i] === "--all") {
    showAll = true;
  } else if (!args[i].startsWith("--")) {
    query = args[i];
  }
}

// ─── Fetch markets ──────────────────────────────────────────────

console.log(`\n🔍 Scanning expiry arbitrage for: "${query}"`);
console.log(`   Threshold: ${threshold}¢\n`);

let rawOutput: string;
try {
  rawOutput = execSync(
    `source "$HOME/.cargo/env" 2>/dev/null; polymarket -o json markets search "${query}" --limit 200`,
    { encoding: "utf-8", shell: "/bin/bash", maxBuffer: 50 * 1024 * 1024 }
  );
} catch (e: any) {
  console.error("Failed to fetch markets:", e.stderr || e.message);
  process.exit(1);
}

let markets: any[];
try {
  const parsed = JSON.parse(rawOutput);
  markets = parsed.markets || parsed.data || parsed || [];
  if (!Array.isArray(markets)) {
    // Try extracting from nested structure
    if (parsed.results) markets = parsed.results;
    else markets = [parsed];
  }
} catch {
  console.error("Failed to parse market data");
  console.log("Raw output:", rawOutput.slice(0, 500));
  process.exit(1);
}

console.log(`📊 Found ${markets.length} markets\n`);

// ─── Extract expiry dates from questions ────────────────────────

const datePatterns = [
  // "by March 31, 2026"
  /by\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:,?\s+(\d{4}))?/i,
  // "by March 31?"
  /by\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\??/i,
  // "by December 31, 2026"
  /by\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2})(?:,?\s+(\d{4}))?/i,
];

const months: Record<string, number> = {
  january: 0, february: 1, march: 2, april: 3, may: 4, june: 5,
  july: 6, august: 7, september: 8, october: 9, november: 10, december: 11,
  jan: 0, feb: 1, mar: 2, apr: 3, jun: 5, jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11,
};

function extractDate(question: string): Date | null {
  for (const pattern of datePatterns) {
    const match = question.match(pattern);
    if (match) {
      const monthStr = match[1].toLowerCase();
      const day = parseInt(match[2]);
      const year = match[3] ? parseInt(match[3]) : 2026;
      const month = months[monthStr];
      if (month !== undefined) {
        return new Date(year, month, day);
      }
    }
  }
  return null;
}

function extractBaseEvent(question: string): string {
  // Remove the date part to get the base event
  return question
    .replace(/\s*by\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,?\s+\d{4})?\s*\??/i, "")
    .replace(/\s*on\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,?\s+\d{4})?\s*\(?[A-Z]*\)?\s*\??/i, "")
    .replace(/\s*before\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\s*\(?[A-Z]*\)?\s*\??/i, "")
    .replace(/\s*in\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\s*\(?[A-Z]*\)?\s*\??/i, "")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\?$/, "")
    .trim();
}

// ─── Group markets by base event ────────────────────────────────

const datedMarkets: DatedMarket[] = [];

for (const m of markets) {
  const q = m.question || m.title || "";
  const date = extractDate(q);
  if (!date) continue;

  // Extract price
  let yesPrice = 0;
  if (m.outcomePrices) {
    let prices = m.outcomePrices;
    if (typeof prices === "string") {
      try { prices = JSON.parse(prices); } catch {}
    }
    if (Array.isArray(prices)) {
      yesPrice = parseFloat(prices[0] || "0");
    }
  }
  if (!yesPrice && m.yes_price !== undefined) yesPrice = m.yes_price;
  if (!yesPrice && m.tokens && m.tokens[0]?.price) yesPrice = parseFloat(m.tokens[0].price);
  if (!yesPrice && m.bestBid !== undefined) yesPrice = m.bestBid;

  // Some markets return price in 0-1, some in cents
  if (yesPrice > 1) yesPrice = yesPrice / 100;

  // Extract volume/liquidity
  const volume = parseFloat(m.volume || "0");
  const liquidity = parseFloat(m.liquidity || "0");

  // Active check — also use "closed" field and endDate
  const endDate = m.endDate ? new Date(m.endDate) : null;
  const isClosed = m.closed === true || m.closedTime != null;

  const active = !isClosed && m.active !== false;
  if (!active && !showAll) continue;

  datedMarkets.push({
    ...m,
    question: q,
    yes_price: yesPrice,
    no_price: 1 - yesPrice,
    volume,
    liquidity,
    active,
    closed: isClosed,
    expiryDate: date,
    expiryStr: date.toISOString().split("T")[0],
  });
}

// Group by base event
const groups: Record<string, DatedMarket[]> = {};
for (const m of datedMarkets) {
  const base = extractBaseEvent(m.question);
  if (!groups[base]) groups[base] = [];
  groups[base].push(m);
}

// Sort each group by date
for (const base of Object.keys(groups)) {
  groups[base].sort((a, b) => a.expiryDate.getTime() - b.expiryDate.getTime());
}

// ─── Find arbitrage opportunities ───────────────────────────────

const opportunities: ArbOpportunity[] = [];

for (const [base, mkts] of Object.entries(groups)) {
  if (mkts.length < 2) continue;

  console.log(`\n📈 ${base}`);
  console.log("─".repeat(80));
  console.log(
    `${"Expiry".padEnd(12)} ${"Yes Price".padStart(10)} ${"Volume".padStart(12)} ${"Liquidity".padStart(12)} ${"Status".padStart(8)}`
  );
  console.log("─".repeat(80));

  for (const m of mkts) {
    const priceStr = `${(m.yes_price * 100).toFixed(2)}¢`;
    const volStr = m.volume > 1e6 ? `$${(m.volume / 1e6).toFixed(1)}M` : `$${(m.volume / 1e3).toFixed(0)}K`;
    const liqStr = m.liquidity > 1e6 ? `$${(m.liquidity / 1e6).toFixed(1)}M` : `$${(m.liquidity / 1e3).toFixed(0)}K`;
    const status = m.active ? "Active" : "Closed";
    console.log(
      `${m.expiryStr.padEnd(12)} ${priceStr.padStart(10)} ${volStr.padStart(12)} ${liqStr.padStart(12)} ${status.padStart(8)}`
    );
  }

  // Check monotonicity
  for (let i = 0; i < mkts.length - 1; i++) {
    for (let j = i + 1; j < mkts.length; j++) {
      const earlier = mkts[i];
      const later = mkts[j];

      if (!earlier.active || !later.active) continue;

      const spreadCents = (earlier.yes_price - later.yes_price) * 100;

      if (spreadCents > threshold) {
        // VIOLATION: earlier expiry priced higher than later
        const arb: ArbOpportunity = {
          earlier,
          later,
          spread: spreadCents,
          profitBps: Math.round(spreadCents * 100 / (earlier.yes_price * 100)),
          action: `BUY YES "${later.question}" @ ${(later.yes_price * 100).toFixed(2)}¢ + BUY NO "${earlier.question}" @ ${(earlier.no_price * 100).toFixed(2)}¢`,
        };
        opportunities.push(arb);
      }

      // Also check: if later is significantly cheaper, flag as potential mispricing
      if (-spreadCents > 50 && earlier.active && later.active) {
        // Large gap between sequential expiries — possible value trade
        // (Not pure arb, but the spread might be too wide)
      }
    }
  }

  // Show term structure analysis
  const activeMkts = mkts.filter((m) => m.active);
  if (activeMkts.length >= 2) {
    console.log("\n  Term Structure:");
    for (let i = 0; i < activeMkts.length - 1; i++) {
      const curr = activeMkts[i];
      const next = activeMkts[i + 1];
      const impliedProb = (next.yes_price - curr.yes_price) * 100;
      const daysDiff = Math.round(
        (next.expiryDate.getTime() - curr.expiryDate.getTime()) / (1000 * 60 * 60 * 24)
      );
      const dailyProb = daysDiff > 0 ? (impliedProb / daysDiff).toFixed(3) : "N/A";
      const arrow = impliedProb >= 0 ? "✅" : "⚠️ VIOLATION";
      console.log(
        `  ${curr.expiryStr} → ${next.expiryStr} (${daysDiff}d): ` +
        `Δ = ${impliedProb >= 0 ? "+" : ""}${impliedProb.toFixed(2)}¢ ` +
        `(${dailyProb}¢/day) ${arrow}`
      );
    }
  }
}

// ─── Report opportunities ───────────────────────────────────────

console.log("\n\n" + "═".repeat(80));

if (opportunities.length === 0) {
  console.log("✅ No arbitrage opportunities found (all term structures are monotonic)");
} else {
  console.log(`🚨 ${opportunities.length} ARBITRAGE OPPORTUNITIES FOUND\n`);

  for (const arb of opportunities.sort((a, b) => b.spread - a.spread)) {
    console.log(`╭${"─".repeat(78)}╮`);
    console.log(`│ SPREAD: ${arb.spread.toFixed(2)}¢ (${arb.profitBps} bps)`.padEnd(79) + "│");
    console.log(`│`.padEnd(79) + "│");
    console.log(`│ Earlier: ${arb.earlier.question}`.slice(0, 79).padEnd(79) + "│");
    console.log(`│   Price: ${(arb.earlier.yes_price * 100).toFixed(2)}¢ YES | Expiry: ${arb.earlier.expiryStr}`.padEnd(79) + "│");
    console.log(`│`.padEnd(79) + "│");
    console.log(`│ Later:   ${arb.later.question}`.slice(0, 79).padEnd(79) + "│");
    console.log(`│   Price: ${(arb.later.yes_price * 100).toFixed(2)}¢ YES | Expiry: ${arb.later.expiryStr}`.padEnd(79) + "│");
    console.log(`│`.padEnd(79) + "│");
    console.log(`│ ACTION:`.padEnd(79) + "│");
    const actionLines = arb.action.match(/.{1,76}/g) || [arb.action];
    for (const line of actionLines) {
      console.log(`│   ${line}`.padEnd(79) + "│");
    }
    console.log(`│`.padEnd(79) + "│");
    console.log(`│ RATIONALE: Later expiry includes all earlier outcomes.`.padEnd(79) + "│");
    console.log(`│ If earlier resolves YES → later MUST resolve YES.`.padEnd(79) + "│");
    console.log(`│ So P(later) ≥ P(earlier) always. Violation = free money.`.padEnd(79) + "│");
    console.log(`╰${"─".repeat(78)}╯\n`);
  }
}

// ─── Summary stats ──────────────────────────────────────────────

console.log("\n📊 Summary:");
console.log(`   Events scanned: ${Object.keys(groups).length}`);
console.log(`   Markets analyzed: ${datedMarkets.filter((m) => m.active).length} active / ${datedMarkets.length} total`);
console.log(`   Arbitrage opportunities: ${opportunities.length}`);
if (opportunities.length > 0) {
  const maxSpread = Math.max(...opportunities.map((o) => o.spread));
  console.log(`   Max spread: ${maxSpread.toFixed(2)}¢`);
}
console.log("");
