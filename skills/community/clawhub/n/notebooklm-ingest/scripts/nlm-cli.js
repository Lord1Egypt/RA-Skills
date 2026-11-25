'use strict';
/**
 * The notebooklm-py boundary — the ONLY place this bundle spawns `notebooklm`.
 *
 * Spec: javis.is/docs/superpowers/specs/2026-10-29-notebooklm-connector-design.md
 *       R11, R14, R15; research F4, F32, F33, F44-F52, F54, F56, F59, F62.
 * Contract: references/cli-contract.md (command surface, env table, jar location).
 *
 * Everything that touches Google is behind this file, and everything in it is
 * injectable — `deps.spawn`, `deps.env`, `deps.fs` — the same way
 * gmail-wiki-ingest injects `deps.fetch` / `deps.now` / `deps.statePath`. The
 * reason is not test hygiene: notebooklm-py may not even be installed in the
 * container this build (the Python runtime is DeepShareIAC's, deferred), so a
 * suite that needed the real CLI could not run at all. Every test in
 * test/nlm-cli.test.js is in-process against a fake spawn, and none of them
 * reaches Google, a Python interpreter, or a cookie jar.
 *
 * THREE HARD RULES LIVE HERE.
 *
 * 1. **The transport is pinned to the library default (R15).** `buildEnv`
 *    deletes `NOTEBOOKLM_TRANSPORT` from the child environment, so the default
 *    httpx path is what runs. If the inherited environment names the
 *    impersonating transport, this module REFUSES to spawn rather than
 *    overriding it quietly: an ops-set variable is a person declaring intent,
 *    and the spec's anti-goal is explicit that selecting it is a design change
 *    requiring approval, never an ops fix (F62). A silent override would hide
 *    the attempt; the refusal surfaces it.
 *
 * 2. **The credential directory is write-probed before any read (R14).**
 *    Google rotates these cookies on a measured 600-second cadence (F59) and
 *    the library writes the refreshed jar back to disk. A read-only path does
 *    not fail at mount time — it fails ten minutes later, silently, and every
 *    later call fails with a dead session (F54, upstream #312). Probing turns
 *    that into a named refusal before the first read instead of a mystery the
 *    next morning.
 *
 * 3. **No cookie value is ever read, printed or logged.** The bundle reports
 *    the jar's path, its mtime and a digest of it — never its contents. See
 *    references/credential-contract.md; TC-S5-2 records a hash for exactly this
 *    reason.
 *
 * Failure classification is the other half of the file. A non-zero exit becomes
 * one machine-readable code with one reason and one next action (R4, R5), so
 * the agent is never left reading a Python traceback and guessing.
 */

const fsNode = require('fs');
const pathNode = require('path');
const crypto = require('crypto');
const { spawn: spawnNode } = require('child_process');

/** The console script notebooklm-py installs. */
const BIN = 'notebooklm';

/**
 * The library's default transport, and the one this bundle pins to.
 * The impersonating alternative is named once, below, only to be refused.
 */
const DEFAULT_TRANSPORT = 'httpx';

/**
 * The transport this bundle must NEVER select: a TLS/JA3 fingerprint
 * impersonation path the library itself labels a PoC (F62). Naming it is how
 * the refusal is written; nothing here can switch it on.
 */
const FORBIDDEN_TRANSPORT = 'curl_cffi';

/** How long a spawned CLI call may take before it is abandoned. */
const SPAWN_TIMEOUT_MS = 180 * 1000;

/** Stdout we are willing to buffer from one call (a note is ≤ 256 KiB). */
const MAX_STDOUT_BYTES = 4 * 1024 * 1024;

const REFUSALS = Object.freeze({
  cli_missing: {
    reason: 'the notebooklm CLI is not installed in this container',
    next: 'ask Samuel to install notebooklm-py in the container image, then run doctor again',
  },
  session_dead: {
    reason: 'the stored Google session no longer authenticates',
    next: 'offer to re-authorise: the sign-in is done by the user in a webview, and no wiki content was lost',
  },
  location_gate: {
    reason: 'Google answered the unsupported-location gate for this host',
    next: 'report the gate and stop; do not retry from another egress, and consider moving the bridge host',
  },
  rate_limited: {
    reason: 'Google rate-limited this account',
    next: 'stop for now and let the next scheduled run pick the notes up; nothing was lost',
  },
  transport_forbidden: {
    reason: `the environment names the impersonating transport, which this skill must never select (${FORBIDDEN_TRANSPORT} is banned by design)`,
    next: 'unset NOTEBOOKLM_TRANSPORT in the container env and re-run; selecting it needs a spec change, not an ops fix',
  },
  credential_path_readonly: {
    reason: 'the credential directory is not writable, so rotated cookies cannot persist',
    next: 'ask Samuel to mount NOTEBOOKLM_HOME read-write; cookies rotate every 600 s and a read-only path stales out within minutes',
  },
  dbsc_canary: {
    reason: 'the CLI reported a Sec-Session-* device-binding header, which has never appeared on this path before',
    next: 'stop and report the canary: DBSC enforcement reaching this path is a design-level event, not a retry',
  },
  nlm_failed: {
    reason: 'the notebooklm CLI exited non-zero for a reason this skill does not recognise',
    next: 'report the exit code and the last line of stderr, and run doctor before retrying',
  },
});

