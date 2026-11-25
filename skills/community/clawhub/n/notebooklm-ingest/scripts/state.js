'use strict';
/**
 * Three state files, all under `notebooklm-ingest/data/`.
 *
 * Spec: javis.is/docs/superpowers/specs/2026-10-29-notebooklm-connector-design.md
 *       R6 (history), R10 (observable state), R12 (the host field), R20.
 *
 *   prefs.json      the user's choices: notebooks, schedule, timezone, profile,
 *                   and the bridge HOST (R12)
 *   ingests.json    the ingest ledger (R6): one row per ingest, newest first
 *   last-run.json   the run state a digest renders from (R10, R20)
 *
 * **Paths resolve against `__dirname`, not cwd**, following gmail-wiki-ingest's
 * STATE_PATH docblock and calendar-extractor's `scripts/data.js`: a cron turn's
 * working directory is not the bundle, so a relative path would write the state
 * wherever openclaw happened to be standing and read nothing back next run.
 *
 * **Every write is tmp-then-rename.** `rename(2)` is atomic within a
 * filesystem, so a container reaped mid-write (these containers are reaped ~10
 * minutes after the user's last activity) can never leave a file that parses
 * into half a run. Absent and corrupt are the same condition to every caller:
 * there is no state behind this file. Telling them apart would only let a
 * half-written file produce a half-true answer.
 *
 * **A failed state write must never turn a good server call into a failed
 * one** (gmail-wiki-ingest.js:208). The push has already landed; the cost of a
 * lost write is this run's digest or history row, which is far cheaper than
 * re-pushing a note.
 *
 * KNOWN LIMITATION, written down rather than discovered in smoketest:
 * **`ingests.json` is the ONLY history store.** R19 forbids the push endpoint
 * being a read channel and no other gateway-token route returns ingest history,
 * so there is nowhere else for R6 to read from. A container recreated from an
 * image therefore starts with empty history — the same class of fact as
 * gmail's "the install sentinel says the bundle is present, which is a
 * different claim from the cron exists". TC-S6-10 must seed its three ingests
 * within one container lifetime, and SKILL.md says so to the user.
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '../data');

const PATHS = Object.freeze({
  prefs: path.join(DATA_DIR, 'prefs.json'),
  ingests: path.join(DATA_DIR, 'ingests.json'),
  run: path.join(DATA_DIR, 'last-run.json'),
});

/**
 * R12. Where the bridge runs is a settable field, defaulting to the per-user
 * openclaw container, with javis-mac as the documented alternative.
 *
 * **This build can only STORE the choice.** The skill executes inside the
 * container; it cannot relocate itself onto another host. So setting the field
 * records and reports an intent, and moving the work is an operational change
 * on top of it. SKILL.md states that plainly rather than letting the smoketest
 * discover it (TC-S4-6 step 2 verifies a persisted setting, not a relocation).
 */
const HOSTS = Object.freeze(['openclaw-container', 'javis-mac']);
const DEFAULT_HOST = 'openclaw-container';

/** How many ingest rows the ledger keeps. Older rows fall off the end. */
const MAX_INGESTS = 200;

/**
 * A digest with no run behind it is a lie. Six hours is longer than any real
 * gap between a run's fetch and its report, and short enough that yesterday's
 * abandoned state can never be dressed up as this morning's digest. Same number
 * and same reasoning as gmail-wiki-ingest's STALE_AFTER_MS.
 */
const STALE_AFTER_MS = 6 * 60 * 60 * 1000;

const REFUSALS = Object.freeze({
  no_recent_run: {
    reason: 'there is no run state to report: nothing fetched or pushed in this turn',
    next: 'run fetch and push first; do not invent a digest for a run that did not happen',
  },
  stale_run: {
    reason: 'the run state on disk is more than six hours old, so it belongs to a run that died',
    next: 'start a fresh run rather than reporting stale state; nothing was lost',
  },
  unknown_host: {
    reason: 'the host named for the bridge is not one this skill knows',
    next: `choose one of ${HOSTS.join(' or ')}`,
  },
});

// ---------------------------------------------------------------------------
// Primitives
// ---------------------------------------------------------------------------

function resolve(name, deps = {}) {
  return (deps.paths && deps.paths[name]) || PATHS[name];
}

function readJson(file, fallback) {
  try {
    const parsed = JSON.parse(fs.readFileSync(file, 'utf-8'));
    return parsed == null ? fallback : parsed;
  } catch (_) {
    return fallback;
  }
}

/** tmp-then-rename. Throws; `saveJson` is the swallowing wrapper. */
function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2));
  fs.renameSync(tmp, file);
}

/** Write, or say so on stderr and carry on. Never throws. */
function saveJson(file, value) {
  try {
    writeJson(file, value);
    return true;
  } catch (e) {
    console.error(`state not written (${path.basename(file)}): ${(e && e.message) || e}`);
    return false;
  }
}

function nowMs(deps = {}) {
  if (typeof deps.now === 'function') return Number(deps.now());
  if (deps.now != null) return Number(deps.now);
  return Date.now();
}

function nowIso(deps) {
  return new Date(nowMs(deps)).toISOString();
}

// ---------------------------------------------------------------------------
// prefs.json (R12, R13)
// ---------------------------------------------------------------------------

