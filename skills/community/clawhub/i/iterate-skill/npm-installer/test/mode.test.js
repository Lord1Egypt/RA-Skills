/**
 * Unit tests for resolveInstallMode() — the global vs project install-mode
 * decision — and parseChecksums() — the SHA256SUMS.txt parser — in the npx
 * installer. Uses node:assert so no extra test runner is required; run via
 * `npm test`.
 */

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { spawnSync } = require('node:child_process');
const { resolveInstallMode, parseChecksums, constantTimeHashEqual, enforceDownloadedSize, parseArgs, buildPythonInstallArgs, isGithubApiUrl, normalizeToken, validateTokenShape, buildAuthFlags, InstallerError, runCommand, runPythonInstall, signaturePolicyError, allowUnsigned, ALLOW_UNSIGNED_ENV, selectSkillRelease } = require('../lib/installer');

// 64-char lowercase hex digest, as sha256 actually produces.
const H = 'a'.repeat(64);
const I = 'b'.repeat(64);
const J = 'c'.repeat(64);
const K = 'd'.repeat(64);

const originalCwd = process.cwd();
const originalHome = os.homedir;

/**
 * Temporarily set the home directory and chdir into a fresh temp directory
 * (the "current working directory"), then run fn(cwd). Always restores state.
 */
