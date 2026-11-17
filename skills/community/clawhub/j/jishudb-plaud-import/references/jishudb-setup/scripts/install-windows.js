#!/usr/bin/env node
'use strict';
// AI-generated: reviewed plan, transport, and cache validation guard external installer execution.

const childProcess = process.getBuiltinModule('node:child_process');
const crypto = process.getBuiltinModule('node:crypto');
const fs = process.getBuiltinModule('node:fs');
const net = process.getBuiltinModule('node:net');
const os = process.getBuiltinModule('node:os');
const path = process.getBuiltinModule('node:path');

const RELEASE_REPOSITORY = 'x-aijishu/jishudb-desktop-releases';
const SOURCE_REPOSITORY = 'x-aijishu/jishudb';
const API_ORIGIN = 'https://api.github.com';
const API_VERSION = '2026-03-10';
const ASSET_REDIRECT_HOST = 'release-assets.githubusercontent.com';
const ASSET_REDIRECT_PREFIX = '/github-production-release-asset/1316997274/';
const PLAN_SCHEMA = 'jishudb-agent-install-plan-v1';
// AI-generated: versioned presentation intent is bound by the reviewed plan digest.
const BACKGROUND_PLAN_SCHEMA = 'jishudb-agent-install-plan-v2';
const REINSTALL_PLAN_SCHEMA = 'jishudb-agent-reinstall-plan-v1';
const PREFERRED_MCP_PORT = 8088;
const RESERVED_LAN_MCP_PORT = 8089;
const DESKTOP_MCP_PORT_SEARCH_LIMIT = 16;
const ENDPOINT_CONFIG_SCHEMA = 1;
const ENDPOINT_CONFIG_FILENAME = 'desktop-endpoint.json';
const MAXIMUM_ENDPOINT_CONFIG_BYTES = 4096;
const PLAN_TTL_MILLISECONDS = 30 * 60 * 1000;
const MAXIMUM_RELEASE_PAGES = 5;
const MAXIMUM_JSON_BYTES = 16 * 1024 * 1024;
const MAXIMUM_CHECKSUM_BYTES = 1024 * 1024;
const MAXIMUM_ASSET_BYTES = 1024 * 1024 * 1024;
const MAXIMUM_PLAN_BYTES = 64 * 1024;
const API_TIMEOUT_MILLISECONDS = 60 * 1000;
const SMALL_ASSET_TIMEOUT_MILLISECONDS = 60 * 1000;
const DOWNLOAD_CHUNK_BYTES = 16 * 1024 * 1024;
const DOWNLOAD_TIMEOUT_MILLISECONDS = 20 * 1000;
const DOWNLOAD_URL_TTL_MILLISECONDS = 5 * 60 * 1000;
const SEMVER_PATTERN = /^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$/;
const SHA256_PATTERN = /^[0-9a-f]{64}$/;
const REVISION_PATTERN = /^[0-9a-f]{40}$/;
const SID_PATTERN = /^S-1-[0-9]+(?:-[0-9]+)+$/;
const CONNECTION_NAME_PATTERN = /^[A-Za-z0-9._-]{1,64}$/;
const CHILD_ENVIRONMENT_ALLOWLIST = new Set([
  'allusersprofile',
  'appdata',
  'commonprogramfiles',
  'commonprogramfiles(x86)',
  'comspec',
  'homedrive',
  'homepath',
  'lang',
  'localappdata',
  'logonserver',
  'number_of_processors',
  'os',
  'path',
  'pathext',
  'processor_architecture',
  'processor_identifier',
  'programdata',
  'programfiles',
  'programfiles(x86)',
  'public',
  'sessionname',
  'systemdrive',
  'systemroot',
  'temp',
  'tmp',
  'tz',
  'userdomain',
  'username',
  'userprofile',
  'windir',
]);

class InstallError extends Error {
  constructor(category, message, options = {}) {
    super(`${category}: ${message}`, options);
    this.name = 'InstallError';
    this.category = category;
    this.publicMessage = message;
  }
}

function fail(category, message) {
  throw new InstallError(category, message);
}

function isRecord(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function requireExactProperties(value, expected, label) {
  if (!isRecord(value)) fail('invalid_contract', `${label} must be an object`);
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    fail('invalid_contract', `${label} fields do not match the reviewed schema`);
  }
}

function requirePattern(value, pattern, label) {
  if (typeof value !== 'string' || !pattern.test(value)) {
    fail('invalid_contract', `${label} is invalid`);
  }
  return value;
}

function requireSafeInteger(value, label, { positive = false } = {}) {
  if (!Number.isSafeInteger(value) || (positive && value <= 0)) {
    fail('invalid_contract', `${label} is invalid`);
  }
  return value;
}

function requireSafeText(value, label, maximumLength = 4096) {
  if (typeof value !== 'string' || value.trim() === '' || value.length > maximumLength || /[\u0000-\u001f\u007f]/.test(value)) {
    fail('invalid_contract', `${label} is invalid`);
  }
  return value;
}

function approvedDesktopMcpPorts() {
  const ports = [PREFERRED_MCP_PORT];
  for (let port = PREFERRED_MCP_PORT + 1; ports.length < DESKTOP_MCP_PORT_SEARCH_LIMIT; port += 1) {
    if (port !== RESERVED_LAN_MCP_PORT) ports.push(port);
  }
  return ports;
}

function isDesktopMcpUrl(value) {
  if (typeof value !== 'string') return false;
  try {
    const parsed = new URL(value);
    const port = Number(parsed.port);
    return parsed.protocol === 'http:'
      && parsed.hostname === '127.0.0.1'
      && parsed.pathname === '/mcp'
      && parsed.search === ''
      && parsed.hash === ''
      && parsed.username === ''
      && parsed.password === ''
      && approvedDesktopMcpPorts().includes(port);
  } catch {
    return false;
  }
}

function parseArguments(argv) {
  const mode = argv[0];
  if (!['check', 'plan', 'download', 'execute'].includes(mode)) {
    fail('invalid_arguments', 'first argument must be check, plan, download, or execute');
  }
  const allowed = new Set(['-PlanPath', '-PlanSha256', '-Client', '-ConfigTarget', '-ConnectionName', '-ReleaseSource']);
  const allowedByMode = {
    check: new Set(),
    plan: new Set(['-PlanPath', '-Client', '-ConfigTarget', '-ConnectionName', '-ReleaseSource']),
    download: new Set(['-PlanPath', '-PlanSha256', '-ReleaseSource']),
    execute: new Set(['-PlanPath', '-PlanSha256', '-ReleaseSource']),
  };
  const values = Object.create(null);
  for (let index = 1; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!allowed.has(key) || value === undefined || Object.hasOwn(values, key)) {
      fail('invalid_arguments', `invalid or duplicate argument ${JSON.stringify(key)}`);
    }
    if (!allowedByMode[mode].has(key)) fail('invalid_arguments', `${key} is not valid in ${mode} mode`);
    values[key] = value;
  }
  if (mode === 'check' && argv.length !== 1) fail('invalid_arguments', 'check mode accepts no additional arguments');
  return {
    mode,
    releaseSource: values['-ReleaseSource'] ?? (mode === 'plan' ? 'cnb' : null),
    planPath: values['-PlanPath'] ?? '',
    planSha256: values['-PlanSha256'] ?? '',
    client: values['-Client'] ?? '',
    configTarget: values['-ConfigTarget'] ?? '',
    connectionName: values['-ConnectionName'] ?? 'jishudb',
  };
}

/** Validate the source selector without letting it override an approved plan. */
function assertReleaseSourceAvailable(source = 'cnb') {
  if (source !== null && !['github', 'cnb'].includes(source)) fail('invalid_release_source', 'release source must be github or cnb');
  return source;
}

const MIRROR_PLAN_SCHEMA = 'jishudb-agent-install-envelope-v1';
const MAXIMUM_CATALOG_BYTES = 1024 * 1024;
const MAXIMUM_APPROVAL_BYTES = 2 * 1024 * 1024;

/** Load only the trust material shipped with this reviewed Skill package. */
function loadMirrorSupport() {
  const requireLocal = process.getBuiltinModule('node:module').createRequire(path.resolve(process.argv[1]));
  try {
    return { catalog: requireLocal('./release-mirror-catalog.cjs'), trust: requireLocal('./release-mirror-trust.json') };
  } catch (error) {
    throw new InstallError('release_source_not_configured', 'CNB catalog verification resources are unavailable; update the complete Skill package', { cause: error });
  }
}

function mirrorFailure(error) {
  if (error instanceof InstallError) throw error;
  throw new InstallError(error.code ?? 'catalog_invalid', error.message ?? 'CNB catalog validation failed', { cause: error });
}

function decodeBoundBytes(value, maximum, label) {
  requireExactProperties(value, ['bytesBase64', 'sha256'], label);
  requirePattern(value.sha256, SHA256_PATTERN, `${label} digest`);
  if (typeof value.bytesBase64 !== 'string' || value.bytesBase64.length > Math.ceil(maximum / 3) * 4) fail('invalid_plan', `${label} bytes exceed their limit`);
  const bytes = Buffer.from(value.bytesBase64, 'base64');
  if (!bytes.length || bytes.length > maximum || bytes.toString('base64') !== value.bytesBase64) fail('invalid_plan', `${label} bytes are not canonical base64`);
  if (sha256Bytes(bytes) !== value.sha256) fail('plan_digest_mismatch', `${label} bytes differ from the approved digest`);
  return bytes;
}

function bindBytes(bytes) {
  return { bytesBase64: bytes.toString('base64'), sha256: sha256Bytes(bytes) };
}

function mirrorFloorRoot(context) {
  return path.join(context.localAppData, 'JishuDBAgentInstall');
}

async function readMirrorFloor(context) {
  const root = mirrorFloorRoot(context);
  if (!fs.existsSync(root)) return null;
  assertRegularPath(root, 'directory', 'invalid_catalog_state');
  await assertPrivateAcl(root, true, context.identity, context.tools);
  const filename = path.join(root, 'release-floor.json');
  if (!fs.existsSync(filename)) return null;
  const floor = await readDownloadJson(filename, context);
  requireExactProperties(floor, ['sequence', 'version', 'payloadSha256'], 'catalog floor');
  requireSafeInteger(floor.sequence, 'catalog sequence', { positive: true });
  requirePattern(floor.version, SEMVER_PATTERN, 'catalog floor version');
  requirePattern(floor.payloadSha256, SHA256_PATTERN, 'catalog floor digest');
  return floor;
}

async function verifyMirrorCatalog(bytes, context, { approved = false } = {}) {
  const { catalog, trust } = loadMirrorSupport();
  let envelope;
  try { envelope = JSON.parse(bytes.toString('utf8')); }
  catch (error) { throw new InstallError('catalog_invalid', 'CNB catalog is not valid JSON', { cause: error }); }
  // An existing exact approval remains valid until its original expiry even
  // when another transaction has subsequently selected a newer catalog.
  const floor = approved ? null : await readMirrorFloor(context);
  const minimumSequence = Math.max(trust.minimumSequence ?? 0, floor?.sequence ?? 0);
  const minimumVersion = floor && compareVersion(floor.version, trust.minimumVersion ?? '0.0.0') > 0 ? floor.version : trust.minimumVersion ?? '0.0.0';
  try {
    const verified = catalog.verifyCatalog(bytes, {
      authority: trust.authority,
      minimumSequence,
      minimumVersion,
      acceptedPayloadSha256: floor?.sequence === envelope?.payload?.sequence ? floor.payloadSha256 : null,
    });
    return { kind: 'cnb', catalogBytes: bytes, verified, catalog };
  } catch (error) { mirrorFailure(error); }
}

async function advanceMirrorFloor(source, context) {
  const root = mirrorFloorRoot(context);
  if (!fs.existsSync(root)) await createPrivateDirectory(root, context.identity, context.tools);
  assertRegularPath(root, 'directory', 'invalid_catalog_state');
  await assertPrivateAcl(root, true, context.identity, context.tools);
  const unlock = await acquireDownloadLock(root, context);
  try {
    // Reverify under the lock so concurrent selections cannot lower the floor.
    const fresh = await verifyMirrorCatalog(source.catalogBytes, context);
    await writeDownloadJson(path.join(root, 'release-floor.json'), {
      sequence: fresh.verified.payload.sequence,
      version: fresh.verified.payload.version,
      payloadSha256: fresh.verified.payloadSha256,
    }, context);
  } finally { await unlock(); }
}

function mirrorSelection(source) {
  const { payload } = source.verified;
  const assets = {};
  for (const role of ['installer', 'checksum', 'candidate']) {
    let artifact;
    try { artifact = source.catalog.selectArtifact(source.verified, { platform: 'win32', architecture: 'x64', kind: role }); }
    catch (error) { mirrorFailure(error); }
    assets[role] = {
      id: artifact.assetId, name: artifact.name, size: artifact.size,
      state: 'uploaded', digest: `sha256:${artifact.sha256}`,
      url: `${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/assets/${artifact.assetId}`,
      mirrorURL: artifact.mirrorURL,
    };
  }
  const release = { id: payload.canonicalRelease.id, tag_name: payload.canonicalRelease.tag,
    target_commitish: payload.canonicalRelease.targetCommitish, immutable: true, draft: false, prerelease: false,
    assets: Object.values(assets) };
  return { version: payload.version, release, ...assets };
}

function mirrorTransport(source) {
  const selected = mirrorSelection(source);
  return { source: 'cnb', assets: Object.fromEntries(['installer', 'checksum', 'candidate'].map(role => [role, selected[role].mirrorURL])) };
}

function createMirrorEnvelope(planBytes, source) {
  return { schema: MIRROR_PLAN_SCHEMA, nativePlan: bindBytes(planBytes), catalog: bindBytes(source.catalogBytes), transport: mirrorTransport(source) };
}

