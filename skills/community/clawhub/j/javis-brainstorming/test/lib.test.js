'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');

const {
  SEEN_TTL_DAYS,
  resolveTz,
  toNaiveLocal,
  localAnchor,
  sessionWindow,
  todoDedupKey,
  composePrompt,
  formatDigest,
  pruneSeen,
} = require('../scripts/lib');

// ---- resolveTz: payload -> TZ env -> system ------------------------------
test('resolveTz prefers the payload tz, then TZ env, then the system zone', () => {
  const savedTz = process.env.TZ;
  try {
    process.env.TZ = 'America/New_York';
    assert.equal(resolveTz('Asia/Tokyo'), 'Asia/Tokyo');
    assert.equal(resolveTz('  Europe/Paris  '), 'Europe/Paris');
    assert.equal(resolveTz(null), 'America/New_York');
    assert.equal(resolveTz(''), 'America/New_York');
    delete process.env.TZ;
    const savedDTF = Intl.DateTimeFormat;
    try {
      Intl.DateTimeFormat = function () {
        return { resolvedOptions: () => ({ timeZone: 'Australia/Sydney' }) };
      };
      assert.equal(resolveTz(null), 'Australia/Sydney');
      Intl.DateTimeFormat = function () {
        return { resolvedOptions: () => ({ timeZone: '' }) };
      };
      assert.equal(resolveTz(null), 'UTC');
      Intl.DateTimeFormat = function () { throw new Error('no Intl'); };
      assert.equal(resolveTz(null), 'UTC');
    } finally {
      Intl.DateTimeFormat = savedDTF;
    }
  } finally {
    if (savedTz === undefined) delete process.env.TZ; else process.env.TZ = savedTz;
  }
});

// ---- naive-local wall-clock (anchor + journal-window serialization) ------
test('toNaiveLocal renders the instant as naive wall-clock in tz (no Z)', () => {
  assert.equal(toNaiveLocal('2026-06-06T04:00:00.000Z', 'America/Los_Angeles'), '2026-06-05T21:00:00');
  assert.doesNotMatch(toNaiveLocal('2026-06-06T04:00:00.000Z', 'America/Los_Angeles'), /[Z+]/);
  assert.equal(toNaiveLocal(null, 'America/Los_Angeles'), null);
  assert.equal(toNaiveLocal('not-a-date', 'America/Los_Angeles'), null);
});

test('localAnchor emits a local wall-clock anchor whose date is the tz-local "today"', () => {
  // 9:11 PM PDT Jun 4 == 2026-06-05T04:11Z. The anchor must carry the LOCAL date.
  const a = localAnchor('2026-06-05T04:11:00.000Z', 'America/Los_Angeles');
  assert.equal(a.reference_date, '2026-06-04');
  assert.equal(a.reference_time, '2026-06-04T21:11:00');
  assert.doesNotMatch(a.reference_time, /Z$/);
  assert.equal(a.reference_weekday, 'Thursday');
  assert.equal(a.reference_time_utc, '2026-06-05T04:11:00.000Z');
});

// ---- sessionWindow: the source-session journal window ---------------------
const TZ = 'America/Los_Angeles';

