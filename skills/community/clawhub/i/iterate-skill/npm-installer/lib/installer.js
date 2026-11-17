/**
 * iterate-skill-installer — Node.js entry point for npx one-command install.
 *
 * This module orchestrates the cross-assistant installation of iterate-skill:
 *   1. Detect Python / pip availability
 *   2. Download the latest GitHub release tarball + checksum
 *   3. Verify SHA256 checksum
 *   4. Extract to a temporary directory
 *   5. Run scripts/install.py to copy skill files into selected AI assistants
 *
 * The actual copy logic and interactive assistant selection live in the
 * Python install script (scripts/install.py) so that behavior stays in one
 * place and can be tested with the Python test suite.
 *
 * ## Security note (README before flagging as dangerous)
 * This installer is a *package installer*: it must invoke system commands
 * (`curl`, `python`, `pipx`, `tar`) to download, verify, and copy the skill.
 * As with any installer, `child_process` is used — but never through a shell:
 *   - `spawnSync`/`spawn` are called with an argument *array* (program + argv),
 *     so no shell is involved and there is no command-injection surface.
 *   - Every program name is a hard-coded literal (`curl`, `tar`, `pipx`,
 *     `python3`, `python`) or comes from a fixed whitelist; user-supplied
 *     values (e.g. `--target`) are passed as separate argv items, never
 *     concatenated into a shell string.
 *   - `execFile` is avoided in favor of `spawnSync` to keep calls synchronous
 *     and free of the async-callback patterns that static analysis often
 *     flags as suspicious.
 */