function withHomeAndCwd(home, fn) {
  return (async () => {
    const cwd = fs.mkdtempSync(path.join(os.tmpdir(), 'iterate-mode-'));
    os.homedir = () => home;
    process.chdir(cwd);
    try {
      return await fn(cwd);
    } finally {
      os.homedir = originalHome;
      process.chdir(originalCwd);
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  })();
}

/**
 * Post-download size enforcement.
 *
 * curl's `--max-filesize` is documented as best-effort: it only applies when
 * the server advertises a Content-Length. A response framed with chunked
 * transfer encoding therefore streams to disk with no cap at all, so the
 * installer re-stats the file after the transfer and fails closed.
 */
function testEnforceDownloadedSize() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'iterate-size-'));
  try {
    const ok = path.join(dir, 'ok.bin');
    fs.writeFileSync(ok, Buffer.alloc(10));
    // Under the cap: accepted.
    enforceDownloadedSize(ok, 1024);

    // Exactly at the cap: accepted (the cap is exclusive only above).
    const exact = path.join(dir, 'exact.bin');
    fs.writeFileSync(exact, Buffer.alloc(1024));
    enforceDownloadedSize(exact, 1024);

    // One byte over: refused.
    const big = path.join(dir, 'big.bin');
    fs.writeFileSync(big, Buffer.alloc(1025));
    assert.throws(
      () => enforceDownloadedSize(big, 1024),
      (err) => err instanceof InstallerError && /safety cap/.test(err.message),
      'a file above the cap must raise InstallerError',
    );
    // The oversized payload is removed so a retry cannot reuse it.
    assert.ok(!fs.existsSync(big), 'oversized download must be deleted');

    // A missing file is left to curl's own error reporting, not double-reported.
    enforceDownloadedSize(path.join(dir, 'never-written.bin'), 1024);

    console.log('  ✓ enforceDownloadedSize rejects an uncapped/oversized download');
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

async function run() {
  // 1) Explicit --target is honored without asking.
  await withHomeAndCwd('/home/u', async () => {
    const opts = { global: true, target: '/x', targetExplicit: true, globalExplicit: false };
    const ask = () => { throw new Error('should not ask'); };
    const out = await resolveInstallMode(opts, ask);
    assert.strictEqual(out.target, '/x', 'target should be preserved');
    assert.strictEqual(out.global, true, 'global should be left untouched for explicit target');
  });

  // 2) Explicit --global is honored without asking.
  await withHomeAndCwd('/home/u', async () => {
    const opts = { global: true, target: null, targetExplicit: false, globalExplicit: true };
    const ask = () => { throw new Error('should not ask'); };
    const out = await resolveInstallMode(opts, ask);
    assert.strictEqual(out.global, true, 'global should be preserved');
    assert.strictEqual(out.target, null, 'target should stay null');
  });

  // 3) cwd === home: no ask, stays global.
  await withHomeAndCwd('/home/u', async () => {
    // Use process.cwd() (the resolved path) so home matches cwd exactly,
    // avoiding macOS /var -> /private/var symlink mismatches.
    os.homedir = () => process.cwd();
    const opts = { global: true, target: null, targetExplicit: false, globalExplicit: false };
    const ask = () => { throw new Error('should not ask when cwd is home'); };
    const out = await resolveInstallMode(opts, ask);
    assert.strictEqual(out.global, true, 'should stay global when cwd is home');
  });

  // 4) cwd !== home and user says yes -> project-level install into cwd.
  await withHomeAndCwd('/home/u', async () => {
    const opts = { global: true, target: null, targetExplicit: false, globalExplicit: false };
    const out = await resolveInstallMode(opts, async () => true);
    assert.strictEqual(out.global, false, 'should switch to project mode');
    assert.strictEqual(out.target, process.cwd(), 'target should be cwd');
  });

  // 5) cwd !== home and user says no -> stays global.
  await withHomeAndCwd('/home/u', async () => {
    const opts = { global: true, target: null, targetExplicit: false, globalExplicit: false };
    const out = await resolveInstallMode(opts, async () => false);
    assert.strictEqual(out.global, true, 'should stay global when user declines');
    assert.strictEqual(out.target, null, 'target should stay null');
  });

  console.log('mode.test.js: all resolveInstallMode tests passed');

  // parseChecksums: must strip the GNU tar binary-mode marker ('*') so both
  // "HASH  name" and "HASH *name" formats resolve, matching the Python side.
  const plain = parseChecksums(`${H}  iterate-skill.tar.gz\n`);
  assert.strictEqual(plain.get('iterate-skill.tar.gz'), H, 'plain format should parse');

  const starred = parseChecksums(`${I} *iterate-skill.tar.gz\n`);
  assert.strictEqual(starred.get('iterate-skill.tar.gz'), I, 'starred format should strip the * marker');

  const crlf = parseChecksums(`${J}  iterate-skill.tar.gz\r\n`);
  assert.strictEqual(crlf.get('iterate-skill.tar.gz'), J, 'CRLF line endings should parse');

  const multi = parseChecksums(`${H}  a.txt\n${I}  b.txt\n`);
  assert.strictEqual(multi.get('a.txt'), H);
  assert.strictEqual(multi.get('b.txt'), I);

  // './' prefix and subpath/basename matching must resolve like the Python
  // side (scripts/install.py _parse_checksum), which matches on basename.
  const dotSlash = parseChecksums(`${H}  ./iterate-skill.tar.gz\n`);
  assert.strictEqual(dotSlash.get('iterate-skill.tar.gz'), H, './ prefix should parse');

  const subpath = parseChecksums(`${H}  dist/iterate-skill.tar.gz\n`);
  assert.strictEqual(subpath.get('iterate-skill.tar.gz'), H, 'subpath entries should match by basename');

  const starredSubpath = parseChecksums(`${H}  *./release/iterate-skill-1.2.3.tar.gz\n`);
  assert.strictEqual(starredSubpath.get('iterate-skill-1.2.3.tar.gz'), H, '*./ and versioned subpath should match by basename');

  // Multiple leading '*' markers must be stripped like Python's lstrip("*")
  // (a malformed entry must never leave a leading '*' in the basename).
  const multiStar = parseChecksums(`${H}  **iterate-skill.tar.gz\n`);
  assert.strictEqual(multiStar.get('iterate-skill.tar.gz'), H, 'all leading * markers should strip (lstrip matching)');

  // Comment lines ('#') must be ignored like the Python side.
  const withComment = parseChecksums(`# generated by CI\n${H}  iterate-skill.tar.gz\n`);
  assert.strictEqual(withComment.get('iterate-skill.tar.gz'), H, 'comment lines should be ignored');
  assert.strictEqual(withComment.size, 1, 'comment lines must not create entries');

  // A non-hex digest in any line must be skipped (fail-closed: the missing
  // asset aborts install later) instead of being parsed as an expected hash.
  const garbage = parseChecksums(`${H}  iterate-skill.tar.gz\nnot-a-hash  other.bin\n`);
  assert.strictEqual(garbage.get('iterate-skill.tar.gz'), H, 'valid line still parses');
  assert.strictEqual(garbage.has('other.bin'), false, 'non-hex digest must be dropped');
  assert.strictEqual(garbage.size, 1, 'garbage lines must not create entries');

  // A duplicate basename with a *different* digest must refuse the whole file
  // (tampered or hand-corrupted checksum) rather than silently pick a winner.
  assert.throws(
    () => parseChecksums(`${H}  x.tar.gz\n${I}  x.tar.gz\n`),
    InstallerError,
    'conflicting duplicate must throw',
  );

  // The same digest repeated is harmless (idempotent/regenerated file).
  const dedup = parseChecksums(`${H}  x.tar.gz\n${H}  x.tar.gz\n`);
  assert.strictEqual(dedup.size, 1, 'identical duplicate should dedupe');
  assert.strictEqual(dedup.get('x.tar.gz'), H);

  // A duplicate whose digest differs only in HEX CASE is the same digest, not
  // a conflict (constantTimeHashEqual compares case-insensitively).
  const caseVariant = `${H.toLowerCase()}  x.tar.gz\n${H}  x.tar.gz\n`;
  const dedupCase = parseChecksums(caseVariant);
  assert.strictEqual(dedupCase.size, 1, 'case-variant duplicate should dedupe');
  assert.strictEqual(dedupCase.get('x.tar.gz'), H, 'first digest retained');

  console.log('mode.test.js: all parseChecksums tests passed');

  // parseArgs: --no-cli must toggle skill-only mode, and default to off.
  assert.strictEqual(parseArgs([]).noCli, false, 'noCli should default to false');
  assert.strictEqual(parseArgs(['--no-cli']).noCli, true, '--no-cli should set noCli');
  assert.strictEqual(parseArgs(['--no-cli', '--force', '--global']).noCli, true, 'noCli persists with other flags');
  assert.strictEqual(parseArgs(['--global']).noCli, false, 'unrelated flags do not set noCli');

  // parseArgs: unrelated flag surface is preserved (target/global/ai/force).
  const combo = parseArgs(['--ai', 'trae', '--target', '/proj', '--force']);
  assert.strictEqual(combo.ai, 'trae', 'ai should parse');
  assert.strictEqual(combo.target, '/proj', 'target should parse');
  assert.strictEqual(combo.force, true, 'force should parse');
  assert.strictEqual(combo.global, false, 'target forces project mode');

  // parseArgs: --version/-v/--help/-h must set the corresponding mode instead
  // of falling through to the unknown-option error.
  assert.strictEqual(parseArgs([]).mode, null, 'mode should default to null');
  assert.strictEqual(parseArgs(['--version']).mode, 'version', '--version should set version mode');
  assert.strictEqual(parseArgs(['-v']).mode, 'version', '-v should set version mode');
  assert.strictEqual(parseArgs(['--help']).mode, 'help', '--help should set help mode');
  assert.strictEqual(parseArgs(['-h']).mode, 'help', '-h should set help mode');

  // parseArgs: default token comes from $GITHUB_TOKEN through normalizeToken
  // (trimmed), and an absent/unset variable resolves to null — the object may
  // only ever carry the normalized value.
  const savedToken = process.env.GITHUB_TOKEN;
  try {
    delete process.env.GITHUB_TOKEN;
    assert.strictEqual(parseArgs([]).token, null, 'no env token should default to null');
    process.env.GITHUB_TOKEN = '  gh_default_token_1  ';
    assert.strictEqual(parseArgs([]).token, 'gh_default_token_1', 'env token should be normalized into the default');
    assert.strictEqual(parseArgs(['--token', 'gh_explicit_2']).token, 'gh_explicit_2', '--token should override the env default');
  } finally {
    if (savedToken === undefined) delete process.env.GITHUB_TOKEN;
    else process.env.GITHUB_TOKEN = savedToken;
  }

  // parseArgs: -h/--help and -v/--version must short-circuit parsing — later
  // malformed flags (unknown options or value-consuming flags missing values
  // or swallowing the next flag) must NOT turn help/version into an error.
  const shortCircuit = [
    ['--help', '--bogus'],
    ['--help', '--ai'],
    ['-h', '--target'],
    ['--version', '--bogus'],
    ['--version', '--token'],
    ['-v', '--ai', '--force'],
  ];
  for (const argv of shortCircuit) {
    const opts = parseArgs(argv);
    assert.ok(
      opts.mode === 'help' || opts.mode === 'version',
      `${argv.join(' ')} should short-circuit to mode, got ${opts.mode}`,
    );
  }
  assert.strictEqual(parseArgs(['--help', '--ai', 'trae']).mode, 'help', 'help wins over a valid later flag');
  assert.strictEqual(parseArgs(['--force', '--help']).mode, 'help', 'help after a normal flag still sets mode');
  assert.strictEqual(parseArgs(['--ai', 'trae', '--version']).mode, 'version', 'version after a normal flag still sets mode');

  // parseArgs: value-consuming flags must reject a following flag as their
  // value instead of silently swallowing it (regression: `--ai --force`
  // previously set ai='--force' and misled the Python side with an invalid
  // choice). Hard argument errors are now THROWN as InstallerError rather than
  // calling process.exit: library code must not kill the host process, so the
  // exit code is set once, at the bin/cli.js boundary.
  assert.throws(() => parseArgs(['--ai', '--force']), InstallerError, '--ai must reject a flag as its value');
  assert.throws(() => parseArgs(['--target', '--global']), InstallerError, '--target must reject a flag as its value');
  assert.throws(() => parseArgs(['--token', '--yes']), InstallerError, '--token must reject a flag as its value');
  assert.throws(() => parseArgs(['--ai']), InstallerError, '--ai without a value must error');
  assert.throws(() => parseArgs(['--token']), InstallerError, '--token without a value must error');

  // The errors must be actionable, not a bare "requires a value".
  assert.throws(() => parseArgs(['--ai', '--force']), /--ai requires a value/);
  assert.throws(() => parseArgs(['--ai']), /--ai requires a value/);
  // parseArgs must never reach the process exit API (a library function that
  // called process.exit would have terminated the test runner above).
  const origExit = process.exit;
  let exitCalled = false;
  process.exit = () => { exitCalled = true; };
  try {
    for (const bad of [['--ai', '--force'], ['--target', '--global'], ['--token', '--yes'], ['--ai'], ['--token']]) {
      try {
        parseArgs(bad);
        assert.fail(`parseArgs(${JSON.stringify(bad)}) should have thrown`);
      } catch (err) {
        assert.ok(err instanceof InstallerError, `parseArgs(${JSON.stringify(bad)}) should throw InstallerError, got ${err}`);
      }
    }
  } finally {
    process.exit = origExit;
  }
  assert.strictEqual(exitCalled, false, 'parseArgs must throw instead of calling process.exit');

  // parseArgs: a bare positional argument must produce a warning instead of
  // being silently ignored (fix: typos like "npx iterate-skill-installer trae").
  const origLog = console.log;
  const warnings = [];
  console.log = (msg) => { warnings.push(msg); };
  try {
    const opts = parseArgs(['trae', '--force']);
    assert.strictEqual(opts.force, true, 'known flags still parse alongside positionals');
    assert.ok(
      warnings.some((w) => w.includes('Ignoring unexpected positional argument: trae')),
      `positional arg should warn, got: ${JSON.stringify(warnings)}`,
    );
  } finally {
    console.log = origLog;
  }

  // parseArgs: --global + --target together must warn that the later flag wins.
  const conflictLogs = [];
  console.log = (msg) => { conflictLogs.push(msg); };
  try {
    const targetThenGlobal = parseArgs(['--target', '/proj', '--global']);
    assert.strictEqual(targetThenGlobal.global, true, 'later --global wins');
    assert.strictEqual(targetThenGlobal.target, null, 'later --global clears the target');
    assert.ok(
      conflictLogs.some((w) => w.includes('--global overrides --target')),
      `conflict should warn, got: ${JSON.stringify(conflictLogs)}`,
    );
    const globalThenTarget = parseArgs(['--global', '--target', '/proj']);
    assert.strictEqual(globalThenTarget.global, false, 'later --target wins');
    assert.strictEqual(globalThenTarget.target, '/proj', 'later --target is kept');
    assert.ok(
      conflictLogs.some((w) => w.includes('--target overrides --global')),
      `conflict should warn, got: ${JSON.stringify(conflictLogs)}`,
    );
  } finally {
    console.log = origLog;
  }

  console.log('mode.test.js: all parseArgs tests passed');

  // buildPythonInstallArgs: a relative --target must be resolved against the
  // current working directory (the Python installer runs with a different
  // cwd, so the raw relative path would point at the wrong place).
  const resolved = buildPythonInstallArgs({ ai: 'trae', target: 'rel/sub', force: true, globalInstall: false });
  assert.deepStrictEqual(
    resolved,
    ['--ai', 'trae', '--target', path.resolve('rel/sub'), '--force'],
    'relative --target should be resolved against cwd',
  );
  const globalArgs = buildPythonInstallArgs({ ai: null, target: null, force: false, globalInstall: true });
  assert.deepStrictEqual(globalArgs, ['--global'], 'global flag should be forwarded');
  assert.deepStrictEqual(
    buildPythonInstallArgs({ ai: null, target: '/abs/target', force: false, globalInstall: false }),
    ['--target', '/abs/target'],
    'absolute --target is passed through unchanged',
  );
  assert.deepStrictEqual(buildPythonInstallArgs({ ai: null, target: null, force: false, globalInstall: false }), [], 'no flags -> empty argv');

  console.log('mode.test.js: all buildPythonInstallArgs tests passed');

  // isGithubApiUrl: the caller's PAT must only ever be attached to the
  // api.github.com host — never to public release-asset / other URLs
  // (credential surface minimalism, mirroring scripts/install.py).
  assert.strictEqual(isGithubApiUrl('https://api.github.com/repos/jingzhao-l/iterate-skill/releases/latest'), true, 'api host should match');
  assert.strictEqual(isGithubApiUrl('https://api.github.com.evil.com/x'), false, 'lookalike host must not match');
  assert.strictEqual(isGithubApiUrl('https://release-assets.githubusercontent.com/foo.tar.gz'), false, 'asset host must not receive the token');
  assert.strictEqual(isGithubApiUrl('https://github.com/x'), false, 'github.com is not the API host');
  assert.strictEqual(isGithubApiUrl('not a url'), false, 'malformed url must not match');

  console.log('mode.test.js: all isGithubApiUrl tests passed');

  // normalizeToken: a token smuggled in with whitespace (e.g. a trailing
  // newline from `$(cat secret)`) must be trimmed; an all-whitespace or empty
  // value is treated as "no token" instead of a 401-baiting credential.
  assert.strictEqual(normalizeToken('  gh_abc  '), 'gh_abc', 'token should be trimmed');
  assert.strictEqual(normalizeToken('gh_abc\n'), 'gh_abc', 'trailing newline should be trimmed');
  assert.strictEqual(normalizeToken('   '), null, 'blank token should become null');
  assert.strictEqual(normalizeToken(''), null, 'empty token should become null');
  assert.strictEqual(normalizeToken(null), null, 'null token should stay null');
  assert.strictEqual(normalizeToken(undefined), null, 'undefined token should become null');
  assert.strictEqual(parseArgs(['--token', '  gh_xyz ']).token, 'gh_xyz', '--token value should be trimmed');

  console.log('mode.test.js: all normalizeToken tests passed');

  // validateTokenShape: parity with install.py's _validate_github_token — a
  // typo'd PAT must fail fast (clear message) instead of a later 401/403.
  // Accepts blank (no token) and the documented prefixes; rejects bad shapes.
  assert.strictEqual(validateTokenShape(null), null, 'no token is valid (auth simply omitted)');
  assert.strictEqual(validateTokenShape(''), null, 'blank token is treated as absent');
  assert.strictEqual(
    validateTokenShape(`ghp_${'a'.repeat(36)}`),
    null,
    'a well-formed legacy PAT is accepted',
  );
  assert.strictEqual(
    validateTokenShape(`github_pat_${'A'.repeat(30)}`),
    null,
    'a fine-grained PAT is accepted',
  );
  assert.ok(validateTokenShape('short') !== null, 'a too-short token is rejected');
  assert.ok(
    validateTokenShape(`abcdefghijklmnopqrstuvwxyz0123456789`) !== null,
    'a correctly sized token without a known prefix is rejected',
  );
  assert.ok(
    validateTokenShape(`ghp_${'a'.repeat(300)}`) !== null,
    'an over-long token is rejected',
  );
  console.log('mode.test.js: all validateTokenShape tests passed');

  // buildAuthFlags: the PAT must only ride on api.github.com requests, and
  // even there redirects must be forbidden so the raw -H Authorization header
  // cannot be echoed onto a foreign host in a -L redirect chain.
  const api = 'https://api.github.com/repos/jingzhao-l/iterate-skill/releases/latest';
  assert.deepStrictEqual(
    buildAuthFlags(api, 'tok'),
    ['-H', 'Authorization: Bearer tok', '--max-redirs', '0'],
    'api request with a token must attach auth and forbid redirects',
  );
  assert.deepStrictEqual(buildAuthFlags('https://release-assets.githubusercontent.com/x', 'tok'), [], 'asset URL must never carry the token');
  assert.deepStrictEqual(buildAuthFlags(api, null), [], 'no token means no auth flags');
  assert.deepStrictEqual(buildAuthFlags(api, ''), [], 'blank token means no auth flags');

  console.log('mode.test.js: all buildAuthFlags tests passed');

  // runCommand: a wedged child must be SIGKILLed after the timeout instead of
  // hanging the installer forever, and the rejection must make the failure
  // classable (InstallerError).
  const timedOut = await runCommand('sleep', ['30'], { timeout: 300 }).then(
    () => ({ timedOut: false }),
    (err) => ({ timedOut: err instanceof InstallerError && /timed out after 300 ms/.test(err.message) }),
  );
  assert.ok(timedOut.timedOut, 'runCommand must reject with a "timed out" InstallerError on timeout');

  // runCommand: the timeout must kill the WHOLE process group, not just the
  // direct child. A `pip`/`curl` that had already spawned a helper outlived a
  // bare child.kill() and kept running (and holding our stdio pipe) after the
  // installer reported a timeout. The grandchild writes a marker file on
  // completion; a group kill prevents it from ever being written.
  if (process.platform !== 'win32') {
    const marker = path.join(os.tmpdir(), `iterate-grandchild-${process.pid}-${Date.now()}`);
    const wrapper = path.join(os.tmpdir(), `iterate-group-${process.pid}.js`);
    // The wrapper (leader) spawns a detached-ish long-lived grandchild that
    // would write `marker` ~2s later, then itself wedges on an endless sleep.
    fs.writeFileSync(
      wrapper,
      `const { spawn } = require('node:child_process');\n` +
        `spawn(process.execPath, ['-e', 'setTimeout(() => require("fs").writeFileSync(${JSON.stringify(marker)}, "x"), 2000)'], { stdio: 'ignore' });\n` +
        `setInterval(() => {}, 1000);\n`,
    );
    try {
      const groupTimedOut = await runCommand(process.execPath, [wrapper], { timeout: 400 }).then(
        () => false,
        (err) => err instanceof InstallerError && /timed out/.test(err.message),
      );
      assert.ok(groupTimedOut, 'group kill path must still report the timeout');
      // Give any surviving grandchild time to fire, then assert it never did.
      await new Promise((r) => setTimeout(r, 2600));
      assert.ok(!fs.existsSync(marker), 'grandchild survived the timeout — process group was not killed');
    } finally {
      fs.rmSync(wrapper, { force: true });
      fs.rmSync(marker, { force: true });
    }
  }

  // runCommand: a grandchild that inherits our stdio pipe keeps 'close' from
  // firing even after the leader is dead. The promise must still settle (via
  // the post-kill fallback) rather than hang the installer forever. The
  // grandchild ignores SIGTERM and outlives the leader deliberately.
  if (process.platform !== 'win32') {
    const holdPipe = path.join(os.tmpdir(), `iterate-holdpipe-${process.pid}.js`);
    fs.writeFileSync(
      holdPipe,
      `const { spawn } = require('node:child_process');\n` +
        `const c = spawn(process.execPath, ['-e', 'process.on("SIGTERM", () => {}); setInterval(() => {}, 1000);'], { stdio: ['ignore', "inherit", "inherit"] });\n` +
        `setInterval(() => {}, 1000);\n`,
    );
    try {
      const raced = await Promise.race([
        runCommand(process.execPath, [holdPipe], { timeout: 300 }).then(
          () => 'settled-ok',
          () => 'settled-reject',
        ),
        new Promise((r) => setTimeout(() => r('never-settled'), 12000)),
      ]);
      assert.strictEqual(raced, 'settled-reject', 'promise must settle even when a grandchild holds the stdio pipe');
    } finally {
      fs.rmSync(holdPipe, { force: true });
    }
  }

  // runCommand: stdout retention must be bounded (no unbounded memory growth
  // for a chatty producer) while still returning the tail of the output.
  const script = "for (let i = 0; i < 200000; i++) console.log('line-' + i);";
  const tail = await runCommand(process.execPath, ['-e', script]);
  assert.ok(tail.includes('line-199999'), 'chatty output must keep its tail');
  assert.ok(tail.length <= 1024 * 1024, 'retained output must be bounded (1 MiB cap)');

  // runPythonInstall: a signal-killed child reports a null exit code which
  // Node surfaces as closer code null; the shell would read that as success,
  // so the promise must normalize it to a non-zero failure. Using a tiny
  // SIGKILL-itself script stands in for a wedged python subprocess.
  const killSelf = path.join(os.tmpdir(), `iterate-kill-self-${process.pid}.js`);
  fs.writeFileSync(killSelf, 'process.kill(process.pid, "SIGKILL");\n');
  try {
    const code = await runPythonInstall(process.execPath, killSelf, []);
    assert.strictEqual(code, 1, 'null (signal-killed) close code must normalize to exit 1');
  } finally {
    fs.rmSync(killSelf, { force: true });
  }

  testEnforceDownloadedSize();
  testSignaturePolicy();
  testSelectSkillRelease();
  testConstantTimeHashEqual();
  testCliBoundary();

  console.log('mode.test.js: all runCommand/runPythonInstall hardening tests passed');
}

// ---------------------------------------------------------------------------
// Constant-time, case-insensitive digest comparison
// ---------------------------------------------------------------------------

function testConstantTimeHashEqual() {
  assert.strictEqual(constantTimeHashEqual(H, H), true, 'identical digests match');
  assert.strictEqual(constantTimeHashEqual(H.toUpperCase(), H), true, 'casing must never decide');
  assert.strictEqual(constantTimeHashEqual(H, I), false, 'different digests do not match');
  assert.strictEqual(constantTimeHashEqual('  ' + H + '  ', H), true, 'surrounding whitespace is trimmed');
  // The length guard exists because timingSafeEqual THROWS on unequal lengths;
  // an empty/short value must refuse cleanly instead.
  assert.strictEqual(constantTimeHashEqual('', ''), false, 'empty digests are refused');
  assert.strictEqual(constantTimeHashEqual('abc', 'abcdef'), false, 'length mismatch is refused without throwing');
  assert.strictEqual(constantTimeHashEqual('a', 'zz'), false, 'single-char mismatch is refused without throwing');
  assert.strictEqual(constantTimeHashEqual('abc', 'abc'), true, 'equal short strings still compare honestly');
  assert.strictEqual(constantTimeHashEqual(H, null), false, 'non-string input is refused');
  assert.strictEqual(constantTimeHashEqual(H, undefined), false, 'undefined input is refused');
  assert.strictEqual(constantTimeHashEqual(H, 123), false, 'numeric input is refused');
}

// ---------------------------------------------------------------------------
// CLI boundary (bin/cli.js): exit codes, not process.exit()
// ---------------------------------------------------------------------------

function testCliBoundary() {
  const cliPath = path.join(__dirname, '..', 'bin', 'cli.js');
  const runCli = (args) => spawnSync(process.execPath, [cliPath, ...args], {
    encoding: 'utf8',
    cwd: originalCwd,
  });

  // `--help` and `--version` must exit 0 (no install attempted).
  const help = runCli(['--help']);
  assert.strictEqual(help.status, 0, `--help must exit 0, got ${help.status}`);

  const version = runCli(['--version']);
  assert.strictEqual(version.status, 0, `--version must exit 0, got ${version.status}`);
  assert.ok(version.stdout.includes('iterate-skill-installer'), 'version prints the package name');

  // A hard argument error must exit non-zero with a clean message and no
  // unhandled-rejection stack trace.
  for (const bad of [['--ai', '--force'], ['--ai'], ['--target', '--global']]) {
    const result = runCli(bad);
    assert.notStrictEqual(result.status, 0, `parseArgs ${JSON.stringify(bad)} must exit non-zero`);
    assert.ok(
      !String(result.stderr).includes('UnhandledPromiseRejection') &&
        !String(result.stderr).includes('ERR_UNHANDLED_REJECTION'),
      `a parse error must not surface as an unhandled rejection: ${JSON.stringify(result.stderr)}`,
    );
    assert.ok(
      /requires a value/.test(String(result.stderr)),
      `the failure message must say which flag needs a value: ${JSON.stringify(result.stderr)}`,
    );
  }
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});

