'use strict';
const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const cli = require('../scripts/gmail-wiki-ingest.js');

function fakeFetch(impl) {
  const calls = [];
  const fn = async (url, init) => {
    calls.push({ url, init, body: JSON.parse(init.body) });
    return impl(url, init);
  };
  fn.calls = calls;
  return fn;
}

const ok = (payload) => async () => ({
  ok: true, status: 200, json: async () => payload,
});

const fail = (status, payload) => async () => ({
  ok: false, status, json: async () => payload,
});

/**
 * A private run-state file per test.
 *
 * `fetch` and `submit` write one as a side effect and `report` deletes it, so a
 * shared path would make this suite order-dependent — and the bundle's own
 * `data/last-run.json` belongs to whatever container the checkout is sitting
 * in, where clobbering it would destroy a real run's only evidence. Every test
 * that touches state therefore injects its own file under the OS temp dir, and
 * the whole directory goes at process exit rather than in an `after` hook, so
 * a test that throws mid-way still cleans up.
 */
const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), 'gmail-wiki-ingest-test-'));
process.on('exit', () => fs.rmSync(SCRATCH, { recursive: true, force: true }));

let scratchSeq = 0;
function statePath() {
  scratchSeq += 1;
  return path.join(SCRATCH, `last-run-${scratchSeq}.json`);
}

// The clock is injected rather than read, because the only thing separating
// today's run from a file left behind by a run that died yesterday is a
// six-hour window on `started_at`. Testing that by sleeping would take seven
// hours; testing it against wall time would make the suite's result depend on
// when it ran.
const T0 = Date.parse('2026-09-04T07:00:00Z');
const HOUR = 60 * 60 * 1000;

function deps(f, extra = {}) {
  return Object.assign({ fetch: f, token: 't', statePath: statePath(), now: T0 }, extra);
}

test('fetch posts the skill slug and the limit', async () => {
  const f = fakeFetch(ok({ status: 'ok', items: [] }));
  const out = await cli.doFetch({ limit: 7 }, deps(f));
  assert.equal(out.status, 'ok');
  assert.equal(f.calls.length, 1);
  assert.match(f.calls[0].url, /\/api\/skill\/candidates\/fetch$/);
  assert.deepEqual(f.calls[0].body, { skill: 'gmail-wiki-ingest', limit: 7 });
});

test('the gateway token travels as a bearer header', async () => {
  const f = fakeFetch(ok({ status: 'ok' }));
  await cli.doFetch({}, deps(f, { token: 'secret-token' }));
  assert.equal(f.calls[0].init.headers.Authorization, 'Bearer secret-token');
});

test('a non-2xx comes back as an envelope, not a throw', async () => {
  // The agent must be able to tell a failed call from an empty mailbox. A
  // thrown error mid-turn reads to it as neither.
  const f = fakeFetch(async () => ({
    ok: false, status: 404,
    json: async () => ({ detail: { error: 'unsupported_skill' } }),
  }));
  const out = await cli.doFetch({}, deps(f));
  assert.equal(out.status, 'error');
  assert.equal(out.error, 'unsupported_skill');
});

test('a network failure comes back as an envelope too', async () => {
  const f = fakeFetch(async () => { throw new Error('ECONNREFUSED'); });
  const out = await cli.doFetch({}, deps(f));
  assert.equal(out.status, 'error');
  assert.equal(out.error, 'network_error');
});

test('submit posts the verdict array verbatim', async () => {
  const f = fakeFetch(ok({ status: 'ok', high: 0, middle: 1, low: 0 }));
  const verdicts = [{ item_key: 't1', score: 0.7, category: 'correspondence', refs: [] }];
  const out = await cli.doSubmit(verdicts, deps(f));
  assert.equal(out.middle, 1);
  assert.deepEqual(f.calls[0].body, { skill: 'gmail-wiki-ingest', verdicts });
});

test('submit carries occurred_at through to the body untouched', async () => {
  // Which day a card files itself under is the skill's judgment (`rubric.md`
  // §5) and the server's to police, and the script is the wire between them
  // and nothing else. It must not whitelist the verdict's keys: the whole
  // reason the judgment lives in this bundle is that it can grow a field
  // without a server deploy, and a script that reshaped verdicts would put a
  // second deploy — of the bundle's code, not its prose — back in that path.
  const f = fakeFetch(ok({ status: 'ok', high: 0, middle: 1, low: 0 }));
  const verdicts = [{
    item_key: 't1',
    score: 0.7,
    category: 'correspondence',
    refs: [],
    reason: 'a receipt forwarded weeks after the purchase it records',
    occurred_at: '2026-09-04T17:22:00Z',
  }];
  const out = await cli.doSubmit(verdicts, deps(f));
  assert.equal(out.middle, 1);
  assert.deepEqual(f.calls[0].body, { skill: 'gmail-wiki-ingest', verdicts });
  // Spelled out separately from the deepEqual above, because that assertion
  // would still pass if a future change dropped the key on both sides.
  assert.equal(f.calls[0].body.verdicts[0].occurred_at, '2026-09-04T17:22:00Z');
});

test('a verdict with no occurred_at submits unchanged', async () => {
  // The field is optional the whole way down, and the fallback belongs to the
  // server — it holds the thread's real newest-message instant and the
  // container holds only its own clock. So an undated verdict must arrive
  // undated: a date stamped in here would be the run's time, not the mail's,
  // and it would file the card on the day it was judged while looking exactly
  // like a date the agent had chosen.
  const f = fakeFetch(ok({ status: 'ok', high: 0, middle: 1, low: 0 }));
  const verdicts = [{
    item_key: 't1',
    score: 0.7,
    category: 'correspondence',
    refs: [],
    reason: 'one sentence',
  }];
  const out = await cli.doSubmit(verdicts, deps(f));
  assert.equal(out.middle, 1);
  assert.deepEqual(f.calls[0].body, { skill: 'gmail-wiki-ingest', verdicts });
  assert.equal('occurred_at' in f.calls[0].body.verdicts[0], false);
});

test('submit refuses a non-array rather than coercing it', async () => {
  // An empty submit is MEANINGFUL: it says the batch was judged and nothing was
  // worth keeping, and it promotes the cursor past every item in it. Coercing a
  // malformed verdict list into that would skip mail permanently.
  const f = fakeFetch(ok({ status: 'ok' }));
  const out = await cli.doSubmit({ not: 'an array' }, deps(f));
  assert.equal(out.error, 'verdicts_must_be_an_array');
  assert.equal(f.calls.length, 0, 'nothing should have been posted');
});

