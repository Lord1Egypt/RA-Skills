/**
 * smartmoney.js — Polymarket Smart Money Classifier (Shared Module)
 *
 * Classifies addresses into: HUMAN > SIGNAL > MM > BOT > COPYBOT > NOISE
 * Results cached for 2 hours (key: smart-money:classified).
 *
 * Usage:
 *   const sm = require('../../polymarket-data-layer/scripts/smartmoney');
 *
 *   // Classify all addresses (returns directly if cached, re-runs if expired or fresh=true)
 *   const classified = await sm.classify();
 *   // classified['0xabc...'] → { label, daily_30d, avg_amount, total_volume,
 *   //                            market_count, min_gap_sec, med_gap_sec,
 *   //                            avg_roi, win_rate, realized_pnl, domains? }
 *
 *   // Load domain expertise (only HUMAN / SIGNAL addresses get domain labels)
 *   const classified = await sm.classify({ withDomains: true });
 *
 *   // Read-only cache, does not trigger re-classification (returns null if cache miss)
 *   const cached = sm.getClassified();
 *
 *   // Threshold config (transparently exported for caller reference)
 *   sm.CFG.humanWinRate  // 0.60
 */

"use strict";

const mcp = require("./mcp-client");
const cache = require("./cache");
const q = require("./queries");

// ── Classification thresholds (consistent with original classify-smart-money.js) ──────────────────────
const CFG = {
  humanDailyMax: 15, // 30-day daily avg < 15 trades
  humanMinGapSec: 30, // min gap between trades > 30 seconds
  humanWinRate: 0.6, // win rate > 60%
  humanAmountPct: 0.6, // avg amount per trade >= global p60 (Top 40%)

  signalBurstCount: 8, // 1-hour same market same direction >= 8 trades
  signalIntervalSec: 60, // densest burst avg interval < 60 seconds

  botMinGapHard: 1, // min_gap <= 1 second → millisecond-level script
  botMedianGapSec: 5, // median_gap < 5 seconds (with daily > 20)
  botDailyMax: 100, // daily avg > 100 trades

  mmBilateralRatio: 0.6, // 7-day bilateral ratio > 60%

  copybotMatchRate: 0.8, // direction match rate > 80%
  copybotLagMin: 10, // min lag 10 seconds
  copybotLagMax: 300, // max lag 5 minutes
  copybotMinPairs: 10, // valid pairs >= 10 trades

  roiMinTotalBought: 1000, // minimum total principal for ROI win rate stats
};

const CACHE_KEY = "smart-money:classified";
const CACHE_TTL = 2 * 3600; // 2 hours

function buildMetadata(queryName) {
  return {
    sourceSkill: "polymarket-smart-money-rankings",
    sourceScript: "polymarket-data-layer/scripts/smartmoney.js",
    queryName,
  };
}

async function runMcpRows(sql, { queryName, timeout = 180_000 } = {}) {
  const result = await mcp.queryStream(sql, {
    timeout,
    metadata: buildMetadata(queryName),
  });
  return result.rows || [];
}

// ── Internal queries (tightly coupled with classification logic, not in queries.js) ───────────────────

/** Global p60 amount threshold (used for HUMAN classification) */
async function fetchP60() {
  const rows = await runMcpRows(
    `
    SELECT quantile(${CFG.humanAmountPct})(amount) AS p60
    FROM default.trades
    WHERE traded_at IS NOT NULL AND amount > 0
  `,
    { queryName: "fetchP60" },
  );
  return Number(rows[0].p60);
}

/** Timing metrics: min_gap / median_gap (last 30 days, used for BOT / HUMAN classification) */
async function fetchGapMetrics() {
  const rows = await runMcpRows(
    `
    SELECT
      address,
      arrayMin(gaps) AS min_gap,
      arrayReduce('quantileExact(0.5)', gaps) AS med_gap
    FROM (
      SELECT
        wallet_address AS address,
        arrayFilter(
          gap -> gap > 0 AND gap < 31536000,
          arrayDifference(arraySort(groupArray(toUnixTimestamp(traded_at))))
        ) AS gaps
      FROM default.trades
      WHERE traded_at >= now() - INTERVAL 30 DAY
        AND traded_at IS NOT NULL
      GROUP BY wallet_address
    )
    WHERE length(gaps) > 0
  `,
    { queryName: "fetchGapMetrics" },
  );
  const m = {};
  for (const r of rows) m[r.address] = r;
  return m;
}

