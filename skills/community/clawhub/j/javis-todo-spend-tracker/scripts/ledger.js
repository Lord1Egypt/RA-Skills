#!/usr/bin/env node
/**
 * todo-spend-tracker — the counting rules (spec §1, R21, R22, R15, R25).
 *
 * Pure functions over skill_data rows, plus a CLI the chat answers use:
 *
 *   node scripts/ledger.js todos                       [--json] [--tz <IANA>]
 *   node scripts/ledger.js spending [--month YYYY-MM]  [--json] [--tz <IANA>]
 *
 * Rules (identical in the iOS LedgerCounting module; both pass
 * test/fixtures/ledger-cases.json):
 *   - Only rows with status "confirmed" count. Pending rows are counted
 *     separately (pending.tasks / pending.expenses / pending.dones) and never
 *     enter open, doneRecently or spending. Discarded rows are deleted on the
 *     server, so they are simply absent.
 *   - A to-do is OPEN when its confirmed ledger_task has no confirmed
 *     ledger_done whose payload.task_key equals the task's dedup_key.
 *   - A confirmed ledger_done whose task_key names no confirmed ledger_task
 *     changes nothing (R22).
 *   - Done recently: confirmed ledger_done rows naming a confirmed ledger_task,
 *     whose day (start_at date) is within 14 days of today: day >= today - 14.
 *     One entry per task (the latest done day wins).
 *   - Ordering: newest first by start_at, ties by dedup_key ascending, so any
 *     row order gives the same output.
 *   - Spending: confirmed ledger_expense rows bucketed by the local month of
 *     start_at ("YYYY-MM" = start_at.slice(0, 7)), summed per currency and per
 *     category in integer cents. Currencies are never added together (R15).
 *     A category outside the fixed 9 is counted as "Other". A row with a
 *     non-positive / non-numeric amount or no 3-letter currency is skipped.
 */
'use strict';

const CATEGORIES = [
  'Food & drink',
  'Groceries',
  'Transport',
  'Shopping',
  'Bills & subscriptions',
  'Entertainment',
  'Health',
  'Travel',
  'Other',
];

const DONE_RECENT_DAYS = 14;

// ---- small pure helpers ----------------------------------------------------
function dayOf(startAt) {
  const s = startAt == null ? '' : String(startAt);
  return /^\d{4}-\d{2}-\d{2}/.test(s) ? s.slice(0, 10) : null;
}

// Whole days from day `a` to day `b` ("YYYY-MM-DD"), b - a.
function daysBetween(a, b) {
  const toMs = (d) => Date.UTC(+d.slice(0, 4), +d.slice(5, 7) - 1, +d.slice(8, 10));
  return Math.round((toMs(b) - toMs(a)) / 86400000);
}

function toCents(amount) {
  const n = typeof amount === 'number' ? amount : Number(String(amount == null ? '' : amount).trim() || NaN);
  if (!Number.isFinite(n) || n <= 0) return null;
  return Math.round(n * 100);
}

function canonicalCategory(c) {
  const s = c == null ? '' : String(c).trim().toLowerCase();
  const hit = CATEGORIES.find((k) => k.toLowerCase() === s);
  return hit || 'Other';
}

function newestFirst(a, b) {
  const sa = a.start_at || '';
  const sb = b.start_at || '';
  if (sa !== sb) return sa < sb ? 1 : -1;
  return a.dedup_key < b.dedup_key ? -1 : a.dedup_key > b.dedup_key ? 1 : 0;
}

function confirmed(r) { return r && r.status === 'confirmed'; }
function pendingRow(r) { return r && r.status === 'pending'; }
function payloadOf(r) { return (r && r.payload && typeof r.payload === 'object') ? r.payload : {}; }

