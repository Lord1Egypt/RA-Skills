#!/usr/bin/env node
/**
 * todo-spend-tracker — fetch-open and push (spec §1, §2; R6, R7, R9, R20, R22).
 *
 *   node scripts/todo-spend-tracker.js fetch-open [--tz <IANA>]
 *       Print { reference_date, reference_time, reference_weekday, tz, open: [
 *       { dedup_key, item, since } ], source } — the open to-dos a "done" may name.
 *
 *   node scripts/todo-spend-tracker.js push --file <extraction.json>
 *   node scripts/todo-spend-tracker.js push <<'JAVIS_LEDGER_JSON'   (quoted heredoc)
 *       Validate the extracted rows, build dedup_key / start_at / source_ref,
 *       and POST them as PENDING rows to /api/skill/data (one call per type:
 *       ledger_task, ledger_expense, ledger_done). Prints a JSON summary of what
 *       was written and what was dropped and why.
 *
 * Extraction JSON (stdin):
 *   {
 *     "source_ref": "<unit session id>",         // required
 *     "unit": "audio:<id>" | "kbd:<id>",         // the dispatcher unit; required for keyboard
 *     "source_kind": "audio" | "keyboard",
 *     "reference_date": "YYYY-MM-DD",            // the unit's local day (UNIT CONTEXT)
 *     "tz": "<IANA>",                            // optional; used only without reference_date
 *     "tasks":    [ { "item", "quote" } ],
 *     "expenses": [ { "item", "amount", "currency", "category", "quote", "date"? } ],
 *     "dones":    [ { "task_key", "quote" } ]
 *   }
 *
 * Row shapes written (§1):
 *   ledger_task    dedup_key task:<source_ref>:<hash(item, unit)>
 *                  payload { item, quote, source: "recording" }
 *   ledger_expense dedup_key exp:<source_ref>:<hash(item, amount, currency, day, unit)>
 *                  payload { item, amount, currency, category, quote, source: "recording" }
 *   ledger_done    dedup_key done:<task_key>:<source_ref>
 *                  payload { task_key, quote, source: "recording" }
 *   start_at = the local day at 00:00, naive ("YYYY-MM-DDT00:00:00"); status "pending";
 *   source_ref = the unit's session id (so a re-run upserts the same rows).
 *   `unit` enters the hash because a keyboard source_ref is one session id per
 *   day: without it, two typed "$5 coffee" units of one day would share a key and
 *   the second would overwrite the first (R0-5). The canonical audio unit
 *   ("audio:<source_ref>") adds nothing, so audio keys do not depend on whether
 *   the agent passed `unit`. An expense `date` must fall in last month or this
 *   month (relative to reference_date), the window the app can confirm in (R8).
 *
 * Env: OPENCLAW_GATEWAY_TOKEN (required), JAVIS_SERVER_URL (default http://javis-server:8000), TZ.
 */
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const lib = require('./lib');
const { CATEGORIES, canonicalCategory } = require('./ledger');

const QUOTE_MAX_WORDS = 25;
const QUOTE_MAX_CHARS = 200;
const ITEM_MAX_CHARS = 200;
const KEY_MAX = 512;
const TYPES = { task: 'ledger_task', expense: 'ledger_expense', done: 'ledger_done' };

// Common currency words and symbols the model may emit, mapped to ISO 4217.
const CURRENCY_ALIASES = {
  '$': 'USD', 'US$': 'USD', 'USD': 'USD', 'DOLLAR': 'USD', 'DOLLARS': 'USD', '美元': 'USD',
  '¥': 'CNY', '￥': 'CNY', 'RMB': 'CNY', 'CNY': 'CNY', 'YUAN': 'CNY', '元': 'CNY', '块': 'CNY', '人民币': 'CNY',
  '€': 'EUR', 'EUR': 'EUR', 'EURO': 'EUR', 'EUROS': 'EUR', '欧元': 'EUR',
  '£': 'GBP', 'GBP': 'GBP', 'POUND': 'GBP', 'POUNDS': 'GBP', '英镑': 'GBP',
  'JPY': 'JPY', 'YEN': 'JPY', '日元': 'JPY',
  'HKD': 'HKD', 'HK$': 'HKD', '港币': 'HKD', '港元': 'HKD',
  'TWD': 'TWD', 'NT$': 'TWD', '台币': 'TWD',
  'CAD': 'CAD', 'C$': 'CAD', 'AUD': 'AUD', 'A$': 'AUD', 'SGD': 'SGD', 'S$': 'SGD',
  'KRW': 'KRW', '₩': 'KRW', 'INR': 'INR', '₹': 'INR', 'CHF': 'CHF', 'MXN': 'MXN', 'NZD': 'NZD',
};