// ---------------------------------------------------------------------------
// Mandatory release-signature policy (mirrors iterate_cli/signing.py)
// ---------------------------------------------------------------------------

function testSignaturePolicy() {
  // Verified → proceed.
  assert.strictEqual(
    signaturePolicyError({ hasSignatureAsset: true, status: 'verified', detail: 'ok' }),
    null,
    'a verified signature must allow the install',
  );

  // Missing .asc → refuse by default...
  const unsigned = signaturePolicyError({ hasSignatureAsset: false });
  assert.ok(/UNSIGNED/.test(unsigned), 'a missing signature must be refused');
  assert.ok(unsigned.includes(ALLOW_UNSIGNED_ENV), 'the refusal must name the escape hatch');
  // ...but the documented override (hosts without gpg) allows it.
  assert.strictEqual(
    signaturePolicyError({ hasSignatureAsset: false, allowUnsigned: true }),
    null,
    'the explicit override must permit an unsigned release',
  );

  // BAD signature → never allowed, override or not.
  for (const allowUnsigned of [false, true]) {
    const bad = signaturePolicyError({
      hasSignatureAsset: true,
      status: 'invalid',
      detail: 'BAD signature',
      allowUnsigned,
    });
    assert.ok(/FAILED/.test(bad), 'a bad signature must always be refused');
    assert.ok(bad.includes(ALLOW_UNSIGNED_ENV), 'and must say the override will not help');
  }

  // No gpg binary → refuse unless overridden.
  const noGpg = signaturePolicyError({
    hasSignatureAsset: true,
    status: 'unavailable',
    detail: 'gpg binary not found on PATH',
  });
  assert.ok(/Cannot verify/.test(noGpg), 'missing gpg must refuse by default');
  assert.strictEqual(
    signaturePolicyError({
      hasSignatureAsset: true,
      status: 'unavailable',
      detail: 'nope',
      allowUnsigned: true,
    }),
    null,
    'missing gpg may be overridden (that is what the override exists for)',
  );

  // Signature exists but could not be fetched → a transport problem, refuse.
  const fetchFailed = signaturePolicyError({
    hasSignatureAsset: true,
    downloadError: 'HTTP 500',
  });
  assert.ok(/Could not download/.test(fetchFailed), 'an unfetchable signature must refuse');

  // allowUnsigned() reads the environment variable.
  //
  // REGRESSION: a bare "any non-empty string" check meant
  // ITERATE_ALLOW_UNSIGNED=0 (or "false", or a stray "no") ENABLED unsigned
  // installs — the exact opposite of the operator's intent, and a silent
  // downgrade of the authenticity gate. Only explicit truthy values count.
  const previous = process.env[ALLOW_UNSIGNED_ENV];
  try {
    for (const on of ['1', 'true', 'TRUE', 'yes', ' Yes ', 'True']) {
      process.env[ALLOW_UNSIGNED_ENV] = on;
      assert.strictEqual(allowUnsigned(), true, `value ${JSON.stringify(on)} must enable the override`);
    }
    for (const off of ['', '   ', '0', 'false', 'FALSE', 'no', 'off', 'maybe', 'yesplease']) {
      process.env[ALLOW_UNSIGNED_ENV] = off;
      assert.strictEqual(
        allowUnsigned(),
        false,
        `value ${JSON.stringify(off)} must NOT enable the override (silent downgrade)`,
      );
    }
    delete process.env[ALLOW_UNSIGNED_ENV];
    assert.strictEqual(allowUnsigned(), false, 'an unset variable must not enable the override');
  } finally {
    if (previous === undefined) delete process.env[ALLOW_UNSIGNED_ENV];
    else process.env[ALLOW_UNSIGNED_ENV] = previous;
  }

  console.log('mode.test.js: all signaturePolicyError tests passed');
}