const { spawn, spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const readline = require('node:readline');

const GITHUB_OWNER = 'jingzhao-l';
const GITHUB_REPO = 'iterate-skill';
// NOTE: deliberately the *release list*, not `/releases/latest`.
// `/releases/latest` resolves to "newest non-prerelease by published_at" for the
// whole repository, and this repository also publishes releases for the
// harness/plugin sub-projects, which carry no iterate-skill.tar.gz. When such a
// release is the most recently published one, `/releases/latest` returns it and
// every install aborts with "Release is missing the iterate-skill.tar.gz asset."
// Listing releases and picking the newest one that actually carries both assets
// is immune to what any other release in the repo was published last.
const RELEASES_API_URL =
  `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/releases?per_page=100`;

// Release asset filenames — named constants so the magic strings are not
// scattered through the download / verify pipeline.
const TARBALL_ASSET_NAME = 'iterate-skill.tar.gz';
const CHECKSUMS_ASSET_NAME = 'SHA256SUMS.txt';
// Detached ASCII-armored GPG signature over the tarball, published alongside
// it in the release. When a local `gpg` binary is available the installer
// verifies authenticity (not just integrity) against the embedded signing key.
const TARBALL_SIGNATURE_ASSET_NAME = 'iterate-skill.tar.gz.asc';

/**
 * Find a release asset by name, tolerating a malformed payload.
 * Guards each element (a malformed GitHub API response can contain a null /
 * non-object entry before the matching asset; `a.name` on null would throw a
 * TypeError instead of the intended clean "release is missing …" error path).
 */
function findReleaseAsset(assets, name) {
  return Array.isArray(assets) ? assets.find((a) => a && a.name === name) : undefined;
}

// Hard cap on a single curl download: a misbehaving CDN or a corrupt release
// must never hang the installer forever.
const CURL_MAX_TIME_SECONDS = '120';

// Byte caps so a misbehaving upstream can never exhaust disk or memory:
// JSON API responses are tiny, checksums are a few KB, and the release
// tarball is far smaller than the generous ceiling below.
const JSON_MAX_BYTES = 10 * 1024 * 1024; // 10 MiB
const CHECKSUMS_MAX_BYTES = 1 * 1024 * 1024; // 1 MiB
const TARBALL_MAX_BYTES = 100 * 1024 * 1024; // 100 MiB

// Hard cap on tarball LISTING output (``tar -tzf`` / ``tar -tvzf``). The
// listing must be seen IN FULL: the link-rejection, single-top-level-directory
// and path-escape guards in extractTarball are meaningless on a truncated view
// (a 1 MiB TailBuffer used to drop the OLDEST entries, exactly where a tampered
// archive hides its symlink). 16 MiB is far beyond the real release (a few
// hundred names) yet still bounded; exceeding it is fail-closed, never a
// silent truncation.
const MAX_LISTING_CHARS = 16 * 1024 * 1024;

// Post-extraction size budget, mirroring scripts/install.py (which enforces it
// during extraction). JS extraction shells out to ``tar -xzf``, which has no
// such bound, so a highly compressed "decompression bomb" could expand to
// many GiB on disk before anything noticed. The extracted tree is re-measured
// and removed when it exceeds these ceilings.
const MAX_EXTRACTED_BYTES = 500 * 1024 * 1024; // 500 MiB total
const MAX_EXTRACTED_MEMBER_BYTES = 256 * 1024 * 1024; // 256 MiB per file

// A strict upper bound for an interactive yes/no prompt. On EOF (piped stdin
// that ends) or a TTY that stops responding, the prompt must fall back to the
// default rather than hang the installer forever.
const ASK_YES_NO_TIMEOUT_MS = 30_000;

// SHA256 digests are exactly 64 lowercase/uppercase hex characters. Any other
// value in a checksum file is corrupt or tampered and must fail closed rather
// than feed a garbage hash into the integrity comparison.
const SHA256_HEX_RE = /^[0-9a-fA-F]{64}$/;

// Curl added --fail-with-body in 7.76. On older curl the installer must fall
// back to plain --fail so the flag is never rejected by the system curl.
const CURL_FAIL_WITH_BODY_MIN = { major: 7, minor: 76 };
let CURL_SUPPORTS_FAIL_WITH_BODY = null; // lazily probed once

// Package version read from package.json at runtime so the --version/-v flag
// and the published npm version always stay in sync.
const VERSION = require('../package.json').version;

// ASCII-armored GPG public key of the iterate-skill signing identity
// (uid: jingzhao-l (sign-github) <ET_lin@outlook.com>, key
// 0929EA31DF4F7429F63FC53189D88B1D043A1298). The release tarball `.asc`
// signature is verified against THIS key. It must stay in sync with the
// GPG_PRIVATE_KEY repo secret used by `.github/workflows/release.yml` to sign
// the release artifacts — if the release is re-keyed, this constant must be
// updated in the same release.
const ITERATE_SIGNING_PUBLIC_KEY = [
  '-----BEGIN PGP PUBLIC KEY BLOCK-----',
  '',
  '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',
  'YVXa4IEQs7aBxKO+n+T2AvUYiKQ=',
  '=DYXk',
  '-----END PGP PUBLIC KEY BLOCK-----',
].join('\n');

//: SHA-1 fingerprint of the pinned signing key (uid jingzhao-l (sign-github)).
//: Verification is only accepted when the ``VALIDSIG`` fingerprint belongs to
//: this key, not merely on a GOODSIG/exit-0 — a substituted signer whose key
//: gpg auto-retrieved would otherwise pass. Keep in sync with
//: ``iterate_cli/signing.py`` and ``scripts/install.py``.
const ITERATE_SIGNING_KEY_FINGERPRINT = '0929EA31DF4F7429F63FC53189D88B1D043A1298';

//: Extract the fingerprints gpg reported as ``VALIDSIG`` in ``--status-fd``
//: output. A status line is ``[GNUPG:] VALIDSIG <fpr> <date> …``.
function validsigFingerprints(statusOutput) {
  const fprs = [];
  for (const line of String(statusOutput || '').split('\n')) {
    if (!line.startsWith('[GNUPG:] VALIDSIG ')) continue;
    const parts = line.split(/\s+/);
    if (parts.length >= 3 && parts[2]) fprs.push(parts[2].toUpperCase());
  }
  return fprs;
}

const ITERATE_BANNER = [
  '██╗████████╗███████╗██████╗  █████╗ ████████╗███████╗',
  '██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝',
  '██║   ██║   █████╗  ██████╔╝███████║   ██║   █████╗  ',
  '██║   ██║   ██╔══╝  ██╔══██╗██╔══██║   ██║   ██╔══╝  ',
  '██║   ██║   ███████╗██║  ██║██║  ██║   ██║   ███████╗',
  '╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝',
];

class InstallerError extends Error {}

function printBanner() {
  console.log();
  for (const line of ITERATE_BANNER) {
    console.log(`\x1b[36m${line}\x1b[0m`);
  }
  console.log();
}

function info(message) {
  console.log(`\x1b[34mℹ\x1b[0m  ${message}`);
}

function success(message) {
  console.log(`\x1b[32m✓\x1b[0m  ${message}`);
}

function warning(message) {
  console.log(`\x1b[33m⚠\x1b[0m  ${message}`);
}

function error(message) {
  console.error(`\x1b[31m✗\x1b[0m  ${message}`);
}

function hint(message) {
  console.log(`\x1b[2m   ${message}\x1b[0m`);
}

function step(message) {
  console.log(`\x1b[36m◆\x1b[0m  ${message}`);
}

function frameSection(title, lines) {
  const maxLen = Math.max(
    title.length,
    ...lines.map((l) => stripAnsi(l).length),
  );
  const innerWidth = maxLen + 2;
  const top = `┌─ ${title} ${'─'.repeat(Math.max(0, innerWidth - title.length - 2))}┐`;
  const bottom = `└${'─'.repeat(innerWidth + 1)}┘`;
  console.log(top);
  for (const line of lines) {
    const visibleLen = stripAnsi(line).length;
    const padding = ' '.repeat(Math.max(0, innerWidth - visibleLen));
    console.log(`│ ${line}${padding}│`);
  }
  console.log(bottom);
}

function stripAnsi(str) {
  // eslint-disable-next-line no-control-regex
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

async function findPython() {
  for (const bin of ['python3', 'python']) {
    if (commandExists(bin)) return bin;
  }
  return null;
}

function commandExists(bin) {
  // Check whether a command is on PATH by running `bin --version` and
  // inspecting the exit code. `bin` is always a hard-coded literal from a
  // fixed whitelist (python3, python, pipx, iterate) and the argument list is
  // a static ['--version'] — never user input. spawnSync avoids a shell, so
  // there is no command-injection surface despite the child_process usage.
  const result = spawnSync(bin, ['--version'], { stdio: 'ignore' });
  return result.status === 0;
}

async function supportsCurlFailWithBody() {
  // Lazily probe ``curl --version`` once; the result is cached for the rest
  // of the run. Falls back to the plain ``--fail`` flag (no probing) when
  // curl itself cannot be invoked or its output is unexpected.
  if (CURL_SUPPORTS_FAIL_WITH_BODY === null) {
    try {
      const versionOut = await runCommand('curl', ['--version']);
      const match = versionOut.match(/curl (\d+)\.(\d+)\.\d+/);
      if (!match) {
        CURL_SUPPORTS_FAIL_WITH_BODY = false;
      } else {
        const major = Number(match[1]);
        const minor = Number(match[2]);
        CURL_SUPPORTS_FAIL_WITH_BODY =
          major > CURL_FAIL_WITH_BODY_MIN.major ||
          (major === CURL_FAIL_WITH_BODY_MIN.major &&
            minor >= CURL_FAIL_WITH_BODY_MIN.minor);
      }
    } catch {
      CURL_SUPPORTS_FAIL_WITH_BODY = false;
    }
  }
  return CURL_SUPPORTS_FAIL_WITH_BODY;
}

function isGithubApiUrl(url) {
  // True only for the GitHub API host. Release-asset and other URLs are
  // public and must never receive the caller's PAT (credential surface
  // minimalism) — mirrors scripts/install.py::_is_github_api_url.
  let hostname = null;
  try {
    hostname = new URL(url).hostname.toLowerCase();
  } catch {
    return false;
  }
  return hostname === 'api.github.com' || hostname.endsWith('.api.github.com');
}

/**
 * Normalize a caller-supplied GitHub token.
 *
 * Tokens frequently arrive with surrounding whitespace (a trailing newline
 * from `export GITHUB_TOKEN=$(cat secret)` or a shell alias that echoes the
 * value); an untrimmed token makes every authenticated call fail with 401
 * while silently burning the user's GitHub API rate limit. An empty result is
 * treated as "no token".
 */
function normalizeToken(raw) {
  if (raw == null) return null;
  const trimmed = String(raw).trim();
  if (trimmed === '') return null;
  // Trim only removes the ends. A PAT never contains interior whitespace or
  // control characters; one that does (a CR/LF smuggled in from a file, a
  // tab-pasted secret) would either split the Authorization header
  // (CRLF/header injection) or fail as a baffling 401 that looks like an
  // expired token. Reject it here, at the single boundary both the CLI and
  // buildAuthFlags normalize through.
  if (/[\s\x00-\x1f\x7f]/.test(trimmed)) {
    throw new InstallerError(
      'GitHub token contains whitespace or control characters; re-copy it (check GITHUB_TOKEN / --token).',
    );
  }
  return trimmed;
}

// GitHub PAT prefixes accepted by scripts/install.py (kept in sync so the two
// installers agree about what a "malformed token" is). A typo'd token used to
// be sent verbatim and surfaced only as a confusing 401/403 later.
const GITHUB_TOKEN_PREFIXES = ['ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_', 'github_pat_'];

/**
 * Return an error message when ``token`` cannot be a GitHub PAT, else null.
 * Mirrors install.py's ``_validate_github_token`` (length + prefix whitelist).
 */
function validateTokenShape(token) {
  if (!token) return null;
  if (token.length < 20 || token.length > 256) {
    return (
      'GitHub token looks malformed: expected a PAT (starts with ghp_/gho_/github_pat_ etc.) ' +
      'of ~40-256 chars, got a very different length.'
    );
  }
  if (!GITHUB_TOKEN_PREFIXES.some((prefix) => token.startsWith(prefix))) {
    return (
      'GitHub token does not look valid: expected a Personal Access Token starting with ' +
      'one of (ghp_, gho_, ghu_, ghs_, ghr_, github_pat_). Double-check the --token value.'
    );
  }
  return null;
}

/**
 * Compose the curl flags that attach the caller's PAT — and only those. The
 * token is never attached to a non-API host; and marking it up differently
 * from install.py would let the two installers disagree about credentials.
 *
 * Critically, a custom `-H "Authorization: Bearer ..."` header is echoed by
 * curl onto EVERY host in a `-L` redirect chain (unlike `--user`, curl has no
 * notion of stripping auth on a host change for raw headers). When the token
 * is attached we therefore forbid redirects outright: a redirect then fails
 * loudly instead of leaking the PAT to a foreign host.
 */
function buildAuthFlags(url, token) {
  // Re-normalize here as well as at the CLI boundary: this is the exact point
  // the token is interpolated into a header, so a raw CR/LF (e.g. a token read
  // from a Windows-created file) must never reach curl — an embedded newline
  // would split the header (CRLF/header injection) or silently break auth.
  const clean = normalizeToken(token);
  if (!clean) return [];
  if (!isGithubApiUrl(url)) return [];
  return ['-H', `Authorization: Bearer ${clean}`, '--max-redirs', '0'];
}

async function fetchJson(url, token) {
  // Prefer curl over Node.js fetch because curl uses the system CA store
  // and avoids Node-specific certificate issues in some environments.
  const failFlag = (await supportsCurlFailWithBody()) ? '--fail-with-body' : '--fail';
  const args = ['-sSL', failFlag, '--max-time', CURL_MAX_TIME_SECONDS, '--max-filesize', String(JSON_MAX_BYTES), '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', '-H', 'User-Agent: iterate-skill-installer', ...buildAuthFlags(url, token)];
  // `--` ends curl's option parsing so a URL that begins with `-` (e.g. a
  // hostile/odd `browser_download_url` served by the API) is treated as a URL,
  // never smuggled in as a curl flag.
  args.push('--', url);
  // stdoutMustBeComplete with an explicit cap: the default 1 MiB TailBuffer
  // would truncate a large /releases payload and JSON.parse then failed with a
  // baffling "Unexpected end of JSON input". The cap now matches the
  // --max-filesize ceiling and an oversized body reports itself as such.
  const stdout = await runCommand('curl', args, {
    stdoutCap: JSON_MAX_BYTES,
    stdoutMustBeComplete: true,
  });
  try {
    return JSON.parse(stdout);
  } catch (err) {
    throw new InstallerError(`Failed to parse GitHub API response: ${err.message}`);
  }
}

/**
 * Download a file with curl.
 *
 * The caller's PAT is only attached for GitHub API hosts; release assets are
 * public downloads and must not receive it. ``maxBytes`` is enforced with
 * curl's ``--max-filesize`` so a misbehaving upstream is aborted rather than
 * exhausting disk.
 *
 * When ``progress`` is enabled (used for the tarball), curl's ``--progress-bar``
 * writes a live percentage bar straight to the terminal (stderr is inherited so
 * the bar is visible; stdout stays captured for non-progress downloads).
 */
async function downloadFile(url, destPath, token, { progress = false, maxBytes = TARBALL_MAX_BYTES } = {}) {
  const failFlag = (await supportsCurlFailWithBody()) ? '--fail-with-body' : '--fail';
  const args = ['-sSL', failFlag, '--max-time', CURL_MAX_TIME_SECONDS, '--max-filesize', String(maxBytes), '-o', destPath, '-H', 'User-Agent: iterate-skill-installer', ...buildAuthFlags(url, token)];
  if (progress) args.push('--progress-bar');
  // `--` ends curl's option parsing so a `-`-leading URL can never be read as
  // a curl flag (option injection); it is always the final positional URL.
  args.push('--', url);
  if (progress) {
    // Let curl write its progress bar directly to the terminal.
    await runCommand('curl', args, { stdio: ['ignore', 'ignore', 'inherit'] });
  } else {
    await runCommand('curl', args);
  }
  // `--max-filesize` is best-effort by curl's own documentation: it is only
  // enforced when the server advertises a Content-Length, so a response sent
  // with chunked transfer encoding streams to disk unbounded. Re-stat after the
  // fact so the cap holds regardless of how the body was framed, and so a
  // truncated-then-huge body cannot be hashed or extracted.
  enforceDownloadedSize(destPath, maxBytes);
}

/**
 * Fail closed when a completed download exceeds ``maxBytes``.
 *
 * The oversized file is removed so a later retry cannot silently reuse it.
 * @param {string} destPath
 * @param {number} maxBytes
 */
function enforceDownloadedSize(destPath, maxBytes) {
  let size;
  try {
    size = fs.statSync(destPath).size;
  } catch (err) {
    // curl already reported a missing output file as a failure; nothing to
    // check here, and re-reporting would mask the real error.
    return;
  }
  if (size > maxBytes) {
    try {
      fs.unlinkSync(destPath);
    } catch {
      // Best effort: the size violation below is what the user must act on.
    }
    throw new InstallerError(
      `Downloaded file is ${size} bytes, above the ${maxBytes} byte safety cap — refusing to proceed.`,
    );
  }
}

// True when the operator explicitly opted out of signature enforcement. Kept
// as an ENVIRONMENT variable (not a flag) so it cannot be enabled from a
// project config and shows up in the invoking environment for audit.
const ALLOW_UNSIGNED_ENV = 'ITERATE_ALLOW_UNSIGNED';

// Only these (case-insensitive) values enable the override. A bare "any
// non-empty string" check meant `ITERATE_ALLOW_UNSIGNED=0` (or "false", or a
// stray "no") ENABLED unsigned installs — the exact opposite of what the
// operator intended, and a silent downgrade of the authenticity gate.
const ALLOW_UNSIGNED_TRUTHY = new Set(['1', 'true', 'yes']);

function allowUnsigned() {
  const raw = process.env[ALLOW_UNSIGNED_ENV];
  if (raw == null) return false;
  return ALLOW_UNSIGNED_TRUTHY.has(String(raw).trim().toLowerCase());
}

/**
 * Apply the MANDATORY release-signature policy (mirrors
 * ``iterate_cli/signing.py`` and ``scripts/install.py``).
 *
 * Returns an error MESSAGE when the install must abort, or null when it may
 * proceed. The ``ITERATE_ALLOW_UNSIGNED`` override downgrades "cannot check"
 * (no ``.asc`` asset / no ``gpg`` binary) to a warning, but it NEVER bypasses a
 * BAD signature — that is exactly the tampering/key-substitution case.
 *
 * @param {object} state
 * @param {boolean} state.hasSignatureAsset  release published an ``.asc``
 * @param {string}  [state.status]           'verified' | 'invalid' | 'unavailable'
 * @param {string}  [state.detail]           verifier detail for messages
 * @param {string}  [state.downloadError]    failure to FETCH the ``.asc``
 * @param {boolean} [state.allowUnsigned]    override (defaults to the env var)
 */
function signaturePolicyError({
  hasSignatureAsset,
  status = null,
  detail = '',
  downloadError = null,
  allowUnsigned: override = allowUnsigned(),
} = {}) {
  if (downloadError) {
    // The release DID publish a signature but we could not fetch it: a
    // transport problem, not a licence to skip authenticity.
    return (
      `Could not download the release signature (${downloadError}). Refusing to install ` +
      `without authenticity verification; retry once the network recovers. Set ` +
      `${ALLOW_UNSIGNED_ENV}=1 only if you accept an unauthenticated install.`
    );
  }
  if (!hasSignatureAsset) {
    if (override) return null;
    return (
      'Release is UNSIGNED: it publishes no .asc signature, so authenticity cannot be ' +
      `verified (SHA256SUMS travels in the same release and is not an independent ` +
      `anchor). Set ${ALLOW_UNSIGNED_ENV}=1 only if you accept an unauthenticated install.`
    );
  }
  if (status === 'verified') return null;
  if (status === 'invalid') {
    return (
      `GPG signature verification FAILED (${detail}). Refusing to install: the tarball ` +
      `is not signed by the pinned iterate signing key. This is either tampering or a ` +
      `key rotation this installer version does not know about; ${ALLOW_UNSIGNED_ENV} ` +
      'does NOT bypass a bad signature.'
    );
  }
  if (override) return null;
  return (
    `Cannot verify the release signature (${detail || 'gpg unavailable'}). Install GnuPG ` +
    `(gpg) and retry, or set ${ALLOW_UNSIGNED_ENV}=1 to accept an unauthenticated install.`
  );
}

function sha256File(filePath) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath);
    stream.on('error', reject);
    stream.on('end', () => resolve(hash.digest('hex')));
    stream.pipe(hash);
  });
}

