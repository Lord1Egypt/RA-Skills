'use strict';

// Behavioral tests for the load-bearing CLI functions in
// scripts/brainstorming.js. The pure helpers are covered by lib.test.js and the
// to-do payload by todo-card.test.js; here we exercise doFetch / doPush /
// normalizeCard through injected IO (an http stub, a card object, and in-memory
// load/save) so the spec's correctness claims are actually asserted.
//
// Spec: docs/superpowers/specs/2026-06-09-brainstorming-skill-design.md
//   - single-unit fetch --session / --kbd-input still emit the anchor
//   - push dedups via the card-level `seen` map (no per-unit gating)
//   - a discernible card is written type="todo" status="pending" with a composed prompt
//   - no discernible goal (no title) -> nothing written

const { test } = require('node:test');
const assert = require('node:assert/strict');

const {
  doFetch,
  doPush,
  pushDigest,
  normalizeCard,
  defaultSubtitle,
} = require('../scripts/brainstorming');

// A recording push client: captures every write() (skill_data) and digest()
// (agent push) call so a test can assert exactly what hit each endpoint. The
// digest mock records the RAW card doPush forwarded through the seam; the
// content the real client (pushDigest) builds from that card is pinned
// separately by the fetch-stub tests below.
function makeClient() {
  const calls = { write: [], digest: [] };
  return {
    calls,
    write: async (_token, items) => { calls.write.push(items); },
    digest: async (_token, card) => { calls.digest.push(card); },
  };
}

// Run `fn` with global.fetch stubbed, recording every call; always restores.
async function withFetchStub(impl, fn) {
  const calls = [];
  const orig = global.fetch;
  global.fetch = async (url, opts) => { calls.push({ url, opts }); return impl(url, opts); };
  try { await fn(calls); } finally { global.fetch = orig; }
}

// Capture console.log/error around a doPush so the summary line is assertable.
async function captureLogs(fn) {
  const logs = [];
  const origLog = console.log;
  const origErr = console.error;
  console.log = (...a) => logs.push(a.join(' '));
  console.error = () => {};
  try { await fn(); } finally { console.log = origLog; console.error = origErr; }
  return logs;
}

function makeStore(initial) {
  const box = { state: initial ? JSON.parse(JSON.stringify(initial)) : { userId: 'self' } };
  return {
    box,
    load: () => JSON.parse(JSON.stringify(box.state)),
    save: (s) => { box.state = JSON.parse(JSON.stringify(s)); },
  };
}

const TZ = 'America/Los_Angeles';
const NOW = () => '2026-06-03T12:00:00.000Z';

const SAMPLE_CARD = {
  title: 'Intro Javis to the OpenClaw community',
  goal: 'introduce Javis to the OpenClaw community, for non-engineer users',
  request: ['an attention hook', 'a step-by-step demo/onboarding flow'],
  source_refs: ['sess-1', 'sess-2'],
};

// ---- fetch: single-unit filtering still emits the anchor -----------------
test('doFetch --session keeps only the matching audio session and emits the anchor', async () => {
  const payload = {
    sessions: [
      { session_id: 'aud-1', source: 'audio', transcript: 'A' },
      { session_id: 'aud-2', source: 'audio', transcript: 'B' },
      { session_id: 'aud-1', source: 'keyboard', transcript: 'collision' },
    ],
  };
  let emitted;
  await doFetch(
    { token: 't', sessionFilter: 'aud-1', kbdFilter: null, hours: 24, limit: 50, tz: TZ },
    { httpGet: async () => payload, now: NOW, emit: (o) => { emitted = o; } }
  );
  assert.equal(emitted.sessions.length, 1);
  assert.equal(emitted.sessions[0].session_id, 'aud-1');
  assert.equal(emitted.sessions[0].source, 'audio');
  assert.equal(emitted.reference_time_utc, NOW());
  assert.equal(emitted.reference_time, '2026-06-03T05:00:00');
  assert.equal(emitted.reference_date, '2026-06-03');
  assert.equal(emitted.reference_weekday, 'Wednesday');
  assert.equal(emitted.tz, TZ);
});

