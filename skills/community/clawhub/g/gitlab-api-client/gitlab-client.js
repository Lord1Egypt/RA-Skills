#!/usr/bin/env node
'use strict';

// ---------------------------------------------------------------------------
// GitLab REST API v4 CLI Client
// ---------------------------------------------------------------------------
// Usage: gitlab-client <resource> <action> [positional-id] [--key value ...]
//
// Reads GITLAB_URL and GITLAB_TOKEN from .env in the same directory as this
// script.  Uses only Node.js built-in http/https modules (plus dotenv).
// ---------------------------------------------------------------------------

const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// ── Load .env from the script's own directory ──────────────────────────────
const SCRIPT_DIR = __dirname;
const envPath = path.join(SCRIPT_DIR, '.env');

try {
  require('dotenv').config({ path: envPath });
} catch {
  // dotenv not installed yet – fall through; we'll check the vars below
}

// Env vars are validated lazily so --help works without .env
let _GITLAB_URL, _GITLAB_TOKEN, _API_BASE;

function getConfig() {
  if (_API_BASE) return { GITLAB_URL: _GITLAB_URL, GITLAB_TOKEN: _GITLAB_TOKEN, API_BASE: _API_BASE };

  _GITLAB_URL = (process.env.GITLAB_URL || '').replace(/\/+$/, '');
  _GITLAB_TOKEN = process.env.GITLAB_TOKEN || '';

  if (!_GITLAB_URL || !_GITLAB_TOKEN) {
    process.stderr.write(
      `Error: GITLAB_URL and GITLAB_TOKEN must be set.\n\n` +
      `Create a file at ${envPath} with:\n\n` +
      `  GITLAB_URL=https://gitlab.example.com\n` +
      `  GITLAB_TOKEN=your-private-access-token\n\n` +
      `Then run:  cd ${SCRIPT_DIR} && npm install\n`
    );
    process.exit(1);
  }

  _API_BASE = `${_GITLAB_URL}/api/v4`;
  return { GITLAB_URL: _GITLAB_URL, GITLAB_TOKEN: _GITLAB_TOKEN, API_BASE: _API_BASE };
}

// ── Boolean flags (presence == true) ───────────────────────────────────────
const BOOLEAN_FLAGS = new Set([
  'owned', 'membership', 'confidential', 'recursive',
  'remove-source-branch', 'squash', 'initialize-with-readme',
  'simple', 'push-events', 'merge-requests-events', 'issues-events',
  'should-remove-source-branch', 'archived',
]);

// ── Argument parser ───────────────────────────────────────────────────────
function parseArgs(argv) {
  const args = argv.slice(2); // drop node, script
  const resource = args[0] || '';
  const action = args[1] || '';
  let positional = null;
  const named = {};

  let i = 2;
  // If arg[2] exists and doesn't start with '--', treat as positional id
  if (i < args.length && !args[i].startsWith('--')) {
    positional = args[i];
    i++;
  }

  while (i < args.length) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2); // e.g. "per-page"
      if (BOOLEAN_FLAGS.has(key)) {
        named[key] = 'true';
        i++;
      } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        named[key] = args[i + 1];
        i += 2;
      } else {
        // flag with no value – treat as boolean true
        named[key] = 'true';
        i++;
      }
    } else {
      i++; // skip unknown positional
    }
  }

  return { resource, action, positional, named };
}

// ── kebab-case → snake_case ───────────────────────────────────────────────
function toSnake(s) {
  return s.replace(/-/g, '_');
}

// ── URL-encode a path segment (project id / file path / branch) ──────────
function enc(v) {
  return encodeURIComponent(v);
}

// ── HTTP request helper ───────────────────────────────────────────────────
function request(method, urlStr, body, { rawResponse = false, maxRedirects = 5 } = {}) {
  return new Promise((resolve, reject) => {
    const doRequest = (urlStr, redirectsLeft) => {
      const parsed = new URL(urlStr);
      const mod = parsed.protocol === 'https:' ? https : http;
      const headers = { 'PRIVATE-TOKEN': getConfig().GITLAB_TOKEN };
      let payload = null;

      if (body && (method === 'POST' || method === 'PUT')) {
        payload = JSON.stringify(body);
        headers['Content-Type'] = 'application/json';
        headers['Content-Length'] = Buffer.byteLength(payload);
      }

      const opts = {
        method,
        hostname: parsed.hostname,
        port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
        path: parsed.pathname + parsed.search,
        headers,
      };

      const req = mod.request(opts, (res) => {
        // Handle redirects
        if ([301, 302, 307, 308].includes(res.statusCode) && res.headers.location) {
          if (redirectsLeft <= 0) return reject(new Error('Too many redirects'));
          const next = new URL(res.headers.location, urlStr).toString();
          return doRequest(next, redirectsLeft - 1);
        }

        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const raw = Buffer.concat(chunks);
          resolve({ status: res.statusCode, headers: res.headers, raw, rawResponse });
        });
      });

      req.on('error', (err) => reject(err));
      if (payload) req.write(payload);
      req.end();
    };

    doRequest(urlStr, maxRedirects);
  });
}