test('an empty verdict array IS posted — it closes the batch', async () => {
  const f = fakeFetch(ok({ status: 'ok', promoted: true }));
  const out = await cli.doSubmit([], deps(f));
  assert.equal(out.promoted, true);
  assert.deepEqual(f.calls[0].body.verdicts, []);
});

test('the skill slug is not caller-settable', async () => {
  // The server validates it against registered adapters, but the CLI should
  // not be the thing that makes a wrong one reachable in the first place.
  const f = fakeFetch(ok({ status: 'ok' }));
  await cli.doSubmit([], deps(f));
  assert.equal(f.calls[0].body.skill, 'gmail-wiki-ingest');
});

// ---- content -------------------------------------------------------------
// The command that reverses this skill's oldest claim: bodies now enter the
// container, before approval, for a shortlist the agent picked. What these
// tests pin is the bound that replaced the old boundary — the request names
// keys and nothing else, it is capped, and what it brings back is handed to
// the agent and never written down.

test('content posts the item keys, and NO skill field', async () => {
  // The inverse of "the skill slug is not caller-settable". `fetch` and
  // `submit` name the skill because a gateway token identifies the user and
  // not the skill; this call has nothing to name, because the server answers
  // out of the batch its own `fetch` staged. A `skill` field here would be the
  // one argument the endpoint exists not to have.
  const f = fakeFetch(ok({ status: 'ok', items: [{ item_key: 't1', text: 'hello' }], unavailable: [] }));
  const out = await cli.doContent(['t1', 't2'], deps(f));

  assert.equal(out.status, 'ok');
  assert.match(f.calls[0].url, /\/api\/skill\/candidates\/content$/);
  assert.deepEqual(f.calls[0].body, { item_keys: ['t1', 't2'] });
  assert.equal(
    Object.prototype.hasOwnProperty.call(f.calls[0].body, 'skill'), false,
    'the skill is bound server-side from the staged batch',
  );
  assert.equal(f.calls[0].init.headers.Authorization, 'Bearer t');
});

test('content refuses a non-array rather than coercing it', async () => {
  const f = fakeFetch(ok({ status: 'ok' }));
  const out = await cli.doContent({ not: 'an array' }, deps(f));
  assert.equal(out.error, 'item_keys_must_be_an_array');
  assert.equal(f.calls.length, 0, 'nothing should have been posted');
});

test('content asks for at most twelve threads, de-duplicated first', async () => {
  // The budget, mirrored from the server so an over-long shortlist is trimmed
  // here rather than answered as a wall of `unavailable` there. A duplicate
  // must not spend one of the twelve.
  const f = fakeFetch(ok({ status: 'ok', items: [], unavailable: [] }));
  const keys = ['t1', 't1', ...Array.from({ length: 20 }, (_, i) => `x${i}`)];
  await cli.doContent(keys, deps(f));

  const sent = f.calls[0].body.item_keys;
  assert.equal(sent.length, cli.CONTENT_BATCH_MAX);
  assert.equal(sent.length, 12);
  assert.deepEqual(sent.slice(0, 3), ['t1', 'x0', 'x1'], 'the duplicate was collapsed, not dropped');
  assert.equal(new Set(sent).size, sent.length);
});

test('content records the arithmetic and never the bodies', async () => {
  // The run-state file is the one thing in the container built to outlive the
  // turn, which is exactly what a body must not do. What lands is how many
  // were asked for, how many arrived, and which keys the server would not
  // answer — the reason strings are the server's word, not the agent's.
  const BODY_NONCE = 'E2E-BODY-NONCE-4471';
  const f = fakeFetch(ok({
    status: 'ok',
    items: [
      { item_key: 't1', text: `From: Ada\n\n${BODY_NONCE}` },
      { item_key: 't2', text: '' },
    ],
    unavailable: [
      { item_key: 't3', reason: 'not_in_batch' },
      { item_key: 't4', reason: 'fetch_failed' },
    ],
  }));
  const d = deps(f);
  cli.writeState({ started_at: new Date(T0 - HOUR).toISOString(), n_items: 4, items: [] }, d);

  await cli.doContent(['t1', 't2', 't3', 't4'], d);

  const raw = fs.readFileSync(d.statePath, 'utf-8');
  assert.equal(raw.includes(BODY_NONCE), false, 'no body may reach the disk');

  const state = JSON.parse(raw);
  assert.equal(state.content_requested, 4);
  assert.equal(state.content_read, 1, 'an empty text is not a body that was read');
  assert.deepEqual(state.content_unavailable, [
    { item_key: 't3', reason: 'not_in_batch' },
    { item_key: 't4', reason: 'fetch_failed' },
  ]);
});

test('content merges into the run state and never claims a submit', async () => {
  // `fetch` overwrites; `submit` and `content` merge. A `content` that
  // overwrote would erase `items[]` and the digest would lose every subject
  // line. Writing `submitted_at` would be worse still: that key is the flag
  // the footer reads to choose its shape.
  const f = router({
    '/candidates/fetch': ok({
      status: 'ok',
      items: [{ thread_id: 't1', subject: 'Contract v3', from: 'Ada' }],
      filtered: {},
    }),
    '/candidates/content': ok({
      status: 'ok', items: [{ item_key: 't1', text: 'body' }], unavailable: [],
    }),
  });
  const d = deps(f);

  await cli.doFetch({}, d);
  await cli.doContent(['t1'], d);

  const state = JSON.parse(fs.readFileSync(d.statePath, 'utf-8'));
  assert.deepEqual(state.items, [{ thread_id: 't1', subject: 'Contract v3', from: 'Ada' }]);
  assert.equal(state.n_items, 1);
  assert.equal(state.content_read, 1);
  assert.equal('submitted_at' in state, false, 'content submits nothing');
});

test('a server that staged no batch comes back as an envelope the agent can read', async () => {
  // §6: the run then judges on metadata alone and says so. It is a 200 with a
  // domain error, so `failed()` classifies it without any new code.
  const f = fakeFetch(ok({ status: 'error', error: 'no_staged_batch' }));
  const d = deps(f);
  const out = await cli.doContent(['t1'], d);

  assert.equal(out.error, 'no_staged_batch');
  assert.equal(fs.existsSync(d.statePath), false, 'a failed content writes no state');
});

