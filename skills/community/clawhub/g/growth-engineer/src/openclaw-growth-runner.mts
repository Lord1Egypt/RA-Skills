#!/usr/bin/env node

import { existsSync, promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import {
  deriveRuntimeDirFromStatePath,
  deriveSchedulerProofPathFromStatePath,
  getActionMode,
  getAllSourceEntries,
  getGitHubArtifactModes,
  getGitHubRequirementText,
  repairOpenClawCronDeliveryStore,
  shouldAutoCreateGitHubArtifact,
} from './openclaw-growth-shared.mjs';
import { applyOpenClawSecretRefs, loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';
import {
  buildDiscordSocialPayload,
  buildSlackSocialPayload,
  humanizeConnectorDiagnostic,
  humanizeNotificationIdentifier,
  renderSocialNotificationMarkdown,
  socialNotificationEventId as canonicalSocialNotificationEventId,
  socialNotificationSummary,
  type SocialNotification,
} from './openclaw-notification-ux.mjs';

const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
const DEFAULT_STATE_PATH = 'data/openclaw-growth-engineer/state.json';
const DEFAULT_SCHEDULER_PROOF_PATH = 'data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl';
const DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES = 360;
const DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MULTIPLIER = 2;
const DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MIN_DELTA = 10;
const DEFAULT_DAILY_ISSUE_HISTORY_RETENTION_DAYS = 365;
const DEFAULT_DAILY_RUNNER_FAILURE_RETENTION_DAYS = 14;
const SELF_UPDATE_INTERVAL_MS = 24 * 60 * 60 * 1000;
const SELF_UPDATE_SKILL_SLUG_CANDIDATES = ['growth-engineer', 'openclaw-growth-engineer'];
const CONNECTOR_NOTIFICATION_STATE_VERSION = 2;
const CONNECTOR_PROBE_INCIDENT_KEY = 'connectorProbe';
const SOURCE_COLLECTION_INCIDENT_KEY = 'sourceCollection';
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
    objective:
      'Check Sentry/GlitchTip and Coolify for production errors, failed deploys, unhealthy resources, and availability blockers across every configured app.',
    instructions:
      'For Sentry/GlitchTip app errors, compare the issue release or app version with ASC production versions first. Ignore errors that only affect TestFlight, debug, staging, unreleased, or non-production app versions. Keep the social output short and action-oriented.',
  },
  {
    key: 'daily',
    title: 'Daily behavioral anomaly guardrail',
    intervalDays: 1,
    criticalOnly: true,
    focusAreas: ['analytics_anomaly', 'onboarding', 'conversion', 'paywall', 'purchase', 'retention', 'revenue'],
    sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'asc_cli', 'feedback', 'github', 'sentry', 'glitchtip', 'coolify'],
    objective:
      'Detect non-Sentry product and payment anomalies that affect real users: broken login or account flows inferred from behavior, onboarding or purchase drop-offs, zero-conversion days, missing buyers, very low active users, retention cliffs, and revenue anomalies.',
    instructions:
      'Compare AnalyticsCLI, RevenueCat, Paddle, ASC, feedback, memory/state, and recent code changes against recent baselines. Use Sentry/GlitchTip/Coolify only as corroborating context; do not repeat pure crash or deployment alerts that belong to the 90-minute healthcheck.',
  },
  {
    key: 'weekly',
    title: 'Weekly executive product and growth summary',
    intervalDays: 7,
    criticalOnly: false,
    focusAreas: ['conversion', 'paywall', 'onboarding', 'marketing', 'retention', 'stability', 'seo'],
    sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry', 'coolify', 'github'],
    objective:
      'Create a deep app-by-app executive summary across all configured projects, connectors, recent releases, code changes, traffic, SEO/acquisition, revenue, activation, conversion, retention, reviews, and production stability.',
    instructions:
      'Be detailed. Group findings per app, explain why each recommendation should improve app usage, revenue, conversion, retention, or traffic, include expected KPI movement, likely code/store surfaces, owner-ready next steps, and verification plans. Generate charts when they clarify the evidence.',
  },
  {
    key: 'monthly',
    title: 'Monthly deep product, business, and code review',
    intervalDays: 30,
    criticalOnly: false,
    focusAreas: ['conversion', 'paywall', 'retention', 'marketing', 'onboarding', 'codebase', 'seo'],
    sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry', 'coolify', 'github'],
    objective:
      'Compare all configured projects month-over-month: MRR, trial conversion, churn, Paddle revenue/subscriber movement, SEO demand/clicks, acquisition channel quality, store/listing conversion, retention, review themes, feature usage, crash totals, and codebase changes.',
    instructions:
      'Be very detailed and app-grouped. Decide what should be built, changed, deleted, priced differently, marketed differently, or instrumented next. Tie conclusions to connector data plus codebase evidence and explain why each recommendation should move revenue, conversion, retention, traffic, or acquisition quality. Generate charts when useful.',
  },
  {
    key: 'quarterly',
    title: '3-month positioning, pricing, and roadmap review',
    intervalDays: 91,
    criticalOnly: false,
    focusAreas: ['marketing', 'paywall', 'retention', 'conversion', 'onboarding'],
    sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'github', 'sentry'],
    objective:
      'Revisit positioning, pricing/packaging, onboarding architecture, roadmap assumptions, tracking quality, codebase constraints, and major funnel bets across every configured app.',
    instructions:
      'Find structural constraints and durable opportunities, not small UI tweaks. Group the analysis by app and tie recommendations to cohort behavior, monetization, SEO demand, reviews, channel quality, and shipped changes. Include concrete roadmap, pricing, conversion, and traffic recommendations.',
  },
  {
    key: 'six_months',
    title: 'Six-month instrumentation and growth-system audit',
    intervalDays: 182,
    criticalOnly: false,
    focusAreas: ['retention', 'conversion', 'paywall', 'marketing', 'general', 'seo'],
    sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry'],
    objective:
      'Audit connector coverage, SDK instrumentation, event taxonomy, data reliability, data memory, growth loops, and whether product/code strategy still matches the best users across configured projects.',
    instructions:
      'Group by app. Prioritize measurement fixes and system changes that make future analysis more trustworthy, then identify the highest-leverage app/revenue/conversion/SEO/traffic improvements. Identify stale events, missing attribution, weak identity, broken feedback loops, and misleading dashboards.',
  },
  {
    key: 'yearly',
    title: 'Yearly evidence reset',
    intervalDays: 365,
    criticalOnly: false,
    focusAreas: ['marketing', 'retention', 'paywall', 'conversion', 'general'],
    sourcePriorities: ['analytics', 'revenuecat', 'paddle', 'seo', 'asc_cli', 'feedback', 'sentry'],
    objective:
      'Reset strategy from evidence across every configured project: market/channel fit, monetization model, retention ceiling, product scope, and whether to double down, reposition, rebuild, or sunset major surfaces/features.',
    instructions:
      'Use the full year of memory, releases, revenue, acquisition, reviews, code changes, and cohort behavior. Produce a strategic operating plan with specific experiments and stop-doing decisions.',
  },
];

type ShellResult = {
  ok: boolean;
  code: number | null;
  stdout: string;
  stderr: string;
};