async function unwrapMirrorEnvelope(envelope, context) {
  requireExactProperties(envelope, ['schema', 'nativePlan', 'catalog', 'transport'], 'mirror envelope');
  if (envelope.schema !== MIRROR_PLAN_SCHEMA) fail('invalid_plan', 'unsupported mirror envelope schema');
  const nativeBytes = decodeBoundBytes(envelope.nativePlan, MAXIMUM_PLAN_BYTES, 'native plan');
  const catalogBytes = decodeBoundBytes(envelope.catalog, MAXIMUM_CATALOG_BYTES, 'catalog');
  const source = await verifyMirrorCatalog(catalogBytes, context, { approved: true });
  requireExactProperties(envelope.transport, ['source', 'assets'], 'transport');
  requireExactProperties(envelope.transport.assets, ['installer', 'checksum', 'candidate'], 'transport assets');
  const expected = mirrorTransport(source);
  if (envelope.transport.source !== expected.source || Object.keys(expected.assets).some(role => envelope.transport.assets[role] !== expected.assets[role])) fail('transport_drift', 'approved transport differs from the authenticated catalog');
  let plan;
  try { plan = JSON.parse(nativeBytes.toString('utf8')); }
  catch (error) { throw new InstallError('invalid_plan', 'native plan JSON is invalid', { cause: error }); }
  validatePlan(plan, context);
  validateMirrorPlanBinding(plan, source);
  return { plan, source, nativeBytes, nativeSha256: envelope.nativePlan.sha256 };
}

function validateMirrorPlanBinding(plan, source) {
  const selected = mirrorSelection(source);
  validateReleaseMatchesPlan(selected.release, plan);
  if (plan.release.sourceRevision !== source.verified.payload.sourceRevision || plan.release.version !== source.verified.payload.version) fail('release_drift', 'native plan source revision differs from the authenticated catalog');
  if (Date.parse(plan.expiresAt) > Date.parse(source.verified.payload.expiresAt)) fail('expired_plan', 'approval outlives the authenticated catalog');
}

async function discoverMirror(context) {
  const { trust } = loadMirrorSupport();
  if (!trust.catalogURL) fail('release_source_not_configured', 'CNB catalog discovery URL is not configured in this Skill package');
  let url;
  try { url = new URL(trust.catalogURL); }
  catch { fail('release_source_not_configured', 'packaged CNB catalog URL is invalid'); }
  if (url.protocol !== 'https:' || url.username || url.password || url.port || url.hash || url.hostname !== 'cnb.cool') fail('blocked_origin', 'catalog URL is outside the packaged CNB origin');
  let response;
  // AI-generated: bootstrap redirects come only from the packaged trust file,
  // never from unsigned catalog content or a caller-provided host override.
  for (let hop = 0; hop <= 3; hop += 1) {
    try { response = await fetchWithTimeout(url, {}, API_TIMEOUT_MILLISECONDS); }
    catch (error) { throw new InstallError('catalog_network_failed', 'CNB catalog request failed; inspect the network diagnostic', { cause: error }); }
    if (![301, 302, 303, 307, 308].includes(response.status)) break;
    await response.body?.cancel().catch(() => {});
    let next;
    try { next = new URL(response.headers.get('location') ?? '', url); }
    catch { fail('blocked_origin', 'catalog redirect URL is invalid'); }
    if (hop === 3 || !response.headers.get('location') || next.protocol !== 'https:' || next.username || next.password || next.port || next.hash || next.search
        || !(trust.bootstrapRedirectAllowlist ?? []).some(rule => next.origin === rule.origin && next.pathname.startsWith(rule.pathPrefix))) {
      fail('blocked_origin', 'catalog redirect is outside the packaged bootstrap policy');
    }
    url = next;
  }
  if (response.status !== 200) {
    await response.body?.cancel().catch(() => {});
    fail([401, 403].includes(response.status) ? 'catalog_authentication_failed' : 'catalog_fetch_failed', `CNB catalog returned HTTP ${response.status}; anonymous direct access is required`);
  }
  let bytes;
  try { bytes = await readBoundedBody(response, MAXIMUM_CATALOG_BYTES, 'catalog_invalid', 'CNB catalog exceeds the size limit'); }
  catch (error) {
    if (error instanceof InstallError) throw error;
    throw new InstallError('catalog_transfer_interrupted', 'CNB catalog transfer was interrupted; inspect the network diagnostic', { cause: error });
  }
  const source = await verifyMirrorCatalog(bytes, context);
  return { source, selected: mirrorSelection(source) };
}

function sourceAssetURL(source, asset) {
  if (source?.kind !== 'cnb') return asset.url;
  const selected = mirrorSelection(source);
  const found = ['installer', 'checksum', 'candidate'].map(role => selected[role]).find(item => item.id === asset.id);
  if (!found || found.url !== asset.url || found.name !== asset.name || found.size !== asset.size) fail('transport_drift', 'asset does not belong to the authenticated catalog');
  return found.mirrorURL;
}

function allowedSourceRedirect(source, initial, target) {
  if (source?.kind !== 'cnb') return isAllowedAssetRedirect(initial, target);
  if (!Object.values(mirrorTransport(source).assets).includes(initial.href)) return false;
  try { source.catalog.assertDownloadURL(target.href, source.verified); return true; }
  catch { return false; }
}

async function assertSourceMatchesPlan(plan, source, context) {
  if (source?.kind !== 'cnb') return assertReleaseMatchesPlan(plan);
  const verified = await verifyMirrorCatalog(source.catalogBytes, context, { approved: true });
  validateMirrorPlanBinding(plan, verified);
  return mirrorSelection(verified).release;
}

function assertRequestedSource(args, source) {
  if (args.releaseSource != null && args.releaseSource !== (source?.kind ?? 'github')) fail('release_source_mismatch', 'source option differs from the approved plan; use the approved source without overriding it');
}

function assertWindowsX64() {
  if (process.platform !== 'win32' || process.arch !== 'x64') {
    fail('unsupported_platform', 'automatic Windows installation requires Windows x64');
  }
  const major = Number(process.versions.node.split('.')[0]);
  if (!Number.isInteger(major) || major < 22) {
    fail('unsupported_node_runtime', 'automatic Windows installation requires Node.js 22 or later');
  }
}

function normalizeLocalWindowsPath(value, label) {
  if (typeof value !== 'string' || /[\0\r\n]/.test(value)
      || value.startsWith('\\\\') || value.startsWith('//')
      || value.startsWith('\\\\?\\') || value.startsWith('\\\\.\\')
      || !path.win32.isAbsolute(value)) {
    fail('invalid_path', `${label} must be an absolute local-drive path`);
  }
  const resolved = path.win32.resolve(value);
  if (!/^[A-Za-z]:\\/.test(resolved) || resolved.slice(2).includes(':')) {
    fail('invalid_path', `${label} must not use UNC, device, or alternate-data-stream syntax`);
  }
  const unsafeComponent = resolved.slice(3).split('\\').some((component) => {
    const basename = component.split('.')[0].toUpperCase();
    return /[<>"|?*]/.test(component) || component.endsWith('.') || component.endsWith(' ')
      || /^(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])$/.test(basename);
  });
  if (unsafeComponent) fail('invalid_path', `${label} contains an unsupported Windows path component`);
  return resolved;
}

function assertNoReparseAncestors(target, label) {
  const resolved = normalizeLocalWindowsPath(target, label);
  const root = path.win32.parse(resolved).root;
  const segments = resolved.slice(root.length).split('\\').filter(Boolean);
  let current = root;
  for (const segment of segments) {
    current = path.win32.join(current, segment);
    if (!fs.existsSync(current)) break;
    const stat = fs.lstatSync(current);
    if (stat.isSymbolicLink()) fail('invalid_path', `${label} must not contain a reparse ancestor`);
    const real = fs.realpathSync.native(current);
    if (path.win32.resolve(real).toLowerCase() !== path.win32.resolve(current).toLowerCase()) {
      fail('invalid_path', `${label} must not resolve through another path`);
    }
  }
  return resolved;
}

function resolveSystemTools() {
  const systemRoot = assertNoReparseAncestors(process.env.SystemRoot ?? '', 'SystemRoot');
  if (process.env.WINDIR
      && normalizeLocalWindowsPath(process.env.WINDIR, 'WINDIR').toLowerCase() !== systemRoot.toLowerCase()) {
    fail('unsupported_platform', 'SystemRoot and WINDIR disagree');
  }
  const system32 = path.join(systemRoot, 'System32');
  const tools = {
    whoami: path.join(system32, 'whoami.exe'),
    icacls: path.join(system32, 'icacls.exe'),
    explorer: path.join(systemRoot, 'explorer.exe'),
    powershell: path.join(system32, 'WindowsPowerShell', 'v1.0', 'powershell.exe'),
  };
  for (const [name, target] of Object.entries(tools)) {
    let stat;
    try {
      stat = fs.lstatSync(target);
    } catch (error) {
      fail('unsupported_platform', `${name}.exe is unavailable: ${error.message}`);
    }
    if (!stat.isFile() || stat.isSymbolicLink()) fail('unsupported_platform', `${name}.exe is not a regular system file`);
  }
  return tools;
}

async function runNative(command, args, options = {}) {
  const resolvedCommand = assertNoReparseAncestors(command, 'native command');
  // AI-assisted: asynchronously capture trusted system-tool output. Some host
  // environments reject synchronous pipe creation with EBUSY; do not bypass
  // SID/ACL validation or fall back to a shell or an unverified executable.
  const label = options.label ?? path.basename(command);
  const result = await new Promise((resolve, reject) => {
    let child;
    const startFailure = cause => new InstallError('native_command_start_failed', `${label} could not start${cause.code ? ` (${cause.code})` : ''}`, { cause });
    try {
      child = childProcess.spawn(resolvedCommand, args, {
        env: options.env ?? process.env, stdio: ['ignore', 'pipe', 'pipe'],
        shell: false, windowsHide: true,
      });
    } catch (error) { reject(startFailure(error)); return; }
    const stdout = [], stderr = [];
    let size = 0, failure = null;
    const stop = error => {
      if (failure) return;
      failure = error;
      child.kill();
    };
    const timer = setTimeout(() => stop(new InstallError('native_command_timeout', `${label} exceeded its execution deadline`)), options.timeoutMilliseconds ?? 30000);
    const capture = chunks => chunk => {
      if (failure) return;
      const bytes = Buffer.from(chunk);
      size += bytes.length;
      if (size > (options.maxBuffer ?? 1024 * 1024)) {
        stop(new InstallError('native_command_output_limit', `${label} exceeded its output limit`));
      } else chunks.push(bytes);
    };
    child.stdout?.on('data', capture(stdout));
    child.stderr?.on('data', capture(stderr));
    const streamFailure = cause => stop(new InstallError('native_command_io_failed', `${label} output could not be read`, { cause }));
    child.stdout?.once('error', streamFailure);
    child.stderr?.once('error', streamFailure);
    child.once('error', error => { clearTimeout(timer); reject(startFailure(error)); });
    child.once('close', (status, signal) => {
      clearTimeout(timer);
      if (failure) { reject(failure); return; }
      if (signal) { reject(new InstallError('native_command_interrupted', `${label} was interrupted by ${signal}`)); return; }
      resolve({ status, stdout: Buffer.concat(stdout).toString(options.encoding ?? 'utf8'), stderr: Buffer.concat(stderr).toString(options.encoding ?? 'utf8') });
    });
  });
  if (result.status !== 0) {
    const diagnostic = (result.stderr || result.stdout || `exit ${result.status}`).trim();
    fail(options.category ?? 'native_command_failed', `${label} failed: ${diagnostic}`);
  }
  return result;
}

async function getCurrentWindowsIdentity(tools) {
  const account = (await runNative(tools.whoami, [], { label: 'whoami' })).stdout.trim();
  const user = (await runNative(tools.whoami, ['/user', '/fo', 'csv', '/nh'], { label: 'whoami SID' })).stdout;
  const sid = user.match(/S-1-[0-9]+(?:-[0-9]+)+/)?.[0] ?? '';
  if (!account || /[\0\r\n]/.test(account) || !SID_PATTERN.test(sid)) {
    fail('unsupported_platform', 'current Windows account or SID is invalid');
  }
  return { account, sid };
}

function assertRegularPath(target, expectedType, category = 'invalid_plan') {
  let resolved;
  try {
    resolved = assertNoReparseAncestors(target, 'path');
  } catch (error) {
    if (error instanceof InstallError) fail(category, error.publicMessage);
    throw error;
  }
  let stat;
  try {
    stat = fs.lstatSync(resolved);
  } catch (error) {
    fail(category, `path is missing: ${error.message}`);
  }
  const validType = expectedType === 'directory' ? stat.isDirectory() : stat.isFile();
  if (!validType || stat.isSymbolicLink()) fail(category, `path must be a regular ${expectedType}`);
  return stat;
}

function parseIcaclsEntries(stdout, target) {
  const entries = [];
  const normalizedTarget = target.toLowerCase();
  for (const original of stdout.split(/\r?\n/)) {
    let line = original.trim();
    if (!line) continue;
    if (line.toLowerCase().startsWith(normalizedTarget)) line = line.slice(target.length).trim();
    const separator = line.lastIndexOf(':(');
    if (separator <= 0) continue;
    entries.push({ identity: line.slice(0, separator).trim(), rights: line.slice(separator + 1) });
  }
  return entries;
}

function aclRightsTokens(entry) {
  return [...entry.rights.matchAll(/\(([^)]+)\)/g)].map((match) => match[1].toUpperCase());
}

function isMandatoryIntegrityEntry(entry) {
  if (!entry.identity.toLowerCase().startsWith('mandatory label\\')) return false;
  const allowed = new Set(['CI', 'I', 'IO', 'NR', 'NW', 'NX', 'OI']);
  const tokens = aclRightsTokens(entry);
  return tokens.some(token => ['NR', 'NW', 'NX'].includes(token))
    && tokens.every(token => allowed.has(token));
}

