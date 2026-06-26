#!/usr/bin/env node
import { existsSync, promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createSign } from 'node:crypto';
import { classifyServiceKind, getActionMode, getAllSourceEntries, getDefaultSourceCommand, getGitHubActionNoun, getGitHubConnectionSummary, getGitHubRequirementText, shouldAutoCreateGitHubArtifact, } from './openclaw-growth-shared.mjs';
import { applyOpenClawSecretRefs, loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';
const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const DEFAULT_CONNECTION_TIMEOUT_MS = 15_000;
const ASC_COMMAND_SMOKE_TIMEOUT_MS = 120_000;
const RUNTIME_DIR = path.dirname(fileURLToPath(import.meta.url));
const ANALYTICSCLI_PACKAGE_SPEC = process.env.ANALYTICSCLI_CLI_PACKAGE || '@analyticscli/cli';
const ANALYTICSCLI_NPM_PREFIX = process.env.ANALYTICSCLI_NPM_PREFIX ||
    (process.env.HOME ? path.join(process.env.HOME, '.local') : path.join(process.cwd(), '.analyticscli-npm'));
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
const SUPPORTED_CONNECTORS = [
    'analytics',
    'github',
    'asc',
    'revenuecat',
    'paddle',
    'seo',
    'sentry',
    'coolify',
    ...ACCOUNT_SIGNAL_CONNECTORS,
];
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
OpenClaw Growth Preflight

Validates local dependencies, configured sources, and required secrets.

Usage:
  node scripts/openclaw-growth-preflight.mjs [options]

Options:
  --config <file>        Config path (default: ${DEFAULT_CONFIG_PATH})
  --test-connections     Run live API/connector smoke checks for enabled channels
  --only-connectors <list>
                         Limit live checks to ${SUPPORTED_CONNECTORS.join(',')}
  --timeout-ms <ms>      Connection test timeout in milliseconds (default: ${DEFAULT_CONNECTION_TIMEOUT_MS})
  --progress-json        Emit machine-readable progress events on stderr
  --json                 Print JSON only (default)
  --help, -h             Show help
`);
    process.exit(exitCode);
}
function parseArgs(argv) {
    const args = {
        config: DEFAULT_CONFIG_PATH,
        json: true,
        progressJson: false,
        testConnections: false,
        onlyConnectors: [],
        timeoutMs: DEFAULT_CONNECTION_TIMEOUT_MS,
    };
    for (let i = 0; i < argv.length; i += 1) {
        const token = argv[i];
        const next = argv[i + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--config') {
            args.config = next || args.config;
            i += 1;
        }
        else if (token === '--test-connections') {
            args.testConnections = true;
        }
        else if (token === '--only-connectors') {
            args.onlyConnectors = parseConnectorList(next || '');
            i += 1;
        }
        else if (token === '--progress-json') {
            args.progressJson = true;
        }
        else if (token === '--timeout-ms') {
            const parsed = Number.parseInt(String(next || ''), 10);
            if (!Number.isFinite(parsed) || parsed <= 0) {
                printHelpAndExit(1, `Invalid value for --timeout-ms: ${String(next || '')}`);
            }
            args.timeoutMs = parsed;
            i += 1;
        }
        else if (token === '--json') {
            args.json = true;
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
function normalizeConnectorKey(value) {
    const normalized = String(value || '').trim().toLowerCase().replace(/[_\s]+/g, '-');
    if (!normalized)
        return null;
    if (normalized === 'all')
        return 'all';
    if (['analytics', 'analyticscli', 'product-analytics', 'events'].includes(normalized))
        return 'analytics';
    if (['github', 'gh', 'github-code', 'codebase', 'code-access'].includes(normalized))
        return 'github';
    if (['asc', 'asc-cli', 'app-store-connect', 'appstoreconnect', 'app-store'].includes(normalized))
        return 'asc';
    if (['revenuecat', 'revenue-cat', 'rc', 'revenuecat-mcp'].includes(normalized))
        return 'revenuecat';
    if (['paddle', 'paddle-billing', 'billing-metrics', 'web-revenue'].includes(normalized))
        return 'paddle';
    if (['seo', 'gsc', 'google-search-console', 'search-console', 'dataforseo', 'organic-search'].includes(normalized))
        return 'seo';
    if (['sentry', 'sentry-api', 'sentry-mcp', 'glitchtip', 'crashes', 'errors', 'crash-reporting'].includes(normalized))
        return 'sentry';
    if (['coolify', 'coolify-api', 'deployment', 'deployments', 'hosting', 'infra', 'infrastructure'].includes(normalized))
        return 'coolify';
    if (['stripe', 'stripe-billing', 'stripe-payments'].includes(normalized))
        return 'stripe';
    if (['lemonsqueezy', 'lemon-squeezy', 'lemon', 'ls'].includes(normalized))
        return 'lemonsqueezy';
    if (['adapty', 'adapty-paywalls', 'adapty-subscriptions'].includes(normalized))
        return 'adapty';
    if (['superwall', 'superwall-paywalls'].includes(normalized))
        return 'superwall';
    if (['google-play', 'google-play-console', 'play-console', 'play-store', 'android-store'].includes(normalized))
        return 'google-play';
    if (['datadog', 'datadog-rum', 'datadog-apm', 'datadog-logs'].includes(normalized))
        return 'datadog';
    if (['bugsnag', 'bugsnag-crashes'].includes(normalized))
        return 'bugsnag';
    if (['intercom', 'intercom-support'].includes(normalized))
        return 'intercom';
    if (['zendesk', 'zendesk-support'].includes(normalized))
        return 'zendesk';
    if (['apple-search-ads', 'apple-ads', 'asa', 'search-ads'].includes(normalized))
        return 'apple-search-ads';
    if (['google-ads', 'adwords'].includes(normalized))
        return 'google-ads';
    if (['meta-ads', 'facebook-ads', 'instagram-ads', 'fb-ads'].includes(normalized))
        return 'meta-ads';
    if (['tiktok-ads', 'tiktok-business', 'tiktok-business-api'].includes(normalized))
        return 'tiktok-ads';
    if (['vercel', 'vercel-deployments', 'vercel-hosting'].includes(normalized))
        return 'vercel';
    if (['cloudflare', 'cf', 'cloudflare-workers', 'cloudflare-pages'].includes(normalized))
        return 'cloudflare';
    if (['resend', 'resend-email'].includes(normalized))
        return 'resend';
    if (['customerio', 'customer-io', 'customer.io', 'cio'].includes(normalized))
        return 'customerio';
    if (['mailchimp', 'mailchimp-marketing'].includes(normalized))
        return 'mailchimp';
    if (['appfollow', 'app-follow'].includes(normalized))
        return 'appfollow';
    if (['apptweak', 'app-tweak'].includes(normalized))
        return 'apptweak';
    if (['linear', 'linear-issues', 'linear-planning'].includes(normalized))
        return 'linear';
    if (['postiz', 'postiz-api', 'social-publishing', 'social-scheduler'].includes(normalized))
        return 'postiz';
    return null;
}
function parseConnectorList(value) {
    if (!String(value || '').trim())
        return [];
    const connectors = new Set();
    for (const entry of String(value).split(',')) {
        const connector = normalizeConnectorKey(entry);
        if (!connector) {
            printHelpAndExit(1, `Unknown connector: ${entry.trim()}. Use ${SUPPORTED_CONNECTORS.join(', ')}, or all.`);
        }
        if (connector === 'all') {
            SUPPORTED_CONNECTORS.forEach((supported) => connectors.add(supported));
        }
        else {
            connectors.add(connector);
        }
    }
    return [...connectors];
}
function shellQuote(value) {
    if (/^[a-zA-Z0-9_./:-]+$/.test(String(value))) {
        return String(value);
    }
    return `'${String(value).replace(/'/g, `'\\''`)}'`;
}
function resolveRuntimeScriptPath(scriptName) {
    const candidates = [
        path.join(RUNTIME_DIR, scriptName),
        path.join(process.cwd(), 'scripts', scriptName),
        path.join(process.cwd(), 'skills', 'growth-engineer', 'scripts', scriptName),
        path.join(process.cwd(), 'skills', 'openclaw-growth-engineer', 'scripts', scriptName),
    ];
    for (const candidate of candidates) {
        if (existsSync(candidate))
            return candidate;
    }
    return path.join(RUNTIME_DIR, scriptName);
}
function nodeRuntimeScriptCommand(scriptName) {
    return `node ${shellQuote(resolveRuntimeScriptPath(scriptName))}`;
}
function replaceLegacyRuntimeScriptCommand(command) {
    const trimmed = String(command || '').trim();
    if (!trimmed)
        return trimmed;
    return trimmed
        .replace(/^node\s+scripts\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-start\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs|openclaw-growth-engineer\.mjs)(?=\s|$)/, (_match, scriptName) => nodeRuntimeScriptCommand(scriptName))
        .replace(/^node\s+(['"]?)(?:\S*\/)?node_modules\/@analyticscli\/growth-engineer\/dist\/runtime\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-start\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs|openclaw-growth-engineer\.mjs)\1(?=\s|$)/, (_match, _quote, scriptName) => nodeRuntimeScriptCommand(scriptName));
}
function commandHasConfigArg(command) {
    return /(?:^|\s)--config(?:=|\s|$)/.test(String(command || ''));
}
function commandIsBuiltinExporter(command) {
    return /(?:^|\s)(?:node\s+)?(?:\S*\/)?(?:export-analytics-summary|export-revenuecat-summary|export-paddle-summary|export-seo-summary|export-sentry-summary|export-coolify-summary|export-asc-summary)\.mjs(?:\s|$)/.test(String(command || ''));
}
function commandSupportsActiveConfig(command) {
    return /(?:^|\s)(?:node\s+)?(?:\S*\/)?(?:export-paddle-summary|export-sentry-summary|export-coolify-summary)\.mjs(?:\s|$)/.test(String(command || ''));
}
function withActiveConfigArg(command, configPath) {
    const trimmed = String(command || '').trim();
    if (!trimmed || !configPath || !commandIsBuiltinExporter(trimmed)) {
        return trimmed;
    }
    if (!commandSupportsActiveConfig(trimmed)) {
        return trimmed
            .replace(/(^|\s)--config=(?:"[^"]*"|'[^']*'|\S+)/, '$1')
            .replace(/(^|\s)--config\s+(?:"[^"]*"|'[^']*'|\S+)/, '$1')
            .trim();
    }
    if (commandHasConfigArg(trimmed)) {
        return trimmed
            .replace(/(^|\s)--config=(?:"[^"]*"|'[^']*'|\S+)/, `$1--config ${shellQuote(configPath)}`)
            .replace(/(^|\s)--config\s+(?:"[^"]*"|'[^']*'|\S+)/, `$1--config ${shellQuote(configPath)}`);
    }
    return `${trimmed} --config ${shellQuote(configPath)}`;
}
function resolveShellCommand() {
    const candidates = [
        process.env.OPENCLAW_SHELL,
        process.env.SHELL,
        '/bin/zsh',
        '/bin/bash',
        '/usr/bin/bash',
        '/bin/sh',
        '/usr/bin/sh',
    ].filter((value) => typeof value === 'string' && value.trim().length > 0);
    for (const candidate of candidates) {
        if (existsSync(candidate)) {
            return candidate;
        }
    }
    return 'sh';
}
function hardenUnattendedShellCommand(command) {
    return String(command || '').replace(/(^|[;&|]\s*)sudo(?!\s+-n(?:\s|$))(?=\s|$)/g, '$1sudo -n');
}
function runShell(command, options = {}) {
    return new Promise((resolve) => {
        const child = spawn(resolveShellCommand(), ['-c', hardenUnattendedShellCommand(command)], {
            stdio: ['ignore', 'pipe', 'pipe'],
            cwd: options.cwd,
            env: {
                ...process.env,
                ...(options.env || {}),
                DEBIAN_FRONTEND: 'noninteractive',
                SUDO_ASKPASS: '/bin/false',
                SUDO_PROMPT: '',
            },
        });
        let stdout = '';
        let stderr = '';
        let settled = false;
        const timeoutMs = options.timeoutMs ?? 60_000;
        const timer = setTimeout(() => {
            if (settled)
                return;
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
            stderr += String(chunk);
        });
        child.on('close', (code) => {
            if (settled)
                return;
            settled = true;
            clearTimeout(timer);
            resolve({
                ok: code === 0,
                code,
                stdout,
                stderr,
            });
        });
    });
}
async function commandExists(commandName) {
    const result = await runShell(`command -v ${shellQuote(commandName)} >/dev/null 2>&1`);
    return result.ok;
}
async function resolveCommandPath(commandName) {
    const result = await runShell(`command -v ${shellQuote(commandName)}`);
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
    const profiles = ['.profile', '.bashrc', '.bash_profile', '.zshrc', '.zprofile'].map((name) => path.join(process.env.HOME, name));
    let wrote = false;
    for (const profile of profiles) {
        let current = '';
        try {
            current = await fs.readFile(profile, 'utf8');
        }
        catch {
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
            command: 'for f in "$HOME/.bash_profile" "$HOME/.bashrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
        },
        {
            shell: '/usr/bin/bash',
            command: 'for f in "$HOME/.bash_profile" "$HOME/.bashrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
        },
        {
            shell: '/bin/zsh',
            command: 'for f in "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
        },
        {
            shell: '/usr/bin/zsh',
            command: 'for f in "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
        },
        {
            shell: '/bin/sh',
            command: '[ -f "$HOME/.profile" ] && . "$HOME/.profile" >/dev/null 2>&1 || true; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
        },
        {
            shell: '/usr/bin/sh',
            command: '[ -f "$HOME/.profile" ] && . "$HOME/.profile" >/dev/null 2>&1 || true; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1',
        },
    ];
    for (const probe of probes) {
        if (!(await fileExists(probe.shell))) {
            continue;
        }
        const result = await runShell(`env HOME=${shellQuote(process.env.HOME)} PATH=${shellQuote(cleanPath)} ${shellQuote(probe.shell)} -lc ${shellQuote(probe.command)}`);
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
        return beforePath
            ? {
                ok: true,
                detail: `analyticscli binary found at ${beforePath}; npm unavailable, so package update was skipped`,
            }
            : {
                ok: false,
                detail: `analyticscli binary missing and npm is unavailable; install ${ANALYTICSCLI_PACKAGE_SPEC}`,
            };
    }
    const globalInstall = await runShell(`npm install -g ${shellQuote(ANALYTICSCLI_PACKAGE_SPEC)}`);
    if (!globalInstall.ok) {
        const installOutput = `${globalInstall.stderr}\n${globalInstall.stdout}`;
        if (isPermissionFailure(installOutput)) {
            await fs.mkdir(ANALYTICSCLI_NPM_PREFIX, { recursive: true });
            const localInstall = await runShell(`npm install -g --prefix ${shellQuote(ANALYTICSCLI_NPM_PREFIX)} ${shellQuote(ANALYTICSCLI_PACKAGE_SPEC)}`);
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
        }
        else {
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
        const helpCheck = await runShell('analyticscli --help >/dev/null 2>&1');
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
function parseCommandHead(command) {
    if (!command || typeof command !== 'string')
        return null;
    const trimmed = command.trim();
    if (!trimmed)
        return null;
    const parts = trimmed.split(/\s+/).filter(Boolean);
    return parts.length > 0 ? parts[0] : null;
}
function isPortableCommandDefault(sourceName, command) {
    const expected = getDefaultSourceCommand(sourceName);
    if (!expected)
        return false;
    const trimmed = String(command || '').trim();
    return trimmed.startsWith(expected) || replaceLegacyRuntimeScriptCommand(trimmed) !== trimmed;
}
function truncate(value, max = 240) {
    const text = String(value || '');
    if (text.length <= max)
        return text;
    return `${text.slice(0, max)}…`;
}
function base64UrlJson(value) {
    return Buffer.from(JSON.stringify(value)).toString('base64url');
}
async function buildAscApiJwt() {
    const keyId = String(process.env.ASC_KEY_ID || '').trim();
    const issuerId = String(process.env.ASC_ISSUER_ID || '').trim();
    const privateKeyPath = String(process.env.ASC_PRIVATE_KEY_PATH || '').trim();
    const privateKey = String(process.env.ASC_PRIVATE_KEY || '').trim() ||
        (String(process.env.ASC_PRIVATE_KEY_B64 || '').trim()
            ? Buffer.from(String(process.env.ASC_PRIVATE_KEY_B64 || '').trim(), 'base64').toString('utf8')
            : privateKeyPath
                ? await fs.readFile(privateKeyPath, 'utf8')
                : '');
    if (!keyId || !issuerId || !privateKey)
        return null;
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
async function testAscAppsListDirect(timeoutMs) {
    const token = await buildAscApiJwt();
    if (!token)
        return { ok: false, detail: 'ASC API credentials are incomplete' };
    try {
        const response = await fetch('https://api.appstoreconnect.apple.com/v1/apps?limit=200', {
            headers: {
                Accept: 'application/json',
                Authorization: `Bearer ${token}`,
            },
            signal: AbortSignal.timeout(timeoutMs),
        });
        const text = await response.text();
        let payload = null;
        try {
            payload = text ? JSON.parse(text) : null;
        }
        catch {
            payload = { raw: text };
        }
        if (!response.ok) {
            const detail = Array.isArray(payload?.errors)
                ? payload.errors.map((entry) => entry?.detail || entry?.title || entry?.code).filter(Boolean).join('; ')
                : text;
            return { ok: false, detail: truncate(`direct Apple API returned HTTP ${response.status}: ${detail}`) };
        }
        const count = Array.isArray(payload?.data) ? payload.data.length : 0;
        return {
            ok: true,
            detail: `direct Apple API apps list returned JSON${count ? ` (${count} app${count === 1 ? '' : 's'})` : ''}`,
        };
    }
    catch (error) {
        return { ok: false, detail: truncate(error?.message || String(error)) };
    }
}
function isAscAppListDeferredError(detail) {
    const normalized = String(detail || '').toLowerCase();
    if (!normalized)
        return false;
    if (normalized.includes('credentials are incomplete') ||
        normalized.includes('401') ||
        normalized.includes('403') ||
        normalized.includes('forbidden') ||
        normalized.includes('unauthorized') ||
        normalized.includes('not authorized') ||
        normalized.includes('invalid issuer') ||
        normalized.includes('invalid token')) {
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
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
function isTransientNetworkFailure(value) {
    return /NETWORK_ERROR|fetch failed|tlsv1 alert|SSL routines|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|socket hang up|network timeout|Temporary failure/i.test(String(value || ''));
}
async function readJson(filePath) {
    const raw = await fs.readFile(filePath, 'utf8');
    return JSON.parse(raw);
}
async function fileExists(filePath) {
    try {
        await fs.access(filePath);
        return true;
    }
    catch {
        return false;
    }
}
function addCheck(checks, name, ok, detail, severity = 'fail') {
    checks.push({
        name,
        status: ok ? 'pass' : severity,
        detail,
    });
}
function emitProgress(enabled, event) {
    if (!enabled)
        return;
    process.stderr.write(`OPENCLAW_PROGRESS ${JSON.stringify(event)}\n`);
}
function checkSliceStatus(checks, startIndex) {
    const slice = checks.slice(startIndex);
    if (slice.some((check) => check.status === 'fail'))
        return 'fail';
    if (slice.some((check) => check.status === 'warn'))
        return 'warn';
    return 'pass';
}
async function runProgressGroup({ checks, progressJson, key, label, detail, run }) {
    emitProgress(progressJson, { phase: 'start', key, label, detail });
    const startIndex = checks.length;
    try {
        await run();
    }
    finally {
        emitProgress(progressJson, {
            phase: 'finish',
            key,
            label,
            detail,
            status: checkSliceStatus(checks, startIndex),
        });
    }
}
function scheduleProgressGroup(tasks, checks, progressJson, { key, label, detail, run }) {
    tasks.push((async () => {
        const groupChecks = [];
        await runProgressGroup({
            checks: groupChecks,
            progressJson,
            key,
            label,
            detail,
            run: () => run(groupChecks),
        });
        checks.push(...groupChecks);
    })());
}
function getSecretName(config, key, fallback) {
    const value = config?.secrets?.[key];
    return typeof value === 'string' && value.trim() ? value.trim() : fallback;
}
function sourceEnabled(config, sourceName) {
    return Boolean(config?.sources?.[sourceName] && config.sources[sourceName].enabled !== false);
}
function isConfiguredGitHubRepo(value) {
    const repo = String(value || '').trim();
    return Boolean(repo && repo !== 'owner/repo' && /^[^/\s]+\/[^/\s]+$/.test(repo));
}
async function fetchWithTimeout(url, options, timeoutMs) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
        });
        const body = await response.text();
        return { ok: response.ok, status: response.status, body };
    }
    finally {
        clearTimeout(timer);
    }
}
async function testAnalyticsConnection(analyticsToken, analyticsTokenEnv, timeoutMs) {
    const hasCli = await commandExists('analyticscli');
    if (!hasCli) {
        return {
            ok: false,
            detail: 'analyticscli binary missing',
        };
    }
    const runCheck = () => runShell('analyticscli projects list --format json', {
        env: analyticsToken
            ? {
                [analyticsTokenEnv]: analyticsToken,
                ANALYTICSCLI_ACCESS_TOKEN: analyticsToken,
                ANALYTICSCLI_READONLY_TOKEN: analyticsToken,
            }
            : undefined,
        timeoutMs,
    });
    let result = await runCheck();
    let retried = false;
    if (!result.ok && isTransientNetworkFailure(result.stderr || result.stdout)) {
        retried = true;
        await sleep(1_500);
        result = await runCheck();
    }
    if (!result.ok) {
        return {
            ok: false,
            detail: truncate(`${retried ? 'transient network error persisted after retry: ' : ''}${result.stderr || `exit ${result.code}`}`),
        };
    }
    return {
        ok: true,
        detail: analyticsToken
            ? `analyticscli token auth check passed${retried ? ' after retry' : ''} (\`projects list\`)`
            : `analyticscli auth check passed${retried ? ' after retry' : ''} (\`projects list\`)`,
    };
}
async function testRevenueCatConnection(revenuecatToken, timeoutMs) {
    if (!revenuecatToken) {
        return {
            ok: false,
            detail: 'missing token',
        };
    }
    try {
        const response = await fetchWithTimeout('https://api.revenuecat.com/v2/projects?limit=1', {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                Authorization: `Bearer ${revenuecatToken}`,
            },
        }, timeoutMs);
        if (!response.ok) {
            return {
                ok: false,
                detail: `HTTP ${response.status}: ${truncate(response.body)}`,
            };
        }
        return {
            ok: true,
            detail: `HTTP ${response.status}`,
        };
    }
    catch (error) {
        return {
            ok: false,
            detail: error instanceof Error ? error.message : String(error),
        };
    }
}
async function testPaddleConnection(paddleToken, timeoutMs, environment = 'live') {
    if (!paddleToken) {
        return {
            ok: false,
            detail: 'missing token',
        };
    }
    const to = new Date().toISOString().slice(0, 10);
    const fromDate = new Date();
    fromDate.setUTCDate(fromDate.getUTCDate() - 2);
    const from = fromDate.toISOString().slice(0, 10);
    try {
        const baseUrl = String(environment || 'live').toLowerCase() === 'sandbox'
            ? 'https://sandbox-api.paddle.com'
            : 'https://api.paddle.com';
        const response = await fetchWithTimeout(`${baseUrl}/metrics/revenue?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                Authorization: `Bearer ${paddleToken}`,
                'Paddle-Version': '1',
            },
        }, timeoutMs);
        if (!response.ok) {
            return {
                ok: false,
                detail: `HTTP ${response.status}: ${truncate(response.body)}`,
            };
        }
        return {
            ok: true,
            detail: `HTTP ${response.status}`,
        };
    }
    catch (error) {
        return {
            ok: false,
            detail: error instanceof Error ? error.message : String(error),
        };
    }
}
function describeAnalyticsConnectionFailure(detail, analyticsTokenEnv, hasAnalyticsToken) {
    if (!hasAnalyticsToken) {
        return `AnalyticsCLI needs query access. Run \`npx -y @analyticscli/growth-engineer wizard --connectors analytics\`, create or copy a readonly CLI token in dash.analyticscli.com -> API Keys, and paste it into the local terminal wizard. Raw error: ${detail}`;
    }
    return `AnalyticsCLI connection failed with \`${analyticsTokenEnv}\` set. Verify that the pasted readonly CLI token is current and has project access. Raw error: ${detail}`;
}
async function testSentryConnection(sentryToken, timeoutMs, baseUrl = 'https://sentry.io') {
    if (!sentryToken) {
        return {
            ok: false,
            detail: 'missing token',
        };
    }
    try {
        const response = await fetchWithTimeout(`${String(baseUrl || 'https://sentry.io').replace(/\/$/, '')}/api/0/organizations/`, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                Authorization: `Bearer ${sentryToken}`,
            },
        }, timeoutMs);
        if (!response.ok) {
            return {
                ok: false,
                detail: `HTTP ${response.status}: ${truncate(response.body)}`,
            };
        }
        return {
            ok: true,
            detail: `HTTP ${response.status}`,
        };
    }
    catch (error) {
        return {
            ok: false,
            detail: error instanceof Error ? error.message : String(error),
        };
    }
}
function normalizeCoolifyBaseUrl(value) {
    const raw = String(value || '').trim().replace(/\/+$/, '');
    if (!raw)
        return '';
    return /^https?:\/\//i.test(raw) ? raw : `https://${raw}`;
}
function resolveCoolifyApiBaseUrl(baseUrl) {
    const normalized = normalizeCoolifyBaseUrl(baseUrl);
    if (!normalized)
        return '';
    if (/\/api\/v1$/i.test(normalized))
        return normalized;
    if (/\/api$/i.test(normalized))
        return `${normalized}/v1`;
    return `${normalized}/api/v1`;
}
async function testCoolifyConnection(coolifyToken, timeoutMs, baseUrl) {
    if (!coolifyToken) {
        return {
            ok: false,
            detail: 'missing token',
        };
    }
    const apiBaseUrl = resolveCoolifyApiBaseUrl(baseUrl);
    if (!apiBaseUrl) {
        return {
            ok: false,
            detail: 'missing base URL',
        };
    }
    try {
        const response = await fetchWithTimeout(`${apiBaseUrl}/applications?limit=1`, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                Authorization: `Bearer ${coolifyToken}`,
            },
        }, timeoutMs);
        if (!response.ok) {
            return {
                ok: false,
                detail: `HTTP ${response.status}: ${truncate(response.body)}`,
            };
        }
        return {
            ok: true,
            detail: `HTTP ${response.status}`,
        };
    }
    catch (error) {
        return {
            ok: false,
            detail: error instanceof Error ? error.message : String(error),
        };
    }
}
function normalizeSentryAccounts(config, sentryTokenEnv) {
    const sentrySource = config?.sources?.sentry;
    const accounts = Array.isArray(sentrySource?.accounts) ? sentrySource.accounts : [];
    if (accounts.length > 0) {
        return accounts.map((account, index) => ({
            key: String(account?.id || account?.key || account?.label || `sentry_${index + 1}`)
                .trim()
                .replace(/[^a-zA-Z0-9._-]+/g, '_'),
            label: String(account?.label || account?.name || account?.id || `Sentry ${index + 1}`).trim(),
            tokenEnv: String(account?.tokenEnv || account?.token_env || account?.secretEnv || sentryTokenEnv).trim(),
            baseUrl: String(account?.baseUrl || account?.base_url || account?.url || 'https://sentry.io').trim(),
            org: String(account?.org || account?.organization || '').trim(),
            projects: Array.isArray(account?.projects)
                ? account.projects.map((project) => String(typeof project === 'string' ? project : project?.project || project?.slug || '').trim()).filter(Boolean)
                : account?.project
                    ? [String(account.project).trim()].filter(Boolean)
                    : [],
            environment: String(account?.environment || process.env.SENTRY_ENVIRONMENT || 'production').trim(),
        }));
    }
    return [
        {
            key: 'sentry',
            label: 'Sentry',
            tokenEnv: sentryTokenEnv,
            baseUrl: String(process.env.SENTRY_BASE_URL || 'https://sentry.io').trim(),
            org: String(process.env.SENTRY_ORG || '').trim(),
            projects: String(process.env.SENTRY_PROJECT || '').trim() ? [String(process.env.SENTRY_PROJECT).trim()] : [],
            environment: String(process.env.SENTRY_ENVIRONMENT || 'production').trim(),
        },
    ];
}
function normalizePaddleAccounts(config, paddleTokenEnv) {
    const paddleSource = config?.sources?.paddle;
    const accounts = Array.isArray(paddleSource?.accounts) ? paddleSource.accounts : [];
    if (accounts.length > 0) {
        return accounts.map((account, index) => ({
            key: String(account?.id || account?.key || account?.label || `paddle_${index + 1}`)
                .trim()
                .replace(/[^a-zA-Z0-9._-]+/g, '_'),
            label: String(account?.label || account?.name || account?.id || `Paddle ${index + 1}`).trim(),
            tokenEnv: String(account?.tokenEnv || account?.token_env || account?.secretEnv || (index === 0 ? paddleTokenEnv : `PADDLE_API_KEY_${index + 1}`)).trim(),
            environment: String(account?.environment || paddleSource?.environment || 'live').trim().toLowerCase() || 'live',
        }));
    }
    return [
        {
            key: 'paddle',
            label: 'Paddle',
            tokenEnv: String(paddleSource?.tokenEnv || paddleTokenEnv).trim(),
            environment: String(paddleSource?.environment || 'live').trim().toLowerCase() || 'live',
        },
    ];
}
function describeSentryAccountTarget(account) {
    const parts = [
        account.label,
        `id=${account.key}`,
        `baseUrl=${account.baseUrl || 'https://sentry.io'}`,
        account.org ? `org=${account.org}` : null,
        account.projects?.length ? `projects=${account.projects.join(',')}` : null,
        account.environment ? `environment=${account.environment}` : null,
        account.tokenEnv ? `tokenEnv=${account.tokenEnv}` : null,
    ].filter(Boolean);
    return parts.join(' ');
}
async function testGitHubConnection(githubToken, githubRepo, timeoutMs, actionMode) {
    if (!githubToken) {
        return {
            ok: false,
            detail: 'missing token',
        };
    }
    try {
        const response = await fetchWithTimeout('https://api.github.com/user', {
            method: 'GET',
            headers: {
                Accept: 'application/vnd.github+json',
                Authorization: `Bearer ${githubToken}`,
            },
        }, timeoutMs);
        if (!response.ok) {
            return {
                ok: false,
                detail: `HTTP ${response.status}: ${truncate(response.body)}`,
            };
        }
        const repo = String(githubRepo || '').trim();
        if (!repo) {
            return {
                ok: false,
                detail: 'project.githubRepo is missing',
            };
        }
        const repoResponse = await fetchWithTimeout(`https://api.github.com/repos/${repo}`, {
            method: 'GET',
            headers: {
                Accept: 'application/vnd.github+json',
                Authorization: `Bearer ${githubToken}`,
            },
        }, timeoutMs);
        if (!repoResponse.ok) {
            return {
                ok: false,
                detail: `repo access check failed (HTTP ${repoResponse.status}: ${truncate(repoResponse.body)})`,
            };
        }
        const artifactPath = actionMode === 'pull_request'
            ? `pulls?state=all&per_page=1`
            : `issues?state=all&per_page=1`;
        const artifactsResponse = await fetchWithTimeout(`https://api.github.com/repos/${repo}/${artifactPath}`, {
            method: 'GET',
            headers: {
                Accept: 'application/vnd.github+json',
                Authorization: `Bearer ${githubToken}`,
            },
        }, timeoutMs);
        if (!artifactsResponse.ok) {
            return {
                ok: false,
                detail: `${getGitHubActionNoun(actionMode)} API check failed (HTTP ${artifactsResponse.status}: ${truncate(artifactsResponse.body)})`,
            };
        }
        return {
            ok: true,
            detail: `${getGitHubConnectionSummary(actionMode)} (${getGitHubRequirementText(actionMode)})`,
        };
    }
    catch (error) {
        return {
            ok: false,
            detail: error instanceof Error ? error.message : String(error),
        };
    }
}
function getProjectCommandCwd(config) {
    const repoRoot = String(config?.project?.repoRoot || '').trim();
    return repoRoot ? path.resolve(repoRoot) : process.cwd();
}
async function testCommandSourceJson(command, cwd = process.cwd(), options = {}) {
    let result = await runShell(command, { cwd, timeoutMs: options.timeoutMs });
    let retried = false;
    if (!result.ok && isTransientNetworkFailure(result.stderr || result.stdout)) {
        retried = true;
        await sleep(1_500);
        result = await runShell(command, { cwd, timeoutMs: options.timeoutMs });
    }
    if (!result.ok) {
        return {
            ok: false,
            detail: truncate(`${retried ? 'transient network error persisted after retry: ' : ''}${result.stderr || `exit ${result.code}`}`),
        };
    }
    try {
        JSON.parse(result.stdout);
    }
    catch {
        return {
            ok: false,
            detail: 'command succeeded but returned non-JSON output',
        };
    }
    return {
        ok: true,
        detail: retried ? 'command returned JSON after retry' : 'command returned JSON',
    };
}
async function testAscCliAppsList(timeoutMs) {
    const result = await runShell('asc apps list --output json', {
        timeoutMs: Math.max(timeoutMs, ASC_COMMAND_SMOKE_TIMEOUT_MS),
        env: {
            ASC_BYPASS_KEYCHAIN: process.env.ASC_BYPASS_KEYCHAIN || '1',
            ASC_TIMEOUT_SECONDS: process.env.ASC_TIMEOUT_SECONDS || '120',
        },
    });
    if (!result.ok) {
        const fallback = await testAscAppsListDirect(Math.max(timeoutMs, ASC_COMMAND_SMOKE_TIMEOUT_MS));
        if (fallback.ok)
            return fallback;
        const detail = `${result.stderr || `exit ${result.code}`} Direct Apple API fallback also failed: ${fallback.detail}`;
        if (isAscAppListDeferredError(detail)) {
            return {
                ok: true,
                detail: 'ASC app listing is temporarily unavailable from Apple; credentials are saved and app discovery will retry later',
            };
        }
        return {
            ok: false,
            detail: truncate(detail),
        };
    }
    try {
        const payload = JSON.parse(result.stdout);
        const count = Array.isArray(payload?.data) ? payload.data.length : Array.isArray(payload) ? payload.length : 0;
        return {
            ok: true,
            detail: `asc apps list returned JSON${count ? ` (${count} app${count === 1 ? '' : 's'})` : ''}`,
        };
    }
    catch {
        return {
            ok: false,
            detail: 'asc apps list succeeded but returned non-JSON output',
        };
    }
}
function onlyAllows(onlyConnectors, connector) {
    return !Array.isArray(onlyConnectors) || onlyConnectors.length === 0 || onlyConnectors.includes(connector);
}
async function runConnectionChecks({ checks, config, configPath, timeoutMs, progressJson = false, onlyConnectors = [] }) {
    const tasks = [];
    const analyticsTokenEnv = getSecretName(config, 'analyticsTokenEnv', 'ANALYTICSCLI_ACCESS_TOKEN');
    const revenuecatTokenEnv = getSecretName(config, 'revenuecatTokenEnv', 'REVENUECAT_API_KEY');
    const paddleTokenEnv = getSecretName(config, 'paddleTokenEnv', 'PADDLE_API_KEY');
    const gscTokenEnv = getSecretName(config, 'gscTokenEnv', 'GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN');
    const sentryTokenEnv = getSecretName(config, 'sentryTokenEnv', 'SENTRY_AUTH_TOKEN');
    const coolifyTokenEnv = getSecretName(config, 'coolifyTokenEnv', 'COOLIFY_API_TOKEN');
    const feedbackTokenEnv = getSecretName(config, 'feedbackTokenEnv', 'FEEDBACK_API_TOKEN');
    const githubTokenEnv = getSecretName(config, 'githubTokenEnv', 'GITHUB_TOKEN');
    const githubRepo = isConfiguredGitHubRepo(config?.project?.githubRepo)
        ? String(config.project.githubRepo).trim()
        : '';
    const actionMode = getActionMode(config);
    const requiresGitHubDelivery = shouldAutoCreateGitHubArtifact(config);
    const commandCwd = getProjectCommandCwd(config);
    const analyticsSource = config.sources?.analytics;
    if (onlyAllows(onlyConnectors, 'analytics')) {
        scheduleProgressGroup(tasks, checks, progressJson, {
            key: 'analytics',
            label: 'AnalyticsCLI',
            detail: 'token auth + readonly query',
            run: async (groupChecks) => {
                if (sourceEnabled(config, 'analytics')) {
                    const analyticsToken = process.env.ANALYTICSCLI_ACCESS_TOKEN || process.env[analyticsTokenEnv] || process.env.ANALYTICSCLI_READONLY_TOKEN || '';
                    const hasAnalyticsToken = Boolean(analyticsToken);
                    const analyticsConnection = await testAnalyticsConnection(analyticsToken, analyticsTokenEnv, timeoutMs);
                    addCheck(groupChecks, 'connection:analytics', analyticsConnection.ok, analyticsConnection.ok
                        ? analyticsConnection.detail
                        : describeAnalyticsConnectionFailure(analyticsConnection.detail, analyticsTokenEnv, hasAnalyticsToken), analyticsConnection.ok ? 'pass' : analyticsSource?.mode === 'command' ? 'fail' : 'warn');
                    if (analyticsSource?.mode === 'command') {
                        const command = withActiveConfigArg(replaceLegacyRuntimeScriptCommand(String(analyticsSource.command || '').trim()), configPath);
                        if (!command) {
                            addCheck(checks, 'connection:analytics-command', false, 'analytics source uses command mode but no command configured');
                        }
                        else {
                            const commandCheck = await testCommandSourceJson(command, commandCwd);
                            addCheck(groupChecks, 'connection:analytics-command', commandCheck.ok, commandCheck.ok
                                ? 'analytics command smoke test passed'
                                : `analytics command smoke test failed (${commandCheck.detail})`);
                        }
                    }
                }
                else {
                    addCheck(groupChecks, 'connection:analytics', true, 'source disabled');
                }
            },
        });
    }
    const revenuecatSource = config.sources?.revenuecat;
    if (onlyAllows(onlyConnectors, 'revenuecat')) {
        scheduleProgressGroup(tasks, checks, progressJson, {
            key: 'revenuecat',
            label: 'RevenueCat',
            detail: 'API key auth + project read',
            run: async (groupChecks) => {
                if (sourceEnabled(config, 'revenuecat')) {
                    const token = process.env[revenuecatTokenEnv] || '';
                    if (!token) {
                        addCheck(groupChecks, `connection:revenuecat`, false, `${revenuecatTokenEnv} missing (required for live RevenueCat API test)`, revenuecatSource?.mode === 'command' ? 'fail' : 'warn');
                    }
                    else {
                        const revenuecatConnection = await testRevenueCatConnection(token, timeoutMs);
                        addCheck(groupChecks, 'connection:revenuecat', revenuecatConnection.ok, revenuecatConnection.ok
                            ? `RevenueCat auth check passed (${revenuecatConnection.detail})`
                            : `RevenueCat auth check failed (${revenuecatConnection.detail})`);
                    }
                }
                else {
                    addCheck(groupChecks, 'connection:revenuecat', true, 'source disabled');
                }
            },
        });
    }
    const paddleSource = config.sources?.paddle;
    if (onlyAllows(onlyConnectors, 'paddle')) {
        scheduleProgressGroup(tasks, checks, progressJson, {
            key: 'paddle',
            label: 'Paddle',
            detail: 'metrics API auth + revenue read',
            run: async (groupChecks) => {
                if (sourceEnabled(config, 'paddle')) {
                    const paddleAccounts = normalizePaddleAccounts(config, paddleTokenEnv);
                    for (const account of paddleAccounts) {
                        const token = process.env[account.tokenEnv] || '';
                        const checkName = paddleAccounts.length > 1 ? `connection:paddle:${account.key}` : 'connection:paddle';
                        if (!token) {
                            addCheck(groupChecks, checkName, false, `${account.tokenEnv} missing for ${account.label} (required for Paddle metrics API test)`, paddleSource?.mode === 'command' ? 'fail' : 'warn');
                            continue;
                        }
                        const paddleConnection = await testPaddleConnection(token, timeoutMs, account.environment);
                        addCheck(groupChecks, checkName, paddleConnection.ok, paddleConnection.ok
                            ? `Paddle metrics auth check passed for ${account.label} (${paddleConnection.detail})`
                            : `Paddle metrics auth check failed for ${account.label} (${paddleConnection.detail})`);
                    }
                    if (paddleSource?.mode === 'command') {
                        const command = withActiveConfigArg(replaceLegacyRuntimeScriptCommand(String(paddleSource.command || '').trim()), configPath);
                        if (!command) {
                            addCheck(groupChecks, 'connection:paddle-command', false, 'paddle source uses command mode but no command configured');
                        }
                        else {
                            const commandCheck = await testCommandSourceJson(`${command} --last 2d --max-signals 1`, commandCwd);
                            addCheck(groupChecks, 'connection:paddle-command', commandCheck.ok, commandCheck.ok
                                ? 'Paddle command smoke test passed'
                                : `Paddle command smoke test failed (${commandCheck.detail})`);
                        }
                    }
                }
                else {
                    addCheck(groupChecks, 'connection:paddle', true, 'source disabled');
                }
            },
        });
    }
    const seoSource = config.sources?.seo;
    if (onlyAllows(onlyConnectors, 'seo')) {
        scheduleProgressGroup(tasks, checks, progressJson, {
            key: 'seo',
            label: 'SEO / GSC',
            detail: 'Search Console auth or CSV/DataForSEO config',
            run: async (groupChecks) => {
                if (sourceEnabled(config, 'seo')) {
                    const hasGscCredential = Boolean(process.env[gscTokenEnv] ||
                        process.env.GSC_ACCESS_TOKEN ||
                        process.env.GOOGLE_APPLICATION_CREDENTIALS ||
                        process.env.GSC_SERVICE_ACCOUNT_JSON ||
                        process.env.GOOGLE_SERVICE_ACCOUNT_JSON);
                    addCheck(groupChecks, 'connection:seo:gsc-credentials', hasGscCredential || seoSource?.mode !== 'command', hasGscCredential
                        ? 'GSC credential is configured'
                        : 'GSC credential missing; command can still run in CSV-only mode if --gsc-csv/--csv is configured', hasGscCredential ? 'pass' : 'warn');
                    addCheck(groupChecks, 'connection:seo:gsc-site', true, process.env.GSC_SITE_URL || seoSource?.siteUrl || seoSource?.site_url
                        ? 'GSC site/property is pinned intentionally'
                        : 'no GSC site/property pinned; exporter will list and query all verified Search Console properties', 'pass');
                    if (seoSource?.mode === 'command') {
                        const command = withActiveConfigArg(replaceLegacyRuntimeScriptCommand(String(seoSource.command || '').trim()), configPath);
                        if (!command) {
                            addCheck(groupChecks, 'connection:seo-command', false, 'seo source uses command mode but no command configured');
                        }
                        else {
                            const commandCheck = await testCommandSourceJson(`${command} --row-limit 5 --max-signals 1`, commandCwd);
                            addCheck(groupChecks, 'connection:seo-command', commandCheck.ok, commandCheck.ok
                                ? 'SEO command smoke test passed'
                                : `SEO command smoke test failed (${commandCheck.detail})`, hasGscCredential || /--csv|--gsc-csv/.test(command) ? 'fail' : 'warn');
                        }
                    }
                }
                else {
                    addCheck(groupChecks, 'connection:seo', true, 'source disabled');
                }
            },
        });
    }
    const sentrySource = config.sources?.sentry;
    if (onlyAllows(onlyConnectors, 'sentry')) {
        scheduleProgressGroup(tasks, checks, progressJson, {
            key: 'sentry',
            label: 'Sentry / GlitchTip',
            detail: 'token/org API + project discovery',
            run: async (groupChecks) => {
                if (sourceEnabled(config, 'sentry')) {
                    const sentryAccounts = normalizeSentryAccounts(config, sentryTokenEnv);
                    for (const account of sentryAccounts) {
                        const token = process.env[account.tokenEnv] || '';
                        const checkName = sentryAccounts.length > 1 ? `connection:sentry:${account.key}` : 'connection:sentry';
                        const accountTarget = describeSentryAccountTarget(account);
                        if (!token) {
                            addCheck(groupChecks, checkName, false, `${account.tokenEnv} missing (required for live Sentry API test for ${accountTarget})`, sentrySource?.mode === 'command' ? 'fail' : 'warn');
                            continue;
                        }
                        const sentryConnection = await testSentryConnection(token, timeoutMs, account.baseUrl);
                        addCheck(groupChecks, checkName, sentryConnection.ok, sentryConnection.ok
                            ? `${accountTarget} auth check passed (${sentryConnection.detail})`
                            : `${accountTarget} auth check failed (${sentryConnection.detail})`);
                    }
                    if (sentrySource?.mode === 'command') {
                        const command = withActiveConfigArg(replaceLegacyRuntimeScriptCommand(String(sentrySource.command || '').trim()), configPath);
                        if (!command) {
                            addCheck(groupChecks, 'connection:sentry-command', false, 'sentry source uses command mode but no command configured');
                        }
                        else {
                            const commandCheck = await testCommandSourceJson(`${command} --limit 1 --max-signals 1 --last 24h`, commandCwd);
                            addCheck(groupChecks, 'connection:sentry-command', commandCheck.ok, commandCheck.ok
                                ? 'Sentry command smoke test passed'
                                : `Sentry command smoke test failed (${commandCheck.detail}); configured accounts: ${sentryAccounts.map(describeSentryAccountTarget).join(' | ')}`);
                        }
                    }
                }
                else {
                    const requiredByConnectorSetup = onlyAllows(onlyConnectors, 'sentry') && onlyConnectors.length > 0;
                    addCheck(groupChecks, 'connection:sentry', !requiredByConnectorSetup, requiredByConnectorSetup
                        ? 'selected Sentry connector is still disabled in sources.sentry'
                        : 'source disabled');
                }
            },
        });
    }
    const coolifySource = config.sources?.coolify;
    if (onlyAllows(onlyConnectors, 'coolify')) {
        scheduleProgressGroup(tasks, checks, progressJson, {
            key: 'coolify',
            label: 'Coolify',
            detail: 'API key auth + deployment/resource read',
            run: async (groupChecks) => {
                if (sourceEnabled(config, 'coolify')) {
                    const token = process.env[coolifySource?.tokenEnv || coolifySource?.secretEnv || coolifyTokenEnv] || '';
                    const baseUrl = String(coolifySource?.baseUrl || coolifySource?.base_url || process.env.COOLIFY_BASE_URL || '').trim();
                    if (!token) {
                        addCheck(groupChecks, 'connection:coolify', false, `${coolifySource?.tokenEnv || coolifySource?.secretEnv || coolifyTokenEnv} missing (required for live Coolify API test)`, coolifySource?.mode === 'command' ? 'fail' : 'warn');
                    }
                    else if (!baseUrl) {
                        addCheck(groupChecks, 'connection:coolify', false, 'COOLIFY_BASE_URL or sources.coolify.baseUrl missing (required for live Coolify API test)', coolifySource?.mode === 'command' ? 'fail' : 'warn');
                    }
                    else {
                        const coolifyConnection = await testCoolifyConnection(token, timeoutMs, baseUrl);
                        addCheck(groupChecks, 'connection:coolify', coolifyConnection.ok, coolifyConnection.ok
                            ? `Coolify auth check passed (${coolifyConnection.detail})`
                            : `Coolify auth check failed (${coolifyConnection.detail})`);
                    }
                    if (coolifySource?.mode === 'command') {
                        const command = withActiveConfigArg(replaceLegacyRuntimeScriptCommand(String(coolifySource.command || '').trim()), configPath);
                        if (!command) {
                            addCheck(groupChecks, 'connection:coolify-command', false, 'coolify source uses command mode but no command configured');
                        }
                        else {
                            const commandCheck = await testCommandSourceJson(`${command} --limit 1 --max-signals 1 --last 24h`, commandCwd);
                            addCheck(groupChecks, 'connection:coolify-command', commandCheck.ok, commandCheck.ok
                                ? 'Coolify command smoke test passed'
                                : `Coolify command smoke test failed (${commandCheck.detail})`);
                        }
                    }
                }
                else {
                    addCheck(groupChecks, 'connection:coolify', true, 'source disabled');
                }
            },
        });
    }
    const feedbackSource = config.sources?.feedback;
    if (!onlyAllows(onlyConnectors, 'feedback')) {
        // Skip feedback during focused connector checks.
    }
    else if (sourceEnabled(config, 'feedback') && feedbackSource?.mode === 'command') {
        const command = withActiveConfigArg(replaceLegacyRuntimeScriptCommand(String(feedbackSource.command || '').trim()), configPath);
        if (!command) {
            addCheck(checks, 'connection:feedback', false, 'feedback source uses command mode but no command configured');
        }
        else {
            const feedbackConnection = await testCommandSourceJson(command, commandCwd);
            addCheck(checks, 'connection:feedback', feedbackConnection.ok, feedbackConnection.ok
                ? 'Feedback command smoke test passed'
                : `Feedback command smoke test failed (${feedbackConnection.detail})`);
        }
    }
    else if (sourceEnabled(config, 'feedback')) {
        if (process.env[feedbackTokenEnv]) {
            addCheck(checks, 'connection:feedback', true, 'source in file mode; FEEDBACK_API_TOKEN is present');
        }
        else {
            addCheck(checks, 'connection:feedback', true, 'source in file mode (no direct API smoke test required)');
        }
    }
    else {
        addCheck(checks, 'connection:feedback', true, 'source disabled');
    }
    for (const extraSource of getAllSourceEntries(config).filter((source) => !source.builtIn)) {
        const serviceKind = classifyServiceKind(extraSource.service || extraSource.key);
        const explicitConnectorKind = normalizeConnectorKey(extraSource.key || extraSource.service);
        const connectorKind = explicitConnectorKind && explicitConnectorKind !== 'all'
            ? explicitConnectorKind
            : serviceKind === 'store'
                ? 'asc'
                : serviceKind === 'revenue'
                    ? 'revenuecat'
                    : serviceKind === 'crash'
                        ? 'sentry'
                        : serviceKind === 'infrastructure'
                            ? 'coolify'
                            : serviceKind === 'seo'
                                ? 'seo'
                                : serviceKind;
        if (!onlyAllows(onlyConnectors, connectorKind))
            continue;
        const checkName = `connection:${extraSource.key}`;
        if (extraSource.enabled === false) {
            addCheck(checks, checkName, true, 'source disabled');
            continue;
        }
        if (extraSource.mode === 'command') {
            const command = withActiveConfigArg(replaceLegacyRuntimeScriptCommand(String(extraSource.command || '').trim()), configPath);
            if (!command) {
                addCheck(checks, checkName, false, 'source uses command mode but no command configured');
                continue;
            }
            const smokeCommand = connectorKind === 'asc' && command.includes('export-asc-summary')
                ? `${command} --reviews-limit 1 --feedback-limit 1 --analytics-instance-limit 1 --max-signals 1`
                : command;
            const commandCheck = connectorKind === 'asc' && command.includes('export-asc-summary')
                ? await testAscCliAppsList(timeoutMs)
                : await testCommandSourceJson(smokeCommand, commandCwd);
            addCheck(checks, checkName, commandCheck.ok, commandCheck.ok
                ? `${extraSource.key} command smoke test passed`
                : `${extraSource.key} command smoke test failed (${commandCheck.detail})`);
            continue;
        }
        if (extraSource.secretEnv) {
            const hasSecret = Boolean(process.env[extraSource.secretEnv]);
            addCheck(checks, checkName, hasSecret || serviceKind === 'feedback', hasSecret
                ? `${extraSource.secretEnv} set`
                : serviceKind === 'feedback'
                    ? 'file mode without direct API test'
                    : `${extraSource.secretEnv} not set (required for this extra connector)`, hasSecret || serviceKind === 'feedback' ? 'pass' : 'warn');
            continue;
        }
        addCheck(checks, checkName, true, 'file mode (no live API smoke test configured)');
    }
    const githubToken = process.env[githubTokenEnv] || '';
    const githubCheckName = actionMode === 'pull_request' ? 'connection:github-pull-requests' : 'connection:github';
    if (onlyAllows(onlyConnectors, 'github')) {
        scheduleProgressGroup(tasks, checks, progressJson, {
            key: 'github',
            label: 'GitHub',
            detail: githubRepo ? `repo access (${githubRepo})` : 'repo access deferred until repo is known',
            run: async (groupChecks) => {
                if (!requiresGitHubDelivery && (!githubToken || !githubRepo)) {
                    addCheck(groupChecks, githubCheckName, true, githubToken
                        ? 'skipped because project.githubRepo is not configured'
                        : 'skipped because GitHub artifact creation is disabled and no GITHUB_TOKEN is configured');
                }
                else if (!githubToken) {
                    addCheck(groupChecks, githubCheckName, !requiresGitHubDelivery, `${githubTokenEnv} missing (required; ${getGitHubRequirementText(actionMode)})`, requiresGitHubDelivery ? 'fail' : 'warn');
                }
                else {
                    const githubConnection = await testGitHubConnection(githubToken, githubRepo, timeoutMs, actionMode);
                    addCheck(groupChecks, githubCheckName, githubConnection.ok, githubConnection.ok
                        ? `GitHub auth check passed (${githubConnection.detail})`
                        : `GitHub auth check failed (${githubConnection.detail})`);
                }
            },
        });
    }
    await Promise.all(tasks);
}
async function main() {
    await loadOpenClawGrowthSecrets();
    const args = parseArgs(process.argv.slice(2));
    const configPath = path.resolve(args.config);
    const checks = [];
    addCheck(checks, 'node-runtime', true, `Node ${process.version}`);
    let config = null;
    try {
        config = await readJson(configPath);
        addCheck(checks, 'config-file', true, `Loaded ${configPath}`);
    }
    catch (error) {
        addCheck(checks, 'config-file', false, `Could not read config at ${configPath}: ${error instanceof Error ? error.message : String(error)}`);
    }
    if (config) {
        await applyOpenClawSecretRefs(config);
        emitProgress(args.progressJson, {
            phase: 'start',
            key: 'preflight',
            label: 'Local preflight',
            detail: 'config, dependencies, and source wiring',
        });
        const actionMode = getActionMode(config);
        const requiresGitHubDelivery = shouldAutoCreateGitHubArtifact(config);
        const analyticsEnabled = sourceEnabled(config, 'analytics');
        addCheck(checks, 'source:analytics:required', analyticsEnabled, analyticsEnabled ? 'enabled' : 'analytics source is required and cannot be disabled');
        const analyticscliEnsure = await ensureAnalyticsCliInstalled();
        addCheck(checks, 'dependency:analyticscli', analyticscliEnsure.ok, analyticscliEnsure.detail);
        const githubRepo = isConfiguredGitHubRepo(config.project?.githubRepo)
            ? String(config.project.githubRepo).trim()
            : '';
        addCheck(checks, 'project:github-repo', true, githubRepo
            ? `configured (${githubRepo})`
            : 'not configured; GitHub repo context/delivery will be inferred later when possible', 'warn');
        const githubTokenEnv = getSecretName(config, 'githubTokenEnv', 'GITHUB_TOKEN');
        const hasGithubToken = Boolean(process.env[githubTokenEnv]);
        addCheck(checks, `secret:${githubTokenEnv}`, hasGithubToken || !requiresGitHubDelivery, hasGithubToken
            ? requiresGitHubDelivery
                ? `set (required; ${getGitHubRequirementText(actionMode)})`
                : 'set (optional when GitHub delivery is disabled)'
            : requiresGitHubDelivery
                ? `missing (required; ${getGitHubRequirementText(actionMode)})`
                : 'optional when GitHub delivery is disabled', requiresGitHubDelivery ? 'fail' : 'warn');
        for (const source of getAllSourceEntries(config)) {
            const sourceName = source.key;
            if (!source || source.enabled === false) {
                addCheck(checks, `source:${sourceName}`, sourceName !== 'analytics', sourceName === 'analytics' ? 'disabled (not allowed)' : 'disabled');
                continue;
            }
            if (source.mode === 'file') {
                const sourcePath = source.path ? path.resolve(String(source.path)) : null;
                if (!sourcePath) {
                    addCheck(checks, `source:${sourceName}:file`, false, 'mode=file but no path configured');
                    continue;
                }
                try {
                    await fs.access(sourcePath);
                    addCheck(checks, `source:${sourceName}:file`, true, `Found ${sourcePath}`);
                }
                catch {
                    addCheck(checks, `source:${sourceName}:file`, false, `Missing file ${sourcePath}`);
                }
                continue;
            }
            if (source.mode === 'command') {
                const command = replaceLegacyRuntimeScriptCommand(String(source.command || '').trim());
                if (!command) {
                    addCheck(checks, `source:${sourceName}:command`, false, 'mode=command but no command configured');
                    continue;
                }
                const usesPortableDefault = isPortableCommandDefault(sourceName, command);
                addCheck(checks, `source:${sourceName}:mode`, usesPortableDefault, usesPortableDefault
                    ? 'mode=command configured with built-in portable exporter'
                    : 'mode=command configured (allowed, but file mode is the recommended default)', 'warn');
                const head = parseCommandHead(command);
                if (!head) {
                    addCheck(checks, `source:${sourceName}:command`, false, 'Could not parse command head');
                    continue;
                }
                const exists = await commandExists(head);
                addCheck(checks, `source:${sourceName}:command-head`, exists, exists ? `Found command head: ${head}` : `Missing command head: ${head}`);
                if (sourceName === 'revenuecat') {
                    const revenuecatTokenEnv = getSecretName(config, 'revenuecatTokenEnv', 'REVENUECAT_API_KEY');
                    const hasRevenuecatToken = Boolean(process.env[revenuecatTokenEnv]);
                    addCheck(checks, `secret:${revenuecatTokenEnv}`, hasRevenuecatToken, hasRevenuecatToken ? 'set (required for RevenueCat command mode)' : 'missing (required for RevenueCat command mode)');
                }
                if (sourceName === 'paddle') {
                    const paddleAccounts = normalizePaddleAccounts(config, getSecretName(config, 'paddleTokenEnv', 'PADDLE_API_KEY'));
                    for (const account of paddleAccounts) {
                        const hasPaddleToken = Boolean(process.env[account.tokenEnv]);
                        addCheck(checks, `secret:${account.tokenEnv}`, hasPaddleToken, hasPaddleToken
                            ? `set (required for Paddle command mode: ${account.label})`
                            : `missing (required for Paddle command mode: ${account.label})`);
                    }
                }
                if (sourceName === 'seo') {
                    const gscTokenEnv = getSecretName(config, 'gscTokenEnv', 'GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN');
                    const hasSearchConsoleAuth = Boolean(process.env[gscTokenEnv] ||
                        process.env.GSC_ACCESS_TOKEN ||
                        process.env.GOOGLE_APPLICATION_CREDENTIALS ||
                        process.env.GSC_SERVICE_ACCOUNT_JSON ||
                        process.env.GOOGLE_SERVICE_ACCOUNT_JSON);
                    const commandText = String(source.command || '');
                    const csvOnly = /--csv|--gsc-csv/.test(commandText);
                    addCheck(checks, `secret:${gscTokenEnv}`, hasSearchConsoleAuth || csvOnly, hasSearchConsoleAuth
                        ? 'set or service-account auth configured'
                        : csvOnly
                            ? 'not required for configured CSV-only SEO command'
                            : 'missing (required for GSC API mode; CSV-only mode may use --gsc-csv/--csv)', hasSearchConsoleAuth || csvOnly ? 'pass' : 'warn');
                }
                if (sourceName === 'sentry') {
                    const sentryTokenEnv = getSecretName(config, 'sentryTokenEnv', 'SENTRY_AUTH_TOKEN');
                    for (const account of normalizeSentryAccounts(config, sentryTokenEnv)) {
                        const hasSentryToken = Boolean(process.env[account.tokenEnv]);
                        addCheck(checks, `secret:${account.tokenEnv}`, hasSentryToken, hasSentryToken
                            ? `set (required for ${account.label} Sentry command mode)`
                            : `missing (required for ${account.label} Sentry command mode)`);
                    }
                }
                if (sourceName === 'coolify') {
                    const coolifyTokenEnv = getSecretName(config, 'coolifyTokenEnv', 'COOLIFY_API_TOKEN');
                    const tokenEnv = String(source.tokenEnv || source.secretEnv || coolifyTokenEnv).trim();
                    const hasCoolifyToken = Boolean(process.env[tokenEnv]);
                    const hasCoolifyBaseUrl = Boolean(source.baseUrl || source.base_url || process.env.COOLIFY_BASE_URL);
                    addCheck(checks, `secret:${tokenEnv}`, hasCoolifyToken, hasCoolifyToken ? 'set (required for Coolify command mode)' : 'missing (required for Coolify command mode)');
                    addCheck(checks, 'source:coolify:base-url', hasCoolifyBaseUrl, hasCoolifyBaseUrl ? 'configured' : 'missing COOLIFY_BASE_URL or sources.coolify.baseUrl');
                }
                if (!source.builtIn && source.secretEnv) {
                    const hasConnectorToken = Boolean(process.env[source.secretEnv]);
                    addCheck(checks, `secret:${source.secretEnv}`, hasConnectorToken, hasConnectorToken
                        ? `set (required for ${sourceName} command mode)`
                        : `missing (required for ${sourceName} command mode)`);
                }
                continue;
            }
            addCheck(checks, `source:${sourceName}`, false, `Unsupported source mode: ${String(source.mode || 'undefined')}`);
        }
        addCheck(checks, actionMode === 'pull_request' ? 'github-pull-request-create' : 'github-issue-create', actionMode === 'pull_request'
            ? config.actions?.autoCreatePullRequests === true
            : config.actions?.autoCreateIssues === true, actionMode === 'pull_request'
            ? config.actions?.autoCreatePullRequests === true
                ? 'enabled'
                : 'disabled by default (drafts only; enable explicitly to create GitHub artifacts)'
            : config.actions?.autoCreateIssues === true
                ? 'enabled'
                : 'disabled by default (drafts only; enable explicitly to create GitHub artifacts)', (actionMode === 'pull_request'
            ? config.actions?.autoCreatePullRequests === true
            : config.actions?.autoCreateIssues === true)
            ? 'pass'
            : 'warn');
        if (config.charting?.enabled) {
            const pythonExists = await commandExists('python3');
            addCheck(checks, 'dependency:python3', pythonExists, pythonExists ? 'python3 found' : 'python3 missing');
            if (pythonExists) {
                const matplotlibCheck = await runShell("python3 -c 'import matplotlib'");
                addCheck(checks, 'dependency:matplotlib', matplotlibCheck.ok, matplotlibCheck.ok ? 'matplotlib import ok' : 'matplotlib missing (install with: python3 -m pip install matplotlib)');
            }
        }
        else {
            addCheck(checks, 'charting', true, 'disabled');
        }
        if (sourceEnabled(config, 'analytics') && config.sources?.analytics?.mode === 'command') {
            const analyticsTokenEnv = getSecretName(config, 'analyticsTokenEnv', 'ANALYTICSCLI_ACCESS_TOKEN');
            const hasAnalyticsToken = Boolean(process.env[analyticsTokenEnv] || process.env.ANALYTICSCLI_ACCESS_TOKEN);
            addCheck(checks, `secret:${analyticsTokenEnv}`, true, hasAnalyticsToken
                ? 'set'
                : `not set; run the connector wizard to store AnalyticsCLI query access locally`);
        }
        emitProgress(args.progressJson, {
            phase: 'finish',
            key: 'preflight',
            label: 'Local preflight',
            detail: 'config, dependencies, and source wiring',
            status: checkSliceStatus(checks, 0),
        });
        if (args.testConnections) {
            await runConnectionChecks({
                checks,
                config,
                configPath,
                progressJson: args.progressJson,
                timeoutMs: args.timeoutMs,
                onlyConnectors: args.onlyConnectors,
            });
        }
    }
    const failCount = checks.filter((check) => check.status === 'fail').length;
    const warnCount = checks.filter((check) => check.status === 'warn').length;
    const passCount = checks.filter((check) => check.status === 'pass').length;
    const result = {
        ok: failCount === 0,
        summary: {
            pass: passCount,
            warn: warnCount,
            fail: failCount,
        },
        checks,
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
