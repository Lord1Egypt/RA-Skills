'use strict';
// R21, R22, R15 — the counting rules on every case of the SHARED fixture file
// (test/fixtures/ledger-cases.json; the iOS LedgerCountingTests read a
// byte-identical copy). TC-S1-4, TC-S1-5, TC-S1-6, TC-S1-11, TC-S1-15.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const { computeLedger, CATEGORIES } = require('../scripts/ledger');

const FIXTURE = path.join(__dirname, 'fixtures', 'ledger-cases.json');
const cases = JSON.parse(fs.readFileSync(FIXTURE, 'utf8'));

test('ledger fixture: file is a non-empty array of {name, now, rows, expect} (TC-S1-4)', () => {
  assert.ok(Array.isArray(cases) && cases.length >= 9);
  for (const c of cases) {
    assert.equal(typeof c.name, 'string');
    assert.match(c.now, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/);
    assert.ok(Array.isArray(c.rows));
    for (const r of c.rows) {
      assert.ok(['ledger_task', 'ledger_expense', 'ledger_done'].includes(r.type), r.dedup_key);
      assert.match(r.start_at, /^\d{4}-\d{2}-\d{2}T00:00:00$/);
      assert.ok(['pending', 'confirmed'].includes(r.status));
    }
    assert.deepEqual(Object.keys(c.expect).sort(), ['doneRecently', 'open', 'pending', 'spending']);
  }
});

for (const c of cases) {
  test(`ledger fixture [R21]: ${c.name}`, () => {
    assert.deepStrictEqual(computeLedger(c.rows, c.now), c.expect);
  });
}

test('ledger fixture covers the required scenarios (TC-S1-5, TC-S1-6, TC-S1-11, TC-S1-15, R15)', () => {
  const names = cases.map((c) => c.name).join('\n');
  for (const needle of ['pending', 'discarded', 'closes', 'undo', 'unknown', 'USD and CNY', 'Oct 31', '14 days', 'shuffled']) {
    assert.ok(names.includes(needle), `missing a case about: ${needle}`);
  }
  const twoCur = cases.find((c) => c.name.includes('USD and CNY'));
  assert.deepEqual(Object.keys(twoCur.expect.spending['2026-10']).sort(), ['CNY', 'USD']);
});

test('ledger [R22]: done rows naming no confirmed to-do give the same counts as without them (TC-S1-15)', () => {
  const c = cases.find((x) => x.name.includes('unknown'));
  const withoutStray = c.rows.filter((r) => r.type !== 'ledger_done');
  assert.deepStrictEqual(computeLedger(c.rows, c.now), computeLedger(withoutStray, c.now));
});

test('ledger [R21]: confirming a pending expense moves it from pending into the total (TC-S1-5)', () => {
  const now = '2026-10-26T09:00:00';
  const row = { type: 'ledger_expense', dedup_key: 'exp:x:1', status: 'pending', start_at: '2026-10-02T00:00:00',
    payload: { item: 'lunch', amount: 10, currency: 'USD', category: 'Food & drink' } };
  const before = computeLedger([row], now);
  assert.deepEqual(before.spending, {});
  assert.equal(before.pending.expenses, 1);
  const after = computeLedger([{ ...row, status: 'confirmed' }], now);
  assert.deepEqual(after.spending, { '2026-10': { USD: { total: 10, byCategory: { 'Food & drink': 10 } } } });
  assert.equal(after.pending.expenses, 0);
});

test('ledger: an unknown category counts as Other; bad amount or currency is skipped', () => {
  const now = '2026-10-26T09:00:00';
  const mk = (k, p) => ({ type: 'ledger_expense', dedup_key: k, status: 'confirmed', start_at: '2026-10-02T00:00:00', payload: p });
  const out = computeLedger([
    mk('a', { item: 'x', amount: 5, currency: 'USD', category: 'Gadgets' }),
    mk('b', { item: 'y', amount: 'abc', currency: 'USD', category: 'Health' }),
    mk('c', { item: 'z', amount: 7, category: 'Health' }),
    mk('d', { item: 'w', amount: -3, currency: 'USD', category: 'Health' }),
  ], now);
  assert.deepEqual(out.spending, { '2026-10': { USD: { total: 5, byCategory: { Other: 5 } } } });
});

test('ledger [R9]: the 9 fixed categories, in order', () => {
  assert.deepEqual(CATEGORIES, ['Food & drink', 'Groceries', 'Transport', 'Shopping', 'Bills & subscriptions',
    'Entertainment', 'Health', 'Travel', 'Other']);
});