// ---- normalisation ---------------------------------------------------------
function cleanText(v, max) {
  if (v == null) return '';
  return String(v).normalize('NFC').replace(/\s+/g, ' ').trim().slice(0, max);
}

// The user's words, at most 25 words (whitespace-separated) and 200 chars.
function cleanQuote(v) {
  const s = cleanText(v, 10000);
  const words = s.split(' ').filter(Boolean);
  const cut = words.length > QUOTE_MAX_WORDS ? words.slice(0, QUOTE_MAX_WORDS).join(' ') : s;
  return cut.slice(0, QUOTE_MAX_CHARS);
}

function normalizeCurrency(v) {
  if (v == null) return null;
  const s = String(v).trim().toUpperCase();
  if (!s) return null;
  return CURRENCY_ALIASES[s] || CURRENCY_ALIASES[String(v).trim()] || null;
}

// Positive amount, rounded to cents; null if missing or not a number.
function normalizeAmount(v) {
  if (v == null || v === '' || typeof v === 'boolean') return null;
  const n = typeof v === 'number' ? v : Number(String(v).replace(/,/g, '').trim());
  if (!Number.isFinite(n) || n <= 0) return null;
  return Math.round(n * 100) / 100;
}

// One of the 9 fixed categories (case-insensitive); anything else -> null (dropped).
function normalizeCategory(v) {
  const s = v == null ? '' : String(v).trim().toLowerCase();
  if (!s) return null;
  const hit = CATEGORIES.find((c) => c.toLowerCase() === s);
  return hit ? canonicalCategory(hit) : null;
}

function itemHashText(item) { return item.toLowerCase(); }

function shortHash(...parts) {
  return crypto.createHash('sha256').update(parts.join('\u001f'), 'utf8').digest('hex').slice(0, 12);
}

// Extra hash parts: [] when there is nothing to add, so keys built without a
// unit/day stay the same as keys built with the canonical audio unit.
function extraParts(...parts) { return parts.filter((p) => p != null && p !== ''); }

function taskKey(sourceRef, item, unitPart = '') {
  return `task:${sourceRef}:${shortHash(itemHashText(item), ...extraParts(unitPart))}`;
}

function expenseKey(sourceRef, item, amount, currency, day = '', unitPart = '') {
  return `exp:${sourceRef}:${shortHash(itemHashText(item), amount.toFixed(2), currency, ...extraParts(day, unitPart))}`;
}

const UNIT_RE = /^(audio|kbd):[A-Za-z0-9._:-]{1,128}$/;

// The unit's contribution to the hash ('' for the canonical audio unit).
function unitHashPart(extraction, sourceRef) {
  const unit = cleanText(extraction.unit, 200);
  const keyboard = extraction.source_kind === 'keyboard' || unit.startsWith('kbd:');
  if (!unit) {
    if (keyboard) {
      throw new Error('push needs "unit" (the dispatcher unit, e.g. "kbd:123") for a keyboard unit: '
        + 'its source_ref is shared by every input typed that day.');
    }
    return '';
  }
  if (!UNIT_RE.test(unit)) throw new Error(`push "unit" must look like "audio:<id>" or "kbd:<id>" (got ${JSON.stringify(unit)}).`);
  if (keyboard && !unit.startsWith('kbd:')) throw new Error(`a keyboard unit must be "kbd:<id>" (got ${JSON.stringify(unit)}).`);
  return unit === `audio:${sourceRef}` ? '' : unit;
}

// First day of the month before `day` ("YYYY-MM-DD").
function previousMonthStart(day) {
  let y = +day.slice(0, 4);
  let m = +day.slice(5, 7) - 1;
  if (m === 0) { m = 12; y -= 1; }
  return `${String(y).padStart(4, '0')}-${String(m).padStart(2, '0')}-01`;
}

function doneKey(taskDedupKey, sourceRef) {
  return `done:${taskDedupKey}:${sourceRef}`;
}

function isDay(s) {
  if (typeof s !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(s)) return false;
  const d = new Date(`${s}T00:00:00Z`);
  return !isNaN(d.getTime()) && d.toISOString().slice(0, 10) === s;
}

function dayStart(day) { return `${day}T00:00:00`; }

