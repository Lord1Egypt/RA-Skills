#!/usr/bin/env node

import { existsSync, promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createSign } from 'node:crypto';
import {
  buildGrowthRunnerCommand,
  buildOpenClawCronAddCommand,
  deriveSchedulerProofPathFromStatePath,
  deriveStatePathFromConfigPath,
  getActionMode,
  getAutomationConfig,
  getDefaultSourceCommand,
  getOpenClawCronEditDeliveryCommandFromInspection,
  buildHermesCronCreateCommand,
  inspectHermesCronInstall,
  inspectOpenClawCronInstall,
  repairOpenClawCronDeliveryStore,
} from './openclaw-growth-shared.mjs';
import { applyOpenClawSecretRefs, loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';

const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const DEFAULT_TEMPLATE_PATH = 'data/openclaw-growth-engineer/config.example.json';
const DEFAULT_HEARTBEAT_PATH = 'HEARTBEAT.md';
const DEFAULT_SCHEDULER_PROOF_PATH = 'data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl';
const HEARTBEAT_MARKER_START = '<!-- openclaw-growth-engineer:start -->';
const HEARTBEAT_MARKER_END = '<!-- openclaw-growth-engineer:end -->';
const ANALYTICSCLI_PACKAGE_SPEC = process.env.ANALYTICSCLI_CLI_PACKAGE || '@analyticscli/cli';
const ANALYTICSCLI_NPM_PREFIX =
  process.env.ANALYTICSCLI_NPM_PREFIX ||
  (process.env.HOME ? path.join(process.env.HOME, '.local') : path.join(process.cwd(), '.analyticscli-npm'));
const RUNTIME_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ASC_TIMEOUT_SECONDS = '120';
const ACCOUNT_SIGNAL_CONNECTORS = [
  'stripe',
  'lemonsqueezy',
  'adapty',
  'superwall',
  'google-play',
  'datadog',
  'bugsnag',
  'intercom',
  'zendesk',
  'apple-search-ads',
  'google-ads',
  'meta-ads',
  'tiktok-ads',
  'vercel',
  'cloudflare',
  'resend',
  'customerio',
  'mailchimp',
  'appfollow',
  'apptweak',
  'linear',
  'postiz',
];
const SUPPORTED_CONNECTORS = ['analytics', 'github', 'asc', 'revenuecat', 'paddle', 'seo', 'sentry', 'coolify', ...ACCOUNT_SIGNAL_CONNECTORS];
const ACCOUNT_SIGNAL_SECRET_ENVS = {
  stripe: ['STRIPE_API_KEY'],
  lemonsqueezy: ['LEMON_SQUEEZY_API_KEY'],
  adapty: ['ADAPTY_API_KEY'],
  superwall: ['SUPERWALL_API_KEY'],
  'google-play': ['GOOGLE_PLAY_SERVICE_ACCOUNT_JSON'],
  datadog: ['DATADOG_API_KEY', 'DATADOG_APP_KEY'],
  bugsnag: ['BUGSNAG_AUTH_TOKEN'],
  intercom: ['INTERCOM_ACCESS_TOKEN'],
  zendesk: ['ZENDESK_SUBDOMAIN', 'ZENDESK_EMAIL', 'ZENDESK_API_TOKEN'],
  'apple-search-ads': ['APPLE_SEARCH_ADS_REFRESH_TOKEN'],
  'google-ads': ['GOOGLE_ADS_DEVELOPER_TOKEN', 'GOOGLE_ADS_CLIENT_ID', 'GOOGLE_ADS_CLIENT_SECRET', 'GOOGLE_ADS_REFRESH_TOKEN'],
  'meta-ads': ['META_ADS_ACCESS_TOKEN'],
  'tiktok-ads': ['TIKTOK_ADS_ACCESS_TOKEN'],
  vercel: ['VERCEL_ACCESS_TOKEN'],
  cloudflare: ['CLOUDFLARE_API_TOKEN'],
  resend: ['RESEND_API_KEY'],
  customerio: ['CUSTOMERIO_APP_API_KEY'],
  mailchimp: ['MAILCHIMP_API_KEY'],
  appfollow: ['APPFOLLOW_API_TOKEN'],
  apptweak: ['APPTWEAK_API_TOKEN'],
  linear: ['LINEAR_API_KEY'],
  postiz: ['POSTIZ_API_KEY'],
};

type ShellResult = {
  ok: boolean;
  code: number | null;
  stdout: string;
  stderr: string;
};

function printHelpAndExit(exitCode, reason = null) {
  if (reason) {
    process.stderr.write(`${reason}\n\n`);
  }
  process.stdout.write(`
OpenClaw Growth Start

Bootstraps setup and first run in one deterministic flow:
1) Ensure config exists (auto-bootstrap from template when missing)
2) Run preflight
3) If preflight passes, run first pass

Usage:
  node scripts/openclaw-growth-start.mjs [options]

Options:
  --config <file>        Config path (default: ${DEFAULT_CONFIG_PATH})
  --project <id>         Optional AnalyticsCLI project ID pin for generated source commands
  --asc-app <id>         Optional ASC app ID filter (defaults to all accessible apps)
  --connectors <list>    Install/enable connector helpers (${SUPPORTED_CONNECTORS.join(',')},all)
  --only-connectors <list>
                         Limit live preflight checks to ${SUPPORTED_CONNECTORS.join(',')}
  --setup-only           Run bootstrap + preflight only (skip first run)
  --no-test-connections  Skip live API smoke checks in preflight
  --openclaw-cron <mode> Configure OpenClaw Gateway cron: auto, enable, require, disable (default: auto)
  --openclaw-cron-schedule <expr>
                         Cron expression for OpenClaw Gateway cron (default: */30 * * * *)
  --openclaw-cron-tz <tz>
                         Timezone for OpenClaw Gateway cron (default: TZ or UTC)
  --progress-json        Emit machine-readable setup progress to stderr
  --help, -h             Show help
`);
  process.exit(exitCode);
}

function resolveDefaultConfigPath() {
  const explicit = String(process.env.OPENCLAW_GROWTH_CONFIG_PATH || '').trim();
  if (explicit) return explicit;
  const homeConfigPath = process.env.HOME ? path.join(process.env.HOME, 'data/openclaw-growth-engineer/config.json') : '';
  const homeStatePath = process.env.HOME ? path.join(process.env.HOME, 'data/openclaw-growth-engineer/state.json') : '';
  if (homeConfigPath && existsSync(homeConfigPath) && existsSync(homeStatePath)) return homeConfigPath;
  if (!existsSync(DEFAULT_CONFIG_PATH) && homeConfigPath && existsSync(homeConfigPath)) return homeConfigPath;
  return DEFAULT_CONFIG_PATH;
}

function parseArgs(argv) {
  const args = {
    config: resolveDefaultConfigPath(),
    project: '',
    ascApp: '',
    run: true,
    testConnections: true,
    connectors: [],
    onlyConnectors: [],
    openclawCron: String(process.env.OPENCLAW_GROWTH_OPENCLAW_CRON || 'auto').trim().toLowerCase(),
    openclawCronSchedule: '',
    openclawCronTimezone: '',
    progressJson: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    const next = argv[i + 1];
    if (token === '--') {
      continue;
    } else if (token === '--config') {
      args.config = next || args.config;
      i += 1;
    } else if (token === '--project') {
      args.project = String(next || '').trim();
      i += 1;
    } else if (token === '--asc-app') {
      args.ascApp = String(next || '').trim();
      i += 1;
    } else if (token === '--connectors') {
      args.connectors = parseConnectorList(next || '');
      i += 1;
    } else if (token === '--only-connectors') {
      args.onlyConnectors = parseConnectorList(next || '');
      i += 1;
    } else if (token === '--setup-only') {
      args.run = false;
    } else if (token === '--no-test-connections') {
      args.testConnections = false;
    } else if (token === '--openclaw-cron') {
      args.openclawCron = String(next || '').trim().toLowerCase() || 'auto';
      i += 1;
    } else if (token === '--enable-openclaw-cron') {
      args.openclawCron = 'enable';
    } else if (token === '--no-openclaw-cron') {
      args.openclawCron = 'disable';
    } else if (token === '--openclaw-cron-schedule') {
      args.openclawCronSchedule = String(next || '').trim();
      i += 1;
    } else if (token === '--openclaw-cron-tz') {
      args.openclawCronTimezone = String(next || '').trim();
      i += 1;
    } else if (token === '--progress-json') {
      args.progressJson = true;
    } else if (token === '--help' || token === '-h') {
      printHelpAndExit(0);
    } else {
      printHelpAndExit(1, `Unknown argument: ${token}`);
    }
  }

  args.openclawCron = validateOpenClawCronMode(args.openclawCron);
  return args;
}

function validateOpenClawCronMode(value) {
  const mode = String(value || 'auto').trim().toLowerCase();
  if (['auto', 'enable', 'require', 'disable'].includes(mode)) return mode;
  printHelpAndExit(1, `Invalid --openclaw-cron mode: ${value}. Use auto, enable, require, or disable.`);
}

function normalizeConnectorKey(value) {
  const normalized = String(value || '').trim().toLowerCase().replace(/[_\s]+/g, '-');
  if (!normalized) return null;
  if (normalized === 'all') return 'all';
  if (['analytics', 'analyticscli', 'product-analytics', 'events'].includes(normalized)) return 'analytics';
  if (['github', 'gh', 'github-code', 'codebase', 'code-access'].includes(normalized)) return 'github';
  if (['asc', 'asc-cli', 'app-store-connect', 'appstoreconnect', 'app-store'].includes(normalized)) return 'asc';
  if (['revenuecat', 'revenue-cat', 'rc', 'revenuecat-mcp'].includes(normalized)) return 'revenuecat';
  if (['paddle', 'paddle-billing', 'billing-metrics', 'web-revenue'].includes(normalized)) return 'paddle';
  if (['seo', 'gsc', 'google-search-console', 'search-console', 'dataforseo', 'organic-search'].includes(normalized)) return 'seo';
  if (['sentry', 'sentry-api', 'sentry-mcp', 'crashes', 'errors', 'crash-reporting'].includes(normalized)) return 'sentry';
  if (['coolify', 'coolify-api', 'deployment', 'deployments', 'hosting', 'infra', 'infrastructure'].includes(normalized)) return 'coolify';
  if (['stripe', 'stripe-billing', 'stripe-payments'].includes(normalized)) return 'stripe';
  if (['lemonsqueezy', 'lemon-squeezy', 'lemon', 'ls'].includes(normalized)) return 'lemonsqueezy';
  if (['adapty', 'adapty-paywalls', 'adapty-subscriptions'].includes(normalized)) return 'adapty';
  if (['superwall', 'superwall-paywalls'].includes(normalized)) return 'superwall';
  if (['google-play', 'google-play-console', 'play-console', 'play-store', 'android-store'].includes(normalized)) return 'google-play';
  if (['datadog', 'datadog-rum', 'datadog-apm', 'datadog-logs'].includes(normalized)) return 'datadog';
  if (['bugsnag', 'bugsnag-crashes'].includes(normalized)) return 'bugsnag';
  if (['intercom', 'intercom-support'].includes(normalized)) return 'intercom';
  if (['zendesk', 'zendesk-support'].includes(normalized)) return 'zendesk';
  if (['apple-search-ads', 'apple-ads', 'asa', 'search-ads'].includes(normalized)) return 'apple-search-ads';
  if (['google-ads', 'adwords'].includes(normalized)) return 'google-ads';
  if (['meta-ads', 'facebook-ads', 'instagram-ads', 'fb-ads'].includes(normalized)) return 'meta-ads';
  if (['tiktok-ads', 'tiktok-business', 'tiktok-business-api'].includes(normalized)) return 'tiktok-ads';
  if (['vercel', 'vercel-deployments', 'vercel-hosting'].includes(normalized)) return 'vercel';
  if (['cloudflare', 'cf', 'cloudflare-workers', 'cloudflare-pages'].includes(normalized)) return 'cloudflare';
  if (['resend', 'resend-email'].includes(normalized)) return 'resend';
  if (['customerio', 'customer-io', 'customer.io', 'cio'].includes(normalized)) return 'customerio';
  if (['mailchimp', 'mailchimp-marketing'].includes(normalized)) return 'mailchimp';
  if (['appfollow', 'app-follow'].includes(normalized)) return 'appfollow';
  if (['apptweak', 'app-tweak'].includes(normalized)) return 'apptweak';
  if (['linear', 'linear-issues', 'linear-planning'].includes(normalized)) return 'linear';
  if (['postiz', 'postiz-api', 'social-publishing', 'social-scheduler'].includes(normalized)) return 'postiz';
  return null;
}

function parseConnectorList(value) {
  if (!String(value || '').trim()) return [];

  const connectors = new Set();
  for (const entry of String(value).split(',')) {
    const connector = normalizeConnectorKey(entry);
    if (!connector) {
      printHelpAndExit(1, `Unknown connector: ${entry.trim()}. Use ${SUPPORTED_CONNECTORS.join(', ')}, or all.`);
    }
    if (connector === 'all') {
      SUPPORTED_CONNECTORS.forEach((supported) => connectors.add(supported));
    } else {
      connectors.add(connector);
    }
  }
  return [...connectors];
}

function quote(value) {
  if (/^[a-zA-Z0-9_./:-]+$/.test(String(value))) {
    return String(value);
  }
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function resolveRuntimeScriptPath(scriptName) {
  const candidates = [
    path.join(RUNTIME_DIR, scriptName),
    path.resolve('scripts', scriptName),
    path.resolve('skills/growth-engineer/scripts', scriptName),
    path.resolve('skills/openclaw-growth-engineer/scripts', scriptName),
  ];
  return candidates.find((candidate) => existsSync(candidate)) || path.join(RUNTIME_DIR, scriptName);
}

function nodeRuntimeScriptCommand(scriptName) {
  return `node ${quote(resolveRuntimeScriptPath(scriptName))}`;
}

function getRuntimeSourceCommand(sourceName) {
  const normalized = String(sourceName || '').trim().toLowerCase();
  if (normalized === 'analytics' || normalized === 'analyticscli') {
    return nodeRuntimeScriptCommand('export-analytics-summary.mjs');
  }
  if (normalized === 'revenuecat' || normalized === 'revenue-cat') {
    return nodeRuntimeScriptCommand('export-revenuecat-summary.mjs');
  }
  if (normalized === 'paddle') {
    return nodeRuntimeScriptCommand('export-paddle-summary.mjs');
  }
  if (['seo', 'gsc', 'google-search-console', 'search-console', 'dataforseo'].includes(normalized)) {
    return nodeRuntimeScriptCommand('export-seo-summary.mjs');
  }
  if (normalized === 'sentry' || normalized === 'glitchtip') {
    return nodeRuntimeScriptCommand('export-sentry-summary.mjs');
  }
  if (normalized === 'coolify') {
    return nodeRuntimeScriptCommand('export-coolify-summary.mjs');
  }
  if (['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(normalized)) {
    return nodeRuntimeScriptCommand('export-asc-summary.mjs');
  }
  return getDefaultSourceCommand(sourceName);
}

function replaceLegacyRuntimeScriptCommand(command) {
  const trimmed = String(command || '').trim();
  if (!trimmed) return trimmed;
  return trimmed
    .replace(
    /^node\s+scripts\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-start\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs|openclaw-growth-engineer\.mjs)(?=\s|$)/,
    (_match, scriptName) => nodeRuntimeScriptCommand(scriptName),
    )
    .replace(
      /^node\s+(['"]?)(?:\S*\/)?node_modules\/@analyticscli\/growth-engineer\/dist\/runtime\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-start\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs|openclaw-growth-engineer\.mjs)\1(?=\s|$)/,
      (_match, _quote, scriptName) => nodeRuntimeScriptCommand(scriptName),
    );
}

function normalizeSourceCommand(sourceName, source) {
  return replaceLegacyRuntimeScriptCommand(source?.command || '') || getRuntimeSourceCommand(sourceName);
}

function isAscSource(source: any) {
  const service = String(source?.service || source?.key || '').trim().toLowerCase();
  return ['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(service);
}

function buildAscExtraSource(source: any = {}) {
  return {
    key: 'asc-cli',
    service: 'asc-cli',
    label: source?.label || 'ASC / App Store Connect CLI',
    enabled: true,
    mode: 'command',
    ...source,
    command: normalizeSourceCommand('asc', source),
  };
}

function migrateRuntimeSourceCommands(config) {
  if (!config || typeof config !== 'object') return config;
  const sources = config.sources && typeof config.sources === 'object' ? config.sources : {};
  const nextSources = { ...sources };
  for (const sourceName of ['analytics', 'revenuecat', 'paddle', 'seo', 'sentry', 'coolify']) {
    if (nextSources[sourceName]?.mode === 'command') {
      nextSources[sourceName] = {
        ...nextSources[sourceName],
        command: normalizeSourceCommand(sourceName, nextSources[sourceName]),
      };
    }
  }
  if (Array.isArray(nextSources.extra)) {
    nextSources.extra = nextSources.extra.map((source) => {
      if (!source || source.mode !== 'command') return source;
      const service = String(source.service || source.key || '').toLowerCase();
      const sourceName = isAscSource(source) ? 'asc' : service;
      return {
        ...source,
        command: normalizeSourceCommand(sourceName, source),
      };
    });
  }
  return {
    ...config,
    sources: nextSources,
  };
}

function truncate(value, max = 240) {
  const text = String(value || '');
  if (text.length <= max) return text;
  return `${text.slice(0, max)}...`;
}

function resolveShellCommand(): string {
  const candidates = [
    process.env.OPENCLAW_SHELL,
    process.env.SHELL,
    '/bin/zsh',
    '/bin/bash',
    '/usr/bin/bash',
    '/bin/sh',
    '/usr/bin/sh',
  ].filter((value): value is string => typeof value === 'string' && value.trim().length > 0);

  for (const candidate of candidates) {
    if (existsSync(candidate)) {
      return candidate;
    }
  }

  return 'sh';
}

function emitProgress(enabled, event) {
  if (!enabled) return;
  process.stderr.write(`OPENCLAW_PROGRESS ${JSON.stringify(event)}\n`);
}

function hardenUnattendedShellCommand(command) {
  return String(command || '').replace(/(^|[;&|]\s*)sudo(?!\s+-n(?:\s|$))(?=\s|$)/g, '$1sudo -n');
}

function runShellCommand(
  command,
  timeoutMs = 120_000,
  options: { env?: NodeJS.ProcessEnv; onStderrLine?: (line: string) => void } = {},
): Promise<ShellResult> {
  return new Promise((resolve) => {
    const childEnv = {
      ...process.env,
      DEBIAN_FRONTEND: 'noninteractive',
      SUDO_ASKPASS: '/bin/false',
      SUDO_PROMPT: '',
    };
    for (const [key, value] of Object.entries(options.env || {})) {
      if (value === undefined) delete childEnv[key];
      else childEnv[key] = value;
    }
    const child = spawn(resolveShellCommand(), ['-c', hardenUnattendedShellCommand(command)], {
      stdio: ['ignore', 'pipe', 'pipe'],
      env: childEnv,
    });

    let stdout = '';
    let stderr = '';
    let stderrBuffer = '';
    let settled = false;

    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill('SIGTERM');
      resolve({
        ok: false,
        code: null,
        stdout,
        stderr: `${stderr}\nTimed out after ${timeoutMs}ms`,
      });
    }, timeoutMs);

    child.stdout.on('data', (chunk) => {
      stdout += String(chunk);
    });
    child.stderr.on('data', (chunk) => {
      const text = String(chunk);
      stderr += text;
      if (!options.onStderrLine) return;
      stderrBuffer += text;
      const lines = stderrBuffer.split(/\r?\n/);
      stderrBuffer = lines.pop() || '';
      for (const line of lines) {
        options.onStderrLine(line);
      }
    });

    child.on('close', (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (options.onStderrLine && stderrBuffer.trim()) {
        options.onStderrLine(stderrBuffer);
      }
      resolve({
        ok: code === 0,
        code,
        stdout,
        stderr,
      });
    });
  });
}

function ascIsolatedEnv(overrides: NodeJS.ProcessEnv = {}): NodeJS.ProcessEnv {
  const env: NodeJS.ProcessEnv = {
    ASC_BYPASS_KEYCHAIN: '1',
    ASC_TIMEOUT_SECONDS: normalizeString(process.env.ASC_TIMEOUT_SECONDS) || DEFAULT_ASC_TIMEOUT_SECONDS,
    ASC_CONFIG_PATH:
      process.env.OPENCLAW_GROWTH_ASC_CONFIG_PATH ||
      path.join(process.env.TMPDIR || '/tmp', `openclaw-growth-asc-env-${process.pid}.json`),
    ...overrides,
  };
  const hasPrivateKeyPath = normalizeString(env.ASC_PRIVATE_KEY_PATH || process.env.ASC_PRIVATE_KEY_PATH);
  if (hasPrivateKeyPath) {
    if (!Object.prototype.hasOwnProperty.call(overrides, 'ASC_PRIVATE_KEY')) env.ASC_PRIVATE_KEY = undefined;
    if (!Object.prototype.hasOwnProperty.call(overrides, 'ASC_PRIVATE_KEY_B64')) env.ASC_PRIVATE_KEY_B64 = undefined;
  }
  return env;
}

function base64UrlJson(value) {
  return Buffer.from(JSON.stringify(value)).toString('base64url');
}

async function buildAscApiJwt(env: NodeJS.ProcessEnv = process.env) {
  const keyId = normalizeString(env.ASC_KEY_ID);
  const issuerId = normalizeString(env.ASC_ISSUER_ID);
  const privateKeyPath = normalizeString(env.ASC_PRIVATE_KEY_PATH);
  const privateKey = normalizeString(env.ASC_PRIVATE_KEY) ||
    (normalizeString(env.ASC_PRIVATE_KEY_B64)
      ? Buffer.from(normalizeString(env.ASC_PRIVATE_KEY_B64), 'base64').toString('utf8')
      : privateKeyPath
        ? await fs.readFile(privateKeyPath, 'utf8')
        : '');
  if (!keyId || !issuerId || !privateKey) return null;
  const now = Math.floor(Date.now() / 1000);
  const signingInput = `${base64UrlJson({ alg: 'ES256', kid: keyId, typ: 'JWT' })}.${base64UrlJson({
    iss: issuerId,
    iat: now - 60,
    exp: now + 15 * 60,
    aud: 'appstoreconnect-v1',
  })}`;
  const signer = createSign('SHA256');
  signer.update(signingInput);
  signer.end();
  const signature = signer.sign({ key: privateKey, dsaEncoding: 'ieee-p1363' });
  return `${signingInput}.${signature.toString('base64url')}`;
}

async function fetchAscApiJson(pathname, timeoutMs = 60_000, env: NodeJS.ProcessEnv = process.env) {
  const token = await buildAscApiJwt(env);
  if (!token) {
    return { ok: false, status: 0, payload: null, error: 'ASC API credentials are incomplete' };
  }
  try {
    const response = await fetch(`https://api.appstoreconnect.apple.com${pathname}`, {
      headers: {
        Accept: 'application/json',
        Authorization: `Bearer ${token}`,
      },
      signal: AbortSignal.timeout(timeoutMs),
    });
    const text = await response.text();
    let payload: any = null;
    try {
      payload = text ? JSON.parse(text) : null;
    } catch {
      payload = { raw: text };
    }
    const error = Array.isArray(payload?.errors)
      ? payload.errors.map((entry) => entry?.detail || entry?.title || entry?.code).filter(Boolean).join('; ')
      : '';
    return { ok: response.ok, status: response.status, payload, error };
  } catch (error: any) {
    return { ok: false, status: 0, payload: null, error: error?.message || String(error) };
  }
}

async function listAscAppsDirect(timeoutMs = 60_000) {
  const result = await fetchAscApiJson('/v1/apps?limit=200', timeoutMs, process.env);
  if (!result.ok) {
    return {
      ok: false,
      error: result.error || `Apple API returned HTTP ${result.status}`,
      apps: [],
    };
  }
  return {
    ok: true,
    error: null,
    apps: extractAscAppChoices(result.payload),
  };
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function commandExists(commandName) {
  const result = await runShellCommand(`command -v ${quote(commandName)} >/dev/null 2>&1`, 30_000);
  return result.ok;
}

async function resolveCommandPath(commandName) {
  const result = await runShellCommand(`command -v ${quote(commandName)}`, 30_000);
  return result.ok ? result.stdout.trim() : null;
}

function prependToPath(binDir) {
  process.env.PATH = `${binDir}${path.delimiter}${process.env.PATH || ''}`;
}

function getPathProfileEntries(binDir) {
  const entries = [binDir];
  if (process.env.HOME && path.resolve(binDir) === path.resolve(process.env.HOME, '.local', 'bin')) {
    entries.push(path.join(process.env.HOME, '.local', 'analyticscli-npm', 'bin'));
  }
  return entries;
}

function renderProfilePathEntries(binDir) {
  const home = process.env.HOME ? path.resolve(process.env.HOME) : null;
  return getPathProfileEntries(binDir)
    .map((entry) => {
      const resolved = path.resolve(entry);
      if (home && (resolved === home || resolved.startsWith(`${home}${path.sep}`))) {
        return `$HOME/${path.relative(home, resolved)}`;
      }
      return entry;
    })
    .join(':');
}

async function ensureProfilePath(binDir) {
  if (process.env.ANALYTICSCLI_SKIP_PROFILE_UPDATE === 'true' || !process.env.HOME) {
    return false;
  }

  const line = `export PATH="${renderProfilePathEntries(binDir)}:$PATH"`;
  const profiles = ['.profile', '.bashrc', '.bash_profile', '.zshrc', '.zprofile'].map((name) =>
    path.join(process.env.HOME!, name),
  );
  let wrote = false;

  for (const profile of profiles) {
    let current = '';
    try {
      current = await fs.readFile(profile, 'utf8');
    } catch {
      await fs.mkdir(path.dirname(profile), { recursive: true });
    }

    if (!current.includes(line)) {
      await fs.appendFile(profile, `\n# AnalyticsCLI CLI user-local npm bin\n${line}\n`, 'utf8');
      wrote = true;
    }
  }

  return wrote;
}

async function verifyFreshShellProfile() {
  if (!process.env.HOME) {
    return false;
  }

  const cleanPath = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin';
  const probes = [
    {
      shell: '/bin/bash',
      command:
        'for f in "$HOME/.bash_profile" "$HOME/.bashrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
    },
    {
      shell: '/usr/bin/bash',
      command:
        'for f in "$HOME/.bash_profile" "$HOME/.bashrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
    },
    {
      shell: '/bin/zsh',
      command:
        'for f in "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
    },
    {
      shell: '/usr/bin/zsh',
      command:
        'for f in "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
    },
    {
      shell: '/bin/sh',
      command:
        '[ -f "$HOME/.profile" ] && . "$HOME/.profile" >/dev/null 2>&1 || true; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
    },
    {
      shell: '/usr/bin/sh',
      command:
        '[ -f "$HOME/.profile" ] && . "$HOME/.profile" >/dev/null 2>&1 || true; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
    },
  ];

  for (const probe of probes) {
    if (!(await fileExists(probe.shell))) {
      continue;
    }
    const result = await runShellCommand(
      `env HOME=${quote(process.env.HOME)} PATH=${quote(cleanPath)} ${quote(probe.shell)} -lc ${quote(probe.command)}`,
      30_000,
    );
    if (result.ok) {
      return true;
    }
  }

  return false;
}

function isUserLocalBin(binDir) {
  if (!process.env.HOME) {
    return false;
  }
  const home = path.resolve(process.env.HOME);
  const resolved = path.resolve(binDir);
  return resolved === home || resolved.startsWith(`${home}${path.sep}`);
}

function isPermissionFailure(output) {
  return /EACCES|permission denied|access denied|operation not permitted/i.test(String(output || ''));
}

async function ensureAnalyticsCliInstalled() {
  const beforePath = await resolveCommandPath('analyticscli');
  const npmExists = await commandExists('npm');
  if (!npmExists) {
    if (beforePath) {
      return {
        ok: true,
        detail: `analyticscli binary found at ${beforePath}; npm unavailable, so package update was skipped`,
      };
    }
    return {
      ok: false,
      detail: `analyticscli binary missing and npm is unavailable; install ${ANALYTICSCLI_PACKAGE_SPEC}`,
    };
  }

  const globalInstall = await runShellCommand(`npm install -g ${quote(ANALYTICSCLI_PACKAGE_SPEC)}`, 180_000);
  if (!globalInstall.ok) {
    const installOutput = `${globalInstall.stderr}\n${globalInstall.stdout}`;
    if (isPermissionFailure(installOutput)) {
      await fs.mkdir(ANALYTICSCLI_NPM_PREFIX, { recursive: true });
      const localInstall = await runShellCommand(
        `npm install -g --prefix ${quote(ANALYTICSCLI_NPM_PREFIX)} ${quote(ANALYTICSCLI_PACKAGE_SPEC)}`,
        180_000,
      );
      if (!localInstall.ok) {
        return beforePath
          ? {
              ok: true,
              detail: `analyticscli binary found at ${beforePath}; update failed globally and in user-local prefix (${truncate(localInstall.stderr || localInstall.stdout)})`,
            }
          : {
              ok: false,
              detail: `npm install failed globally and in user-local prefix ${ANALYTICSCLI_NPM_PREFIX}: ${truncate(localInstall.stderr || localInstall.stdout)}`,
            };
      }
      const localBinDir = path.join(ANALYTICSCLI_NPM_PREFIX, 'bin');
      prependToPath(localBinDir);
      await ensureProfilePath(localBinDir);
    } else {
      return beforePath
        ? {
            ok: true,
            detail: `analyticscli binary found at ${beforePath}; package update failed (${truncate(installOutput)})`,
          }
        : {
            ok: false,
            detail: `npm install -g ${ANALYTICSCLI_PACKAGE_SPEC} failed: ${truncate(installOutput)}`,
          };
    }
  }

  const afterPath = await resolveCommandPath('analyticscli');
  if (afterPath) {
    const helpCheck = await runShellCommand('analyticscli --help >/dev/null 2>&1', 30_000);
    if (!helpCheck.ok) {
      return {
        ok: false,
        detail: `analyticscli binary found at ${afterPath}, but --help failed: ${truncate(helpCheck.stderr || helpCheck.stdout)}`,
      };
    }

    const binDir = path.dirname(afterPath);
    if (isUserLocalBin(binDir)) {
      await ensureProfilePath(binDir);
      if (!(await verifyFreshShellProfile())) {
        return {
          ok: false,
          detail: `analyticscli works at ${afterPath}, but a fresh shell still cannot resolve it after profile update; add ${renderProfilePathEntries(binDir)} to PATH`,
        };
      }
      return {
        ok: true,
        detail: `analyticscli package ensured via ${ANALYTICSCLI_PACKAGE_SPEC}; binary found at ${afterPath}; shell profiles updated and fresh shell verification passed`,
      };
    }
  }

  return afterPath
    ? {
        ok: true,
        detail: `analyticscli package ensured via ${ANALYTICSCLI_PACKAGE_SPEC}; binary found at ${afterPath}`,
      }
    : {
        ok: false,
        detail: `Installed ${ANALYTICSCLI_PACKAGE_SPEC}, but analyticscli is still not on PATH`,
      };
}

async function readJson(filePath): Promise<any> {
  const raw = await fs.readFile(filePath, 'utf8');
  return JSON.parse(raw);
}

async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function formatHeartbeatInterval(minutes) {
  const intervalMinutes = Math.max(1, Math.floor(Number(minutes) || 1440));
  if (intervalMinutes % 1440 === 0) return `${intervalMinutes / 1440}d`;
  if (intervalMinutes % 60 === 0) return `${intervalMinutes / 60}h`;
  return `${intervalMinutes}m`;
}

function getHeartbeatInterval(config) {
  const scheduleInterval = Number(config?.schedule?.intervalMinutes);
  const healthInterval = Number(config?.schedule?.connectorHealthCheckIntervalMinutes);
  return Math.min(
    Number.isFinite(scheduleInterval) && scheduleInterval > 0 ? scheduleInterval : 1440,
    Number.isFinite(healthInterval) && healthInterval > 0 ? healthInterval : 360,
  );
}

function relativeWorkspacePath(filePath) {
  const relative = path.relative(process.cwd(), filePath);
  return relative && !relative.startsWith('..') && !path.isAbsolute(relative) ? relative : filePath;
}

function isEffectivelyEmptyHeartbeat(value) {
  return String(value || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#') && !line.startsWith('<!--') && !line.startsWith('-->'))
    .length === 0;
}

function renderHeartbeatBlock(configPath, config) {
  const interval = formatHeartbeatInterval(getHeartbeatInterval(config));
  const displayConfigPath = relativeWorkspacePath(configPath);
  const displayStatePath = deriveStatePathFromConfigPath(displayConfigPath);
  const runnerCommand = buildGrowthRunnerCommand(displayConfigPath, displayStatePath);
  const statusCommand = `node scripts/openclaw-growth-status.mjs --config ${quote(displayConfigPath)} --json --only-connectors asc`;
  const wizardCommand = 'npx -y @analyticscli/growth-engineer wizard --connectors';
  return `${HEARTBEAT_MARKER_START}
tasks:

- name: openclaw-growth-engineer-run
  interval: ${interval}
  prompt: "Run \`${runnerCommand}\` from the workspace if the config and runtime files exist. The runner owns schedule.cadences, connectorHealthCheckIntervalMinutes, skipIfNoDataChange, and skipIfIssueSetUnchanged. ASC/App Store Connect is a Growth Engineer local CLI connector, not a chat tool. If asked whether ASC analytics access is available, never inspect loaded chat/MCP tools and never answer no because no Apple tool is callable. Answer from \`${statusCommand}\` or the latest connector setup result. If ASC reports connected/pass/healthy, or setup just finished successfully, answer exactly: Yes. ASC analytics is connected through Growth Engineer local asc CLI/API-key setup. If it reports connector-health alerts, production crashes, generated issues, or actionable growth findings, summarize only the action and evidence. If setup files are missing, tell the user to run \`${wizardCommand}\`. If there is no actionable output, reply HEARTBEAT_OK."

# Keep this section small. Do not put secrets in HEARTBEAT.md.
${HEARTBEAT_MARKER_END}`;
}

async function ensureGrowthHeartbeat(configPath, config) {
  const heartbeatPath = path.resolve(DEFAULT_HEARTBEAT_PATH);
  const block = renderHeartbeatBlock(configPath, config);
  let existing = '';
  let existed = true;
  try {
    existing = await fs.readFile(heartbeatPath, 'utf8');
  } catch {
    existed = false;
  }

  const markerPattern = new RegExp(`${HEARTBEAT_MARKER_START}[\\s\\S]*?${HEARTBEAT_MARKER_END}`);
  const next = markerPattern.test(existing)
    ? existing.replace(markerPattern, block)
    : isEffectivelyEmptyHeartbeat(existing)
      ? `# OpenClaw heartbeat checklist\n\n${block}\n`
      : `${existing.trimEnd()}\n\n${block}\n`;

  if (next !== existing) {
    await fs.writeFile(heartbeatPath, next, 'utf8');
    return {
      path: heartbeatPath,
      interval: formatHeartbeatInterval(getHeartbeatInterval(config)),
      created: !existed || isEffectivelyEmptyHeartbeat(existing),
      updated: existed && !isEffectivelyEmptyHeartbeat(existing),
    };
  }

  return {
    path: heartbeatPath,
    interval: formatHeartbeatInterval(getHeartbeatInterval(config)),
    created: false,
    updated: false,
  };
}

function applyOpenClawCronOverrides(config, args) {
  const automation = getAutomationConfig(config);
  const cron = {
    ...automation.openclawCron,
    ...(args.openclawCronSchedule ? { schedule: args.openclawCronSchedule } : {}),
    ...(args.openclawCronTimezone ? { timezone: args.openclawCronTimezone } : {}),
  };
  return {
    ...config,
    automation: {
      ...(config?.automation || {}),
      openclawCron: cron,
    },
  };
}

function getOpenClawCronProofCommands(configPath) {
  const displayConfigPath = relativeWorkspacePath(configPath);
  const statePath = deriveStatePathFromConfigPath(displayConfigPath);
  const proofPath = deriveSchedulerProofPathFromStatePath(statePath);
  return {
    listCommand: 'openclaw cron list',
    runsCommand: 'openclaw cron runs --id <job-id>',
    stateCommand: `jq '.connectorHealth, .cadences, .lastRunAt, .skippedReason' ${quote(statePath)}`,
    proofCommand: `tail -n 20 ${quote(proofPath)}`,
    manualWakeCommand: `openclaw system event --text ${quote(`Run OpenClaw Growth Engineer now using config ${relativeWorkspacePath(configPath)} and inspect scheduler proof.`)} --mode now`,
  };
}

async function ensureOpenClawCronSchedule(configPath, config, mode = 'auto') {
  const normalizedMode = validateOpenClawCronMode(mode);
  const automation = getAutomationConfig(config);
  const proof = getOpenClawCronProofCommands(configPath);
  if (normalizedMode === 'disable' || automation.openclawCron.enabled === false) {
    return {
      ok: true,
      enabled: false,
      installed: false,
      status: 'disabled',
      detail: 'OpenClaw Gateway cron setup disabled',
      proof,
    };
  }

  const openclawPath = await resolveCommandPath('openclaw');
  if (!openclawPath) {
    const detail = 'openclaw CLI not found on PATH; skipping OpenClaw Gateway cron setup';
    return {
      ok: normalizedMode === 'auto',
      enabled: true,
      installed: false,
      status: normalizedMode === 'auto' ? 'skipped' : 'failed',
      detail,
      remediation: 'Run this setup inside the VPS shell where OpenClaw Gateway is installed, or install the openclaw CLI.',
      proof,
    };
  }

  const displayConfigPath = relativeWorkspacePath(configPath);
  const addCommand = buildOpenClawCronAddCommand(displayConfigPath, config);
  const inspection = await inspectOpenClawCronInstall({
    configPath: displayConfigPath,
    config,
    runCommand: runShellCommand,
    readFile: fs.readFile,
  });
  if (inspection.exists && inspection.verified) {
    return {
      ok: true,
      enabled: true,
      installed: true,
      status: 'already_configured_verified',
      detail: `OpenClaw cron job already exists and matches the Growth Engineer runner contract: ${automation.openclawCron.name}`,
      schedule: automation.openclawCron.schedule,
      timezone: automation.openclawCron.timezone,
      source: inspection.source,
      proof,
    };
  }

  if (inspection.exists && inspection.reason === 'delivery_mismatch') {
    const editCommand = getOpenClawCronEditDeliveryCommandFromInspection(inspection, config);
    if (editCommand) {
      const edit = await runShellCommand(editCommand, 60_000);
      if (edit.ok) {
        return {
          ok: true,
          enabled: true,
          installed: true,
          status: 'repaired_delivery_cli',
          detail: `Repaired OpenClaw cron delivery with: ${editCommand}`,
          schedule: automation.openclawCron.schedule,
          timezone: automation.openclawCron.timezone,
          command: editCommand,
          source: inspection.source,
          proof,
        };
      }
    }

    const repair = await repairOpenClawCronDeliveryStore({
      configPath: displayConfigPath,
      config,
      readFile: fs.readFile,
      writeFile: fs.writeFile,
    });
    if (repair.repaired) {
      return {
        ok: true,
        enabled: true,
        installed: true,
        status: 'repaired_delivery',
        detail: `Repaired OpenClaw cron delivery for "${automation.openclawCron.name}" in ${repair.path}`,
        schedule: automation.openclawCron.schedule,
        timezone: automation.openclawCron.timezone,
        source: repair.path,
        command: editCommand || undefined,
        proof,
      };
    }
  }

  const add = await runShellCommand(addCommand, 60_000);
  const existingDetail = inspection.exists
    ? `Existing OpenClaw cron job "${automation.openclawCron.name}" was not verifiably wired to the current runner contract (${inspection.reason} via ${inspection.source}). `
    : '';
  return {
    ok: add.ok || (normalizedMode === 'auto' && !inspection.exists),
    enabled: true,
    installed: add.ok,
    status: add.ok ? (inspection.exists ? 'reconfigured' : 'configured') : inspection.exists ? 'needs_repair' : 'failed',
    detail: add.ok
      ? `${existingDetail}Configured OpenClaw cron job "${automation.openclawCron.name}" (${automation.openclawCron.schedule}, ${automation.openclawCron.timezone})`
      : `${existingDetail}${add.stderr.trim() || add.stdout.trim() || `openclaw cron add exited ${add.code}`}`,
    schedule: automation.openclawCron.schedule,
    timezone: automation.openclawCron.timezone,
    command: addCommand,
    remediation:
      inspection.exists && !add.ok
        ? `Remove the stale OpenClaw cron job named "${automation.openclawCron.name}" with your installed OpenClaw CLI, then rerun: ${addCommand}`
        : undefined,
    proof,
  };
}

async function ensureHermesCronSchedule(configPath, config, mode = 'auto') {
  const normalizedMode = validateOpenClawCronMode(mode);
  const automation = getAutomationConfig(config);
  const displayConfigPath = relativeWorkspacePath(configPath);
  const statePath = deriveStatePathFromConfigPath(displayConfigPath);
  const proofPath = deriveSchedulerProofPathFromStatePath(statePath);
  const workdir = path.resolve(automation.hermesCron.workdir || process.cwd());
  const proof = {
    listCommand: 'hermes cron list',
    statusCommand: 'hermes cron status <job-id>',
    stateCommand: `jq '.connectorHealth, .cadences, .lastRunAt, .skippedReason' ${quote(statePath)}`,
    proofCommand: `tail -n 20 ${quote(proofPath)}`,
  };

  if (normalizedMode === 'disable' || automation.hermesCron.enabled === false) {
    return {
      ok: true,
      enabled: false,
      installed: false,
      status: 'disabled',
      detail: 'Hermes cron setup disabled',
      proof,
    };
  }

  const hermesPath = await resolveCommandPath('hermes');
  if (!hermesPath) {
    return {
      ok: normalizedMode === 'auto',
      enabled: true,
      installed: false,
      status: normalizedMode === 'auto' ? 'skipped' : 'failed',
      detail: 'hermes CLI not found on PATH; skipping Hermes cron setup',
      remediation: 'Run this setup inside the host shell where Hermes Gateway is installed, or install the hermes CLI.',
      proof,
    };
  }

  const createCommand = buildHermesCronCreateCommand(displayConfigPath, config, { workdir });
  const inspection = await inspectHermesCronInstall({
    configPath: displayConfigPath,
    config,
    runCommand: runShellCommand,
    readFile: fs.readFile,
    workdir,
  });
  if (inspection.exists && inspection.verified) {
    return {
      ok: true,
      enabled: true,
      installed: true,
      status: 'already_configured_verified',
      detail: `Hermes cron job already exists and matches the Growth Engineer runner contract: ${automation.hermesCron.name}`,
      schedule: automation.hermesCron.schedule,
      workdir,
      source: inspection.source,
      proof,
    };
  }

  const create = await runShellCommand(createCommand, 60_000);
  const existingDetail = inspection.exists
    ? `Existing Hermes cron job "${automation.hermesCron.name}" was not verifiably wired to the current runner contract (${inspection.reason} via ${inspection.source}). `
    : '';
  return {
    ok: create.ok || (normalizedMode === 'auto' && !inspection.exists),
    enabled: true,
    installed: create.ok,
    status: create.ok ? (inspection.exists ? 'reconfigured' : 'configured') : inspection.exists ? 'needs_repair' : 'failed',
    detail: create.ok
      ? `${existingDetail}Configured Hermes cron job "${automation.hermesCron.name}" (${automation.hermesCron.schedule})`
      : `${existingDetail}${create.stderr.trim() || create.stdout.trim() || `hermes cron create exited ${create.code}`}`,
    schedule: automation.hermesCron.schedule,
    workdir,
    command: createCommand,
    remediation:
      inspection.exists && !create.ok
        ? `Remove the stale Hermes cron job named "${automation.hermesCron.name}" with your installed Hermes CLI, then rerun: ${createCommand}`
        : undefined,
    proof,
  };
}

async function appendHelperDetail(details, label, result) {
  if (result.ok) {
    details.push(`${label}: ok`);
    return;
  }
  details.push(`${label}: ${truncate(result.stderr || result.stdout || `exit ${result.code ?? 'unknown'}`)}`);
}

async function installClawHubSkill(skillName, details) {
  if (await commandExists('clawhub')) {
    const result = await runShellCommand(`clawhub install ${quote(skillName)} || clawhub install ${quote(skillName)} --force`, 180_000);
    await appendHelperDetail(details, `ClawHub skill ${skillName}`, result);
    return result.ok;
  }
  if (await commandExists('npx')) {
    const result = await runShellCommand(
      `npx -y clawhub install ${quote(skillName)} || npx -y clawhub install ${quote(skillName)} --force`,
      180_000,
    );
    await appendHelperDetail(details, `ClawHub skill ${skillName}`, result);
    return result.ok;
  }
  details.push(`ClawHub skill ${skillName}: skipped because neither clawhub nor npx is available`);
  return false;
}

async function installAgentSkill(repo, details) {
  if (!(await commandExists('npx'))) {
    details.push(`Agent skill ${repo}: skipped because npx is unavailable`);
    return false;
  }
  const result = await runShellCommand(`npx -y skills add ${quote(repo)}`, 180_000);
  await appendHelperDetail(details, `Agent skill ${repo}`, result);
  return result.ok;
}

async function installSystemBinary(commandName, details) {
  if (await commandExists(commandName)) {
    details.push(`${commandName} binary found at ${await resolveCommandPath(commandName)}`);
    return true;
  }

  if (await commandExists('brew')) {
    const result = await runShellCommand(`brew install ${quote(commandName)}`, 600_000);
    await appendHelperDetail(details, `brew install ${commandName}`, result);
  } else if (await commandExists('apt-get')) {
    const prefix = process.getuid?.() === 0 ? '' : 'sudo -n ';
    const result = await runShellCommand(`${prefix}apt-get update && ${prefix}apt-get install -y ${quote(commandName)}`, 600_000);
    await appendHelperDetail(details, `apt-get install ${commandName}`, result);
  } else if (await commandExists('winget')) {
    const packageId = commandName === 'gh' ? 'GitHub.cli' : commandName;
    const result = await runShellCommand(`winget install --id ${quote(packageId)} -e --silent`, 600_000);
    await appendHelperDetail(details, `winget install ${packageId}`, result);
  } else {
    details.push(`No supported non-interactive installer found for ${commandName}`);
  }

  const installedPath = await resolveCommandPath(commandName);
  if (installedPath) {
    details.push(`${commandName} binary found at ${installedPath}`);
    return true;
  }
  return false;
}

function getUserLocalBinDir() {
  return process.env.HOME ? path.join(process.env.HOME, '.local', 'bin') : null;
}

function prependPath(dir) {
  const current = process.env.PATH || '';
  if (!current.split(':').includes(dir)) {
    process.env.PATH = `${dir}:${current}`;
  }
}

function getGitHubCliReleaseAssetName(version) {
  const arch = process.arch === 'x64' ? 'amd64' : process.arch === 'arm64' ? 'arm64' : '';
  if (process.platform === 'linux' && arch) {
    return `gh_${version}_linux_${arch}.tar.gz`;
  }
  return null;
}

async function resolveGitHubCliReleaseAssetUrl() {
  const response = await fetch('https://api.github.com/repos/cli/cli/releases/latest', {
    headers: {
      Accept: 'application/vnd.github+json',
      'User-Agent': 'openclaw-growth-start',
    },
  });
  if (!response.ok) {
    throw new Error(`GitHub CLI release lookup failed (${response.status})`);
  }
  const release = await response.json();
  const version = String(release?.tag_name || '').replace(/^v/, '');
  const assetName = getGitHubCliReleaseAssetName(version);
  if (!assetName) {
    throw new Error(`No user-local gh installer is defined for ${process.platform}/${process.arch}`);
  }
  const asset = Array.isArray(release?.assets) ? release.assets.find((entry) => entry?.name === assetName) : null;
  if (!asset?.browser_download_url) {
    throw new Error(`GitHub CLI release asset not found: ${assetName}`);
  }
  return asset.browser_download_url;
}

async function installGitHubCliUserLocal(details) {
  const binDir = getUserLocalBinDir();
  if (!binDir) {
    details.push('gh user-local install skipped because HOME is not set');
    return false;
  }
  if (!(await commandExists('curl'))) {
    details.push('gh user-local install skipped because curl is unavailable');
    return false;
  }
  if (!(await commandExists('tar'))) {
    details.push('gh user-local install skipped because tar is unavailable');
    return false;
  }

  try {
    const url = await resolveGitHubCliReleaseAssetUrl();
    const cacheDir = path.join(process.env.HOME, '.cache', 'openclaw-gh');
    const command = [
      'set -eu',
      `mkdir -p ${quote(binDir)} ${quote(cacheDir)}`,
      `tmp="$(mktemp -d ${quote(path.join(cacheDir, 'gh.XXXXXX'))})"`,
      'trap \'rm -rf "$tmp"\' EXIT',
      `curl -fsSL ${quote(url)} -o "$tmp/gh.tar.gz"`,
      'tar -xzf "$tmp/gh.tar.gz" -C "$tmp"',
      'gh_bin="$(find "$tmp" -path "*/bin/gh" -type f | head -n 1)"',
      'test -n "$gh_bin"',
      `cp "$gh_bin" ${quote(path.join(binDir, 'gh'))}`,
      `chmod 755 ${quote(path.join(binDir, 'gh'))}`,
      'for profile in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.zprofile"; do touch "$profile"; grep -Fq \'export PATH="$HOME/.local/bin:$PATH"\' "$profile" || printf \'\\n# OpenClaw user-local bin\\nexport PATH="$HOME/.local/bin:$PATH"\\n\' >> "$profile"; done',
    ].join(' && ');
    const result = await runShellCommand(command, 600_000);
    prependPath(binDir);
    await appendHelperDetail(details, `user-local gh install to ${path.join(binDir, 'gh')}`, result);
    const installedPath = await resolveCommandPath('gh');
    if (installedPath) {
      details.push(`gh binary found at ${installedPath}`);
      return true;
    }
  } catch (error) {
    details.push(`user-local gh install failed: ${error instanceof Error ? error.message : String(error)}`);
  }
  return false;
}

function resolveMcpNpmCacheDir() {
  return process.env.OPENCLAW_MCP_NPM_CACHE ||
    (process.env.HOME ? path.join(process.env.HOME, '.cache', 'openclaw-mcp-npm') : path.join(process.cwd(), '.openclaw-mcp-npm-cache'));
}

function escapeTomlString(value) {
  return String(value).replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

async function upsertRevenueCatCodexMcpConfig(apiKey) {
  if (!process.env.HOME) return null;

  const configDir = path.join(process.env.HOME, '.codex');
  const configFile = path.join(configDir, 'config.toml');
  await fs.mkdir(configDir, { recursive: true });
  let existing = '';
  try {
    existing = await fs.readFile(configFile, 'utf8');
  } catch {
    existing = '';
  }
  const block = `[mcp_servers.revenuecat]
command = "npx"
args = ["--yes", "--cache", "${escapeTomlString(resolveMcpNpmCacheDir())}", "mcp-remote", "https://mcp.revenuecat.ai/mcp", "--header", "Authorization: Bearer \${AUTH_TOKEN}"]
env = { AUTH_TOKEN = "${escapeTomlString(apiKey)}" }
type = "stdio"
startup_timeout_ms = 20000
`;
  const pattern = /(?:^|\n)\[mcp_servers\.revenuecat\]\n(?:.*\n)*?(?=\n\[|\s*$)/m;
  const next = pattern.test(existing)
    ? existing.replace(pattern, `${existing.startsWith('[mcp_servers.revenuecat]') ? '' : '\n'}${block}`)
    : `${existing.trimEnd()}${existing.trim() ? '\n\n' : ''}${block}`;
  await fs.writeFile(configFile, `${next.trimEnd()}\n`, 'utf8');
  return configFile;
}

async function upsertSentryCodexMcpConfig(token) {
  if (!process.env.HOME) return null;

  const configDir = path.join(process.env.HOME, '.codex');
  const configFile = path.join(configDir, 'config.toml');
  await fs.mkdir(configDir, { recursive: true });
  let existing = '';
  try {
    existing = await fs.readFile(configFile, 'utf8');
  } catch {
    existing = '';
  }
  const envEntries = [
    `SENTRY_ACCESS_TOKEN = "${escapeTomlString(token)}"`,
    process.env.SENTRY_BASE_URL && process.env.SENTRY_BASE_URL !== 'https://sentry.io'
      ? `SENTRY_HOST = "${escapeTomlString(String(process.env.SENTRY_BASE_URL).replace(/^https?:\/\//, '').replace(/\/$/, ''))}"`
      : null,
  ].filter(Boolean);
  const block = `[mcp_servers.sentry]
command = "npx"
args = ["--yes", "--cache", "${escapeTomlString(resolveMcpNpmCacheDir())}", "@sentry/mcp-server@latest"]
env = { ${envEntries.join(', ')} }
type = "stdio"
startup_timeout_ms = 30000
`;
  const pattern = /(?:^|\n)\[mcp_servers\.sentry\]\n(?:.*\n)*?(?=\n\[|\s*$)/m;
  const next = pattern.test(existing)
    ? existing.replace(pattern, `${existing.startsWith('[mcp_servers.sentry]') ? '' : '\n'}${block}`)
    : `${existing.trimEnd()}${existing.trim() ? '\n\n' : ''}${block}`;
  await fs.writeFile(configFile, `${next.trimEnd()}\n`, 'utf8');
  return configFile;
}

async function installRevenueCatConnector() {
  const details = [];
  if (!(await commandExists('npx'))) {
    return { connector: 'revenuecat', ok: false, detail: 'npx is required for RevenueCat MCP transport but is unavailable' };
  }
  const check = await runShellCommand(`npx --yes --cache ${quote(resolveMcpNpmCacheDir())} mcp-remote`, 120_000);
  const output = `${check.stderr}\n${check.stdout}`;
  const available = check.ok || /Usage: .*mcp-remote|Usage: .*proxy\.ts/i.test(output);
  if (!available) {
    await appendHelperDetail(details, 'npx mcp-remote availability check', check);
    return { connector: 'revenuecat', ok: false, detail: details.join('; ') };
  }
  details.push(`RevenueCat MCP transport mcp-remote is available via npx cache ${resolveMcpNpmCacheDir()}`);
  const apiKey = String(process.env.REVENUECAT_API_KEY || '').trim();
  if (apiKey) {
    const configFile = await upsertRevenueCatCodexMcpConfig(apiKey);
    details.push(configFile ? `RevenueCat MCP configured in ${configFile}` : 'RevenueCat MCP transport available; HOME missing so MCP config was not written');
  } else {
    details.push('Set REVENUECAT_API_KEY, then rerun this command to write the RevenueCat MCP client config');
  }
  return { connector: 'revenuecat', ok: true, detail: details.join('; ') };
}

async function installSentryConnector() {
  const details = [];
  if (await commandExists('npx')) {
    const check = await runShellCommand(`npx --yes --cache ${quote(resolveMcpNpmCacheDir())} @sentry/mcp-server@latest --help`, 120_000);
    const output = `${check.stderr}\n${check.stdout}`;
    const available = check.ok || /sentry|mcp-server|access-token/i.test(output);
    if (available) {
      details.push(`Sentry MCP server is available via npx cache ${resolveMcpNpmCacheDir()}`);
    } else {
      await appendHelperDetail(details, 'Sentry MCP availability check', check);
    }
  } else {
    details.push('npx unavailable; Sentry MCP config was skipped, direct API exporter remains available');
  }

  const token = String(process.env.SENTRY_AUTH_TOKEN || '').trim();
  if (token && (await commandExists('npx'))) {
    const configFile = await upsertSentryCodexMcpConfig(token);
    details.push(configFile ? `Sentry MCP configured in ${configFile}` : 'Sentry MCP available; HOME missing so MCP config was not written');
  } else if (!token) {
    details.push('Set SENTRY_AUTH_TOKEN, then rerun this command to write Sentry MCP client config');
  }

  details.push('Sentry direct API exporter enabled via node scripts/export-sentry-summary.mjs');
  return { connector: 'sentry', ok: true, detail: details.join('; ') };
}

async function installCoolifyConnector() {
  return {
    connector: 'coolify',
    ok: true,
    detail: 'Coolify uses the built-in read-only API exporter; create a token in Coolify Keys & Tokens / API tokens and store COOLIFY_BASE_URL plus COOLIFY_API_TOKEN with the connector wizard',
  };
}

async function installGitHubConnector() {
  const details = [];
  await installClawHubSkill('github', details);
  let ok = await installSystemBinary('gh', details);
  if (!ok) {
    ok = await installGitHubCliUserLocal(details);
  }
  const repo = await detectGitHubRepo();
  if (repo) {
    details.push(`GitHub repo configured for code access: ${repo}`);
  } else if (process.env.GITHUB_TOKEN) {
    details.push('GITHUB_TOKEN is set; repo selection is deferred per app/task');
  } else {
    details.push('GitHub token not configured yet; rerun connector wizard for github when ready');
  }
  return { connector: 'github', ok, detail: details.join('; ') };
}

async function installAscConnector() {
  const details = [];
  await installAgentSkill('rorkai/app-store-connect-cli-skills', details);
  let ok = await installSystemBinary('asc', details);
  if (!ok && (await commandExists('curl'))) {
    const result = await runShellCommand('curl -fsSL https://asccli.sh/install | bash', 600_000);
    await appendHelperDetail(details, 'asc install script', result);
    ok = Boolean(await resolveCommandPath('asc'));
  }
  return { connector: 'asc', ok, detail: `${details.join('; ')}${ok ? '; next run asc auth status --validate or asc auth login' : ''}` };
}

async function installAnalyticsConnector() {
  const analyticsCliPath = await resolveCommandPath('analyticscli');
  return {
    connector: 'analytics',
    ok: Boolean(analyticsCliPath),
    detail: analyticsCliPath
      ? `analyticscli binary found at ${analyticsCliPath}; token is read from the wizard-managed AnalyticsCLI environment`
      : 'analyticscli binary missing after dependency setup',
  };
}

function isAccountSignalConnector(connector) {
  return ACCOUNT_SIGNAL_CONNECTORS.includes(connector);
}

async function installAccountSignalConnector(connector) {
  const envs = ACCOUNT_SIGNAL_SECRET_ENVS[connector] || [];
  const missing = envs.filter((envName) => !String(process.env[envName] || '').trim());
  return {
    connector,
    ok: missing.length === 0,
    detail:
      missing.length === 0
        ? 'account-wide credential is present; project/app/product scope is discovered later'
        : `missing account-wide credential(s): ${missing.join(', ')}`,
  };
}

async function enableConnectorConfig(configPath, connectors) {
  if (connectors.length === 0 || !(await fileExists(configPath))) return;
  const config = await readJson(configPath);
  const extra = Array.isArray(config.sources?.extra) ? config.sources.extra : [];
  const hasAscExtra = extra.some(isAscSource);
  const next = {
    ...config,
    sources: {
      ...(config.sources || {}),
      analytics: connectors.includes('analytics')
        ? { ...(config.sources?.analytics || {}), enabled: true, mode: 'command', command: normalizeSourceCommand('analytics', config.sources?.analytics) }
        : config.sources?.analytics,
      revenuecat: connectors.includes('revenuecat')
        ? { ...(config.sources?.revenuecat || {}), enabled: true, mode: 'command', command: normalizeSourceCommand('revenuecat', config.sources?.revenuecat) }
        : config.sources?.revenuecat,
      paddle: connectors.includes('paddle')
        ? { ...(config.sources?.paddle || {}), enabled: true, mode: 'command', command: normalizeSourceCommand('paddle', config.sources?.paddle) }
        : config.sources?.paddle,
      seo: connectors.includes('seo')
        ? { ...(config.sources?.seo || {}), enabled: true, mode: 'command', command: normalizeSourceCommand('seo', config.sources?.seo) }
        : config.sources?.seo,
      sentry: connectors.includes('sentry')
        ? { ...(config.sources?.sentry || {}), enabled: true, mode: 'command', command: normalizeSourceCommand('sentry', config.sources?.sentry) }
        : config.sources?.sentry,
      coolify: connectors.includes('coolify')
        ? {
            ...(config.sources?.coolify || {}),
            enabled: true,
            mode: 'command',
            command: normalizeSourceCommand('coolify', config.sources?.coolify),
            baseUrl: config.sources?.coolify?.baseUrl || process.env.COOLIFY_BASE_URL || 'https://coolify.wotaso.com',
            tokenEnv: config.sources?.coolify?.tokenEnv || 'COOLIFY_API_TOKEN',
          }
        : config.sources?.coolify,
      extra: extra.map((source) =>
        connectors.includes('asc') && isAscSource(source)
          ? buildAscExtraSource(source)
          : connectors.includes(String(source?.key || source?.service || '')) && isAccountSignalConnector(String(source?.key || source?.service || ''))
            ? { ...source, enabled: true, mode: source.mode || 'file' }
          : source,
      ).concat(connectors.includes('asc') && !hasAscExtra ? [buildAscExtraSource()] : []),
    },
  };
  await writeJson(configPath, next);
}

async function installConnectorHelpers(configPath, connectors) {
  await enableConnectorConfig(configPath, connectors);
  const results = [];
  for (const connector of connectors) {
    if (connector === 'analytics') results.push(await installAnalyticsConnector());
    if (connector === 'github') results.push(await installGitHubConnector());
    if (connector === 'asc') results.push(await installAscConnector());
    if (connector === 'revenuecat') results.push(await installRevenueCatConnector());
    if (connector === 'paddle') results.push({ connector, ok: true, detail: 'Paddle uses the built-in metrics exporter; token is checked during preflight' });
    if (connector === 'seo') results.push({ connector, ok: true, detail: 'SEO/GSC uses the built-in exporter; credentials or CSV inputs are checked during preflight' });
    if (connector === 'sentry') results.push(await installSentryConnector());
    if (connector === 'coolify') results.push(await installCoolifyConnector());
    if (isAccountSignalConnector(connector)) results.push(await installAccountSignalConnector(connector));
  }
  return results;
}

function parseGitHubRepoFromRemote(remoteUrl) {
  const value = String(remoteUrl || '').trim();
  if (!value) return null;

  const sshMatch = value.match(/^git@github\.com:([^/]+\/[^/]+?)(?:\.git)?$/i);
  if (sshMatch) return sshMatch[1];

  const httpsMatch = value.match(/^https?:\/\/github\.com\/([^/]+\/[^/]+?)(?:\.git)?$/i);
  if (httpsMatch) return httpsMatch[1];

  return null;
}

function isConfiguredGitHubRepo(value) {
  const repo = String(value || '').trim();
  return Boolean(repo && repo !== 'owner/repo' && /^[^/\s]+\/[^/\s]+$/.test(repo));
}

async function detectGitHubRepo() {
  const explicit = String(process.env.OPENCLAW_GITHUB_REPO || '').trim();
  if (isConfiguredGitHubRepo(explicit)) return explicit;

  const remoteResult = await runShellCommand('git config --get remote.origin.url', 10_000);
  if (!remoteResult.ok) return null;
  return parseGitHubRepoFromRemote(remoteResult.stdout.trim());
}

async function ensureConfig(configPath) {
  if (await fileExists(configPath)) {
    const originalConfig = await readJson(configPath);
    const config = migrateRuntimeSourceCommands(originalConfig);
    let changed = JSON.stringify(originalConfig.sources || {}) !== JSON.stringify(config.sources || {});
    if (!isConfiguredGitHubRepo(config?.project?.githubRepo)) {
      const detectedRepo = await detectGitHubRepo();
      if (detectedRepo) {
        config.project = {
          ...(config.project || {}),
          githubRepo: detectedRepo,
        };
        changed = true;
      }
    }
    if (changed) {
      await writeJson(configPath, config);
      return {
        created: false,
        configPath,
        githubRepo: config.project?.githubRepo || null,
      };
    }
    return {
      created: false,
      configPath,
      githubRepo: null,
    };
  }

  const templatePath = path.resolve(DEFAULT_TEMPLATE_PATH);
  const template = await readJson(templatePath);
  const detectedRepo = await detectGitHubRepo();
  const githubRepo = detectedRepo || '';

  const config = {
    ...template,
    generatedAt: new Date().toISOString(),
    project: {
      ...template.project,
      githubRepo,
      repoRoot: '.',
    },
    sources: {
      ...template.sources,
      analytics: {
        enabled: true,
        mode: 'command',
        command: getRuntimeSourceCommand('analytics'),
      },
      revenuecat: {
        ...(template.sources?.revenuecat || {}),
        enabled: false,
        mode: 'command',
        command: getRuntimeSourceCommand('revenuecat'),
      },
      sentry: {
        ...(template.sources?.sentry || {}),
        enabled: false,
        mode: 'command',
        command: getRuntimeSourceCommand('sentry'),
      },
      coolify: {
        ...(template.sources?.coolify || {}),
        enabled: false,
        mode: 'command',
        command: getRuntimeSourceCommand('coolify'),
        baseUrl: template.sources?.coolify?.baseUrl || process.env.COOLIFY_BASE_URL || 'https://coolify.wotaso.com',
        tokenEnv: template.sources?.coolify?.tokenEnv || 'COOLIFY_API_TOKEN',
      },
      feedback: {
        ...(template.sources?.feedback || {}),
        enabled: false,
      },
      extra: Array.isArray(template.sources?.extra) ? template.sources.extra : [],
    },
    actions: {
      ...template.actions,
      mode: 'issue',
      autoCreateIssues: true,
      autoCreatePullRequests: false,
      draftPullRequests: true,
      proposalBranchPrefix: 'openclaw/proposals',
    },
  };

  await writeJson(configPath, config);
  return {
    created: true,
    configPath,
    githubRepo,
  };
}

function parseJsonFromStdout(stdout) {
  const raw = String(stdout || '').trim();
  if (!raw) return null;
  const firstBrace = raw.indexOf('{');
  const firstBracket = raw.indexOf('[');
  const starts = [firstBrace, firstBracket].filter((index) => index >= 0);
  if (starts.length === 0) return null;
  const jsonStart = Math.min(...starts);
  try {
    return JSON.parse(raw.slice(jsonStart));
  } catch {
    return null;
  }
}

function normalizeString(value) {
  return typeof value === 'string' && value.trim() ? value.trim() : null;
}

function extractProjectChoices(payload) {
  const candidates = (() => {
    if (Array.isArray(payload)) return payload;
    if (payload && typeof payload === 'object') {
      if (Array.isArray(payload.projects)) return payload.projects;
      if (Array.isArray(payload.items)) return payload.items;
      if (Array.isArray(payload.data)) return payload.data;
    }
    return [];
  })();

  const byId = new Map();
  for (const candidate of candidates) {
    if (!candidate || typeof candidate !== 'object') continue;
    const id =
      normalizeString(candidate.id) ||
      normalizeString(candidate.projectId) ||
      normalizeString(candidate.project_id);
    if (!id) continue;
    const name = normalizeString(candidate.name) || normalizeString(candidate.displayName);
    const slug = normalizeString(candidate.slug);
    byId.set(id, {
      id,
      name,
      slug,
      label: name || slug || id,
    });
  }

  return [...byId.values()].sort((a, b) => String(a.label).localeCompare(String(b.label)));
}

function isMissingProjectSelection(text) {
  return /Project ID is missing|Pass --project <id>|analyticscli projects select/i.test(String(text || ''));
}

function commandHasProjectFlag(command) {
  return /(^|\s)--project(\s|=|$)/.test(String(command || ''));
}

function appendProjectFlag(command, projectId) {
  const raw = String(command || '').trim();
  if (!raw || commandHasProjectFlag(raw)) return raw;
  return `${raw} --project ${quote(projectId)}`;
}

function commandHasAscAppFlag(command) {
  return /(^|\s)--app(\s|=|$)/.test(String(command || ''));
}

function removeAscAppFlag(command) {
  const raw = String(command || '').trim();
  if (!raw || !commandHasAscAppFlag(raw)) return raw;
  return raw
    .replace(/(^|\s)--app(?:=(?:"[^"]*"|'[^']*'|\S+)|\s+(?:"[^"]*"|'[^']*'|\S+))/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function appendAscAppFlag(command, appId) {
  const raw = String(command || '').trim();
  if (!raw || commandHasAscAppFlag(raw)) return raw;
  return `${raw} --app ${quote(appId)}`;
}

async function configureAnalyticsProject(configPath, projectId) {
  const normalizedProjectId = normalizeString(projectId);
  if (!normalizedProjectId) return false;

  const config = await readJson(configPath);
  let changed = false;
  for (const sourceName of ['analytics', 'feedback']) {
    const source = config?.sources?.[sourceName];
    if (!source || source.enabled === false || source.mode !== 'command' || !source.command) {
      continue;
    }
    const nextCommand = appendProjectFlag(source.command, normalizedProjectId);
    if (nextCommand !== source.command) {
      source.command = nextCommand;
      changed = true;
    }
  }

  if (!config.project || typeof config.project !== 'object') {
    config.project = {};
  }
  if (config.project.analyticsProjectId !== normalizedProjectId) {
    config.project.analyticsProjectId = normalizedProjectId;
    changed = true;
  }

  if (changed) {
    await writeJson(configPath, config);
  }
  return changed;
}

async function configureAscApp(configPath, appId) {
  const normalizedAppId = normalizeString(appId);
  if (!normalizedAppId) return false;

  const config = await readJson(configPath);
  let changed = false;
  const extraSources = Array.isArray(config?.sources?.extra) ? config.sources.extra : [];

  for (const source of extraSources) {
    if (!source || typeof source !== 'object') continue;
    const service = String(source.service || source.key || '').trim().toLowerCase();
    if (!['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(service)) continue;
    if (source.mode === 'command' && source.command) {
      const nextCommand = appendAscAppFlag(source.command, normalizedAppId);
      if (nextCommand !== source.command) {
        source.command = nextCommand;
        changed = true;
      }
    }
  }

  if (!config.project || typeof config.project !== 'object') {
    config.project = {};
  }
  if (config.project.ascAppId !== normalizedAppId) {
    config.project.ascAppId = normalizedAppId;
    changed = true;
  }

  if (changed) {
    await writeJson(configPath, config);
  }
  process.env.ASC_APP_ID = normalizedAppId;
  return changed;
}

async function configureAscAllApps(configPath) {
  const config = await readJson(configPath);
  let changed = false;
  const extraSources = Array.isArray(config?.sources?.extra) ? config.sources.extra : [];

  for (const source of extraSources) {
    if (!source || typeof source !== 'object') continue;
    const service = String(source.service || source.key || '').trim().toLowerCase();
    if (!['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(service)) continue;
    if (source.mode === 'command' && source.command) {
      const nextCommand = removeAscAppFlag(source.command);
      if (nextCommand !== source.command) {
        source.command = nextCommand;
        changed = true;
      }
    }
  }

  if (config.project && typeof config.project === 'object' && config.project.ascAppId) {
    delete config.project.ascAppId;
    changed = true;
  }

  if (changed) {
    await writeJson(configPath, config);
  }
  delete process.env.ASC_APP_ID;
  return changed;
}

function configHasEnabledAscSource(config) {
  if (config?.sources?.asc && config.sources.asc.enabled !== false) return true;
  const extraSources = Array.isArray(config?.sources?.extra) ? config.sources.extra : [];
  return extraSources.some((source) => {
    if (!source || typeof source !== 'object' || source.enabled === false) return false;
    return isAscSource(source);
  });
}

function extractAscAppChoices(payload) {
  const candidates = (() => {
    if (Array.isArray(payload)) return payload;
    if (payload && typeof payload === 'object') {
      if (Array.isArray(payload.apps)) return payload.apps;
      if (Array.isArray(payload.items)) return payload.items;
      if (Array.isArray(payload.data)) return payload.data;
    }
    return [];
  })();

  const byId = new Map();
  for (const candidate of candidates) {
    if (!candidate || typeof candidate !== 'object') continue;
    const attrs = candidate.attributes && typeof candidate.attributes === 'object' ? candidate.attributes : {};
    const id =
      normalizeString(candidate.id) ||
      normalizeString(candidate.appId) ||
      normalizeString(candidate.app_id);
    if (!id) continue;
    const name =
      normalizeString(candidate.name) ||
      normalizeString(candidate.appName) ||
      normalizeString(candidate.displayName) ||
      normalizeString(attrs.name) ||
      normalizeString(attrs.bundleId);
    const bundleId =
      normalizeString(candidate.bundleId) ||
      normalizeString(candidate.bundle_id) ||
      normalizeString(attrs.bundleId);
    byId.set(id, {
      id,
      name,
      bundleId,
      label: [name || id, bundleId ? `(${bundleId})` : null, id !== name ? id : null].filter(Boolean).join(' '),
    });
  }

  return [...byId.values()].sort((a, b) => String(a.label).localeCompare(String(b.label)));
}

async function listAscApps() {
  const result = await runShellCommand('asc apps list --output json', 60_000, { env: ascIsolatedEnv() });
  if (!result.ok) {
    const fallback = await listAscAppsDirect(60_000);
    if (fallback.ok) return fallback;
    return {
      ok: false,
      error: `${result.stderr || `exit ${result.code}`} Direct Apple API fallback also failed: ${fallback.error}`,
      apps: [],
    };
  }
  const payload = parseJsonFromStdout(result.stdout);
  return {
    ok: true,
    error: null,
    apps: extractAscAppChoices(payload),
  };
}

function isAscAppListDeferredError(error) {
  const normalized = normalizeString(error).toLowerCase();
  if (!normalized) return false;
  if (isInvalidAscPrivateKeyError(error) || isAscPrivateKeyPermissionError(error)) return false;
  return normalized.includes('unexpected error occurred on the server side') ||
    normalized.includes('timed out after') ||
    normalized.includes('fetch failed') ||
    normalized.includes('network timeout') ||
    normalized.includes('econnreset') ||
    normalized.includes('etimedout') ||
    normalized.includes('eai_again') ||
    normalized.includes('enotfound');
}

async function ensureAscAppConfigured(configPath, explicitAppId) {
  if (normalizeString(explicitAppId)) {
    const changed = await configureAscApp(configPath, explicitAppId);
    return { ok: true, configured: true, changed, appId: explicitAppId, appScope: 'single_app', needsUserInput: false };
  }

  const config = await readJson(configPath);
  if (!configHasEnabledAscSource(config)) {
    return { ok: true, configured: false, changed: false, appId: null, appScope: 'disabled', needsUserInput: false };
  }

  const changed = await configureAscAllApps(configPath);

  const appList = await listAscApps();
  if (!appList.ok) {
    if (isAscAppListDeferredError(appList.error)) {
      return {
        ok: true,
        configured: true,
        changed,
        appId: null,
        appScope: 'all_accessible_apps_deferred',
        appCount: null,
        apps: [],
        needsUserInput: false,
        deferred: true,
        detail: 'App Store Connect app listing is temporarily unavailable; saved ASC configuration and will retry app discovery later',
        error: truncate(appList.error, 800),
      };
    }
    return {
      ok: false,
      configured: false,
      changed: false,
      appId: null,
      needsUserInput: false,
      error: truncate(appList.error, 800),
    };
  }

  return {
    ok: true,
    configured: true,
    changed,
    appId: null,
    appScope: 'all_accessible_apps',
    apps: appList.apps,
    appCount: appList.apps.length,
    needsUserInput: false,
  };
}

function extractAscAnalyticsRequestIds(payload) {
  return extractAscAnalyticsRequests(payload).map((request) => request.id);
}

function extractAscAnalyticsRequests(payload) {
  const candidates = (() => {
    if (Array.isArray(payload)) return payload;
    if (payload && typeof payload === 'object') {
      if (Array.isArray(payload.requests)) return payload.requests;
      if (Array.isArray(payload.analyticsReportRequests)) return payload.analyticsReportRequests;
      if (Array.isArray(payload.items)) return payload.items;
      if (Array.isArray(payload.data)) return payload.data;
    }
    return [];
  })();

  const requests = [];
  const seenIds = new Set();
  for (const candidate of candidates) {
    if (!candidate || typeof candidate !== 'object') continue;
    const id = normalizeString(candidate.id) || normalizeString(candidate.requestId) || normalizeString(candidate.request_id);
    if (!id || seenIds.has(id)) continue;
    seenIds.add(id);
    const attributes = candidate.attributes && typeof candidate.attributes === 'object' ? candidate.attributes : {};
    const state = normalizeString(candidate.state) ||
      normalizeString(candidate.requestState) ||
      normalizeString(candidate.request_state) ||
      normalizeString(attributes.state) ||
      normalizeString(attributes.requestState) ||
      normalizeString(attributes.request_state);
    requests.push({ id, state });
  }
  return requests;
}

function extractAscAnalyticsRequestId(payload) {
  if (payload && typeof payload === 'object') {
    const id = normalizeString(payload.id) || normalizeString(payload.requestId) || normalizeString(payload.request_id);
    if (id) return id;
  }
  return extractAscAnalyticsRequestIds(payload)[0] || null;
}

function isAscAnalyticsRequestAlreadyExists(error) {
  const normalized = normalizeString(error).toLowerCase();
  return normalized.includes('already have such an entity') || normalized.includes('state_error');
}

function isAscAnalyticsRequestCreationDeferredError(error) {
  const normalized = normalizeString(error).toLowerCase();
  if (!normalized) return false;
  if (isInvalidAscPrivateKeyError(error) || isAscPrivateKeyPermissionError(error)) return false;
  if (
    normalized.includes('401') ||
    normalized.includes('unauthorized') ||
    normalized.includes('invalid issuer') ||
    normalized.includes('invalid token') ||
    normalized.includes('not authorized')
  ) {
    return false;
  }
  return isAscAppListDeferredError(error) ||
    normalized.includes('forbidden for security') ||
    normalized.includes('for security reasons');
}

async function listAscAnalyticsRequests(appId) {
  const result = await runShellCommand(`asc analytics requests --app ${quote(appId)} --output json`, 60_000, {
    env: ascIsolatedEnv(),
  });
  if (!result.ok) {
    const error = result.stderr || `exit ${result.code}`;
    return {
      ok: false,
      ids: [],
      error: describeAscPrivateKeyAuthFailure('Reports', error) || error,
    };
  }
  const requests = extractAscAnalyticsRequests(parseJsonFromStdout(result.stdout));
  return { ok: true, ids: requests.map((request) => request.id), requests, error: null };
}

function getAscBootstrapAdminEnv() {
  const keyId = normalizeString(process.env.ASC_BOOTSTRAP_KEY_ID);
  const issuerId = normalizeString(process.env.ASC_BOOTSTRAP_ISSUER_ID);
  const privateKeyPath = normalizeString(process.env.ASC_BOOTSTRAP_PRIVATE_KEY_PATH);
  const privateKey = normalizeString(process.env.ASC_BOOTSTRAP_PRIVATE_KEY);
  const privateKeyB64 = normalizeString(process.env.ASC_BOOTSTRAP_PRIVATE_KEY_B64);
  if (!keyId || !issuerId || (!privateKeyPath && !privateKey && !privateKeyB64)) return null;
  return {
    ASC_KEY_ID: keyId,
    ASC_ISSUER_ID: issuerId,
    ...(privateKeyPath ? { ASC_PRIVATE_KEY_PATH: privateKeyPath } : {}),
    ...(privateKey ? { ASC_PRIVATE_KEY: privateKey } : {}),
    ...(privateKeyB64 ? { ASC_PRIVATE_KEY_B64: privateKeyB64 } : {}),
  };
}

async function removeTemporaryAscBootstrapPrivateKey() {
  const shouldDelete = normalizeString(process.env.ASC_BOOTSTRAP_PRIVATE_KEY_DELETE_AFTER_USE);
  const privateKeyPath = normalizeString(process.env.ASC_BOOTSTRAP_PRIVATE_KEY_PATH);
  if (!privateKeyPath || !['1', 'true', 'yes'].includes(shouldDelete.toLowerCase())) return null;
  if (privateKeyPath === normalizeString(process.env.ASC_PRIVATE_KEY_PATH)) {
    return {
      deleted: false,
      detail: 'temporary Admin .p8 path matches ASC_PRIVATE_KEY_PATH; kept it in place',
    };
  }
  return {
    deleted: false,
    detail: `kept temporary Admin .p8 copy at ${privateKeyPath}`,
  };
}

async function ensureAscAnalyticsRequest(appId) {
  const normalizedAppId = normalizeString(appId);
  if (!normalizedAppId) {
    return { ok: true, status: 'skipped', requestId: null, detail: 'no single ASC app configured' };
  }

  const existingRequests = await listAscAnalyticsRequests(normalizedAppId);
  if (existingRequests.ok) {
    const completedRequest = existingRequests.requests.find((request) => normalizeString(request.state)?.toUpperCase() === 'COMPLETED');
    if (completedRequest) {
      return { ok: true, status: 'completed', requestId: completedRequest.id, detail: `completed request ${completedRequest.id}` };
    }
    if (existingRequests.ids.length > 0) {
      return { ok: true, status: 'pending', requestId: existingRequests.ids[0], detail: `existing request ${existingRequests.ids[0]} found; report instances may still be processing` };
    }
  }

  const created = await runShellCommand(
    `asc analytics request --app ${quote(normalizedAppId)} --access-type ONGOING --output json`,
    60_000,
    { env: ascIsolatedEnv() },
  );
  let finalCreated = created;
  let usedBootstrapAdmin = false;
  let attemptedBootstrapAdmin = false;
  if (!created.ok) {
    const bootstrapEnv = getAscBootstrapAdminEnv();
    if (bootstrapEnv) {
      attemptedBootstrapAdmin = true;
      finalCreated = await runShellCommand(
        `asc analytics request --app ${quote(normalizedAppId)} --access-type ONGOING --output json`,
        60_000,
        { env: ascIsolatedEnv(bootstrapEnv) },
      );
      usedBootstrapAdmin = finalCreated.ok;
    }
  }
  if (!finalCreated.ok) {
    const error = finalCreated.stderr || `exit ${finalCreated.code}`;
    if (isAscAnalyticsRequestAlreadyExists(error)) {
      return {
        ok: true,
        status: 'existing',
        requestId: null,
        detail: 'ongoing Analytics Report Request already exists; Apple does not expose request IDs through app-scoped listing',
        usedBootstrapAdmin,
      };
    }
    if (isAscAnalyticsRequestCreationDeferredError(error)) {
      return {
        ok: true,
        status: 'deferred',
        requestId: null,
        detail: 'Apple did not create the Analytics Report Request now; setup saved ASC credentials and will retry later',
        usedBootstrapAdmin,
      };
    }
    const role = attemptedBootstrapAdmin ? 'Setup Admin' : 'Reports';
    return {
      ok: false,
      status: 'create_failed',
      requestId: null,
      error: describeAscPrivateKeyAuthFailure(role, error) || error,
    };
  }

  const requestId = extractAscAnalyticsRequestId(parseJsonFromStdout(finalCreated.stdout));
  return {
    ok: true,
    status: 'created',
    requestId,
    detail: requestId
      ? `created ongoing request ${requestId}${usedBootstrapAdmin ? ' with temporary Admin key' : ''}; report instances will appear after Apple processing`
      : `created ongoing request${usedBootstrapAdmin ? ' with temporary Admin key' : ''}; report instances will appear after Apple processing`,
    usedBootstrapAdmin,
  };
}

async function ensureAscAnalyticsRequestsForAppScope(ascAppSetup) {
  if (!ascAppSetup?.ok || ascAppSetup.appScope === 'disabled') {
    return { ok: true, status: 'skipped', requestId: null, requestIds: [], detail: 'ASC source is not enabled', results: [] };
  }
  if (ascAppSetup.appScope === 'all_accessible_apps_deferred') {
    return {
      ok: true,
      status: 'deferred',
      requestId: null,
      requestIds: [],
      detail: 'Apple app listing is temporarily unavailable; Analytics Report Request check deferred until Apple app discovery works again',
      results: [],
    };
  }

  const apps = ascAppSetup.appId
    ? [{ id: ascAppSetup.appId }]
    : Array.isArray(ascAppSetup.apps)
      ? ascAppSetup.apps.filter((app) => normalizeString(app?.id))
      : [];

  if (apps.length === 0) {
    return { ok: true, status: 'skipped', requestId: null, requestIds: [], detail: 'no accessible ASC apps found', results: [] };
  }

  const results = [];
  for (const app of apps) {
    const result = await ensureAscAnalyticsRequest(app.id);
    results.push({
      appId: app.id,
      appName: app.name || null,
      ...result,
    });
  }

  const failures = results.filter((result) => !result.ok);
  if (failures.length > 0) {
    return {
      ok: false,
      status: failures.length === results.length ? 'failed' : 'partial_failed',
      requestId: null,
      requestIds: results.map((result) => result.requestId).filter(Boolean),
      results,
      error: failures
        .map((failure) => `${failure.appName || failure.appId}: ${failure.error || failure.status || 'unknown error'}`)
        .join('; '),
    };
  }

  const counts = results.reduce((memo, result) => {
    memo[result.status] = (memo[result.status] || 0) + 1;
    return memo;
  }, {});
  const detail = Object.entries(counts)
    .map(([status, count]) => `${count} ${status}`)
    .join(', ');

  return {
    ok: true,
    status: 'ok',
    requestId: results[0]?.requestId || null,
    requestIds: results.map((result) => result.requestId).filter(Boolean),
    detail: `checked ${results.length} ASC app(s): ${detail}`,
    results,
  };
}

async function listAnalyticsProjects() {
  const result = await runShellCommand('analyticscli projects list --format json', 60_000);
  if (!result.ok) {
    return {
      ok: false,
      error: result.stderr || `exit ${result.code}`,
      projects: [],
    };
  }
  const payload = parseJsonFromStdout(result.stdout);
  return {
    ok: true,
    error: null,
    projects: extractProjectChoices(payload),
  };
}

function configHasEnabledAnalyticsSource(config) {
  return Boolean(config?.sources?.analytics && config.sources.analytics.enabled !== false);
}

async function ensureAnalyticsProjectConfigured(configPath, explicitProjectId) {
  if (normalizeString(explicitProjectId)) {
    const changed = await configureAnalyticsProject(configPath, explicitProjectId);
    return { ok: true, configured: true, changed, projectId: explicitProjectId, projectScope: 'single_project', needsUserInput: false };
  }

  const config = await readJson(configPath);
  if (!configHasEnabledAnalyticsSource(config)) {
    return { ok: true, configured: false, changed: false, projectId: null, projectScope: 'disabled', needsUserInput: false };
  }

  const configuredProjectId = normalizeString(config.project?.analyticsProjectId);
  if (configuredProjectId) {
    const changed = await configureAnalyticsProject(configPath, configuredProjectId);
    return { ok: true, configured: true, changed, projectId: configuredProjectId, projectScope: 'single_project', needsUserInput: false };
  }

  const projectList = await listAnalyticsProjects();
  if (!projectList.ok) {
    return {
      ok: true,
      configured: false,
      changed: false,
      projectId: null,
      projectScope: 'all_accessible_projects',
      projectCount: null,
      needsUserInput: false,
      warning: truncate(projectList.error, 800),
    };
  }

  return {
    ok: true,
    configured: false,
    changed: false,
    projectId: null,
    projectScope: 'all_accessible_projects',
    projectCount: projectList.projects.length,
    projects: projectList.projects,
    needsUserInput: false,
  };
}

async function buildProjectSelectionResponse({ configCreated, configPath, projectConfigured, rawError }) {
  const projectList = await listAnalyticsProjects();
  const projects = projectList.projects;
  return {
    ok: false,
    phase: 'analytics_project_scope_error',
    setupComplete: false,
    configCreated,
    configPath,
    projectConfigured,
    needsUserInput: false,
    question: null,
    message: 'An AnalyticsCLI command still requires a project pin, but connector setup should use all accessible projects by default.',
    projects,
    suggestedProjectId: null,
    nextCommand: `node scripts/openclaw-growth-start.mjs --config ${quote(configPath)}`,
    alternatePersistCommand: null,
    retryCommand: `node scripts/openclaw-growth-start.mjs --config ${quote(configPath)}`,
    rawError: truncate(rawError, 800),
    projectListError: projectList.ok ? null : truncate(projectList.error, 800),
  };
}

function remediationForCheck(checkName, configPath) {
  if (checkName === 'dependency:analyticscli') {
    return 'Run AnalyticsCLI CLI with `npx -y @analyticscli/cli --help`, or use `@analyticscli/cli` after stable release.';
  }
  if (checkName === 'project:github-repo') {
    return `Set \`project.githubRepo\` in ${configPath} (owner/repo).`;
  }
  if (checkName.startsWith('secret:GITHUB_TOKEN')) {
    return 'Set `GITHUB_TOKEN` (fine-grained PAT with repository `Issues: Read/Write` and `Contents: Read`).';
  }
  if (checkName === 'source:analytics:file') {
    return 'Write `data/openclaw-growth-engineer/analytics_summary.json` via your analytics refresh step (API-key based source command/file generation).';
  }
  if (checkName === 'connection:analytics') {
    return 'Run `npx -y @analyticscli/growth-engineer wizard --connectors analytics` and paste a fresh AnalyticsCLI readonly CLI token into the local terminal wizard.';
  }
  if (checkName === 'connection:github') {
    return 'Verify `GITHUB_TOKEN` and repo access to `/repos/<owner>/<repo>` + issues API.';
  }
  if (checkName === 'connection:github-pull-requests') {
    return 'Verify `GITHUB_TOKEN` and repo access to `/repos/<owner>/<repo>/pulls`, plus `Pull requests: Read/Write` and `Contents: Read/Write` scopes.';
  }
  if (checkName === 'connection:asc_cli') {
    return 'ASC setup should list all App Store Connect apps the API key can access. Rerun the connector wizard with an API key scoped to the whole account; do not set ASC_APP_ID for normal Growth Engineer runs.';
  }
  return 'Fix this blocker and rerun start.';
}

function isInvalidAscPrivateKeyError(error) {
  return /invalid private key|failed to parse|asn1|sequence truncated|malformed/i.test(String(error || ''));
}

function isAscPrivateKeyPermissionError(error) {
  return /too permissive|chmod 600/i.test(String(error || ''));
}

function describeAscPrivateKeyAuthFailure(role, error) {
  if (isAscPrivateKeyPermissionError(error)) {
    return `ASC ${role} key auth failed: the .p8 file permissions are too open. ${error}`;
  }
  if (isInvalidAscPrivateKeyError(error)) {
    return `ASC ${role} key auth failed: the .p8 key could not be parsed. ${error}`;
  }
  return null;
}

function describeAscAppSetupFailure(error) {
  if (isAscPrivateKeyPermissionError(error)) {
    return 'ASC Reports key auth failed: the .p8 file permissions are too open.';
  }
  if (isInvalidAscPrivateKeyError(error)) {
    return 'ASC Reports key auth failed: the .p8 key could not be parsed.';
  }
  return `Could not list App Store Connect apps (${error || 'unknown error'})`;
}

function remediateAscAppSetupFailure(error) {
  if (isAscPrivateKeyPermissionError(error)) {
    return 'Rerun ASC setup. The wizard copies AuthKey_<KEY_ID>.p8 into a secure local file with chmod 600 before testing asc.';
  }
  if (isInvalidAscPrivateKeyError(error)) {
    return 'Use the original downloaded AuthKey_<KEY_ID>.p8 file for the Reports key. The wizard bypasses old asc keychain/config credentials during setup.';
  }
  return 'Verify ASC credentials, key role access, and `asc apps list --output json`.';
}

async function runPreflight(configPath, testConnections, progressJson = false, onlyConnectors = []) {
  const commandParts = [
    nodeRuntimeScriptCommand('openclaw-growth-preflight.mjs'),
    '--config',
    quote(configPath),
  ];
  if (testConnections) {
    commandParts.push('--test-connections');
  }
  if (onlyConnectors.length > 0) {
    commandParts.push('--only-connectors', quote(onlyConnectors.join(',')));
  }
  if (progressJson) {
    commandParts.push('--progress-json');
  }
  const command = commandParts.join(' ');
  const result = await runShellCommand(command, 180_000, {
    onStderrLine: progressJson
      ? (line) => {
          if (line.startsWith('OPENCLAW_PROGRESS ')) {
            process.stderr.write(`${line}\n`);
          }
        }
      : undefined,
  });
  const payload = parseJsonFromStdout(result.stdout);
  return {
    shell: result,
    payload,
  };
}

async function runFirstPass(configPath) {
  const statePath = path.resolve(deriveStatePathFromConfigPath(configPath));
  const command = `${nodeRuntimeScriptCommand('openclaw-growth-runner.mjs')} --config ${quote(configPath)} --state ${quote(statePath)}`;
  return runShellCommand(command, 300_000);
}

async function main() {
  await loadOpenClawGrowthSecrets();
  const args = parseArgs(process.argv.slice(2));
  const configPath = path.resolve(args.config);
  const schedulerProofPath = path.resolve(deriveSchedulerProofPathFromStatePath(deriveStatePathFromConfigPath(configPath)));

  const configResult = await ensureConfig(configPath);
  const initialConfig = applyOpenClawCronOverrides(await readJson(configPath), args);
  await applyOpenClawSecretRefs(initialConfig);
  const heartbeat = await ensureGrowthHeartbeat(configPath, initialConfig);
  const openclawCron = await ensureOpenClawCronSchedule(configPath, initialConfig, args.openclawCron);
  const hermesCron = await ensureHermesCronSchedule(configPath, initialConfig, args.openclawCron);
  if (!openclawCron.ok) {
    process.stdout.write(
      `${JSON.stringify(
        {
          ok: false,
          phase: 'openclaw_cron_setup',
          configCreated: configResult.created,
          configPath,
          heartbeat,
          openclawCron,
          hermesCron,
          blockers: [
            {
              check: 'scheduler:openclaw-cron',
              detail: openclawCron.detail,
              remediation: openclawCron.remediation || 'Fix OpenClaw cron setup and rerun start.',
            },
          ],
        },
        null,
        2,
      )}\n`,
    );
    process.exitCode = 1;
    return;
  }
  if (!hermesCron.ok) {
    process.stdout.write(
      `${JSON.stringify(
        {
          ok: false,
          phase: 'hermes_cron_setup',
          configCreated: configResult.created,
          configPath,
          heartbeat,
          openclawCron,
          hermesCron,
          blockers: [
            {
              check: 'scheduler:hermes-cron',
              detail: hermesCron.detail,
              remediation: hermesCron.remediation || 'Fix Hermes cron setup and rerun start.',
            },
          ],
        },
        null,
        2,
      )}\n`,
    );
    process.exitCode = 1;
    return;
  }
  const projectConfigured = await configureAnalyticsProject(configPath, args.project);
  const ascAppConfiguredFromArg = await configureAscApp(configPath, args.ascApp);
  const analyticscliEnsure = await ensureAnalyticsCliInstalled();
  if (!analyticscliEnsure.ok) {
    process.stdout.write(
      `${JSON.stringify(
        {
          ok: false,
          phase: 'dependency_setup',
          configCreated: configResult.created,
          configPath,
          heartbeat,
          openclawCron,
          hermesCron,
          projectConfigured,
          ascAppConfigured: ascAppConfiguredFromArg,
          blockers: [
            {
              check: 'dependency:analyticscli',
              detail: analyticscliEnsure.detail,
              remediation: `Install the npm package with \`npm install -g ${ANALYTICSCLI_PACKAGE_SPEC}\` or set ANALYTICSCLI_NPM_PREFIX to a writable prefix.`,
            },
          ],
        },
        null,
        2,
      )}\n`,
    );
    process.exitCode = 1;
    return;
  }

  if (args.connectors.length > 0) {
    emitProgress(args.progressJson, {
      phase: 'start',
      key: 'connectorSetup',
      label: 'Connector helpers',
      detail: 'installing and enabling selected helpers',
    });
  }
  const connectorSetup = args.connectors.length > 0 ? await installConnectorHelpers(configPath, args.connectors) : [];
  const failedConnectors = connectorSetup.filter((entry) => !entry.ok);
  if (args.connectors.length > 0) {
    emitProgress(args.progressJson, {
      phase: 'finish',
      key: 'connectorSetup',
      label: 'Connector helpers',
      detail: failedConnectors.length > 0
        ? `${failedConnectors.length} helper setup step(s) need attention`
        : 'selected helpers enabled',
      status: failedConnectors.length > 0 ? 'fail' : 'pass',
    });
  }
  if (failedConnectors.length > 0 && !args.run) {
    process.stdout.write(
      `${JSON.stringify(
        {
          ok: false,
          phase: 'connector_setup',
          configCreated: configResult.created,
          configPath,
          heartbeat,
          openclawCron,
          hermesCron,
          projectConfigured,
          ascAppConfigured: ascAppConfiguredFromArg,
          connectorSetup,
          blockers: failedConnectors.map((entry) => ({
            check: `connector:${entry.connector}`,
            detail: entry.detail,
            remediation:
              entry.connector === 'analytics'
                ? 'Paste a fresh AnalyticsCLI readonly token into the connector wizard so it can store ANALYTICSCLI_ACCESS_TOKEN.'
                : entry.connector === 'github'
                ? 'Provide a GitHub token through the connector wizard for code access.'
                : entry.connector === 'asc'
                  ? 'Install the ASC CLI and provide ASC_KEY_ID, ASC_ISSUER_ID, and ASC_PRIVATE_KEY_PATH or ASC_PRIVATE_KEY. Resolve the app after auth succeeds.'
                  : entry.connector === 'sentry'
                    ? 'Set SENTRY_AUTH_TOKEN plus SENTRY_ORG in the connector wizard. Defer project scope to app/repo context, or configure sources.sentry.accounts[].projects[] only when a fixed mapping is known.'
                    : entry.connector === 'coolify'
                      ? 'Set COOLIFY_BASE_URL and COOLIFY_API_TOKEN from Coolify Keys & Tokens / API tokens in the connector wizard.'
                    : 'Set REVENUECAT_API_KEY and rerun connector setup to write RevenueCat MCP config.',
          })),
        },
        null,
        2,
      )}\n`,
    );
    process.exitCode = 1;
    return;
  }

  emitProgress(args.progressJson, {
    phase: 'start',
    key: 'analyticsProject',
    label: 'AnalyticsCLI scope',
    detail: 'checking accessible analytics projects',
  });
  const analyticsProjectSetup = await ensureAnalyticsProjectConfigured(configPath, args.project);
  emitProgress(args.progressJson, {
    phase: 'finish',
    key: 'analyticsProject',
    label: 'AnalyticsCLI scope',
    detail: analyticsProjectSetup.ok
      ? analyticsProjectSetup.projectId
        ? `using ${analyticsProjectSetup.projectId}`
        : analyticsProjectSetup.projectScope === 'all_accessible_projects'
          ? `using all accessible projects (${analyticsProjectSetup.projectCount ?? 'unknown'} found)`
          : 'no project pin needed'
      : 'analytics scope check failed',
    status: analyticsProjectSetup.ok ? 'pass' : 'fail',
  });
  const shouldRunAscSetup =
    args.onlyConnectors.length === 0 ||
    args.onlyConnectors.includes('asc') ||
    Boolean(normalizeString(args.ascApp)) ||
    configHasEnabledAscSource(initialConfig);
  let ascAppSetup: any = {
    ok: true,
    configured: false,
    changed: false,
    appId: null,
    appScope: 'skipped_by_connector_filter',
    needsUserInput: false,
  };
  let ascAnalyticsRequestSetup: any = {
    ok: true,
    status: 'skipped',
    requestId: null,
    requestIds: [],
    detail: 'ASC connector was not selected',
    results: [],
  };

  if (shouldRunAscSetup) {
    emitProgress(args.progressJson, {
      phase: 'start',
      key: 'ascApp',
      label: 'ASC app scope',
      detail: 'resolving App Store Connect app scope',
    });
    ascAppSetup = await ensureAscAppConfigured(configPath, args.ascApp);
    emitProgress(args.progressJson, {
      phase: 'finish',
      key: 'ascApp',
      label: 'ASC app scope',
      detail: ascAppSetup.ok
        ? ascAppSetup.appId
          ? `using app ${ascAppSetup.appId}`
          : ascAppSetup.appScope === 'all_accessible_apps'
            ? `using all accessible apps (${ascAppSetup.appCount || 0} found)`
            : ascAppSetup.appScope === 'all_accessible_apps_deferred'
              ? 'saved ASC config; app discovery deferred because Apple app listing is temporarily unavailable'
            : 'not enabled'
        : describeAscAppSetupFailure(ascAppSetup.error),
      status: ascAppSetup.ok ? 'pass' : 'fail',
    });
    if (!ascAppSetup.ok) {
      process.stdout.write(
        `${JSON.stringify(
          {
            ok: false,
            phase: 'asc_app_setup',
            configCreated: configResult.created,
            configPath,
            heartbeat,
            openclawCron,
            hermesCron,
            projectConfigured: projectConfigured || analyticsProjectSetup.configured,
            analyticsProjectId: analyticsProjectSetup.projectId || null,
            ascAppConfigured: false,
            connectorSetup,
            needsUserInput: false,
            question: null,
            apps: [],
            nextCommand: null,
            blockers: [
              {
                check: 'connection:asc_app',
                detail: describeAscAppSetupFailure(ascAppSetup.error),
                remediation: remediateAscAppSetupFailure(ascAppSetup.error),
              },
            ],
          },
          null,
          2,
        )}\n`,
      );
      process.exitCode = 1;
      return;
    }

    emitProgress(args.progressJson, {
      phase: 'start',
      key: 'ascAnalyticsRequest',
      label: 'ASC analytics reports',
      detail: 'checking ongoing Analytics Report Request',
    });
    ascAnalyticsRequestSetup = await ensureAscAnalyticsRequestsForAppScope(ascAppSetup);
    const temporaryAscBootstrapKeyCleanup = await removeTemporaryAscBootstrapPrivateKey();
    if (temporaryAscBootstrapKeyCleanup?.detail) {
      emitProgress(args.progressJson, {
        phase: 'finish',
        key: 'ascBootstrapAdminKeyCleanup',
        label: 'ASC temporary Admin key',
        detail: temporaryAscBootstrapKeyCleanup.detail,
        status: 'pass',
      });
      process.stderr.write(`${temporaryAscBootstrapKeyCleanup.detail}. Revoke the temporary Admin API key in App Store Connect.\n`);
    }
    emitProgress(args.progressJson, {
      phase: 'finish',
      key: 'ascAnalyticsRequest',
      label: 'ASC analytics reports',
      detail: ascAnalyticsRequestSetup.ok
        ? ascAnalyticsRequestSetup.detail
        : `could not ensure Analytics Report Request (${truncate(ascAnalyticsRequestSetup.error, 240)})`,
      status: ascAnalyticsRequestSetup.ok ? 'pass' : 'fail',
    });
    if (!ascAnalyticsRequestSetup.ok) {
      process.stdout.write(
        `${JSON.stringify(
          {
            ok: false,
            phase: 'asc_analytics_request_setup',
            configCreated: configResult.created,
            configPath,
            heartbeat,
            openclawCron,
            hermesCron,
            projectConfigured: projectConfigured || analyticsProjectSetup.configured,
            analyticsProjectId: analyticsProjectSetup.projectId || null,
            ascAppConfigured: ascAppSetup.configured,
            ascAppId: ascAppSetup.appId || null,
            ascAppScope: ascAppSetup.appScope || null,
            ascAnalyticsRequestResults: ascAnalyticsRequestSetup.results || [],
            connectorSetup,
            needsUserInput: false,
            question: null,
            blockers: [
              {
                check: 'connection:asc_analytics_request',
                detail: `Could not ensure App Store Connect Analytics Report Request: ${truncate(ascAnalyticsRequestSetup.error, 800)}`,
                remediation: 'Create the ongoing Analytics Report Request once with a temporary ASC Admin key. After the request exists, remove or revoke the Admin key and keep Growth Engineer configured with Sales and Reports or Finance for daily downloads.',
              },
            ],
          },
          null,
          2,
        )}\n`,
      );
      process.exitCode = 1;
      return;
    }
  }

  const preflightResult = await runPreflight(configPath, args.testConnections, args.progressJson, args.onlyConnectors);
  const preflightPayload = preflightResult.payload;

  if (!preflightPayload) {
    throw new Error(
      `Preflight returned invalid output.\nstdout:\n${preflightResult.shell.stdout}\nstderr:\n${preflightResult.shell.stderr}`,
    );
  }

  const failures = Array.isArray(preflightPayload.checks)
    ? preflightPayload.checks.filter((check) => check.status === 'fail')
    : [];

  if (failures.length > 0) {
    const blockers = failures.map((check) => ({
      check: check.name,
      detail: check.detail,
      remediation: remediationForCheck(check.name, configPath),
    }));
    process.stdout.write(
      `${JSON.stringify(
        {
          ok: false,
          phase: 'preflight',
          configCreated: configResult.created,
          configPath,
          heartbeat,
          openclawCron,
          hermesCron,
          projectConfigured: projectConfigured || analyticsProjectSetup.configured,
          analyticsProjectId: analyticsProjectSetup.projectId || null,
          ascAppConfigured: ascAppSetup.configured,
          ascAppId: ascAppSetup.appId || null,
          ascAppScope: ascAppSetup.appScope || null,
          ascAnalyticsRequestStatus: ascAnalyticsRequestSetup.status,
          ascAnalyticsRequestId: ascAnalyticsRequestSetup.requestId || null,
          ascAnalyticsRequestIds: ascAnalyticsRequestSetup.requestIds || [],
          githubRepo: configResult.githubRepo,
          connectorSetup,
          checks: preflightPayload.checks || [],
          blockers,
        },
        null,
        2,
      )}\n`,
    );
    process.exitCode = 1;
    return;
  }

  if (!args.run) {
    process.stdout.write(
      `${JSON.stringify(
        {
          ok: true,
          phase: 'setup_complete',
          configCreated: configResult.created,
          configPath,
          heartbeat,
          openclawCron,
          hermesCron,
          projectConfigured: projectConfigured || analyticsProjectSetup.configured,
          analyticsProjectId: analyticsProjectSetup.projectId || null,
          ascAppConfigured: ascAppSetup.configured,
          ascAppId: ascAppSetup.appId || null,
          ascAppScope: ascAppSetup.appScope || null,
          ascAnalyticsRequestStatus: ascAnalyticsRequestSetup.status,
          ascAnalyticsRequestId: ascAnalyticsRequestSetup.requestId || null,
          ascAnalyticsRequestIds: ascAnalyticsRequestSetup.requestIds || [],
          connectorSetup,
          schedulerProofPath,
          message: 'Preflight passed. First run skipped due to --setup-only.',
        },
        null,
        2,
      )}\n`,
    );
    return;
  }

  const runResult = await runFirstPass(configPath);
  if (!runResult.ok) {
    const rawError = runResult.stderr || `exit ${runResult.code}`;
    if (isMissingProjectSelection(rawError)) {
      process.stdout.write(
        `${JSON.stringify(
          await buildProjectSelectionResponse({
            configCreated: configResult.created,
            configPath,
            projectConfigured,
            rawError,
          }),
          null,
          2,
        )}\n`,
      );
      return;
    }

    process.stdout.write(
      `${JSON.stringify(
        {
          ok: false,
          phase: 'first_run',
          configCreated: configResult.created,
          configPath,
          heartbeat,
          openclawCron,
          hermesCron,
          projectConfigured,
          error: rawError,
        },
        null,
        2,
      )}\n`,
    );
    process.exitCode = 1;
    return;
  }

  const actionMode = getActionMode(await readJson(configPath));
  process.stdout.write(
    `${JSON.stringify(
      {
        ok: true,
        phase: 'first_run_complete',
        configCreated: configResult.created,
        configPath,
        heartbeat,
        openclawCron,
        hermesCron,
        projectConfigured,
        actionMode,
        runnerOutput: runResult.stdout.trim(),
        schedulerProofPath,
      },
      null,
      2,
    )}\n`,
  );
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