test('doFetch --kbd-input resolves one row via the dedicated keyboard-input endpoint', async () => {
  let calledUrl;
  const payload = {
    sessions: [
      { session_id: '4217', source: 'keyboard', started_at: 1, ended_at: 1, transcript: 'targeted input' },
    ],
  };
  let emitted;
  await doFetch(
    { token: 't', sessionFilter: null, kbdFilter: '4217', hours: 24, limit: 50, tz: TZ },
    { httpGet: async (url) => { calledUrl = url; return payload; }, now: NOW, emit: (o) => { emitted = o; } }
  );
  assert.match(calledUrl, /\/api\/transcripts\/keyboard-input\/4217$/);
  assert.doesNotMatch(calledUrl, /transcripts\/recent/);
  assert.equal(emitted.sessions.length, 1);
  assert.equal(emitted.sessions[0].source, 'keyboard');
});

test('doFetch with no filter returns the whole window unchanged (manual path)', async () => {
  const payload = {
    sessions: [
      { session_id: 'a', source: 'audio', transcript: 'A' },
      { session_id: 'b', source: 'keyboard', transcript: 'B' },
    ],
  };
  let emitted;
  await doFetch(
    { token: 't', sessionFilter: null, kbdFilter: null, hours: 24, limit: 50, tz: TZ },
    { httpGet: async () => payload, now: NOW, emit: (o) => { emitted = o; } }
  );
  assert.equal(emitted.sessions.length, 2);
});

// ---- normalizeCard: compose the prompt + defaults ------------------------
test('normalizeCard composes the prompt and fills icon/subtitle/dedupKey defaults', () => {
  const card = normalizeCard(SAMPLE_CARD);
  assert.equal(card.title, SAMPLE_CARD.title);
  assert.equal(card.icon, '🧠');
  assert.equal(card.subtitle, 'Brainstorm · 2 sessions');
  assert.match(card.prompt, /^I want to introduce Javis to the OpenClaw community/);
  assert.match(card.prompt, /session_id\(s\): sess-1, sess-2\./);
  assert.match(card.prompt, /^- an attention hook$/m);
  assert.match(card.prompt, /content-brainstorming flow/);
  assert.ok(card.dedupKey && card.dedupKey.includes('|'));
  assert.equal(card.sourceRef, 'sess-1');
});

test('normalizeCard returns null for a card with no title (silent no-card outcome)', () => {
  assert.equal(normalizeCard({ goal: 'something' }), null);
  assert.equal(normalizeCard(null), null);
  assert.equal(normalizeCard('x'), null);
  assert.equal(normalizeCard([]), null);
});

test('normalizeCard honors an agent-supplied explicit prompt and dedup_key', () => {
  const card = normalizeCard({
    title: 'My deck', goal: 'a deck', dedup_key: 'fixed-key', prompt: 'use THIS exact prompt',
  });
  assert.equal(card.prompt, 'use THIS exact prompt');
  assert.equal(card.dedupKey, 'fixed-key');
});

test('defaultSubtitle pluralizes by session count', () => {
  assert.equal(defaultSubtitle([]), 'Brainstorm');
  assert.equal(defaultSubtitle(['a']), 'Brainstorm');
  assert.equal(defaultSubtitle(['a', 'b']), 'Brainstorm · 2 sessions');
});

// ---- push: write a type=todo pending card + record in `seen` -------------
test('doPush writes one type=todo pending item, delivers the digest, and records it in `seen`', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });
  const card = normalizeCard(SAMPLE_CARD);

  const logs = await captureLogs(() =>
    doPush({ token: 't', client, card, ...store, now: NOW }));

  assert.equal(client.calls.write.length, 1);
  const [item] = client.calls.write[0];
  assert.equal(item.status, 'pending');
  assert.equal(item.payload.icon, '🧠');
  assert.equal(item.payload.title, SAMPLE_CARD.title);
  assert.match(item.payload.prompt, /content-brainstorming flow/);
  assert.ok(!('start_at' in item), 'no journal window without session times (never invented)');
  assert.ok(!('end_at' in item), 'no journal window without session times (never invented)');
  // doPush hands the UNMODIFIED normalized card through the digest seam; what
  // pushDigest renders from it is pinned by the fetch-stub tests below.
  assert.equal(client.calls.digest.length, 1);
  assert.deepEqual(client.calls.digest[0], card);
  assert.equal(Object.keys(store.box.state.seen).length, 1);
  // The summary line reports the digest delivery explicitly.
  assert.equal(logs.at(-1), `Wrote 1 brainstorm to-do card (${SAMPLE_CARD.title}). Chat digest: delivered.`);
});

