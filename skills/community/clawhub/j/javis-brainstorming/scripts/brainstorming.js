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
 *          flags it returns the whole time window (the manual ask). It also
 *          REMEMBERS each returned session's raw started_at/ended_at instants in
 *          per-user state (`sessionWindows`, same 30-day TTL as `seen`, capped at
 *          500 entries) so `push` can anchor the card without being re-handed them.
 *   push   read a to-do-card JSON object on stdin, dedup it against per-user local
 *          state (the `seen` map, 30-day TTL), and write it to
 *          POST /api/skill/data type="todo" status="pending" (best-effort mirror),
 *          then deliver a markdown digest of the card via /api/agent/push (NON-FATAL
 *          — the summary line reports delivered / FAILED). The skill does NOT
 *          self-gate per unit — the server owns run-once (DispatchRouteExecuted).
 *          push stamps the item's OPTIONAL start_at/end_at journal window from the
 *          source session's started_at/ended_at — earliest session by started_at
 *          among the card's source_refs, serialized naive-local in tz
 *          (calendar-extractor convention). The window is resolved from the UNION
 *          of the `sessionWindows` map `fetch` remembered and any `sessions` the
 *          stdin JSON carries (piped overrides remembered by session_id), so a
 *          bare card object still gets its day. Missing/malformed times => omitted;
 *          a date is NEVER invented.
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
  SEEN_TTL_DAYS,
  SESSION_WINDOWS_MAX,
  resolveTz,
  localAnchor,
  instantIso,
  sessionWindow,
  unionSessions,
  todoDedupKey,
  composePrompt,
  formatDigest,
  pruneByTtl,
  pruneSeen,
  capRecent,
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

// Persist the journal window of every session this fetch returned, so a later
// `push` can anchor the card even when the agent pipes only the card object
// (design 2026-09-11 §B: the anchor must not depend on an LLM re-piping an
// array the skill itself fetched).
//
//   state.sessionWindows = { "<session_id>": { started_at, ended_at?, seen_at } }
//
// Values are RAW ISO instants, never naive-local strings: tz is resolved per run
// and a window frozen in one tz would render wrong after the user's tz changes.
// `sessionWindow` converts to naive-local at the last moment, and instantIso
// normalizes the live wire's epoch seconds to ISO on the way in, so the map
// feeds it exactly the kind of value the envelope does.
//
// A session with no usable `started_at` carries no window and is not recorded;
// a session with no usable `ended_at` records its `started_at` alone (the key is
// simply absent — buildTodoItem then emits start_at without end_at).
//
// The map prunes with the SAME 30-day TTL as `seen` (pruneByTtl, keyed on
// seen_at), then keeps at most its SESSION_WINDOWS_MAX most recent entries. A
// fetch that returned zero sessions leaves the existing map in place — it is
// never cleared — and `seen` / `lastRunAt` are never touched here.
//
// It also records `state.tz` — but ONLY the tz the SERVER supplied on the fetch
// envelope. `push` falls back to it when the agent pipes no `tz`, which is the
// same defect the session map fixes: the agent had to re-pipe a value the skill
// already had. Recording a fallback-derived tz instead would be worse than
// recording nothing — the container runs with TZ unset, so `resolveTz` yields
// UTC, and persisting that would make every later card STICKILY wrong by the
// user's whole offset (verified on prod 2026-09-12: a bare-card push wrote
// 20:12 for a session that started 13:12 local).
function rememberSessionWindows(sessions, nowIso, { load, save }, serverTz) {
  const state = load();
  const tz = (serverTz == null ? '' : String(serverTz)).trim();
  if (tz) state.tz = tz;
  const kept = pruneByTtl(state.sessionWindows || {}, (w) => w && w.seen_at, SEEN_TTL_DAYS);
  for (const s of Array.isArray(sessions) ? sessions : []) {
    const id = sessionId(s);
    if (!id) continue;
    const started_at = instantIso(s.started_at);
    if (!started_at) continue;
    const window = { started_at };
    const ended_at = instantIso(s.ended_at);
    if (ended_at) window.ended_at = ended_at;
    window.seen_at = nowIso;
    kept[id] = window;
  }
  state.sessionWindows = capRecent(kept, (w) => w && w.seen_at, SESSION_WINDOWS_MAX);
  save(state);
}

