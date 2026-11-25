'use strict';
// U8 — THE SEAM. The one suite that reads the OTHER repo.
//
// Why it exists. This bundle and javis-server were built to two different
// contracts and both suites were green: 185 assertions here, 4504 there, and a
// connector that would have 404'd on its first real push. Nothing could catch
// it, because nothing crossed the repo boundary — `test/server.test.js`
// asserted this bundle's own constant, `tests/api/test_skill_wiki_sources.py`
// asserted the server's own route, and neither ever saw the other. Four
// mismatches lived in that gap at once:
//
//   1. the path          /api/skill/sources/push  vs  /api/skill/wiki/sources
//   2. the request       `path` + `notebook` sent, `notebook_id` never sent,
//                        all three silently dropped by pydantic
//   3. the response      read as `pages` / `spend`, answered as
//                        `page` / `feeds` / `budget`
//   4. the refusals      eight codes each, ONE of them shared
//
// So this file reads javis-server's own source — the router, the request model,
// the envelope and the refusal vocabulary — and checks them against what
// scripts/server.js pins. It is deliberately crude (regex over source text, not
// an import): the alternative is running Python from a Node test, and the four
// facts it needs are each one line.
//
// WHEN JAVIS-SERVER IS NOT THERE, every case skips with a reason. That is
// honest rather than silent: in a container, or on a machine with only this
// repo checked out, there is nothing to compare against and a green assertion
// would be a lie. On the workspace machine where both repos sit side by side —
// which is where this build happens, and where the drift happened — it runs.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const srv = require('../scripts/server.js');

/** ClawSkills/notebooklm-ingest/test → the workspace → javis-server. */
const SERVER_REPO = path.resolve(__dirname, '../../../javis-server');
const FILES = {
  router: path.join(SERVER_REPO, 'app/routers/skill_wiki_sources.py'),
  service: path.join(SERVER_REPO, 'app/services/skill_wiki_sources.py'),
  main: path.join(SERVER_REPO, 'app/main.py'),
  gates: path.join(SERVER_REPO, 'app/wiki_source_gates.py'),
};

const PRESENT = Object.values(FILES).every((f) => fs.existsSync(f));
const WHY = `javis-server is not checked out at ${SERVER_REPO}: nothing to compare against`;
const read = (key) => fs.readFileSync(FILES[key], 'utf8');