// ── Pagination info helper ────────────────────────────────────────────────
function showPagination(headers) {
  const page = headers['x-page'];
  const totalPages = headers['x-total-pages'];
  const total = headers['x-total'];
  const perPage = headers['x-per-page'];
  const nextPage = headers['x-next-page'];

  if (page || total) {
    const parts = [];
    if (page && totalPages) parts.push(`Page ${page}/${totalPages}`);
    else if (page) parts.push(`Page ${page}`);
    if (perPage && total) parts.push(`showing ${perPage} of ${total} items`);
    else if (total) parts.push(`${total} total items`);
    if (nextPage) parts.push(`next page: ${nextPage}`);
    process.stderr.write(parts.join(', ') + '\n');
  }
}

// ── Main request + output ─────────────────────────────────────────────────
async function apiCall(method, endpoint, { query = {}, body = null, plainText = false } = {}) {
  // Build URL with query params
  const qs = Object.entries(query)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');
  const url = `${getConfig().API_BASE}${endpoint}${qs ? '?' + qs : ''}`;

  let resp;
  try {
    resp = await request(method, url, body, { rawResponse: plainText });
  } catch (err) {
    process.stderr.write(`Network error: ${err.message}\n`);
    process.exit(1);
  }

  if (resp.status >= 400) {
    let errMsg = '';
    try {
      const json = JSON.parse(resp.raw.toString('utf8'));
      errMsg = JSON.stringify(json, null, 2);
    } catch {
      errMsg = resp.raw.toString('utf8');
    }
    process.stderr.write(`HTTP ${resp.status} Error:\n${errMsg}\n`);
    process.exit(1);
  }

  if (plainText) {
    process.stdout.write(resp.raw.toString('utf8'));
    return;
  }

  // Show pagination info on stderr for list endpoints
  showPagination(resp.headers);

  // Output JSON
  const text = resp.raw.toString('utf8');
  if (!text || text.trim() === '') {
    // No content (204 etc)
    process.stdout.write('{}\n');
    return;
  }
  try {
    const json = JSON.parse(text);
    process.stdout.write(JSON.stringify(json, null, 2) + '\n');
  } catch {
    process.stdout.write(text + '\n');
  }
}

// ── Helper: require a named param or die ──────────────────────────────────
function requireParam(named, key, label) {
  if (!named[key]) {
    process.stderr.write(`Error: --${key} is required${label ? ' (' + label + ')' : ''}.\n`);
    process.exit(1);
  }
  return named[key];
}

// ── Pick known query params from named args ───────────────────────────────
function pickQuery(named, keys) {
  const q = {};
  for (const k of keys) {
    if (named[k] !== undefined) q[toSnake(k)] = named[k];
  }
  return q;
}

// ── Pick known body params from named args ────────────────────────────────
function pickBody(named, keys) {
  const b = {};
  for (const k of keys) {
    if (named[k] !== undefined) b[toSnake(k)] = named[k];
  }
  return Object.keys(b).length ? b : null;
}

// ── Convenience: project id from --project or positional ──────────────────
function projectId(named, positional) {
  return named['project'] || positional || null;
}

// ── Error: unknown action ─────────────────────────────────────────────────
function unknownAction(resource, action, validActions) {
  process.stderr.write(
    `Unknown action "${action}" for resource "${resource}".\n` +
    `Valid actions: ${validActions.join(', ')}\n`
  );
  process.exit(1);
}

// ══════════════════════════════════════════════════════════════════════════
// ── Resource handlers ─────────────────────────────────────────────────────
// ══════════════════════════════════════════════════════════════════════════

