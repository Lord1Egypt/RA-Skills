'use strict';
// U3 — the javis-server push transport. R2 (TC-S4-1, TC-S1-6), R3 (TC-S1-2),
// R4 (TC-S1-3), R5 (TC-S1-4), R19 (TC-S1-5).
//
// The fake-fetch helpers are gmail-wiki-ingest/test/cli.test.js:11-38 verbatim,
// so a reader who knows that suite knows this one.

const { test } = require('node:test');
const assert = require('node:assert/strict');

const srv = require('../scripts/server.js');

function fakeFetch(impl) {
  const calls = [];
  const fn = async (url, init) => {
    calls.push({ url, init, body: JSON.parse(init.body) });
    return impl(url, init);
  };
  fn.calls = calls;
  return fn;
}

const ok = (payload) => async () => ({ ok: true, status: 200, json: async () => payload });
const fail = (status, payload) => async () => ({ ok: false, status, json: async () => payload });

const UUID = '2eecd5b1-ca2d-493e-a57e-3158f6b8e1b3';   // the real note id from F65

function note(extra = {}) {
  return Object.assign({
    sourceId: UUID,
    title: '新建记事',
    text: 'body\n',
    bodyHash: 'a'.repeat(64),
    notebook: 'Thermodynamics',
  }, extra);
}

function deps(f) {
  return { fetch: f, token: 'gw-token' };
}

/**
 * ONE SUCCESSFUL PUSH, IN JAVIS-SERVER'S OWN SHAPE.
 *
 * Copied key for key from `_envelope` in
 * javis-server/app/services/skill_wiki_sources.py, because the previous
 * fixture was this bundle's guess at it (`{status:'ok', pages:[…],
 * spend:{…}}`) — and a fake built from a guess makes every test that uses it
 * agree with the guess. test/contract.test.js checks the key names against
 * that file whenever a javis-server checkout sits beside this one.
 */
function pending(extra = {}) {
  return Object.assign({
    status: 'pending',
    source_type: 'notebooklm',
    source_id: UUID,
    source_slug: `notebooklm-note-${UUID}`,
    page: { page_type: 'source', slug: `notebooklm-note-${UUID}`, action: 'create' },
    feeds: [{ page_type: 'topic', slug: 'Entropy', action: 'update' }],
    would_change: 'new',
    budget: {
      units_per_hour: 50,
      units_remaining: 47,
      window_seconds: 3600,
      shared_with: ['external', 'notebooklm', 'obsidian'],
    },
    notice: null,
    canary: { flagged: false, first: false, headers: [] },
    error: null,
    error_description: null,
    next_step: null,
  }, extra);
}

// ---------------------------------------------------------------------------
// R2 — one gateway-token-authenticated endpoint
// ---------------------------------------------------------------------------

test('R2 TC-S4-1: the push carries the bearer token and the typed body', async () => {
  const f = fakeFetch(ok(pending()));
  const out = await srv.pushSource(note(), deps(f));
  assert.equal(out.status, 'pending');

  const call = f.calls[0];
  assert.equal(call.url, `${srv.SERVER}${srv.ENDPOINTS.push}`);
  assert.equal(call.init.method, 'POST');
  assert.equal(call.init.headers.Authorization, 'Bearer gw-token');
  assert.equal(call.init.headers['Content-Type'], 'application/json');
  assert.equal(call.body.source_type, 'notebooklm');
  assert.equal(call.body.source_id, UUID, 'F65: the note uuid travels verbatim, with no mapping table');
  assert.equal(call.body.body_hash, 'a'.repeat(64));
  assert.equal(call.body.dry_run, false);
  assert.equal(call.body.op, 'upsert');
});

test('R2: every field on the wire is one javis-server declares', async () => {
  // The regression this whole file exists for. `WikiSourcePushRequest` takes
  // source_type / source_id / op / title / text / body_hash / notebook_id /
  // dry_run / upstream_error / response_headers — and pydantic DROPS anything
  // else without a word, so a field this bundle invents is not a contract, it
  // is a silence. `skill`, `path` and `notebook` were all being dropped.
  const f = fakeFetch(ok(pending()));
  await srv.pushSource(note({ skill: 'something-else', path: 'NotebookLM/x/y.md' }), deps(f));
  const sent = Object.keys(f.calls[0].body).sort();
  assert.deepEqual(sent, [
    'body_hash', 'dry_run', 'notebook_id', 'op', 'source_id', 'source_type',
    'text', 'title',
  ]);
  for (const dropped of ['skill', 'path', 'notebook', 'user_id']) {
    assert.equal(dropped in f.calls[0].body, false, `${dropped} is not a request field`);
  }
});