function parseArgs(argv) {
  const args = {
    config: DEFAULT_CONFIG_PATH,
    state: DEFAULT_STATE_PATH,
    loop: false,
    noSelfUpdate: false,
    validateNotificationState: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    const next = argv[i + 1];
    if (token === '--') {
      continue;
    } else if (token === '--config') {
      args.config = next;
      i += 1;
    } else if (token === '--state') {
      args.state = next;
      i += 1;
    } else if (token === '--loop') {
      args.loop = true;
    } else if (token === '--no-self-update') {
      args.noSelfUpdate = true;
    } else if (token === '--validate-notification-state') {
      args.validateNotificationState = true;
    } else if (token === '--help' || token === '-h') {
      printHelpAndExit(0);
    } else {
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
  --validate-notification-state
                     Validate connector incident migration and transitions, then exit

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
  if (!trimmed) return trimmed;
  return trimmed
    .replace(
    /^node\s+scripts\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-engineer\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs)(?=\s|$)/,
    (_match, scriptName) => nodeRuntimeScriptCommand(scriptName),
    )
    .replace(
      /^node\s+(['"]?)(?:\S*\/)?node_modules\/@analyticscli\/growth-engineer\/dist\/runtime\/(export-analytics-summary\.mjs|export-revenuecat-summary\.mjs|export-paddle-summary\.mjs|export-seo-summary\.mjs|export-sentry-summary\.mjs|export-coolify-summary\.mjs|export-asc-summary\.mjs|openclaw-growth-engineer\.mjs|openclaw-growth-status\.mjs|openclaw-growth-preflight\.mjs|openclaw-growth-runner\.mjs)\1(?=\s|$)/,
      (_match, _quote, scriptName) => nodeRuntimeScriptCommand(scriptName),
    );
}

function commandHasConfigArg(command) {
  return /(?:^|\s)--config(?:=|\s|$)/.test(String(command || ''));
}

function commandIsBuiltinExporter(command) {
  return /(?:^|\s)(?:node\s+)?(?:\S*\/)?(?:export-analytics-summary|export-revenuecat-summary|export-paddle-summary|export-seo-summary|export-sentry-summary|export-coolify-summary|export-asc-summary)\.mjs(?:\s|$)/.test(
    String(command || ''),
  );
}

function commandSupportsActiveConfig(command) {
  return /(?:^|\s)(?:node\s+)?(?:\S*\/)?(?:export-paddle-summary|export-sentry-summary|export-coolify-summary)\.mjs(?:\s|$)/.test(
    String(command || ''),
  );
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

async function readJson(filePath): Promise<any> {
  const raw = await fs.readFile(filePath, 'utf8');
  return JSON.parse(raw);
}

async function readJsonOptional(filePath, fallback) {
  try {
    return await readJson(filePath);
  } catch {
    return fallback;
  }
}

let atomicWriteSequence = 0;

async function writeJsonAtomic(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  atomicWriteSequence += 1;
  const temporaryPath = `${filePath}.${process.pid}.${Date.now()}.${atomicWriteSequence}.tmp`;
  try {
    await fs.writeFile(
      temporaryPath,
      `${JSON.stringify(value, null, 2)}\n`,
      'utf8',
    );
    await fs.rename(temporaryPath, filePath);
  } catch (error) {
    await fs.unlink(temporaryPath).catch(() => {});
    throw error;
  }
}

async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true });
}

async function appendSchedulerProof(event, details: Record<string, any> = {}) {
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
  return /NETWORK_ERROR|fetch failed|tlsv1 alert|SSL routines|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|socket hang up|network timeout|Temporary failure|upstream connect error|disconnect\/reset before headers|HTTP 5\d\d|API 5\d\d/i.test(
    String(value || ''),
  );
}

function isRequiredSource(sourceConfig, sourceName) {
  if (sourceConfig?.required === true) return true;
  if (sourceConfig?.required === false) return false;
  return String(sourceName || '').toLowerCase() === 'analytics';
}

function isSentryCompatibleSource(sourceConfig, sourceName) {
  const sourceKey = String(sourceName || '').toLowerCase();
  const service = String(sourceConfig?.service || sourceConfig?.provider || '').toLowerCase();
  const command = String(sourceConfig?.command || '').toLowerCase();
  return (
    sourceKey === 'sentry' ||
    sourceKey === 'glitchtip' ||
    service === 'sentry' ||
    service === 'glitchtip' ||
    command.includes('export-sentry-summary')
  );
}

function shouldDegradeTransientSourceFailure(sourceConfig, sourceName, retried) {
  if (!retried) return false;
  if (sourceConfig?.degradeTransientFailures === false) return false;
  if (!isRequiredSource(sourceConfig, sourceName)) return true;
  if (isSentryCompatibleSource(sourceConfig, sourceName)) return true;
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

async function inferGitHubRepo(config) {
  const configured = String(config?.project?.githubRepo || '').trim();
  if (isConfiguredGitHubRepo(configured)) return configured;

  const explicit = String(process.env.OPENCLAW_GITHUB_REPO || '').trim();
  if (isConfiguredGitHubRepo(explicit)) return explicit;

  const repoRoot = path.resolve(config?.project?.repoRoot || '.');
  const remoteResult = await runShellCommand('git config --get remote.origin.url', 10_000, {
    cwd: repoRoot,
  });
  if (!remoteResult.ok) return '';
  return parseGitHubRepoFromRemote(remoteResult.stdout.trim()) || '';
}

async function filesHaveSameContent(leftPath, rightPath) {
  try {
    const [left, right] = await Promise.all([fs.readFile(leftPath), fs.readFile(rightPath)]);
    return left.equals(right);
  } catch {
    return false;
  }
}

async function shouldRunSelfUpdate(workspaceRoot, force) {
  if (force) return true;
  const statePath = path.join(workspaceRoot, 'data/openclaw-growth-engineer/self-update.json');
  const state = await readJsonOptional(statePath, null);
  const lastCheckedAt = Date.parse(String(state?.lastCheckedAt || ''));
  return !Number.isFinite(lastCheckedAt) || Date.now() - lastCheckedAt > SELF_UPDATE_INTERVAL_MS;
}

async function writeSelfUpdateState(workspaceRoot, value) {
  const statePath = path.join(workspaceRoot, 'data/openclaw-growth-engineer/self-update.json');
  await fs.mkdir(path.dirname(statePath), { recursive: true });
  await fs.writeFile(
    statePath,
    `${JSON.stringify({ version: 1, checkedAt: new Date().toISOString(), ...value }, null, 2)}\n`,
    'utf8',
  );
}

async function rerunCurrentProcessWithoutSelfUpdate() {
  return await new Promise<number | null>((resolve) => {
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
  if (args.noSelfUpdate) return false;
  if (isTruthyEnv(process.env.OPENCLAW_GROWTH_SKIP_SELF_UPDATE)) return false;
  if (isTruthyEnv(process.env.OPENCLAW_GROWTH_DISABLE_SELF_UPDATE)) return false;
  if (isFalseyEnv(process.env.OPENCLAW_GROWTH_SELF_UPDATE)) return false;

  const workspaceRoot = process.cwd();
  const installedSkill = resolveInstalledSelfUpdateSkill(workspaceRoot);
  if (!installedSkill) return false;
  if (!(await commandExists('npx'))) return false;

  const force = String(process.env.OPENCLAW_GROWTH_SELF_UPDATE || '').trim().toLowerCase() === 'always';
  if (!(await shouldRunSelfUpdate(workspaceRoot, force))) return false;

  const beforeOrigin = await readJsonOptional(installedSkill.originPath, null);
  const beforeVersion = String(beforeOrigin?.installedVersion || '');
  process.stdout.write(`Checking for Growth Engineer skill updates (${installedSkill.slug})...\n`);
  const updateResult = await runShellCommand(
    `npx -y clawhub --no-input --dir skills update ${quote(installedSkill.slug)} --force`,
    120_000,
  );
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
  }).catch(() => {});

  if (!updateResult.ok) {
    const detail = String(updateResult.stderr || updateResult.stdout || 'update failed').trim().split(/\r?\n/).pop();
    process.stdout.write(`Skill update check skipped: ${detail}\n`);
    return false;
  }
  if ((!afterVersion || afterVersion === beforeVersion) && !runtimeOutdated) return false;

  process.stdout.write(
    afterVersion && afterVersion !== beforeVersion
      ? `Updated OpenClaw Growth Engineer skill ${beforeVersion || 'unknown'} -> ${afterVersion}. Refreshing workspace runtime...\n`
      : 'Refreshing workspace runtime from the installed OpenClaw Growth Engineer skill...\n',
  );
  const bootstrapResult = await runShellCommand(
    `bash ${quote(installedSkill.bootstrapPath)}`,
    60_000,
  );
  if (!bootstrapResult.ok) {
    process.stdout.write('Workspace runtime refresh failed; continuing with current process.\n');
    return false;
  }
  process.stdout.write('Restarting runner with refreshed runtime...\n');
  const code = await rerunCurrentProcessWithoutSelfUpdate();
  process.exit(code ?? 0);
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

function hardenUnattendedShellCommand(command) {
  return String(command || '').replace(/(^|[;&|]\s*)sudo(?!\s+-n(?:\s|$))(?=\s|$)/g, '$1sudo -n');
}

function redactCommandForDiagnostics(command) {
  const raw = String(command || '').trim();
  if (!raw) return '';
  return raw
    .replace(
      /((?:^|\s)(?:[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASS|KEY|AUTH|CREDENTIAL)[A-Z0-9_]*)=)(?:"[^"]*"|'[^']*'|\S+)/gi,
      '$1[redacted]',
    )
    .replace(
      /((?:^|\s)--(?:token|access-token|api-key|key|secret|password|pass|authorization|auth|bearer)(?:=|\s+))(?:"[^"]*"|'[^']*'|\S+)/gi,
      '$1[redacted]',
    );
}

function truncateDiagnosticText(value, maxLength = 2000) {
  const text = String(value || '').trim();
  if (text.length <= maxLength) return text;
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

function runShellCommand(command, timeoutMs = 120_000, options: { cwd?: string; input?: string; env?: Record<string, string> } = {}): Promise<ShellResult> {
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
      if (settled) return;
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
      if (settled) return;
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
  if (!raw) return null;
  const firstBrace = raw.indexOf('{');
  const firstBracket = raw.indexOf('[');
  const starts = [firstBrace, firstBracket].filter((index) => index >= 0);
  if (starts.length === 0) return null;
  try {
    return JSON.parse(raw.slice(Math.min(...starts)));
  } catch {
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
  if (!lastCheckedAt) return true;
  const last = Date.parse(String(lastCheckedAt));
  if (!Number.isFinite(last)) return true;
  return Date.now() - last >= intervalMinutes * 60_000;
}

function normalizeCadenceKey(value) {
  const normalized = String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[\s-]+/g, '_');
  if (['3_months', 'three_months', 'quarter', 'quarterly'].includes(normalized)) return 'quarterly';
  if (['6_months', 'six_months', 'half_year', 'half_yearly'].includes(normalized)) return 'six_months';
  if (['1y', '1_year', 'one_year', 'annual', 'annually'].includes(normalized)) return 'yearly';
  return normalized;
}

function getCadenceDefinitions(config) {
  const configured = Array.isArray(config?.schedule?.cadences) ? config.schedule.cadences : [];
  const byKey = new Map(DEFAULT_CADENCES.map((cadence) => [cadence.key, { ...cadence }]));
  for (const cadence of configured) {
    if (!cadence || typeof cadence !== 'object') continue;
    const key = normalizeCadenceKey(cadence.key || cadence.id || cadence.label);
    if (!key) continue;
    const base: any = byKey.get(key) || { key };
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
  return ([...byKey.values()] as any[]).filter((cadence) => cadence.enabled !== false);
}

function cadenceIsDue(cadence, state) {
  const lastRanAt = state?.cadences?.[cadence.key]?.lastRanAt;
  const intervalMinutes = Number(cadence.intervalMinutes || 0);
  if (intervalMinutes > 0) {
    if (!lastRanAt) return true;
    const last = Date.parse(String(lastRanAt));
    if (!Number.isFinite(last)) return true;
    return Date.now() - last >= Math.max(1, intervalMinutes) * 60 * 1000;
  }
  const intervalDays = Number(cadence.intervalDays || 1);
  if (!lastRanAt) return true;
  const last = Date.parse(String(lastRanAt));
  if (!Number.isFinite(last)) return true;
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
  return Object.entries(statusPayload?.connectors || {}).map(([key, value]: [string, any]) => ({
    key,
    label: String(value?.label || key),
    status: String(value?.status || 'unknown'),
    detail: String(value?.detail || ''),
    nextAction: typeof value?.nextAction === 'string' ? value.nextAction : null,
    accounts: Array.isArray(value?.accounts) ? value.accounts : [],
    failureCount: Math.max(0, Number(value?.failureCount || 0)),
  }));
}

function getUnhealthyConfiguredConnectors(statusPayload) {
  return getConnectorEntries(statusPayload).filter((entry) =>
    ['blocked', 'partial', 'unknown'].includes(entry.status),
  );
}

function getConnectedConnectorKeys(statusPayload) {
  return getConnectorEntries(statusPayload)
    .filter((entry) => entry.status === 'connected')
    .map((entry) => entry.key)
    .sort();
}

function buildConnectorHealthFingerprint(unhealthyConnectors) {
  const normalizeDiagnostic = (entry) =>
    humanizeConnectorDiagnostic(entry?.detail)
      .replace(
        /\b\d{4}-\d{2}-\d{2}(?:T|\s)\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\b/gi,
        '[timestamp]',
      )
      .replace(/\b(?:request|trace|correlation)[-_ ]?id\s*[:=]\s*\S+/gi, 'request-id=[id]')
      .replace(/\b\d+(?:\.\d+)?\s*(?:ms|milliseconds?|seconds?|minutes?)\b/gi, '[duration]')
      .replace(/\s+/g, ' ')
      .trim();
  const actionCategory = (entry) => {
    const text = `${entry?.detail || ''} ${entry?.nextAction || ''}`.toLowerCase();
    if (/transient|upstream|network|timeout|retry/.test(text)) return 'retry';
    if (/auth|credential|token|secret|permission/.test(text)) return 'credentials';
    if (/setup|wizard|disabled|missing|create/.test(text)) return 'setup';
    return 'review';
  };
  return sha256(
    unhealthyConnectors
      .map(
        (entry) =>
          `${entry.key}|${entry.status}|${normalizeDiagnostic(entry)}|${actionCategory(entry)}|${Number(entry.failureCount || 0)}`,
      )
      .sort()
      .join('\n'),
  );
}

function blankConnectorNotificationIncident(kind) {
  return {
    kind,
    status: 'recovered',
    activeFingerprint: null,
    lastObservedFingerprint: null,
    recoveredFingerprint: null,
    occurrenceCount: 0,
    firstSeenAt: null,
    lastSeenAt: null,
    lastTransitionAt: null,
    lastRecoveredAt: null,
    lastNotifiedFingerprint: null,
    lastNotificationAt: null,
    lastNotificationDeliveries: [],
    lastNotificationEventId: null,
    lastNotificationReceipts: {},
    lastNotificationAllChannelsSent: false,
    lastNotificationExternalSent: false,
    lastExternalAlertedFingerprint: null,
    lastExternalAlertedAt: null,
  };
}

function normalizeConnectorNotificationIncident(value, kind) {
  const fallback = blankConnectorNotificationIncident(kind);
  if (!value || typeof value !== 'object') return fallback;
  const activeFingerprint = String(value.activeFingerprint || '').trim() || null;
  const storedStatus = String(value.status || '').trim().toLowerCase();
  const status = activeFingerprint
    ? storedStatus === 'new'
      ? 'new'
      : 'ongoing'
    : 'recovered';
  const lastExternalAlertedFingerprint =
    String(value.lastExternalAlertedFingerprint || '').trim() || null;
  const lastNotificationExternalSent =
    typeof value.lastNotificationExternalSent === 'boolean'
      ? value.lastNotificationExternalSent
      : Boolean(lastExternalAlertedFingerprint);
  const lastNotificationAllChannelsSent =
    typeof value.lastNotificationAllChannelsSent === 'boolean'
      ? value.lastNotificationAllChannelsSent
      : lastNotificationExternalSent;
  return {
    ...fallback,
    ...value,
    kind,
    status,
    activeFingerprint,
    lastObservedFingerprint:
      String(value.lastObservedFingerprint || value.lastFingerprint || '').trim() || activeFingerprint,
    recoveredFingerprint: String(value.recoveredFingerprint || '').trim() || null,
    occurrenceCount: Math.max(0, Number(value.occurrenceCount || 0)),
    lastNotifiedFingerprint:
      String(value.lastNotifiedFingerprint || value.lastAlertedFingerprint || '').trim() || null,
    lastNotificationExternalSent,
    lastNotificationAllChannelsSent,
    lastExternalAlertedFingerprint,
    lastNotificationEventId:
      String(value.lastNotificationEventId || '').trim() || null,
    lastNotificationReceipts:
      value.lastNotificationReceipts &&
      typeof value.lastNotificationReceipts === 'object'
        ? value.lastNotificationReceipts
        : {},
    lastNotificationDeliveries: Array.isArray(value.lastNotificationDeliveries)
      ? value.lastNotificationDeliveries
      : Array.isArray(value.lastAlertDeliveries)
        ? value.lastAlertDeliveries
        : [],
  };
}

function getPersistedSourceCollectionFailures(state) {
  if (Array.isArray(state?.lastSourceCollectionFailures)) {
    return state.lastSourceCollectionFailures;
  }
  if (Array.isArray(state?.lastSourceFailures)) {
    return state.lastSourceFailures;
  }
  return [];
}

/**
 * Migrates the original shared connectorHealth alert fields into one incident
 * stream. Existing source failures identify the source-collection stream;
 * otherwise the legacy state belongs to the scheduled connector probe.
 *
 * Once version 2 exists, missing streams are initialized independently and the
 * ambiguous legacy fields are never used again.
 */
function getConnectorNotificationIncidents(state) {
  const healthState = state?.connectorHealth || {};
  const stored = healthState.incidents;
  if (
    stored &&
    typeof stored === 'object' &&
    Number(stored.version || 0) >= CONNECTOR_NOTIFICATION_STATE_VERSION
  ) {
    return {
      ...stored,
      version: CONNECTOR_NOTIFICATION_STATE_VERSION,
      [CONNECTOR_PROBE_INCIDENT_KEY]: normalizeConnectorNotificationIncident(
        stored[CONNECTOR_PROBE_INCIDENT_KEY],
        'connector_probe',
      ),
      [SOURCE_COLLECTION_INCIDENT_KEY]: normalizeConnectorNotificationIncident(
        stored[SOURCE_COLLECTION_INCIDENT_KEY],
        'source_collection',
      ),
    };
  }

  const sourceFailures = getPersistedSourceCollectionFailures(state);
  const legacyKind =
    sourceFailures.length > 0 ? SOURCE_COLLECTION_INCIDENT_KEY : CONNECTOR_PROBE_INCIDENT_KEY;
  const legacyActiveFingerprint =
    String(
      healthState.activeIncidentFingerprint ||
        (healthState.lastStatusOk === false ? healthState.lastFingerprint : '') ||
        '',
    ).trim() || null;
  const legacyIncident = normalizeConnectorNotificationIncident(
    {
      status: legacyActiveFingerprint ? 'ongoing' : 'recovered',
      activeFingerprint: legacyActiveFingerprint,
      lastObservedFingerprint: healthState.lastFingerprint || legacyActiveFingerprint,
      recoveredFingerprint: legacyActiveFingerprint ? null : healthState.lastFingerprint || null,
      occurrenceCount: legacyActiveFingerprint ? 1 : 0,
      firstSeenAt: healthState.lastAlertedAt || healthState.lastCheckedAt || null,
      lastSeenAt: healthState.lastCheckedAt || null,
      lastTransitionAt: healthState.lastAlertedAt || healthState.lastCheckedAt || null,
      lastRecoveredAt: healthState.lastRecoveredAt || null,
      lastNotifiedFingerprint:
        healthState.lastAlertedFingerprint ||
        healthState.lastExternalAlertedFingerprint ||
        legacyActiveFingerprint,
      lastNotificationAt:
        healthState.lastAlertedAt || healthState.lastExternalAlertedAt || null,
      lastNotificationDeliveries: healthState.lastAlertDeliveries || [],
      lastNotificationExternalSent:
        typeof healthState.lastAlertExternalSent === 'boolean'
          ? healthState.lastAlertExternalSent
          : Boolean(healthState.lastExternalAlertedFingerprint),
      lastExternalAlertedFingerprint: healthState.lastExternalAlertedFingerprint || null,
      lastExternalAlertedAt: healthState.lastExternalAlertedAt || null,
      migratedFromLegacyConnectorHealth: true,
    },
    legacyKind === SOURCE_COLLECTION_INCIDENT_KEY
      ? 'source_collection'
      : 'connector_probe',
  );

  return {
    version: CONNECTOR_NOTIFICATION_STATE_VERSION,
    migratedAt: new Date().toISOString(),
    [CONNECTOR_PROBE_INCIDENT_KEY]:
      legacyKind === CONNECTOR_PROBE_INCIDENT_KEY
        ? legacyIncident
        : blankConnectorNotificationIncident('connector_probe'),
    [SOURCE_COLLECTION_INCIDENT_KEY]:
      legacyKind === SOURCE_COLLECTION_INCIDENT_KEY
        ? legacyIncident
        : blankConnectorNotificationIncident('source_collection'),
  };
}

function transitionConnectorNotificationIncident(previousValue, kind, fingerprint, observedAt) {
  const previous = normalizeConnectorNotificationIncident(previousValue, kind);
  const currentFingerprint = String(fingerprint || '').trim() || null;
  if (currentFingerprint) {
    const unchanged = previous.activeFingerprint === currentFingerprint;
    return {
      ...previous,
      kind,
      status: unchanged ? 'ongoing' : 'new',
      activeFingerprint: currentFingerprint,
      lastObservedFingerprint: currentFingerprint,
      recoveredFingerprint: null,
      occurrenceCount: Number(previous.occurrenceCount || 0) + 1,
      firstSeenAt: unchanged ? previous.firstSeenAt || observedAt : observedAt,
      lastSeenAt: observedAt,
      lastTransitionAt: unchanged
        ? previous.lastTransitionAt || observedAt
        : observedAt,
    };
  }

  const recoveredFingerprint = previous.activeFingerprint || previous.recoveredFingerprint || null;
  return {
    ...previous,
    kind,
    status: 'recovered',
    activeFingerprint: null,
    recoveredFingerprint,
    lastSeenAt: observedAt,
    lastTransitionAt: previous.activeFingerprint
      ? observedAt
      : previous.lastTransitionAt || observedAt,
    lastRecoveredAt: previous.activeFingerprint
      ? observedAt
      : previous.lastRecoveredAt || null,
  };
}

function connectorIncidentNotificationEventId(incident) {
  const fingerprint =
    incident?.status === 'recovered'
      ? incident?.recoveredFingerprint
      : incident?.activeFingerprint;
  const phase = incident?.status === 'recovered' ? 'recovered' : 'active';
  return `${incident?.kind || 'connector_probe'}:${phase}:${fingerprint || 'healthy'}`;
}

function pendingConnectorIncidentChannelKeys(previousValue, nextValue, channelKeys) {
  const uniqueKeys: string[] = Array.from(
    new Set<string>(
      (Array.isArray(channelKeys) ? channelKeys : []).map((key: unknown) =>
        String(key),
      ),
    ),
  );
  const eventId = connectorIncidentNotificationEventId(nextValue);
  if (previousValue?.lastNotificationEventId !== eventId) {
    const legacyEventAlreadyDelivered =
      !previousValue?.lastNotificationEventId &&
      previousValue?.lastNotificationExternalSent === true &&
      String(previousValue?.lastNotifiedFingerprint || '') ===
        String(
          nextValue?.status === 'recovered'
            ? nextValue?.recoveredFingerprint || ''
            : nextValue?.activeFingerprint || '',
        );
    return legacyEventAlreadyDelivered ? [] : uniqueKeys;
  }
  const receipts: Record<string, any> =
    previousValue?.lastNotificationReceipts &&
    typeof previousValue.lastNotificationReceipts === 'object'
      ? previousValue.lastNotificationReceipts
      : {};
  return uniqueKeys.filter((key) => receipts[key]?.sent !== true);
}

function shouldNotifyConnectorIncident(previousValue, nextValue, channelKeys = null) {
  const previousActiveFingerprint =
    String(previousValue?.activeFingerprint || '').trim() || null;
  if (nextValue?.status === 'new') {
    return nextValue.activeFingerprint !== previousActiveFingerprint;
  }
  if (nextValue?.status === 'ongoing') {
    if (Array.isArray(channelKeys)) {
      return (
        pendingConnectorIncidentChannelKeys(
          previousValue,
          nextValue,
          channelKeys,
        ).length > 0
      );
    }
    if (typeof previousValue?.lastNotificationAllChannelsSent === 'boolean') {
      return previousValue.lastNotificationAllChannelsSent !== true;
    }
    return previousValue?.lastNotificationExternalSent !== true;
  }
  if (nextValue?.status === 'recovered') {
    if (previousActiveFingerprint) return true;
    if (Array.isArray(channelKeys)) {
      return (
        pendingConnectorIncidentChannelKeys(
          previousValue,
          nextValue,
          channelKeys,
        ).length > 0
      );
    }
    return Boolean(
      previousValue?.lastNotificationAt &&
        previousValue?.recoveredFingerprint &&
        previousValue?.lastNotificationAllChannelsSent !== true,
    );
  }
  return false;
}

function markConnectorIncidentNotification(
  incident,
  deliveries,
  notifiedAt,
  configuredChannelKeys = null,
) {
  const fingerprint =
    incident.status === 'recovered'
      ? incident.recoveredFingerprint
      : incident.activeFingerprint;
  const eventId = connectorIncidentNotificationEventId(incident);
  const sameEvent = incident.lastNotificationEventId === eventId;
  const receipts = sameEvent &&
    incident.lastNotificationReceipts &&
    typeof incident.lastNotificationReceipts === 'object'
    ? { ...incident.lastNotificationReceipts }
    : {};
  for (const delivery of deliveries) {
    const channelKey = String(
      delivery?.channelKey || delivery?.target || '',
    ).trim();
    if (!channelKey || channelKey === 'external_notification') continue;
    receipts[channelKey] = {
      sent: delivery?.sent === true,
      external: delivery?.external === true,
      target: delivery?.target || channelKey,
      detail: delivery?.detail || null,
      retryable: delivery?.retryable !== false,
      attemptCount: Number(delivery?.attemptCount || 1),
      updatedAt: notifiedAt,
    };
  }
  const channelKeys = Array.isArray(configuredChannelKeys)
    ? [...new Set(configuredChannelKeys)]
    : Object.keys(receipts);
  const allChannelsSent =
    channelKeys.length === 0 ||
    channelKeys.every((key) => receipts[key]?.sent === true);
  const externalSent = Object.values(receipts).some(
    (receipt: any) => receipt?.sent === true && receipt?.external === true,
  );
  return {
    ...incident,
    lastNotifiedFingerprint: fingerprint || null,
    lastNotificationAt: notifiedAt,
    lastNotificationDeliveries: deliveries,
    lastNotificationEventId: eventId,
    lastNotificationReceipts: receipts,
    lastNotificationAllChannelsSent: allChannelsSent,
    lastNotificationExternalSent: externalSent,
    ...(externalSent
      ? {
          lastExternalAlertedFingerprint: fingerprint || null,
          lastExternalAlertedAt: notifiedAt,
        }
      : {}),
  };
}

function incidentLabel(kind) {
  return kind === 'source_collection' ? 'source collection' : 'connector probe';
}

function buildConnectorRecoveryAlert(kind) {
  return `${kind === 'source_collection' ? 'Data collection' : 'Connector health'} recovered.\n`;
}

function assertNotificationStateValidation(condition, message) {
  if (!condition) {
    throw new Error(`Notification-state validation failed: ${message}`);
  }
}

function validateConnectorNotificationStateModel() {
  const firstAt = '2026-07-23T10:00:00.000Z';
  const secondAt = '2026-07-23T10:05:00.000Z';
  const recoveredAt = '2026-07-23T10:10:00.000Z';
  const legacyFingerprint = 'legacy-source-fingerprint';
  const migrated = getConnectorNotificationIncidents({
    connectorHealth: {
      lastStatusOk: false,
      lastFingerprint: legacyFingerprint,
      activeIncidentFingerprint: legacyFingerprint,
      lastAlertedFingerprint: legacyFingerprint,
      lastExternalAlertedFingerprint: legacyFingerprint,
      lastAlertedAt: firstAt,
    },
    lastSourceCollectionFailures: [
      {
        key: 'analytics',
        detail: 'upstream unavailable',
      },
    ],
  });
  assertNotificationStateValidation(
    migrated.version === CONNECTOR_NOTIFICATION_STATE_VERSION,
    'legacy state did not migrate to the current version',
  );
  assertNotificationStateValidation(
    migrated[SOURCE_COLLECTION_INCIDENT_KEY].activeFingerprint === legacyFingerprint,
    'legacy source incident was not assigned to source collection',
  );
  assertNotificationStateValidation(
    migrated[CONNECTOR_PROBE_INCIDENT_KEY].activeFingerprint === null,
    'legacy source incident leaked into connector-probe state',
  );

  const newProbe = transitionConnectorNotificationIncident(
    migrated[CONNECTOR_PROBE_INCIDENT_KEY],
    'connector_probe',
    'probe-fingerprint',
    firstAt,
  );
  const notifiedProbe = markConnectorIncidentNotification(
    newProbe,
    [{ sent: true, external: true, target: 'validator' }],
    firstAt,
  );
  const ongoingProbe = transitionConnectorNotificationIncident(
    notifiedProbe,
    'connector_probe',
    'probe-fingerprint',
    secondAt,
  );
  assertNotificationStateValidation(newProbe.status === 'new', 'new probe incident not modeled');
  assertNotificationStateValidation(
    ongoingProbe.status === 'ongoing',
    'unchanged probe incident not modeled as ongoing',
  );
  assertNotificationStateValidation(
    !shouldNotifyConnectorIncident(notifiedProbe, ongoingProbe),
    'successfully delivered unchanged probe incident would be sent again',
  );
  assertNotificationStateValidation(
    ongoingProbe.lastTransitionAt === notifiedProbe.lastTransitionAt,
    'ongoing observation overwrote the original transition timestamp',
  );
  assertNotificationStateValidation(
    ongoingProbe.occurrenceCount === notifiedProbe.occurrenceCount + 1,
    'ongoing observation did not increment occurrenceCount',
  );
  const failedProbeDelivery = markConnectorIncidentNotification(
    newProbe,
    [{ sent: false, external: true, target: 'validator' }],
    firstAt,
  );
  const retryableOngoingProbe = transitionConnectorNotificationIncident(
    failedProbeDelivery,
    'connector_probe',
    'probe-fingerprint',
    secondAt,
  );
  assertNotificationStateValidation(
    shouldNotifyConnectorIncident(failedProbeDelivery, retryableOngoingProbe),
    'failed external delivery would not be retried for ongoing incident',
  );
  const mixedProbeDelivery = markConnectorIncidentNotification(
    newProbe,
    [
      {
        sent: true,
        external: true,
        target: 'discord',
        channelKey: 'discord:bridge',
      },
      {
        sent: false,
        external: true,
        target: 'slack',
        channelKey: 'slack:SLACK_WEBHOOK_URL',
      },
    ],
    firstAt,
    ['discord:bridge', 'slack:SLACK_WEBHOOK_URL'],
  );
  const mixedOngoingProbe = transitionConnectorNotificationIncident(
    mixedProbeDelivery,
    'connector_probe',
    'probe-fingerprint',
    secondAt,
  );
  const mixedPendingKeys = pendingConnectorIncidentChannelKeys(
    mixedProbeDelivery,
    mixedOngoingProbe,
    ['discord:bridge', 'slack:SLACK_WEBHOOK_URL'],
  );
  assertNotificationStateValidation(
    mixedPendingKeys.length === 1 &&
      mixedPendingKeys[0] === 'slack:SLACK_WEBHOOK_URL',
    'successful channels would be retried together with a failed channel',
  );
  const completedMixedDelivery = markConnectorIncidentNotification(
    mixedOngoingProbe,
    [
      {
        sent: true,
        external: true,
        target: 'slack',
        channelKey: 'slack:SLACK_WEBHOOK_URL',
      },
    ],
    secondAt,
    ['discord:bridge', 'slack:SLACK_WEBHOOK_URL'],
  );
  assertNotificationStateValidation(
    completedMixedDelivery.lastNotificationAllChannelsSent === true &&
      completedMixedDelivery.lastNotificationReceipts['discord:bridge']?.sent === true,
    'channel receipts were not merged after a selective retry',
  );
  const growthSnapshot = {
    issuesPayload: { issue_count: 1, issues: [{ title: 'Example finding' }] },
    activeCadences: [],
    sourceFiles: {},
    createdGitHubArtifact: false,
    chartManifestPath: null,
  };
  const failedGrowthDelivery = markGrowthRunNotificationState({
    previousState: null,
    fingerprint: 'growth-fingerprint',
    deliveries: [
      {
        sent: true,
        external: true,
        target: 'discord',
        channelKey: 'discord:bridge',
      },
      {
        sent: false,
        external: true,
        target: 'slack',
        channelKey: 'slack:SLACK_WEBHOOK_URL',
      },
    ],
    configuredChannelKeys: ['discord:bridge', 'slack:SLACK_WEBHOOK_URL'],
    snapshot: growthSnapshot,
    attemptedAt: firstAt,
  });
  assertNotificationStateValidation(
    failedGrowthDelivery.allChannelsSent === false &&
      failedGrowthDelivery.snapshot === growthSnapshot &&
      pendingGrowthRunChannelKeys(
        failedGrowthDelivery,
        'growth-fingerprint',
        ['discord:bridge', 'slack:SLACK_WEBHOOK_URL'],
      ).join(',') === 'slack:SLACK_WEBHOOK_URL',
    'failed growth delivery would be lost or retried on successful channels',
  );
  const deduplicatedChannels = mergeNotificationChannelsWithDeliveries(
    [
      {
        type: 'slack',
        enabled: true,
        label: 'primary',
        webhookEnv: 'SLACK_WEBHOOK_URL',
      },
    ],
    [
      {
        type: 'slack',
        enabled: true,
        label: 'legacy-fallback',
        webhookEnv: 'SLACK_WEBHOOK_URL',
      },
    ],
  );
  const disabledFallbackChannels = mergeNotificationChannelsWithDeliveries(
    [{ type: 'slack', enabled: false }],
    [
      {
        type: 'slack',
        enabled: true,
        webhookEnv: 'SLACK_WEBHOOK_URL',
      },
    ],
  );
  const defaultChannelOverride = mergeNotificationChannelsWithDeliveries(
    [{ type: 'openclaw-chat', enabled: true }],
    [
      {
        type: 'openclaw-chat',
        enabled: true,
        markdownPath: '.openclaw/chat/latest.md',
        jsonPath: '.openclaw/chat/latest.json',
      },
    ],
  );
  assertNotificationStateValidation(
    deduplicatedChannels.length === 1 &&
      disabledFallbackChannels.length === 0 &&
      defaultChannelOverride.length === 1,
    'channel identity or explicit fallback suppression is not deterministic',
  );

  const sourceIncident = transitionConnectorNotificationIncident(
    blankConnectorNotificationIncident('source_collection'),
    'source_collection',
    'source-fingerprint',
    firstAt,
  );
  const notifiedSource = markConnectorIncidentNotification(
    sourceIncident,
    [{ sent: true, external: true, target: 'validator' }],
    firstAt,
  );
  assertNotificationStateValidation(
    notifiedProbe.lastExternalAlertedFingerprint === 'probe-fingerprint',
    'probe external fingerprint was not retained',
  );
  assertNotificationStateValidation(
    notifiedSource.lastExternalAlertedFingerprint === 'source-fingerprint',
    'source external fingerprint was not retained independently',
  );
  const independentStore = {
    ...migrated,
    [CONNECTOR_PROBE_INCIDENT_KEY]: notifiedProbe,
    [SOURCE_COLLECTION_INCIDENT_KEY]: notifiedSource,
  };
  const sourceAfterAnotherObservation = transitionConnectorNotificationIncident(
    independentStore[SOURCE_COLLECTION_INCIDENT_KEY],
    'source_collection',
    'source-fingerprint',
    secondAt,
  );
  const storeAfterSourceObservation = {
    ...independentStore,
    [SOURCE_COLLECTION_INCIDENT_KEY]: sourceAfterAnotherObservation,
  };
  assertNotificationStateValidation(
    storeAfterSourceObservation[CONNECTOR_PROBE_INCIDENT_KEY]
      .lastExternalAlertedFingerprint === 'probe-fingerprint',
    'source observation overwrote the connector-probe fingerprint',
  );

  const recoveredSource = transitionConnectorNotificationIncident(
    notifiedSource,
    'source_collection',
    null,
    recoveredAt,
  );
  assertNotificationStateValidation(
    recoveredSource.status === 'recovered',
    'source recovery transition not modeled',
  );
  assertNotificationStateValidation(
    shouldNotifyConnectorIncident(notifiedSource, recoveredSource),
    'first recovery would not be emitted',
  );
  const notifiedRecovery = markConnectorIncidentNotification(
    recoveredSource,
    [{ sent: true, external: true, target: 'validator' }],
    recoveredAt,
  );
  const stillRecoveredSource = transitionConnectorNotificationIncident(
    notifiedRecovery,
    'source_collection',
    null,
    '2026-07-23T10:15:00.000Z',
  );
  assertNotificationStateValidation(
    !shouldNotifyConnectorIncident(notifiedRecovery, stillRecoveredSource),
    'successfully delivered recovery would be emitted more than once',
  );
  const failedRecovery = markConnectorIncidentNotification(
    recoveredSource,
    [{ sent: false, external: true, target: 'validator' }],
    recoveredAt,
  );
  const retryableRecovery = transitionConnectorNotificationIncident(
    failedRecovery,
    'source_collection',
    null,
    '2026-07-23T10:15:00.000Z',
  );
  assertNotificationStateValidation(
    shouldNotifyConnectorIncident(failedRecovery, retryableRecovery),
    'failed external recovery delivery would not be retried',
  );
  const recurringSource = transitionConnectorNotificationIncident(
    notifiedRecovery,
    'source_collection',
    'source-fingerprint',
    '2026-07-23T10:20:00.000Z',
  );
  assertNotificationStateValidation(
    recurringSource.status === 'new' &&
      shouldNotifyConnectorIncident(notifiedRecovery, recurringSource),
    'same incident fingerprint did not become new after recovery',
  );
  assertNotificationStateValidation(
    buildConnectorRecoveryAlert('source_collection').trim() ===
      'Data collection recovered.',
    'recovery output is not compact',
  );
  const recoveryNotification = buildConnectorSocialNotification(
    { generatedAt: recoveredAt },
    [],
    'source-fingerprint',
    { kind: 'source_collection', status: 'recovered' },
  );
  const recoveryDiscordPayload = buildDiscordSocialPayload(recoveryNotification);
  const recoveryDiscordEmbed: any = recoveryDiscordPayload.embeds?.[0];
  assertNotificationStateValidation(
    recoveryDiscordPayload.embeds?.length === 1 &&
      recoveryDiscordEmbed &&
      Array.isArray(recoveryDiscordEmbed.fields) &&
      recoveryDiscordEmbed.fields.length <= 2,
    'Discord recovery output is not a compact single embed',
  );
  const timeoutFingerprintA = buildConnectorHealthFingerprint([
    {
      key: 'asc_cli',
      status: 'partial',
      detail: 'Timed out after 120000ms; request id first-123',
      nextAction: 'Retry later.',
    },
  ]);
  const timeoutFingerprintB = buildConnectorHealthFingerprint([
    {
      key: 'asc_cli',
      status: 'partial',
      detail: 'Timed out after 180000ms; request id second-456',
      nextAction: 'Retry later.',
    },
  ]);
  assertNotificationStateValidation(
    timeoutFingerprintA === timeoutFingerprintB,
    'volatile timeout/request diagnostics changed the incident fingerprint',
  );
  const groupedSourceFailures = buildSourceFailureStatusPayload(
    '/host/config.json',
    [
      {
        key: 'glitchtip',
        service: 'sentry',
        detail: 'first account failed',
      },
      {
        key: 'glitchtip',
        service: 'sentry',
        detail: 'second account failed',
      },
    ],
  );
  const groupedSourceConnectors: any = groupedSourceFailures.connectors;
  assertNotificationStateValidation(
    Object.keys(groupedSourceConnectors).length === 1 &&
      groupedSourceConnectors.sentry?.failureCount === 2 &&
      groupedSourceConnectors.sentry?.failures?.length === 2,
    'multiple failures for one provider overwrote one another',
  );
  const migratedDeliveredIncident = normalizeConnectorNotificationIncident(
    {
      activeFingerprint: 'legacy-delivered',
      lastNotifiedFingerprint: 'legacy-delivered',
      lastNotificationExternalSent: true,
    },
    'connector_probe',
  );
  const migratedOngoingIncident = transitionConnectorNotificationIncident(
    migratedDeliveredIncident,
    'connector_probe',
    'legacy-delivered',
    secondAt,
  );
  assertNotificationStateValidation(
    pendingConnectorIncidentChannelKeys(
      migratedDeliveredIncident,
      migratedOngoingIncident,
      ['discord:migrated'],
    ).length === 0,
    'legacy delivered incident would emit a surprise migration alert',
  );
  const firstSlackEnv = 'ANALYTICSCLI_VALIDATION_SLACK_A';
  const secondSlackEnv = 'ANALYTICSCLI_VALIDATION_SLACK_B';
  process.env[firstSlackEnv] = 'https://hooks.example.test/same-target';
  process.env[secondSlackEnv] = 'https://hooks.example.test/same-target';
  const firstTargetKey = notificationChannelKey({
    type: 'slack',
    webhookEnv: firstSlackEnv,
  });
  const aliasTargetKey = notificationChannelKey({
    type: 'slack',
    webhookEnv: secondSlackEnv,
  });
  process.env[secondSlackEnv] = 'https://hooks.example.test/rotated-target';
  const rotatedTargetKey = notificationChannelKey({
    type: 'slack',
    webhookEnv: secondSlackEnv,
  });
  delete process.env[firstSlackEnv];
  delete process.env[secondSlackEnv];
  assertNotificationStateValidation(
    firstTargetKey === aliasTargetKey &&
      firstTargetKey !== rotatedTargetKey,
    'channel receipts did not follow the resolved transport target',
  );

  return {
    ok: true,
    version: CONNECTOR_NOTIFICATION_STATE_VERSION,
    transitions: ['new', 'ongoing', 'recovered'],
    retryPolicy: 'per-channel until every configured delivery succeeds',
    independentIncidentKeys: [
      CONNECTOR_PROBE_INCIDENT_KEY,
      SOURCE_COLLECTION_INCIDENT_KEY,
    ],
  };
}

function humanConnectorName(key) {
  if (key === 'analyticscli') return 'AnalyticsCLI';
  if (key === 'appStoreConnect') return 'App Store Connect';
  if (key === 'revenuecat') return 'RevenueCat';
  if (key === 'sentry') return 'Sentry';
  if (key === 'github') return 'GitHub';
  return key;
}

function connectorWizardKey(key) {
  if (key === 'analyticscli') return 'analytics';
  if (key === 'appStoreConnect') return 'asc';
  if (key === 'revenuecat') return 'revenuecat';
  if (key === 'sentry') return 'sentry';
  if (key === 'github') return 'github';
  return '';
}

function buildConnectorWizardCommand(configPath, entry) {
  const connector = connectorWizardKey(entry.key);
  if (!connector) return null;
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
  if (!detail) return 'needs attention.';
  return detail.length > 180 ? `${detail.slice(0, 177)}...` : detail;
}

function connectorNotificationAction(entry, incidentKind) {
  const connector = humanizeNotificationIdentifier(entry?.key);
  if (incidentKind === 'source_collection') {
    if (/transient|upstream|network|retry/i.test(`${entry?.detail || ''} ${entry?.nextAction || ''}`)) {
      return 'Growth Engineer will retry automatically. If this repeats, check provider availability and credentials.';
    }
    return `Check the ${connector} credentials or source setup in the host terminal.`;
  }
  return `Complete the ${connector} connector setup in the host terminal.`;
}

function buildConnectorSocialNotification(
  statusPayload,
  unhealthyConnectors,
  fingerprint,
  incident = { kind: 'connector_probe', status: 'new' },
): SocialNotification {
  const generatedAt = String(statusPayload?.generatedAt || new Date().toISOString());
  const sourceCollection = incident.kind === 'source_collection';
  const recovered = incident.status === 'recovered';
  const count = unhealthyConnectors.length;
  const blocked = unhealthyConnectors.some(
    (entry) => String(entry?.status || '').toLowerCase() === 'blocked',
  );

  if (recovered) {
    return {
      schema: 'analyticscli.social-notification',
      version: 1,
      kind: 'recovery',
      state: 'recovered',
      severity: 'success',
      title: sourceCollection ? 'Data collection recovered' : 'Connector health recovered',
      summary: sourceCollection
        ? 'All configured sources are responding again.'
        : 'All configured connections are healthy again.',
      items: [],
      nextStep: 'No action needed.',
      automation: 'Monitoring continues automatically.',
      generatedAt,
      fingerprint: String(fingerprint || '') || undefined,
      scope: String(statusPayload?.configPath || '') || undefined,
    };
  }

  return {
    schema: 'analyticscli.social-notification',
    version: 1,
    kind: sourceCollection ? 'source_collection' : 'connector_health',
    state: incident.status === 'ongoing' ? 'ongoing' : 'new',
    severity: blocked ? 'critical' : 'warning',
    title: sourceCollection ? 'Data collection degraded' : 'Connector setup incomplete',
    summary: `${count} ${sourceCollection ? (count === 1 ? 'source is' : 'sources are') : count === 1 ? 'connection is' : 'connections are'} affected.`,
    impact: sourceCollection
      ? 'This analysis may be incomplete; healthy sources were still processed.'
      : 'Data from affected connections may be missing until setup is complete.',
    items: unhealthyConnectors.map((entry) => ({
      id: String(entry?.key || ''),
      label: humanizeNotificationIdentifier(entry?.label || entry?.key),
      status: humanizeNotificationIdentifier(entry?.status || 'needs attention'),
      summary: humanizeConnectorDiagnostic(entry?.detail),
      action: connectorNotificationAction(entry, incident.kind),
    })),
    nextStep: sourceCollection
      ? 'Review the affected sources; automatic collection will retry on the next scheduled run.'
      : 'Finish the affected connector setup in the host terminal.',
    automation: sourceCollection
      ? 'Growth Engineer keeps processing healthy sources and retries failed collection.'
      : 'Growth Engineer will verify coverage again automatically.',
    generatedAt,
    fingerprint: String(fingerprint || '') || undefined,
    scope: String(statusPayload?.configPath || '') || undefined,
  };
}

function buildConnectorHealthAlert(
  statusPayload,
  unhealthyConnectors,
  incidentKind = 'connector_probe',
) {
  return renderSocialNotificationMarkdown(
    buildConnectorSocialNotification(
      statusPayload,
      unhealthyConnectors,
      buildConnectorHealthFingerprint(unhealthyConnectors),
      { kind: incidentKind, status: 'new' },
    ),
  );
}

function sourceFailureConnectorKey(failure) {
  const service = String(failure?.service || '').toLowerCase();
  const key = String(failure?.key || '').toLowerCase();
  const source = String(failure?.source || '').toLowerCase();
  if (service.includes('sentry') || key === 'glitchtip') return 'sentry';
  if (source === 'sentry' || source === 'glitchtip') return 'sentry';
  if (service.includes('revenuecat')) return 'revenuecat';
  if (service.includes('paddle')) return 'paddle';
  if (service.includes('seo') || service.includes('gsc') || service.includes('search-console') || service.includes('dataforseo')) return 'seo';
  if (key === 'paddle') return 'paddle';
  if (key === 'seo') return 'seo';
  if (service.includes('coolify')) return 'coolify';
  if (service.includes('github')) return 'github';
  if (key === 'analytics') return 'analyticscli';
  return String(failure?.key || 'source');
}

function getSentryAccountTargets(config) {
  const accounts = Array.isArray(config?.sources?.sentry?.accounts) ? config.sources.sentry.accounts : [];
  if (accounts.length === 0) return [];
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
  const groupedFailures = new Map();
  for (const failure of sourceFailures) {
    const key = sourceFailureConnectorKey(failure);
    const current = groupedFailures.get(key) || [];
    current.push(failure);
    groupedFailures.set(key, current);
  }
  for (const [key, failures] of groupedFailures.entries()) {
    const retryable = failures.every((failure) =>
      Boolean(failure.retryable || failure.transient),
    );
    const detail =
      failures.length === 1
        ? `Source collection failed during scheduled run: ${failures[0].detail}`
        : `${failures.length} ${humanizeNotificationIdentifier(key)} source/account collections failed during the scheduled run.`;
    connectors[key] = {
      label: humanizeNotificationIdentifier(key),
      status: 'partial',
      detail,
      failureCount: failures.length,
      failures: failures.map((failure) => ({
        key: failure.key || failure.source || key,
        service: failure.service || null,
        detail: failure.detail,
        retryable: Boolean(failure.retryable || failure.transient),
      })),
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
  const healthState = state?.connectorHealth || {};
  const checkedAt = new Date().toISOString();
  const statusPayload = buildSourceFailureStatusPayload(configPath, sourceFailures, config);
  const unhealthyConnectors = getUnhealthyConfiguredConnectors(statusPayload);
  const fingerprint =
    unhealthyConnectors.length > 0
      ? buildConnectorHealthFingerprint(unhealthyConnectors)
      : null;
  const incidents = getConnectorNotificationIncidents(state);
  const previousIncident = incidents[SOURCE_COLLECTION_INCIDENT_KEY];
  let nextIncident = transitionConnectorNotificationIncident(
    previousIncident,
    'source_collection',
    fingerprint,
    checkedAt,
  );
  const configuredChannelKeys = getConnectorHealthChannelKeys(config);
  const pendingChannelKeys = pendingConnectorIncidentChannelKeys(
    previousIncident,
    nextIncident,
    configuredChannelKeys,
  );
  const shouldNotify =
    config?.notifications?.connectorHealth?.enabled !== false &&
    shouldNotifyConnectorIncident(
      previousIncident,
      nextIncident,
      configuredChannelKeys,
    );
  let notificationTriggered = false;
  let notificationDeliveries: any[] = [];
  let alertPaths: { markdownPath: string; jsonPath: string } | null = null;

  if (shouldNotify) {
    const notificationFingerprint =
      nextIncident.activeFingerprint || nextIncident.recoveredFingerprint;
    const socialNotification = buildConnectorSocialNotification(
      statusPayload,
      unhealthyConnectors,
      notificationFingerprint,
      {
        kind: 'source_collection',
        status: nextIncident.status,
      },
    );
    const message = renderSocialNotificationMarkdown(socialNotification);
    alertPaths = await writeConnectorHealthAlert(
      runtimeDir,
      message,
      statusPayload,
      unhealthyConnectors,
      notificationFingerprint,
      {
        kind: 'source_collection',
        status: nextIncident.status,
      },
      socialNotification,
    );
    notificationDeliveries = await deliverConnectorHealthAlert({
      config,
      configPath,
      message,
      statusPayload,
      unhealthyConnectors,
      fingerprint: notificationFingerprint,
      incident: {
        kind: 'source_collection',
        status: nextIncident.status,
      },
      notification: socialNotification,
      onlyChannelKeys: pendingChannelKeys,
    });
    notificationTriggered = true;
    nextIncident = {
      ...markConnectorIncidentNotification(
        nextIncident,
        notificationDeliveries,
        checkedAt,
        configuredChannelKeys,
      ),
      lastAlertMarkdownPath: alertPaths.markdownPath,
      lastAlertJsonPath: alertPaths.jsonPath,
    };
  }

  const nextHealthState: Record<string, any> = {
    ...healthState,
    incidents: {
      ...incidents,
      version: CONNECTOR_NOTIFICATION_STATE_VERSION,
      [SOURCE_COLLECTION_INCIDENT_KEY]: nextIncident,
    },
    sourceCollectionLastCheckedAt: checkedAt,
    sourceCollectionLastStatusOk: sourceFailures.length === 0,
    sourceCollectionLastFingerprint: fingerprint,
    sourceCollectionLastError:
      sourceFailures.length > 0
        ? sourceFailures
            .map((failure) => `${failure.key || failure.source}: ${failure.detail}`)
            .join('\n')
        : null,
  };

  const nextState = {
    ...state,
    connectorHealth: nextHealthState,
    lastSourceCollectionFailures: sourceFailures,
  };
  await fs.mkdir(path.dirname(statePath), { recursive: true });
  await writeJsonAtomic(statePath, nextState);
  await appendSchedulerProof(
    sourceFailures.length > 0
      ? 'source_collection_degraded'
      : previousIncident.activeFingerprint
        ? 'source_collection_recovered'
        : 'source_collection_healthy',
    {
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
    incidentStatus: nextIncident.status,
    activeIncidentFingerprint: nextIncident.activeFingerprint,
    notificationTriggered,
    alertTriggered: notificationTriggered,
    deliveryCount: notificationDeliveries.length,
    externalDeliverySent: notificationTriggered
      ? hasSuccessfulExternalDelivery(notificationDeliveries)
      : false,
    socialOutput: notificationTriggered
      ? nextIncident.status === 'recovered'
        ? 'CONNECTOR_HEALTH_RECOVERED'
        : 'CONNECTOR_HEALTH_ALERT'
      : 'HEARTBEAT_OK',
    socialReason: notificationTriggered
      ? nextIncident.status === 'recovered'
        ? 'source-collection incident recovered'
        : nextIncident.status === 'ongoing'
          ? 'retrying unchanged source-collection incident after failed external delivery'
          : 'new or changed source-collection connector incident'
      : sourceFailures.length > 0
        ? 'source-collection connector incident ongoing and unchanged'
        : 'source collection remains healthy',
    },
  );
  return nextState;
}

async function writeConnectorHealthAlert(
  runtimeDir,
  message,
  statusPayload,
  unhealthyConnectors,
  fingerprint,
  incident = { kind: 'connector_probe', status: 'new' },
  notification = null,
) {
  const alertDir = path.join(runtimeDir, 'connector-health');
  await ensureDir(alertDir);
  const filePrefix =
    incident.kind === 'source_collection' ? 'source-collection-latest' : 'latest';
  const markdownPath = path.join(alertDir, `${filePrefix}.md`);
  const jsonPath = path.join(alertDir, `${filePrefix}.json`);
  await fs.writeFile(markdownPath, message, 'utf8');
  await fs.writeFile(
    jsonPath,
    JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        fingerprint,
        incident,
        ...(notification
          ? { notification: socialNotificationSummary(notification) }
          : {}),
        unhealthyConnectors,
        status: statusPayload,
      },
      null,
      2,
    ),
    'utf8',
  );
  return { markdownPath, jsonPath };
}

function notificationChannelKey(channel) {
  const type = String(channel?.type || 'openclaw-chat').trim().toLowerCase();
  if (type === 'openclaw-chat') {
    const markdownPath = String(channel?.markdownPath || '').trim();
    const jsonPath = String(channel?.jsonPath || '').trim();
    return `openclaw-chat:path-${sha256(`${markdownPath}|${jsonPath}`).slice(0, 16)}`;
  }
  if (type === 'slack') {
    const envName = String(
      channel?.webhookEnv || 'SLACK_WEBHOOK_URL',
    ).trim();
    const target = process.env[envName] || `env:${envName}`;
    return `slack:target-${sha256(target).slice(0, 16)}`;
  }
  if (type === 'webhook') {
    const envName = String(
      channel?.urlEnv || channel?.webhookEnv || 'OPENCLAW_WEBHOOK_URL',
    ).trim();
    const target = process.env[envName] || `env:${envName}`;
    const method = String(channel?.method || 'POST').trim().toUpperCase();
    const headers = stableStringify(channel?.headers || {});
    return `webhook:target-${sha256(`${target}|${method}|${headers}`).slice(0, 16)}`;
  }
  if (type === 'discord') {
    return `discord:command-${sha256(String(channel?.command || '').trim()).slice(0, 16)}`;
  }
  if (type === 'command') {
    return `command:${sha256(String(channel?.command || '').trim()).slice(0, 16)}`;
  }
  return `${type}:${sha256(
    String(
      channel?.command || channel?.urlEnv || channel?.webhookEnv || '',
    ).trim(),
  ).slice(0, 16)}`;
}

function notificationChannelHasExplicitIdentity(channel) {
  const type = String(channel?.type || 'openclaw-chat').trim().toLowerCase();
  if (type === 'openclaw-chat') {
    return Boolean(
      String(channel?.markdownPath || '').trim() ||
        String(channel?.jsonPath || '').trim(),
    );
  }
  if (type === 'slack') return Boolean(String(channel?.webhookEnv || '').trim());
  if (type === 'webhook') {
    return Boolean(
      String(channel?.urlEnv || channel?.webhookEnv || '').trim(),
    );
  }
  if (type === 'discord' || type === 'command') {
    return Boolean(String(channel?.command || '').trim());
  }
  return false;
}

function mergeNotificationChannelsWithDeliveries(configuredChannels, deliveryChannels) {
  const configured = Array.isArray(configuredChannels) ? configuredChannels : [];
  const disabledKeys = new Set(
    configured
      .filter(
        (channel) =>
          channel?.enabled === false &&
          notificationChannelHasExplicitIdentity(channel),
      )
      .map((channel) => notificationChannelKey(channel)),
  );
  const disabledTypes = new Set(
    configured
      .filter(
        (channel) =>
          channel?.enabled === false &&
          !notificationChannelHasExplicitIdentity(channel),
      )
      .map((channel) => String(channel?.type || 'openclaw-chat')),
  );
  const configuredTypeOverrides = new Set(
    configured
      .filter(
        (channel) =>
          channel?.enabled !== false &&
          !notificationChannelHasExplicitIdentity(channel),
      )
      .map((channel) => String(channel?.type || 'openclaw-chat')),
  );
  const channels = [];
  const seen = new Set();
  const appendChannel = (channel) => {
    const key = notificationChannelKey(channel);
    const type = String(channel?.type || 'openclaw-chat');
    if (
      seen.has(key) ||
      disabledKeys.has(key) ||
      disabledTypes.has(type)
    ) {
      return;
    }
    channels.push(channel);
    seen.add(key);
  };
  for (const channel of configured.filter(
    (entry) => entry?.enabled !== false,
  )) {
    appendChannel(channel);
  }
  for (const channel of deliveryChannels) {
    const type = String(channel?.type || 'openclaw-chat');
    if (configuredTypeOverrides.has(type)) continue;
    appendChannel(channel);
  }
  return channels;
}

function socialNotificationEventId(notification) {
  return canonicalSocialNotificationEventId(notification);
}

function notificationScope(config, configPath = '') {
  return String(
    config?.project?.githubRepo ||
      config?.project?.repoRoot ||
      config?.project?.name ||
      configPath ||
      'growth-engineer',
  ).trim();
}

function safeDeliveryErrorDetail(error) {
  const value = error instanceof Error ? error.message : String(error || 'delivery failed');
  return value
    .replace(/https?:\/\/[^\s]+/gi, '[endpoint]')
    .replace(/(?:token|secret|authorization|api[-_ ]?key)\s*[:=]\s*\S+/gi, '$1=[redacted]')
    .replace(
      /\/(?:home|Users|private|tmp|var|opt)\/[^\s)"'`]+/g,
      '[host path]',
    )
    .slice(0, 320);
}

function discordDeliveryEnvironment(notification) {
  return {
    OPENCLAW_DISCORD_DELIVERY_FORMAT: 'embed',
    OPENCLAW_NOTIFICATION_EVENT_ID: socialNotificationEventId(notification),
    OPENCLAW_DISCORD_RECEIPT_PATH: path.join(
      path.dirname(schedulerProofPath),
      'discord-delivery-receipts.json',
    ),
  };
}

function sanitizeOutboundPayload(value, key = '') {
  if (
    /(?:authorization|password|private.?key|api.?key|access.?token|refresh.?token|secret)/i.test(
      key,
    ) &&
    !/(?:env|name)$/i.test(key)
  ) {
    return '[redacted]';
  }
  if (typeof value === 'string') {
    return value
      .replace(/\bBearer\s+[A-Za-z0-9._~+/=-]+/gi, 'Bearer [redacted]')
      .replace(
        /\b(token|secret|password|authorization|api[-_ ]?key)\s*[:=]\s*["']?[^\s"',;}]+/gi,
        '$1=[redacted]',
      )
      .replace(
        /\/(?:home|Users|private|tmp|var|opt)\/[^\s)"'`]+/g,
        '[host path]',
      );
  }
  if (Array.isArray(value)) {
    return value.map((entry) => sanitizeOutboundPayload(entry));
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([entryKey, entryValue]) => [
        entryKey,
        sanitizeOutboundPayload(entryValue, entryKey),
      ]),
    );
  }
  return value;
}

async function sendNotificationHttpRequest(url, init, maxAttempts = 2) {
  let lastStatus = null;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const response = await fetch(url, {
        ...init,
        signal: AbortSignal.timeout(15_000),
      });
      lastStatus = response.status;
      if (response.ok) {
        return {
          sent: true,
          detail: `HTTP ${response.status}`,
          attemptCount: attempt,
        };
      }
      const retryable = response.status === 429 || response.status >= 500;
      if (!retryable || attempt >= maxAttempts) {
        return {
          sent: false,
          detail: `HTTP ${response.status}`,
          attemptCount: attempt,
          retryable,
        };
      }
      const retryAfterSeconds = Number(response.headers.get('retry-after'));
      const delayMs = Number.isFinite(retryAfterSeconds)
        ? Math.min(5_000, Math.max(250, retryAfterSeconds * 1_000))
        : 750 * attempt;
      await new Promise((resolvePromise) => setTimeout(resolvePromise, delayMs));
    } catch (error) {
      if (attempt >= maxAttempts) {
        return {
          sent: false,
          detail: safeDeliveryErrorDetail(error),
          attemptCount: attempt,
          retryable: true,
        };
      }
      await new Promise((resolvePromise) => setTimeout(resolvePromise, 500 * attempt));
    }
  }
  return {
    sent: false,
    detail: lastStatus ? `HTTP ${lastStatus}` : 'delivery failed',
    attemptCount: maxAttempts,
    retryable: true,
  };
}

function getDeliveryNotificationChannels(config, kind) {
  const channels = [];
  const deliveries = config?.deliveries || {};
  if (deliveries.openclawChat?.enabled) {
    const isConnectorHealth = kind === 'connectorHealth';
    channels.push({
      type: 'openclaw-chat',
      label: 'openclaw_chat',
      legacyCompatible: true,
      markdownPath: isConnectorHealth
        ? deliveries.openclawChat.connectorHealthMarkdownPath || deliveries.openclawChat.markdownPath
        : deliveries.openclawChat.growthRunMarkdownPath ||
          deliveries.openclawChat.markdownPath ||
          '.openclaw/chat/growth-summary.md',
      jsonPath: isConnectorHealth
        ? deliveries.openclawChat.connectorHealthJsonPath || deliveries.openclawChat.jsonPath
        : deliveries.openclawChat.growthRunJsonPath ||
          deliveries.openclawChat.jsonPath ||
          '.openclaw/chat/growth-summary.json',
    });
  }
  if (deliveries.slack?.enabled) {
    channels.push({
      type: 'slack',
      label: 'slack',
      webhookEnv: deliveries.slack.webhookEnv || 'SLACK_WEBHOOK_URL',
      username: deliveries.slack.username,
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

function getConnectorHealthChannelKeys(config) {
  if (config?.notifications?.connectorHealth?.enabled === false) return [];
  return getConnectorHealthChannels(config).map((channel) =>
    notificationChannelKey(channel),
  );
}

function resolveOpenClawChatDeliveryPath(channelPath, fallbackPath) {
  const targetPath = String(channelPath || fallbackPath || '').trim();
  if (!targetPath) return path.resolve(process.cwd(), fallbackPath);
  return path.isAbsolute(targetPath) ? targetPath : path.resolve(process.cwd(), targetPath);
}

async function writeConfiguredOpenClawChatAlert(
  configPath,
  channel,
  message,
  statusPayload,
  unhealthyConnectors,
  fingerprint,
  incident,
  notification,
) {
  const markdownPath = resolveOpenClawChatDeliveryPath(channel.markdownPath, '.openclaw/chat/connector-health.md');
  const jsonPath = resolveOpenClawChatDeliveryPath(channel.jsonPath, '.openclaw/chat/connector-health.json');
  const payload = {
    channel: channel.label || 'openclaw_chat',
    generatedAt: new Date().toISOString(),
    fingerprint,
    incident,
    schemaVersion: 1,
    eventId: socialNotificationEventId(notification),
    notification: socialNotificationSummary(notification),
    unhealthyConnectors,
    status: statusPayload,
  };
  await fs.mkdir(path.dirname(markdownPath), { recursive: true });
  await fs.mkdir(path.dirname(jsonPath), { recursive: true });
  await fs.writeFile(markdownPath, message, 'utf8');
  await writeJsonAtomic(jsonPath, payload);
  const incidentBaseName =
    incident?.kind === 'source_collection'
      ? 'source-collection'
      : 'connector-health';
  const incidentMarkdownPath = path.join(
    path.dirname(markdownPath),
    `${incidentBaseName}.md`,
  );
  const incidentJsonPath = path.join(
    path.dirname(jsonPath),
    `${incidentBaseName}.json`,
  );
  if (
    incidentMarkdownPath !== markdownPath ||
    incidentJsonPath !== jsonPath
  ) {
    await fs.mkdir(path.dirname(incidentMarkdownPath), { recursive: true });
    await fs.mkdir(path.dirname(incidentJsonPath), { recursive: true });
    await fs.writeFile(incidentMarkdownPath, message, 'utf8');
    await writeJsonAtomic(incidentJsonPath, payload);
  }
  return {
    sent: true,
    external: false,
    target: channel.label || 'openclaw_chat',
    detail: `wrote local OpenClaw chat outbox and ${incidentBaseName} incident snapshot`,
  };
}

async function sendSlackConnectorHealthAlert(channel, notification) {
  const webhookEnv = channel.webhookEnv || 'SLACK_WEBHOOK_URL';
  const webhookUrl = process.env[webhookEnv];
  if (!webhookUrl) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'slack',
      detail: `${webhookEnv} not set`,
      retryable: false,
    };
  }
  const payload = {
    ...buildSlackSocialPayload(notification),
    ...(channel.username ? { username: channel.username } : {}),
  };
  const result = await sendNotificationHttpRequest(webhookUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return {
    ...result,
    external: true,
    target: channel.label || 'slack',
  };
}

async function sendWebhookConnectorHealthAlert(
  channel,
  message,
  statusPayload,
  unhealthyConnectors,
  fingerprint,
  incident,
  notification,
) {
  const urlEnv = channel.urlEnv || channel.webhookEnv || 'OPENCLAW_WEBHOOK_URL';
  const webhookUrl = process.env[urlEnv];
  if (!webhookUrl) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'webhook',
      detail: `${urlEnv} not set`,
      retryable: false,
    };
  }
  const result = await sendNotificationHttpRequest(webhookUrl, {
    method: channel.method || 'POST',
    headers: {
      'content-type': 'application/json',
      ...(channel.headers || {}),
    },
    body: JSON.stringify({
      type: 'openclaw.connector_health',
      schemaVersion: 1,
      eventId: socialNotificationEventId(notification),
      generatedAt: new Date().toISOString(),
      text: message,
      fingerprint,
      incident,
      notification: socialNotificationSummary(notification),
      unhealthyConnectors: sanitizeOutboundPayload(unhealthyConnectors),
      status: sanitizeOutboundPayload(statusPayload),
    }),
  });
  return {
    ...result,
    external: true,
    target: channel.label || 'webhook',
  };
}

async function sendCommandConnectorHealthAlert(channel, message) {
  if (!channel.command) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'command',
      detail: 'command not configured',
      retryable: false,
    };
  }
  const result = await runShellCommand(String(channel.command), 60_000, { input: message });
  return {
    sent: result.ok,
    external: true,
    target: channel.label || 'command',
    detail: result.ok
      ? 'sent'
      : safeDeliveryErrorDetail(
          result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
        ),
  };
}

async function sendDiscordConnectorHealthAlert(
  channel,
  message,
  statusPayload,
  unhealthyConnectors,
  fingerprint,
  incident,
  notification,
) {
  if (!channel.command) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'discord',
      detail: 'discord command not configured',
      retryable: false,
    };
  }
  const payload = buildDiscordSocialPayload(notification);
  const result = await runShellCommand(String(channel.command), 60_000, {
    input: JSON.stringify(payload),
    env: discordDeliveryEnvironment(notification),
  });
  return {
    sent: result.ok,
    external: true,
    target: channel.label || 'discord',
    detail: result.ok
      ? 'sent'
      : safeDeliveryErrorDetail(
          result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
        ),
  };
}