// ---------------------------------------------------------------------------
// Environment (R15, R14)
// ---------------------------------------------------------------------------

/**
 * The variables the spawned `notebooklm` process is allowed to see.
 *
 * AN ALLOWLIST, NOT A SUBTRACTION. The child is a third-party Python CLI whose
 * ~65 undocumented RPC ids the spec deliberately keeps out of the server tree;
 * handing it the whole container environment hands it `OPENCLAW_GATEWAY_TOKEN`,
 * which is this user's bearer for javis-server. One traceback that renders
 * `os.environ` — ordinary in httpx and Playwright debug paths — and that token
 * is in the captured stderr, which `lastLine()` then relays up to 300
 * characters of into a refusal the agent prints and the state file keeps.
 *
 * Everything the CLI genuinely needs is here: a home and a PATH to find its own
 * interpreter, the proxy and certificate variables an egress may require, the
 * locale, and `NOTEBOOKLM_*` (minus the transport, below) which is its own
 * configuration surface. Anything else a future version wants is added here
 * deliberately, which is the point.
 */
const ENV_ALLOWLIST = Object.freeze([
  'HOME', 'PATH', 'LANG', 'LC_ALL', 'TZ', 'TMPDIR', 'TEMP', 'TMP',
  'HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY', 'ALL_PROXY',
  'http_proxy', 'https_proxy', 'no_proxy', 'all_proxy',
  'SSL_CERT_FILE', 'SSL_CERT_DIR', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE',
  'PLAYWRIGHT_BROWSERS_PATH', 'PYTHONUNBUFFERED', 'PYTHONIOENCODING',
]);

const ENV_PREFIX_RE = /^NOTEBOOKLM_/;

/**
 * The child environment, and the transport pin.
 *
 * Returns `{ok: true, env, transport, warning}` or a refusal envelope. The
 * effective transport is returned rather than assumed, because TC-S4-3 step 2
 * reads it out of the run's own log line.
 */
function buildEnv(baseEnv) {
  const source = baseEnv || {};
  const env = {};
  for (const key of Object.keys(source)) {
    if (ENV_ALLOWLIST.includes(key) || ENV_PREFIX_RE.test(key)) env[key] = source[key];
  }
  const named = String(source.NOTEBOOKLM_TRANSPORT || '').trim().toLowerCase();

  // Pin by removal: with the variable absent the library takes its own default,
  // so the pin cannot drift if the default is ever renamed upstream.
  delete env.NOTEBOOKLM_TRANSPORT;

  if (named === FORBIDDEN_TRANSPORT) {
    return Object.assign(
      { ok: false, error: 'transport_forbidden', detail: 'NOTEBOOKLM_TRANSPORT names the banned transport' },
      REFUSALS.transport_forbidden,
    );
  }

  const warning = named && named !== DEFAULT_TRANSPORT
    ? `NOTEBOOKLM_TRANSPORT=${named} ignored; pinned to the library default`
    : null;

  return { ok: true, env, transport: DEFAULT_TRANSPORT, warning };
}

/**
 * The credential directory: `NOTEBOOKLM_HOME`, else `~/.notebooklm` (F44). The
 * jar itself lives at `<dir>/profiles/<profile>/storage_state.json`.
 */
function credentialDir(baseEnv) {
  const source = baseEnv || {};
  if (source.NOTEBOOKLM_HOME && String(source.NOTEBOOKLM_HOME).trim()) {
    return String(source.NOTEBOOKLM_HOME);
  }
  return pathNode.join(String(source.HOME || ''), '.notebooklm');
}

/** Where the Playwright cookie jar sits for a profile (F44). Path only. */
function credentialJarPath(baseEnv, profile) {
  return pathNode.join(credentialDir(baseEnv), 'profiles', String(profile || 'default'), 'storage_state.json');
}