// ---- build rows ------------------------------------------------------------
// Pure: extraction + the open to-do keys -> { rows: {ledger_task:[...], ...}, dropped: [...] }.
// `openKeys` is the set of dedup_keys a done may name (from fetch-open).
function buildRows(extraction, { openKeys, referenceDate }) {
  const ex = extraction || {};
  const sourceRef = cleanText(ex.source_ref, 400);
  if (!sourceRef) throw new Error('push needs "source_ref" (the unit session id) to build idempotent dedup keys.');
  if (!isDay(referenceDate)) throw new Error(`push needs a valid reference_date YYYY-MM-DD (got ${JSON.stringify(referenceDate)}).`);
  const open = openKeys instanceof Set ? openKeys : new Set(openKeys || []);
  const unitPart = unitHashPart(ex, sourceRef);
  const earliestDay = previousMonthStart(referenceDate);

  const rows = { ledger_task: [], ledger_expense: [], ledger_done: [] };
  const dropped = [];
  const seen = new Set();
  const add = (type, row) => {
    if (row.dedup_key.length > KEY_MAX) { dropped.push({ kind: type, reason: 'dedup_key too long' }); return; }
    if (seen.has(row.dedup_key)) { dropped.push({ kind: type, reason: 'duplicate in this unit', dedup_key: row.dedup_key }); return; }
    seen.add(row.dedup_key);
    rows[type].push(row);
  };
  const list = (v) => (Array.isArray(v) ? v : []);

  for (const t of list(ex.tasks)) {
    const item = cleanText(t && t.item, ITEM_MAX_CHARS);
    if (!item) { dropped.push({ kind: 'task', reason: 'empty item' }); continue; }
    add(TYPES.task, {
      dedup_key: taskKey(sourceRef, item, unitPart),
      payload: { item, quote: cleanQuote(t.quote), source: 'recording' },
      status: 'pending',
      start_at: dayStart(referenceDate),
      source_ref: sourceRef,
    });
  }

  for (const e of list(ex.expenses)) {
    const item = cleanText(e && e.item, ITEM_MAX_CHARS);
    const amount = normalizeAmount(e && e.amount);
    const currency = normalizeCurrency(e && e.currency);
    const category = normalizeCategory(e && e.category);
    if (!item) { dropped.push({ kind: 'expense', reason: 'empty item' }); continue; }
    if (amount == null) { dropped.push({ kind: 'expense', item, reason: 'unknown amount' }); continue; }
    if (!currency) { dropped.push({ kind: 'expense', item, reason: 'unknown currency' }); continue; }
    if (!category) { dropped.push({ kind: 'expense', item, reason: `unknown category ${JSON.stringify(e.category)}` }); continue; }
    const day = e.date != null && isDay(String(e.date)) ? String(e.date) : referenceDate;
    // The app shows Confirm/Discard only for last month and this month, so a
    // purchase dated elsewhere (or in the future) could never be confirmed.
    if (day < earliestDay || day > referenceDate) {
      dropped.push({ kind: 'expense', item, reason: `date ${day} outside last month and this month` });
      continue;
    }
    add(TYPES.expense, {
      dedup_key: expenseKey(sourceRef, item, amount, currency, day, unitPart),
      payload: { item, amount, currency, category, quote: cleanQuote(e.quote), source: 'recording' },
      status: 'pending',
      start_at: dayStart(day),
      source_ref: sourceRef,
    });
  }

  for (const d of list(ex.dones)) {
    const key = cleanText(d && d.task_key, KEY_MAX);
    if (!key || !open.has(key)) {
      dropped.push({ kind: 'done', task_key: key || null, reason: 'names no open to-do' });
      continue;
    }
    add(TYPES.done, {
      dedup_key: doneKey(key, sourceRef),
      payload: { task_key: key, quote: cleanQuote(d.quote), source: 'recording' },
      status: 'pending',
      start_at: dayStart(referenceDate),
      source_ref: sourceRef,
    });
  }

  return { rows, dropped };
}