function isPrivateAclEntries(entries, directory, identity) {
  const accessEntries = entries.filter(entry => !isMandatoryIntegrityEntry(entry));
  const allowedIdentities = new Set([identity.sid, `*${identity.sid}`, identity.account].map((value) => value.toLowerCase()));
  const tokens = accessEntries.length === 1
    ? [...accessEntries[0].rights.matchAll(/\(([^)]+)\)/g)].map((match) => match[1]).sort()
    : [];
  const expectedTokens = directory ? ['CI', 'F', 'OI'] : ['F'];
  return accessEntries.length === 1
    && allowedIdentities.has(accessEntries[0].identity.toLowerCase())
    && tokens.length === expectedTokens.length
    && tokens.every((token, index) => token === expectedTokens[index]);
}

async function assertPrivateAcl(target, directory, identity, tools) {
  const result = await runNative(tools.icacls, [target], { label: 'inspect private ACL' });
  const entries = parseIcaclsEntries(result.stdout, target);
  if (!isPrivateAclEntries(entries, directory, identity)) {
    const allowedIdentities = new Set(
      [identity.sid, `*${identity.sid}`, identity.account].map(value => value.toLowerCase()),
    );
    const summary = entries.map((entry) => {
      let principal = 'other-principal';
      if (allowedIdentities.has(entry.identity.toLowerCase())) principal = 'current-user';
      else if (isMandatoryIntegrityEntry(entry)) principal = 'mandatory-label';
      return `${principal}:${aclRightsTokens(entry).sort().join(',') || 'none'}`;
    }).join('|') || 'none';
    fail(
      'invalid_permissions',
      `private path ACL is not one explicit current-user FullControl entry; observed ${summary}`,
    );
  }
}

async function setPrivateAcl(target, directory, identity, tools) {
  assertRegularPath(target, directory ? 'directory' : 'file', 'invalid_permissions');
  // Preserve explicit owner access before removing inherited grants. Otherwise
  // an intermediate failure can strand the new path with an empty DACL.
  const grant = `*${identity.sid}:${directory ? '(OI)(CI)F' : 'F'}`;
  await runNative(tools.icacls, [target, '/grant:r', grant], { label: 'set private ACL' });
  await runNative(tools.icacls, [target, '/inheritancelevel:r'], { label: 'disable ACL inheritance' });
  await runNative(
    tools.icacls,
    [target, '/remove:g', '*S-1-5-18', '*S-1-5-32-544'],
    { label: 'remove system and administrator ACL grants' },
  );
  await runNative(tools.icacls, [target, '/setowner', `*${identity.sid}`], { label: 'set private owner' });
  await runNative(tools.icacls, [target, '/verify'], { label: 'verify private ACL' });
  await assertPrivateAcl(target, directory, identity, tools);
}

async function createPrivateDirectory(target, identity, tools) {
  const resolved = normalizeLocalWindowsPath(target, 'private directory');
  assertNoReparseAncestors(path.win32.dirname(resolved), 'private directory parent');
  fs.mkdirSync(resolved, { recursive: false });
  await setPrivateAcl(resolved, true, identity, tools);
}

/** Remove only the still-pinned file created by this failed invocation. */
function cleanupCreatedPrivateFile(target, created, failure) {
  try {
    assertNoReparseAncestors(target, 'failed private file');
    const current = fs.lstatSync(target, { bigint: true });
    if (!created || created.ino === 0n || !current.isFile() || current.isSymbolicLink()
        || current.nlink !== 1n || current.dev !== created.dev || current.ino !== created.ino) {
      fail('cleanup_identity_changed', 'failed private file was replaced or linked; inspect it before cleanup');
    }
    fs.unlinkSync(target);
  } catch (error) {
    if (error.code === 'ENOENT') return;
    // Keep the original write/ACL failure; cleanup failure is separate evidence.
    failure.cleanup = { path: target, status: 'manual_recovery_required',
      errorCategory: error.category ?? error.code ?? 'cleanup_failed',
      message: redactDiagnostic(error.message) };
  }
}

async function writePrivateFileExclusive(target, content, identity, tools) {
  const descriptor = fs.openSync(target, 'wx', 0o600);
  let created;
  try {
    // Retain the handle through hardening and cleanup so its file ID cannot be
    // recycled for an unrelated replacement at the same path.
    created = fs.fstatSync(descriptor, { bigint: true });
    fs.writeFileSync(descriptor, content);
    fs.fsyncSync(descriptor);
    await setPrivateAcl(target, false, identity, tools);
    assertRegularPath(target, 'file');
  } catch (error) {
    cleanupCreatedPrivateFile(target, created, error);
    throw error;
  } finally {
    fs.closeSync(descriptor);
  }
}

function sha256File(target) {
  const hash = crypto.createHash('sha256');
  const descriptor = fs.openSync(target, 'r');
  const buffer = Buffer.allocUnsafe(1024 * 1024);
  try {
    for (;;) {
      const count = fs.readSync(descriptor, buffer, 0, buffer.length, null);
      if (count === 0) break;
      hash.update(buffer.subarray(0, count));
    }
  } finally {
    fs.closeSync(descriptor);
  }
  return hash.digest('hex');
}

function sha256Bytes(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function assertFileDigest(target, expected, label) {
  if (sha256File(target) !== expected) fail('digest_mismatch', `${label} SHA-256 does not match the approved digest`);
}

function assertFileSize(target, expected, label) {
  const stat = assertRegularPath(target, 'file', 'asset_size_mismatch');
  if (stat.size !== expected) fail('asset_size_mismatch', `${label} size does not match the approved artifact`);
}

async function readBoundedBody(response, maximumBytes, category, message) {
  const declared = response.headers.get('content-length');
  if (declared !== null && (!/^[0-9]+$/.test(declared) || Number(declared) > maximumBytes)) {
    if (response.body) await response.body.cancel().catch(() => {});
    fail(category, message);
  }
  if (!response.body) fail(category, 'HTTP response body is unavailable');
  const chunks = [];
  let total = 0;
  for await (const chunk of response.body) {
    total += chunk.length;
    if (total > maximumBytes) {
      await response.body.cancel().catch(() => {});
      fail(category, message);
    }
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks, total);
}

async function fetchWithTimeout(url, options, timeoutMilliseconds) {
  return fetch(url, {
    ...options,
    signal: AbortSignal.timeout(timeoutMilliseconds),
    redirect: 'manual',
  });
}

function assertApiDestination(value) {
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    fail('invalid_api_destination', 'GitHub API URL is invalid');
  }
  if (parsed.protocol !== 'https:' || parsed.hostname !== 'api.github.com' || parsed.port
      || parsed.username || parsed.password || parsed.hash) {
    fail('invalid_api_destination', 'GitHub API URL is outside the reviewed origin');
  }
  return parsed;
}

async function invokeApiJson(url) {
  const parsed = assertApiDestination(url);
  const response = await fetchWithTimeout(parsed, {
    headers: {
      Accept: 'application/vnd.github+json',
      'User-Agent': 'jishudb-agent-install/0.2',
      'X-GitHub-Api-Version': API_VERSION,
    },
  }, API_TIMEOUT_MILLISECONDS);
  if (response.status !== 200) {
    const delay = rateLimitDelay(response);
    if (response.body) await response.body.cancel().catch(() => {});
    if (delay !== null) {
      const error = new InstallError('github_rate_limited', 'GitHub API rate limit requires waiting');
      error.retryAfterSeconds = delay;
      throw error;
    }
    fail('github_api_failed', `GitHub API returned HTTP ${response.status}`);
  }
  const body = await readBoundedBody(response, MAXIMUM_JSON_BYTES, 'github_api_failed', 'GitHub API response exceeds the supported size');
  try {
    return JSON.parse(body.toString('utf8'));
  } catch {
    fail('github_api_failed', 'GitHub API returned invalid JSON');
  }
}

async function getReleasePages(fetchPage = async (page) => invokeApiJson(
  `${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases?per_page=100&page=${page}`,
)) {
  const releases = [];
  for (let page = 1; page <= MAXIMUM_RELEASE_PAGES; page += 1) {
    const items = await fetchPage(page);
    if (!Array.isArray(items)) fail('github_api_failed', 'GitHub releases response must be an array');
    releases.push(...items);
    if (items.length < 100) return releases;
  }
  fail('pagination_bound', `release selection exceeded ${MAXIMUM_RELEASE_PAGES} pages`);
}

function getApiDigest(asset, label) {
  if (!isRecord(asset) || asset.state !== 'uploaded' || !Number.isSafeInteger(asset.size) || asset.size <= 0) {
    fail('invalid_release_asset', `${label} is not a complete uploaded asset`);
  }
  requirePattern(asset.digest, /^sha256:[0-9a-f]{64}$/, `${label} digest`);
  return asset.digest.slice(7);
}

function getExactAsset(release, name, label) {
  const matches = Array.isArray(release.assets) ? release.assets.filter((asset) => asset?.name === name) : [];
  if (matches.length !== 1) fail('invalid_release_asset', `${label} must exist exactly once`);
  const asset = matches[0];
  getApiDigest(asset, label);
  requireSafeInteger(asset.id, `${label} ID`, { positive: true });
  if (asset.url !== `${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/assets/${asset.id}`) {
    fail('invalid_release_asset', `${label} API URL is not canonical`);
  }
  return asset;
}

function parseSemver(value) {
  if (typeof value !== 'string' || value.length > 64) return null;
  const match = SEMVER_PATTERN.exec(value);
  if (!match || match.slice(1).some((part) => part.length > 10)) return null;
  const parts = match.slice(1).map((part) => BigInt(part));
  return parts.some((part) => part > 2147483647n) ? null : parts;
}

function compareSemver(left, right) {
  for (let index = 0; index < 3; index += 1) {
    if (left[index] > right[index]) return -1;
    if (left[index] < right[index]) return 1;
  }
  return 0;
}

async function selectEligibleRelease(fetchPage) {
  const eligible = [];
  for (const release of await getReleasePages(fetchPage)) {
    if (!isRecord(release) || release.draft || release.prerelease || release.immutable !== true) continue;
    const tag = typeof release.tag_name === 'string' ? release.tag_name : '';
    const version = tag.startsWith('v') ? tag.slice(1) : '';
    const versionParts = parseSemver(version);
    if (!versionParts) continue;
    const installerName = `JishuDB-Windows-x64-${version}-Setup.exe`;
    try {
      eligible.push({
        versionParts,
        version,
        release,
        installer: getExactAsset(release, installerName, 'installer'),
        checksum: getExactAsset(release, `${installerName}.sha256`, 'checksum'),
        candidate: getExactAsset(release, `${installerName}.candidate.json`, 'candidate'),
      });
    } catch (error) {
      if (!(error instanceof InstallError)) throw error;
    }
  }
  if (eligible.length === 0) fail('no_eligible_immutable_release', 'no eligible immutable stable Windows release is available');
  eligible.sort((left, right) => compareSemver(left.versionParts, right.versionParts));
  return eligible[0];
}

function isAllowedAssetRedirect(source, target) {
  return source.protocol === 'https:'
    && source.hostname === 'api.github.com'
    && source.port === ''
    && /^\/repos\/x-aijishu\/jishudb-desktop-releases\/releases\/assets\/[1-9][0-9]*$/.test(source.pathname)
    && target.protocol === 'https:'
    && target.hostname === ASSET_REDIRECT_HOST
    && target.port === ''
    && target.username === ''
    && target.password === ''
    && target.hash === ''
    && target.pathname.startsWith(ASSET_REDIRECT_PREFIX);
}

async function saveAsset(
  url,
  destination,
  maximumBytes = MAXIMUM_ASSET_BYTES,
  timeoutMilliseconds = SMALL_ASSET_TIMEOUT_MILLISECONDS,
  sourceInfo = null,
) {
  const source = sourceInfo?.kind === 'cnb' ? new URL(url) : assertApiDestination(url);
  if (sourceInfo?.kind === 'cnb' && !Object.values(mirrorTransport(sourceInfo).assets).includes(source.href)) fail('blocked_origin', 'asset URL differs from the authenticated catalog');
  const fetchAsset = async (target, options) => {
    try { return await fetchWithTimeout(target, options, timeoutMilliseconds); }
    catch (error) {
      if (!sourceInfo) throw error;
      throw new InstallError('asset_network_failed', 'CNB metadata request failed; inspect the network diagnostic', { cause: error });
    }
  };
  let response = await fetchAsset(source, {
    headers: sourceInfo?.kind === 'cnb' ? {} : {
      Accept: 'application/octet-stream',
      'User-Agent': 'jishudb-agent-install/0.2',
      'X-GitHub-Api-Version': API_VERSION,
    },
  });
  if (response.status === 302) {
    const location = response.headers.get('location');
    if (!location) fail('invalid_asset_redirect', 'asset redirect has no Location');
    const target = new URL(location, source);
    if (!allowedSourceRedirect(sourceInfo, source, target)) fail('invalid_asset_redirect', 'asset redirect is outside the approved transport policy');
    if (response.body) await response.body.cancel().catch(() => {});
    response = await fetchAsset(target, {});
  }
  if (response.status !== 200) {
    if (response.body) await response.body.cancel().catch(() => {});
    fail('asset_download_failed', `asset request returned HTTP ${response.status}`);
  }
  const declared = response.headers.get('content-length');
  if (declared !== null && (!/^[0-9]+$/.test(declared) || Number(declared) > maximumBytes)) {
    if (response.body) await response.body.cancel().catch(() => {});
    fail('asset_download_failed', 'asset exceeds the supported size');
  }
  if (!response.body) fail('asset_download_failed', 'asset response body is unavailable');

  const descriptor = fs.openSync(destination, 'wx', 0o600);
  let total = 0;
  try {
    for await (const chunk of response.body) {
      total += chunk.length;
      if (total > maximumBytes) fail('asset_download_failed', 'asset exceeds the supported size');
      let offset = 0;
      while (offset < chunk.length) offset += fs.writeSync(descriptor, chunk, offset, chunk.length - offset);
    }
    fs.fsyncSync(descriptor);
  } catch (error) {
    if (!sourceInfo || error instanceof InstallError || (error.code && /^(EACCES|EPERM|ENOSPC|EIO|ENOENT|EEXIST|EBUSY)$/.test(error.code))) throw error;
    throw new InstallError('asset_transfer_interrupted', 'CNB metadata transfer was interrupted; inspect the network diagnostic', { cause: error });
  } finally {
    fs.closeSync(descriptor);
  }
}

