'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_SOURCE_PACKAGE = '@okki-global/okki-go';
const DEFAULT_CHANNEL_CODE = 'organic';
const DEFAULT_SKILL_VERSION = '1.3.3';
const DEFAULT_SKILL_RUNTIME = 'unknown';

function firstLine(value) {
  return String(value || '').trim().split(/\r?\n/)[0];
}

function cleanHeaderValue(value) {
  const normalized = firstLine(value).replace(/[\u0000-\u001f\u007f]/g, '');
  return normalized ? normalized.slice(0, 160) : '';
}

function readJsonFileSafe(filePath) {
  if (!filePath || !fs.existsSync(filePath)) return {};
  try {
    const parsed = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed : {};
  } catch (_) {
    return {};
  }
}

function getConfigHome(env = process.env) {
  if (env.XDG_CONFIG_HOME) return env.XDG_CONFIG_HOME;
  const home = env.HOME || os.homedir();
  return home ? path.join(home, '.config') : '';
}

function getOkkiConfigDir(options = {}) {
  const configHome = options.configHome || getConfigHome(options.env || process.env);
  return configHome ? path.join(configHome, 'okki-go') : '';
}

function defaultSkillRoot() {
  return path.resolve(__dirname, '..', '..');
}

function readInstallIdFromFile(configDir) {
  if (!configDir) return '';
  const installIdPath = path.join(configDir, 'install-id');
  if (!fs.existsSync(installIdPath)) return '';
  try {
    return cleanHeaderValue(fs.readFileSync(installIdPath, 'utf8'));
  } catch (_) {
    return '';
  }
}

function pick(...values) {
  for (const value of values) {
    const cleaned = cleanHeaderValue(value);
    if (cleaned) return cleaned;
  }
  return '';
}

function resolveRuntimeAttribution(options = {}) {
  const env = options.env || process.env;
  const skillRoot = options.skillRoot || defaultSkillRoot();
  const configDir = getOkkiConfigDir(options);
  const attribution = readJsonFileSafe(options.attributionPath || path.join(configDir, 'install-attribution.json'));
  const manifest = readJsonFileSafe(options.manifestPath || path.join(skillRoot, '.okki-go-manifest.json'));

  const sourcePackage = pick(
    env.OKKIGO_SOURCE_PACKAGE,
    env.OKKI_GO_SOURCE_PACKAGE,
    attribution.sourcePackage,
    attribution.source_package,
    manifest.sourcePackage,
    manifest.source_package,
    DEFAULT_SOURCE_PACKAGE
  );
  const channelCode = pick(
    env.OKKIGO_CHANNEL_CODE,
    env.OKKI_GO_CHANNEL_CODE,
    attribution.channelCode,
    attribution.channel_code,
    manifest.channelCode,
    manifest.channel_code,
    DEFAULT_CHANNEL_CODE
  );
  const campaignId = pick(
    env.OKKIGO_CAMPAIGN_ID,
    env.OKKI_GO_CAMPAIGN_ID,
    attribution.campaignId,
    attribution.campaign_id,
    manifest.campaignId,
    manifest.campaign_id
  );
  const installId = pick(
    env.OKKIGO_INSTALL_ID,
    env.OKKI_GO_INSTALL_ID,
    attribution.installId,
    attribution.install_id,
    manifest.installId,
    manifest.install_id,
    readInstallIdFromFile(configDir)
  );
  const skillVersion = pick(
    env.OKKIGO_SKILL_VERSION,
    attribution.skillVersion,
    attribution.skill_version,
    manifest.version,
    DEFAULT_SKILL_VERSION
  );
  const runtime = pick(
    env.OKKIGO_SKILL_RUNTIME,
    attribution.runtime,
    manifest.runtime,
    DEFAULT_SKILL_RUNTIME
  );

  const isWrapper = Boolean(
    (sourcePackage && sourcePackage !== DEFAULT_SOURCE_PACKAGE) ||
    (channelCode && channelCode !== DEFAULT_CHANNEL_CODE) ||
    campaignId
  );

  return {
    installId,
    skillVersion,
    runtime,
    sourceType: isWrapper ? 'npm_wrapper' : '',
    sourcePackage,
    channelCode,
    campaignId,
    agent: cleanHeaderValue(env.OKKIGO_AGENT),
    agentModel: cleanHeaderValue(env.OKKIGO_AGENT_MODEL)
  };
}

function runtimeAttributionHeaders(options = {}) {
  const attribution = resolveRuntimeAttribution(options);
  const headers = {
    'X-Okki-Skill-Version': attribution.skillVersion,
    'X-Okki-Skill-Runtime': attribution.runtime
  };

  if (attribution.installId) headers['X-Okki-Install-Id'] = attribution.installId;

  if (attribution.sourceType) {
    headers['X-Okki-Source-Type'] = attribution.sourceType;
    if (attribution.sourcePackage) headers['X-Okki-Source-Package'] = attribution.sourcePackage;
    if (attribution.channelCode) headers['X-Okki-Channel-Code'] = attribution.channelCode;
    if (attribution.campaignId) headers['X-Okki-Campaign-Id'] = attribution.campaignId;
  }

  if (attribution.agent) headers['X-Okki-Agent'] = attribution.agent;
  if (attribution.agentModel) headers['X-Okki-Agent-Model'] = attribution.agentModel;

  return headers;
}

function curlHeaderArgumentLines(headers = runtimeAttributionHeaders()) {
  const lines = [];
  for (const [name, value] of Object.entries(headers)) {
    if (!value) continue;
    lines.push('-H', `${name}: ${value}`);
  }
  return lines;
}

function main() {
  const mode = process.argv[2] || '--json';
  if (mode === '--json') {
    process.stdout.write(`${JSON.stringify(runtimeAttributionHeaders(), null, 2)}\n`);
    return;
  }
  if (mode === '--curl-lines') {
    const lines = curlHeaderArgumentLines();
    if (lines.length > 0) process.stdout.write(`${lines.join('\n')}\n`);
    return;
  }
  if (mode === '--curl-null') {
    const lines = curlHeaderArgumentLines();
    if (lines.length > 0) process.stdout.write(`${lines.join('\0')}\0`);
    return;
  }
  process.stderr.write('Usage: node scripts/lib/runtime-attribution.js [--json|--curl-lines|--curl-null]\n');
  process.exit(2);
}

if (require.main === module) {
  main();
}

module.exports = {
  DEFAULT_SOURCE_PACKAGE,
  curlHeaderArgumentLines,
  resolveRuntimeAttribution,
  runtimeAttributionHeaders
};