test('the content command takes its keys from stdin, and refuses bad JSON', async () => {
  const f = fakeFetch(ok({ status: 'ok', items: [], unavailable: [] }));
  const d = deps(f);

  const good = await cli.runCommand(['node', 'x.js', 'content'], '["t1","t2"]', d);
  assert.equal(good.exitCode, 0);
  assert.deepEqual(f.calls[0].body.item_keys, ['t1', 't2']);

  const bad = await cli.runCommand(['node', 'x.js', 'content'], '[not json', deps(f));
  assert.equal(bad.out.error, 'unparseable_item_keys');
  assert.equal(bad.exitCode, 1);
  assert.equal(f.calls.length, 1, 'a JSON error must never reach content as an empty request');
});

test('main waits for content on stdin instead of posting an empty request', () => {
  // The gate in `main` is a named set of commands, and a command missing from
  // it fails SILENTLY: it receives '', parses to [], and asks the server for
  // nothing — which is indistinguishable from the agent deciding to judge on
  // metadata alone. The only way to catch that is through `main` itself, so
  // this spawns the CLI the way the cron turn does. Unparseable stdin is the
  // refusal that reaches an exit code without touching network or token.
  const script = path.join(__dirname, '..', 'scripts', 'gmail-wiki-ingest.js');
  const bad = spawnSync(process.execPath, [script, 'content'], { input: '[not json', encoding: 'utf8' });

  assert.equal(bad.status, 1);
  assert.equal(JSON.parse(bad.stdout).error, 'unparseable_item_keys');
});

test('parseArgv finds the command and its flags', () => {
  const { cmd, flag } = cli.parseArgv(['node', 'x.js', 'fetch', '--limit', '9']);
  assert.equal(cmd, 'fetch');
  assert.equal(flag('limit', '25'), '9');
  assert.equal(flag('missing', 'dflt'), 'dflt');
});

// ---- the run digest ------------------------------------------------------
// Everything below is the `report` half. It exists because the run is
// otherwise silent, so what these tests are really pinning down is the one
// message a day a user gets to trust: that its counters are the server's, that
// a subject line written by a stranger cannot forge any part of it, and that a
// run which did not happen produces no message at all.

// The two endpoints a full run touches, keyed by the fragment of the URL that
// picks them apart. A test that only stubs one of them and gets asked for the
// other should fail loudly rather than quietly return undefined.
function router(routes) {
  return fakeFetch(async (url, init) => {
    for (const [fragment, handler] of Object.entries(routes)) {
      if (url.includes(fragment)) return handler(url, init);
    }
    throw new Error(`no stub for ${url}`);
  });
}

const pushCalls = (f) => f.calls.filter((c) => c.url.includes('/api/agent/push'));

// A run that reached `submit`, of which the sanitization cases vary exactly one
// field. Started an hour before the injected clock, which is well inside the
// staleness window and nothing like a real gap.
function submittedRun(overrides = {}) {
  return Object.assign({
    started_at: new Date(T0 - HOUR).toISOString(),
    submitted_at: new Date(T0 - HOUR).toISOString(),
    n_items: 1,
    filtered: {},
    high: 1, middle: 0, low: 0, promoted: true,
    items: [{ thread_id: 't1', subject: 'a subject', from: 'Ada' }],
    acted: [{ item_key: 't1', band: 'high' }],
  }, overrides);
}

// Seed state, report against it, and hand back the exact bytes that were
// pushed. `doReport` returns the same string it posted, so asserting on the
// return value asserts on the message the user would see.
async function reportOn(state, input) {
  const f = router({ '/api/agent/push': ok({ status: 'ok' }) });
  const d = deps(f);
  cli.writeState(state, d);
  const out = await cli.doReport(input, d);
  assert.equal(out.status, 'ok', `report refused: ${out.error}`);
  return { content: out.content, f, d };
}

const bulletOf = (content) => content.split('\n').find((l) => l.startsWith('• '));

test('fetch → submit → report renders the digest from server-issued facts', async () => {
  const f = router({
    '/candidates/fetch': ok({
      status: 'ok',
      items: [
        { thread_id: 't1', subject: 'Re: Agent Builder roadmap', from: 'Ada', date: 'x' },
        { thread_id: 't2', subject: 'Contract v3', from: 'legal@acme.com', date: 'x' },
        { thread_id: 't3', subject: 'Your weekly digest', from: 'noreply@vendor.io', date: 'x' },
      ],
      filtered: { machine_mail: 12, already_distilled: 3 },
    }),
    '/candidates/submit': ok({
      status: 'ok',
      high: 1, middle: 2, low: 22, unvalidated: 0, dropped: 22, gated: 0,
      rejected: [], uncovered: 0, promoted: true,
      acted: [
        { item_key: 't1', band: 'high' },
        { item_key: 't2', band: 'middle' },
        { item_key: 't3', band: 'low' },
      ],
    }),
    '/api/agent/push': ok({ status: 'ok' }),
  });
  const d = deps(f);

  await cli.doFetch({ limit: 25 }, d);
  await cli.doSubmit([{ item_key: 't1' }, { item_key: 't2' }, { item_key: 't3' }], d);
  const out = await cli.doReport({
    headline: '3 ingested, 2 to review',
    notes: { t1: 'Agent-Builder', t2: 'no page yet' },
  }, d);

  // Byte for byte. The agent contributed the headline and the two notes and
  // nothing else: every subject, sender, band and number below came back out
  // of the state file the two server responses wrote.
  //
  // `legal at acme.com` is the one place this diverges from the design's
  // sketched output. GFM autolinks a bare address out of running text, so the
  // sketch's verbatim `legal@acme.com` would have rendered the sender as a
  // tappable mailto — which the design's own rule 4 forbids. The address is
  // defused rather than redacted, because unlike a URL it is the information.
  assert.equal(out.content, [
    '📨 Gmail → Wiki — 3 ingested, 2 to review',
    '',
    '**Added to your wiki**',
    '• **Re: Agent Builder roadmap** — Ada',
    '  → Agent-Builder',
    '**Waiting for your confirm**',
    '• **Contract v3** — legal at acme.com',
    '  → no page yet',
    '',
    '—',
    'high=1 · middle=2 · low=22 · gated=0 · filtered 15 · cursor promoted',
  ].join('\n'));

  // No session_id and no dedup_key, deliberately: with neither set the server
  // resolves session_source="history" and every daily report joins the one
  // running thread instead of branching the chat tree each morning.
  const push = pushCalls(f);
  assert.equal(push.length, 1);
  assert.deepEqual(push[0].body, { skill: 'gmail-wiki-ingest', content: out.content });
  assert.equal(fs.existsSync(d.statePath), false, 'state should be cleared by a landed push');
});

