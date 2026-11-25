'use strict';
// U2 — the notebooklm-py boundary. R15 (TC-S4-3, TC-S0-3), R14 (TC-S5-2),
// R11 (TC-S5-3), R12 (TC-S0-4).
//
// Every test here is in-process against a fake spawn. Nothing reaches Google, a
// Python interpreter or a real cookie jar — which is not only hygiene: the
// container may not have notebooklm-py installed at all this build, so a suite
// that needed it could not run.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const cli = require('../scripts/nlm-cli.js');

const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), 'notebooklm-ingest-cli-'));
process.on('exit', () => fs.rmSync(SCRATCH, { recursive: true, force: true }));

let seq = 0;
function credDir() {
  seq += 1;
  const dir = path.join(SCRATCH, `home-${seq}`);
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

/** A spawn that records its calls and answers from a canned result. */
function fakeSpawn(result) {
  const calls = [];
  const fn = async (bin, argv, options) => {
    calls.push({ bin, argv, env: options.env });
    return typeof result === 'function' ? result(bin, argv, options) : result;
  };
  fn.calls = calls;
  return fn;
}

const exit0 = (stdout = '') => ({ code: 0, stdout, stderr: '' });
const exitN = (code, stderr) => ({ code, stdout: '', stderr });

function deps(spawn, env = {}) {
  return {
    spawn,
    env: Object.assign({ NOTEBOOKLM_HOME: credDir(), HOME: SCRATCH }, env),
  };
}

// ---------------------------------------------------------------------------
// R15 — the transport pin (TC-S4-3)
// ---------------------------------------------------------------------------

test('R15 TC-S4-3: the child env has no transport variable, so the library default runs', async () => {
  const spawn = fakeSpawn(exit0('6 notebooks'));
  const out = await cli.run(cli.argvNotebooks('spike'), deps(spawn));
  assert.equal(out.ok, true);
  assert.equal(spawn.calls.length, 1);
  assert.equal(
    Object.prototype.hasOwnProperty.call(spawn.calls[0].env, 'NOTEBOOKLM_TRANSPORT'), false,
    'the variable must be deleted, not set — pinning by removal survives an upstream rename',
  );
  assert.equal(out.transport, cli.DEFAULT_TRANSPORT);
});

test('R15 TC-S4-3: an inherited banned transport is a REFUSAL, not a silent override', async () => {
  const spawn = fakeSpawn(exit0());
  const out = await cli.run(
    cli.argvNotebooks('spike'),
    deps(spawn, { NOTEBOOKLM_TRANSPORT: cli.FORBIDDEN_TRANSPORT }),
  );
  assert.equal(out.ok, false);
  assert.equal(out.error, 'transport_forbidden');
  assert.equal(spawn.calls.length, 0, 'nothing may be spawned once the env declares the banned transport');
  assert.match(out.next, /unset NOTEBOOKLM_TRANSPORT/);
  assert.match(out.next, /spec change/, 'R15: it is a design change, never an ops fix');
});

test('R15: the refusal is case- and whitespace-insensitive (an ops value is hand-typed)', async () => {
  for (const value of [' CURL_CFFI ', 'Curl_Cffi', cli.FORBIDDEN_TRANSPORT.toUpperCase()]) {
    const spawn = fakeSpawn(exit0());
    const out = await cli.run(cli.argvDoctor('p'), deps(spawn, { NOTEBOOKLM_TRANSPORT: value }));
    assert.equal(out.error, 'transport_forbidden', `value ${JSON.stringify(value)} must still be refused`);
  }
});

test('R15: any other named transport is ignored with a warning, and the default still runs', async () => {
  const built = cli.buildEnv({ NOTEBOOKLM_TRANSPORT: 'something-else' });
  assert.equal(built.ok, true);
  assert.equal(built.transport, cli.DEFAULT_TRANSPORT);
  assert.match(built.warning, /pinned to the library default/);
  assert.equal(Object.prototype.hasOwnProperty.call(built.env, 'NOTEBOOKLM_TRANSPORT'), false);
});

test('R15: naming the default explicitly is not a warning', () => {
  const built = cli.buildEnv({ NOTEBOOKLM_TRANSPORT: cli.DEFAULT_TRANSPORT });
  assert.equal(built.ok, true);
  assert.equal(built.warning, null);
});

test('R15 TC-S4-3: a stderr mention of the banned transport classifies as transport_forbidden', () => {
  // The library's own error when the opt-in path is half-configured. It must
  // not be reported as a generic failure — R15 is the reason this skill exists
  // in its current shape, and a run that touched that path at all is news.
  const stderr = 'ImportError: curl_cffi is required for this transport'; // never selected
  const out = cli.classify(exitN(1, stderr));
  assert.equal(out.error, 'transport_forbidden');
});

// ---------------------------------------------------------------------------
// R14 — the credential path (TC-S5-2, TC-S0-3)
// ---------------------------------------------------------------------------

test('R14 TC-S0-3: a writable credential directory passes the probe and leaves nothing behind', () => {
  const dir = credDir();
  const out = cli.probeCredentialPath({ NOTEBOOKLM_HOME: dir });
  assert.equal(out.ok, true);
  assert.equal(out.path, dir);
  assert.deepEqual(fs.readdirSync(dir), [], 'the probe file must be removed');
});

test('R14 TC-S0-3: a read-only credential directory is a named refusal before any read', async () => {
  const spawn = fakeSpawn(exit0('notes'));
  const readonlyFs = {
    mkdirSync: () => {},
    writeFileSync: () => { const e = new Error('EROFS: read-only file system'); e.code = 'EROFS'; throw e; },
    unlinkSync: () => {},
  };
  const out = await cli.run(cli.argvNoteGet('abc', 'p'), {
    spawn, env: { NOTEBOOKLM_HOME: '/mnt/ro' }, fs: readonlyFs,
  });
  assert.equal(out.ok, false);
  assert.equal(out.error, 'credential_path_readonly');
  assert.equal(spawn.calls.length, 0, 'the probe runs BEFORE the read, so a stale-out cannot be reported as a dead session');
  assert.match(out.next, /read-write/);
  assert.match(out.reason, /rotated cookies cannot persist/);
  assert.match(out.next, /600 s/, 'R14: the 600-second cadence is why this matters');
});

test('R14: the credential directory falls back to ~/.notebooklm when NOTEBOOKLM_HOME is unset', () => {
  assert.equal(cli.credentialDir({ HOME: '/home/node' }), '/home/node/.notebooklm');
  assert.equal(cli.credentialDir({ HOME: '/home/node', NOTEBOOKLM_HOME: '  ' }), '/home/node/.notebooklm');
  assert.equal(cli.credentialDir({ NOTEBOOKLM_HOME: '/creds' }), '/creds');
});

test('R14 F44: the jar path is <home>/profiles/<profile>/storage_state.json', () => {
  assert.equal(
    cli.credentialJarPath({ NOTEBOOKLM_HOME: '/creds' }, 'spike'),
    '/creds/profiles/spike/storage_state.json',
  );
  assert.equal(
    cli.credentialJarPath({ NOTEBOOKLM_HOME: '/creds' }, undefined),
    '/creds/profiles/default/storage_state.json',
  );
});

test('R14 TC-S5-2: the fingerprint reports mtime, size and a digest — never a cookie', () => {
  const dir = credDir();
  const jar = cli.credentialJarPath({ NOTEBOOKLM_HOME: dir }, 'spike');
  fs.mkdirSync(path.dirname(jar), { recursive: true });
  // A jar-shaped fixture with a cookie-shaped value, so the assertion below is
  // about this function and not about the fixture being empty.
  fs.writeFileSync(jar, JSON.stringify({ cookies: [{ name: 'LSID', value: 'SECRET-VALUE-DO-NOT-PRINT' }] }));

  const fp = cli.credentialFingerprint({ NOTEBOOKLM_HOME: dir }, 'spike');
  assert.equal(fp.present, true);
  assert.equal(fp.path, jar);
  assert.ok(fp.bytes > 0);
  assert.match(fp.digest, /^[0-9a-f]{64}$/);
  assert.match(fp.mtime, /^\d{4}-\d{2}-\d{2}T/);

  const rendered = JSON.stringify(fp);
  assert.equal(rendered.includes('SECRET-VALUE-DO-NOT-PRINT'), false, 'no cookie value may appear');
  assert.equal(rendered.includes('LSID'), false, 'not even a cookie NAME is reported');
});

test('R14: a missing jar is reported as absent rather than throwing', () => {
  const fp = cli.credentialFingerprint({ NOTEBOOKLM_HOME: path.join(SCRATCH, 'nope') }, 'p');
  assert.equal(fp.present, false);
  assert.equal(fp.digest, undefined);
});

// ---------------------------------------------------------------------------
// Argv construction — arrays, never shell strings
// ---------------------------------------------------------------------------

test('argv: the global profile flag comes first and every command is an array', () => {
  assert.deepEqual(cli.argvNotebooks('spike'), ['-p', 'spike', 'list']);
  assert.deepEqual(cli.argvNoteList('nb-1', 'spike'), ['-p', 'spike', 'note', 'list', 'nb-1']);
  assert.deepEqual(cli.argvNoteGet('n-1', 'spike'), ['-p', 'spike', 'note', 'get', 'n-1']);
  assert.deepEqual(cli.argvAuthCheck('spike'), ['-p', 'spike', 'auth', 'check']);
  assert.deepEqual(cli.argvAuthCheck('spike', { test: true }), ['-p', 'spike', 'auth', 'check', '--test']);
  assert.deepEqual(cli.argvDoctor('spike'), ['-p', 'spike', 'doctor']);
  assert.deepEqual(
    cli.argvDownloadReport('r-1', '/tmp/r.md', 'spike'),
    ['-p', 'spike', 'download', 'report', 'r-1', '/tmp/r.md'],
  );
});

test('argv: a hostile notebook title is one argument, not shell syntax', () => {
  const argv = cli.argvNoteGet('x"; rm -rf / #', 'p');
  assert.deepEqual(argv, ['-p', 'p', 'note', 'get', 'x"; rm -rf / #']);
  assert.equal(argv.length, 5, 'the injection attempt stays a single argv element');
});

test('argv: a missing id throws rather than building a command that means something else', () => {
  assert.throws(() => cli.argvNoteGet('', 'p'), /noteId is required/);
  assert.throws(() => cli.argvNoteList(null, 'p'), /notebookId is required/);
  assert.throws(() => cli.argvDownloadReport('r', '', 'p'), /destination is required/);
});

test('argv: no profile omits the flag entirely rather than passing an empty one', () => {
  assert.deepEqual(cli.argvNotebooks(undefined), ['list']);
});

// ---------------------------------------------------------------------------
// R11 — classification (TC-S5-3)
// ---------------------------------------------------------------------------

test('R11 TC-S5-3: a dead session is its own code with a re-authorise next action', async () => {
  const spawn = fakeSpawn(exitN(1, 'AuthError: CookieMismatch — the stored session is no longer valid'));
  const out = await cli.run(cli.argvNoteGet('n-1', 'p'), deps(spawn));
  assert.equal(out.ok, false);
  assert.equal(out.error, 'session_dead');
  assert.match(out.next, /re-authoris/i);
  assert.match(out.next, /no wiki content was lost/, 'R11: the message must say nothing was lost');
});

test('R11: a password change reads as a dead session (F33), not a generic failure', async () => {
  const spawn = fakeSpawn(exitN(1, 'notebooklm.errors.AuthError: not authenticated; please sign in again'));
  const out = await cli.run(cli.argvNotebooks('p'), deps(spawn));
  assert.equal(out.error, 'session_dead');
});

test('R4: the location gate, the rate limit and a missing CLI are three distinct codes', async () => {
  const cases = [
    ['location_gate', 'redirected to ?location=unsupported'],
    ['rate_limited', 'RateLimitError: too many requests'],
    ['cli_missing', 'ModuleNotFoundError: No module named notebooklm'],
  ];
  for (const [code, stderr] of cases) {
    const out = await cli.run(cli.argvNotebooks('p'), deps(fakeSpawn(exitN(1, stderr))));
    assert.equal(out.error, code, stderr);
    assert.ok(out.reason && out.next, `${code} must carry a reason and a next action`);
  }
});

test('R4: ENOENT from spawn is cli_missing, with an install next action', async () => {
  const boom = async () => { const e = new Error('spawn notebooklm ENOENT'); e.code = 'ENOENT'; throw e; };
  const out = await cli.run(cli.argvDoctor('p'), deps(boom));
  assert.equal(out.error, 'cli_missing');
  assert.match(out.next, /install notebooklm-py/);
  assert.equal(out.exit, null);
});

test('R4: exit 127 is cli_missing even with empty stderr', () => {
  assert.equal(cli.classify({ code: 127, stdout: '', stderr: '' }).error, 'cli_missing');
});

test('R16: a Sec-Session-* sighting wins over every other pattern and is its own canary code', () => {
  // DBSC never engaged in research (F56). The first sighting is a design-level
  // event, so it must not be swallowed by the auth pattern it arrives beside.
  const out = cli.classify(exitN(1, 'AuthError: response carried Sec-Session-Id; not authenticated'));
  assert.equal(out.error, 'dbsc_canary');
  assert.match(out.next, /not a retry/);
});

test('R4: an unrecognised failure is nlm_failed and carries the LAST line of stderr', () => {
  const out = cli.classify(exitN(3, 'Traceback (most recent call last):\n  File "x"\nValueError: boom'));
  assert.equal(out.error, 'nlm_failed');
  assert.equal(out.detail, 'ValueError: boom', 'a traceback\'s useful half is its last line');
  assert.equal(out.exit, 3);
});

test('R4: the detail a refusal carries is bounded (it is rendered into the user\'s chat)', () => {
  const out = cli.classify(exitN(1, `x${'y'.repeat(5000)}`));
  assert.ok(out.detail.length <= 300, `detail was ${out.detail.length} chars`);
});

test('every refusal code carries exactly one reason and one next action (R4, R5)', () => {
  for (const [code, r] of Object.entries(cli.REFUSALS)) {
    assert.match(code, /^[a-z][a-z0-9_]*$/);
    assert.ok(r.reason && !r.reason.includes('\n'), `${code}.reason`);
    assert.ok(r.next && r.next.length > 10, `${code}.next`);
  }
});

// ---------------------------------------------------------------------------
// preflight — the doctor answer (R11 + R14 + R15 in one call)
// ---------------------------------------------------------------------------

test('doctor: reports the effective transport, the credential state and the auth check', async () => {
  const dir = credDir();
  const spawn = fakeSpawn(exit0('Token fetch PASS\nNotebooks 6'));
  const report = await cli.preflight('spike', { spawn, env: { NOTEBOOKLM_HOME: dir } });
  assert.equal(report.transport, cli.DEFAULT_TRANSPORT);
  assert.equal(report.transport_pinned, true);
  assert.equal(report.credential_writable, true);
  assert.deepEqual(report.checks.map((c) => [c.check, c.ok]), [['credential_path', true], ['auth', true]]);
  assert.deepEqual(spawn.calls[0].argv, ['-p', 'spike', 'auth', 'check', '--test']);
});

test('doctor: stops at the transport refusal and never probes or spawns', async () => {
  const spawn = fakeSpawn(exit0());
  const report = await cli.preflight('spike', {
    spawn, env: { NOTEBOOKLM_HOME: credDir(), NOTEBOOKLM_TRANSPORT: cli.FORBIDDEN_TRANSPORT },
  });
  assert.equal(report.transport_pinned, false);
  assert.equal(report.transport, null);
  assert.deepEqual(report.checks.map((c) => c.check), ['transport']);
  assert.equal(spawn.calls.length, 0);
});

test('doctor: a dead session is reported as a failed auth check, not as a crash', async () => {
  const report = await cli.preflight('spike', {
    spawn: fakeSpawn(exitN(1, 'CookieMismatch')),
    env: { NOTEBOOKLM_HOME: credDir() },
  });
  const auth = report.checks.find((c) => c.check === 'auth');
  assert.equal(auth.ok, false);
  assert.equal(auth.error, 'session_dead');
  assert.match(auth.next, /re-authoris/i);
});

// ---------------------------------------------------------------------------
// The child environment is an ALLOWLIST (the container's bearer token is in
// this process's env, and the child is a third-party Python CLI)
// ---------------------------------------------------------------------------

test('the spawned CLI never sees OPENCLAW_GATEWAY_TOKEN', () => {
  const built = cli.buildEnv({
    HOME: '/home/node',
    PATH: '/usr/bin',
    NOTEBOOKLM_HOME: '/data/creds',
    OPENCLAW_GATEWAY_TOKEN: 'gw-SECRET',
    JAVIS_SERVER_URL: 'http://javis-server:8000',
    AWS_SECRET_ACCESS_KEY: 'also-SECRET',
  });
  assert.equal(built.ok, true);
  assert.equal(JSON.stringify(built.env).includes('SECRET'), false);
  assert.equal('OPENCLAW_GATEWAY_TOKEN' in built.env, false);
  assert.equal('JAVIS_SERVER_URL' in built.env, false);
  // …while everything the CLI genuinely needs is still there.
  assert.equal(built.env.HOME, '/home/node');
  assert.equal(built.env.PATH, '/usr/bin');
  assert.equal(built.env.NOTEBOOKLM_HOME, '/data/creds');
});

test('an allowlist, not a subtraction: a variable nobody listed does not travel', () => {
  const built = cli.buildEnv({ HOME: '/h', SOME_FUTURE_SECRET: 'x', NOTEBOOKLM_PROFILE: 'default' });
  assert.deepEqual(Object.keys(built.env).sort(), ['HOME', 'NOTEBOOKLM_PROFILE']);
  assert.ok(cli.ENV_ALLOWLIST.includes('HOME'));
  assert.equal(cli.ENV_ALLOWLIST.includes('OPENCLAW_GATEWAY_TOKEN'), false);
});

test('the proxy and certificate variables an egress needs are allowed through', () => {
  const built = cli.buildEnv({
    HTTPS_PROXY: 'http://proxy:3128', https_proxy: 'http://proxy:3128',
    SSL_CERT_FILE: '/etc/ssl/cert.pem', TZ: 'America/Los_Angeles',
  });
  assert.equal(built.env.HTTPS_PROXY, 'http://proxy:3128');
  assert.equal(built.env.SSL_CERT_FILE, '/etc/ssl/cert.pem');
  assert.equal(built.env.TZ, 'America/Los_Angeles');
});

test('R15: the transport is still removed even though NOTEBOOKLM_* is allowed through', () => {
  const built = cli.buildEnv({ NOTEBOOKLM_HOME: '/d', NOTEBOOKLM_TRANSPORT: 'something-else' });
  assert.equal(built.ok, true);
  assert.equal('NOTEBOOKLM_TRANSPORT' in built.env, false);
  assert.equal(built.env.NOTEBOOKLM_HOME, '/d');
});

// ---------------------------------------------------------------------------
// R16 — the canary's header names, for the report javis-server records
// ---------------------------------------------------------------------------

test('R16: the Sec-Session-* names are extracted so the sighting can be reported', () => {
  const names = cli.secSessionHeaders(
    'HTTP/2 401\nSec-Session-Registration: challenge=abc\nsec-session-id: 7\nDate: now',
  );
  assert.deepEqual(names, ['sec-session-registration', 'sec-session-id']);
});

test('R16: the extracted names are bounded and shaped, because they go into a request body', () => {
  const flood = Array.from({ length: 50 }, (_, i) => `Sec-Session-${i}`).join('\n');
  const names = cli.secSessionHeaders(flood);
  assert.ok(names.length <= cli.MAX_CANARY_HEADERS, `${names.length} names`);
  for (const n of names) assert.match(n, /^sec-session-[a-z0-9-]*$/);
  assert.deepEqual(cli.secSessionHeaders(''), []);
  assert.deepEqual(cli.secSessionHeaders(null), []);
});

test('R16: a classified canary carries the names with it', () => {
  const out = cli.classify({ code: 1, stdout: '', stderr: 'blocked: Sec-Session-Id required' });
  assert.equal(out.error, 'dbsc_canary');
  assert.deepEqual(out.headers, ['sec-session-id']);
});

test('R16 F5a: a SUCCESSFUL call whose headers carry Sec-Session-* still fires the canary', async () => {
  // The break this covers: `run` returned `{ok: true}` the moment the exit
  // code was 0, so `classify` never saw a successful call's output — and
  // `Sec-Session-Registration` is precisely the header Google sends on a call
  // that WORKS, as the invitation to bind the session to a device key. The
  // tripwire could therefore only ever fire months later, as a 401, long
  // after DBSC enforcement had broken the path.
  const spawn = fakeSpawn({
    code: 0,
    stdout: '# Entropy\n\nthe note body\n',
    stderr: 'HTTP/2 200\nSec-Session-Registration: challenge=abc, path="/dbsc"\n',
  });
  const out = await cli.run(cli.argvNoteGet('n-1', 'p'), deps(spawn));
  assert.equal(out.ok, false, 'a zero exit must not outrank the canary');
  assert.equal(out.error, 'dbsc_canary');
  assert.deepEqual(out.headers, ['sec-session-registration']);
  assert.equal(out.exit, 0, 'the exit code is reported as it was, not invented');
  assert.equal(out.transport, cli.DEFAULT_TRANSPORT, 'the run still says which transport it used');
  assert.match(out.next, /canary/i);
});

test('R16 F5a: the note BODY is not the haystack, so a note that types the header is not a sighting', async () => {
  // The other side of the same change. On a successful `note get`, stdout is
  // third-party text from a shared notebook. If it were scanned, a note whose
  // body merely quotes `Sec-Session-Id` would end every run and post a false
  // first-sighting to the account's permanent canary record.
  const spawn = fakeSpawn({
    code: 0,
    stdout: 'Notes on DBSC: the browser sends Sec-Session-Id with each request.\n',
    stderr: '',
  });
  const out = await cli.run(cli.argvNoteGet('n-1', 'p'), deps(spawn));
  assert.equal(out.ok, true);
  assert.equal(out.stdout.includes('Sec-Session-Id'), true, 'the body is delivered intact');
});

test('R16: an ordinary failure carries no headers field at all', () => {
  const out = cli.classify({ code: 1, stdout: '', stderr: 'ValueError: nope' });
  assert.equal(out.error, 'nlm_failed');
  assert.equal('headers' in out, false);
});
