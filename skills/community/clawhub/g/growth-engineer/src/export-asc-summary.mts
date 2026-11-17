#!/usr/bin/env node

import { spawn } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import { promisify } from 'node:util';
import { gunzip } from 'node:zlib';
import { buildAscSummary, writeJsonOutput } from './openclaw-exporters-lib.mjs';
import { loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';

const gunzipAsync = promisify(gunzip);

function printHelpAndExit(exitCode, reason = null) {
  if (reason) {
    process.stderr.write(`${reason}\n\n`);
  }
  process.stdout.write(`
Export ASC Summary

Builds an OpenClaw-compatible store/release summary JSON from the asc CLI.

Usage:
  node scripts/export-asc-summary.mjs [options]

Options:
  --app <id>             Optional App Store Connect app ID filter (defaults to all accessible apps)
  --out <file>           Write JSON to file instead of stdout
  --start <date>         App Store Connect Analytics start date (YYYY-MM-DD, default: 30 complete days)
  --end <date>           App Store Connect Analytics end date (YYYY-MM-DD, default: two days ago UTC)
  --cache-dir <dir>      Cache downloaded ASC batch reports (default: data/openclaw-growth-engineer/asc-cache)
  --force-refresh        Re-download reports even when the daily cache already has them
  --country <code>       Ratings country override (default: all countries)
  --reviews-limit <n>    Review summarizations limit (default: 20)
  --feedback-limit <n>   TestFlight feedback limit (default: 20)
  --analytics-report-scope <scope> App Analytics report coverage: all or core (default: all)
  --analytics-report-limit <n> Maximum App Analytics report types to download (default: unlimited)
  --analytics-instance-limit <n> Maximum App Analytics instances per report to inspect (default: 8)
  --command-timeout-ms <n> Maximum time for each asc command (default: 45000)
  --max-signals <n>      Maximum signals to emit (default: 4)
  --help, -h             Show help
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const defaultEnd = formatDate(addDays(new Date(), -2));
  const defaultStart = formatDate(addDays(parseDate(defaultEnd), -29));
  const args = {
    app: '',
    out: '',
    start: String(process.env.ASC_ANALYTICS_START || defaultStart).trim(),
    end: String(process.env.ASC_ANALYTICS_END || defaultEnd).trim(),
    cacheDir: String(process.env.ASC_BATCH_CACHE_DIR || 'data/openclaw-growth-engineer/asc-cache').trim(),
    forceRefresh: ['1', 'true', 'yes'].includes(String(process.env.ASC_FORCE_REFRESH || '').toLowerCase()),
    country: '',
    reviewsLimit: 20,
    feedbackLimit: 20,
    analyticsReportScope: String(process.env.ASC_ANALYTICS_REPORT_SCOPE || 'all').trim().toLowerCase(),
    analyticsReportLimit: Number.parseInt(String(process.env.ASC_ANALYTICS_REPORT_LIMIT || '0'), 10),
    analyticsInstanceLimit: 8,
    commandTimeoutMs: Number.parseInt(String(process.env.ASC_EXPORT_COMMAND_TIMEOUT_MS || '45000'), 10),
    maxSignals: 4,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    const next = argv[index + 1];

    if (token === '--') {
      continue;
    } else if (token === '--app') {
      args.app = String(next || '').trim();
      index += 1;
    } else if (token === '--out') {
      args.out = String(next || '').trim();
      index += 1;
    } else if (token === '--start') {
      args.start = String(next || '').trim();
      index += 1;
    } else if (token === '--end') {
      args.end = String(next || '').trim();
      index += 1;
    } else if (token === '--cache-dir') {
      args.cacheDir = String(next || '').trim();
      index += 1;
    } else if (token === '--force-refresh') {
      args.forceRefresh = true;
    } else if (token === '--country') {
      args.country = String(next || '').trim();
      index += 1;
    } else if (token === '--reviews-limit') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for --reviews-limit: ${String(next || '')}`);
      }
      args.reviewsLimit = parsed;
      index += 1;
    } else if (token === '--feedback-limit') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for --feedback-limit: ${String(next || '')}`);
      }
      args.feedbackLimit = parsed;
      index += 1;
    } else if (token === '--analytics-report-scope') {
      const parsed = String(next || '').trim().toLowerCase();
      if (!['all', 'core'].includes(parsed)) {
        printHelpAndExit(1, `Invalid value for --analytics-report-scope: ${String(next || '')}. Use all or core.`);
      }
      args.analyticsReportScope = parsed;
      index += 1;
    } else if (token === '--analytics-report-limit') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed < 0) {
        printHelpAndExit(1, `Invalid value for --analytics-report-limit: ${String(next || '')}`);
      }
      args.analyticsReportLimit = parsed;
      index += 1;
    } else if (token === '--analytics-instance-limit') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for --analytics-instance-limit: ${String(next || '')}`);
      }
      args.analyticsInstanceLimit = parsed;
      index += 1;
    } else if (token === '--command-timeout-ms') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed < 1000) {
        printHelpAndExit(1, `Invalid value for --command-timeout-ms: ${String(next || '')}`);
      }
      args.commandTimeoutMs = parsed;
      index += 1;
    } else if (token === '--max-signals') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for --max-signals: ${String(next || '')}`);
      }
      args.maxSignals = parsed;
      index += 1;
    } else if (token === '--help' || token === '-h') {
      printHelpAndExit(0);
    } else {
      printHelpAndExit(1, `Unknown argument: ${token}`);
    }
  }

  if (!['all', 'core'].includes(args.analyticsReportScope)) {
    printHelpAndExit(1, `Invalid value for ASC_ANALYTICS_REPORT_SCOPE: ${args.analyticsReportScope}. Use all or core.`);
  }
  if (!Number.isFinite(args.analyticsReportLimit) || args.analyticsReportLimit < 0) {
    args.analyticsReportLimit = 0;
  }

  return args;
}

function addDays(date, days) {
  const copy = new Date(date);
  copy.setUTCDate(copy.getUTCDate() + days);
  return copy;
}

function parseDate(value) {
  return new Date(`${value}T00:00:00Z`);
}

function formatDate(date) {
  return date.toISOString().slice(0, 10);
}

function ascCommandEnv(overrides: Record<string, string> = {}): NodeJS.ProcessEnv {
  const env = { ...process.env, ...overrides };
  delete env.ASC_TIMEOUT;
  delete env.ASC_TIMEOUT_SECONDS;
  delete env.ASC_VENDOR_NUMBER;
  return env;
}

function runJsonCommand(command, commandArgs, options: { timeoutMs?: number; env?: Record<string, string> } = {}) {
  const timeoutMs = Number.isFinite(Number(options.timeoutMs)) ? Number(options.timeoutMs) : 45_000;
  return new Promise((resolve, reject) => {
    const child = spawn(command, commandArgs, {
      stdio: ['ignore', 'pipe', 'pipe'],
      env: ascCommandEnv(options.env || {}),
    });

    let stdout = '';
    let stderr = '';
    let timedOut = false;
    let settled = false;
    let forceKillTimeout: NodeJS.Timeout | null = null;
    const timeout = setTimeout(() => {
      timedOut = true;
      child.kill('SIGTERM');
      forceKillTimeout = setTimeout(() => {
        if (settled) return;
        child.kill('SIGKILL');
        settled = true;
        reject(new Error(`${command} ${commandArgs.join(' ')} timed out after ${timeoutMs}ms`));
      }, 2_000);
    }, timeoutMs);

    child.stdout.on('data', (chunk) => {
      stdout += String(chunk);
    });
    child.stderr.on('data', (chunk) => {
      stderr += String(chunk);
    });
    child.on('error', (error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      if (forceKillTimeout) clearTimeout(forceKillTimeout);
      reject(error);
    });
    child.on('close', (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      if (forceKillTimeout) clearTimeout(forceKillTimeout);
      if (timedOut) {
        reject(new Error(`${command} ${commandArgs.join(' ')} timed out after ${timeoutMs}ms`));
        return;
      }
      if (code !== 0) {
        reject(Object.assign(new Error(stderr.trim() || `${command} exited with code ${code}`), { exitCode: code }));
        return;
      }

      try {
        resolve(JSON.parse(stdout));
      } catch {
        reject(new Error(`${command} returned non-JSON output`));
      }
    });
  });
}

function envValue(name) {
  return normalizeString(process.env[name]);
}

function getAscAuthCandidates() {
  const candidates = [
    {
      label: 'ASC',
      keyId: envValue('ASC_KEY_ID'),
      issuerId: envValue('ASC_ISSUER_ID'),
      privateKeyPath: envValue('ASC_PRIVATE_KEY_PATH'),
      privateKey: envValue('ASC_PRIVATE_KEY'),
      privateKeyB64: envValue('ASC_PRIVATE_KEY_B64'),
    },
    {
      label: 'ASC_ANALYTICS',
      keyId: envValue('ASC_ANALYTICS_KEY_ID'),
      issuerId: envValue('ASC_ANALYTICS_ISSUER_ID'),
      privateKeyPath: envValue('ASC_ANALYTICS_PRIVATE_KEY_PATH'),
      privateKey: envValue('ASC_ANALYTICS_PRIVATE_KEY'),
      privateKeyB64: envValue('ASC_ANALYTICS_PRIVATE_KEY_B64'),
    },
    {
      label: 'ASC_ADMIN',
      keyId: envValue('ASC_ADMIN_KEY_ID'),
      issuerId: envValue('ASC_ADMIN_ISSUER_ID'),
      privateKeyPath: envValue('ASC_ADMIN_PRIVATE_KEY_PATH'),
      privateKey: envValue('ASC_ADMIN_PRIVATE_KEY'),
      privateKeyB64: envValue('ASC_ADMIN_PRIVATE_KEY_B64'),
    },
    {
      label: 'ASC_BOOTSTRAP',
      keyId: envValue('ASC_BOOTSTRAP_KEY_ID'),
      issuerId: envValue('ASC_BOOTSTRAP_ISSUER_ID'),
      privateKeyPath: envValue('ASC_BOOTSTRAP_PRIVATE_KEY_PATH'),
      privateKey: envValue('ASC_BOOTSTRAP_PRIVATE_KEY'),
      privateKeyB64: envValue('ASC_BOOTSTRAP_PRIVATE_KEY_B64'),
    },
  ];
  return candidates.filter((candidate) => (
    candidate.keyId &&
    candidate.issuerId &&
    (candidate.privateKeyPath || candidate.privateKey || candidate.privateKeyB64)
  ));
}

function getAscAnalyticsFallbackEnv() {
  const candidates = getAscAuthCandidates().filter((candidate) => candidate.label !== 'ASC');
  for (const candidate of candidates) {
    return {
      label: candidate.label,
      env: {
        ASC_BYPASS_KEYCHAIN: '1',
        ASC_KEY_ID: candidate.keyId,
        ASC_ISSUER_ID: candidate.issuerId,
        ...(candidate.privateKeyPath ? { ASC_PRIVATE_KEY_PATH: candidate.privateKeyPath } : {}),
        ...(candidate.privateKey ? { ASC_PRIVATE_KEY: candidate.privateKey } : {}),
        ...(candidate.privateKeyB64 ? { ASC_PRIVATE_KEY_B64: candidate.privateKeyB64 } : {}),
      },
    };
  }
  return null;
}

function base64Url(value) {
  return Buffer.from(typeof value === 'string' ? value : JSON.stringify(value)).toString('base64url');
}

async function readAscPrivateKey(candidate) {
  if (candidate.privateKey) return candidate.privateKey;
  if (candidate.privateKeyB64) return Buffer.from(candidate.privateKeyB64, 'base64').toString('utf8');
  if (candidate.privateKeyPath) return fs.readFile(candidate.privateKeyPath, 'utf8');
  throw new Error(`${candidate.label} private key is not configured`);
}

async function createAppleApiJwt(candidate) {
  const privateKey = await readAscPrivateKey(candidate);
  const issuedAt = Math.floor(Date.now() / 1000);
  const header = { alg: 'ES256', kid: candidate.keyId, typ: 'JWT' };
  const claims = {
    iss: candidate.issuerId,
    iat: issuedAt,
    exp: issuedAt + 15 * 60,
    aud: 'appstoreconnect-v1',
  };
  const signingInput = `${base64Url(header)}.${base64Url(claims)}`;
  const signature = crypto
    .sign('SHA256', Buffer.from(signingInput), { key: privateKey, dsaEncoding: 'ieee-p1363' })
    .toString('base64url');
  return `${signingInput}.${signature}`;
}

function isAppleApiAuthBlocked(error) {
  return isAscAnalyticsAuthBlockedMessage(error instanceof Error ? error.message : String(error));
}

async function fetchWithTimeout(url, options: { timeoutMs?: number; headers?: Record<string, string> } = {}) {
  const timeoutMs = Number.isFinite(Number(options.timeoutMs)) ? Number(options.timeoutMs) : 45_000;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, {
      headers: options.headers,
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }
}

async function appleApiRequest(candidate, pathOrUrl, options: { timeoutMs?: number; binary?: boolean } = {}) {
  const url = String(pathOrUrl).startsWith('http')
    ? String(pathOrUrl)
    : `https://api.appstoreconnect.apple.com${pathOrUrl}`;
  const token = await createAppleApiJwt(candidate);
  const response = await fetchWithTimeout(url, {
    timeoutMs: options.timeoutMs,
    headers: { Authorization: `Bearer ${token}` },
  });
  const body = Buffer.from(await response.arrayBuffer());
  if (!response.ok) {
    let message = body.toString('utf8').slice(0, 500);
    try {
      const parsed = JSON.parse(body.toString('utf8'));
      if (Array.isArray(parsed.errors) && parsed.errors[0]) {
        const error = parsed.errors[0];
        message = `${error.status || response.status} ${error.code || ''} ${error.title || ''}: ${error.detail || ''}`.trim();
      }
    } catch {
      // Use the raw body snippet.
    }
    throw new Error(`Apple API ${response.status} ${url}: ${message}`);
  }
  if (options.binary) return body;
  try {
    return JSON.parse(body.toString('utf8'));
  } catch {
    throw new Error(`Apple API returned non-JSON output for ${url}`);
  }
}

