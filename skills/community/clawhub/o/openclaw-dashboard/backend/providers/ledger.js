'use strict';
/**
 * Ledger Provider — reads from ledger.db (SQLite).
 * Provides: today summary, history trends, per-channel breakdown, drift detection.
 */
const cfg = require('../lib/config');
const { sqliteJson } = require('../lib/sqlite-helper');
const { jsonReply } = require('../lib/http-helpers');
const gt = require('./ground-truth');

function getTodayPstDateString() {
  const now = new Date();
  const pst = new Date(now.toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }));
  const y = pst.getFullYear();
  const m = String(pst.getMonth() + 1).padStart(2, '0');
  const d = String(pst.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function handleToday(_req, res) {
  const todayDate = getTodayPstDateString();
  const rows = sqliteJson(cfg.LEDGER_DB, `
    SELECT provider, model, channel, chat_id,
      count(*) as calls,
      sum(input_tokens) as input_tokens,
      sum(output_tokens) as output_tokens,
      sum(cache_read_tokens) as cache_read_tokens,
      sum(cache_write_tokens) as cache_write_tokens,
      round(sum(cost_total), 6) as cost_total
    FROM calls
    WHERE date(ts, 'localtime') >= '${todayDate}'
    GROUP BY provider, model, channel, chat_id
    ORDER BY cost_total DESC
  `);

  // Enrich with channel names from Ground Truth
  const channelNames = gt.parse().channelNames;
  for (const r of rows) {
    r.channel_name = channelNames[r.chat_id] || r.channel || null;
  }

  // Compute totals
  let totalCost = 0, totalTokens = 0, totalCalls = 0;
  for (const r of rows) {
    totalCost += r.cost_total || 0;
    totalTokens += (r.input_tokens || 0) + (r.output_tokens || 0)
      + (r.cache_read_tokens || 0) + (r.cache_write_tokens || 0);
    totalCalls += r.calls || 0;
  }

  jsonReply(res, 200, {
    date: todayDate,
    total_cost: Math.round(totalCost * 10000) / 10000,
    total_tokens: totalTokens,
    total_calls: totalCalls,
    by_model: rows,
  });
}

function handleHistory(req, res, query) {
  const days = parseInt(query.days || '30', 10);
  const rows = sqliteJson(cfg.LEDGER_DB, `
    SELECT date(ts, 'localtime') as day, provider, model,
      count(*) as calls,
      sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
      sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as tokens,
      round(sum(cost_total), 6) as cost_total,
      round(sum(cost_total), 6) as cost,
      CASE WHEN lower(provider) LIKE '%local%' OR lower(provider) LIKE '%ollama%'
           OR lower(model) LIKE '%.gguf%' THEN 1 ELSE 0 END as is_local
    FROM calls
    WHERE date(ts, 'localtime') >= date('now', 'localtime', '-${days} days')
    GROUP BY day, provider, model
    ORDER BY day ASC, cost_total DESC
  `);

  // Aggregate summary per day: paid_cost, local_tokens, total_tokens
  const dayTotals = {};
  for (const r of rows) {
    const d = r.day;
    if (!dayTotals[d]) dayTotals[d] = { day: d, total_tokens: 0, local_tokens: 0, paid_tokens: 0, cost: 0 };
    dayTotals[d].total_tokens += r.total_tokens || 0;
    dayTotals[d].cost         += r.cost_total   || 0;
    if (r.is_local) dayTotals[d].local_tokens += r.total_tokens || 0;
    else            dayTotals[d].paid_tokens  += r.total_tokens || 0;
  }

  jsonReply(res, 200, { days, rows, daily_totals: Object.values(dayTotals).sort((a,b) => a.day < b.day ? -1 : 1) });
}

function handleByChannel(req, res, query) {
  const days = parseInt(query.days || '7', 10);
  const channelNames = gt.parse().channelNames;
  const rows = sqliteJson(cfg.LEDGER_DB, `
    SELECT chat_id, channel,
      count(*) as calls,
      sum(input_tokens + output_tokens) as total_tokens,
      round(sum(cost_total), 6) as cost_total
    FROM calls
    WHERE date(ts, 'localtime') >= date('now', 'localtime', '-${days} days') AND chat_id IS NOT NULL
    GROUP BY chat_id
    ORDER BY cost_total DESC
  `);
  for (const r of rows) {
    r.channel_name = channelNames[r.chat_id] || r.channel || null;
  }
  jsonReply(res, 200, { days, rows });
}

function handleDrift(req, res, query) {
  const days = parseInt(query.days || '30', 10);
  const provider = query.provider || 'anthropic';
  const rows = sqliteJson(cfg.LEDGER_DB, `
    SELECT date(ts, 'localtime') as day,
      sum(input_tokens) as ledger_input,
      sum(output_tokens) as ledger_output,
      round(sum(cost_total), 6) as ledger_cost
    FROM calls
    WHERE provider = '${provider}' AND date(ts, 'localtime') >= date('now', 'localtime', '-${days} days')
    GROUP BY day ORDER BY day
  `);
  jsonReply(res, 200, { provider, days, rows });
}

/**
 * Get token usage breakdown by source type: channel, thread, cron
 */
function handleBySource(req, res, query) {
  const days = parseInt(query.days || '7', 10);

  // Daily breakdown by source category
  const dailyRows = sqliteJson(cfg.LEDGER_DB, `
    WITH daily_calls AS (
      SELECT
        date(ts, 'localtime') as day,
        CASE
          WHEN source_kind = 'cron' OR session_key LIKE '%:cron:%' THEN 'cron'
          WHEN thread_id IS NOT NULL AND thread_id != '' THEN 'thread'
          ELSE 'channel'
        END as source_type,
        input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, cost_total
      FROM calls
      WHERE date(ts, 'localtime') >= date('now', 'localtime', '-${days} days')
    )
    SELECT
      day,
      source_type,
      count(*) as calls,
      sum(input_tokens) as input_tokens,
      sum(output_tokens) as output_tokens,
      sum(cache_read_tokens) as cache_read_tokens,
      sum(cache_write_tokens) as cache_write_tokens,
      sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
      round(sum(cost_total), 4) as cost_usd
    FROM daily_calls
    GROUP BY day, source_type
    ORDER BY day DESC, source_type
  `);

  // Summary totals
  const summaryRows = sqliteJson(cfg.LEDGER_DB, `
    SELECT
      CASE
        WHEN source_kind = 'cron' OR session_key LIKE '%:cron:%' THEN 'cron'
        WHEN thread_id IS NOT NULL AND thread_id != '' THEN 'thread'
        ELSE 'channel'
      END as source_type,
      count(*) as total_calls,
      sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
      round(sum(cost_total), 4) as total_cost
    FROM calls
    WHERE date(ts, 'localtime') >= date('now', 'localtime', '-${days} days')
    GROUP BY source_type
  `);

  // Cron job details
  const cronRows = sqliteJson(cfg.LEDGER_DB, `
    SELECT
      date(ts, 'localtime') as day,
      COALESCE(cron_job_id,
        CASE
          WHEN session_key LIKE 'agent:main:cron:%'
          THEN substr(session_key, 18, instr(substr(session_key, 18), ':') - 1)
          ELSE 'unknown'
        END
      ) as job_id,
      count(*) as calls,
      sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as total_tokens,
      round(sum(cost_total), 4) as cost_usd
    FROM calls
    WHERE (source_kind = 'cron' OR session_key LIKE '%:cron:%')
      AND date(ts, 'localtime') >= date('now', 'localtime', '-${days} days')
    GROUP BY day, job_id
    ORDER BY day DESC, cost_usd DESC
  `);

  // Group daily data by date
  const daily = {};
  for (const r of dailyRows) {
    if (!daily[r.day]) daily[r.day] = {};
    daily[r.day][r.source_type] = {
      calls: r.calls,
      input_tokens: r.input_tokens,
      output_tokens: r.output_tokens,
      cache_read_tokens: r.cache_read_tokens,
      cache_write_tokens: r.cache_write_tokens,
      total_tokens: r.total_tokens,
      cost_usd: r.cost_usd
    };
  }

  // Group cron details by date
  const cronDetails = {};
  for (const r of cronRows) {
    if (!cronDetails[r.day]) cronDetails[r.day] = [];
    cronDetails[r.day].push({
      job_id: r.job_id,
      calls: r.calls,
      total_tokens: r.total_tokens,
      cost_usd: r.cost_usd
    });
  }

  // Build summary object
  const summary = {};
  for (const r of summaryRows) {
    summary[r.source_type] = {
      calls: r.total_calls,
      tokens: r.total_tokens,
      cost: r.total_cost
    };
  }

  jsonReply(res, 200, { days, summary, daily, cron_details: cronDetails });
}

function register(router) {
  router.add('GET', '/api/ledger/today',      (req, res) => handleToday(req, res));
  router.add('GET', '/api/ledger/history',     (req, res, q) => handleHistory(req, res, q));
  router.add('GET', '/api/ledger/by-channel',  (req, res, q) => handleByChannel(req, res, q));
  router.add('GET', '/api/ledger/drift',       (req, res, q) => handleDrift(req, res, q));
  router.add('GET', '/api/ledger/by-source',   (req, res, q) => handleBySource(req, res, q));

  // Legacy compatibility routes (frontend cost.js may use /ops/ledger/* paths)
  router.add('GET', '/ops/ledger/today',   (req, res) => handleToday(req, res));
  router.add('GET', '/ops/ledger/history', (req, res, q) => handleHistory(req, res, q));
}

module.exports = { register };
