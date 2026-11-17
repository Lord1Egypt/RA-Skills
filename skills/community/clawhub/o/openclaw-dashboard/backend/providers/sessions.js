'use strict';
/**
 * Sessions Provider — active sessions + sub-agents.
 * Reads: sessions.json, subagents/runs.json
 * Enriches with Ground Truth channel names.
 */
const fs = require('fs');
const cfg = require('../lib/config');
const { jsonReply } = require('../lib/http-helpers');
const { sqliteJson } = require('../lib/sqlite-helper');
const gt = require('./ground-truth');

function loadCronNameMap() {
  try {
    const raw = JSON.parse(fs.readFileSync(cfg.CRON_STORE_PATH, 'utf8'));
    const jobs = Array.isArray(raw) ? raw : (raw.jobs || []);
    const map = new Map();
    for (const j of jobs) {
      const id = String(j.id || j.jobId || '');
      if (!id) continue;
      map.set(id, j.name || id);
    }
    return map;
  } catch {
    return new Map();
  }
}

function isRunSession(key) {
  // Skip run-specific sessions (they are children of base sessions)
  return /:run:[a-f0-9-]{8,36}/i.test(String(key));
}

function prettifySessionName(entry, key, chatId, channelNames, cronNameMap) {
  const rawDisplay = String(entry?.displayName || '').trim();
  const groupChannel = String(entry?.groupChannel || '').trim();
  const groupSubject = String(entry?.groupSubject || '').trim();

  // Cron sessions: resolve job id to human-friendly cron name
  const cronMatch = String(key).match(/:cron:([a-f0-9-]{8,36})/i);
  if (cronMatch) {
    const cronId = cronMatch[1];
    const cronName = cronNameMap.get(cronId) || cronId;
    return `Cron · ${cronName}`;
  }

  // Prefer thread/channel names captured by OpenClaw session metadata
  if (rawDisplay && !/^discord:g-/i.test(rawDisplay)) return rawDisplay;
  if (groupChannel) return groupChannel;
  if (groupSubject) return groupSubject;

  // Fall back to static channel mapping, then readable id
  if (chatId && channelNames[chatId]) return channelNames[chatId];
  if (chatId) return `#${chatId}`;

  return rawDisplay || key;
}

function readSessions() {
  try {
    return JSON.parse(fs.readFileSync(cfg.SESSIONS_FILE, 'utf8'));
  } catch {
    return {};
  }
}

function readSubagentRuns() {
  try {
    return JSON.parse(fs.readFileSync(cfg.SUBAGENT_RUNS_FILE, 'utf8'));
  } catch {
    return [];
  }
}