async function appleApiRequestWithCandidates(label, pathOrUrl, warnings, options: { timeoutMs?: number; binary?: boolean } = {}) {
  const candidates = getAscAuthCandidates();
  if (candidates.length === 0) {
    return { ok: false, payload: null, error: 'ASC API key is not configured for direct Apple API access', credential: null };
  }
  const errors = [];
  for (const candidate of candidates) {
    try {
      const payload = await appleApiRequest(candidate, pathOrUrl, options);
      return { ok: true, payload, error: null, credential: candidate.label };
    } catch (error) {
      const detail = error instanceof Error ? error.message : String(error);
      errors.push(`${candidate.label}: ${detail}`);
      if (!isAppleApiAuthBlocked(error)) break;
    }
  }
  const error = errors.join('; ');
  warnings.push(`${label}: ${error}`);
  return { ok: false, payload: null, error, credential: null };
}

function isAscAnalyticsAuthBlockedMessage(value) {
  const normalized = String(value || '').toLowerCase();
  return normalized.includes('forbidden for security') ||
    normalized.includes('api key in use does not allow this request') ||
    normalized.includes('does not allow this request') ||
    normalized.includes('403') ||
    normalized.includes('forbidden');
}

function isAscAnalyticsTemporarilyUnavailableMessage(value) {
  const normalized = String(value || '').toLowerCase();
  return normalized.includes('timed out after') ||
    normalized.includes('unexpected error occurred') ||
    normalized.includes('fetch failed') ||
    normalized.includes('network timeout') ||
    normalized.includes('econnreset') ||
    normalized.includes('etimedout') ||
    normalized.includes('eai_again') ||
    normalized.includes('enotfound');
}