function compareVersion(left, right) {
  const normalize = (value) => value.split('.').map((part) => Number(part));
  const a = normalize(left);
  const b = normalize(right);
  for (let index = 0; index < Math.max(a.length, b.length); index += 1) {
    const difference = (a[index] ?? 0) - (b[index] ?? 0);
    if (difference !== 0) return difference;
  }
  return 0;
}

function validateWindowsCandidate(candidate, selected, windowsRelease = os.release()) {
  requireExactProperties(candidate, [
    'artifact', 'authorization', 'bundleIdentifier', 'distribution', 'minimumSystemVersion',
    'product', 'productName', 'publication', 'revision', 'runtimeLock', 'schemaVersion',
    'source', 'target', 'version',
    ...(Object.hasOwn(candidate, 'agentBackgroundLaunch') ? ['agentBackgroundLaunch'] : []),
  ], 'candidate');
  if (Object.hasOwn(candidate, 'agentBackgroundLaunch') && candidate.agentBackgroundLaunch !== 1) fail('invalid_candidate', 'unsupported Agent launch contract');
  requireExactProperties(candidate.runtimeLock, ['path', 'sha256'], 'candidate.runtimeLock');
  requireExactProperties(candidate.artifact, ['name', 'sha256', 'size'], 'candidate.artifact');
  requireExactProperties(candidate.distribution, ['authenticode', 'installationScope', 'mode', 'publisherIdentity', 'smartScreenAssessment'], 'candidate.distribution');
  requireExactProperties(candidate.authorization, ['mode', 'publisherIdentity'], 'candidate.authorization');
  requireExactProperties(candidate.publication, ['requested'], 'candidate.publication');
  requireExactProperties(candidate.source, ['repository', 'runId', 'runAttempt'], 'candidate.source');
  if (candidate.schemaVersion !== 1 || candidate.product !== 'jishudb-desktop'
      || candidate.productName !== 'JishuDB' || candidate.bundleIdentifier !== 'com.aijishu.jishudb'
      || candidate.target !== 'windows-x64' || candidate.version !== selected.version) {
    fail('invalid_candidate', 'candidate product, target, or version is invalid');
  }
  requirePattern(candidate.revision, REVISION_PATTERN, 'candidate revision');
  requirePattern(candidate.minimumSystemVersion, /^10\.0\.[0-9]+$/, 'candidate minimum Windows version');
  if (!/^[0-9]+\.[0-9]+\.[0-9]+(?:\.[0-9]+)?$/.test(windowsRelease)) {
    fail('unsupported_platform', 'current Windows version is invalid');
  }
  requirePattern(String(candidate.source.runId), /^[1-9][0-9]*$/, 'candidate source run ID');
  requireSafeInteger(candidate.source.runAttempt, 'candidate source run attempt', { positive: true });
  if (compareVersion(windowsRelease, candidate.minimumSystemVersion) < 0 || Number(windowsRelease.split('.')[2] ?? 0) < 22000) {
    fail('unsupported_platform', 'automatic installation requires a supported Windows 11 build');
  }
  if (candidate.source.repository !== SOURCE_REPOSITORY
      || candidate.artifact.name !== selected.installer.name
      || candidate.artifact.sha256 !== getApiDigest(selected.installer, 'installer')
      || candidate.artifact.size !== selected.installer.size
      || candidate.runtimeLock.path !== 'packaging/windows/desktop-runtime-lock.json'
      || !SHA256_PATTERN.test(candidate.runtimeLock.sha256)
      || candidate.distribution.mode !== 'per-user-nsis-v1'
      || candidate.distribution.publisherIdentity !== 'none'
      || candidate.distribution.authenticode !== 'not-signed'
      || candidate.distribution.smartScreenAssessment !== 'unknown-publisher-manual-approval-required'
      || candidate.distribution.installationScope !== 'current-user'
      || candidate.authorization.mode !== 'windows-fresh-install-v1'
      || candidate.authorization.publisherIdentity !== 'none'
      || candidate.publication.requested !== true) {
    fail('invalid_candidate', 'candidate source, artifact, distribution, or authorization is invalid');
  }
}

function newAssetPlan(asset, role) {
  return {
    role,
    id: requireSafeInteger(asset.id, `${role} ID`, { positive: true }),
    name: requireSafeText(asset.name, `${role} name`, 255),
    size: requireSafeInteger(asset.size, `${role} size`, { positive: true }),
    url: requireSafeText(asset.url, `${role} URL`, 2048),
    sha256: getApiDigest(asset, role),
  };
}

function assertPlanShape(plan) {
  requireExactProperties(plan, ['schema', 'createdAt', 'expiresAt', 'operation', 'platform', 'userSid', 'release', 'assets', 'installation', 'connection', 'publisher', ...([BACKGROUND_PLAN_SCHEMA, REINSTALL_PLAN_SCHEMA].includes(plan.schema) ? ['launchMode'] : []), ...(plan.schema === REINSTALL_PLAN_SCHEMA ? ['retainedData'] : [])], 'plan');
  if (plan.schema === REINSTALL_PLAN_SCHEMA) requireExactProperties(plan.retainedData, ['instanceId', 'bootstrapSha256', 'markerSha256'], 'plan.retainedData');
  requireExactProperties(plan.release, ['repository', 'id', 'tag', 'version', 'targetCommitish', 'sourceRepository', 'sourceRevision'], 'plan.release');
  requireExactProperties(plan.assets, ['installer', 'checksum', 'candidate'], 'plan.assets');
  requireExactProperties(plan.installation, ['applicationRoot', 'dataRoot', 'bootstrapPath', 'desktopShortcut', 'dataOwnershipAcknowledged'], 'plan.installation');
  requireExactProperties(plan.connection, ['client', 'configTarget', 'name', 'url', 'profile'], 'plan.connection');
  requireExactProperties(plan.publisher, ['identity', 'authenticode', 'smartScreen'], 'plan.publisher');
  for (const role of ['installer', 'checksum', 'candidate']) {
    requireExactProperties(plan.assets[role], ['role', 'id', 'name', 'size', 'url', 'sha256'], `plan.assets.${role}`);
  }
}

async function assertReleaseMatchesPlan(plan) {
  const release = await invokeApiJson(`${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/${plan.release.id}`);
  validateReleaseMatchesPlan(release, plan);
  return release;
}

function validateReleaseMatchesPlan(release, plan) {
  if (!isRecord(release) || release.id !== plan.release.id || release.immutable !== true || release.draft || release.prerelease
      || release.tag_name !== plan.release.tag || String(release.target_commitish) !== plan.release.targetCommitish) {
    fail('release_drift', 'release identity or immutable state changed');
  }
  for (const role of ['installer', 'checksum', 'candidate']) {
    const expected = plan.assets[role];
    const actual = getExactAsset(release, expected.name, role);
    if (actual.id !== expected.id || actual.size !== expected.size || actual.url !== expected.url
        || getApiDigest(actual, role) !== expected.sha256) {
      fail('release_drift', `${role} asset changed after approval`);
    }
  }
}

function isTcpPortAvailable(port) {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.unref();
    server.once('error', (error) => {
      if (error.code === 'EADDRINUSE' || error.code === 'EACCES') resolve(false);
      else reject(error);
    });
    server.listen({ host: '127.0.0.1', port, exclusive: true }, () => {
      server.close((error) => error ? reject(error) : resolve(true));
    });
  });
}

async function getFreeDesktopMcpUrl() {
  for (const port of approvedDesktopMcpPorts()) {
    if (await isTcpPortAvailable(port)) return `http://127.0.0.1:${port}/mcp`;
  }
  fail('endpoint_unavailable', 'no free port exists in the bounded Desktop endpoint set');
}

/** Read retained endpoint preferences without treating them as an installation. */
function readSavedDesktopEndpoint(bootstrapPath) {
  const endpointPath = path.join(path.dirname(bootstrapPath), ENDPOINT_CONFIG_FILENAME);
  try { fs.lstatSync(endpointPath); }
  catch (error) {
    if (error.code === 'ENOENT') return null;
    throw new InstallError('endpoint_inspection_failed', 'could not inspect the saved Desktop endpoint; check file access before installing', { cause: error });
  }
  // AI-assisted security boundary: retained preferences must be bounded regular
  // files, not links or alternative paths. Reuse never grants install authority.
  const stat = assertRegularPath(endpointPath, 'file', 'invalid_endpoint');
  if (stat.nlink !== 1 || stat.size <= 0 || stat.size > MAXIMUM_ENDPOINT_CONFIG_BYTES) {
    fail('invalid_endpoint', 'saved Desktop endpoint must be a single regular file no larger than 4096 bytes');
  }
  let contents;
  try { contents = fs.readFileSync(endpointPath, 'utf8'); }
  catch (error) {
    throw new InstallError('endpoint_inspection_failed', 'could not read the saved Desktop endpoint; check file access before installing', { cause: error });
  }
  let saved;
  try { saved = JSON.parse(contents); }
  catch (error) {
    throw new InstallError('invalid_endpoint', 'saved Desktop endpoint is not valid JSON; inspect it before installing', { cause: error });
  }
  if (!isRecord(saved) || Object.keys(saved).sort().join(',') !== 'localPort,schemaVersion'
      || saved.schemaVersion !== ENDPOINT_CONFIG_SCHEMA || !Number.isInteger(saved.localPort)
      || !approvedDesktopMcpPorts().includes(saved.localPort)) {
    fail('invalid_endpoint', 'saved Desktop endpoint has an unsupported schema or port; inspect it before installing');
  }
  return { endpointPath, mcpUrl: `http://127.0.0.1:${saved.localPort}/mcp` };
}

/** Choose an approved endpoint while preserving valid preferences after uninstall. */
async function selectInstallationEndpoint(bootstrapPath, { preserveData = false } = {}) {
  const saved = readSavedDesktopEndpoint(bootstrapPath);
  // Desktop retains the legacy port for an existing data directory when no
  // endpoint preference exists; the interactive installer must agree with it.
  if (!saved) return preserveData ? `http://127.0.0.1:${PREFERRED_MCP_PORT}/mcp` : getFreeDesktopMcpUrl();
  return saved.mcpUrl;
}

function readInstallationMetadata(filename) {
  const stat = assertRegularPath(filename, 'file', 'invalid_data_location');
  if (stat.nlink !== 1 || stat.size <= 0 || stat.size > MAXIMUM_ENDPOINT_CONFIG_BYTES) {
    fail('invalid_data_location', 'data-location metadata must be a small regular, non-linked file');
  }
  let bytes;
  try { bytes = fs.readFileSync(filename); }
  catch (error) { throw new InstallError('installation_inspection_failed', 'could not read retained data-location metadata', { cause: error }); }
  try { return { value: JSON.parse(bytes.toString('utf8')), sha256: sha256Bytes(bytes) }; }
  catch (error) { throw new InstallError('invalid_data_location', 'retained data-location metadata is not valid JSON', { cause: error }); }
}

/** Resolve the existing data owner; never infer a database from an endpoint file. */
function readRetainedInstallation(installation) {
  try { fs.lstatSync(installation.bootstrapPath); }
  catch (error) {
    if (error.code === 'ENOENT') return null;
    throw new InstallError('installation_inspection_failed', 'could not inspect the retained data location', { cause: error });
  }
  const bootstrap = readInstallationMetadata(installation.bootstrapPath);
  const value = bootstrap.value;
  if (!isRecord(value) || Object.keys(value).sort().join(',') !== 'dataRoot,instanceId,product,schemaVersion'
      || value.schemaVersion !== 1 || value.product !== 'JishuDB' || !/^[0-9a-f]{32}$/.test(value.instanceId)
      || typeof value.dataRoot !== 'string' || !path.isAbsolute(value.dataRoot)) {
    fail('invalid_data_location', 'retained data location has an unsupported identity or path');
  }
  const dataRoot = assertNoReparseAncestors(value.dataRoot, 'retained data directory');
  if (dataRoot.toLowerCase() !== value.dataRoot.toLowerCase()) fail('invalid_data_location', 'retained data directory is not canonical');
  const contains = (parent, child) => {
    const relative = path.relative(parent, child);
    return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
  };
  if (contains(installation.applicationRoot, dataRoot) || contains(dataRoot, installation.applicationRoot)) {
    fail('invalid_data_location', 'retained data and application directories must not overlap');
  }
  assertRegularPath(dataRoot, 'directory', 'invalid_data_location');
  const marker = readInstallationMetadata(path.join(dataRoot, '.jishudb-data-root'));
  if (!isRecord(marker.value) || Object.keys(marker.value).sort().join(',') !== 'instanceId,product,schemaVersion'
      || marker.value.schemaVersion !== 1 || marker.value.product !== 'JishuDB' || marker.value.instanceId !== value.instanceId) {
    fail('invalid_data_location', 'retained data directory ownership does not match data-location.json');
  }
  return { dataRoot, retainedData: { instanceId: value.instanceId, bootstrapSha256: bootstrap.sha256, markerSha256: marker.sha256 } };
}