function handleSessions(req, res, query) {
  const hideStale = String((query || {}).hideStale || '0') === '1';
  const raw = readSessions();
  const channelNames = gt.parse().channelNames;
  const cronNameMap = loadCronNameMap();

  // Get today's date in PST
  const now = new Date();
  const pst = new Date(now.toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }));
  const todayDate = `${pst.getFullYear()}-${String(pst.getMonth()+1).padStart(2,'0')}-${String(pst.getDate()).padStart(2,'0')}`;

  // Fetch today's per-session stats from ledger
  let ledgerIndex = { bySessionKey: new Map(), byChat: new Map() };
  try {
    const rows = sqliteJson(cfg.LEDGER_DB, `
      SELECT session_key, chat_id, channel, model,
        count(*) as messages,
        sum(input_tokens) as input_tokens,
        sum(output_tokens) as output_tokens,
        sum(cache_read_tokens + cache_write_tokens) as cache_tokens,
        sum(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as totalTokens,
        round(sum(cost_total), 6) as cost
      FROM calls WHERE date(ts, 'localtime') >= '${todayDate}'
      GROUP BY session_key, chat_id, channel
    `);
    ledgerIndex = buildLedgerIndex(rows);
  } catch {}

  const sessions = [];
  for (const [key, entry] of Object.entries(raw)) {
    // Skip run-specific sessions (children of base sessions) to avoid duplicates
    if (isRunSession(key)) continue;

    const origin = entry.origin || {};
    const chatId = extractChatId(key, origin);
    const channel = origin.provider || origin.surface || 'unknown';
    const displayName = prettifySessionName(entry, key, chatId, channelNames, cronNameMap);
    const daysSinceUpdate = entry.updatedAt ? ((Date.now() - entry.updatedAt) / 86400000) : 99;

    // Match ledger stats by canonical identity: exact session key first, then discord chat id, then sessionId fallback
    const ledger = resolveLedgerStats(ledgerIndex, key, entry.sessionId, chatId, channel);

    const todayCost = ledger?.cost || 0;
    const todayTokens = ledger?.totalTokens || 0;
    const todayMessages = ledger?.messages || 0;

    const isCron = /^Cron · /.test(displayName) || /:cron:/i.test(key);
    const isHeartbeat = key === 'agent:main:main' || channel === 'heartbeat';
    const looksPseudoChannel = !!chatId && (!displayName || displayName === `#${chatId}` || /^discord:\d+#/i.test(displayName) || /^#\d{6,}$/.test(displayName));
    const isInteractiveChannel = !isCron && !isHeartbeat && channel === 'discord' && !!chatId && !looksPseudoChannel;
    const rowKind = isCron ? 'cron' : isHeartbeat ? 'system' : isInteractiveChannel ? 'channel' : looksPseudoChannel ? 'other' : 'other';
    const fitEligible = rowKind === 'channel';

    sessions.push({
      key,
      sessionId: entry.sessionId,
      chatType: entry.chatType || 'unknown',
      channel,
      chatId,
      channelId: chatId,
      channelName: chatId ? (channelNames[chatId] || null) : null,
      displayName,
      rowKind,
      fitEligible,
      model: entry.model || 'unknown',
      thinkingLevel: entry.thinkingLevel || '—',
      status: todayMessages > 0 ? 'active' : (daysSinceUpdate < 1 ? 'idle' : 'stale'),
      updatedAt: entry.updatedAt,
      daysSinceUpdate: daysSinceUpdate.toFixed(1),
      allTime: { tokens: entry.totalTokens || 0 },
      today: {
        messages: todayMessages,
        totalTokens: todayTokens,
        cost: todayCost,
        effectiveMessages: fitEligible ? todayMessages : 0,
        noReplyRate: 0,
        topModels: ledger ? [{ model: ledger.model, tokens: todayTokens }] : [],
        models: {},
      },
      recentTopics: [],
      lastTo: entry.lastTo,
    });
  }

  // Sort: active first, then by today cost
  const statusOrder = { error: 0, active: 1, idle: 2, stale: 3 };
  sessions.sort((a, b) => (statusOrder[a.status] || 9) - (statusOrder[b.status] || 9) || b.today.cost - a.today.cost);

  // Apply hideStale filter (7+ days no activity)
  const visibleSessions = hideStale
    ? sessions.filter(s => parseFloat(s.daysSinceUpdate) < 7)
    : sessions;

  // Build summary
  const active = visibleSessions.filter(s => s.status === 'active').length;
  const todayCostTotal = visibleSessions.reduce((s, r) => s + r.today.cost, 0);
  const todayMsgTotal = visibleSessions.reduce((s, r) => s + r.today.messages, 0);

  jsonReply(res, 200, {
    sessions: visibleSessions,
    alerts: [],
    summary: {
      total: visibleSessions.length,
      active,
      errors: 0,
      todayCost: todayCostTotal,
      todayMessages: todayMsgTotal,
      topModel: '—',
    },
    cachedAt: Date.now(),
  });
}

function findLedgerStatsBySessionId(todayStats, sessionId) {
  if (!sessionId) return null;
  for (const [k, v] of Object.entries(todayStats)) {
    if (k.includes(sessionId)) return v;
  }
  return null;
}