async function runBestEffortAscQueryResult(label, args, warnings, options: { timeoutMs?: number; env?: Record<string, string>; retryWithAnalyticsFallback?: boolean } = {}) {
  try {
    return { ok: true, payload: await runJsonCommand('asc', args, options), error: null };
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    if (options.retryWithAnalyticsFallback && isAscAnalyticsAuthBlockedMessage(detail)) {
      const fallback = getAscAnalyticsFallbackEnv();
      if (fallback) {
        try {
          const payload = await runJsonCommand('asc', args, { ...options, env: { ...(options.env || {}), ...fallback.env } });
          warnings.push(`${label}: retried with ${fallback.label} key`);
          return { ok: true, payload, error: null };
        } catch (fallbackError) {
          const fallbackDetail = fallbackError instanceof Error ? fallbackError.message : String(fallbackError);
          warnings.push(`${label}: ${detail}; ${fallback.label} retry also failed: ${fallbackDetail}`);
          return { ok: false, payload: null, error: fallbackDetail };
        }
      }
    }
    warnings.push(`${label}: ${detail}`);
    return { ok: false, payload: null, error: detail };
  }
}

async function runBestEffortAscQuery(label, args, warnings, options: { timeoutMs?: number; env?: Record<string, string>; retryWithAnalyticsFallback?: boolean } = {}) {
  const result = await runBestEffortAscQueryResult(label, args, warnings, options);
  return result.payload;
}

function normalizeString(value) {
  return typeof value === 'string' && value.trim() ? value.trim() : null;
}

function normalizeKey(value) {
  return String(value || '').toLowerCase().replace(/[^a-z0-9]/g, '');
}

function coerceNumber(value) {
  if (value === null || value === undefined) return null;
  const normalized = String(value).trim().replace(/%$/, '').replace(/,/g, '');
  if (!normalized) return null;
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

function addMetricTotals(metrics, measure, value, date = null, { rate = false } = {}) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) return;
  const key = normalizeKey(measure);
  if (!key) return;
  const existing = metrics.get(key) || {
    measure,
    total: 0,
    previousTotal: null,
    percentChange: null,
    data: [],
    count: 0,
    rate,
  };
  existing.count += 1;
  existing.total = rate ? existing.total + Number(value) : existing.total + Number(value);
  if (date) existing.data.push({ date, value: Number(value) });
  metrics.set(key, existing);
}

function finishMetricTotals(metrics) {
  return [...metrics.values()].map((metric) => ({
    measure: metric.measure,
    total: metric.rate && metric.count > 0 ? metric.total / metric.count : metric.total,
    previousTotal: metric.previousTotal,
    percentChange: metric.percentChange,
    data: metric.data,
  }));
}