/** Admit only absent applications or bounded, recognized uninstall cache residue. */
function assertReinstallableApplication(applicationRoot) {
  assertNoReparseAncestors(applicationRoot, 'application directory');
  try { fs.lstatSync(applicationRoot); }
  catch (error) {
    if (error.code !== 'ENOENT') throw new InstallError('installation_inspection_failed', 'could not inspect the application directory', { cause: error });
    return;
  }
  assertRegularPath(applicationRoot, 'directory', 'application_state_requires_review');
  const executableMarkers = ['JishuDB.exe', 'resources/app.asar', 'resources/runtime/jishudb.exe'];
  for (const relative of executableMarkers) {
    try { fs.lstatSync(path.join(applicationRoot, relative)); }
    catch (error) {
      if (error.code === 'ENOENT') continue;
      throw new InstallError('installation_inspection_failed', 'could not inspect installed application files', { cause: error });
    }
    fail('existing_installation', 'application files already exist; verify and start the existing Desktop instead of reinstalling');
  }
  // AI-assisted: allow the observed Python bytecode left by uninstall, without
  // deleting it or admitting arbitrary user files, links or unbounded trees.
  const pending = [''];
  let entries = 0, bytes = 0;
  while (pending.length) {
    const relative = pending.pop();
    for (const entry of fs.readdirSync(path.join(applicationRoot, relative), { withFileTypes: true })) {
      if (++entries > 4096) fail('application_state_requires_review', 'application residue exceeds the inspection limit');
      const child = path.posix.join(relative, entry.name);
      const target = path.join(applicationRoot, child);
      const stat = assertRegularPath(target, entry.isDirectory() ? 'directory' : 'file', 'application_state_requires_review');
      if (entry.isDirectory()) {
        if (!['resources', 'resources/runtime', 'resources/runtime/python'].includes(child)
            && !child.startsWith('resources/runtime/python/')) {
          fail('application_state_requires_review', 'application directory contains unrecognized content; preserve it for review');
        }
        pending.push(child);
      } else {
        bytes += stat.size;
        if (stat.nlink !== 1 || bytes > 64 * 1024 * 1024
            || !/^resources\/runtime\/python\/(?:[^/]+\/)*__pycache__\/[^/]+\.pyc$/.test(child)) {
          fail('application_state_requires_review', 'application directory contains unrecognized content; preserve it for review');
        }
      }
    }
  }
}

function assertReinstallationDestinations(plan) {
  assertReinstallableApplication(plan.installation.applicationRoot);
  const current = readRetainedInstallation(plan.installation);
  if (!current || current.dataRoot !== plan.installation.dataRoot
      || Object.keys(plan.retainedData).some(key => current.retainedData[key] !== plan.retainedData[key])) {
    fail('installation_state_changed', 'retained data location or ownership changed after approval; inspect it and create a new plan');
  }
  const endpoint = readSavedDesktopEndpoint(plan.installation.bootstrapPath);
  const actualURL = endpoint?.mcpUrl ?? `http://127.0.0.1:${PREFERRED_MCP_PORT}/mcp`;
  if (plan.connection && actualURL !== plan.connection.url) {
    fail('endpoint_conflict', 'retained Desktop endpoint changed after approval; create a new plan without overwriting configuration');
  }
}

function assertDesktopEndpointCompatible(bootstrapPath, mcpUrl) {
  if (!isDesktopMcpUrl(mcpUrl)) fail('invalid_endpoint', 'approved Desktop MCP endpoint is invalid');
  const saved = readSavedDesktopEndpoint(bootstrapPath);
  if (saved && saved.mcpUrl !== mcpUrl) {
    fail('endpoint_conflict', 'saved Desktop endpoint differs from the approved plan; create a new plan without deleting existing data');
  }
  return saved;
}

function assertFreshInstallationDestinations(installation) {
  for (const target of [installation.applicationRoot, installation.dataRoot, installation.bootstrapPath]) {
    try { fs.lstatSync(target); }
    catch (error) {
      if (error.code === 'ENOENT') continue;
      throw new InstallError('installation_inspection_failed', 'could not inspect an installation destination; check file access before installing', { cause: error });
    }
    if (target === installation.applicationRoot) fail('existing_installation', 'application files already exist; verify and start the existing Desktop');
    fail('retained_data_requires_review', 'data or data-location state exists; preserve it and create a reviewed data-preserving reinstall plan');
  }
}

function assertInstallationDestinations(plan) {
  if (plan.schema === REINSTALL_PLAN_SCHEMA) assertReinstallationDestinations(plan);
  else assertFreshInstallationDestinations(plan.installation);
}

/** Dispatch a verified local target through the existing interactive desktop. */
async function dispatchDesktopTarget(target, context) {
  // AI-assisted: detached children still inherit a host's Windows job. Explorer
  // delegates to the existing desktop instead of owning the long-lived app.
  const broker = childProcess.spawn(context.tools.explorer, [target], {
    env: sanitizedChildEnvironment(), stdio: 'ignore', windowsHide: false, shell: false,
  });
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      broker.kill();
      reject(new Error('desktop shell handoff timed out; inspect the launch before retrying'));
    }, 30000);
    broker.once('error', error => { clearTimeout(timer); reject(error); });
    broker.once('close', (code, signal) => {
      clearTimeout(timer);
      // Explorer can return 1 after delegation. Neither code proves app readiness.
      if (!signal && (code === 0 || code === 1)) resolve();
      else reject(new Error(`desktop shell exited with ${signal ?? code}`));
    });
  });
}

/** Create and read back a private shortcut; paths travel as data, never shell code. */
async function createDesktopShortcut(shortcutPath, application, background, context) {
  const payload = Buffer.from(JSON.stringify({
    shortcutPath, application, workingDirectory: path.dirname(application),
    arguments: background ? '--jishudb-agent-background' : '',
  }), 'utf8').toString('base64');
  // AI-assisted: use only the verified system PowerShell and WSH COM interface.
  // No execution-policy override, elevation, scheduled task, or host-policy change.
  const script = `$ErrorActionPreference='Stop'
$p=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('${payload}')) | ConvertFrom-Json
if(Test-Path -LiteralPath $p.shortcutPath){throw 'Launch shortcut already exists'}
$shell=New-Object -ComObject WScript.Shell
$link=$shell.CreateShortcut($p.shortcutPath)
$link.TargetPath=$p.application
$link.Arguments=$p.arguments
$link.WorkingDirectory=$p.workingDirectory
$link.Save()
$saved=$shell.CreateShortcut($p.shortcutPath)
if($saved.TargetPath -ine $p.application -or $saved.Arguments -cne $p.arguments -or $saved.WorkingDirectory -ine $p.workingDirectory){throw 'Launch shortcut readback mismatch'}
`;
  await runNative(context.tools.powershell, [
    '-NoProfile', '-NonInteractive', '-EncodedCommand', Buffer.from(script, 'utf16le').toString('base64'),
  ], { env: sanitizedChildEnvironment(), label: 'create Desktop launch shortcut', category: 'desktop_shortcut_failed' });
  const stat = assertRegularPath(shortcutPath, 'file', 'desktop_shortcut_failed');
  if (stat.nlink !== 1 || stat.size === 0 || stat.size > 64 * 1024) fail('desktop_shortcut_failed', 'invalid Desktop launch shortcut');
  await setPrivateAcl(shortcutPath, false, context.identity, context.tools);
}

/** Preserve the approved presentation mode while handing app lifetime to Explorer. */
async function launchInstalledDesktop(plan, loaded, context) {
  const application = assertNoReparseAncestors(path.join(plan.installation.applicationRoot, 'JishuDB.exe'), 'Desktop application');
  assertRegularPath(application, 'file', 'installed_receipt_invalid');
  const launchRoot = path.join(loaded.transactionRoot, `desktop-launch-${crypto.randomUUID()}`);
  await createPrivateDirectory(launchRoot, context.identity, context.tools);
  const shortcutPath = path.join(launchRoot, 'JishuDB.lnk');
  try {
    await createDesktopShortcut(shortcutPath, application, plan.launchMode === 'agent-background', context);
    await dispatchDesktopTarget(shortcutPath, context);
  } catch (cause) {
    throw new InstallError('desktop_launch_failed', 'Desktop is installed but its shell launch was not confirmed; inspect the launch before retrying, do not reinstall', { cause });
  }
  // Retain the private link for asynchronous shell consumption and diagnosis.
  // Dispatch is not health proof; the caller checks readiness in a new host call.
  return { launchStatus: 'requested', launchMethod: 'desktop-shell', shortcutPath };
}

/** Hand retained data to the existing interactive installer, never its fresh-only Agent entrypoint. */
async function launchInteractiveReinstallation(installerPath, plan, loaded, context) {
  const receiptPath = path.join(loaded.transactionRoot, 'interactive-reinstall-started.json');
  // AI-assisted: a private, exclusive receipt prevents repeated execute from
  // launching another installer. The exact approved data identity is rechecked
  // by the caller; the native installer retains its own ownership validation.
  await writePrivateFileExclusive(receiptPath, `${JSON.stringify({
    schemaVersion: 1, planSha256: loaded.approvalSha256, version: plan.release.version,
    dataRoot: plan.installation.dataRoot, instanceId: plan.retainedData.instanceId,
    status: 'launch_requested',
  }, null, 2)}\n`, context.identity, context.tools);
  try {
    await dispatchDesktopTarget(installerPath, context);
  } catch (error) {
    throw new InstallError('installer_launch_failed', 'could not start the verified reinstall wizard; inspect the launch attempt before retrying', { cause: error });
  }
  return {
    status: 'user_action_required', operation: plan.operation, version: plan.release.version,
    applicationRoot: plan.installation.applicationRoot, dataRoot: plan.installation.dataRoot,
    installerPath, launchStatus: 'requested',
    mcpUrl: plan.connection.url, next: 'complete_interactive_reinstall_and_verify_existing_data',
  };
}

function removeFileQuietly(target) {
  if (!target) return;
  try {
    fs.rmSync(target, { force: true });
  } catch {
    // Best-effort transaction cleanup.
  }
}

function removeDirectoryQuietly(target) {
  if (!target) return;
  try {
    fs.rmSync(target, { force: true, recursive: true });
  } catch {
    // Best-effort transaction cleanup.
  }
}

async function runCheck(context) {
  assertWindowsX64();
  const probeRoot = path.join(context.tempRoot, `JishuDBAgentCheck-${crypto.randomUUID().replaceAll('-', '')}`);
  try {
    await createPrivateDirectory(probeRoot, context.identity, context.tools);
    const probeFile = path.join(probeRoot, 'acl-probe.json');
    await writePrivateFileExclusive(probeFile, '{}\n', context.identity, context.tools);
    const releaseProbe = await getReleasePages(async (page) => [{ page }]);
    if (releaseProbe.length !== 1 || releaseProbe[0].page !== 1) {
      fail('unsupported_node_runtime', 'Node.js release-list behavior is incompatible');
    }
    return { status: 'compatible', host: 'node', version: process.version };
  } finally {
    removeDirectoryQuietly(probeRoot);
  }
}