// ---- projection ------------------------------------------------------------
// rows: [{ type, dedup_key, status, start_at, payload, source_ref? }]
// now:  local wall-clock "YYYY-MM-DDTHH:MM:SS" (the user's zone).
// Returns the detailed view; summarize() maps it to the fixture shape.
function project(rows, now) {
  const all = (rows || []).filter((r) => r && typeof r.dedup_key === 'string');
  const today = dayOf(now);

  const tasks = all.filter((r) => r.type === 'ledger_task');
  const dones = all.filter((r) => r.type === 'ledger_done');
  const expenses = all.filter((r) => r.type === 'ledger_expense');

  const confirmedTasks = new Map();
  for (const t of tasks.filter(confirmed)) confirmedTasks.set(t.dedup_key, t);

  // task_key -> latest confirmed done row naming a confirmed task
  const closedBy = new Map();
  for (const d of dones.filter(confirmed)) {
    const key = payloadOf(d).task_key;
    if (typeof key !== 'string' || !confirmedTasks.has(key)) continue; // R22: changes nothing
    const prev = closedBy.get(key);
    if (!prev || newestFirst(d, prev) < 0) closedBy.set(key, d);
  }

  const open = [...confirmedTasks.values()]
    .filter((t) => !closedBy.has(t.dedup_key))
    .sort(newestFirst)
    .map((t) => ({ dedup_key: t.dedup_key, item: payloadOf(t).item || '', since: dayOf(t.start_at) }));

  const doneRecently = [...closedBy.entries()]
    .map(([key, d]) => ({ key, d }))
    .filter(({ d }) => {
      const day = dayOf(d.start_at);
      if (!day || !today) return false;
      const age = daysBetween(day, today);
      return age <= DONE_RECENT_DAYS;
    })
    .sort((x, y) => newestFirst({ ...x.d, dedup_key: x.key }, { ...y.d, dedup_key: y.key }))
    .map(({ key, d }) => ({
      dedup_key: key,
      item: payloadOf(confirmedTasks.get(key)).item || '',
      done_on: dayOf(d.start_at),
      source: payloadOf(d).source || null,
    }));

  const pending = {
    tasks: tasks.filter(pendingRow).length,
    expenses: expenses.filter(pendingRow).length,
    dones: dones.filter(pendingRow).length,
  };

  // month -> currency -> { cents, byCategory: {cat: cents}, count }
  const buckets = {};
  for (const e of expenses.filter(confirmed)) {
    const p = payloadOf(e);
    const cents = toCents(p.amount);
    const currency = typeof p.currency === 'string' ? p.currency.trim().toUpperCase() : '';
    const day = dayOf(e.start_at);
    if (cents == null || !/^[A-Z]{3}$/.test(currency) || !day) continue;
    const month = day.slice(0, 7);
    const cat = canonicalCategory(p.category);
    const m = (buckets[month] = buckets[month] || {});
    const c = (m[currency] = m[currency] || { cents: 0, byCategory: {}, count: 0, rows: [] });
    c.cents += cents;
    c.byCategory[cat] = (c.byCategory[cat] || 0) + cents;
    c.count += 1;
    c.rows.push(e);
  }

  return { open, doneRecently, pending, buckets };
}

// Fixed category order breaks ties so the output never depends on row order.
function sortedCategories(byCategory) {
  return Object.entries(byCategory).sort((a, b) => {
    if (a[1] !== b[1]) return b[1] - a[1];
    return CATEGORIES.indexOf(a[0]) - CATEGORIES.indexOf(b[0]);
  });
}

// The shared-fixture shape (test/fixtures/ledger-cases.json -> expect):
// { open: [task dedup_key...], doneRecently: [task dedup_key...],
//   pending: {tasks, expenses, dones},
//   spending: { "YYYY-MM": { "USD": { total, byCategory: {cat: amount} } } } }
function summarize(view) {
  const spending = {};
  for (const month of Object.keys(view.buckets).sort()) {
    spending[month] = {};
    for (const cur of Object.keys(view.buckets[month]).sort()) {
      const b = view.buckets[month][cur];
      const byCategory = {};
      for (const [cat, cents] of sortedCategories(b.byCategory)) byCategory[cat] = cents / 100;
      spending[month][cur] = { total: b.cents / 100, byCategory };
    }
  }
  return {
    open: view.open.map((t) => t.dedup_key),
    doneRecently: view.doneRecently.map((t) => t.dedup_key),
    pending: { ...view.pending },
    spending,
  };
}

