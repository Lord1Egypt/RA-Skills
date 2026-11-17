'use strict';
// R21 — the same rows always give the same counts, in any order (TC-S1-14).

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const { computeLedger, project, formatTodosAnswer, formatSpendingAnswer } = require('../scripts/ledger');

const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'ledger-cases.json'), 'utf8'));

// Small seeded PRNG (mulberry32) so a failure is reproducible.
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(arr, rand) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

for (const c of cases) {
  test(`ledger-shuffle [R21, TC-S1-14]: ${c.name}`, () => {
    const rand = rng(1234);
    const base = computeLedger(c.rows, c.now);
    for (let i = 0; i < 25; i += 1) {
      const rows = shuffle(c.rows, rand);
      assert.deepStrictEqual(computeLedger(rows, c.now), base);
      assert.deepStrictEqual(computeLedger(rows.slice().reverse(), c.now), base);
    }
  });
}

test('ledger-shuffle [R25, TC-S1-14]: chat answers are identical for shuffled rows', () => {
  const rand = rng(99);
  for (const c of cases) {
    const month = c.now.slice(0, 7);
    const t0 = formatTodosAnswer(project(c.rows, c.now));
    const s0 = formatSpendingAnswer(project(c.rows, c.now), month);
    for (let i = 0; i < 10; i += 1) {
      const rows = shuffle(c.rows, rand);
      assert.equal(formatTodosAnswer(project(rows, c.now)), t0);
      assert.equal(formatSpendingAnswer(project(rows, c.now), month), s0);
    }
  }
});