function getRunnerFailureChannels(config) {
  const candidates = [];
  if (config?.notifications?.connectorHealth?.enabled !== false) {
    candidates.push(...getConnectorHealthChannels(config));
  }
  if (config?.notifications?.growthRun?.enabled !== false) {
    candidates.push(...getGrowthRunChannels(config));
  }
  const byKey = new Map();
  for (const channel of candidates) {
    byKey.set(notificationChannelKey(channel), channel);
  }
  return [...byKey.values()];
}

async function deliverRunnerFailureNotification({
  config,
  configPath,
  notification,
  onlyChannelKeys = null,
}) {
  const message = renderSocialNotificationMarkdown(notification);
  const selectedChannelKeys = Array.isArray(onlyChannelKeys)
    ? new Set(onlyChannelKeys)
    : null;
  const channels = getRunnerFailureChannels(config).filter(
    (channel) =>
      !selectedChannelKeys ||
      selectedChannelKeys.has(notificationChannelKey(channel)),
  );
  const results = [];
  for (const channel of channels) {
    const channelKey = notificationChannelKey(channel);
    try {
      let result;
      if (channel.type === 'openclaw-chat') {
        const configuredMarkdownPath = resolveOpenClawChatDeliveryPath(
          channel.markdownPath,
          '.openclaw/chat/growth-summary.md',
        );
        const configuredJsonPath = resolveOpenClawChatDeliveryPath(
          channel.jsonPath,
          '.openclaw/chat/growth-summary.json',
        );
        const markdownPath = path.join(
          path.dirname(configuredMarkdownPath),
          'runner-failure.md',
        );
        const jsonPath = path.join(
          path.dirname(configuredJsonPath),
          'runner-failure.json',
        );
        await fs.mkdir(path.dirname(markdownPath), { recursive: true });
        await fs.mkdir(path.dirname(jsonPath), { recursive: true });
        await fs.writeFile(markdownPath, message, 'utf8');
        await writeJsonAtomic(jsonPath, {
          channel: channel.label || 'openclaw_chat',
          generatedAt: notification.generatedAt,
          schemaVersion: 1,
          eventId: socialNotificationEventId(notification),
          notification: socialNotificationSummary(notification),
        });
        result = {
          sent: true,
          external: false,
          target: channel.label || 'openclaw_chat',
          detail: 'wrote local runner-failure outbox',
        };
      } else if (channel.type === 'slack') {
        result = await sendSlackConnectorHealthAlert(channel, notification);
      } else if (channel.type === 'webhook') {
        const urlEnv =
          channel.urlEnv ||
          channel.webhookEnv ||
          'OPENCLAW_WEBHOOK_URL';
        const webhookUrl = process.env[urlEnv];
        result = webhookUrl
          ? {
              ...(await sendNotificationHttpRequest(webhookUrl, {
                method: channel.method || 'POST',
                headers: {
                  'content-type': 'application/json',
                  ...(channel.headers || {}),
                },
                body: JSON.stringify({
                  type: 'openclaw.runner_failure',
                  schemaVersion: 1,
                  eventId: socialNotificationEventId(notification),
                  generatedAt: notification.generatedAt,
                  text: message,
                  notification: socialNotificationSummary(notification),
                }),
              })),
              external: true,
              target: channel.label || 'webhook',
            }
          : {
              sent: false,
              external: true,
              target: channel.label || 'webhook',
              detail: `${urlEnv} not set`,
              retryable: false,
            };
      } else if (channel.type === 'discord') {
        result = await sendDiscordConnectorHealthAlert(
          channel,
          message,
          null,
          [],
          notification.fingerprint,
          { kind: 'runner_failure', status: 'new' },
          notification,
        );
      } else if (channel.type === 'command') {
        result = await sendCommandConnectorHealthAlert(channel, message);
      } else {
        result = {
          sent: false,
          external: channel.type !== 'openclaw-chat',
          target: channel.label || String(channel.type || 'unknown'),
          detail: 'unsupported channel type',
          retryable: false,
        };
      }
      results.push({
        ...result,
        channelKey,
        notification: socialNotificationSummary(notification),
      });
    } catch (deliveryError) {
      results.push({
        sent: false,
        external: channel.type !== 'openclaw-chat',
        target: channel.label || String(channel.type || 'unknown'),
        channelKey,
        detail: safeDeliveryErrorDetail(deliveryError),
        notification: socialNotificationSummary(notification),
      });
    }
  }
  return results;
}

