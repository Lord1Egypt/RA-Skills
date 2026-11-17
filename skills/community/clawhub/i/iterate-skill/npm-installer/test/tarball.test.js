/**
 * Tarball safety-hardening tests for the npx installer.
 *
 * Covers the guards in extractTarball()/rejectLinkEntries():
 *   - symbolic / hard link entries are refused outright;
 *   - the single-top-level-directory contract required by --strip-components=1;
 *   - the FAIL-CLOSED listing cap (regression for the TailBuffer bypass, where
 *     a >cap listing silently dropped the OLDEST entries — hiding exactly the
 *     symlink the guard exists to catch — while tar still extracted it);
 *   - the post-extraction decompression-bomb budget.
 *
 * Requires the system `tar` (macOS/Linux); skipped on Windows where the
 * installer falls back to a different extraction path.
 */

const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const {
  extractTarball,
  rejectLinkEntries,
  enforceExtractedSize,
  measureTree,
  FullBuffer,
  MAX_LISTING_CHARS,
  MAX_EXTRACTED_BYTES,
  declaredEntrySize,
  sumDeclaredSizes,
  validateEntryNames,
  InstallerError,
} = require('../lib/installer');

const isWindows = process.platform === 'win32';

function tmpDir(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), prefix));
}

function runTar(args, cwd) {
  const res = spawnSync('tar', args, { cwd, encoding: 'utf8' });
  assert.strictEqual(res.status, 0, `tar ${args.join(' ')} failed: ${res.stderr}`);
}

/**
 * Create a FIFO with the `mkfifo` tool.
 *
 * `fs.mkfifoSync` was removed from Node's fs module (it sat in the
 * "deprecated since v24" bucket), so the only portable way to build one is the
 * shell builtin, which exists on macOS and Linux. Returns false when the tool
 * is absent so the caller can skip the case instead of failing the run.
 *
 * @param {string} fifoPath
 * @returns {boolean} whether the FIFO was created
 */
function makeFifo(fifoPath) {
  const res = spawnSync('mkfifo', [fifoPath], { encoding: 'utf8' });
  return res.status === 0 && fs.existsSync(fifoPath);
}

/**
 * Build a release-shaped tarball (single top-level `iterate/` directory).
 *
 * @param {object} opts
 * @param {'sym'|'hard'|'fifo'|null} opts.link  optional special entry to smuggle in
 * @param {number} opts.filler           number of long-named filler files
 * @param {number} opts.fillerBytes      bytes per filler file
 * @param {boolean} opts.extraTopLevel   add a second top-level directory
 */
function buildTarball({
  link = null,
  filler = 0,
  fillerBytes = 1,
  extraTopLevel = false,
} = {}) {
  const stage = tmpDir('iterate-tar-');
  const root = path.join(stage, 'iterate');
  fs.mkdirSync(root, { recursive: true });
  fs.writeFileSync(path.join(root, 'SKILL.md'), '---\nname: iterate\nversion: 0.0.0\n---\n');
  if (link === 'sym') {
    fs.symlinkSync('/etc', path.join(root, 'sneaky-link'));
  } else if (link === 'hard') {
    fs.linkSync(path.join(root, 'SKILL.md'), path.join(root, 'sneaky-hard'));
  } else if (link === 'fifo') {
    assert.ok(makeFifo(path.join(root, 'sneaky-fifo')), 'mkfifo is unavailable here');
  }
  for (let i = 0; i < filler; i += 1) {
    const name = `filler-${String(i).padStart(6, '0')}-${'x'.repeat(180)}`;
    fs.writeFileSync(path.join(root, name), 'x'.repeat(fillerBytes));
  }
  if (extraTopLevel) {
    const other = path.join(stage, 'z-pwn');
    fs.mkdirSync(other, { recursive: true });
    fs.writeFileSync(path.join(other, 'evil.md'), 'evil');
  }
  const tarball = path.join(stage, 'iterate-skill.tar.gz');
  runTar(['-czf', tarball, ...(extraTopLevel ? ['iterate', 'z-pwn'] : ['iterate'])], stage);
  return { tarball, stage };
}

