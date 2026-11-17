#!/usr/bin/env node
/**
 * todo-spend-tracker — shared HTTP, auth, timezone and local-state helpers.
 *
 * Adapted from calendar-extractor/scripts/lib.js (toNaiveLocal, localAnchor) and
 * calendar-extractor/scripts/calendar-extractor.js (resolveTz, fetchServerTz,
 * defaultHttpGet, postSkillData) so this skill shares their timezone discipline:
 * the prod openclaw container has an EMPTY TZ (-> UTC), so "today" must come from
 * the user's zone (the /api/transcripts/recent envelope `tz`), never the container.
 *
 * Spec: javis.is/docs/superpowers/specs/2026-10-26-personal-state-ledger-design.md §1, §2.
 */
'use strict';

const SLUG = 'todo-spend-tracker';
const SERVER = process.env.JAVIS_SERVER_URL || 'http://javis-server:8000';

// ---- auth ----------------------------------------------------------------
function requireToken() {
  const t = process.env.OPENCLAW_GATEWAY_TOKEN;
  if (!t) throw new Error('OPENCLAW_GATEWAY_TOKEN is required (injected inside the openclaw container).');
  return t;
}

// ---- HTTP ----------------------------------------------------------------
// An HTTP error carries its status so callers can tell "not allowed to read"
// (401/403) from an outage.
class HttpError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function httpGet(url, token) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new HttpError(`GET ${url.replace(SERVER, '')} -> HTTP ${res.status}`, res.status);
  return res.json();
}

async function httpPostJson(url, token, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new HttpError(`POST ${url.replace(SERVER, '')} -> HTTP ${res.status}`, res.status);
  try { return await res.json(); } catch (_) { return null; }
}

// GET /api/skill/data?skill=todo-spend-tracker&type=<type>[&from=&to=] -> items[]
// Each returned item is tagged with `type` (the read response carries the type
// once per request, not per item) so the counting code sees one flat row list.
async function readSkillData(token, type, { from, to } = {}, deps = {}) {
  const get = deps.httpGet || httpGet;
  let url = `${SERVER}/api/skill/data?skill=${encodeURIComponent(SLUG)}&type=${encodeURIComponent(type)}`;
  if (from) url += `&from=${encodeURIComponent(from)}`;
  if (to) url += `&to=${encodeURIComponent(to)}`;
  const data = await get(url, token);
  const items = data && Array.isArray(data.items) ? data.items : [];
  return items.map((it) => ({ ...it, type }));
}

// POST /api/skill/data upsert for one ledger type.
async function writeSkillData(token, type, items, deps = {}) {
  const post = deps.httpPostJson || httpPostJson;
  return post(`${SERVER}/api/skill/data`, token, { skill: SLUG, type, merge: 'upsert', items });
}

// ---- timezone ------------------------------------------------------------
// Order: explicit -> TZ env -> system zone -> UTC.
function resolveTz(explicitTz) {
  if (explicitTz && typeof explicitTz === 'string' && explicitTz.trim()) return explicitTz.trim();
  if (process.env.TZ && process.env.TZ.trim()) return process.env.TZ.trim();
  try {
    const z = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (z) return z;
  } catch (_) { /* fall through */ }
  return 'UTC';
}

// The user's zone rides on the /api/transcripts/recent envelope (gateway-token
// readable). Best-effort: any failure returns null and the caller falls back.
async function fetchServerTz(token, deps = {}) {
  try {
    const get = deps.httpGet || httpGet;
    const since = encodeURIComponent(new Date(Date.now() - 3600 * 1000).toISOString());
    const data = await get(`${SERVER}/api/transcripts/recent?since=${since}&limit=1`, token);
    const tz = data && data.tz;
    return tz && String(tz).trim() ? String(tz).trim() : null;
  } catch (_) {
    return null;
  }
}

// explicit -> server (authoritative) -> TZ env -> system.
async function resolveUserTz({ explicitTz, token, deps = {} } = {}) {
  if (explicitTz && String(explicitTz).trim()) return String(explicitTz).trim();
  if (deps.fetchTz) {
    const t = await deps.fetchTz();
    if (t) return String(t).trim();
  } else if (token) {
    const t = await fetchServerTz(token, deps);
    if (t) return t;
  }
  return resolveTz(null);
}

// Wall-clock of instant `iso` in `tz`, zoneless: "YYYY-MM-DDTHH:MM:SS".
function toNaiveLocal(iso, tz) {
  if (!iso) return null;
  const d = new Date(iso);
  if (isNaN(d.getTime())) return null;
  const p = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz, hour12: false,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  }).formatToParts(d).reduce((o, x) => ((o[x.type] = x.value), o), {});
  let { year, month, day, hour } = p;
  // Some ICU builds emit "24" at midnight meaning the start of the next day.
  if (hour === '24') {
    hour = '00';
    const next = new Date(Date.UTC(+year, +month - 1, +day) + 86400000);
    year = String(next.getUTCFullYear()).padStart(4, '0');
    month = String(next.getUTCMonth() + 1).padStart(2, '0');
    day = String(next.getUTCDate()).padStart(2, '0');
  }
  return `${year}-${month}-${day}T${hour}:${p.minute}:${p.second}`;
}

// The relative-date anchor for the agent: local "now", local date and weekday.
function localAnchor(iso, tz) {
  const local = toNaiveLocal(iso, tz);
  const d = new Date(iso);
  const weekday = isNaN(d.getTime())
    ? null
    : new Intl.DateTimeFormat('en-US', { timeZone: tz, weekday: 'long' }).format(d);
  return {
    reference_time: local,
    reference_date: local ? local.slice(0, 10) : null,
    reference_weekday: weekday,
    reference_time_utc: iso,
  };
}

module.exports = {
  SLUG,
  SERVER,
  HttpError,
  requireToken,
  httpGet,
  httpPostJson,
  readSkillData,
  writeSkillData,
  resolveTz,
  fetchServerTz,
  resolveUserTz,
  toNaiveLocal,
  localAnchor,
};