/** SIGNAL: 1h same market same outcome ≥8 trades and densest burst interval < 60s */
async function fetchSignalSet() {
  const rows = await runMcpRows(
    `
    SELECT address FROM (
      SELECT wallet_address AS address,
        max(cnt)    AS burst_max,
        min(avg_iv) AS burst_iv_min
      FROM (
        SELECT
          wallet_address, condition_id, outcome_side,
          toStartOfHour(traded_at) AS hr,
          count()                                                    AS cnt,
          (max(toUnixTimestamp(traded_at)) - min(toUnixTimestamp(traded_at)))
            / greatest(count() - 1, 1)                              AS avg_iv
        FROM default.trades
        WHERE traded_at >= now() - INTERVAL 30 DAY
          AND traded_at IS NOT NULL
          AND condition_id IS NOT NULL
        GROUP BY wallet_address, condition_id, outcome_side, hr
        HAVING cnt >= ${CFG.signalBurstCount}
      )
      GROUP BY address
    )
    WHERE burst_max >= ${CFG.signalBurstCount}
      AND burst_iv_min < ${CFG.signalIntervalSec}
  `,
    { queryName: "fetchSignalSet" },
  );
  return new Set(rows.map((r) => r.address));
}

/** MM: 7-day bilateral trade ratio > 60% */
async function fetchMmSet() {
  const rows = await runMcpRows(
    `
    SELECT address FROM (
      SELECT wallet_address AS address,
        countIf(b > 0 AND s > 0) / greatest(count(), 1) AS bi_ratio
      FROM (
        SELECT wallet_address, condition_id,
          countIf(side = 'buy')  AS b,
          countIf(side = 'sell') AS s
        FROM default.trades
        WHERE traded_at >= now() - INTERVAL 7 DAY
          AND traded_at IS NOT NULL
        GROUP BY wallet_address, condition_id
      )
      GROUP BY address
    )
    WHERE bi_ratio > ${CFG.mmBilateralRatio}
  `,
    { queryName: "fetchMmSet" },
  );
  return new Set(rows.map((r) => r.address));
}

/** BOT: Three timing rules (any match triggers) */
async function fetchBotSet() {
  const rows = await runMcpRows(
    `
    SELECT address FROM (
      SELECT
        address,
        arrayMin(gaps) AS min_gap,
        arrayReduce('quantileExact(0.5)', gaps) AS med_gap,
        trades / 30.0 AS daily
      FROM (
        SELECT
          wallet_address AS address,
          count() AS trades,
          arrayFilter(
            gap -> gap > 0 AND gap < 86400,
            arrayDifference(arraySort(groupArray(toUnixTimestamp(traded_at))))
          ) AS gaps
        FROM default.trades
        WHERE traded_at >= now() - INTERVAL 30 DAY
          AND traded_at IS NOT NULL
        GROUP BY wallet_address
      )
      WHERE length(gaps) > 0
    )
    WHERE min_gap <= ${CFG.botMinGapHard}
       OR (med_gap < ${CFG.botMedianGapSec} AND daily > 20)
       OR daily > ${CFG.botDailyMax}
  `,
    { queryName: "fetchBotSet" },
  );
  return new Set(rows.map((r) => r.address));
}

/** COPYBOT: Follow HUMAN addresses (requires humanSet to be determined first) */
async function fetchCopybotSet(humanSet) {
  if (humanSet.size === 0) return new Set();
  const humanList = [...humanSet]
    .slice(0, 200)
    .map((a) => `'${a}'`)
    .join(", ");
  try {
    const rows = await runMcpRows(
      `
      SELECT follower FROM (
        SELECT
          b.wallet_address AS follower,
          countIf(
            a.outcome_side = b.outcome_side
            AND a.condition_id = b.condition_id
          ) / count() AS match_rate,
          count()        AS pair_cnt
        FROM default.trades a
        JOIN default.trades b
          ON  a.condition_id    = b.condition_id
          AND a.wallet_address != b.wallet_address
          AND b.traded_at       > a.traded_at
          AND toUnixTimestamp(b.traded_at) - toUnixTimestamp(a.traded_at)
              BETWEEN ${CFG.copybotLagMin} AND ${CFG.copybotLagMax}
        WHERE a.wallet_address IN (${humanList})
          AND a.traded_at >= now() - INTERVAL 30 DAY
          AND b.traded_at >= now() - INTERVAL 30 DAY
        GROUP BY follower
        HAVING pair_cnt >= ${CFG.copybotMinPairs}
      )
      WHERE match_rate > ${CFG.copybotMatchRate}
    `,
      { queryName: "fetchCopybotSet" },
    );
    return new Set(rows.map((r) => r.follower));
  } catch (e) {
    process.stderr.write(`  ⚠ COPYBOT query failed (skipping): ${e.message}\n`);
    return new Set();
  }
}

