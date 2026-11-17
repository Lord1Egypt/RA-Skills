'use strict';
// chat answers — R25 (computed by the script, pending given as a count),
// R15 (a second currency is named separately, never added), R21.
// TC-S5-3 (run: npm test -- --test-name-pattern=chat).

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const { project, formatTodosAnswer, formatSpendingAnswer, runCli, formatMoney } = require('../scripts/ledger');

const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'ledger-cases.json'), 'utf8'));
const byName = (s) => cases.find((c) => c.name.includes(s));

test('chat [R25, TC-S5-3]: to-do answer lists open items with since-dates and gives pending as a count', () => {
  const c = byName('pending rows');
  const text = formatTodosAnswer(project(c.rows, c.now));
  assert.equal(text, [
    'You have 1 open to-do:',
    '- Call the bank (since Oct 20)',
    '',
    '1 more to-do is waiting for you to confirm (not counted).',
    '1 "Done?" offer is waiting for you to confirm.',
    '',
    '[Open To-dos & Spending ›](javis://todos)',
  ].join('\n'));
  assert.ok(!text.includes('Renew passport'), 'pending items are counted, not listed');
});

test('chat [R25]: to-do answer names done-recently items and handles none open', () => {
  const c = byName('14 days');
  const text = formatTodosAnswer(project(c.rows, c.now));
  assert.match(text, /^You have no open to-dos\./);
  assert.match(text, /Done in the last 14 days: Call the dentist, Fix the bike\./);
  assert.ok(!text.includes('Return the library books'));
});

test('chat [R25, R15, TC-S5-3]: spending answer copies the fixture numbers; CNY is separate', () => {
  const c = byName('USD and CNY');
  const text = formatSpendingAnswer(project(c.rows, c.now), '2026-10');
  assert.equal(text, [
    'You spent $20.80 in October 2026 (confirmed purchases only).',
    '',
    '| Category | Amount |',
    '|---|---|',
    '| Food & drink | $12.00 |',
    '| Transport | $8.50 |',
    '| Shopping | $0.30 |',
    '',
    'Also 35.00 CNY in CNY, kept separate (not added to the USD total): Food & drink 35.00 CNY.',
    '',
    '[See by category ›](javis://todos/month)',
  ].join('\n'));
  // The numbers match the fixture expectation exactly.
  const exp = c.expect.spending['2026-10'];
  assert.ok(text.includes(formatMoney(exp.USD.total * 100, 'USD')));
  for (const [cat, amt] of Object.entries(exp.USD.byCategory)) assert.ok(text.includes(`| ${cat} | ${formatMoney(Math.round(amt * 100), 'USD')} |`));
});

test('chat [R25]: spending answer gives pending purchases as a count and handles an empty month', () => {
  const c = byName('pending rows');
  const text = formatSpendingAnswer(project(c.rows, c.now), '2026-10');
  assert.match(text, /You spent \$12\.00 in October 2026 \(confirmed purchases only\)\./);
  assert.match(text, /1 purchase is waiting for you to confirm \(not counted\)\./);
  assert.ok(!text.includes('taxi'));
  const empty = formatSpendingAnswer(project([], c.now), '2026-09');
  assert.match(empty, /^Nothing spent in September 2026 \(confirmed purchases only\)\./);
});

function cliDeps(rowsByType, captured) {
  return {
    token: 't',
    fetchTz: async () => 'America/Los_Angeles',
    now: () => '2026-10-26T16:00:00.000Z',
    httpGet: async (url) => {
      captured.push(url);
      return { items: rowsByType[new URL(url).searchParams.get('type')] || [] };
    },
    out: (s) => captured.push(s),
  };
}

test('chat [R25, TC-S5-3]: `ledger.js todos` reads the rows and prints the answer', async () => {
  const c = byName('pending rows');
  const rows = { ledger_task: c.rows.filter((r) => r.type === 'ledger_task'), ledger_done: c.rows.filter((r) => r.type === 'ledger_done') };
  const cap = [];
  assert.equal(await runCli(['todos'], cliDeps(rows, cap)), 0);
  assert.equal(cap.at(-1), formatTodosAnswer(project(c.rows, c.now)));
});

test('chat [R25, R15]: `ledger.js spending --month` asks for that month window and prints per-currency JSON', async () => {
  const c = byName('USD and CNY');
  const cap = [];
  await runCli(['spending', '--month', '2026-10', '--json'], cliDeps({ ledger_expense: c.rows }, cap));
  const url = new URL(cap[0]);
  assert.equal(url.searchParams.get('from'), '2026-10-01T00:00:00');
  assert.equal(url.searchParams.get('to'), '2026-11-01T00:00:00');
  const out = JSON.parse(cap.at(-1));
  assert.equal(out.month, '2026-10');
  assert.deepEqual(out.currencies.USD, { total: 20.8, purchases: 4, byCategory: { 'Food & drink': 12, Transport: 8.5, Shopping: 0.3 } });
  assert.deepEqual(out.currencies.CNY, { total: 35, purchases: 1, byCategory: { 'Food & drink': 35 } });
});

test('chat: `ledger.js spending` defaults to the user\'s local month (not UTC)', async () => {
  const cap = [];
  const deps = cliDeps({}, cap);
  deps.now = () => '2026-11-01T05:00:00.000Z'; // still Oct 31 in Los Angeles
  await runCli(['spending', '--json'], deps);
  assert.equal(JSON.parse(cap.at(-1)).month, '2026-10');
});

test('chat: a refused read prints a hint with the app link and exits non-zero', async () => {
  const cap = [];
  const deps = cliDeps({}, cap);
  deps.httpGet = async () => { const e = new Error('HTTP 401'); e.status = 401; throw e; };
  const code = await runCli(['todos'], deps);
  assert.equal(code, 3);
  assert.match(cap.at(-1), /javis:\/\/todos/);
  // R27: the gateway token IS the supported read credential, so a refusal is a
  // degraded path, not "needs a user token".
  assert.doesNotMatch(cap.at(-1), /user token|gateway token was refused/);
});
