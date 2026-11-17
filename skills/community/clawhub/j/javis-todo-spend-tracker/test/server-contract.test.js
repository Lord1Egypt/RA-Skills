'use strict';
// Server contract — R27 / build finding R0-1: the skill reads its rows with the
// container gateway token, and GET /api/skill/data (read_skill_data) now accepts
// it. These tests replay response bodies captured verbatim from the real handler
// (test/fixtures/server-read-responses.json) and serve them ONLY for the exact
// request path the handler answered, so a drift in either the query the skill
// builds (skill / type / from / to) or the SkillDataReadResponse shape
// ({ skill, type, items: [{ dedup_key, status, payload, start_at, ... }] }) fails here.
// Spec §2, §4; R22 (done-offers), R25 (chat answers).

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const lib = require('../scripts/lib');
const { fetchOpen } = require('../scripts/todo-spend-tracker');
const { runCli } = require('../scripts/ledger');

const { responses } = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'server-read-responses.json'), 'utf8'));
const TZ = 'America/Los_Angeles';
const NOW = '2026-10-27T22:09:15.000Z';

// A fake server that answers only the paths the real handler answered.
function realServer(seen = []) {
  const byPath = new Map(Object.values(responses).map((r) => [r.path, r.body]));
  return async (url, token) => {
    assert.equal(token, 'gw-token', 'reads carry the container gateway token');
    const p = url.slice(lib.SERVER.length);
    seen.push(p);
    if (!byPath.has(p)) {
      const e = new Error(`GET ${p} -> HTTP 404 (not a path the real handler answered)`);
      e.status = 404;
      throw e;
    }
    return byPath.get(p);
  };
}

test('contract [R27]: readSkillData builds the exact query the real handler answered and flattens items', async () => {
  const seen = [];
  const rows = await lib.readSkillData('gw-token', 'ledger_task', {}, { httpGet: realServer(seen) });
  assert.deepEqual(seen, [responses.ledger_task.path]);
  assert.equal(rows.length, responses.ledger_task.body.items.length);
  for (const r of rows) {
    assert.equal(r.type, 'ledger_task');
    assert.equal(typeof r.dedup_key, 'string');
    assert.ok(['pending', 'confirmed'].includes(r.status));
    assert.match(r.start_at, /^\d{4}-\d{2}-\d{2}T00:00:00$/, 'ledger rows read back as naive local days');
    assert.equal(r.is_utc, false);
  }
});

test('contract [R22, R27]: fetch-open uses the server rows (a confirmed done closes its to-do)', async () => {
  const out = await fetchOpen({ token: 'gw-token', tz: TZ, now: NOW, deps: { httpGet: realServer() } });
  assert.equal(out.source, 'server');
  assert.equal(out.warning, undefined);
  assert.deepEqual(out.open, [{ dedup_key: 'task:sess-A:947c978408fb', item: 'Call the bank', since: '2026-10-20' }]);
});

test('contract [R25, R27]: `ledger.js todos` answers from the server rows', async () => {
  const cap = [];
  const code = await runCli(['todos'], {
    token: 'gw-token', fetchTz: async () => TZ, now: () => NOW, httpGet: realServer(), out: (s) => cap.push(s),
  });
  assert.equal(code, 0);
  assert.equal(cap.at(-1), [
    'You have 1 open to-do:',
    '- Call the bank (since Oct 20)',
    '',
    'Done in the last 14 days: Buy ink.',
    '',
    '[Open To-dos & Spending ›](javis://todos)',
  ].join('\n'));
});

test('contract [R25, R15, R27]: `ledger.js spending` sends the month window the handler filters on', async () => {
  const seen = [];
  const cap = [];
  const code = await runCli(['spending', '--month', '2026-10'], {
    token: 'gw-token', fetchTz: async () => TZ, now: () => NOW, httpGet: realServer(seen), out: (s) => cap.push(s),
  });
  assert.equal(code, 0);
  assert.deepEqual(seen, [responses.ledger_expense_2026_10.path]);
  assert.match(cap.at(-1), /^You spent \$4\.50 in October 2026 \(confirmed purchases only\)\./);
  assert.match(cap.at(-1), /1 purchase is waiting for you to confirm \(not counted\)\./);
});