function addBreakdownMetric(target, key, field, value) {
  if (!key || value === null || value === undefined || !Number.isFinite(Number(value))) return;
  const existing = target.get(key) || {
    key,
    title: key,
    impressions: 0,
    pageViewUnique: 0,
    units: 0,
    redownloads: 0,
    purchases: 0,
    proceeds: 0,
    crashes: 0,
  };
  existing[field] = (existing[field] || 0) + Number(value);
  target.set(key, existing);
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readReportText(filePath) {
  const buffer = await fs.readFile(filePath);
  if (buffer.length >= 2 && buffer[0] === 0x1f && buffer[1] === 0x8b) {
    return (await gunzipAsync(buffer)).toString('utf8');
  }
  return buffer.toString('utf8');
}

async function materializeParsedReport(rawPath, parsedPath) {
  const content = await readReportText(rawPath);
  await fs.mkdir(path.dirname(parsedPath), { recursive: true });
  await fs.writeFile(parsedPath, content, 'utf8');
}

function splitDelimitedLine(line, delimiter) {
  const cells = [];
  let current = '';
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      if (quoted && line[index + 1] === '"') {
        current += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === delimiter && !quoted) {
      cells.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  cells.push(current);
  return cells;
}

async function parseDelimitedReport(filePath) {
  const content = await readReportText(filePath);
  const lines = content.split(/\r?\n/).filter((line) => line.trim());
  if (lines.length < 2) return [];
  const delimiter = lines[0].includes('\t') ? '\t' : ',';
  const headers = splitDelimitedLine(lines[0], delimiter).map((header) => header.trim());
  return lines.slice(1).map((line) => {
    const cells = splitDelimitedLine(line, delimiter);
    const row = {};
    headers.forEach((header, index) => {
      row[header] = cells[index] ?? '';
    });
    return row;
  });
}

function findHeader(row, candidates) {
  const byKey = new Map(Object.keys(row).map((key) => [normalizeKey(key), key]));
  for (const candidate of candidates) {
    const match = byKey.get(normalizeKey(candidate));
    if (match) return match;
  }
  return null;
}

function firstRowValue(row, candidates) {
  const header = findHeader(row, candidates);
  if (!header) return null;
  const value = String(row[header] || '').trim();
  return value || null;
}

function reportColumns(report) {
  if (!Array.isArray(report?.rows) || report.rows.length === 0) return [];
  return Object.keys(report.rows[0] || {});
}

function isNumericReportValue(value) {
  const normalized = String(value ?? '').trim().replace(/%$/, '').replace(/,/g, '');
  if (!normalized) return false;
  return Number.isFinite(Number(normalized));
}

function classifyReportColumns(report) {
  const columns = reportColumns(report);
  const metricHints = [
    'impressions',
    'unique impressions',
    'product page views',
    'page views',
    'units',
    'first-time downloads',
    'redownloads',
    'conversion rate',
    'crashes',
    'sessions',
    'active devices',
    'installations',
    'deletions',
    'purchases',
    'proceeds',
    'paying users',
    'subscriptions',
    'trial starts',
    'sales',
    'developer proceeds',
  ].map(normalizeKey);
  const metrics = [];
  const dimensions = [];
  for (const column of columns) {
    const normalized = normalizeKey(column);
    const dimensionName = /\b(identifier| id|id |date|country|territory|currency|code|type|name|reason|version|sku|provider|developer|platform|device|client|category|period)\b/i.test(column) ||
      /identifier|country|territory|currency|code|type|name|reason|version|sku|provider|developer|platform|device|client|category|period/.test(normalized);
    const sampleValues = Array.isArray(report?.rows)
      ? report.rows.slice(0, 50).map((row) => row?.[column]).filter((value) => String(value ?? '').trim())
      : [];
    const numericShare = sampleValues.length > 0
      ? sampleValues.filter(isNumericReportValue).length / sampleValues.length
      : 0;
    const forcedMetric = metricHints.includes(normalized);
    const nameLooksMetric = forcedMetric ||
      /\b(count|counts|rate|duration|amount|proceeds|units|sessions|crashes|views|impressions|purchases|installs|downloads|deletions|users)\b/i.test(column);
    if (forcedMetric || (!dimensionName && (numericShare >= 0.8 || nameLooksMetric))) {
      metrics.push(column);
    } else {
      dimensions.push(column);
    }
  }
  return { metrics, dimensions };
}

function reportCachePaths(appCacheDir, baseName) {
  const safeBase = String(baseName || 'report').replace(/[^a-zA-Z0-9._-]+/g, '-');
  return {
    rawPath: path.join(appCacheDir, `${safeBase}.txt.gz`),
    parsedPath: path.join(appCacheDir, `${safeBase}.txt`),
    manifestPath: path.join(appCacheDir, `${safeBase}.manifest.json`),
  };
}

async function loadCachedReport(label, paths) {
  if (await fileExists(paths.parsedPath)) {
    const rows = await parseDelimitedReport(paths.parsedPath);
    return { label, outputPath: paths.parsedPath, rows, cacheStatus: 'hit' };
  }
  if (await fileExists(paths.rawPath)) {
    await materializeParsedReport(paths.rawPath, paths.parsedPath);
    const rows = await parseDelimitedReport(paths.parsedPath);
    return { label, outputPath: paths.parsedPath, rows, cacheStatus: 'hit_raw' };
  }
  return null;
}

async function writeReportManifest(paths, report) {
  await fs.writeFile(
    paths.manifestPath,
    `${JSON.stringify(
      {
        label: report.label,
        fetchedAt: new Date().toISOString(),
        outputPath: report.outputPath,
        rowCount: report.rows.length,
        cacheStatus: report.cacheStatus,
      },
      null,
      2,
    )}\n`,
    'utf8',
  );
}

async function persistRawReport(label, paths, buffer, cacheStatus) {
  await fs.mkdir(path.dirname(paths.rawPath), { recursive: true });
  await fs.writeFile(paths.rawPath, buffer);
  await materializeParsedReport(paths.rawPath, paths.parsedPath);
  const rows = await parseDelimitedReport(paths.parsedPath);
  const report = { label, outputPath: paths.parsedPath, rows, cacheStatus };
  await writeReportManifest(paths, report);
  return report;
}

async function downloadAppleSalesReportDirect(appCacheDir, baseName, args, warnings) {
  const vendor = String(process.env.ASC_VENDOR_NUMBER || '').trim();
  if (!vendor) return null;
  const paths = reportCachePaths(appCacheDir, baseName);
  if (!args.forceRefresh) {
    const cached = await loadCachedReport('ASC daily sales batch report', paths);
    if (cached) return cached;
  }

  const query = new URLSearchParams({
    'filter[frequency]': 'DAILY',
    'filter[reportDate]': args.end,
    'filter[reportSubType]': 'SUMMARY',
    'filter[reportType]': 'SALES',
    'filter[vendorNumber]': vendor,
  });
  const result = await appleApiRequestWithCandidates(
    'ASC daily sales batch report direct API',
    `/v1/salesReports?${query.toString()}`,
    warnings,
    { timeoutMs: args.commandTimeoutMs, binary: true },
  );
  if (!result.ok || !Buffer.isBuffer(result.payload)) return null;
  const report = await persistRawReport('ASC daily sales batch report', paths, result.payload, 'downloaded_direct_api');
  warnings.push(`ASC daily sales batch report: downloaded with direct Apple API${result.credential ? ` (${result.credential})` : ''}`);
  return report;
}

async function listAppleApiCollection(pathOrUrl, warnings, label, timeoutMs, limit = 200) {
  const items = [];
  let url = String(pathOrUrl);
  while (url) {
    const separator = url.includes('?') ? '&' : '?';
    const pagedUrl = url.includes('limit=') ? url : `${url}${separator}limit=${limit}`;
    const result = await appleApiRequestWithCandidates(label, pagedUrl, warnings, { timeoutMs });
    if (!result.ok || !result.payload || typeof result.payload !== 'object') {
      return { ok: false, items, error: result.error, credential: result.credential };
    }
    if (Array.isArray(result.payload.data)) items.push(...result.payload.data);
    url = normalizeString(result.payload.links?.next) || '';
  }
  return { ok: true, items, error: null, credential: null };
}

function scoreAnalyticsReport(report) {
  const attrs = report?.attributes && typeof report.attributes === 'object' ? report.attributes : {};
  const name = String(attrs.name || '');
  const category = String(attrs.category || '');
  const text = `${category} ${name}`.toLowerCase();
  if (text.includes('app store discovery and engagement standard')) return 100;
  if (text.includes('app downloads standard')) return 95;
  if (text.includes('app store purchases standard')) return 90;
  if (text.includes('app store installation and deletion standard')) return 85;
  if (text.includes('app sessions standard')) return 80;
  if (text.includes('app crashes')) return 75;
  if (text.includes('subscription event report standard')) return 70;
  if (text.includes('subscription state report standard')) return 65;
  if (/app store|download|purchase|install|session|crash|engagement/.test(text) && text.includes('standard')) return 40;
  return 1;
}

function pickRelevantAnalyticsReports(reports, args) {
  const scored = [];
  for (const report of reports) {
    if (report?.id) scored.push({ report, score: scoreAnalyticsReport(report) });
  }
  const ordered = scored
    .sort((a, b) => b.score - a.score)
    .filter((entry) => args.analyticsReportScope === 'all' || entry.score > 1);
  const limit = Math.max(0, Number(args.analyticsReportLimit) || 0);
  return (limit > 0 ? ordered.slice(0, limit) : ordered).map((entry) => entry.report);
}

function pickBestReportInstance(instances, endDate) {
  const withDate = instances
    .map((instance) => ({
      instance,
      date: normalizeString(instance?.attributes?.processingDate) || '',
    }))
    .filter((entry) => entry.instance?.id);
  const exact = withDate.find((entry) => entry.date === endDate);
  if (exact) return exact.instance;
  const before = withDate
    .filter((entry) => entry.date && entry.date <= endDate)
    .sort((a, b) => b.date.localeCompare(a.date))[0];
  if (before) return before.instance;
  return withDate.sort((a, b) => b.date.localeCompare(a.date))[0]?.instance || null;
}

async function downloadAppleAnalyticsReportsDirect(appId, requestId, appCacheDir, args, warnings) {
  const reportsResult = await listAppleApiCollection(
    `/v1/analyticsReportRequests/${encodeURIComponent(requestId)}/reports`,
    warnings,
    'ASC analytics reports direct API',
    args.commandTimeoutMs,
  );
  if (!reportsResult.ok) return [];
  const selectedReports = pickRelevantAnalyticsReports(reportsResult.items, args);
  warnings.push(`ASC App Analytics report catalog: selected ${selectedReports.length}/${reportsResult.items.length} report type(s) (${args.analyticsReportScope})`);
  const downloaded = [];

  for (const report of selectedReports) {
    const attrs = report.attributes && typeof report.attributes === 'object' ? report.attributes : {};
    const reportName = normalizeString(attrs.name) || report.id;
    const instancesResult = await listAppleApiCollection(
      `/v1/analyticsReports/${encodeURIComponent(report.id)}/instances`,
      warnings,
      `ASC analytics instances direct API ${reportName}`,
      args.commandTimeoutMs,
      20,
    );
    if (!instancesResult.ok || instancesResult.items.length === 0) continue;
    const instance = pickBestReportInstance(instancesResult.items, args.end);
    if (!instance?.id) continue;
    const segmentsResult = await listAppleApiCollection(
      `/v1/analyticsReportInstances/${encodeURIComponent(instance.id)}/segments`,
      warnings,
      `ASC analytics segments direct API ${reportName}`,
      args.commandTimeoutMs,
      20,
    );
    if (!segmentsResult.ok || segmentsResult.items.length === 0) continue;

    let segmentIndex = 0;
    for (const segment of segmentsResult.items) {
      const segmentUrl = normalizeString(segment?.attributes?.url);
      if (!segmentUrl) continue;
      const paths = reportCachePaths(appCacheDir, `analytics-direct-${report.id}-${instance.id}-${segmentIndex}`);
      if (!args.forceRefresh) {
        const cached = await loadCachedReport(`ASC App Analytics ${reportName}`, paths);
        if (cached) {
          downloaded.push(cached);
          segmentIndex += 1;
          continue;
        }
      }
      try {
        const response = await fetchWithTimeout(segmentUrl, { timeoutMs: args.commandTimeoutMs });
        if (!response.ok) throw new Error(`segment download failed with HTTP ${response.status}`);
        const buffer = Buffer.from(await response.arrayBuffer());
        downloaded.push(await persistRawReport(`ASC App Analytics ${reportName}`, paths, buffer, 'downloaded_direct_api'));
      } catch (error) {
        warnings.push(`ASC App Analytics ${reportName}: ${error instanceof Error ? error.message : String(error)}`);
      }
      segmentIndex += 1;
    }
  }

  if (downloaded.length > 0) {
    warnings.push(`ASC App Analytics batch report: downloaded ${downloaded.length} report segment(s) with direct Apple API`);
  }
  return downloaded;
}

async function loadCachedReportsFromDir(appCacheDir, warnings, reason) {
  let entries = [];
  try {
    entries = await fs.readdir(appCacheDir);
  } catch {
    return [];
  }
  const manifests = entries.filter((entry) => entry.endsWith('.manifest.json')).sort();
  const reports = [];
  for (const manifestName of manifests) {
    try {
      const manifestPath = path.join(appCacheDir, manifestName);
      const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
      const parsedPath = String(manifest.outputPath || '').trim();
      if (!parsedPath || !(await fileExists(parsedPath))) continue;
      const rows = await parseDelimitedReport(parsedPath);
      reports.push({
        label: String(manifest.label || manifestName.replace(/\.manifest\.json$/, '')),
        outputPath: parsedPath,
        rows,
        cacheStatus: 'fallback_hit',
      });
    } catch {
      // Ignore malformed cache entries; a fresh download will repair them.
    }
  }
  if (reports.length > 0 && reason) {
    warnings.push(`${reason}: using ${reports.length} cached ASC report(s) from ${appCacheDir}`);
  }
  return reports;
}

async function loadLatestCachedReports(appCacheRoot, requestedEnd, warnings) {
  let entries = [];
  try {
    entries = await fs.readdir(appCacheRoot, { withFileTypes: true });
  } catch {
    return [];
  }
  const requestedTime = parseDate(requestedEnd).getTime();
  const dateDirs = entries
    .filter((entry) => entry.isDirectory() && /^\d{4}-\d{2}-\d{2}$/.test(entry.name))
    .map((entry) => entry.name)
    .filter((date) => parseDate(date).getTime() <= requestedTime)
    .sort()
    .reverse();
  for (const date of dateDirs) {
    const reports = await loadCachedReportsFromDir(
      path.join(appCacheRoot, date),
      warnings,
      `ASC App Analytics batch report unavailable for ${requestedEnd}`,
    );
    if (reports.length > 0) return reports;
  }
  return [];
}

function summarizeBatchRows(rows, appId) {
  const metrics = new Map();
  const sourceBreakdowns = new Map();
  const crashBreakdowns = new Map();
  for (const row of rows) {
    const appIdHeader = findHeader(row, ['apple identifier', 'app apple identifier', 'app id', 'adam id']);
    if (appIdHeader && String(row[appIdHeader] || '').trim() && String(row[appIdHeader]).trim() !== String(appId)) {
      continue;
    }
    const dateHeader = findHeader(row, ['date', 'begin date', 'start date', 'end date']);
    const date = dateHeader ? String(row[dateHeader] || '').slice(0, 10) : null;
    const fields = [
      { measure: 'impressions', candidates: ['impressions', 'unique impressions', 'impression count'] },
      { measure: 'pageViewUnique', candidates: ['unique product page views', 'product page views', 'page views', 'page view count', 'page views unique'] },
      { measure: 'units', candidates: ['units', 'app units', 'downloads', 'first-time downloads'] },
      { measure: 'redownloads', candidates: ['redownloads', 're-downloads'] },
      { measure: 'conversionRate', candidates: ['conversion rate', 'app store conversion rate'], rate: true },
      { measure: 'crashRate', candidates: ['crash rate'], rate: true },
      { measure: 'crashes', candidates: ['crashes', 'crash count'] },
      { measure: 'sessions', candidates: ['sessions', 'session count'] },
      { measure: 'activeDevices', candidates: ['active devices', 'active devices count', 'unique devices'] },
      { measure: 'installations', candidates: ['installations', 'installs', 'app installations'] },
      { measure: 'deletions', candidates: ['deletions', 'deletes', 'app deletions'] },
      { measure: 'purchases', candidates: ['purchases', 'purchase count', 'sales', 'paying purchases'] },
      { measure: 'payingUsers', candidates: ['paying users', 'unique paying users'] },
      { measure: 'subscriptions', candidates: ['subscriptions', 'active subscriptions', 'paid subscriptions'] },
      { measure: 'trialStarts', candidates: ['trial starts', 'free trial starts', 'introductory offer starts'] },
      { measure: 'proceeds', candidates: ['developer proceeds', 'proceeds'] },
    ];
    for (const field of fields) {
      const header = findHeader(row, field.candidates);
      if (!header) continue;
      addMetricTotals(metrics, field.measure, coerceNumber(row[header]), date, { rate: Boolean(field.rate) });
    }

    const source =
      firstRowValue(row, ['source type', 'download source type', 'source', 'source name', 'referrer', 'app referrer', 'web referrer', 'campaign']) ||
      firstRowValue(row, ['page type', 'event type']);
    if (source) {
      const sourceFields = [
        { field: 'impressions', candidates: ['impressions', 'unique impressions', 'impression count'] },
        { field: 'pageViewUnique', candidates: ['unique product page views', 'product page views', 'page views', 'page view count', 'page views unique'] },
        { field: 'units', candidates: ['units', 'app units', 'downloads', 'first-time downloads'] },
        { field: 'redownloads', candidates: ['redownloads', 're-downloads'] },
        { field: 'purchases', candidates: ['purchases', 'purchase count', 'sales'] },
        { field: 'proceeds', candidates: ['developer proceeds', 'proceeds'] },
      ];
      for (const field of sourceFields) {
        const header = findHeader(row, field.candidates);
        if (header) addBreakdownMetric(sourceBreakdowns, source, field.field, coerceNumber(row[header]));
      }
    }

    const crashesHeader = findHeader(row, ['crashes', 'crash count']);
    const crashes = crashesHeader ? coerceNumber(row[crashesHeader]) : null;
    if (crashes !== null && crashes > 0) {
      const version = firstRowValue(row, ['app version', 'version', 'app version number']) || 'Unknown app version';
      const platform = firstRowValue(row, ['platform', 'device type', 'device', 'os']) || '';
      const key = `${version}${platform ? ` (${platform})` : ''}`;
      addBreakdownMetric(crashBreakdowns, key, 'crashes', crashes);
    }
  }
  const results = finishMetricTotals(metrics);
  return {
    results,
    sourceBreakdown: [...sourceBreakdowns.values()]
      .filter((entry) => entry.impressions > 0 || entry.pageViewUnique > 0 || entry.units > 0 || entry.purchases > 0 || entry.proceeds > 0)
      .sort((a, b) => (b.pageViewUnique || b.impressions || b.units || 0) - (a.pageViewUnique || a.impressions || a.units || 0)),
    crashBreakdown: [...crashBreakdowns.values()]
      .map((entry) => ({ label: entry.title, value: entry.crashes }))
      .filter((entry) => entry.value > 0)
      .sort((a, b) => b.value - a.value),
    overviewMetricCatalog: results.map((metric) => ({
      section: 'batchReports',
      measure: metric.measure,
      total: metric.total,
      previousTotal: metric.previousTotal,
      percentChange: metric.percentChange,
      type: 'COUNT',
    })),
  };
}

function extractItems(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.items)) return payload.items;
  if (Array.isArray(payload?.requests)) return payload.requests;
  return [];
}