test('doPush digest failure is non-fatal: card written, seen recorded, summary reports the reason', async () => {
  const client = makeClient();
  client.digest = async () => { throw new Error('POST /api/agent/push -> HTTP 502'); };
  const store = makeStore({ userId: 'self' });

  const logs = await captureLogs(() =>
    doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), ...store, now: NOW }));

  assert.equal(client.calls.write.length, 1, 'the pending card write still happens');
  assert.equal(Object.keys(store.box.state.seen).length, 1, 'the card is still recorded seen');
  assert.equal(logs.at(-1),
    `Wrote 1 brainstorm to-do card (${SAMPLE_CARD.title}). Chat digest FAILED: POST /api/agent/push -> HTTP 502`);
});

test('doPush dedups: an already-seen card is not re-written and sends no digest', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });

  await doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), ...store, now: NOW });
  assert.equal(client.calls.write.length, 1);

  await doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), ...store, now: NOW });
  assert.equal(client.calls.write.length, 1, 'no second write for a seen card');
  assert.equal(client.calls.digest.length, 1, 'no second digest for a seen card');
});

test('doPush with a null card (no discernible goal) writes nothing and sends no digest', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });

  await doPush({ token: 't', client, card: null, ...store, now: NOW });

  assert.equal(client.calls.write.length, 0, 'no write when there is no card');
  assert.equal(client.calls.digest.length, 0);
  assert.ok(!store.box.state.seen || Object.keys(store.box.state.seen).length === 0);
});

test('doPush can suppress the digest', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });

  await doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), ...store, now: NOW, digest: false });

  assert.equal(client.calls.write.length, 1, 'card still written');
  assert.equal(client.calls.digest.length, 0, 'digest suppressed');
});

// ---- pushDigest: the REAL request body, pinned against a literal ----------
// These exercise the production pushDigest (not the injected test seam) via a
// stubbed global fetch, so a regression in the {skill, content} body — e.g.
// reverting to the old generic nudge string or dropping the slug — fails here.
test('pushDigest POSTs {skill: slug, content: formatDigest(card), dedup_key} to /api/agent/push', async () => {
  const card = normalizeCard(SAMPLE_CARD);
  await withFetchStub(async () => ({ ok: true }), async (calls) => {
    await pushDigest('tok-1', card);
    assert.equal(calls.length, 1);
    assert.match(calls[0].url, /\/api\/agent\/push$/);
    assert.equal(calls[0].opts.method, 'POST');
    assert.equal(calls[0].opts.headers.Authorization, 'Bearer tok-1');
    assert.equal(calls[0].opts.headers['Content-Type'], 'application/json');
    const body = JSON.parse(calls[0].opts.body);
    assert.deepEqual(Object.keys(body).sort(), ['content', 'dedup_key', 'skill']);
    assert.equal(body.skill, 'javis-brainstorming');
    // The card's dedup_key rides on the push so javis-server derives a
    // deterministic per-card Agent Chat session (user, skill, dedup_key).
    assert.equal(body.dedup_key, card.dedupKey);
    // Expected content written out independently (NOT computed via formatDigest)
    // so this assertion can actually fail if the digest content regresses.
    assert.equal(body.content, [
      '## 🧠 Brainstorm — new card / 新腦力激盪',
      '',
      '- **Intro Javis to the OpenClaw community**',
      '  - 🎯 introduce Javis to the OpenClaw community, for non-engineer users',
      '  - 📋 an attention hook · a step-by-step demo/onboarding flow',
      '  - 📡 2 sessions',
      '',
      '✅ **Confirm** in the Calendar tab saves it to your calendar · **Discard** drops it · tap the card anytime to reopen this chat.',
    ].join('\n'));
  });
});