test('an empty batch still reports — "nothing new" plus the filter footer', async () => {
  // The proof-of-life case. A quiet mailbox and a broken sync look identical
  // from the outside, so the run with nothing to say still has to say it.
  const f = router({
    '/candidates/fetch': ok({
      status: 'ok', items: [], filtered: { machine_mail: 12, already_distilled: 3 },
    }),
    '/api/agent/push': ok({ status: 'ok' }),
  });
  const d = deps(f);

  await cli.doFetch({}, d);
  const out = await cli.doReport({ headline: 'nothing new' }, d);

  assert.equal(out.content, [
    '📨 Gmail → Wiki — nothing new',
    '',
    '—',
    '0 fetched · filtered 15 (machine_mail 12, already_distilled 3)',
  ].join('\n'));
  assert.equal(pushCalls(f).length, 1);
  assert.equal(
    f.calls.some((c) => c.url.includes('/candidates/submit')), false,
    'an empty batch has no verdicts to submit',
  );
});

test('a failed submit still reports, with the fetch counters alone', async () => {
  const f = router({
    '/candidates/fetch': ok({
      status: 'ok',
      items: [{ thread_id: 't1', subject: 'Contract v3', from: 'legal@acme.com' }],
      filtered: { machine_mail: 12, already_distilled: 3 },
    }),
    '/candidates/submit': fail(502, { detail: { error: 'upstream_unavailable' } }),
    '/api/agent/push': ok({ status: 'ok' }),
  });
  const d = deps(f);

  await cli.doFetch({}, d);
  const submitted = await cli.doSubmit([{ item_key: 't1' }], d);
  assert.equal(submitted.status, 'error');

  const out = await cli.doReport({ headline: 'checked, nothing kept' }, d);

  // No sections: nothing was banded, so there is nothing to list. The footer
  // takes its fetch-only shape, which keeps the filter breakdown — a thread
  // that vanished at the machine-mail filter and one that lost the LOW band
  // must not read the same in the morning.
  assert.equal(out.content, [
    '📨 Gmail → Wiki — checked, nothing kept',
    '',
    '—',
    '1 fetched · filtered 15 (machine_mail 12, already_distilled 3)',
  ].join('\n'));
  assert.equal(out.content.includes('high='), false, 'submit never answered');
});

test('state older than six hours is refused, and nothing is pushed', async () => {
  const f = router({ '/api/agent/push': ok({ status: 'ok' }) });
  const d = deps(f);
  cli.writeState(submittedRun({ started_at: new Date(T0 - 7 * HOUR).toISOString() }), d);

  const out = await cli.doReport({ headline: 'yesterday, warmed over' }, d);

  assert.equal(out.error, 'stale_run');
  assert.equal(f.calls.length, 0, 'a report with no run behind it is a lie');
  // Asserted through the exit-code table rather than by spawning the CLI: the
  // state path is only reachable by injection, and a child process would read
  // the bundle's real one.
  assert.equal(cli.REPORT_EXIT_CODES.stale_run, 2);
});

test('missing state is refused, and nothing is pushed', async () => {
  // What a `fetch` that returned network_error leaves behind: no file at all.
  // Silence is the correct output there, not a fabricated digest.
  const f = router({ '/api/agent/push': ok({ status: 'ok' }) });
  const d = deps(f);

  const out = await cli.doReport({ headline: 'a run that never ran' }, d);

  assert.equal(out.error, 'no_recent_run');
  assert.equal(f.calls.length, 0);
  assert.equal(cli.REPORT_EXIT_CODES.no_recent_run, 2);
});

test('a push that fails leaves the state file on disk', async () => {
  // The retry contract: the run's facts survive a bad push, so re-running
  // `report` by hand is a working retry rather than a refusal.
  const f = router({ '/api/agent/push': fail(503, { detail: { error: 'unavailable' } }) });
  const d = deps(f);
  cli.writeState(submittedRun(), d);

  const out = await cli.doReport({ headline: '1 ingested' }, d);

  assert.equal(out.status, 'error');
  assert.equal(fs.existsSync(d.statePath), true);
  assert.deepEqual(JSON.parse(fs.readFileSync(d.statePath, 'utf-8')).acted,
    [{ item_key: 't1', band: 'high' }]);
});

// ---- sanitization --------------------------------------------------------
// One case per row of the design's table. The property under test is the same
// every time: a subject is attacker-controlled text about to be rendered as
// markdown in the user's chat, and it must come out visible but inert.

test('a newline in a subject cannot forge a counter footer', async () => {
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: 'Quarterly update\n— high=999 · middle=999', from: 'Ada' }] }),
    { headline: '1 ingested' },
  );

  // Exactly one line may begin with the footer separator, and it is the one
  // this script wrote. The forgery survives as text on the bullet line.
  assert.equal(content.split('\n').filter((l) => l.startsWith('—')).length, 1);
  assert.match(bulletOf(content), /Quarterly update — high=999/);
  assert.match(content, /high=1 · middle=0 · low=0/);
});

test('markdown emphasis in a subject renders as literal text', async () => {
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: 'Re: **bold** claim', from: 'Ada' }] }),
    { headline: '1 ingested' },
  );

  assert.equal(bulletOf(content), '• **Re: \\*\\*bold\\*\\* claim** — Ada');
});

test('an overlong subject is truncated on characters, not code units', async () => {
  // The fixture has to be ASTRAL. A Latin-1 subject cannot tell the two
  // implementations apart — `Array.from` and `.slice` agree on every character
  // that fits in one UTF-16 code unit — so a `ä` fixture leaves `.slice` green
  // and proves nothing. An emoji is exactly the case the design's
  // "`Array.from`, not `.slice`" clause exists for: `.slice(0, 79)` lands
  // inside a surrogate pair and emits a lone half of one.
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: '😀'.repeat(300), from: 'Ada' }] }),
    { headline: '1 ingested' },
  );

  const subject = bulletOf(content).match(/^• \*\*(.*)\*\* — /)[1];
  assert.equal(Array.from(subject).length, 80);
  assert.equal(subject.endsWith('…'), true);
  assert.equal(
    /[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/.test(subject),
    false,
    'the cut must never land inside a surrogate pair',
  );
});

