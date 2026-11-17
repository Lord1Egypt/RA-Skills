#!/usr/bin/env node

import { existsSync, promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createSign } from 'node:crypto';
import { applyOpenClawSecretRefs, loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';

const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const DEFAULT_TIMEOUT_MS = 15_000;
const RUNTIME_DIR = path.dirname(fileURLToPath(import.meta.url));
const WIZARD_COMMAND = 'npx -y @analyticscli/growth-engineer wizard';

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
OpenClaw Growth Connector Status

Usage:
  node scripts/openclaw-growth-status.mjs [options]

Options:
  --config <file>      Config path (default: ${DEFAULT_CONFIG_PATH})
  --timeout-ms <ms>    Live check timeout in milliseconds (default: ${DEFAULT_TIMEOUT_MS})
  --only-connectors <list>
                       Limit live checks to selected connectors
  --json               Print JSON (default)
  --progress-json      Emit machine-readable connector progress events on stderr
  --help, -h           Show help
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
    timeoutMs: DEFAULT_TIMEOUT_MS,
    json: true,
    progressJson: false,
    onlyConnectors: [] as string[],
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    const next = argv[index + 1];
    if (token === '--') {
      continue;
    } else if (token === '--config') {
      args.config = next || args.config;
      index += 1;
    } else if (token === '--timeout-ms') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for --timeout-ms: ${String(next || '')}`);
      }
      args.timeoutMs = parsed;
      index += 1;
    } else if (token === '--json') {
      args.json = true;
    } else if (token === '--progress-json') {
      args.progressJson = true;
    } else if (token === '--only-connectors') {
      args.onlyConnectors = String(next || '')
        .split(',')
        .map((entry) => entry.trim())
        .filter(Boolean);
      index += 1;
    } else if (token === '--help' || token === '-h') {
      printHelpAndExit(0);
    } else {
      printHelpAndExit(1, `Unknown argument: ${token}`);
    }
  }

  return args;
}

function onlyAllows(onlyConnectors: string[], connector: string) {
  return !Array.isArray(onlyConnectors) || onlyConnectors.length === 0 || onlyConnectors.includes(connector);
}

function quote(value) {
  if (/^[a-zA-Z0-9_./:=@-]+$/.test(String(value))) {
    return String(value);
  }
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function resolveRuntimeScriptPath(scriptName) {
  const candidates = [
    path.join(RUNTIME_DIR, scriptName),
    path.resolve('scripts', scriptName),
    path.resolve('skills/openclaw-growth-engineer/scripts', scriptName),
  ];
  return candidates.find((candidate) => existsSync(candidate)) || path.join(RUNTIME_DIR, scriptName);
}

function nodeRuntimeScriptCommand(scriptName) {
  return `node ${quote(resolveRuntimeScriptPath(scriptName))}`;
}

function emitProgress(enabled, event) {
  if (!enabled) return;
  process.stderr.write(`OPENCLAW_PROGRESS ${JSON.stringify(event)}\n`);
}

function runShell(
  command,
  options: { cwd?: string; timeoutMs?: number; onStderrLine?: (line: string) => void } = {},
): Promise<ShellResult> {
  return new Promise((resolve) => {
    const child = spawn('/bin/sh', ['-lc', command], {
      cwd: options.cwd || process.cwd(),
      env: process.env,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    let stderrBuffer = '';
    const timer = setTimeout(() => {
      child.kill('SIGTERM');
    }, options.timeoutMs || DEFAULT_TIMEOUT_MS);
    child.stdout.on('data', (chunk) => {
      stdout += String(chunk);
    });
    child.stderr.on('data', (chunk) => {
      const text = String(chunk);
      stderr += text;
      if (options.onStderrLine) {
        stderrBuffer += text;
        const lines = stderrBuffer.split(/\r?\n/);
        stderrBuffer = lines.pop() || '';
        for (const line of lines) options.onStderrLine(line);
      }
    });
    child.on('error', (error) => {
      clearTimeout(timer);
      resolve({ ok: false, code: null, stdout, stderr: error.message });
    });
    child.on('close', (code) => {
      clearTimeout(timer);
      if (options.onStderrLine && stderrBuffer.trim()) options.onStderrLine(stderrBuffer.trim());
      resolve({ ok: code === 0, code, stdout, stderr });
    });
  });
}

async function readJson(filePath): Promise<any> {
  const raw = await fs.readFile(filePath, 'utf8');
  return JSON.parse(raw);
}

function checkByName(preflight, name) {
  return (Array.isArray(preflight?.checks) ? preflight.checks : []).find((check) => check?.name === name) || null;
}

function checksByPrefix(preflight, prefix) {
  return (Array.isArray(preflight?.checks) ? preflight.checks : []).filter((check) =>
    String(check?.name || '').startsWith(prefix),
  );
}

function connector(status, detail, extra: Record<string, unknown> = {}) {
  return {
    status,
    detail,
    ...extra,
  };
}

function isAscSource(source: any) {
  const service = String(source?.service || source?.key || '').trim().toLowerCase();
  return ['asc', 'asc-cli', 'app-store-connect', 'app_store_connect'].includes(service);
}

function configHasEnabledAscSource(config: any) {
  if (config?.sources?.asc && config.sources.asc.enabled !== false) return true;
  return (Array.isArray(config?.sources?.extra) ? config.sources.extra : []).some(
    (source) => isAscSource(source) && source?.enabled !== false,
  );
}

function getSentryAccountMetadata(config) {
  const sentrySource = config?.sources?.sentry || {};
  const configured = Array.isArray(sentrySource.accounts) ? sentrySource.accounts : [];
  const accounts = configured.length > 0
    ? configured
    : [{
        id: 'sentry',
        label: 'Sentry',
        baseUrl: process.env.SENTRY_BASE_URL || 'https://sentry.io',
        tokenEnv: config?.secrets?.sentryTokenEnv || 'SENTRY_AUTH_TOKEN',
        org: process.env.SENTRY_ORG || '',
        projects: process.env.SENTRY_PROJECT ? [process.env.SENTRY_PROJECT] : [],
        environment: process.env.SENTRY_ENVIRONMENT || 'production',
      }];
  const byId = new Map();
  for (const [index, account] of accounts.entries()) {
    const id = String(account?.id || account?.key || account?.label || `sentry_${index + 1}`)
      .trim()
      .replace(/[^a-zA-Z0-9._-]+/g, '_');
    byId.set(id, {
      id,
      label: String(account?.label || account?.name || account?.id || `Sentry ${index + 1}`).trim(),
      baseUrl: String(account?.baseUrl || account?.base_url || account?.url || 'https://sentry.io').trim(),
      org: String(account?.org || account?.organization || '').trim(),
      projects: Array.isArray(account?.projects)
        ? account.projects.map((project) => String(typeof project === 'string' ? project : project?.project || project?.slug || '').trim()).filter(Boolean)
        : account?.project
          ? [String(account.project).trim()].filter(Boolean)
          : [],
      environment: String(account?.environment || process.env.SENTRY_ENVIRONMENT || 'production').trim(),
    });
  }
  return byId;
}

function isEnabled(source) {
  return Boolean(source && source.enabled !== false);
}

function isConfiguredRepo(value) {
  const repo = String(value || '').trim();
  return Boolean(repo && repo !== 'owner/repo' && /^[^/\s]+\/[^/\s]+$/.test(repo));
}

function normalizeString(value) {
  return String(value || '').trim();
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

async function fetchAscApiJson(pathname, timeoutMs = DEFAULT_TIMEOUT_MS, env: NodeJS.ProcessEnv = process.env) {
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

async function listAscAppIdsDirect(timeoutMs = DEFAULT_TIMEOUT_MS) {
  const result = await fetchAscApiJson('/v1/apps?limit=200', timeoutMs, process.env);
  if (!result.ok) {
    return {
      ok: false,
      error: result.error || `Apple API returned HTTP ${result.status}`,
      appIds: [],
    };
  }
  return {
    ok: true,
    error: null,
    appIds: extractAscAppIds(result.payload),
  };
}

function parseJsonFromStdout(stdout) {
  const text = String(stdout || '').trim();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    const first = text.indexOf('{');
    const last = text.lastIndexOf('}');
    if (first >= 0 && last > first) {
      try {
        return JSON.parse(text.slice(first, last + 1));
      } catch {
        return null;
      }
    }
    return null;
  }
}

function extractAscAppIds(payload) {
  const candidates = (() => {
    if (Array.isArray(payload)) return payload;
    if (payload && typeof payload === 'object') {
      if (Array.isArray(payload.apps)) return payload.apps;
      if (Array.isArray(payload.items)) return payload.items;
      if (Array.isArray(payload.data)) return payload.data;
    }
    return [];
  })();
  const ids = [];
  for (const candidate of candidates) {
    const attrs = candidate?.attributes && typeof candidate.attributes === 'object' ? candidate.attributes : {};
    const id = normalizeString(candidate?.id) || normalizeString(candidate?.appId) || normalizeString(candidate?.app_id) || normalizeString(attrs.id);
    if (id) ids.push(id);
  }
  return [...new Set(ids)];
}

function extractAscAnalyticsRequestIds(payload) {
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
  const ids = [];
  for (const candidate of candidates) {
    const id = normalizeString(candidate?.id) || normalizeString(candidate?.requestId) || normalizeString(candidate?.request_id);
    if (id) ids.push(id);
  }
  return [...new Set(ids)];
}

function isAscAnalyticsRequestCollectionUnsupported(error) {
  const normalized = normalizeString(error).toLowerCase();
  return normalized.includes("does not allow 'get_collection'") ||
    normalized.includes('allowed operations are: create, delete, get_instance');
}

function isAscAppListDeferredError(detail) {
  const normalized = normalizeString(detail).toLowerCase();
  if (!normalized) return false;
  if (
    normalized.includes('credentials are incomplete') ||
    normalized.includes('401') ||
    normalized.includes('403') ||
    normalized.includes('forbidden') ||
    normalized.includes('unauthorized') ||
    normalized.includes('not authorized') ||
    normalized.includes('invalid issuer') ||
    normalized.includes('invalid token')
  ) {
    return false;
  }
  return normalized.includes('unexpected error occurred on the server side') ||
    normalized.includes('timed out after') ||
    normalized.includes('fetch failed') ||
    normalized.includes('network timeout') ||
    normalized.includes('econnreset') ||
    normalized.includes('etimedout') ||
    normalized.includes('eai_again') ||
    normalized.includes('enotfound');
}

async function runPreflight(configPath, timeoutMs, progressJson = false, onlyConnectors: string[] = []) {
  const command = [
    nodeRuntimeScriptCommand('openclaw-growth-preflight.mjs'),
    '--config',
    quote(configPath),
    '--test-connections',
    '--timeout-ms',
    String(timeoutMs),
    '--json',
    ...(onlyConnectors.length > 0 ? ['--only-connectors', quote(onlyConnectors.join(','))] : []),
    ...(progressJson ? ['--progress-json'] : []),
  ].join(' ');
  const result = await runShell(command, {
    timeoutMs: Math.max(timeoutMs + 5_000, 20_000),
    onStderrLine: progressJson
      ? (line) => {
          if (line.startsWith('OPENCLAW_PROGRESS ')) process.stderr.write(`${line}\n`);
        }
      : undefined,
  });
  const output = result.stdout.trim();
  if (!output) {
    return {
      ok: false,
      error: result.stderr.trim() || 'preflight returned no JSON output',
      payload: null,
    };
  }
  try {
    return {
      ok: true,
      error: null,
      payload: JSON.parse(output),
    };
  } catch {
    return {
      ok: false,
      error: result.stderr.trim() || 'preflight returned invalid JSON',
      payload: null,
    };
  }
}

async function checkGitHub(config, timeoutMs) {
  const repo = String(config?.project?.githubRepo || '').trim();
  const hasRepo = isConfiguredRepo(repo);
  const token = String(process.env.GITHUB_TOKEN || '').trim();

  if (token && hasRepo) {
    const result = await runShell(`gh api ${quote(`repos/${repo}`)} >/dev/null`, { timeoutMs });
    if (result.ok) {
      return connector('connected', `GitHub token can read ${repo}`, { repo });
    }
    const fallback = await runShell(
      `curl -fsS -H ${quote('Accept: application/vnd.github+json')} -H ${quote(`Authorization: Bearer ${token}`)} ${quote(`https://api.github.com/repos/${repo}`)} >/dev/null`,
      { timeoutMs },
    );
    return fallback.ok
      ? connector('connected', `GitHub token can read ${repo}`, { repo })
      : connector('blocked', `GITHUB_TOKEN is set, but repo access check failed for ${repo}`, { repo });
  }

  if (hasRepo) {
    const ghStatus = await runShell('gh auth status >/dev/null 2>&1', { timeoutMs });
    if (ghStatus.ok) {
      const repoCheck = await runShell(`gh api ${quote(`repos/${repo}`)} >/dev/null`, { timeoutMs });
      return repoCheck.ok
        ? connector('connected', `gh auth can read ${repo}`, { repo })
        : connector('blocked', `gh is logged in, but cannot read ${repo}`, { repo });
    }
  }

  if (token && !hasRepo) {
    const authCheck = await runShell(
      `curl -fsS -H ${quote('Accept: application/vnd.github+json')} -H ${quote(`Authorization: Bearer ${token}`)} https://api.github.com/user >/dev/null`,
      { timeoutMs },
    );
    return authCheck.ok ? connector('connected', 'GITHUB_TOKEN is valid; repo selection is deferred per app/task', {
      repoScope: 'per_app_or_task',
    }) : connector('blocked', 'GITHUB_TOKEN is set, but GitHub auth check failed', {
      nextAction: `Run: ${WIZARD_COMMAND} --connectors github.`,
    });
  }
  return connector('not_connected', hasRepo ? 'No GITHUB_TOKEN or gh auth found' : 'project.githubRepo is not configured', {
    nextAction: `Run: ${WIZARD_COMMAND} --connectors github.`,
  });
}