// ── PROJECTS ──────────────────────────────────────────────────────────────
async function handleProjects(action, positional, named) {
  const actions = ['list', 'get', 'search', 'create', 'edit', 'delete', 'fork', 'members', 'hooks'];

  switch (action) {
    case 'list': {
      const q = pickQuery(named, [
        'page', 'per-page', 'search', 'owned', 'membership',
        'visibility', 'order-by', 'sort', 'archived', 'simple',
      ]);
      return apiCall('GET', '/projects', { query: q });
    }
    case 'get': {
      const id = positional || requireParam(named, 'id', 'project id');
      return apiCall('GET', `/projects/${enc(id)}`);
    }
    case 'search': {
      const term = positional || requireParam(named, 'search', 'search term');
      return apiCall('GET', '/projects', { query: { search: term } });
    }
    case 'create': {
      const body = pickBody(named, [
        'name', 'description', 'visibility', 'namespace-id', 'initialize-with-readme',
      ]);
      if (!body || !body.name) {
        requireParam(named, 'name', 'project name');
      }
      return apiCall('POST', '/projects', { body });
    }
    case 'edit': {
      const id = positional || requireParam(named, 'id', 'project id');
      const body = pickBody(named, ['name', 'description', 'visibility', 'default-branch']);
      return apiCall('PUT', `/projects/${enc(id)}`, { body });
    }
    case 'delete': {
      const id = positional || requireParam(named, 'id', 'project id');
      return apiCall('DELETE', `/projects/${enc(id)}`);
    }
    case 'fork': {
      const id = positional || requireParam(named, 'id', 'project id');
      const body = pickBody(named, ['namespace']);
      return apiCall('POST', `/projects/${enc(id)}/fork`, { body });
    }
    case 'members': {
      const id = positional || requireParam(named, 'id', 'project id');
      return apiCall('GET', `/projects/${enc(id)}/members`);
    }
    case 'hooks': {
      const id = positional || requireParam(named, 'id', 'project id');
      return apiCall('GET', `/projects/${enc(id)}/hooks`);
    }
    default:
      unknownAction('projects', action, actions);
  }
}

// ── ISSUES ────────────────────────────────────────────────────────────────
async function handleIssues(action, positional, named) {
  const actions = ['list', 'get', 'create', 'edit', 'close', 'reopen', 'delete', 'notes', 'add-note'];
  const pid = projectId(named, null);

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, [
        'state', 'labels', 'milestone', 'assignee-id', 'search', 'scope',
        'page', 'per-page', 'order-by', 'sort', 'created-after', 'created-before',
      ]);
      return apiCall('GET', `/projects/${enc(p)}/issues`, { query: q });
    }
    case 'get': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'issue iid');
      return apiCall('GET', `/projects/${enc(p)}/issues/${enc(iid)}`);
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'title', 'issue title');
      const body = pickBody(named, [
        'title', 'description', 'labels', 'assignee-ids', 'milestone-id',
        'due-date', 'confidential',
      ]);
      return apiCall('POST', `/projects/${enc(p)}/issues`, { body });
    }
    case 'edit': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'issue iid');
      const body = pickBody(named, [
        'title', 'description', 'state-event', 'labels', 'assignee-ids',
      ]);
      return apiCall('PUT', `/projects/${enc(p)}/issues/${enc(iid)}`, { body });
    }
    case 'close': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'issue iid');
      return apiCall('PUT', `/projects/${enc(p)}/issues/${enc(iid)}`, {
        body: { state_event: 'close' },
      });
    }
    case 'reopen': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'issue iid');
      return apiCall('PUT', `/projects/${enc(p)}/issues/${enc(iid)}`, {
        body: { state_event: 'reopen' },
      });
    }
    case 'delete': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'issue iid');
      return apiCall('DELETE', `/projects/${enc(p)}/issues/${enc(iid)}`);
    }
    case 'notes': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'issue iid');
      return apiCall('GET', `/projects/${enc(p)}/issues/${enc(iid)}/notes`);
    }
    case 'add-note': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'issue iid');
      requireParam(named, 'body', 'note body');
      return apiCall('POST', `/projects/${enc(p)}/issues/${enc(iid)}/notes`, {
        body: { body: named['body'] },
      });
    }
    default:
      unknownAction('issues', action, actions);
  }
}