/**
 * Constant-time, case-insensitive comparison of two SHA256 hex digests.
 *
 * Casing must never decide the outcome: `sha256sum`/other tools may emit
 * upper-case hex, and a case-sensitive `===` would reject a perfectly good
 * release. Both sides are lower-cased and compared with `timingSafeEqual` —
 * the expected hash travels over the network beside the tarball, so an
 * early-exit string inequality would leak prefix information usable to forge a
 * checksum. The length guard keeps `timingSafeEqual` from throwing on
 * mismatched lengths (an empty/short value is refused outright).
 *
 * Exported so the comparison itself is unit-testable (the inline version it
 * replaces could only be exercised by a full network install).
 */
function constantTimeHashEqual(actualHash, expectedHash) {
  if (typeof actualHash !== 'string' || typeof expectedHash !== 'string') return false;
  const actualBuf = Buffer.from(actualHash.trim().toLowerCase(), 'utf8');
  const expectedBuf = Buffer.from(expectedHash.trim().toLowerCase(), 'utf8');
  return (
    actualBuf.length === expectedBuf.length &&
    actualBuf.length > 0 &&
    crypto.timingSafeEqual(actualBuf, expectedBuf)
  );
}

// Best-effort GPG authenticity verification of a downloaded artifact against
// the embedded signing key. Returns one of:
//   'verified'    — `gpg` present and the detached signature is valid.
//   'invalid'     — `gpg` present, but the signature did not verify (key
//                    mismatch or tampered signature). Reported loudly, never
//                    silently ignored.
//   'unavailable' — no `gpg` binary, or the public key could not be imported.
//                    The caller treats this as non-blocking because SHA256
//                    already guarantees integrity; GPG adds authenticity as a
//                    defense-in-depth layer, not the only gate.
// Runs inside an isolated temporary GNUPGHOME so the end user's own keyring and
// gpg-agent are never touched or modified.
// gpg calls are local and short. Without a timeout a wedged gpg-agent (or a
// pinentry dialog nobody can see) hangs the installer forever; SHA256 already
// gates integrity, so treating a stuck authenticity check as 'unavailable' is
// both honest and non-blocking.
const GPG_TIMEOUT_MS = 30 * 1000;

function verifyGpgDetachedSignature(artifactPath, signaturePath, publicKeyArmor, tmpDir, options = {}) {
  const timeout = options.timeoutMs ?? GPG_TIMEOUT_MS;
  // NOTE: gpg derives its agent socket from the homedir
  // (<homedir>/S.gpg-agent) and unix sockets cap out around 104 characters, so
  // keep this path SHORT — a deep tmpdir made gpg fail with "File name too
  // long: can't connect to the gpg-agent".
  const gpgHome = path.join(tmpDir, 'g');
  fs.mkdirSync(gpgHome, { recursive: true, mode: 0o700 });
  const keyPath = path.join(tmpDir, 'iterate-skill-pubkey.asc');
  fs.writeFileSync(keyPath, publicKeyArmor, 'utf8');

  const importResult = spawnSync(
    'gpg',
    ['--homedir', gpgHome, '--batch', '--yes', '--quiet', '--no-autostart', '--import', keyPath],
    { encoding: 'utf8', timeout, killSignal: 'SIGKILL' }
  );
  if (importResult.error) {
    if (importResult.error.code === 'ENOENT') {
      return { status: 'unavailable', detail: 'gpg binary not found' };
    }
    if (importResult.error.code === 'ETIMEDOUT' || importResult.signal === 'SIGKILL') {
      // A hung gpg is not missing evidence: classify it 'invalid' so the
      // ITERATE_ALLOW_UNSIGNED override cannot bypass authenticity (fail closed,
      // mirroring the verify-timeout branch below and scripts/install.py).
      return {
        status: 'invalid',
        detail: `gpg import timed out after ${timeout} ms (treated as invalid)`,
      };
    }
    return { status: 'unavailable', detail: importResult.error.message };
  }
  if (importResult.status !== 0) {
    // Failure to import the release key means we cannot establish authenticity
    // — not that the artifact is forged. Classifying it 'invalid' claimed
    // evidence of tampering that this run never had, and only 'unavailable'
    // matches the documented non-blocking policy.
    return {
      status: 'unavailable',
      detail: (importResult.stderr || '').trim() || 'failed to import the signing key',
    };
  }

  const verifyResult = spawnSync(
    'gpg',
    ['--homedir', gpgHome, '--batch', '--quiet', '--no-autostart', '--no-auto-key-retrieve', '--status-fd', '1', '--verify', signaturePath, artifactPath],
    { encoding: 'utf8', timeout, killSignal: 'SIGKILL' }
  );
  if (verifyResult.error) {
    if (verifyResult.error.code === 'ETIMEDOUT' || verifyResult.signal === 'SIGKILL') {
      // A hung gpg is not a missing dependency: classify it as 'invalid' so the
      // ITERATE_ALLOW_UNSIGNED override cannot bypass authenticity. Mirrors
      // iterate_cli/signing.py and scripts/install.py (keep in sync).
      return {
        status: 'invalid',
        detail: `gpg verify timed out after ${timeout} ms (treated as invalid)`,
      };
    }
    return { status: 'unavailable', detail: `gpg launch failed: ${verifyResult.error.message}` };
  }
  // A GOODSIG (or exit 0) alone does not prove the signer is the pinned key: a
  // substituted signer whose key gpg auto-retrieved would pass. Require a
  // VALIDSIG fingerprint belonging to the pinned key, mirroring
  // iterate_cli/signing.py and scripts/install.py (keep in sync).
  const signerFingerprints = validsigFingerprints(verifyResult.stdout);
  const matchesPinned = signerFingerprints.some(
    (fpr) => fpr === ITERATE_SIGNING_KEY_FINGERPRINT
  );
  if (verifyResult.status === 0 && matchesPinned) {
    return { status: 'verified', detail: (verifyResult.stderr || '').trim() };
  }
  return { status: 'invalid', detail: (verifyResult.stderr || '').trim() || `gpg exited ${verifyResult.status}` };
}