function extractId(item) {
  return normalizeString(item?.id) || normalizeString(item?.requestId) || normalizeString(item?.attributes?.id);
}

function extractInstances(payload) {
  const instances = [];
  const visit = (value) => {
    if (!value || typeof value !== 'object') return;
    if (Array.isArray(value)) {
      for (const item of value) visit(item);
      return;
    }
    const id = extractId(value);
    const type = normalizeString(value.type) || normalizeString(value.kind) || '';
    const attrs = value.attributes && typeof value.attributes === 'object' ? value.attributes : {};
    if (id && /instance/i.test(`${type} ${attrs.name || ''} ${attrs.category || ''}`)) {
      instances.push({ id, name: normalizeString(attrs.name) || normalizeString(value.name) });
    }
    for (const child of Object.values(value)) visit(child);
  };
  visit(payload);
  const byId = new Map();
  for (const instance of instances) byId.set(instance.id, instance);
  return [...byId.values()];
}

async function downloadAndParseReport(label, commandArgs, appCacheDir, baseName, args, warnings) {
  const paths = reportCachePaths(appCacheDir, baseName);
  if (!args.forceRefresh) {
    const cached = await loadCachedReport(label, paths);
    if (cached) return cached;
  }

  try {
    await fs.mkdir(appCacheDir, { recursive: true });
    await runJsonCommand('asc', [...commandArgs, '--output', paths.rawPath], { timeoutMs: args.commandTimeoutMs });
    await materializeParsedReport(paths.rawPath, paths.parsedPath);
    const rows = await parseDelimitedReport(paths.parsedPath);
    const report = { label, outputPath: paths.parsedPath, rows, cacheStatus: 'downloaded' };
    await writeReportManifest(paths, report);
    return report;
  } catch (error) {
    const compressedError = error instanceof Error ? error.message : String(error);
    const analyticsFallback = isAscAnalyticsAuthBlockedMessage(compressedError) ? getAscAnalyticsFallbackEnv() : null;
    if (analyticsFallback) {
      try {
        await runJsonCommand('asc', [...commandArgs, '--output', paths.rawPath], {
          timeoutMs: args.commandTimeoutMs,
          env: analyticsFallback.env,
        });
        await materializeParsedReport(paths.rawPath, paths.parsedPath);
        const rows = await parseDelimitedReport(paths.parsedPath);
        const report = { label, outputPath: paths.parsedPath, rows, cacheStatus: `downloaded_${analyticsFallback.label.toLowerCase()}` };
        await writeReportManifest(paths, report);
        warnings.push(`${label}: retried with ${analyticsFallback.label} key`);
        return report;
      } catch (fallbackKeyError) {
        warnings.push(`${label}: ${analyticsFallback.label} retry failed: ${fallbackKeyError instanceof Error ? fallbackKeyError.message : String(fallbackKeyError)}`);
      }
    }
    try {
      await runJsonCommand('asc', [...commandArgs, '--output', paths.parsedPath, '--decompress'], { timeoutMs: args.commandTimeoutMs });
      const rows = await parseDelimitedReport(paths.parsedPath);
      const report = { label, outputPath: paths.parsedPath, rows, cacheStatus: 'downloaded_decompressed' };
      await writeReportManifest(paths, report);
      return report;
    } catch (fallbackError) {
      const cached = await loadCachedReport(label, paths);
      if (cached) {
        warnings.push(`${label}: fresh download failed; using cached report (${compressedError})`);
        return cached;
      }
      warnings.push(`${label}: ${fallbackError instanceof Error ? fallbackError.message : String(fallbackError)}`);
      return null;
    }
  }
}

