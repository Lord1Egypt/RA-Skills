/**
 * Security-boundary tests for the npx installer.
 *
 * Covers:
 *   - token normalization rejecting interior whitespace/control characters
 *     (header injection) while still trimming the ends;
 *   - `--flag=value` parsing for value-taking flags, with boolean and unknown
 *     flags still failing loudly;
 *   - the GPG authenticity check: bounded runtime, honest classification of an
 *     import failure (unavailable, not "invalid"), and bad signatures still
 *     reported as invalid;
 *   - the fail-closed declared-size guard (a partially parsed listing must not
 *     make the decompression-bomb budget look small).
 *
 * The GPG cases drive a fake `gpg` on PATH; no system gpg is required.
 */

const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {
  assertDeclaredSizesKnown,
  buildAuthFlags,
  findReleaseAsset,
  GPG_TIMEOUT_MS,
  InstallerError,
  normalizeToken,
  parseArgs,
  sumDeclaredSizes,
  verifyGpgDetachedSignature,
} = require('../lib/installer');

const VALID_TOKEN = `ghp_${'a'.repeat(36)}`;

const _FAKE_GPG = `#!/usr/bin/env bash
mode="\${FAKE_GPG_MODE:-ok}"
case " $* " in
  *" --import "*)
    case "$mode" in
      import-fail) printf 'gpg: import failed\\n' >&2; exit 2 ;;
      hang) sleep 10 ;;
    esac
    exit 0
    ;;
  *" --verify "*)
    case "$mode" in
      verify-bad) printf 'gpg: BAD signature\\n' >&2; exit 1 ;;
      # A GOODSIG from a NON-pinned key: exit 0 but VALIDSIG names another key.
      verify-other-key)
        printf '[GNUPG:] GOODSIG DEADBEEF Other <x@example.invalid>\\n'
        printf '[GNUPG:] VALIDSIG DEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEF 2026-01-01 1 0 4 0 1 8 00 DEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEF\\n'
        exit 0 ;;
      verify-no-validsig)
        printf '[GNUPG:] GOODSIG DEADBEEF Other <x@example.invalid>\\n'
        exit 0 ;;
      ok)
        printf '[GNUPG:] GOODSIG DEADBEEF jingzhao-l <ET_lin@outlook.com>\\n'
        printf '[GNUPG:] VALIDSIG 0929EA31DF4F7429F63FC53189D88B1D043A1298 2026-01-01 1 0 4 0 1 8 00 0929EA31DF4F7429F63FC53189D88B1D043A1298\\n'
        exit 0 ;;
    esac
    exit 0
    ;;
esac
exit 0
`;

function tmpDir(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), prefix));
}