function parseChecksums(text) {
  const map = new Map();
  for (const line of text.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const parts = trimmed.split(/\s+/);
    if (parts.length < 2) continue;
    // Reject any entry whose digest is not a 64-char hex string so a corrupt
    // or tampered checksum file fails closed: a missing asset ("not found")
    // aborts the install, whereas a garbage digest would masquerade as a
    // valid expected hash.
    if (!SHA256_HEX_RE.test(parts[0])) continue;
    // Normalize the filename the same way scripts/install.py does
    // (_parse_checksum): strip all leading GNU tar binary-mode markers a la
    // Python's name.lstrip("*") (ONE '*', or several in a malformed entry —
    // strip them all so the two parsers can never disagree), then strip the
    // './' prefix, then match on the basename so entries with a subpath or
    // versioned component (e.g. "dist/iterate-skill.tar.gz" or
    // "./iterate-skill.tar.gz") still resolve to the expected asset.
    const normalized = parts[1].replace(/^\*+/, '').replace(/^\.\//, '');
    const basename = normalized.split('/').pop();
    // A duplicate basename carrying a *different* digest is a red flag (the
    // file is hand-corrupted or two sources disagree); refuse the whole file
    // instead of silently letting one value win. Digests are compared
    // case-insensitively (hex), matching constantTimeHashEqual — two entries
    // that differ only in hex case are the SAME digest, not a conflict.
    if (
      map.has(basename) &&
      map.get(basename).toLowerCase() !== parts[0].toLowerCase()
    ) {
      throw new InstallerError(
        `Duplicate checksum entry for ${basename} with a different value — refusing to proceed.`,
      );
    }
    map.set(basename, parts[0]);
  }
  return map;
}

/**
 * Bounded in-memory output buffer: retains only the last ``cap`` characters.
 * Used by ``runCommand`` so a chatty child (a verbose build listing, pip log
 * flood, etc.) can never drive the installer's memory usage unbounded.
 */
class TailBuffer {
  constructor(cap) {
    this.cap = cap;
    this.text = '';
  }
  push(chunk) {
    if (!chunk) return;
    if (this.text.length + chunk.length > this.cap) {
      this.text = (this.text + chunk).slice(-this.cap);
    } else {
      this.text += chunk;
    }
  }
  toString() {
    return this.text;
  }
}

/**
 * Fail-closed output buffer for output that must be observed COMPLETELY
 * (tarball listings, API JSON). Unlike TailBuffer — which keeps the newest
 * text and is right for diagnostics — this one records that the cap was
 * exceeded instead of discarding the oldest content, because a partially seen
 * SECURITY listing is worse than no listing at all.
 */
class FullBuffer {
  constructor(cap) {
    this.cap = cap;
    this.text = '';
    this.overflowed = false;
  }
  push(chunk) {
    if (!chunk || this.overflowed) return;
    if (this.text.length + chunk.length > this.cap) {
      this.overflowed = true;
      this.text = (this.text + chunk).slice(0, this.cap);
      return;
    }
    this.text += chunk;
  }
  toString() {
    return this.text;
  }
}

// Default ceiling for a single child command: 10 minutes then SIGKILL. Long
// operations in this file (pip/pipx installs, venv creation) can legitimately
// take minutes on slow networks, but a wedged child must never hang the
// installer forever.
const DEFAULT_COMMAND_TIMEOUT_MS = 10 * 60 * 1000;
// Grace period between the SIGKILL and giving up on 'close'. A grandchild that
// inherited our stdio pipe keeps that pipe open, so Node withholds 'close'
// even though the leader is already dead — without this the promise would
// never settle and the installer would hang despite the timeout having fired.
const POST_KILL_SETTLE_MS = 5 * 1000;
// Hard cap on retained stdout/stderr per command (memory bound).
const MAX_CAPTURED_OUTPUT_CHARS = 1024 * 1024;

// True only on POSIX: Windows has no process groups keyed by negative pid and
// `detached` there means "new console window", not "new process group".
const IS_POSIX = process.platform !== 'win32';

function killProcessTree(child) {
  // The child was spawned detached (POSIX), so it is its own process-group
  // leader and its negative pid addresses the WHOLE group. A bare
  // `child.kill()` only signals the immediate process, so a `pip` that had
  // already spawned a compiler/download helper outlived the kill and kept
  // running (and holding our stdio pipe) after the installer "timed out".
  if (IS_POSIX && child.pid) {
    try {
      process.kill(-child.pid, 'SIGKILL');
      return;
    } catch (err) {
      // ESRCH: the group is already gone. EPERM: fall through to the leader.
      if (err && err.code === 'ESRCH') return;
    }
  }
  try {
    child.kill('SIGKILL');
  } catch {
    // Already exited — nothing left to signal.
  }
}

function runCommand(bin, args, options = {}) {
  const {
    timeout = DEFAULT_COMMAND_TIMEOUT_MS,
    // Cap on retained stdout. Diagnostics want a TAIL (newest text); security
    // listings / parseable payloads want the WHOLE thing or nothing, which is
    // what ``stdoutMustBeComplete`` switches on.
    stdoutCap = MAX_CAPTURED_OUTPUT_CHARS,
    stdoutMustBeComplete = false,
    ...spawnOptions
  } = options;
  return new Promise((resolve, reject) => {
    // `detached` on POSIX puts the child in its own process group so the
    // timeout can kill the entire tree, not just the leader. It does not
    // change how we await the child (we never unref it).
    const child = spawn(bin, args, { stdio: 'pipe', detached: IS_POSIX, ...spawnOptions });
    const stdoutTail = stdoutMustBeComplete
      ? new FullBuffer(stdoutCap)
      : new TailBuffer(stdoutCap);
    const stderrTail = new TailBuffer(MAX_CAPTURED_OUTPUT_CHARS);
    child.stdout?.on('data', (data) => stdoutTail.push(data.toString()));
    child.stderr?.on('data', (data) => stderrTail.push(data.toString()));
    let killed = false;
    let settled = false;
    let killFallback = null;
    const settle = (fn, value) => {
      if (settled) return;
      settled = true;
      fn(value);
    };
    const timer =
      timeout > 0
        ? setTimeout(() => {
            killed = true;
            killProcessTree(child);
            // The leader may be dead while a grandchild still holds our stdio
            // pipe open, in which case 'close' never arrives. Guarantee the
            // promise settles either way.
            killFallback = setTimeout(() => {
              settle(reject, new InstallerError(`${bin} timed out after ${timeout} ms`));
            }, POST_KILL_SETTLE_MS);
          }, timeout)
        : null;
    const finish = (code) => {
      if (timer) clearTimeout(timer);
      if (killFallback) clearTimeout(killFallback);
      if (killed) {
        settle(reject, new InstallerError(`${bin} timed out after ${timeout} ms`));
        return;
      }
      if (code === 0) {
        if (stdoutMustBeComplete && stdoutTail.overflowed) {
          settle(
            reject,
            new InstallerError(
              `${bin} produced more than ${stdoutCap} characters of output; refusing to act on a truncated result.`,
            ),
          );
          return;
        }
        settle(resolve, stdoutTail.toString());
      } else {
        settle(reject, new InstallerError(`${bin} exited with ${code}: ${stderrTail.toString() || stdoutTail.toString()}`));
      }
    };
    child.on('close', finish);
    child.on('error', (err) => {
      if (timer) clearTimeout(timer);
      if (killFallback) clearTimeout(killFallback);
      settle(reject, err);
    });
  });
}

async function rejectLinkEntries(tarballPath, { listingCap = MAX_LISTING_CHARS } = {}) {
  // Inspect the verbose listing and reject any symbolic ("l") or hard ("h")
  // link entry — and any device ("b" block / "c" character), FIFO ("p") or
  // socket special node. We deliberately reject *all* links rather than
  // validating their targets: the release tarball contains none, so any link is
  // a sign of a tampered archive and refusing it outright is the safest
  // response to a symlink-escape attempt (see extractTarball above). Special
  // nodes are rejected for the same reason: neither the release nor its
  // installer ever ships one, and a FIFO/device could wedge or bypass a later
  // read of the extracted tree.
  //
  // stdoutMustBeComplete: this listing is a SECURITY input. The old 1 MiB
  // tail buffer silently dropped the OLDEST entries, so an archive with enough
  // filler members to push its listing past the cap hid a symlink/hardlink
  // entry from this scan entirely (while `tar -xzf` still extracted it).
  // A listing over the cap now fails closed instead.
  //
  // Returns the COMPLETE verbose listing so callers (extractTarball) can reuse
  // it for the pre-extraction declared-size check without a second tar run.
  const verbose = await runCommand('tar', ['-tvzf', tarballPath], {
    stdoutCap: listingCap,
    stdoutMustBeComplete: true,
  });
  const TYPE_LABELS = {
    l: 'symbolic link',
    h: 'hard link',
    b: 'block device node',
    c: 'character device node',
    p: 'FIFO',
    s: 'socket',
  };
  for (const line of verbose.split(/\r?\n/)) {
    if (!line) {
      continue;
    }
    const type = line[0];
    const label = TYPE_LABELS[type];
    if (label) {
      throw new InstallerError(
        `Refusing to extract tarball: archive contains a ${label}, which the release never ships.`,
      );
    }
  }
  return verbose;
}

// A month abbreviation ("Jan".."Dec") appears in the timestamp column of the
// bsdtar verbose listing; GNU tar prints an ISO date ("2023-01-01"). Both mark
// the end of the size/user fields, so the numeric token immediately before the
// first such token is the entry's declared uncompressed size in EITHER format.
const MONTH_ABBR_RE = /^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$/;
const ISO_DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

/**
 * Parse one `tar -tvzf` line's declared uncompressed size, or null when the
 * line cannot be parsed. `size` is the numeric field immediately preceding the
 * timestamp column (see MONTH_ABBR_RE / ISO_DATE_RE).
 */
function declaredEntrySize(line) {
  const tokens = line.trim().split(/\s+/);
  for (let i = 1; i < tokens.length; i += 1) {
    if (ISO_DATE_RE.test(tokens[i]) || MONTH_ABBR_RE.test(tokens[i])) {
      const candidate = tokens[i - 1];
      return /^\d+$/.test(candidate) ? Number(candidate) : null;
    }
  }
  return null;
}

/**
 * Sum the declared uncompressed sizes in a `tar -tvzf` listing.
 *
 * This is the PRE-extraction half of the decompression-bomb guard: `tar -xzf`
 * has no size bound and the download cap only limits the COMPRESSED size, so a
 * small highly-compressible archive can declare (and would expand to) many GiB.
 * Reading the declared sizes out of the listing lets us refuse BEFORE writing
 * anything to disk. Returns the total plus how many entries were parsed so a
 * caller can distinguish "empty" from "unparseable format".
 */
function sumDeclaredSizes(verboseListing) {
  let total = 0;
  let parsed = 0;
  let entries = 0;
  for (const line of verboseListing.split(/\r?\n/)) {
    if (!line.trim()) continue;
    entries += 1;
    const size = declaredEntrySize(line);
    if (size !== null) {
      total += size;
      parsed += 1;
    }
  }
  return { total, parsed, entries };
}

/**
 * Refuse a listing whose sizes could not all be read.
 *
 * A partially parsed listing used to sum only the entries it understood, so a
 * localized tar (e.g. `oct.` instead of `Oct`, or a numeric date format) made
 * the bomb guard compare a bogus small total and let the archive through. All
 * entries must be understood before the total may be trusted.
 */
function assertDeclaredSizesKnown(declared) {
  if (declared.parsed === declared.entries) return;
  const unknown = declared.entries - declared.parsed;
  throw new InstallerError(
    `Refusing to extract tarball: could not read the declared size of ${unknown} of ` +
      `${declared.entries} entries. This is commonly a localized tar listing; rerun with LC_ALL=C.`,
  );
}

/**
 * Validate every archive member NAME before extraction.
 *
 * Rejects, in order:
 *   - absolute paths (`/etc/...`, `C:\...`), which invite ambiguity between
 *     tar implementations about what the "first component" is;
 *   - any `..` path component (path traversal), which — even when the
 *     top-level-strip logic happens to keep it inside destDir — violates the
 *     release's "single top-level directory" contract and must never appear;
 *   - archives without exactly one top-level directory (required by
 *     --strip-components=1);
 *   - entries that still escape destDir after the top-level component is
 *     stripped.
 *
 * Pure and exported so the guards are unit-testable without crafting hostile
 * tarballs. Returns the resolved top-level directory name.
 */
function validateEntryNames(entries, absoluteDest) {
  // Reject absolute-path entries outright before any other accounting.
  for (const entry of entries) {
    if (entry.startsWith('/') || /^[A-Za-z]:[\\/]/.test(entry)) {
      throw new InstallerError(
        `Refusing to extract tarball: entry "${entry}" uses an absolute path.`,
      );
    }
  }

  // Reject any ``..`` component. A name-based resolve() check below already
  // catches escapes, but an explicit rejection is unambiguous and also refuses
  // the "stripped away" cases (e.g. a lone `..` top-level) that resolve back
  // inside destDir while still violating the archive contract.
  for (const entry of entries) {
    if (entry.split('/').includes('..')) {
      throw new InstallerError(
        `Refusing to extract tarball: entry "${entry}" contains a ".." path component.`,
      );
    }
  }

  // Enforce the single-top-level-directory contract required by
  // --strip-components=1.
  const topLevelComponents = new Set(entries.map((entry) => entry.split('/')[0]));
  if (topLevelComponents.size !== 1) {
    const tops = [...topLevelComponents].join(', ');
    throw new InstallerError(
      `Refusing to extract tarball: expected exactly one top-level directory, found multiple (${tops}).`,
    );
  }
  const topLevel = entries[0].split('/')[0];

  // Validate every entry stays inside destDir after stripping the single
  // top-level directory component (--strip-components=1).
  for (const entry of entries) {
    const stripped = entry.split('/').slice(1).join('/');
    if (stripped === '') {
      // The single top-level directory entry itself maps to destDir after
      // stripping; any other entry that strips to an empty path is malformed.
      const isTopLevelEntry = entry === topLevel || entry === `${topLevel}/`;
      if (!isTopLevelEntry) {
        throw new InstallerError(
          `Refusing to extract tarball: entry "${entry}" has an empty path after stripping the top-level directory.`,
        );
      }
      continue;
    }
    const resolved = path.resolve(absoluteDest, stripped);
    if (resolved !== absoluteDest && !resolved.startsWith(absoluteDest + path.sep)) {
      throw new InstallerError(
        `Refusing to extract tarball: entry "${entry}" escapes destination directory.`,
      );
    }
  }

  return topLevel;
}

async function extractTarball(
  tarballPath,
  destDir,
  { listingCap = MAX_LISTING_CHARS, declaredSizeCap = MAX_EXTRACTED_BYTES } = {},
) {
  // Use the system tar command (available on macOS, Linux, and Windows 10+),
  // but defend against path-traversal tarballs: before extracting we list the
  // archive contents and refuse to extract any entry whose resolved path
  // escapes destDir (e.g. a "../" prefix). This keeps the installer
  // dependency-free while closing the theoretical escape vector.
  //
  // Extraction uses --strip-components=1, which relies on the archive having
  // exactly one top-level directory (see README "Release tarball structure").
  // Archives that violate that contract — multiple top-level directories, or
  // entries with no path left after stripping — are rejected outright.
  //
  // A name-based `../` check alone is not enough: a tarball can smuggle a
  // symlink whose in-archive name looks safe but whose target points outside
  // destDir, then place files "through" that symlink (e.g. `link/passwd` where
  // `link -> /etc`). Because extraction happens with a system `tar`, the write
  // would follow the link before we could validate — so any symbolic or hard
  // link is rejected *before* extraction. The release tarball never uses links.
  // Note: dest is created AFTER every guard below (not before), so a refused
  // archive never leaves a directory behind. `tar -xzf` requires the target to
  // exist, so mkdir stays inside this function rather than with the caller.
  const absoluteDest = path.resolve(destDir);

  // 1. List archive entries (no extraction yet). Must be complete — see
  //    rejectLinkEntries: every guard below reads THIS listing, and a tail
  //    buffer would let a big archive hide entries from all of them.
  const listing = await runCommand('tar', ['-tzf', tarballPath], {
    stdoutCap: listingCap,
    stdoutMustBeComplete: true,
  });
  const entries = listing.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  if (entries.length === 0) {
    throw new InstallerError('Refusing to extract tarball: archive contains no entries.');
  }

  // 1a/2/3. Reject absolute paths and `..` components, enforce the single
  //         top-level directory, and prove every entry stays inside destDir.
  validateEntryNames(entries, absoluteDest);

  // 1b. Reject any symbolic/hard link — and any device/FIFO/socket node —
  // before touching the tree. The verbose listing's first character is the
  // entry type for both GNU tar and bsdtar (macOS): '-' regular, 'd' directory,
  // 'l' symbolic link, 'h' hard link, 'b'/'c' device, 'p' FIFO. The COMPLETE
  // listing is returned so the declared-size check below can reuse it.
  const verbose = await rejectLinkEntries(tarballPath, { listingCap });

  // 1c. PRE-extraction decompression-bomb check: refuse an archive whose
  //     declared uncompressed total exceeds the budget, using the sizes from
  //     the listing we already parsed. This fails before a single byte is
  //     written, complementing the post-extraction re-measure in step 5.
  const declared = sumDeclaredSizes(verbose);
  assertDeclaredSizesKnown(declared);
  if (declared.total > declaredSizeCap) {
    throw new InstallerError(
      `Refusing to extract tarball: declared uncompressed size ${declared.total} bytes ` +
        `exceeds the safety budget (${declaredSizeCap} bytes).`,
    );
  }

  // 4. Now extract safely — the content has been validated above.
  fs.mkdirSync(absoluteDest, { recursive: true });
  await runCommand('tar', ['-xzf', tarballPath, '-C', absoluteDest, '--strip-components=1']);

  // 5. Decompression-bomb guard (mirrors scripts/install.py). ``tar`` itself
  //    has no size bound, and ``--max-filesize`` on the download only limits
  //    the COMPRESSED size, so a small, highly compressible archive could have
  //    expanded to many GiB already. Re-measure the extracted tree and fail
  //    closed (removing it) when it exceeds the budget.
  enforceExtractedSize(absoluteDest);
}

/**
 * Fail closed when an extracted tree exceeds the size budget.
 *
 * Separate, injectable-budget helper so the bomb guard is unit-testable
 * without writing 500 MiB to disk. Removes ``root`` on violation.
 */
function enforceExtractedSize(
  root,
  { maxTotal = MAX_EXTRACTED_BYTES, maxMember = MAX_EXTRACTED_MEMBER_BYTES } = {},
) {
  const extracted = measureTree(root);
  if (extracted.total > maxTotal || extracted.largest > maxMember) {
    try {
      fs.rmSync(root, { recursive: true, force: true });
    } catch {
      // Best effort: the size violation below is the actionable message.
    }
    throw new InstallerError(
      `Refusing to keep extracted tarball: expanded size ${extracted.total} bytes ` +
        `(largest member ${extracted.largest} bytes) exceeds the safety budget ` +
        `(${maxTotal} total / ${maxMember} per file).`,
    );
  }
  return extracted;
}

/**
 * Total and largest-file sizes of a directory tree.
 *
 * Symlinks are skipped (``lstat``): following them could walk outside the
 * extraction directory, and the release ships none (any link was already
 * rejected before extraction).
 */
function measureTree(root) {
  let total = 0;
  let largest = 0;
  const stack = [root];
  while (stack.length > 0) {
    const current = stack.pop();
    let entries;
    try {
      entries = fs.readdirSync(current, { withFileTypes: true });
    } catch {
      continue; // Unreadable entry: nothing to account for.
    }
    for (const entry of entries) {
      const full = path.join(current, entry.name);
      if (entry.isSymbolicLink()) continue;
      if (entry.isDirectory()) {
        stack.push(full);
        continue;
      }
      try {
        const size = fs.lstatSync(full).size;
        total += size;
        if (size > largest) largest = size;
      } catch {
        // Raced/removed entry: skip.
      }
    }
  }
  return { total, largest };
}

function runPythonInstall(pythonBin, installScript, args, options = {}) {
  // A wedged pip/skill install must never hang the whole installer forever.
  // On timeout we SIGKILL the child's *process group*: spawn in its own
  // session (detached) so grandchildren holding the pipes are reaped too,
  // mirroring the Python updater's killpg hardening.
  const { timeout = DEFAULT_COMMAND_TIMEOUT_MS, ...spawnOptions } = options;
  const detached = process.platform !== 'win32';
  return new Promise((resolve, reject) => {
    const child = spawn(pythonBin, [installScript, 'install', ...args], {
      stdio: 'inherit',
      env: { ...process.env, FORCE_COLOR: '1' },
      detached,
      ...spawnOptions,
    });
    const timer =
      timeout > 0
        ? setTimeout(() => {
            try {
              if (child.pid === undefined) {
                child.kill('SIGKILL');
              } else if (detached) {
                process.kill(-child.pid, 'SIGKILL'); // negative pid = whole group
              } else {
                child.kill('SIGKILL');
              }
            } catch {
              // Process already gone — nothing to reap.
            }
          }, timeout)
        : null;
    child.on('close', (code) => {
      if (timer) clearTimeout(timer);
      // Resolve with the exit code (rather than rejecting) so the caller can
      // distinguish "real failure" from "user cancelled the selection" and
      // avoid reporting a false success. A signal-killed child reports a null
      // code, which the shell would otherwise read as success; normalize to a
      // non-zero failure.
      resolve(typeof code === 'number' ? code : 1);
    });
    child.on('error', (err) => {
      if (timer) clearTimeout(timer);
      reject(err);
    });
  });
}

async function cleanup(dir) {
  try {
    fs.rmSync(dir, { recursive: true, force: true });
  } catch {
    // ignore cleanup errors
  }
}

/**
 * Install the iterate CLI (the `iterate` command) so the user can run
 * `iterate onboard` / `iterate status` / `iterate refresh` right after
 * installation, making the one-command flow actually end-to-end.
 *
 * The CLI is not required for the AI-assistant skill itself, so a failure
 * here is non-fatal: we warn and let the user install it later.
 *
 * Strategy: prefer ``pipx`` (isolated global install) when available,
 * otherwise fall back to ``python -m pip install --user``. If ``iterate``
 * already exists on PATH, skip entirely.
 */
async function installCli(pythonBin, sourceDir) {
  if (commandExists('iterate')) {
    success('iterate CLI already available.');
    return;
  }

  step('Installing iterate CLI (for `iterate onboard` / status / refresh)');
  try {
    if (commandExists('pipx')) {
      await runCommand('pipx', ['install', '--force', '.', '-q'], { cwd: sourceDir });
      success('iterate CLI installed via pipx.');
    } else {
      // No pipx: fall back to `pip install --user`. On macOS/Linux this can
      // fail with a PEP 668 "externally-managed-environment" error (e.g.
      // Homebrew Python). Detect that and give the user an actionable next
      // step instead of a generic failure message.
      try {
        await runCommand(pythonBin, ['-m', 'pip', 'install', '--user', '--quiet', '.'], {
          cwd: sourceDir,
        });
        success('iterate CLI installed via pip --user.');
      } catch (err) {
        const msg = err && err.message ? err.message : '';
        if (msg.includes('externally-managed')) {
          warning('System Python is externally managed (PEP 668); `pip install --user` was blocked.');
          hint('Install pipx and retry:  brew install pipx && pipx install .');
          hint('Or override the check:  python3 -m pip install --user --break-system-packages .');
        } else {
          throw err;
        }
      }
    }
  } catch (err) {
    warning(`Could not install iterate CLI: ${err.message}`);
    // Not on PyPI: the only public install paths are the repo (or its
    // release source dir) — the old "pipx install <repo>" placeholder was not
    // copy-pasteable at all.
    hint('Install it later with:  pipx install "git+https://github.com/jingzhao-l/iterate-skill.git"');
    hint('  (or, from a downloaded release/repo root:  pipx install .  /  pip install .)');
    return;
  }

  if (commandExists('iterate')) {
    success('iterate CLI is ready to use.');
  } else {
    hint('Ensure ~/.local/bin (or pipx bin) is on your PATH.');
  }
}

/**
 * Ask the user a yes/no question on the terminal.
 *
 * Used to decide whether the current directory should be treated as the
 * target project when the installer is launched from a non-home directory.
 * Falls back to ``defaultNo`` if the input is unrecognized, on EOF (piped
 * stdin that ends without an answer) or after a timeout, so a non-interactive
 * or hung invocation resolves instead of blocking forever.
 */
function askYesNo(question, defaultNo = false) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const hint = defaultNo ? '[y/N]' : '[Y/n]';
    let settled = false;
    const finish = (value) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      rl.close();
      resolve(value);
    };
    // EOF (stdin is a closed pipe, or the terminal disappears) never invokes
    // rl.question's callback; the interface 'close' event is the signal that
    // no answer is coming, so fall back to the default instead of hanging.
    rl.on('close', () => finish(defaultNo));
    const timer = setTimeout(() => finish(defaultNo), ASK_YES_NO_TIMEOUT_MS);
    rl.question(`\x1b[36m◆\x1b[0m  ${question} ${hint} `, (answer) => {
      const a = answer.trim().toLowerCase();
      if (a === 'y' || a === 'yes') finish(true);
      else if (a === 'n' || a === 'no') finish(false);
      else finish(defaultNo);
    });
  });
}