async function checkAscAnalyticsReadiness(timeoutMs) {
  const vendorNumber = normalizeString(process.env.ASC_VENDOR_NUMBER);
  const appList = await runShell('asc apps list --output json', { timeoutMs: Math.max(5_000, timeoutMs) });
  const directAppList = appList.ok ? null : await listAscAppIdsDirect(Math.max(5_000, timeoutMs));
  if (!appList.ok && !directAppList?.ok) {
    const detail = `ASC App Analytics readiness could not list apps with asc CLI or direct Apple API: ${normalizeString(appList.stderr) || `exit ${appList.code}`}; ${directAppList?.error || 'direct API failed'}`;
    if (isAscAppListDeferredError(detail)) {
      if (!vendorNumber) {
        return {
          status: 'partial',
          detail: 'ASC credentials are configured, but Apple app discovery is temporarily unavailable and ASC_VENDOR_NUMBER is missing for Sales and Trends/App Units',
          vendorNumber,
          appCount: 0,
          checkedAppCount: 0,
          requestCount: 0,
        };
      }
      return {
        status: 'connected',
        detail: 'ASC credentials and ASC_VENDOR_NUMBER are configured; Apple app discovery is temporarily unavailable and will retry later',
        vendorNumber,
        appCount: 0,
        checkedAppCount: 0,
        requestCount: 0,
      };
    }
    return {
      status: 'blocked',
      detail,
      vendorNumber,
      appCount: 0,
      checkedAppCount: 0,
      requestCount: 0,
    };
  }

  const appIds = appList.ok ? extractAscAppIds(parseJsonFromStdout(appList.stdout)) : directAppList?.appIds || [];
  if (appIds.length === 0) {
    return {
      status: 'blocked',
      detail: 'ASC App Analytics readiness found no accessible apps; App Analytics reports cannot be verified',
      vendorNumber,
      appCount: 0,
      checkedAppCount: 0,
      requestCount: 0,
    };
  }

  const checkedAppIds = appIds.slice(0, 12);
  const results: any[] = [];
  for (const appId of checkedAppIds) {
    const result = await runShell(`asc analytics requests --app ${quote(appId)} --output json`, {
      timeoutMs: Math.max(5_000, timeoutMs),
    });
    const error = result.ok ? null : normalizeString(result.stderr) || `exit ${result.code}`;
    const collectionUnsupported = !result.ok && isAscAnalyticsRequestCollectionUnsupported(error);
    const ids = result.ok ? extractAscAnalyticsRequestIds(parseJsonFromStdout(result.stdout)) : [];
    results.push({
      appId,
      ok: result.ok || collectionUnsupported,
      collectionUnsupported,
      requestCount: ids.length,
      error: collectionUnsupported ? null : error,
    });
  }

  const failed = results.filter((result) => !result.ok);
  const appsWithRequests = results.filter((result) => result.requestCount > 0);
  const collectionUnsupportedCount = results.filter((result) => result.collectionUnsupported).length;
  const requestCount = results.reduce((sum, result) => sum + Number(result.requestCount || 0), 0);
  if (failed.length > 0) {
    return {
      status: 'blocked',
      detail: `ASC App Analytics report requests could not be queried for ${failed.length}/${results.length} checked app(s): ${failed[0].error}`,
      vendorNumber,
      appCount: appIds.length,
      checkedAppCount: results.length,
      requestCount,
      results,
    };
  }
  if (collectionUnsupportedCount > 0) {
    if (!vendorNumber) {
      return {
        status: 'partial',
        detail: `ASC API auth and app access are available for ${results.length} checked app(s), but ASC_VENDOR_NUMBER is missing for Sales and Trends/App Units`,
        vendorNumber,
        appCount: appIds.length,
        checkedAppCount: results.length,
        requestCount,
        results,
      };
    }
    return {
      status: 'connected',
      detail: `ASC API auth, app access, and ASC_VENDOR_NUMBER are available for ${results.length} checked app(s); Apple does not allow app-scoped request listing, so setup verifies existing requests through create/duplicate handling`,
      vendorNumber,
      appCount: appIds.length,
      checkedAppCount: results.length,
      requestCount,
      results,
    };
  }
  if (appsWithRequests.length === 0) {
    return {
      status: 'blocked',
      detail: `ASC App Analytics has no report requests for ${results.length} checked app(s); create the initial ongoing Analytics Report Requests once with a temporary Admin key, then run steady-state ingestion with Sales and Reports or Finance`,
      vendorNumber,
      appCount: appIds.length,
      checkedAppCount: results.length,
      requestCount: 0,
      results,
    };
  }
  if (!vendorNumber) {
    return {
      status: 'partial',
      detail: `ASC App Analytics report requests exist for ${appsWithRequests.length}/${results.length} checked app(s), but ASC_VENDOR_NUMBER is missing for Sales and Trends/App Units`,
      vendorNumber,
      appCount: appIds.length,
      checkedAppCount: results.length,
      requestCount,
      results,
    };
  }
  if (appsWithRequests.length < results.length) {
    return {
      status: 'partial',
      detail: `ASC App Analytics report requests exist for ${appsWithRequests.length}/${results.length} checked app(s); missing requests must be created for full account coverage`,
      vendorNumber,
      appCount: appIds.length,
      checkedAppCount: results.length,
      requestCount,
      results,
    };
  }
  return {
    status: 'connected',
    detail: `ASC API auth, App Analytics report requests, and ASC_VENDOR_NUMBER are available for ${results.length} checked app(s)`,
    vendorNumber,
    appCount: appIds.length,
    checkedAppCount: results.length,
    requestCount,
    results,
  };
}