test('R2: the skill slug is pinned on the digest, which is the body that takes one', async () => {
  const f = fakeFetch(ok({ status: 'ok' }));
  await srv.pushDigest('hello', deps(f));
  assert.equal(f.calls[0].body.skill, 'notebooklm-ingest');
  assert.equal(srv.SKILL, 'notebooklm-ingest');
});

// ---------------------------------------------------------------------------
// R17 — the notebook reaches the locator as notebook_id, or not at all
// ---------------------------------------------------------------------------

test('R17: a notebook title is slugified into a notebook_id the server accepts', async () => {
  const f = fakeFetch(ok(pending()));
  await srv.pushSource(note({ notebook: 'Qwen research' }), deps(f));
  assert.equal(f.calls[0].body.notebook_id, 'Qwen-research');
  assert.match(f.calls[0].body.notebook_id, srv.NOTEBOOK_ID_RE);
});

test('R17: a notebook id travels verbatim when it is already a legal segment', () => {
  assert.equal(srv.notebookId('nb-1'), 'nb-1');
  assert.equal(srv.notebookId('a.b_c-9'), 'a.b_c-9');
});

test('R17: a notebook with no legal segment in it is OMITTED, never sent as a 400', async () => {
  // check_namespace refuses anything outside [A-Za-z0-9][A-Za-z0-9._-]{0,127},
  // so forwarding the NAME would turn a CJK notebook into a hard
  // invalid_request — no ingest at all, instead of a locator with one segment
  // fewer.
  assert.equal(srv.notebookId('新建记事'), null);
  assert.equal(srv.notebookId('   '), null);
  const f = fakeFetch(ok(pending()));
  await srv.pushSource(note({ notebook: '新建记事' }), deps(f));
  assert.equal('notebook_id' in f.calls[0].body, false);
});

test('R17: a notebook_id can never walk out of its own path segment', () => {
  for (const hostile of ['../../etc', '/abs/path', 'a/b', '..', '.']) {
    const out = srv.notebookId(hostile);
    if (out !== null) assert.match(out, srv.NOTEBOOK_ID_RE, hostile);
    assert.equal(String(out).includes('/'), false, hostile);
  }
});

test('R2 TC-S1-6: a missing gateway token throws loudly (a broken container, not a refusal)', async () => {
  const saved = process.env.OPENCLAW_GATEWAY_TOKEN;
  delete process.env.OPENCLAW_GATEWAY_TOKEN;
  try {
    await assert.rejects(
      () => srv.postJson('/x', {}, { fetch: fakeFetch(ok({})) }),
      /OPENCLAW_GATEWAY_TOKEN is required/,
    );
  } finally {
    if (saved !== undefined) process.env.OPENCLAW_GATEWAY_TOKEN = saved;
  }
});

test('R2: there are exactly two endpoints, both writes', () => {
  assert.deepEqual(Object.keys(srv.ENDPOINTS).sort(), ['digest', 'push']);
  // javis-server app/routers/skill_wiki_sources.py: @router.post("/skill/wiki/
  // sources"), mounted with prefix "/api" in app/main.py. test/contract.test.js
  // reads those files; this is the value they must agree on.
  assert.equal(srv.ENDPOINTS.push, '/api/skill/wiki/sources');
  assert.equal(srv.ENDPOINTS.digest, '/api/agent/push');
});

// ---------------------------------------------------------------------------
// R19 — write-only, enforced by the module's surface
// ---------------------------------------------------------------------------

test('R19 TC-S1-5: the module exports no read helper', () => {
  const readish = Object.keys(module.require('../scripts/server.js'))
    .filter((k) => /^(get|read|list|fetch|search|export|download)/i.test(k));
  assert.deepEqual(readish, [], `these exports read: ${readish.join(', ')}`);
});

