'use strict';
/**
 * Cron Provider — reads cron/jobs.json + cron/runs/, enriches with Ground Truth + Ledger.
 */
const fs = require('fs');
const path = require('path');
const cfg = require('../lib/config');
const { jsonReply } = require('../lib/http-helpers');
const { sqliteJson } = require('../lib/sqlite-helper');
const gt = require('./ground-truth');

function loadCronStore() {
  try {
    const raw = fs.readFileSync(cfg.CRON_STORE_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : (parsed.jobs || []);
  } catch {
    return [];
  }
}

function dedupeJobs(jobs) {
  const byId = new Map();
  for (const job of (jobs || [])) {
    const id = job?.id || job?.jobId;
    if (!id) continue;
    byId.set(id, job); // keep latest definition when duplicated
  }
  return Array.from(byId.values());
}

function loadCronRuns(jobId, limit = 10) {
  // Read JSONL file at ~/.openclaw/cron/runs/{jobId}.jsonl
  const runsFile = path.join(cfg.CRON_RUNS_DIR, `${jobId}.jsonl`);
  try {
    const raw = fs.readFileSync(runsFile, 'utf8');
    const lines = raw.trim().split('\n').filter(Boolean);
    const runs = [];
    for (const line of lines) {
      try {
        const record = JSON.parse(line);
        if (record.action === 'finished') {
          // Normalize fields to match expected format
          const provider = record.provider || null;
          const modelRaw = record.model || null;
          const model = provider && modelRaw ? `${provider}/${modelRaw}` : (modelRaw || provider || null);
          runs.push({
            status: record.status || 'unknown',
            startedAt: new Date(record.runAtMs).toISOString(),
            finishedAt: new Date(record.ts).toISOString(),
            durationMs: record.durationMs || 0,
            model,
            provider,
            tokens: record.usage?.total_tokens || 0,
            costUsd: 0, // Not available in JSONL
          });
        }
      } catch {}
    }
    runs.sort((a, b) => {
      const ta = Date.parse(a.finishedAt || a.startedAt || 0);
      const tb = Date.parse(b.finishedAt || b.startedAt || 0);
      return tb - ta;
    });
    return runs.slice(0, limit);
  } catch {
    return [];
  }
}

function loadLastCronRun(jobId) {
  const runs = loadCronRuns(jobId, 1);
  return runs[0] || null;
}

function handleCronList(_req, res) {
  const jobs = dedupeJobs(loadCronStore());
  const channelNames = gt.parse().channelNames;

  const enriched = jobs.map(job => {
    const id = job.id || job.jobId;
    const lastRun = loadLastCronRun(id);
    const deliveryTo = job.delivery?.to;
    const chatId = deliveryTo ? (deliveryTo.match(/(\d{17,20})/) || [])[1] : null;

    return {
      id,
      name: job.name,
      enabled: job.enabled !== false,
      schedule: job.schedule,
      model: job.payload?.model || null,
      sessionTarget: job.sessionTarget,
      delivery: job.delivery,
      deliveryChatId: chatId,
      deliveryChannelName: chatId ? (channelNames[chatId] || null) : null,
      lastRun: lastRun ? {
        status: lastRun.status,
        startedAt: lastRun.startedAt,
        finishedAt: lastRun.finishedAt,
        durationMs: lastRun.durationMs,
        usage: lastRun.usage || null,
      } : null,
    };
  });

  jsonReply(res, 200, { count: enriched.length, jobs: enriched });
}

function handleCronRuns(req, res, query) {
  const jobId = query.jobId;
  if (!jobId) return jsonReply(res, 400, { error: 'jobId required' });
  const limit = parseInt(query.limit || '10', 10);
  const runs = loadCronRuns(jobId, limit);
  jsonReply(res, 200, { jobId, count: runs.length, runs });
}

function handleCronCosts(_req, res) {
  const jobs = dedupeJobs(loadCronStore());

  // ── Ledger: token/cost per job (remote models — JSONL has no usage) ─
  // session_key format: agent:main:cron:{jobId}:run:{runId}
  const todayLedger   = {}; // jobId → { tokens, cost }         (today)
  const historyLedger = {}; // jobId → { tokens, cost, runs }   (last 30d)
  try {
    const todayStr30 = new Date(Date.now() - 30 * 86400 * 1000)
      .toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
    const ledgerRows = sqliteJson(cfg.LEDGER_DB, `
      SELECT
        substr(session_key,
          instr(session_key,':cron:')+6,
          instr(session_key,':run:')-instr(session_key,':cron:')-6
        ) as job_id,
        date(ts,'localtime') as day,
        sum(input_tokens+output_tokens+cache_read_tokens+cache_write_tokens) as tokens,
        round(sum(cost_total),6) as cost,
        count(DISTINCT session_key) as runs
      FROM calls
      WHERE session_key LIKE '%:cron:%'
        AND date(ts,'localtime') >= '${todayStr30}'
      GROUP BY job_id, day
    `);
    const todayStr = new Date().toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
    for (const r of ledgerRows) {
      if (!r.job_id) continue;
      // history
      if (!historyLedger[r.job_id]) historyLedger[r.job_id] = { tokens: 0, cost: 0, runs: 0 };
      historyLedger[r.job_id].tokens += r.tokens || 0;
      historyLedger[r.job_id].cost   += r.cost   || 0;
      historyLedger[r.job_id].runs   += r.runs   || 0;
      // today
      if (r.day === todayStr) {
        todayLedger[r.job_id] = { tokens: r.tokens || 0, cost: r.cost || 0 };
      }
    }
  } catch (_) { /* ledger unavailable — degrade gracefully */ }

  // ── Per-job run stats from JSONL files ────────────────────────────
  const DAYS = 30;
  const cutoff = Date.now() - DAYS * 86400 * 1000;

  const jobStats = jobs.map(job => {
    const id = job.id || job.jobId;
    const runs = loadCronRuns(id, 200); // up to 200 runs for stats
    const recentRuns = runs.filter(r => Date.parse(r.finishedAt || r.startedAt || '') >= cutoff);

    // Aggregate by day
    const byDay = {};
    for (const r of recentRuns) {
      const ts = Date.parse(r.finishedAt || r.startedAt || '');
      if (!Number.isFinite(ts)) continue;
      const day = new Date(ts).toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' }); // YYYY-MM-DD
      if (!byDay[day]) byDay[day] = { date: day, runs: 0, tokens: 0, cost: 0 };
      byDay[day].runs++;
      byDay[day].tokens += r.tokens || 0;
      byDay[day].cost += r.costUsd || 0;
    }
    const daily = Object.values(byDay).sort((a, b) => a.date < b.date ? -1 : 1);
    for (const d of daily) {
      d.tokensPerRun = d.runs > 0 ? Math.round(d.tokens / d.runs) : 0;
      d.costPerRun = d.runs > 0 ? d.cost / d.runs : 0;
    }

    const totalRuns = recentRuns.length;
    const jsonlTokens = recentRuns.reduce((s, r) => s + (r.tokens || 0), 0);
    const jsonlCost   = recentRuns.reduce((s, r) => s + (r.costUsd || 0), 0);
    const ledgerHist  = historyLedger[id] || { tokens: 0, cost: 0 };
    const totalTokens = jsonlTokens || ledgerHist.tokens;  // JSONL first, ledger fallback
    const totalCost   = jsonlCost   || ledgerHist.cost;
    const totalDurationMs = recentRuns.reduce((s, r) => s + (r.durationMs || 0), 0);

    // Detect missing usage (cost = 0 but run finished)
    const runsWithoutUsage = recentRuns.filter(r => !r.tokens && r.status === 'ok').length;
    const runsWithZeroTokens = recentRuns.filter(r => (r.tokens || 0) === 0).length;

    return {
      id,
      name: job.name || id,
      model: job.model || job.payload?.model || null,
      runs: totalRuns,
      totalTokens,
      totalCost,
      avgDurationSec: totalRuns > 0 ? totalDurationMs / totalRuns / 1000 : 0,
      tokensPerRun: totalRuns > 0 ? Math.round(totalTokens / totalRuns) : 0,
      costPerRun: totalRuns > 0 ? totalCost / totalRuns : 0,
      avgDailyCost: daily.length > 0 ? totalCost / daily.length : 0,
      today: (() => {
        const todayStr = new Date().toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
        const jsonlDay = byDay[todayStr] || { runs: 0, tokens: 0, cost: 0 };
        const ledger   = todayLedger[id]  || { tokens: 0, cost: 0 };
        return {
          runs:   jsonlDay.runs,
          tokens: jsonlDay.tokens || ledger.tokens,   // prefer JSONL; fallback to ledger
          cost:   jsonlDay.cost   || ledger.cost,
        };
      })(),
      daily,
      _review: { runsWithoutUsage, runsWithZeroTokens },
    };
  }).filter(j => j.runs > 0); // only jobs that have run at all

  // ── Per-model aggregation ─────────────────────────────────────────
  const byModel = new Map();
  for (const j of jobStats) {
    const model = j.model || 'unknown';
    if (!byModel.has(model)) {
      byModel.set(model, {
        model,
        runs: 0,
        totalTokens: 0,
        totalCost: 0,
        jobs: [],
      });
    }
    const m = byModel.get(model);
    m.runs += j.runs;
    m.totalTokens += j.totalTokens;
    m.totalCost += j.totalCost;
    m.jobs.push({
      id: j.id,
      name: j.name,
      runs: j.runs,
      totalTokens: j.totalTokens,
      totalCost: j.totalCost,
    });
  }
  const modelStats = Array.from(byModel.values()).sort((a, b) =>
    b.totalCost !== a.totalCost ? b.totalCost - a.totalCost : b.totalTokens - a.totalTokens
  );

  // ── Summary ───────────────────────────────────────────────────────
  const totalRuns = jobStats.reduce((s, j) => s + j.runs, 0);
  const totalCronCost = jobStats.reduce((s, j) => s + j.totalCost, 0);
  const totalCronTokens = jobStats.reduce((s, j) => s + j.totalTokens, 0);

  // Interactive (non-cron) cost from ledger
  const interactiveRows = sqliteJson(cfg.LEDGER_DB, `
    SELECT date(ts, 'localtime') as day,
      count(*) as calls,
      sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as tokens,
      round(sum(cost_total), 6) as cost
    FROM calls
    WHERE session_key NOT LIKE '%:cron:%'
      AND date(ts, 'localtime') >= date('now', 'localtime', '-${DAYS} days')
    GROUP BY day ORDER BY day
  `);

  // Cron cost from ledger per day (for daily trend, since JSONL has no cost)
  const cronLedgerRows = sqliteJson(cfg.LEDGER_DB, `
    SELECT date(ts, 'localtime') as day,
      count(*) as calls,
      sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as tokens,
      round(sum(cost_total), 6) as cost
    FROM calls
    WHERE session_key LIKE '%:cron:%'
      AND date(ts, 'localtime') >= date('now', 'localtime', '-${DAYS} days')
    GROUP BY day ORDER BY day
  `);

  const cronByDay = {};
  for (const r of cronLedgerRows) cronByDay[r.day] = r;

  const interByDay = {};
  for (const r of interactiveRows) interByDay[r.day] = r;

  // ── Daily trend ───────────────────────────────────────────────────
  // Build last N days
  const allDays = new Set([
    ...Object.keys(cronByDay),
    ...Object.keys(interByDay),
  ]);
  const dailyTrend = [...allDays].sort().map(day => {
    const cron = cronByDay[day] || {};
    const inter = interByDay[day] || {};
    const cronCost = Number(cron.cost || 0);
    const interCost = Number(inter.cost || 0);
    const totalCost = cronCost + interCost;
    // Simplified: cron = "fixed baseline", interactive = "variable"
    return {
      date: day,
      fixedBaselineCost: cronCost,      // cron jobs
      workloadVariableCost: 0,          // reserved
      interactiveCost: interCost,
      cronCost,
      interCost,
      totalCost,
      fixedCostSharePct: totalCost > 0 ? Math.round((cronCost / totalCost) * 100) : 0,
    };
  });

  const avgDailyCronCost = dailyTrend.length > 0
    ? dailyTrend.reduce((s, d) => s + d.cronCost, 0) / dailyTrend.length
    : 0;
  const avgDailyInterCost = dailyTrend.length > 0
    ? dailyTrend.reduce((s, d) => s + d.interCost, 0) / dailyTrend.length
    : 0;

  const todayStr = new Date().toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
  const todayCron = cronByDay[todayStr] || {};
  const todayInter = interByDay[todayStr] || {};

  // ── Review / data quality ─────────────────────────────────────────
  const totalRunsWithoutUsage = jobStats.reduce((s, j) => s + j._review.runsWithoutUsage, 0);
  const totalRunsWithZeroTokens = jobStats.reduce((s, j) => s + j._review.runsWithZeroTokens, 0);
  const daysWithCron = Object.keys(cronByDay).length;
  const daysWithInteractive = Object.keys(interByDay).length;
  const interactiveMsgsWithUsage = interactiveRows.reduce((s, r) => s + Number(r.calls || 0), 0);
  const notes = [];
  if (totalRunsWithZeroTokens > 0) notes.push(`${totalRunsWithZeroTokens} cron runs have 0 tokens — may be HEARTBEAT_OK / NO_REPLY only runs`);

  // Clean up internal review fields
  const cleanJobs = jobStats.map(({ _review, ...rest }) => rest);

  jsonReply(res, 200, {
    summary: {
      totalRuns,
      totalCronCost,
      totalCronTokens,
      avgDailyCronCost,
      avgDailyInterCost,
      avgFixedBaselineCost: avgDailyCronCost,
      avgWorkloadVariableCost: 0,
      avgInteractiveVariableCost: avgDailyInterCost,
      days: DAYS,
      today: {
        cronCost: Number(todayCron.cost || 0),
        cronTokens: Number(todayCron.tokens || 0),
        interactiveCost: Number(todayInter.cost || 0),
      },
    },
    jobs: cleanJobs,
    modelStats,
    dailyTrend,
    review: {
      cron: {
        finishedRuns: totalRuns,
        runsWithoutUsage: totalRunsWithoutUsage,
        runsWithZeroTokens: totalRunsWithZeroTokens,
      },
      interactive: {
        messagesWithUsage: interactiveMsgsWithUsage,
      },
      coverage: {
        daysWithCron,
        daysWithInteractive,
        interactiveCoveragePct: daysWithCron > 0
          ? Math.round((daysWithInteractive / daysWithCron) * 100) : 0,
      },
      notes,
    },
    // Legacy raw rows for any caller that still uses { rows }
    rows: [],
  });
}

function handleCronToday(_req, res) {
  const jobs = dedupeJobs(loadCronStore());
  const now = new Date();
  const todayStart = new Date(now.toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }));
  todayStart.setHours(0, 0, 0, 0);
  const todayStr = todayStart.toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });

  // Ledger fallback for remote cron run cost/token visibility in the overview panel.
  const ledgerByJob = {};
  try {
    const rows = sqliteJson(cfg.LEDGER_DB, `
      SELECT
        substr(session_key,
          instr(session_key,':cron:')+6,
          instr(session_key,':run:')-instr(session_key,':cron:')-6
        ) as job_id,
        round(sum(cost_total), 6) as cost_usd,
        sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
        max(ts) as last_ts
      FROM calls
      WHERE session_key LIKE '%:cron:%'
        AND date(ts,'localtime') = '${todayStr}'
      GROUP BY job_id
    `);
    for (const r of rows || []) {
      if (!r.job_id) continue;
      ledgerByJob[r.job_id] = {
        costUsd: Number(r.cost_usd || 0),
        tokens: Number(r.total_tokens || 0),
        lastTs: r.last_ts || null,
      };
    }
  } catch {}

  const todayJobs = jobs
    .filter(j => j.enabled !== false)
    .map(job => {
      const id = job.id || job.jobId;
      const lastRun = loadLastCronRun(id);
      const runTs = Date.parse(lastRun?.startedAt || lastRun?.finishedAt || '');
      const ranToday = Number.isFinite(runTs) && runTs >= todayStart.getTime();
      const ledger = ledgerByJob[id] || { costUsd: 0, tokens: 0, lastTs: null };
      return {
        id,
        name: job.name,
        model: job.payload?.model || null,
        last: lastRun ? {
          status: lastRun.status,
          startedAt: lastRun.startedAt,
          endedAt: lastRun.finishedAt,
          durationMs: lastRun.durationMs,
          model: lastRun.model || null,
          provider: lastRun.provider || null,
          tokens: Number(lastRun.tokens || 0) || ledger.tokens || 0,
          costUsd: Number(lastRun.costUsd || 0) || ledger.costUsd || 0,
        } : null,
        ranToday,
      };
    })
    .filter(j => j.ranToday);

  // Return with todayJobs key to match frontend expectation
  jsonReply(res, 200, { date: todayStart.toISOString().split('T')[0], todayJobs });
}

function register(router) {
  router.add('GET', '/api/cron',        (req, res) => handleCronList(req, res));
  router.add('GET', '/api/cron/runs',   (req, res, q) => handleCronRuns(req, res, q));
  router.add('GET', '/api/cron/costs',  (req, res) => handleCronCosts(req, res));
  router.add('GET', '/api/cron/today',  (req, res) => handleCronToday(req, res));

  // Legacy compat
  router.add('GET', '/ops/cron',        (req, res) => handleCronList(req, res));
  router.add('GET', '/ops/cron-costs',  (req, res) => handleCronCosts(req, res));
  router.add('GET', '/cron/today',      (req, res) => handleCronToday(req, res));
}

module.exports = { register };