// ── Classification Function ──────────────────────────────────────────────────────────────────

function classifyAddress(
  addr,
  { base, gap, roi, signalSet, mmSet, botSet, copybotSet, p60 },
) {
  const b = base[addr] || {};
  const g = gap[addr] || {};
  const r = roi[addr] || {};

  const daily = Number(b.daily || 0);
  const avgAmt = Number(b.avg_amount || 0);
  const minGap = Number(g.min_gap ?? 9999);
  const medGap = Number(g.med_gap ?? 9999);
  const avgRoi = Number(r.avg_roi || 0);
  const winRate = Number(r.win_rate || 0);

  // ① HUMAN (highest priority)
  if (
    daily < CFG.humanDailyMax &&
    avgAmt >= p60 &&
    minGap > CFG.humanMinGapSec &&
    (avgRoi > 0 || winRate >= CFG.humanWinRate)
  )
    return "HUMAN";

  // ② SIGNAL
  if (signalSet.has(addr)) return "SIGNAL";

  // ③ MM
  if (mmSet.has(addr)) return "MM";

  // ④ BOT
  if (botSet.has(addr)) return "BOT";

  // ⑤ COPYBOT
  if (copybotSet.has(addr)) return "COPYBOT";

  // ⑥ NOISE
  return "NOISE";
}

// ── Domain Labels ──────────────────────────────────────────────────────────────────

/**
 * Calculate domain labels based on volume distribution across domains for each address (max 3).
 *
 * Strategy:
 *   - If highest domain share < 30% → assign GEN (no clear specialization)
 *   - Otherwise take domains with share >= 15%, max 3, sorted by share descending
 *
 * @param {Object} addrDomVols  { addr → { [domain]: volume, _total: volume } }
 * @returns {Object}  { addr → ['CRY', 'POL', ...] }
 */
function computeDomainTags(addrDomVols) {
  const result = {};
  for (const [addr, domVols] of Object.entries(addrDomVols)) {
    const total = domVols._total || 0;
    const entries = Object.entries(domVols).filter(([k]) => k !== "_total");
    if (total === 0 || entries.length === 0) {
      result[addr] = ["GEN"];
      continue;
    }
    const sorted = entries
      .map(([d, v]) => ({ d, s: v / total }))
      .sort((a, b) => b.s - a.s);

    if (sorted[0].s < 0.3) {
      result[addr] = ["GEN"];
    } else {
      const labels = sorted
        .filter((x) => x.s >= 0.15)
        .slice(0, 3)
        .map((x) => x.d);
      result[addr] = labels.length ? labels : ["GEN"];
    }
  }
  return result;
}

// ── Main Entry ────────────────────────────────────────────────────────────────────

/**
 * Classify all Polymarket addresses.
 *
 * Flow:
 *   1. Check cache (2h TTL), return if hit
 *   2. Parallel query base metrics (baseMetrics / gapMetrics / roiMetrics / p60)
 *   3. Parallel run SIGNAL / MM / BOT set queries
 *   4. First round classification (determine humanSet), then query COPYBOT
 *   5. Final classification → write cache → return
 *
 * @param {{ fresh?: boolean, withDomains?: boolean }} opts
 *   fresh=true       Ignore cache and force re-classification
 *   withDomains=true Calculate domain expertise for HUMAN/SIGNAL addresses (slow, +10~30s)
 *
 * @returns {Promise<Object>}
 *   { address → { label, daily_30d, avg_amount, total_volume, market_count,
 *                 min_gap_sec, med_gap_sec, avg_roi, win_rate, realized_pnl,
 *                 domains? } }
 */