test('R19 TC-S1-5: every request this module can make is a POST', async () => {
  const f = fakeFetch(ok({ status: 'ok' }));
  await srv.pushSource(note(), deps(f));
  await srv.pushDigest('digest', deps(f));
  await srv.postJson(srv.ENDPOINTS.push, {}, deps(f));
  assert.equal(f.calls.length, 3);
  for (const c of f.calls) assert.equal(c.init.method, 'POST');
});

test('R19: a push response is never treated as a content channel', async () => {
  // Even if the server echoed a body back, nothing in this module reads it into
  // a note: pushSource returns the envelope and keeps no state.
  const f = fakeFetch(ok({ status: 'ok', text: 'SOMEONE ELSE WIKI TEXT' }));
  const out = await srv.pushSource(note(), deps(f));
  assert.equal(out.text, 'SOMEONE ELSE WIKI TEXT', 'the envelope is returned as-is');
  // …and the module offers no function that would turn it into a source.
  assert.equal(typeof srv.ingestResponse, 'undefined');
  assert.equal(typeof srv.readSource, 'undefined');
});

// ---------------------------------------------------------------------------
// R3 — dry run
// ---------------------------------------------------------------------------

test('R3 TC-S1-2: a dry run sets the flag on the one endpoint and makes no other call', async () => {
  const f = fakeFetch(ok(Object.assign(pending(), {
    status: 'dry_run', notice: 'the concept pages cannot be listed before the distill runs',
  })));
  const out = await srv.pushSource(note({ dryRun: true }), deps(f));
  assert.equal(f.calls.length, 1, 'a dry run is one call, not a probe plus a write');
  assert.equal(f.calls[0].body.dry_run, true);
  assert.equal(f.calls[0].url.endsWith(srv.ENDPOINTS.push), true);
  assert.equal(srv.pagesFrom(out)[0].status, 'new');
  assert.match(out.notice, /cannot be listed/);
});

test('R3: dry_run is explicit false rather than absent on a real push', async () => {
  const f = fakeFetch(ok(pending()));
  await srv.pushSource(note(), deps(f));
  assert.equal(f.calls[0].body.dry_run, false, 'a flag that is easy to forget is always sent');
});

// ---------------------------------------------------------------------------
// R20 / R9 — the answer is read with the server's own key names
// ---------------------------------------------------------------------------

test('R20: the page list is `page` then `feeds`, with the server\'s markers', () => {
  const rows = srv.pagesFrom(pending());
  assert.deepEqual(rows.map((r) => [r.slug, r.status]), [
    [`notebooklm-note-${UUID}`, 'new'],
    ['Entropy', 'updated'],
  ]);
  assert.equal(rows[0].url, null, 'the envelope names pages by slug and hands back no content');
});

test('R20: reading a key the server does not send is an empty list, which is the bug', () => {
  // The shape this bundle used to read. Kept as a test so the next reader sees
  // why `pages` is wrong rather than rediscovering it in production: every
  // push reported zero pages, every ledger row recorded 0, and the dry run
  // previewed nothing at all.
  assert.deepEqual(pending().pages, undefined);
  assert.deepEqual(pending().spend, undefined);
  assert.equal(srv.pagesFrom({}).length, 0);
});

test('R20: a page with no slug is dropped rather than rendered as an empty bullet', () => {
  assert.deepEqual(srv.pagesFrom({ page: { page_type: 'source' }, feeds: [null, 'x'] }), []);
});

test('R9: the budget comes off the envelope as the server states it', () => {
  const b = srv.budgetFrom(pending());
  assert.deepEqual(b, {
    units_per_hour: 50, units_remaining: 47, window_seconds: 3600,
    shared_with: ['external', 'notebooklm', 'obsidian'],
  });
  assert.equal(srv.budgetFrom({}), null);
  assert.equal(srv.budgetFrom({ budget: [] }), null, 'an array is not the budget object');
});

test('R9: a refusal states the budget too, because it is a fact about the account', async () => {
  const body = Object.assign(pending(), {
    status: 'refused', error: 'budget_exhausted',
    error_description: 'this account has spent its 50 wiki-ingest units for the rolling hour',
    next_step: 'wait for the rolling hour to free wiki-ingest units, then push again; nothing was stored, so no content was lost',
  });
  body.budget.units_remaining = 0;
  const out = await srv.pushSource(note(), deps(fakeFetch(fail(429, body))));
  assert.equal(srv.failed(out), true);
  assert.equal(srv.budgetFrom(out.detail).units_remaining, 0);
});

