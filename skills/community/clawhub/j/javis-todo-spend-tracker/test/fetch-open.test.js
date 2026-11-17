'use strict';
// fetch-open — R6 (reads the open to-dos first), R7/R22 (the dones may only
// name these keys). TC-S2-5, TC-S2-11. R0-2: no local fallback list.

const { test } = require('node:test');
const assert = require('node:assert/strict');

const { fetchOpen, doPush, taskKey } = require('../scripts/todo-spend-tracker');

const NOW = '2026-10-26T16:00:00.000Z';
const TZ = 'America/Los_Angeles';

test('fetch-open [R6]: lists confirmed open to-dos newest first with the anchor', async () => {
  const urls = [];
  const rowsByType = {
    ledger_task: [
      { dedup_key: 'task:a:1', status: 'confirmed', start_at: '2026-10-20T00:00:00', payload: { item: 'Call the bank' } },
      { dedup_key: 'task:b:2', status: 'confirmed', start_at: '2026-10-22T00:00:00', payload: { item: 'Buy ink' } },
      { dedup_key: 'task:c:3', status: 'pending', start_at: '2026-10-23T00:00:00', payload: { item: 'Pending one' } },
      { dedup_key: 'task:d:4', status: 'confirmed', start_at: '2026-10-21T00:00:00', payload: { item: 'Already offered' } },
      { dedup_key: 'task:e:5', status: 'confirmed', start_at: '2026-10-19T00:00:00', payload: { item: 'Closed' } },
    ],
    ledger_done: [
      { dedup_key: 'done:task:d:4:s', status: 'pending', start_at: '2026-10-25T00:00:00', payload: { task_key: 'task:d:4' } },
      { dedup_key: 'done:task:e:5:s', status: 'confirmed', start_at: '2026-10-25T00:00:00', payload: { task_key: 'task:e:5' } },
    ],
  };
  const out = await fetchOpen({ token: 't', tz: TZ, now: NOW, deps: { httpGet: async (url) => {
    urls.push(url);
    return { items: rowsByType[new URL(url).searchParams.get('type')] };
  } } });
  assert.equal(out.source, 'server');
  assert.equal(out.reference_date, '2026-10-26');
  assert.equal(out.tz, TZ);
  assert.deepEqual(out.open, [
    { dedup_key: 'task:b:2', item: 'Buy ink', since: '2026-10-22' },
    { dedup_key: 'task:a:1', item: 'Call the bank', since: '2026-10-20' },
  ]);
  assert.ok(urls.every((u) => u.includes('skill=todo-spend-tracker')));
});

test('fetch-open [R22, R24, R0-2]: a refused server read (401) gives NO open to-dos, so no done is offered', async () => {
  const deps = {
    httpPostJson: async () => ({}),
    httpGet: async () => { const e = new Error('GET /api/skill/data -> HTTP 401'); e.status = 401; throw e; },
  };
  // A to-do this container wrote earlier must not come back from a local copy:
  // the user may have discarded it, ticked it in the app or deleted its recording.
  await doPush({ token: 't', extraction: { source_ref: 'u1', reference_date: '2026-10-25', tasks: [{ item: 'Call the bank' }] }, ...deps, emit: () => {} });
  const out = await fetchOpen({ token: 't', tz: TZ, now: NOW, deps });
  assert.equal(out.source, 'unavailable');
  assert.match(out.warning, /401/);
  assert.deepEqual(out.open, []);
  assert.equal(out.reference_date, '2026-10-26');
  // A done pushed while the list is unknown is dropped (R22), never written.
  let summary;
  const posts = [];
  await doPush({ token: 't', extraction: { source_ref: 'u2', reference_date: '2026-10-26', dones: [{ task_key: taskKey('u1', 'Call the bank'), quote: 'called the bank' }] },
    ...deps, httpPostJson: async (_u, _t, body) => { posts.push(body); return {}; }, emit: (o) => { summary = o; } });
  assert.equal(summary.written.ledger_done, 0);
  assert.equal(summary.dropped[0].reason, 'names no open to-do');
  assert.equal(posts.length, 0);
});

test('fetch-open [R24, R0-2]: the skill keeps no local copy of to-do text', () => {
  const lib = require('../scripts/lib');
  assert.equal(lib.loadState, undefined);
  assert.equal(lib.saveState, undefined);
  const src = require('node:fs').readFileSync(require.resolve('../scripts/todo-spend-tracker'), 'utf8');
  assert.doesNotMatch(src, /saveState|writeFileSync/);
});

test('fetch-open: other server errors are not hidden', async () => {
  await assert.rejects(fetchOpen({ token: 't', tz: TZ, now: NOW, deps: {
    httpGet: async () => { const e = new Error('HTTP 500'); e.status = 500; throw e; },
  } }), /500/);
});