async function expectInstallerError(promise, needle) {
  try {
    await promise;
  } catch (err) {
    assert.ok(err instanceof InstallerError, `expected InstallerError, got ${err}`);
    assert.ok(
      String(err.message).includes(needle),
      `error message ${JSON.stringify(err.message)} must mention ${JSON.stringify(needle)}`,
    );
    return err;
  }
  throw new Error(`expected a failure mentioning ${JSON.stringify(needle)}, but it succeeded`);
}

async function testFullBuffer() {
  const buf = new FullBuffer(10);
  buf.push('12345');
  assert.strictEqual(buf.toString(), '12345');
  assert.strictEqual(buf.overflowed, false);
  buf.push('67890ABCDEF');
  assert.strictEqual(buf.overflowed, true, 'overflow must be recorded');
  assert.strictEqual(buf.toString(), '1234567890', 'head is retained, not the tail');
  // Once overflowed, further pushes are ignored (bounded memory).
  buf.push('more');
  assert.strictEqual(buf.toString(), '1234567890');
}

async function testListingCapFailClosed() {
  // REGRESSION: a listing that exceeds the cap must ABORT, never be silently
  // truncated. With a 1 MiB tail buffer, the archive below (whose listing
  // exceeds the injected cap) had its OLDEST entries dropped from the scan —
  // including the symlink — and extraction then proceeded.
  const { tarball, stage } = buildTarball({ link: 'sym', filler: 40 });
  try {
    const dest = path.join(stage, 'out');
    await expectInstallerError(
      extractTarball(tarball, dest, { listingCap: 50 }),
      'truncated result',
    );
    // The refused archive must not have produced the symlink on disk.
    assert.ok(
      !fs.existsSync(path.join(dest, 'sneaky-link')),
      'a truncated listing must never reach extraction',
    );
  } finally {
    fs.rmSync(stage, { recursive: true, force: true });
  }
}

async function testLinkRejection() {
  // A FIFO is built through the `mkfifo` tool; when it is absent the case is
  // skipped rather than failing the whole run (see makeFifo).
  const probe = path.join(tmpDir('iterate-fifo-probe-'), 'probe');
  let kinds = [
    ['sym', 'symbolic link'],
    ['hard', 'hard link'],
    // A FIFO/device node is refused for the same reason as a link: the release
    // never ships one, and a special node could wedge or bypass a later read of
    // the extracted tree.
    ['fifo', 'FIFO'],
  ];
  if (!makeFifo(probe)) {
    fs.rmSync(path.dirname(probe), { recursive: true, force: true });
    console.log('tarball.test.js: skipping FIFO case (mkfifo unavailable)');
    kinds = kinds.filter(([kind]) => kind !== 'fifo');
  } else {
    fs.rmSync(path.dirname(probe), { recursive: true, force: true });
  }
  for (const [kind, needle] of kinds) {
    const { tarball, stage } = buildTarball({ link: kind });
    try {
      await expectInstallerError(rejectLinkEntries(tarball), needle);
      const dest = path.join(stage, 'out');
      await expectInstallerError(extractTarball(tarball, dest), needle);
      assert.ok(!fs.existsSync(dest) || !fs.existsSync(path.join(dest, 'sneaky-link')));
    } finally {
      fs.rmSync(stage, { recursive: true, force: true });
    }
  }
}

async function testDeclaredSizeRefusedBeforeExtraction() {
  // PRE-extraction half of the decompression-bomb guard: a tarball whose
  // declared uncompressed total exceeds the budget must be refused BEFORE any
  // byte is written (tar has no size bound and the download cap only bounds the
  // COMPRESSED size).
  const { tarball, stage } = buildTarball({ filler: 4, fillerBytes: 2048 });
  try {
    const dest = path.join(stage, 'out');
    await expectInstallerError(
      extractTarball(tarball, dest, { declaredSizeCap: 1024 }),
      'declared uncompressed size',
    );
    // The guards all run before `mkdirSync`, so a refused archive must not
    // leave a destination directory behind at all.
    assert.ok(!fs.existsSync(dest), 'a refused archive must not create the dest tree');
  } finally {
    fs.rmSync(stage, { recursive: true, force: true });
  }
}

