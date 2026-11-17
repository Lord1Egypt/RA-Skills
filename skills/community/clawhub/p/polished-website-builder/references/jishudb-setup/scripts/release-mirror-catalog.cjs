'use strict';

// AI-generated supply-chain trust boundary; human security review is pending.
// This dependency-free contract is copied byte-for-byte into distributed Skills.
// Never obtain authority from the catalog or replace independently embedded trust.
const crypto = require('node:crypto');

const DOMAIN = 'jishudb-release-mirror-catalog-v1';
const RENEWAL_DOMAIN = 'jishudb-release-mirror-catalog-v2';
const RENEWED_METADATA = Object.freeze(['latest.yml', 'latest-mac.yml', 'SHA256SUMS.txt']);
const REPOSITORY = 'x-aijishu/jishudb-desktop-releases';
const MAX_CATALOG_BYTES = 256 * 1024;
const MAX_LIFETIME_MS = 7 * 24 * 60 * 60 * 1000;
const SEMVER = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;
const HEX256 = /^[0-9a-f]{64}$/;

class MirrorCatalogError extends Error {
  constructor(code, message, options) {
    super(message, options);
    this.name = 'MirrorCatalogError';
    this.code = code;
  }
}

function fail(code, message, cause) {
  throw new MirrorCatalogError(code, message, cause ? { cause } : undefined);
}

function exact(value, keys, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)
      || ![Object.prototype, null].includes(Object.getPrototypeOf(value))
      || Object.keys(value).sort().join('\n') !== [...keys].sort().join('\n')) {
    fail('catalog_invalid', `${label} fields are invalid`);
  }
}

function text(value, pattern, label) {
  if (typeof value !== 'string' || !pattern.test(value)) fail('catalog_invalid', `${label} is invalid`);
  return value;
}

function positive(value, label, maximum = Number.MAX_SAFE_INTEGER) {
  if (!Number.isSafeInteger(value) || value < 1 || value > maximum) fail('catalog_invalid', `${label} is invalid`);
  return value;
}

/** Sorted-key JSON matching the existing update-manifest-signature.mjs contract. */
function canonicalJSON(value, seen = new Set()) {
  if (value === null || ['boolean', 'string'].includes(typeof value)) return JSON.stringify(value);
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) fail('catalog_invalid', 'Non-finite catalog number');
    return JSON.stringify(value);
  }
  if (typeof value !== 'object' || seen.has(value) || seen.size >= 64) fail('catalog_invalid', 'Unsupported, cyclic, or excessively nested catalog value');
  seen.add(value);
  try {
    if (Array.isArray(value)) return `[${value.map(item => canonicalJSON(item, seen)).join(',')}]`;
    if (![Object.prototype, null].includes(Object.getPrototypeOf(value))) fail('catalog_invalid', 'Catalog must contain plain objects');
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalJSON(value[key], seen)}`).join(',')}}`;
  } finally { seen.delete(value); }
}

function canonicalBytes(value) { return Buffer.from(canonicalJSON(value), 'utf8'); }

function base64(value, maximum, label) {
  if (typeof value !== 'string' || value.length === 0 || value.length > maximum || !/^[A-Za-z0-9+/]+={0,2}$/.test(value)) {
    fail('catalog_signature_invalid', `${label} is invalid`);
  }
  const result = Buffer.from(value, 'base64');
  if (result.toString('base64') !== value) fail('catalog_signature_invalid', `${label} is not canonical Base64`);
  return result;
}

function normalizeAuthority(raw) {
  let key;
  try {
    exact(raw, ['algorithm', 'keyId', 'publicKey'], 'Embedded authority');
    const bytes = base64(raw.publicKey, 256, 'Public key');
    key = crypto.createPublicKey({ key: bytes, format: 'der', type: 'spki' });
    if (key.asymmetricKeyType !== 'ed25519' || !Buffer.from(key.export({ format: 'der', type: 'spki' })).equals(bytes)
        || raw.algorithm !== 'Ed25519' || raw.keyId !== `ed25519-sha256:${crypto.createHash('sha256').update(bytes).digest('hex')}`) {
      fail('catalog_signature_invalid', 'Embedded authority is invalid');
    }
  } catch (error) { fail('catalog_signature_invalid', 'Independently approved Ed25519 authority is required', error); }
  return Object.freeze({ algorithm: raw.algorithm, keyId: raw.keyId, publicKey: raw.publicKey });
}