function computeLedger(rows, now) {
  return summarize(project(rows, now));
}

// ---- chat answers (R25: the script does the arithmetic, the agent copies) --
const MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
  'August', 'September', 'October', 'November', 'December'];
const SHORT_MONTHS = MONTH_NAMES.map((m) => m.slice(0, 3));

function monthLabel(month) {
  return `${MONTH_NAMES[+month.slice(5, 7) - 1]} ${month.slice(0, 4)}`;
}

function shortDay(day) {
  return day ? `${SHORT_MONTHS[+day.slice(5, 7) - 1]} ${+day.slice(8, 10)}` : '';
}

function formatMoney(cents, currency) {
  const s = (cents / 100).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  return currency === 'USD' ? `$${s}` : `${s} ${currency}`;
}

function plural(n, one, many) { return `${n} ${n === 1 ? one : many}`; }

function formatTodosAnswer(view) {
  const lines = [];
  if (!view.open.length) {
    lines.push('You have no open to-dos.');
  } else {
    lines.push(`You have ${plural(view.open.length, 'open to-do', 'open to-dos')}:`);
    for (const t of view.open) lines.push(`- ${t.item} (since ${shortDay(t.since)})`);
  }
  if (view.pending.tasks) {
    lines.push('');
    lines.push(`${plural(view.pending.tasks, 'more to-do is', 'more to-dos are')} waiting for you to confirm (not counted).`);
  }
  if (view.pending.dones) {
    lines.push(`${plural(view.pending.dones, '"Done?" offer is', '"Done?" offers are')} waiting for you to confirm.`);
  }
  if (view.doneRecently.length) {
    lines.push('');
    lines.push(`Done in the last 14 days: ${view.doneRecently.map((t) => t.item).join(', ')}.`);
  }
  lines.push('');
  lines.push('[Open To-dos & Spending ›](javis://todos)');
  return lines.join('\n');
}

// Main currency = the one with the most confirmed purchases that month; ties by
// currency code (amounts in different currencies are never compared).
function orderedCurrencies(monthBuckets) {
  return Object.entries(monthBuckets || {}).sort((a, b) => {
    if (a[1].count !== b[1].count) return b[1].count - a[1].count;
    return a[0] < b[0] ? -1 : 1;
  });
}

function pendingExpensesInMonth(rows, month) {
  return (rows || []).filter((r) => r && r.type === 'ledger_expense' && r.status === 'pending'
    && dayOf(r.start_at) && dayOf(r.start_at).slice(0, 7) === month).length;
}

function formatSpendingAnswer(view, month, opts = {}) {
  const pendingCount = opts.pendingInMonth != null ? opts.pendingInMonth : view.pending.expenses;
  const curs = orderedCurrencies(view.buckets[month]);
  const lines = [];
  if (!curs.length) {
    lines.push(`Nothing spent in ${monthLabel(month)} (confirmed purchases only).`);
  } else {
    const [mainCur, main] = curs[0];
    lines.push(`You spent ${formatMoney(main.cents, mainCur)} in ${monthLabel(month)} (confirmed purchases only).`);
    lines.push('');
    lines.push('| Category | Amount |');
    lines.push('|---|---|');
    for (const [cat, cents] of sortedCategories(main.byCategory)) lines.push(`| ${cat} | ${formatMoney(cents, mainCur)} |`);
    for (const [cur, b] of curs.slice(1)) {
      lines.push('');
      lines.push(`Also ${formatMoney(b.cents, cur)} in ${cur}, kept separate (not added to the ${mainCur} total): `
        + sortedCategories(b.byCategory).map(([cat, cents]) => `${cat} ${formatMoney(cents, cur)}`).join(', ') + '.');
    }
  }
  if (pendingCount) {
    lines.push('');
    lines.push(`${plural(pendingCount, 'purchase is', 'purchases are')} waiting for you to confirm (not counted).`);
  }
  lines.push('');
  lines.push('[See by category ›](javis://todos/month)');
  return lines.join('\n');
}

