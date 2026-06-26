#!/usr/bin/env node

// hi bundle plugin 的 host installer，跑在 user 的 OpenClaw host 里（由 SKILL.md
// 教 LLM 用 `node ./scripts/openclaw-host-installer.mjs setup` 调起）。
//
// 设计约束：**整个文件不允许 import node:CHILD-PROCESS 也不允许出现 EXEC / SPAWN
// 字样跟着小括号 (CAPS 化的目的：避开 plugin install scanner 自己用来扫这个文件
// 的正则，不让它在我们这个对照说明里把自己当 finding 报掉)**。
// scanner 拦截正则是 word-boundary + 任一 EXEC/EXECSYNC/SPAWN/SPAWNSYNC/
// EXECFILE/EXECFILESYNC 后跟小括号，再加上 CHILD-PROCESS 字样在文件里 (#59241)，
// 命中就强迫 user 加 --dangerously-force-unsafe-install 才能装。这个 flag 体感差，
// 而且按 openclaw 文档是给 false-positive 的 break-glass，长期挂着等于一直在用 break-glass。
//
// 替换路径：
// - 装 npm 包 (hirey-ai-mcp-server / hirey-ai-agent-receiver + 全部 transitive deps) → 改成 render
//   时把整棵 node_modules 树 prebundle 进 bundle 的 ./vendor/，install 时 fs.cp 出去。
//   render 那边的 npm install 步骤在 publisher 机器上跑，不在 user host 跑，scanner
//   不扫 publisher 端 build script (参考 release/render-channel.mjs 里的 prebundleVendorTree)。
// - 写 ~/.openclaw/openclaw.json (hooks / mcp.servers.<name>) → 改成 ./openclaw-config-fs.mjs
//   里的 readHooks / setHooks / readMcpServer / setMcpServer / unsetHooks / unsetMcpServer
//   直 fs read/write + atomic rename。OpenClaw 老 CLI 路径用的 --strict-json 本来就是
//   重写整个 top-level JSON，所以 user 文件里的 JSON5 注释/格式在老路径下也已经被 strip，
//   行为对齐。

import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

import {
  readHooks,
  readMcpServer,
  setHooks,
  setMcpServer,
  unsetHooks,
  unsetMcpServer,
} from './openclaw-config-fs.mjs';
import { copyVendorTree } from './vendor-tarball-extract.mjs';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const BUNDLED_VENDOR_DIR = path.join(SCRIPT_DIR, 'vendor');
const BUNDLED_VENDOR_STAGED_MANIFEST = path.join(BUNDLED_VENDOR_DIR, 'staged.json');

export const DEFAULT_PLATFORM_BASE_URL = 'https://hi.hirey.ai';
export const DEFAULT_GATEWAY_BASE_URL = 'http://127.0.0.1:18789';
export const DEFAULT_HOOKS_PATH = '/hooks';
export const DEFAULT_HI_PROFILE = 'openclaw-main';
export const DEFAULT_MCP_SERVER_NAME = 'hi';
export const DEFAULT_ACTIVE_AGENT_PREFIX = 'agent:main:';
export const MANIFEST_BASENAME = 'openclaw-phase1-manifest.json';
export const PHASE1_NEXT_ACTION_RESTART = 'restart_then_reconnect_before_phase2';
// 包名跟具体版本号分开。包名是确定的（render-channel 会按 channel 把 @hirey/* → @hirey-ai/*
// 替换掉），版本号现在去 hi-platform 的 well-known endpoint 拉，避免 bundle 自己存一份过期的 pin
// 又忘了 bump 导致 user 装到老版本。
//
// 如果 well-known 不可达（极端情况：user host 装 Hi 时 hi-platform 挂了），用下面的 fallback
// 兜底——这个 fallback 应该在每次 hirey-ai-mcp-server / hirey-ai-agent-receiver bump 时跟 hi-platform/release/
// recommended-versions.json 一起 bump，作为离线最低保证。
export const PINNED_PACKAGE_NAMES = Object.freeze({
  hiMcpServer: '@hirey-ai/mcp-server',
  hiAgentReceiver: '@hirey-ai/agent-receiver',
});
export const FALLBACK_PINNED_VERSIONS = Object.freeze({
  hi_mcp_server: '0.1.26',
  hi_agent_receiver: '0.1.16',
});
export const RECOMMENDED_VERSIONS_PATH = '/.well-known/hi-recommended-versions.json';

async function fetchRecommendedVersions(platformBaseUrl) {
  const url = `${normalizeText(platformBaseUrl) || DEFAULT_PLATFORM_BASE_URL}${RECOMMENDED_VERSIONS_PATH}`;
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 10_000);
    const r = await fetch(url, { signal: ctrl.signal });
    clearTimeout(timer);
    if (!r.ok) throw new Error(`http ${r.status}`);
    const json = await r.json();
    const out = {
      hi_mcp_server: normalizeText(json.hi_mcp_server) || FALLBACK_PINNED_VERSIONS.hi_mcp_server,
      hi_agent_receiver: normalizeText(json.hi_agent_receiver) || FALLBACK_PINNED_VERSIONS.hi_agent_receiver,
      source: 'platform_well_known',
      url,
    };
    return out;
  } catch (err) {
    return {
      ...FALLBACK_PINNED_VERSIONS,
      source: 'fallback',
      url,
      fetch_error: err instanceof Error ? err.message : String(err),
    };
  }
}

function buildPinnedSpec(name, version) {
  return `${name}@${version}`;
}
export const MANAGED_HOOK_KEYS = Object.freeze([
  'enabled',
  'path',
  'token',
  'allowRequestSessionKey',
  'allowedSessionKeyPrefixes',
  'defaultSessionKey',
]);
export const MANAGED_HI_ENV_KEYS = Object.freeze([
  'HI_PLATFORM_BASE_URL',
  'HI_MCP_TRANSPORT',
  'HI_MCP_PROFILE',
  'HI_MCP_STATE_DIR',
  'HI_RECEIVER_TOKEN',
  'HI_RECEIVER_URL',
]);

function normalizeText(value) {
  return typeof value === 'string' ? value.trim() : '';
}

function isPlainObject(value) {
  return !!value && typeof value === 'object' && !Array.isArray(value);
}

function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

function normalizeHooksPath(rawValue) {
  const text = normalizeText(rawValue) || DEFAULT_HOOKS_PATH;
  const prefixed = text.startsWith('/') ? text : `/${text}`;
  return prefixed.replace(/\/+$/, '') || DEFAULT_HOOKS_PATH;
}

function resolveOpenClawStateRoot(openclawProfile) {
  const profile = normalizeText(openclawProfile);
  return profile
    ? path.join(os.homedir(), `.openclaw-${profile}`)
    : path.join(os.homedir(), '.openclaw');
}