function timestamp(value, label) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value)
      || !Number.isFinite(Date.parse(value)) || new Date(value).toISOString() !== value) fail('catalog_invalid', `${label} must be canonical UTC`);
  return Date.parse(value);
}

function url(value, label, allowQuery = false) {
  let parsed;
  try { parsed = new URL(value); } catch { fail('blocked_origin', `${label} is invalid`); }
  if (typeof value !== 'string' || value.length > 8192 || parsed.href !== value || parsed.protocol !== 'https:'
      || parsed.username || parsed.password || parsed.port || parsed.hash || (!allowQuery && parsed.search)
      || /[\\\x00-\x20\x7f]/.test(value) || parsed.pathname.includes('%') || parsed.pathname.includes('//')) {
    fail('blocked_origin', `${label} must be a canonical HTTPS URL`);
  }
  return parsed;
}

function artifactSpecifications(version) {
  text(version, SEMVER, 'Version');
  if (version.split('.').some(item => !Number.isSafeInteger(Number(item)))) fail('catalog_invalid', 'Version components are too large');
  const mac = `jishudb-desktop-${version}-darwin-arm64`;
  const windows = `JishuDB-Windows-x64-${version}`;
  return [
    ...[`${mac}.dmg`, `${mac}.dmg.sha256`, `${mac}.dmg.candidate.json`, `${mac}.zip`, `${mac}.zip.sha256`, `${mac}.update-candidate.json`, 'latest-mac.yml']
      .map(name => ({ name, platform: 'darwin', architecture: 'arm64' })),
    ...[`${windows}-Setup.exe`, `${windows}-Setup.exe.sha256`, `${windows}-Setup.exe.candidate.json`, `${windows}-Setup.exe.blockmap`, `${windows}.update-candidate.json`, 'latest.yml', 'SHA256SUMS.txt']
      .map(name => ({ name, platform: 'win32', architecture: 'x64' })),
  ].sort((a, b) => a.name < b.name ? -1 : a.name > b.name ? 1 : 0);
}

