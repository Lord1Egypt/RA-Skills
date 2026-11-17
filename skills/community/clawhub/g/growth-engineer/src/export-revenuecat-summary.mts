#!/usr/bin/env node

import process from 'node:process';
import { buildRevenueCatSummary, writeJsonOutput } from './openclaw-exporters-lib.mjs';
import { loadOpenClawGrowthSecrets } from './openclaw-growth-env.mjs';

const API_BASE = 'https://api.revenuecat.com/v2';

function printHelpAndExit(exitCode, reason = null) {
  if (reason) {
    process.stderr.write(`${reason}\n\n`);
  }
  process.stdout.write(`
Export RevenueCat Summary

Builds an OpenClaw-compatible RevenueCat summary JSON from the RevenueCat API v2.

Usage:
  node scripts/export-revenuecat-summary.mjs [options]

Options:
  --project <id>       RevenueCat project ID (default: summarize all visible projects)
  --currency <code>    Currency for overview metrics (default: USD)
  --from <date>        Start date YYYY-MM-DD for revenue/charts (default: 30 days before --to)
  --to <date>          End date YYYY-MM-DD for revenue/charts (default: yesterday UTC)
  --last <duration>    Relative revenue/chart window like 30d (used when --from is omitted)
  --charts <a,b>       RevenueCat charts to fetch (default: revenue,mrr,actives,trials,trials_new,trial_conversion_rate,churn,refund_rate)
  --limit <n>          Maximum list entries to fetch per endpoint (default: 20)
  --max-projects <n>   Maximum visible projects to summarize when --project is omitted (default: 10)
  --out <file>         Write JSON to file instead of stdout
  --max-signals <n>    Maximum signals to emit (default: 4)
  --help, -h           Show help
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const defaultTo = formatDate(addDays(new Date(), -1));
  const args = {
    project: '',
    currency: 'USD',
    from: '',
    to: defaultTo,
    last: '30d',
    charts: ['revenue', 'mrr', 'actives', 'trials', 'trials_new', 'trial_conversion_rate', 'churn', 'refund_rate'],
    limit: 20,
    maxProjects: 10,
    out: '',
    maxSignals: 8,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    const next = argv[index + 1];

    if (token === '--') {
      continue;
    } else if (token === '--project') {
      args.project = String(next || '').trim();
      index += 1;
    } else if (token === '--currency') {
      args.currency = String(next || 'USD').trim().toUpperCase() || 'USD';
      index += 1;
    } else if (token === '--from') {
      args.from = String(next || '').trim();
      index += 1;
    } else if (token === '--to') {
      args.to = String(next || '').trim();
      index += 1;
    } else if (token === '--last') {
      args.last = String(next || args.last).trim() || args.last;
      index += 1;
    } else if (token === '--charts') {
      args.charts = String(next || '')
        .split(',')
        .map((value) => value.trim())
        .filter(Boolean);
      index += 1;
    } else if (token === '--limit') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for --limit: ${String(next || '')}`);
      }
      args.limit = parsed;
      index += 1;
    } else if (token === '--max-projects') {
      const parsed = Number.parseInt(String(next || ''), 10);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        printHelpAndExit(1, `Invalid value for --max-projects: ${String(next || '')}`);
      }
      args.maxProjects = parsed;
      index += 1;
    } else if (token === '--out') {
      args.out = String(next || '').trim();
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

  if (!args.from) {
    args.from = formatDate(addDays(new Date(`${args.to}T00:00:00Z`), -parseDurationDays(args.last, 30)));
  }
  return args;
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
  if (!match) return fallback;
  const parsed = Number.parseInt(match[1], 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function previousWindow(from, to) {
  const start = new Date(`${from}T00:00:00Z`);
  const end = new Date(`${to}T00:00:00Z`);
  const days = Math.max(1, Math.round((end.getTime() - start.getTime()) / 86_400_000) + 1);
  const previousEnd = addDays(start, -1);
  const previousStart = addDays(previousEnd, -days + 1);
  return { from: formatDate(previousStart), to: formatDate(previousEnd) };
}

function buildUrl(pathname, params = {}) {
  const url = new URL(`${API_BASE}${pathname}`);
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === '') continue;
    url.searchParams.set(key, String(value));
  }
  return url.toString();
}

async function fetchRevenueCatJson(pathname, params = {}) {
  const token = String(process.env.REVENUECAT_API_KEY || '').trim();
  if (!token) {
    throw new Error('Missing REVENUECAT_API_KEY. Rerun the connector wizard and paste a RevenueCat API v2 secret key.');
  }

  const response = await fetch(buildUrl(pathname, params), {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      Authorization: `Bearer ${token}`,
      'User-Agent': 'openclaw-growth-revenuecat-exporter',
    },
  });
  const body = await response.text();
  if (!response.ok) {
    throw new Error(`RevenueCat ${pathname} failed with HTTP ${response.status}: ${body.slice(0, 500)}`);
  }
  return body.trim() ? JSON.parse(body) : {};
}