/**
 * Write-probe the credential directory (R14).
 *
 * Creates the directory if it is missing, writes and removes a probe file, and
 * refuses if either fails. A read-only mount is then a named refusal at the top
 * of the run rather than a dead session ten minutes in.
 */
function probeCredentialPath(baseEnv, deps = {}) {
  const fs = deps.fs || fsNode;
  const dir = credentialDir(baseEnv);
  const probe = pathNode.join(dir, `.javis-write-probe-${process.pid}`);
  try {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(probe, 'probe');
    fs.unlinkSync(probe);
    return { ok: true, path: dir };
  } catch (e) {
    return Object.assign(
      { ok: false, error: 'credential_path_readonly', detail: `${dir}: ${e && e.message ? e.message : e}` },
      REFUSALS.credential_path_readonly,
    );
  }
}

/**
 * What the bundle is allowed to say about the stored credential: where it is,
 * whether it exists, when it last changed, how big it is, and a digest.
 * **Never a cookie name and never a value** — the digest is what TC-S5-2
 * compares across a rotation window.
 */
function credentialFingerprint(baseEnv, profile, deps = {}) {
  const fs = deps.fs || fsNode;
  const file = credentialJarPath(baseEnv, profile);
  try {
    const stat = fs.statSync(file);
    const digest = crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
    return { path: file, present: true, bytes: stat.size, mtime: new Date(stat.mtimeMs).toISOString(), digest };
  } catch (_) {
    return { path: file, present: false };
  }
}

// ---------------------------------------------------------------------------
// Argv constructors — never a shell string
// ---------------------------------------------------------------------------
/**
 * Every command is built as an ARRAY, so a notebook title with a quote or a
 * semicolon in it is an argument rather than shell syntax. The global
 * `-p <profile>` comes first, as the CLI requires.
 *
 * Only the commands research verified exist are constructed here (F4,
 * F44-F52): `list`, `note list`, `note get`, `download report`, `auth check`,
 * `doctor`. No flag is invented — notably no `--json`, which nothing in the
 * research confirms — so stdout comes back as text and SKILL.md's flow has the
 * agent read it. That is the house split: thin script, thick SKILL.md.
 */
function globals(profile) {
  return profile ? ['-p', String(profile)] : [];
}

function argvNotebooks(profile) {
  return [...globals(profile), 'list'];
}

function argvNoteList(notebookId, profile) {
  if (!notebookId || !String(notebookId).trim()) throw new Error('argvNoteList: notebookId is required');
  return [...globals(profile), 'note', 'list', String(notebookId)];
}

function argvNoteGet(noteId, profile) {
  if (!noteId || !String(noteId).trim()) throw new Error('argvNoteGet: noteId is required');
  return [...globals(profile), 'note', 'get', String(noteId)];
}

function argvDownloadReport(reportId, destination, profile) {
  if (!reportId || !String(reportId).trim()) throw new Error('argvDownloadReport: reportId is required');
  if (!destination || !String(destination).trim()) throw new Error('argvDownloadReport: destination is required');
  return [...globals(profile), 'download', 'report', String(reportId), String(destination)];
}

function argvAuthCheck(profile, { test = false } = {}) {
  const argv = [...globals(profile), 'auth', 'check'];
  if (test) argv.push('--test');
  return argv;
}

function argvDoctor(profile) {
  return [...globals(profile), 'doctor'];
}

// ---------------------------------------------------------------------------
// Failure classification (R11, R4, R5)
// ---------------------------------------------------------------------------

/**
 * Patterns are matched in this order, most specific first. The canary comes
 * before everything because a `Sec-Session-*` sighting changes what the whole
 * design believes (F56) and must not be swallowed by a generic auth match.
 */
const PATTERNS = [
  ['dbsc_canary', /sec-session-/i],
  ['transport_forbidden', new RegExp(FORBIDDEN_TRANSPORT.replace('_', '[_-]'), 'i')],
  ['location_gate', /location=unsupported|unsupported[_ -]?location/i],
  ['rate_limited', /ratelimit|rate[ _-]?limit|too many requests|\b429\b/i],
  [
    'session_dead',
    /cookiemismatch|not authenticated|authentication (failed|expired)|auth ?error|sid cookie|sign ?in again|re-?authenticat|401 unauthorized|invalid credentials/i,
  ],
  ['cli_missing', /no module named|command not found|is not recognized|ModuleNotFoundError/i],
];