async function downloadBatchAnalyticsReports(appId, args, warnings) {
  const reports = [];
  const appCacheRoot = path.resolve(args.cacheDir || path.join(os.tmpdir(), 'openclaw-asc-cache'), appId);
  const appCacheDir = path.join(appCacheRoot, args.end);

  const vendor = String(process.env.ASC_VENDOR_NUMBER || '').trim();
  if (vendor) {
    const sales = await downloadAppleSalesReportDirect(appCacheDir, 'sales-daily', args, warnings) ||
      await downloadAndParseReport(
        'ASC daily sales batch report',
        [
          'analytics',
          'sales',
          '--vendor',
          vendor,
          '--type',
          'SALES',
          '--subtype',
          'SUMMARY',
          '--frequency',
          'DAILY',
          '--date',
          args.end,
        ],
        appCacheDir,
        'sales-daily',
        args,
        warnings,
      );
    if (sales) reports.push(sales);
  }

  const directRequestsResult = await listAppleApiCollection(
    `/v1/apps/${encodeURIComponent(appId)}/analyticsReportRequests`,
    warnings,
    'ASC analytics requests direct API',
    args.commandTimeoutMs,
    20,
  );
  const directRequestId = directRequestsResult.items.map(extractId).find(Boolean);
  if (directRequestId) {
    const directReports = await downloadAppleAnalyticsReportsDirect(appId, directRequestId, appCacheDir, args, warnings);
    if (directReports.length > 0) return [...reports, ...directReports];
  }

  const requestsResult = await runBestEffortAscQueryResult('ASC analytics requests query', [
    'analytics',
    'requests',
    '--app',
    appId,
    '--output',
    'json',
  ], warnings, { timeoutMs: args.commandTimeoutMs, retryWithAnalyticsFallback: true });
  const requestsPayload = requestsResult.payload;
  let requestId = extractItems(requestsPayload).map(extractId).find(Boolean);
  if (!requestId) {
    if (!requestsResult.ok && isAscAnalyticsAuthBlockedMessage(requestsResult.error)) {
      warnings.push('ASC App Analytics batch report: API key can list apps but cannot read App Analytics report requests; Sales and Trends data remains available when ASC_VENDOR_NUMBER is set');
      return reports.length > 0 ? reports : loadLatestCachedReports(appCacheRoot, args.end, warnings);
    }
    if (!requestsResult.ok && isAscAnalyticsTemporarilyUnavailableMessage(requestsResult.error)) {
      warnings.push('ASC App Analytics batch report: request listing is temporarily unavailable; skipped request creation and will retry later');
      return reports.length > 0 ? reports : loadLatestCachedReports(appCacheRoot, args.end, warnings);
    }
    const createdRequestResult = await runBestEffortAscQueryResult('ASC analytics ongoing request creation', [
      'analytics',
      'request',
      '--app',
      appId,
      '--access-type',
      'ONGOING',
      '--output',
      'json',
    ], warnings, { timeoutMs: args.commandTimeoutMs, retryWithAnalyticsFallback: true });
    const createdRequest = createdRequestResult.payload;
    const createdRequestId = extractId(createdRequest) || extractItems(createdRequest).map(extractId).find(Boolean);
    if (createdRequestId || createdRequestResult.ok) {
      warnings.push(
        createdRequestId
          ? `ASC App Analytics batch report: created ongoing analytics request ${createdRequestId}; report instances will be available after Apple finishes processing`
          : 'ASC App Analytics batch report: requested ongoing analytics access; report instances will be available after Apple finishes processing',
      );
    } else if (isAscAnalyticsAuthBlockedMessage(createdRequestResult.error)) {
      warnings.push('ASC App Analytics batch report: API key cannot create/read App Analytics report requests; use an Admin setup key once to create requests, then rerun with the Reports key');
    }
    return reports.length > 0 ? reports : loadLatestCachedReports(appCacheRoot, args.end, warnings);
  }

  const viewPayload = await runBestEffortAscQuery('ASC analytics reports view query', [
    'analytics',
    'view',
    '--request-id',
    requestId,
    '--date',
    args.end,
    '--include-segments',
    '--paginate',
    '--output',
    'json',
  ], warnings, { timeoutMs: args.commandTimeoutMs, retryWithAnalyticsFallback: true });
  const instances = extractInstances(viewPayload).slice(0, Math.max(1, Number(args.analyticsInstanceLimit) || 8));
  if (instances.length === 0) {
    warnings.push(`ASC App Analytics batch report: request ${requestId} has no downloadable instances for ${args.end}`);
    const cached = await loadCachedReportsFromDir(appCacheDir, warnings, 'ASC App Analytics batch report has no downloadable instances');
    if (reports.length > 0 || cached.length > 0) return [...reports, ...cached];
    return loadLatestCachedReports(appCacheRoot, args.end, warnings);
  }

  for (const instance of instances) {
    const report = await downloadAndParseReport(
      `ASC App Analytics batch report ${instance.id}`,
      ['analytics', 'download', '--request-id', requestId, '--instance-id', instance.id],
      appCacheDir,
      `analytics-${instance.id}`,
      args,
      warnings,
    );
    if (report) reports.push(report);
  }

  return reports;
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
    byId.set(id, {
      id,
      name:
        normalizeString(candidate.name) ||
        normalizeString(candidate.appName) ||
        normalizeString(candidate.displayName) ||
        normalizeString(attrs.name),
      bundleId:
        normalizeString(candidate.bundleId) ||
        normalizeString(candidate.bundle_id) ||
        normalizeString(attrs.bundleId),
    });
  }
  return [...byId.values()];
}