// ── MERGE REQUESTS ────────────────────────────────────────────────────────
async function handleMrs(action, positional, named) {
  const actions = [
    'list', 'get', 'create', 'edit', 'merge', 'changes', 'commits',
    'notes', 'add-note', 'approve', 'pipelines',
  ];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, [
        'state', 'labels', 'milestone', 'source-branch', 'target-branch',
        'search', 'scope', 'page', 'per-page', 'order-by', 'sort',
      ]);
      return apiCall('GET', `/projects/${enc(p)}/merge_requests`, { query: q });
    }
    case 'get': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      return apiCall('GET', `/projects/${enc(p)}/merge_requests/${enc(iid)}`);
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'source-branch', 'source branch');
      requireParam(named, 'target-branch', 'target branch');
      requireParam(named, 'title', 'MR title');
      const body = pickBody(named, [
        'source-branch', 'target-branch', 'title', 'description',
        'assignee-id', 'reviewer-ids', 'labels', 'milestone-id',
        'remove-source-branch', 'squash',
      ]);
      return apiCall('POST', `/projects/${enc(p)}/merge_requests`, { body });
    }
    case 'edit': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      const body = pickBody(named, [
        'title', 'description', 'state-event', 'labels', 'assignee-id',
      ]);
      return apiCall('PUT', `/projects/${enc(p)}/merge_requests/${enc(iid)}`, { body });
    }
    case 'merge': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      const body = pickBody(named, [
        'merge-commit-message', 'squash', 'should-remove-source-branch',
      ]);
      return apiCall('PUT', `/projects/${enc(p)}/merge_requests/${enc(iid)}/merge`, { body });
    }
    case 'changes': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      return apiCall('GET', `/projects/${enc(p)}/merge_requests/${enc(iid)}/changes`);
    }
    case 'commits': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      return apiCall('GET', `/projects/${enc(p)}/merge_requests/${enc(iid)}/commits`);
    }
    case 'notes': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      return apiCall('GET', `/projects/${enc(p)}/merge_requests/${enc(iid)}/notes`);
    }
    case 'add-note': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      requireParam(named, 'body', 'note body');
      return apiCall('POST', `/projects/${enc(p)}/merge_requests/${enc(iid)}/notes`, {
        body: { body: named['body'] },
      });
    }
    case 'approve': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      return apiCall('POST', `/projects/${enc(p)}/merge_requests/${enc(iid)}/approve`);
    }
    case 'pipelines': {
      const p = requireParam(named, 'project', 'project id');
      const iid = positional || requireParam(named, 'iid', 'MR iid');
      return apiCall('GET', `/projects/${enc(p)}/merge_requests/${enc(iid)}/pipelines`);
    }
    default:
      unknownAction('mrs', action, actions);
  }
}

// ── BRANCHES ──────────────────────────────────────────────────────────────
async function handleBranches(action, positional, named) {
  const actions = ['list', 'get', 'create', 'delete', 'delete-merged'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['search', 'page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/repository/branches`, { query: q });
    }
    case 'get': {
      const p = requireParam(named, 'project', 'project id');
      const branch = positional || requireParam(named, 'branch', 'branch name');
      return apiCall('GET', `/projects/${enc(p)}/repository/branches/${enc(branch)}`);
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'branch', 'branch name');
      requireParam(named, 'ref', 'ref to branch from');
      const body = pickBody(named, ['branch', 'ref']);
      return apiCall('POST', `/projects/${enc(p)}/repository/branches`, { body });
    }
    case 'delete': {
      const p = requireParam(named, 'project', 'project id');
      const branch = positional || requireParam(named, 'branch', 'branch name');
      return apiCall('DELETE', `/projects/${enc(p)}/repository/branches/${enc(branch)}`);
    }
    case 'delete-merged': {
      const p = requireParam(named, 'project', 'project id');
      return apiCall('DELETE', `/projects/${enc(p)}/repository/merged_branches`);
    }
    default:
      unknownAction('branches', action, actions);
  }
}

// ── COMMITS ───────────────────────────────────────────────────────────────
async function handleCommits(action, positional, named) {
  const actions = ['list', 'get', 'diff', 'comments', 'add-comment'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['ref-name', 'since', 'until', 'path', 'page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/repository/commits`, { query: q });
    }
    case 'get': {
      const p = requireParam(named, 'project', 'project id');
      const sha = positional || requireParam(named, 'sha', 'commit SHA');
      return apiCall('GET', `/projects/${enc(p)}/repository/commits/${enc(sha)}`);
    }
    case 'diff': {
      const p = requireParam(named, 'project', 'project id');
      const sha = positional || requireParam(named, 'sha', 'commit SHA');
      return apiCall('GET', `/projects/${enc(p)}/repository/commits/${enc(sha)}/diff`);
    }
    case 'comments': {
      const p = requireParam(named, 'project', 'project id');
      const sha = positional || requireParam(named, 'sha', 'commit SHA');
      return apiCall('GET', `/projects/${enc(p)}/repository/commits/${enc(sha)}/comments`);
    }
    case 'add-comment': {
      const p = requireParam(named, 'project', 'project id');
      const sha = positional || requireParam(named, 'sha', 'commit SHA');
      requireParam(named, 'note', 'comment text');
      return apiCall('POST', `/projects/${enc(p)}/repository/commits/${enc(sha)}/comments`, {
        body: { note: named['note'] },
      });
    }
    default:
      unknownAction('commits', action, actions);
  }
}

