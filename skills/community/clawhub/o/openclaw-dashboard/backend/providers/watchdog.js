'use strict';
/**
 * Watchdog Provider — gateway watchdog timeline + status.
 * Reads: ~/.openclaw/watchdogs/gateway-discord/state.json (plaintext)
 *        ~/.openclaw/watchdogs/gateway-discord/events.jsonl (JSON lines with `time` field)
 */
const fs   = require('fs');
const path = require('path');
const cfg  = require('../lib/config');
const { jsonReply } = require('../lib/http-helpers');

const WATCHDOG_STATE_FILE  = path.join(cfg.WATCHDOG_DIR, 'state.json');
const WATCHDOG_EVENTS_FILE = path.join(cfg.WATCHDOG_DIR, 'events.jsonl');

// state.json is plaintext: "healthy 0 1772864074 0 0"
// Fields: status consecutive_failures last_check_ts total_alerts total_recoveries
function readState() {
  try {
    const raw = fs.readFileSync(WATCHDOG_STATE_FILE, 'utf8').trim();
    // Try JSON first
    try { return JSON.parse(raw); } catch {}
    // Parse plaintext format
    const parts = raw.split(/\s+/);
    if (parts.length >= 1) {
      return {
        status:               parts[0] || 'unknown',
        consecutive_failures: parseInt(parts[1] || '0', 10),
        last_check_ts:        parseInt(parts[2] || '0', 10),
        total_alerts:         parseInt(parts[3] || '0', 10),
        total_recoveries:     parseInt(parts[4] || '0', 10),
      };
    }
    return null;
  } catch {
    return null;
  }
}

// events.jsonl lines: { "time": "ISO", "event": "...", ... }
function readEvents(limit = 500) {
  try {
    const raw = fs.readFileSync(WATCHDOG_EVENTS_FILE, 'utf8');
    const lines = raw.trim().split('\n').filter(Boolean);
    const events = [];
    const start = Math.max(0, lines.length - limit);
    for (let i = start; i < lines.length; i++) {
      try { events.push(JSON.parse(lines[i])); } catch {}
    }
    return events;
  } catch {
    return [];
  }
}

// Map event type to a runtime status string
function eventToRuntimeStatus(ev) {
  const event  = String(ev?.event  || '').toLowerCase();
  const reason = String(ev?.reason || '').toLowerCase();
  const sev    = String(ev?.severity || '').toLowerCase();
  if (event === 'recovered' || event === 'silent_recovery' || reason === 'recovered') return 'healthy';
  if (sev === 'critical' || event === 'alert' || event === 'suppressed' || event === 'check_failed' || reason.includes('runtime_stopped')) return 'down';
  return null;
}

// Build uptime timeline. Points use ISO ts strings (frontend Date.parse-able).
function buildTimeline(eventsAsc, startMs, endMs, stepMs, initialStatus) {
  const points = [];
  let idx    = 0;
  let status = initialStatus;
  for (let t = startMs; t <= endMs; t += stepMs) {
    while (idx < eventsAsc.length) {
      const ts = Date.parse(eventsAsc[idx]?.time || '');
      if (!Number.isFinite(ts) || ts > t) break;
      const mapped = eventToRuntimeStatus(eventsAsc[idx]);
      if (mapped) status = mapped;
      idx++;
    }
    points.push({ ts: new Date(t).toISOString(), status });
  }
  return points;
}

function handleWatchdog(req, res, query) {
  const reqLimit  = parseInt(query.limit         || '200', 10);
  const reqWindow = parseInt(query.windowMinutes || '1440', 10);
  const limit         = Number.isFinite(reqLimit)  ? Math.min(Math.max(reqLimit, 1), 500)    : 200;
  const windowMinutes = Number.isFinite(reqWindow) ? Math.min(Math.max(reqWindow, 5), 10080) : 1440;
  const criticalOnly  = String(query.criticalOnly || '0') === '1';

  const state  = readState();
  const allRaw = readEvents(1000);

  // Normalise: events must have a parseable .time field
  const allEvents = allRaw
    .map(ev => ({ ...ev, _ts: Date.parse(ev?.time || '') }))
    .filter(ev => Number.isFinite(ev._ts))
    .sort((a, b) => a._ts - b._ts);

  const now     = Date.now();
  const startMs = now - windowMinutes * 60 * 1000;

  const inWindow = allEvents.filter(ev => ev._ts >= startMs);

  // Determine initial status from the last event *before* our window
  const watchdogStatus = String(state?.status || 'unknown');
  let initialStatus    = watchdogStatus === 'healthy' ? 'healthy' : 'unknown';
  for (let i = allEvents.length - 1; i >= 0; i--) {
    if (allEvents[i]._ts < startMs) {
      const mapped = eventToRuntimeStatus(allEvents[i]);
      if (mapped) { initialStatus = mapped; break; }
    }
  }

  const stepSeconds = 30;
  const points = buildTimeline(allEvents, startMs, now, stepSeconds * 1000, initialStatus);
  const downCount    = points.filter(p => p.status === 'down').length;
  const healthyCount = points.filter(p => p.status === 'healthy').length;

  // Events for the list (strip internal _ts)
  const eventsForList = (criticalOnly
    ? inWindow.filter(ev => String(ev.severity || '').toLowerCase() === 'critical')
    : inWindow
  ).slice(-limit).reverse().map(({ _ts, ...ev }) => ev);

  // Derive effective status
  // Avoid process inspection through shell in hardened mode.
  const rt = { running: null, pid: null };
  const effectiveStatus = watchdogStatus === 'healthy' ? 'healthy' : 'degraded';

  jsonReply(res, 200, {
    effectiveStatus,
    watchdog: state,
    runtime: {
      running: rt.running,
      pid: rt.pid,
      checkedAt: new Date().toISOString(),
    },
    recentEvents: eventsForList,
    timeline: {
      windowMinutes,
      stepSeconds,
      points,
      downCount,
      healthyCount,
      filteredListCriticalOnly: criticalOnly,
    },
    files: {
      stateAvailable: Boolean(WATCHDOG_STATE_FILE),
      eventsAvailable: Boolean(WATCHDOG_EVENTS_FILE),
    },
  });
}

function handleHealthSummary(_req, res) {
  const state = readState();
  const events = readEvents(100);
  const status = String(state?.status || 'unknown');
  const lastEvent = events.length ? events[events.length - 1] : null;
  jsonReply(res, 200, {
    ok: true,
    effectiveStatus: status === 'healthy' ? 'healthy' : 'degraded',
    watchdog: {
      status,
      consecutiveFailures: Number(state?.consecutive_failures || 0),
      totalAlerts: Number(state?.total_alerts || 0),
      totalRecoveries: Number(state?.total_recoveries || 0),
      lastCheckTs: Number(state?.last_check_ts || 0),
    },
    lastEvent: lastEvent || null,
    runtime: {
      running: null,
      pid: null,
      checkedAt: new Date().toISOString(),
    },
  });
}

function register(router) {
  // Frontend calls /ops/watchdog?limit=200&windowMinutes=1440
  router.add('GET', '/ops/watchdog', (req, res, q) => handleWatchdog(req, res, q));
  // Keep /api/watchdog as alias
  router.add('GET', '/api/watchdog',  (req, res, q) => handleWatchdog(req, res, q));
  router.add('GET', '/ops/health/summary', (req, res) => handleHealthSummary(req, res));
  router.add('GET', '/api/health/summary', (req, res) => handleHealthSummary(req, res));
}

module.exports = { register, readState, readEvents };