async function listAscApps() {
  let payload = null;
  try {
    payload = await runJsonCommand('asc', ['apps', 'list', '--output', 'json']);
  } catch (error) {
    const warnings = [];
    const direct = await listAppleApiCollection('/v1/apps', warnings, 'ASC apps direct API', 45_000);
    if (!direct.ok) {
      throw new Error(`${error instanceof Error ? error.message : String(error)}; direct Apple API fallback failed: ${direct.error || warnings.join('; ')}`);
    }
    payload = { data: direct.items };
  }
  const apps = extractAscAppChoices(payload);
  if (apps.length === 0) {
    throw new Error('asc apps list returned no accessible apps');
  }
  return apps;
}

async function buildSingleAppSummary(appId, args) {
  const warnings = [];
  const metadataTimeoutMs = Math.min(Number(args.commandTimeoutMs) || 45_000, 8_000);
  const ratingsArgs = ['reviews', 'ratings', '--app', appId];
  if (args.country) {
    ratingsArgs.push('--country', args.country);
  } else {
    ratingsArgs.push('--all');
  }

  const [
    statusPayload,
    ratingsPayload,
    reviewSummariesPayload,
    feedbackPayload,
    batchReports,
  ] = await Promise.all([
    runBestEffortAscQuery('ASC status query', [
      'status',
      '--app',
      appId,
      '--include',
      'builds,testflight,submission,review,appstore',
      '--output',
      'json',
    ], warnings, { timeoutMs: metadataTimeoutMs }),
    runBestEffortAscQuery('ASC ratings query', ratingsArgs, warnings, { timeoutMs: metadataTimeoutMs }),
    runBestEffortAscQuery('ASC review summarizations query', [
      'reviews',
      'summarizations',
      '--app',
      appId,
      '--platform',
      'IOS',
      '--limit',
      String(args.reviewsLimit),
      '--fields',
      'text,createdDate,locale',
      '--output',
      'json',
    ], warnings, { timeoutMs: metadataTimeoutMs }),
    runBestEffortAscQuery('ASC beta feedback query', [
      'testflight',
      'feedback',
      'list',
      '--app',
      appId,
      '--limit',
      String(args.feedbackLimit),
      '--sort',
      '-createdDate',
      '--output',
      'json',
    ], warnings, { timeoutMs: metadataTimeoutMs }),
    downloadBatchAnalyticsReports(appId, args, warnings),
  ]);
  const batchRows = batchReports.flatMap((report) => report.rows);
  const batchAnalyticsPayload = batchRows.length > 0 ? summarizeBatchRows(batchRows, appId) : null;

  return buildAscSummary({
    appId,
    statusPayload,
    ratingsPayload,
    reviewSummariesPayload,
    feedbackPayload,
    batchAnalyticsPayload,
    analyticsWindow: { start: args.start, end: args.end },
    analyticsWarnings: warnings,
    batchReports: batchReports.map((report) => ({
      label: report.label,
      outputPath: report.outputPath,
      rowCount: report.rows.length,
      cacheStatus: report.cacheStatus || null,
      columns: reportColumns(report),
      ...classifyReportColumns(report),
    })),
    maxSignals: args.maxSignals,
  });
}