test('pushDigest forwards an explicit card dedup_key verbatim (per-card session key)', async () => {
  const card = normalizeCard({ ...SAMPLE_CARD, dedup_key: 'fixed-card-key' });
  assert.equal(card.dedupKey, 'fixed-card-key');
  await withFetchStub(async () => ({ ok: true }), async (calls) => {
    await pushDigest('tok-1', card);
    const body = JSON.parse(calls[0].opts.body);
    assert.equal(body.dedup_key, 'fixed-card-key');
  });
});

test('pushDigest throws with the HTTP status on a non-ok response', async () => {
  await withFetchStub(async () => ({ ok: false, status: 502 }), async () => {
    await assert.rejects(
      () => pushDigest('tok-1', normalizeCard(SAMPLE_CARD)),
      /POST \/api\/agent\/push -> HTTP 502/);
  });
});

// ---- push: the start_at/end_at journal window -----------------------------
// Spec 2026-06-10 (brainstorm card tap-and-confirm): push stamps the item's
// OPTIONAL start_at/end_at from the SOURCE session's started_at/ended_at —
// earliest session by started_at among the card's source_refs, that SAME
// session's ended_at — serialized naive-local in the resolved tz (the
// calendar-extractor convention). Missing/malformed times => fields omitted.
test('doPush stamps start_at/end_at from the source session times, naive-local in tz', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });
  const sessions = [
    { session_id: 'sess-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' },
  ];
  const card = normalizeCard({ ...SAMPLE_CARD, source_refs: ['sess-1'] });

  await captureLogs(() =>
    doPush({ token: 't', client, card, sessions, tz: TZ, ...store, now: NOW }));

  const [item] = client.calls.write[0];
  // 19:05Z/19:30Z @ America/Los_Angeles == the 12:05–12:30 PM journal window.
  assert.equal(item.start_at, '2026-06-09T12:05:00');
  assert.equal(item.end_at, '2026-06-09T12:30:00');
  assert.doesNotMatch(item.start_at, /[Z+]/, 'naive LOCAL wall-clock — no zone designator');
  assert.equal(item.status, 'pending');
  assert.ok(!('start_at' in item.payload), 'dates are item-level, never payload-level');
});

test('doPush with multiple source_refs uses the earliest session and that SAME session\'s ended_at', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });
  const sessions = [
    { session_id: 'sess-2', source: 'audio', started_at: '2026-06-09T22:00:00.000Z', ended_at: '2026-06-09T23:00:00.000Z' },
    { session_id: 'sess-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' },
  ];

  await captureLogs(() =>
    doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), sessions, tz: TZ, ...store, now: NOW }));

  const [item] = client.calls.write[0];
  assert.equal(item.start_at, '2026-06-09T12:05:00', 'earliest started_at wins');
  assert.equal(item.end_at, '2026-06-09T12:30:00', 'the earliest session\'s OWN end, not the later one\'s');
});

test('doPush omits start_at/end_at entirely when session times are missing or malformed', async () => {
  for (const sessions of [
    [],                                                            // no sessions piped at all
    [{ session_id: 'sess-1', source: 'audio' }],                   // no started_at
    [{ session_id: 'sess-1', started_at: 'not-a-date' }],          // malformed started_at
    [{ session_id: 'other', started_at: '2026-06-09T19:05:00Z' }], // no ref match
  ]) {
    const client = makeClient();
    const store = makeStore({ userId: 'self' });
    await captureLogs(() =>
      doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), sessions, tz: TZ, ...store, now: NOW }));
    const [item] = client.calls.write[0];
    assert.ok(!('start_at' in item), `omitted for ${JSON.stringify(sessions)}`);
    assert.ok(!('end_at' in item), `omitted for ${JSON.stringify(sessions)}`);
  }
});

test('doPush keeps start_at and omits only end_at when the source session has no usable ended_at', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });
  const sessions = [
    { session_id: 'sess-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z' },
  ];

  await captureLogs(() =>
    doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), sessions, tz: TZ, ...store, now: NOW }));

  const [item] = client.calls.write[0];
  assert.equal(item.start_at, '2026-06-09T12:05:00');
  assert.ok(!('end_at' in item));
});

test('doPush does NOT write per-unit gating state (server owns run-once)', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self' });
  await doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), ...store, now: NOW });
  assert.ok(!store.box.state.extractedUnits, 'no per-unit gating state is written');
});