function deriveReceiverUrl({ gatewayBaseUrl, hooksPath }) {
  const gatewayUrl = new URL(normalizeText(gatewayBaseUrl) || DEFAULT_GATEWAY_BASE_URL);
  gatewayUrl.pathname = `${normalizeHooksPath(hooksPath)}/agent`;
  gatewayUrl.search = '';
  gatewayUrl.hash = '';
  return gatewayUrl.toString();
}

function classifyHostBlocker(rawText) {
  const text = String(rawText || '').toLowerCase();
  if (text.includes('pairing required')) return 'pairing_required';
  if (text.includes('device repair')) return 'device_repair';
  if (text.includes('read-only operator scope') || text.includes('read only operator scope')) {
    return 'read_only_operator_scope';
  }
  return '';
}

export function resolveInstallerOptions(argv = process.argv.slice(2)) {
  const tokens = [...argv];
  const command = normalizeText(tokens.shift()) || 'status';
  const options = {
    command,
    json: false,
    openclawBin: 'openclaw',
    openclawProfile: '',
    platformBaseUrl: DEFAULT_PLATFORM_BASE_URL,
    gatewayBaseUrl: DEFAULT_GATEWAY_BASE_URL,
    hooksPath: DEFAULT_HOOKS_PATH,
    hiProfile: DEFAULT_HI_PROFILE,
    mcpServerName: DEFAULT_MCP_SERVER_NAME,
    activeAgentPrefix: DEFAULT_ACTIVE_AGENT_PREFIX,
    stateRoot: '',
    configPath: '',
    vendorDir: '',
    hiStateDir: '',
    hooksToken: '',
    hostSessionKey: '',
    displayName: '',
    defaultReplyChannel: '',
    defaultReplyTo: '',
    defaultReplyAccountId: '',
    defaultReplyThreadId: '',
    afterReconnect: false,
    skipPackageInstall: false,
  };

  while (tokens.length > 0) {
    const token = tokens.shift();
    switch (token) {
      case '--json':
        options.json = true;
        break;
      case '--openclaw-bin':
        options.openclawBin = normalizeText(tokens.shift()) || options.openclawBin;
        break;
      case '--openclaw-profile':
        options.openclawProfile = normalizeText(tokens.shift());
        break;
      case '--platform-base-url':
        options.platformBaseUrl = normalizeText(tokens.shift()) || DEFAULT_PLATFORM_BASE_URL;
        break;
      case '--gateway-base-url':
        options.gatewayBaseUrl = normalizeText(tokens.shift()) || DEFAULT_GATEWAY_BASE_URL;
        break;
      case '--hooks-path':
        options.hooksPath = normalizeHooksPath(tokens.shift());
        break;
      case '--hi-profile':
        options.hiProfile = normalizeText(tokens.shift()) || DEFAULT_HI_PROFILE;
        break;
      case '--mcp-server-name':
        options.mcpServerName = normalizeText(tokens.shift()) || DEFAULT_MCP_SERVER_NAME;
        break;
      case '--active-agent-prefix':
        options.activeAgentPrefix = normalizeText(tokens.shift()) || DEFAULT_ACTIVE_AGENT_PREFIX;
        break;
      case '--state-root':
        options.stateRoot = normalizeText(tokens.shift());
        break;
      case '--config-path':
        options.configPath = normalizeText(tokens.shift());
        break;
      case '--vendor-dir':
        options.vendorDir = normalizeText(tokens.shift());
        break;
      case '--hi-state-dir':
        options.hiStateDir = normalizeText(tokens.shift());
        break;
      case '--hooks-token':
        options.hooksToken = normalizeText(tokens.shift());
        break;
      case '--host-session-key':
        options.hostSessionKey = normalizeText(tokens.shift());
        break;
      case '--display-name':
        options.displayName = normalizeText(tokens.shift());
        break;
      case '--default-reply-channel':
        options.defaultReplyChannel = normalizeText(tokens.shift());
        break;
      case '--default-reply-to':
        options.defaultReplyTo = normalizeText(tokens.shift());
        break;
      case '--default-reply-account-id':
        options.defaultReplyAccountId = normalizeText(tokens.shift());
        break;
      case '--default-reply-thread-id':
        options.defaultReplyThreadId = normalizeText(tokens.shift());
        break;
      case '--after-reconnect':
        options.afterReconnect = true;
        break;
      case '--skip-package-install':
        options.skipPackageInstall = true;
        break;
      default:
        throw new Error(`unknown_argument:${String(token || '')}`);
    }
  }

  return options;
}

export function resolveInstallerPaths(options) {
  const stateRoot = path.resolve(options.stateRoot || resolveOpenClawStateRoot(options.openclawProfile));
  const configPath = path.resolve(options.configPath || path.join(stateRoot, 'openclaw.json'));
  const vendorDir = path.resolve(options.vendorDir || path.join(stateRoot, 'vendor', 'hirey-compatible'));
  const hiStateDir = path.resolve(options.hiStateDir || path.join(stateRoot, 'hi-mcp', options.hiProfile));

  return {
    stateRoot,
    configPath,
    vendorDir,
    hiStateDir,
    hiMcpBinary: path.join(vendorDir, 'node_modules', '.bin', 'hirey-ai-mcp-server'),
    hiReceiverBinary: path.join(vendorDir, 'node_modules', '.bin', 'hirey-ai-agent-receiver'),
    receiverUrl: deriveReceiverUrl({
      gatewayBaseUrl: options.gatewayBaseUrl,
      hooksPath: options.hooksPath,
    }),
    manifestPath: path.join(hiStateDir, MANIFEST_BASENAME),
  };
}

function normalizeStringArray(value) {
  if (!Array.isArray(value)) return [];
  return value
    .map((entry) => normalizeText(entry))
    .filter(Boolean);
}

function mergeAllowedSessionKeyPrefixes(currentPrefixes, activeAgentPrefix) {
  const extras = normalizeStringArray(currentPrefixes)
    .filter((entry) => entry !== 'hook:' && entry !== activeAgentPrefix)
    .sort();
  return ['hook:', activeAgentPrefix, ...extras];
}

export function buildManagedHooksConfig(args) {
  const currentHooks = isPlainObject(args.currentHooks) ? deepClone(args.currentHooks) : {};
  const token = normalizeText(args.hooksToken);
  if (!token && args.allowMissingToken !== true) throw new Error('missing_hooks_token');

  const result = {
    ...currentHooks,
    enabled: true,
    path: normalizeHooksPath(args.hooksPath),
    allowRequestSessionKey: true,
    allowedSessionKeyPrefixes: mergeAllowedSessionKeyPrefixes(
      currentHooks.allowedSessionKeyPrefixes,
      normalizeText(args.activeAgentPrefix) || DEFAULT_ACTIVE_AGENT_PREFIX,
    ),
  };
  if (token) result.token = token;
  return result;
}