test('R16: a flagged canary is read off any answer, and an unflagged one is null', () => {
  assert.equal(srv.canaryFrom(pending()), null);
  const flagged = srv.canaryFrom({ canary: { flagged: true, first: true, headers: ['sec-session-id'] } });
  assert.deepEqual(flagged, { flagged: true, first: true, headers: ['sec-session-id'] });
});

test('R16 F5b: a push carries response_headers when the run saw a sighting, and the key is absent otherwise', async () => {
  // The second break in the tripwire. javis-server's `_canary` reads
  // `response_headers` off EVERY push and writes the one-row-per-account
  // `source_canary` log from it — and no caller ever set the key, so the
  // argument was `None` on every call and the row was never written.
  const bare = fakeFetch(ok(pending()));
  await srv.pushSource(note(), deps(bare));
  assert.equal('response_headers' in bare.calls[0].body, false, 'no sighting, no key');

  const f = fakeFetch(ok(pending()));
  await srv.pushSource(note({ responseHeaders: ['Sec-Session-Registration'] }), deps(f));
  assert.deepEqual(f.calls[0].body.response_headers, { 'sec-session-registration': '' });
  // The note itself still travels: a canary is reported ALONGSIDE the push,
  // never instead of it.
  assert.equal(f.calls[0].body.text, 'body\n');
});

test('R16 F5b: the names on the wire are bounded and carry no values', () => {
  // These names are persisted in a wiki_logs row, and a Sec-Session-* VALUE
  // is a device-binding challenge sitting next to a cookie.
  assert.deepEqual(
    srv.canaryHeadersBody({ 'Sec-Session-Id': 'challenge=secret' }),
    { 'sec-session-id': '' },
  );
  const flood = Array.from({ length: 80 }, (_, i) => `sec-session-${i}`);
  assert.equal(Object.keys(srv.canaryHeadersBody(flood)).length, srv.MAX_CANARY_HEADERS);
  const long = srv.canaryHeadersBody([`sec-session-${'x'.repeat(500)}`]);
  for (const name of Object.keys(long)) {
    assert.ok(name.length <= srv.MAX_CANARY_NAME_CHARS, `${name.length} characters`);
    assert.match(name, /^[a-z0-9._-]+$/);
  }
  for (const empty of [null, undefined, {}, [], ['  '], [42]]) {
    assert.equal(srv.canaryHeadersBody(empty), null, JSON.stringify(empty));
  }
});

// ---------------------------------------------------------------------------
// R16 / R4 — the upstream report, the only push a dead run makes
// ---------------------------------------------------------------------------

test('R16: reportUpstream sends upstream_error and the header names, and no text', async () => {
  const f = fakeFetch(fail(502, {
    status: 'refused', error: 'upstream_unavailable',
    error_description: "the skill reported its upstream connection as 'dbsc_canary'; nothing was stored",
    next_step: 'ask Javis to re-authorise the connection, then run the fetch again; no wiki content was lost and nothing was changed',
    canary: { flagged: true, first: true, headers: ['sec-session-id'] },
  }));
  const out = await srv.reportUpstream({
    sourceId: UUID, upstreamError: 'dbsc_canary',
    responseHeaders: { 'sec-session-id': '' },
  }, deps(f));

  const body = f.calls[0].body;
  assert.equal(f.calls[0].url.endsWith(srv.ENDPOINTS.push), true);
  assert.equal(body.upstream_error, 'dbsc_canary');
  assert.deepEqual(body.response_headers, { 'sec-session-id': '' });
  assert.equal('text' in body, false, 'there is no note to send: the fetch never got one');
  // The expected answer IS the refusal, and it carries the canary the server
  // has now recorded as a first appearance.
  assert.equal(out.error, 'upstream_unavailable');
  assert.equal(srv.canaryFrom(out.detail).first, true);
});

test('R16: reportUpstream will not post a source id that is not a uuid', async () => {
  const f = fakeFetch(ok({}));
  const out = await srv.reportUpstream({ sourceId: 'not-a-uuid', upstreamError: 'session_dead' }, deps(f));
  assert.equal(out.error, 'source_id_invalid');
  assert.equal(f.calls.length, 0);
});