// ---- fetch-open ------------------------------------------------------------
// Open to-dos a done may name: confirmed tasks with no confirmed done, minus
// tasks that already have a pending done offer. Only the server knows which
// to-dos the user confirmed, discarded, ticked in the app or lost with a deleted
// recording, so when it refuses the read (401/403) the list is EMPTY and no done
// can be offered this run (R22: a done must name a confirmed open to-do). There
// is deliberately no container-local fallback: a local copy offered discarded
// and ticked to-dos, never re-offered after "Not yet", and kept to-do text from
// deleted recordings (R24).
async function fetchOpen({ token, tz, now, deps = {} }) {
  const { project } = require('./ledger');
  const nowIso = now || new Date().toISOString();
  const anchor = lib.localAnchor(nowIso, tz);
  try {
    const rows = [
      ...await lib.readSkillData(token, 'ledger_task', {}, deps),
      ...await lib.readSkillData(token, 'ledger_done', {}, deps),
    ];
    const offered = new Set(rows
      .filter((r) => r.type === 'ledger_done' && r.status === 'pending' && r.payload)
      .map((r) => r.payload.task_key));
    const open = project(rows, anchor.reference_time).open.filter((t) => !offered.has(t.dedup_key));
    return { ...anchor, tz, open, source: 'server' };
  } catch (e) {
    if (!(e && (e.status === 401 || e.status === 403))) throw e;
    return {
      ...anchor, tz, open: [], source: 'unavailable',
      warning: `server read refused (${e.message}); the open to-dos are unknown, so record no "done" this run`,
    };
  }
}

// ---- push ------------------------------------------------------------------
async function doPush(deps = {}) {
  const token = deps.token || lib.requireToken();
  const extraction = deps.extraction || parseExtraction(deps.file ? fs.readFileSync(deps.file, 'utf8') : await readStdin());
  let referenceDate = extraction.reference_date;
  let tz = extraction.tz;
  if (!isDay(referenceDate)) {
    tz = await lib.resolveUserTz({ explicitTz: tz, token, deps });
    const nowIso = deps.now ? deps.now() : new Date().toISOString();
    referenceDate = lib.localAnchor(nowIso, tz).reference_date;
  }

  const wantsDone = Array.isArray(extraction.dones) && extraction.dones.length > 0;
  let openKeys = new Set();
  if (wantsDone) {
    try {
      const open = deps.openList || (await fetchOpen({ token, tz: tz || lib.resolveTz(null), deps })).open;
      openKeys = new Set(open.map((t) => t.dedup_key));
    } catch (e) {
      // Without the open list no done can be checked, so every done is dropped
      // (R22); to-dos and purchases are still written.
      console.error(`⚠️ could not read open to-dos (${e.message}); dropping done rows.`);
    }
  }

  const { rows, dropped } = buildRows(extraction, { openKeys, referenceDate });
  const written = {};
  for (const type of Object.values(TYPES)) {
    written[type] = rows[type].length;
    if (!rows[type].length) continue;
    await lib.writeSkillData(token, type, rows[type], deps);
  }

  const summary = {
    source_ref: extraction.source_ref,
    reference_date: referenceDate,
    written,
    dropped,
  };
  (deps.emit || ((o) => console.log(JSON.stringify(o, null, 2))))(summary);
  return summary;
}

async function readStdin() {
  let input = '';
  for await (const chunk of process.stdin) input += chunk;
  return input;
}

function parseExtraction(raw) {
  const input = String(raw == null ? '' : raw).trim();
  if (!input) throw new Error('push expects the extraction JSON object (--file <path> or stdin), got empty input.');
  let parsed;
  try { parsed = JSON.parse(input); } catch (e) { throw new Error(`stdin is not valid JSON: ${e.message}`); }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error('push stdin must be an object { source_ref, reference_date, tasks, expenses, dones }.');
  }
  return parsed;
}

function getFlag(argv, name, dflt) {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 && i + 1 < argv.length ? argv[i + 1] : dflt;
}

async function main(argv) {
  const cmd = argv[0];
  if (cmd === 'fetch-open') {
    const token = lib.requireToken();
    const tz = await lib.resolveUserTz({ explicitTz: getFlag(argv, 'tz', null), token });
    console.log(JSON.stringify(await fetchOpen({ token, tz }), null, 2));
    return;
  }
  if (cmd === 'push') { await doPush({ file: getFlag(argv, 'file', null) || undefined }); return; }
  console.log([
    'Usage:',
    '  node scripts/todo-spend-tracker.js fetch-open [--tz <IANA>]',
    '  node scripts/todo-spend-tracker.js push --file <extraction.json>',
    "  node scripts/todo-spend-tracker.js push <<'JAVIS_LEDGER_JSON'   # quoted heredoc, never echo '...'",
  ].join('\n'));
  if (cmd && cmd !== '--help') process.exitCode = 2;
}

module.exports = {
  buildRows,
  fetchOpen,
  doPush,
  taskKey,
  expenseKey,
  doneKey,
  shortHash,
  parseExtraction,
  previousMonthStart,
  cleanQuote,
  normalizeAmount,
  normalizeCurrency,
  normalizeCategory,
};

if (require.main === module) {
  main(process.argv.slice(2)).catch((err) => {
    console.error('❌', err.message);
    process.exit(1);
  });
}
