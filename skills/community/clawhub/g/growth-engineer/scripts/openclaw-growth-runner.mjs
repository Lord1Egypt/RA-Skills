#!/usr/bin/env node
import { existsSync, promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { deriveRuntimeDirFromStatePath, deriveSchedulerProofPathFromStatePath, getActionMode, getAllSourceEntries, getGitHubArtifactModes, getGitHubRequirementText, repairOpenClawCronDeliveryStore, shouldAutoCreateGitHubArtifact, } from './openclaw-growth-shared.mjs';
import { applyOpenClawSecretRefs, loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';
const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const DEFAULT_STATE_PATH = 'data/openclaw-growth-engineer/state.json';
const DEFAULT_SCHEDULER_PROOF_PATH = 'data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl';
const DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES = 360;
const DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MULTIPLIER = 2;
const DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MIN_DELTA = 10;
const DEFAULT_DAILY_RUNNER_FAILURE_RETENTION_DAYS = 14;
const SELF_UPDATE_INTERVAL_MS = 24 * 60 * 60 * 1000;
const SELF_UPDATE_SKILL_SLUG_CANDIDATES = ['growth-engineer', 'openclaw-growth-engineer'];
const RUNTIME_DIR = path.dirname(fileURLToPath(import.meta.url));
let schedulerProofPath = path.resolve(DEFAULT_SCHEDULER_PROOF_PATH);
const DEFAULT_CADENCES = [
    {
        key: 'healthcheck',
        title: '90-minute production error healthcheck',
        intervalMinutes: 90,
        criticalOnly: true,
        focusAreas: ['crash', 'deployment', 'availability'],
        sourcePriorities: ['sentry', 'glitchtip', 'coolify', 'asc_cli'],
        objective: 'Check Sentry/GlitchTip and Coolify for production errors, failed deploys, unhealthy resources, and availability blockers across every configured app.',
        instructions: 'For Sentry/GlitchTip app errors, compare the issue release or app version with ASC production versions first. Ignore errors that only affect TestFlight, debug, staging, unreleased, or non-production app versions. Keep the social output short and action-oriented.',
    },
    {
        key: 'daily',
        title: 'Daily behavioral anomaly guardrail',
        intervalDays: 1,
        criticalOnly: true,
        focusAreas: ['analytics_anomaly', 'onboarding', 'conversion', 'paywall', 'purchase', 'retention', 'revenue'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'asc_cli', 'feedback', 'github', 'sentry', 'glitchtip', 'coolify'],
        objective: 'Detect non-Sentry product and payment anomalies that affect real users: broken login or account flows inferred from behavior, onboarding or purchase drop-offs, zero-conversion days, missing buyers, very low active users, retention cliffs, and revenue anomalies.',
        instructions: 'Compare AnalyticsCLI, RevenueCat, Paddle, ASC, feedback, memory/state, and recent code changes against recent baselines. Use Sentry/GlitchTip/Coolify only as corroborating context; do not repeat pure crash or deployment alerts that belong to the 90-minute healthcheck.',
    },
    {
        key: 'weekly',
        title: 'Weekly executive product and growth summary',
        intervalDays: 7,
        criticalOnly: false,
        focusAreas: ['conversion', 'paywall', 'onboarding', 'marketing', 'retention', 'stability', 'seo'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry', 'coolify', 'github'],
        objective: 'Create a deep app-by-app executive summary across all configured projects, connectors, recent releases, code changes, traffic, SEO/acquisition, revenue, activation, conversion, retention, reviews, and production stability.',
        instructions: 'Be detailed. Group findings per app, explain why each recommendation should improve app usage, revenue, conversion, retention, or traffic, include expected KPI movement, likely code/store surfaces, owner-ready next steps, and verification plans. Generate charts when they clarify the evidence.',
    },
    {
        key: 'monthly',
        title: 'Monthly deep product, business, and code review',
        intervalDays: 30,
        criticalOnly: false,
        focusAreas: ['conversion', 'paywall', 'retention', 'marketing', 'onboarding', 'codebase', 'seo'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry', 'coolify', 'github'],
        objective: 'Compare all configured projects month-over-month: MRR, trial conversion, churn, Paddle revenue/subscriber movement, SEO demand/clicks, acquisition channel quality, store/listing conversion, retention, review themes, feature usage, crash totals, and codebase changes.',
        instructions: 'Be very detailed and app-grouped. Decide what should be built, changed, deleted, priced differently, marketed differently, or instrumented next. Tie conclusions to connector data plus codebase evidence and explain why each recommendation should move revenue, conversion, retention, traffic, or acquisition quality. Generate charts when useful.',
    },
    {
        key: 'quarterly',
        title: '3-month positioning, pricing, and roadmap review',
        intervalDays: 91,
        criticalOnly: false,
        focusAreas: ['marketing', 'paywall', 'retention', 'conversion', 'onboarding'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'github', 'sentry'],
        objective: 'Revisit positioning, pricing/packaging, onboarding architecture, roadmap assumptions, tracking quality, codebase constraints, and major funnel bets across every configured app.',
        instructions: 'Find structural constraints and durable opportunities, not small UI tweaks. Group the analysis by app and tie recommendations to cohort behavior, monetization, SEO demand, reviews, channel quality, and shipped changes. Include concrete roadmap, pricing, conversion, and traffic recommendations.',
    },
    {
        key: 'six_months',
        title: 'Six-month instrumentation and growth-system audit',
        intervalDays: 182,
        criticalOnly: false,
        focusAreas: ['retention', 'conversion', 'paywall', 'marketing', 'general', 'seo'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry'],
        objective: 'Audit connector coverage, SDK instrumentation, event taxonomy, data reliability, data memory, growth loops, and whether product/code strategy still matches the best users across configured projects.',
        instructions: 'Group by app. Prioritize measurement fixes and system changes that make future analysis more trustworthy, then identify the highest-leverage app/revenue/conversion/SEO/traffic improvements. Identify stale events, missing attribution, weak identity, broken feedback loops, and misleading dashboards.',
    },
    {
        key: 'yearly',
        title: 'Yearly evidence reset',
        intervalDays: 365,
        criticalOnly: false,
        focusAreas: ['marketing', 'retention', 'paywall', 'conversion', 'general'],
        sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry'],
        objective: 'Reset strategy from evidence across every configured project: market/channel fit, monetization model, retention ceiling, product scope, and whether to double down, reposition, rebuild, or sunset major surfaces/features.',
        instructions: 'Use the full year of memory, releases, revenue, acquisition, reviews, code changes, and cohort behavior. Produce a strategic operating plan with specific experiments and stop-doing decisions.',
    },
];
function parseArgs(argv) {
    const args = {
        config: DEFAULT_CONFIG_PATH,
        state: DEFAULT_STATE_PATH,
        loop: false,
        noSelfUpdate: false,
    };
    for (let i = 0; i < argv.length; i += 1) {
        const token = argv[i];
        const next = argv[i + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--config') {
            args.config = next;
            i += 1;
        }
        else if (token === '--state') {
            args.state = next;
            i += 1;
        }
        else if (token === '--loop') {
            args.loop = true;
        }
        else if (token === '--no-self-update') {
            args.noSelfUpdate = true;
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
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
OpenClaw Growth Runner

Usage:
  node scripts/openclaw-growth-runner.mjs [--config <file>] [--state <file>] [--loop]

Options:
  --no-self-update   Skip the ClawHub skill update check for this run

Default config: ${DEFAULT_CONFIG_PATH}
Default state:  ${DEFAULT_STATE_PATH}
`);
    process.exit(exitCode);
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
function replaceLegacyRuntimeScriptCommand(command) {
    const trimmed = String(command || '').trim();
    if (!trimmed)
        return trimmed;
    return trimmed
        .replace(/^node\s+scripts\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-engineer\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs)(?=\s|$)/, (_match, scriptName) => nodeRuntimeScriptCommand(scriptName))
        .replace(/^node\s+(['"]?)(?:\S*\/)?node_modules\/@analyticscli\/growth-engineer\/dist\/runtime\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-engineer\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs)\1(?=\s|$)/, (_match, _quote, scriptName) => nodeRuntimeScriptCommand(scriptName));
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
            .replace(/(^|\s)--config=(?:"[^"]*"|'[^']*'|\S+)/, `$1--config ${quote(configPath)}`)
            .replace(/(^|\s)--config\s+(?:"[^"]*"|'[^']*'|\S+)/, `$1--config ${quote(configPath)}`);
    }
    return `${trimmed} --config ${quote(configPath)}`;
}
async function readJson(filePath) {
    const raw = await fs.readFile(filePath, 'utf8');
    return JSON.parse(raw);
}
async function readJsonOptional(filePath, fallback) {
    try {
        return await readJson(filePath);
    }
    catch {
        return fallback;
    }
}
async function ensureDir(dirPath) {
    await fs.mkdir(dirPath, { recursive: true });
}
async function appendSchedulerProof(event, details = {}) {
    const proofPath = schedulerProofPath;
    const entry = {
        ts: new Date().toISOString(),
        event,
        pid: process.pid,
        cwd: process.cwd(),
        ...details,
    };
    await fs.mkdir(path.dirname(proofPath), { recursive: true });
    await fs.appendFile(proofPath, `${JSON.stringify(entry)}\n`, 'utf8');
}
function useSchedulerProofPathForStatePath(statePath) {
    schedulerProofPath = path.resolve(deriveSchedulerProofPathFromStatePath(statePath));
    return schedulerProofPath;
}
function sha256(input) {
    return createHash('sha256').update(input).digest('hex');
}
function stableStringify(value) {
    return JSON.stringify(value, Object.keys(value).sort(), 2);
}
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
function isTransientNetworkFailure(value) {
    return /NETWORK_ERROR|fetch failed|tlsv1 alert|SSL routines|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|socket hang up|network timeout|Temporary failure|upstream connect error|disconnect\/reset before headers|HTTP 5\d\d|API 5\d\d/i.test(String(value || ''));
}
function isRequiredSource(sourceConfig, sourceName) {
    if (sourceConfig?.required === true)
        return true;
    if (sourceConfig?.required === false)
        return false;
    return String(sourceName || '').toLowerCase() === 'analytics';
}
function isSentryCompatibleSource(sourceConfig, sourceName) {
    const sourceKey = String(sourceName || '').toLowerCase();
    const service = String(sourceConfig?.service || sourceConfig?.provider || '').toLowerCase();
    const command = String(sourceConfig?.command || '').toLowerCase();
    return (sourceKey === 'sentry' ||
        sourceKey === 'glitchtip' ||
        service === 'sentry' ||
        service === 'glitchtip' ||
        command.includes('export-sentry-summary'));
}
function shouldDegradeTransientSourceFailure(sourceConfig, sourceName, retried) {
    if (!retried)
        return false;
    if (sourceConfig?.degradeTransientFailures === false)
        return false;
    if (!isRequiredSource(sourceConfig, sourceName))
        return true;
    if (isSentryCompatibleSource(sourceConfig, sourceName))
        return true;
    return sourceConfig?.degradeRequiredTransientFailures !== false;
}
function isTruthyEnv(value) {
    return ['1', 'true', 'yes', 'y', 'on'].includes(String(value || '').trim().toLowerCase());
}
function isFalseyEnv(value) {
    return ['0', 'false', 'no', 'n', 'off'].includes(String(value || '').trim().toLowerCase());
}
async function commandExists(commandName) {
    const result = await runShellCommand(`command -v ${quote(commandName)} >/dev/null 2>&1`, 10_000);
    return result.ok;
}
function parseGitHubRepoFromRemote(remoteUrl) {
    const value = String(remoteUrl || '').trim();
    if (!value)
        return null;
    const sshMatch = value.match(/^git@github\.com:([^/]+\/[^/]+?)(?:\.git)?$/i);
    if (sshMatch)
        return sshMatch[1];
    const httpsMatch = value.match(/^https?:\/\/github\.com\/([^/]+\/[^/]+?)(?:\.git)?$/i);
    if (httpsMatch)
        return httpsMatch[1];
    return null;
}
function isConfiguredGitHubRepo(value) {
    const repo = String(value || '').trim();
    return Boolean(repo && repo !== 'owner/repo' && /^[^/\s]+\/[^/\s]+$/.test(repo));
}
async function inferGitHubRepo(config) {
    const configured = String(config?.project?.githubRepo || '').trim();
    if (isConfiguredGitHubRepo(configured))
        return configured;
    const explicit = String(process.env.OPENCLAW_GITHUB_REPO || '').trim();
    if (isConfiguredGitHubRepo(explicit))
        return explicit;
    const repoRoot = path.resolve(config?.project?.repoRoot || '.');
    const remoteResult = await runShellCommand('git config --get remote.origin.url', 10_000, {
        cwd: repoRoot,
    });
    if (!remoteResult.ok)
        return '';
    return parseGitHubRepoFromRemote(remoteResult.stdout.trim()) || '';
}
async function filesHaveSameContent(leftPath, rightPath) {
    try {
        const [left, right] = await Promise.all([fs.readFile(leftPath), fs.readFile(rightPath)]);
        return left.equals(right);
    }
    catch {
        return false;
    }
}
async function shouldRunSelfUpdate(workspaceRoot, force) {
    if (force)
        return true;
    const statePath = path.join(workspaceRoot, 'data/openclaw-growth-engineer/self-update.json');
    const state = await readJsonOptional(statePath, null);
    const lastCheckedAt = Date.parse(String(state?.lastCheckedAt || ''));
    return !Number.isFinite(lastCheckedAt) || Date.now() - lastCheckedAt > SELF_UPDATE_INTERVAL_MS;
}
async function writeSelfUpdateState(workspaceRoot, value) {
    const statePath = path.join(workspaceRoot, 'data/openclaw-growth-engineer/self-update.json');
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await fs.writeFile(statePath, `${JSON.stringify({ version: 1, checkedAt: new Date().toISOString(), ...value }, null, 2)}\n`, 'utf8');
}
async function rerunCurrentProcessWithoutSelfUpdate() {
    return await new Promise((resolve) => {
        const child = spawn(process.execPath, process.argv.slice(1), {
            env: {
                ...process.env,
                OPENCLAW_GROWTH_SKIP_SELF_UPDATE: '1',
            },
            stdio: 'inherit',
        });
        child.on('error', () => resolve(1));
        child.on('close', (code) => resolve(code));
    });
}
function getSelfUpdateSkillCandidates(workspaceRoot) {
    const explicit = String(process.env.OPENCLAW_GROWTH_SKILL_SLUG || '').trim();
    const uniqueSlugs = [...new Set([explicit, ...SELF_UPDATE_SKILL_SLUG_CANDIDATES].filter(Boolean))];
    return uniqueSlugs.map((slug) => {
        const skillRoot = path.join(workspaceRoot, 'skills', slug);
        return {
            slug,
            skillRoot,
            originPath: path.join(skillRoot, '.clawhub/origin.json'),
            runnerPath: path.join(skillRoot, 'scripts/openclaw-growth-runner.mjs'),
            bootstrapPath: path.join(skillRoot, 'scripts/bootstrap-openclaw-workspace.sh'),
        };
    });
}
function resolveInstalledSelfUpdateSkill(workspaceRoot) {
    return getSelfUpdateSkillCandidates(workspaceRoot).find((candidate) => existsSync(candidate.originPath)) || null;
}
async function maybeSelfUpdateFromClawHub(args) {
    if (args.noSelfUpdate)
        return false;
    if (isTruthyEnv(process.env.OPENCLAW_GROWTH_SKIP_SELF_UPDATE))
        return false;
    if (isTruthyEnv(process.env.OPENCLAW_GROWTH_DISABLE_SELF_UPDATE))
        return false;
    if (isFalseyEnv(process.env.OPENCLAW_GROWTH_SELF_UPDATE))
        return false;
    const workspaceRoot = process.cwd();
    const installedSkill = resolveInstalledSelfUpdateSkill(workspaceRoot);
    if (!installedSkill)
        return false;
    if (!(await commandExists('npx')))
        return false;
    const force = String(process.env.OPENCLAW_GROWTH_SELF_UPDATE || '').trim().toLowerCase() === 'always';
    if (!(await shouldRunSelfUpdate(workspaceRoot, force)))
        return false;
    const beforeOrigin = await readJsonOptional(installedSkill.originPath, null);
    const beforeVersion = String(beforeOrigin?.installedVersion || '');
    process.stdout.write(`Checking for Growth Engineer skill updates (${installedSkill.slug})...\n`);
    const updateResult = await runShellCommand(`npx -y clawhub --no-input --dir skills update ${quote(installedSkill.slug)} --force`, 120_000);
    const afterOrigin = await readJsonOptional(installedSkill.originPath, null);
    const afterVersion = String(afterOrigin?.installedVersion || beforeVersion || '');
    const workspaceRunnerPath = path.resolve(process.argv[1] || 'scripts/openclaw-growth-runner.mjs');
    const runtimeOutdated = !(await filesHaveSameContent(workspaceRunnerPath, installedSkill.runnerPath));
    await writeSelfUpdateState(workspaceRoot, {
        lastCheckedAt: new Date().toISOString(),
        ok: updateResult.ok,
        skillSlug: installedSkill.slug,
        skillRoot: installedSkill.skillRoot,
        previousVersion: beforeVersion || null,
        installedVersion: afterVersion || null,
    }).catch(() => { });
    if (!updateResult.ok) {
        const detail = String(updateResult.stderr || updateResult.stdout || 'update failed').trim().split(/\r?\n/).pop();
        process.stdout.write(`Skill update check skipped: ${detail}\n`);
        return false;
    }
    if ((!afterVersion || afterVersion === beforeVersion) && !runtimeOutdated)
        return false;
    process.stdout.write(afterVersion && afterVersion !== beforeVersion
        ? `Updated OpenClaw Growth Engineer skill ${beforeVersion || 'unknown'} -> ${afterVersion}. Refreshing workspace runtime...\n`
        : 'Refreshing workspace runtime from the installed OpenClaw Growth Engineer skill...\n');
    const bootstrapResult = await runShellCommand(`bash ${quote(installedSkill.bootstrapPath)}`, 60_000);
    if (!bootstrapResult.ok) {
        process.stdout.write('Workspace runtime refresh failed; continuing with current process.\n');
        return false;
    }
    process.stdout.write('Restarting runner with refreshed runtime...\n');
    const code = await rerunCurrentProcessWithoutSelfUpdate();
    process.exit(code ?? 0);
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
function redactCommandForDiagnostics(command) {
    const raw = String(command || '').trim();
    if (!raw)
        return '';
    return raw
        .replace(/((?:^|\s)(?:[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASS|KEY|AUTH|CREDENTIAL)[A-Z0-9_]*)=)(?:"[^"]*"|'[^']*'|\S+)/gi, '$1[redacted]')
        .replace(/((?:^|\s)--(?:token|access-token|api-key|key|secret|password|pass|authorization|auth|bearer)(?:=|\s+))(?:"[^"]*"|'[^']*'|\S+)/gi, '$1[redacted]');
}
function truncateDiagnosticText(value, maxLength = 2000) {
    const text = String(value || '').trim();
    if (text.length <= maxLength)
        return text;
    return `${text.slice(0, maxLength - 1)}…`;
}
function buildSourceCommandFailureMessage(sourceName, resolvedCommand, detail) {
    const safeCommand = redactCommandForDiagnostics(resolvedCommand);
    const safeDetail = truncateDiagnosticText(detail);
    return safeCommand
        ? `Source "${sourceName}" command failed: command \`${safeCommand}\`; ${safeDetail}`
        : `Source "${sourceName}" command failed: ${safeDetail}`;
}
function isSudoPasswordPrompt(stderr) {
    return /sudo: (?:a password is required|a terminal is required to read the password|no tty present)/i.test(String(stderr || ''));
}
function runShellCommand(command, timeoutMs = 120_000, options = {}) {
    return new Promise((resolve) => {
        const hardenedCommand = hardenUnattendedShellCommand(command);
        const child = spawn(resolveShellCommand(), ['-c', hardenedCommand], {
            stdio: options.input === undefined ? ['ignore', 'pipe', 'pipe'] : ['pipe', 'pipe', 'pipe'],
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
        const timer = setTimeout(() => {
            if (settled)
                return;
            settled = true;
            child.kill('SIGTERM');
            resolve({ ok: false, code: null, stdout, stderr: `${stderr}\nTimed out after ${timeoutMs}ms` });
        }, timeoutMs);
        child.stdout.on('data', (chunk) => {
            stdout += String(chunk);
        });
        child.stderr.on('data', (chunk) => {
            stderr += String(chunk);
            if (!settled && isSudoPasswordPrompt(stderr)) {
                settled = true;
                clearTimeout(timer);
                child.kill('SIGTERM');
                resolve({
                    ok: false,
                    code: null,
                    stdout,
                    stderr: `${stderr.trim()}\nBlocked non-interactive sudo prompt. Configure passwordless sudo for this exact command or remove sudo from the Growth Engineer connector command.`,
                });
            }
        });
        if (options.input !== undefined) {
            child.stdin.end(options.input);
        }
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
function getSecretName(config, key, fallback) {
    const value = config?.secrets?.[key];
    return typeof value === 'string' && value.trim() ? value.trim() : fallback;
}
async function assertHardRequirements(config) {
    const missing = [];
    const analyticsSource = config?.sources?.analytics;
    const actionMode = getActionMode(config);
    const requiresGitHubDelivery = shouldAutoCreateGitHubArtifact(config);
    if (!analyticsSource || analyticsSource.enabled === false) {
        missing.push('sources.analytics must be enabled');
    }
    const analyticscliExists = await commandExists('analyticscli');
    if (!analyticscliExists) {
        missing.push('analyticscli binary is required');
    }
    if (requiresGitHubDelivery) {
        const githubRepo = String(config?.project?.githubRepo || '').trim();
        const githubTokenEnv = getSecretName(config, 'githubTokenEnv', 'GITHUB_TOKEN');
        if (githubRepo && !process.env[githubTokenEnv]) {
            missing.push(`${githubTokenEnv} env var is required (${getGitHubRequirementText(actionMode)})`);
        }
    }
    if (missing.length > 0) {
        const message = `Hard requirements missing:\n- ${missing.join('\n- ')}`;
        throw new Error(message);
    }
}
function getProjectCommandCwd(config) {
    const repoRoot = String(config?.project?.repoRoot || '').trim();
    return repoRoot ? path.resolve(repoRoot) : process.cwd();
}
function parseJsonFromStdout(stdout) {
    const raw = String(stdout || '').trim();
    if (!raw)
        return null;
    const firstBrace = raw.indexOf('{');
    const firstBracket = raw.indexOf('[');
    const starts = [firstBrace, firstBracket].filter((index) => index >= 0);
    if (starts.length === 0)
        return null;
    try {
        return JSON.parse(raw.slice(Math.min(...starts)));
    }
    catch {
        return null;
    }
}
function getConnectorHealthIntervalMinutes(config) {
    const configured = Number(config?.schedule?.connectorHealthCheckIntervalMinutes);
    return Number.isFinite(configured) && configured > 0
        ? configured
        : DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES;
}
function isDue(lastCheckedAt, intervalMinutes) {
    if (!lastCheckedAt)
        return true;
    const last = Date.parse(String(lastCheckedAt));
    if (!Number.isFinite(last))
        return true;
    return Date.now() - last >= intervalMinutes * 60_000;
}
function normalizeCadenceKey(value) {
    const normalized = String(value || '')
        .trim()
        .toLowerCase()
        .replace(/[\s-]+/g, '_');
    if (['3_months', 'three_months', 'quarter', 'quarterly'].includes(normalized))
        return 'quarterly';
    if (['6_months', 'six_months', 'half_year', 'half_yearly'].includes(normalized))
        return 'six_months';
    if (['1y', '1_year', 'one_year', 'annual', 'annually'].includes(normalized))
        return 'yearly';
    return normalized;
}
function getCadenceDefinitions(config) {
    const configured = Array.isArray(config?.schedule?.cadences) ? config.schedule.cadences : [];
    const byKey = new Map(DEFAULT_CADENCES.map((cadence) => [cadence.key, { ...cadence }]));
    for (const cadence of configured) {
        if (!cadence || typeof cadence !== 'object')
            continue;
        const key = normalizeCadenceKey(cadence.key || cadence.id || cadence.label);
        if (!key)
            continue;
        const base = byKey.get(key) || { key };
        byKey.set(key, {
            ...base,
            ...cadence,
            key,
            enabled: cadence.enabled !== false,
            focusAreas: Array.isArray(cadence.focusAreas) ? cadence.focusAreas : base.focusAreas || [],
            sourcePriorities: Array.isArray(cadence.sourcePriorities)
                ? cadence.sourcePriorities
                : base.sourcePriorities || [],
        });
    }
    return [...byKey.values()].filter((cadence) => cadence.enabled !== false);
}
function cadenceIsDue(cadence, state) {
    const lastRanAt = state?.cadences?.[cadence.key]?.lastRanAt;
    const intervalMinutes = Number(cadence.intervalMinutes || 0);
    if (intervalMinutes > 0) {
        if (!lastRanAt)
            return true;
        const last = Date.parse(String(lastRanAt));
        if (!Number.isFinite(last))
            return true;
        return Date.now() - last >= Math.max(1, intervalMinutes) * 60 * 1000;
    }
    const intervalDays = Number(cadence.intervalDays || 1);
    if (!lastRanAt)
        return true;
    const last = Date.parse(String(lastRanAt));
    if (!Number.isFinite(last))
        return true;
    return Date.now() - last >= Math.max(1, intervalDays) * 24 * 60 * 60 * 1000;
}
function getDueCadences(config, state) {
    return getCadenceDefinitions(config).filter((cadence) => cadenceIsDue(cadence, state));
}
function markCadencesRan(state, cadences, ranAt) {
    const nextCadences = { ...(state?.cadences || {}) };
    for (const cadence of cadences) {
        nextCadences[cadence.key] = {
            ...(nextCadences[cadence.key] || {}),
            lastRanAt: ranAt,
            title: cadence.title,
        };
    }
    return nextCadences;
}
function getConnectorEntries(statusPayload) {
    return Object.entries(statusPayload?.connectors || {}).map(([key, value]) => ({
        key,
        status: String(value?.status || 'unknown'),
        detail: String(value?.detail || ''),
        nextAction: typeof value?.nextAction === 'string' ? value.nextAction : null,
        accounts: Array.isArray(value?.accounts) ? value.accounts : [],
    }));
}
function getUnhealthyConfiguredConnectors(statusPayload) {
    return getConnectorEntries(statusPayload).filter((entry) => ['blocked', 'partial', 'unknown'].includes(entry.status));
}
function getConnectedConnectorKeys(statusPayload) {
    return getConnectorEntries(statusPayload)
        .filter((entry) => entry.status === 'connected')
        .map((entry) => entry.key)
        .sort();
}
function buildConnectorHealthFingerprint(unhealthyConnectors) {
    return sha256(unhealthyConnectors
        .map((entry) => `${entry.key}|${entry.status}|${entry.detail}|${entry.nextAction || ''}`)
        .sort()
        .join('\n'));
}
function humanConnectorName(key) {
    if (key === 'analyticscli')
        return 'AnalyticsCLI';
    if (key === 'appStoreConnect')
        return 'App Store Connect';
    if (key === 'revenuecat')
        return 'RevenueCat';
    if (key === 'sentry')
        return 'Sentry';
    if (key === 'github')
        return 'GitHub';
    return key;
}
function connectorWizardKey(key) {
    if (key === 'analyticscli')
        return 'analytics';
    if (key === 'appStoreConnect')
        return 'asc';
    if (key === 'revenuecat')
        return 'revenuecat';
    if (key === 'sentry')
        return 'sentry';
    if (key === 'github')
        return 'github';
    return '';
}
function buildConnectorWizardCommand(configPath, entry) {
    const connector = connectorWizardKey(entry.key);
    if (!connector)
        return null;
    const configArg = configPath ? ` --config ${quote(configPath)}` : '';
    return `npx -y @analyticscli/growth-engineer wizard${configArg} --connectors ${quote(connector)}`;
}
function conciseConnectorDetail(entry) {
    const detail = String(entry?.detail || '').replace(/\s+/g, ' ').trim();
    if (/SENTRY_AUTH_TOKEN is required|SENTRY_AUTH_TOKEN.*missing/i.test(detail)) {
        return 'SENTRY_AUTH_TOKEN missing for source collection.';
    }
    if (/source .*disabled|still disabled/i.test(detail)) {
        return 'source is still disabled after setup.';
    }
    if (!detail)
        return 'needs attention.';
    return detail.length > 180 ? `${detail.slice(0, 177)}...` : detail;
}
function buildConnectorHealthAlert(statusPayload, unhealthyConnectors) {
    const configPath = statusPayload?.configPath || DEFAULT_CONFIG_PATH;
    const lines = [`OpenClaw connector health: ${unhealthyConnectors.length} issue(s)`];
    for (const entry of unhealthyConnectors) {
        lines.push(`- ${humanConnectorName(entry.key)}: ${entry.status} - ${conciseConnectorDetail(entry)}`);
        const command = buildConnectorWizardCommand(configPath, entry);
        if (command) {
            lines.push(`  Fix: \`${command}\``);
        }
    }
    lines.push('Secrets stay in the host terminal or secret store.');
    return `${lines.join('\n')}\n`;
}
function sourceFailureConnectorKey(failure) {
    const service = String(failure?.service || '').toLowerCase();
    const key = String(failure?.key || '').toLowerCase();
    const source = String(failure?.source || '').toLowerCase();
    if (service.includes('sentry') || key === 'glitchtip')
        return 'sentry';
    if (source === 'sentry' || source === 'glitchtip')
        return 'sentry';
    if (service.includes('revenuecat'))
        return 'revenuecat';
    if (service.includes('paddle'))
        return 'paddle';
    if (service.includes('seo') || service.includes('gsc') || service.includes('search-console') || service.includes('dataforseo'))
        return 'seo';
    if (key === 'paddle')
        return 'paddle';
    if (key === 'seo')
        return 'seo';
    if (service.includes('coolify'))
        return 'coolify';
    if (service.includes('github'))
        return 'github';
    if (key === 'analytics')
        return 'analyticscli';
    return String(failure?.key || 'source');
}
function getSentryAccountTargets(config) {
    const accounts = Array.isArray(config?.sources?.sentry?.accounts) ? config.sources.sentry.accounts : [];
    if (accounts.length === 0)
        return [];
    return accounts.map((account, index) => ({
        id: String(account?.id || account?.key || account?.label || `sentry_${index + 1}`)
            .trim()
            .replace(/[^a-zA-Z0-9._-]+/g, '_'),
        label: String(account?.label || account?.name || account?.id || `Sentry ${index + 1}`).trim(),
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
function buildSourceFailureStatusPayload(configPath, sourceFailures, config = null) {
    const connectors = {};
    for (const failure of sourceFailures) {
        const key = sourceFailureConnectorKey(failure);
        const detail = `Source collection failed during scheduled run: ${failure.detail}`;
        const retryable = Boolean(failure.retryable || failure.transient);
        connectors[key] = {
            status: 'partial',
            detail,
            accounts: key === 'sentry' ? getSentryAccountTargets(config) : [],
            nextAction: retryable
                ? 'Provider returned a transient upstream/network error after retry. Rerun the Growth Engineer later; if it repeats, check the provider status page and connector credentials.'
                : 'Run the connector wizard or source command on the host terminal and fix the reported source error.',
        };
    }
    return {
        generatedAt: new Date().toISOString(),
        configPath,
        connectors,
        sourceFailures,
    };
}
async function recordSourceCollectionFailures({ config, configPath, state, statePath, runtimeDir, sourceFailures }) {
    if (sourceFailures.length === 0) {
        return {
            ...state,
            lastSourceCollectionFailures: [],
        };
    }
    const healthState = state?.connectorHealth || {};
    const checkedAt = new Date().toISOString();
    const statusPayload = buildSourceFailureStatusPayload(configPath, sourceFailures, config);
    const unhealthyConnectors = getUnhealthyConfiguredConnectors(statusPayload);
    const fingerprint = buildConnectorHealthFingerprint(unhealthyConnectors);
    const previousExternallyDeliveredFingerprint = healthState.lastExternalAlertedFingerprint || null;
    let alertTriggered = false;
    let alertDeliveries = [];
    const nextHealthState = {
        ...healthState,
        lastCheckedAt: checkedAt,
        lastStatusOk: false,
        lastFingerprint: fingerprint,
        activeIncidentFingerprint: fingerprint,
        lastError: sourceFailures.map((failure) => `${failure.key || failure.source}: ${failure.detail}`).join('\n'),
    };
    if (previousExternallyDeliveredFingerprint !== fingerprint) {
        const message = buildConnectorHealthAlert(statusPayload, unhealthyConnectors);
        const paths = await writeConnectorHealthAlert(runtimeDir, message, statusPayload, unhealthyConnectors, fingerprint);
        const deliveries = await deliverConnectorHealthAlert({
            config,
            configPath,
            message,
            statusPayload,
            unhealthyConnectors,
            fingerprint,
        });
        alertTriggered = true;
        alertDeliveries = deliveries;
        nextHealthState.lastAlertedAt = checkedAt;
        nextHealthState.lastAlertedFingerprint = fingerprint;
        nextHealthState.lastAlertMarkdownPath = paths.markdownPath;
        nextHealthState.lastAlertJsonPath = paths.jsonPath;
        nextHealthState.lastAlertDeliveries = deliveries;
        nextHealthState.lastAlertExternalSent = hasSuccessfulExternalDelivery(deliveries);
        if (nextHealthState.lastAlertExternalSent) {
            nextHealthState.lastExternalAlertedAt = checkedAt;
            nextHealthState.lastExternalAlertedFingerprint = fingerprint;
        }
    }
    const nextState = {
        ...state,
        connectorHealth: nextHealthState,
        lastSourceCollectionFailures: sourceFailures,
    };
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await fs.writeFile(statePath, JSON.stringify(nextState, null, 2), 'utf8');
    await appendSchedulerProof('source_collection_degraded', {
        configPath,
        statePath,
        checkedAt,
        sourceFailures: sourceFailures.map((failure) => ({
            key: failure.key,
            detail: failure.detail,
            retryable: failure.retryable,
        })),
        unhealthyConnectors: unhealthyConnectors.map((entry) => ({
            key: entry.key,
            status: entry.status,
            detail: entry.detail,
        })),
        alertTriggered,
        deliveryCount: alertDeliveries.length,
        externalDeliverySent: alertTriggered ? hasSuccessfulExternalDelivery(alertDeliveries) : false,
        socialOutput: alertTriggered ? 'CONNECTOR_HEALTH_ALERT' : 'HEARTBEAT_OK',
        socialReason: alertTriggered
            ? 'new or changed source-collection connector incident'
            : 'source-collection connector incident unchanged',
    });
    return nextState;
}
async function writeConnectorHealthAlert(runtimeDir, message, statusPayload, unhealthyConnectors, fingerprint) {
    const alertDir = path.join(runtimeDir, 'connector-health');
    await ensureDir(alertDir);
    const markdownPath = path.join(alertDir, 'latest.md');
    const jsonPath = path.join(alertDir, 'latest.json');
    await fs.writeFile(markdownPath, message, 'utf8');
    await fs.writeFile(jsonPath, JSON.stringify({
        generatedAt: new Date().toISOString(),
        fingerprint,
        unhealthyConnectors,
        status: statusPayload,
    }, null, 2), 'utf8');
    return { markdownPath, jsonPath };
}
function notificationChannelKey(channel) {
    const type = String(channel?.type || 'openclaw-chat');
    if (type === 'openclaw-chat')
        return 'openclaw-chat';
    if (type === 'slack')
        return `slack:${channel?.label || channel?.webhookEnv || 'slack'}`;
    if (type === 'webhook')
        return `webhook:${channel?.label || channel?.urlEnv || channel?.webhookEnv || 'webhook'}`;
    if (type === 'discord')
        return `discord:${channel?.label || channel?.command || 'discord'}`;
    if (type === 'command')
        return `command:${channel?.label || channel?.command || 'command'}`;
    return `${type}:${channel?.label || type}`;
}
function mergeNotificationChannelsWithDeliveries(configuredChannels, deliveryChannels) {
    const configured = Array.isArray(configuredChannels) ? configuredChannels : [];
    const seen = new Set(configured.map((channel) => notificationChannelKey(channel)));
    const channels = configured.filter((channel) => channel?.enabled !== false);
    for (const channel of deliveryChannels) {
        if (!seen.has(notificationChannelKey(channel))) {
            channels.push(channel);
        }
    }
    return channels;
}
function getDeliveryNotificationChannels(config, kind) {
    const channels = [];
    const deliveries = config?.deliveries || {};
    if (deliveries.openclawChat?.enabled) {
        const isConnectorHealth = kind === 'connectorHealth';
        channels.push({
            type: 'openclaw-chat',
            label: 'openclaw_chat',
            markdownPath: isConnectorHealth
                ? deliveries.openclawChat.connectorHealthMarkdownPath || deliveries.openclawChat.markdownPath
                : deliveries.openclawChat.growthRunMarkdownPath || '.openclaw/chat/growth-summary.md',
            jsonPath: isConnectorHealth
                ? deliveries.openclawChat.connectorHealthJsonPath || deliveries.openclawChat.jsonPath
                : deliveries.openclawChat.growthRunJsonPath || '.openclaw/chat/growth-summary.json',
        });
    }
    if (deliveries.slack?.enabled) {
        channels.push({
            type: 'slack',
            label: 'slack',
            webhookEnv: deliveries.slack.webhookEnv || 'SLACK_WEBHOOK_URL',
        });
    }
    if (deliveries.webhook?.enabled) {
        channels.push({
            type: 'webhook',
            label: 'webhook',
            urlEnv: deliveries.webhook.urlEnv || 'OPENCLAW_WEBHOOK_URL',
            method: deliveries.webhook.method || 'POST',
            headers: deliveries.webhook.headers || {},
        });
    }
    if (deliveries.command?.enabled) {
        channels.push({
            type: 'command',
            label: deliveries.command.label || 'command',
            command: deliveries.command.command || '',
        });
    }
    if (deliveries.discord?.enabled) {
        channels.push({
            type: 'discord',
            label: deliveries.discord.label || 'discord',
            command: deliveries.discord.command || '',
        });
    }
    return channels;
}
function getConnectorHealthChannels(config) {
    const configuredChannels = Array.isArray(config?.notifications?.connectorHealth?.channels)
        ? config.notifications.connectorHealth.channels
        : [];
    return mergeNotificationChannelsWithDeliveries(configuredChannels, getDeliveryNotificationChannels(config, 'connectorHealth'));
}
function resolveOpenClawChatDeliveryPath(channelPath, fallbackPath) {
    const targetPath = String(channelPath || fallbackPath || '').trim();
    if (!targetPath)
        return path.resolve(process.cwd(), fallbackPath);
    return path.isAbsolute(targetPath) ? targetPath : path.resolve(process.cwd(), targetPath);
}
async function writeConfiguredOpenClawChatAlert(configPath, channel, message, statusPayload, unhealthyConnectors, fingerprint) {
    const markdownPath = resolveOpenClawChatDeliveryPath(channel.markdownPath, '.openclaw/chat/connector-health.md');
    const jsonPath = resolveOpenClawChatDeliveryPath(channel.jsonPath, '.openclaw/chat/connector-health.json');
    await fs.mkdir(path.dirname(markdownPath), { recursive: true });
    await fs.mkdir(path.dirname(jsonPath), { recursive: true });
    await fs.writeFile(markdownPath, message, 'utf8');
    await fs.writeFile(jsonPath, JSON.stringify({
        channel: channel.label || 'openclaw_chat',
        generatedAt: new Date().toISOString(),
        fingerprint,
        unhealthyConnectors,
        status: statusPayload,
    }, null, 2), 'utf8');
    return {
        sent: true,
        external: false,
        target: channel.label || 'openclaw_chat',
        detail: `wrote local OpenClaw chat outbox ${markdownPath} and ${jsonPath}`,
    };
}
async function sendSlackConnectorHealthAlert(channel, message) {
    const webhookEnv = channel.webhookEnv || 'SLACK_WEBHOOK_URL';
    const webhookUrl = process.env[webhookEnv];
    if (!webhookUrl) {
        return { sent: false, target: channel.label || 'slack', detail: `${webhookEnv} not set` };
    }
    const response = await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ text: message }),
    });
    return {
        sent: response.ok,
        external: true,
        target: channel.label || 'slack',
        detail: response.ok ? `HTTP ${response.status}` : `HTTP ${response.status}: ${await response.text()}`,
    };
}
async function sendWebhookConnectorHealthAlert(channel, message, statusPayload, unhealthyConnectors, fingerprint) {
    const urlEnv = channel.urlEnv || channel.webhookEnv || 'OPENCLAW_WEBHOOK_URL';
    const webhookUrl = process.env[urlEnv];
    if (!webhookUrl) {
        return { sent: false, target: channel.label || 'webhook', detail: `${urlEnv} not set` };
    }
    const response = await fetch(webhookUrl, {
        method: channel.method || 'POST',
        headers: {
            'content-type': 'application/json',
            ...(channel.headers || {}),
        },
        body: JSON.stringify({
            type: 'openclaw.connector_health',
            generatedAt: new Date().toISOString(),
            text: message,
            fingerprint,
            unhealthyConnectors,
            status: statusPayload,
        }),
    });
    return {
        sent: response.ok,
        external: true,
        target: channel.label || 'webhook',
        detail: response.ok ? `HTTP ${response.status}` : `HTTP ${response.status}: ${await response.text()}`,
    };
}
async function sendCommandConnectorHealthAlert(channel, message) {
    if (!channel.command) {
        return { sent: false, target: channel.label || 'command', detail: 'command not configured' };
    }
    const result = await runShellCommand(String(channel.command), 60_000, { input: message });
    return {
        sent: result.ok,
        external: true,
        target: channel.label || 'command',
        detail: result.ok ? 'sent' : result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
    };
}
async function sendDiscordConnectorHealthAlert(channel, message, statusPayload, unhealthyConnectors, fingerprint) {
    if (!channel.command) {
        return { sent: false, target: channel.label || 'discord', detail: 'discord command not configured' };
    }
    const payload = buildDiscordConnectorHealthPayload(message, statusPayload, unhealthyConnectors, fingerprint);
    const result = await runShellCommand(String(channel.command), 60_000, {
        input: JSON.stringify(payload),
        env: { OPENCLAW_DISCORD_DELIVERY_FORMAT: 'embed' },
    });
    return {
        sent: result.ok,
        external: true,
        target: channel.label || 'discord',
        detail: result.ok ? 'sent' : result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
    };
}
function hasExternalNotificationChannel(channels) {
    return channels.some((channel) => channel?.type && channel.type !== 'openclaw-chat');
}
function hasSuccessfulExternalDelivery(results) {
    return results.some((result) => result?.sent === true && result?.external === true);
}
function discordTruncate(value, maxLength) {
    const text = String(value || '').replace(/\s+/g, ' ').trim();
    if (text.length <= maxLength)
        return text;
    return `${text.slice(0, Math.max(0, maxLength - 1)).trim()}…`;
}
function discordField(name, value, inline = false) {
    return {
        name: discordTruncate(name, 256) || 'Detail',
        value: discordTruncate(value, 1024) || '-',
        inline,
    };
}
function connectorStatusColor(unhealthyConnectors) {
    return unhealthyConnectors.some((entry) => String(entry?.status || '').toLowerCase() === 'blocked')
        ? 0xd92d20
        : 0xf79009;
}
function buildDiscordConnectorHealthPayload(message, statusPayload, unhealthyConnectors, fingerprint) {
    const fields = unhealthyConnectors.slice(0, 10).map((entry) => {
        const command = buildConnectorWizardCommand(statusPayload?.configPath || DEFAULT_CONFIG_PATH, entry);
        const parts = [
            `Status: ${entry.status || 'blocked'}`,
            conciseConnectorDetail(entry),
            command ? `Fix: \`${command}\`` : null,
        ].filter(Boolean);
        return discordField(humanConnectorName(entry.key), parts.join('\n'));
    });
    if (unhealthyConnectors.length > 10) {
        fields.push(discordField('More issues', `${unhealthyConnectors.length - 10} additional connector(s) need attention.`));
    }
    return {
        content: '',
        embeds: [
            {
                title: `OpenClaw connector health: ${unhealthyConnectors.length} issue(s)`,
                description: 'Secrets stay in the host terminal or secret store.',
                color: connectorStatusColor(unhealthyConnectors),
                fields,
                footer: {
                    text: `CONNECTOR_HEALTH_ALERT • ${String(fingerprint || '').slice(0, 12)}`,
                },
                timestamp: statusPayload?.generatedAt || new Date().toISOString(),
            },
        ],
        fallbackText: message,
    };
}
function truncateMessageText(value, maxLength = 96) {
    const text = String(value || '').replace(/\s+/g, ' ').trim();
    if (text.length <= maxLength)
        return text;
    return `${text.slice(0, Math.max(0, maxLength - 3)).trim()}...`;
}
function issueProjectLabel(issue) {
    return String(issue?.app || issue?.source_project || issue?.sourceProject || issue?.project || 'unscoped').trim();
}
function issueSourceUrl(issue) {
    const direct = String(issue?.source_url || issue?.sourceUrl || issue?.issue_url || issue?.issueUrl || '').trim();
    if (direct)
        return direct;
    const body = String(issue?.body || '');
    const match = body.match(/(?:Issue link|Permalink):\s*(https?:\/\/\S+)/i);
    return match ? match[1].replace(/[).,;]+$/, '') : '';
}
function formatIssueSummaryLine(issue, maxTitleLength = 92) {
    const title = truncateMessageText(issue?.title, maxTitleLength);
    const url = issueSourceUrl(issue);
    return url ? `${title} (${url})` : title;
}
function groupIssuesByProject(issues, maxIssues = 4) {
    const grouped = new Map();
    for (const issue of issues.slice(0, maxIssues)) {
        const label = issueProjectLabel(issue);
        const bucket = grouped.get(label) || [];
        bucket.push(issue);
        grouped.set(label, bucket);
    }
    return [...grouped.entries()];
}
function getDailyIssueDedupeConfig(config) {
    const raw = config?.schedule?.dailyIssueDedupe || config?.notifications?.growthRun?.dailyIssueDedupe || {};
    const multiplier = Number(raw.eventGrowthMultiplier ?? raw.multiplier);
    const minDelta = Number(raw.eventGrowthMinDelta ?? raw.minDelta);
    return {
        enabled: raw.enabled !== false,
        eventGrowthMultiplier: Number.isFinite(multiplier) && multiplier > 1
            ? multiplier
            : DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MULTIPLIER,
        eventGrowthMinDelta: Number.isFinite(minDelta) && minDelta > 0
            ? minDelta
            : DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MIN_DELTA,
    };
}
function getDailyRunnerFailureDedupeConfig(config) {
    const raw = config?.schedule?.dailyRunnerFailureDedupe || config?.notifications?.growthRun?.dailyRunnerFailureDedupe || {};
    const retentionDays = Number(raw.retentionDays);
    return {
        enabled: raw.enabled !== false,
        retentionDays: Number.isFinite(retentionDays) && retentionDays > 0
            ? retentionDays
            : DEFAULT_DAILY_RUNNER_FAILURE_RETENTION_DAYS,
    };
}
function resolveDailyIssueDedupeTimeZone(config) {
    return String(config?.schedule?.timezone ||
        config?.automation?.openclawCron?.timezone ||
        process.env.TZ ||
        'UTC').trim() || 'UTC';
}
function normalizeRunnerFailureForFingerprint(errorMessage) {
    return redactCommandForDiagnostics(errorMessage)
        .replace(/\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\b/g, '[timestamp]')
        .replace(/--since(?:=|\s+)(?:"[^"]*"|'[^']*'|\S+)/g, '--since [timestamp]')
        .replace(/--until(?:=|\s+)(?:"[^"]*"|'[^']*'|\S+)/g, '--until [timestamp]')
        .replace(/\bpid\s+\d+\b/gi, 'pid [pid]')
        .replace(/\s+/g, ' ')
        .trim();
}
function buildRunnerFailureFingerprint(errorMessage) {
    return sha256(normalizeRunnerFailureForFingerprint(errorMessage));
}
function pruneDailyRunnerFailures(failures, now, retentionDays) {
    const cutoffMs = now.getTime() - retentionDays * 24 * 60 * 60 * 1000;
    return Object.fromEntries(Object.entries(failures || {}).filter(([, entry]) => {
        const lastSeenMs = Date.parse(String(entry?.lastSeenAt || entry?.firstSeenAt || ''));
        return !Number.isFinite(lastSeenMs) || lastSeenMs >= cutoffMs;
    }));
}
function parseFailureArgs(argv) {
    const args = {
        config: DEFAULT_CONFIG_PATH,
        state: DEFAULT_STATE_PATH,
    };
    for (let i = 0; i < argv.length; i += 1) {
        const token = argv[i];
        const next = argv[i + 1];
        if (token === '--config' && next) {
            args.config = next;
            i += 1;
        }
        else if (token === '--state' && next) {
            args.state = next;
            i += 1;
        }
    }
    return args;
}
async function recordRunnerFailure({ configPath, statePath, error, argv = [], now = new Date() }) {
    const errorMessage = truncateDiagnosticText(error instanceof Error ? error.message : String(error));
    const config = await readJsonOptional(configPath, {});
    const state = await readJsonOptional(statePath, {
        sourceHashes: {},
        lastIssueFingerprint: null,
        lastRunAt: null,
        sourceCursors: {},
    });
    const dedupeConfig = getDailyRunnerFailureDedupeConfig(config);
    const timeZone = resolveDailyIssueDedupeTimeZone(config);
    const date = formatDateInTimeZone(now, timeZone);
    const fingerprint = buildRunnerFailureFingerprint(errorMessage);
    const nowIso = now.toISOString();
    const previousDailyFailures = state?.dailyRunnerFailures?.date === date
        ? state.dailyRunnerFailures
        : null;
    const previousFailures = previousDailyFailures?.failures && typeof previousDailyFailures.failures === 'object'
        ? previousDailyFailures.failures
        : {};
    const failures = pruneDailyRunnerFailures(previousFailures, now, dedupeConfig.retentionDays);
    const previousEntry = failures[fingerprint] || null;
    const suppressed = dedupeConfig.enabled && Boolean(previousEntry);
    const nextEntry = {
        ...(previousEntry || {}),
        fingerprint,
        error: errorMessage,
        normalizedError: normalizeRunnerFailureForFingerprint(errorMessage),
        firstSeenAt: previousEntry?.firstSeenAt || nowIso,
        lastSeenAt: nowIso,
    };
    if (suppressed) {
        nextEntry.suppressedCount = Number(previousEntry?.suppressedCount || 0) + 1;
    }
    else {
        nextEntry.lastReportedAt = nowIso;
        nextEntry.reportCount = Number(previousEntry?.reportCount || 0) + 1;
    }
    failures[fingerprint] = nextEntry;
    const nextState = {
        ...state,
        dailyRunnerFailures: {
            date,
            timeZone,
            failures,
            updatedAt: nowIso,
        },
        lastRunnerFailure: {
            fingerprint,
            error: errorMessage,
            failedAt: nowIso,
            suppressed,
        },
    };
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await fs.writeFile(statePath, JSON.stringify(nextState, null, 2), 'utf8');
    await appendSchedulerProof(suppressed ? 'runner_failed_suppressed' : 'runner_failed', {
        configPath,
        statePath,
        error: errorMessage,
        errorFingerprint: fingerprint,
        date,
        timeZone,
        argv,
        suppressed,
        reportCount: nextEntry.reportCount || 0,
        suppressedCount: nextEntry.suppressedCount || 0,
        socialOutput: suppressed ? 'HEARTBEAT_OK' : 'RUNNER_FAILED',
        socialReason: suppressed
            ? 'runner failure unchanged and already reported today'
            : 'new runner failure for current day',
    });
    return {
        suppressed,
        exitCode: suppressed ? 0 : 1,
        fingerprint,
    };
}
function formatDateInTimeZone(date, timeZone) {
    try {
        const parts = new Intl.DateTimeFormat('en-CA', {
            timeZone,
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
        }).formatToParts(date);
        const byType = Object.fromEntries(parts.map((part) => [part.type, part.value]));
        if (byType.year && byType.month && byType.day) {
            return `${byType.year}-${byType.month}-${byType.day}`;
        }
    }
    catch {
        // Fall back to UTC below for invalid host timezone settings.
    }
    return date.toISOString().slice(0, 10);
}
function normalizeIssueIdentityPart(value) {
    return String(value || '')
        .trim()
        .toLowerCase()
        .replace(/\s+/g, ' ');
}
function buildDailyIssueKey(issue) {
    const stableIdentity = [
        issueSourceUrl(issue),
        issue?.source_url,
        issue?.sourceUrl,
        issue?.issue_url,
        issue?.issueUrl,
        issue?.signal_id,
        issue?.signalId,
        issue?.id,
    ]
        .map((value) => String(value || '').trim())
        .find(Boolean);
    const fallbackIdentity = [
        issueProjectLabel(issue),
        issue?.source,
        issue?.area,
        issue?.title,
    ]
        .map(normalizeIssueIdentityPart)
        .filter(Boolean)
        .join('|');
    return sha256(stableIdentity || fallbackIdentity || stableStringify(issue));
}
function coerceIssueNumber(value) {
    if (value === null || value === undefined || value === '')
        return null;
    if (typeof value === 'number')
        return Number.isFinite(value) ? value : null;
    const normalized = String(value).replace(/,/g, '').trim();
    if (!normalized)
        return null;
    const number = Number(normalized);
    return Number.isFinite(number) ? number : null;
}
function issueEventCount(issue) {
    const direct = [
        issue?.events,
        issue?.eventCount,
        issue?.event_count,
        issue?.current_value,
        issue?.currentValue,
        issue?.count,
    ];
    for (const value of direct) {
        const number = coerceIssueNumber(value);
        if (number !== null)
            return number;
    }
    const text = [
        issue?.impact,
        issue?.summary,
        ...(Array.isArray(issue?.evidence) ? issue.evidence : []),
        issue?.body,
    ]
        .filter(Boolean)
        .join('\n');
    const match = text.match(/\bEvents?:\s*([0-9][0-9,]*(?:\.[0-9]+)?)/i);
    return match ? coerceIssueNumber(match[1]) : null;
}
function isDrasticDailyIssueEventGrowth(currentEvents, previousEntry, dedupeConfig) {
    if (currentEvents === null || currentEvents === undefined)
        return false;
    const previousEvents = coerceIssueNumber(previousEntry?.lastReportedEvents ?? previousEntry?.lastSeenEvents);
    if (previousEvents === null || previousEvents < 0)
        return false;
    const requiredEvents = Math.max(previousEvents * dedupeConfig.eventGrowthMultiplier, previousEvents + dedupeConfig.eventGrowthMinDelta);
    return currentEvents >= requiredEvents;
}
function applyDailyIssueDedupe(issuesPayload, state, config, activeCadences, now = new Date()) {
    const issues = Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [];
    const dedupeConfig = getDailyIssueDedupeConfig(config);
    if (!dedupeConfig.enabled || !isShortOperationalCadence(activeCadences) || issues.length === 0) {
        return {
            issuesPayload,
            dailyIssueReports: state?.dailyIssueReports || null,
            suppressedCount: 0,
            reportedCount: issues.length,
            hasDrasticEventGrowth: false,
        };
    }
    const timeZone = resolveDailyIssueDedupeTimeZone(config);
    const date = formatDateInTimeZone(now, timeZone);
    const nowIso = now.toISOString();
    const previousState = state?.dailyIssueReports?.date === date ? state.dailyIssueReports : null;
    const previousIssues = previousState?.issues && typeof previousState.issues === 'object'
        ? previousState.issues
        : {};
    const nextIssues = { ...previousIssues };
    const reportableIssues = [];
    let suppressedCount = 0;
    let hasDrasticEventGrowth = false;
    for (const issue of issues) {
        const key = buildDailyIssueKey(issue);
        const previousEntry = previousIssues[key] || null;
        const events = issueEventCount(issue);
        const shouldReport = !previousEntry || isDrasticDailyIssueEventGrowth(events, previousEntry, dedupeConfig);
        const reportReason = !previousEntry ? 'new_daily_issue' : 'event_growth';
        const nextEntry = {
            ...(previousEntry || {}),
            title: String(issue?.title || previousEntry?.title || '').slice(0, 240),
            app: issueProjectLabel(issue),
            sourceUrl: issueSourceUrl(issue) || previousEntry?.sourceUrl || null,
            lastSeenAt: nowIso,
            lastSeenEvents: events ?? previousEntry?.lastSeenEvents ?? null,
        };
        if (shouldReport) {
            reportableIssues.push(issue);
            if (previousEntry)
                hasDrasticEventGrowth = true;
            nextEntry.lastReportedAt = nowIso;
            nextEntry.lastReportedEvents = events ?? previousEntry?.lastReportedEvents ?? null;
            nextEntry.lastReportReason = reportReason;
            nextEntry.reportCount = Number(previousEntry?.reportCount || 0) + 1;
        }
        else {
            suppressedCount += 1;
            nextEntry.suppressedCount = Number(previousEntry?.suppressedCount || 0) + 1;
        }
        nextIssues[key] = nextEntry;
    }
    return {
        issuesPayload: {
            ...issuesPayload,
            issue_count: reportableIssues.length,
            issues: reportableIssues,
            suppressed_issue_count: suppressedCount,
            daily_issue_dedupe: {
                date,
                timeZone,
                suppressedCount,
                reportedCount: reportableIssues.length,
                eventGrowthMultiplier: dedupeConfig.eventGrowthMultiplier,
                eventGrowthMinDelta: dedupeConfig.eventGrowthMinDelta,
            },
        },
        dailyIssueReports: {
            date,
            timeZone,
            issues: nextIssues,
            updatedAt: nowIso,
        },
        suppressedCount,
        reportedCount: reportableIssues.length,
        hasDrasticEventGrowth,
    };
}
async function deliverConnectorHealthAlert({ config, configPath, message, statusPayload, unhealthyConnectors, fingerprint }) {
    const channels = getConnectorHealthChannels(config);
    if (config?.notifications?.connectorHealth?.enabled === false) {
        return [{ sent: false, target: 'notifications', detail: 'connector health notifications disabled' }];
    }
    if (channels.length === 0) {
        return [{ sent: false, target: 'none', detail: 'no connector health notification channels configured' }];
    }
    const results = [];
    for (const channel of channels) {
        try {
            if (channel.type === 'openclaw-chat') {
                results.push(await writeConfiguredOpenClawChatAlert(configPath, channel, message, statusPayload, unhealthyConnectors, fingerprint));
            }
            else if (channel.type === 'slack') {
                results.push(await sendSlackConnectorHealthAlert(channel, message));
            }
            else if (channel.type === 'webhook') {
                results.push(await sendWebhookConnectorHealthAlert(channel, message, statusPayload, unhealthyConnectors, fingerprint));
            }
            else if (channel.type === 'discord') {
                results.push(await sendDiscordConnectorHealthAlert(channel, message, statusPayload, unhealthyConnectors, fingerprint));
            }
            else if (channel.type === 'command') {
                results.push(await sendCommandConnectorHealthAlert(channel, message));
            }
            else {
                results.push({ sent: false, target: channel.label || String(channel.type || 'unknown'), detail: 'unsupported channel type' });
            }
        }
        catch (error) {
            results.push({
                sent: false,
                target: channel.label || String(channel.type || 'unknown'),
                detail: error instanceof Error ? error.message : String(error),
            });
        }
    }
    if (!hasSuccessfulExternalDelivery(results)) {
        results.push({
            sent: false,
            external: true,
            target: 'external_notification',
            detail: hasExternalNotificationChannel(channels)
                ? 'No external notification channel successfully sent the alert.'
                : 'Alert written locally, but no external notification channel configured.',
        });
    }
    return results;
}
function getGrowthRunChannels(config) {
    const configuredChannels = Array.isArray(config?.notifications?.growthRun?.channels)
        ? config.notifications.growthRun.channels
        : [];
    return mergeNotificationChannelsWithDeliveries(configuredChannels, getDeliveryNotificationChannels(config, 'growthRun'));
}
async function readChartAttachments(chartManifestPath) {
    if (!chartManifestPath)
        return [];
    try {
        const manifest = await readJson(chartManifestPath);
        return Array.isArray(manifest?.charts)
            ? manifest.charts
                .map((chart) => ({
                signalId: String(chart.signal_id || chart.signalId || '').trim(),
                filePath: String(chart.file_path || chart.filePath || '').trim(),
                caption: String(chart.caption || chart.title || 'Data chart').trim(),
            }))
                .filter((chart) => chart.filePath)
            : [];
    }
    catch {
        return [];
    }
}
function buildGrowthRunSummaryMessage({ issuesPayload, activeCadences, sourceFiles, createdGitHubArtifact, charts = [] }) {
    const issueCount = Number(issuesPayload?.issue_count || 0);
    const cadenceNames = activeCadences.length > 0
        ? activeCadences.map((cadence) => cadence.title || cadence.key).join(', ')
        : 'ad-hoc growth pass';
    const sourceNames = Object.keys(sourceFiles || {}).sort().join(', ') || 'none';
    const issues = Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [];
    if (isShortOperationalCadence(activeCadences)) {
        const heading = activeCadences.some((cadence) => String(cadence?.key) === 'healthcheck')
            ? 'OpenClaw healthcheck'
            : 'OpenClaw daily';
        const lines = [
            `${heading}: ${issueCount > 0 ? `${issueCount} finding(s)` : 'OK'}`,
        ];
        if (issueCount > 0) {
            const groupedIssues = groupIssuesByProject(issues, 4);
            if (groupedIssues.length > 0) {
                lines.push('Top by project:');
                for (const [project, projectIssues] of groupedIssues) {
                    const formatted = projectIssues.map((issue) => formatIssueSummaryLine(issue, 84)).filter(Boolean);
                    if (formatted.length > 0)
                        lines.push(`- ${project}: ${formatted.join(' | ')}`);
                }
            }
            lines.push(createdGitHubArtifact
                ? 'Action: GitHub artifact attempted.'
                : 'Action: external alert only.');
        }
        const suppressedIssueCount = Number(issuesPayload?.suppressed_issue_count || 0);
        if (suppressedIssueCount > 0) {
            lines.push(`Suppressed today: ${suppressedIssueCount} previously reported finding(s).`);
        }
        if (charts.length > 0) {
            lines.push(`Charts: ${charts.length}`);
        }
        return `${lines.join('\n')}\n`;
    }
    const lines = [
        `OpenClaw Growth run finished (${new Date().toISOString()}).`,
        `Cadence: ${cadenceNames}`,
        `Sources inspected: ${sourceNames}`,
        `Generated proposals: ${issueCount}`,
    ];
    if (issuesPayload?.summary) {
        lines.push(`Summary: ${issuesPayload.summary}`);
    }
    if (createdGitHubArtifact) {
        lines.push('GitHub artifact creation was attempted for the generated proposals.');
    }
    if (charts.length > 0) {
        lines.push(`Charts generated: ${charts.length}`);
        for (const chart of charts.slice(0, 5)) {
            lines.push(`- ${chart.caption}: ${chart.filePath}`);
        }
    }
    const topIssues = issues.slice(0, isDeepAnalysisCadence(activeCadences) ? 5 : 3);
    if (topIssues.length > 0) {
        lines.push('');
        lines.push(isDeepAnalysisCadence(activeCadences) ? 'App-by-app findings and next steps:' : 'Top findings:');
        for (const issue of topIssues) {
            lines.push(`- ${issue.title} (${issue.priority || 'medium'}, ${issue.area || 'general'})`);
            if (isDeepAnalysisCadence(activeCadences)) {
                for (const evidence of firstEvidenceLines(issue, 2)) {
                    lines.push(`  Evidence: ${evidence}`);
                }
                if (issue.expected_impact) {
                    lines.push(`  Impact: ${issue.expected_impact}`);
                }
            }
        }
    }
    lines.push('');
    lines.push(isDeepAnalysisCadence(activeCadences)
        ? 'No secrets were included. Full details are in the generated issue drafts, charts, and OpenClaw chat handoff.'
        : 'No secrets were included.');
    return `${lines.join('\n')}\n`;
}
function growthRunTitle(activeCadences) {
    if (isShortOperationalCadence(activeCadences)) {
        return activeCadences.some((cadence) => String(cadence?.key) === 'healthcheck')
            ? 'OpenClaw healthcheck'
            : 'OpenClaw daily';
    }
    if (isDeepAnalysisCadence(activeCadences))
        return 'OpenClaw growth review';
    return 'OpenClaw growth run';
}
function buildDiscordGrowthRunPayload(message, issuesPayload, activeCadences, sourceFiles, fingerprint, createdGitHubArtifact, charts = []) {
    const issues = Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [];
    const issueCount = Number(issuesPayload?.issue_count || 0);
    const fields = [
        discordField('Cadence', activeCadences.length > 0
            ? activeCadences.map((cadence) => cadence.title || cadence.key).join(', ')
            : 'ad-hoc growth pass', false),
        discordField('Sources', Object.keys(sourceFiles || {}).sort().join(', ') || 'none', true),
        discordField('Findings', String(issueCount), true),
    ];
    if (createdGitHubArtifact) {
        fields.push(discordField('Action', 'GitHub artifact creation was attempted.', true));
    }
    const suppressedIssueCount = Number(issuesPayload?.suppressed_issue_count || 0);
    if (suppressedIssueCount > 0) {
        fields.push(discordField('Suppressed today', `${suppressedIssueCount} previously reported finding(s).`, true));
    }
    if (charts.length > 0) {
        fields.push(discordField('Charts', String(charts.length), true));
    }
    const groupedIssues = isShortOperationalCadence(activeCadences)
        ? groupIssuesByProject(issues, 4).map(([project, projectIssues]) => ({
            name: project,
            value: projectIssues.map((issue) => formatIssueSummaryLine(issue, 84)).filter(Boolean).join('\n'),
        }))
        : issues.slice(0, isDeepAnalysisCadence(activeCadences) ? 5 : 3).map((issue) => ({
            name: `${issue.priority || 'medium'} • ${issue.area || 'general'}`,
            value: formatIssueSummaryLine(issue, 96),
        }));
    for (const entry of groupedIssues) {
        if (entry.value)
            fields.push(discordField(entry.name, entry.value));
    }
    const summary = String(issuesPayload?.summary || '').trim();
    return {
        content: '',
        embeds: [
            {
                title: `${growthRunTitle(activeCadences)}: ${issueCount > 0 ? `${issueCount} finding(s)` : 'OK'}`,
                description: discordTruncate(summary || 'No secrets were included.', 500),
                color: issueCount > 0 ? 0xf79009 : 0x12b76a,
                fields: fields.slice(0, 20),
                footer: {
                    text: `GROWTH_RUN • ${String(fingerprint || '').slice(0, 12)}`,
                },
                timestamp: new Date().toISOString(),
            },
        ],
        fallbackText: message,
    };
}
async function writeConfiguredOpenClawChatGrowthSummary(configPath, channel, message, issuesPayload, activeCadences, fingerprint, charts) {
    const markdownPath = resolveOpenClawChatDeliveryPath(channel.markdownPath, '.openclaw/chat/growth-summary.md');
    const jsonPath = resolveOpenClawChatDeliveryPath(channel.jsonPath, '.openclaw/chat/growth-summary.json');
    await fs.mkdir(path.dirname(markdownPath), { recursive: true });
    await fs.mkdir(path.dirname(jsonPath), { recursive: true });
    await fs.writeFile(markdownPath, message, 'utf8');
    await fs.writeFile(jsonPath, JSON.stringify({
        channel: channel.label || 'openclaw_chat',
        generatedAt: new Date().toISOString(),
        fingerprint,
        activeCadences,
        issueCount: Number(issuesPayload?.issue_count || 0),
        issues: Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [],
        charts,
        attachments: charts.map((chart) => ({
            type: 'image/png',
            path: chart.filePath,
            caption: chart.caption,
        })),
    }, null, 2), 'utf8');
    return {
        sent: true,
        external: false,
        target: channel.label || 'openclaw_chat',
        detail: `wrote local OpenClaw chat outbox ${markdownPath} and ${jsonPath}`,
    };
}
async function sendSlackGrowthSummary(channel, message) {
    const webhookEnv = channel.webhookEnv || 'SLACK_WEBHOOK_URL';
    const webhookUrl = process.env[webhookEnv];
    if (!webhookUrl) {
        return { sent: false, target: channel.label || 'slack', detail: `${webhookEnv} not set` };
    }
    const response = await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ text: message }),
    });
    return {
        sent: response.ok,
        external: true,
        target: channel.label || 'slack',
        detail: response.ok ? `HTTP ${response.status}` : `HTTP ${response.status}: ${await response.text()}`,
    };
}
async function sendWebhookGrowthSummary(channel, message, issuesPayload, activeCadences, fingerprint, charts) {
    const urlEnv = channel.urlEnv || channel.webhookEnv || 'OPENCLAW_WEBHOOK_URL';
    const webhookUrl = process.env[urlEnv];
    if (!webhookUrl) {
        return { sent: false, target: channel.label || 'webhook', detail: `${urlEnv} not set` };
    }
    const response = await fetch(webhookUrl, {
        method: channel.method || 'POST',
        headers: {
            'content-type': 'application/json',
            ...(channel.headers || {}),
        },
        body: JSON.stringify({
            type: 'openclaw.growth_run',
            generatedAt: new Date().toISOString(),
            text: message,
            fingerprint,
            activeCadences,
            issueCount: Number(issuesPayload?.issue_count || 0),
            issues: Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [],
            charts,
            attachments: charts.map((chart) => ({
                type: 'image/png',
                path: chart.filePath,
                caption: chart.caption,
            })),
        }),
    });
    return {
        sent: response.ok,
        external: true,
        target: channel.label || 'webhook',
        detail: response.ok ? `HTTP ${response.status}` : `HTTP ${response.status}: ${await response.text()}`,
    };
}
async function sendCommandGrowthSummary(channel, message) {
    if (!channel.command) {
        return { sent: false, target: channel.label || 'command', detail: 'command not configured' };
    }
    const result = await runShellCommand(String(channel.command), 60_000, { input: message });
    return {
        sent: result.ok,
        external: true,
        target: channel.label || 'command',
        detail: result.ok ? 'sent' : result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
    };
}
async function sendDiscordGrowthSummary(channel, message, issuesPayload, activeCadences, sourceFiles, fingerprint, createdGitHubArtifact, charts) {
    if (!channel.command) {
        return { sent: false, target: channel.label || 'discord', detail: 'discord command not configured' };
    }
    const payload = buildDiscordGrowthRunPayload(message, issuesPayload, activeCadences, sourceFiles, fingerprint, createdGitHubArtifact, charts);
    const result = await runShellCommand(String(channel.command), 60_000, {
        input: JSON.stringify(payload),
        env: { OPENCLAW_DISCORD_DELIVERY_FORMAT: 'embed' },
    });
    return {
        sent: result.ok,
        external: true,
        target: channel.label || 'discord',
        detail: result.ok ? 'sent' : result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
    };
}
async function deliverGrowthRunSummary({ config, configPath, issuesPayload, activeCadences, sourceFiles, fingerprint, createdGitHubArtifact, chartManifestPath, }) {
    if (config?.notifications?.growthRun?.enabled === false) {
        return [{ sent: false, target: 'notifications', detail: 'growth run notifications disabled' }];
    }
    const channels = getGrowthRunChannels(config);
    if (channels.length === 0) {
        return [{ sent: false, target: 'none', detail: 'no growth run notification channels configured' }];
    }
    const charts = await readChartAttachments(chartManifestPath);
    const message = buildGrowthRunSummaryMessage({
        issuesPayload,
        activeCadences,
        sourceFiles,
        createdGitHubArtifact,
        charts,
    });
    const results = [];
    for (const channel of channels) {
        try {
            if (channel.type === 'openclaw-chat') {
                results.push(await writeConfiguredOpenClawChatGrowthSummary(configPath, channel, message, issuesPayload, activeCadences, fingerprint, charts));
            }
            else if (channel.type === 'slack') {
                results.push(await sendSlackGrowthSummary(channel, message));
            }
            else if (channel.type === 'webhook') {
                results.push(await sendWebhookGrowthSummary(channel, message, issuesPayload, activeCadences, fingerprint, charts));
            }
            else if (channel.type === 'discord') {
                results.push(await sendDiscordGrowthSummary(channel, message, issuesPayload, activeCadences, sourceFiles, fingerprint, createdGitHubArtifact, charts));
            }
            else if (channel.type === 'command') {
                results.push(await sendCommandGrowthSummary(channel, message));
            }
            else {
                results.push({ sent: false, target: channel.label || String(channel.type || 'unknown'), detail: 'unsupported channel type' });
            }
        }
        catch (error) {
            results.push({
                sent: false,
                target: channel.label || String(channel.type || 'unknown'),
                detail: error instanceof Error ? error.message : String(error),
            });
        }
    }
    return results;
}
async function maybeRunConnectorHealthCheck({ config, configPath, state, statePath, runtimeDir }) {
    const healthState = state?.connectorHealth || {};
    const intervalMinutes = getConnectorHealthIntervalMinutes(config);
    if (!isDue(healthState.lastCheckedAt, intervalMinutes)) {
        await appendSchedulerProof('connector_health_not_due', {
            configPath,
            statePath,
            intervalMinutes,
            lastCheckedAt: healthState.lastCheckedAt || null,
            persistedLastStatusOk: healthState.lastStatusOk !== false,
            activeIncidentFingerprint: healthState.activeIncidentFingerprint || null,
            socialOutput: 'HEARTBEAT_OK',
            socialReason: 'connector health was not due; persisted unhealthy state is not a new event',
        });
        return state;
    }
    await ensureDir(runtimeDir);
    const statusCommand = [
        nodeRuntimeScriptCommand('openclaw-growth-status.mjs'),
        '--config',
        quote(configPath),
        '--timeout-ms',
        '15000',
        '--json',
    ].join(' ');
    const checkedAt = new Date().toISOString();
    const statusResult = await runShellCommand(statusCommand, 90_000);
    const statusPayload = parseJsonFromStdout(statusResult.stdout);
    if (!statusPayload) {
        const nextState = {
            ...state,
            connectorHealth: {
                ...healthState,
                lastCheckedAt: checkedAt,
                lastError: statusResult.stderr.trim() || statusResult.stdout.trim() || 'connector status returned no JSON',
            },
        };
        await fs.mkdir(path.dirname(statePath), { recursive: true });
        await fs.writeFile(statePath, JSON.stringify(nextState, null, 2), 'utf8');
        await appendSchedulerProof('connector_health_check_failed', {
            configPath,
            statePath,
            intervalMinutes,
            checkedAt,
            error: nextState.connectorHealth.lastError,
        });
        return nextState;
    }
    const unhealthyConnectors = getUnhealthyConfiguredConnectors(statusPayload);
    const connectedConnectors = getConnectedConnectorKeys(statusPayload);
    const fingerprint = buildConnectorHealthFingerprint(unhealthyConnectors);
    const nextHealthState = {
        ...healthState,
        lastCheckedAt: checkedAt,
        lastStatusOk: unhealthyConnectors.length === 0,
        lastFingerprint: fingerprint,
        connectedConnectors,
        lastError: null,
    };
    const previousExternallyDeliveredFingerprint = healthState.lastExternalAlertedFingerprint || null;
    let alertTriggered = false;
    let alertDeliveries = [];
    if (unhealthyConnectors.length === 0) {
        nextHealthState.activeIncidentFingerprint = null;
        nextHealthState.lastExternalAlertedFingerprint = null;
        if (healthState.lastStatusOk === false) {
            nextHealthState.lastRecoveredAt = checkedAt;
        }
    }
    else {
        nextHealthState.activeIncidentFingerprint = fingerprint;
    }
    if (unhealthyConnectors.length > 0 &&
        previousExternallyDeliveredFingerprint !== fingerprint) {
        const message = buildConnectorHealthAlert(statusPayload, unhealthyConnectors);
        const paths = await writeConnectorHealthAlert(runtimeDir, message, statusPayload, unhealthyConnectors, fingerprint);
        const deliveries = await deliverConnectorHealthAlert({
            config,
            configPath,
            message,
            statusPayload,
            unhealthyConnectors,
            fingerprint,
        });
        alertTriggered = true;
        alertDeliveries = deliveries;
        nextHealthState.lastAlertedAt = checkedAt;
        nextHealthState.lastAlertedFingerprint = fingerprint;
        nextHealthState.lastAlertMarkdownPath = paths.markdownPath;
        nextHealthState.lastAlertJsonPath = paths.jsonPath;
        nextHealthState.lastAlertDeliveries = deliveries;
        nextHealthState.lastAlertExternalSent = hasSuccessfulExternalDelivery(deliveries);
        if (nextHealthState.lastAlertExternalSent) {
            nextHealthState.lastExternalAlertedAt = checkedAt;
            nextHealthState.lastExternalAlertedFingerprint = fingerprint;
        }
    }
    const nextState = {
        ...state,
        connectorHealth: nextHealthState,
    };
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await fs.writeFile(statePath, JSON.stringify(nextState, null, 2), 'utf8');
    await appendSchedulerProof('connector_health_checked', {
        configPath,
        statePath,
        intervalMinutes,
        checkedAt,
        lastStatusOk: nextHealthState.lastStatusOk,
        connectedConnectors,
        unhealthyConnectors: unhealthyConnectors.map((entry) => ({
            key: entry.key,
            status: entry.status,
            detail: entry.detail,
        })),
        alertMarkdownPath: nextHealthState.lastAlertMarkdownPath || null,
        alertTriggered,
        deliveryCount: alertDeliveries.length,
        externalDeliverySent: alertTriggered ? hasSuccessfulExternalDelivery(alertDeliveries) : false,
        socialOutput: alertTriggered ? 'CONNECTOR_HEALTH_ALERT' : 'HEARTBEAT_OK',
        socialReason: alertTriggered
            ? 'new or changed connector-health incident'
            : unhealthyConnectors.length > 0
                ? 'connector-health incident unchanged'
                : healthState.lastStatusOk === false
                    ? 'connector health recovered'
                    : 'connector health unchanged healthy',
    });
    if (unhealthyConnectors.length > 0 && !alertTriggered) {
        await appendSchedulerProof('connector_health_unchanged', {
            configPath,
            statePath,
            checkedAt,
            fingerprint,
            socialOutput: 'HEARTBEAT_OK',
        });
    }
    return nextState;
}
function buildIssueFingerprint(issuesPayload) {
    const titles = Array.isArray(issuesPayload?.issues)
        ? issuesPayload.issues.map((issue) => `${issue.title}|${issue.priority}|${issue.area}`).sort()
        : [];
    return sha256(titles.join('\n'));
}
function isShortOperationalCadence(cadences) {
    if (!Array.isArray(cadences) || cadences.length === 0)
        return false;
    return cadences.every((cadence) => {
        const key = String(cadence?.key || '').toLowerCase();
        return key === 'healthcheck' || key === 'daily' || cadence?.criticalOnly === true;
    });
}
function isDeepAnalysisCadence(cadences) {
    if (!Array.isArray(cadences))
        return false;
    return cadences.some((cadence) => ['weekly', 'monthly', 'quarterly', 'six_months', 'yearly'].includes(String(cadence?.key || '').toLowerCase()));
}
function firstEvidenceLines(issue, maxLines = 2) {
    const body = String(issue?.body || '');
    const evidenceMatch = body.match(/## Evidence\n([\s\S]*?)(?:\n## |\n?$)/);
    if (!evidenceMatch)
        return [];
    return evidenceMatch[1]
        .split('\n')
        .map((line) => line.replace(/^-\s*/, '').trim())
        .filter(Boolean)
        .slice(0, maxLines);
}
async function runAnalyzer({ config, runtimeDir, sourceFiles, createGitHubArtifact, githubArtifactMode = getActionMode(config), chartManifestPath, cadencePlanPath, }) {
    await ensureDir(runtimeDir);
    if (!sourceFiles.analytics) {
        throw new Error('Analytics source is required (enable and configure `sources.analytics`).');
    }
    const outFile = path.resolve(config.project?.outFile || 'data/openclaw-growth-engineer/issues.generated.json');
    const args = [
        resolveRuntimeScriptPath('openclaw-growth-engineer.mjs'),
        '--analytics',
        sourceFiles.analytics,
        '--repo-root',
        path.resolve(config.project?.repoRoot || '.'),
        '--out',
        outFile,
        '--max-issues',
        String(config.project?.maxIssues || 4),
        '--title-prefix',
        String(config.project?.titlePrefix || '[Growth]'),
    ];
    if (sourceFiles.revenuecat) {
        args.push('--revenuecat', sourceFiles.revenuecat);
    }
    if (sourceFiles.paddle) {
        args.push('--source', `paddle=${sourceFiles.paddle}`);
    }
    if (sourceFiles.seo) {
        args.push('--source', `seo=${sourceFiles.seo}`);
    }
    if (sourceFiles.sentry) {
        args.push('--sentry', sourceFiles.sentry);
    }
    if (sourceFiles.coolify) {
        args.push('--source', `coolify=${sourceFiles.coolify}`);
    }
    if (sourceFiles.feedback) {
        args.push('--feedback', sourceFiles.feedback);
    }
    for (const source of getAllSourceEntries(config).filter((entry) => !entry.builtIn)) {
        if (sourceFiles[source.key]) {
            args.push('--source', `${source.key}=${sourceFiles[source.key]}`);
        }
    }
    if (createGitHubArtifact) {
        const repo = String(config.project?.githubRepo || '').trim();
        args.push(githubArtifactMode === 'pull_request' ? '--create-pull-requests' : '--create-issues', '--repo', repo);
        if (githubArtifactMode === 'pull_request') {
            args.push('--allow-proposal-pull-requests');
        }
        const labels = Array.isArray(config.project?.labels) ? config.project.labels : [];
        if (labels.length > 0) {
            args.push('--labels', labels.join(','));
        }
        if (config.actions?.proposalBranchPrefix) {
            args.push('--branch-prefix', String(config.actions.proposalBranchPrefix));
        }
        if (config.actions?.draftPullRequests === false) {
            args.push('--no-draft-pull-requests');
        }
    }
    if (chartManifestPath) {
        args.push('--chart-manifest', chartManifestPath);
    }
    if (cadencePlanPath) {
        args.push('--cadence-plan', cadencePlanPath);
    }
    const analyzer = await runShellCommand(`node ${args.map(quote).join(' ')}`);
    if (!analyzer.ok) {
        throw new Error(`Analyzer failed: ${analyzer.stderr || `exit ${analyzer.code}`}`);
    }
    const issuesPayload = await readJson(outFile);
    return {
        outFile,
        sourceFiles,
        issuesPayload,
        analyzerStdout: analyzer.stdout.trim(),
    };
}
async function maybeGenerateCharts({ config, payloads, runtimeDir, activeCadences }) {
    if (!config.charting?.enabled) {
        return null;
    }
    if (!isDeepAnalysisCadence(activeCadences)) {
        return null;
    }
    const analyticsPayload = payloads.analytics;
    if (!analyticsPayload) {
        return null;
    }
    await ensureDir(runtimeDir);
    const chartsDir = path.join(runtimeDir, 'charts');
    await ensureDir(chartsDir);
    const analyticsForChartsPath = path.join(runtimeDir, 'analytics_for_charts.json');
    const manifestPath = path.join(chartsDir, 'manifest.json');
    await fs.writeFile(analyticsForChartsPath, JSON.stringify(analyticsPayload, null, 2), 'utf8');
    const defaultCommand = [
        'python3',
        resolveRuntimeScriptPath('openclaw-growth-charts.py'),
        '--analytics',
        analyticsForChartsPath,
        '--out-dir',
        chartsDir,
        '--manifest',
        manifestPath,
    ]
        .map(quote)
        .join(' ');
    const command = String(config.charting?.command || defaultCommand);
    const result = await runShellCommand(command);
    if (!result.ok) {
        process.stderr.write(`[${new Date().toISOString()}] Chart generation failed: ${result.stderr || `exit ${result.code}`}\n`);
        return null;
    }
    return manifestPath;
}
function quote(value) {
    if (/^[a-zA-Z0-9_./:-]+$/.test(value)) {
        return value;
    }
    return `'${String(value).replace(/'/g, `'\\''`)}'`;
}
function computeSourceHashes(sourcePayloadMap) {
    const hashes = {};
    for (const [key, value] of Object.entries(sourcePayloadMap)) {
        hashes[key] = sha256(stableStringify(value));
    }
    return hashes;
}
function normalizeLookback(value, fallback = '30d') {
    const normalized = String(value || fallback).trim();
    return /^[0-9]+[dhm]$/.test(normalized) ? normalized : fallback;
}
function commandHasExplicitTimeBounds(command) {
    return /(^|\s)--(?:since|until|last)\b/.test(String(command));
}
function resolveCursorAwareCommand(command, sourceConfig, cursorState) {
    const rawCommand = String(command || '').trim();
    if (!rawCommand) {
        return rawCommand;
    }
    if (sourceConfig?.cursorMode !== 'auto_since_last_fetch') {
        return rawCommand;
    }
    if (commandHasExplicitTimeBounds(rawCommand)) {
        return rawCommand;
    }
    const lastCollectedAt = String(cursorState?.lastCollectedAt || '').trim();
    if (lastCollectedAt) {
        return `${rawCommand} --since ${quote(lastCollectedAt)}`;
    }
    const lookback = normalizeLookback(sourceConfig?.initialLookback, '30d');
    return `${rawCommand} --last ${quote(lookback)}`;
}
async function resolveSourcePayloadWithCursor(sourceConfig, sourceName, cursorState, commandCwd = process.cwd(), configPath = null) {
    if (!sourceConfig || sourceConfig.enabled === false) {
        return {
            payload: null,
            nextCursor: cursorState || null,
            resolvedCommand: null,
            failure: null,
        };
    }
    if (sourceConfig.mode === 'command') {
        if (!sourceConfig.command) {
            throw new Error(`Source "${sourceName}" has mode=command but no command configured.`);
        }
        const resolvedCommand = resolveCursorAwareCommand(withActiveConfigArg(replaceLegacyRuntimeScriptCommand(sourceConfig.command), configPath), sourceConfig, cursorState);
        let result = await runShellCommand(String(resolvedCommand), 120_000, { cwd: commandCwd });
        let retried = false;
        if (!result.ok && isTransientNetworkFailure(result.stderr || result.stdout)) {
            retried = true;
            await sleep(1_500);
            result = await runShellCommand(String(resolvedCommand), 120_000, { cwd: commandCwd });
        }
        if (!result.ok) {
            const detail = `${retried ? 'transient network error persisted after retry: ' : ''}${result.stderr || `exit ${result.code}`}`;
            if (shouldDegradeTransientSourceFailure(sourceConfig, sourceName, retried)) {
                return {
                    payload: null,
                    nextCursor: cursorState || null,
                    resolvedCommand,
                    failure: {
                        key: sourceName,
                        label: sourceConfig.label || sourceName,
                        service: sourceConfig.service || sourceName,
                        source: sourceName,
                        transient: true,
                        retryable: true,
                        retried: true,
                        at: new Date().toISOString(),
                        detail,
                    },
                };
            }
            throw new Error(buildSourceCommandFailureMessage(sourceName, resolvedCommand, detail));
        }
        const fetchedAt = new Date().toISOString();
        try {
            return {
                payload: JSON.parse(result.stdout),
                nextCursor: sourceConfig.cursorMode === 'auto_since_last_fetch'
                    ? {
                        lastCollectedAt: fetchedAt,
                        updatedAt: fetchedAt,
                        lastCommand: resolvedCommand,
                        lastRetriedTransientFailureAt: retried ? fetchedAt : null,
                    }
                    : cursorState || null,
                resolvedCommand,
                failure: null,
            };
        }
        catch {
            throw new Error(`Source "${sourceName}" returned non-JSON output.`);
        }
    }
    if (!sourceConfig.path) {
        throw new Error(`Source "${sourceName}" has mode=file but no path configured.`);
    }
    return {
        payload: await readJson(path.resolve(String(sourceConfig.path))),
        nextCursor: cursorState || null,
        resolvedCommand: null,
        failure: null,
    };
}
async function loadSourcePayloads(config, state, configPath) {
    const payloads = {};
    const sourceCursors = { ...(state?.sourceCursors || {}) };
    const sourceFailures = [];
    const commandCwd = getProjectCommandCwd(config);
    for (const source of getAllSourceEntries(config)) {
        const currentCursor = sourceCursors[source.key] || null;
        let result;
        try {
            result = await resolveSourcePayloadWithCursor(source, source.key, currentCursor, commandCwd, configPath);
        }
        catch (error) {
            if (source.key === 'analytics') {
                throw error;
            }
            const detail = error instanceof Error ? error.message : String(error);
            sourceFailures.push({
                key: source.key,
                label: source.label || source.key,
                service: source.service || source.key,
                detail,
                retryable: isTransientNetworkFailure(detail),
                failedAt: new Date().toISOString(),
            });
            process.stderr.write(`[${new Date().toISOString()}] Optional source "${source.key}" failed; continuing without it: ${detail}\n`);
            continue;
        }
        const payload = result.payload;
        if (payload) {
            payloads[source.key] = payload;
        }
        if (result.nextCursor) {
            sourceCursors[source.key] = result.nextCursor;
        }
        if (result.failure) {
            sourceFailures.push(result.failure);
            await appendSchedulerProof('source_collection_degraded', {
                configPath,
                source: result.failure.source,
                transient: result.failure.transient,
                retried: result.failure.retried,
                detail: result.failure.detail,
                socialOutput: 'HEARTBEAT_OK',
            });
        }
    }
    return {
        payloads,
        sourceCursors,
        sourceFailures,
    };
}
async function materializeSourceFiles(config, payloads, runtimeDir) {
    await ensureDir(runtimeDir);
    const sourceFiles = {};
    for (const source of getAllSourceEntries(config)) {
        const payload = payloads[source.key];
        if (!payload) {
            continue;
        }
        const filePath = path.join(runtimeDir, `${source.key}.json`);
        await fs.writeFile(filePath, JSON.stringify(payload, null, 2), 'utf8');
        sourceFiles[source.key] = filePath;
    }
    return sourceFiles;
}
function hasSourceChanges(previousHashes, currentHashes) {
    const allKeys = new Set([...Object.keys(previousHashes || {}), ...Object.keys(currentHashes || {})]);
    for (const key of allKeys) {
        if ((previousHashes || {})[key] !== (currentHashes || {})[key]) {
            return true;
        }
    }
    return false;
}
async function runOnce(configPath, statePath) {
    await appendSchedulerProof('runner_invoked', {
        configPath,
        statePath,
        argv: process.argv.slice(2),
    });
    const config = await readJson(configPath);
    const cronDeliveryRepair = await repairOpenClawCronDeliveryStore({
        configPath,
        config,
        readFile: fs.readFile,
        writeFile: fs.writeFile,
    });
    if (cronDeliveryRepair.repaired) {
        await appendSchedulerProof('openclaw_cron_delivery_repaired', {
            configPath,
            statePath,
            path: cronDeliveryRepair.path,
            repairedCount: cronDeliveryRepair.repairedCount,
        });
    }
    await applyOpenClawSecretRefs(config);
    const inferredGitHubRepo = await inferGitHubRepo(config);
    if (inferredGitHubRepo) {
        config.project = {
            ...(config.project || {}),
            githubRepo: inferredGitHubRepo,
        };
    }
    await assertHardRequirements(config);
    const state = await readJsonOptional(statePath, {
        sourceHashes: {},
        lastIssueFingerprint: null,
        lastRunAt: null,
        sourceCursors: {},
    });
    const runtimeDir = path.resolve(deriveRuntimeDirFromStatePath(statePath));
    const stateAfterHealthCheck = await maybeRunConnectorHealthCheck({
        config,
        configPath,
        state,
        statePath,
        runtimeDir,
    });
    const activeCadences = getDueCadences(config, stateAfterHealthCheck);
    const { payloads, sourceCursors, sourceFailures } = await loadSourcePayloads(config, stateAfterHealthCheck, configPath);
    const stateAfterSourceCollection = await recordSourceCollectionFailures({
        config,
        configPath,
        state: stateAfterHealthCheck,
        statePath,
        runtimeDir,
        sourceFailures,
    });
    const currentHashes = computeSourceHashes(payloads);
    if (activeCadences.length === 0) {
        process.stdout.write(`[${new Date().toISOString()}] No scheduled cadence due. Skip run.\n`);
        const completedAt = new Date().toISOString();
        await fs.mkdir(path.dirname(statePath), { recursive: true });
        await fs.writeFile(statePath, JSON.stringify({
            ...stateAfterHealthCheck,
            ...stateAfterSourceCollection,
            sourceHashes: currentHashes,
            sourceCursors,
            lastSourceFailures: sourceFailures,
            lastRunAt: completedAt,
            skippedReason: 'cadence_not_due',
        }, null, 2), 'utf8');
        await appendSchedulerProof('runner_completed', {
            configPath,
            statePath,
            completedAt,
            skippedReason: 'cadence_not_due',
            sourceFailures,
            socialOutput: 'HEARTBEAT_OK',
        });
        return;
    }
    const githubArtifactModes = getGitHubArtifactModes(config).filter((mode) => shouldAutoCreateGitHubArtifact(config, mode));
    const createGitHubArtifact = githubArtifactModes.length > 0 && Boolean(String(config.project?.githubRepo || '').trim());
    const sourceFiles = await materializeSourceFiles(config, payloads, runtimeDir);
    const cadencePlanPath = path.join(runtimeDir, 'cadence-plan.json');
    await fs.writeFile(cadencePlanPath, JSON.stringify({
        generatedAt: new Date().toISOString(),
        cadences: activeCadences,
    }, null, 2), 'utf8');
    const chartManifestPath = await maybeGenerateCharts({
        config,
        payloads,
        runtimeDir,
        activeCadences,
    });
    const dryRun = await runAnalyzer({
        config,
        runtimeDir,
        sourceFiles,
        createGitHubArtifact: false,
        chartManifestPath,
        cadencePlanPath,
    });
    const dailyIssueDedupe = applyDailyIssueDedupe(dryRun.issuesPayload, stateAfterSourceCollection, config, activeCadences);
    const deliverableIssuesPayload = dailyIssueDedupe.issuesPayload;
    const issueFingerprint = buildIssueFingerprint(deliverableIssuesPayload);
    const unchangedIssueSet = issueFingerprint === stateAfterSourceCollection.lastIssueFingerprint &&
        !dailyIssueDedupe.hasDrasticEventGrowth;
    if (Number(dryRun.issuesPayload?.issue_count || 0) > 0 &&
        Number(deliverableIssuesPayload?.issue_count || 0) === 0 &&
        dailyIssueDedupe.suppressedCount > 0) {
        process.stdout.write(`[${new Date().toISOString()}] All findings were already reported today. Skip GitHub creation and external growth notification.\n`);
        const completedAt = new Date().toISOString();
        await fs.mkdir(path.dirname(statePath), { recursive: true });
        await fs.writeFile(statePath, JSON.stringify({
            ...stateAfterHealthCheck,
            ...stateAfterSourceCollection,
            sourceHashes: currentHashes,
            sourceCursors,
            lastSourceFailures: sourceFailures,
            dailyIssueReports: dailyIssueDedupe.dailyIssueReports,
            lastIssueFingerprint: issueFingerprint,
            lastRunAt: completedAt,
            lastOutFile: dryRun.outFile,
            cadences: markCadencesRan(stateAfterSourceCollection, activeCadences, completedAt),
            lastGrowthRunNotifications: [
                {
                    sent: false,
                    target: 'growth_run',
                    detail: `all ${dailyIssueDedupe.suppressedCount} finding(s) already reported today; external growth notification suppressed`,
                },
            ],
            skippedReason: 'daily_issue_dedupe',
        }, null, 2), 'utf8');
        await appendSchedulerProof('runner_completed', {
            configPath,
            statePath,
            completedAt,
            skippedReason: 'daily_issue_dedupe',
            activeCadences: activeCadences.map((cadence) => cadence.key),
            outFile: dryRun.outFile,
            issueCount: Number(dryRun.issuesPayload?.issue_count || 0),
            suppressedIssueCount: dailyIssueDedupe.suppressedCount,
            sourceFailures,
            externalGrowthNotification: 'suppressed_daily_issue_dedupe',
            socialOutput: 'HEARTBEAT_OK',
        });
        return;
    }
    if (unchangedIssueSet &&
        config.schedule?.skipIfIssueSetUnchanged !== false) {
        process.stdout.write(`[${new Date().toISOString()}] Issue set unchanged. Skip GitHub creation and external growth notification.\n`);
        const completedAt = new Date().toISOString();
        await fs.mkdir(path.dirname(statePath), { recursive: true });
        await fs.writeFile(statePath, JSON.stringify({
            ...stateAfterHealthCheck,
            ...stateAfterSourceCollection,
            sourceHashes: currentHashes,
            sourceCursors,
            lastSourceFailures: sourceFailures,
            dailyIssueReports: dailyIssueDedupe.dailyIssueReports,
            lastIssueFingerprint: issueFingerprint,
            lastRunAt: completedAt,
            lastOutFile: dryRun.outFile,
            cadences: markCadencesRan(stateAfterSourceCollection, activeCadences, completedAt),
            lastGrowthRunNotifications: [
                {
                    sent: false,
                    target: 'growth_run',
                    detail: 'issue set unchanged; external growth notification suppressed',
                },
            ],
            skippedReason: 'issue_set_unchanged',
        }, null, 2), 'utf8');
        await appendSchedulerProof('runner_completed', {
            configPath,
            statePath,
            completedAt,
            skippedReason: 'issue_set_unchanged',
            activeCadences: activeCadences.map((cadence) => cadence.key),
            outFile: dryRun.outFile,
            issueCount: Number(dryRun.issuesPayload?.issue_count || 0),
            sourceFailures,
            externalGrowthNotification: 'suppressed_unchanged_issue_set',
            socialOutput: 'HEARTBEAT_OK',
        });
        return;
    }
    const issueSetChangedOrExplicitlyAllowed = !unchangedIssueSet || config.schedule?.skipIfIssueSetUnchanged === false;
    const shouldCreateGitHubArtifact = createGitHubArtifact &&
        Number(deliverableIssuesPayload?.issue_count || 0) > 0 &&
        issueSetChangedOrExplicitlyAllowed;
    if (shouldCreateGitHubArtifact) {
        for (const githubArtifactMode of githubArtifactModes) {
            await runAnalyzer({
                config,
                runtimeDir,
                sourceFiles,
                createGitHubArtifact: true,
                githubArtifactMode,
                chartManifestPath,
                cadencePlanPath,
            });
        }
        process.stdout.write(`[${new Date().toISOString()}] Created GitHub ${githubArtifactModes.map((mode) => (mode === 'pull_request' ? 'pull requests' : 'issues')).join(' and ')}.\n`);
    }
    else {
        process.stdout.write(`[${new Date().toISOString()}] Drafts generated only (${getActionMode(config)} auto-create disabled).\n`);
    }
    const completedAt = new Date().toISOString();
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await fs.writeFile(statePath, JSON.stringify({
        ...stateAfterHealthCheck,
        ...stateAfterSourceCollection,
        sourceHashes: currentHashes,
        sourceCursors,
        lastSourceFailures: sourceFailures,
        dailyIssueReports: dailyIssueDedupe.dailyIssueReports,
        lastIssueFingerprint: issueFingerprint,
        lastRunAt: completedAt,
        lastOutFile: dryRun.outFile,
        cadences: markCadencesRan(stateAfterSourceCollection, activeCadences, completedAt),
        lastGrowthRunNotifications: await deliverGrowthRunSummary({
            config,
            configPath,
            issuesPayload: deliverableIssuesPayload,
            activeCadences,
            sourceFiles,
            fingerprint: issueFingerprint,
            createdGitHubArtifact: shouldCreateGitHubArtifact,
            chartManifestPath,
        }),
        skippedReason: null,
    }, null, 2), 'utf8');
    await appendSchedulerProof('runner_completed', {
        configPath,
        statePath,
        completedAt,
        skippedReason: null,
        activeCadences: activeCadences.map((cadence) => cadence.key),
        outFile: dryRun.outFile,
        issueCount: Number(dryRun.issuesPayload?.issue_count || 0),
        sourceFailures,
        createdGitHubArtifact: shouldCreateGitHubArtifact,
    });
}
async function main() {
    await loadOpenClawGrowthSecrets();
    const args = parseArgs(process.argv.slice(2));
    await maybeSelfUpdateFromClawHub(args);
    const configPath = path.resolve(args.config);
    const statePath = path.resolve(args.state);
    useSchedulerProofPathForStatePath(statePath);
    if (!args.loop) {
        await runOnce(configPath, statePath);
        return;
    }
    const config = await readJson(configPath);
    const intervalMinutes = Math.max(1, Number(config.schedule?.intervalMinutes || 1440));
    process.stdout.write(`Starting loop. Interval: ${intervalMinutes} minute(s)\n`);
    while (true) {
        try {
            await maybeSelfUpdateFromClawHub(args);
            await runOnce(configPath, statePath);
        }
        catch (error) {
            const failureDecision = await recordRunnerFailure({
                configPath,
                statePath,
                error,
                argv: process.argv.slice(2),
            }).catch(async () => {
                await appendSchedulerProof('runner_failed', {
                    configPath,
                    statePath,
                    error: error instanceof Error ? error.message : String(error),
                }).catch(() => { });
                return null;
            });
            process.stderr.write(`[${new Date().toISOString()}] Run failed${failureDecision?.suppressed ? ' (already reported today)' : ''}: ${error instanceof Error ? error.message : String(error)}\n`);
        }
        await sleep(intervalMinutes * 60_000);
    }
}
main().catch(async (error) => {
    const fallbackArgs = parseFailureArgs(process.argv.slice(2));
    const configPath = path.resolve(fallbackArgs.config);
    const statePath = path.resolve(fallbackArgs.state);
    useSchedulerProofPathForStatePath(statePath);
    const failureDecision = await recordRunnerFailure({
        configPath,
        statePath,
        error,
        argv: process.argv.slice(2),
    }).catch(async () => {
        await appendSchedulerProof('runner_failed', {
            error: error instanceof Error ? error.message : String(error),
            argv: process.argv.slice(2),
        }).catch(() => { });
        return null;
    });
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = failureDecision?.exitCode ?? 1;
});
