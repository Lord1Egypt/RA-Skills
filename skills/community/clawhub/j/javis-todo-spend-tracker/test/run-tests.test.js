'use strict';
// R0-8: the test plan's `npm test -- ledger` / `-- ledger-shuffle` / `-- chat`
// (TC-S1-4, TC-S1-14, TC-S5-3) resolve to their test files.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const { resolveTargets } = require('../run-tests');

test('run-tests [R0-8, TC-S1-4, TC-S1-14, TC-S5-3]: named targets map to test/<name>.test.js', () => {
  assert.deepEqual(resolveTargets(['ledger']), [path.join('test', 'ledger.test.js')]);
  assert.deepEqual(resolveTargets(['ledger-shuffle']), [path.join('test', 'ledger-shuffle.test.js')]);
  assert.deepEqual(resolveTargets(['chat']), [path.join('test', 'chat.test.js')]);
  const all = resolveTargets([]);
  assert.ok(all.includes(path.join('test', 'push.test.js')));
  assert.ok(all.every((f) => f.endsWith('.test.js')));
});