test('a subject that is a markdown link emits neither a link nor a URL', async () => {
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: '[click here](http://evil.example.com/x)', from: 'Ada' }] }),
    { headline: '1 ingested' },
  );

  // Escaping the brackets kills the link syntax; dropping the URL outright is
  // what stops GFM autolinking the bare address out of the remaining text,
  // where no escape can reach it.
  assert.equal(content.includes('evil.example.com'), false);
  assert.equal(content.includes('](http'), false);
  assert.match(bulletOf(content), /\\\[click here\\\]/);
});

test('a subject beginning with # cannot become a heading', async () => {
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: '# URGENT wire transfer', from: 'Ada' }] }),
    { headline: '1 ingested' },
  );

  assert.match(bulletOf(content), /\\# URGENT wire transfer/);
  assert.equal(content.split('\n').some((l) => l.startsWith('#')), false);
});

test('an inline <br> in a subject cannot forge a line', async () => {
  // Rule 1's forgery through a second door. The chat renderer parses raw
  // inline HTML and turns `<br>` into a real line break, so a subject can
  // reproduce the server-issued counter footer underneath its own bullet
  // without ever containing a newline for the C0 collapse to catch.
  const { content } = await reportOn(
    submittedRun({
      items: [{
        thread_id: 't1',
        subject: 'Invoice 4471<br>—<br>high=99 · middle=0 · low=0 · filtered 0 · cursor promoted',
        from: 'Ada',
      }],
    }),
    { headline: '1 ingested' },
  );

  assert.match(bulletOf(content), /Invoice 4471\\<br\\>/);
  assert.equal(content.includes('<br>'), false, 'the tag must not survive as markup');
  assert.equal(content.split('\n').filter((l) => l.startsWith('—')).length, 1);
  assert.match(content, /high=1 · middle=0 · low=0/);
});

test('an angle-bracketed sender address is not an autolink', async () => {
  // A From header arrives as `Display Name <addr@host>`, and both halves of
  // that are link syntax: the angle brackets are a CommonMark autolink and the
  // bare address inside them is a GFM one. On the NORMAL path — no hostility
  // required — that renders every sender as a tappable mailto whose display
  // name and address a stranger chose.
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: 'Payroll', from: 'Ada <ada@x.com>' }] }),
    { headline: '1 ingested' },
  );

  assert.equal(bulletOf(content), '• **Payroll** — Ada \\<ada at x.com\\>');
  assert.equal(content.includes('@'), false, 'no @-shaped token survives to be autolinked');
});

test('a bare email address in a subject cannot autolink either', async () => {
  const { content } = await reportOn(
    submittedRun({
      items: [{
        thread_id: 't1',
        subject: 'Payment failed — remit to billing@evil-attacker.com',
        from: 'Ada',
      }],
    }),
    { headline: '1 ingested' },
  );

  assert.equal(content.includes('@'), false);
  assert.match(bulletOf(content), /remit to billing at evil-attacker\.com/);
});

test("a subject's own backslash cannot disarm the escape that follows it", async () => {
  // The escaper's blind spot if the backslash is not itself an active:
  // `\*x\*` escapes to `\\*x\\*`, which a parser reads as a literal backslash
  // followed by a LIVE emphasis delimiter. The subject would then control
  // formatting inside a message the user reads as server-issued.
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: '\\*ACTION REQUIRED\\*', from: 'Ada' }] }),
    { headline: '1 ingested' },
  );

  assert.equal(bulletOf(content), '• **\\\\\\*ACTION REQUIRED\\\\\\*** — Ada');

  // The property behind the byte assertion: the escaping is a faithful,
  // reversible encoding, so unescaping returns exactly what the sender wrote
  // and nothing was left live along the way.
  const subject = bulletOf(content).match(/^• \*\*(.*)\*\* — /)[1];
  assert.equal(subject.replace(/\\(.)/g, '$1'), '\\*ACTION REQUIRED\\*');
});

test("a subject ending in a backslash cannot swallow the bullet's bold", async () => {
  // An unescaped trailing `\` eats the `**` that closes the bullet. The strong
  // span then stays open to the NEXT bullet's `**`, swallowing this thread's
  // sender and the following thread's row into it.
  const { content } = await reportOn(
    submittedRun({ items: [{ thread_id: 't1', subject: 'Payroll update\\', from: 'Ada' }] }),
    { headline: '1 ingested' },
  );

  assert.equal(bulletOf(content), '• **Payroll update\\\\** — Ada');
});

test('a line separator that is not a newline still cannot forge a footer', async () => {
  // U+2028, U+2029 and NEL break a line in the iOS text layer exactly as LF
  // does, and none of them is a C0 control or something `.trim()` reaches in
  // the middle of a string. The zero-width and bidi controls in the sender are
  // the other half of the same hole: not line-breaking but invisible, and a
  // right-to-left override makes a sender read backwards.
  const { content } = await reportOn(
    submittedRun({
      items: [{
        thread_id: 't1',
        subject: 'Quarterly update\u2028— high=999\u2029and\u0085more',
        from: 'A\u202Eda\u200B',
      }],
    }),
    { headline: '1 ingested' },
  );

  assert.equal(bulletOf(content), '• **Quarterly update — high=999 and more** — Ada');
  assert.equal(content.split('\n').filter((l) => l.startsWith('—')).length, 1);
  assert.equal(
    /[\u0085\u2028\u2029\u200B-\u200F\u202A-\u202E\u2060-\u2064\uFEFF]/.test(content), false,
    'nothing invisible or line-breaking reaches the chat',
  );
});

// ---- volume and band filtering -------------------------------------------

test('twelve acted items render five bullets and a count of the rest', async () => {
  const items = Array.from({ length: 12 }, (_, i) => ({
    thread_id: `t${i}`, subject: `Thread ${i}`, from: 'Ada',
  }));
  const { content } = await reportOn(
    submittedRun({
      items,
      acted: items.map((it) => ({ item_key: it.thread_id, band: 'high' })),
      high: 12,
    }),
    { headline: '12 ingested' },
  );

  assert.equal(content.split('\n').filter((l) => l.startsWith('• ')).length, 5);
  assert.match(content, /^\.\.\.and 7 more$/m);
  assert.equal(content.includes('Thread 5'), false, 'the sixth thread is folded into the count');
});

