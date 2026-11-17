#!/bin/zsh
set -euo pipefail
setopt NULL_GLOB
umask 077

readonly RELEASE_REPOSITORY="x-aijishu/jishudb-desktop-releases"
readonly SOURCE_REPOSITORY="x-aijishu/jishudb"
readonly API_ORIGIN="https://api.github.com"
readonly API_VERSION="2026-03-10"
readonly ASSET_REDIRECT_HOST="release-assets.githubusercontent.com"
readonly PLAN_SCHEMA="jishudb-agent-install-plan-v1"
readonly PREFERRED_MCP_PORT=8088
readonly RESERVED_LAN_MCP_PORT=8089
readonly ENDPOINT_CONFIG_SCHEMA=1
readonly ENDPOINT_CONFIG_FILENAME="desktop-endpoint.json"
readonly MAX_RELEASE_PAGES=5
readonly DOWNLOAD_SLICE_SECONDS=20
readonly DOWNLOAD_SLICE_BYTES=16777216
readonly DOWNLOAD_LOCATION_TTL_SECONDS=300
readonly SCRIPT_ROOT="${0:A:h}"

MODE="${1:-}"
[[ "$MODE" == "plan" || "$MODE" == "download" || "$MODE" == "execute" ]] || {
  print -u2 -- "usage: install-macos.zsh <plan|download|execute> [options]"
  exit 2
}
shift

CURRENT_STAGE="$MODE"
TRANSACTION_LOCK=""
PLAN_PATH=""
PLAN_SHA256=""
RELEASE_SOURCE="cnb"
RELEASE_SOURCE_SPECIFIED=0
CNB_NODE=""
CNB_CONTEXT=""
CNB_RESULT=""
CANDIDATE_TAG=""
CANDIDATE_REVISION=""
CLIENT=""
CONFIG_TARGET=""
CONNECTION_NAME="jishudb"
CLEANUP_MOUNT=""
typeset -a CLEANUP_PATHS
CLEANUP_PATHS=()

cleanup() {
  if [[ -n "$CLEANUP_MOUNT" ]]; then
    /usr/bin/hdiutil detach "$CLEANUP_MOUNT" >/dev/null 2>&1 || true
  fi
  local target
  for target in "${CLEANUP_PATHS[@]}"; do
    [[ -n "$target" ]] && /bin/rm -rf -- "$target"
  done
  if [[ -n "$TRANSACTION_LOCK" ]]; then
    /bin/rmdir -- "$TRANSACTION_LOCK" 2>/dev/null || true
  fi
}

trap cleanup EXIT