// ---------------------------------------------------------------------------
// R4 / R5 — one code, one reason, one next action
// ---------------------------------------------------------------------------

test('R4 R5 TC-S1-3: a hash mismatch is the server\'s code, reason and next action', async () => {
  // The server's actual answer for this case: `invalid_request`, with the
  // field named in error_description and the fix in next_step.
  const f = fakeFetch(fail(400, {
    status: 'refused', error: 'invalid_request',
    error_description: 'body_hash does not match the text',
    next_step: 'fix the named field and push again; hash the normalised text with sha256 and send exactly the bytes you hashed',
  }));
  const out = await srv.pushSource(note(), deps(f));
  assert.equal(srv.failed(out), true);
  assert.equal(out.error, 'invalid_request');
  const d = srv.describeRefusal(out);
  assert.match(d.reason, /body_hash does not match the text/);
  assert.match(d.next, /hash the normalised text/);
});

test('R5: the server\'s next_step beats this bundle\'s row, for every code', async () => {
  // R5's failure mode is not a missing action, it is a USELESS one: the server
  // computed an action against this request and the transport used to drop it
  // for "report the code verbatim and stop".
  for (const code of Object.keys(srv.REFUSALS)) {
    const out = await srv.pushSource(note(), deps(fakeFetch(fail(400, {
      status: 'refused', error: code,
      error_description: `the server's own reason for ${code}`,
      next_step: `the server's own action for ${code}`,
    }))));
    const d = srv.describeRefusal(out);
    assert.equal(d.code, code);
    assert.equal(d.reason, `the server's own reason for ${code}`);
    assert.equal(d.next, `the server's own action for ${code}`);
  }
});

test('R5: a code that arrives with no next_step falls back to this bundle\'s row', async () => {
  const out = await srv.pushSource(note(), deps(fakeFetch(fail(409, { error: 'conflict' }))));
  const d = srv.describeRefusal(out);
  assert.equal(d.code, 'conflict');
  assert.match(d.next, /do not re-push under the same id/);
});

test('R4: this bundle has a row for every code javis-server can answer with', () => {
  // REFUSAL_NEXT_STEPS in javis-server app/services/skill_wiki_sources.py.
  // test/contract.test.js reads that file; this is the list it must match.
  for (const code of [
    'invalid_request', 'unsupported_source_type', 'payload_too_large',
    'quota_exceeded', 'conflict', 'budget_exhausted', 'upstream_unavailable',
    'internal_error',
  ]) {
    assert.ok(srv.REFUSALS[code], `no row for the server code ${code}`);
  }
});

test('R4: a server-written sentence is bounded before it is relayed', async () => {
  const out = await srv.pushSource(note(), deps(fakeFetch(fail(400, {
    error: 'invalid_request',
    error_description: 'x'.repeat(5000),
    next_step: 'y'.repeat(5000),
  }))));
  const d = srv.describeRefusal(out);
  assert.ok(d.reason.length <= 400, `reason was ${d.reason.length}`);
  assert.ok(d.next.length <= 400, `next was ${d.next.length}`);
});

test('R4: a refusal envelope read directly (status refused) is still a failure', () => {
  assert.equal(srv.failed({ status: 'refused', error: 'conflict' }), true);
  assert.equal(srv.failed({ status: 'pending', error: null }), false);
  assert.equal(srv.failed({ status: 'unchanged', error: null }), false);
  assert.equal(srv.failed({ status: 'dry_run', error: null }), false);
});

test('R4 R5 TC-S1-3: a 413 maps to the same oversize code normalize.js uses', async () => {
  const f = fakeFetch(fail(413, { error: 'payload_too_large' }));
  const out = await srv.pushSource(note(), deps(f));
  assert.equal(
    out.error, 'payload_too_large',
    'the server\'s own code wins when it sends one',
  );
  // And with no code in the body, the status decides, landing on normalize's name.
  const bare = fakeFetch(fail(413, null));
  assert.equal((await srv.pushSource(note(), deps(bare))).error, 'text_too_large');
});

