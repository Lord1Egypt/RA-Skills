/**
 * queries.js — Common Polymarket Pre-built Queries
 *
 * Encapsulates common queries based on mcp-client for direct use by skills,
 * does not contain any business classification logic (thresholds, label determination, etc. are decided by the caller).
 *
 * Usage:
 *   const q = require('../../polymarket-data-layer/scripts/queries');
 *
 *   const addrs  = await q.allAddresses();
 *   const base   = await q.baseMetrics({ days: 30 });
 *   const roi    = await q.roiMetrics({ minBought: 1000 });
 *   const vols   = await q.conditionVols(['0xabc...', '0xdef...']);
 */

"use strict";

const mcp = require("./mcp-client");
const cache = require("./cache");
const gamma = require("./gamma-client");

// ── Utilities ──────────────────────────────────────────────────────
function toMap(rows, key = "address") {
  const m = {};
  for (const r of rows) m[r[key]] = r;
  return m;
}

function buildMetadata(queryName, extra = {}) {
  return {
    sourceSkill: "polymarket-data-layer",
    sourceScript: "polymarket-data-layer/scripts/queries.js",
    queryName,
    ...extra,
  };
}

async function runRows(
  sql,
  {
    queryName,
    timeout = 60_000,
    maxRows = 50_000,
    useStream = false,
    metadata = {},
  } = {},
) {
  const mergedMetadata = buildMetadata(queryName, metadata);

  if (useStream) {
    const result = await mcp.queryStream(sql, {
      timeout,
      metadata: mergedMetadata,
    });
    return result.rows || [];
  }

  return mcp.queryWithRetry(sql, {
    timeout,
    maxRows,
    metadata: mergedMetadata,
  });
}

// ── Query Functions ──────────────────────────────────────────────────

/**
 * Full deduped address list (incremental, cache first).
 *
 * Cache format (key: all-addresses):
 *   { addresses: string[], lastCheckedAt: 'YYYY-MM-DD HH:MM:SS' }
 *
 * Incremental strategy:
 *   When cache exists, only query new addresses with traded_at > lastCheckedAt, append to existing set.
 *   Addresses only increase, never decrease, so accumulated set is always valid, no TTL set.
 *
 * @param {{ fresh?: boolean }} opts  fresh=true ignores cache and forces full re-query
 * @returns {Promise<string[]>}
 */
async function allAddresses({ fresh = false } = {}) {
  const CACHE_KEY = "all-addresses";
  const cached = !fresh && cache.get(CACHE_KEY, { ttl: Infinity });

  // When cache exists, use incremental: only query new addresses, use DISTINCT instead of GROUP BY + max (faster)
  let rows;
  if (cached) {
    rows = await runRows(
      `
      SELECT DISTINCT wallet_address AS address
      FROM default.trades
      WHERE traded_at > toDateTime('${cached.lastCheckedAt}')
        AND traded_at IS NOT NULL
    `,
      {
        queryName: "allAddresses",
        timeout: 180_000,
        useStream: true,
        metadata: { cacheMode: "incremental" },
      },
    );
  } else {
    rows = await runRows(
      `
      SELECT DISTINCT wallet_address AS address
      FROM default.trades
      WHERE traded_at IS NOT NULL
    `,
      {
        queryName: "allAddresses",
        timeout: 180_000,
        useStream: true,
        metadata: { cacheMode: "full" },
      },
    );
  }

  // New lastCheckedAt: use server now() instead of scanning max(traded_at) to avoid full table rescan
  const nowRows = await runRows(
    `SELECT formatDateTime(now(), '%Y-%m-%d %H:%i:%S') AS ts`,
    {
      queryName: "allAddresses",
      maxRows: 1,
      metadata: { cacheMode: cached ? "incremental" : "full" },
    },
  );
  const lastCheckedAt =
    nowRows[0]?.ts || new Date().toISOString().replace("T", " ").slice(0, 19);

  const newAddrs = rows.map((r) => r.address);
  const merged = cached
    ? [...new Set([...cached.addresses, ...newAddrs])]
    : newAddrs;

  cache.set(CACHE_KEY, { addresses: merged, lastCheckedAt });
  return merged;
}