function listItems(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.items)) return payload.items;
  if (Array.isArray(payload?.data)) return payload.data;
  return [];
}

function projectId(project) {
  return String(project?.id || project?.project_id || '').trim();
}

async function fetchOptional(projectIdValue, label, pathname, params, warnings) {
  try {
    return await fetchRevenueCatJson(pathname, params);
  } catch (error) {
    warnings.push(`${label} for ${projectIdValue}: ${error instanceof Error ? error.message : String(error)}`);
    return null;
  }
}

async function buildSingleProjectSummary(project, args) {
  const id = projectId(project);
  if (!id) {
    throw new Error('RevenueCat project response did not contain a project id.');
  }

  const warnings = [];
  const limit = Math.max(1, Math.min(Number(args.limit) || 20, 100));
  const previous = previousWindow(args.from, args.to);
  const chartParams = {
    start_date: args.from,
    end_date: args.to,
    currency: args.currency,
    aggregate: 'total,average',
  };
  const chartNames = [...new Set(args.charts)].slice(0, 12);
  const [overviewPayload, revenuePayload, previousRevenuePayload, appsPayload, productsPayload, offeringsPayload, entitlementsPayload, paywallsPayload, webhooksPayload, customersPayload, ...chartResults] = await Promise.all([
    fetchOptional(id, 'overview metrics', `/projects/${encodeURIComponent(id)}/metrics/overview`, { currency: args.currency }, warnings),
    fetchOptional(id, 'revenue metric', `/projects/${encodeURIComponent(id)}/metrics/revenue`, { start_date: args.from, end_date: args.to, currency: args.currency, revenue_type: 'revenue' }, warnings),
    fetchOptional(id, 'previous revenue metric', `/projects/${encodeURIComponent(id)}/metrics/revenue`, { start_date: previous.from, end_date: previous.to, currency: args.currency, revenue_type: 'revenue' }, warnings),
    fetchOptional(id, 'apps', `/projects/${encodeURIComponent(id)}/apps`, { limit }, warnings),
    fetchOptional(id, 'products', `/projects/${encodeURIComponent(id)}/products`, { limit }, warnings),
    fetchOptional(id, 'offerings', `/projects/${encodeURIComponent(id)}/offerings`, { limit }, warnings),
    fetchOptional(id, 'entitlements', `/projects/${encodeURIComponent(id)}/entitlements`, { limit }, warnings),
    fetchOptional(id, 'paywalls', `/projects/${encodeURIComponent(id)}/paywalls`, { limit }, warnings),
    fetchOptional(id, 'webhook integrations', `/projects/${encodeURIComponent(id)}/integrations/webhooks`, { limit }, warnings),
    fetchOptional(id, 'customers', `/projects/${encodeURIComponent(id)}/customers`, { limit }, warnings),
    ...chartNames.map((chartName) =>
      fetchOptional(id, `chart ${String(chartName)}`, `/projects/${encodeURIComponent(id)}/charts/${encodeURIComponent(String(chartName))}`, chartParams, warnings)
        .then((payload) => ({ chartName: String(chartName), payload })),
    ),
  ]);

  return buildRevenueCatSummary({
    project,
    projectId: id,
    window: `${args.from}_${args.to}`,
    overviewPayload,
    revenuePayload,
    previousRevenuePayload,
    appsPayload,
    productsPayload,
    offeringsPayload,
    entitlementsPayload,
    paywallsPayload,
    webhooksPayload,
    customersPayload,
    chartsPayload: Object.fromEntries(chartResults.filter((entry) => entry.payload).map((entry) => [entry.chartName, entry.payload])),
    warnings,
    maxSignals: args.maxSignals,
  });
}

async function main() {
  await loadOpenClawGrowthSecrets();
  const args = parseArgs(process.argv.slice(2));
  const projectsPayload = await fetchRevenueCatJson('/projects', { limit: Math.max(1, Math.min(Number(args.limit) || 20, 100)) });
  const projects = listItems(projectsPayload);
  if (projects.length === 0) {
    throw new Error('RevenueCat API returned no visible projects for this key.');
  }

  const selectedProjects = args.project
    ? [projects.find((project) => projectId(project) === args.project) || { id: args.project }]
    : projects.slice(0, Math.max(1, Math.min(Number(args.maxProjects) || 10, 50)));
  const summaries = await Promise.all(selectedProjects.map((project) => buildSingleProjectSummary(project, args)));
  const summary = summaries.length === 1 ? summaries[0] : buildRevenueCatSummary({
    projects: summaries,
    window: `${args.from}_${args.to}`,
    maxSignals: args.maxSignals,
    availableProjectCount: projects.length,
    availableProjectIds: projects.map(projectId).filter(Boolean),
  });

  if (!args.project) {
    (summary.meta as Record<string, unknown>).availableProjectCount = projects.length;
    (summary.meta as Record<string, unknown>).availableProjectIds = projects.map(projectId).filter(Boolean);
  }

  await writeJsonOutput(args.out, summary);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