test('LOW rows get no bullet and still reach the footer count', async () => {
  // The whole reason the join filters by band: a digest that listed twenty-two
  // discards would bury the one thread that needs an answer.
  const items = [
    { thread_id: 't1', subject: 'Contract v3', from: 'legal@acme.com' },
    { thread_id: 't2', subject: 'Your weekly digest', from: 'noreply@vendor.io' },
    { thread_id: 't3', subject: 'Flash sale', from: 'ads@vendor.io' },
  ];
  const { content } = await reportOn(
    submittedRun({
      items,
      acted: [
        { item_key: 't1', band: 'middle' },
        { item_key: 't2', band: 'low' },
        { item_key: 't3', band: 'low' },
      ],
      high: 0, middle: 1, low: 22, promoted: false,
    }),
    { headline: '1 to review' },
  );

  assert.equal(content.split('\n').filter((l) => l.startsWith('• ')).length, 1);
  assert.equal(content.includes('Your weekly digest'), false);
  assert.equal(content.includes('Flash sale'), false);
  assert.match(content, /high=0 · middle=1 · low=22 · gated=0 · filtered 0 · cursor held/);
});

test('the category gate is visible in the footer, and the number is the server\'s', async () => {
  // A run where every thread was dropped at the category gate used to render
  // identically to a run that judged nothing — no gate count reached the
  // footer. That run happened in production and was undiagnosable from the
  // digest. The count comes off the submit response through the run state, so
  // this drives it end to end rather than seeding the state directly.
  const f = router({
    '/candidates/fetch': ok({
      status: 'ok',
      items: [
        { thread_id: 't1', subject: 'Invoice 4471', from: 'billing' },
        { thread_id: 't2', subject: 'Flash sale', from: 'ads' },
        { thread_id: 't3', subject: 'Status page update', from: 'ops' },
      ],
      filtered: {},
    }),
    '/candidates/submit': ok({
      status: 'ok',
      high: 0, middle: 0, low: 0, unvalidated: 0, dropped: 3, gated: 3,
      rejected: [], uncovered: 0, promoted: true, acted: [],
    }),
    '/api/agent/push': ok({ status: 'ok' }),
  });
  const d = deps(f);

  await cli.doFetch({}, d);
  await cli.doSubmit([{ item_key: 't1' }, { item_key: 't2' }, { item_key: 't3' }], d);
  const out = await cli.doReport({ headline: 'nothing kept' }, d);

  assert.equal(out.content, [
    '📨 Gmail → Wiki — nothing kept',
    '',
    '—',
    'high=0 · middle=0 · low=0 · gated=3 · filtered 0 · cursor promoted',
  ].join('\n'));
});

test('a batch that was all LOW does not read as a batch that was all mislabelled', async () => {
  // The footer renders `gated`, NOT the server's `dropped`, and this is the
  // run that shows why. Ten threads the agent labelled `correspondence`
  // perfectly correctly, every one scored below cut B: the server returns
  // low=10 AND dropped=10, because `dropped` counts the LOW band as well as
  // the category gate. Rendered as `dropped=` that is twenty outcomes for ten
  // threads, and it sends the agent — which reads its own digest — to hunt a
  // labelling bug that does not exist. The real signal is a cut point.
  const f = router({
    '/candidates/fetch': ok({
      status: 'ok',
      items: [{ thread_id: 't1', subject: 'lunch?', from: 'ada' }],
      filtered: {},
    }),
    '/candidates/submit': ok({
      status: 'ok',
      high: 0, middle: 0, low: 10, unvalidated: 0, dropped: 10, gated: 0,
      rejected: [], uncovered: 0, promoted: true, acted: [],
    }),
    '/api/agent/push': ok({ status: 'ok' }),
  });
  const d = deps(f);

  await cli.doFetch({}, d);
  await cli.doSubmit([{ item_key: 't1' }], d);
  const out = await cli.doReport({ headline: 'nothing kept' }, d);

  assert.match(out.content, /low=10 · gated=0/);
  // and the number that double-counts them never reaches the digest at all
  assert.equal(out.content.includes('dropped'), false);
});

test('a gate count the agent could have forged renders as zero', async () => {
  // Same property as every counter in the footer: it is read as a number out
  // of the run state, so a string that would have forged a whole second footer
  // reaches the digest as 0 rather than as text.
  const { content } = await reportOn(
    submittedRun({ gated: '3 · cursor promoted\n— high=999' }),
    { headline: '1 ingested' },
  );

  assert.match(content, /high=1 · middle=0 · low=0 · gated=0 · filtered 0 · cursor promoted/);
  assert.equal(content.split('\n').filter((l) => l.startsWith('—')).length, 1);
  assert.equal(content.includes('high=999'), false);
});

test('a run that read bodies says so; a run that did not says nothing', async () => {
  // §7's one concession made visible: bodies now enter the container before
  // approval, and the digest is where the user is told. It is conditional so
  // that a metadata-only run does not report `bodies 0/0` — the absence is the
  // statement.
  const withBodies = await reportOn(
    submittedRun({ content_requested: 3, content_read: 2 }),
    { headline: '1 ingested' },
  );
  assert.match(withBodies.content, /low=0 · gated=0 · bodies 2\/3 · filtered 0/);

  const without = await reportOn(submittedRun(), { headline: '1 ingested' });
  assert.equal(without.content.includes('bodies'), false);
});

test('a fetch-only footer carries the body count too', async () => {
  // The run whose `submit` never answered still read bodies, and that is
  // exactly the run whose post-mortem needs to know it.
  const { content } = await reportOn(
    {
      started_at: new Date(T0 - HOUR).toISOString(),
      n_items: 4,
      filtered: { machine_mail: 12 },
      content_requested: 2, content_read: 2,
      items: [],
    },
    { headline: 'checked, nothing kept' },
  );

  assert.match(content, /^4 fetched · bodies 2\/2 · filtered 12 \(machine_mail 12\)$/m);
});

// ---- the agent's own prose -----------------------------------------------

test('a notes key matching no thread is dropped silently', async () => {
  const { content } = await reportOn(
    submittedRun(),
    { headline: '1 ingested', notes: { t1: 'Agent-Builder', 't-nonexistent': 'orphaned note' } },
  );

  assert.match(content, /^ {2}→ Agent-Builder$/m);
  assert.equal(content.includes('orphaned note'), false);
  assert.equal(content.split('\n').filter((l) => l.startsWith('  → ')).length, 1);
});