async function runPlan(args, context) {
  assertReleaseSourceAvailable(args.releaseSource);
  assertWindowsX64();
  if (!args.client.trim() || !args.configTarget.trim()) fail('invalid_arguments', 'Client and ConfigTarget are required in plan mode');
  requireSafeText(args.client.trim(), 'Client', 512);
  requireSafeText(args.configTarget, 'ConfigTarget');
  let configTarget;
  try {
    configTarget = assertNoReparseAncestors(args.configTarget, 'ConfigTarget');
  } catch (error) {
    if (error instanceof InstallError) fail('invalid_arguments', error.publicMessage);
    throw error;
  }
  if (!CONNECTION_NAME_PATTERN.test(args.connectionName)) fail('invalid_arguments', 'ConnectionName must be filesystem-safe');

  const localAppData = context.localAppData;
  const applicationRoot = path.join(localAppData, 'Programs', 'JishuDB');
  let dataRoot = path.join(localAppData, 'Programs', 'JishuDBData');
  const bootstrapPath = path.join(localAppData, 'JishuDB', 'data-location.json');
  // Planning and downloading do not authorize product writes. Inspection issues
  // are reported now and enforced before execute, without blocking downloads.
  const preflightWarnings = [];
  const inspect = async operation => {
    try { return await operation(); }
    catch (error) {
      if (!(error instanceof InstallError)) throw error;
      preflightWarnings.push({ errorCategory: error.category, message: error.publicMessage });
      return null;
    }
  };
  const retained = await inspect(() => readRetainedInstallation({ applicationRoot, dataRoot, bootstrapPath }));
  if (retained) dataRoot = retained.dataRoot;
  const mcpUrl = await inspect(() => selectInstallationEndpoint(bootstrapPath, { preserveData: !!retained })) ?? `http://127.0.0.1:${PREFERRED_MCP_PORT}/mcp`;

  const evidenceRoot = path.join(context.tempRoot, `JishuDBAgentEvidence-${crypto.randomUUID().replaceAll('-', '')}`);
  let targetPlanPath = '';
  let targetPlanParent = '';
  let planParentCreated = false;
  let planReady = false;
  try {
    await createPrivateDirectory(evidenceRoot, context.identity, context.tools);
    const { selected, source } = args.releaseSource === 'cnb' ? await discoverMirror(context) : { selected: await selectEligibleRelease(), source: null };
    const candidatePath = path.join(evidenceRoot, 'candidate.json');
    const checksumPath = path.join(evidenceRoot, 'checksum.txt');
    await saveAsset(sourceAssetURL(source, selected.candidate), candidatePath, MAXIMUM_JSON_BYTES, SMALL_ASSET_TIMEOUT_MILLISECONDS, source);
    await saveAsset(sourceAssetURL(source, selected.checksum), checksumPath, MAXIMUM_CHECKSUM_BYTES, SMALL_ASSET_TIMEOUT_MILLISECONDS, source);
    assertFileSize(candidatePath, selected.candidate.size, 'candidate');
    assertFileSize(checksumPath, selected.checksum.size, 'checksum');
    assertFileDigest(candidatePath, getApiDigest(selected.candidate, 'candidate'), 'candidate');
    assertFileDigest(checksumPath, getApiDigest(selected.checksum, 'checksum'), 'checksum');
    const candidate = JSON.parse(fs.readFileSync(candidatePath, 'utf8'));
    validateWindowsCandidate(candidate, selected);
    const expectedChecksum = `${getApiDigest(selected.installer, 'installer')}  ${selected.installer.name}\n`;
    if (fs.readFileSync(checksumPath, 'utf8').replaceAll('\r\n', '\n') !== expectedChecksum) {
      fail('invalid_checksum', 'adjacent checksum content is not exact');
    }

    const customPlanPath = args.planPath.trim() !== '';
    if (customPlanPath) {
      try {
        targetPlanPath = assertNoReparseAncestors(args.planPath, 'custom plan path');
      } catch (error) {
        if (error instanceof InstallError) fail('invalid_plan_path', error.publicMessage);
        throw error;
      }
      targetPlanParent = path.dirname(targetPlanPath);
    } else {
      targetPlanParent = path.join(context.tempRoot, `JishuDBAgentInstall-${crypto.randomUUID().replaceAll('-', '')}`);
      targetPlanPath = path.join(targetPlanParent, 'install-plan.json');
    }
    if (fs.existsSync(targetPlanPath)) fail('invalid_plan_path', 'plan output already exists');
    if (customPlanPath && fs.existsSync(targetPlanParent)) fail('invalid_plan_path', 'custom plan parent must be absent');
    if (!fs.existsSync(targetPlanParent)) {
      if (!fs.existsSync(path.dirname(targetPlanParent))) {
        fail('invalid_plan_path', 'custom plan parent must have an existing local parent directory');
      }
      planParentCreated = true;
      await createPrivateDirectory(targetPlanParent, context.identity, context.tools);
    }

    const now = new Date();
    const plan = {
      schema: retained ? REINSTALL_PLAN_SCHEMA : candidate.agentBackgroundLaunch === 1 ? BACKGROUND_PLAN_SCHEMA : PLAN_SCHEMA,
      ...(retained ? { launchMode: 'interactive-installer', retainedData: retained.retainedData }
        : candidate.agentBackgroundLaunch === 1 ? {launchMode: 'agent-background'} : {}),
      createdAt: now.toISOString(),
      expiresAt: new Date(Math.min(now.getTime() + PLAN_TTL_MILLISECONDS, source ? Date.parse(source.verified.payload.expiresAt) : Infinity)).toISOString(),
      operation: retained ? 'reinstall-preserve-data' : 'fresh-install',
      platform: 'windows-x64',
      userSid: context.identity.sid,
      release: {
        repository: RELEASE_REPOSITORY,
        id: requireSafeInteger(selected.release.id, 'release ID', { positive: true }),
        tag: selected.release.tag_name,
        version: selected.version,
        targetCommitish: requireSafeText(String(selected.release.target_commitish), 'target commitish', 512),
        sourceRepository: SOURCE_REPOSITORY,
        sourceRevision: candidate.revision,
      },
      assets: {
        installer: newAssetPlan(selected.installer, 'installer'),
        checksum: newAssetPlan(selected.checksum, 'checksum'),
        candidate: newAssetPlan(selected.candidate, 'candidate'),
      },
      installation: {
        applicationRoot,
        dataRoot,
        bootstrapPath,
        desktopShortcut: true,
        dataOwnershipAcknowledged: true,
      },
      connection: {
        client: requireSafeText(args.client.trim(), 'client', 512),
        configTarget,
        name: args.connectionName,
        url: mcpUrl,
        profile: 'default',
      },
      publisher: {
        identity: 'none',
        authenticode: 'not-signed',
        smartScreen: 'unknown-publisher-manual-approval-required',
      },
    };
    const planBytes = Buffer.from(`${JSON.stringify(plan, null, 2)}\n`, 'utf8');
    if (planBytes.length > MAXIMUM_PLAN_BYTES) fail('invalid_plan', 'plan exceeds the supported size');
    await assertSourceMatchesPlan(plan, source, context);
    validatePlan(plan, context);
    const approvalBytes = source ? Buffer.from(`${JSON.stringify(createMirrorEnvelope(planBytes, source), null, 2)}\n`) : planBytes;
    if (approvalBytes.length > MAXIMUM_APPROVAL_BYTES) fail('invalid_plan', 'approval envelope exceeds the size limit');
    const digest = sha256Bytes(approvalBytes);
    await writePrivateFileExclusive(targetPlanPath, approvalBytes, context.identity, context.tools);
    if (source) await advanceMirrorFloor(source, context);
    if (sha256File(targetPlanPath) !== digest) fail('plan_drift', 'plan changed before approval');
    planReady = true;
    return {
      status: 'plan_ready',
      authorization: { status: 'caller_verification_required', basis: 'existing_user_request_or_new_confirmation' },
      next: 'download_when_authorized',
      planPath: targetPlanPath,
      planSha256: digest,
      approval: {
        operation: plan.operation,
        preflightWarnings,
        releaseSource: source?.kind ?? 'github',
        ...(source ? { catalogSha256: sha256Bytes(source.catalogBytes), nativePlanSha256: sha256Bytes(planBytes), transport: mirrorTransport(source) } : {}),
        version: plan.release.version,
        expiresAt: plan.expiresAt,
        releaseId: plan.release.id,
        installer: plan.assets.installer.name,
        installerSha256: plan.assets.installer.sha256,
        applicationRoot,
        dataRoot,
        client: plan.connection.client,
        configTarget: plan.connection.configTarget,
        mcpUrl: plan.connection.url,
        profile: 'default',
        launchMode: plan.launchMode ?? 'foreground',
        publisher: 'unsigned',
        coveredMutations: ['download', retained ? 'interactive reinstall preserving the existing data directory' : 'per-user install', 'Desktop launch', 'non-secret client entry'],
        userPresence: ['SmartScreen or Unknown Publisher', ...(retained ? ['confirm the approved application directory and existing data directory in the installer'] : ['first administrator']), 'MCP secret entry', 'client trust'],
      },
    };
  } finally {
    removeDirectoryQuietly(evidenceRoot);
    if (!planReady) {
      removeFileQuietly(targetPlanPath);
      if (planParentCreated) removeDirectoryQuietly(targetPlanParent);
    }
  }
}

function parseStrictIso(value, label) {
  if (typeof value !== 'string') fail('invalid_plan', `${label} is invalid`);
  const parsed = new Date(value);
  if (!Number.isFinite(parsed.getTime()) || parsed.toISOString() !== value) fail('invalid_plan', `${label} is invalid`);
  return parsed;
}

function validatePlan(plan, context) {
  assertPlanShape(plan);
  const reinstall = plan.schema === REINSTALL_PLAN_SCHEMA;
  if (!([PLAN_SCHEMA, BACKGROUND_PLAN_SCHEMA, REINSTALL_PLAN_SCHEMA].includes(plan.schema)) || (plan.schema === BACKGROUND_PLAN_SCHEMA && plan.launchMode !== 'agent-background')
      || (reinstall && plan.launchMode !== 'interactive-installer') || plan.operation !== (reinstall ? 'reinstall-preserve-data' : 'fresh-install') || plan.platform !== 'windows-x64'
      || plan.userSid !== context.identity.sid || plan.release.repository !== RELEASE_REPOSITORY
      || plan.release.sourceRepository !== SOURCE_REPOSITORY || !isDesktopMcpUrl(plan.connection.url)
      || plan.connection.profile !== 'default' || plan.installation.dataOwnershipAcknowledged !== true) {
    fail('invalid_plan', 'plan is outside the reviewed automatic-install contract');
  }
  requirePattern(plan.userSid, SID_PATTERN, 'plan user SID');
  requirePattern(plan.release.version, SEMVER_PATTERN, 'plan version');
  requirePattern(plan.release.sourceRevision, REVISION_PATTERN, 'plan source revision');
  if (plan.release.tag !== `v${plan.release.version}`) fail('invalid_plan', 'plan release tag is invalid');
  requireSafeInteger(plan.release.id, 'plan release ID', { positive: true });
  requireSafeText(plan.release.targetCommitish, 'plan target commitish', 512);
  const installerName = `JishuDB-Windows-x64-${plan.release.version}-Setup.exe`;
  const expectedNames = {
    installer: installerName,
    checksum: `${installerName}.sha256`,
    candidate: `${installerName}.candidate.json`,
  };
  for (const role of ['installer', 'checksum', 'candidate']) {
    const asset = plan.assets[role];
    requireSafeInteger(asset.id, `plan ${role} ID`, { positive: true });
    requireSafeInteger(asset.size, `plan ${role} size`, { positive: true });
    const maximum = role === 'installer' ? MAXIMUM_ASSET_BYTES : role === 'candidate' ? MAXIMUM_JSON_BYTES : MAXIMUM_CHECKSUM_BYTES;
    if (asset.size > maximum) fail('invalid_plan', `plan ${role} exceeds its supported size`);
    requirePattern(asset.sha256, SHA256_PATTERN, `plan ${role} digest`);
    if (asset.role !== role || asset.name !== expectedNames[role]
        || asset.url !== `${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/assets/${asset.id}`) {
      fail('invalid_plan', `plan ${role} asset identity is invalid`);
    }
  }
  const localAppData = context.localAppData;
  if (plan.installation.applicationRoot !== path.join(localAppData, 'Programs', 'JishuDB')
      || (!reinstall && plan.installation.dataRoot !== path.join(localAppData, 'Programs', 'JishuDBData'))
      || plan.installation.bootstrapPath !== path.join(localAppData, 'JishuDB', 'data-location.json')
      || typeof plan.installation.desktopShortcut !== 'boolean') {
    fail('invalid_plan', 'plan installation destinations are invalid');
  }
  if (reinstall) {
    requirePattern(plan.retainedData.instanceId, /^[0-9a-f]{32}$/, 'retained instance ID');
    for (const key of ['bootstrapSha256', 'markerSha256']) requirePattern(plan.retainedData[key], SHA256_PATTERN, `retained ${key}`);
    const dataRoot = normalizeLocalWindowsPath(plan.installation.dataRoot, 'retained data root');
    if (dataRoot !== plan.installation.dataRoot) fail('invalid_plan', 'retained data root is not canonical');
  }
  if (!CONNECTION_NAME_PATTERN.test(plan.connection.name)
      || typeof plan.connection.client !== 'string' || !plan.connection.client.trim()
      || plan.connection.client.length > 4096 || /[\u0000-\u001f\u007f]/.test(plan.connection.client)
      || typeof plan.connection.configTarget !== 'string' || plan.connection.configTarget.length > 4096
      || /[\u0000-\u001f\u007f]/.test(plan.connection.configTarget)
      || !path.isAbsolute(plan.connection.configTarget)) {
    fail('invalid_plan', 'plan connection identity is invalid');
  }
  try {
    const normalizedConfigTarget = assertNoReparseAncestors(plan.connection.configTarget, 'plan ConfigTarget');
    if (normalizedConfigTarget.toLowerCase() !== plan.connection.configTarget.toLowerCase()) {
      fail('invalid_plan', 'plan ConfigTarget is not canonical');
    }
  } catch (error) {
    if (error instanceof InstallError && error.category !== 'invalid_plan') fail('invalid_plan', error.publicMessage);
    throw error;
  }
  if (plan.publisher.identity !== 'none' || plan.publisher.authenticode !== 'not-signed'
      || plan.publisher.smartScreen !== 'unknown-publisher-manual-approval-required') {
    fail('invalid_plan', 'plan publisher identity is invalid');
  }
  const createdAt = parseStrictIso(plan.createdAt, 'plan createdAt');
  const expiresAt = parseStrictIso(plan.expiresAt, 'plan expiresAt');
  const now = new Date();
  if (expiresAt <= createdAt || expiresAt - createdAt > PLAN_TTL_MILLISECONDS || now > expiresAt
      || createdAt.getTime() > now.getTime() + 5 * 60 * 1000) {
    fail('expired_plan', 'installation plan is expired or has an invalid lifetime');
  }
}

async function writeDesktopEndpointConfig(bootstrapPath, mcpUrl, context) {
  // Preserve the exact retained file when its validated port matches approval.
  if (assertDesktopEndpointCompatible(bootstrapPath, mcpUrl)) return;
  const stateRoot = path.dirname(bootstrapPath);
  if (!fs.existsSync(stateRoot)) await createPrivateDirectory(stateRoot, context.identity, context.tools);
  else assertRegularPath(stateRoot, 'directory', 'invalid_endpoint');
  const endpointPath = path.join(stateRoot, ENDPOINT_CONFIG_FILENAME);
  const port = Number(new URL(mcpUrl).port);
  await writePrivateFileExclusive(endpointPath, `${JSON.stringify({ localPort: port, schemaVersion: ENDPOINT_CONFIG_SCHEMA }, null, 2)}\n`, context.identity, context.tools);
}