function summarizeAnalytics(preflight, config) {
  if (!isEnabled(config?.sources?.analytics)) {
    return connector('blocked', 'AnalyticsCLI source is disabled');
  }
  const connection = checkByName(preflight, 'connection:analytics');
  const command = checkByName(preflight, 'connection:analytics-command');
  if (connection?.status === 'pass' && (!command || command.status === 'pass')) {
    return connector('connected', 'AnalyticsCLI auth and exporter smoke test passed');
  }
  if (connection?.status === 'pass' && command?.status !== 'pass') {
    return connector('partial', command?.detail || 'AnalyticsCLI auth passed, exporter smoke test did not pass');
  }
  return connector('blocked', connection?.detail || 'AnalyticsCLI connection was not verified');
}

function summarizeRevenueCat(preflight, config) {
  if (!isEnabled(config?.sources?.revenuecat)) {
    return connector('not_enabled', 'RevenueCat source is disabled');
  }
  const connection = checkByName(preflight, 'connection:revenuecat');
  if (connection?.status === 'pass') {
    return connector('connected', 'RevenueCat API key live check passed');
  }
  return connector('blocked', connection?.detail || 'RevenueCat connection was not verified');
}

function summarizeSentry(preflight, config) {
  if (!isEnabled(config?.sources?.sentry)) {
    return connector('not_enabled', 'Sentry source is disabled');
  }
  const accountConnections = checksByPrefix(preflight, 'connection:sentry:');
  const connection = checkByName(preflight, 'connection:sentry');
  const command = checkByName(preflight, 'connection:sentry-command');
  const accountMetadata = getSentryAccountMetadata(config);
  if (accountConnections.length > 0) {
    const failed = accountConnections.filter((entry) => entry.status !== 'pass');
    const accounts = accountConnections.map((entry) => ({
      ...(accountMetadata.get(String(entry.name || '').replace(/^connection:sentry:/, '')) || {}),
      id: String(entry.name || '').replace(/^connection:sentry:/, ''),
      status: entry.status === 'pass' ? 'connected' : 'blocked',
      detail: entry.detail,
    }));
    if (failed.length === 0 && (!command || command.status === 'pass')) {
      return connector('connected', `Sentry API checks passed for ${accountConnections.length} account(s)`, { accounts });
    }
    if (failed.length === 0 && command?.status !== 'pass') {
      return connector('partial', command?.detail || 'Sentry API checks passed, exporter smoke test did not pass', {
        accounts,
      });
    }
    return connector('blocked', failed[0]?.detail || 'One or more Sentry accounts failed connection checks', {
      accounts,
      nextAction: 'Verify each sources.sentry.accounts[] tokenEnv/baseUrl/org/projects entry, then rerun status.',
    });
  }
  if (connection?.status === 'pass' && (!command || command.status === 'pass')) {
    return connector('connected', command ? 'Sentry API and exporter smoke test passed' : 'Sentry API auth check passed', {
      accounts: [...accountMetadata.values()].map((account) => ({ ...account, status: 'connected' })),
    });
  }
  if (connection?.status === 'pass' && command?.status !== 'pass') {
    return connector('partial', command?.detail || 'Sentry API auth passed, exporter smoke test did not pass', {
      accounts: [...accountMetadata.values()].map((account) => ({ ...account, status: 'connected' })),
    });
  }
  return connector('blocked', connection?.detail || 'Sentry connection was not verified', {
    accounts: [...accountMetadata.values()].map((account) => ({
      ...account,
      status: 'blocked',
      detail: connection?.detail || 'Sentry connection was not verified',
    })),
    nextAction: `Run: ${WIZARD_COMMAND} --connectors sentry.`,
  });
}