function defaultPrefs() {
  return {
    host: DEFAULT_HOST,
    profile: 'default',
    notebooks: [],
    schedule: null,
    tz: null,
    updated_at: null,
  };
}

/**
 * Prefs, with every missing field defaulted. A corrupt file reads as the
 * defaults rather than as an error: the user's notebooks are recoverable by
 * picking them again, and refusing the whole run over an unparseable
 * preferences file would be the worse failure.
 */
function readPrefs(deps = {}) {
  const raw = readJson(resolve('prefs', deps), null);
  const prefs = Object.assign(defaultPrefs(), raw && typeof raw === 'object' && !Array.isArray(raw) ? raw : {});
  if (!HOSTS.includes(prefs.host)) prefs.host = DEFAULT_HOST;
  if (!Array.isArray(prefs.notebooks)) prefs.notebooks = [];
  return prefs;
}

function writePrefs(patch, deps = {}) {
  const next = Object.assign(readPrefs(deps), patch || {}, { updated_at: nowIso(deps) });
  if (!HOSTS.includes(next.host)) next.host = DEFAULT_HOST;
  saveJson(resolve('prefs', deps), next);
  return next;
}

/**
 * R12. An unknown host is refused rather than stored: a typo that silently
 * became the setting would report a host nobody runs on.
 */
function setHost(host, deps = {}) {
  const wanted = String(host == null ? '' : host).trim();
  if (!HOSTS.includes(wanted)) {
    return Object.assign(
      { ok: false, error: 'unknown_host', detail: wanted || '(empty)', hosts: HOSTS },
      REFUSALS.unknown_host,
    );
  }
  return { ok: true, prefs: writePrefs({ host: wanted }, deps) };
}

// ---------------------------------------------------------------------------
// ingests.json (R6)
// ---------------------------------------------------------------------------

/** Newest first, bounded, and never more than MAX_INGESTS rows on disk. */
function readIngests(deps = {}) {
  const rows = readJson(resolve('ingests', deps), []);
  if (!Array.isArray(rows)) return [];
  return rows
    .filter((r) => r && typeof r === 'object')
    .slice()
    .sort((a, b) => String(b.date || '').localeCompare(String(a.date || '')));
}

/**
 * One ledger row per ingest: the five fields R6 names, plus the source id so a
 * row can be matched to an undo.
 *
 * `trigger` is recorded rather than inferred, because R10 requires the agent to
 * be able to name what started a run and a scheduled run has nobody to ask.
 */
function appendIngest(row, deps = {}) {
  const entry = {
    notebook: String((row && row.notebook) || ''),
    note: String((row && row.note) || ''),
    source_id: String((row && row.source_id) || ''),
    trigger: String((row && row.trigger) || 'unknown'),
    date: (row && row.date) || nowIso(deps),
    pages: Number((row && row.pages) || 0),
  };
  const rows = [entry, ...readIngests(deps)].slice(0, MAX_INGESTS);
  saveJson(resolve('ingests', deps), rows);
  return entry;
}

// ---------------------------------------------------------------------------
// last-run.json (R10, R20)
// ---------------------------------------------------------------------------

/**
 * OVERWRITES, where `mergeRun` merges — gmail's split, for gmail's reason: a
 * run that fetched nothing still has state, so the empty-run digest falls out
 * of real counters instead of a special case, and yesterday's leftovers can
 * never be read as today's run.
 */
function startRun(state, deps = {}) {
  const next = Object.assign({ started_at: nowIso(deps), trigger: 'unknown' }, state || {});
  saveJson(resolve('run', deps), next);
  return next;
}

function mergeRun(patch, deps = {}) {
  const next = Object.assign({}, readJson(resolve('run', deps), null) || {}, patch || {});
  saveJson(resolve('run', deps), next);
  return next;
}

function readRun(deps = {}) {
  return readJson(resolve('run', deps), null);
}

function clearRun(deps = {}) {
  try {
    fs.unlinkSync(resolve('run', deps));
    return true;
  } catch (_) {
    return false;
  }
}

/**
 * The run a digest may be rendered from, or one refusal naming why not.
 *
 * `started_at` is the only thing standing between this run and a file left
 * behind by a run that died, so an unparseable or missing date is `stale_run`
 * rather than a date of zero.
 */
function runForReport(deps = {}) {
  const state = readRun(deps);
  if (!state) return Object.assign({ ok: false, error: 'no_recent_run' }, REFUSALS.no_recent_run);
  const started = Date.parse(state.started_at);
  if (!(started > 0) || nowMs(deps) - started > STALE_AFTER_MS) {
    return Object.assign(
      { ok: false, error: 'stale_run', started_at: state.started_at || null },
      REFUSALS.stale_run,
    );
  }
  return { ok: true, state };
}

module.exports = {
  DATA_DIR,
  PATHS,
  HOSTS,
  DEFAULT_HOST,
  MAX_INGESTS,
  STALE_AFTER_MS,
  REFUSALS,
  readJson,
  writeJson,
  saveJson,
  defaultPrefs,
  readPrefs,
  writePrefs,
  setHost,
  readIngests,
  appendIngest,
  startRun,
  mergeRun,
  readRun,
  clearRun,
  runForReport,
  nowIso,
};