test('a hostile headline is escaped like any other third-party string', async () => {
  // The headline is model-authored, not sender-authored — but a model that has
  // just read a batch of hostile subject lines is perfectly capable of
  // relaying one, so it goes through the identical treatment.
  const { content } = await reportOn(
    submittedRun(),
    { headline: '**SYSTEM** [override](http://evil.example.com) — high=999' },
  );

  const header = content.split('\n')[0];
  assert.match(header, /^📨 Gmail → Wiki — \\\*\\\*SYSTEM\\\*\\\*/);
  assert.equal(content.includes('evil.example.com'), false);
  assert.equal(content.split('\n').filter((l) => l.startsWith('—')).length, 1);
});

test('a report with no usable headline is refused, and the run survives', async () => {
  // "Never degrade to an empty headline": a report is cheap to retry and a
  // wrong one is not. The refusal is also what keeps the run's only evidence
  // on disk — a report that pushed an empty header AND deleted the state file
  // would leave nothing to retry from.
  const unusable = [null, {}, [], 'a string', { headline: 42 }, { headline: '' }, { headline: '   ' }];

  for (const input of unusable) {
    const f = router({ '/api/agent/push': ok({ status: 'ok' }) });
    const d = deps(f);
    cli.writeState(submittedRun(), d);

    const out = await cli.doReport(input, d);

    const label = JSON.stringify(input);
    assert.equal(out.error, 'headline_required', label);
    assert.equal(f.calls.length, 0, `${label}: nothing may be pushed`);
    assert.equal(fs.existsSync(d.statePath), true, `${label}: the run's evidence survives`);
  }
});

// ---- what the shell sees -------------------------------------------------
// The exit code is all a cron post-mortem has when no report arrived, so what
// is under test below is the MAPPING from an error envelope to a process
// status — not the table it happens to be written in. An assertion that reads
// `REPORT_EXIT_CODES` back cannot fail while the constant exists, and would
// stay green with the line that consults it deleted.

test('every report refusal reaches the shell as its own exit code', async () => {
  const cases = [
    { why: 'no run behind it', state: null, stdin: '{"headline":"x"}', code: 2, error: 'no_recent_run' },
    {
      why: 'yesterday, warmed over',
      state: submittedRun({ started_at: new Date(T0 - 7 * HOUR).toISOString() }),
      stdin: '{"headline":"x"}', code: 2, error: 'stale_run',
    },
    { why: 'stdin is not JSON', state: submittedRun(), stdin: '{not json', code: 1, error: 'unparseable_report_input' },
    { why: 'no headline in it', state: submittedRun(), stdin: '{}', code: 1, error: 'headline_required' },
    // 2 and 1 say "this run produced nothing"; a push that did not land keeps
    // postJson's contract instead, where the envelope on stdout is the signal
    // and the run is retryable, so the shell sees success.
    {
      why: 'the push did not land', state: submittedRun(), stdin: '{"headline":"x"}',
      code: 0, error: 'unavailable', push: fail(503, { detail: { error: 'unavailable' } }),
    },
  ];

  for (const c of cases) {
    const f = router({ '/api/agent/push': c.push || ok({ status: 'ok' }) });
    const d = deps(f);
    if (c.state) cli.writeState(c.state, d);

    const { out, exitCode } = await cli.runCommand(['node', 'x.js', 'report'], c.stdin, d);

    assert.equal(out.error, c.error, c.why);
    assert.equal(exitCode, c.code, c.why);
    if (c.code !== 0) assert.equal(pushCalls(f).length, 0, `${c.why}: nothing may be pushed`);
    if (c.state) assert.equal(fs.existsSync(d.statePath), true, `${c.why}: the run survives`);
  }
});

test('a landed report exits 0 and clears the run', async () => {
  const f = router({ '/api/agent/push': ok({ status: 'ok' }) });
  const d = deps(f);
  cli.writeState(submittedRun(), d);

  const { out, exitCode } = await cli.runCommand(
    ['node', 'x.js', 'report'], '{"headline":"1 ingested"}', d,
  );

  assert.equal(out.status, 'ok');
  assert.equal(exitCode, 0);
  assert.equal(fs.existsSync(d.statePath), false);
});

test('an unknown command is usage, and submit still refuses bad stdin', async () => {
  const f = router({});

  const usage = await cli.runCommand(['node', 'x.js'], '', deps(f));
  assert.equal(usage.out, null, 'no envelope: there was no command to answer');
  assert.equal(usage.exitCode, 2);

  const bad = await cli.runCommand(['node', 'x.js', 'submit'], '{not json', deps(f));
  assert.equal(bad.out.error, 'unparseable_verdicts');
  assert.equal(bad.exitCode, 1);
  assert.equal(f.calls.length, 0, 'a JSON error must never reach submit as an empty batch');
});

test('the process exit code is the one runCommand returned', () => {
  // The one case that goes through `main`. Everything above calls `runCommand`
  // directly and would stay green if `main` stopped setting process.exitCode
  // at all — and then a cron turn that pushed nothing would exit 0 and be
  // invisible in exactly the post-mortem this exists for. Unparseable stdin is
  // the refusal that reaches a code without touching state, network or token.
  const script = path.join(__dirname, '..', 'scripts', 'gmail-wiki-ingest.js');

  const bad = spawnSync(process.execPath, [script, 'report'], { input: '{not json', encoding: 'utf8' });
  assert.equal(bad.status, 1);
  assert.equal(JSON.parse(bad.stdout).error, 'unparseable_report_input');

  const usage = spawnSync(process.execPath, [script], { input: '', encoding: 'utf8' });
  assert.equal(usage.status, 2);
  assert.match(usage.stderr, /^usage: gmail-wiki-ingest\.js/);
  assert.equal(usage.stdout, '', 'usage is not an envelope');
});