/** Enforce signed metadata semantics before producing or consuming a catalog. */
function validatePayload(payload) {
  const renewal = payload?.schemaVersion === 2;
  exact(payload, ['schemaVersion', 'domain', 'product', 'channel', 'sequence', 'version', 'sourceRevision', 'issuedAt', 'expiresAt', 'canonicalRelease', 'mirror', 'artifacts', ...(renewal ? ['policyRelease', 'previousCatalogSha256', 'evidenceArtifacts'] : [])], 'Catalog payload');
  if (![1, 2].includes(payload.schemaVersion) || payload.domain !== (renewal ? RENEWAL_DOMAIN : DOMAIN) || payload.product !== 'jishudb-desktop' || payload.channel !== 'stable') fail('catalog_invalid', 'Catalog domain or channel is unsupported');
  positive(payload.sequence, 'Sequence');
  const specifications = artifactSpecifications(payload.version);
  text(payload.sourceRevision, /^[0-9a-f]{40}$/, 'Source revision');
  const issued = timestamp(payload.issuedAt, 'issuedAt');
  const expires = timestamp(payload.expiresAt, 'expiresAt');
  if (expires <= issued || expires - issued > MAX_LIFETIME_MS) fail('catalog_invalid', 'Catalog lifetime must be positive and at most seven days');
  const release = payload.canonicalRelease;
  exact(release, ['repository', 'id', 'tag', 'url', 'targetCommitish'], 'Canonical release');
  positive(release.id, 'Canonical release ID');
  text(release.targetCommitish, /^[A-Za-z0-9][A-Za-z0-9._/-]{0,254}$/, 'Canonical target commitish');
  if (release.targetCommitish.includes('..') || release.targetCommitish.includes('//')) fail('catalog_invalid', 'Canonical target commitish is invalid');
  if (release.repository !== REPOSITORY || release.tag !== `v${payload.version}`
      || release.url !== `https://github.com/${REPOSITORY}/releases/tag/v${payload.version}`) fail('catalog_invalid', 'Canonical release identity is invalid');
  if (renewal) {
    const policy = payload.policyRelease;
    exact(policy, ['repository', 'id', 'tag', 'url', 'targetCommitish'], 'Policy release');
    positive(policy.id, 'Policy release ID');
    if (policy.id === release.id || policy.repository !== REPOSITORY || typeof policy.tag !== 'string' || !policy.tag.startsWith(`v${payload.version}-policy.`)
        || !/^[1-9][0-9]*\.[1-9][0-9]*$/.test(policy.tag.slice(`v${payload.version}-policy.`.length))
        || policy.url !== `https://github.com/${REPOSITORY}/releases/tag/${policy.tag}`) fail('catalog_invalid', 'Policy release identity is invalid');
    text(policy.targetCommitish, /^[A-Za-z0-9][A-Za-z0-9._/-]{0,254}$/, 'Policy target commitish');
    if (policy.targetCommitish.includes('..') || policy.targetCommitish.includes('//')) fail('catalog_invalid', 'Policy target commitish is invalid');
    text(payload.previousCatalogSha256, HEX256, 'Predecessor catalog digest');
    if (payload.sequence < 2) fail('catalog_invalid', 'Renewal must follow an existing publication');
  }
  exact(payload.mirror, ['repositoryURL', 'redirectAllowlist', ...(renewal ? ['releaseTag'] : [])], 'Mirror policy');
  if (renewal && payload.mirror.releaseTag !== `v${payload.version}-policy.${payload.sequence}`) fail('catalog_invalid', 'Renewal publication tag must bind application version and sequence');
  const repository = url(payload.mirror.repositoryURL, 'Mirror repository');
  if (repository.origin !== 'https://cnb.cool' || !/^\/(?:[A-Za-z0-9_-]+\/)+[A-Za-z0-9_.-]+$/.test(repository.pathname)) fail('blocked_origin', 'Mirror must use the confirmed CNB repository');
  const versionPrefix = `${repository.pathname}/-/releases/download/${publicationTag(payload)}/`;
  const redirects = payload.mirror.redirectAllowlist;
  if (!Array.isArray(redirects) || redirects.length > 8) fail('catalog_invalid', 'Redirect policy must be a bounded list');
  const seenRedirects = new Set();
  for (const rule of redirects) {
    exact(rule, ['origin', 'pathPrefix'], 'Redirect rule');
    const parsed = url(`${rule.origin}${rule.pathPrefix}`, 'Redirect prefix');
    if (!['https://cnb.cool', 'https://asset.cnb.cool'].includes(rule.origin) || parsed.origin !== rule.origin
        || !rule.pathPrefix.endsWith('/') || rule.pathPrefix === '/' || rule.pathPrefix.length < 2
        || (rule.origin === 'https://cnb.cool' && !rule.pathPrefix.startsWith(versionPrefix))) fail('blocked_origin', 'Redirect rule exceeds the signed CNB release boundary');
    const identity = `${rule.origin}${rule.pathPrefix}`;
    if (seenRedirects.has(identity)) fail('catalog_invalid', 'Duplicate redirect rule');
    seenRedirects.add(identity);
  }
  if (!Array.isArray(payload.artifacts) || payload.artifacts.length !== specifications.length) fail('catalog_invalid', 'Catalog must contain all fourteen protected release artifacts');
  const seenIds = new Set();
  const seenURLs = new Set();
  payload.artifacts.forEach((artifact, index) => {
    exact(artifact, ['name', 'platform', 'architecture', 'size', 'sha256', 'canonicalURL', 'assetId', 'mirrorURL'], 'Artifact');
    const expected = specifications[index];
    for (const key of ['name', 'platform', 'architecture']) {
      if (artifact[key] !== expected[key]) fail('catalog_invalid', 'Artifacts must be exact, unique, and sorted by name');
    }
    positive(artifact.size, 'Artifact size', 4 * 1024 ** 3);
    positive(artifact.assetId, 'GitHub asset ID');
    text(artifact.sha256, HEX256, 'Artifact SHA-256');
    const sourceTag = renewal && RENEWED_METADATA.includes(artifact.name) ? payload.policyRelease.tag : release.tag;
    if (artifact.canonicalURL !== `https://github.com/${REPOSITORY}/releases/download/${sourceTag}/${artifact.name}`) fail('catalog_invalid', 'Artifact canonical identity is invalid');
    const location = url(artifact.mirrorURL, 'Mirror artifact');
    if (location.origin !== repository.origin || location.pathname !== `${versionPrefix}${artifact.name}`) fail('blocked_origin', 'Mirror artifact must use its exact immutable version and filename');
    if (seenIds.has(artifact.assetId) || seenURLs.has(artifact.mirrorURL)) fail('catalog_invalid', 'Duplicate artifact identity');
    seenIds.add(artifact.assetId);
    seenURLs.add(artifact.mirrorURL);
  });
  if (renewal) {
    if (!Array.isArray(payload.evidenceArtifacts) || payload.evidenceArtifacts.length < 1) fail('catalog_invalid', 'Renewal audit inventory is required');
    let previousName = '';
    for (const artifact of payload.evidenceArtifacts) {
      exact(artifact, ['name', 'size', 'sha256', 'canonicalURL', 'assetId', 'mirrorURL'], 'Renewal evidence artifact');
      text(artifact.name, /^policy-refresh-[1-9][0-9]*-[1-9][0-9]*\.json$/, 'Renewal evidence name');
      if (artifact.name <= previousName) fail('catalog_invalid', 'Evidence artifacts must be unique and sorted');
      previousName = artifact.name;
      positive(artifact.size, 'Evidence size', MAX_CATALOG_BYTES);
      positive(artifact.assetId, 'Evidence asset ID');
      text(artifact.sha256, HEX256, 'Evidence SHA-256');
      if (artifact.canonicalURL !== `https://github.com/${REPOSITORY}/releases/download/${payload.policyRelease.tag}/${artifact.name}`) fail('catalog_invalid', 'Evidence canonical identity is invalid');
      const location = url(artifact.mirrorURL, 'Evidence mirror');
      if (location.origin !== repository.origin || location.pathname !== `${versionPrefix}${artifact.name}`) fail('blocked_origin', 'Evidence must use the exact renewal publication');
      if (seenIds.has(artifact.assetId) || seenURLs.has(artifact.mirrorURL)) fail('catalog_invalid', 'Duplicate evidence identity');
      seenIds.add(artifact.assetId);
      seenURLs.add(artifact.mirrorURL);
    }
    const [run, attempt] = payload.policyRelease.tag.slice(`v${payload.version}-policy.`.length).split('.');
    if (!payload.evidenceArtifacts.some(item => item.name === `policy-refresh-${run}-${attempt}.json`)) fail('catalog_invalid', 'Current policy audit record is missing');
  }
  if (canonicalBytes(payload).length > MAX_CATALOG_BYTES) fail('catalog_invalid', 'Catalog is too large');
  return payload;
}