async function loadApprovedPlan(args, context) {
  assertWindowsX64();
  if (!args.planPath.trim() || !args.planSha256.trim()) fail('invalid_arguments', 'PlanPath and PlanSha256 are required in download or execute mode');
  requirePattern(args.planSha256, SHA256_PATTERN, 'PlanSha256');
  let resolvedPlan;
  try {
    resolvedPlan = assertNoReparseAncestors(args.planPath, 'plan path');
  } catch (error) {
    if (error instanceof InstallError) fail('invalid_plan', error.publicMessage);
    throw error;
  }
  const transactionRoot = path.dirname(resolvedPlan);
  assertRegularPath(transactionRoot, 'directory');
  await assertPrivateAcl(transactionRoot, true, context.identity, context.tools);
  const planStat = assertRegularPath(resolvedPlan, 'file');
  if (planStat.size <= 0 || planStat.size > MAXIMUM_APPROVAL_BYTES) fail('invalid_plan', 'plan size is invalid');
  await assertPrivateAcl(resolvedPlan, false, context.identity, context.tools);
  const planBytes = fs.readFileSync(resolvedPlan);
  if (planBytes.length !== planStat.size || sha256Bytes(planBytes) !== args.planSha256) {
    fail('plan_digest_mismatch', 'plan SHA-256 does not match the approved digest');
  }
  let plan;
  try {
    plan = JSON.parse(planBytes.toString('utf8'));
  } catch {
    fail('invalid_plan', 'plan JSON is invalid');
  }
  let decoded = { plan, source: null, nativeSha256: args.planSha256 };
  if (plan?.schema === MIRROR_PLAN_SCHEMA) decoded = await unwrapMirrorEnvelope(plan, context);
  else {
    if (planBytes.length > MAXIMUM_PLAN_BYTES) fail('invalid_plan', 'native plan exceeds the size limit');
    validatePlan(plan, context);
  }
  assertRequestedSource(args, decoded.source);
  return { ...decoded, resolvedPlan, transactionRoot, approvalSha256: args.planSha256 };
}

// AI-generated: resumable bytes remain plan-bound and cannot authorize installation.

/** Validate an exact range before consuming any bytes, including timeout prefixes. */
function validateRangeResponse(response, start, end, total) {
  if (response.status !== 206
      || response.headers.get('content-range') !== `bytes ${start}-${end}/${total}`
      || ![null, 'identity'].includes(response.headers.get('content-encoding'))) {
    fail('invalid_download_range', 'server did not return the exact approved byte range');
  }
  const length = response.headers.get('content-length');
  if (length !== null && length !== String(end - start + 1)) {
    fail('invalid_download_range', 'range Content-Length does not match the requested bytes');
  }
}

/** Buffer one bounded range; discard network failures and retain only timeout prefixes. */
async function readDownloadRange(response, start, end, total, signal) {
  try { validateRangeResponse(response, start, end, total); }
  catch (error) { await response.body?.cancel().catch(() => {}); throw error; }
  if (!response.body) fail('asset_download_failed', 'range response body is unavailable');
  const chunks = [];
  let bytes = 0;
  let timedOut = false;
  try {
    for await (const chunk of response.body) {
      bytes += chunk.length;
      if (bytes > end - start + 1) fail('invalid_download_range', 'range response exceeds its declared length');
      chunks.push(Buffer.from(chunk));
    }
  } catch (error) {
    if (error instanceof InstallError) throw error;
    if (!signal.aborted || signal.reason?.name !== 'TimeoutError') {
      throw new InstallError('download_network_failed', `range transfer failed: ${redactDiagnostic(error.message)}`, { cause: error });
    }
    timedOut = true;
  }
  if (!bytes) fail('download_stalled', 'download made no progress; inspect connectivity before starting a new plan');
  if (!timedOut && bytes !== end - start + 1) fail('invalid_download_range', 'range response ended before its declared length');
  return Buffer.concat(chunks, bytes);
}

async function assertDownloadFile(target, context) {
  const stat = assertRegularPath(target, 'file', 'invalid_download_cache');
  if (stat.nlink !== 1) fail('invalid_download_cache', 'download cache must not have hard links');
  await assertPrivateAcl(target, false, context.identity, context.tools);
  return stat;
}

async function readDownloadJson(target, context) {
  const stat = await assertDownloadFile(target, context);
  if (stat.size > MAXIMUM_JSON_BYTES) fail('invalid_download_cache', 'download metadata exceeds its size limit');
  try { return JSON.parse(fs.readFileSync(target, 'utf8')); }
  catch { fail('invalid_download_cache', 'download metadata is incomplete or invalid'); }
}

async function writeDownloadJson(target, value, context) {
  // Publish validated metadata atomically; a host kill leaves only an unused scratch file.
  const scratch = `${target}.${crypto.randomUUID()}.tmp`;
  try {
    await writePrivateFileExclusive(scratch, `${JSON.stringify(value)}\n`, context.identity, context.tools);
    fs.renameSync(scratch, target);
  } finally { removeFileQuietly(scratch); }
}

/** A leftover lock is inspected explicitly; never delete another invocation's lock. */
async function acquireDownloadLock(root, context) {
  const lock = path.join(root, 'download.lock');
  try {
    await writePrivateFileExclusive(lock, JSON.stringify({ pid: process.pid, createdAt: new Date().toISOString() }), context.identity, context.tools);
  } catch (error) {
    if (error.code === 'EEXIST') fail('download_locked', 'another download or a host-killed invocation owns download.lock; inspect its process before recovery');
    throw error;
  }
  return async () => { await assertDownloadFile(lock, context); fs.unlinkSync(lock); };
}

function rateLimitDelay(response, now = Date.now()) {
  if (![403, 429].includes(response.status)) return null;
  const retry = response.headers.get('retry-after');
  const reset = response.headers.get('x-ratelimit-reset');
  if (retry !== null) {
    const seconds = /^\d+$/.test(retry) ? Number(retry) : Math.ceil((Date.parse(retry) - now) / 1000);
    if (Number.isSafeInteger(seconds)) return Math.max(1, Math.min(seconds, 86400));
  }
  if (response.headers.get('x-ratelimit-remaining') === '0' && /^\d+$/.test(reset ?? '')) {
    return Math.max(1, Math.min(86400, Math.ceil(Number(reset) - now / 1000)));
  }
  return response.status === 429 ? 60 : null;
}

function waitingDownload(plan, downloadedBytes, retryAfterSeconds, reason) {
  return { status: 'download_waiting', stage: 'download', downloadedBytes,
    totalBytes: plan.assets.installer.size, retryAfterSeconds, reason };
}

async function requestDownload(url, options) {
  try { return await fetch(url, options); }
  catch (error) {
    const timeout = options.signal.aborted && options.signal.reason?.name === 'TimeoutError';
    throw new InstallError(timeout ? 'download_timeout' : 'download_network_failed',
      timeout ? 'download request timed out before receiving a valid range' : 'download request failed; inspect the network diagnostic',
      { cause: error });
  }
}

/** Reject a known storage shortage before spending time on network requests. */
function assertDownloadSpace(directory, remainingBytes) {
  if (remainingBytes === 0) return;
  let available;
  try {
    const stats = fs.statfsSync(directory, { bigint: true });
    available = stats.bavail * stats.bsize;
  } catch (cause) {
    throw new InstallError('download_storage_unavailable', 'could not inspect download storage; check access to the cache drive', { cause });
  }
  if (available < BigInt(remainingBytes)) {
    fail('insufficient_download_space', `download needs ${remainingBytes} more bytes but only ${available} are available; free space on the cache drive and retry within valid authorization`);
  }
}

/** Download one range without installing, launching, or changing client configuration. */
async function runDownload(args, context) {
  assertReleaseSourceAvailable(args.releaseSource);
  const { plan, transactionRoot, source: sourceInfo, approvalSha256 } = await loadApprovedPlan(args, context);
  const unlock = await acquireDownloadLock(transactionRoot, context);
  let offset = 0;
  try {
    const installerPath = path.join(transactionRoot, plan.assets.installer.name);
    offset = fs.existsSync(installerPath) ? (await assertDownloadFile(installerPath, context)).size : 0;
    if (offset > plan.assets.installer.size) fail('invalid_download_cache', 'partial installer exceeds the approved size');
    assertDownloadSpace(transactionRoot, plan.assets.installer.size - offset);
    const snapshotPath = path.join(transactionRoot, 'download-release.json');
    if (sourceInfo && offset > 0 && !fs.existsSync(snapshotPath)) fail('invalid_download_cache', 'partial mirror cache has no approval binding');
    if (fs.existsSync(snapshotPath)) {
      const snapshot = await readDownloadJson(snapshotPath, context);
      if (sourceInfo && (snapshot.approvalSha256 !== approvalSha256 || snapshot.catalogSha256 !== sha256Bytes(sourceInfo.catalogBytes))) fail('invalid_download_cache', 'cached release belongs to another approval');
      validateReleaseMatchesPlan(snapshot, plan);
    } else {
      const release = await assertSourceMatchesPlan(plan, sourceInfo, context);
      await writeDownloadJson(snapshotPath, sourceInfo ? { ...release, approvalSha256, catalogSha256: sha256Bytes(sourceInfo.catalogBytes) } : release, context);
    }
    const urlPath = path.join(transactionRoot, 'download-url.json');
    const progress = (bytesThisStep) => ({ status: offset === plan.assets.installer.size ? 'downloaded' : 'download_pending',
      stage: 'download', downloadedBytes: offset, totalBytes: plan.assets.installer.size, bytesThisStep,
      expiresAt: plan.expiresAt });
    if (offset === plan.assets.installer.size) {
      assertFileDigest(installerPath, plan.assets.installer.sha256, 'installer');
      if (fs.existsSync(urlPath)) { await assertDownloadFile(urlPath, context); fs.unlinkSync(urlPath); }
      return progress(0);
    }
    const source = new URL(sourceAssetURL(sourceInfo, plan.assets.installer));
    let target = source;
    let cached = false;
    if (fs.existsSync(urlPath)) {
      const record = await readDownloadJson(urlPath, context);
      let cachedUrl;
      try { cachedUrl = new URL(record?.url); }
      catch { fail('invalid_download_cache', 'cached download URL is invalid'); }
      const created = Date.parse(record.createdAt);
      if (record.assetId !== plan.assets.installer.id || !Number.isFinite(created)
          || !allowedSourceRedirect(sourceInfo, source, cachedUrl)
          || (sourceInfo && record.approvalSha256 !== approvalSha256)) fail('invalid_download_cache', 'cached download URL is not bound to the approved asset');
      if (created <= Date.now() && Date.now() - created < DOWNLOAD_URL_TTL_MILLISECONDS) {
        target = cachedUrl; cached = true;
      } else { fs.unlinkSync(urlPath); }
    }
    const end = Math.min(offset + DOWNLOAD_CHUNK_BYTES, plan.assets.installer.size) - 1;
    const signal = AbortSignal.timeout(DOWNLOAD_TIMEOUT_MILLISECONDS);
    const headers = { Range: `bytes=${offset}-${end}`, 'Accept-Encoding': 'identity' };
    let response = await requestDownload(target, { redirect: 'manual', signal, headers: cached || sourceInfo ? headers : {
      ...headers, Accept: 'application/octet-stream', 'User-Agent': 'jishudb-agent-install/0.3', 'X-GitHub-Api-Version': API_VERSION,
    } });
    if (!cached && response.status === 302) {
      const redirect = new URL(response.headers.get('location') ?? '', source);
      if (!allowedSourceRedirect(sourceInfo, source, redirect)) { await response.body?.cancel(); fail('invalid_asset_redirect', 'download redirect is outside the approved transport policy'); }
      await response.body?.cancel();
      await writeDownloadJson(urlPath, { assetId: plan.assets.installer.id, url: redirect.href, createdAt: new Date().toISOString(), ...(sourceInfo ? { approvalSha256 } : {}) }, context);
      response = await requestDownload(redirect, { redirect: 'manual', signal, headers });
    }
    const delay = rateLimitDelay(response);
    if (delay !== null) { await response.body?.cancel(); return waitingDownload(plan, offset, delay, 'rate_limited'); }
    if (cached && response.status === 403) {
      await response.body?.cancel(); fs.unlinkSync(urlPath);
      return waitingDownload(plan, offset, 1, 'download_url_refresh_required');
    }
    if (response.status !== 206) { await response.body?.cancel(); fail('asset_download_failed', `installer range request returned HTTP ${response.status}`); }
    const bytes = await readDownloadRange(response, offset, end, plan.assets.installer.size, signal);
    if (sourceInfo) {
      validatePlan(plan, context);
      await assertSourceMatchesPlan(plan, sourceInfo, context);
    }
    // Recheck the current cache before appending a validated prefix; final SHA remains mandatory.
    if (!fs.existsSync(installerPath)) await writePrivateFileExclusive(installerPath, Buffer.alloc(0), context.identity, context.tools);
    if ((await assertDownloadFile(installerPath, context)).size !== offset) fail('invalid_download_cache', 'download cache changed during the request');
    const descriptor = fs.openSync(installerPath, 'r+');
    try {
      let written = 0;
      while (written < bytes.length) written += fs.writeSync(descriptor, bytes, written, bytes.length - written, offset + written);
      fs.fsyncSync(descriptor);
    } finally { fs.closeSync(descriptor); }
    offset += bytes.length;
    if (offset === plan.assets.installer.size) {
      assertFileDigest(installerPath, plan.assets.installer.sha256, 'installer');
      if (fs.existsSync(urlPath)) { await assertDownloadFile(urlPath, context); fs.unlinkSync(urlPath); }
    }
    return progress(bytes.length);
  } catch (error) {
    if (error.category === 'github_rate_limited') return waitingDownload(plan, offset, error.retryAfterSeconds, 'rate_limited');
    if (error instanceof InstallError) throw error;
    if (error.code && /^(EACCES|EPERM|ENOSPC|EIO|ENOENT|EEXIST|EBUSY)$/.test(error.code)) {
      throw new InstallError('download_storage_failed', `download cache I/O failed: ${redactDiagnostic(error.message)}`, { cause: error });
    }
    throw error;
  } finally { await unlock(); }
}

