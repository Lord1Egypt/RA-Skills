'use strict';

// Tests for scripts/todo-card.js — the shared write side of the general to-do
// card surface (Layer 1). The payload contract is the load-bearing piece:
// icon/title/prompt are REQUIRED; subtitle is optional; source_refs defaults [].
// Item-level start_at/end_at are an OPTIONAL passthrough (naive LOCAL
// wall-clock, calendar-extractor convention) — never invented, and payload-level
// dates are still dropped.

const { test } = require('node:test');
const assert = require('node:assert/strict');

const {
  buildTodoPayload,
  buildTodoItem,
  postTodoCards,
} = require('../scripts/todo-card');

// ---- buildTodoPayload: required fields -----------------------------------
test('buildTodoPayload requires icon, title, and prompt', () => {
  assert.throws(() => buildTodoPayload({ title: 't', prompt: 'p' }), /icon/);
  assert.throws(() => buildTodoPayload({ icon: '🧠', prompt: 'p' }), /title/);
  assert.throws(() => buildTodoPayload({ icon: '🧠', title: 't' }), /prompt/);
  // Blank/whitespace-only is treated as missing.
  assert.throws(() => buildTodoPayload({ icon: '  ', title: 't', prompt: 'p' }), /icon/);
  assert.throws(() => buildTodoPayload({ icon: '🧠', title: '   ', prompt: 'p' }), /title/);
  assert.throws(() => buildTodoPayload({ icon: '🧠', title: 't', prompt: '' }), /prompt/);
});

test('buildTodoPayload rejects non-object input', () => {
  assert.throws(() => buildTodoPayload(null), /object/);
  assert.throws(() => buildTodoPayload('x'), /object/);
  assert.throws(() => buildTodoPayload([1, 2]), /object/);
});

test('buildTodoPayload keeps the fixed contract shape and drops extras', () => {
  const payload = buildTodoPayload({
    icon: '🧠',
    title: '  Intro Javis  ',
    subtitle: '  Brainstorm · 2 sessions ',
    prompt: '  paste me into Claude ',
    source_refs: ['  s1 ', '', 's2'],
    bogus: 'should be dropped',
    start_at: '2026-06-06T00:00:00Z', // dates live at ITEM level, never in payload — must be dropped
  });
  assert.deepEqual(payload, {
    icon: '🧠',
    title: 'Intro Javis',
    prompt: 'paste me into Claude',
    subtitle: 'Brainstorm · 2 sessions',
    source_refs: ['s1', 's2'],
  });
  assert.ok(!('bogus' in payload));
  assert.ok(!('start_at' in payload), 'dates are item-level, never payload-level');
});

test('buildTodoPayload makes subtitle optional and source_refs default to []', () => {
  const payload = buildTodoPayload({ icon: '🧠', title: 't', prompt: 'p' });
  assert.ok(!('subtitle' in payload), 'subtitle omitted when blank/absent');
  assert.deepEqual(payload.source_refs, []);
  // A bare string source_refs is coerced to a one-element array.
  const one = buildTodoPayload({ icon: '🧠', title: 't', prompt: 'p', source_refs: ' sess-1 ' });
  assert.deepEqual(one.source_refs, ['sess-1']);
});

// ---- buildTodoItem: pending status + optional dates ----------------------
test('buildTodoItem requires a dedup_key and emits status=pending; dates absent when not supplied', () => {
  assert.throws(() => buildTodoItem({ payload: { icon: '🧠', title: 't', prompt: 'p' } }), /dedup_key/);
  const item = buildTodoItem({
    dedupKey: 'intro-javis|abc123',
    sourceRef: 'sess-1',
    payload: { icon: '🧠', title: 't', prompt: 'p', source_refs: ['sess-1'] },
  });
  assert.equal(item.dedup_key, 'intro-javis|abc123');
  assert.equal(item.status, 'pending');
  assert.equal(item.source_ref, 'sess-1');
  assert.ok(!('start_at' in item), 'no start_at unless the caller supplies one (never invented)');
  assert.ok(!('end_at' in item), 'no end_at unless the caller supplies one (never invented)');
  assert.equal(item.payload.prompt, 'p');
});