function hasExternalNotificationChannel(channels) {
  return channels.some((channel) => channel?.type && channel.type !== 'openclaw-chat');
}

function hasSuccessfulExternalDelivery(results) {
  return results.some((result) => result?.sent === true && result?.external === true);
}

function discordTruncate(value, maxLength) {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (text.length <= maxLength) return text;
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

function buildDiscordConnectorHealthPayload(
  message,
  statusPayload,
  unhealthyConnectors,
  fingerprint,
  incident = { kind: 'connector_probe', status: 'new' },
) {
  if (incident.status === 'recovered') {
    return {
      content: '',
      embeds: [
        {
          title: `OpenClaw ${incidentLabel(incident.kind)} recovered`,
          color: 0x12b76a,
          footer: {
            text: `CONNECTOR_HEALTH_RECOVERED • ${String(fingerprint || '').slice(0, 12)}`,
          },
          timestamp: statusPayload?.generatedAt || new Date().toISOString(),
        },
      ],
      fallbackText: message,
    };
  }

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
        title:
          incident.kind === 'source_collection'
            ? `OpenClaw source collection: ${unhealthyConnectors.length} issue(s)`
            : `OpenClaw connector health: ${unhealthyConnectors.length} issue(s)`,
        description: 'Secrets stay in the host terminal or secret store.',
        color: connectorStatusColor(unhealthyConnectors),
        fields,
        footer: {
          text: `CONNECTOR_HEALTH_ALERT • ${incident.status.toUpperCase()} • ${String(fingerprint || '').slice(0, 12)}`,
        },
        timestamp: statusPayload?.generatedAt || new Date().toISOString(),
      },
    ],
    fallbackText: message,
  };
}

