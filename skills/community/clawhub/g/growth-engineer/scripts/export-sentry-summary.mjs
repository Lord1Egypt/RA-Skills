#!/usr/bin/env node
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { writeJsonOutput, buildSentrySummary } from './openclaw-exporters-lib.mjs';
const DEFAULT_BASE_URL = 'https://sentry.io';
const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const DEFAULT_SENTRY_FETCH_RETRIES = 3;
const DEFAULT_SENTRY_REQUEST_TIMEOUT_MS = 15_000;
const DEFAULT_SENTRY_FETCH_CONCURRENCY = 3;
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
function parseRetryAfterMs(value) {
    const raw = String(value || '').trim();
    if (!raw)
        return null;
    const seconds = Number(raw);
    if (Number.isFinite(seconds) && seconds >= 0)
        return seconds * 1000;
    const dateMs = Date.parse(raw);
    if (Number.isFinite(dateMs))
        return Math.max(0, dateMs - Date.now());
    return null;
}
function isRetryableSentryStatus(status) {
    return status === 429 || status >= 500;
}
function positiveIntegerEnv(name, fallback, min = 1, max = 120_000) {
    const parsed = Number.parseInt(String(process.env[name] || ''), 10);
    if (!Number.isFinite(parsed))
        return fallback;
    return Math.max(min, Math.min(max, parsed));
}
function sentryRequestTimeoutMs() {
    return positiveIntegerEnv('OPENCLAW_SENTRY_REQUEST_TIMEOUT_MS', DEFAULT_SENTRY_REQUEST_TIMEOUT_MS, 1_000, 60_000);
}
function sentryFetchConcurrency() {
    return positiveIntegerEnv('OPENCLAW_SENTRY_FETCH_CONCURRENCY', DEFAULT_SENTRY_FETCH_CONCURRENCY, 1, 10);
}
function getSentryRetryDelayMs(response, attempt) {
    const retryAfterMs = parseRetryAfterMs(response.headers.get('retry-after'));
    if (retryAfterMs !== null)
        return Math.min(retryAfterMs, 15_000);
    return Math.min(1_000 * 2 ** attempt, 8_000);
}
function isAbortError(error) {
    return error && typeof error === 'object' && (error.name === 'AbortError' || error.code === 'ABORT_ERR');
}
function isRetryableSentryError(error) {
    const status = error && typeof error === 'object' ? Number(error.status) : null;
    if (Number.isFinite(status) && isRetryableSentryStatus(status))
        return true;
    if (error && typeof error === 'object' && error.retryable === true)
        return true;
    return /timed out|timeout|fetch failed|network|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|socket hang up|Sentry API (?:429|5\d\d)/i.test(error instanceof Error ? error.message : String(error || ''));
}
function compactErrorDetail(error) {
    const raw = error instanceof Error ? error.message : String(error || 'unknown error');
    const text = raw
        .replace(/<!doctype html>[\s\S]*?<\/html>/gi, 'HTML error response')
        .replace(/<[^>]+>/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    if (/Sentry API 429/i.test(text))
        return 'Sentry API rate-limited the request.';
    if (/Sentry API 5\d\d/i.test(text))
        return 'Sentry API returned a retryable 5xx response.';
    if (/timed out|timeout/i.test(text))
        return 'Sentry request timed out after retry.';
    if (/fetch failed|network|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|socket hang up/i.test(text)) {
        return 'Sentry network request failed after retry.';
    }
    return text.length > 220 ? `${text.slice(0, 217)}...` : text;
}
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
Export Sentry Summary

Builds an OpenClaw-compatible crash/stability summary JSON from the Sentry API.

Usage:
  node scripts/export-sentry-summary.mjs [options]

Options:
  --org <slug>           Sentry organization slug (default: SENTRY_ORG)
  --project <slug>       Sentry project slug (default: SENTRY_PROJECT)
  --environment <name>   Sentry environment filter (default: SENTRY_ENVIRONMENT or production)
  --last <duration>      Sentry statsPeriod, e.g. 24h, 7d, 30d (default: 7d)
  --query <query>        Issue search query (default: is:unresolved)
  --limit <n>            Max Sentry issues to fetch, capped at 50 (default: 20)
  --events-per-issue <n> Fetch recent events for each returned issue, capped at 10 (default: 0)
  --max-signals <n>      Max normalized signals/issues to emit (default: 5)
  --base-url <url>       Sentry base URL for self-hosted instances (default: SENTRY_BASE_URL or ${DEFAULT_BASE_URL})
  --config <file>        OpenClaw config with sources.sentry.accounts[] (default: ${DEFAULT_CONFIG_PATH} when present)
  --accounts-file <file> JSON file containing an accounts[] array or array
  --out <file>           Write JSON to file instead of stdout
  --help, -h             Show help
`);
    process.exit(exitCode);
}
function parseArgs(argv) {
    const args = {
        org: String(process.env.SENTRY_ORG || '').trim(),
        project: String(process.env.SENTRY_PROJECT || '').trim(),
        environment: String(process.env.SENTRY_ENVIRONMENT || 'production').trim(),
        last: '7d',
        query: 'is:unresolved',
        limit: 20,
        eventsPerIssue: 0,
        maxSignals: 5,
        baseUrl: String(process.env.SENTRY_BASE_URL || DEFAULT_BASE_URL).trim(),
        config: '',
        accountsFile: '',
        out: '',
    };
    for (let index = 0; index < argv.length; index += 1) {
        const token = argv[index];
        const next = argv[index + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--org') {
            args.org = String(next || '').trim();
            index += 1;
        }
        else if (token === '--project') {
            args.project = String(next || '').trim();
            index += 1;
        }
        else if (token === '--environment') {
            args.environment = String(next || '').trim();
            index += 1;
        }
        else if (token === '--last') {
            args.last = String(next || args.last).trim();
            index += 1;
        }
        else if (token === '--query') {
            args.query = String(next || '').trim();
            index += 1;
        }
        else if (token === '--limit') {
            args.limit = normalizeInteger(next, '--limit', 1, 50);
            index += 1;
        }
        else if (token === '--events-per-issue') {
            args.eventsPerIssue = normalizeInteger(next, '--events-per-issue', 0, 10);
            index += 1;
        }
        else if (token === '--max-signals') {
            args.maxSignals = normalizeInteger(next, '--max-signals', 1, 20);
            index += 1;
        }
        else if (token === '--base-url') {
            args.baseUrl = String(next || '').trim();
            index += 1;
        }
        else if (token === '--config') {
            args.config = String(next || '').trim();
            index += 1;
        }
        else if (token === '--accounts-file') {
            args.accountsFile = String(next || '').trim();
            index += 1;
        }
        else if (token === '--out') {
            args.out = String(next || '').trim();
            index += 1;
        }
        else if (token === '--help' || token === '-h') {
            printHelpAndExit(0);
        }
        else {
            printHelpAndExit(1, `Unknown argument: ${token}`);
        }
    }
    return args;
}
async function readJsonIfPresent(filePath, required = false) {
    const normalized = String(filePath || '').trim();
    if (!normalized)
        return null;
    try {
        return JSON.parse(await fs.readFile(path.resolve(normalized), 'utf8'));
    }
    catch (error) {
        if (!required && error && typeof error === 'object' && error.code === 'ENOENT')
            return null;
        throw error;
    }
}
function normalizeArray(value) {
    if (Array.isArray(value))
        return value;
    if (Array.isArray(value?.accounts))
        return value.accounts;
    return [];
}
function normalizeProjectEntries(account) {
    const projects = Array.isArray(account?.projects) ? account.projects : account?.project ? [account.project] : [];
    return projects
        .map((entry) => (typeof entry === 'string' ? { project: entry } : entry))
        .filter((entry) => entry && typeof entry === 'object' && String(entry.project || entry.slug || '').trim())
        .map((entry) => ({
        project: String(entry.project || entry.slug || '').trim(),
        org: String(entry.org || entry.organization || account.org || account.organization || '').trim(),
        environment: String(entry.environment || account.environment || process.env.SENTRY_ENVIRONMENT || 'production').trim(),
        last: String(entry.last || account.last || '').trim(),
        query: String(entry.query || account.query || '').trim(),
        limit: entry.limit || account.limit,
        eventsPerIssue: entry.eventsPerIssue || entry.events_per_issue || account.eventsPerIssue || account.events_per_issue,
    }));
}
function normalizeAccountConfigs(rawAccounts, args) {
    const normalized = rawAccounts.flatMap((account, index) => {
        if (!account || typeof account !== 'object')
            return [];
        const id = String(account.id || account.key || account.label || `sentry_${index + 1}`).trim();
        const baseUrl = String(account.baseUrl || account.base_url || account.url || args.baseUrl || DEFAULT_BASE_URL).trim();
        const tokenEnv = String(account.tokenEnv || account.token_env || account.secretEnv || 'SENTRY_AUTH_TOKEN').trim();
        const projectEntries = normalizeProjectEntries(account);
        if (projectEntries.length > 0) {
            return projectEntries.map((projectEntry) => ({
                ...projectEntry,
                id: `${id}_${projectEntry.project}`.replace(/[^a-zA-Z0-9._-]+/g, '_'),
                accountId: id,
                label: String(account.label || account.name || id).trim(),
                baseUrl,
                tokenEnv,
                maxSignals: args.maxSignals,
            }));
        }
        const org = String(account.org || account.organization || args.org || '').trim();
        if (!org)
            return [];
        return [{
                id: id.replace(/[^a-zA-Z0-9._-]+/g, '_'),
                accountId: id,
                label: String(account.label || account.name || id).trim(),
                baseUrl,
                tokenEnv,
                org,
                project: '',
                environment: String(account.environment || args.environment || process.env.SENTRY_ENVIRONMENT || 'production').trim(),
                last: String(account.last || args.last || '').trim(),
                query: String(account.query || args.query || '').trim(),
                limit: account.limit || args.limit,
                eventsPerIssue: account.eventsPerIssue || args.eventsPerIssue,
                maxSignals: args.maxSignals,
            }];
    });
    return dedupeAccountConfigs(normalized);
}
function dedupeAccountConfigs(accounts) {
    const seen = new Set();
    const result = [];
    for (const account of accounts) {
        const key = JSON.stringify({
            baseUrl: String(account.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, '').toLowerCase(),
            tokenEnv: account.tokenEnv,
            org: account.org,
            project: account.project || '',
            environment: account.environment || '',
            last: account.last || '',
            query: account.query || '',
            limit: account.limit || '',
            eventsPerIssue: account.eventsPerIssue || '',
        });
        if (seen.has(key))
            continue;
        seen.add(key);
        result.push(account);
    }
    return result;
}
async function expandDiscoveredProjects(account, token) {
    if (String(account.project || '').trim())
        return [account];
    const org = requireValue(account.org, 'SENTRY_ORG');
    const url = buildUrl(account.baseUrl || DEFAULT_BASE_URL, `/api/0/organizations/${encodeURIComponent(org)}/projects/`, {
        per_page: 100,
    });
    const payload = await sentryFetchList(url, token);
    const projects = apiListItems(payload)
        .map((project) => String(project?.slug || project?.name || '').trim())
        .filter(Boolean);
    const uniqueProjects = [...new Set(projects)];
    if (uniqueProjects.length === 0) {
        throw new Error(`No Sentry projects are visible for org ${org}. Check token scopes org:read/project:read/event:read and org access.`);
    }
    return uniqueProjects.map((project) => ({
        ...account,
        project,
        id: `${account.accountId || account.id}_${project}`.replace(/[^a-zA-Z0-9._-]+/g, '_'),
    }));
}
async function loadConfiguredAccounts(args) {
    const accountPayload = args.accountsFile ? await readJsonIfPresent(args.accountsFile, true) : null;
    const accountsFromFile = normalizeArray(accountPayload);
    if (accountsFromFile.length > 0)
        return normalizeAccountConfigs(accountsFromFile, args);
    const configPath = args.config || DEFAULT_CONFIG_PATH;
    const config = await readJsonIfPresent(configPath, Boolean(args.config));
    const accountsFromConfig = normalizeArray(config?.sources?.sentry);
    if (accountsFromConfig.length > 0)
        return normalizeAccountConfigs(accountsFromConfig, args);
    const singleAccount = {
        id: 'sentry',
        label: 'Sentry',
        baseUrl: args.baseUrl,
        tokenEnv: 'SENTRY_AUTH_TOKEN',
        org: args.org,
        project: args.project,
        environment: args.environment,
        last: args.last,
        query: args.query,
        limit: args.limit,
        eventsPerIssue: args.eventsPerIssue,
    };
    return normalizeProjectEntries(singleAccount).length > 0 ? normalizeAccountConfigs([singleAccount], args) : [];
}
function normalizeInteger(value, label, min, max) {
    const parsed = Number.parseInt(String(value || ''), 10);
    if (!Number.isFinite(parsed) || parsed < min || parsed > max) {
        printHelpAndExit(1, `${label} must be an integer between ${min} and ${max}`);
    }
    return parsed;
}
function requireValue(value, label) {
    const normalized = String(value || '').trim();
    if (!normalized) {
        throw new Error(`${label} is required. Set it in the Sentry connector wizard or pass the flag explicitly.`);
    }
    return normalized;
}
function describeAccountTarget(account) {
    const parts = [
        account.label || account.accountId || account.id || 'Sentry',
        account.accountId || account.id ? `id=${account.accountId || account.id}` : null,
        `baseUrl=${account.baseUrl || DEFAULT_BASE_URL}`,
        account.org ? `org=${account.org}` : null,
        account.project ? `project=${account.project}` : null,
        account.environment ? `environment=${account.environment}` : null,
        account.tokenEnv ? `tokenEnv=${account.tokenEnv}` : null,
    ].filter(Boolean);
    return parts.join(' ');
}
function withAccountTargetError(error, account, action) {
    const detail = error instanceof Error ? error.message : String(error);
    const wrapped = new Error(`${action} failed for ${describeAccountTarget(account)}: ${detail}`);
    wrapped.status = error && typeof error === 'object' ? error.status : undefined;
    wrapped.retryable = isRetryableSentryError(error);
    return wrapped;
}
function buildUrl(baseUrl, pathname, params) {
    const url = new URL(pathname, `${baseUrl.replace(/\/$/, '')}/`);
    for (const [key, value] of Object.entries(params)) {
        if (value === undefined || value === null || value === '')
            continue;
        url.searchParams.set(key, String(value));
    }
    return url;
}
function apiListItems(payload) {
    if (Array.isArray(payload))
        return payload;
    if (!payload || typeof payload !== 'object')
        return [];
    if (Array.isArray(payload.results))
        return payload.results;
    if (Array.isArray(payload.data))
        return payload.data;
    if (Array.isArray(payload.projects))
        return payload.projects;
    return [];
}
async function sentryFetchJson(url, token) {
    let lastError = null;
    for (let attempt = 0; attempt < DEFAULT_SENTRY_FETCH_RETRIES; attempt += 1) {
        let response;
        const controller = new AbortController();
        const timeoutMs = sentryRequestTimeoutMs();
        const timeout = setTimeout(() => controller.abort(), timeoutMs);
        try {
            response = await fetch(url, {
                method: 'GET',
                signal: controller.signal,
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${token}`,
                    'User-Agent': 'openclaw-growth-sentry-exporter',
                },
            });
        }
        catch (error) {
            lastError = isAbortError(error) ? new Error(`Sentry API request timed out after ${timeoutMs}ms`) : error;
            if (lastError && typeof lastError === 'object') {
                lastError.retryable = true;
            }
            if (attempt < DEFAULT_SENTRY_FETCH_RETRIES - 1) {
                await sleep(Math.min(1_000 * 2 ** attempt, 8_000));
                continue;
            }
            throw lastError;
        }
        finally {
            clearTimeout(timeout);
        }
        const body = await response.text();
        if (response.ok) {
            return body ? JSON.parse(body) : null;
        }
        lastError = new Error(`Sentry API ${response.status}: ${body.slice(0, 500) || 'request failed'}`);
        lastError.status = response.status;
        lastError.retryable = isRetryableSentryStatus(response.status);
        if (isRetryableSentryStatus(response.status) && attempt < DEFAULT_SENTRY_FETCH_RETRIES - 1) {
            await sleep(getSentryRetryDelayMs(response, attempt));
            continue;
        }
        throw lastError;
    }
    throw lastError || new Error('Sentry API request failed');
}
async function sentryFetchList(url, token) {
    const items = [];
    let nextUrl = url;
    for (let page = 0; nextUrl && page < 10; page += 1) {
        const payload = await sentryFetchJson(nextUrl, token);
        items.push(...apiListItems(payload));
        const next = payload && typeof payload === 'object' ? payload.next : null;
        nextUrl = typeof next === 'string' && next.trim() ? new URL(next, `${nextUrl.origin}/`) : null;
    }
    return items;
}
function redactString(value) {
    return String(value || '')
        .replace(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g, '[REDACTED_EMAIL]')
        .replace(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g, '[REDACTED_IP]');
}
function redactData(value) {
    if (typeof value === 'string')
        return redactString(value);
    if (Array.isArray(value))
        return value.map((entry) => redactData(entry));
    if (value && typeof value === 'object') {
        return Object.fromEntries(Object.entries(value).map(([key, entry]) => [
            key,
            ['email', 'ip', 'ip_address'].includes(key.toLowerCase()) ? '[REDACTED]' : redactData(entry),
        ]));
    }
    return value;
}
async function listIssues(account, token) {
    try {
        const org = encodeURIComponent(requireValue(account.org, 'SENTRY_ORG'));
        const project = encodeURIComponent(requireValue(account.project, 'SENTRY_PROJECT'));
        const url = buildUrl(account.baseUrl || DEFAULT_BASE_URL, `/api/0/projects/${org}/${project}/issues/`, {
            statsPeriod: account.last,
            environment: account.environment,
            query: account.query,
            per_page: account.limit,
        });
        const payload = await sentryFetchJson(url, token);
        return Array.isArray(payload) ? payload : [];
    }
    catch (error) {
        throw withAccountTargetError(error, account, 'Sentry issue fetch');
    }
}
async function listIssueEvents(account, token, issueId) {
    try {
        const url = buildUrl(account.baseUrl || DEFAULT_BASE_URL, `/api/0/issues/${encodeURIComponent(issueId)}/events/`, {
            per_page: account.eventsPerIssue,
        });
        return (await sentryFetchList(url, token)).slice(0, Math.max(0, Number(account.eventsPerIssue) || 0));
    }
    catch (error) {
        throw withAccountTargetError(error, account, `Sentry issue event fetch ${issueId}`);
    }
}
function buildFailureRecord(error, account, action) {
    return {
        id: account.id || account.accountId || null,
        accountId: account.accountId || account.id || null,
        label: account.label || account.accountId || account.id || 'Sentry',
        baseUrl: account.baseUrl || DEFAULT_BASE_URL,
        org: account.org || null,
        project: account.project || null,
        environment: account.environment || null,
        action,
        retryable: isRetryableSentryError(error),
        detail: compactErrorDetail(error),
    };
}
function formatBlockingFailures(failures) {
    return failures
        .slice(0, 5)
        .map((failure) => {
        const target = [
            failure.label,
            failure.org ? `org=${failure.org}` : null,
            failure.project ? `project=${failure.project}` : null,
        ].filter(Boolean).join(' ');
        return `${target}: ${failure.detail}`;
    })
        .join('\n');
}
async function mapLimit(items, limit, mapper) {
    const results = [];
    let nextIndex = 0;
    const workerCount = Math.min(limit, items.length);
    const workers = Array.from({ length: workerCount }, async () => {
        while (nextIndex < items.length) {
            const index = nextIndex;
            nextIndex += 1;
            results[index] = await mapper(items[index], index);
        }
    });
    await Promise.all(workers);
    return results;
}
function attachFailureMeta(summary, failures) {
    if (failures.length === 0)
        return summary;
    return {
        ...summary,
        meta: {
            ...(summary?.meta || {}),
            partial: true,
            failureCount: failures.length,
            failures: failures.map((failure) => ({
                id: failure.id,
                accountId: failure.accountId,
                label: failure.label,
                baseUrl: failure.baseUrl,
                org: failure.org,
                project: failure.project,
                environment: failure.environment,
                action: failure.action,
                retryable: failure.retryable,
                detail: failure.detail,
            })),
        },
    };
}
async function main() {
    const args = parseArgs(process.argv.slice(2));
    const configuredAccounts = await loadConfiguredAccounts(args);
    if (configuredAccounts.length === 0) {
        throw new Error(`No Sentry account configured. Set SENTRY_AUTH_TOKEN plus SENTRY_ORG, pass --org, or add sources.sentry.accounts[] in ${args.config || DEFAULT_CONFIG_PATH}.`);
    }
    const accounts = [];
    const failures = [];
    for (const account of configuredAccounts) {
        try {
            const token = requireValue(process.env[account.tokenEnv], `${account.tokenEnv} for ${describeAccountTarget(account)}`);
            accounts.push(...await expandDiscoveredProjects(account, token));
        }
        catch (error) {
            const wrapped = withAccountTargetError(error, account, 'Sentry project discovery');
            failures.push(buildFailureRecord(wrapped, account, 'project_discovery'));
        }
    }
    const summaries = [];
    await mapLimit(accounts, sentryFetchConcurrency(), async (account) => {
        try {
            const token = requireValue(process.env[account.tokenEnv], `${account.tokenEnv} for ${describeAccountTarget(account)}`);
            const issuesPayload = redactData(await listIssues(account, token));
            const eventsPerIssue = Math.max(0, Math.min(Number(account.eventsPerIssue ?? args.eventsPerIssue) || 0, 10));
            if (eventsPerIssue > 0) {
                await mapLimit(issuesPayload, sentryFetchConcurrency(), async (issue) => {
                    const issueId = String(issue?.id || '').trim();
                    if (!issueId)
                        return;
                    try {
                        issue.eventsPayload = redactData(await listIssueEvents({ ...account, eventsPerIssue }, token, issueId));
                    }
                    catch (error) {
                        failures.push(buildFailureRecord(error, account, 'issue_event_fetch'));
                    }
                });
            }
            summaries.push({
                id: account.id,
                label: account.label,
                org: account.org,
                project: account.project,
                environment: account.environment,
                last: account.last || args.last,
                issuesPayload,
                eventsPerIssue,
                maxSignals: args.maxSignals,
            });
        }
        catch (error) {
            failures.push(buildFailureRecord(error, account, 'issue_fetch'));
        }
    });
    const blockingFailures = failures.filter((failure) => !failure.retryable && failure.action !== 'issue_event_fetch');
    if (blockingFailures.length > 0) {
        throw new Error(`Sentry connector has non-retryable configuration/auth failures:\n${formatBlockingFailures(blockingFailures)}`);
    }
    const summary = summaries.length === 1
        ? buildSentrySummary(summaries[0])
        : buildSentrySummary({ accounts: summaries, last: args.last, maxSignals: args.maxSignals });
    await writeJsonOutput(args.out, attachFailureMeta(summary, failures));
}
main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
});