test('R4 R5 TC-S1-4: every refusal code has exactly one reason and one next action', () => {
  const codes = Object.keys(srv.REFUSALS);
  assert.ok(codes.length >= 7);
  for (const code of codes) {
    const r = srv.REFUSALS[code];
    assert.match(code, /^[a-z][a-z0-9_]*$/);
    assert.ok(r.reason && !r.reason.includes('\n'), `${code}.reason must be one line`);
    assert.ok(r.next && r.next.length > 10, `${code}.next`);
    assert.notEqual(r.reason, r.next, `${code}: the reason and the next action must differ`);
  }
});

test('R4: an unknown server code is reported by name, never dressed up as a known one', () => {
  const d = srv.describeRefusal({ status: 'error', error: 'some_new_code' });
  assert.equal(d.code, 'some_new_code');
  assert.match(d.reason, /some_new_code/);
  assert.match(d.next, /verbatim/);
});

test('R4: a 401 with no body still lands on the unauthorized row', async () => {
  const out = await srv.pushSource(note(), deps(fakeFetch(fail(401, null))));
  assert.equal(out.error, 'unauthorized');
  assert.match(srv.describeRefusal(out).next, /broken container/);
});

test('R4: a bad source id is refused before any request is made', async () => {
  const f = fakeFetch(ok({ status: 'ok' }));
  const out = await srv.pushSource(note({ sourceId: '2EECD5B1-CA2D-493E-A57E-3158F6B8E1B3' }), deps(f));
  assert.equal(out.error, 'source_id_invalid', 'uppercase is refused, not normalised (two spellings would be two rows)');
  assert.equal(f.calls.length, 0);
});

// ---------------------------------------------------------------------------
// postJson's three invariants
// ---------------------------------------------------------------------------

test('a non-2xx is an envelope, not a throw', async () => {
  const out = await srv.postJson('/x', {}, deps(fakeFetch(fail(500, { error: 'boom' }))));
  assert.equal(out.status, 'error');
  assert.equal(out.http_status, 500);
});

test('a network error is an envelope with its own code', async () => {
  const boom = async () => { throw new Error('ECONNREFUSED'); };
  const out = await srv.postJson('/x', {}, { fetch: boom, token: 't' });
  assert.equal(out.error, 'network_error');
  assert.match(srv.describeRefusal(out).next, /nothing was written/);
});

test('a 2xx that is not JSON is unparseable_response, never a bare null', async () => {
  const notJson = async () => ({ ok: true, status: 200, json: async () => { throw new Error('<html>'); } });
  const out = await srv.postJson('/x', {}, { fetch: notJson, token: 't' });
  assert.notEqual(out, null);
  assert.equal(out.error, 'unparseable_response');
});

test('a 2xx that parses to a non-object is also unparseable_response', async () => {
  const out = await srv.postJson('/x', {}, deps(fakeFetch(ok('ok'))));
  assert.equal(out.error, 'unparseable_response');
});

// ---------------------------------------------------------------------------
// …and its fourth: every call is BOUNDED
// ---------------------------------------------------------------------------

test('a wedged javis-server is a network_error, not a hang', async () => {
  // `fetch` with no signal waits ~300s for response headers (undici's
  // default). That is five minutes of a chat turn spent on a server that is up
  // and answering nothing — and `notebooks`/`notes`, which were network-free
  // before they started reporting an R16 sighting, are exactly the commands a
  // user is sitting in front of.
  let signal = null;
  const wedged = async (url, init) => {
    signal = init.signal;
    return new Promise((_, reject) => {
      init.signal.addEventListener('abort', () => reject(init.signal.reason || new Error('aborted')));
    });
  };

  const out = await srv.postJson('/x', {}, { fetch: wedged, token: 't', timeoutMs: 25 });

  assert.equal(out.error, 'network_error', 'a timeout is an unreachable server, not a new code to handle');
  assert.match(out.detail, /timed out/);
  assert.match(srv.describeRefusal(out).next, /nothing was written/);
  assert.ok(signal instanceof AbortSignal, 'the bound travels with the request');
  assert.equal(signal.aborted, true);
});