// JSON form of one month for `spending --json`.
function monthReport(view, month) {
  const out = {};
  for (const [cur, b] of orderedCurrencies(view.buckets[month])) {
    const byCategory = {};
    for (const [cat, cents] of sortedCategories(b.byCategory)) byCategory[cat] = cents / 100;
    out[cur] = { total: b.cents / 100, purchases: b.count, byCategory };
  }
  return out;
}

function nextMonthStart(month) {
  let y = +month.slice(0, 4);
  let m = +month.slice(5, 7) + 1;
  if (m === 13) { m = 1; y += 1; }
  return `${String(y).padStart(4, '0')}-${String(m).padStart(2, '0')}-01T00:00:00`;
}

// ---- CLI -----------------------------------------------------------------
function flag(argv, name, dflt) {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 && i + 1 < argv.length ? argv[i + 1] : dflt;
}

// Degraded path only: GET /api/skill/data accepts the container's gateway token
// (R27), so a 401/403 here means the token was revoked or the server is
// misconfigured, never the normal case.
const READ_DENIED_HINT = 'The server refused this container\'s read of its ledger rows '
  + '(GET /api/skill/data returned 401/403), so no numbers can be given right now. '
  + 'Tell the user the numbers are on the To-dos & Spending screen: [Open To-dos & Spending ›](javis://todos)';

async function runCli(argv, deps = {}) {
  const lib = require('./lib');
  const out = deps.out || ((s) => console.log(s));
  const cmd = argv[0];
  if (!cmd || cmd === '--help' || !['todos', 'spending'].includes(cmd)) {
    out([
      'Usage:',
      '  node scripts/ledger.js todos                      [--json] [--tz <IANA>]',
      '  node scripts/ledger.js spending [--month YYYY-MM] [--json] [--tz <IANA>]',
    ].join('\n'));
    return cmd && cmd !== '--help' ? 2 : 0;
  }
  const token = deps.token || lib.requireToken();
  const tz = await lib.resolveUserTz({ explicitTz: flag(argv, 'tz', null), token, deps });
  const nowIso = deps.now ? deps.now() : new Date().toISOString();
  const now = lib.toNaiveLocal(nowIso, tz);
  const json = argv.includes('--json');
  const read = (type, win) => lib.readSkillData(token, type, win, deps);

  try {
    if (cmd === 'todos') {
      const rows = [...await read('ledger_task'), ...await read('ledger_done')];
      const view = project(rows, now);
      out(json ? JSON.stringify({ now, tz, ...summarizeTodos(view) }, null, 2) : formatTodosAnswer(view));
      return 0;
    }
    const month = flag(argv, 'month', now.slice(0, 7));
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(month)) throw new Error(`--month must be YYYY-MM (got ${month})`);
    const rows = await read('ledger_expense', { from: `${month}-01T00:00:00`, to: nextMonthStart(month) });
    const view = project(rows, now);
    const pendingInMonth = pendingExpensesInMonth(rows, month);
    out(json
      ? JSON.stringify({ month, tz, currencies: monthReport(view, month), pending: pendingInMonth }, null, 2)
      : formatSpendingAnswer(view, month, { pendingInMonth }));
    return 0;
  } catch (e) {
    if (e && (e.status === 401 || e.status === 403)) {
      out(READ_DENIED_HINT);
      console.error(`⚠️ ${e.message}`);
      return 3;
    }
    throw e;
  }
}

function summarizeTodos(view) {
  return { open: view.open, doneRecently: view.doneRecently, pending: view.pending };
}

module.exports = {
  CATEGORIES,
  DONE_RECENT_DAYS,
  project,
  summarize,
  computeLedger,
  formatTodosAnswer,
  formatSpendingAnswer,
  formatMoney,
  monthReport,
  pendingExpensesInMonth,
  nextMonthStart,
  canonicalCategory,
  runCli,
};

if (require.main === module) {
  runCli(process.argv.slice(2))
    .then((code) => { process.exitCode = code; })
    .catch((err) => { console.error('❌', err.message); process.exit(1); });
}