/**
 * The `Sec-Session-*` header names the CLI output mentions, lowercased.
 *
 * R16's other half. Spotting the canary in this container is only half the
 * requirement — "the FIRST appearance" is a fact about the ACCOUNT, and only
 * javis-server can hold it (`wiki_logs`, op `source_canary`). So the names are
 * extracted here and the caller reports them to the server, rather than the
 * sighting dying as one line in one chat turn.
 *
 * Bounded and shape-checked because this is third-party text on its way into a
 * request body: at most eight names, each at most 64 characters of
 * `[a-z0-9-]`, which is also what the server's gate will reduce them to.
 */
const SEC_SESSION_RE = /sec-session-[a-z0-9-]{0,52}/gi;
const MAX_CANARY_HEADERS = 8;

function secSessionHeaders(text) {
  const found = String(text == null ? '' : text).match(SEC_SESSION_RE) || [];
  const names = [];
  for (const raw of found) {
    const name = raw.toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 64);
    if (name && !names.includes(name)) names.push(name);
    if (names.length >= MAX_CANARY_HEADERS) break;
  }
  return names;
}

/** One refusal envelope out of a spawn result or a spawn error. */
function classify(result) {
  const spawnError = result && result.spawnError;
  if (spawnError) {
    const code = spawnError.code === 'ENOENT' ? 'cli_missing' : 'nlm_failed';
    return Object.assign(
      { ok: false, error: code, detail: String(spawnError.message || spawnError), exit: null },
      REFUSALS[code],
    );
  }

  const exit = result && result.code != null ? Number(result.code) : null;
  const haystack = `${(result && result.stderr) || ''}\n${(result && result.stdout) || ''}`;

  if (exit === 127) {
    return Object.assign({ ok: false, error: 'cli_missing', detail: lastLine(result), exit }, REFUSALS.cli_missing);
  }

  for (const [code, re] of PATTERNS) {
    if (re.test(haystack)) {
      const refusal = Object.assign(
        { ok: false, error: code, detail: lastLine(result), exit }, REFUSALS[code],
      );
      // The canary travels with the refusal so the caller can report the
      // sighting to javis-server, which is where "first appearance" lives.
      if (code === 'dbsc_canary') refusal.headers = secSessionHeaders(haystack);
      return refusal;
    }
  }

  return Object.assign({ ok: false, error: 'nlm_failed', detail: lastLine(result), exit }, REFUSALS.nlm_failed);
}

/**
 * The one line of CLI output a refusal is allowed to carry.
 *
 * Bounded because the detail is rendered into the user's chat, and truncated to
 * the LAST line because a Python traceback's useful half is at the bottom. A
 * cookie value is never in stderr, but the bound is also what keeps a stray one
 * from being relayed wholesale if it ever were.
 */
function lastLine(result) {
  const text = String((result && result.stderr) || (result && result.stdout) || '').trim();
  if (!text) return null;
  const lines = text.split('\n').filter((l) => l.trim());
  return (lines[lines.length - 1] || '').slice(0, 300);
}

// ---------------------------------------------------------------------------
// Spawning
// ---------------------------------------------------------------------------

/**
 * The real spawn, used when no `deps.spawn` is injected. Resolves
 * `{code, stdout, stderr}`; never rejects, because a spawn failure is
 * classified rather than thrown (ENOENT arrives as `spawnError`).
 */
function defaultSpawn(bin, argv, options) {
  return new Promise((resolve) => {
    let child;
    try {
      child = spawnNode(bin, argv, { env: options.env, stdio: ['ignore', 'pipe', 'pipe'] });
    } catch (e) {
      resolve({ spawnError: e });
      return;
    }
    let stdout = '';
    let stderr = '';
    let settled = false;
    const finish = (payload) => {
      if (settled) return;
      settled = true;
      resolve(payload);
    };
    const timer = setTimeout(() => {
      try { child.kill('SIGKILL'); } catch (_) { /* already gone */ }
      finish({ code: 124, stdout, stderr: `${stderr}\ntimed out after ${SPAWN_TIMEOUT_MS} ms` });
    }, SPAWN_TIMEOUT_MS);
    timer.unref ? timer.unref() : null;

    child.stdout.setEncoding('utf8');
    child.stderr.setEncoding('utf8');
    child.stdout.on('data', (d) => {
      if (stdout.length < MAX_STDOUT_BYTES) stdout += d;
    });
    child.stderr.on('data', (d) => {
      if (stderr.length < MAX_STDOUT_BYTES) stderr += d;
    });
    child.on('error', (e) => {
      clearTimeout(timer);
      finish({ spawnError: e });
    });
    child.on('close', (code) => {
      clearTimeout(timer);
      finish({ code, stdout, stderr });
    });
  });
}