test('the bound is on the shared transport, so every caller has one', async () => {
  // Not just the listing report: the push, the upstream report and the digest
  // all go through postJson, and a bound one caller passes is a bound the
  // others do not have.
  const seen = [];
  const f = async (url, init) => {
    seen.push(init.signal);
    return { ok: true, status: 200, json: async () => ({ status: 'ok' }) };
  };
  await srv.pushSource(note(), { fetch: f, token: 't' });
  await srv.reportUpstream({ sourceId: UUID, upstreamError: 'dbsc_canary' }, { fetch: f, token: 't' });
  await srv.pushDigest('digest', { fetch: f, token: 't' });

  assert.equal(seen.length, 3);
  for (const s of seen) assert.ok(s instanceof AbortSignal, 'every request carries a bound');
  assert.ok(
    srv.REQUEST_TIMEOUT_MS > 0 && srv.REQUEST_TIMEOUT_MS < 300 * 1000,
    `the default bound must be under undici's ~300s: ${srv.REQUEST_TIMEOUT_MS}`,
  );
});

// ---------------------------------------------------------------------------
// R17 — the wiki path says NotebookLM, not Obsidian
// ---------------------------------------------------------------------------

test('R17 TC-S2-1: the path is rooted at NotebookLM and never at an Obsidian name', () => {
  const p = srv.buildPath('Thermodynamics', '新建记事', UUID);
  assert.equal(p, 'NotebookLM/Thermodynamics/新建记事.md');
  assert.equal(p.startsWith('obsidian'), false);
  assert.doesNotMatch(p.toLowerCase(), /javis-wiki/, 'never under the wiki download root');
});

test('R17: a separator inside a title becomes a hyphen, not a new segment', () => {
  assert.equal(srv.buildPath('A/B', 'C\\D', UUID), 'NotebookLM/A-B/C-D.md');
});

test('R17: an empty title falls back to the note id, so the path is always valid', () => {
  // 4 of the 6 notebooks in the research account have an empty title (F64).
  assert.equal(srv.buildPath('', '', UUID), `NotebookLM/notebook/${UUID}.md`);
  assert.equal(srv.buildPath('   ', null, UUID), `NotebookLM/notebook/${UUID}.md`);
});

test('R17: no path segment is empty, "." or ".." (javis-server refuses those)', () => {
  for (const [book, title] of [['..', '.'], ['.', '..'], ['/', '//'], ['...', '....']]) {
    const p = srv.buildPath(book, title, UUID);
    const segments = p.split('/');
    for (const s of segments) {
      assert.notEqual(s, '');
      assert.notEqual(s, '.');
      assert.notEqual(s, '..');
    }
    assert.ok(p.endsWith('.md'));
    assert.equal(p.startsWith('/'), false, 'the path must be relative');
  }
});

test('R17: an absurd title is truncated and the path stays inside the 1024-char ceiling', () => {
  const p = srv.buildPath('Book', 'x'.repeat(5000), UUID);
  assert.ok(p.length <= srv.MAX_PATH_CHARS, `path was ${p.length} chars`);
  assert.ok(p.startsWith('NotebookLM/Book/'), 'the provenance segments survive the truncation');
  assert.ok(p.endsWith('.md'));
});

test('R17: buildPath is a DISPLAY path and never reaches the wire', async () => {
  // The server derives the locator itself (locator_for) and the request model
  // has no `path`: pydantic dropped this field in silence, so twenty lines of
  // provenance went into a value nothing read.
  const f = fakeFetch(ok(pending()));
  await srv.pushSource(note({ path: 'NotebookLM/Reports/weekly.md' }), deps(f));
  assert.equal('path' in f.calls[0].body, false);
  assert.equal(srv.buildPath('Reports', 'weekly', UUID), 'NotebookLM/Reports/weekly.md');
});

// ---------------------------------------------------------------------------
// The digest call
// ---------------------------------------------------------------------------

test('R10: the digest posts to /api/agent/push with no session_id and no dedup_key', async () => {
  const f = fakeFetch(ok({ status: 'ok' }));
  await srv.pushDigest('hello', deps(f));
  assert.equal(f.calls[0].url.endsWith('/api/agent/push'), true);
  assert.deepEqual(Object.keys(f.calls[0].body).sort(), ['content', 'skill']);
});

test('R10: an empty digest is refused rather than pushed as a blank message', async () => {
  const f = fakeFetch(ok({ status: 'ok' }));
  const out = await srv.pushDigest('   ', deps(f));
  assert.equal(out.error, 'empty_digest');
  assert.equal(f.calls.length, 0);
});