function publicationTag(payload) { return payload.schemaVersion === 2 ? payload.mirror.releaseTag : `v${payload.version}`; }
function catalogArtifacts(payload) { return [...payload.artifacts, ...(payload.schemaVersion === 2 ? payload.evidenceArtifacts : [])]; }

function compareVersions(a, b) {
  const left = a.split('.').map(Number);
  const right = b.split('.').map(Number);
  for (let index = 0; index < 3; index += 1) {
    if (left[index] !== right[index]) return left[index] < right[index] ? -1 : 1;
  }
  return 0;
}

function freeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    Object.freeze(value);
    Object.values(value).forEach(freeze);
  }
  return value;
}

/** Authenticate a bounded envelope with independent trust, freshness and rollback floors. */
function verifyCatalog(envelope, { authority, nowMs = Date.now(), minimumSequence = 0, minimumVersion = '0.0.0', acceptedPayloadSha256 = null, maxClockSkewMs = 300000 } = {}) {
  if (Buffer.isBuffer(envelope) || typeof envelope === 'string') {
    if (Buffer.byteLength(envelope) > MAX_CATALOG_BYTES) fail('catalog_invalid', 'Catalog exceeds the maximum size');
    try { envelope = JSON.parse(envelope.toString()); } catch (error) { fail('catalog_invalid', 'Catalog is not valid JSON', error); }
  }
  exact(envelope, ['payload', 'signature'], 'Catalog envelope');
  const trusted = normalizeAuthority(authority);
  // Verify the complete domain-separated payload before trusting any location.
  const bytes = canonicalBytes(envelope.payload);
  if (bytes.length > MAX_CATALOG_BYTES) fail('catalog_invalid', 'Catalog exceeds the maximum size');
  try {
    exact(envelope.signature, ['algorithm', 'keyId', 'value'], 'Catalog signature');
    const signatureBytes = base64(envelope.signature.value, 88, 'Signature');
    if (envelope.signature.algorithm !== 'Ed25519' || envelope.signature.keyId !== trusted.keyId || signatureBytes.length !== 64
        || !crypto.verify(null, bytes, crypto.createPublicKey({ key: Buffer.from(trusted.publicKey, 'base64'), format: 'der', type: 'spki' }), signatureBytes)) fail('catalog_signature_invalid', 'Catalog signature does not match embedded authority');
  } catch (error) { fail('catalog_signature_invalid', 'Catalog signature verification failed', error); }
  const payload = validatePayload(envelope.payload);
  if (!Number.isFinite(nowMs) || !Number.isSafeInteger(minimumSequence) || minimumSequence < 0
      || !Number.isSafeInteger(maxClockSkewMs) || maxClockSkewMs < 0 || maxClockSkewMs > 300000
      || (acceptedPayloadSha256 !== null && !HEX256.test(acceptedPayloadSha256))) fail('catalog_invalid', 'Local catalog verification policy is invalid');
  artifactSpecifications(minimumVersion);
  if (Date.parse(payload.issuedAt) > nowMs + maxClockSkewMs) fail('catalog_not_yet_valid', 'Catalog issue time is in the future');
  if (Date.parse(payload.expiresAt) <= nowMs) fail('catalog_expired', 'Catalog has expired; obtain a fresh signed catalog');
  if (payload.sequence < minimumSequence || compareVersions(payload.version, minimumVersion) < 0) fail('catalog_rollback', 'Catalog is older than the accepted release floor');
  const payloadSha256 = crypto.createHash('sha256').update(bytes).digest('hex');
  if (payload.sequence === minimumSequence && acceptedPayloadSha256 !== null && acceptedPayloadSha256 !== payloadSha256) fail('catalog_equivocation', 'Catalog changed under an already accepted sequence');
  return freeze({ payload: JSON.parse(bytes), signature: { ...envelope.signature }, payloadSha256, authority: trusted });
}