/**
 * Resolve the install mode (global vs project) before any download happens.
 *
 * Rules:
 *   - If the user passed --target or --global explicitly, honor it.
 *   - Otherwise ("global" by default), if the current directory is NOT the
 *     user's home directory, ask whether it is the target project directory.
 *     If so, switch to a project-level install into the current directory.
 */
async function resolveInstallMode(options, ask = askYesNo) {
  if (options.targetExplicit || options.globalExplicit) {
    return options;
  }
  const cwd = process.cwd();
  const home = os.homedir();
  if (cwd !== home) {
    // defaultNo = true (kept as the behavior AND made visible in the prompt):
    // the question used to render "[Y/n]" while Enter, EOF and the timeout all
    // resolved to No — a user pressing Enter to accept was silently sent to a
    // global install instead. Now the prompt shows "[y/N]" and matches.
    const answer = await ask(
      `Install into this project? / 当前目录 ${cwd} 看起来是项目目录，是否安装到此项目？` +
        ' (n = install globally to your home directory / 全局安装)',
      true,
    );
    if (answer) {
      options.target = cwd;
      options.global = false;
    }
  }
  return options;
}

function getVenvPython(venvDir) {
  const isWindows = process.platform === 'win32';
  const pythonName = isWindows ? 'python.exe' : 'python';
  return path.join(venvDir, isWindows ? 'Scripts' : 'bin', pythonName);
}

