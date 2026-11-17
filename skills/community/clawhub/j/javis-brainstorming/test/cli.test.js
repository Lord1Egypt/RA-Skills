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
    { httpGet: async () => payload, now: NOW, emit: (o) => { emitted = o; }, ...makeStore() }
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
    { httpGet: async (url) => { calledUrl = url; return payload; }, now: NOW, emit: (o) => { emitted = o; }, ...makeStore() }
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
    { httpGet: async () => payload, now: NOW, emit: (o) => { emitted = o; }, ...makeStore() }
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
  // `seen` is TTL-pruned against the REAL clock, so the entry the first push
  // records must be stamped with a real-clock `now` — the frozen NOW fixture
  // ages past SEEN_TTL_DAYS and this test silently stops testing dedup.
  const now = () => new Date().toISOString();

  await doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), ...store, now });
  assert.equal(client.calls.write.length, 1);

  await doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), ...store, now });
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

// ---- the remembered session-window map -----------------------------------
// Spec: docs/superpowers/specs/2026-09-11-brainstorming-card-time-anchor-design.md
//   §B fetch persists every returned session's raw instants in
//      state.sessionWindows (TTL-pruned on seen_at, capped at 500)
//   §C push resolves the window from the UNION of that map and any piped
//      `sessions`, the piped copy overriding by session_id
//   §D when both sources miss, the card is written with NO dates — never a
//      time-based last resort
// pruneByTtl measures against the real clock, so a pre-seeded `seen_at` is
// built relative to Date.now(), never off the frozen NOW fixture.
const FRESH = new Date(Date.now() - 2 * 86400 * 1000).toISOString();
const REMEMBERED = {
  'sess-1': {
    started_at: '2026-06-09T19:05:00.000Z',
    ended_at: '2026-06-09T19:30:00.000Z',
    seen_at: FRESH,
  },
};

test('doPush with a BARE card object stamps the window from the remembered sessionWindows map', async () => {
  // THE regression test: the agent pipes only the card — no `sessions` — and the
  // card must still land on the day its source session was captured.
  const client = makeClient();
  const store = makeStore({ userId: 'self', sessionWindows: REMEMBERED });
  const card = normalizeCard({ ...SAMPLE_CARD, source_refs: ['sess-1'] });

  await captureLogs(() =>
    doPush({ token: 't', client, card, tz: TZ, ...store, now: NOW }));

  const [item] = client.calls.write[0];
  assert.equal(item.start_at, '2026-06-09T12:05:00', 'anchored from the remembered map alone');
  assert.equal(item.end_at, '2026-06-09T12:30:00');
  assert.doesNotMatch(item.start_at, /[Z+]/, 'naive LOCAL wall-clock — no zone designator');
  assert.ok(!('start_at' in item.payload), 'dates are item-level, never payload-level');
  assert.deepEqual(store.box.state.sessionWindows, REMEMBERED, 'push does not rewrite the map');
});

test('doPush with piped sessions and an EMPTY map still stamps the window (the existing path)', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self', sessionWindows: {} });
  const sessions = [
    { session_id: 'sess-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' },
  ];

  await captureLogs(() =>
    doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), sessions, tz: TZ, ...store, now: NOW }));

  const [item] = client.calls.write[0];
  assert.equal(item.start_at, '2026-06-09T12:05:00');
  assert.equal(item.end_at, '2026-06-09T12:30:00');
});

test('doPush lets a piped session override the remembered one for the same session_id', async () => {
  const client = makeClient();
  const store = makeStore({ userId: 'self', sessionWindows: REMEMBERED });
  const sessions = [
    { session_id: 'sess-1', source: 'audio', started_at: '2026-06-09T21:00:00.000Z', ended_at: '2026-06-09T21:45:00.000Z' },
  ];

  await captureLogs(() =>
    doPush({ token: 't', client, card: normalizeCard({ ...SAMPLE_CARD, source_refs: ['sess-1'] }), sessions, tz: TZ, ...store, now: NOW }));

  const [item] = client.calls.write[0];
  assert.equal(item.start_at, '2026-06-09T14:00:00', 'the fresher piped read wins');
  assert.equal(item.end_at, '2026-06-09T14:45:00');
});

