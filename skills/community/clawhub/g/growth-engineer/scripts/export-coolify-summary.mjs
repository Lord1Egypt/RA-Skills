#!/usr/bin/env node
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { buildCoolifySummary, writeJsonOutput } from './openclaw-exporters-lib.mjs';
const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const DEFAULT_TOKEN_ENV = 'COOLIFY_API_TOKEN';
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
Export Coolify Summary

Builds an OpenClaw-compatible hosting/deployment summary JSON from the Coolify API.

Usage:
  node scripts/export-coolify-summary.mjs [options]

Options:
  --base-url <url>       Coolify base URL, for example https://coolify.example.com (default: COOLIFY_BASE_URL or config)
  --token-env <name>     Environment variable containing the Coolify API token (default: COOLIFY_API_TOKEN or config)
  --last <duration>      Window for recent deployment signals, e.g. 24h, 7d (default: 24h)
  --limit <n>            Max items to read per endpoint where supported (default: 50)
  --max-signals <n>      Max normalized signals to emit (default: 8)
  --config <file>        OpenClaw config with sources.coolify (default: ${DEFAULT_CONFIG_PATH} when present)
  --out <file>           Write JSON to file instead of stdout
  --help, -h             Show help
`);
    process.exit(exitCode);
}
function parseArgs(argv) {
    const args = {
        baseUrl: String(process.env.COOLIFY_BASE_URL || '').trim(),
        tokenEnv: DEFAULT_TOKEN_ENV,
        last: '24h',
        limit: 50,
        maxSignals: 8,
        config: '',
        out: '',
    };
    for (let index = 0; index < argv.length; index += 1) {
        const token = argv[index];
        const next = argv[index + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--base-url') {
            args.baseUrl = String(next || '').trim();
            index += 1;
        }
        else if (token === '--token-env') {
            args.tokenEnv = String(next || DEFAULT_TOKEN_ENV).trim();
            index += 1;
        }
        else if (token === '--last') {
            args.last = String(next || args.last).trim();
            index += 1;
        }
        else if (token === '--limit') {
            args.limit = normalizeInteger(next, '--limit', 1, 200);
            index += 1;
        }
        else if (token === '--max-signals') {
            args.maxSignals = normalizeInteger(next, '--max-signals', 1, 20);
            index += 1;
        }
        else if (token === '--config') {
            args.config = String(next || '').trim();
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
function normalizeInteger(value, label, min, max) {
    const parsed = Number.parseInt(String(value || ''), 10);
    if (!Number.isFinite(parsed) || parsed < min || parsed > max) {
        printHelpAndExit(1, `${label} must be an integer between ${min} and ${max}`);
    }
    return parsed;
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
function normalizeBaseUrl(value) {
    const raw = String(value || '').trim().replace(/\/+$/, '');
    if (!raw)
        return '';
    if (!/^https?:\/\//i.test(raw))
        return `https://${raw}`;
    return raw;
}
function resolveApiBaseUrl(baseUrl) {
    const normalized = normalizeBaseUrl(baseUrl);
    if (!normalized)
        return '';
    if (/\/api\/v1$/i.test(normalized))
        return normalized;
    if (/\/api$/i.test(normalized))
        return `${normalized}/v1`;
    return `${normalized}/api/v1`;
}
function apiListItems(payload) {
    if (Array.isArray(payload))
        return payload;
    if (!payload || typeof payload !== 'object')
        return [];
    if (Array.isArray(payload.data))
        return payload.data;
    if (Array.isArray(payload.results))
        return payload.results;
    if (Array.isArray(payload.items))
        return payload.items;
    return [];
}
function redactString(value) {
    return String(value || '')
        .replace(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g, '[REDACTED_EMAIL]')
        .replace(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g, '[REDACTED_IP]')
        .replace(/(token|password|secret|key)=([^&\s]+)/gi, '$1=[REDACTED]');
}
function redactData(value) {
    if (typeof value === 'string')
        return redactString(value);
    if (Array.isArray(value))
        return value.map((entry) => redactData(entry));
    if (value && typeof value === 'object') {
        return Object.fromEntries(Object.entries(value).map(([key, entry]) => {
            const lower = key.toLowerCase();
            if (/(token|password|secret|private_key|api_key)/.test(lower))
                return [key, '[REDACTED]'];
            return [key, redactData(entry)];
        }));
    }
    return value;
}
async function coolifyFetchJson({ apiBaseUrl, token, pathname, limit }) {
    const url = new URL(pathname.replace(/^\//, ''), `${apiBaseUrl}/`);
    if (limit && !url.searchParams.has('limit'))
        url.searchParams.set('limit', String(limit));
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            Authorization: `Bearer ${token}`,
            'User-Agent': 'openclaw-growth-coolify-exporter',
        },
    });
    const body = await response.text();
    if (!response.ok) {
        throw new Error(`${url.pathname}: HTTP ${response.status}: ${body.slice(0, 500) || 'request failed'}`);
    }
    return body ? JSON.parse(body) : null;
}
async function readEndpoint({ apiBaseUrl, token, pathname, limit, warnings }) {
    try {
        const payload = await coolifyFetchJson({ apiBaseUrl, token, pathname, limit });
        return apiListItems(payload);
    }
    catch (error) {
        warnings.push(error instanceof Error ? error.message : String(error));
        return [];
    }
}
async function loadCoolifyConfig(args) {
    const configPath = args.config || DEFAULT_CONFIG_PATH;
    const config = await readJsonIfPresent(configPath, Boolean(args.config));
    const source = config?.sources?.coolify && typeof config.sources.coolify === 'object'
        ? config.sources.coolify
        : {};
    return {
        baseUrl: normalizeBaseUrl(args.baseUrl || source.baseUrl || source.base_url || process.env.COOLIFY_BASE_URL || ''),
        tokenEnv: String(source.tokenEnv || source.token_env || source.secretEnv || args.tokenEnv || DEFAULT_TOKEN_ENV).trim(),
    };
}
async function main() {
    const args = parseArgs(process.argv.slice(2));
    const config = await loadCoolifyConfig(args);
    const baseUrl = normalizeBaseUrl(config.baseUrl);
    if (!baseUrl) {
        throw new Error('COOLIFY_BASE_URL is required. Pass --base-url or configure sources.coolify.baseUrl.');
    }
    const token = String(process.env[config.tokenEnv] || '').trim();
    if (!token) {
        throw new Error(`${config.tokenEnv} is required. Create a Coolify API token with read-only permissions and store it in the local secrets file.`);
    }
    const warnings = [];
    const apiBaseUrl = resolveApiBaseUrl(baseUrl);
    const [applications, deployments, resources, servers] = await Promise.all([
        readEndpoint({ apiBaseUrl, token, pathname: '/applications', limit: args.limit, warnings }),
        readEndpoint({ apiBaseUrl, token, pathname: '/deployments', limit: args.limit, warnings }),
        readEndpoint({ apiBaseUrl, token, pathname: '/resources', limit: args.limit, warnings }),
        readEndpoint({ apiBaseUrl, token, pathname: '/servers', limit: args.limit, warnings }),
    ]);
    const summary = buildCoolifySummary({
        baseUrl,
        last: args.last,
        maxSignals: args.maxSignals,
        applications: redactData(applications),
        deployments: redactData(deployments),
        resources: redactData(resources),
        servers: redactData(servers),
        warnings,
    });
    await writeJsonOutput(args.out, summary);
}
main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
});