// ── REPO (repository files / tree / compare) ─────────────────────────────
async function handleRepo(action, positional, named) {
  const actions = ['tree', 'file', 'raw', 'create-file', 'update-file', 'delete-file', 'compare'];

  switch (action) {
    case 'tree': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['path', 'ref', 'recursive', 'page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/repository/tree`, { query: q });
    }
    case 'file': {
      const p = requireParam(named, 'project', 'project id');
      const fp = requireParam(named, 'file-path', 'file path');
      const q = pickQuery(named, ['ref']);
      return apiCall('GET', `/projects/${enc(p)}/repository/files/${enc(fp)}`, { query: q });
    }
    case 'raw': {
      const p = requireParam(named, 'project', 'project id');
      const fp = requireParam(named, 'file-path', 'file path');
      const q = pickQuery(named, ['ref']);
      return apiCall('GET', `/projects/${enc(p)}/repository/files/${enc(fp)}/raw`, {
        query: q,
        plainText: true,
      });
    }
    case 'create-file': {
      const p = requireParam(named, 'project', 'project id');
      const fp = requireParam(named, 'file-path', 'file path');
      requireParam(named, 'branch', 'branch');
      requireParam(named, 'content', 'file content');
      requireParam(named, 'commit-message', 'commit message');
      const body = pickBody(named, ['branch', 'content', 'commit-message', 'encoding']);
      return apiCall('POST', `/projects/${enc(p)}/repository/files/${enc(fp)}`, { body });
    }
    case 'update-file': {
      const p = requireParam(named, 'project', 'project id');
      const fp = requireParam(named, 'file-path', 'file path');
      requireParam(named, 'branch', 'branch');
      requireParam(named, 'content', 'file content');
      requireParam(named, 'commit-message', 'commit message');
      const body = pickBody(named, ['branch', 'content', 'commit-message']);
      return apiCall('PUT', `/projects/${enc(p)}/repository/files/${enc(fp)}`, { body });
    }
    case 'delete-file': {
      const p = requireParam(named, 'project', 'project id');
      const fp = requireParam(named, 'file-path', 'file path');
      requireParam(named, 'branch', 'branch');
      requireParam(named, 'commit-message', 'commit message');
      // DELETE with body: send as query + body
      const body = pickBody(named, ['branch', 'commit-message']);
      return apiCall('DELETE', `/projects/${enc(p)}/repository/files/${enc(fp)}`, { body });
    }
    case 'compare': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'from', 'from ref');
      requireParam(named, 'to', 'to ref');
      const q = pickQuery(named, ['from', 'to']);
      return apiCall('GET', `/projects/${enc(p)}/repository/compare`, { query: q });
    }
    default:
      unknownAction('repo', action, actions);
  }
}

// ── PIPELINES ─────────────────────────────────────────────────────────────
async function handlePipelines(action, positional, named) {
  const actions = ['list', 'get', 'jobs', 'job-log', 'retry', 'cancel', 'create'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['status', 'ref', 'page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/pipelines`, { query: q });
    }
    case 'get': {
      const p = requireParam(named, 'project', 'project id');
      const pid = positional || requireParam(named, 'pipeline-id', 'pipeline id');
      return apiCall('GET', `/projects/${enc(p)}/pipelines/${enc(pid)}`);
    }
    case 'jobs': {
      const p = requireParam(named, 'project', 'project id');
      const pid = positional || requireParam(named, 'pipeline-id', 'pipeline id');
      return apiCall('GET', `/projects/${enc(p)}/pipelines/${enc(pid)}/jobs`);
    }
    case 'job-log': {
      const p = requireParam(named, 'project', 'project id');
      const jid = positional || requireParam(named, 'job-id', 'job id');
      return apiCall('GET', `/projects/${enc(p)}/jobs/${enc(jid)}/trace`, { plainText: true });
    }
    case 'retry': {
      const p = requireParam(named, 'project', 'project id');
      const pid = positional || requireParam(named, 'pipeline-id', 'pipeline id');
      return apiCall('POST', `/projects/${enc(p)}/pipelines/${enc(pid)}/retry`);
    }
    case 'cancel': {
      const p = requireParam(named, 'project', 'project id');
      const pid = positional || requireParam(named, 'pipeline-id', 'pipeline id');
      return apiCall('POST', `/projects/${enc(p)}/pipelines/${enc(pid)}/cancel`);
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'ref', 'ref/branch');
      const body = { ref: named['ref'] };
      // Handle --variables "KEY1=val1,KEY2=val2"
      if (named['variables']) {
        const vars = named['variables'].split(',').map((pair) => {
          const [key, ...rest] = pair.split('=');
          return { key: key.trim(), value: rest.join('=').trim() };
        });
        body.variables = vars;
      }
      return apiCall('POST', `/projects/${enc(p)}/pipeline`, { body });
    }
    default:
      unknownAction('pipelines', action, actions);
  }
}