/**
 * Basic trading metrics (daily avg count, avg amount per order, market count, total volume).
 *
 * @param {{ days?: number }} opts  Statistics window, default 30 days
 * @returns {Promise<Object>}  { address → { daily, avg_amount, market_count, total_volume } }
 */
async function baseMetrics({ days = 30 } = {}) {
  return toMap(
    await runRows(
      `
    SELECT
      wallet_address                      AS address,
      count() / ${days}.0                 AS daily,
      avg(toFloat64(amount))              AS avg_amount,
      countDistinct(condition_id)         AS market_count,
      sum(toFloat64(amount))              AS total_volume
    FROM default.trades
    WHERE traded_at >= now() - INTERVAL ${days} DAY
      AND traded_at IS NOT NULL
    GROUP BY wallet_address
  `,
      {
        queryName: "baseMetrics",
        timeout: 180_000,
        useStream: true,
      },
    ),
  );
}

/**
 * ROI / Win rate / Realized PnL (from positions table).
 *
 * @param {{ minBought?: number }} opts  Filter out addresses with total bought < minBought (default 1000 USDC)
 * @returns {Promise<Object>}  { address → { avg_roi, win_rate, realized_pnl } }
 */
async function roiMetrics({ minBought = 1000 } = {}) {
  return toMap(
    await runRows(
      `
    SELECT
      address,
      (sum_pnl + sum_upnl) / (sum_bought + 1e-9)  AS avg_roi,
      sum_wins / (sum_closed + 1e-9)               AS win_rate,
      sum_pnl                                      AS realized_pnl
    FROM (
      SELECT
        wallet_address                                         AS address,
        sum(toFloat64(realized_pnl))                           AS sum_pnl,
        sum(toFloat64(unrealized_pnl))                         AS sum_upnl,
        sum(toFloat64(total_bought))                           AS sum_bought,
        countIf(is_closed = 1 AND toFloat64(realized_pnl) > 0) AS sum_wins,
        countIf(is_closed = 1)                                 AS sum_closed
      FROM default.positions
      GROUP BY wallet_address
      HAVING sum(toFloat64(total_bought)) >= ${minBought}
    )
  `,
      {
        queryName: "roiMetrics",
        timeout: 180_000,
        useStream: true,
      },
    ),
  );
}

/**
 * Cumulative trading volume by domain for specified addresses (incremental cache, 2-day TTL).
 * Applicable for domain expertise analysis scenarios.
 *
 * Cache format (key: conditionVols):
 *   { domVols: { addr → { [domain]: volume, _total: volume } }, lastCheckedAt: 'YYYY-MM-DD HH:MM:SS' }
 *
 * Incremental strategy:
 *   - When cache exists, only query new trades with traded_at > lastCheckedAt, delta mapped via gamma and overlaid on cache
 *   - New addresses not in cache, do full supplementary query
 *   - After 2-day TTL expires, full re-query to avoid accumulation of mapping errors for early unmapped conditionIds
 *
 * @param {string[]} addresses
 * @param {{ fresh?: boolean }} opts  fresh=true ignores cache and forces full re-query
 * @returns {Promise<Object>}  { addr → { [domain]: volume, _total: volume } }
 */
