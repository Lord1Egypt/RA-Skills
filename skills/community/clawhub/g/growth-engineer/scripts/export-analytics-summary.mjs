#!/usr/bin/env node
import { spawn } from 'node:child_process';
import process from 'node:process';
import { buildAnalyticsSummary, writeJsonOutput } from './openclaw-exporters-lib.mjs';
import { loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';
function printHelpAndExit(exitCode, reason = null) {
    if (reason) {
        process.stderr.write(`${reason}\n\n`);
    }
    process.stdout.write(`
Export Analytics Summary

Builds an OpenClaw-compatible analytics_summary JSON by querying analyticscli.

Usage:
  node scripts/export-analytics-summary.mjs [options]

Options:
  --project <id>       Optional AnalyticsCLI project ID pin (default: all visible projects)
  --last <duration>    Relative time window like 30d (default: 30d)
  --out <file>         Write JSON to file instead of stdout
  --include-debug      Include development/debug data
  --max-signals <n>    Maximum signals to emit (default: 4)
  --help, -h           Show help
`);
    process.exit(exitCode);
}
function parseArgs(argv) {
    const args = {
        project: '',
        last: '30d',
        out: '',
        includeDebug: false,
        maxSignals: 4,
    };
    for (let index = 0; index < argv.length; index += 1) {
        const token = argv[index];
        const next = argv[index + 1];
        if (token === '--') {
            continue;
        }
        else if (token === '--project') {
            args.project = String(next || '').trim();
            index += 1;
        }
        else if (token === '--last') {
            args.last = String(next || '30d').trim() || '30d';
            index += 1;
        }
        else if (token === '--out') {
            args.out = String(next || '').trim();
            index += 1;
        }
        else if (token === '--include-debug') {
            args.includeDebug = true;
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
    return args;
}
function runJsonCommand(command, commandArgs) {
    const token = String(process.env.ANALYTICSCLI_ACCESS_TOKEN || process.env.ANALYTICSCLI_READONLY_TOKEN || '').trim();
    return new Promise((resolve, reject) => {
        const child = spawn(command, commandArgs, {
            stdio: ['ignore', 'pipe', 'pipe'],
            env: token ? { ...process.env, ANALYTICSCLI_ACCESS_TOKEN: token } : process.env,
        });
        let stdout = '';
        let stderr = '';
        child.stdout.on('data', (chunk) => {
            stdout += String(chunk);
        });
        child.stderr.on('data', (chunk) => {
            stderr += String(chunk);
        });
        child.on('error', reject);
        child.on('close', (code) => {
            if (code !== 0) {
                reject(Object.assign(new Error(stderr.trim() || `${command} exited with code ${code}`), { exitCode: code }));
                return;
            }
            try {
                resolve(JSON.parse(stdout));
            }
            catch {
                reject(new Error(`${command} returned non-JSON output`));
            }
        });
    });
}
function buildBaseArgs(input) {
    const args = [];
    args.push('--format', 'json');
    if (input.project) {
        args.push('--project', input.project);
    }
    if (input.includeDebug) {
        args.push('--include-debug');
    }
    return args;
}
function extractProjectChoices(payload) {
    const candidates = (() => {
        if (Array.isArray(payload))
            return payload;
        if (payload && typeof payload === 'object') {
            if (Array.isArray(payload.projects))
                return payload.projects;
            if (Array.isArray(payload.items))
                return payload.items;
            if (Array.isArray(payload.data))
                return payload.data;
        }
        return [];
    })();
    const byId = new Map();
    for (const candidate of candidates) {
        if (!candidate || typeof candidate !== 'object')
            continue;
        const id = String(candidate.id || candidate.projectId || candidate.project_id || '').trim();
        if (!id)
            continue;
        const name = String(candidate.name || candidate.displayName || '').trim();
        const slug = String(candidate.slug || '').trim();
        byId.set(id, {
            id,
            label: name || slug || id,
        });
    }
    return [...byId.values()].sort((a, b) => String(a.label).localeCompare(String(b.label)));
}
async function listAnalyticsProjects() {
    const payload = await runJsonCommand('analyticscli', ['projects', 'list', '--format', 'json']);
    return extractProjectChoices(payload);
}
async function runOptionalAnalyticsQuery(label, args, options = {}) {
    try {
        return {
            payload: await runJsonCommand('analyticscli', args),
            warning: null,
        };
    }
    catch (error) {
        const exitCode = error && typeof error === 'object' && 'exitCode' in error ? error.exitCode : null;
        if (options.softFail || exitCode === 2) {
            return {
                payload: null,
                warning: `${label}: ${error instanceof Error ? error.message : String(error)}`,
            };
        }
        throw new Error(`${label} failed: ${error instanceof Error ? error.message : String(error)}`);
    }
}
async function buildProjectSummary(project, args) {
    const baseArgs = buildBaseArgs({ ...args, project: project.id });
    const onboardingJourney = await runOptionalAnalyticsQuery(`${project.label} onboarding journey query`, [
        ...baseArgs,
        'get',
        'onboarding-journey',
        '--within',
        'user',
        '--last',
        args.last,
        '--with-trends',
    ], { softFail: true });
    const retention = await runOptionalAnalyticsQuery(`${project.label} retention query`, [
        ...baseArgs,
        'retention',
        '--anchor-event',
        'onboarding:start',
        '--days',
        '1,3,7',
        '--max-age-days',
        '90',
        '--last',
        args.last,
    ], { softFail: true });
    const summary = buildAnalyticsSummary({
        projectId: project.id,
        project: project.label,
        last: args.last,
        onboardingJourney: onboardingJourney.payload,
        retention: retention.payload,
        maxSignals: args.maxSignals,
    });
    const queryWarnings = [onboardingJourney.warning, retention.warning].filter(Boolean);
    if (queryWarnings.length > 0) {
        summary.meta.queryWarnings = queryWarnings;
    }
    summary.meta.projectId = project.id;
    summary.meta.projectLabel = project.label;
    return summary;
}
function priorityRank(priority) {
    if (priority === 'high')
        return 3;
    if (priority === 'medium')
        return 2;
    return 1;
}
function coerceNumber(value) {
    const numeric = typeof value === 'number' ? value : Number(value);
    return Number.isFinite(numeric) ? numeric : 0;
}
function combineProjectSummaries(projects, summaries, input) {
    const signals = summaries.flatMap((summary) => (Array.isArray(summary.signals) ? summary.signals : []).map((signal) => ({
        ...signal,
        id: `${summary.meta?.projectId || summary.project}:${signal.id}`,
        project: summary.project,
        evidence: [`Project: ${summary.project}`, ...(Array.isArray(signal.evidence) ? signal.evidence : [])],
    })));
    signals.sort((a, b) => {
        const priorityDelta = priorityRank(String(b.priority || 'low')) - priorityRank(String(a.priority || 'low'));
        if (priorityDelta !== 0)
            return priorityDelta;
        return Math.abs(coerceNumber(b.delta_percent ?? b.deltaPercent)) - Math.abs(coerceNumber(a.delta_percent ?? a.deltaPercent));
    });
    return {
        project: 'all_accessible_projects',
        window: summaries[0]?.window || `last_${input.last}`,
        signals: signals.slice(0, Math.max(1, Number(input.maxSignals) || 4)),
        meta: {
            generatedAt: new Date().toISOString(),
            source: 'analyticscli',
            projectScope: 'all_accessible_projects',
            projectsScanned: projects.length,
            projects: summaries.map((summary) => ({
                id: summary.meta?.projectId || null,
                label: summary.meta?.projectLabel || summary.project,
                signalCount: Array.isArray(summary.signals) ? summary.signals.length : 0,
                queryWarnings: summary.meta?.queryWarnings || [],
            })),
        },
    };
}
async function main() {
    await loadOpenClawGrowthSecrets();
    const args = parseArgs(process.argv.slice(2));
    if (!args.project) {
        const projects = await listAnalyticsProjects();
        if (projects.length > 0) {
            const summaries = [];
            for (const project of projects) {
                summaries.push(await buildProjectSummary(project, args));
            }
            await writeJsonOutput(args.out, combineProjectSummaries(projects, summaries, args));
            return;
        }
    }
    const baseArgs = buildBaseArgs(args);
    const onboardingJourney = await runOptionalAnalyticsQuery('onboarding journey query', [
        ...baseArgs,
        'get',
        'onboarding-journey',
        '--within',
        'user',
        '--last',
        args.last,
        '--with-trends',
    ]);
    const retention = await runOptionalAnalyticsQuery('retention query', [
        ...baseArgs,
        'retention',
        '--anchor-event',
        'onboarding:start',
        '--days',
        '1,3,7',
        '--max-age-days',
        '90',
        '--last',
        args.last,
    ]);
    const summary = buildAnalyticsSummary({
        projectId: args.project,
        last: args.last,
        onboardingJourney: onboardingJourney.payload,
        retention: retention.payload,
        maxSignals: args.maxSignals,
    });
    const queryWarnings = [onboardingJourney.warning, retention.warning].filter(Boolean);
    if (queryWarnings.length > 0) {
        summary.meta.queryWarnings = queryWarnings;
    }
    await writeJsonOutput(args.out, summary);
}
main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
});