// ── GROUPS ─────────────────────────────────────────────────────────────────
async function handleGroups(action, positional, named) {
  const actions = ['list', 'get', 'projects', 'members', 'issues', 'mrs'];

  switch (action) {
    case 'list': {
      const q = pickQuery(named, ['search', 'owned', 'page', 'per-page']);
      return apiCall('GET', '/groups', { query: q });
    }
    case 'get': {
      const id = positional || requireParam(named, 'id', 'group id');
      return apiCall('GET', `/groups/${enc(id)}`);
    }
    case 'projects': {
      const id = positional || requireParam(named, 'id', 'group id');
      const q = pickQuery(named, ['search', 'page', 'per-page']);
      return apiCall('GET', `/groups/${enc(id)}/projects`, { query: q });
    }
    case 'members': {
      const id = positional || requireParam(named, 'id', 'group id');
      return apiCall('GET', `/groups/${enc(id)}/members`);
    }
    case 'issues': {
      const id = positional || requireParam(named, 'id', 'group id');
      const q = pickQuery(named, ['state', 'page', 'per-page']);
      return apiCall('GET', `/groups/${enc(id)}/issues`, { query: q });
    }
    case 'mrs': {
      const id = positional || requireParam(named, 'id', 'group id');
      const q = pickQuery(named, ['state', 'page', 'per-page']);
      return apiCall('GET', `/groups/${enc(id)}/merge_requests`, { query: q });
    }
    default:
      unknownAction('groups', action, actions);
  }
}

// ── USERS ──────────────────────────────────────────────────────────────────
async function handleUsers(action, positional, named) {
  const actions = ['me', 'list', 'get', 'projects'];

  switch (action) {
    case 'me':
      return apiCall('GET', '/user');
    case 'list': {
      const q = pickQuery(named, ['search', 'page', 'per-page']);
      return apiCall('GET', '/users', { query: q });
    }
    case 'get': {
      const id = positional || requireParam(named, 'id', 'user id');
      return apiCall('GET', `/users/${enc(id)}`);
    }
    case 'projects': {
      const id = positional || requireParam(named, 'id', 'user id');
      const q = pickQuery(named, ['page', 'per-page']);
      return apiCall('GET', `/users/${enc(id)}/projects`, { query: q });
    }
    default:
      unknownAction('users', action, actions);
  }
}

// ── LABELS ─────────────────────────────────────────────────────────────────
async function handleLabels(action, positional, named) {
  const actions = ['list', 'create', 'edit', 'delete'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/labels`, { query: q });
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'name', 'label name');
      requireParam(named, 'color', 'label color');
      const body = pickBody(named, ['name', 'color', 'description']);
      return apiCall('POST', `/projects/${enc(p)}/labels`, { body });
    }
    case 'edit': {
      const p = requireParam(named, 'project', 'project id');
      const labelId = positional || requireParam(named, 'label-id', 'label id');
      const body = pickBody(named, ['new-name', 'color', 'description']);
      return apiCall('PUT', `/projects/${enc(p)}/labels/${enc(labelId)}`, { body });
    }
    case 'delete': {
      const p = requireParam(named, 'project', 'project id');
      const labelId = positional || requireParam(named, 'label-id', 'label id');
      return apiCall('DELETE', `/projects/${enc(p)}/labels/${enc(labelId)}`);
    }
    default:
      unknownAction('labels', action, actions);
  }
}

// ── MILESTONES ─────────────────────────────────────────────────────────────
async function handleMilestones(action, positional, named) {
  const actions = ['list', 'get', 'create', 'edit', 'delete'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['state', 'page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/milestones`, { query: q });
    }
    case 'get': {
      const p = requireParam(named, 'project', 'project id');
      const mid = positional || requireParam(named, 'milestone-id', 'milestone id');
      return apiCall('GET', `/projects/${enc(p)}/milestones/${enc(mid)}`);
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'title', 'milestone title');
      const body = pickBody(named, ['title', 'description', 'due-date', 'start-date']);
      return apiCall('POST', `/projects/${enc(p)}/milestones`, { body });
    }
    case 'edit': {
      const p = requireParam(named, 'project', 'project id');
      const mid = positional || requireParam(named, 'milestone-id', 'milestone id');
      const body = pickBody(named, ['title', 'description', 'state-event', 'due-date', 'start-date']);
      return apiCall('PUT', `/projects/${enc(p)}/milestones/${enc(mid)}`, { body });
    }
    case 'delete': {
      const p = requireParam(named, 'project', 'project id');
      const mid = positional || requireParam(named, 'milestone-id', 'milestone id');
      return apiCall('DELETE', `/projects/${enc(p)}/milestones/${enc(mid)}`);
    }
    default:
      unknownAction('milestones', action, actions);
  }
}

