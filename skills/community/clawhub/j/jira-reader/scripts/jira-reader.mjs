#!/usr/bin/env node

import { readFileSync } from 'node:fs';
const VERSION = '0.4.0';
loadEnvFile(process.env.JIRA_ENV_FILE || '.env');

class JiraRequestError extends Error { constructor(status, message) { super(message); this.status = status; } }

const config = {
  baseUrl: env('JIRA_BASE_URL'), email: env('JIRA_EMAIL'), project: env('JIRA_PROJECT'),
  token: env('JIRA_ACCESS_TOKEN'), cloudId: env('JIRA_CLOUD_ID'),
};
const [command, ...args] = process.argv.slice(2);
if (!command || command === '--help' || command === '-h') { usage(); process.exit(0); }
if (command === '--version' || command === '-v') { console.log(VERSION); process.exit(0); }

try {
  requireConfig(command);
  if (command === 'me') print(await jiraGet('/rest/api/3/myself'));
  else if (command === 'project') {
    const key = args[0] || config.project;
    print(await jiraGet(`/rest/api/3/project/${encodeURIComponent(key)}`));
  } else if (command === 'issue') {
    const issueKey = requiredArg(args[0], 'issue key');
    const fields = option(args, '--fields') || 'summary,status,assignee,reporter,priority,issuetype,created,updated,description,labels,components,fixVersions,project';
    print(summarizeIssue(await jiraGet(`/rest/api/3/issue/${encodeURIComponent(issueKey)}?fields=${encodeURIComponent(fields)}`)));
  } else if (command === 'search') print(await search(requiredArg(option(args, '--jql'), '--jql'), parseMax(option(args, '--max'), 20)));
  else if (command === 'recent') print(await search(`project = ${config.project} ORDER BY updated DESC`, parseMax(option(args, '--max'), 10)));
  else if (command === 'my-open') print(await search(`project = ${config.project} AND assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC`, parseMax(option(args, '--max'), 20)));
  else if (command === 'my-tasks-directory') print(await myTasksDirectory(args));
  else fail(`Unknown command: ${command}`);
} catch (error) { fail(error.message || String(error)); }

function env(name) { return process.env[name]?.trim() || ''; }

function loadEnvFile(path) {
  let content;
  try { content = readFileSync(path, 'utf8'); } catch (error) { if (error.code === 'ENOENT') return; throw error; }
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const match = /^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/.exec(line);
    if (!match) continue;
    const [, name, rawValue] = match;
    if (process.env[name] === undefined) process.env[name] = parseEnvValue(rawValue);
  }
}