function truncateMessageText(value, maxLength = 96) {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (text.length <= maxLength) return text;
  return `${text.slice(0, Math.max(0, maxLength - 3)).trim()}...`;
}

function issueProjectLabel(issue) {
  return String(issue?.app || issue?.source_project || issue?.sourceProject || issue?.project || 'unscoped').trim();
}

function issueSourceUrl(issue) {
  const direct = String(issue?.source_url || issue?.sourceUrl || issue?.issue_url || issue?.issueUrl || '').trim();
  if (direct) return direct;
  const body = String(issue?.body || '');
  const match = body.match(/(?:Issue link|Permalink):\s*(https?:\/\/\S+)/i);
  return match ? match[1].replace(/[).,;]+$/, '') : '';
}

function formatIssueSummaryLine(issue, maxTitleLength = 92) {
  const title = truncateMessageText(issue?.title, maxTitleLength);
  const url = issueSourceUrl(issue);
  return url ? `${title} (${url})` : title;
}

function issueOccurredAt(issue) {
  const directCandidates = [
    issue?.occurredAt,
    issue?.occurred_at,
    issue?.lastSeenAt,
    issue?.last_seen_at,
    issue?.lastSeen,
    issue?.latestEventAt,
    issue?.latest_event_at,
    issue?.timestamp,
  ];
  for (const candidate of directCandidates) {
    const value = String(candidate || '').trim();
    if (value && Number.isFinite(Date.parse(value))) return new Date(value).toISOString();
  }
  const text = [
    ...(Array.isArray(issue?.evidence) ? issue.evidence : []),
    issue?.body,
  ]
    .filter(Boolean)
    .join('\n');
  const timestampMatch = text.match(
    /(?:Last seen|Latest sampled event|Latest event|Occurred at):\s*([^\n]+)/i,
  );
  if (!timestampMatch?.[1]) return null;
  const value = timestampMatch[1].replace(/^[`'"\s]+|[`'"\s]+$/g, '');
  return Number.isFinite(Date.parse(value)) ? new Date(value).toISOString() : null;
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
  const historyRetentionDays = Number(raw.historyRetentionDays ?? raw.retentionDays);
  return {
    enabled: raw.enabled !== false,
    eventGrowthMultiplier:
      Number.isFinite(multiplier) && multiplier > 1
        ? multiplier
        : DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MULTIPLIER,
    eventGrowthMinDelta:
      Number.isFinite(minDelta) && minDelta > 0
        ? minDelta
        : DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MIN_DELTA,
    historyRetentionDays:
      Number.isFinite(historyRetentionDays) && historyRetentionDays > 0
        ? historyRetentionDays
        : DEFAULT_DAILY_ISSUE_HISTORY_RETENTION_DAYS,
  };
}

function getDailyRunnerFailureDedupeConfig(config) {
  const raw = config?.schedule?.dailyRunnerFailureDedupe || config?.notifications?.growthRun?.dailyRunnerFailureDedupe || {};
  const retentionDays = Number(raw.retentionDays);
  return {
    enabled: raw.enabled !== false,
    retentionDays:
      Number.isFinite(retentionDays) && retentionDays > 0
        ? retentionDays
        : DEFAULT_DAILY_RUNNER_FAILURE_RETENTION_DAYS,
  };
}

function resolveDailyIssueDedupeTimeZone(config) {
  return String(
    config?.schedule?.timezone ||
      config?.automation?.openclawCron?.timezone ||
      process.env.TZ ||
      'UTC',
  ).trim() || 'UTC';
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
  return Object.fromEntries(
    Object.entries(failures || {}).filter(([, entry]: any) => {
      const lastSeenMs = Date.parse(String(entry?.lastSeenAt || entry?.firstSeenAt || ''));
      return !Number.isFinite(lastSeenMs) || lastSeenMs >= cutoffMs;
    }),
  );
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
    } else if (token === '--state' && next) {
      args.state = next;
      i += 1;
    }
  }
  return args;
}