async function createVenv(pythonBin, venvDir) {
  await runCommand(pythonBin, ['-m', 'venv', venvDir]);
}

async function installRequirements(pythonBin, requirementsPath) {
  if (!fs.existsSync(requirementsPath)) return;
  await runCommand(pythonBin, ['-m', 'pip', 'install', '--quiet', '--requirement', requirementsPath]);
}

/**
 * Build the argv passed to the Python installer (scripts/install.py install).
 *
 * Exported as a pure function so the flag surface — including the relative
 * ``--target`` resolution — can be unit-tested without running the full
 * download pipeline. A relative ``--target`` is resolved against the current
 * working directory here because the Python installer runs with ``cwd`` set
 * to the extracted release directory; passing the raw relative path would
 * make it point at the wrong place.
 */
function buildPythonInstallArgs(options) {
  const args = [];
  if (options.ai) args.push('--ai', options.ai);
  if (options.target) args.push('--target', path.resolve(options.target));
  if (options.force) args.push('--force');
  if (options.globalInstall) args.push('--global');
  return args;
}

/**
 * Parse the installer's command-line arguments.
 *
 * Kept as a pure function (exported) so the flag surface — including the
 * skill-only ``--no-cli`` switch — can be unit-tested without spawning the
 * full download-and-install pipeline. Hard argument errors (a value-consuming
 * flag missing its value, an unknown option) THROW an ``InstallerError`` for
 * the CLI boundary to report; library code must never call ``process.exit``
 * (which would skip the caller's cleanup/flush and is untestable in-process).
 */