test('doPush with NEITHER source writes the card undated and still reports success', async () => {
  // §D: no time-based last resort. An unknown source session costs the card its
  // day; it never gets a guessed one.
  const client = makeClient();
  const store = makeStore({ userId: 'self', sessionWindows: { 'other-session': { started_at: '2026-06-09T19:05:00.000Z', seen_at: FRESH } } });

  const logs = await captureLogs(() =>
    doPush({ token: 't', client, card: normalizeCard(SAMPLE_CARD), tz: TZ, ...store, now: NOW }));

  assert.equal(client.calls.write.length, 1, 'the card is still written');
  const [item] = client.calls.write[0];
  assert.ok(!('start_at' in item), 'no invented date');
  assert.ok(!('end_at' in item));
  assert.equal(item.status, 'pending');
  assert.equal(Object.keys(store.box.state.seen).length, 1);
  assert.equal(logs.at(-1), `Wrote 1 brainstorm to-do card (${SAMPLE_CARD.title}). Chat digest: delivered.`);
});

// push holds no whole-state snapshot across its network round-trips. §B's memory
// lives in the same state file but belongs to `fetch`, so a push that saved the
// object it loaded before client.write/client.digest would revert a window a
// concurrent fetch remembered mid-flight — and the next bare-card push citing
// that session would write the card undated, the exact failure §B removes.
test('doPush re-reads state before saving, so a concurrent fetch\'s sessionWindows survive', async () => {
  const store = makeStore({ userId: 'self', sessionWindows: {}, seen: {} });
  const card = normalizeCard({ ...SAMPLE_CARD, source_refs: ['sess-1'] });
  const written = [];
  // Both awaited round-trips interleave a concurrent writer: the skill_data
  // write races a `fetch` remembering a window, the digest races another push
  // remembering its own card.
  const client = {
    write: async (_token, items) => {
      written.push(items);
      const s = store.load();
      s.sessionWindows = { ...(s.sessionWindows || {}), 'sess-9': { started_at: '2026-06-10T18:00:00.000Z', ended_at: '2026-06-10T18:20:00.000Z', seen_at: FRESH } };
      store.save(s);
    },
    digest: async () => {
      const s = store.load();
      s.seen = { ...(s.seen || {}), 'a-concurrent-card|feedface': FRESH };
      store.save(s);
    },
  };

  await captureLogs(() => doPush({ token: 't', client, card, tz: TZ, ...store, now: NOW }));

  assert.deepEqual(store.box.state.sessionWindows, {
    'sess-9': { started_at: '2026-06-10T18:00:00.000Z', ended_at: '2026-06-10T18:20:00.000Z', seen_at: FRESH },
  }, "the concurrent fetch's remembered window is NOT reverted by push's save");
  assert.deepEqual(Object.keys(store.box.state.seen).sort(), ['a-concurrent-card|feedface', card.dedupKey].sort(),
    'both this run\'s card and the concurrently-seen one are kept');
  assert.equal(store.box.state.lastRunAt, NOW());
  assert.equal(store.box.state.userId, 'self', 'unrelated keys survive the merge');
  assert.equal(written.length, 1);
});

test('doPush early returns also merge into a freshly read state', async () => {
  // The no-card and already-seen branches take the same commit path, so neither
  // can write a stale snapshot back over a key push does not own.
  const seenKey = normalizeCard(SAMPLE_CARD).dedupKey;
  for (const deps of [{ card: null }, { card: normalizeCard(SAMPLE_CARD) }]) {
    const store = makeStore({ userId: 'self', sessionWindows: REMEMBERED, seen: { [seenKey]: FRESH } });
    await captureLogs(() => doPush({ token: 't', client: makeClient(), tz: TZ, ...store, now: NOW, ...deps }));
    assert.deepEqual(store.box.state.sessionWindows, REMEMBERED, 'the remembered map is untouched by push');
    assert.equal(store.box.state.lastRunAt, NOW());
  }
});