/** `@router.post("/skill/wiki/sources")` → `/skill/wiki/sources`. */
function routePath(source) {
  const m = source.match(/@router\.post\(\s*["']([^"']+)["']/);
  return m && m[1];
}

/** The `prefix=` this router is mounted under in create_app(). */
function routerPrefix(source) {
  const m = source.match(/skill_wiki_sources\.router,\s*prefix=["']([^"']+)["']/);
  return m && m[1];
}

/** The field names a pydantic model declares, in declaration order. */
function modelFields(source, className) {
  const body = source.split(`class ${className}(BaseModel):`)[1];
  if (!body) return [];
  const upTo = body.split(/\nclass |\n@router/)[0];
  return [...upTo.matchAll(/^ {4}([a-z_][a-z0-9_]*)\s*:/gm)].map((m) => m[1]);
}

/** The keys `_envelope` builds. */
function envelopeKeys(source) {
  const body = source.split('def _envelope(')[1].split('\ndef ')[0];
  return [...body.matchAll(/^\s{8}["']([a-z_]+)["']\s*:/gm)].map((m) => m[1]);
}

/** The codes `REFUSAL_NEXT_STEPS` defines. */
function refusalCodes(source) {
  const body = source.split('REFUSAL_NEXT_STEPS: Dict[str, str] = {')[1].split('\n}')[0];
  return [...body.matchAll(/^\s{4}["']([a-z_]+)["']\s*:/gm)].map((m) => m[1]);
}

test('R2: the path this bundle posts to is the path javis-server serves', { skip: PRESENT ? false : WHY }, () => {
  const served = `${routerPrefix(read('main'))}${routePath(read('router'))}`;
  assert.equal(
    srv.ENDPOINTS.push, served,
    `this bundle posts to ${srv.ENDPOINTS.push}; javis-server serves ${served}`,
  );
});

test('R2: every field this bundle sends is a field the request model declares', { skip: PRESENT ? false : WHY }, async () => {
  const declared = new Set(modelFields(read('router'), 'WikiSourcePushRequest'));
  assert.ok(declared.size >= 8, `only parsed ${declared.size} fields out of the model`);

  const sent = new Set();
  const spy = async (url, init) => {
    for (const k of Object.keys(JSON.parse(init.body))) sent.add(k);
    return { ok: true, status: 202, json: async () => ({ status: 'pending' }) };
  };
  const deps = { fetch: spy, token: 't' };
  const id = '2eecd5b1-ca2d-493e-a57e-3158f6b8e1b3';
  await srv.pushSource({ sourceId: id, title: 't', text: 'x', bodyHash: 'a'.repeat(64), notebook: 'Qwen research' }, deps);
  // The same push WITH a sighting on it (R16): `response_headers` is read off
  // every push by `_canary`, so it has to be a field the model declares here
  // too and not only on the upstream report.
  await srv.pushSource({
    sourceId: id, title: 't', text: 'x', bodyHash: 'a'.repeat(64),
    notebook: 'Qwen research', responseHeaders: ['sec-session-registration'],
  }, deps);
  assert.ok(sent.has('response_headers'), 'the canary must actually be on the push body');
  await srv.reportUpstream({ sourceId: id, upstreamError: 'session_dead', responseHeaders: { 'sec-session-id': '' } }, deps);

  const undeclared = [...sent].filter((k) => !declared.has(k));
  assert.deepEqual(
    undeclared, [],
    `pydantic drops these without a word, so they are a silence and not a contract: ${undeclared.join(', ')}`,
  );
});

test('R20 R9 R16: every key this bundle reads is a key the envelope carries', { skip: PRESENT ? false : WHY }, () => {
  const keys = new Set(envelopeKeys(read('service')));
  assert.ok(keys.size >= 10, `only parsed ${keys.size} envelope keys`);
  // What pagesFrom / budgetFrom / canaryFrom / doPush read off an answer.
  for (const key of ['page', 'feeds', 'budget', 'canary', 'notice', 'status',
    'source_slug', 'error', 'error_description', 'next_step']) {
    assert.ok(keys.has(key), `the envelope has no ${key}`);
  }
  // And the two this bundle used to read, which never existed.
  for (const ghost of ['pages', 'spend']) {
    assert.equal(keys.has(ghost), false, `${ghost} is not an envelope key — do not read it`);
  }
});

test('R4 R5: this bundle has a row for every refusal code javis-server can answer with', { skip: PRESENT ? false : WHY }, () => {
  const codes = refusalCodes(read('service'));
  assert.ok(codes.length >= 8, `only parsed ${codes.length} refusal codes`);
  const missing = codes.filter((c) => !srv.REFUSALS[c]);
  assert.deepEqual(
    missing, [],
    `javis-server can answer with these and this bundle has no row for them: ${missing.join(', ')}`,
  );
});

test('R17: the source type this bundle sends is one javis-server has a slug prefix for', { skip: PRESENT ? false : WHY }, () => {
  const ingest = fs.readFileSync(path.join(SERVER_REPO, 'app/services/obsidian_ingest.py'), 'utf8');
  const block = ingest.split('SLUG_PREFIXES = {')[1].split('}')[0];
  const kinds = [...block.matchAll(/["']([a-z]+)["']\s*:/g)].map((m) => m[1]);
  assert.ok(kinds.includes(srv.SOURCE_TYPE), `no slug prefix for ${srv.SOURCE_TYPE}: ${kinds.join(', ')}`);
  assert.match(block, new RegExp(`["']${srv.SOURCE_TYPE}["']\\s*:\\s*["']${srv.SOURCE_TYPE}-note-["']`));
});

test('R17: the notebook_id this bundle derives passes the server\'s own segment rule', { skip: PRESENT ? false : WHY }, () => {
  const m = read('gates').match(/LOCATOR_SEGMENT_RE = re\.compile\(r"([^"]+)"\)/);
  assert.ok(m, 'could not read LOCATOR_SEGMENT_RE');
  const server = new RegExp(`^${m[1]}$`);
  for (const title of ['Qwen research', 'nb-1', 'A/B notes', 'Thermodynamics!!', '  spaced  ']) {
    const derived = srv.notebookId(title);
    if (derived === null) continue;         // omitted is always safe
    assert.match(derived, server, `${title} → ${derived} would be a hard invalid_request`);
  }
  // And a title with nothing legal in it must be omitted, never sent.
  assert.equal(srv.notebookId('新建记事'), null);
});

test('R16: the canary names this bundle sends survive the server\'s own gate', { skip: PRESENT ? false : WHY }, () => {
  // `sec_session_headers` reads KEYS and keeps only those starting with the
  // prefix, reduced to [a-z0-9._-] and bounded. A body whose names the gate
  // would discard is a sighting the account never records.
  const gates = read('gates');
  const prefix = (gates.match(/SEC_SESSION_PREFIX\s*=\s*["']([^"']+)["']/) || [])[1];
  assert.ok(prefix, 'could not read SEC_SESSION_PREFIX');
  const strip = (gates.match(/_CANARY_NAME_STRIP_RE = re\.compile\(r"([^"]+)"\)/) || [])[1];
  assert.ok(strip, 'could not read _CANARY_NAME_STRIP_RE');
  const maxNames = Number((gates.match(/MAX_CANARY_HEADERS\s*=\s*(\d+)/) || [])[1]);
  const maxChars = Number((gates.match(/MAX_CANARY_NAME_CHARS\s*=\s*(\d+)/) || [])[1]);
  assert.equal(srv.MAX_CANARY_HEADERS, maxNames, 'this bundle bounds the names differently from the server');
  assert.equal(srv.MAX_CANARY_NAME_CHARS, maxChars);

  const body = srv.canaryHeadersBody(['Sec-Session-Registration', 'sec-session-id']);
  const names = Object.keys(body);
  assert.equal(names.length, 2);
  for (const name of names) {
    assert.ok(name.startsWith(prefix), `${name} would be discarded: the gate keeps only ${prefix}*`);
    // Nothing the gate would strip is ever in a name this bundle sends.
    assert.equal(name.replace(new RegExp(strip, 'g'), ''), name);
  }
});