test('buildTodoItem nulls an absent source_ref', () => {
  const item = buildTodoItem({ dedupKey: 'k', payload: { icon: '🧠', title: 't', prompt: 'p' } });
  assert.equal(item.source_ref, null);
});

test('buildTodoItem passes a supplied naive-local start_at/end_at through verbatim', () => {
  const item = buildTodoItem({
    dedupKey: 'k',
    payload: { icon: '🧠', title: 't', prompt: 'p' },
    startAt: '2026-06-09T12:05:00',
    endAt: '2026-06-09T12:30:00',
  });
  assert.equal(item.start_at, '2026-06-09T12:05:00');
  assert.equal(item.end_at, '2026-06-09T12:30:00');
});

test('buildTodoItem emits start_at alone when end_at is absent, and drops end_at without a start_at', () => {
  const startOnly = buildTodoItem({
    dedupKey: 'k',
    payload: { icon: '🧠', title: 't', prompt: 'p' },
    startAt: '2026-06-09T12:05:00',
  });
  assert.equal(startOnly.start_at, '2026-06-09T12:05:00');
  assert.ok(!('end_at' in startOnly));

  // An end without a start is not a coherent window — dropped, not invented.
  const endOnly = buildTodoItem({
    dedupKey: 'k',
    payload: { icon: '🧠', title: 't', prompt: 'p' },
    endAt: '2026-06-09T12:30:00',
  });
  assert.ok(!('start_at' in endOnly));
  assert.ok(!('end_at' in endOnly));
});

test('buildTodoItem rejects zoned/non-naive date strings (the UTC-read-as-local bug class)', () => {
  const payload = { icon: '🧠', title: 't', prompt: 'p' };
  assert.throws(
    () => buildTodoItem({ dedupKey: 'k', payload, startAt: '2026-06-06T04:00:00.000Z' }),
    /naive LOCAL wall-clock/);
  assert.throws(
    () => buildTodoItem({ dedupKey: 'k', payload, startAt: '2026-06-06T04:00:00+02:00' }),
    /naive LOCAL wall-clock/);
  assert.throws(
    () => buildTodoItem({
      dedupKey: 'k', payload,
      startAt: '2026-06-09T12:05:00', endAt: '2026-06-09T19:30:00Z',
    }),
    /end_at/);
  // Blank/whitespace dates are treated as absent, not an error.
  const blank = buildTodoItem({ dedupKey: 'k', payload, startAt: '  ', endAt: '' });
  assert.ok(!('start_at' in blank));
  assert.ok(!('end_at' in blank));
});

// ---- postTodoCards: POST shape (injected http) ---------------------------
test('postTodoCards POSTs skill/data with type=todo merge=upsert', async () => {
  let captured;
  const httpPost = async (url, token, body) => { captured = { url, token, body }; return { ok: true }; };
  const item = buildTodoItem({ dedupKey: 'k', payload: { icon: '🧠', title: 't', prompt: 'p' } });

  const res = await postTodoCards(
    { skill: 'brainstorming', items: [item], token: 'tok', server: 'http://javis-server:8000' },
    { httpPost }
  );

  assert.deepEqual(res, { ok: true });
  assert.match(captured.url, /\/api\/skill\/data$/);
  assert.equal(captured.token, 'tok');
  assert.equal(captured.body.skill, 'brainstorming');
  assert.equal(captured.body.type, 'todo');
  assert.equal(captured.body.merge, 'upsert');
  assert.equal(captured.body.items.length, 1);
  assert.equal(captured.body.items[0].status, 'pending');
});

test('postTodoCards validates skill + non-empty items', async () => {
  const httpPost = async () => ({});
  await assert.rejects(
    postTodoCards({ skill: '', items: [{}], token: 't', server: 's' }, { httpPost }),
    /skill name/
  );
  await assert.rejects(
    postTodoCards({ skill: 'brainstorming', items: [], token: 't', server: 's' }, { httpPost }),
    /non-empty items/
  );
});