// IO-injectable core so doFetch is unit-testable. `deps.httpGet(url, token)`
// returns the parsed JSON body (the default hits javis-server via fetch).
async function doFetch(opts = {}, deps = {}) {
  const token = opts.token || requireToken();
  const httpGet = deps.httpGet || defaultHttpGet;
  const load = deps.load || loadState;
  const save = deps.save || saveState;
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
  // Everything the server returned, BEFORE --session/--kbd-input narrows it.
  const fetched = isEnvelope
    ? (Array.isArray(data.sessions) ? data.sessions : [])
    : (Array.isArray(data) ? data : []);

  const sessions = kbdFilter ? fetched : filterToUnit(fetched, { sessionFilter });

  const base = isEnvelope ? data : {};
  const payloadTz = 'tz' in opts ? opts.tz : (deps.tz != null ? deps.tz : base.tz);
  const tz = resolveTz(payloadTz);

  // Remember EVERY session this fetch returned, not just the one --session
  // narrowed the envelope to. The window costs nothing to keep, and a card whose
  // source_refs cite a sibling session from the same fetch still gets its day.
  //
  // Remembering is NON-FATAL: an unwritable state file must never cost the agent
  // the envelope it is waiting on (the card then degrades to the piped-sessions
  // path, exactly as before this design).
  try { rememberSessionWindows(fetched, nowIso, { load, save }, payloadTz); }
  catch (e) { console.error('⚠️ session-window memory not updated (non-fatal):', e.message); }

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
// they feed the optional start_at/end_at stamping (layered over the
// `sessionWindows` map `fetch` remembered) and are otherwise ignored. Both are
// optional: a bare card object is anchored from the remembered map alone.
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

// push owns exactly TWO keys of the per-user state file: `seen` and `lastRunAt`.
// It re-reads the state immediately before writing and merges only those two
// into the fresh copy, instead of saving the whole-object snapshot it loaded at
// the top of the run. That snapshot is held across two awaited network
// round-trips (client.write, client.digest) and now carries `sessionWindows` —
// a key push does not own. A `fetch` that completes inside that window does its
// own load->save of `sessionWindows` (rememberSessionWindows), and saving the
// stale snapshot would revert it; the next bare-card push citing that session
// would then find NEITHER source and write the card undated — exactly the
// failure design 2026-09-11 §B exists to remove. Concurrently-added `seen`
// entries survive for the same reason: the fresh map is the base (TTL-pruned
// like any other read of it) and this run's keys are layered on top.
function commitPushState({ load, save, seen, nowIso }) {
  let fresh = {};
  try {
    const s = load();
    if (s && typeof s === 'object' && !Array.isArray(s)) fresh = s;
  } catch (e) {
    console.error('⚠️ state re-read before save failed, writing this run\'s keys only:', e.message);
  }
  fresh.seen = { ...pruneSeen(fresh.seen || {}), ...seen };
  fresh.lastRunAt = nowIso;
  save(fresh);
}

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
  const digest = deps.digest !== undefined ? deps.digest : true;

  const state = load();
  // tz precedence: piped -> the tz `fetch` remembered from the server -> TZ env
  // -> system zone. The remembered rung is why a BARE card is anchored in the
  // USER's zone: the container runs with TZ unset, so without it resolveTz lands
  // on UTC and toNaiveLocal writes the UTC wall-clock as if it were local — a
  // whole-offset error that moves an evening session to the next day, which is
  // the exact class of bug the journal window exists to prevent.
  const pipedTz = 'tz' in deps ? deps.tz : (stdin ? stdin.tz : null);
  const tz = resolveTz(pipedTz || state.tz);
  const seen = pruneSeen(state.seen || {});
  const nowIso = deps.now ? deps.now() : new Date().toISOString();

  // No discernible goal/request in the transcript -> no card. Silence is a valid
  // detector outcome (the agent emits nothing / a card with no title).
  if (!card) {
    commitPushState({ load, save, seen, nowIso });
    console.log('No brainstorm card to write (no discernible goal).');
    return;
  }

  if (seen[card.dedupKey]) {
    commitPushState({ load, save, seen, nowIso });
    console.log('Brainstorm card already seen — nothing to write.');
    return;
  }

  // Build the validated type="todo" item (icon/title/prompt REQUIRED). The
  // OPTIONAL start_at/end_at journal window comes from the source session's
  // times (earliest session among source_refs, naive-local in tz), resolved
  // over the UNION of both sources: the `sessionWindows` map `fetch` remembered
  // is the base, and any piped `sessions` are layered on top, overriding by
  // session_id (design 2026-09-11 §C). When BOTH sources miss the card's
  // source_refs, sessionWindow returns {} and the fields are omitted entirely —
  // there is deliberately no time-based last resort; a date is never invented.
  const known = unionSessions(state.sessionWindows || {}, sessions);
  const { start_at, end_at } = sessionWindow(known, card.source_refs, tz);
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

  // Re-read + merge (NOT save(state)): the snapshot loaded above predates two
  // network round-trips and must not carry a stale `sessionWindows` back to disk.
  seen[card.dedupKey] = nowIso;
  commitPushState({ load, save, seen, nowIso });
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