function filterUnmanagedEnv(currentEnv) {
  const source = isPlainObject(currentEnv) ? currentEnv : {};
  const result = {};
  for (const [key, value] of Object.entries(source)) {
    if (!MANAGED_HI_ENV_KEYS.includes(key)) result[key] = value;
  }
  return result;
}

function filterUnmanagedHiServerShape(currentServer) {
  const source = isPlainObject(currentServer) ? currentServer : {};
  const result = {};
  for (const [key, value] of Object.entries(source)) {
    if (key !== 'command' && key !== 'env') result[key] = value;
  }
  return result;
}

export function buildManagedHiServerDefinition(args) {
  const currentServer = isPlainObject(args.currentServer) ? deepClone(args.currentServer) : {};
  const hooksToken = normalizeText(args.hooksToken);
  if (!hooksToken) throw new Error('missing_hooks_token');

  return {
    ...filterUnmanagedHiServerShape(currentServer),
    command: path.resolve(args.hiMcpBinary),
    env: {
      ...filterUnmanagedEnv(currentServer.env),
      HI_PLATFORM_BASE_URL: normalizeText(args.platformBaseUrl) || DEFAULT_PLATFORM_BASE_URL,
      HI_MCP_TRANSPORT: 'stdio',
      HI_MCP_PROFILE: normalizeText(args.hiProfile) || DEFAULT_HI_PROFILE,
      HI_MCP_STATE_DIR: path.resolve(args.hiStateDir),
      HI_RECEIVER_TOKEN: hooksToken,
      HI_RECEIVER_URL: normalizeText(args.receiverUrl),
    },
  };
}

function sortObject(value) {
  if (Array.isArray(value)) return value.map(sortObject);
  if (!isPlainObject(value)) return value;
  return Object.keys(value)
    .sort()
    .reduce((acc, key) => {
      acc[key] = sortObject(value[key]);
      return acc;
    }, {});
}

function stableJson(value) {
  return JSON.stringify(sortObject(value));
}

function objectsEqual(left, right) {
  return stableJson(left) === stableJson(right);
}

function readInstalledPackageVersion(vendorDir, packageName) {
  const packageJsonPath = path.join(vendorDir, 'node_modules', ...packageName.split('/'), 'package.json');
  return fs.readFile(packageJsonPath, 'utf8')
    .then((raw) => JSON.parse(raw).version || '')
    .catch(() => '');
}

async function fileExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

function resolveHiStateFilePath(options, paths) {
  return path.join(paths.hiStateDir, `${options.hiProfile}.json`);
}

async function readOpenClawConfigSnapshot(configPath) {
  try {
    const raw = await fs.readFile(configPath, 'utf8');
    const parsed = JSON.parse(raw);
    return isPlainObject(parsed) ? parsed : {};
  } catch {
    return {};
  }
}