// ---------------------------------------------------------------------------
// selectSkillRelease — the newest-stable-release filter
// ---------------------------------------------------------------------------

function testSelectSkillRelease() {
  const mk = (tag, assets, extra = {}) => ({
    tag_name: tag,
    draft: false,
    prerelease: false,
    assets: assets.map((name) => ({ name })),
    ...extra,
  });
  const T = 'iterate-skill.tar.gz';
  const C = 'SHA256SUMS.txt';
  const S = 'iterate-skill.tar.gz.asc';

  // A release carrying tarball + checksum is selectable WITHOUT the .asc —
  // the signature is enforced later by signaturePolicyError, so the
  // ITERATE_ALLOW_UNSIGNED override actually works (previously the filter
  // required the signature and made that override unreachable).
  const unsigned = selectSkillRelease([mk('v3.14.0', [T, C])]);
  assert.strictEqual(unsigned && unsigned.tag_name, 'v3.14.0',
    'an unsigned release must still be selectable (policy decides later)');

  // A signed release is selectable too.
  const signed = selectSkillRelease([mk('v3.14.0', [T, C, S])]);
  assert.strictEqual(signed && signed.tag_name, 'v3.14.0', 'a signed release is selectable');

  // Newest-first: the first usable release wins, skipping an incomplete one.
  const newestWins = selectSkillRelease([
    mk('v3.15.0', [T]), // missing checksums → skipped
    mk('v3.14.0', [T, C]),
  ]);
  assert.strictEqual(newestWins && newestWins.tag_name, 'v3.14.0',
    'an incomplete newest release is skipped for the next usable one');

  // Drafts / prereleases / missing-tarball / missing-checksum are skipped.
  assert.strictEqual(
    selectSkillRelease([mk('v9.9.9', [T, C], { draft: true })]), null,
    'a draft is never selected',
  );
  assert.strictEqual(
    selectSkillRelease([mk('v9.9.9', [T, C], { prerelease: true })]), null,
    'a prerelease is never selected',
  );
  assert.strictEqual(
    selectSkillRelease([mk('v9.9.9', [C])]), null,
    'a release without the tarball is not usable',
  );
  assert.strictEqual(
    selectSkillRelease([mk('v9.9.9', [T])]), null,
    'a release without the checksum is not usable',
  );
  assert.strictEqual(
    selectSkillRelease([mk('v9.9.9', [])]), null,
    'a release without assets is not usable',
  );
  assert.strictEqual(selectSkillRelease('not-an-array'), null,
    'a non-array payload selects nothing');

  console.log('mode.test.js: all selectSkillRelease tests passed');
}