test('doFetch writes each returned session into sessionWindows and leaves seen/lastRunAt untouched', async () => {
  const store = makeStore({
    userId: 'self',
    seen: { 'an-old-card|deadbeef': FRESH },
    lastRunAt: FRESH,
  });
  const payload = {
    sessions: [
      { session_id: 'aud-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' },
      // The LIVE wire shape: epoch seconds, normalized to a raw ISO instant.
      { id: 'aud-2', source: 'audio', started_at: 1781031900, ended_at: 1781033400 },
      { session_id: 'no-times', source: 'audio', transcript: 'nothing to remember' },
    ],
  };
  await doFetch(
    { token: 't', sessionFilter: null, kbdFilter: null, hours: 24, limit: 50, tz: TZ },
    { httpGet: async () => payload, now: NOW, emit: () => {}, ...store }
  );

  const windows = store.box.state.sessionWindows;
  assert.deepEqual(Object.keys(windows).sort(), ['aud-1', 'aud-2'], 'keyed by session_id OR id; a session with no usable started_at is not remembered');
  assert.deepEqual(windows['aud-1'], {
    started_at: '2026-06-09T19:05:00.000Z',
    ended_at: '2026-06-09T19:30:00.000Z',
    seen_at: NOW(),
  });
  assert.equal(windows['aud-2'].started_at, '2026-06-09T19:05:00.000Z', 'epoch seconds stored as a RAW ISO instant');
  assert.doesNotMatch(windows['aud-1'].started_at, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/, 'raw instants, not naive-local');
  assert.deepEqual(store.box.state.seen, { 'an-old-card|deadbeef': FRESH }, '`seen` is fetch-untouched');
  assert.equal(store.box.state.lastRunAt, FRESH, '`lastRunAt` is push-owned');
});

// ---- tz: the second thing push must not depend on the agent re-piping -------
// Found on prod 2026-09-12: the container runs with TZ unset, so a bare card
// (no piped tz) resolved to UTC and toNaiveLocal wrote the UTC wall-clock as if
// it were local — 20:12 for a session that started 13:12 in the user's zone. An
// evening session lands on the NEXT DAY, which is the placement bug the journal
// window exists to prevent.
test('doFetch remembers the SERVER tz; push anchors a bare card in it even when the container is UTC', async () => {
  const store = makeStore({ userId: 'self' });
  const savedTz = process.env.TZ;
  try {
    process.env.TZ = 'UTC';  // the container, faithfully
    await doFetch(
      { token: 't', sessionFilter: null, kbdFilter: null, hours: 24, limit: 50 },
      {
        httpGet: async () => ({
          tz: 'America/Los_Angeles',
          sessions: [{ session_id: 'sess-tz', source: 'audio', started_at: '2026-09-11T20:12:21.053Z', ended_at: '2026-09-11T20:14:57.432Z' }],
        }),
        now: NOW, emit: () => {}, ...store,
      }
    );
    assert.equal(store.box.state.tz, 'America/Los_Angeles', 'fetch records the server tz');

    const client = makeClient();
    await doPush({
      token: 't', client,
      card: normalizeCard({ ...SAMPLE_CARD, title: 'tz probe', source_refs: ['sess-tz'] }),
      now: NOW, ...store,
    });
    const item = client.calls.write[0][0];
    assert.equal(item.start_at, '2026-09-11T13:12:21', 'anchored in the USER tz, not the container UTC');
    assert.equal(item.end_at, '2026-09-11T13:14:57');
  } finally {
    if (savedTz === undefined) delete process.env.TZ; else process.env.TZ = savedTz;
  }
});

test('a piped tz still wins over the remembered one', async () => {
  const store = makeStore({ userId: 'self', tz: 'America/Los_Angeles', sessionWindows: {
    'sess-tz': { started_at: '2026-09-11T20:12:21.053Z', seen_at: NOW() },
  } });
  const client = makeClient();
  await doPush({
    token: 't', client, tz: 'Asia/Tokyo',
    card: normalizeCard({ ...SAMPLE_CARD, title: 'piped tz probe', source_refs: ['sess-tz'] }),
    now: NOW, ...store,
  });
  assert.equal(client.calls.write[0][0].start_at, '2026-09-12T05:12:21', 'piped Tokyo beats remembered LA');
});

test('doFetch does NOT remember a tz the server did not supply', async () => {
  const store = makeStore({ userId: 'self' });
  await doFetch(
    { token: 't', sessionFilter: null, kbdFilter: null, hours: 24, limit: 50 },
    { httpGet: async () => ({ sessions: [{ session_id: 's1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z' }] }),
      now: NOW, emit: () => {}, ...store }
  );
  assert.equal(store.box.state.tz, undefined,
    'persisting a fallback-derived tz would make every later card stickily wrong');
});

