'use strict';
/**
 * Spark Provider — DGX Spark observability.
 * Reads: spark-metrics/snapshot.json, spark-metrics/metrics.sqlite, spark-watchdog-state.json
 */
const fs = require('fs');
const cfg = require('../lib/config');
const { sqliteJson } = require('../lib/sqlite-helper');
const { jsonReply } = require('../lib/http-helpers');

// ── Spark Ground Truth ──────────────────────────────────────────────
let _gtCache = null;
let _gtMtime = 0;

function readGroundTruth() {
  try {
    const st = fs.statSync(cfg.SPARK_METRICS_GT_FILE);
    if (st.mtimeMs === _gtMtime && _gtCache) return _gtCache;
    _gtMtime = st.mtimeMs;
    const raw = fs.readFileSync(cfg.SPARK_METRICS_GT_FILE, 'utf8');
    _gtCache = JSON.parse(raw);
    return _gtCache;
  } catch {
    return _gtCache || null;
  }
}

// ── Snapshot (real-time) ────────────────────────────────────────────
function readSnapshot() {
  const gt = readGroundTruth();
  if (!gt?.snapshotPath) return null;
  try {
    const raw = fs.readFileSync(gt.snapshotPath, 'utf8');
    const j = JSON.parse(raw);
    const ram = j.ram || {};
    const totalKb = Number(ram.ram_total_kb || 0);
    const usedKb = Number(ram.ram_used_kb || 0);
    const usedPct = totalKb > 0 ? (usedKb / totalKb) * 100 : null;
    return {
      ...j,
      derived: {
        ram_used_pct: usedPct !== null ? Number(usedPct.toFixed(2)) : null,
      },
    };
  } catch {
    return null;
  }
}

// ── Watchdog State ──────────────────────────────────────────────────
function readWatchdogState() {
  try {
    const raw = fs.readFileSync(cfg.SPARK_WATCHDOG_STATE, 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

// ── History (from metrics.sqlite) ───────────────────────────────────
function queryHistory(hours) {
  const gt = readGroundTruth();
  if (!gt?.sqlitePath) return [];
  const cutoff = Math.floor(Date.now() / 1000) - (hours * 3600);
  return sqliteJson(gt.sqlitePath, `
    SELECT ts, ts_iso, gpu_util_pct, gpu_temp_c, gpu_power_w,
           ram_used_kb, ram_total_kb, ram_available_kb,
           prompt_tokens_total, tokens_predicted_total,
           prompt_seconds_total, tokens_predicted_seconds_total
    FROM spark_samples
    WHERE ts >= ${cutoff}
    ORDER BY ts ASC
  `);
}

// ── HTTP handlers ───────────────────────────────────────────────────
function handleSnapshot(_req, res) {
  const snapshot = readSnapshot();
  const watchdog = readWatchdogState();
  const gt = readGroundTruth();
  jsonReply(res, 200, {
    snapshot,
    watchdog,
    config: gt ? { sampleEverySeconds: gt.sampleEverySeconds } : null,
  });
}

function handleHistory(req, res, query) {
  const hours = parseInt(query.hours || '24', 10);
  const rows = queryHistory(hours);
  jsonReply(res, 200, { hours, count: rows.length, rows });
}

function register(router) {
  router.add('GET', '/api/spark/snapshot', (req, res) => handleSnapshot(req, res));
  router.add('GET', '/api/spark/history',  (req, res, q) => handleHistory(req, res, q));

  // Legacy compat
  router.add('GET', '/spark/snapshot', (req, res) => handleSnapshot(req, res));
  router.add('GET', '/spark/history',  (req, res, q) => handleHistory(req, res, q));
}

module.exports = { register, readSnapshot, readWatchdogState, readGroundTruth };