async function runExecute(args, context) {
  assertReleaseSourceAvailable(args.releaseSource);
  const loaded = await loadApprovedPlan(args, context);
  const { plan, resolvedPlan, transactionRoot, source, nativeBytes, nativeSha256 } = loaded;
  const reinstall = plan.schema === REINSTALL_PLAN_SCHEMA;
  if (reinstall && fs.existsSync(path.join(transactionRoot, 'interactive-reinstall-started.json'))) {
    fail('installer_already_started', 'this approved reinstall has already been handed to the installer; finish or inspect it before another attempt');
  }
  const mcpPort = Number(new URL(plan.connection.url).port);
  if (!await isTcpPortAvailable(mcpPort)) fail('endpoint_conflict', 'the approved Desktop MCP port is no longer available; create a new plan');
  assertInstallationDestinations(plan);
  assertDesktopEndpointCompatible(plan.installation.bootstrapPath, plan.connection.url);

  const installerPath = path.join(transactionRoot, plan.assets.installer.name);
  const checksumPath = path.join(transactionRoot, plan.assets.checksum.name);
  const candidatePath = path.join(transactionRoot, plan.assets.candidate.name);
  const unlock = await acquireDownloadLock(transactionRoot, context);
  let installerCompleted = false;
  try {
    if (!fs.existsSync(installerPath)) fail('download_required', 'run download until status=downloaded before execute');
    await assertDownloadFile(installerPath, context);
    assertFileSize(installerPath, plan.assets.installer.size, 'installer');
    assertFileDigest(installerPath, plan.assets.installer.sha256, 'installer');
    await assertSourceMatchesPlan(plan, source, context);
    for (const [asset, destination, maximumBytes, timeoutMilliseconds] of [
      [plan.assets.candidate, candidatePath, MAXIMUM_JSON_BYTES, SMALL_ASSET_TIMEOUT_MILLISECONDS],
      [plan.assets.checksum, checksumPath, MAXIMUM_CHECKSUM_BYTES, SMALL_ASSET_TIMEOUT_MILLISECONDS],
    ]) {
      if (fs.existsSync(destination)) await assertDownloadFile(destination, context);
      else await saveAsset(sourceAssetURL(source, asset), destination, maximumBytes, timeoutMilliseconds, source);
      assertFileSize(destination, asset.size, asset.role);
      assertFileDigest(destination, asset.sha256, asset.role);
    }
    const expectedChecksum = `${plan.assets.installer.sha256}  ${plan.assets.installer.name}\n`;
    if (fs.readFileSync(checksumPath, 'utf8').replaceAll('\r\n', '\n') !== expectedChecksum) {
      fail('invalid_checksum', 'adjacent checksum content is not exact');
    }
    const candidate = JSON.parse(fs.readFileSync(candidatePath, 'utf8'));
    const selected = {
      version: plan.release.version,
      installer: {
        id: plan.assets.installer.id,
        name: plan.assets.installer.name,
        size: plan.assets.installer.size,
        state: 'uploaded',
        url: plan.assets.installer.url,
        digest: `sha256:${plan.assets.installer.sha256}`,
      },
    };
    validateWindowsCandidate(candidate, selected);
    if (!reinstall && (candidate.agentBackgroundLaunch === 1) !== (plan.schema === BACKGROUND_PLAN_SCHEMA)) fail('invalid_candidate', 'Agent launch capability no longer matches the approved plan');
    if (candidate.revision !== plan.release.sourceRevision) fail('invalid_candidate', 'candidate source revision does not match the approved plan');
    await assertSourceMatchesPlan(plan, source, context);

    validatePlan(plan, context);
    let nativePlanPath = resolvedPlan;
    if (source && !reinstall) {
      // AI-generated: exact embedded bytes and their already-approved digest are
      // passed to the legacy parser; never authorize a newly serialized child.
      nativePlanPath = path.join(transactionRoot, 'native-install-plan.json');
      if (nativePlanPath === resolvedPlan) fail('invalid_plan', 'outer approval cannot occupy the native child path');
      if (fs.existsSync(nativePlanPath)) {
        await assertDownloadFile(nativePlanPath, context);
        assertFileDigest(nativePlanPath, nativeSha256, 'native plan');
      } else await writePrivateFileExclusive(nativePlanPath, nativeBytes, context.identity, context.tools);
      const reloaded = await loadApprovedPlan(args, context);
      if (reloaded.nativeSha256 !== nativeSha256) fail('plan_digest_mismatch', 'native plan binding changed before installation');
    }
    assertInstallationDestinations(plan);
    assertDesktopEndpointCompatible(plan.installation.bootstrapPath, plan.connection.url);
    if (!await isTcpPortAvailable(mcpPort)) fail('endpoint_conflict', 'the approved Desktop MCP port became occupied before installation');
    if (reinstall) return await launchInteractiveReinstallation(installerPath, plan, loaded, context);
    const installer = childProcess.spawnSync(installerPath, [
      '/S',
      `/JISHUDB_AGENT_PLAN=${nativePlanPath}`,
      `/JISHUDB_AGENT_PLAN_SHA256=${nativeSha256 ?? args.planSha256}`,
    ], {
      env: sanitizedChildEnvironment(),
      stdio: 'ignore',
      windowsHide: false,
      shell: false,
    });
    if (installer.error) throw installer.error;
    if (installer.status !== 0) fail('installer_failed', `Windows installer returned exit code ${installer.status}`);
    installerCompleted = true;

    const application = path.join(plan.installation.applicationRoot, 'JishuDB.exe');
    const runtime = path.join(plan.installation.applicationRoot, 'resources', 'runtime', 'jishudb.exe');
    assertRegularPath(application, 'file', 'installed_receipt_invalid');
    assertRegularPath(plan.installation.bootstrapPath, 'file', 'installed_receipt_invalid');
    assertRegularPath(runtime, 'file', 'installed_receipt_invalid');
    await writeDesktopEndpointConfig(plan.installation.bootstrapPath, plan.connection.url, context);
    const launch = await launchInstalledDesktop(plan, loaded, context);
    return {
      status: 'installed',
      ...launch,
      version: plan.release.version,
      applicationRoot: plan.installation.applicationRoot,
      dataRoot: plan.installation.dataRoot,
      mcpUrl: plan.connection.url,
      next: 'wait_for_desktop_and_user_onboarding',
    };
  } catch (error) {
    if (installerCompleted) {
      error.installation = {
        status: 'installer_completed',
        version: plan.release.version,
        applicationRoot: plan.installation.applicationRoot,
        dataRoot: plan.installation.dataRoot,
        mcpUrl: plan.connection.url,
        next: 'verify_existing_installation_before_launch',
      };
    }
    throw error;
  } finally {
    await unlock();
  }
}

function redactDiagnostic(value) {
  return String(value)
    .replace(/([?&][A-Za-z0-9_.~-]{1,64}=)[^&\s]*/g, '$1<redacted>')
    .replace(/\b(https?:\/\/)[^/\s@]+@/gi, '$1<redacted>@')
    .replace(/\b(Bearer)\s+[^\s]+/gi, '$1 <redacted>');
}

function sanitizedChildEnvironment(source = process.env) {
  const environment = Object.create(null);
  for (const [key, value] of Object.entries(source)) {
    if (typeof value === 'string' && CHILD_ENVIRONMENT_ALLOWLIST.has(key.toLowerCase())) {
      environment[key] = value;
    }
  }
  return environment;
}

/** Build a child-only proxy environment without changing host or system settings. */
function downloadProxyEnvironment(source = process.env) {
  const values = {};
  for (const name of ['HTTP_PROXY', 'HTTPS_PROXY']) {
    const raw = source[name.toLowerCase()] || source[name];
    if (!raw) continue;
    let parsed;
    try {
      if (typeof raw !== 'string') throw new TypeError('proxy URL must be text');
      parsed = new URL(raw);
      decodeURIComponent(parsed.username);
      decodeURIComponent(parsed.password);
    } catch { fail('invalid_proxy_configuration', `${name} must contain a valid HTTP or HTTPS proxy URL`); }
    if (!['http:', 'https:'].includes(parsed.protocol) || !parsed.hostname
        || parsed.hash || parsed.search || parsed.pathname !== '/' || /[\u0000-\u0020\u007f]/.test(raw)) {
      fail('invalid_proxy_configuration', `${name} must be an HTTP or HTTPS proxy URL without a path, query, fragment, or whitespace`);
    }
    values[name] = raw;
  }
  if (Object.keys(values).length === 0) return null;
  const exclusions = new Set((source.no_proxy || source.NO_PROXY || '').split(',').map(value => value.trim()).filter(Boolean));
  for (const host of ['localhost', '127.0.0.1', '::1', '[::1]']) exclusions.add(host);
  const environment = { ...source };
  for (const key of Object.keys(environment)) {
    if (['http_proxy', 'https_proxy', 'no_proxy', 'node_use_env_proxy'].includes(key.toLowerCase())) delete environment[key];
  }
  return { ...environment, ...values, NO_PROXY: [...exclusions].join(','), NODE_USE_ENV_PROXY: '1' };
}

/** Restart this helper once so Node initializes fetch's proxy dispatcher at startup. */
function runWithDownloadProxy(argv, runtime = process, spawnSync = childProcess.spawnSync) {
  const environment = downloadProxyEnvironment(runtime.env);
  if (!environment) return null;
  if (!runtime.allowedNodeEnvironmentFlags.has('--use-env-proxy')) {
    fail('unsupported_proxy_runtime', 'configured download proxies require Node.js 22.21+ or 24.5+ with --use-env-proxy support');
  }
  const ready = runtime.execArgv.includes('--use-env-proxy')
    && runtime.env.NODE_USE_ENV_PROXY === '1'
    && ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY'].every(key => runtime.env[key] === environment[key])
    && !Object.keys(runtime.env).some(key => ['http_proxy', 'https_proxy', 'no_proxy'].includes(key));
  if (ready) return null;
  // AI-generated: proxy credentials travel only in the child environment, never argv or output.
  const flags = runtime.execArgv.filter(flag => !['--use-env-proxy', '--no-use-env-proxy'].includes(flag));
  const child = spawnSync(runtime.execPath, [...flags, '--use-env-proxy', runtime.argv[1], ...argv], {
    env: environment,
    stdio: 'inherit',
    windowsHide: true,
    shell: false,
  });
  if (child.error) throw new InstallError('proxy_helper_launch_failed', 'could not start the proxy-enabled download helper', { cause: child.error });
  if (child.signal) fail('proxy_helper_interrupted', `proxy-enabled download helper was interrupted by ${child.signal}`);
  if (!Number.isInteger(child.status)) fail('proxy_helper_launch_failed', 'proxy-enabled download helper returned no exit status');
  return child.status;
}

async function main(argv = process.argv.slice(2)) {
  try {
    const args = parseArguments(argv);
    assertReleaseSourceAvailable(args.releaseSource);
    assertWindowsX64();
    const proxyStatus = runWithDownloadProxy(argv);
    if (proxyStatus !== null) return proxyStatus;
    const tools = resolveSystemTools();
    const identity = await getCurrentWindowsIdentity(tools);
    const tempRoot = assertNoReparseAncestors(os.tmpdir(), 'temporary directory');
    const localAppData = assertNoReparseAncestors(process.env.LOCALAPPDATA ?? '', 'LOCALAPPDATA');
    assertRegularPath(tempRoot, 'directory', 'unsupported_platform');
    assertRegularPath(localAppData, 'directory', 'unsupported_platform');
    const context = { identity, localAppData, tempRoot, tools };
    let result;
    if (args.mode === 'check') result = await runCheck(context);
    else if (args.mode === 'plan') result = await runPlan(args, context);
    else if (args.mode === 'download') result = await runDownload(args, context);
    else result = await runExecute(args, context);
    process.stdout.write(`${JSON.stringify(result)}\n`);
    return 0;
  } catch (error) {
    const diagnostic = redactDiagnostic(error?.message ?? error);
    process.stderr.write(`${diagnostic}\n`);
    if (error?.cause) process.stderr.write(`${redactDiagnostic(error.cause?.cause?.code ?? error.cause.code ?? error.cause.message)}\n`);
    const known = error instanceof InstallError;
    process.stdout.write(`${JSON.stringify({
      status: 'failed',
      stage: ['check', 'plan', 'download', 'execute'].includes(argv[0]) ? argv[0] : 'arguments',
      errorCategory: known ? error.category : 'unexpected_failure',
      message: known ? error.publicMessage : 'installation helper failed; inspect the local diagnostic',
      ...(error?.installation ? { installation: error.installation } : {}),
      ...(error?.cleanup ? { cleanup: error.cleanup } : {}),
    })}\n`);
    return 1;
  }
}

const exported = {
  InstallError,
  runNative,
  dispatchDesktopTarget,
  createDesktopShortcut,
  launchInstalledDesktop,
  assertReinstallableApplication,
  runPlan,
  loadApprovedPlan,
  createMirrorEnvelope,
  unwrapMirrorEnvelope,
  verifyMirrorCatalog,
  discoverMirror,
  mirrorSelection,
  advanceMirrorFloor,
  assertReleaseSourceAvailable,
  downloadProxyEnvironment,
  runWithDownloadProxy,
  fetchWithTimeout,
  requestDownload,
  validateRangeResponse,
  readDownloadRange,
  rateLimitDelay,
  runDownload,
  runExecute,
  readSavedDesktopEndpoint,
  selectInstallationEndpoint,
  assertDesktopEndpointCompatible,
  assertFreshInstallationDestinations,
  readRetainedInstallation,
  assertReinstallationDestinations,
  writeDesktopEndpointConfig,
  validateReleaseMatchesPlan,
  approvedDesktopMcpPorts,
  assertPlanShape,
  compareSemver,
  getReleasePages,
  isAllowedAssetRedirect,
  isDesktopMcpUrl,
  isPrivateAclEntries,
  normalizeLocalWindowsPath,
  parseArguments,
  parseIcaclsEntries,
  parseSemver,
  redactDiagnostic,
  sanitizedChildEnvironment,
  selectEligibleRelease,
  validatePlan,
  validateWindowsCandidate,
};

const commonJsModule = typeof module === 'object' && module?.exports ? module : null;
if (commonJsModule) commonJsModule.exports = exported;

const directCommonJsExecution = commonJsModule && typeof require === 'function' && require.main === commonJsModule;
if (!commonJsModule || directCommonJsExecution) {
  main().then((status) => { process.exitCode = status; });
}