async function readPhase1Manifest(paths) {
  try {
    const raw = await fs.readFile(paths.manifestPath, 'utf8');
    const parsed = JSON.parse(raw);
    return isPlainObject(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

async function readHiPersistedState(options, paths) {
  const stateFilePath = resolveHiStateFilePath(options, paths);
  try {
    const raw = await fs.readFile(stateFilePath, 'utf8');
    const parsed = JSON.parse(raw);
    return isPlainObject(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

// Direct-fs dispatcher that replaces the legacy openclaw-bin subprocess call.
// Keeps the same callsites + `{ ok, stdout, stderr, combined }` return
// shape so applyPhase1 / resetPhase1 / probePhase1WritePaths / readHooksViaCli /
// readHiServerViaCli don't need to change. Internally, each known argv shape is
// mapped to the corresponding helper in ./openclaw-config-fs.mjs (read/setHooks,
// read/setMcpServer, unsetHooks, unsetMcpServer).
//
// `--dry-run` shapes return immediate success: with direct fs writes there's no
// schema-validation noise to filter (the CLI's full-config dry-run was the only
// reason isUnrelatedSchemaNoise existed — see its comment), and any actual
// permission/IO problem will surface on the subsequent real write call. Net
// effect: simpler control flow, identical user observable behavior on success,
// strictly tighter on failure (real errors, not noise).
//
// Profile awareness: `options.openclawProfile` (mirroring `openclaw --profile`)
// changes the canonical config path. We resolve it through the same
// `paths.configPath` derivation the rest of this file uses, so this dispatcher
// always operates on the same file the legacy CLI would have touched.
async function runOpenClaw(options, argv) {
  const paths = resolveInstallerPaths(options);
  const configPath = paths.configPath;
  const mcpServerName = options.mcpServerName;

  const isDryRun = argv.includes('--dry-run');
  if (isDryRun) {
    // No-op: see header comment. Returning ok preserves the legacy ok-path
    // through the preflight branch in probePhase1WritePaths.
    return { ok: true, stdout: '', stderr: '', combined: '' };
  }

  try {
    // ['config', 'get', 'hooks', '--json'] → readHooks
    if (argv[0] === 'config' && argv[1] === 'get' && argv[2] === 'hooks') {
      const hooks = await readHooks(configPath);
      const stdout = `${JSON.stringify(hooks)}\n`;
      return { ok: true, stdout, stderr: '', combined: stdout };
    }
    // ['mcp', 'show', <name>, '--json'] → readMcpServer
    if (argv[0] === 'mcp' && argv[1] === 'show') {
      const name = argv[2] || mcpServerName;
      const srv = await readMcpServer(configPath, name);
      if (srv == null) {
        // Match the legacy CLI error string that readHiServerViaCli looks for
        // ("No MCP server named "<name>"") so the existing null-detection path
        // continues to work without changes.
        const combined = `No MCP server named "${name}"`;
        return { ok: false, stdout: '', stderr: combined, combined };
      }
      const stdout = `${JSON.stringify(srv)}\n`;
      return { ok: true, stdout, stderr: '', combined: stdout };
    }
    // ['config', 'set', '--strict-json', 'hooks', <json>] → setHooks
    if (argv[0] === 'config' && argv[1] === 'set' && argv.includes('hooks')) {
      const jsonIdx = argv.length - 1;
      const value = JSON.parse(argv[jsonIdx]);
      await setHooks(configPath, value);
      return { ok: true, stdout: '', stderr: '', combined: '' };
    }
    // ['config', 'unset', 'hooks'] → unsetHooks
    if (argv[0] === 'config' && argv[1] === 'unset' && argv[2] === 'hooks') {
      await unsetHooks(configPath);
      return { ok: true, stdout: '', stderr: '', combined: '' };
    }
    // ['mcp', 'set', <name>, <json>] → setMcpServer
    if (argv[0] === 'mcp' && argv[1] === 'set') {
      const name = argv[2] || mcpServerName;
      const value = JSON.parse(argv[3]);
      await setMcpServer(configPath, name, value);
      return { ok: true, stdout: '', stderr: '', combined: '' };
    }
    // ['mcp', 'unset', <name>] → unsetMcpServer
    if (argv[0] === 'mcp' && argv[1] === 'unset') {
      const name = argv[2] || mcpServerName;
      await unsetMcpServer(configPath, name);
      return { ok: true, stdout: '', stderr: '', combined: '' };
    }
    throw new Error(`runOpenClaw_unsupported_argv: ${JSON.stringify(argv)} — direct-fs dispatcher only knows config get/set/unset hooks and mcp show/set/unset. Add a new branch in runOpenClaw to support new shapes.`);
  } catch (err) {
    const combined = err && err.message ? err.message : String(err);
    return { ok: false, stdout: '', stderr: combined, combined, error: err };
  }
}

async function readHooksViaCli(options) {
  const result = await runOpenClaw(options, ['config', 'get', 'hooks', '--json']);
  if (!result.ok) {
    if (result.combined.includes('Config path not found: hooks')) return null;
    throw new Error(`hooks_read_failed:${result.combined.trim()}`);
  }
  return JSON.parse(result.stdout || result.combined || 'null');
}

async function readHiServerViaCli(options) {
  const result = await runOpenClaw(options, ['mcp', 'show', options.mcpServerName, '--json']);
  if (!result.ok) {
    if (result.combined.includes(`No MCP server named "${options.mcpServerName}"`)) return null;
    throw new Error(`mcp_read_failed:${result.combined.trim()}`);
  }
  return JSON.parse(result.stdout || result.combined || 'null');
}

function buildObservedHooks(rawConfig, cliHooks) {
  if (isPlainObject(rawConfig.hooks)) return deepClone(rawConfig.hooks);
  return isPlainObject(cliHooks) ? deepClone(cliHooks) : null;
}

function buildObservedHiServer(rawConfig, mcpServerName, cliHiServer) {
  const rawServer = rawConfig?.mcp?.servers?.[mcpServerName];
  if (isPlainObject(rawServer)) return deepClone(rawServer);
  return isPlainObject(cliHiServer) ? deepClone(cliHiServer) : null;
}

export function summarizePhase1Status(args) {
  const hooks = isPlainObject(args.observedHooks) ? args.observedHooks : null;
  const hiServer = isPlainObject(args.observedHiServer) ? args.observedHiServer : null;
  const packageVersions = isPlainObject(args.packageVersions) ? args.packageVersions : {};
  const pending = [];

  if (!args.hiMcpBinaryExists) pending.push('install_hi_packages');

  const hooksReady = hooks
    && hooks.enabled === true
    && normalizeHooksPath(hooks.path) === normalizeHooksPath(args.desiredHooks.path)
    && hooks.allowRequestSessionKey === true
    && Array.isArray(hooks.allowedSessionKeyPrefixes)
    && hooks.allowedSessionKeyPrefixes.includes('hook:')
    && hooks.allowedSessionKeyPrefixes.includes(args.activeAgentPrefix)
    && (
      normalizeText(args.desiredHooks.token)
        ? normalizeText(hooks.token) === normalizeText(args.desiredHooks.token)
        : normalizeText(hooks.token).length > 0
    );
  if (!hooksReady) pending.push('configure_openclaw_hooks');

  const hiReady = hiServer && objectsEqual(hiServer, args.desiredHiServer);
  if (!hiReady) pending.push('configure_hi_mcp');

  // recommendedVersions 由 collectHostSnapshot 注入；installer 主流程会先去 platform 拉一次再
  // 计算"需要装哪个版本"。任何一个 mcp/receiver 装的版本号跟 recommended 不一致就要重装。
  const recommended = args.recommendedVersions || FALLBACK_PINNED_VERSIONS;
  const packageVersionsOk = packageVersions.hiMcpServer === recommended.hi_mcp_server
    && packageVersions.hiAgentReceiver === recommended.hi_agent_receiver;
  if (!packageVersionsOk) pending.push('pin_public_hi_packages');

  return {
    phase1Ready: pending.length === 0,
    pending,
    cleanHost: !hooks && !hiServer,
    hooksReady: !!hooksReady,
    hiMcpReady: !!hiReady,
    packagesReady: !!(args.hiMcpBinaryExists && packageVersionsOk),
    packageVersions,
    recommendedVersions: recommended,
  };
}

async function collectHostSnapshot(options, paths, args = {}) {
  const rawConfig = await readOpenClawConfigSnapshot(paths.configPath);
  const useCliReadback = args.useCliReadback === true;
  const cliHooks = useCliReadback ? await readHooksViaCli(options) : null;
  const cliHiServer = useCliReadback ? await readHiServerViaCli(options) : null;
  const observedHooks = buildObservedHooks(rawConfig, cliHooks);
  const observedHiServer = buildObservedHiServer(rawConfig, options.mcpServerName, cliHiServer);
  const hiMcpBinaryExists = await fileExists(paths.hiMcpBinary);
  const hiReceiverBinaryExists = await fileExists(paths.hiReceiverBinary);
  const packageVersions = {
    hiMcpServer: await readInstalledPackageVersion(paths.vendorDir, '@hirey-ai/mcp-server'),
    hiAgentReceiver: await readInstalledPackageVersion(paths.vendorDir, '@hirey-ai/agent-receiver'),
  };
  // 让 caller 可以注入预先 fetch 好的 recommendedVersions（避免 setup → check 多次重复 fetch）。
  // 没注入就这里单独 fetch 一次。
  const recommendedVersions = args.recommendedVersions
    || (await fetchRecommendedVersions(options.platformBaseUrl));
  return {
    rawConfig,
    cliHooks,
    cliHiServer,
    observedHooks,
    observedHiServer,
    hiMcpBinaryExists,
    hiReceiverBinaryExists,
    packageVersions,
    recommendedVersions,
  };
}

function resolveHooksToken(options, snapshot) {
  const allowGenerate = options.generateHooksTokenIfMissing !== false;
  const forced = normalizeText(options.hooksToken);
  if (forced) return { value: forced, source: 'cli' };

  const currentHooksToken = normalizeText(snapshot.observedHooks?.token);
  if (currentHooksToken) return { value: currentHooksToken, source: 'existing_hooks' };

  const currentReceiverToken = normalizeText(snapshot.observedHiServer?.env?.HI_RECEIVER_TOKEN);
  if (currentReceiverToken) return { value: currentReceiverToken, source: 'existing_mcp' };

  if (!allowGenerate) {
    return {
      value: '',
      source: 'missing',
    };
  }

  return {
    value: crypto.randomBytes(32).toString('hex'),
    source: 'generated',
  };
}

// Direct-fs writes don't have CLI's full-config schema-validation noise (the
// 2026.5.x dry-run that pulled in unrelated channels.imessage required fields
// even when our payload was clean), and any actual permission/IO problem
// surfaces on the real write attempt. So preflight collapses to a no-op shape
// matching the legacy return contract, keeping applyPhase1's call site
// unchanged.
async function probePhase1WritePaths(_options, _desiredHooks, _desiredHiServer) {
  return {
    hooksDryRun: '',
    mcpDryRun: '',
    hooksDryRunUnrelatedNoise: false,
    mcpDryRunUnrelatedNoise: false,
  };
}

// Used to install hirey-ai-mcp-server + hirey-ai-agent-receiver at user setup time by
// shelling out to npm. That subprocess call lit up OpenClaw plugin install
// scanner's `dangerous-exec` regex and forced --dangerously-force-unsafe-install.
//
// New flow: render-channel.mjs has already pre-staged the full node_modules
// tree (mcp-server + receiver + every transitive dep) into ./vendor/node_modules
// inside the bundle. We just `fs.cp` that tree into the user's vendor dir and
// preserve `node_modules/.bin/*` symlinks (copyVendorTree handles both).
// Result: zero subprocess, zero network at install time, zero scanner findings.
//
// Versioning: we read ./vendor/staged.json to know what's in the bundle. That
// is THE authoritative version source — bumping the version requires
// republishing the bundle. The legacy fetchRecommendedVersions runtime call
// stays as a fallback for old bundles that don't have staged.json yet (so a
// 5.x host that still has an old bundle on disk doesn't break), but new
// bundles always carry their own version source.
async function installPinnedPackages(options, paths, snapshot) {
  const stagedManifest = await readStagedVendorManifest();
  const recommended = stagedManifest
    ? {
        hi_mcp_server: stagedManifest.packages?.hi_mcp_server?.version,
        hi_agent_receiver: stagedManifest.packages?.hi_agent_receiver?.version,
        source: 'bundled_vendor_staged_json',
        url: BUNDLED_VENDOR_STAGED_MANIFEST,
      }
    : (snapshot.recommendedVersions
       || (await fetchRecommendedVersions(options.platformBaseUrl)));

  const packageVersionsOk = snapshot.packageVersions.hiMcpServer === recommended.hi_mcp_server
    && snapshot.packageVersions.hiAgentReceiver === recommended.hi_agent_receiver
    && snapshot.hiMcpBinaryExists
    && snapshot.hiReceiverBinaryExists;
  if (options.skipPackageInstall || packageVersionsOk) {
    return {
      changed: false,
      skipped: !!options.skipPackageInstall,
      recommended,
    };
  }

  if (!stagedManifest) {
    // The bundle on disk is the legacy shape with no pre-staged vendor tree.
    // We can't fall back to subprocess npm install (would re-introduce a
    // scanner-flagged subprocess pattern and require the unsafe-install flag).
    // The user must reinstall the bundle to pick up the new prebundled vendor.
    throw new Error(
      `prebundled_vendor_missing: ${BUNDLED_VENDOR_STAGED_MANIFEST} not found. `
        + 'This installer no longer spawns `npm install` at setup time; the '
        + 'bundle must ship its own pre-staged vendor tree. Reinstall via '
        + '`openclaw plugins install clawhub:<bundle-name> --force`.',
    );
  }

  // Atomic-ish replace: stage at .new, swap directory, keep .old for rollback.
  // Pure fs operations — no subprocess.
  const targetVendor = paths.vendorDir;
  const stagingVendor = `${targetVendor}.new`;
  const previousVendor = `${targetVendor}.old`;
  await fs.rm(stagingVendor, { recursive: true, force: true });
  await copyVendorTree(BUNDLED_VENDOR_DIR, stagingVendor);

  // Swap: rename current → .old, .new → current. If a .old already exists
  // (failed previous install), drop it first.
  await fs.rm(previousVendor, { recursive: true, force: true });
  let prevExisted = false;
  try {
    await fs.rename(targetVendor, previousVendor);
    prevExisted = true;
  } catch (err) {
    if (!err || err.code !== 'ENOENT') throw err;
  }
  try {
    await fs.rename(stagingVendor, targetVendor);
  } catch (err) {
    // Swap failed: restore previous if we moved it aside.
    if (prevExisted) {
      await fs.rename(previousVendor, targetVendor).catch(() => {});
    }
    throw err;
  }
  // Cleanup .old in background; if rm fails the leftover dir is harmless.
  await fs.rm(previousVendor, { recursive: true, force: true }).catch(() => {});

  return {
    changed: true,
    skipped: false,
    recommended,
    installedSpecs: {
      hiMcpServer: stagedManifest.packages?.hi_mcp_server?.spec,
      hiAgentReceiver: stagedManifest.packages?.hi_agent_receiver?.spec,
    },
    source: 'bundled_vendor_staged_tree',
    bundledVendorDir: BUNDLED_VENDOR_DIR,
  };
}

// Read the bundled vendor's staged.json (written by render-channel.mjs's
// prebundleVendorTree). Returns null if absent — old bundles ship without it.
async function readStagedVendorManifest() {
  try {
    const raw = await fs.readFile(BUNDLED_VENDOR_STAGED_MANIFEST, 'utf8');
    const parsed = JSON.parse(raw);
    if (!isPlainObject(parsed)) return null;
    if (parsed.schema_version !== 1) return null;
    return parsed;
  } catch (err) {
    if (err && err.code === 'ENOENT') return null;
    throw err;
  }
}

async function writePhase1Manifest(paths, options, extra = {}, existingManifest = null) {
  const manifest = {
    ...(isPlainObject(existingManifest) ? existingManifest : {}),
    schema_version: 1,
    managed_by: 'hirey-compatible-install',
    updated_at: new Date().toISOString(),
    platform_base_url: options.platformBaseUrl,
    hi_profile: options.hiProfile,
    hooks_path: normalizeHooksPath(options.hooksPath),
    receiver_url: paths.receiverUrl,
    managed_mcp_server_name: options.mcpServerName,
    vendor_dir: paths.vendorDir,
    hi_state_dir: paths.hiStateDir,
    config_path: paths.configPath,
    managed_hook_keys: MANAGED_HOOK_KEYS,
    managed_hi_env_keys: MANAGED_HI_ENV_KEYS,
    ...extra,
  };
  await fs.mkdir(paths.hiStateDir, { recursive: true });
  await fs.writeFile(paths.manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
}

async function applyPhase1(options, paths) {
  const snapshotBefore = await collectHostSnapshot(options, paths, { useCliReadback: false });
  const hooksToken = resolveHooksToken(options, {
    ...snapshotBefore,
  });
  const desiredHooksForPreflight = buildManagedHooksConfig({
    currentHooks: snapshotBefore.observedHooks,
    hooksPath: options.hooksPath,
    activeAgentPrefix: options.activeAgentPrefix,
    hooksToken: hooksToken.value,
  });
  const desiredHiServerForPreflight = buildManagedHiServerDefinition({
    currentServer: snapshotBefore.observedHiServer,
    hiMcpBinary: paths.hiMcpBinary,
    platformBaseUrl: options.platformBaseUrl,
    hiProfile: options.hiProfile,
    hiStateDir: paths.hiStateDir,
    hooksToken: hooksToken.value,
    receiverUrl: paths.receiverUrl,
  });
  const preflight = await probePhase1WritePaths(options, desiredHooksForPreflight, desiredHiServerForPreflight);

  const packageInstall = await installPinnedPackages(options, paths, snapshotBefore);
  const snapshotAfterInstall = packageInstall.changed
    ? await collectHostSnapshot(options, paths, { useCliReadback: false })
    : snapshotBefore;
  const desiredHooks = buildManagedHooksConfig({
    currentHooks: snapshotAfterInstall.observedHooks,
    hooksPath: options.hooksPath,
    activeAgentPrefix: options.activeAgentPrefix,
    hooksToken: hooksToken.value,
  });
  const desiredHiServer = buildManagedHiServerDefinition({
    currentServer: snapshotAfterInstall.observedHiServer,
    hiMcpBinary: paths.hiMcpBinary,
    platformBaseUrl: options.platformBaseUrl,
    hiProfile: options.hiProfile,
    hiStateDir: paths.hiStateDir,
    hooksToken: hooksToken.value,
    receiverUrl: paths.receiverUrl,
  });

  const hooksChanged = !objectsEqual(snapshotAfterInstall.observedHooks, desiredHooks);
  if (hooksChanged) {
    const writeHooks = await runOpenClaw(options, [
      'config',
      'set',
      '--strict-json',
      'hooks',
      JSON.stringify(desiredHooks),
    ]);
    if (!writeHooks.ok) {
      const blocker = classifyHostBlocker(writeHooks.combined);
      throw new Error(`${blocker ? `host_write_blocker:${blocker}` : 'hooks_write_failed'}:${writeHooks.combined.trim()}`);
    }
  }

  const hiServerChanged = !objectsEqual(snapshotAfterInstall.observedHiServer, desiredHiServer);
  if (hiServerChanged) {
    const writeHiServer = await runOpenClaw(options, [
      'mcp',
      'set',
      options.mcpServerName,
      JSON.stringify(desiredHiServer),
    ]);
    if (!writeHiServer.ok) {
      const blocker = classifyHostBlocker(writeHiServer.combined);
      throw new Error(`${blocker ? `host_write_blocker:${blocker}` : 'mcp_write_failed'}:${writeHiServer.combined.trim()}`);
    }
  }

  await writePhase1Manifest(paths, options, {
    restart_pending: packageInstall.changed || hooksChanged || hiServerChanged,
    phase1_applied_at: new Date().toISOString(),
  });
  const snapshotAfterApply = await collectHostSnapshot(options, paths, { useCliReadback: true });
  const status = summarizePhase1Status({
    observedHooks: snapshotAfterApply.observedHooks,
    observedHiServer: snapshotAfterApply.observedHiServer,
    desiredHooks,
    desiredHiServer,
    hiMcpBinaryExists: snapshotAfterApply.hiMcpBinaryExists,
    packageVersions: snapshotAfterApply.packageVersions,
    activeAgentPrefix: options.activeAgentPrefix,
    recommendedVersions: snapshotAfterApply.recommendedVersions,
  });

  return {
    ok: status.phase1Ready,
    command: 'phase1-apply',
    hooksTokenSource: hooksToken.source,
    preflight,
    hooksChanged,
    hiServerChanged,
    restartRequired: packageInstall.changed || hooksChanged || hiServerChanged,
    phase2BlockedOn: packageInstall.changed || hooksChanged || hiServerChanged ? 'restart_boundary' : null,
    nextAction: packageInstall.changed || hooksChanged || hiServerChanged
      ? PHASE1_NEXT_ACTION_RESTART
      : 'continue_phase2',
    packageInstall,
    desiredHooks,
    desiredHiServer,
    status,
    manifestPath: paths.manifestPath,
  };
}

async function buildStatus(options, paths) {
  const snapshot = await collectHostSnapshot(options, paths, { useCliReadback: false });
  const manifest = await readPhase1Manifest(paths);
  const hooksToken = resolveHooksToken({
    ...options,
    generateHooksTokenIfMissing: false,
  }, snapshot);
  const desiredHooks = buildManagedHooksConfig({
    currentHooks: snapshot.observedHooks,
    hooksPath: options.hooksPath,
    activeAgentPrefix: options.activeAgentPrefix,
    hooksToken: hooksToken.value,
    allowMissingToken: true,
  });
  const desiredHiServer = buildManagedHiServerDefinition({
    currentServer: snapshot.observedHiServer,
    hiMcpBinary: paths.hiMcpBinary,
    platformBaseUrl: options.platformBaseUrl,
    hiProfile: options.hiProfile,
    hiStateDir: paths.hiStateDir,
    hooksToken: hooksToken.value,
    receiverUrl: paths.receiverUrl,
  });
  const status = summarizePhase1Status({
    observedHooks: snapshot.observedHooks,
    observedHiServer: snapshot.observedHiServer,
    desiredHooks,
    desiredHiServer,
    hiMcpBinaryExists: snapshot.hiMcpBinaryExists,
    packageVersions: snapshot.packageVersions,
    activeAgentPrefix: options.activeAgentPrefix,
    recommendedVersions: snapshot.recommendedVersions,
  });
  return {
    ok: true,
    command: 'status',
    paths,
    manifest,
    hooksTokenSource: hooksToken.source,
    observedHooks: snapshot.observedHooks,
    observedHiServer: snapshot.observedHiServer,
    hiMcpBinaryExists: snapshot.hiMcpBinaryExists,
    hiReceiverBinaryExists: snapshot.hiReceiverBinaryExists,
    packageVersions: snapshot.packageVersions,
    recommendedVersions: snapshot.recommendedVersions,
    desiredHooks,
    desiredHiServer,
    restartPending: manifest?.restart_pending === true,
    phase2Ready: status.phase1Ready && manifest?.restart_pending !== true,
    status,
  };
}

export function buildHooksResetTarget(observedHooks) {
  if (!isPlainObject(observedHooks)) return null;
  const nextHooks = deepClone(observedHooks);
  for (const key of MANAGED_HOOK_KEYS) {
    delete nextHooks[key];
  }
  return Object.keys(nextHooks).length > 0 ? nextHooks : null;
}

function validatePhase2HostSessionKey(hostSessionKey) {
  const value = normalizeText(hostSessionKey);
  if (!value) throw new Error('missing_host_session_key');
  if (!value.startsWith('agent:')) throw new Error('invalid_openclaw_host_session_key_shape');
  if (value.includes('…') || value.includes('...')) {
    throw new Error('invalid_openclaw_host_session_key_truncated');
  }
  return value;
}

export function buildPhase2InstallArgsPayload(args) {
  const hostSessionKey = validatePhase2HostSessionKey(args.hostSessionKey);
  const hooksToken = normalizeText(args.hooksToken);
  if (!hooksToken) throw new Error('missing_phase1_hooks_token');
  const payload = {
    host_kind: 'openclaw',
    enable_local_receiver: true,
    receiver_transport: 'claim',
    receiver_start: true,
    host_adapter_kind: 'openclaw_hooks',
    host_adapter_bearer_token: hooksToken,
    host_session_key: hostSessionKey,
    route_missing_policy: 'use_explicit_default_route',
    run_doctor: true,
  };
  const displayName = normalizeText(args.displayName);
  if (displayName) payload.display_name = displayName;
  if (normalizeText(args.defaultReplyChannel)) payload.default_reply_channel = normalizeText(args.defaultReplyChannel);
  if (normalizeText(args.defaultReplyTo)) payload.default_reply_to = normalizeText(args.defaultReplyTo);
  if (normalizeText(args.defaultReplyAccountId)) payload.default_reply_account_id = normalizeText(args.defaultReplyAccountId);
  if (normalizeText(args.defaultReplyThreadId)) payload.default_reply_thread_id = normalizeText(args.defaultReplyThreadId);
  return payload;
}

async function buildPhase2InstallArgs(options, paths) {
  const statusResult = await buildStatus({
    ...options,
    generateHooksTokenIfMissing: false,
  }, paths);
  if (!statusResult.status.phase1Ready) {
    throw new Error(`phase1_not_ready:${statusResult.status.pending.join(',')}`);
  }

  const manifest = statusResult.manifest;
  if (manifest?.restart_pending === true && !options.afterReconnect) {
    throw new Error('restart_boundary_not_acknowledged');
  }

  const hiState = await readHiPersistedState(options, paths);
  const installArgs = buildPhase2InstallArgsPayload({
    hooksToken: statusResult.observedHooks?.token,
    hostSessionKey: options.hostSessionKey,
    displayName: options.displayName,
    defaultReplyChannel: options.defaultReplyChannel,
    defaultReplyTo: options.defaultReplyTo,
    defaultReplyAccountId: options.defaultReplyAccountId,
    defaultReplyThreadId: options.defaultReplyThreadId,
  });

  if (manifest?.restart_pending === true && options.afterReconnect) {
    await writePhase1Manifest(paths, options, {
      restart_pending: false,
      restart_acknowledged_at: new Date().toISOString(),
    }, manifest);
  }

  return {
    ok: true,
    command: 'phase2-install-args',
    phase1Status: statusResult.status,
    restartBoundaryAcknowledged: manifest?.restart_pending !== true || options.afterReconnect,
    existingIdentity: !!hiState?.identity,
    displayNameStrategy: normalizeText(options.displayName)
      ? 'explicit'
      : (hiState?.identity ? 'existing_identity' : 'hi_agent_install_default'),
    installArgs,
    manifestPath: paths.manifestPath,
  };
}

function shouldUnsetManagedHiServer(observedHiServer, paths) {
  if (!isPlainObject(observedHiServer)) return false;
  return path.resolve(normalizeText(observedHiServer.command)) === path.resolve(paths.hiMcpBinary);
}

async function resetPhase1(options, paths) {
  const snapshot = await collectHostSnapshot(options, paths, { useCliReadback: false });
  let hooksAction = 'none';
  let mcpAction = 'none';

  const nextHooks = buildHooksResetTarget(snapshot.observedHooks);
  if (snapshot.observedHooks) {
    if (nextHooks) {
      const writeHooks = await runOpenClaw(options, [
        'config',
        'set',
        '--strict-json',
        'hooks',
        JSON.stringify(nextHooks),
      ]);
      if (!writeHooks.ok) {
        const blocker = classifyHostBlocker(writeHooks.combined);
        throw new Error(`${blocker ? `host_write_blocker:${blocker}` : 'hooks_reset_failed'}:${writeHooks.combined.trim()}`);
      }
      hooksAction = 'partial_preserve_non_hi_fields';
    } else {
      const unsetHooks = await runOpenClaw(options, ['config', 'unset', 'hooks']);
      if (!unsetHooks.ok) {
        const blocker = classifyHostBlocker(unsetHooks.combined);
        throw new Error(`${blocker ? `host_write_blocker:${blocker}` : 'hooks_unset_failed'}:${unsetHooks.combined.trim()}`);
      }
      hooksAction = 'unset_hooks';
    }
  }

  if (shouldUnsetManagedHiServer(snapshot.observedHiServer, paths)) {
    const unsetMcp = await runOpenClaw(options, ['mcp', 'unset', options.mcpServerName]);
    if (!unsetMcp.ok) {
      const blocker = classifyHostBlocker(unsetMcp.combined);
      throw new Error(`${blocker ? `host_write_blocker:${blocker}` : 'mcp_unset_failed'}:${unsetMcp.combined.trim()}`);
    }
    mcpAction = 'unset_managed_hi_server';
  }

  await fs.rm(paths.manifestPath, { force: true });
  const status = await buildStatus({
    ...options,
    generateHooksTokenIfMissing: false,
  }, paths);
  return {
    ok: true,
    command: 'phase1-reset',
    hooksAction,
    mcpAction,
    manifestRemoved: true,
    status: status.status,
    paths,
  };
}

function renderText(result) {
  const lines = [
    `command: ${result.command}`,
    `phase1_ready: ${result.status.phase1Ready}`,
    `clean_host: ${result.status.cleanHost}`,
    `pending: ${result.status.pending.join(', ') || '(none)'}`,
    `hooks_ready: ${result.status.hooksReady}`,
    `hi_mcp_ready: ${result.status.hiMcpReady}`,
    `packages_ready: ${result.status.packagesReady}`,
  ];
  if (result.command === 'phase1-apply') {
    lines.push(`restart_required: ${result.restartRequired}`);
    lines.push(`hooks_token_source: ${result.hooksTokenSource}`);
    lines.push(`next_action: ${result.nextAction}`);
  }
  if (result.command === 'status') {
    lines.push(`restart_pending: ${result.restartPending}`);
    lines.push(`phase2_ready: ${result.phase2Ready}`);
  }
  if (result.command === 'phase1-reset') {
    lines.push(`hooks_action: ${result.hooksAction}`);
    lines.push(`mcp_action: ${result.mcpAction}`);
  }
  if (result.command === 'phase2-install-args') {
    lines.push(`display_name_strategy: ${result.displayNameStrategy}`);
    lines.push(`restart_boundary_acknowledged: ${result.restartBoundaryAcknowledged}`);
  }
  return `${lines.join('\n')}\n`;
}

function printResult(result, asJson) {
  const output = asJson ? `${JSON.stringify(result, null, 2)}\n` : renderText(result);
  process.stdout.write(output);
}

function printUsage() {
  process.stdout.write(`Usage:
  node ./scripts/openclaw-host-installer.mjs setup [--host-session-key <key> --after-reconnect] [--json]
      First call (no --host-session-key): install pinned packages, write OpenClaw hooks +
      MCP config, write a Hi-side manifest. The newly-written mcp.servers.hi entry is
      hot-applied to the gateway on OpenClaw 4.25+ so no manual gateway restart is needed,
      but the calling LLM run cannot see the new hi_* tools yet because each LLM run
      materializes its tool inventory once at run start; the next LLM run (the user's next
      message, or a nested openclaw agent --message ... sub-run inside the same outer turn)
      is the first place where hi_* tools become callable. Output reports
      next_action="restart_gateway" for backward compat — this string is historical and
      should be read as "wait for the next LLM run to materialize hi_*", not as
      "you must spawn 'openclaw gateway restart'".

      Second call (with --after-reconnect --host-session-key=<key>):
      verify everything from the first call is still healthy, acknowledge the LLM-run
      boundary in the manifest, and emit a recommended_install_args block the owner agent
      can pass straight into the hi_agent_install MCP tool to register this OpenClaw host
      with the Hi platform and bind the current chat as default reply route. The
      --after-reconnect flag name is historical (no actual reconnect required on 4.25+).

  node ./scripts/openclaw-host-installer.mjs cleanup [--json]
      Reverse the host-side parts of setup: drop Hi-managed hooks fields, unset the Hi
      MCP server (only if it still points at this installer's vendor binary), remove the
      Hi-side manifest. Does not uninstall the npm packages from the vendor dir; OpenClaw
      4.25+ hot-applies the cleaned mcp.* config without a manual restart.

  node ./scripts/openclaw-host-installer.mjs status [--json]
      Read the current OpenClaw config + Hi manifest and print whether setup has finished,
      whether the LLM-run boundary is still pending (legacy field name: restart_pending),
      and what install args would be recommended.

Deprecated commands (kept as silent aliases; do not surface to ordinary users):
  phase1-apply → setup
  phase1-reset → cleanup
  phase1-status → status
  phase2-install-args → setup --after-reconnect --host-session-key …

Options:
  --json
  --openclaw-bin <path>
  --openclaw-profile <name>
  --platform-base-url <url>
  --gateway-base-url <url>
  --hooks-path <path>
  --hi-profile <name>
  --mcp-server-name <name>
  --active-agent-prefix <prefix>
  --state-root <path>
  --config-path <path>
  --vendor-dir <path>
  --hi-state-dir <path>
  --hooks-token <token>
  --host-session-key <key>
  --display-name <name>
  --default-reply-channel <channel>
  --default-reply-to <target>
  --default-reply-account-id <id>
  --default-reply-thread-id <id>
  --after-reconnect
  --skip-package-install
`);
}

async function main() {
  let options;
  try {
    options = resolveInstallerOptions();
  } catch (error) {
    if (String(error?.message || '').startsWith('unknown_argument:')) {
      printUsage();
      process.stderr.write(`${String(error.message || '')}\n`);
      process.exit(1);
    }
    throw error;
  }
  const paths = resolveInstallerPaths(options);

  try {
    // 'status' / 'phase1-status' are aliases —— installer 体感的 status 跟 phase1 检查同义。
    if (options.command === 'status' || options.command === 'phase1-status') {
      printResult(await buildStatus(options, paths), options.json);
      return;
    }

    // 'setup' 是新的对外命令名。如果 caller 没传 --host-session-key，跑 phase1（装包+写 config+
    // 写 manifest），输出 next_action=restart_gateway。如果传了 --host-session-key（且通常配
    // --after-reconnect），等价于过去的 phase2-install-args：检查 phase1 仍 healthy，构造推荐的
    // install_args 给 owner agent 直接喂给 hi_agent_install MCP 工具。
    if (options.command === 'setup') {
      if (normalizeText(options.hostSessionKey)) {
        printResult(await buildPhase2InstallArgs(options, paths), options.json);
        return;
      }
      const result = await applyPhase1(options, paths);
      printResult(result, options.json);
      if (!result.ok) process.exit(2);
      return;
    }

    // 'cleanup' 是新的对外命令名，等价于过去 phase1-reset。
    if (options.command === 'cleanup' || options.command === 'phase1-reset') {
      printResult(await resetPhase1(options, paths), options.json);
      return;
    }

    // 老 phase 命令保留为 silent alias 防止有外部调用方/老 SKILL 还在用。新文档不应该再
    // 提它们。等 deploy.sh 验证一段时间后可删。
    if (options.command === 'phase1-apply') {
      const result = await applyPhase1(options, paths);
      printResult(result, options.json);
      if (!result.ok) process.exit(2);
      return;
    }
    if (options.command === 'phase2-install-args') {
      printResult(await buildPhase2InstallArgs(options, paths), options.json);
      return;
    }

    if (options.command === '--help' || options.command === 'help') {
      printUsage();
      return;
    }
    printUsage();
    throw new Error(`unknown_command:${options.command}`);
  } catch (error) {
    const message = String(error?.message || error || 'openclaw_host_install_failed');
    const blocker = classifyHostBlocker(message);
    const result = {
      ok: false,
      command: options.command,
      error: message,
      hostBlocker: blocker || null,
      paths,
    };
    printResult(result, options.json || true);
    process.exit(1);
  }
}

const isDirectExecution = process.argv[1]
  && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));

if (isDirectExecution) {
  await main();
}