async function buildAllAppsSummary(args) {
  const apps = args.app ? [{ id: args.app }] : await listAscApps();
  const summaries = [];
  const warnings = [];

  for (const app of apps) {
    try {
      summaries.push(await buildSingleAppSummary(app.id, args));
    } catch (error) {
      warnings.push({
        appId: app.id,
        appName: app.name || null,
        error: error instanceof Error ? error.message : String(error),
        publicStatusHint: String(error instanceof Error ? error.message : error)
          .toLowerCase()
          .includes('403')
          ? 'app may not be public yet or ASC analytics reports may not be available for this app'
          : null,
      });
    }
  }

  if (summaries.length === 0) {
    throw new Error(`ASC summary failed for every accessible app: ${JSON.stringify(warnings)}`);
  }

  if (summaries.length === 1) {
    const summary = summaries[0];
    if (warnings.length > 0) {
      summary.meta = { ...(summary.meta || {}), warnings };
    }
    return summary;
  }

  const signals = summaries
    .flatMap((summary) =>
      (Array.isArray(summary.signals) ? summary.signals : []).map((signal) => ({
        ...signal,
        id: `${summary.meta?.appId || 'app'}_${signal.id}`,
        evidence: [
          `ASC app: ${summary.meta?.appId || 'unknown'}`,
          ...(Array.isArray(signal.evidence) ? signal.evidence : []),
        ],
      })),
    )
    .sort((a, b) => {
      const priorityRank = { high: 0, medium: 1, low: 2 };
      return (priorityRank[a.priority] ?? 3) - (priorityRank[b.priority] ?? 3);
    })
    .slice(0, Math.max(1, Number(args.maxSignals) || 4));

  return {
    project: 'app-store-connect:all',
    window: 'latest',
    signals,
    meta: {
      generatedAt: new Date().toISOString(),
      source: 'asc',
      appScope: 'all',
      appCount: apps.length,
      summarizedAppCount: summaries.length,
      appIds: summaries.map((summary) => summary.meta?.appId).filter(Boolean),
      warnings,
    },
  };
}

async function main() {
  await loadOpenClawGrowthSecrets();
  const args = parseArgs(process.argv.slice(2));
  const summary = await buildAllAppsSummary(args);

  await writeJsonOutput(args.out, summary);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