test('doFetch --session remembers EVERY fetched session, not just the one the envelope narrows to', async () => {
  const store = makeStore({ userId: 'self' });
  const payload = {
    sessions: [
      { session_id: 'aud-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z', transcript: 'the unit' },
      { session_id: 'aud-2', source: 'audio', started_at: '2026-06-09T17:00:00.000Z', ended_at: '2026-06-09T17:20:00.000Z', transcript: 'a sibling' },
      { session_id: 'aud-3', source: 'audio', started_at: '2026-06-09T15:00:00.000Z', transcript: 'another sibling' },
    ],
  };
  let emitted;
  await doFetch(
    { token: 't', sessionFilter: 'aud-1', kbdFilter: null, hours: 24, limit: 50, tz: TZ },
    { httpGet: async () => payload, now: NOW, emit: (o) => { emitted = o; }, ...store }
  );

  // The envelope still narrows -- the agent sees only the dispatcher's unit.
  assert.equal(emitted.sessions.length, 1, 'the envelope is still filtered to the unit');
  assert.equal(emitted.sessions[0].session_id, 'aud-1');

  // The memory does not. A card citing a sibling from the same fetch still gets its day.
  assert.deepEqual(
    Object.keys(store.box.state.sessionWindows).sort(),
    ['aud-1', 'aud-2', 'aud-3'],
    'every fetched session is remembered, filtered or not'
  );

  // And push can anchor from a sibling the envelope never carried.
  const client = makeClient();
  await doPush({
    token: 't',
    client,
    card: normalizeCard({ ...SAMPLE_CARD, source_refs: ['aud-2'] }),
    now: NOW,
    ...store,
  });
  const item = client.calls.write[0][0];
  assert.equal(item.start_at, '2026-06-09T10:00:00', 'anchored from a sibling session the envelope did not carry');
  assert.equal(item.end_at, '2026-06-09T10:20:00');
});

test('doFetch records started_at alone for a session with no ended_at; push then stamps start_at only', async () => {
  const store = makeStore({ userId: 'self' });
  const payload = {
    sessions: [{ session_id: 'sess-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z' }],
  };
  await doFetch(
    { token: 't', sessionFilter: null, kbdFilter: null, hours: 24, limit: 50, tz: TZ },
    { httpGet: async () => payload, now: NOW, emit: () => {}, ...store }
  );
  assert.deepEqual(store.box.state.sessionWindows['sess-1'], {
    started_at: '2026-06-09T19:05:00.000Z',
    seen_at: NOW(),
  }, 'ended_at is omitted, not written null');

  const client = makeClient();
  await captureLogs(() =>
    doPush({ token: 't', client, card: normalizeCard({ ...SAMPLE_CARD, source_refs: ['sess-1'] }), tz: TZ, ...store, now: NOW }));

  const [item] = client.calls.write[0];
  assert.equal(item.start_at, '2026-06-09T12:05:00');
  assert.ok(!('end_at' in item), "buildTodoItem's rule: an end only beside a start");
});

test('doFetch returning zero sessions leaves the existing sessionWindows map intact', async () => {
  const store = makeStore({ userId: 'self', sessionWindows: REMEMBERED, seen: { k: FRESH } });
  await doFetch(
    { token: 't', sessionFilter: 'no-such-session', kbdFilter: null, hours: 24, limit: 50, tz: TZ },
    { httpGet: async () => ({ sessions: [] }), now: NOW, emit: () => {}, ...store }
  );
  assert.deepEqual(store.box.state.sessionWindows, REMEMBERED, 'an empty fetch never clears the map');
  assert.deepEqual(store.box.state.seen, { k: FRESH });
});

test('doFetch still emits the envelope when the state write fails (remembering is non-fatal)', async () => {
  let emitted;
  const logs = await captureLogs(() => doFetch(
    { token: 't', sessionFilter: null, kbdFilter: null, hours: 24, limit: 50, tz: TZ },
    {
      httpGet: async () => ({ sessions: [{ session_id: 'aud-1', started_at: '2026-06-09T19:05:00.000Z' }] }),
      now: NOW,
      emit: (o) => { emitted = o; },
      load: () => ({ userId: 'self' }),
      save: () => { throw new Error('EROFS: read-only file system'); },
    }
  ));
  assert.equal(emitted.sessions.length, 1, 'the agent still gets its envelope');
  assert.equal(emitted.reference_date, '2026-06-03');
  assert.equal(logs.length, 0, 'the envelope goes through emit, the warning through console.error');
});