function buildLedgerIndex(rows) {
  const bySessionKey = new Map();
  const byChat = new Map();
  for (const r of rows || []) {
    const key = String(r.session_key || '');
    const chatId = String(r.chat_id || '');
    if (key) bySessionKey.set(key, r);
    if (chatId) {
      const prev = byChat.get(chatId) || {
        session_key: null,
        chat_id: chatId,
        channel: r.channel || null,
        model: r.model || null,
        messages: 0,
        input_tokens: 0,
        output_tokens: 0,
        cache_tokens: 0,
        totalTokens: 0,
        cost: 0,
      };
      prev.messages += Number(r.messages || 0);
      prev.input_tokens += Number(r.input_tokens || 0);
      prev.output_tokens += Number(r.output_tokens || 0);
      prev.cache_tokens += Number(r.cache_tokens || 0);
      prev.totalTokens += Number(r.totalTokens || 0);
      prev.cost += Number(r.cost || 0);
      if (!prev.model && r.model) prev.model = r.model;
      byChat.set(chatId, prev);
    }
  }
  return { bySessionKey, byChat };
}

function resolveLedgerStats(index, key, sessionId, chatId, channel) {
  if (key && index.bySessionKey.has(key)) return index.bySessionKey.get(key);
  if (chatId && channel === 'discord' && index.byChat.has(String(chatId))) return index.byChat.get(String(chatId));
  return findLedgerStatsBySessionId(Object.fromEntries(index.bySessionKey), sessionId);
}

function handleSubagents(_req, res) {
  const runs = readSubagentRuns();
  jsonReply(res, 200, { count: runs.length, runs });
}

function extractChatId(sessionKey, origin) {
  // Discord: "agent:main:discord:channel:1234567890"
  const m = sessionKey.match(/discord:channel:(\d+)/);
  if (m) return m[1];
  // Broader fallback: any channel:<id> in session key
  const mKey = sessionKey.match(/channel:(\d{6,})/);
  if (mKey) return mKey[1];
  // From origin.to: "channel:1234567890"
  const to = origin.to || '';
  const m2 = to.match(/channel:(\d{6,})/);
  if (m2) return m2[1];
  return null;
}