function withFakeGpg(mode, fn) {
  const dir = tmpDir('iterate-gpg-');
  const fake = path.join(dir, 'gpg');
  fs.writeFileSync(fake, _FAKE_GPG, 'utf8');
  fs.chmodSync(fake, 0o755);
  const oldPath = process.env.PATH;
  const oldMode = process.env.FAKE_GPG_MODE;
  process.env.PATH = `${dir}${path.delimiter}${oldPath || ''}`;
  process.env.FAKE_GPG_MODE = mode;
  try {
    return fn(dir);
  } finally {
    process.env.PATH = oldPath;
    if (oldMode === undefined) delete process.env.FAKE_GPG_MODE;
    else process.env.FAKE_GPG_MODE = oldMode;
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

function runGpg(options = {}) {
  const dir = tmpDir('iterate-gpg-artifacts-');
  try {
    return verifyGpgDetachedSignature(
      path.join(dir, 'artifact.tar.gz'),
      path.join(dir, 'artifact.tar.gz.asc'),
      '-----BEGIN PGP PUBLIC KEY BLOCK-----\nfake\n-----END PGP PUBLIC KEY BLOCK-----\n',
      dir,
      options,
    );
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

function testTokenNormalization() {
  assert.strictEqual(normalizeToken(null), null);
  assert.strictEqual(normalizeToken(undefined), null);
  assert.strictEqual(normalizeToken(''), null);
  assert.strictEqual(normalizeToken('   \n\t '), null);
  assert.strictEqual(normalizeToken(`  ${VALID_TOKEN}\n`), VALID_TOKEN);

  for (const raw of [
    `ghp_abc\ndef`,
    `ghp_abc def`,
    `ghp_abc\tdef`,
    'ghp_abc\u0000def',
    'ghp_abc\u007fdef',
  ]) {
    assert.throws(
      () => normalizeToken(raw),
      (err) => err instanceof InstallerError && /whitespace or control characters/.test(err.message),
      `expected ${JSON.stringify(raw)} to be rejected`,
    );
  }

  // The same boundary guards the header: an interior newline must never reach
  // buildAuthFlags, even when the caller bypasses parseArgs.
  assert.throws(
    () => buildAuthFlags('https://api.github.com/x', 'ghp_abc\ndef'),
    /whitespace or control characters/,
  );
  console.log('security.test.js: token normalization tests passed');
}

function testEqualsSyntax() {
  delete process.env.GITHUB_TOKEN;

  let opts = parseArgs(['--ai=trae']);
  assert.strictEqual(opts.ai, 'trae');
  assert.strictEqual(opts.mode, null);

  opts = parseArgs(['--ai=trae', '--force']);
  assert.strictEqual(opts.ai, 'trae');
  assert.strictEqual(opts.force, true);

  opts = parseArgs(['--target=/tmp/somewhere']);
  assert.strictEqual(opts.target, '/tmp/somewhere');
  assert.strictEqual(opts.global, false);
  assert.strictEqual(opts.targetExplicit, true);

  opts = parseArgs([`--token=${VALID_TOKEN}`]);
  assert.strictEqual(opts.token, VALID_TOKEN);

  // The spaced form must keep consuming the following argv entry.
  opts = parseArgs(['--ai', 'cursor', '--no-cli']);
  assert.strictEqual(opts.ai, 'cursor');
  assert.strictEqual(opts.noCli, true);

  for (const argv of [['--ai='], ['--target='], ['--token=']]) {
    assert.throws(() => parseArgs(argv), /requires a value/, argv.join(' '));
  }
  for (const argv of [['--force=1'], ['--global=yes'], ['--no-cli=true']]) {
    assert.throws(() => parseArgs(argv), /does not take a value/, argv.join(' '));
  }
  assert.throws(() => parseArgs(['--bogus=x']), /unknown option --bogus/);
  assert.throws(() => parseArgs(['--ai', '--force']), /requires a value/);
  console.log('security.test.js: --flag=value parsing tests passed');
}

function testGpgClassification() {
  assert.strictEqual(GPG_TIMEOUT_MS, 30000);

  withFakeGpg('ok', () => {
    const result = runGpg();
    assert.strictEqual(result.status, 'verified', JSON.stringify(result));
  });

  withFakeGpg('verify-bad', () => {
    const result = runGpg();
    assert.strictEqual(result.status, 'invalid', JSON.stringify(result));
    assert.match(result.detail, /BAD signature/);
  });

  withFakeGpg('verify-other-key', () => {
    // A GOODSIG from a NON-pinned signer must NOT authenticate: exit 0 is not
    // enough, the VALIDSIG fingerprint must belong to the pinned key.
    const result = runGpg();
    assert.strictEqual(result.status, 'invalid', JSON.stringify(result));
  });

  withFakeGpg('verify-no-validsig', () => {
    // A GOODSIG with no VALIDSIG line is likewise not proof of the pinned key.
    const result = runGpg();
    assert.strictEqual(result.status, 'invalid', JSON.stringify(result));
  });

  withFakeGpg('import-fail', () => {
    // An un-importable key is missing evidence, not proof of tampering.
    const result = runGpg();
    assert.strictEqual(result.status, 'unavailable', JSON.stringify(result));
    assert.match(result.detail, /import failed/);
  });

  withFakeGpg('hang', () => {
    const started = Date.now();
    const result = runGpg({ timeoutMs: 100 });
    const elapsed = Date.now() - started;
    // A hung gpg is not missing evidence: classify it 'invalid' so the
    // ITERATE_ALLOW_UNSIGNED override cannot bypass authenticity (fail closed,
    // mirroring iterate_cli/signing.py and scripts/install.py).
    assert.strictEqual(result.status, 'invalid', JSON.stringify(result));
    assert.match(result.detail, /timed out/);
    // The whole point of the bound: return, don't wait for the sleeping gpg.
    assert.ok(elapsed < 5000, `gpg timeout took ${elapsed} ms`);
  });

  // No gpg binary at all: a PATH with no gpg still yields 'unavailable'.
  const empty = tmpDir('iterate-no-gpg-');
  const oldPath = process.env.PATH;
  process.env.PATH = empty;
  try {
    const result = runGpg();
    assert.strictEqual(result.status, 'unavailable', JSON.stringify(result));
    assert.match(result.detail, /not found/);
  } finally {
    process.env.PATH = oldPath;
    fs.rmSync(empty, { recursive: true, force: true });
  }
  console.log('security.test.js: gpg classification/timeout tests passed');
}

function testDeclaredSizesFailClosed() {
  const complete = sumDeclaredSizes(
    [
      '-rw-r--r--  0 user group 12 Oct 20 12:00 a.txt',
      '-rw-r--r--  0 user group 34 2023-01-02 03:04 b.txt',
    ].join('\n'),
  );
  assert.deepStrictEqual(complete, { total: 46, parsed: 2, entries: 2 });
  assert.doesNotThrow(() => assertDeclaredSizesKnown(complete));
  // An empty listing is legitimate (nothing to extract) and must not throw.
  assert.doesNotThrow(() => assertDeclaredSizesKnown(sumDeclaredSizes('')));

  // A localized listing (e.g. French "oct.") is not understood; summing only
  // the understood entries would understate the bomb budget.
  const partial = sumDeclaredSizes(
    [
      '-rw-r--r--  0 user group 10 Oct 20 12:00 a.txt',
      '-rw-r--r--  0 user group 99999999999 oct. 20 12:00 huge.bin',
    ].join('\n'),
  );
  assert.strictEqual(partial.parsed, 1);
  assert.strictEqual(partial.entries, 2);
  assert.throws(
    () => assertDeclaredSizesKnown(partial),
    (err) => err instanceof InstallerError && /could not read the declared size of 1 of 2/.test(err.message),
  );
  console.log('security.test.js: declared-size fail-closed tests passed');
}

function testFindReleaseAssetNullElements() {
  // A malformed GitHub API payload may contain a null / non-object entry
  // before the matching asset; findReleaseAsset must skip it instead of
  // throwing `TypeError: Cannot read properties of null (reading 'name')`.
  const assets = [null, undefined, {name: 'other'}, {name: 'iterate-skill.tar.gz'}];
  const found = findReleaseAsset(assets, 'iterate-skill.tar.gz');
  assert.strictEqual(found.name, 'iterate-skill.tar.gz');
  // No matching asset (and a null element) -> undefined, no throw.
  assert.strictEqual(findReleaseAsset([null, {name: 'x'}], 'SHA256SUMS.txt'), undefined);
  // Not an array -> undefined.
  assert.strictEqual(findReleaseAsset(undefined, 'iterate-skill.tar.gz'), undefined);
  console.log('security.test.js: findReleaseAsset null-element tests passed');
}

function run() {
  testTokenNormalization();
  testEqualsSyntax();
  testGpgClassification();
  testDeclaredSizesFailClosed();
  testFindReleaseAssetNullElements();
  console.log('security.test.js: all security tests passed');
}

run();