// ── TAGS ───────────────────────────────────────────────────────────────────
async function handleTags(action, positional, named) {
  const actions = ['list', 'create', 'delete'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['search', 'page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/repository/tags`, { query: q });
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'tag-name', 'tag name');
      requireParam(named, 'ref', 'ref');
      const body = pickBody(named, ['tag-name', 'ref', 'message']);
      return apiCall('POST', `/projects/${enc(p)}/repository/tags`, { body });
    }
    case 'delete': {
      const p = requireParam(named, 'project', 'project id');
      const tag = positional || requireParam(named, 'tag-name', 'tag name');
      return apiCall('DELETE', `/projects/${enc(p)}/repository/tags/${enc(tag)}`);
    }
    default:
      unknownAction('tags', action, actions);
  }
}

// ── RELEASES ──────────────────────────────────────────────────────────────
async function handleReleases(action, positional, named) {
  const actions = ['list', 'create'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/releases`, { query: q });
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'tag-name', 'tag name');
      const body = pickBody(named, ['tag-name', 'name', 'description']);
      return apiCall('POST', `/projects/${enc(p)}/releases`, { body });
    }
    default:
      unknownAction('releases', action, actions);
  }
}

// ── SNIPPETS ──────────────────────────────────────────────────────────────
async function handleSnippets(action, positional, named) {
  const actions = ['list', 'get', 'create'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/snippets`, { query: q });
    }
    case 'get': {
      const p = requireParam(named, 'project', 'project id');
      const sid = positional || requireParam(named, 'snippet-id', 'snippet id');
      return apiCall('GET', `/projects/${enc(p)}/snippets/${enc(sid)}`);
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'title', 'snippet title');
      requireParam(named, 'file-name', 'file name');
      requireParam(named, 'content', 'snippet content');
      const body = pickBody(named, ['title', 'file-name', 'content', 'visibility']);
      return apiCall('POST', `/projects/${enc(p)}/snippets`, { body });
    }
    default:
      unknownAction('snippets', action, actions);
  }
}

// ── SEARCH ────────────────────────────────────────────────────────────────
async function handleSearch(action, positional, named) {
  const actions = ['global', 'project', 'group'];

  switch (action) {
    case 'global': {
      requireParam(named, 'scope', 'search scope');
      requireParam(named, 'search', 'search query');
      const q = pickQuery(named, ['scope', 'search', 'page', 'per-page']);
      return apiCall('GET', '/search', { query: q });
    }
    case 'project': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'scope', 'search scope');
      requireParam(named, 'search', 'search query');
      const q = pickQuery(named, ['scope', 'search', 'page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/search`, { query: q });
    }
    case 'group': {
      const g = requireParam(named, 'group', 'group id');
      requireParam(named, 'scope', 'search scope');
      requireParam(named, 'search', 'search query');
      const q = pickQuery(named, ['scope', 'search', 'page', 'per-page']);
      return apiCall('GET', `/groups/${enc(g)}/search`, { query: q });
    }
    default:
      unknownAction('search', action, actions);
  }
}