function normalizeDisplayChannelName(name) {
  let s = String(name || '').trim();
  if (!s) return '';
  if (/^discord:g-/i.test(s)) return '';
  s = s.replace(/^Discord thread\s+/i, '');
  s = s.replace(/^#?([^›]+)›\s*.*$/, '$1').trim();
  s = s.replace(/\s+—\s+.*$/, '');
  s = s.replace(/\s+\(.+\)$/, '');
  s = s.replace(/\s+Channel\s+Config$/i, '');
  s = s.replace(/\s+Gardening\s+Log$/i, '');
  s = s.replace(/\s+Log$/i, '');
  s = s.trim();
  if (!s) return '';
  if (!s.startsWith('#') && !/^discord:/i.test(s)) s = `#${s.replace(/^#+/, '')}`;
  if (/^#\d{6,}$/.test(s)) return '';
  return s;
}

function extractThreadName(displayName, groupSubject) {
  const d = String(displayName || '').trim();
  if (/^Discord thread /i.test(d)) {
    const m = d.match(/^Discord thread\s+([^›]+?)\s+›\s+(.+)$/i);
    if (m && m[2]) return m[2].trim();
  }
  const gs = String(groupSubject || '').trim();
  return gs || null;
}

function extractParentChannelName(displayName) {
  const d = String(displayName || '').trim();
  if (/^Discord thread /i.test(d)) {
    const m = d.match(/^Discord thread\s+([^›]+?)\s+›\s+(.+)$/i);
    if (m && m[1]) return normalizeDisplayChannelName(m[1]);
  }
  return null;
}

function handleDiscordSurfaces(_req, res) {
  const gtData = gt.parse();
  const channelNames = gtData.channelNames;
  const rawSessions = readSessions();

  // Build a light metadata index from live OpenClaw sessions so we can surface
  // human-friendly Discord channel/thread labels even when Ground Truth is incomplete.
  const sessionMetaByChat = new Map();
  for (const [key, entry] of Object.entries(rawSessions || {})) {
    const origin = entry.origin || {};
    const channel = entry.channel || origin.provider || origin.surface || 'unknown';
    const chatId = extractChatId(key, origin);
    if (!chatId || channel !== 'discord') continue;
    const displayName = String(entry.displayName || '').trim();
    const groupChannel = String(entry.groupChannel || '').trim();
    const groupSubject = String(entry.groupSubject || '').trim();
    const threadId = String(origin.threadId || entry.lastThreadId || '').trim() || null;
    const prev = sessionMetaByChat.get(chatId) || { displayName: '', groupChannel: '', groupSubject: '', threadId: null };

    // Prefer richer human-readable metadata over generic discord:g-* placeholders.
    const pickBetter = (a, b) => {
      const score = (v) => {
        const s = String(v || '').trim();
        if (!s) return 0;
        if (/^discord:g-/i.test(s)) return 1;
        if (/^#\d{6,}$/.test(s)) return 1;
        if (/^discord:\d+#/i.test(s)) return 2;
        if (/^Discord thread /i.test(s)) return 5;
        if (s.startsWith('#')) return 4;
        return 3;
      };
      return score(b) > score(a) ? b : a;
    };

    sessionMetaByChat.set(chatId, {
      displayName: pickBetter(prev.displayName, displayName),
      groupChannel: pickBetter(prev.groupChannel, groupChannel),
      groupSubject: pickBetter(prev.groupSubject, groupSubject),
      threadId: prev.threadId || threadId,
    });
  }

  let rows = [];
  try {
    const channelRows = sqliteJson(cfg.LEDGER_DB, `
      SELECT
        chat_id as channelId,
        COUNT(*) as calls,
        SUM(input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) as totalTokens,
        ROUND(SUM(cost_total), 6) as costUsd,
        MAX(model) as topModel,
        MAX(ts) as lastTs
      FROM calls
      WHERE date(ts, 'localtime') >= date('now', 'localtime')
        AND channel = 'discord'
        AND chat_id IS NOT NULL
        AND chat_id != ''
      GROUP BY chat_id
      ORDER BY costUsd DESC
    `);

    const baseRows = channelRows.map(r => {
      const meta = sessionMetaByChat.get(String(r.channelId)) || {};
      const derivedThreadName = extractThreadName(meta.displayName, meta.groupSubject);
      const parentChannelName = extractParentChannelName(meta.displayName);
      const channelName = normalizeDisplayChannelName(meta.groupChannel)
        || normalizeDisplayChannelName(gt.getChannelName(String(r.channelId)))
        || parentChannelName
        || normalizeDisplayChannelName(meta.displayName)
        || `#${r.channelId}`;
      return {
        surfaceType: 'channel',
        channelId: r.channelId,
        channelName,
        threadId: meta.threadId || null,
        threadName: derivedThreadName,
        parentChannelName,
        calls: Number(r.calls || 0),
        totalTokens: Number(r.totalTokens || 0),
        costUsd: Number(r.costUsd || 0),
        topModel: r.topModel || null,
        lastTs: r.lastTs || null,
      };
    });

    rows = baseRows
      .map(r => ({
        ...r,
        surfaceType: r.threadId && r.threadName ? 'thread-surface' : 'channel-surface',
      }))
      .sort((a, b) => Number(b.costUsd || 0) - Number(a.costUsd || 0));
  } catch (e) {
    return jsonReply(res, 500, { ok: false, error: e.message, rows: [] });
  }

  const summary = rows.reduce((acc, r) => {
    acc.calls += r.calls;
    acc.totalTokens += r.totalTokens;
    acc.costUsd += r.costUsd;
    return acc;
  }, { calls: 0, totalTokens: 0, costUsd: 0 });

  jsonReply(res, 200, { ok: true, rows, summary, cachedAt: Date.now() });
}

function register(router) {
  router.add('GET', '/api/sessions',   (req, res, q) => handleSessions(req, res, q));
  router.add('GET', '/api/subagents',  (req, res) => handleSubagents(req, res));
  router.add('GET', '/api/discord-surfaces', (req, res) => handleDiscordSurfaces(req, res));
  // Legacy compat
  router.add('GET', '/ops/sessions',   (req, res, q) => handleSessions(req, res, q));
  router.add('GET', '/ops/discord-surfaces', (req, res) => handleDiscordSurfaces(req, res));
}

module.exports = { register, readSessions };