function parseArgs(argv) {
  const options = {
    global: true,
    ai: null,
    target: null,
    force: false,
    noCli: false,
    token: normalizeToken(process.env.GITHUB_TOKEN),
    // Non-install action requested via -h/--help/-v/--version. bin/cli.js
    // inspects this before running main() and exits 0 without installing.
    mode: null,
    // Track whether the user explicitly chose global/project mode so the
    // installer can later ask about the current directory's project intent.
    globalExplicit: false,
    targetExplicit: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    const next = argv[i + 1];

    // Accept `--flag=value` as well as `--flag value`: `--ai=trae` is the
    // spelling users copy from other CLIs, and it used to die as an unknown
    // option. Split it here so every value-taking switch shares one path.
    let name = arg;
    let inlineValue = null;
    if (arg.startsWith('--')) {
      const eq = arg.indexOf('=');
      if (eq !== -1) {
        name = arg.slice(0, eq);
        inlineValue = arg.slice(eq + 1);
      }
    }

    // -h/--help and -v/--version short-circuit parsing: later arguments (even
    // malformed or value-consuming flags) must not turn `--help`/`--version`
    // into an error exit. bin/cli.js exits 0 on these modes before installing.
    if (name === '--help' || name === '-h') {
      options.mode = 'help';
      break;
    }
    if (name === '--version' || name === '-v') {
      options.mode = 'version';
      break;
    }

    // Boolean flags never take a value; `--force=1` is a typo worth naming
    // rather than silently treating as --force.
    if (inlineValue !== null && ['--global', '--force', '--no-cli'].includes(name)) {
      throw new InstallerError(`${name} does not take a value`);
    }

    switch (name) {
      case '--ai': {
        const value = inlineValue !== null ? inlineValue : next;
        if (!value || value.startsWith('-')) {
          throw new InstallerError('--ai requires a value (a flag was found instead)');
        }
        options.ai = value;
        if (inlineValue === null) i++;
        break;
      }
      case '--target': {
        const value = inlineValue !== null ? inlineValue : next;
        if (!value || value.startsWith('-')) {
          throw new InstallerError('--target requires a value (a flag was found instead)');
        }
        if (options.globalExplicit) {
          warning('--target overrides --global: installing into the project directory instead.');
        }
        options.target = value;
        options.global = false;
        options.targetExplicit = true;
        if (inlineValue === null) i++;
        break;
      }
      case '--global':
        if (options.targetExplicit) {
          warning('--global overrides --target: installing into the user home directory instead.');
        }
        options.global = true;
        options.target = null;
        options.globalExplicit = true;
        break;
      case '--force':
        options.force = true;
        break;
      case '--no-cli':
        // Skill-only install: skip the automated `iterate` CLI install so a
        // user who only wants the skill is not surprised by a global install.
        options.noCli = true;
        break;
      case '--token': {
        const value = inlineValue !== null ? inlineValue : next;
        if (!value || value.startsWith('-')) {
          throw new InstallerError('--token requires a value (a flag was found instead)');
        }
        options.token = normalizeToken(value);
        if (inlineValue === null) i++;
        break;
      }
      default:
        if (arg.startsWith('-')) {
          throw new InstallerError(`unknown option ${name}`);
        }
        // A bare positional argument is not a valid installer flag; warn so a
        // typo like "npx iterate-skill-installer trae" is not silently ignored.
        warning(`Ignoring unexpected positional argument: ${arg}`);
        break;
    }
  }

  return options;
}

/**
 * Select the newest stable skill release from a GitHub release list.
 *
 * The list endpoint returns releases newest-published first. A usable release
 * must carry the tarball AND its checksums. The detached signature is
 * deliberately NOT part of the filter: a release without one is selectable and
 * then handled by ``signaturePolicyError``, which aborts unless the documented
 * ``ITERATE_ALLOW_UNSIGNED`` override is set — matching the Python installer's
 * ``_select_skill_release`` (requiring the signature at selection time made
 * that override unreachable, and the two installers disagreed).
 *
 * @param {Array} releases - The GitHub releases payload (newest first).
 * @returns {object|null} The selected release, or null when none is usable.
 */
function selectSkillRelease(releases) {
  if (!Array.isArray(releases)) return null;
  return (
    releases.find(
      (r) =>
        r &&
        !r.draft &&
        !r.prerelease &&
        Array.isArray(r.assets) &&
        r.assets.some((a) => a && a.name === TARBALL_ASSET_NAME) &&
        r.assets.some((a) => a && a.name === CHECKSUMS_ASSET_NAME),
    ) || null
  );
}