async function recordRunnerFailure({ configPath, statePath, error, argv = [], now = new Date() }) {
  const errorMessage = truncateDiagnosticText(
    String(
      sanitizeOutboundPayload(
        error instanceof Error ? error.message : String(error),
      ),
    ),
  );
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
  const previousEntry: any = failures[fingerprint] || null;
  const notification: SocialNotification = {
    schema: 'analyticscli.social-notification',
    version: 1,
    kind: 'runner_failure',
    state: 'new',
    severity: 'critical',
    title: 'Growth Engineer run failed',
    summary: 'The scheduled analysis did not complete.',
    impact:
      'Connector checks or growth findings from this run may be incomplete.',
    items: [
      {
        id: 'runner',
        label: 'Automation',
        status: 'Failed',
        summary: safeDeliveryErrorDetail(errorMessage),
        action:
          'Review the sanitized runner diagnostics on the host; the next scheduled run will retry automatically.',
      },
    ],
    nextStep:
      'Check the runner diagnostics and connector availability on the host.',
    automation: 'The next scheduled run will retry automatically.',
    generatedAt: nowIso,
    fingerprint,
    scope: notificationScope(config, configPath),
  };
  const configuredChannels = getRunnerFailureChannels(config);
  const configuredChannelKeys = configuredChannels.map((channel) =>
    notificationChannelKey(channel),
  );
  const previousReceipts =
    previousEntry?.notificationReceipts &&
    typeof previousEntry.notificationReceipts === 'object'
      ? previousEntry.notificationReceipts
      : {};
  const pendingChannelKeys = configuredChannelKeys.filter(
    (key) => previousReceipts[key]?.sent !== true,
  );
  const allConfiguredChannelsPreviouslySent =
    configuredChannelKeys.length === 0 || pendingChannelKeys.length === 0;
  const suppressed =
    dedupeConfig.enabled &&
    Boolean(previousEntry) &&
    allConfiguredChannelsPreviouslySent;
  const notificationDeliveries = suppressed
    ? []
    : await deliverRunnerFailureNotification({
        config,
        configPath,
        notification,
        onlyChannelKeys: pendingChannelKeys,
      });
  const notificationReceipts = { ...previousReceipts };
  for (const delivery of notificationDeliveries) {
    const channelKey = String(
      delivery?.channelKey || delivery?.target || '',
    ).trim();
    if (!channelKey) continue;
    notificationReceipts[channelKey] = {
      sent: delivery?.sent === true,
      external: delivery?.external === true,
      target: delivery?.target || channelKey,
      detail: delivery?.detail || null,
      updatedAt: nowIso,
    };
  }
  const externalDeliverySent = Object.values(notificationReceipts).some(
    (receipt: any) => receipt?.sent === true && receipt?.external === true,
  );
  const nextEntry: Record<string, any> = {
    ...(previousEntry || {}),
    fingerprint,
    error: errorMessage,
    normalizedError: normalizeRunnerFailureForFingerprint(errorMessage),
    firstSeenAt: previousEntry?.firstSeenAt || nowIso,
    lastSeenAt: nowIso,
    notification: socialNotificationSummary(notification),
    notificationDeliveries,
    notificationReceipts,
    notificationAllChannelsSent:
      configuredChannelKeys.length === 0 ||
      configuredChannelKeys.every(
        (key) => notificationReceipts[key]?.sent === true,
      ),
    externalDeliverySent,
  };

  if (suppressed) {
    nextEntry.suppressedCount = Number(previousEntry?.suppressedCount || 0) + 1;
  } else {
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
      notification: socialNotificationSummary(notification),
      notificationDeliveries,
      externalDeliverySent,
    },
  };
  await fs.mkdir(path.dirname(statePath), { recursive: true });
  await writeJsonAtomic(statePath, nextState);
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
    notification: socialNotificationSummary(notification),
    notificationEnabled: true,
    externalDeliverySent,
    deliveryFailed:
      !suppressed &&
      configuredChannelKeys.length > 0 &&
      !notificationDeliveries.some((delivery) => delivery?.sent === true),
    socialOutput: suppressed
      ? 'HEARTBEAT_OK'
      : externalDeliverySent
        ? 'EXTERNAL_NOTIFICATION_SENT'
        : 'RUNNER_FAILED',
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
  } catch {
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
  if (value === null || value === undefined || value === '') return null;
  if (typeof value === 'number') return Number.isFinite(value) ? value : null;
  const normalized = String(value).replace(/,/g, '').trim();
  if (!normalized) return null;
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
    if (number !== null) return number;
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
  if (currentEvents === null || currentEvents === undefined) return false;
  const previousEvents = coerceIssueNumber(
    previousEntry?.lastReportedEvents ?? previousEntry?.lastSeenEvents,
  );
  if (previousEvents === null || previousEvents < 0) return false;
  const requiredEvents = Math.max(
    previousEvents * dedupeConfig.eventGrowthMultiplier,
    previousEvents + dedupeConfig.eventGrowthMinDelta,
  );
  return currentEvents >= requiredEvents;
}

