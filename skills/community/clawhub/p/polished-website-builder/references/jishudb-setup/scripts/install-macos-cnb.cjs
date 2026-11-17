#!/usr/bin/env node
'use strict';

// AI-generated security-sensitive macOS mirror transport. Human review pending.
// OS signature, installation and user-presence checks remain in install-macos.zsh.
const fs = require('node:fs/promises');
const { constants } = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const { verifyCatalog, assertDownloadURL, canonicalJSON } = require('./release-mirror-catalog.cjs');

const CATALOG_LIMIT = 1024 * 1024;
const METADATA_LIMIT = 16 * 1024 * 1024;
const REDIRECTS = new Set([301, 302, 303, 307, 308]);
const CATALOG_ORIGINS = new Set(['https://cnb.cool', 'https://asset.cnb.cool']);

function sanitizedCause(error, depth = 0) {
  if (!error || depth > 3) return undefined;
  const message = String(error.message || 'Unknown failure').replace(/https?:\/\/[^\s"'<>]+/gi, '[redacted-url]').slice(0, 2048);
  const cause = new Error(message);
  cause.name = /^[A-Za-z]+Error$/.test(error.name || '') ? error.name : 'Error';
  if (/^[A-Za-z][A-Za-z0-9_]{0,63}$/.test(error.code || '')) cause.code = error.code;
  if (error.cause && error.cause !== error) cause.cause = sanitizedCause(error.cause, depth + 1);
  return cause;
}

function fail(code, message, cause) {
  throw Object.assign(new Error(message, cause ? { cause: sanitizedCause(cause) } : undefined), { code });
}

function assertCatalogURL(value, config) {
  let url;
  try { url = new URL(value); } catch { fail('blocked_origin', 'Catalog URL is invalid.'); }
  if (!CATALOG_ORIGINS.has(url.origin) || url.username || url.password || url.hash || url.port
      || url.href !== value || url.pathname.includes('%') || url.pathname.includes('//')
      || (url.search && url.origin !== 'https://asset.cnb.cool')) {
    fail('blocked_origin', 'Catalog URL must use an approved anonymous CNB HTTPS origin.');
  }
  if (config && value !== config.catalogURL && !config.bootstrapRedirectAllowlist?.some((rule) =>
    rule.origin === url.origin && typeof rule.pathPrefix === 'string' && rule.pathPrefix.length > 1
      && rule.pathPrefix.endsWith('/') && url.pathname.startsWith(rule.pathPrefix))) {
    fail('blocked_origin', 'Catalog redirect is outside the independently bundled bootstrap policy.');
  }
  return url;
}

function canonicalAssetURL(asset) {
  return `https://api.github.com/repos/x-aijishu/jishudb-desktop-releases/releases/assets/${asset.assetId}`;
}

function normalizedRelease(verified) {
  const { payload } = verified;
  return {
    id: payload.canonicalRelease.id, tag_name: payload.canonicalRelease.tag,
    target_commitish: payload.canonicalRelease.targetCommitish,
    immutable: true, draft: false, prerelease: false,
    assets: payload.artifacts.map((asset) => ({
      id: asset.assetId, name: asset.name, size: asset.size, url: canonicalAssetURL(asset),
      state: 'uploaded', digest: `sha256:${asset.sha256}`,
    })),
  };
}

function transportBinding(verified, config) {
  return { source: 'cnb', catalogURL: config.catalogURL, payloadSha256: verified.payloadSha256,
    sequence: verified.payload.sequence, keyId: config.authority.keyId,
    catalog: { payload: verified.payload, signature: verified.signature } };
}

/** Fetch unsigned bytes anonymously; only the shared verifier establishes trust. */
async function responseFor(url, { fetchImpl, signal, headers, validateURL }) {
  let target = url;
  for (let redirects = 0; redirects <= 3; redirects += 1) {
    validateURL(target);
    let response;
    try {
      response = await fetchImpl(target, { redirect: 'manual', signal, headers });
    } catch (error) {
      fail(signal.aborted ? 'download_timeout' : 'transport_failed',
        signal.aborted ? 'CNB request timed out.' : 'CNB request failed.', error);
    }
    if (response.redirected) fail('blocked_origin', 'HTTP transport followed an unchecked redirect.');
    if (!REDIRECTS.has(response.status)) return response;
    const location = response.headers.get('location');
    await response.body?.cancel();
    if (!location || redirects === 3) fail('blocked_origin', 'CNB redirect is missing or exceeds the bound.');
    try { target = new URL(location, target).href; } catch { fail('blocked_origin', 'CNB redirect URL is invalid.'); }
  }
}

async function readBounded(response, limit, signal) {
  if (response.status !== 200) {
    fail(response.status === 401 || response.status === 403 ? 'metadata_authentication_required' : 'catalog_unavailable',
      `Anonymous CNB catalog returned HTTP ${response.status}.`);
  }
  const chunks = [];
  let size = 0;
  try {
    for await (const chunk of response.body) {
      size += chunk.length;
      if (size > limit) fail('catalog_invalid', 'CNB catalog exceeds the bounded metadata size.');
      chunks.push(chunk);
    }
  } catch (error) {
    if (/^[a-z][a-z0-9_]*$/.test(error.code || '')) throw error;
    fail(signal?.aborted ? 'download_timeout' : 'transfer_interrupted', 'CNB catalog transfer was interrupted.', error);
  }
  try { return JSON.parse(Buffer.concat(chunks).toString('utf8')); }
  catch (error) { fail('catalog_invalid', 'CNB catalog is not valid JSON.', error); }
}

async function readPrivateJSON(file, { optional = false } = {}) {
  let descriptor;
  try { descriptor = await fs.open(file, constants.O_RDONLY | constants.O_NOFOLLOW); } catch (error) {
    if (optional && error.code === 'ENOENT') return null;
    fail('unsafe_cache', 'CNB private state could not be opened without following links.', error);
  }
  try {
    const stat = await descriptor.stat();
    if (!stat.isFile() || stat.nlink !== 1 || (stat.mode & 0o777) !== 0o600
        || stat.uid !== process.getuid() || stat.size > CATALOG_LIMIT) {
      fail('unsafe_cache', 'CNB state must be a bounded, private, current-user regular file.');
    }
    const bytes = await descriptor.readFile();
    if (bytes.length > CATALOG_LIMIT) fail('unsafe_cache', 'CNB state exceeds its size bound.');
    try { return JSON.parse(bytes.toString('utf8')); }
    catch (error) { fail('unsafe_cache', 'CNB private state is not valid JSON.', error); }
  } finally {
    await descriptor.close();
  }
}

async function savePrivateJSON(file, value) {
  const temporary = `${file}.${crypto.randomUUID()}.tmp`;
  try {
    await fs.writeFile(temporary, JSON.stringify(value) + '\n', { mode: 0o600, flag: 'wx' });
    await fs.rename(temporary, file);
  } finally { await fs.rm(temporary, { force: true }); }
}

/** Create the macOS CNB bridge. Production config is bundled, never CLI supplied. */
function createMacCnbBridge({ config, fetchImpl = globalThis.fetch,
  statePath = path.join(os.homedir(), '.cache', 'jishudb-agent-install', 'cnb-release-state.json'),
  now = Date.now, transferTimeoutMs = 20000 } = {}) {
  if (!config?.catalogURL || !config?.authority) {
    fail('release_source_not_configured', 'CNB catalog location and approved trust material are not bundled yet.');
  }
  assertCatalogURL(config.catalogURL);

  function verify(envelope, state = {}) {
    const minimumSequence = Math.max(config.minimumSequence || 0, state.sequence || 0);
    return verifyCatalog(envelope, { authority: config.authority, nowMs: now(),
      minimumSequence,
      minimumVersion: [state.version || '0.0.0', config.minimumVersion || '0.0.0'].sort((left, right) => {
        const a = left.split('.').map(Number), b = right.split('.').map(Number);
        return a[0] - b[0] || a[1] - b[1] || a[2] - b[2];
      }).at(-1),
      acceptedPayloadSha256: state.sequence === minimumSequence ? state.payloadSha256 || null : null });
  }

  function assertPlan(verified, plan) {
    if (!plan) return;
    const expected = transportBinding(verified, config);
    if (!plan.transport || canonicalJSON(plan.transport) !== canonicalJSON(expected)
        || plan.release.version !== verified.payload.version || plan.release.sourceRevision !== verified.payload.sourceRevision
        || plan.release.id !== verified.payload.canonicalRelease.id || plan.release.tag !== verified.payload.canonicalRelease.tag
        || plan.release.targetCommitish !== verified.payload.canonicalRelease.targetCommitish) {
      fail('release_drift', 'The CNB catalog no longer matches the approved plan; approval was not renewed.');
    }
    if (!Number.isFinite(Date.parse(plan.expiresAt)) || now() >= Date.parse(plan.expiresAt)) {
      fail('plan_expired', 'The installation plan expired; cached bytes were retained without extending approval.');
    }
    if (Date.parse(plan.expiresAt) > Date.parse(verified.payload.expiresAt)) {
      fail('invalid_plan', 'Installation approval cannot outlive its signed catalog.');
    }
    for (const asset of Object.values(plan.assets)) {
      const match = verified.payload.artifacts.find((entry) => canonicalAssetURL(entry) === asset.url);
      if (!match || match.sha256 !== asset.sha256 || match.size !== asset.size || match.name !== asset.name || match.assetId !== asset.id) {
        fail('release_drift', 'Approved artifact identity differs from the signed CNB catalog.');
      }
    }
  }

  async function discover(plan) {
    // Approved transactions retain their exact signed selection until either
    // catalog or approval expires. A mutable latest pointer cannot renew consent.
    if (plan) {
      const verified = verify(plan.transport?.catalog);
      assertPlan(verified, plan);
      return { envelope: plan.transport.catalog, release: normalizedRelease(verified),
        transport: transportBinding(verified, config) };
    }
    const directory = path.dirname(statePath);
    await fs.mkdir(directory, { recursive: true, mode: 0o700 });
    const stat = await fs.lstat(directory);
    if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid() || (stat.mode & 0o777) !== 0o700) {
      fail('unsafe_cache', 'CNB rollback state directory must be private and owned by the current user.');
    }
    const lock = `${statePath}.lock`;
    try { await fs.mkdir(lock, { mode: 0o700 }); }
    catch (error) {
      if (error.code === 'EEXIST') fail('transaction_busy', 'CNB release state is locked; inspect the other or interrupted operation.');
      throw error;
    }
    try {
      const state = await readPrivateJSON(statePath, { optional: true });
      if (state && (!Number.isSafeInteger(state.sequence) || state.sequence < 0 || !/^[a-f0-9]{64}$/.test(state.payloadSha256)
          || !/^\d+\.\d+\.\d+$/.test(state.version))) fail('unsafe_cache', 'CNB rollback state is invalid.');
      const signal = AbortSignal.timeout(30000);
      const response = await responseFor(config.catalogURL, { fetchImpl, signal,
        headers: { 'Accept-Encoding': 'identity' }, validateURL: (url) => assertCatalogURL(url, config) });
      const envelope = await readBounded(response, CATALOG_LIMIT, signal);
      const verified = verify(envelope, state || {});
      assertPlan(verified, plan);
      await savePrivateJSON(statePath, { sequence: verified.payload.sequence, version: verified.payload.version,
        payloadSha256: verified.payloadSha256 });
      return { envelope, release: normalizedRelease(verified), transport: transportBinding(verified, config) };
    } finally { await fs.rmdir(lock); }
  }

  async function asset(context, canonicalURL, destination, { offset, end, headersPath } = {}) {
    const verified = verify(context.envelope);
    if (canonicalJSON(context.transport) !== canonicalJSON(transportBinding(verified, config))) {
      fail('release_drift', 'Cached CNB transport binding differs from its signed catalog.');
    }
    const artifact = verified.payload.artifacts.find((entry) => canonicalAssetURL(entry) === canonicalURL);
    if (!artifact || artifact.platform !== 'darwin' || artifact.architecture !== 'arm64') {
      fail('blocked_origin', 'Requested macOS artifact is absent from the signed CNB catalog.');
    }
    const ranged = offset !== undefined;
    if (ranged && (!Number.isSafeInteger(offset) || !Number.isSafeInteger(end) || offset < 0
        || end < offset || end >= artifact.size || end - offset + 1 > METADATA_LIMIT)) {
      fail('invalid_download_slice', 'Requested CNB range is outside the approved bounded artifact.');
    }
    if (!ranged && artifact.size > METADATA_LIMIT) fail('asset_size_mismatch', 'Full metadata fetch exceeds the size bound.');
    const signal = AbortSignal.timeout(transferTimeoutMs);
    const response = await responseFor(artifact.mirrorURL, { fetchImpl, signal,
      validateURL: (url) => assertDownloadURL(url, verified),
      headers: { 'Accept-Encoding': 'identity', ...(ranged ? { Range: `bytes=${offset}-${end}` } : {}) } });
    if (response.status !== (ranged ? 206 : 200)) {
      fail(response.status === 401 || response.status === 403 ? 'asset_authentication_required' : 'asset_download_failed',
        `Anonymous CNB artifact returned HTTP ${response.status}; cache was not advanced.`);
    }
    if (response.headers.has('content-encoding') && response.headers.get('content-encoding') !== 'identity') {
      fail('invalid_download_slice', 'CNB asset uses an unexpected content encoding.');
    }
    if (ranged && response.headers.get('content-range') !== `bytes ${offset}-${end}/${artifact.size}`) {
      fail('invalid_download_slice', 'CNB returned an unexpected byte range; cache was not advanced.');
    }
    const file = await fs.open(destination, 'wx', 0o600);
    const digest = crypto.createHash('sha256');
    let bytes = 0;
    let timedOut = false;
    try {
      try {
        for await (const chunk of response.body) {
          bytes += chunk.byteLength;
          if (bytes > (ranged ? end - offset + 1 : artifact.size)) fail('asset_size_mismatch', 'CNB returned too many bytes.');
          digest.update(chunk);
          try { await file.writeFile(chunk); }
          catch (error) { fail('cache_write_failed', 'CNB download bytes could not be written to the private cache.', error); }
        }
      } catch (error) {
        const timeout = signal.aborted && (error === signal.reason || ['AbortError', 'TimeoutError'].includes(error.name));
        if (ranged && timeout && bytes > 0) timedOut = true;
        else if (/^[a-z][a-z0-9_]*$/.test(error.code || '')) throw error;
        else if (timeout) fail('download_timeout', 'CNB asset transfer timed out without reusable bytes.', error);
        else fail('transfer_interrupted', 'CNB asset transfer was interrupted; cache was not advanced.', error);
      }
      if (!timedOut && bytes !== (ranged ? end - offset + 1 : artifact.size)) {
        fail('asset_size_mismatch', 'CNB returned a truncated successful transfer.');
      }
      if (!ranged && digest.digest('hex') !== artifact.sha256) fail('digest_mismatch', 'CNB metadata digest differs from its signed catalog.');
      if (headersPath) await fs.writeFile(headersPath,
        `HTTP/1.1 ${response.status}\r\nContent-Range: ${response.headers.get('content-range')}\r\n\r\n`,
        { mode: 0o600, flag: 'wx' });
      return { httpStatus: String(response.status), bytes, curlCode: timedOut ? 28 : 0 };
    } finally { await file.close(); }
  }

  return { discover, asset, assertPlan };
}

async function main(argv) {
  if (Number(process.versions.node.split('.')[0]) < 22) fail('node_runtime_required', 'CNB installation requires Node.js 22 or newer.');
  const config = JSON.parse(await fs.readFile(path.join(__dirname, 'release-mirror-trust.json'), 'utf8'));
  const bridge = createMacCnbBridge({ config });
  const [command, ...args] = argv;
  if (command === 'discover' || command === 'refresh') {
    const plan = command === 'refresh' ? await readPrivateJSON(args[1]) : undefined;
    const context = await bridge.discover(plan);
    await fs.writeFile(args[0], JSON.stringify(context) + '\n', { mode: 0o600, flag: 'wx' });
    return { status: 'catalog_verified' };
  }
  if (command === 'verify-plan') {
    await bridge.discover(await readPrivateJSON(args[0]));
    return { status: 'approval_verified' };
  }
  if (command === 'asset' || command === 'slice') {
    const context = await readPrivateJSON(args[0]);
    return bridge.asset(context, args[1], args[2], command === 'slice'
      ? { headersPath: args[3], offset: Number(args[4]), end: Number(args[5]) } : {});
  }
  if (command === 'release') {
    const context = await readPrivateJSON(args[0]);
    const verified = verifyCatalog(context.envelope, { authority: config.authority,
      minimumSequence: config.minimumSequence, minimumVersion: config.minimumVersion });
    const expected = `https://api.github.com/repos/x-aijishu/jishudb-desktop-releases/releases/${verified.payload.canonicalRelease.id}`;
    if (args[1] !== expected) fail('release_drift', 'CNB release revalidation requested a different canonical identity.');
    await fs.writeFile(args[2], JSON.stringify(normalizedRelease(verified)) + '\n', { mode: 0o600 });
    return { status: 'catalog_verified' };
  }
  fail('invalid_arguments', 'Unsupported macOS CNB bridge command.');
}

module.exports = { createMacCnbBridge, normalizedRelease, transportBinding, assertCatalogURL };
if (require.main === module) main(process.argv.slice(2)).then((result) => process.stdout.write(JSON.stringify(result) + '\n'))
  .catch((error) => {
    const category = /^[a-z][a-z0-9_]*$/.test(error.code || '') ? error.code : 'cnb_transport_failed';
    process.stdout.write(JSON.stringify({ status: 'failed', errorCategory: category,
      message: String(error.message).replace(/https?:\/\/\S+/g, '[redacted-url]') }) + '\n');
    process.exitCode = 1;
  });