async function classify({ fresh = false, withDomains = false } = {}) {
  if (!fresh) {
    const cached = cache.get(CACHE_KEY, { ttl: CACHE_TTL });
    if (cached) {
      return cached;
    }
  }

  const totalSteps = withDomains ? 10 : 8;
  let step = 0;
  const t0 = Date.now();
  function log(msg) {
    step++;
    const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
    process.stderr.write(
      `[smart-money] [${step}/${totalSteps}] ${msg} (+${elapsed}s)\n`,
    );
  }

  // 1. Sequential fetch base data (sequential to avoid concurrent competition for shared analysis resources)
  process.stderr.write(`[smart-money] Starting classification (${totalSteps} steps total)...\n`);

  log("p60 amount threshold...");
  const p60 = await fetchP60();
  process.stderr.write(`  p60 = $${p60.toFixed(2)} USDC\n`);

  log("All addresses...");
  const allAddrs = await q.allAddresses();
  process.stderr.write(`  ${allAddrs.length.toLocaleString()} addresses\n`);

  log("Base metrics (daily avg, avg amount, total volume)...");
  const base = await q.baseMetrics();

  log("Timing metrics (min_gap / median_gap)...");
  const gap = await fetchGapMetrics();

  log("ROI / Win rate (positions table)...");
  const roi = await q.roiMetrics({ minBought: CFG.roiMinTotalBought });

  // 2. Sequential run set queries for each type
  log("SIGNAL detection...");
  const signalSet = await fetchSignalSet();
  process.stderr.write(`  ${signalSet.size}\n`);

  log("MM detection...");
  const mmSet = await fetchMmSet();
  process.stderr.write(`  ${mmSet.size}\n`);

  log("BOT detection...");
  const botSet = await fetchBotSet();
  process.stderr.write(`  ${botSet.size}\n`);

  // 3. First round classification (determine humanSet for COPYBOT)
  const preLabels = {};
  const humanSet = new Set();
  for (const addr of allAddrs) {
    const label = classifyAddress(addr, {
      base,
      gap,
      roi,
      p60,
      signalSet,
      mmSet,
      botSet,
      copybotSet: new Set(),
    });
    preLabels[addr] = label;
    if (label === "HUMAN") humanSet.add(addr);
  }
  process.stderr.write(`  HUMAN candidates: ${humanSet.size}\n`);

  // 4. COPYBOT query (depends on humanSet)
  // step count not included in totalSteps because this step follows BOT
  const elapsed8 = ((Date.now() - t0) / 1000).toFixed(1);
  process.stderr.write(
    `[smart-money] COPYBOT detection (JOIN query)... (+${elapsed8}s)\n`,
  );
  const copybotSet = await fetchCopybotSet(humanSet);
  process.stderr.write(`  ${copybotSet.size}\n`);

  // 5. Final classification + merge metrics
  const classified = {};
  for (const addr of allAddrs) {
    let label = preLabels[addr];
    if (label !== "HUMAN" && copybotSet.has(addr)) label = "COPYBOT";

    const b = base[addr] || {};
    const g = gap[addr] || {};
    const r = roi[addr] || {};

    classified[addr] = {
      label,
      daily_30d: Number(b.daily || 0),
      avg_amount: Number(b.avg_amount || 0),
      total_volume: Number(b.total_volume || 0),
      market_count: Number(b.market_count || 0),
      min_gap_sec: g.min_gap != null ? Number(g.min_gap) : null,
      med_gap_sec: g.med_gap != null ? Number(g.med_gap) : null,
      avg_roi: Number(r.avg_roi || 0),
      win_rate: Number(r.win_rate || 0),
      realized_pnl: Number(r.realized_pnl || 0),
    };
  }

  // Statistics classification results
  const counts = {};
  for (const { label } of Object.values(classified))
    counts[label] = (counts[label] || 0) + 1;
  process.stderr.write(
    `  Classification complete: ${Object.entries(counts)
      .map(([k, v]) => `${k}=${v}`)
      .join(" ")}\n`,
  );

  // 6. Optional: Domain expertise (all addresses, gamma mapping done inside conditionVols)
  if (withDomains) {
    log("conditionVols (domain volume distribution, batch query)...");
    const batchTotal = Math.ceil(allAddrs.length / 2000);
    process.stderr.write(`  ${batchTotal} batches, 2000 addresses each\n`);
    const domVols = await q.conditionVols(allAddrs, { fresh });

    log("Calculate domain labels...");
    const domainTags = computeDomainTags(domVols);
    for (const addr of allAddrs) {
      classified[addr].domains = domainTags[addr] || ["GEN"];
    }
  }

  const totalElapsed = ((Date.now() - t0) / 1000).toFixed(1);
  process.stderr.write(`[smart-money] Classification complete, total time ${totalElapsed}s\n`);

  cache.set(CACHE_KEY, classified);
  return classified;
}

/**
 * Read-only access to cached classification results, does not trigger re-classification.
 * Suitable for callers that only need to consume existing results without long queries from cache expiration.
 *
 * @param {{ maxAge?: number }} opts  maxAge in seconds, default 2 hours
 * @returns {Object|null}  null means cache miss or expired
 */
function getClassified({ maxAge = CACHE_TTL } = {}) {
  return cache.get(CACHE_KEY, { ttl: maxAge }) || null;
}

module.exports = { classify, getClassified, computeDomainTags, CFG };