/**
 * Run one CLI command with the pin and the probe in front of it.
 *
 * Order matters: the transport pin is checked before anything is spawned, and
 * the credential probe before anything is read, so neither failure can be
 * reported as a dead session. `transport` rides on every result — success and
 * refusal alike — because TC-S4-3 reads it from the run's log line.
 */
async function run(argv, deps = {}) {
  const baseEnv = deps.env || process.env;

  const built = buildEnv(baseEnv);
  if (!built.ok) return built;

  if (deps.skipProbe !== true) {
    const probe = probeCredentialPath(baseEnv, deps);
    if (!probe.ok) return Object.assign(probe, { transport: built.transport });
  }

  const spawnFn = deps.spawn || defaultSpawn;
  let result;
  try {
    result = await spawnFn(deps.bin || BIN, argv, { env: built.env });
  } catch (e) {
    result = { spawnError: e };
  }

  if (result && result.spawnError) {
    return Object.assign(classify(result), { transport: built.transport });
  }
  if (result && Number(result.code) === 0) {
    // R16, and the half that nearly was not here. `Sec-Session-Registration`
    // is how DBSC STARTS: Google sends it on a call that SUCCEEDS, inviting
    // the client to bind the session to a device key. A canary that only ever
    // ran through `classify` — which a zero exit never reached — could not see
    // the one header the tripwire exists for, so it would first fire months
    // later, as a 401, when enforcement had already broken the path.
    //
    // STDERR ONLY, and this is not an optimisation. On a successful
    // `note get`, STDOUT IS THE NOTE — third-party text from a shared
    // notebook. Scanning it would let a note whose body merely types
    // `Sec-Session-Id` end every run and post a false sighting to the
    // account's permanent canary record. Headers are diagnostics; they come
    // out on stderr.
    const canary = { code: result.code, stdout: '', stderr: result.stderr };
    if (secSessionHeaders(result.stderr).length) {
      return Object.assign(classify(canary), { transport: built.transport });
    }
    return {
      ok: true,
      code: 0,
      stdout: String(result.stdout == null ? '' : result.stdout),
      stderr: String(result.stderr == null ? '' : result.stderr),
      transport: built.transport,
      warning: built.warning || undefined,
    };
  }
  return Object.assign(classify(result), { transport: built.transport });
}

/**
 * The preflight `doctor` runs: the effective transport, whether the credential
 * path is writable, what the jar looks like (never its contents), and whether
 * the session still authenticates. R11, R14 and R15 in one answer.
 */
async function preflight(profile, deps = {}) {
  const baseEnv = deps.env || process.env;
  const built = buildEnv(baseEnv);
  const report = {
    transport: built.ok ? built.transport : null,
    transport_pinned: built.ok,
    credential: credentialFingerprint(baseEnv, profile, deps),
    checks: [],
  };
  if (built.warning) report.warning = built.warning;
  if (!built.ok) {
    report.checks.push({ check: 'transport', ok: false, error: built.error, reason: built.reason, next: built.next });
    return report;
  }

  const probe = probeCredentialPath(baseEnv, deps);
  report.credential_writable = probe.ok;
  report.checks.push(probe.ok
    ? { check: 'credential_path', ok: true, path: probe.path }
    : { check: 'credential_path', ok: false, error: probe.error, reason: probe.reason, next: probe.next });
  if (!probe.ok) return report;

  const auth = await run(argvAuthCheck(profile, { test: true }), Object.assign({ skipProbe: true }, deps));
  report.checks.push(auth.ok
    ? { check: 'auth', ok: true }
    : { check: 'auth', ok: false, error: auth.error, reason: auth.reason, next: auth.next, detail: auth.detail });
  return report;
}

module.exports = {
  BIN,
  DEFAULT_TRANSPORT,
  FORBIDDEN_TRANSPORT,
  ENV_ALLOWLIST,
  MAX_CANARY_HEADERS,
  REFUSALS,
  SPAWN_TIMEOUT_MS,
  buildEnv,
  secSessionHeaders,
  credentialDir,
  credentialJarPath,
  credentialFingerprint,
  probeCredentialPath,
  argvNotebooks,
  argvNoteList,
  argvNoteGet,
  argvDownloadReport,
  argvAuthCheck,
  argvDoctor,
  classify,
  run,
  preflight,
};