function parseEnvValue(rawValue) {
  let value = rawValue.trim();
  if (value.startsWith('"') && value.endsWith('"')) return value.slice(1, -1).replace(/\\n/g, '\n').replace(/\\"/g, '"').replace(/\\\\/g, '\\');
  if (value.startsWith("'") && value.endsWith("'")) return value.slice(1, -1);
  const commentStart = value.search(/\s#/);
  if (commentStart !== -1) value = value.slice(0, commentStart).trimEnd();
  return value;
}

function requireConfig(activeCommand) {
  const missing = [];
  if (!config.baseUrl) missing.push('JIRA_BASE_URL');
  if (!config.token) missing.push('JIRA_ACCESS_TOKEN');
  if (!config.email) missing.push('JIRA_EMAIL');
  if (['project', 'recent', 'my-open'].includes(activeCommand) && !config.project) missing.push('JIRA_PROJECT');
  if (missing.length) fail(`Missing required env vars: ${missing.join(', ')}`);
  config.baseUrl = config.baseUrl.replace(/\/+$/, '');
}

async function jiraGet(path) { return jiraRequest('GET', path); }

async function jiraRequest(method, path, body) {
  if (!['GET', 'POST'].includes(method)) fail('Only read-only Jira requests are allowed');
  const response = await fetch(await jiraUrl(path), {
    method,
    headers: { Authorization: `Basic ${basicToken()}`, Accept: 'application/json', 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) {
    const responseText = await response.text();
    throw new JiraRequestError(response.status, `Jira API error ${response.status}: ${redact(responseText).slice(0, 800)}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

async function jiraUrl(path) {
  const cloudId = config.cloudId || await discoverCloudId();
  return `https://api.atlassian.com/ex/jira/${encodeURIComponent(cloudId)}${path}`;
}

async function discoverCloudId() {
  const response = await fetch(`${config.baseUrl}/_edge/tenant_info`, { headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`Could not discover Jira Cloud ID from JIRA_BASE_URL: HTTP ${response.status}`);
  const data = await response.json();
  if (!data.cloudId) throw new Error('Could not discover Jira Cloud ID from JIRA_BASE_URL');
  config.cloudId = data.cloudId;
  return config.cloudId;
}

async function search(jql, maxResults) {
  const data = await jiraRequest('POST', '/rest/api/3/search/jql', {
    jql, maxResults,
    fields: ['summary', 'status', 'assignee', 'priority', 'issuetype', 'updated', 'project'],
  });
  return {
    total: data.total ?? data.issues?.length ?? 0,
    maxResults: data.maxResults ?? maxResults,
    issues: (data.issues || []).map(summarizeIssue),
  };
}

async function myTasksDirectory(args) {
  const maxResults = parseMax(option(args, '--max'), 100);
  const requestedProject = option(args, '--project');
  const projectClause = requestedProject ? `project = "${escapeJql(requestedProject)}" AND ` : '';
  const jql = `${projectClause}assignee = currentUser() AND statusCategory != Done ORDER BY project ASC, status ASC, updated DESC`;
  const result = await search(jql, maxResults);
  const directory = {};
  for (const issue of result.issues) {
    const projectKey = issue.project?.key || issue.key?.split('-')[0] || 'UNKNOWN';
    const statusName = issue.status || 'Unknown';
    directory[projectKey] ??= {};
    directory[projectKey][statusName] ??= [];
    directory[projectKey][statusName].push(issue);
  }
  return {
    view: 'current-user-open-tasks',
    generatedAt: new Date().toISOString(),
    scope: { project: requestedProject || null, statusCategory: 'not Done' },
    total: result.total,
    returned: result.issues.length,
    truncated: result.total > result.issues.length,
    directory,
  };
}

function summarizeIssue(issue) {
  const fields = issue.fields || {};
  return {
    key: issue.key,
    url: `${config.baseUrl}/browse/${issue.key}`,
    project: fields.project ? { key: fields.project.key, name: fields.project.name } : undefined,
    type: fields.issuetype?.name,
    summary: fields.summary,
    status: fields.status?.name,
    priority: fields.priority?.name,
    assignee: fields.assignee?.displayName || null,
    reporter: fields.reporter?.displayName || null,
    updated: fields.updated,
    created: fields.created,
    labels: fields.labels,
    components: fields.components?.map((component) => component.name),
    fixVersions: fields.fixVersions?.map((version) => version.name),
    description: summarizeDescription(fields.description),
  };
}

function summarizeDescription(doc) {
  if (!doc) return undefined;
  const text = collectText(doc).replace(/\s+/g, ' ').trim();
  return text ? text.slice(0, 1200) : undefined;
}

function collectText(node) {
  if (!node || typeof node !== 'object') return '';
  let result = typeof node.text === 'string' ? node.text : '';
  if (Array.isArray(node.content)) result += ' ' + node.content.map(collectText).join(' ');
  return result;
}

function escapeJql(value) { return String(value).replace(/\\/g, '\\\\').replace(/"/g, '\\"'); }

function option(args, name) {
  const index = args.indexOf(name);
  if (index === -1) return undefined;
  if (!args[index + 1] || args[index + 1].startsWith('--')) fail(`Missing value for ${name}`);
  return args[index + 1];
}

function requiredArg(value, label) { if (!value) fail(`Missing ${label}`); return value; }

function parseMax(value, fallback) {
  if (!value) return fallback;
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed < 1 || parsed > 100) fail('--max must be between 1 and 100');
  return parsed;
}

function print(value) { console.log(JSON.stringify(value, null, 2)); }

function redact(text) {
  let redacted = text;
  if (config.token) redacted = redacted.replaceAll(config.token, '<redacted>');
  if (config.email && config.token) redacted = redacted.replaceAll(basicToken(), '<redacted>');
  return redacted;
}

function basicToken() { return Buffer.from(`${config.email}:${config.token}`).toString('base64'); }
function fail(message) { console.error(message); process.exit(1); }

function usage() {
  console.log(`jira-reader ${VERSION}\n\nUsage:\n  jira-reader me\n  jira-reader project [PROJECT_KEY]\n  jira-reader issue ISSUE-123 [--fields summary,status]\n  jira-reader search --jql "project = PROJ ORDER BY updated DESC" [--max 20]\n  jira-reader recent [--max 10]\n  jira-reader my-open [--max 20]\n  jira-reader my-tasks-directory [--project PROJ] [--max 100]\n\nmy-tasks-directory returns open tasks assigned to currentUser() grouped by project and status.\n`);
}