function summarizeCoolify(preflight, config) {
  if (!isEnabled(config?.sources?.coolify)) {
    return connector('not_enabled', 'Coolify source is disabled');
  }
  const connection = checkByName(preflight, 'connection:coolify');
  const command = checkByName(preflight, 'connection:coolify-command');
  if (connection?.status === 'pass' && (!command || command.status === 'pass')) {
    return connector('connected', command ? 'Coolify API and exporter smoke test passed' : 'Coolify API auth check passed');
  }
  if (connection?.status === 'pass' && command?.status !== 'pass') {
    return connector('partial', command?.detail || 'Coolify API auth passed, exporter smoke test did not pass');
  }
  return connector('blocked', connection?.detail || 'Coolify connection was not verified', {
    nextAction: `Run: ${WIZARD_COMMAND} --connectors coolify.`,
  });
}

async function summarizeAsc(preflight, config, timeoutMs) {
  const ascSources = checksByPrefix(preflight, 'connection:asc_cli');
  const ascConnection = ascSources[0] || null;
  if (!configHasEnabledAscSource(config)) {
    return connector('not_enabled', 'App Store Connect CLI source is disabled');
  }
  if (ascConnection?.status === 'pass') {
    const analyticsReadiness = await checkAscAnalyticsReadiness(timeoutMs);
    if (analyticsReadiness.status !== 'connected') {
      return connector(analyticsReadiness.status, analyticsReadiness.detail, {
        appScope: 'all_accessible_apps',
        appAnalyticsReports: 'required',
        vendorNumber: analyticsReadiness.vendorNumber ? 'set' : 'missing',
        checkedAppCount: analyticsReadiness.checkedAppCount,
        requestCount: analyticsReadiness.requestCount,
        nextAction: `Run: ${WIZARD_COMMAND} --connectors asc.`,
      });
    }
    return connector('connected', analyticsReadiness.detail, {
      appScope: 'all_accessible_apps',
      appAnalyticsReports: 'available',
      vendorNumber: 'set',
      checkedAppCount: analyticsReadiness.checkedAppCount,
      requestCount: analyticsReadiness.requestCount,
      analyticsMode: 'api_key_batch_reports',
    });
  }
  return connector('blocked', ascConnection?.detail || 'ASC connection was not verified', {
    appScope: 'all_accessible_apps',
  });
}