// ── RUNNERS ───────────────────────────────────────────────────────────────
async function handleRunners(action, positional, named) {
  const actions = ['list', 'all'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/runners`, { query: q });
    }
    case 'all': {
      const q = pickQuery(named, ['type', 'status', 'page', 'per-page']);
      return apiCall('GET', '/runners/all', { query: q });
    }
    default:
      unknownAction('runners', action, actions);
  }
}

// ── HOOKS (webhooks) ──────────────────────────────────────────────────────
async function handleHooks(action, positional, named) {
  const actions = ['list', 'create', 'delete'];

  switch (action) {
    case 'list': {
      const p = requireParam(named, 'project', 'project id');
      const q = pickQuery(named, ['page', 'per-page']);
      return apiCall('GET', `/projects/${enc(p)}/hooks`, { query: q });
    }
    case 'create': {
      const p = requireParam(named, 'project', 'project id');
      requireParam(named, 'url', 'webhook URL');
      const body = pickBody(named, [
        'url', 'push-events', 'merge-requests-events', 'issues-events', 'token',
      ]);
      return apiCall('POST', `/projects/${enc(p)}/hooks`, { body });
    }
    case 'delete': {
      const p = requireParam(named, 'project', 'project id');
      const hid = positional || requireParam(named, 'hook-id', 'hook id');
      return apiCall('DELETE', `/projects/${enc(p)}/hooks/${enc(hid)}`);
    }
    default:
      unknownAction('hooks', action, actions);
  }
}

// ══════════════════════════════════════════════════════════════════════════
// ── Usage / help ──────────────────────────────────────────────────────────
// ══════════════════════════════════════════════════════════════════════════

const RESOURCES = {
  projects:   ['list', 'get', 'search', 'create', 'edit', 'delete', 'fork', 'members', 'hooks'],
  issues:     ['list', 'get', 'create', 'edit', 'close', 'reopen', 'delete', 'notes', 'add-note'],
  mrs:        ['list', 'get', 'create', 'edit', 'merge', 'changes', 'commits', 'notes', 'add-note', 'approve', 'pipelines'],
  branches:   ['list', 'get', 'create', 'delete', 'delete-merged'],
  commits:    ['list', 'get', 'diff', 'comments', 'add-comment'],
  repo:       ['tree', 'file', 'raw', 'create-file', 'update-file', 'delete-file', 'compare'],
  pipelines:  ['list', 'get', 'jobs', 'job-log', 'retry', 'cancel', 'create'],
  groups:     ['list', 'get', 'projects', 'members', 'issues', 'mrs'],
  users:      ['me', 'list', 'get', 'projects'],
  labels:     ['list', 'create', 'edit', 'delete'],
  milestones: ['list', 'get', 'create', 'edit', 'delete'],
  tags:       ['list', 'create', 'delete'],
  releases:   ['list', 'create'],
  snippets:   ['list', 'get', 'create'],
  search:     ['global', 'project', 'group'],
  runners:    ['list', 'all'],
  hooks:      ['list', 'create', 'delete'],
};

function showHelp() {
  let msg = 'Usage: gitlab-client <resource> <action> [id] [--key value ...]\n\n';
  msg += 'Resources and actions:\n\n';
  for (const [res, acts] of Object.entries(RESOURCES)) {
    msg += `  ${res.padEnd(12)} ${acts.join(', ')}\n`;
  }
  msg += '\nExamples:\n';
  msg += '  gitlab-client projects list --owned --per-page 50\n';
  msg += '  gitlab-client projects get 42\n';
  msg += '  gitlab-client issues list --project 42 --state opened\n';
  msg += '  gitlab-client mrs create --project 42 --source-branch feat --target-branch main --title "My MR"\n';
  msg += '  gitlab-client users me\n';
  msg += '  gitlab-client pipelines job-log --project 42 --job-id 1234\n';
  msg += '\nUse --help for this message.\n';
  process.stdout.write(msg);
}

// ══════════════════════════════════════════════════════════════════════════
// ── Main dispatch ─────────────────────────────────────────────────────────
// ══════════════════════════════════════════════════════════════════════════

const HANDLERS = {
  projects:   handleProjects,
  issues:     handleIssues,
  mrs:        handleMrs,
  branches:   handleBranches,
  commits:    handleCommits,
  repo:       handleRepo,
  pipelines:  handlePipelines,
  groups:     handleGroups,
  users:      handleUsers,
  labels:     handleLabels,
  milestones: handleMilestones,
  tags:       handleTags,
  releases:   handleReleases,
  snippets:   handleSnippets,
  search:     handleSearch,
  runners:    handleRunners,
  hooks:      handleHooks,
};

async function main() {
  // Check for --help anywhere in raw args before parsing
  if (process.argv.includes('--help') || process.argv.includes('-h') || process.argv.length <= 2) {
    showHelp();
    process.exit(0);
  }

  const { resource, action, positional, named } = parseArgs(process.argv);

  if (!resource || resource === 'help') {
    showHelp();
    process.exit(0);
  }

  if (!action) {
    const acts = RESOURCES[resource];
    if (acts) {
      process.stderr.write(
        `Usage: gitlab-client ${resource} <action> [options]\n` +
        `Actions: ${acts.join(', ')}\n`
      );
    } else {
      process.stderr.write(
        `Unknown resource "${resource}". Valid resources: ${Object.keys(RESOURCES).join(', ')}\n`
      );
    }
    process.exit(1);
  }

  const handler = HANDLERS[resource];
  if (!handler) {
    process.stderr.write(
      `Unknown resource "${resource}". Valid resources: ${Object.keys(RESOURCES).join(', ')}\n`
    );
    process.exit(1);
  }

  await handler(action, positional, named);
}

main().catch((err) => {
  process.stderr.write(`Unexpected error: ${err.message}\n`);
  process.exit(1);
});