/** Sign only using the existing protected private key and independently approved authority. */
function signCatalog(payload, privateKeyBase64, authority) {
  validatePayload(payload);
  const trusted = normalizeAuthority(authority);
  let key;
  try {
    const bytes = base64(privateKeyBase64, 512, 'Private key');
    key = crypto.createPrivateKey({ key: bytes, format: 'der', type: 'pkcs8' });
    if (key.asymmetricKeyType !== 'ed25519' || !Buffer.from(key.export({ format: 'der', type: 'pkcs8' })).equals(bytes)
        || crypto.createPublicKey(key).export({ format: 'der', type: 'spki' }).toString('base64') !== trusted.publicKey) fail('catalog_signature_invalid', 'Signing key does not match the approved authority');
  } catch (error) { fail('catalog_signature_invalid', 'Protected signing key is invalid', error); }
  const bytes = canonicalBytes(payload);
  return { payload: JSON.parse(bytes), signature: { algorithm: 'Ed25519', keyId: trusted.keyId, value: crypto.sign(null, bytes, key).toString('base64') } };
}

/** Select the exact install-related artifact from an already verified catalog. */
function selectArtifact(verified, { platform, architecture, kind }) {
  const payload = verified.payload;
  const version = payload.version;
  const base = platform === 'win32' && architecture === 'x64' ? `JishuDB-Windows-x64-${version}-Setup.exe`
    : platform === 'darwin' && architecture === 'arm64' ? `jishudb-desktop-${version}-darwin-arm64.dmg` : null;
  const suffix = { installer: '', candidate: '.candidate.json', checksum: '.sha256' }[kind];
  if (!base || suffix === undefined) fail('catalog_invalid', 'Requested catalog platform or artifact kind is unsupported');
  const found = payload.artifacts.find(artifact => artifact.name === `${base}${suffix}`);
  if (!found) fail('catalog_invalid', 'Selected installation artifact is missing');
  return found;
}

/** Check every initial request and redirect; queries are allowed only on asset.cnb.cool. */
function assertDownloadURL(value, verified) {
  const parsed = url(value, 'Download URL', true);
  const payload = verified.payload;
  if (catalogArtifacts(payload).some(artifact => artifact.mirrorURL === value)) return parsed;
  if (parsed.search && parsed.origin !== 'https://asset.cnb.cool') fail('blocked_origin', 'Only the final CNB asset hop may carry a signed query');
  if (!payload.mirror.redirectAllowlist.some(rule => parsed.origin === rule.origin && parsed.pathname.startsWith(rule.pathPrefix))) fail('blocked_origin', 'Download redirect is outside the authenticated catalog policy');
  return parsed;
}

module.exports = { DOMAIN, RENEWAL_DOMAIN, RENEWED_METADATA, publicationTag, catalogArtifacts, REPOSITORY, MAX_CATALOG_BYTES, MAX_LIFETIME_MS, MirrorCatalogError,
  canonicalJSON, canonicalBytes, normalizeAuthority, artifactSpecifications, validatePayload,
  verifyCatalog, signCatalog, selectArtifact, assertDownloadURL };
