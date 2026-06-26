#!/usr/bin/env node
/**
 * init.js — polymarket-data-layer Cache Warm-up Script
 *
 * Sequentially runs all time-consuming queries and writes to cache,
 * so other skills can hit cache directly on first call.
 *
 * Usage:
 *   node init.js               # Warm up all (including domain expertise)
 *   node init.js --no-domains  # Skip domain expertise (faster, ~2-3 min)
 *   node init.js --fresh       # Ignore existing cache, force re-query
 */

"use strict";

const mcp = require("./mcp-client");
const q = require("./queries");
const sm = require("./smartmoney");
const cache = require("./cache");

const args = process.argv.slice(2);
const noDomains = args.includes("--no-domains");
const fresh = args.includes("--fresh");

function banner(text) {
  console.log("\n" + "─".repeat(56));
  console.log(`  ${text}`);
  console.log("─".repeat(56));
}

function step(n, total, label) {
  process.stdout.write(`\n[${n}/${total}] ${label} ... `);
}

function done(detail = "") {
  console.log(`✓${detail ? "  " + detail : ""}`);
}

async function main() {
  const TOTAL = noDomains ? 4 : 4; // smartmoney handles domains internally

  banner(`polymarket-data-layer Cache Warm-up  ${new Date().toLocaleString()}`);
  console.log(`  Mode: ${fresh ? "Force refresh" : "Incremental (skip existing cache)"}`);
  console.log(`  Domain Expertise: ${noDomains ? "Skip" : "Include (HUMAN / SIGNAL)"}`);

  // ── 0. Health check ──────────────────────────────────────────────────────────
  step(0, TOTAL, "MCP service health check");
  const alive = await mcp.ping(8000);
  if (!alive) {
    console.log("✗");
    console.error("\n❌ MCP service unavailable, please check network or service status");
    process.exit(1);
  }
  done("Connection OK");

  // ── 1. All addresses ───────────────────────────────────────────────────────
  step(1, TOTAL, "allAddresses");
  const addrs = await q.allAddresses({ fresh });
  done(`${addrs.length.toLocaleString()} addresses`);

  // ── 2. Base metrics ───────────────────────────────────────────────────────
  step(2, TOTAL, "baseMetrics (last 30 days)");
  const base = await q.baseMetrics();
  done(`${Object.keys(base).length.toLocaleString()} entries`);

  // ── 3. ROI / Win rate ─────────────────────────────────────────────────────
  step(3, TOTAL, "roiMetrics");
  const roi = await q.roiMetrics();
  done(`${Object.keys(roi).length.toLocaleString()} entries`);

  // ── 4. Smart money classification (including domain expertise) ─────────────────────────────────────
  step(4, TOTAL, `smartmoney.classify({ withDomains: ${!noDomains} })`);
  console.log(""); // newline, classify will output progress internally
  const classified = await sm.classify({ fresh, withDomains: !noDomains });

  const counts = {};
  for (const { label } of Object.values(classified)) {
    counts[label] = (counts[label] || 0) + 1;
  }
  const summary = ["HUMAN", "SIGNAL", "MM", "BOT", "COPYBOT", "NOISE"]
    .filter((l) => counts[l])
    .map((l) => `${l} ${counts[l]}`)
    .join(" · ");
  done(summary);

  // ── Complete ──────────────────────────────────────────────────────────────
  banner(`✅ Cache warm-up complete`);
  console.log(
    `  Validity:   2 hours (smartmoney) / Permanent incremental (addresses) / 2 days (conditionVols)`,
  );
  console.log(`  Cache dir: ${require("path").join(__dirname, "cache/")}`);
  console.log("");
}

main().catch((err) => {
  console.error("\n❌ Warm-up failed:", err.message || err);
  process.exit(1);
});