test('sessionWindow serializes the source session times as naive-local in tz', () => {
  const sessions = [
    { session_id: 's1', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' },
  ];
  // 19:05Z / 19:30Z == 12:05 / 12:30 PDT — the journal window the spec shows.
  assert.deepEqual(sessionWindow(sessions, ['s1'], TZ), {
    start_at: '2026-06-09T12:05:00',
    end_at: '2026-06-09T12:30:00',
  });
  assert.doesNotMatch(sessionWindow(sessions, ['s1'], TZ).start_at, /[Z+]/);
});

test('sessionWindow with multiple source_refs picks the EARLIEST session and that SAME session\'s ended_at', () => {
  const sessions = [
    { session_id: 'late', started_at: '2026-06-09T22:00:00.000Z', ended_at: '2026-06-09T23:00:00.000Z' },
    { session_id: 'early', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' },
    { session_id: 'unrelated', started_at: '2026-06-09T01:00:00.000Z', ended_at: '2026-06-09T02:00:00.000Z' },
  ];
  // 'unrelated' is earlier still but NOT among the refs — must be ignored.
  assert.deepEqual(sessionWindow(sessions, ['late', 'early'], TZ), {
    start_at: '2026-06-09T12:05:00',
    end_at: '2026-06-09T12:30:00', // the EARLY session's end, not the late one's
  });
});

test('sessionWindow omits both fields when no source session has a usable started_at', () => {
  assert.deepEqual(sessionWindow([], ['s1'], TZ), {});
  assert.deepEqual(sessionWindow(null, ['s1'], TZ), {});
  assert.deepEqual(sessionWindow([{ session_id: 's1' }], ['s1'], TZ), {});
  assert.deepEqual(sessionWindow([{ session_id: 's1', started_at: 'not-a-date' }], ['s1'], TZ), {});
  // Non-finite numerics are unusable — skipped.
  assert.deepEqual(sessionWindow([{ session_id: 's1', started_at: NaN, ended_at: NaN }], ['s1'], TZ), {});
  // No refs at all -> no window (we never guess a session).
  assert.deepEqual(sessionWindow([{ session_id: 's1', started_at: '2026-06-09T19:05:00Z' }], [], TZ), {});
});

test('sessionWindow accepts NUMERIC epoch seconds (the live javis-server wire contract)', () => {
  // javis-server emits started_at/ended_at as Optional[float] epoch seconds
  // (UTC instants) for BOTH audio and keyboard sessions on the two endpoints
  // this skill fetches. 1781031900 == 2026-06-09T19:05:00Z == 12:05 PDT.
  const sessions = [
    { session_id: 's1', started_at: 1781031900, ended_at: 1781033400 },
  ];
  assert.deepEqual(sessionWindow(sessions, ['s1'], TZ), {
    start_at: '2026-06-09T12:05:00',
    end_at: '2026-06-09T12:30:00',
  });
  // Fractional epoch seconds (server floats) and mixed numeric/string sessions
  // both resolve; earliest-numeric wins over a later ISO session.
  const mixed = [
    { session_id: 'late', started_at: '2026-06-09T22:00:00.000Z', ended_at: '2026-06-09T23:00:00.000Z' },
    { session_id: 'early', started_at: 1781031900.25, ended_at: 1781033400.75 },
  ];
  assert.deepEqual(sessionWindow(mixed, ['late', 'early'], TZ), {
    start_at: '2026-06-09T12:05:00',
    end_at: '2026-06-09T12:30:00',
  });
});

test('sessionWindow keeps start_at and omits only end_at when ended_at is missing/malformed', () => {
  const noEnd = sessionWindow(
    [{ session_id: 's1', started_at: '2026-06-09T19:05:00.000Z' }], ['s1'], TZ);
  assert.deepEqual(noEnd, { start_at: '2026-06-09T12:05:00' });
  const badEnd = sessionWindow(
    [{ session_id: 's1', started_at: '2026-06-09T19:05:00.000Z', ended_at: 'garbage' }], ['s1'], TZ);
  assert.deepEqual(badEnd, { start_at: '2026-06-09T12:05:00' });
});

test('sessionWindow matches sessions by session_id or id', () => {
  const viaId = sessionWindow(
    [{ id: 's1', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' }],
    ['s1'], TZ);
  assert.equal(viaId.start_at, '2026-06-09T12:05:00');
});

// ---- todoDedupKey --------------------------------------------------------
test('todoDedupKey is stable for equivalent cards and varies by title/goal', () => {
  const a = todoDedupKey({ title: 'Intro  Javis', goal: 'introduce Javis to the community' });
  const b = todoDedupKey({ title: 'intro javis', goal: '  introduce Javis to the community ' });
  assert.equal(a, b, 'whitespace/case-insensitive on title and goal');

  const otherTitle = todoDedupKey({ title: 'Pitch Javis', goal: 'introduce Javis to the community' });
  const otherGoal = todoDedupKey({ title: 'Intro Javis', goal: 'a totally different objective' });
  assert.notEqual(a, otherTitle, 'different title -> different key');
  assert.notEqual(a, otherGoal, 'same title, different goal -> different key (re-brainstorm is new)');
});

test('todoDedupKey is bounded (<=512 chars) even for very long goals', () => {
  const key = todoDedupKey({ title: 'x', goal: 'g'.repeat(5000) });
  assert.ok(key.length <= 512);
});

// ---- composePrompt: sample card -> expected prompt substrings ------------
test('composePrompt assembles the literal template with the card fields', () => {
  const prompt = composePrompt({
    goal: 'introduce Javis to the OpenClaw community, for non-engineer users',
    request: ['an attention hook', 'a step-by-step demo/onboarding flow'],
    source_refs: ['sess-aaa', 'sess-bbb'],
  });
  // Goal line.
  assert.match(prompt, /^I want to introduce Javis to the OpenClaw community, for non-engineer users\./m);
  // Source line names the javis_mcp connector and the session ids.
  assert.match(prompt, /Source: my Javis voice note\(s\), session_id\(s\): sess-aaa, sess-bbb\./);
  assert.match(prompt, /javis_mcp connector \(get_transcript_tool \/ search_transcripts_tool\)/);
  // Each request becomes a bullet.
  assert.match(prompt, /^- an attention hook$/m);
  assert.match(prompt, /^- a step-by-step demo\/onboarding flow$/m);
  // The literal content-brainstorming hand-off instruction is always present.
  assert.match(prompt, /Run the content-brainstorming flow: ask me clarifying questions one at a time/);
  assert.match(prompt, /produce a structured brief before drafting\./);
});

test('composePrompt degrades gracefully with no requests and no source_refs', () => {
  const prompt = composePrompt({ goal: 'organize my product launch ideas' });
  assert.match(prompt, /^I want to organize my product launch ideas\./m);
  // Falls back to a placeholder source hint and a generic bullet.
  assert.match(prompt, /session_id\(s\): \(see my recent voice notes\)/);
  assert.match(prompt, /^- a structured brief I can act on$/m);
});

// ---- formatDigest: Agent Chat markdown -----------------------------------
const DIGEST_FOOTER = '✅ **Confirm** in the Calendar tab saves it to your calendar · **Discard** drops it · tap the card anytime to reopen this chat.';

test('formatDigest renders the full calendar-style digest for a complete card', () => {
  const md = formatDigest({
    icon: '🧠',
    title: 'Intro Javis to the OpenClaw community',
    goal: 'introduce Javis to the OpenClaw community, for non-engineer users',
    request: ['an attention hook', 'a step-by-step demo/onboarding flow'],
    source_refs: ['sess-aaa', 'sess-bbb'],
  });
  assert.equal(md, [
    '## 🧠 Brainstorm — new card / 新腦力激盪',
    '',
    '- **Intro Javis to the OpenClaw community**',
    '  - 🎯 introduce Javis to the OpenClaw community, for non-engineer users',
    '  - 📋 an attention hook · a step-by-step demo/onboarding flow',
    '  - 📡 2 sessions',
    '',
    DIGEST_FOOTER,
  ].join('\n'));
});

test('formatDigest omits the 🎯 line for a goal-less card', () => {
  const md = formatDigest({ title: 'T', goal: '', request: ['r1'], source_refs: ['s1'] });
  assert.doesNotMatch(md, /🎯/);
  assert.match(md, /^ {2}- 📋 r1$/m);
});

test('formatDigest omits the 📋 line for a request-less card', () => {
  const md = formatDigest({ title: 'T', goal: 'g', request: [], source_refs: ['s1'] });
  assert.doesNotMatch(md, /📋/);
  assert.match(md, /^ {2}- 🎯 g$/m);
});

test('formatDigest pluralizes the 📡 session count and omits it at zero refs', () => {
  assert.doesNotMatch(formatDigest({ title: 'T', source_refs: [] }), /📡/);
  assert.match(formatDigest({ title: 'T', source_refs: ['a'] }), /^ {2}- 📡 1 session$/m);
  assert.match(formatDigest({ title: 'T', source_refs: ['a', 'b', 'c'] }), /^ {2}- 📡 3 sessions$/m);
});

test('formatDigest uses the card icon in the header when the agent overrode it', () => {
  assert.match(formatDigest({ title: 'T', icon: '🎨' }), /^## 🎨 Brainstorm — new card \/ 新腦力激盪$/m);
  // No override -> the default 🧠.
  assert.match(formatDigest({ title: 'T' }), /^## 🧠 Brainstorm — new card \/ 新腦力激盪$/m);
});

test('formatDigest collapses interior newlines in title/goal/request so multi-line LLM text cannot break the digest markdown', () => {
  const md = formatDigest({
    title: 'Line1\nLine2',
    goal: 'goal A\n## fake header',
    request: ['item\none', 'item\ttwo'],
    source_refs: ['s1'],
  });
  assert.equal(md, [
    '## 🧠 Brainstorm — new card / 新腦力激盪',
    '',
    '- **Line1 Line2**',
    '  - 🎯 goal A ## fake header',
    '  - 📋 item one · item two',
    '  - 📡 1 session',
    '',
    DIGEST_FOOTER,
  ].join('\n'));
  // No injected column-0 header line beyond the fixed digest header.
  assert.equal(md.split('\n').filter((l) => l.startsWith('## ')).length, 1);
});

test('formatDigest header and footer are fixed even on a bare card', () => {
  const md = formatDigest({ title: 'Bare' });
  assert.equal(md, [
    '## 🧠 Brainstorm — new card / 新腦力激盪',
    '',
    '- **Bare**',
    '',
    DIGEST_FOOTER,
  ].join('\n'));
});

// ---- pruning by TTL ------------------------------------------------------
test('pruneSeen drops entries older than TTL and unparseable ones', () => {
  const now = Date.now();
  const fresh = new Date(now - 1 * 86400 * 1000).toISOString();
  const stale = new Date(now - (SEEN_TTL_DAYS + 1) * 86400 * 1000).toISOString();
  const seen = { keep: fresh, drop: stale, bad: 'not-a-date' };
  const out = pruneSeen(seen);
  assert.deepEqual(Object.keys(out), ['keep']);
  assert.equal(out.keep, fresh);
});

test('pruneSeen on empty / missing map yields {}', () => {
  assert.deepEqual(pruneSeen(null), {});
  assert.deepEqual(pruneSeen({}), {});
});

test('prune honors a custom ttlDays', () => {
  const now = Date.now();
  const tenDaysAgo = new Date(now - 10 * 86400 * 1000).toISOString();
  assert.deepEqual(pruneSeen({ k: tenDaysAgo }, 5), {});
  assert.deepEqual(Object.keys(pruneSeen({ k: tenDaysAgo }, 30)), ['k']);
});
