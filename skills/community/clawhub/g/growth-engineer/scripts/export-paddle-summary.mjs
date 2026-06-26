#!/usr/bin/env node
import { promises as fs } from 'node:fs';
import process from 'node:process';
import { buildPaddleSummary, writeJsonOutput } from './openclaw-exporters-lib.mjs';
import { loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
Export Paddle Summary

Builds an OpenClaw-compatible Paddle metrics summary JSON from Paddle Billing metrics.

Usage:
  node scripts/export-paddle-summary.mjs [options]

Options:
  --environment <live|sandbox> Paddle environment (default: live)
  --from <date>                Start date YYYY-MM-DD (default: 30 days before --to)
  --to <date>                  End date YYYY-MM-DD, exclusive in Paddle metrics (default: today UTC)
  --last <duration>            Relative window like 30d (used when --from is omitted)
  --config <file>              Growth config path for sources.paddle.accounts[]
  --out <file>                 Write JSON to file instead of stdout
  --max-signals <n>            Maximum signals to emit (default: 6)
  --help, -h                   Show help

Environment:
  PADDLE_API_KEY               Paddle API key for the account metrics endpoints
`);
    process.exit(exitCode);
}
function formatDate(date) {
    return date.toISOString().slice(0, 10);
}
function addDays(date, days) {
    const copy = new Date(date);
    copy.setUTCDate(copy.getUTCDate() + days);
    return copy;
}
function parseDurationDays(value, fallback) {
    const match = String(value || '').trim().match(/^(\d+)\s*d$/i);
    if (!match)
        return fallback;
    const parsed = Number.parseInt(match[1], 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}
function parseArgs(argv) {
    const defaultTo = formatDate(new Date());
    const args = {
        environment: String(process.env.PADDLE_ENVIRONMENT || 'live').trim().toLowerCase() || 'live',
        from: '',
        to: defaultTo,
        last: '30d',
        config: String(process.env.OPENCLAW_GROWTH_CONFIG_PATH || '').trim(),
        out: '',
        maxSignals: 6,
    };
    for (let index = 0; index < argv.length; index += 1) {
        const token = argv[index];
        const next = argv[index + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--environment') {
            args.environment = String(next || '').trim().toLowerCase();
            index += 1;
        }
        else if (token === '--from') {
            args.from = String(next || '').trim();
            index += 1;
        }
        else if (token === '--to') {
            args.to = String(next || '').trim();
            index += 1;
        }
        else if (token === '--last') {
            args.last = String(next || '').trim() || args.last;
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
        else if (token === '--max-signals') {
            const parsed = Number.parseInt(String(next || ''), 10);
            if (!Number.isFinite(parsed) || parsed <= 0) {
                printHelpAndExit(1, `Invalid value for --max-signals: ${String(next || '')}`);
            }
            args.maxSignals = parsed;
            index += 1;
        }
        else if (token === '--help' || token === '-h') {
            printHelpAndExit(0);
        }
        else {
            printHelpAndExit(1, `Unknown argument: ${token}`);
        }
    }
    if (!['live', 'sandbox'].includes(args.environment)) {
        printHelpAndExit(1, `Invalid --environment: ${args.environment}. Use live or sandbox.`);
    }
    if (!args.from) {
        args.from = formatDate(addDays(new Date(`${args.to}T00:00:00Z`), -parseDurationDays(args.last, 30)));
    }
    return args;
}
function paddleBaseUrl(environment) {
    return environment === 'sandbox' ? 'https://sandbox-api.paddle.com' : 'https://api.paddle.com';
}
function buildUrl(baseUrl, pathname, args) {
    const url = new URL(pathname, baseUrl);
    url.searchParams.set('from', args.from);
    url.searchParams.set('to', args.to);
    return url.toString();
}
async function readJsonIfPresent(filePath) {
    if (!filePath)
        return null;
    try {
        return JSON.parse(await fs.readFile(filePath, 'utf8'));
    }
    catch {
        return null;
    }
}
function normalizePaddleAccount(account, index, source, args) {
    const id = String(account?.id || account?.key || account?.label || `paddle_${index + 1}`)
        .trim()
        .replace(/[^a-zA-Z0-9._-]+/g, '_');
    return {
        id,
        label: String(account?.label || account?.name || account?.id || `Paddle ${index + 1}`).trim(),
        tokenEnv: String(account?.tokenEnv || account?.token_env || account?.secretEnv || (index === 0 ? source?.tokenEnv || 'PADDLE_API_KEY' : `PADDLE_API_KEY_${index + 1}`)).trim(),
        environment: String(account?.environment || source?.environment || args.environment || 'live').trim().toLowerCase() || 'live',
    };
}
async function resolvePaddleAccounts(args) {
    const config = await readJsonIfPresent(args.config);
    const source = config?.sources?.paddle || {};
    const accounts = Array.isArray(source.accounts) ? source.accounts : [];
    if (accounts.length > 0) {
        return accounts.map((account, index) => normalizePaddleAccount(account, index, source, args));
    }
    const tokenEnv = String(source.tokenEnv || config?.secrets?.paddleTokenEnv || 'PADDLE_API_KEY').trim();
    return [
        {
            id: 'paddle',
            label: 'Paddle',
            tokenEnv,
            environment: String(source.environment || args.environment || 'live').trim().toLowerCase() || 'live',
        },
    ];
}
async function fetchPaddleMetric(baseUrl, pathname, args, tokenEnv) {
    const token = String(process.env[tokenEnv] || '').trim();
    if (!token) {
        throw new Error(`Missing ${tokenEnv}. Rerun the connector wizard and paste a Paddle API key from Developer Tools > Authentication v2.`);
    }
    const response = await fetch(buildUrl(baseUrl, pathname, args), {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            Authorization: `Bearer ${token}`,
            'Paddle-Version': '1',
            'User-Agent': 'openclaw-growth-paddle-exporter',
        },
    });
    const body = await response.text();
    if (!response.ok) {
        throw new Error(`Paddle ${pathname} failed with HTTP ${response.status}: ${body.slice(0, 500)}`);
    }
    return body.trim() ? JSON.parse(body) : {};
}
async function fetchOptionalMetric(baseUrl, pathname, key, args, warnings, tokenEnv) {
    try {
        return [key, await fetchPaddleMetric(baseUrl, pathname, args, tokenEnv)];
    }
    catch (error) {
        warnings.push(`${key}: ${error instanceof Error ? error.message : String(error)}`);
        return [key, null];
    }
}
async function fetchAccountSummary(args, account) {
    const environment = ['live', 'sandbox'].includes(account.environment) ? account.environment : args.environment;
    const baseUrl = paddleBaseUrl(environment);
    const warnings = [];
    const pairs = await Promise.all([
        fetchOptionalMetric(baseUrl, '/metrics/revenue', 'revenue', args, warnings, account.tokenEnv),
        fetchOptionalMetric(baseUrl, '/metrics/monthly-recurring-revenue', 'monthlyRecurringRevenue', args, warnings, account.tokenEnv),
        fetchOptionalMetric(baseUrl, '/metrics/active-subscribers', 'activeSubscribers', args, warnings, account.tokenEnv),
        fetchOptionalMetric(baseUrl, '/metrics/refunds', 'refunds', args, warnings, account.tokenEnv),
        fetchOptionalMetric(baseUrl, '/metrics/chargebacks', 'chargebacks', args, warnings, account.tokenEnv),
        fetchOptionalMetric(baseUrl, '/metrics/checkout-conversion', 'checkoutConversion', args, warnings, account.tokenEnv),
    ]);
    const metrics = Object.fromEntries(pairs);
    return {
        ...account,
        environment,
        window: `${args.from}_${args.to}`,
        metrics,
        warnings,
        maxSignals: args.maxSignals,
    };
}
async function main() {
    await loadOpenClawGrowthSecrets();
    const args = parseArgs(process.argv.slice(2));
    const accounts = await resolvePaddleAccounts(args);
    const accountSummaries = await Promise.all(accounts.map((account) => fetchAccountSummary(args, account)));
    const summary = accountSummaries.length > 1
        ? buildPaddleSummary({ accounts: accountSummaries, window: `${args.from}_${args.to}`, maxSignals: args.maxSignals })
        : buildPaddleSummary(accountSummaries[0]);
    await writeJsonOutput(args.out, summary);
}
main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
});