async function main() {
  const secretsInfo = await loadOpenClawGrowthSecrets();
  const args = parseArgs(process.argv.slice(2));
  const configPath = path.resolve(args.config);
  const config = await readJson(configPath);
  await applyOpenClawSecretRefs(config);
  const onlyConnectors = args.onlyConnectors;
  const preflight = await runPreflight(configPath, args.timeoutMs, args.progressJson, onlyConnectors);
  const preflightPayload = preflight.payload;
  if (onlyAllows(onlyConnectors, 'asc')) {
    emitProgress(args.progressJson, {
      phase: 'start',
      key: 'appStoreConnect',
      label: 'App Store Connect',
      detail: 'ASC API-key reports auth',
    });
  }

  const [githubStatus, ascStatus] = await Promise.all([
    onlyAllows(onlyConnectors, 'github')
      ? checkGitHub(config, args.timeoutMs)
      : Promise.resolve(connector('not_enabled', 'GitHub check skipped; connector is not selected for live health')),
    onlyAllows(onlyConnectors, 'asc')
      ? preflightPayload
        ? summarizeAsc(preflightPayload, config, args.timeoutMs)
        : Promise.resolve(connector('unknown', preflight.error || 'Preflight did not run'))
      : Promise.resolve(connector('not_enabled', 'App Store Connect check skipped; connector is not selected for live health')),
  ]);

  const connectors: Record<string, any> = {};
  const statusOrUnknown = (summary) =>
    preflightPayload ? summary(preflightPayload, config) : connector('unknown', preflight.error || 'Preflight did not run');
  if (onlyAllows(onlyConnectors, 'analytics')) connectors.analyticscli = statusOrUnknown(summarizeAnalytics);
  if (onlyAllows(onlyConnectors, 'github')) connectors.github = githubStatus;
  if (onlyAllows(onlyConnectors, 'revenuecat')) connectors.revenuecat = statusOrUnknown(summarizeRevenueCat);
  if (onlyAllows(onlyConnectors, 'sentry')) connectors.sentry = statusOrUnknown(summarizeSentry);
  if (onlyAllows(onlyConnectors, 'coolify')) connectors.coolify = statusOrUnknown(summarizeCoolify);
  if (onlyAllows(onlyConnectors, 'asc')) connectors.appStoreConnect = ascStatus;
  if (onlyAllows(onlyConnectors, 'asc')) {
    emitProgress(args.progressJson, {
      phase: 'finish',
      key: 'appStoreConnect',
      label: 'App Store Connect',
      detail: connectors.appStoreConnect?.detail || 'ASC check complete',
      status: connectors.appStoreConnect?.status === 'connected' ? 'pass' : connectors.appStoreConnect?.status === 'partial' ? 'warn' : 'fail',
    });
  }

  const values = Object.values(connectors);
  const allConnected = values.every((entry: any) => entry.status === 'connected');
  const connectorNextActions = values
    .map((entry: any) => entry.nextAction)
    .filter((value): value is string => typeof value === 'string' && value.trim().length > 0);
  const result = {
    ok: allConnected,
    configPath,
    secretsFileLoaded: secretsInfo.loaded,
    secretsFilePath: secretsInfo.filePath,
    connectors,
    nextAction: allConnected
      ? null
      : connectorNextActions[0] || 'Run the connector wizard for any connector whose status is blocked, partial, not_enabled, or not_connected.',
  };

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (!result.ok) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