async function main(options = {}) {
  printBanner();

  // Resolve global vs project mode before downloading. If the user launched
  // the installer from a non-home directory without explicit flags, ask
  // whether that directory is the target project.
  options = await resolveInstallMode(options);

  const {
    global: globalInstall = true,
    ai = null,
    token = null,
    target = null,
    force = false,
    noCli = false,
  } = options;

  // Fail fast on a malformed PAT (same rule as scripts/install.py): sending a
  // typo'd token produced a confusing 401/403 only AFTER the API round-trip.
  const tokenError = validateTokenShape(token);
  if (tokenError) {
    error(tokenError);
    return 1;
  }

  step('Checking environment');
  const pythonBin = await findPython();
  if (!pythonBin) {
    error('Python is required but was not found on PATH.');
    hint('Install Python 3.10+ and ensure "python3" or "python" is available.');
    return 1;
  }
  success(`Found Python: ${pythonBin}`);
  frameSection('Environment', [
    `\x1b[32m✓\x1b[0m Python: ${pythonBin}`,
    `\x1b[34mℹ\x1b[0m Install mode: ${globalInstall ? 'global' : 'project'}`,
  ]);

  info('Fetching latest release from GitHub...');
  let releases;
  try {
    releases = await fetchJson(RELEASES_API_URL, token);
  } catch (err) {
    error(`Could not fetch release info: ${err.message}`);
    hint('You can set GITHUB_TOKEN for higher API rate limits.');
    return 1;
  }

  // The list endpoint returns releases newest-published first. Select the first
  // that is a stable release carrying BOTH assets we need, so a release from
  // another sub-project (or one whose assets are still uploading) is skipped
  // rather than mistaken for the latest skill release.
  if (!Array.isArray(releases)) {
    // A non-array payload (an error object, a single release object) used to
    // be used AS the release and then failed with the misleading "Latest
    // release has no tag." — say what actually went wrong.
    error('GitHub API returned an unexpected payload (expected an array of releases).');
    hint('Retry, or set GITHUB_TOKEN if this is a rate-limit artefact.');
    return 1;
  }
  // Announce releases that carry the tarball but not the checksum/signature
  // pair: they are skipped, which silently installs an OLDER release when the
  // newest one is mid-upload. Saying so out loud keeps "installed an old
  // version" visible.
  for (const candidate of releases) {
    if (!candidate || candidate.draft || candidate.prerelease) continue;
    const assets = Array.isArray(candidate.assets) ? candidate.assets : [];
    const hasTarball = assets.some((a) => a && a.name === TARBALL_ASSET_NAME);
    const missing = [];
    if (!assets.some((a) => a && a.name === CHECKSUMS_ASSET_NAME)) missing.push(CHECKSUMS_ASSET_NAME);
    if (!assets.some((a) => a && a.name === TARBALL_SIGNATURE_ASSET_NAME)) missing.push(TARBALL_SIGNATURE_ASSET_NAME);
    if (hasTarball && missing.length > 0) {
      warning(
        `Skipping release ${candidate.tag_name}: has ${TARBALL_ASSET_NAME} but no ${missing.join(' / ')}.`,
      );
    }
  }
  // A usable release must carry the tarball and its checksums. The detached
  // signature is NOT part of the selection filter: a release without one is
  // selectable and then handled by signaturePolicyError, which ABORTS unless
  // the documented ITERATE_ALLOW_UNSIGNED override is set — matching the
  // Python installer (_select_skill_release), where requiring the signature at
  // selection time made that override unreachable.
  const release = selectSkillRelease(releases);

  if (!release) {
    error(
      `No published release in the last 100 carries a ${TARBALL_ASSET_NAME} + ` +
        `${CHECKSUMS_ASSET_NAME} asset pair.`
    );
    hint('This is usually a GitHub API rate limit; retry with GITHUB_TOKEN set.');
    return 1;
  }

  const tag = release.tag_name;
  if (!tag) {
    error('Latest release has no tag.');
    return 1;
  }
  success(`Latest release: ${tag}`);

  const tarballAsset = findReleaseAsset(release.assets, TARBALL_ASSET_NAME);
  const checksumAsset = findReleaseAsset(release.assets, CHECKSUMS_ASSET_NAME);
  // Optional `.asc` signature; its absence only downgrades authenticity to
  // integrity (see the best-effort verify below), never fails the install.
  const signatureAsset = findReleaseAsset(release.assets, TARBALL_SIGNATURE_ASSET_NAME);

  if (!tarballAsset) {
    error(`Release is missing the ${TARBALL_ASSET_NAME} asset.`);
    return 1;
  }
  if (!checksumAsset) {
    error(`Release is missing ${CHECKSUMS_ASSET_NAME} asset.`);
    return 1;
  }

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ig-install-'));
  const tarballPath = path.join(tmpDir, TARBALL_ASSET_NAME);
  const checksumPath = path.join(tmpDir, CHECKSUMS_ASSET_NAME);

  try {
    info(`Downloading release tarball (${TARBALL_ASSET_NAME})...`);
    try {
      await downloadFile(tarballAsset.browser_download_url, tarballPath, token, { progress: true });
    } catch (err) {
      error(`Could not download release tarball: ${err.message}`);
      hint(`A 403/404 usually means the GitHub rate limit or an expired asset URL; retry with GITHUB_TOKEN set.`);
      return 1;
    }

    info('Downloading checksums...');
    try {
      await downloadFile(checksumAsset.browser_download_url, checksumPath, token, {
        maxBytes: CHECKSUMS_MAX_BYTES,
      });
    } catch (err) {
      error(`Could not download ${CHECKSUMS_ASSET_NAME}: ${err.message}`);
      return 1;
    }

    info('Verifying checksum...');
    const checksums = parseChecksums(fs.readFileSync(checksumPath, 'utf8'));
    const expectedHash = checksums.get(TARBALL_ASSET_NAME);
    if (!expectedHash) {
      error(`Checksum file does not contain ${TARBALL_ASSET_NAME}`);
      return 1;
    }
    const actualHash = await sha256File(tarballPath);
    // Constant-time, case-insensitive compare (see constantTimeHashEqual).
    const hashMatches = constantTimeHashEqual(actualHash, expectedHash);
    if (!hashMatches) {
      error('Checksum mismatch — refusing to install.');
      return 1;
    }
    success('Checksum verified.');
    frameSection('Release', [
      `\x1b[32m✓\x1b[0m Version: ${tag}`,
      `\x1b[32m✓\x1b[0m SHA256 checksum verified`,
    ]);

    // GPG authenticity check — MANDATORY (see signaturePolicyError).
    //
    // SHA256SUMS.txt travels in the SAME release as the tarball, so an attacker
    // who can replace one can replace both; the pinned public key below is the
    // only anchor they cannot forge. A missing `.asc`, a host without `gpg`, an
    // unfetchable signature, or a signature that does not verify all ABORT the
    // install. The single documented escape hatch is ``ITERATE_ALLOW_UNSIGNED``
    // (hosts without GnuPG) and it never bypasses a BAD signature.
    let signatureStatus = null;
    let signatureDetail = '';
    let signatureDownloadError = null;
    if (signatureAsset) {
      const signaturePath = path.join(tmpDir, TARBALL_SIGNATURE_ASSET_NAME);
      try {
        await downloadFile(signatureAsset.browser_download_url, signaturePath, token, {
          maxBytes: CHECKSUMS_MAX_BYTES,
        });
        const sig = verifyGpgDetachedSignature(tarballPath, signaturePath, ITERATE_SIGNING_PUBLIC_KEY, tmpDir);
        signatureStatus = sig.status;
        signatureDetail = sig.detail;
      } catch (err) {
        signatureDownloadError = err.message;
      }
    }
    const signatureError = signaturePolicyError({
      hasSignatureAsset: Boolean(signatureAsset),
      status: signatureStatus,
      detail: signatureDetail,
      downloadError: signatureDownloadError,
    });
    if (signatureError) {
      error(signatureError);
      return 1;
    }
    if (signatureStatus === 'verified') {
      success('GPG signature verified.');
    } else if (allowUnsigned()) {
      warning(
        `Signature NOT verified (${signatureDetail || 'no signature'}) but accepted because ` +
          `${ALLOW_UNSIGNED_ENV} is set — SHA256 integrity only.`,
      );
    }

    info('Extracting release...');
    const sourceDir = path.join(tmpDir, 'source');
    fs.mkdirSync(sourceDir, { recursive: true });
    await extractTarball(tarballPath, sourceDir);
    success('Release extracted.');

    const installScript = path.join(sourceDir, 'scripts', 'install.py');
    if (!fs.existsSync(installScript)) {
      error(`Install script not found at ${installScript}`);
      return 1;
    }

    info('Creating isolated Python environment...');
    const venvDir = path.join(tmpDir, 'venv');
    try {
      await createVenv(pythonBin, venvDir);
    } catch (err) {
      error(`Could not create Python venv: ${err.message}`);
      hint('Ensure the Python "venv" module is available.');
      return 1;
    }
    const venvPython = getVenvPython(venvDir);

    info('Installing Python dependencies...');
    const requirementsPath = path.join(sourceDir, 'scripts', 'requirements.txt');
    try {
      await installRequirements(venvPython, requirementsPath);
      success('Dependencies ready.');
    } catch (err) {
      error(`Could not install Python dependencies: ${err.message}`);
      return 1;
    }

    const installArgs = buildPythonInstallArgs({ ai, target, force, globalInstall });

    info('Starting skill installation (Python installer)...');
    const installExit = await runPythonInstall(venvPython, installScript, installArgs, { cwd: sourceDir });
    if (installExit !== 0) {
      // The Python installer prints a specific reason (e.g. "No assistants
      // selected. Installation cancelled."). Do not proceed to the CLI install
      // or print a success box — the install was cancelled or failed.
      warning('Skill installation was cancelled or failed; stopping.');
      return installExit;
    }
    success('iterate-skill installation finished.');

    if (noCli) {
      // Skill-only install: explain how to add the CLI later instead of
      // silently installing it globally.
      hint('Skipped installing the iterate CLI (--no-cli).');
      hint('Install it later for `iterate onboard` with:  pipx install "git+https://github.com/jingzhao-l/iterate-skill.git"');
    } else {
      // Install the iterate CLI so `iterate onboard` works right after
      // install. Made explicit up front so skill-only users are not surprised
      // by a global CLI install (skip with --no-cli).
      step('Installing the iterate CLI (skip with --no-cli)');
      await installCli(pythonBin, sourceDir);
    }

    frameSection('Done', [
      `\x1b[32m✓\x1b[0m iterate-skill ${tag} installed`,
      `  Run \x1b[36miterate onboard\x1b[0m in your project to initialize.`,
    ]);
    return 0;
  } finally {
    await cleanup(tmpDir);
  }
}

module.exports = {
  main,
  parseArgs,
  buildPythonInstallArgs,
  VERSION,
  ITERATE_BANNER,
  InstallerError,
  resolveInstallMode,
  askYesNo,
  selectSkillRelease,
  parseChecksums,
  constantTimeHashEqual,
  enforceDownloadedSize,
  findReleaseAsset,
  extractTarball,
  rejectLinkEntries,
  sumDeclaredSizes,
  assertDeclaredSizesKnown,
  declaredEntrySize,
  validateEntryNames,
  isGithubApiUrl,
  normalizeToken,
  validateTokenShape,
  allowUnsigned,
  signaturePolicyError,
  ALLOW_UNSIGNED_ENV,
  buildAuthFlags,
  supportsCurlFailWithBody,
  // Executed under test for the timeout/null-exit-code hardening; retaining
  // the exports also keeps them statically reachable for QA/debugging.
  runCommand,
  runPythonInstall,
  TailBuffer,
  FullBuffer,
  measureTree,
  enforceExtractedSize,
  verifyGpgDetachedSignature,
  GPG_TIMEOUT_MS,
  MAX_LISTING_CHARS,
  MAX_EXTRACTED_BYTES,
  MAX_EXTRACTED_MEMBER_BYTES,
  DEFAULT_COMMAND_TIMEOUT_MS,
};
