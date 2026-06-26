#!/usr/bin/env node

// Overlay Protocol — Market Scanner
// Fetches all active markets with current prices and percentage changes.
// Usage: node scan.js [--details <market>]

import { fetchMarkets, fetchWithTimeout, PRICES_API, fmtPrice, fmtPct, padCol, resolveMarket } from "./common.js";

function pct(now, then) {
  if (then == null || then === 0) return null;
  return ((now - then) / Math.abs(then)) * 100;
}

// Parse --details <market>
let detailsQuery = null;
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--details" && i + 1 < args.length) {
    detailsQuery = args[++i];
  }
}

if (detailsQuery) {
  const [marketsRaw, pricesRaw] = await Promise.all([
    fetchMarkets(),
    fetchWithTimeout(PRICES_API).then((r) => r.json()),
  ]);
  const market = await resolveMarket(detailsQuery);
  const priceData = pricesRaw.find((p) => p.marketAddress.toLowerCase() === market.address);
  for (const m of marketsRaw["56"] || []) {
    for (const c of m.chains || []) {
      if (String(c.chainId) === "56" && c.deploymentAddress.toLowerCase() === market.address) {
        console.log(`== ${m.marketName} (${market.address}) ==`);
        if (priceData) {
          const price = priceData.latestPrice;
          console.log(`Price: ${fmtPrice(price)}  |  1h: ${fmtPct(pct(price, priceData.priceOneHourAgo))}  |  24h: ${fmtPct(pct(price, priceData.priceOneDayAgo))}  |  7d: ${fmtPct(pct(price, priceData.priceSevenDaysAgo))}`);
        }
        console.log("");
        console.log(m.descriptionText ? m.descriptionText.replace(/\\n/g, "\n") : "No description available.");
        process.exit(0);
      }
    }
  }
  console.error(`No description found for ${detailsQuery}`);
  process.exit(1);
}

const [marketsRaw, pricesRaw] = await Promise.all([
  fetchMarkets(),
  fetchWithTimeout(PRICES_API).then((r) => r.json()),
]);

const nameMap = {};
for (const m of marketsRaw["56"] || []) {
  for (const c of m.chains || []) {
    if (String(c.chainId) === "56" && !c.disabled && !c.deprecated) {
      nameMap[c.deploymentAddress.toLowerCase()] = m.marketName;
    }
  }
}

const rows = [];
for (const m of pricesRaw) {
  const addr = m.marketAddress.toLowerCase();
  if (!nameMap[addr]) continue;
  const price = m.latestPrice;
  rows.push({
    name: nameMap[addr], price,
    h1: pct(price, m.priceOneHourAgo),
    h24: pct(price, m.priceOneDayAgo),
    d7: pct(price, m.priceSevenDaysAgo),
  });
}
rows.sort((a, b) => a.name.localeCompare(b.name));

const now = new Date().toISOString().replace(/\.\d+Z/, "Z");
console.log(`== Overlay Markets (${now}) ==`);
console.log(`${rows.length} active markets on BSC\n`);
console.log(padCol("Market", 30, true) + padCol("Price", 18) + padCol("1h%", 10) + padCol("24h%", 10) + padCol("7d%", 10));
console.log("-".repeat(78));

for (const r of rows) {
  console.log(padCol(r.name, 30, true) + padCol(fmtPrice(r.price), 18) + padCol(fmtPct(r.h1), 10) + padCol(fmtPct(r.h24), 10) + padCol(fmtPct(r.d7), 10));
}

const with24h = rows.filter((r) => r.h24 != null).sort((a, b) => b.h24 - a.h24);
const with1h = rows.filter((r) => r.h1 != null).sort((a, b) => b.h1 - a.h1);

console.log("");
console.log("24h Gainers: " + with24h.slice(0, 3).map((r) => `${r.name} ${fmtPct(r.h24)}`).join(", "));
console.log("24h Losers:  " + with24h.slice(-3).reverse().map((r) => `${r.name} ${fmtPct(r.h24)}`).join(", "));
console.log("1h Gainers:  " + with1h.slice(0, 3).map((r) => `${r.name} ${fmtPct(r.h1)}`).join(", "));
console.log("1h Losers:   " + with1h.slice(-3).reverse().map((r) => `${r.name} ${fmtPct(r.h1)}`).join(", "));