async function conditionVols(addresses, { fresh = false } = {}) {
  if (!addresses || addresses.length === 0) return {};

  const CACHE_KEY = "conditionVols";
  const CACHE_TTL_SEC = 2 * 24 * 3600; // 2 days
  const BATCH = 2000;
  const addrList = [...new Set(addresses.map((a) => a.toLowerCase()))];
  const cached = !fresh && cache.get(CACHE_KEY, { ttl: CACHE_TTL_SEC });

  // Batch query, returns conditionId-level intermediate results { addr → { conditionId → vol } }
  async function queryBatchedRaw(addrs, extraWhere = "") {
    const raw = {};
    const total = Math.ceil(addrs.length / BATCH);
    for (let i = 0; i < addrs.length; i += BATCH) {
      const batchNum = Math.floor(i / BATCH) + 1;
      process.stderr.write(`\r  conditionVols batch ${batchNum}/${total}...`);
      const inList = addrs
        .slice(i, i + BATCH)
        .map((a) => `'${a}'`)
        .join(", ");
      const batchRows = await runRows(
        `
        SELECT wallet_address AS addr,
               condition_id,
               sum(toFloat64(amount)) AS vol
        FROM default.trades
        WHERE wallet_address IN (${inList})
          AND traded_at IS NOT NULL
          AND amount > 0
          AND condition_id IS NOT NULL
          ${extraWhere}
        GROUP BY addr, condition_id
      `,
        {
          queryName: "conditionVols",
          timeout: 180_000,
          useStream: true,
          metadata: {
            batchSize: addrs.slice(i, i + BATCH).length,
            cacheMode: extraWhere ? "incremental" : "full",
          },
        },
      );
      for (const r of batchRows) {
        if (!raw[r.addr]) raw[r.addr] = {};
        raw[r.addr][r.condition_id] =
          (raw[r.addr][r.condition_id] || 0) + Number(r.vol);
      }
    }
    process.stderr.write("\n");
    return raw;
  }

  // Full conditionId top 10k by total volume, one gamma mapping, merge to domVols
  async function applyGammaAndMerge(base, rawCondVols) {
    const cidVolMap = {};
    for (const condVols of Object.values(rawCondVols)) {
      for (const [cid, vol] of Object.entries(condVols)) {
        cidVolMap[cid] = (cidVolMap[cid] || 0) + vol;
      }
    }
    const topCids = Object.entries(cidVolMap)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10_000)
      .map(([cid]) => cid);

    const domainMap =
      topCids.length > 0 ? await gamma.buildDomainMap(topCids) : {};
    for (const [addr, condVols] of Object.entries(rawCondVols)) {
      if (!base[addr]) base[addr] = { _total: 0 };
      for (const [cid, vol] of Object.entries(condVols)) {
        base[addr]._total = (base[addr]._total || 0) + vol;
        const d = domainMap[cid];
        if (d) base[addr][d] = (base[addr][d] || 0) + vol;
      }
    }
  }

  // Use server current time as this session's lastCheckedAt
  const nowRows = await runRows(
    `SELECT formatDateTime(now(), '%Y-%m-%d %H:%i:%S') AS ts`,
    {
      queryName: "conditionVols",
      maxRows: 1,
      metadata: { cacheMode: cached ? "incremental" : "full" },
    },
  );
  const lastCheckedAt =
    nowRows[0]?.ts || new Date().toISOString().replace("T", " ").slice(0, 19);

  let domVols;

  if (!cached) {
    domVols = {};
    const raw = await queryBatchedRaw(addrList);
    await applyGammaAndMerge(domVols, raw);
  } else {
    domVols = cached.domVols;

    // New addresses: not in cache, need full supplementary query
    const newAddrs = addrList.filter((a) => !(a in domVols));
    if (newAddrs.length > 0) {
      process.stderr.write(
        `\n  conditionVols new address supplementary query ${newAddrs.length}...\n`,
      );
      const raw = await queryBatchedRaw(newAddrs);
      await applyGammaAndMerge(domVols, raw);
    }

    // Incremental: only query new trades after lastCheckedAt
    const deltaRaw = await queryBatchedRaw(
      addrList,
      `AND traded_at > toDateTime('${cached.lastCheckedAt}')`,
    );
    await applyGammaAndMerge(domVols, deltaRaw);
  }

  cache.set(CACHE_KEY, { domVols, lastCheckedAt });
  return domVols;
}

module.exports = { allAddresses, baseMetrics, roiMetrics, conditionVols };