while (( $# > 0 )); do
  case "$1" in
    --release-source)
      (( $# >= 2 && RELEASE_SOURCE_SPECIFIED == 0 )) || { print -u2 -- "--release-source requires exactly one value"; exit 2; }
      RELEASE_SOURCE="$2"
      RELEASE_SOURCE_SPECIFIED=1
      shift 2
      ;;
    --plan)
      (( $# >= 2 )) || { print -u2 -- "--plan requires a value"; exit 2; }
      PLAN_PATH="$2"
      shift 2
      ;;
    --plan-sha256)
      (( $# >= 2 )) || { print -u2 -- "--plan-sha256 requires a value"; exit 2; }
      PLAN_SHA256="$2"
      shift 2
      ;;
    --candidate-tag)
      (( $# >= 2 )) || { print -u2 -- "--candidate-tag requires a value"; exit 2; }
      CANDIDATE_TAG="$2"
      shift 2
      ;;
    --candidate-revision)
      (( $# >= 2 )) || { print -u2 -- "--candidate-revision requires a value"; exit 2; }
      CANDIDATE_REVISION="$2"
      shift 2
      ;;
    --client)
      (( $# >= 2 )) || { print -u2 -- "--client requires a value"; exit 2; }
      CLIENT="$2"
      shift 2
      ;;
    --config-target)
      (( $# >= 2 )) || { print -u2 -- "--config-target requires a value"; exit 2; }
      CONFIG_TARGET="$2"
      shift 2
      ;;
    --connection-name)
      (( $# >= 2 )) || { print -u2 -- "--connection-name requires a value"; exit 2; }
      CONNECTION_NAME="$2"
      shift 2
      ;;
    *)
      print -u2 -- "unsupported option: $1"
      exit 2
      ;;
  esac
done

fail() {
  local category="$1"
  local message="$2"
  print -u2 -- "${category}: ${message}"
  jxa result failed "$category" "$message" "$CURRENT_STAGE" || true
  exit 1
}

jxa() {
  /usr/bin/osascript -l JavaScript - "$@" <<'JXA'
ObjC.import('Foundation');

function unwrap(value) {
  return ObjC.unwrap(value);
}

function readText(path) {
  const data = $.NSData.dataWithContentsOfFile(path);
  if (!data) throw new Error('cannot read file');
  return unwrap($.NSString.alloc.initWithDataEncoding(data, $.NSUTF8StringEncoding));
}

function readJSON(path) {
  return JSON.parse(readText(path));
}

// AI-generated download boundary: accept only bytes from the exact requested
// range of the approved asset. Full-file SHA-256 is still required before use.
function validateDownloadSlice(headers, httpCode, offset, end, total, bytes, curlCode) {
  for (const value of [offset, end, total, bytes, curlCode]) {
    if (!Number.isSafeInteger(value) || value < 0) throw new Error('invalid slice values');
  }
  if (offset > end || end >= total || bytes > end - offset + 1 ||
      ![0, 28].includes(curlCode)) throw new Error('invalid slice bounds or transfer failure');
  const blocks = headers.trim().split(/\r?\n\r?\n/);
  const block = blocks[blocks.length - 1];
  const status = block.match(/^HTTP\/[^ ]+ ([0-9]{3})/);
  if (!status || status[1] !== String(httpCode) || httpCode !== '206') {
    throw new Error('server did not honor the requested byte range');
  }
  const ranges = [...block.matchAll(/^content-range:\s*bytes (\d+)-(\d+)\/(\d+)\s*$/gim)];
  const encodings = [...block.matchAll(/^content-encoding:\s*(.+)$/gim)];
  if (ranges.length !== 1 || Number(ranges[0][1]) !== offset ||
      Number(ranges[0][2]) !== end || Number(ranges[0][3]) !== total ||
      encodings.some(match => match[1].trim().toLowerCase() !== 'identity')) {
    throw new Error('response range or encoding differs from the approved asset');
  }
  if (curlCode === 0 && bytes !== end - offset + 1) throw new Error('truncated successful range');
  return bytes;
}

function exactKeys(value, keys, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error(label + ' must be an object');
  }
  const actual = Object.keys(value).sort().join('\n');
  const expected = keys.slice().sort().join('\n');
  if (actual !== expected) throw new Error(label + ' fields do not match the reviewed schema');
}

function requireString(value, pattern, label) {
  if (typeof value !== 'string' || !pattern.test(value)) throw new Error(label + ' is invalid');
  return value;
}

function requireSafeText(value, label) {
  if (typeof value !== 'string' || value.length < 1 || value.length > 1024 || /[\u0000-\u001f\u007f]/.test(value)) {
    throw new Error(label + ' is invalid');
  }
  return value;
}

function requireDesktopMCPURL(value) {
  const match = /^http:\/\/127\.0\.0\.1:([0-9]+)\/mcp$/.exec(value);
  if (!match) throw new Error('Desktop MCP URL is invalid');
  const port = Number(match[1]);
  if (port !== 8088 && (port < 8090 || port > 8104)) {
    throw new Error('Desktop MCP URL is outside the bounded port selection');
  }
  return value;
}

function assetDigest(asset, label) {
  if (!asset || asset.state !== 'uploaded' || !Number.isSafeInteger(asset.size) || asset.size <= 0) {
    throw new Error(label + ' is not a complete uploaded asset');
  }
  return requireString(asset.digest, /^sha256:[0-9a-f]{64}$/, label + ' digest').slice(7);
}

function exactAsset(release, name, label) {
  const matches = release.assets.filter((asset) => asset.name === name);
  if (matches.length !== 1) throw new Error(label + ' must exist exactly once');
  const asset = matches[0];
  assetDigest(asset, label);
  const expected = 'https://api.github.com/repos/x-aijishu/jishudb-desktop-releases/releases/assets/' + asset.id;
  if (asset.url !== expected) throw new Error(label + ' API URL is not canonical');
  return asset;
}

function semverParts(value) {
  const match = /^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$/.exec(value);
  if (!match) return null;
  return match.slice(1).map(Number);
}

function compareSemver(left, right) {
  for (let index = 0; index < 3; index += 1) {
    if (left[index] !== right[index]) return right[index] - left[index];
  }
  return 0;
}

function selectRelease(paths) {
  const releases = [];
  paths.forEach((path) => {
    const page = readJSON(path);
    if (!Array.isArray(page)) throw new Error('release page must be an array');
    page.forEach((release) => releases.push(release));
  });
  return selectFromReleases(releases, null);
}

// AI-generated opt-in rehearsal boundary: an exact tag and source are mandatory.
function candidateRequest(tag, revision) {
  requireString(tag, /^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-desktop-candidate\.[1-9][0-9]{0,6})?$/, 'candidate tag');
  requireString(revision, /^[0-9a-f]{40}$/, 'candidate source revision');
  return { tag, revision, version: tag.slice(1).split('-desktop-candidate.')[0] };
}

function selectFromReleases(releases, requested) {
  const eligible = [];
  releases.forEach((release) => {
    if (release.draft !== false || release.immutable !== true) return;
    if (requested) {
      if (release.prerelease !== true || release.tag_name !== requested.tag) return;
    } else {
      if (release.prerelease !== false || typeof release.tag_name !== 'string' || !/^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$/.test(release.tag_name)) return;
    }
    const version = requested ? requested.version : release.tag_name.slice(1);
    const parts = semverParts(version);
    const signedName = 'jishudb-desktop-' + version + '-darwin-arm64.dmg';
    const hasSignedAssets = Array.isArray(release.assets) && release.assets.some((asset) =>
      [signedName, signedName + '.sha256', signedName + '.candidate.json'].includes(asset.name));
    const installerName = (requested || hasSignedAssets) ? signedName : 'jishudb-desktop-' + version + '-unsigned-darwin-arm64.dmg';
    try {
      eligible.push({
        ...(requested ? {candidateRevision: requested.revision} : {}),
        version,
        parts,
        release: {
          id: release.id,
          tag: release.tag_name,
          targetCommitish: String(release.target_commitish),
          immutable: release.immutable,
          draft: release.draft,
          prerelease: release.prerelease,
        },
        installer: exactAsset(release, installerName, 'installer'),
        checksum: exactAsset(release, installerName + '.sha256', 'checksum'),
        candidate: exactAsset(release, installerName + '.candidate.json', 'candidate'),
      });
    } catch (_) {
      return;
    }
  });
  if (eligible.length === 0) throw new Error(requested ? 'requested immutable signed macOS prerelease is unavailable' : 'no eligible immutable stable macOS release is available');
  if (requested && eligible.length !== 1) throw new Error('candidate release is ambiguous');
  eligible.sort((left, right) => compareSemver(left.parts, right.parts));
  const selected = eligible[0];
  delete selected.parts;
  return selected;
}

// AI-generated signed-candidate boundary. Metadata binds OS checks; it never
// substitutes for codesign, Gatekeeper or notarization-ticket verification.
function validateSignedCandidate(candidate, selected) {
  exactKeys(candidate, ['artifact', 'artwork', 'authorization', 'bundleIdentifier', 'distribution',
    'minimumSystemVersion', 'product', 'productName', 'revision', 'runtimeLock', 'schemaVersion',
    'signing', 'source', 'target', 'version',
    ...(Object.prototype.hasOwnProperty.call(candidate, 'agentBackgroundLaunch') ? ['agentBackgroundLaunch'] : [])], 'candidate');
  exactKeys(candidate.artifact, ['name', 'sha256', 'size'], 'candidate.artifact');
  exactKeys(candidate.runtimeLock, ['path', 'sha256'], 'candidate.runtimeLock');
  exactKeys(candidate.source, ['repository', 'runAttempt', 'runId'], 'candidate.source');
  exactKeys(candidate.distribution, ['appNotarization', 'dmgNotarization', 'hardenedRuntime', 'mode',
    'publisherIdentity', 'secureTimestamp', 'teamIdentifier'], 'candidate.distribution');
  exactKeys(candidate.authorization, ['localUserPresence', 'mode', 'publisherIdentity', 'teamIdentifier'], 'candidate.authorization');
  exactKeys(candidate.authorization.localUserPresence, ['firstAdmin', 'migration', 'recovery'], 'candidate.authorization.localUserPresence');
  exactKeys(candidate.signing, ['certificateExpiresAt', 'certificateFingerprintSha256', 'nativeFileCount'], 'candidate.signing');
  exactKeys(candidate.artwork, ['icns', 'png', 'source'], 'candidate.artwork');
  if (candidate.schemaVersion !== 3 || candidate.product !== 'jishudb-desktop'
    || candidate.productName !== 'JishuDB' || candidate.bundleIdentifier !== 'com.aijishu.jishudb'
    || candidate.target !== 'darwin-arm64' || candidate.version !== selected.version
    || candidate.source.repository !== 'x-aijishu/jishudb'
    || candidate.artifact.name !== 'jishudb-desktop-' + selected.version + '-darwin-arm64.dmg'
    || candidate.artifact.name !== selected.installer.name
    || candidate.artifact.sha256 !== assetDigest(selected.installer, 'installer')
    || candidate.artifact.size !== selected.installer.size
    || candidate.runtimeLock.path !== 'packaging/macos/desktop-runtime-lock.json'
    || candidate.distribution.mode !== 'developer-id-notarized-dmg-v1'
    || candidate.distribution.publisherIdentity !== 'developer-id'
    || candidate.distribution.hardenedRuntime !== true || candidate.distribution.secureTimestamp !== true
    || candidate.authorization.mode !== 'signed-developer-id-v1'
    || candidate.authorization.publisherIdentity !== 'developer-id'
    || candidate.authorization.teamIdentifier !== candidate.distribution.teamIdentifier
    || ['firstAdmin', 'migration', 'recovery'].some((key) => candidate.authorization.localUserPresence[key] !== true)) {
    throw new Error('signed candidate identity or authority is invalid');
  }
  requireString(candidate.revision, /^[0-9a-f]{40}$/, 'candidate revision');
  requireString(candidate.runtimeLock.sha256, /^[0-9a-f]{64}$/, 'candidate runtime lock');
  requireString(candidate.distribution.teamIdentifier, /^[A-Z0-9]{10}$/, 'candidate team');
  requireString(candidate.source.runId, /^[1-9][0-9]*$/, 'candidate run ID');
  requireString(candidate.minimumSystemVersion, /^\d+\.\d+(?:\.\d+)?$/, 'minimum system version');
  requireString(candidate.signing.certificateFingerprintSha256, /^[0-9a-f]{64}$/, 'certificate fingerprint');
  requireString(candidate.signing.certificateExpiresAt, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/, 'certificate expiry');
  if (!Number.isFinite(Date.parse(candidate.signing.certificateExpiresAt))
    || !Number.isSafeInteger(candidate.signing.nativeFileCount) || candidate.signing.nativeFileCount <= 0
    || !Number.isSafeInteger(candidate.source.runAttempt) || candidate.source.runAttempt <= 0
    || (Object.prototype.hasOwnProperty.call(candidate, 'agentBackgroundLaunch') && candidate.agentBackgroundLaunch !== 1)) {
    throw new Error('signed candidate evidence is invalid');
  }
  ['appNotarization', 'dmgNotarization'].forEach((key) => {
    const value = candidate.distribution[key];
    exactKeys(value, ['status', 'stapled', 'submissionId'], key);
    if (value.status !== 'Accepted' || value.stapled !== true || typeof value.submissionId !== 'string' || !value.submissionId.trim()) throw new Error('candidate notarization is incomplete');
  });
  const artworkPaths = { source: 'desktop/assets/logo-jishudb.svg', png: 'desktop/assets/jishudb-icon.png', icns: 'desktop/assets/jishudb.icns' };
  Object.keys(artworkPaths).forEach((key) => {
    exactKeys(candidate.artwork[key], ['path', 'sha256'], 'artwork.' + key);
    if (candidate.artwork[key].path !== artworkPaths[key]) throw new Error('candidate artwork path is invalid');
    requireString(candidate.artwork[key].sha256, /^[0-9a-f]{64}$/, 'artwork digest');
  });
  return candidate;
}

function candidatePublisher(candidate) {
  return candidate.schemaVersion === 3
    ? { identity: 'developer-id', gatekeeper: 'accepted', teamIdentifier: candidate.distribution.teamIdentifier }
    : { identity: 'none', gatekeeper: 'manual-required' };
}

function validateCandidate(candidate, selected) {
  if (selected.candidateRevision && candidate.revision !== selected.candidateRevision) {
    throw new Error('candidate revision differs from the explicitly requested source');
  }
  if (selected.release && selected.release.prerelease === true &&
      (candidate.schemaVersion !== 3 || candidate.agentBackgroundLaunch !== 1)) {
    throw new Error('rehearsal requires a signed background-launch candidate');
  }
  if (candidate && candidate.schemaVersion === 3) return validateSignedCandidate(candidate, selected);
  exactKeys(candidate, [
    'artifact', 'authorization', 'bundleIdentifier', 'distribution',
    'minimumSystemVersion', 'nativeFileCount', 'product', 'productName',
    'revision', 'runtimeLockSha256', 'schemaVersion', 'source', 'target', 'version',
    ...(Object.prototype.hasOwnProperty.call(candidate, 'agentBackgroundLaunch') ? ['agentBackgroundLaunch'] : []),
  ], 'candidate');
  if (Object.prototype.hasOwnProperty.call(candidate, 'agentBackgroundLaunch') && candidate.agentBackgroundLaunch !== 1) throw new Error('unsupported Agent launch contract');
  exactKeys(candidate.artifact, ['name', 'sha256'], 'candidate.artifact');
  exactKeys(candidate.source, ['repository', 'runAttempt', 'runId'], 'candidate.source');
  exactKeys(candidate.distribution, ['adHocIntegritySeal', 'gatekeeperAssessment', 'mode', 'notarization', 'publisherIdentity'], 'candidate.distribution');
  exactKeys(candidate.authorization, ['compensatingControls', 'localUserPresence', 'mode', 'publisherIdentity', 'risk'], 'candidate.authorization');
  exactKeys(candidate.authorization.localUserPresence, ['firstAdmin', 'migration', 'recovery'], 'candidate.authorization.localUserPresence');
  if (candidate.schemaVersion !== 2 || candidate.product !== 'jishudb-desktop' ||
      candidate.productName !== 'JishuDB' || candidate.bundleIdentifier !== 'com.aijishu.jishudb' ||
      candidate.target !== 'darwin-arm64' || candidate.version !== selected.version ||
      candidate.source.repository !== 'x-aijishu/jishudb' ||
      !/^[1-9][0-9]*$/.test(candidate.source.runId) || !Number.isSafeInteger(candidate.source.runAttempt) || candidate.source.runAttempt <= 0 ||
      candidate.artifact.name !== selected.installer.name ||
      candidate.artifact.sha256 !== assetDigest(selected.installer, 'installer') ||
      candidate.distribution.mode !== 'unsigned-dmg-v1' ||
      candidate.distribution.publisherIdentity !== 'none' || candidate.distribution.notarization !== 'not-applicable' ||
      candidate.distribution.gatekeeperAssessment !== 'manual-required' ||
      candidate.distribution.adHocIntegritySeal !== 'runtime-macho-then-whole-app-v1' ||
      candidate.authorization.mode !== 'unsigned-local-user-presence-v1' ||
      candidate.authorization.publisherIdentity !== 'none' ||
      candidate.authorization.localUserPresence.firstAdmin !== true ||
      candidate.authorization.localUserPresence.migration !== true ||
      candidate.authorization.localUserPresence.recovery !== true) {
    throw new Error('candidate product, source, artifact, distribution, or authorization is invalid');
  }
  requireString(candidate.revision, /^[0-9a-f]{40}$/, 'candidate revision');
  requireString(candidate.runtimeLockSha256, /^[0-9a-f]{64}$/, 'candidate runtime lock digest');
  if (!Number.isSafeInteger(candidate.nativeFileCount) || candidate.nativeFileCount <= 0 ||
      typeof candidate.minimumSystemVersion !== 'string' || !/^\d+\.\d+(?:\.\d+)?$/.test(candidate.minimumSystemVersion) ||
      !Array.isArray(candidate.authorization.compensatingControls) || candidate.authorization.compensatingControls.length < 1 ||
      typeof candidate.authorization.risk !== 'string' || candidate.authorization.risk.length < 1) {
    throw new Error('candidate platform or authorization evidence is invalid');
  }
  return candidate;
}

function assetPlan(asset, role) {
  return {
    role,
    id: asset.id,
    name: asset.name,
    size: asset.size,
    url: asset.url,
    sha256: assetDigest(asset, role),
  };
}

function createPlan(selected, candidate, argv) {
  const now = new Date();
  const expires = new Date(Math.min(now.getTime() + 120 * 60 * 1000,
    selected.transport ? Date.parse(selected.transport.catalog.payload.expiresAt) : Infinity));
  return {
    ...(selected.transport ? {transport: selected.transport} : {}),
    schema: selected.release.prerelease === true ? 'jishudb-agent-install-plan-v3' : candidate.agentBackgroundLaunch === 1 ? 'jishudb-agent-install-plan-v2' : 'jishudb-agent-install-plan-v1',
    ...(selected.release.prerelease === true ? {releaseChannel: 'candidate'} : {}),
    ...(candidate.agentBackgroundLaunch === 1 ? {launchMode: 'agent-background'} : {}),
    createdAt: now.toISOString(),
    expiresAt: expires.toISOString(),
    operation: 'fresh-install',
    platform: 'darwin-arm64',
    userId: argv[0],
    release: {
      repository: 'x-aijishu/jishudb-desktop-releases',
      id: selected.release.id,
      tag: selected.release.tag,
      version: selected.version,
      targetCommitish: selected.release.targetCommitish,
      sourceRepository: 'x-aijishu/jishudb',
      sourceRevision: candidate.revision,
    },
    assets: {
      installer: assetPlan(selected.installer, 'installer'),
      checksum: assetPlan(selected.checksum, 'checksum'),
      candidate: assetPlan(selected.candidate, 'candidate'),
    },
    installation: {
      applicationPath: requireSafeText(argv[1], 'application path'),
      dataRoot: requireSafeText(argv[2], 'data root'),
      dataOwnershipAcknowledged: true,
    },
    connection: {
      client: requireSafeText(argv[3], 'client'),
      configTarget: requireSafeText(argv[4], 'config target'),
      name: requireString(argv[5], /^[A-Za-z0-9._-]{1,64}$/, 'connection name'),
      url: requireDesktopMCPURL(argv[6]),
      profile: 'default',
    },
    publisher: candidatePublisher(candidate),
  };
}

function validatePlan(plan) {
  const rehearsal = plan && plan.schema === 'jishudb-agent-install-plan-v3';
  exactKeys(plan, [
    'schema', 'createdAt', 'expiresAt', 'operation', 'platform', 'userId',
    'release', 'assets', 'installation', 'connection', 'publisher',
    ...(['jishudb-agent-install-plan-v2', 'jishudb-agent-install-plan-v3'].includes(plan.schema) ? ['launchMode'] : []),
    ...(rehearsal ? ['releaseChannel'] : []),
    ...(plan.transport ? ['transport'] : []),
  ], 'plan');
  if (plan.transport) {
    exactKeys(plan.transport, ['source', 'catalogURL', 'payloadSha256', 'sequence', 'keyId', 'catalog'], 'plan.transport');
    if (plan.transport.source !== 'cnb' || rehearsal || !Number.isSafeInteger(plan.transport.sequence)
        || plan.transport.sequence < 1 || !/^https:\/\/cnb\.cool\//.test(plan.transport.catalogURL)
        || !/^[0-9a-f]{64}$/.test(plan.transport.payloadSha256)
        || !/^ed25519-sha256:[0-9a-f]{64}$/.test(plan.transport.keyId)) {
      throw new Error('plan CNB transport binding is invalid');
    }
    exactKeys(plan.transport.catalog, ['payload', 'signature'], 'plan.transport.catalog');
    if (Date.parse(plan.expiresAt) > Date.parse(plan.transport.catalog.payload.expiresAt)) {
      throw new Error('plan outlives its signed CNB catalog');
    }
  }
  exactKeys(plan.release, ['repository', 'id', 'tag', 'version', 'targetCommitish', 'sourceRepository', 'sourceRevision'], 'plan.release');
  exactKeys(plan.assets, ['installer', 'checksum', 'candidate'], 'plan.assets');
  exactKeys(plan.installation, ['applicationPath', 'dataRoot', 'dataOwnershipAcknowledged'], 'plan.installation');
  exactKeys(plan.connection, ['client', 'configTarget', 'name', 'url', 'profile'], 'plan.connection');
  const signed = plan.publisher && plan.publisher.identity === 'developer-id';
  if (plan.transport && !signed) throw new Error('CNB requires a signed Developer ID release');
  exactKeys(plan.publisher, signed ? ['identity', 'gatekeeper', 'teamIdentifier'] : ['identity', 'gatekeeper'], 'plan.publisher');
  if (signed) requireString(plan.publisher.teamIdentifier, /^[A-Z0-9]{10}$/, 'plan publisher team');
  ['installer', 'checksum', 'candidate'].forEach((role) => {
    exactKeys(plan.assets[role], ['role', 'id', 'name', 'size', 'url', 'sha256'], 'plan.assets.' + role);
  });
  const created = new Date(plan.createdAt);
  const expires = new Date(plan.expiresAt);
  const now = new Date();
  if (!Number.isFinite(created.getTime()) || !Number.isFinite(expires.getTime()) ||
      expires <= created || expires - created > 120 * 60 * 1000 || now > expires) {
    throw new Error('plan is expired or has an invalid lifetime');
  }
  requireDesktopMCPURL(plan.connection.url);
  if (!['jishudb-agent-install-plan-v1', 'jishudb-agent-install-plan-v2', 'jishudb-agent-install-plan-v3'].includes(plan.schema) ||
      (rehearsal && (plan.releaseChannel !== 'candidate' || !signed)) ||
      (plan.schema !== 'jishudb-agent-install-plan-v1' && plan.launchMode !== 'agent-background') || plan.operation !== 'fresh-install' ||
      plan.platform !== 'darwin-arm64' || plan.release.repository !== 'x-aijishu/jishudb-desktop-releases' ||
      plan.release.sourceRepository !== 'x-aijishu/jishudb' ||
      plan.connection.profile !== 'default' ||
      plan.installation.dataOwnershipAcknowledged !== true ||
      (signed ? plan.publisher.gatekeeper !== 'accepted' : plan.publisher.identity !== 'none' || plan.publisher.gatekeeper !== 'manual-required')) {
    throw new Error('plan is outside the reviewed automatic-install contract');
  }
  if (rehearsal && candidateRequest(plan.release.tag, plan.release.sourceRevision).version !== plan.release.version) {
    throw new Error('candidate tag does not match the plan version');
  }
  if (!/^[1-9][0-9]*$/.test(plan.userId) || !Number.isSafeInteger(plan.release.id) || plan.release.id <= 0 ||
      !semverParts(plan.release.version) || (!rehearsal && plan.release.tag !== 'v' + plan.release.version) ||
      typeof plan.release.targetCommitish !== 'string' || plan.release.targetCommitish.length < 1 ||
      /[\u0000-\u001f\u007f]/.test(plan.release.targetCommitish)) {
    throw new Error('plan release or user identity is invalid');
  }
  requireString(plan.release.sourceRevision, /^[0-9a-f]{40}$/, 'plan source revision');
  const installerName = 'jishudb-desktop-' + plan.release.version + (signed ? '-darwin-arm64.dmg' : '-unsigned-darwin-arm64.dmg');
  const names = {
    installer: installerName,
    checksum: installerName + '.sha256',
    candidate: installerName + '.candidate.json',
  };
  ['installer', 'checksum', 'candidate'].forEach((role) => {
    const asset = plan.assets[role];
    if (asset.role !== role || !Number.isSafeInteger(asset.id) || asset.id <= 0 ||
        asset.name !== names[role] || !Number.isSafeInteger(asset.size) || asset.size <= 0 ||
        !/^[0-9a-f]{64}$/.test(asset.sha256) ||
        asset.url !== 'https://api.github.com/repos/x-aijishu/jishudb-desktop-releases/releases/assets/' + asset.id) {
      throw new Error('plan ' + role + ' asset identity is invalid');
    }
  });
  requireSafeText(plan.installation.applicationPath, 'plan application path');
  requireSafeText(plan.installation.dataRoot, 'plan data root');
  requireSafeText(plan.connection.client, 'plan client');
  requireSafeText(plan.connection.configTarget, 'plan config target');
  requireString(plan.connection.name, /^[A-Za-z0-9._-]{1,64}$/, 'plan connection name');
  return plan;
}

function releaseMatchesPlan(release, plan) {
  const rehearsal = plan.schema === 'jishudb-agent-install-plan-v3';
  if (release.immutable !== true || release.draft !== false || release.prerelease !== rehearsal ||
      release.id !== plan.release.id || release.tag_name !== plan.release.tag ||
      String(release.target_commitish) !== plan.release.targetCommitish) {
    throw new Error('release identity or immutable state changed');
  }
  ['installer', 'checksum', 'candidate'].forEach((role) => {
    const expected = plan.assets[role];
    const actual = exactAsset(release, expected.name, role);
    if (actual.id !== expected.id || actual.size !== expected.size || actual.url !== expected.url ||
        assetDigest(actual, role) !== expected.sha256) {
      throw new Error(role + ' asset changed after approval');
    }
  });
}

function valueAtPath(value, path) {
  return path.split('.').reduce((current, key) => current[key], value);
}

function run(argv) {
  const command = argv.shift();
  if (command === 'json-value') return String(valueAtPath(JSON.parse(argv[0]), argv[1]));
  if (command === 'plan-source') return readJSON(argv[0]).transport ? 'cnb' : 'github';
  if (command === 'cnb-plan-expired') {
    const plan = readJSON(argv[0]);
    return String(Boolean(plan.transport && Number.isFinite(Date.parse(plan.expiresAt)) && Date.now() >= Date.parse(plan.expiresAt)));
  }
  if (command === 'select-cnb') {
    const context = readJSON(argv[0]);
    const selected = selectFromReleases([context.release], null);
    selected.candidateRevision = context.envelope.payload.sourceRevision;
    selected.transport = context.transport;
    return JSON.stringify(selected);
  }
  if (command === 'download-slice') {
    return String(validateDownloadSlice(readText(argv[0]), argv[1], ...argv.slice(2).map(Number)));
  }
  if (command === 'count') {
    const value = readJSON(argv[0]);
    if (!Array.isArray(value)) throw new Error('release page must be an array');
    return String(value.length);
  }
  if (command === 'version-at-least') {
    const parse = (value) => {
      if (!/^\d+\.\d+(?:\.\d+)?$/.test(value)) throw new Error('platform version is invalid');
      const parts = value.split('.').map(Number);
      while (parts.length < 3) parts.push(0);
      return parts;
    };
    const current = parse(argv[0]);
    const minimum = parse(argv[1]);
    for (let index = 0; index < 3; index += 1) {
      if (current[index] > minimum[index]) return 'ok';
      if (current[index] < minimum[index]) throw new Error('platform version is unsupported');
    }
    return 'ok';
  }
  if (command === 'resolve-path') {
    const path = $.NSString.stringWithString(argv[0]);
    return unwrap(path.stringByResolvingSymlinksInPath.stringByStandardizingPath);
  }
  if (command === 'select') return JSON.stringify(selectRelease(argv));
  if (command === 'candidate-request') {
    candidateRequest(argv[0], argv[1]);
    return 'ok';
  }
  if (command === 'select-candidate') {
    return JSON.stringify(selectFromReleases([readJSON(argv[0])], candidateRequest(argv[1], argv[2])));
  }
  if (command === 'candidate') {
    validateCandidate(readJSON(argv[0]), readJSON(argv[1]));
    return 'ok';
  }
  if (command === 'create-plan') {
    const selected = readJSON(argv[0]);
    const candidate = validateCandidate(readJSON(argv[1]), selected);
    return JSON.stringify(createPlan(selected, candidate, argv.slice(2)), null, 2) + '\n';
  }
  if (command === 'validate-plan') {
    const plan = validatePlan(readJSON(argv[0]));
    if (plan.userId !== argv[1]) throw new Error('plan user does not match the current user');
    return 'ok';
  }
  if (command === 'value') return String(valueAtPath(readJSON(argv[0]), argv[1]));
  if (command === 'plan-value') return String(valueAtPath(validatePlan(readJSON(argv[0])), argv[1]));
  if (command === 'candidate-plan') {
    const plan = validatePlan(readJSON(argv[1]));
    const selected = {
      version: plan.release.version,
      candidateRevision: plan.release.sourceRevision,
      release: {prerelease: plan.schema === 'jishudb-agent-install-plan-v3'},
      installer: {
        name: plan.assets.installer.name,
        size: plan.assets.installer.size,
        state: 'uploaded',
        digest: 'sha256:' + plan.assets.installer.sha256,
      },
    };
    const candidate = validateCandidate(readJSON(argv[0]), selected);
    if (Object.keys(plan.publisher).some((key) => candidatePublisher(candidate)[key] !== plan.publisher[key])) throw new Error('candidate publisher does not match the approved plan');
    if ((candidate.agentBackgroundLaunch === 1) !== (plan.launchMode === 'agent-background')) throw new Error('Agent launch capability no longer matches the approved plan');
    if (candidate.revision !== plan.release.sourceRevision) throw new Error('candidate revision does not match the plan');
    return 'ok';
  }
  if (command === 'release-match') {
    releaseMatchesPlan(readJSON(argv[0]), validatePlan(readJSON(argv[1])));
    return 'ok';
  }
  if (command === 'redirect') {
    const source = $.NSURLComponents.componentsWithString(argv[0]);
    const target = $.NSURLComponents.componentsWithString(argv[1]);
    const targetUser = unwrap(target.user) || '';
    const targetPassword = unwrap(target.password) || '';
    const targetFragment = unwrap(target.fragment) || '';
    if (!source || !target || unwrap(source.scheme) !== 'https' || unwrap(source.host) !== 'api.github.com' ||
        !/^\/repos\/x-aijishu\/jishudb-desktop-releases\/releases\/assets\/[1-9][0-9]*$/.test(unwrap(source.path)) ||
        unwrap(target.scheme) !== 'https' || unwrap(target.host) !== 'release-assets.githubusercontent.com' ||
        targetUser !== '' || targetPassword !== '' || targetFragment !== '' ||
        !/^\/github-production-release-asset\/1316997274\//.test(unwrap(target.path))) {
      throw new Error('asset redirect is outside the reviewed GitHub release host');
    }
    return 'ok';
  }
  if (command === 'manifest') {
    const manifest = readJSON(argv[0]);
    if (manifest.version !== argv[1] || manifest.revision !== argv[2]) throw new Error('installed release manifest does not match the plan');
    return 'ok';
  }
  if (command === 'result') {
    if (argv[0] === 'failed') return JSON.stringify({status: 'failed', errorCategory: argv[1], message: argv[2], stage: argv[3]});
    if (argv[0] === 'waiting') {
      const plan = validatePlan(readJSON(argv[1]));
      return JSON.stringify({status: 'download_waiting', stage: 'download',
        errorCategory: argv[5] || 'github_rate_limited', planPath: argv[1], planSha256: argv[2],
        downloadedBytes: Number(argv[3]), totalBytes: plan.assets.installer.size,
        retryAfterSeconds: Number(argv[4]), next: 'wait_then_repeat_download_with_same_plan'});
    }
    if (argv[0] === 'download') {
      const plan = validatePlan(readJSON(argv[1]));
      const bytes = Number(argv[3]);
      return JSON.stringify({status: bytes === plan.assets.installer.size ? 'downloaded' : 'download_pending',
        stage: 'download', planPath: argv[1], planSha256: argv[2], downloadedBytes: bytes,
        totalBytes: plan.assets.installer.size, bytesThisStep: Number(argv[4]),
        next: bytes === plan.assets.installer.size ? 'execute' : 'repeat_download_with_same_plan'});
    }
    if (argv[0] === 'plan') {
      const plan = readJSON(argv[1]);
      return JSON.stringify({
        status: 'plan_ready',
        authorization: { status: 'caller_verification_required', basis: 'existing_user_request_or_new_confirmation' },
        next: 'download_when_authorized',
        planPath: argv[1],
        planSha256: argv[2],
        approval: {
          version: plan.release.version,
          expiresAt: plan.expiresAt,
          releaseChannel: plan.releaseChannel || 'stable',
          releaseTag: plan.release.tag,
          sourceRevision: plan.release.sourceRevision,
          releaseId: plan.release.id,
          installer: plan.assets.installer.name,
          installerSha256: plan.assets.installer.sha256,
          applicationPath: plan.installation.applicationPath,
          dataRoot: plan.installation.dataRoot,
          client: plan.connection.client,
          configTarget: plan.connection.configTarget,
          mcpUrl: plan.connection.url,
          profile: plan.connection.profile,
          launchMode: plan.launchMode || 'foreground',
          publisher: plan.publisher,
          releaseSource: plan.transport ? 'cnb' : 'github',
          ...(plan.transport ? {catalogSha256: plan.transport.payloadSha256,
            catalogExpiresAt: plan.transport.catalog.payload.expiresAt} : {}),
          coveredMutations: ['download', 'per-user install', 'Desktop launch', 'non-secret client entry'],
          userPresence: ['OS installation prompts', 'browser agreement and OAuth consent or existing-account login', 'owner verification where required', 'client trust'],
        },
      });
    }
    if (argv[0] === 'installed') {
      return JSON.stringify({status: 'installed', version: argv[1], applicationPath: argv[2], dataRoot: argv[3], mcpUrl: requireDesktopMCPURL(argv[4]), next: 'wait_for_desktop_and_user_onboarding'});
    }
  }
  throw new Error('unsupported helper command');
}
JXA
}

# CNB alone requires Node for Ed25519 verification; ordinary GitHub installs
# retain the existing zsh/JXA dependency contract.
cnb_bridge() {
  local output category message
  if ! output=$("$CNB_NODE" "${SCRIPT_ROOT}/install-macos-cnb.cjs" "$@"); then
    category=$(jxa json-value "$output" errorCategory 2>/dev/null) || category="cnb_transport_failed"
    message=$(jxa json-value "$output" message 2>/dev/null) || message="CNB transport helper failed"
    fail "$category" "$message"
  fi
  CNB_RESULT="$output"
}

cnb_prepare_context() {
  local root
  root=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/JishuDBCnbCatalog.XXXXXX")
  CLEANUP_PATHS+=("$root")
  CNB_CONTEXT="${root}/catalog.json"
  if [[ "$MODE" == plan ]]; then
    cnb_bridge discover "$CNB_CONTEXT"
  else
    cnb_bridge refresh "$CNB_CONTEXT" "$PLAN_PATH"
  fi
}

# Recheck the original authorization after slow transport/OS checks, without
# renewing its lifetime or trying to acquire the transaction lock a second time.
cnb_revalidate_approval() {
  [[ "$RELEASE_SOURCE" == cnb ]] || return 0
  [[ "$(file_sha256 "$PLAN_PATH")" == "$PLAN_SHA256" ]] || fail "plan_digest_mismatch" "approved plan changed during the transaction"
  jxa validate-plan "$PLAN_PATH" "$(/usr/bin/id -u)" >/dev/null || fail "plan_expired" "approved plan expired during the transaction"
  cnb_bridge verify-plan "$PLAN_PATH"
}

rate_limit_seconds() {
  local headers="$1" remaining reset retry_after now
  remaining=$(/usr/bin/awk 'tolower($1)=="x-ratelimit-remaining:" {gsub(/\r/, "", $2); print $2}' "$headers")
  reset=$(/usr/bin/awk 'tolower($1)=="x-ratelimit-reset:" {gsub(/\r/, "", $2); print $2}' "$headers")
  retry_after=$(/usr/bin/awk 'tolower($1)=="retry-after:" {gsub(/\r/, "", $2); print $2}' "$headers")
  now=$(/bin/date +%s)
  if [[ "$remaining" == 0 && "$reset" == <-> ]]; then
    print -- $(( reset > now ? reset - now : 1 ))
  elif [[ "$retry_after" == <-> ]]; then
    print -- "$retry_after"
  else
    print -- 0
  fi
}

api_get() {
  local url="$1" destination="$2" http_status retry_seconds=0
  if [[ "$RELEASE_SOURCE" == cnb ]]; then
    cnb_bridge release "$CNB_CONTEXT" "$url" "$destination"
    return
  fi
  local headers="${destination}.response-headers"
  assert_private_cache_file "$headers"
  CLEANUP_PATHS+=("$headers")
  http_status=$(/usr/bin/curl --silent --show-error --proto '=https' --tlsv1.2 \
    --connect-timeout 10 --max-time 30 --max-redirs 0 --max-filesize 16777216 \
    --header 'Accept: application/vnd.github+json' \
    --header "X-GitHub-Api-Version: ${API_VERSION}" \
    --header 'User-Agent: jishudb-agent-install/0.1' --dump-header "$headers" \
    --output "$destination" --write-out '%{http_code}' "$url") || {
      /bin/rm -f -- "$destination"
      fail "github_api_failed" "GitHub API request failed"
    }
  if [[ "$http_status" != "200" ]]; then
    /bin/rm -f -- "$destination"
    if [[ "$http_status" == "403" || "$http_status" == "429" ]]; then
      retry_seconds=$(rate_limit_seconds "$headers")
      if (( retry_seconds > 0 )); then
        if [[ "$MODE" == "download" ]]; then
          local partial="${PLAN_PATH:h}/installer.partial" bytes=0
          assert_private_cache_file "$partial"
          [[ ! -f "$partial" ]] || bytes=$(/usr/bin/stat -f '%z' "$partial")
          jxa result waiting "$PLAN_PATH" "$PLAN_SHA256" "$bytes" "$retry_seconds"
          exit 0
        fi
        fail "github_rate_limited" "GitHub API rate limit reached; wait ${retry_seconds} seconds before another request"
      fi
    fi
    fail "github_api_failed" "GitHub API returned HTTP ${http_status}"
  fi
}

asset_download() {
  local url="$1"
  local destination="$2"
  if [[ "$RELEASE_SOURCE" == cnb ]]; then
    /bin/rm -f -- "$destination"
    cnb_bridge asset "$CNB_CONTEXT" "$url" "$destination"
    return
  fi
  local headers="${destination}.headers"
  local first="${destination}.first"
  local http_status location
  /bin/rm -f -- "$destination" "$headers" "$first"
  http_status=$(/usr/bin/curl --silent --show-error --proto '=https' --tlsv1.2 \
    --connect-timeout 10 --max-time 30 --max-redirs 0 --max-filesize 16777216 \
    --header 'Accept: application/octet-stream' \
    --header "X-GitHub-Api-Version: ${API_VERSION}" \
    --header 'User-Agent: jishudb-agent-install/0.1' \
    --dump-header "$headers" --output "$first" --write-out '%{http_code}' "$url") ||
    fail "asset_download_failed" "GitHub asset request failed"
  if [[ "$http_status" == "200" ]]; then
    /bin/mv -- "$first" "$destination"
  elif [[ "$http_status" == "302" ]]; then
    location=$(/usr/bin/awk 'tolower($1)=="location:" {sub(/^[^:]*:[[:space:]]*/, ""); sub(/\r$/, ""); print; exit}' "$headers")
    [[ -n "$location" ]] || fail "invalid_asset_redirect" "asset redirect has no Location"
    jxa redirect "$url" "$location" >/dev/null || fail "invalid_asset_redirect" "asset redirect is outside the reviewed GitHub release host"
    http_status=$(/usr/bin/curl --silent --show-error --proto '=https' --tlsv1.2 \
      --connect-timeout 10 --max-time 30 --max-redirs 0 --max-filesize 16777216 \
      --header 'User-Agent:' \
      --output "$destination" --write-out '%{http_code}' "$location") ||
      fail "asset_download_failed" "GitHub release-asset request failed"
    [[ "$http_status" == "200" ]] || fail "asset_download_failed" "GitHub release-asset request returned HTTP ${http_status}"
  else
    fail "asset_download_failed" "GitHub asset request returned HTTP ${http_status}"
  fi
  /bin/rm -f -- "$headers" "$first"
}

file_sha256() {
  /usr/bin/shasum -a 256 "$1" | /usr/bin/awk '{print $1}'
}

assert_digest() {
  local path="$1" expected="$2" label="$3"
  [[ "$(file_sha256 "$path")" == "$expected" ]] || fail "digest_mismatch" "${label} SHA-256 does not match the approved release digest"
}

assert_size() {
  local path="$1" expected="$2" label="$3"
  [[ "$(/usr/bin/stat -f '%z' "$path")" == "$expected" ]] || fail "asset_size_mismatch" "${label} size does not match the GitHub API"
}

validate_bundle_symlinks() {
  local bundle="$1" label="$2" bundle_real link target resolved
  [[ -d "$bundle" && ! -L "$bundle" ]] || fail "installer_content_invalid" "${label} is not a regular application bundle"
  bundle_real=$(jxa resolve-path "$bundle") || fail "installer_content_invalid" "${label} path could not be resolved"
  while IFS= read -r -d '' link; do
    target=$(/usr/bin/readlink "$link") || fail "installer_content_invalid" "${label} contains an unreadable symlink"
    [[ -n "$target" && "$target" != /* ]] || fail "installer_content_invalid" "${label} contains an absolute or empty symlink"
    [[ -e "${link:h}/${target}" ]] || fail "installer_content_invalid" "${label} contains a dangling symlink"
    resolved=$(jxa resolve-path "${link:h}/${target}") || fail "installer_content_invalid" "${label} symlink target could not be resolved"
    case "$resolved" in
      "$bundle_real"/*) ;;
      *) fail "installer_content_invalid" "${label} contains an escaping symlink" ;;
    esac
  done < <(/usr/bin/find -P "$bundle" -type l -print0)
}

# AI-generated signature boundary: run only for a digest-bound Developer ID
# candidate, using the exact TeamIdentifier included in the approved plan.
verify_signed_artifact() {
  local target="$1" team="$2" kind="$3" signature_info
  /usr/bin/codesign --verify --deep --strict "$target" >/dev/null 2>&1 ||
    fail "signature_invalid" "Developer ID signature verification failed"
  signature_info=$(/usr/bin/codesign --display --verbose=4 "$target" 2>&1) ||
    fail "signature_invalid" "Developer ID signature could not be inspected"
  print -r -- "$signature_info" | /usr/bin/grep -Fqx "TeamIdentifier=${team}" ||
    fail "publisher_mismatch" "Developer ID team differs from the approved plan"
  print -r -- "$signature_info" | /usr/bin/grep -q '^Authority=Developer ID Application:' ||
    fail "signature_invalid" "Artifact lacks a Developer ID Application signature"
  if [[ "$kind" == "dmg" ]]; then
    /usr/sbin/spctl --assess --type open --context context:primary-signature "$target" >/dev/null 2>&1 ||
      fail "gatekeeper_rejected" "Gatekeeper rejected the signed DMG"
  else
    /usr/sbin/spctl --assess --type execute "$target" >/dev/null 2>&1 ||
      fail "gatekeeper_rejected" "Gatekeeper rejected the signed application"
  fi
}

create_transaction_root() {
  /usr/bin/mktemp -d "${TMPDIR:-/tmp}/JishuDBAgentInstall.XXXXXX"
}

port_is_available() {
  local port="$1"
  ! /usr/bin/nc -z -G 1 127.0.0.1 "$port" >/dev/null 2>&1
}

select_mcp_url() {
  local port
  for port in 8088 {8090..8104}; do
    if port_is_available "$port"; then
      print -r -- "http://127.0.0.1:${port}/mcp"
      return 0
    fi
  done
  return 1
}

write_endpoint_config() {
  local data_root="$1"
  local mcp_url="$2"
  local port="${${mcp_url#http://127.0.0.1:}%%/*}"
  [[ "$port" == "8088" || ( "$port" -ge 8090 && "$port" -le 8104 ) ]] ||
    fail "invalid_endpoint" "approved Desktop MCP endpoint is invalid"
  /bin/mkdir -m 700 -- "$data_root" || fail "endpoint_persistence_failed" "Desktop data root could not be created"
  local endpoint_path="${data_root}/${ENDPOINT_CONFIG_FILENAME}"
  [[ ! -e "$endpoint_path" ]] || fail "endpoint_conflict" "Desktop endpoint configuration appeared before launch"
  /usr/bin/printf '{\n  "localPort": %d,\n  "schemaVersion": %d\n}\n' "$port" "$ENDPOINT_CONFIG_SCHEMA" > "$endpoint_path" ||
    fail "endpoint_persistence_failed" "Desktop endpoint could not be persisted"
  /bin/chmod 600 "$endpoint_path"
}

run_plan() {
  [[ "$(/usr/bin/uname -s)" == "Darwin" && "$(/usr/bin/uname -m)" == "arm64" ]] || fail "unsupported_platform" "automatic macOS installation requires macOS arm64"
  [[ -n "$CLIENT" && -n "$CONFIG_TARGET" ]] || fail "invalid_arguments" "--client and --config-target are required in plan mode"
  [[ "$CONNECTION_NAME" =~ '^[A-Za-z0-9._-]{1,64}$' ]] || fail "invalid_arguments" "connection name is invalid"

  local evidence_root page_path count selected_path candidate_path checksum_path mcp_url
  local transaction_root target_plan digest installer_name installer_sha checksum_text expected_checksum
  evidence_root=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/JishuDBAgentEvidence.XXXXXX")
  CLEANUP_PATHS+=("$evidence_root")
  selected_path="${evidence_root}/selected.json"
  if [[ "$RELEASE_SOURCE" == cnb ]]; then
    [[ -z "$CANDIDATE_TAG" && -z "$CANDIDATE_REVISION" ]] || fail "invalid_arguments" "CNB catalogs support only approved stable releases"
    cnb_prepare_context
    jxa select-cnb "$CNB_CONTEXT" > "$selected_path" || fail "catalog_invalid" "CNB catalog has no eligible signed macOS release"
  elif [[ -n "$CANDIDATE_TAG" || -n "$CANDIDATE_REVISION" ]]; then
    jxa candidate-request "$CANDIDATE_TAG" "$CANDIDATE_REVISION" >/dev/null || fail "invalid_arguments" "candidate testing requires an exact tag and full source revision"
    page_path="${evidence_root}/candidate-release.json"
    api_get "${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/tags/${CANDIDATE_TAG}" "$page_path"
    jxa select-candidate "$page_path" "$CANDIDATE_TAG" "$CANDIDATE_REVISION" > "$selected_path" || fail "candidate_release_unavailable" "the requested immutable signed prerelease is not eligible; no stable fallback was attempted"
  else
    local -a pages
    pages=()
    local page
    for page in {1..$MAX_RELEASE_PAGES}; do
      page_path="${evidence_root}/releases-${page}.json"
      api_get "${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases?per_page=100&page=${page}" "$page_path"
      pages+=("$page_path")
      count=$(jxa count "$page_path") || fail "invalid_release_response" "release page is invalid"
      (( count < 100 )) && break
      (( page < MAX_RELEASE_PAGES )) || fail "pagination_bound" "release selection exceeded ${MAX_RELEASE_PAGES} pages"
    done
    jxa select "${pages[@]}" > "$selected_path" || fail "no_eligible_immutable_release" "no eligible immutable stable macOS release is available"
  fi
  candidate_path="${evidence_root}/candidate.json"
  checksum_path="${evidence_root}/checksum.txt"
  asset_download "$(jxa value "$selected_path" 'candidate.url')" "$candidate_path"
  asset_download "$(jxa value "$selected_path" 'checksum.url')" "$checksum_path"
  assert_size "$candidate_path" "$(jxa value "$selected_path" 'candidate.size')" "candidate"
  assert_size "$checksum_path" "$(jxa value "$selected_path" 'checksum.size')" "checksum"
  assert_digest "$candidate_path" "$(jxa value "$selected_path" 'candidate.digest' | /usr/bin/sed 's/^sha256://')" "candidate"
  assert_digest "$checksum_path" "$(jxa value "$selected_path" 'checksum.digest' | /usr/bin/sed 's/^sha256://')" "checksum"
  jxa candidate "$candidate_path" "$selected_path" >/dev/null || fail "invalid_candidate" "candidate contract is invalid"
  jxa version-at-least "$(/usr/bin/sw_vers -productVersion)" "$(jxa value "$candidate_path" 'minimumSystemVersion')" >/dev/null || fail "unsupported_platform" "macOS does not meet the release minimum version"
  local revision
  revision=$(jxa value "$candidate_path" 'revision')
  installer_name=$(jxa value "$selected_path" 'installer.name')
  installer_sha=$(jxa value "$selected_path" 'installer.digest' | /usr/bin/sed 's/^sha256://')
  checksum_text=$(<"$checksum_path")
  expected_checksum="${installer_sha}  ${installer_name}"
  [[ "$checksum_text" == "$expected_checksum" ]] || fail "invalid_checksum" "adjacent checksum content is not exact"
  mcp_url=$(select_mcp_url) || fail "endpoint_unavailable" "no free port exists in the bounded Desktop endpoint set"

  if [[ -z "$PLAN_PATH" ]]; then
    transaction_root=$(create_transaction_root)
    CLEANUP_PATHS+=("$transaction_root")
    PLAN_PATH="${transaction_root}/install-plan.json"
  else
    PLAN_PATH="${PLAN_PATH:A}"
    [[ ! -e "$PLAN_PATH" && ! -e "${PLAN_PATH:h}" ]] || fail "invalid_plan_path" "custom plan parent must be absent"
    /bin/mkdir -m 700 -p -- "${PLAN_PATH:h}"
    transaction_root="${PLAN_PATH:h}"
    CLEANUP_PATHS+=("$transaction_root")
  fi
  local app_path="${HOME}/Applications/JishuDB.app"
  local data_root="${HOME}/Library/Application Support/JishuDB"
  CONFIG_TARGET="${CONFIG_TARGET:A}"
  jxa create-plan "$selected_path" "$candidate_path" "$(/usr/bin/id -u)" "$app_path" "$data_root" "$CLIENT" "$CONFIG_TARGET" "$CONNECTION_NAME" "$mcp_url" > "$PLAN_PATH" ||
    fail "invalid_plan" "could not create the reviewed transaction plan"
  /bin/chmod 600 "$PLAN_PATH"
  local release_confirmation="${evidence_root}/release-confirmation.json"
  api_get "${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/$(jxa plan-value "$PLAN_PATH" 'release.id')" "$release_confirmation"
  jxa release-match "$release_confirmation" "$PLAN_PATH" >/dev/null || fail "release_drift" "release changed during plan creation"
  digest=$(file_sha256 "$PLAN_PATH")
  jxa result plan "$PLAN_PATH" "$digest"
  CLEANUP_PATHS=("$evidence_root")
  [[ -z "$CNB_CONTEXT" ]] || CLEANUP_PATHS+=("${CNB_CONTEXT:h}")
}

validate_approved_plan() {
  [[ -z "$CANDIDATE_TAG" && -z "$CANDIDATE_REVISION" ]] || fail "invalid_arguments" "candidate selection is plan-only; execute the unchanged approved plan"
  [[ "$(/usr/bin/uname -s)" == "Darwin" && "$(/usr/bin/uname -m)" == "arm64" ]] || fail "unsupported_platform" "automatic macOS installation requires macOS arm64"
  [[ -n "$PLAN_PATH" && "$PLAN_SHA256" =~ '^[0-9a-f]{64}$' ]] || fail "invalid_arguments" "--plan and a lowercase SHA-256 are required in download or execute mode"
  PLAN_PATH="${PLAN_PATH:A}"
  [[ -f "$PLAN_PATH" && ! -L "$PLAN_PATH" ]] || fail "invalid_plan" "plan must be a regular non-symlink file"
  [[ "$(/usr/bin/stat -f '%u' "$PLAN_PATH")" == "$(/usr/bin/id -u)" ]] || fail "invalid_plan" "plan is not owned by the current user"
  [[ "$(/usr/bin/stat -f '%Lp' "$PLAN_PATH")" == "600" ]] || fail "invalid_plan" "plan permissions must be 0600"
  [[ "$(file_sha256 "$PLAN_PATH")" == "$PLAN_SHA256" ]] || fail "plan_digest_mismatch" "plan SHA-256 does not match the approved digest"
  [[ "$(jxa cnb-plan-expired "$PLAN_PATH")" != true ]] || fail "plan_expired" "CNB approval expired; retained bytes do not renew approval"
  jxa validate-plan "$PLAN_PATH" "$(/usr/bin/id -u)" >/dev/null || fail "invalid_plan" "plan is expired or outside the reviewed contract"
  local approved_source
  approved_source=$(jxa plan-source "$PLAN_PATH") || fail "invalid_plan" "plan source cannot be read"
  if (( RELEASE_SOURCE_SPECIFIED == 1 )) && [[ "$RELEASE_SOURCE" != "$approved_source" ]]; then
    fail "release_source_mismatch" "release source differs from the unchanged approved plan"
  fi
  RELEASE_SOURCE="$approved_source"
  assert_release_source_available

  local transaction_root="${PLAN_PATH:h}"
  [[ -d "$transaction_root" && ! -L "$transaction_root" &&
     "$(/usr/bin/stat -f '%u:%Lp' "$transaction_root")" == "$(/usr/bin/id -u):700" ]] ||
    fail "unsafe_transaction" "plan directory must be private and owned by the current user"
  /bin/mkdir -m 700 -- "${transaction_root}/transfer.lock" 2>/dev/null ||
    fail "transaction_busy" "another operation or interrupted host owns this plan; inspect it before continuing"
  TRANSACTION_LOCK="${transaction_root}/transfer.lock"
  [[ "$RELEASE_SOURCE" != cnb ]] || cnb_prepare_context
}

# AI-generated file boundary: reject foreign files and links before using cached
# data. Cache presence never substitutes for complete size and digest validation.
assert_private_cache_file() {
  local target="$1"
  [[ ! -L "$target" ]] || fail "unsafe_cache" "cached asset must not be a symlink"
  if [[ -e "$target" ]]; then
    [[ -f "$target" && "$(/usr/bin/stat -f '%u:%Lp:%l' "$target")" == "$(/usr/bin/id -u):600:1" ]] ||
      fail "unsafe_cache" "cached asset must be a private current-user regular file without hard links"
  fi
}

run_download() {
  validate_approved_plan
  local root="${PLAN_PATH:h}" release_path partial_path installer_path url expected_size expected_sha
  local offset end chunk headers first http_status location curl_code=0 received added=0
  release_path="${root}/download-release.json"
  partial_path="${root}/installer.partial"
  installer_path="${root}/$(jxa plan-value "$PLAN_PATH" 'assets.installer.name')"
  assert_private_cache_file "$partial_path"
  assert_private_cache_file "$installer_path"
  assert_private_cache_file "$release_path"
  # One pre-download release snapshot per approved transaction. Execute fetches
  # the release again before and after complete-asset verification.
  if [[ ! -f "$release_path" ]]; then
    local release_draft
    release_draft=$(/usr/bin/mktemp "${root}/release-snapshot.XXXXXX")
    CLEANUP_PATHS+=("$release_draft")
    api_get "${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/$(jxa plan-value "$PLAN_PATH" 'release.id')" "$release_draft"
    jxa release-match "$release_draft" "$PLAN_PATH" >/dev/null || fail "release_drift" "release changed before download"
    /bin/mv -- "$release_draft" "$release_path"
  fi
  jxa release-match "$release_path" "$PLAN_PATH" >/dev/null || fail "release_drift" "cached release differs from the approved plan"
  expected_size=$(jxa plan-value "$PLAN_PATH" 'assets.installer.size')
  expected_sha=$(jxa plan-value "$PLAN_PATH" 'assets.installer.sha256')
  if [[ -f "$installer_path" ]]; then
    assert_size "$installer_path" "$expected_size" installer
    assert_digest "$installer_path" "$expected_sha" installer
    cnb_revalidate_approval
    assert_private_cache_file "${root}/download-location.txt"
    /bin/rm -f -- "$partial_path" "${root}/download-location.txt"
    jxa result download "$PLAN_PATH" "$PLAN_SHA256" "$expected_size" 0
    return
  fi
  if [[ ! -e "$partial_path" ]]; then
    ( setopt noclobber; : > "$partial_path" ) || fail "unsafe_cache" "partial file appeared concurrently"
  fi
  offset=$(/usr/bin/stat -f '%z' "$partial_path")
  (( offset <= expected_size )) || fail "asset_size_mismatch" "partial asset exceeds approved size"
  if (( offset < expected_size )); then
    end=$(( offset + DOWNLOAD_SLICE_BYTES - 1 ))
    (( end < expected_size )) || end=$(( expected_size - 1 ))
    local slice_root
    slice_root=$(/usr/bin/mktemp -d "${root}/slice.XXXXXX")
    CLEANUP_PATHS+=("$slice_root")
    chunk="${slice_root}/bytes"
    headers="${slice_root}/headers"
    first="${slice_root}/api-body"
    url=$(jxa plan-value "$PLAN_PATH" 'assets.installer.url')
    local location_cache="${root}/download-location.txt" cache_age using_cached_location=0
    assert_private_cache_file "$location_cache"
    http_status=""
    if [[ "$RELEASE_SOURCE" == cnb ]]; then
      cnb_bridge slice "$CNB_CONTEXT" "$url" "$chunk" "$headers" "$offset" "$end"
      /usr/bin/printf '%s\n' "$CNB_RESULT" > "${slice_root}/result.json"
      http_status=$(jxa value "${slice_root}/result.json" httpStatus)
      curl_code=$(jxa value "${slice_root}/result.json" curlCode)
    else
      if [[ -f "$location_cache" ]]; then
        cache_age=$(( $(/bin/date +%s) - $(/usr/bin/stat -f '%m' "$location_cache") ))
        if (( cache_age >= 0 && cache_age < DOWNLOAD_LOCATION_TTL_SECONDS )); then
          (( $(/usr/bin/stat -f '%z' "$location_cache") <= 8192 )) || fail "invalid_asset_redirect" "cached redirect exceeds the length limit"
          location=$(<"$location_cache")
          using_cached_location=1
          jxa redirect "$url" "$location" >/dev/null || fail "invalid_asset_redirect" "cached redirect is outside the reviewed GitHub host"
          http_status="302"
        else
          /bin/rm -- "$location_cache"
        fi
      fi
      if [[ -z "$http_status" ]]; then
        # Fetch a fresh signed redirect only when needed, rather than exhausting
        # anonymous GitHub API quota on every range. Never print the signed URL.
        http_status=$(/usr/bin/curl --silent --show-error --proto '=https' --tlsv1.2 \
          --connect-timeout 10 --max-time "$DOWNLOAD_SLICE_SECONDS" --max-redirs 0 \
          --max-filesize "$DOWNLOAD_SLICE_BYTES" --range "${offset}-${end}" \
          --header 'Accept: application/octet-stream' --header "X-GitHub-Api-Version: ${API_VERSION}" \
          --header 'User-Agent: jishudb-agent-install/0.1' \
          --dump-header "$headers" --output "$first" --write-out '%{http_code}' "$url") || curl_code=$?
        if [[ "$http_status" == "403" || "$http_status" == "429" ]]; then
          local retry_seconds
          retry_seconds=$(rate_limit_seconds "$headers")
          if (( retry_seconds > 0 )); then
            jxa result waiting "$PLAN_PATH" "$PLAN_SHA256" "$offset" "$retry_seconds"
            return
          fi
        fi
        if [[ "$http_status" == "302" && "$curl_code" == 0 ]]; then
          location=$(/usr/bin/awk 'tolower($1)=="location:" {sub(/^[^:]*:[[:space:]]*/, ""); sub(/\r$/, ""); print; exit}' "$headers")
          jxa redirect "$url" "$location" >/dev/null || fail "invalid_asset_redirect" "asset redirect is outside the reviewed GitHub host"
          /usr/bin/printf '%s' "$location" > "${slice_root}/location"
          /bin/mv -- "${slice_root}/location" "$location_cache"
        fi
      fi
      if [[ "$http_status" == "302" && "$curl_code" == 0 ]]; then
        http_status=$(/usr/bin/curl --silent --show-error --proto '=https' --tlsv1.2 \
          --connect-timeout 10 --max-time "$DOWNLOAD_SLICE_SECONDS" --max-redirs 0 \
          --max-filesize "$DOWNLOAD_SLICE_BYTES" --range "${offset}-${end}" \
          --header 'User-Agent:' --dump-header "$headers" \
          --output "$chunk" --write-out '%{http_code}' "$location") || curl_code=$?
      elif [[ "$http_status" == "206" ]]; then
        /bin/mv -- "$first" "$chunk"
      else
        fail "asset_download_failed" "GitHub asset request failed (curl ${curl_code}, HTTP ${http_status}); cached bytes were not advanced"
      fi
      if [[ "$http_status" == "403" || "$http_status" == "429" ]]; then
        local cdn_retry_seconds
        cdn_retry_seconds=$(rate_limit_seconds "$headers")
        if (( cdn_retry_seconds > 0 )); then
          jxa result waiting "$PLAN_PATH" "$PLAN_SHA256" "$offset" "$cdn_retry_seconds"
          return
        fi
        /bin/rm -f -- "$location_cache"
        if [[ "$http_status" == "403" && "$using_cached_location" == 1 ]]; then
          # Refresh an expired cached URL once. A newly issued URL failing the
          # same way is terminal, not an unbounded authorization retry loop.
          jxa result waiting "$PLAN_PATH" "$PLAN_SHA256" "$offset" 1 download_url_refresh_required
          return
        fi
      fi
      [[ "$http_status" == "206" ]] || fail "asset_download_failed" "GitHub CDN request failed (curl ${curl_code}, HTTP ${http_status}); cached bytes were not advanced"
    fi
    [[ -f "$chunk" ]] || fail "asset_download_failed" "download produced no data (curl ${curl_code}, HTTP ${http_status})"
    received=$(/usr/bin/stat -f '%z' "$chunk")
    jxa download-slice "$headers" "$http_status" "$offset" "$end" "$expected_size" "$received" "$curl_code" >/dev/null ||
      fail "invalid_download_slice" "download range was not valid (curl ${curl_code}, HTTP ${http_status}); cached bytes were not advanced"
    (( received > 0 )) || fail "download_stalled" "download made no progress within the bounded step"
    cnb_revalidate_approval
    /bin/cat -- "$chunk" >> "$partial_path"
    added="$received"
    offset=$(/usr/bin/stat -f '%z' "$partial_path")
  fi
  if (( offset == expected_size )); then
    CURRENT_STAGE="verification"
    assert_digest "$partial_path" "$expected_sha" installer
    cnb_revalidate_approval
    /bin/mv -- "$partial_path" "$installer_path"
    /bin/rm -f -- "${root}/download-location.txt"
  fi
  jxa result download "$PLAN_PATH" "$PLAN_SHA256" "$offset" "$added"
}

run_execute() {
  validate_approved_plan
  local app_path data_root release_id version revision installer_name mcp_url mcp_port
  app_path=$(jxa plan-value "$PLAN_PATH" 'installation.applicationPath')
  data_root=$(jxa plan-value "$PLAN_PATH" 'installation.dataRoot')
  release_id=$(jxa plan-value "$PLAN_PATH" 'release.id')
  version=$(jxa plan-value "$PLAN_PATH" 'release.version')
  revision=$(jxa plan-value "$PLAN_PATH" 'release.sourceRevision')
  installer_name=$(jxa plan-value "$PLAN_PATH" 'assets.installer.name')
  mcp_url=$(jxa plan-value "$PLAN_PATH" 'connection.url')
  mcp_port="${${mcp_url#http://127.0.0.1:}%%/*}"
  [[ "$app_path" == "${HOME}/Applications/JishuDB.app" && "$data_root" == "${HOME}/Library/Application Support/JishuDB" ]] || fail "invalid_plan" "installation destinations are not canonical"
  [[ ! -e "$app_path" && ! -e "$data_root" ]] || fail "existing_installation" "automatic installation requires absent application and data destinations"
  port_is_available "$mcp_port" || fail "endpoint_conflict" "the approved Desktop MCP port is no longer available; create a new plan"

  local transaction_root release_path installer_path checksum_path candidate_path mount_point staging_root staged_app manifest_path
  transaction_root="${PLAN_PATH:h}"
  release_path="${transaction_root}/release.json"
  installer_path="${transaction_root}/${installer_name}"
  checksum_path="${transaction_root}/$(jxa plan-value "$PLAN_PATH" 'assets.checksum.name')"
  candidate_path="${transaction_root}/$(jxa plan-value "$PLAN_PATH" 'assets.candidate.name')"
  mount_point="${transaction_root}/mount"
  staging_root="${HOME}/Applications/.JishuDB.installing.$(/usr/bin/uuidgen)"
  CLEANUP_PATHS+=("$checksum_path" "$candidate_path" "$release_path")
  assert_private_cache_file "$installer_path"
  [[ -f "$installer_path" ]] || fail "download_required" "run download with the approved plan until status is downloaded before execute"
  assert_private_cache_file "$checksum_path"
  assert_private_cache_file "$candidate_path"
  assert_private_cache_file "$release_path"
  [[ ! -e "$mount_point" && ! -L "$mount_point" ]] || fail "unsafe_transaction" "mount path already exists"

  api_get "${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/${release_id}" "$release_path"
  jxa release-match "$release_path" "$PLAN_PATH" >/dev/null || fail "release_drift" "release changed after approval"
  asset_download "$(jxa plan-value "$PLAN_PATH" 'assets.candidate.url')" "$candidate_path"
  asset_download "$(jxa plan-value "$PLAN_PATH" 'assets.checksum.url')" "$checksum_path"
  CURRENT_STAGE="verification"
  assert_size "$candidate_path" "$(jxa plan-value "$PLAN_PATH" 'assets.candidate.size')" "candidate"
  assert_size "$checksum_path" "$(jxa plan-value "$PLAN_PATH" 'assets.checksum.size')" "checksum"
  assert_size "$installer_path" "$(jxa plan-value "$PLAN_PATH" 'assets.installer.size')" "installer"
  assert_digest "$candidate_path" "$(jxa plan-value "$PLAN_PATH" 'assets.candidate.sha256')" "candidate"
  assert_digest "$checksum_path" "$(jxa plan-value "$PLAN_PATH" 'assets.checksum.sha256')" "checksum"
  assert_digest "$installer_path" "$(jxa plan-value "$PLAN_PATH" 'assets.installer.sha256')" "installer"
  jxa candidate-plan "$candidate_path" "$PLAN_PATH" >/dev/null || fail "invalid_candidate" "candidate does not match the approved plan"
  jxa version-at-least "$(/usr/bin/sw_vers -productVersion)" "$(jxa value "$candidate_path" 'minimumSystemVersion')" >/dev/null || fail "unsupported_platform" "macOS does not meet the release minimum version"
  local checksum_text expected_checksum
  checksum_text=$(<"$checksum_path")
  expected_checksum="$(jxa plan-value "$PLAN_PATH" 'assets.installer.sha256')  ${installer_name}"
  [[ "$checksum_text" == "$expected_checksum" ]] || fail "invalid_checksum" "adjacent checksum content is not exact"
  api_get "${API_ORIGIN}/repos/${RELEASE_REPOSITORY}/releases/${release_id}" "$release_path"
  jxa release-match "$release_path" "$PLAN_PATH" >/dev/null || fail "release_drift" "release changed during download"

  local signed_team=""
  if [[ "$(jxa plan-value "$PLAN_PATH" 'publisher.identity')" == "developer-id" ]]; then
    signed_team=$(jxa plan-value "$PLAN_PATH" 'publisher.teamIdentifier')
    verify_signed_artifact "$installer_path" "$signed_team" dmg
  fi
  CURRENT_STAGE="mount"
  CLEANUP_MOUNT="$mount_point"
  CLEANUP_PATHS+=("$mount_point" "$staging_root")
  /bin/mkdir -m 700 -- "$mount_point"
  /usr/bin/hdiutil attach -readonly -nobrowse -mountpoint "$mount_point" "$installer_path" >/dev/null || fail "installer_mount_failed" "verified DMG could not be mounted read-only"
  [[ -d "${mount_point}/JishuDB.app" && ! -L "${mount_point}/JishuDB.app" ]] || fail "installer_content_invalid" "DMG does not contain one regular JishuDB.app"
  local -a mounted_apps
  mounted_apps=("$mount_point"/*.app)
  (( ${#mounted_apps} == 1 )) || fail "installer_content_invalid" "DMG contains an ambiguous application set"
  validate_bundle_symlinks "${mount_point}/JishuDB.app" "mounted application bundle"
  [[ -z "$signed_team" ]] || verify_signed_artifact "${mount_point}/JishuDB.app" "$signed_team" app
  local bundle_id bundle_version runtime_binary
  bundle_id=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "${mount_point}/JishuDB.app/Contents/Info.plist")
  bundle_version=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "${mount_point}/JishuDB.app/Contents/Info.plist")
  [[ "$bundle_id" == "com.aijishu.jishudb" && "$bundle_version" == "$version" ]] || fail "installer_content_invalid" "bundle identity or version does not match the plan"
  runtime_binary="${mount_point}/JishuDB.app/Contents/Resources/runtime/jishudb"
  [[ -f "$runtime_binary" && ! -L "$runtime_binary" ]] || fail "installer_content_invalid" "packaged runtime is missing or unsafe"
  manifest_path="${mount_point}/JishuDB.app/Contents/Resources/runtime/RELEASE-MANIFEST.json"
  [[ -f "$manifest_path" && ! -L "$manifest_path" ]] || fail "installer_content_invalid" "release manifest is missing"
  jxa manifest "$manifest_path" "$version" "$revision" >/dev/null || fail "installer_content_invalid" "release manifest does not match the plan"

  CURRENT_STAGE="install"
  cnb_revalidate_approval
  /bin/mkdir -p -m 700 -- "${HOME}/Applications"
  /bin/mkdir -m 700 -- "$staging_root"
  /usr/bin/ditto --rsrc --extattr "${mount_point}/JishuDB.app" "${staging_root}/JishuDB.app" || fail "installer_copy_failed" "validated application bundle could not be staged"
  validate_bundle_symlinks "${staging_root}/JishuDB.app" "staged application bundle"
  [[ -z "$signed_team" ]] || verify_signed_artifact "${staging_root}/JishuDB.app" "$signed_team" app
  [[ ! -e "$app_path" ]] || fail "existing_installation" "application destination appeared during staging"
  cnb_revalidate_approval
  /bin/mv -- "${staging_root}/JishuDB.app" "$app_path"
  /usr/bin/hdiutil detach "$mount_point" >/dev/null || fail "installer_cleanup_failed" "DMG could not be detached"
  CLEANUP_MOUNT=""
  /bin/rmdir "$mount_point" "$staging_root" 2>/dev/null || true
  validate_bundle_symlinks "$app_path" "installed application bundle"
  [[ -z "$signed_team" ]] || verify_signed_artifact "$app_path" "$signed_team" app
  [[ -f "${app_path}/Contents/Resources/runtime/jishudb" && ! -L "${app_path}/Contents/Resources/runtime/jishudb" ]] || fail "installed_receipt_invalid" "installed runtime receipt is invalid"
  jxa manifest "${app_path}/Contents/Resources/runtime/RELEASE-MANIFEST.json" "$version" "$revision" >/dev/null || fail "installed_receipt_invalid" "installed release manifest does not match the plan"
  CURRENT_STAGE="launch"
  cnb_revalidate_approval
  write_endpoint_config "$data_root" "$mcp_url"
  if [[ "$(jxa plan-value "$PLAN_PATH" 'schema')" != "jishudb-agent-install-plan-v1" ]]; then
    /usr/bin/open -g "$app_path" --args --jishudb-agent-background || fail "desktop_launch_failed" "installed Desktop could not be launched in background"
  else
    /usr/bin/open "$app_path" || fail "desktop_launch_failed" "installed Desktop could not be launched"
  fi
  jxa result installed "$version" "$app_path" "$data_root" "$mcp_url"
}

# AI-generated: block unavailable sources before any discovery, cache access,
# or installation. A CNB request must never become an implicit GitHub request.
assert_release_source_available() {
  case "$RELEASE_SOURCE" in
    github) ;;
    cnb)
      CNB_NODE=$(command -v node) || fail "node_runtime_required" "CNB installation requires Node.js 22 or newer"
      "$CNB_NODE" -e 'process.exit(Number(process.versions.node.split(".")[0]) >= 22 ? 0 : 1)' ||
        fail "node_runtime_required" "CNB installation requires Node.js 22 or newer"
      [[ -f "${SCRIPT_ROOT}/install-macos-cnb.cjs" && -f "${SCRIPT_ROOT}/release-mirror-catalog.cjs" &&
         -f "${SCRIPT_ROOT}/release-mirror-trust.json" ]] ||
        fail "release_source_not_configured" "CNB verifier and independently approved trust must be bundled with this installer"
      ;;
    *)
      fail "invalid_release_source" "release source must be github or cnb"
      ;;
  esac
}

# Existing transactions resolve their approved source before requiring its tools.
if [[ "$MODE" == "plan" ]] || (( RELEASE_SOURCE_SPECIFIED == 1 )); then
  assert_release_source_available
fi

if [[ "$MODE" == "plan" ]]; then
  run_plan
elif [[ "$MODE" == "download" ]]; then
  run_download
else
  run_execute
fi