test('a 2xx whose body is not JSON is an envelope, not a null', async () => {
  // An ingress that answered before the app did, or a truncated response.
  // Handing the null straight back makes the caller read `.status` off it and
  // die with a TypeError, which the shell reports as exit 1 — the code
  // reserved for a malformed agent payload — so a transport failure would be
  // post-mortemed as the agent's fault, with no envelope on stdout to correct
  // the record.
  const f = router({
    '/api/agent/push': async () => ({
      ok: true,
      status: 200,
      json: async () => { throw new SyntaxError('Unexpected end of JSON input'); },
    }),
  });
  const d = deps(f);
  cli.writeState(submittedRun(), d);

  const { out, exitCode } = await cli.runCommand(
    ['node', 'x.js', 'report'], '{"headline":"1 ingested"}', d,
  );

  assert.equal(out.status, 'error');
  assert.equal(out.error, 'unparseable_response');
  assert.equal(exitCode, 0, "a transport failure keeps postJson's envelope contract");
  assert.equal(fs.existsSync(d.statePath), true, 'so a manual retry has something to render');
});

// ---- the documented wire shape ------------------------------------------
//
// These read the bundle's own prose, which is unusual for a test suite and is
// the point. The script never parses `context` — it prints the fetch envelope
// and the AGENT reads it — so the only thing standing between the server's
// bytes and a citation is what SKILL.md, rubric.md and tool-contract.md say
// those bytes look like. A doc that describes the wrong shape is not a
// cosmetic defect here; it is the whole of the contract, and nothing else in
// this file can catch it.
//
// SOURCE OF TRUTH: javis-server `gmail_candidate_adapter._serialize_model`,
// pinned there by tests/services/test_gmail_candidate_adapter.py
// (`test_context_carries_the_knowledge_model`). It emits a `fields` header and
// POSITIONAL rows, and blanks a title that merely de-slugifies its own slug.
// The bundle documented objects with named keys and a title that is always
// present — both wrong, and both in the exact place the agent is told to cite
// from.

const DOCS = {
  'SKILL.md': fs.readFileSync(path.join(__dirname, '../SKILL.md'), 'utf8'),
  'rubric.md': fs.readFileSync(path.join(__dirname, '../rubric.md'), 'utf8'),
  'references/tool-contract.md': fs.readFileSync(
    path.join(__dirname, '../references/tool-contract.md'), 'utf8',
  ),
};

test('every doc that describes knowledge_model names the fields header', () => {
  for (const [name, text] of Object.entries(DOCS)) {
    assert.ok(
      text.includes('"page_type", "slug", "title", "degree"'),
      `${name} describes knowledge_model without naming the fields header, so ` +
      'a reader has no way to know the rows are positional or in what order',
    );
  }
});

test('the worked example in SKILL.md is a positional row, not an object', () => {
  const text = DOCS['SKILL.md'];
  const start = text.indexOf('"knowledge_model"');
  assert.ok(start > 0, 'SKILL.md no longer shows a fetch envelope example');
  const block = text.slice(start, text.indexOf('```', start));

  assert.match(block, /"nodes":\s*\[\s*\[/, 'nodes[] must be shown as arrays');
  // The old rendering. An object here would send the agent looking for
  // `nodes[i].slug` on a four-element array.
  assert.equal(
    /"nodes"[\s\S]*"page_type"\s*:/.test(block), false,
    'the example still renders a node as an object with named keys',
  );
  // And the example must be output the server can actually produce: a title
  // that de-slugifies to its own slug ships as "".
  assert.equal(
    block.includes('"Agent-Builder", "Agent Builder"'), false,
    'the example shows a title the server blanks before sending it',
  );
});

test('the blank title is documented as a rule, not left to be discovered', () => {
  // 37% of a real wiki. An agent that reads "" as a missing page, or that cites
  // a title because one was promised, is following the doc rather than the wire.
  assert.match(DOCS['SKILL.md'], /`title` is often `""`/);
  assert.match(DOCS['references/tool-contract.md'], /de-slugifies its own slug/);
});

test('a disabled scope stops the run silently, at fetch and at submit', () => {
  // javis-server answers `disabled` (not an ok, empty batch) when the scope is
  // off, so a user who disconnected Google stops getting a daily "nothing new".
  // Without these rows the generic non-ok row applies and the agent reports an
  // error string instead; and a `submit` that answers `disabled` must not be
  // followed by a `report`, which would render the fetch counters still in run
  // state into a digest for a user who just turned this off.
  const md = DOCS['SKILL.md'];
  assert.match(md, /`fetch` returns `\{"error": "disabled"\}` \| [^\n]*Stop silently/);
  assert.match(md, /`submit` returns `\{"error": "disabled"\}` \| [^\n]*do not `report`/);
  assert.doesNotMatch(md, /returns an empty batch when the scope is\s+off/);
});

test('the rubric says which element of a node row the slug is', () => {
  // Position 0 is the page type — the one thing a citation must not carry — so
  // reading the wrong element yields a ref that looks plausible and validates
  // against nothing.
  assert.match(DOCS['rubric.md'], /nodes\[i\]\[1\]/);
});

test('the rubric sends a date-only occurred_at as midday, not midnight', () => {
  // The rubric's own headline case — "a receipt forwarded weeks later belongs
  // on the purchase date" — is the one that hands the agent a bare calendar
  // date, and the canonical way to write a bare date with the required zone is
  // `T00:00:00Z`. That instant is the previous evening everywhere west of UTC,
  // so an August 1 purchase files under July 31 for a Pacific user: the exact
  // off-by-a-day this field was added to remove. It cannot be caught anywhere
  // else — the server accepts it (parses, zoned, past), no counter moves, and
  // it renders correctly for a UTC or Shanghai reader, so a test run outside
  // the Americas sees nothing. The rule therefore has to be in the prose the
  // agent reads, which makes this the only place it can be pinned.
  const text = DOCS['rubric.md'];
  assert.match(text, /midday/,
    'rubric §5 no longer tells the agent what time of day a bare date carries');
  assert.match(text, /2026-08-01T12:00:00Z/,
    'rubric §5 must SHOW the midday form; the agent copies the example, and ' +
    'the only worked example used to be an instant with a real time on it');
  assert.match(text, /midnight/,
    'rubric §5 must name midnight as the wrong answer, not merely imply it');
});

test('the wire contract says midnight is accepted rather than policed', () => {
  // tool-contract.md lists the server's two rules (zoned, not future) as a
  // table, which reads as an exhaustive gate. A midnight-UTC value passes both
  // and is still wrong, so the contract has to say the gap is there — a reader
  // who takes the table as complete concludes anything accepted is placed
  // correctly.
  const text = DOCS['references/tool-contract.md'];
  assert.match(text, /2026-08-01T00:00:00Z/,
    'the contract must show the value that slips through, not describe it');
  assert.match(text, /midday/,
    'the contract must point at the fix it expects the skill to apply');
});