function testEntryNameValidation() {
  const dest = '/tmp/iterate-dest';
  const good = ['iterate/', 'iterate/SKILL.md'];

  assert.strictEqual(validateEntryNames(good, dest), 'iterate', 'a clean archive is accepted');

  assert.throws(() => validateEntryNames(['/etc/passwd'], dest), /absolute path/);
  assert.throws(() => validateEntryNames(['C:\\evil'], dest), /absolute path/);
  assert.throws(() => validateEntryNames(['iterate/../etc/passwd'], dest), /\.\./);
  assert.throws(() => validateEntryNames(['..'], dest), /\.\./);
  assert.throws(
    () => validateEntryNames(['iterate/', 'other/', 'other/evil'], dest),
    /exactly one top-level directory/,
  );
}

function testDeclaredSizeParsing() {
  // GNU tar (ISO date) and bsdtar (macOS, month abbreviation) formats must both
  // yield the entry's declared size — otherwise a platform would silently get
  // total=0 and the pre-extraction budget would never fire.
  assert.strictEqual(declaredEntrySize('drwxr-xr-x  0 0 0        0 2026-01-01 12:00 iterate/'), 0);
  assert.strictEqual(declaredEntrySize('-rw-r--r--  0 0 0      4096 Jan  1 12:00 iterate/SKILL.md'), 4096);
  assert.strictEqual(
    declaredEntrySize('-rw-r--r--  0 0 0      1234 Dec 31 23:59 iterate/a.txt'),
    1234,
  );
  assert.deepStrictEqual(
    sumDeclaredSizes('-rw-r--r--  0 0 0      4096 Jan  1 12:00 iterate/a\n' +
      'drwxr-xr-x  0 0 0         0 Jan  1 12:00 iterate/\n' +
      '-rw-r--r--  0 0 0      1024 Jan  1 12:00 iterate/b\n'),
    { total: 5120, parsed: 3, entries: 3 },
    'declared sizes must sum across entries',
  );
}

async function testCleanArchiveExtracts() {
  const { tarball, stage } = buildTarball({ filler: 3 });
  try {
    // A clean archive must NOT be refused by the complete-listing check...
    await rejectLinkEntries(tarball);
    const dest = path.join(stage, 'out');
    await extractTarball(tarball, dest);
    assert.ok(fs.existsSync(path.join(dest, 'SKILL.md')), 'clean archive extracts');
    assert.strictEqual(measureTree(dest).total > 0, true);
  } finally {
    fs.rmSync(stage, { recursive: true, force: true });
  }
}

async function testMultiTopLevelRejected() {
  const { tarball, stage } = buildTarball({ extraTopLevel: true });
  try {
    await expectInstallerError(
      extractTarball(tarball, path.join(stage, 'out')),
      'exactly one top-level directory',
    );
  } finally {
    fs.rmSync(stage, { recursive: true, force: true });
  }
}

async function testExtractedSizeBudget() {
  const { tarball, stage } = buildTarball({ filler: 5 });
  try {
    const dest = path.join(stage, 'out');
    await extractTarball(tarball, dest);
    const measured = measureTree(dest);
    assert.ok(measured.total > 0 && measured.largest > 0);
    // Simulate a bomb: a budget far below what was extracted must refuse and
    // remove the tree.
    await expectInstallerError(
      Promise.resolve().then(() => enforceExtractedSize(dest, { maxTotal: 10, maxMember: 10 })),
      'exceeds the safety budget',
    );
    assert.ok(!fs.existsSync(dest), 'the over-budget tree is removed');
  } finally {
    fs.rmSync(stage, { recursive: true, force: true });
  }
}

function testListingCapIsGenerous() {
  assert.ok(
    MAX_LISTING_CHARS >= 4 * 1024 * 1024,
    'the complete-listing cap must leave ample headroom over a real release listing',
  );
}

async function run() {
  await testFullBuffer();
  console.log('tarball.test.js: FullBuffer tests passed');
  // Pure parsing/validation tests run on every platform, including Windows
  // where the tar-backed tests below are skipped.
  testDeclaredSizeParsing();
  testEntryNameValidation();
  console.log('tarball.test.js: declared-size + entry-name validation tests passed');
  if (isWindows) {
    console.log('tarball.test.js: skipping tar-backed tests on Windows');
    return;
  }
  await testListingCapFailClosed();
  await testLinkRejection();
  await testDeclaredSizeRefusedBeforeExtraction();
  await testCleanArchiveExtracts();
  await testMultiTopLevelRejected();
  await testExtractedSizeBudget();
  testListingCapIsGenerous();
  console.log('tarball.test.js: all tarball hardening tests passed');
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