function pruneDailyIssueHistory(
  issues: Record<string, any>,
  now: Date,
  retentionDays: number,
): Record<string, any> {
  const cutoffMs = now.getTime() - retentionDays * 24 * 60 * 60 * 1000;
  return Object.fromEntries(
    Object.entries(issues || {}).filter(([, entry]: any) => {
      const lastSeenMs = Date.parse(
        String(entry?.lastSeenAt || entry?.lastReportedAt || ''),
      );
      return !Number.isFinite(lastSeenMs) || lastSeenMs >= cutoffMs;
    }),
  );
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
  const previousState = state?.dailyIssueReports || null;
  const previousIssues = pruneDailyIssueHistory(
    previousState?.issues && typeof previousState.issues === 'object'
      ? previousState.issues
      : {},
    now,
    dedupeConfig.historyRetentionDays,
  );
  const nextIssues = { ...previousIssues };
  const reportableIssues = [];
  let suppressedCount = 0;
  let hasDrasticEventGrowth = false;

  for (const issue of issues) {
    const key = buildDailyIssueKey(issue);
    const previousEntry = previousIssues[key] || null;
    const events = issueEventCount(issue);
    const shouldReport =
      !previousEntry || isDrasticDailyIssueEventGrowth(events, previousEntry, dedupeConfig);
    const reportReason = !previousEntry ? 'new_daily_issue' : 'event_growth';
    const nextEntry: Record<string, any> = {
      ...(previousEntry || {}),
      title: String(issue?.title || previousEntry?.title || '').slice(0, 240),
      app: issueProjectLabel(issue),
      sourceUrl: issueSourceUrl(issue) || previousEntry?.sourceUrl || null,
      lastSeenAt: nowIso,
      lastSeenEvents: events ?? previousEntry?.lastSeenEvents ?? null,
      occurredAt: issueOccurredAt(issue) || previousEntry?.occurredAt || null,
    };

    if (shouldReport) {
      reportableIssues.push(issue);
      if (previousEntry) hasDrasticEventGrowth = true;
      nextEntry.lastReportedAt = nowIso;
      nextEntry.lastReportedEvents = events ?? previousEntry?.lastReportedEvents ?? null;
      nextEntry.lastReportReason = reportReason;
      nextEntry.reportCount = Number(previousEntry?.reportCount || 0) + 1;
    } else {
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
        historyRetentionDays: dedupeConfig.historyRetentionDays,
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

async function deliverConnectorHealthAlert({
  config,
  configPath,
  message,
  statusPayload,
  unhealthyConnectors,
  fingerprint,
  incident = { kind: 'connector_probe', status: 'new' },
  notification,
  onlyChannelKeys = null,
}) {
  const allChannels = getConnectorHealthChannels(config);
  const selectedChannelKeys = Array.isArray(onlyChannelKeys)
    ? new Set(onlyChannelKeys)
    : null;
  const channels = selectedChannelKeys
    ? allChannels.filter((channel) =>
        selectedChannelKeys.has(notificationChannelKey(channel)),
      )
    : allChannels;
  if (config?.notifications?.connectorHealth?.enabled === false) {
    return [{ sent: false, target: 'notifications', detail: 'connector health notifications disabled' }];
  }
  if (allChannels.length === 0) {
    return [{ sent: false, target: 'none', detail: 'no connector health notification channels configured' }];
  }
  if (channels.length === 0) return [];

  const results = [];
  for (const channel of channels) {
    const channelKey = notificationChannelKey(channel);
    try {
      let result;
      if (channel.type === 'openclaw-chat') {
        result = await writeConfiguredOpenClawChatAlert(
          configPath,
          channel,
          message,
          statusPayload,
          unhealthyConnectors,
          fingerprint,
          incident,
          notification,
        );
      } else if (channel.type === 'slack') {
        result = await sendSlackConnectorHealthAlert(channel, notification);
      } else if (channel.type === 'webhook') {
        result = await sendWebhookConnectorHealthAlert(
          channel,
          message,
          statusPayload,
          unhealthyConnectors,
          fingerprint,
          incident,
          notification,
        );
      } else if (channel.type === 'discord') {
        result = await sendDiscordConnectorHealthAlert(
          channel,
          message,
          statusPayload,
          unhealthyConnectors,
          fingerprint,
          incident,
          notification,
        );
      } else if (channel.type === 'command') {
        result = await sendCommandConnectorHealthAlert(channel, message);
      } else {
        result = {
          sent: false,
          target: channel.label || String(channel.type || 'unknown'),
          detail: 'unsupported channel type',
        };
      }
      results.push({
        ...result,
        channelKey,
        notification: socialNotificationSummary(notification),
      });
    } catch (error) {
      results.push({
        sent: false,
        external: channel.type !== 'openclaw-chat',
        target: channel.label || String(channel.type || 'unknown'),
        channelKey,
        detail: safeDeliveryErrorDetail(error),
        notification: socialNotificationSummary(notification),
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

function getGrowthRunChannelKeys(config) {
  if (config?.notifications?.growthRun?.enabled === false) return [];
  return getGrowthRunChannels(config).map((channel) =>
    notificationChannelKey(channel),
  );
}

function growthRunNotificationEventId(fingerprint) {
  return `growth_findings:summary:${String(fingerprint || 'no-fingerprint')}`;
}

function pendingGrowthRunChannelKeys(previousState, fingerprint, channelKeys) {
  const uniqueKeys: string[] = Array.from(
    new Set<string>(
      (Array.isArray(channelKeys) ? channelKeys : []).map((key: unknown) =>
        String(key),
      ),
    ),
  );
  if (
    previousState?.eventId !== growthRunNotificationEventId(fingerprint)
  ) {
    return uniqueKeys;
  }
  const receipts: Record<string, any> =
    previousState?.receipts && typeof previousState.receipts === 'object'
      ? previousState.receipts
      : {};
  return uniqueKeys.filter((key) => receipts[key]?.sent !== true);
}

function markGrowthRunNotificationState({
  previousState,
  fingerprint,
  deliveries,
  configuredChannelKeys,
  snapshot,
  attemptedAt,
}) {
  const eventId = growthRunNotificationEventId(fingerprint);
  const receipts: Record<string, any> =
    previousState?.eventId === eventId &&
    previousState?.receipts &&
    typeof previousState.receipts === 'object'
      ? { ...previousState.receipts }
      : {};
  for (const delivery of deliveries) {
    const channelKey = String(
      delivery?.channelKey || delivery?.target || '',
    ).trim();
    if (!channelKey || channelKey === 'external_notification') continue;
    receipts[channelKey] = {
      sent: delivery?.sent === true,
      external: delivery?.external === true,
      target: delivery?.target || channelKey,
      detail: delivery?.detail || null,
      retryable: delivery?.retryable !== false,
      attemptCount:
        Number(receipts[channelKey]?.attemptCount || 0) +
        Number(delivery?.attemptCount || 1),
      updatedAt: attemptedAt,
    };
  }
  const channelKeys: string[] = Array.from(
    new Set<string>(
      (Array.isArray(configuredChannelKeys) ? configuredChannelKeys : []).map(
        (key: unknown) => String(key),
      ),
    ),
  );
  const allChannelsSent =
    channelKeys.length === 0 ||
    channelKeys.every((key) => receipts[key]?.sent === true);
  return {
    version: 1,
    eventId,
    fingerprint,
    receipts,
    allChannelsSent,
    lastAttemptAt: attemptedAt,
    completedAt: allChannelsSent ? attemptedAt : null,
    snapshot: allChannelsSent ? null : snapshot,
  };
}

async function readChartAttachments(chartManifestPath) {
  if (!chartManifestPath) return [];
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
  } catch {
    return [];
  }
}

function issueNotificationAction(issue) {
  const directCandidates = [
    issue?.next_step,
    issue?.nextStep,
    issue?.recommendation,
    issue?.proposed_action,
    issue?.proposedAction,
  ];
  for (const candidate of directCandidates) {
    const value = Array.isArray(candidate) ? candidate[0] : candidate;
    if (String(value || '').trim()) return String(value).trim();
  }
  const body = String(issue?.body || '');
  const proposedImplementation = body.match(
    /## Proposed Implementation\s*\n+\s*-\s*([^\n]+)/i,
  );
  if (proposedImplementation?.[1]) return proposedImplementation[1].trim();
  return 'Review the evidence and assign an owner before changing production.';
}

function growthNotificationTitle(activeCadences, issueCount) {
  if (activeCadences.some((cadence) => String(cadence?.key) === 'healthcheck')) {
    return issueCount > 0 ? 'Production findings' : 'Production health check';
  }
  if (activeCadences.some((cadence) => String(cadence?.key) === 'daily')) {
    return issueCount > 0 ? 'Daily product signals' : 'Daily product check';
  }
  if (isDeepAnalysisCadence(activeCadences)) return 'Growth review';
  return 'Growth Engineer summary';
}

function buildGrowthSocialNotification({
  issuesPayload,
  activeCadences,
  fingerprint,
  createdGitHubArtifact,
  charts = [],
  scope = '',
  timeZone = 'UTC',
}): SocialNotification {
  const issues = Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [];
  const issueCount = Number(issuesPayload?.issue_count || 0);
  const highestPriority = issues.some((issue) =>
    ['critical', 'urgent'].includes(String(issue?.priority || '').toLowerCase()),
  );
  const suppressedIssueCount = Number(issuesPayload?.suppressed_issue_count || 0);
  const summary = String(issuesPayload?.summary || '').trim();

  return {
    schema: 'analyticscli.social-notification',
    version: 1,
    kind: 'growth_findings',
    state: 'summary',
    severity:
      issueCount === 0 ? 'success' : highestPriority ? 'critical' : 'warning',
    title: growthNotificationTitle(activeCadences, issueCount),
    summary:
      summary ||
      (issueCount > 0
        ? `${issueCount} ${issueCount === 1 ? 'finding needs' : 'findings need'} review.`
        : 'No new actionable findings.'),
    impact:
      issueCount > 0
        ? 'Prioritized production, product, and growth risks may affect users or conversion.'
        : undefined,
    items: issues.slice(0, 8).map((issue) => ({
      id: String(issue?.signal_id || issue?.id || ''),
      label: humanizeNotificationIdentifier(issueProjectLabel(issue)),
      status: [
        humanizeNotificationIdentifier(issue?.priority || 'medium'),
        humanizeNotificationIdentifier(issue?.area || 'general'),
      ].join(' · '),
      summary: String(issue?.title || 'Untitled finding').trim(),
      action: issueNotificationAction(issue),
      url: issueSourceUrl(issue) || undefined,
      occurredAt: issueOccurredAt(issue) || undefined,
    })),
    nextStep:
      issueCount > 0
        ? createdGitHubArtifact
          ? 'Review the generated GitHub work item and assign an owner.'
          : 'Review the top finding and assign an owner before changing production.'
        : 'No action needed.',
    automation: createdGitHubArtifact
      ? 'GitHub work-item creation was requested; no production change was made automatically.'
      : issueCount > 0
        ? 'Alert only; no repository or production change was made.'
        : 'Monitoring continues automatically.',
    ...(charts.length > 0
      ? {
          evidence: {
            count: charts.length,
            chartCount: charts.length,
            files: charts.map((chart) => chart.filePath),
          },
        }
      : {}),
    ...(suppressedIssueCount > 0
      ? {
          nextRetryAt: undefined,
          summary: `${summary ? `${summary} ` : ''}${suppressedIssueCount} previously reported ${suppressedIssueCount === 1 ? 'finding was' : 'findings were'} omitted.`.trim(),
        }
      : {}),
    generatedAt: new Date().toISOString(),
    fingerprint: String(fingerprint || '') || undefined,
    scope: String(scope || '') || undefined,
    timeZone: String(timeZone || 'UTC'),
  };
}

function buildGrowthRunSummaryMessage({ issuesPayload, activeCadences, sourceFiles, createdGitHubArtifact, charts = [] }) {
  return renderSocialNotificationMarkdown(
    buildGrowthSocialNotification({
      issuesPayload,
      activeCadences,
      fingerprint: buildIssueFingerprint(issuesPayload),
      createdGitHubArtifact,
      charts,
    }),
  );
}

function growthRunTitle(activeCadences) {
  if (isShortOperationalCadence(activeCadences)) {
    return activeCadences.some((cadence) => String(cadence?.key) === 'healthcheck')
      ? 'OpenClaw healthcheck'
      : 'OpenClaw daily';
  }
  if (isDeepAnalysisCadence(activeCadences)) return 'OpenClaw growth review';
  return 'OpenClaw growth run';
}

function buildDiscordGrowthRunPayload(message, issuesPayload, activeCadences, sourceFiles, fingerprint, createdGitHubArtifact, charts = []) {
  const issues = Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [];
  const issueCount = Number(issuesPayload?.issue_count || 0);
  const fields = [
    discordField('Cadence', activeCadences.length > 0
      ? activeCadences.map((cadence) => cadence.title || cadence.key).join(', ')
      : 'ad-hoc growth pass',
      false),
    discordField('Sources', Object.keys(sourceFiles || {}).sort().join(', ') || 'none', true),
    discordField('Findings', String(issueCount), true),
  ];
  if (createdGitHubArtifact) {
    fields.push(discordField('Action', 'GitHub artifact creation was attempted.', true));
  }
  const suppressedIssueCount = Number(issuesPayload?.suppressed_issue_count || 0);
  if (suppressedIssueCount > 0) {
    fields.push(discordField('Omitted', `${suppressedIssueCount} previously reported finding(s).`, true));
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
    if (entry.value) fields.push(discordField(entry.name, entry.value));
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

function buildLegacyOpenClawGrowthMarkdown(issuesPayload) {
  const issues = Array.isArray(issuesPayload?.issues)
    ? issuesPayload.issues
    : [];
  const sections = [
    '# OpenClaw Proposal Outbox',
    '',
    `Generated: ${issuesPayload?.generated_at || issuesPayload?.generatedAt || new Date().toISOString()}`,
    `Repo: ${issuesPayload?.repo_root || issuesPayload?.repoRoot || ''}`,
    `Proposals: ${Number(issuesPayload?.issue_count || 0)}`,
    '',
    'This detailed handoff is kept for existing OpenClaw and doc-feeding integrations. The compact social notification is available in growth-summary.md and in the JSON notification field.',
  ];
  for (const [index, issue] of issues.entries()) {
    sections.push('', `## ${index + 1}. ${issue?.title || 'Untitled finding'}`);
    sections.push(`- Priority: ${issue?.priority || 'medium'}`);
    sections.push(`- Area: ${issue?.area || 'general'}`);
    if (issue?.source) sections.push(`- Source: ${issue.source}`);
    if (issue?.expected_impact) {
      sections.push(`- Expected impact: ${issue.expected_impact}`);
    }
    if (issue?.confidence) sections.push(`- Confidence: ${issue.confidence}`);
    if (Array.isArray(issue?.files) && issue.files.length > 0) {
      sections.push(
        `- Candidate files: ${issue.files.map((file) => `\`${file}\``).join(', ')}`,
      );
    }
    if (String(issue?.body || '').trim()) {
      sections.push('', String(issue.body).trim());
    }
  }
  return `${sections.join('\n')}\n`;
}

async function writeConfiguredOpenClawChatGrowthSummary(
  configPath,
  channel,
  message,
  issuesPayload,
  activeCadences,
  fingerprint,
  charts,
  notification,
) {
  const markdownPath = resolveOpenClawChatDeliveryPath(channel.markdownPath, '.openclaw/chat/growth-summary.md');
  const jsonPath = resolveOpenClawChatDeliveryPath(channel.jsonPath, '.openclaw/chat/growth-summary.json');
  const generatedAt =
    issuesPayload?.generated_at ||
    issuesPayload?.generatedAt ||
    new Date().toISOString();
  const outboxPayload = {
    channel: channel.label || 'openclaw_chat',
    generatedAt,
    fingerprint,
    repoRoot: issuesPayload?.repo_root || issuesPayload?.repoRoot || null,
    schemaVersion: 1,
    eventId: socialNotificationEventId(notification),
    notification: socialNotificationSummary(notification),
    activeCadences,
    issueCount: Number(issuesPayload?.issue_count || 0),
    issues: Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [],
    charts,
    attachments: charts.map((chart) => ({
      type: 'image/png',
      path: chart.filePath,
      caption: chart.caption,
    })),
  };
  await fs.mkdir(path.dirname(markdownPath), { recursive: true });
  await fs.mkdir(path.dirname(jsonPath), { recursive: true });
  await fs.writeFile(
    markdownPath,
    channel.legacyCompatible
      ? buildLegacyOpenClawGrowthMarkdown(issuesPayload)
      : message,
    'utf8',
  );
  await writeJsonAtomic(jsonPath, outboxPayload);

  const compactMarkdownPath = path.join(
    path.dirname(markdownPath),
    'growth-summary.md',
  );
  const compactJsonPath = path.join(path.dirname(jsonPath), 'growth-summary.json');
  if (
    channel.legacyCompatible &&
    (compactMarkdownPath !== markdownPath || compactJsonPath !== jsonPath)
  ) {
    await fs.mkdir(path.dirname(compactMarkdownPath), { recursive: true });
    await fs.mkdir(path.dirname(compactJsonPath), { recursive: true });
    await fs.writeFile(compactMarkdownPath, message, 'utf8');
    await writeJsonAtomic(compactJsonPath, outboxPayload);
  }
  return {
    sent: true,
    external: false,
    target: channel.label || 'openclaw_chat',
    detail: channel.legacyCompatible
      ? `wrote legacy OpenClaw handoff ${markdownPath} and compact social outbox ${compactMarkdownPath}`
      : `wrote local OpenClaw chat outbox ${markdownPath} and ${jsonPath}`,
  };
}

async function sendSlackGrowthSummary(channel, notification) {
  const webhookEnv = channel.webhookEnv || 'SLACK_WEBHOOK_URL';
  const webhookUrl = process.env[webhookEnv];
  if (!webhookUrl) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'slack',
      detail: `${webhookEnv} not set`,
      retryable: false,
    };
  }
  const payload = {
    ...buildSlackSocialPayload(notification),
    ...(channel.username ? { username: channel.username } : {}),
  };
  const result = await sendNotificationHttpRequest(webhookUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return {
    ...result,
    external: true,
    target: channel.label || 'slack',
  };
}

async function sendWebhookGrowthSummary(
  channel,
  message,
  issuesPayload,
  activeCadences,
  fingerprint,
  charts,
  notification,
) {
  const urlEnv = channel.urlEnv || channel.webhookEnv || 'OPENCLAW_WEBHOOK_URL';
  const webhookUrl = process.env[urlEnv];
  if (!webhookUrl) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'webhook',
      detail: `${urlEnv} not set`,
      retryable: false,
    };
  }
  const result = await sendNotificationHttpRequest(webhookUrl, {
    method: channel.method || 'POST',
    headers: {
      'content-type': 'application/json',
      ...(channel.headers || {}),
    },
    body: JSON.stringify({
      type: 'openclaw.growth_run',
      schemaVersion: 1,
      eventId: socialNotificationEventId(notification),
      generatedAt: new Date().toISOString(),
      text: message,
      fingerprint,
      notification: socialNotificationSummary(notification),
      activeCadences: sanitizeOutboundPayload(activeCadences),
      issueCount: Number(issuesPayload?.issue_count || 0),
      issues: sanitizeOutboundPayload(
        Array.isArray(issuesPayload?.issues) ? issuesPayload.issues : [],
      ),
      charts: sanitizeOutboundPayload(charts),
      attachments: sanitizeOutboundPayload(
        charts.map((chart) => ({
          type: 'image/png',
          fileName: path.basename(String(chart.filePath || 'chart.png')),
          caption: chart.caption,
          availableLocally: true,
        })),
      ),
    }),
  });
  return {
    ...result,
    external: true,
    target: channel.label || 'webhook',
  };
}

async function sendCommandGrowthSummary(channel, message) {
  if (!channel.command) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'command',
      detail: 'command not configured',
      retryable: false,
    };
  }
  const result = await runShellCommand(String(channel.command), 60_000, { input: message });
  return {
    sent: result.ok,
    external: true,
    target: channel.label || 'command',
    detail: result.ok
      ? 'sent'
      : safeDeliveryErrorDetail(
          result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
        ),
  };
}

async function sendDiscordGrowthSummary(channel, message, notification) {
  if (!channel.command) {
    return {
      sent: false,
      external: true,
      target: channel.label || 'discord',
      detail: 'discord command not configured',
      retryable: false,
    };
  }
  const payload = buildDiscordSocialPayload(notification);
  const result = await runShellCommand(String(channel.command), 60_000, {
    input: JSON.stringify(payload),
    env: discordDeliveryEnvironment(notification),
  });
  return {
    sent: result.ok,
    external: true,
    target: channel.label || 'discord',
    detail: result.ok
      ? 'sent'
      : safeDeliveryErrorDetail(
          result.stderr.trim() || result.stdout.trim() || `exit ${result.code}`,
        ),
  };
}

async function deliverGrowthRunSummary({
  config,
  configPath,
  issuesPayload,
  activeCadences,
  sourceFiles,
  fingerprint,
  createdGitHubArtifact,
  chartManifestPath,
  onlyChannelKeys = null,
}) {
  if (config?.notifications?.growthRun?.enabled === false) {
    return [{ sent: false, target: 'notifications', detail: 'growth run notifications disabled' }];
  }
  const allChannels = getGrowthRunChannels(config);
  const selectedChannelKeys = Array.isArray(onlyChannelKeys)
    ? new Set(onlyChannelKeys)
    : null;
  const channels = selectedChannelKeys
    ? allChannels.filter((channel) =>
        selectedChannelKeys.has(notificationChannelKey(channel)),
      )
    : allChannels;
  if (allChannels.length === 0) {
    return [{ sent: false, target: 'none', detail: 'no growth run notification channels configured' }];
  }
  if (channels.length === 0) return [];
  const charts = await readChartAttachments(chartManifestPath);
  const notification = buildGrowthSocialNotification({
    issuesPayload,
    activeCadences,
    fingerprint,
    createdGitHubArtifact,
    charts,
    scope: notificationScope(config, configPath),
    timeZone: resolveDailyIssueDedupeTimeZone(config),
  });
  const message = renderSocialNotificationMarkdown(notification);
  const results = [];
  for (const channel of channels) {
    const channelKey = notificationChannelKey(channel);
    try {
      let result;
      if (channel.type === 'openclaw-chat') {
        result = await writeConfiguredOpenClawChatGrowthSummary(
          configPath,
          channel,
          message,
          issuesPayload,
          activeCadences,
          fingerprint,
          charts,
          notification,
        );
      } else if (channel.type === 'slack') {
        result = await sendSlackGrowthSummary(channel, notification);
      } else if (channel.type === 'webhook') {
        result = await sendWebhookGrowthSummary(
          channel,
          message,
          issuesPayload,
          activeCadences,
          fingerprint,
          charts,
          notification,
        );
      } else if (channel.type === 'discord') {
        result = await sendDiscordGrowthSummary(channel, message, notification);
      } else if (channel.type === 'command') {
        result = await sendCommandGrowthSummary(channel, message);
      } else {
        result = {
          sent: false,
          target: channel.label || String(channel.type || 'unknown'),
          detail: 'unsupported channel type',
        };
      }
      results.push({
        ...result,
        channelKey,
        notification: socialNotificationSummary(notification),
      });
    } catch (error) {
      results.push({
        sent: false,
        external: channel.type !== 'openclaw-chat',
        target: channel.label || String(channel.type || 'unknown'),
        channelKey,
        detail: safeDeliveryErrorDetail(error),
        notification: socialNotificationSummary(notification),
      });
    }
  }
  return results;
}

async function retryPendingGrowthRunNotification({
  config,
  configPath,
  state,
  statePath,
}) {
  let previous = state?.growthRunNotification;
  if (!previous?.snapshot) {
    const legacyDeliveries = Array.isArray(state?.lastGrowthRunNotifications)
      ? state.lastGrowthRunNotifications
      : [];
    const legacyDeliveryFailed = legacyDeliveries.some(
      (delivery) =>
        delivery?.sent === false &&
        delivery?.external !== false &&
        !/suppressed|unchanged|disabled|no connector/i.test(
          String(delivery?.detail || ''),
        ),
    );
    const legacyFingerprint = String(
      state?.lastIssueFingerprint || '',
    ).trim();
    const legacyOutFile = String(state?.lastOutFile || '').trim();
    if (legacyDeliveryFailed && legacyFingerprint && legacyOutFile) {
      const issuesPayload = await readJsonOptional(legacyOutFile, null);
      if (issuesPayload && typeof issuesPayload === 'object') {
        previous = {
          version: 1,
          eventId: growthRunNotificationEventId(legacyFingerprint),
          fingerprint: legacyFingerprint,
          receipts: {},
          allChannelsSent: false,
          lastAttemptAt: null,
          completedAt: null,
          migratedFromLegacyDeliveryState: true,
          snapshot: {
            issuesPayload,
            activeCadences: [],
            sourceFiles: {},
            createdGitHubArtifact: false,
            chartManifestPath: null,
          },
        };
      }
    }
  }
  const snapshot = previous?.snapshot;
  if (!previous || previous.allChannelsSent === true || !snapshot) return state;

  const configuredChannelKeys = getGrowthRunChannelKeys(config);
  const pendingChannelKeys = pendingGrowthRunChannelKeys(
    previous,
    previous.fingerprint,
    configuredChannelKeys,
  );
  if (pendingChannelKeys.length === 0) {
    const completedAt = new Date().toISOString();
    const completedNotificationState = markGrowthRunNotificationState({
      previousState: previous,
      fingerprint: previous.fingerprint,
      deliveries: [],
      configuredChannelKeys,
      snapshot,
      attemptedAt: completedAt,
    });
    const nextState = {
      ...state,
      growthRunNotification: completedNotificationState,
    };
    await fs.mkdir(path.dirname(statePath), { recursive: true });
    await writeJsonAtomic(statePath, nextState);
    return nextState;
  }

  const attemptedAt = new Date().toISOString();
  const deliveries = await deliverGrowthRunSummary({
    config,
    configPath,
    issuesPayload: snapshot.issuesPayload,
    activeCadences: snapshot.activeCadences || [],
    sourceFiles: snapshot.sourceFiles || {},
    fingerprint: previous.fingerprint,
    createdGitHubArtifact: Boolean(snapshot.createdGitHubArtifact),
    chartManifestPath: snapshot.chartManifestPath || null,
    onlyChannelKeys: pendingChannelKeys,
  });
  const growthRunNotification = markGrowthRunNotificationState({
    previousState: previous,
    fingerprint: previous.fingerprint,
    deliveries,
    configuredChannelKeys,
    snapshot,
    attemptedAt,
  });
  const nextState = {
    ...state,
    growthRunNotification,
    lastGrowthRunNotifications: deliveries,
  };
  await fs.mkdir(path.dirname(statePath), { recursive: true });
  await writeJsonAtomic(statePath, nextState);
  await appendSchedulerProof('growth_notification_retry', {
    configPath,
    statePath,
    fingerprint: previous.fingerprint,
    attemptedAt,
    pendingChannelKeys,
    completed: growthRunNotification.allChannelsSent,
    deliveries: deliveries.map((delivery) => ({
      channelKey: delivery.channelKey || null,
      target: delivery.target,
      sent: delivery.sent === true,
      detail: delivery.detail || null,
    })),
  });
  return nextState;
}

async function maybeRunConnectorHealthCheck({ config, configPath, state, statePath, runtimeDir }) {
  const healthState = state?.connectorHealth || {};
  const incidents = getConnectorNotificationIncidents(state);
  const previousIncident = incidents[CONNECTOR_PROBE_INCIDENT_KEY];
  const intervalMinutes = getConnectorHealthIntervalMinutes(config);
  if (!isDue(healthState.lastCheckedAt, intervalMinutes)) {
    await appendSchedulerProof('connector_health_not_due', {
      configPath,
      statePath,
      intervalMinutes,
      lastCheckedAt: healthState.lastCheckedAt || null,
      persistedLastStatusOk: healthState.lastStatusOk !== false,
      incidentStatus: previousIncident.status,
      activeIncidentFingerprint: previousIncident.activeFingerprint,
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
  let statusPayload = parseJsonFromStdout(statusResult.stdout);
  let statusCheckError = null;
  if (!statusPayload) {
    statusCheckError = safeDeliveryErrorDetail(
      statusResult.stderr.trim() ||
        statusResult.stdout.trim() ||
        'connector status returned no JSON',
    );
    statusPayload = {
      generatedAt: checkedAt,
      configPath,
      connectors: {
        connector_status: {
          label: 'Connector status check',
          status: 'partial',
          detail:
            'The scheduled connector status check failed; connector coverage could not be verified.',
          nextAction:
            'Review the sanitized runner diagnostics on the host. The next scheduled check will retry automatically.',
        },
      },
    };
    await appendSchedulerProof('connector_health_check_failed', {
      configPath,
      statePath,
      intervalMinutes,
      checkedAt,
      error: statusCheckError,
      notificationEnabled:
        config?.notifications?.connectorHealth?.enabled !== false,
    });
  }

  const unhealthyConnectors = getUnhealthyConfiguredConnectors(statusPayload);
  const connectedConnectors = getConnectedConnectorKeys(statusPayload);
  const fingerprint =
    unhealthyConnectors.length > 0
      ? buildConnectorHealthFingerprint(unhealthyConnectors)
      : null;
  let nextIncident = transitionConnectorNotificationIncident(
    previousIncident,
    'connector_probe',
    fingerprint,
    checkedAt,
  );
  const configuredChannelKeys = getConnectorHealthChannelKeys(config);
  const pendingChannelKeys = pendingConnectorIncidentChannelKeys(
    previousIncident,
    nextIncident,
    configuredChannelKeys,
  );
  const shouldNotify =
    config?.notifications?.connectorHealth?.enabled !== false &&
    shouldNotifyConnectorIncident(
      previousIncident,
      nextIncident,
      configuredChannelKeys,
    );
  let notificationTriggered = false;
  let notificationDeliveries: any[] = [];
  let alertPaths: { markdownPath: string; jsonPath: string } | null = null;

  if (shouldNotify) {
    const notificationFingerprint =
      nextIncident.activeFingerprint || nextIncident.recoveredFingerprint;
    const socialNotification = buildConnectorSocialNotification(
      statusPayload,
      unhealthyConnectors,
      notificationFingerprint,
      {
        kind: 'connector_probe',
        status: nextIncident.status,
      },
    );
    const message = renderSocialNotificationMarkdown(socialNotification);
    alertPaths = await writeConnectorHealthAlert(
      runtimeDir,
      message,
      statusPayload,
      unhealthyConnectors,
      notificationFingerprint,
      {
        kind: 'connector_probe',
        status: nextIncident.status,
      },
      socialNotification,
    );
    notificationDeliveries = await deliverConnectorHealthAlert({
      config,
      configPath,
      message,
      statusPayload,
      unhealthyConnectors,
      fingerprint: notificationFingerprint,
      incident: {
        kind: 'connector_probe',
        status: nextIncident.status,
      },
      notification: socialNotification,
      onlyChannelKeys: pendingChannelKeys,
    });
    notificationTriggered = true;
    nextIncident = {
      ...markConnectorIncidentNotification(
        nextIncident,
        notificationDeliveries,
        checkedAt,
        configuredChannelKeys,
      ),
      lastAlertMarkdownPath: alertPaths.markdownPath,
      lastAlertJsonPath: alertPaths.jsonPath,
    };
  }

  const nextHealthState: Record<string, any> = {
    ...healthState,
    incidents: {
      ...incidents,
      version: CONNECTOR_NOTIFICATION_STATE_VERSION,
      [CONNECTOR_PROBE_INCIDENT_KEY]: nextIncident,
    },
    lastCheckedAt: checkedAt,
    lastStatusOk: unhealthyConnectors.length === 0,
    lastFingerprint: fingerprint,
    activeIncidentFingerprint: nextIncident.activeFingerprint,
    connectedConnectors,
    lastError: statusCheckError,
  };

  if (nextIncident.status === 'recovered') {
    nextHealthState.lastExternalAlertedFingerprint = null;
    if (previousIncident.activeFingerprint) {
      nextHealthState.lastRecoveredAt = checkedAt;
    }
  }

  if (notificationTriggered) {
    nextHealthState.lastAlertedAt = checkedAt;
    nextHealthState.lastAlertedFingerprint =
      nextIncident.activeFingerprint || nextIncident.recoveredFingerprint;
    nextHealthState.lastAlertMarkdownPath = alertPaths?.markdownPath || null;
    nextHealthState.lastAlertJsonPath = alertPaths?.jsonPath || null;
    nextHealthState.lastAlertDeliveries = notificationDeliveries;
    nextHealthState.lastAlertExternalSent =
      hasSuccessfulExternalDelivery(notificationDeliveries);
    if (nextHealthState.lastAlertExternalSent) {
      nextHealthState.lastExternalAlertedAt = checkedAt;
      nextHealthState.lastExternalAlertedFingerprint =
        nextIncident.status === 'recovered'
          ? null
          : nextIncident.lastExternalAlertedFingerprint;
    }
  }

  const nextState = {
    ...state,
    connectorHealth: nextHealthState,
  };
  await fs.mkdir(path.dirname(statePath), { recursive: true });
  await writeJsonAtomic(statePath, nextState);
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
    incidentStatus: nextIncident.status,
    alertMarkdownPath: nextHealthState.lastAlertMarkdownPath || null,
    notificationTriggered,
    alertTriggered: notificationTriggered,
    deliveryCount: notificationDeliveries.length,
    externalDeliverySent: notificationTriggered
      ? hasSuccessfulExternalDelivery(notificationDeliveries)
      : false,
    socialOutput: notificationTriggered
      ? nextIncident.status === 'recovered'
        ? 'CONNECTOR_HEALTH_RECOVERED'
        : 'CONNECTOR_HEALTH_ALERT'
      : 'HEARTBEAT_OK',
    socialReason: notificationTriggered
      ? nextIncident.status === 'recovered'
        ? 'connector-health incident recovered'
        : nextIncident.status === 'ongoing'
          ? 'retrying unchanged connector-health incident after failed external delivery'
          : 'new or changed connector-health incident'
      : unhealthyConnectors.length > 0
        ? 'connector-health incident ongoing and unchanged'
        : 'connector health remains healthy',
  });
  if (unhealthyConnectors.length > 0 && !notificationTriggered) {
    await appendSchedulerProof('connector_health_unchanged', {
      configPath,
      statePath,
      checkedAt,
      fingerprint,
      incidentStatus: nextIncident.status,
      socialOutput: 'HEARTBEAT_OK',
    });
  }
  return nextState;
}

function buildIssueFingerprint(issuesPayload) {
  const issues = Array.isArray(issuesPayload?.issues)
    ? issuesPayload.issues
        .map((issue) =>
          [
            issue?.signal_id || issue?.signalId || issue?.id || '',
            issueProjectLabel(issue),
            issue?.source || '',
            issue?.title || '',
            issue?.priority || '',
            issue?.area || '',
            issue?.expected_impact || issue?.expectedImpact || '',
            issueSourceUrl(issue) || '',
          ]
            .map((value) => String(value || '').replace(/\s+/g, ' ').trim())
            .join('|'),
        )
        .sort()
    : [];
  return sha256(issues.join('\n'));
}

function isShortOperationalCadence(cadences) {
  if (!Array.isArray(cadences) || cadences.length === 0) return false;
  return cadences.every((cadence) => {
    const key = String(cadence?.key || '').toLowerCase();
    return key === 'healthcheck' || key === 'daily' || cadence?.criticalOnly === true;
  });
}

function isDeepAnalysisCadence(cadences) {
  if (!Array.isArray(cadences)) return false;
  return cadences.some((cadence) =>
    ['weekly', 'monthly', 'quarterly', 'six_months', 'yearly'].includes(String(cadence?.key || '').toLowerCase()),
  );
}

function firstEvidenceLines(issue, maxLines = 2) {
  const body = String(issue?.body || '');
  const evidenceMatch = body.match(/## Evidence\n([\s\S]*?)(?:\n## |\n?$)/);
  if (!evidenceMatch) return [];
  return evidenceMatch[1]
    .split('\n')
    .map((line) => line.replace(/^-\s*/, '').trim())
    .filter(Boolean)
    .slice(0, maxLines);
}

async function runAnalyzer({
  config,
  runtimeDir,
  sourceFiles,
  createGitHubArtifact,
  githubArtifactMode = getActionMode(config),
  chartManifestPath,
  cadencePlanPath,
}) {
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
    args.push(
      githubArtifactMode === 'pull_request' ? '--create-pull-requests' : '--create-issues',
      '--repo',
      repo,
    );
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
    process.stderr.write(
      `[${new Date().toISOString()}] Chart generation failed: ${result.stderr || `exit ${result.code}`}\n`,
    );
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
    const resolvedCommand = resolveCursorAwareCommand(
      withActiveConfigArg(replaceLegacyRuntimeScriptCommand(sourceConfig.command), configPath),
      sourceConfig,
      cursorState,
    );
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
      throw new Error(
        buildSourceCommandFailureMessage(sourceName, resolvedCommand, detail),
      );
    }
    const fetchedAt = new Date().toISOString();
    try {
      return {
        payload: JSON.parse(result.stdout),
        nextCursor:
          sourceConfig.cursorMode === 'auto_since_last_fetch'
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
    } catch {
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
  const sourceFailures: any[] = [];
  const commandCwd = getProjectCommandCwd(config);
  for (const source of getAllSourceEntries(config)) {
    const currentCursor = sourceCursors[source.key] || null;
    let result;
    try {
      result = await resolveSourcePayloadWithCursor(source, source.key, currentCursor, commandCwd, configPath);
    } catch (error) {
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
  const sourceFiles: Record<string, string> = {};
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
  const stateAfterGrowthNotificationRetry =
    await retryPendingGrowthRunNotification({
      config,
      configPath,
      state,
      statePath,
    });
  const runtimeDir = path.resolve(deriveRuntimeDirFromStatePath(statePath));
  const stateAfterHealthCheck = await maybeRunConnectorHealthCheck({
    config,
    configPath,
    state: stateAfterGrowthNotificationRetry,
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
    await writeJsonAtomic(statePath, {
      ...stateAfterHealthCheck,
      ...stateAfterSourceCollection,
      sourceHashes: currentHashes,
      sourceCursors,
      lastSourceFailures: sourceFailures,
      lastRunAt: completedAt,
      skippedReason: 'cadence_not_due',
    });
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

  const githubArtifactModes = getGitHubArtifactModes(config).filter((mode) =>
    shouldAutoCreateGitHubArtifact(config, mode),
  );
  const createGitHubArtifact =
    githubArtifactModes.length > 0 && Boolean(String(config.project?.githubRepo || '').trim());
  const sourceFiles = await materializeSourceFiles(config, payloads, runtimeDir);
  const cadencePlanPath = path.join(runtimeDir, 'cadence-plan.json');
  await fs.writeFile(
    cadencePlanPath,
    JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        cadences: activeCadences,
      },
      null,
      2,
    ),
    'utf8',
  );
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

  const dailyIssueDedupe = applyDailyIssueDedupe(
    dryRun.issuesPayload,
    stateAfterSourceCollection,
    config,
    activeCadences,
  );
  const deliverableIssuesPayload = dailyIssueDedupe.issuesPayload;
  const issueFingerprint = buildIssueFingerprint(deliverableIssuesPayload);
  const unchangedIssueSet =
    issueFingerprint === stateAfterSourceCollection.lastIssueFingerprint &&
    !dailyIssueDedupe.hasDrasticEventGrowth;

  if (
    Number(dryRun.issuesPayload?.issue_count || 0) > 0 &&
    Number(deliverableIssuesPayload?.issue_count || 0) === 0 &&
    dailyIssueDedupe.suppressedCount > 0
  ) {
    process.stdout.write(`[${new Date().toISOString()}] All findings were already reported today. Skip GitHub creation and external growth notification.\n`);
    const completedAt = new Date().toISOString();
    await writeJsonAtomic(statePath, {
      ...stateAfterHealthCheck,
      ...stateAfterSourceCollection,
      sourceHashes: currentHashes,
      sourceCursors,
      lastSourceFailures: sourceFailures,
      dailyIssueReports: dailyIssueDedupe.dailyIssueReports,
      lastIssueFingerprint: issueFingerprint,
      lastRunAt: completedAt,
      lastOutFile: dryRun.outFile,
      cadences: markCadencesRan(
        stateAfterSourceCollection,
        activeCadences,
        completedAt,
      ),
      lastGrowthRunNotifications: [
        {
          sent: false,
          target: 'growth_run',
          detail: `all ${dailyIssueDedupe.suppressedCount} finding(s) already reported today; external growth notification suppressed`,
        },
      ],
      skippedReason: 'daily_issue_dedupe',
    });
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

  if (
    unchangedIssueSet &&
    config.schedule?.skipIfIssueSetUnchanged !== false
  ) {
    process.stdout.write(`[${new Date().toISOString()}] Issue set unchanged. Skip GitHub creation and external growth notification.\n`);
    const completedAt = new Date().toISOString();
    await writeJsonAtomic(statePath, {
      ...stateAfterHealthCheck,
      ...stateAfterSourceCollection,
      sourceHashes: currentHashes,
      sourceCursors,
      lastSourceFailures: sourceFailures,
      dailyIssueReports: dailyIssueDedupe.dailyIssueReports,
      lastIssueFingerprint: issueFingerprint,
      lastRunAt: completedAt,
      lastOutFile: dryRun.outFile,
      cadences: markCadencesRan(
        stateAfterSourceCollection,
        activeCadences,
        completedAt,
      ),
      lastGrowthRunNotifications: [
        {
          sent: false,
          target: 'growth_run',
          detail: 'issue set unchanged; external growth notification suppressed',
        },
      ],
      skippedReason: 'issue_set_unchanged',
    });
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

  const issueSetChangedOrExplicitlyAllowed =
    !unchangedIssueSet || config.schedule?.skipIfIssueSetUnchanged === false;
  const shouldCreateGitHubArtifact =
    createGitHubArtifact &&
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
    process.stdout.write(
      `[${new Date().toISOString()}] Created GitHub ${githubArtifactModes.map((mode) => (mode === 'pull_request' ? 'pull requests' : 'issues')).join(' and ')}.\n`,
    );
  } else {
    process.stdout.write(
      `[${new Date().toISOString()}] Drafts generated only (${getActionMode(config)} auto-create disabled).\n`,
    );
  }

  const completedAt = new Date().toISOString();
  const growthRunNotificationSnapshot = {
    issuesPayload: deliverableIssuesPayload,
    activeCadences,
    sourceFiles,
    createdGitHubArtifact: shouldCreateGitHubArtifact,
    chartManifestPath,
  };
  const growthNotificationsEnabled =
    config?.notifications?.growthRun?.enabled !== false;
  const suppressCleanOperationalNotification =
    Number(deliverableIssuesPayload?.issue_count || 0) === 0 &&
    isShortOperationalCadence(activeCadences);
  const shouldDeliverGrowthRunNotification =
    growthNotificationsEnabled && !suppressCleanOperationalNotification;
  const growthRunNotificationDeliveries =
    shouldDeliverGrowthRunNotification
      ? await deliverGrowthRunSummary({
          config,
          configPath,
          issuesPayload: deliverableIssuesPayload,
          activeCadences,
          sourceFiles,
          fingerprint: issueFingerprint,
          createdGitHubArtifact: shouldCreateGitHubArtifact,
          chartManifestPath,
        })
      : [
          {
            sent: false,
            external: false,
            target: 'growth_run',
            detail: growthNotificationsEnabled
              ? 'clean operational run; social notification suppressed'
              : 'growth run notifications disabled',
            retryable: false,
          },
        ];
  const growthRunNotification = markGrowthRunNotificationState({
    previousState: stateAfterSourceCollection.growthRunNotification,
    fingerprint: issueFingerprint,
    deliveries: growthRunNotificationDeliveries,
    configuredChannelKeys: shouldDeliverGrowthRunNotification
      ? getGrowthRunChannelKeys(config)
      : [],
    snapshot: growthRunNotificationSnapshot,
    attemptedAt: completedAt,
  });
  const externalDeliverySent = hasSuccessfulExternalDelivery(
    growthRunNotificationDeliveries,
  );
  const localDeliveryWritten = growthRunNotificationDeliveries.some(
    (delivery) => delivery?.sent === true && delivery?.external !== true,
  );
  const anyDeliverySent = growthRunNotificationDeliveries.some(
    (delivery) => delivery?.sent === true,
  );
  const structuredNotification =
    growthRunNotificationDeliveries.find((delivery) => delivery?.notification)
      ?.notification || null;
  await writeJsonAtomic(statePath, {
    ...stateAfterHealthCheck,
    ...stateAfterSourceCollection,
    sourceHashes: currentHashes,
    sourceCursors,
    lastSourceFailures: sourceFailures,
    dailyIssueReports: dailyIssueDedupe.dailyIssueReports,
    lastIssueFingerprint: issueFingerprint,
    lastRunAt: completedAt,
    lastOutFile: dryRun.outFile,
    cadences: markCadencesRan(
      stateAfterSourceCollection,
      activeCadences,
      completedAt,
    ),
    lastGrowthRunNotifications: growthRunNotificationDeliveries,
    growthRunNotification,
    skippedReason: null,
  });
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
    notificationEnabled: growthNotificationsEnabled,
    notificationSuppressed: !shouldDeliverGrowthRunNotification,
    externalDeliverySent,
    localDeliveryWritten,
    deliveryFailed:
      shouldDeliverGrowthRunNotification && !anyDeliverySent,
    notification: structuredNotification,
    socialOutput: !shouldDeliverGrowthRunNotification
      ? 'HEARTBEAT_OK'
      : externalDeliverySent
        ? 'EXTERNAL_NOTIFICATION_SENT'
        : localDeliveryWritten
          ? 'GROWTH_RUN_ALERT'
          : 'NOTIFICATION_DELIVERY_FAILED',
    socialReason: !growthNotificationsEnabled
      ? 'growth notifications disabled'
      : suppressCleanOperationalNotification
        ? 'clean operational run'
        : externalDeliverySent
          ? 'notification already delivered by the runner'
          : localDeliveryWritten
            ? 'structured notification is available for native-agent delivery'
            : 'configured notification delivery did not succeed',
  });
}

function isProcessAlive(pid) {
  const numericPid = Number(pid);
  if (!Number.isInteger(numericPid) || numericPid <= 0) return false;
  try {
    process.kill(numericPid, 0);
    return true;
  } catch (error) {
    return error?.code === 'EPERM';
  }
}

async function acquireRunnerLock(statePath) {
  const lockPath = `${statePath}.runner.lock`;
  await fs.mkdir(path.dirname(lockPath), { recursive: true });

  for (let attempt = 0; attempt < 2; attempt += 1) {
    const token = `${process.pid}:${Date.now()}:${attempt}`;
    try {
      const handle = await fs.open(lockPath, 'wx');
      await handle.writeFile(
        `${JSON.stringify({
          version: 1,
          pid: process.pid,
          token,
          acquiredAt: new Date().toISOString(),
          statePath,
        })}\n`,
        'utf8',
      );
      return {
        lockPath,
        async release() {
          await handle.close().catch(() => {});
          const current = await readJsonOptional(lockPath, null);
          if (current?.token === token) {
            await fs.unlink(lockPath).catch(() => {});
          }
        },
      };
    } catch (error) {
      if (error?.code !== 'EEXIST') throw error;
      const existing = await readJsonOptional(lockPath, null);
      if (isProcessAlive(existing?.pid)) return null;

      let stale = Boolean(existing?.pid);
      if (!stale) {
        const stats = await fs.stat(lockPath).catch(() => null);
        stale = Boolean(
          stats && Date.now() - stats.mtimeMs > 2 * 60 * 60 * 1000,
        );
      }
      if (!stale) return null;
      await fs.unlink(lockPath).catch(() => {});
    }
  }
  return null;
}

async function runOnceWithLock(configPath, statePath) {
  const lock = await acquireRunnerLock(statePath);
  if (!lock) {
    process.stdout.write(
      `[${new Date().toISOString()}] Another Growth Engineer run owns this state; duplicate run skipped.\n`,
    );
    await appendSchedulerProof('runner_skipped_lock_held', {
      configPath,
      statePath,
    });
    return false;
  }
  try {
    await runOnce(configPath, statePath);
    return true;
  } finally {
    await lock.release();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.validateNotificationState) {
    process.stdout.write(`${JSON.stringify(validateConnectorNotificationStateModel(), null, 2)}\n`);
    return;
  }

  await loadOpenClawGrowthSecrets();
  await maybeSelfUpdateFromClawHub(args);
  const configPath = path.resolve(args.config);
  const statePath = path.resolve(args.state);
  useSchedulerProofPathForStatePath(statePath);

  if (!args.loop) {
    await runOnceWithLock(configPath, statePath);
    return;
  }

  const config = await readJson(configPath);
  const intervalMinutes = Math.max(1, Number(config.schedule?.intervalMinutes || 1440));
  process.stdout.write(`Starting loop. Interval: ${intervalMinutes} minute(s)\n`);
  while (true) {
    try {
      await maybeSelfUpdateFromClawHub(args);
      await runOnceWithLock(configPath, statePath);
    } catch (error) {
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
        }).catch(() => {});
        return null;
      });
      process.stderr.write(
        `[${new Date().toISOString()}] Run failed${failureDecision?.suppressed ? ' (already reported today)' : ''}: ${error instanceof Error ? error.message : String(error)}\n`,
      );
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
    }).catch(() => {});
    return null;
  });
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = failureDecision?.exitCode ?? 1;
});
