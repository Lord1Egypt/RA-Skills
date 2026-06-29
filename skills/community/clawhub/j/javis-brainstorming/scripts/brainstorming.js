#!/usr/bin/env node
/**
 * brainstorming — first consumer of the general "to-do card" surface (Layer 2 of
 * docs/superpowers/specs/2026-06-09-brainstorming-skill-design.md).
 *
 * AUTO-RUN by the javis-server session-dispatcher when a completed unit matches
 * the `brainstorm` route (no approve-to-run card — the human gate is the to-do
 * card's Confirm/Discard), OR run by the LLM on user-typed commands
 * ("brainstorm this" / "整理成簡報" / "帮我腦力激盪").
 *
 * It does NO brainstorming itself. It turns a brainstorm-worthy voice/keyboard
 * unit into a `type="todo"` card whose `prompt` hands off to Claude's
 * content-brainstorming skill (with javis_mcp pulling the source transcript).
 *
 * Two subcommands:
 *   fetch  GET recent session transcripts from javis-server and print them as JSON
 *          to stdout (same shape/approach as calendar-extractor). The agent reads
 *          this, decides whether there is a discernible goal, and COMPOSES a
 *          to-do card. With --session <id> / --kbd-input <id> the payload is
 *          filtered to a single unit (the auto-run dispatcher unit); with no
 *          flags it returns the whole time window (the manual ask).
 *   push   read a to-do-card JSON object on stdin, dedup it against per-user local
 *          state (the `seen` map, 30-day TTL), and write it to
 *          POST /api/skill/data type="todo" status="pending" (best-effort mirror),
 *          then deliver a markdown digest of the card via /api/agent/push (NON-FATAL
 *          — the summary line reports delivered / FAILED). The skill does NOT
 *          self-gate per unit — the server owns run-once (DispatchRouteExecuted).
 *          When the stdin JSON also carries the fetch payload's `sessions` (and
 *          `tz`), push stamps the item's OPTIONAL start_at/end_at journal window
 *          from the source session's started_at/ended_at — earliest session by
 *          started_at among the card's source_refs, serialized naive-local in tz
 *          (calendar-extractor convention). Missing/malformed times => omitted.
 *
 * Usage:
 *   node brainstorming.js <userId> fetch [--hours N] [--limit N]
 *   node brainstorming.js <userId> fetch --session <sessionId> [--hours N]
 *   node brainstorming.js <userId> fetch --kbd-input <inputId> [--hours N]
 *   node brainstorming.js <userId> push  < todo-card.json
 *   node brainstorming.js --help
 *
 * Env:
 *   OPENCLAW_GATEWAY_TOKEN  required for fetch/push — Bearer auth to javis-server
 *   JAVIS_SERVER_URL        optional — defaults to http://javis-server:8000
 *   TZ                      optional — IANA zone for the relative-date anchor
 *
 * Verified endpoints (javis-server):
 *   GET  /api/transcripts/recent  (get_gateway_user; params since, limit)
 *   GET  /api/transcripts/keyboard-input/<id>  (get_gateway_user; one keyboard row)
 *   POST /api/skill/data          (get_gateway_user; upsert by dedup_key; type=todo)
 *   POST /api/agent/push          (get_gateway_user; {skill, content, dedup_key})  — chat digest
 *                                  (dedup_key → server-derived per-card Agent Chat session)
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { resolveUserId, safeUserPath, readJson, writeJson } = require('./data');
const {
  resolveTz,
  localAnchor,
  sessionWindow,
  todoDedupKey,
  composePrompt,
  formatDigest,
  pruneSeen,
} = require('./lib');
const { buildTodoItem, postTodoCards } = require('./todo-card');

// Must equal the published clawhub slug: the server seeds the dispatch route only
// when metadata.routes[].skill == install slug, and the dispatcher then triggers
// /<slug>, so SKILL.md name + route.skill + this SLUG must all match the slug.
const SLUG = 'javis-brainstorming';
const ICON = '🧠';
const SERVER = process.env.JAVIS_SERVER_URL || 'http://javis-server:8000';

// argv is parsed lazily so `require()`-ing this module from a unit test is
// side-effect-free (no --help exit, no userId sanitize/exit on the test argv).
const SUBCOMMANDS = ['fetch', 'push'];
let userId, subcommand, rest;

function parseArgv() {
  if (process.argv.includes('--help')) {
    console.log([
      'Usage:',
      '  node brainstorming.js <userId> fetch [--hours N] [--limit N]',
      '  node brainstorming.js <userId> fetch --session <sessionId> [--hours N]',
      '  node brainstorming.js <userId> fetch --kbd-input <inputId> [--hours N]',
      '  node brainstorming.js <userId> push  < todo-card.json',
      '',
      'fetch  GET recent transcripts from javis-server -> JSON on stdout',
      '         --session/--kbd-input filter to one unit (the auto-run dispatcher unit)',
      'push   read a to-do-card JSON object on stdin -> dedup (seen) + write type=todo pending',
    ].join('\n'));
    process.exit(0);
  }

  const a2 = process.argv[2];
  if (SUBCOMMANDS.includes(a2)) {
    userId = resolveUserId(null);
    subcommand = a2;
    rest = process.argv.slice(3);
  } else {
    userId = resolveUserId(a2);
    subcommand = process.argv[3] || 'fetch';
    rest = process.argv.slice(4);
  }
}

function getFlag(name, dflt) {
  const i = rest.indexOf(`--${name}`);
  return i >= 0 && i + 1 < rest.length ? rest[i + 1] : dflt;
}

function requireToken() {
  const t = process.env.OPENCLAW_GATEWAY_TOKEN;
  if (!t) throw new Error('OPENCLAW_GATEWAY_TOKEN is required (injected inside the openclaw container).');
  return t;
}

function loadState() {
  const p = safeUserPath(userId);
  if (!fs.existsSync(p)) return { userId };
  try {
    return readJson(p);
  } catch (e) {
    console.error(`⚠️ state file unreadable, starting fresh: ${e.message}`);
    return { userId };
  }
}
function saveState(state) {
  writeJson(safeUserPath(userId), state);
}

// ---- fetch ---------------------------------------------------------------
function sessionSource(s) {
  return (s && (s.source || s.source_kind) || '').toString().trim().toLowerCase();
}
function sessionId(s) {
  return (s && (s.session_id || s.id) || '').toString().trim();
}

// `--session` (audio) keeps the one non-keyboard session whose session_id
// matches; `--kbd-input` (keyboard) resolves a single row via the dedicated
// server endpoint. With no filter the input is unchanged.
function filterToUnit(sessions, { sessionFilter }) {
  if (sessionFilter) {
    return sessions.filter((s) => sessionSource(s) !== 'keyboard' && sessionId(s) === sessionFilter);
  }
  return sessions;
}

// IO-injectable core so doFetch is unit-testable. `deps.httpGet(url, token)`
// returns the parsed JSON body (the default hits javis-server via fetch).
async function doFetch(opts = {}, deps = {}) {
  const token = opts.token || requireToken();
  const httpGet = deps.httpGet || defaultHttpGet;
  const nowIso = deps.now ? deps.now() : new Date().toISOString();

  const sessionFilter = 'sessionFilter' in opts ? opts.sessionFilter : getFlag('session', null);
  const kbdFilter = 'kbdFilter' in opts ? opts.kbdFilter : getFlag('kbd-input', null);
  const hours = 'hours' in opts ? opts.hours : (parseInt(getFlag('hours', '24'), 10) || 24);
  const limit = 'limit' in opts ? opts.limit : (parseInt(getFlag('limit', '50'), 10) || 50);

  const url = kbdFilter
    ? `${SERVER}/api/transcripts/keyboard-input/${encodeURIComponent(kbdFilter)}`
    : `${SERVER}/api/transcripts/recent?since=${encodeURIComponent(new Date(Date.now() - hours * 3600 * 1000).toISOString())}&limit=${limit}`;
  const data = await httpGet(url, token);

  const isEnvelope = data && typeof data === 'object' && !Array.isArray(data);
  let sessions = isEnvelope
    ? (Array.isArray(data.sessions) ? data.sessions : [])
    : (Array.isArray(data) ? data : []);

  if (!kbdFilter) sessions = filterToUnit(sessions, { sessionFilter });

  const base = isEnvelope ? data : {};
  const payloadTz = 'tz' in opts ? opts.tz : (deps.tz != null ? deps.tz : base.tz);
  const tz = resolveTz(payloadTz);

  // The relative-date anchor lets the agent resolve "today" coherently if the
  // goal references it; the sessions' started_at/ended_at are what `push` later
  // stamps as the card's optional start_at/end_at journal window.
  const out = { ...localAnchor(nowIso, tz), tz, ...base, sessions };
  if (deps.emit) deps.emit(out);
  else console.log(JSON.stringify(out, null, 2));
  return out;
}

async function defaultHttpGet(url, token) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error(`GET ${url.replace(SERVER, '')} -> HTTP ${res.status}`);
  return res.json();
}

// ---- push helpers --------------------------------------------------------
// Normalize the agent's stdin to-do card into the fields the contract needs.
// The agent supplies {title, goal, request[], key_points[]?, source_refs[],
// subtitle?, icon?, dedup_key?}. We compose the ready-to-paste prompt here so the
// agent never has to assemble the literal template by hand (the spec keeps the
// template fixed; only the bracketed fields vary).
function normalizeCard(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return null;
  const title = (raw.title || raw.name || '').toString().trim();
  if (!title) return null;
  const goal = (raw.goal || '').toString().trim();
  const subtitle = (raw.subtitle || '').toString().trim();
  const request = Array.isArray(raw.request)
    ? raw.request.map((r) => String(r).trim()).filter(Boolean)
    : [];
  const source_refs = Array.isArray(raw.source_refs)
    ? raw.source_refs.map((r) => String(r).trim()).filter(Boolean)
    : (raw.source_ref ? [String(raw.source_ref).trim()] : []);

  // The prompt is the only behavioral field. Prefer an agent-supplied prompt
  // (it may have richer phrasing); otherwise compose it from the template.
  const prompt = (raw.prompt && String(raw.prompt).trim())
    || composePrompt({ goal, request, source_refs });

  return {
    title,
    goal,
    subtitle: subtitle || defaultSubtitle(source_refs),
    request,
    source_refs,
    prompt,
    icon: (raw.icon && String(raw.icon).trim()) || ICON,
    dedupKey: (raw.dedup_key && String(raw.dedup_key).trim()) || todoDedupKey({ title, goal }),
    sourceRef: source_refs[0] || null,
  };
}

function defaultSubtitle(sourceRefs) {
  const n = sourceRefs.length;
  return n > 1 ? `Brainstorm · ${n} sessions` : 'Brainstorm';
}

// Read + parse the stdin push JSON: a single card object, or an envelope
// {card:{…}, sessions?:[…], tz?:"…"}. `sessions` (the fetch payload's
// sessions[], or at least the {session_id, started_at, ended_at} of the card's
// source_refs) and `tz` may ride either on the envelope or on the card itself;
// they feed the optional start_at/end_at stamping and are otherwise ignored.
async function readStdinPush() {
  let input = '';
  for await (const chunk of process.stdin) input += chunk;
  input = input.trim();
  if (!input) throw new Error('push expects a to-do-card JSON object on stdin (got empty input).');

  let parsed;
  try { parsed = JSON.parse(input); }
  catch (e) { throw new Error(`stdin is not valid JSON: ${e.message}`); }

  const raw = parsed && parsed.card && typeof parsed.card === 'object' ? parsed.card : parsed;
  const sessions = Array.isArray(parsed && parsed.sessions)
    ? parsed.sessions
    : (raw && Array.isArray(raw.sessions) ? raw.sessions : []);
  const tz = (parsed && parsed.tz) || (raw && raw.tz) || null;
  return { card: normalizeCard(raw), sessions, tz };
}

// Deliver the Agent Chat digest of a novel card: iOS renders the slug as a
// `[push:javis-brainstorming]` user bubble and the formatDigest(card) markdown
// (calendar-extractor style) as the Javis message.
//
// `dedup_key` is the card's stable key (the SAME value written to the type="todo"
// row). javis-server derives a deterministic per-card Agent Chat session from
// (user, skill, dedup_key), so each card's digest lands in — and re-tapping the
// card reopens — its OWN session instead of one rolling per-skill thread. The
// derivation is server-owned (single source of truth); the skill only forwards
// the key it already computed (see references/todo-card-contract.md §1f).
async function pushDigest(token, card) {
  const res = await fetch(`${SERVER}/api/agent/push`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ skill: SLUG, content: formatDigest(card), dedup_key: card.dedupKey }),
  });
  if (!res.ok) throw new Error(`POST /api/agent/push -> HTTP ${res.status}`);
}

// The server writes the push path performs, wrapped so tests can inject a
// recording mock instead of the real javis-server client.
const defaultPushClient = {
  write: (token, items) => postTodoCards({ skill: SLUG, items, token, server: SERVER }),
  digest: (token, card) => pushDigest(token, card),
};

// ---- push ----------------------------------------------------------------
// The skill does NOT self-gate per unit (the server owns run-once). push only
// dedups the card against the `seen` map so the same card is never written twice
// across overlapping manual windows or a re-run. A genuinely novel card is
// written type="todo" status="pending", then its Agent Chat digest is delivered.
async function doPush(deps = {}) {
  const client = deps.client || defaultPushClient;
  const load = deps.load || loadState;
  const save = deps.save || saveState;
  const token = deps.token || requireToken();
  const stdin = 'card' in deps ? null : await readStdinPush();
  const card = 'card' in deps ? deps.card : stdin.card;
  const sessions = 'sessions' in deps ? deps.sessions : (stdin ? stdin.sessions : []);
  const tz = resolveTz('tz' in deps ? deps.tz : (stdin ? stdin.tz : null));
  const digest = deps.digest !== undefined ? deps.digest : true;

  const state = load();
  const seen = pruneSeen(state.seen || {});
  const nowIso = deps.now ? deps.now() : new Date().toISOString();

  // No discernible goal/request in the transcript -> no card. Silence is a valid
  // detector outcome (the agent emits nothing / a card with no title).
  if (!card) {
    state.seen = seen;
    state.lastRunAt = nowIso;
    save(state);
    console.log('No brainstorm card to write (no discernible goal).');
    return;
  }

  if (seen[card.dedupKey]) {
    state.seen = seen;
    state.lastRunAt = nowIso;
    save(state);
    console.log('Brainstorm card already seen — nothing to write.');
    return;
  }

  // Build the validated type="todo" item (icon/title/prompt REQUIRED). The
  // OPTIONAL start_at/end_at journal window comes from the source session's
  // times (earliest session among source_refs, naive-local in tz); when the
  // session times are missing/malformed, sessionWindow returns {} and the
  // fields are omitted entirely — never invented.
  const { start_at, end_at } = sessionWindow(sessions, card.source_refs, tz);
  const item = buildTodoItem({
    dedupKey: card.dedupKey,
    sourceRef: card.sourceRef,
    startAt: start_at,
    endAt: end_at,
    payload: {
      icon: card.icon,
      title: card.title,
      subtitle: card.subtitle,
      prompt: card.prompt,
      source_refs: card.source_refs,
    },
  });

  try { await client.write(token, [item]); }
  catch (e) { console.error('⚠️ skill_data write failed (non-fatal):', e.message); }

  // The digest is a first-class step but stays NON-FATAL: a delivery failure
  // must never lose the pending card (already written above) nor fail the run.
  // Its outcome is reported explicitly in the summary line so a broken push
  // chain is diagnosable from the agent run log instead of silent.
  let digestNote = '';
  if (digest) {
    digestNote = ' Chat digest: delivered.';
    try { await client.digest(token, card); }
    catch (e) {
      console.error('⚠️ agent push digest failed (non-fatal):', e.message);
      digestNote = ` Chat digest FAILED: ${e.message}`;
    }
  }

  seen[card.dedupKey] = nowIso;
  state.seen = seen;
  state.lastRunAt = nowIso;
  save(state);
  console.log(`Wrote 1 brainstorm to-do card (${card.title}).${digestNote}`);
}

async function main() {
  parseArgv();
  if (subcommand === 'fetch') return doFetch();
  if (subcommand === 'push') return doPush();
  throw new Error(`Unknown subcommand '${subcommand}'. Use 'fetch' or 'push' (see --help).`);
}

module.exports = {
  doFetch,
  doPush,
  pushDigest,
  filterToUnit,
  sessionSource,
  sessionId,
  normalizeCard,
  defaultSubtitle,
};

if (require.main === module) {
  main().catch((err) => {
    console.error('❌', err.message);
    process.exit(1);
  });
}
