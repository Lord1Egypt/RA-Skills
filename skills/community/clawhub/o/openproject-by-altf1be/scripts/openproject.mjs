#!/usr/bin/env node

/**
 * OpenClaw OpenProject Skill — CLI for OpenProject management via API v3.
 * Supports both cloud and self-hosted instances.
 *
 * @author Abdelkrim BOUJRAF <abdelkrim@alt-f1.be>
 * @license MIT
 * @see https://www.alt-f1.be
 */

// File I/O is used ONLY for reading user-specified attachments that the user
// explicitly passes via --file flag. No arbitrary file access.
import { readFileSync, statSync } from 'node:fs';
import { basename, resolve, posix } from 'node:path';
import { Buffer } from 'node:buffer';
import { config } from 'dotenv';
import { Command } from 'commander';

// ── Config ──────────────────────────────────────────────────────────────────

config(); // load .env

let _cfg;
function getCfg() {
  if (!_cfg) {
    // Only OpenProject-specific env vars are read — nothing else.
    const host     = process.env.OP_HOST;
    const apiToken = process.env.OP_API_TOKEN;

    const missing = [];
    if (!host)     missing.push('OP_HOST');
    if (!apiToken) missing.push('OP_API_TOKEN');

    if (missing.length) {
      console.error(`ERROR: Missing required env var(s): ${missing.join(', ')}. See .env.example`);
      process.exit(1);
    }

    _cfg = {
      host,
      apiToken,
      defaultProject: process.env.OP_DEFAULT_PROJECT || '',
      maxResults:     parseInt(process.env.OP_MAX_RESULTS || '50', 10),
      maxFileSize:    parseInt(process.env.OP_MAX_FILE_SIZE || '52428800', 10), // 50 MB
    };
  }
  return _cfg;
}
const CFG = new Proxy({}, { get: (_, prop) => getCfg()[prop] });

// ── Security helpers ────────────────────────────────────────────────────────

function safePath(p) {
  if (!p) return '';
  const normalized = posix.normalize(p).replace(/\\/g, '/');
  if (normalized.includes('..')) {
    console.error('ERROR: Path traversal detected — ".." is not allowed');
    process.exit(1);
  }
  return normalized.replace(/^\/+/, '');
}

function checkFileSize(filePath) {
  const stat = statSync(filePath);
  if (stat.size > CFG.maxFileSize) {
    console.error(`ERROR: File exceeds size limit (${(stat.size / 1048576).toFixed(1)} MB > ${(CFG.maxFileSize / 1048576).toFixed(1)} MB)`);
    process.exit(1);
  }
  return stat.size;
}

// ── HTTP client with rate-limit retry ───────────────────────────────────────

function authHeader() {
  // OpenProject uses Basic auth with 'apikey' as username
  const token = Buffer.from(`apikey:${CFG.apiToken}`).toString('base64');
  return `Basic ${token}`;
}

function baseUrl() {
  const host = CFG.host.replace(/\/+$/, '');
  const prefix = host.startsWith('http') ? host : `https://${host}`;
  return `${prefix}/api/v3`;
}

async function opFetch(path, options = {}, retries = 3) {
  const url = path.startsWith('http') ? path : `${baseUrl()}${path}`;
  const headers = {
    'Authorization': authHeader(),
    'Accept': 'application/json',
    ...options.headers,
  };

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  }

  for (let attempt = 1; attempt <= retries; attempt++) {
    const resp = await fetch(url, { ...options, headers });

    if (resp.status === 429) {
      const retryAfter = parseInt(resp.headers.get('retry-after') || '5', 10);
      const backoff = retryAfter * 1000 * attempt;
      if (attempt < retries) {
        console.error(`⏳ Rate limited — retrying in ${(backoff / 1000).toFixed(0)}s (attempt ${attempt}/${retries})`);
        await new Promise(r => setTimeout(r, backoff));
        continue;
      }
    }

    if (resp.status === 204) return null;

    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }

    if (!resp.ok) {
      const msg = json?.message
        || json?.errorIdentifier
        || json?._embedded?.errors?.map(e => e.message).join(', ')
        || body
        || resp.statusText;
      const err = new Error(msg);
      err.statusCode = resp.status;
      throw err;
    }

    return json;
  }
}

// ── HAL helpers ─────────────────────────────────────────────────────────────

function halLink(obj, rel) {
  return obj?._links?.[rel]?.title || obj?._links?.[rel]?.href?.split('/').pop() || '?';
}

function halId(obj, rel) {
  const href = obj?._links?.[rel]?.href;
  if (!href) return null;
  const match = href.match(/\/(\d+)$/);
  return match ? match[1] : null;
}

// ── Work Package commands ───────────────────────────────────────────────────

async function cmdWpList(options) {
  const project = options.project || CFG.defaultProject;
  const filters = [];

  if (project) {
    const projResp = await opFetch(`/projects/${project}`);
    filters.push({ project: { operator: '=', values: [String(projResp.id)] } });
  }
  if (options.status) {
    // Resolve status name to ID
    const statuses = await opFetch('/statuses');
    const match = statuses._embedded.elements.find(
      s => s.name.toLowerCase() === options.status.toLowerCase()
    );
    if (match) filters.push({ status: { operator: '=', values: [String(match.id)] } });
  }
  if (options.assignee === 'me') {
    filters.push({ assignee: { operator: '=', values: ['me'] } });
  } else if (options.assignee) {
    filters.push({ assignee: { operator: '=', values: [options.assignee] } });
  }
  if (options.type) {
    filters.push({ type: { operator: '=', values: [options.type] } });
  }

  const filterParam = filters.length ? `&filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
  const resp = await opFetch(`/work_packages?pageSize=${CFG.maxResults}${filterParam}&sortBy=[["updatedAt","desc"]]`);

  if (!resp._embedded.elements.length) {
    console.log('No work packages found.');
    return;
  }

  for (const wp of resp._embedded.elements) {
    const status = halLink(wp, 'status');
    const priority = halLink(wp, 'priority');
    const assignee = halLink(wp, 'assignee');
    const type = halLink(wp, 'type');
    const updated = wp.updatedAt?.substring(0, 10) || '';
    console.log(`📋  #${String(wp.id).padEnd(6)}  ${type.padEnd(10)}  ${status.padEnd(14)}  ${priority.padEnd(8)}  ${(assignee || 'Unassigned').padEnd(20)}  ${updated}  ${wp.subject}`);
  }
  console.log(`\n${resp._embedded.elements.length} of ${resp.total} work packages`);
}

async function cmdWpCreate(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set OP_DEFAULT_PROJECT)');
    process.exit(1);
  }
  if (!options.subject) {
    console.error('ERROR: --subject is required');
    process.exit(1);
  }

  const payload = {
    subject: options.subject,
    _links: {
      type: { href: null },
      priority: { href: null },
    },
  };

  if (options.description) {
    payload.description = { format: 'markdown', raw: options.description };
  }

  // Resolve type
  if (options.type) {
    const types = await opFetch(`/projects/${project}/types`);
    const match = types._embedded.elements.find(
      t => t.name.toLowerCase() === options.type.toLowerCase()
    );
    if (match) payload._links.type = { href: `/api/v3/types/${match.id}` };
  }

  // Resolve priority
  if (options.priority) {
    const priorities = await opFetch('/priorities');
    const match = priorities._embedded.elements.find(
      p => p.name.toLowerCase() === options.priority.toLowerCase()
    );
    if (match) payload._links.priority = { href: `/api/v3/priorities/${match.id}` };
  }

  // Clean null links
  if (!payload._links.type.href) delete payload._links.type;
  if (!payload._links.priority.href) delete payload._links.priority;
  if (Object.keys(payload._links).length === 0) delete payload._links;

  const result = await opFetch(`/projects/${project}/work_packages`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Created: #${result.id} — ${result.subject}`);
  console.log(`   URL: ${CFG.host}/work_packages/${result.id}`);
}

async function cmdWpRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const wp = await opFetch(`/work_packages/${options.id}`);

  console.log(`📋 #${wp.id}: ${wp.subject}`);
  console.log(`   Type:        ${halLink(wp, 'type')}`);
  console.log(`   Status:      ${halLink(wp, 'status')}`);
  console.log(`   Priority:    ${halLink(wp, 'priority')}`);
  console.log(`   Assignee:    ${halLink(wp, 'assignee')}`);
  console.log(`   Author:      ${halLink(wp, 'author')}`);
  console.log(`   Project:     ${halLink(wp, 'project')}`);
  console.log(`   Version:     ${halLink(wp, 'version')}`);
  console.log(`   Category:    ${halLink(wp, 'category')}`);
  console.log(`   Created:     ${wp.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${wp.updatedAt?.substring(0, 10) || '?'}`);
  console.log(`   % Done:      ${wp.percentageDone ?? '?'}%`);
  console.log(`   Estimated:   ${wp.estimatedTime || '?'}`);
  console.log(`   URL:         ${CFG.host}/work_packages/${wp.id}`);

  if (wp.description?.raw) {
    console.log(`\n📝 Description:\n${wp.description.raw}`);
  }
}

async function cmdWpUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  // Get current work package for lockVersion
  const current = await opFetch(`/work_packages/${options.id}`);
  const payload = { lockVersion: current.lockVersion, _links: {} };

  if (options.subject) payload.subject = options.subject;
  if (options.description) payload.description = { format: 'markdown', raw: options.description };
  if (options.percentDone !== undefined) payload.percentageDone = parseInt(options.percentDone, 10);

  if (options.status) {
    const statuses = await opFetch('/statuses');
    const match = statuses._embedded.elements.find(
      s => s.name.toLowerCase() === options.status.toLowerCase()
    );
    if (match) payload._links.status = { href: `/api/v3/statuses/${match.id}` };
  }

  if (options.priority) {
    const priorities = await opFetch('/priorities');
    const match = priorities._embedded.elements.find(
      p => p.name.toLowerCase() === options.priority.toLowerCase()
    );
    if (match) payload._links.priority = { href: `/api/v3/priorities/${match.id}` };
  }

  if (options.type) {
    const projectId = halId(current, 'project');
    if (projectId) {
      const types = await opFetch(`/projects/${projectId}/types`);
      const match = types._embedded.elements.find(
        t => t.name.toLowerCase() === options.type.toLowerCase()
      );
      if (match) payload._links.type = { href: `/api/v3/types/${match.id}` };
    }
  }

  if (Object.keys(payload._links).length === 0) delete payload._links;

  await opFetch(`/work_packages/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Updated: #${options.id}`);
}

async function cmdWpDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: openproject wp-delete --id 42 --confirm');
    process.exit(1);
  }

  await opFetch(`/work_packages/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Deleted: #${options.id}`);
}

// ── Project commands ────────────────────────────────────────────────────────

async function cmdProjectList() {
  const resp = await opFetch(`/projects?pageSize=${CFG.maxResults}`);

  if (!resp._embedded.elements.length) {
    console.log('No projects found.');
    return;
  }

  for (const p of resp._embedded.elements) {
    const status = p.active ? '✅' : '⏸️';
    const updated = p.updatedAt?.substring(0, 10) || '';
    console.log(`${status}  ${p.identifier.padEnd(25)}  ${p.name.padEnd(30)}  ${updated}`);
  }
  console.log(`\n${resp._embedded.elements.length} project(s)`);
}

async function cmdProjectRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required (project identifier or numeric ID)');
    process.exit(1);
  }

  const p = await opFetch(`/projects/${options.id}`);

  console.log(`📂 ${p.name}`);
  console.log(`   Identifier:  ${p.identifier}`);
  console.log(`   ID:          ${p.id}`);
  console.log(`   Active:      ${p.active ? 'Yes' : 'No'}`);
  console.log(`   Public:      ${p.public ? 'Yes' : 'No'}`);
  console.log(`   Created:     ${p.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${p.updatedAt?.substring(0, 10) || '?'}`);
  console.log(`   URL:         ${CFG.host}/projects/${p.identifier}`);

  if (p.description?.raw) {
    console.log(`\n📝 Description:\n${p.description.raw}`);
  }
}

async function cmdProjectCreate(options) {
  if (!options.name) {
    console.error('ERROR: --name is required');
    process.exit(1);
  }

  const payload = {
    name: options.name,
  };
  if (options.identifier) payload.identifier = options.identifier;
  if (options.description) payload.description = { format: 'markdown', raw: options.description };
  if (options.public !== undefined) payload.public = options.public === 'true';

  const result = await opFetch('/projects', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Created project: ${result.name}`);
  console.log(`   Identifier: ${result.identifier}`);
  console.log(`   ID: ${result.id}`);
  console.log(`   URL: ${CFG.host}/projects/${result.identifier}`);
}

// ── Comment (Activity) commands ─────────────────────────────────────────────

async function cmdCommentList(options) {
  if (!options.wpId) {
    console.error('ERROR: --wp-id is required');
    process.exit(1);
  }

  const resp = await opFetch(`/work_packages/${options.wpId}/activities`);

  const comments = resp._embedded.elements.filter(a => a.comment?.raw);
  if (!comments.length) {
    console.log('No comments.');
    return;
  }

  for (const a of comments) {
    const author = halLink(a, 'user');
    const created = a.createdAt?.substring(0, 16).replace('T', ' ') || '?';
    const body = a.comment.raw;
    console.log(`💬 #${a.id}  ${author}  ${created}`);
    console.log(`   ${body.substring(0, 200)}${body.length > 200 ? '...' : ''}`);
    console.log('');
  }
  console.log(`${comments.length} comment(s)`);
}

async function cmdCommentAdd(options) {
  if (!options.wpId || !options.body) {
    console.error('ERROR: --wp-id and --body are required');
    process.exit(1);
  }

  const result = await opFetch(`/work_packages/${options.wpId}/activities`, {
    method: 'POST',
    body: JSON.stringify({
      comment: { format: 'markdown', raw: options.body },
    }),
  });

  console.log(`✅ Comment added to #${options.wpId}`);
  console.log(`   ID: ${result.id}`);
}

// ── Attachment commands ─────────────────────────────────────────────────────

async function cmdAttachmentList(options) {
  if (!options.wpId) {
    console.error('ERROR: --wp-id is required');
    process.exit(1);
  }

  const resp = await opFetch(`/work_packages/${options.wpId}/attachments`);

  if (!resp._embedded.elements.length) {
    console.log('No attachments.');
    return;
  }

  for (const a of resp._embedded.elements) {
    const size = `${(a.fileSize / 1024).toFixed(1)} KB`;
    const created = a.createdAt?.substring(0, 10) || '';
    const author = halLink(a, 'author');
    console.log(`📎  #${String(a.id).padEnd(8)}  ${a.fileName.padEnd(30)}  ${size.padStart(12)}  ${created}  ${author}`);
  }
  console.log(`\n${resp._embedded.elements.length} attachment(s)`);
}

async function cmdAttachmentAdd(options) {
  if (!options.wpId || !options.file) {
    console.error('ERROR: --wp-id and --file are required');
    process.exit(1);
  }

  const filePath = resolve(safePath(options.file) || options.file);
  checkFileSize(filePath);

  const fileContent = readFileSync(filePath);
  const fileName = basename(filePath);

  const form = new FormData();
  form.append('file', new Blob([fileContent]), fileName);
  form.append('metadata', JSON.stringify({ fileName, description: { format: 'plain', raw: '' } }));

  const url = `${baseUrl()}/work_packages/${options.wpId}/attachments`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Authorization': authHeader() },
    body: form,
  });

  if (!resp.ok) {
    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }
    const msg = json?.message || json?.errorIdentifier || body;
    console.error(`ERROR (${resp.status}): ${msg}`);
    process.exit(1);
  }

  const result = await resp.json();
  console.log(`✅ Attachment uploaded to #${options.wpId}`);
  console.log(`   File: ${result.fileName}`);
  console.log(`   Size: ${(result.fileSize / 1024).toFixed(1)} KB`);
  console.log(`   ID: ${result.id}`);
}

async function cmdAttachmentDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: openproject attachment-delete --id 10 --confirm');
    process.exit(1);
  }

  await opFetch(`/attachments/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Attachment #${options.id} deleted`);
}

// ── Time Entry commands ─────────────────────────────────────────────────────

async function cmdTimeList(options) {
  const filters = [];
  const project = options.project || CFG.defaultProject;

  if (project) {
    const projResp = await opFetch(`/projects/${project}`);
    filters.push({ project: { operator: '=', values: [String(projResp.id)] } });
  }
  if (options.wpId) {
    filters.push({ work_package: { operator: '=', values: [options.wpId] } });
  }

  const filterParam = filters.length ? `&filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
  const resp = await opFetch(`/time_entries?pageSize=${CFG.maxResults}${filterParam}`);

  if (!resp._embedded.elements.length) {
    console.log('No time entries found.');
    return;
  }

  for (const t of resp._embedded.elements) {
    const user = halLink(t, 'user');
    const wpId = halId(t, 'workPackage') || '?';
    const hours = t.hours ? t.hours.replace('PT', '').replace('H', 'h ').replace('M', 'm').trim() : '?';
    const date = t.spentOn || '?';
    const comment = t.comment?.raw || '';
    console.log(`⏱️  #${String(t.id).padEnd(6)}  WP#${wpId.padEnd(6)}  ${hours.padEnd(8)}  ${date}  ${user.padEnd(20)}  ${comment.substring(0, 40)}`);
  }
  console.log(`\n${resp._embedded.elements.length} time entries`);
}

async function cmdTimeCreate(options) {
  if (!options.wpId || !options.hours) {
    console.error('ERROR: --wp-id and --hours are required');
    process.exit(1);
  }

  const hours = parseFloat(options.hours);
  const isoDuration = `PT${Math.floor(hours)}H${Math.round((hours % 1) * 60)}M`;

  const payload = {
    hours: isoDuration,
    comment: options.comment ? { format: 'plain', raw: options.comment } : undefined,
    spentOn: options.date || new Date().toISOString().substring(0, 10),
    _links: {
      workPackage: { href: `/api/v3/work_packages/${options.wpId}` },
    },
  };

  if (options.activityId) {
    payload._links.activity = { href: `/api/v3/time_entries/activities/${options.activityId}` };
  }

  const result = await opFetch('/time_entries', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Time logged: ${options.hours}h on WP#${options.wpId}`);
  console.log(`   ID: ${result.id}`);
}

async function cmdTimeUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const payload = {};
  if (options.hours) {
    const hours = parseFloat(options.hours);
    payload.hours = `PT${Math.floor(hours)}H${Math.round((hours % 1) * 60)}M`;
  }
  if (options.comment) payload.comment = { format: 'plain', raw: options.comment };
  if (options.date) payload.spentOn = options.date;

  await opFetch(`/time_entries/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Time entry #${options.id} updated`);
}

async function cmdTimeDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: openproject time-delete --id 5 --confirm');
    process.exit(1);
  }

  await opFetch(`/time_entries/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Time entry #${options.id} deleted`);
}

// ── Reference Data commands ─────────────────────────────────────────────────

async function cmdStatusList() {
  const resp = await opFetch('/statuses');
  console.log('Available statuses:\n');
  for (const s of resp._embedded.elements) {
    const closed = s.isClosed ? '🔒' : '🔓';
    console.log(`  ${closed}  ID: ${String(s.id).padEnd(4)}  ${s.name}`);
  }
}

async function cmdTypeList() {
  const resp = await opFetch('/types');
  console.log('Available types:\n');
  for (const t of resp._embedded.elements) {
    console.log(`  🏷️  ID: ${String(t.id).padEnd(4)}  ${t.name}`);
  }
}

async function cmdPriorityList() {
  const resp = await opFetch('/priorities');
  console.log('Available priorities:\n');
  for (const p of resp._embedded.elements) {
    const def = p.isDefault ? ' (default)' : '';
    console.log(`  ⚡  ID: ${String(p.id).padEnd(4)}  ${p.name}${def}`);
  }
}

async function cmdMemberList(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set OP_DEFAULT_PROJECT)');
    process.exit(1);
  }

  const resp = await opFetch(`/projects/${project}/memberships?pageSize=${CFG.maxResults}`);

  if (!resp._embedded.elements.length) {
    console.log('No members found.');
    return;
  }

  for (const m of resp._embedded.elements) {
    const user = halLink(m, 'principal');
    const roles = m._embedded?.roles?.map(r => r.name).join(', ') || halLink(m, 'roles');
    console.log(`  👤  ${user.padEnd(25)}  ${roles}`);
  }
  console.log(`\n${resp._embedded.elements.length} member(s)`);
}

async function cmdVersionList(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set OP_DEFAULT_PROJECT)');
    process.exit(1);
  }

  const resp = await opFetch(`/projects/${project}/versions`);

  if (!resp._embedded.elements.length) {
    console.log('No versions found.');
    return;
  }

  for (const v of resp._embedded.elements) {
    const status = v.status || '?';
    const date = v.endDate || 'no date';
    console.log(`  🏁  ID: ${String(v.id).padEnd(4)}  ${v.name.padEnd(25)}  ${status.padEnd(10)}  ${date}`);
  }
  console.log(`\n${resp._embedded.elements.length} version(s)`);
}

async function cmdCategoryList(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set OP_DEFAULT_PROJECT)');
    process.exit(1);
  }

  const resp = await opFetch(`/projects/${project}/categories`);

  if (!resp._embedded.elements.length) {
    console.log('No categories found.');
    return;
  }

  for (const c of resp._embedded.elements) {
    console.log(`  📁  ID: ${String(c.id).padEnd(4)}  ${c.name}`);
  }
  console.log(`\n${resp._embedded.elements.length} category/categories`);
}

// ── Document commands ────────────────────────────────────────────────────────

async function cmdDocumentList() {
  const resp = await opFetch(`/documents?pageSize=${CFG.maxResults}`);
  if (!resp._embedded.elements.length) { console.log('No documents found.'); return; }
  for (const d of resp._embedded.elements) {
    const project = halLink(d, 'project');
    const created = d.createdAt?.substring(0, 10) || '?';
    console.log(`  📄  #${String(d.id).padEnd(6)}  ${(d.title || '?').padEnd(30)}  ${project}  ${created}`);
  }
  console.log(`\n${resp._embedded.elements.length} document(s)`);
}

async function cmdDocumentRead(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const d = await opFetch(`/documents/${options.id}`);
  console.log(`📄 Document #${d.id}: ${d.title || '?'}`);
  console.log(`   Project:     ${halLink(d, 'project')}`);
  console.log(`   Created:     ${d.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${d.updatedAt?.substring(0, 10) || '?'}`);
  if (d.description?.raw) console.log(`\n📝 Description:\n${d.description.raw}`);
}

async function cmdDocumentUpdate(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const payload = {};
  if (options.title) payload.title = options.title;
  if (options.description) payload.description = { format: 'markdown', raw: options.description };
  await opFetch(`/documents/${options.id}`, { method: 'PATCH', body: JSON.stringify(payload) });
  console.log(`✅ Document #${options.id} updated`);
}

// ── Revision commands ────────────────────────────────────────────────────────

async function cmdRevisionRead(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const r = await opFetch(`/revisions/${options.id}`);
  console.log(`🔀 Revision #${r.id}`);
  console.log(`   Identifier:  ${r.identifier || '?'}`);
  if (r.message?.raw) console.log(`   Message:     ${r.message.raw}`);
  console.log(`   Author:      ${halLink(r, 'author')}`);
  console.log(`   Created:     ${r.createdAt?.substring(0, 10) || '?'}`);
}

async function cmdRevisionListByWp(options) {
  if (!options.wpId) { console.error('ERROR: --wp-id is required'); process.exit(1); }
  const resp = await opFetch(`/work_packages/${options.wpId}/revisions`);
  if (!resp._embedded.elements.length) { console.log('No revisions found.'); return; }
  for (const r of resp._embedded.elements) {
    const msg = r.message?.raw?.substring(0, 60) || '';
    console.log(`  🔀  #${String(r.id).padEnd(6)}  ${(r.identifier || '?').padEnd(12)}  ${msg}`);
  }
  console.log(`\n${resp._embedded.elements.length} revision(s)`);
}

// ── Capability & Action commands ─────────────────────────────────────────────

async function cmdCapabilityList(options) {
  const filters = [];
  if (options.context) filters.push({ context: { operator: '=', values: [options.context] } });
  if (options.action) filters.push({ action: { operator: '=', values: [options.action] } });
  if (options.principal) filters.push({ principal: { operator: '=', values: [options.principal] } });
  const filterParam = filters.length ? `&filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
  const resp = await opFetch(`/capabilities?pageSize=${CFG.maxResults}${filterParam}`);
  if (!resp._embedded.elements.length) { console.log('No capabilities found.'); return; }
  for (const c of resp._embedded.elements) {
    const action = halLink(c, 'action') || '?';
    const context = halLink(c, 'context') || 'global';
    const principal = halLink(c, 'principal') || '?';
    console.log(`  🔑  ${String(c.id).padEnd(30)}  ${action.padEnd(25)}  ${context.padEnd(20)}  ${principal}`);
  }
  console.log(`\n${resp._embedded.elements.length} of ${resp.total} capability/capabilities`);
}

async function cmdCapabilityGlobal() {
  const resp = await opFetch('/capabilities/context/global');
  if (!resp._embedded.elements.length) { console.log('No global capabilities.'); return; }
  for (const c of resp._embedded.elements) {
    const action = halLink(c, 'action') || '?';
    console.log(`  🔑  ${action}`);
  }
  console.log(`\n${resp._embedded.elements.length} global capability/capabilities`);
}

async function cmdActionList() {
  const resp = await opFetch('/actions');
  if (!resp._embedded.elements.length) { console.log('No actions found.'); return; }
  for (const a of resp._embedded.elements) {
    console.log(`  ⚡  ${a.id}`);
  }
  console.log(`\n${resp._embedded.elements.length} action(s)`);
}

async function cmdActionRead(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const a = await opFetch(`/actions/${options.id}`);
  console.log(`⚡ Action: ${a.id}`);
}

// ── My Preferences commands ──────────────────────────────────────────────────

async function cmdMyPreferencesRead() {
  const p = await opFetch('/my_preferences');
  console.log('⚙️ My Preferences');
  const skip = ['_type', '_links'];
  for (const [key, val] of Object.entries(p)) {
    if (skip.includes(key)) continue;
    const display = typeof val === 'object' ? JSON.stringify(val) : val;
    console.log(`   ${key}: ${display}`);
  }
}

async function cmdMyPreferencesUpdate(options) {
  const payload = {};
  if (options.timeZone) payload.timeZone = options.timeZone;
  if (options.autoHidePopups !== undefined) payload.autoHidePopups = options.autoHidePopups === 'true';
  if (options.commentOrder) payload.commentSortDescending = options.commentOrder === 'desc';
  if (options.warnOnLeavingUnsaved !== undefined) payload.warnOnLeavingUnsaved = options.warnOnLeavingUnsaved === 'true';
  await opFetch('/my_preferences', { method: 'PATCH', body: JSON.stringify(payload) });
  console.log('✅ Preferences updated');
}

// ── Render commands ──────────────────────────────────────────────────────────

async function cmdRenderMarkdown(options) {
  if (!options.text) { console.error('ERROR: --text is required'); process.exit(1); }
  const result = await opFetch('/render/markdown', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: options.text,
  });
  console.log(typeof result === 'string' ? result : result?.html || JSON.stringify(result));
}

async function cmdRenderPlain(options) {
  if (!options.text) { console.error('ERROR: --text is required'); process.exit(1); }
  const result = await opFetch('/render/plain', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: options.text,
  });
  console.log(typeof result === 'string' ? result : result?.html || JSON.stringify(result));
}

// ── Post commands ────────────────────────────────────────────────────────────

async function cmdPostRead(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const p = await opFetch(`/posts/${options.id}`);
  console.log(`📝 Post #${p.id}: ${p.subject || '?'}`);
  console.log(`   Author:      ${halLink(p, 'author')}`);
  console.log(`   Project:     ${halLink(p, 'project')}`);
  console.log(`   Created:     ${p.createdAt?.substring(0, 10) || '?'}`);
  if (p.description?.raw) console.log(`\n${p.description.raw}`);
}

async function cmdPostAttachmentList(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const resp = await opFetch(`/posts/${options.id}/attachments`);
  if (!resp._embedded.elements.length) { console.log('No attachments.'); return; }
  for (const a of resp._embedded.elements) {
    const size = `${(a.fileSize / 1024).toFixed(1)} KB`;
    console.log(`📎  #${String(a.id).padEnd(8)}  ${a.fileName.padEnd(30)}  ${size.padStart(12)}`);
  }
  console.log(`\n${resp._embedded.elements.length} attachment(s)`);
}

// ── Reminder commands ────────────────────────────────────────────────────────

async function cmdReminderList() {
  const resp = await opFetch(`/reminders?pageSize=${CFG.maxResults}`);
  if (!resp._embedded.elements.length) { console.log('No reminders found.'); return; }
  for (const r of resp._embedded.elements) {
    const wp = halLink(r, 'workPackage') || '?';
    const note = r.note || '';
    console.log(`  ⏰  #${String(r.id).padEnd(6)}  WP: ${wp.padEnd(20)}  ${r.remindAt || '?'}  ${note.substring(0, 40)}`);
  }
  console.log(`\n${resp._embedded.elements.length} reminder(s)`);
}

async function cmdReminderCreate(options) {
  if (!options.wpId || !options.remindAt) {
    console.error('ERROR: --wp-id and --remind-at are required');
    process.exit(1);
  }
  const payload = {
    remindAt: options.remindAt,
    note: options.note || null,
  };
  const result = await opFetch(`/work_packages/${options.wpId}/reminders`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  console.log(`✅ Reminder created for WP#${options.wpId}`);
  console.log(`   ID: ${result.id}`);
  console.log(`   Remind at: ${result.remindAt}`);
}

async function cmdReminderUpdate(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const payload = {};
  if (options.remindAt) payload.remindAt = options.remindAt;
  if (options.note !== undefined) payload.note = options.note || null;
  await opFetch(`/reminders/${options.id}`, { method: 'PATCH', body: JSON.stringify(payload) });
  console.log(`✅ Reminder #${options.id} updated`);
}

async function cmdReminderDelete(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag'); process.exit(1); }
  await opFetch(`/reminders/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Reminder #${options.id} deleted`);
}

// ── Project Status commands ──────────────────────────────────────────────────

async function cmdProjectStatusRead(options) {
  if (!options.id) { console.error('ERROR: --id is required'); process.exit(1); }
  const s = await opFetch(`/project_statuses/${options.id}`);
  console.log(`🚦 Project Status: ${s.name || s.id}`);
  if (s.color) console.log(`   Color: ${s.color}`);
}

// ── Project Phase commands (Enterprise) ──────────────────────────────────────

async function cmdProjectPhaseDefinitionList() {
  const resp = await opFetch('/project_phase_definitions');

  if (!resp._embedded.elements.length) {
    console.log('No project phase definitions found.');
    return;
  }

  for (const d of resp._embedded.elements) {
    const color = d.color || '';
    console.log(`  🔄  ID: ${String(d.id).padEnd(6)}  ${(d.name || '?').padEnd(25)}  ${color}`);
  }
  console.log(`\n${resp._embedded.elements.length} phase definition(s)`);
}

async function cmdProjectPhaseDefinitionRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const d = await opFetch(`/project_phase_definitions/${options.id}`);

  console.log(`🔄 Phase Definition #${d.id}: ${d.name || '?'}`);
  if (d.color) console.log(`   Color:       ${d.color}`);
  if (d.position !== undefined) console.log(`   Position:    ${d.position}`);
}

async function cmdProjectPhaseRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const p = await opFetch(`/project_phases/${options.id}`);

  console.log(`🔄 Project Phase #${p.id}`);
  console.log(`   Definition:  ${halLink(p, 'phaseDefinition') || '?'}`);
  console.log(`   Project:     ${halLink(p, 'project') || '?'}`);
  if (p.startDate) console.log(`   Start:       ${p.startDate}`);
  if (p.endDate) console.log(`   End:         ${p.endDate}`);
  console.log(`   Created:     ${p.createdAt?.substring(0, 10) || '?'}`);
}

// ── Portfolio commands (Enterprise) ──────────────────────────────────────────

async function cmdPortfolioList() {
  const resp = await opFetch(`/portfolios?pageSize=${CFG.maxResults}`);

  if (!resp._embedded.elements.length) {
    console.log('No portfolios found.');
    return;
  }

  for (const p of resp._embedded.elements) {
    console.log(`  📊  #${String(p.id).padEnd(6)}  ${p.name || p.title || '?'}`);
  }
  console.log(`\n${resp._embedded.elements.length} portfolio(s)`);
}

async function cmdPortfolioRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const p = await opFetch(`/portfolios/${options.id}`);

  console.log(`📊 Portfolio #${p.id}: ${p.name || p.title || '?'}`);
  if (p.description?.raw) console.log(`   Description: ${p.description.raw}`);
  console.log(`   Created:     ${p.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${p.updatedAt?.substring(0, 10) || '?'}`);
}

async function cmdPortfolioUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const payload = {};
  if (options.name) payload.name = options.name;
  if (options.description) payload.description = { format: 'markdown', raw: options.description };

  await opFetch(`/portfolios/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Portfolio #${options.id} updated`);
}

async function cmdPortfolioDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }

  await opFetch(`/portfolios/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Portfolio #${options.id} deleted`);
}

// ── Program commands (Enterprise) ───────────────────────────────────────────

async function cmdProgramList() {
  const resp = await opFetch(`/programs?pageSize=${CFG.maxResults}`);

  if (!resp._embedded.elements.length) {
    console.log('No programs found.');
    return;
  }

  for (const p of resp._embedded.elements) {
    console.log(`  🏗️  #${String(p.id).padEnd(6)}  ${p.name || p.title || '?'}`);
  }
  console.log(`\n${resp._embedded.elements.length} program(s)`);
}

async function cmdProgramRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const p = await opFetch(`/programs/${options.id}`);

  console.log(`🏗️ Program #${p.id}: ${p.name || p.title || '?'}`);
  if (p.description?.raw) console.log(`   Description: ${p.description.raw}`);
  console.log(`   Created:     ${p.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${p.updatedAt?.substring(0, 10) || '?'}`);
}

async function cmdProgramUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const payload = {};
  if (options.name) payload.name = options.name;
  if (options.description) payload.description = { format: 'markdown', raw: options.description };

  await opFetch(`/programs/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Program #${options.id} updated`);
}

async function cmdProgramDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }

  await opFetch(`/programs/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Program #${options.id} deleted`);
}

// ── Placeholder User commands (Enterprise) ──────────────────────────────────

async function cmdPlaceholderUserList() {
  const resp = await opFetch(`/placeholder_users?pageSize=${CFG.maxResults}`);

  if (!resp._embedded.elements.length) {
    console.log('No placeholder users found.');
    return;
  }

  for (const u of resp._embedded.elements) {
    const status = u.status || '?';
    console.log(`  👻  ID: ${String(u.id).padEnd(6)}  ${u.name.padEnd(25)}  [${status}]`);
  }
  console.log(`\n${resp._embedded.elements.length} placeholder user(s)`);
}

async function cmdPlaceholderUserRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const u = await opFetch(`/placeholder_users/${options.id}`);

  console.log(`👻 Placeholder User #${u.id}: ${u.name}`);
  console.log(`   Status:      ${u.status || '?'}`);
  console.log(`   Created:     ${u.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${u.updatedAt?.substring(0, 10) || '?'}`);
}

async function cmdPlaceholderUserCreate(options) {
  if (!options.name) {
    console.error('ERROR: --name is required');
    process.exit(1);
  }

  const result = await opFetch('/placeholder_users', {
    method: 'POST',
    body: JSON.stringify({ name: options.name }),
  });

  console.log(`✅ Placeholder user created: ${result.name}`);
  console.log(`   ID: ${result.id}`);
}

async function cmdPlaceholderUserUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const payload = {};
  if (options.name) payload.name = options.name;

  await opFetch(`/placeholder_users/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Placeholder user #${options.id} updated`);
}

async function cmdPlaceholderUserDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }

  await opFetch(`/placeholder_users/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Placeholder user #${options.id} deleted`);
}

// ── Budget commands (Enterprise) ─────────────────────────────────────────────

async function cmdBudgetRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const b = await opFetch(`/budgets/${options.id}`);

  console.log(`💰 Budget #${b.id}: ${b.subject || '?'}`);
  console.log(`   Project:     ${halLink(b, 'project')}`);
  if (b.spent !== undefined) console.log(`   Spent:       ${b.spent}`);
  if (b.laborBudget !== undefined) console.log(`   Labor:       ${b.laborBudget}`);
  if (b.materialBudget !== undefined) console.log(`   Material:    ${b.materialBudget}`);
  if (b.overallCosts !== undefined) console.log(`   Overall:     ${b.overallCosts}`);
  console.log(`   Created:     ${b.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${b.updatedAt?.substring(0, 10) || '?'}`);

  if (b.description?.raw) {
    console.log(`\n📝 Description:\n${b.description.raw}`);
  }
}

async function cmdBudgetList(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set OP_DEFAULT_PROJECT)');
    process.exit(1);
  }

  const resp = await opFetch(`/projects/${project}/budgets`);

  if (!resp._embedded.elements.length) {
    console.log('No budgets found.');
    return;
  }

  for (const b of resp._embedded.elements) {
    const spent = b.spent !== undefined ? `spent: ${b.spent}` : '';
    console.log(`  💰  #${String(b.id).padEnd(6)}  ${(b.subject || '?').padEnd(30)}  ${spent}`);
  }
  console.log(`\n${resp._embedded.elements.length} budget(s)`);
}

// ── Meeting commands (Enterprise) ────────────────────────────────────────────

async function cmdMeetingRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const m = await opFetch(`/meetings/${options.id}`);

  console.log(`📅 Meeting #${m.id}: ${m.title || '?'}`);
  console.log(`   Type:        ${m._type || '?'}`);
  console.log(`   Project:     ${halLink(m, 'project')}`);
  console.log(`   Author:      ${halLink(m, 'author')}`);
  if (m.startTime) console.log(`   Start:       ${m.startTime}`);
  if (m.duration) console.log(`   Duration:    ${m.duration}`);
  if (m.location) console.log(`   Location:    ${m.location}`);
  console.log(`   Created:     ${m.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${m.updatedAt?.substring(0, 10) || '?'}`);
}

async function cmdMeetingAttachmentList(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const resp = await opFetch(`/meetings/${options.id}/attachments`);

  if (!resp._embedded.elements.length) {
    console.log('No attachments on this meeting.');
    return;
  }

  for (const a of resp._embedded.elements) {
    const size = `${(a.fileSize / 1024).toFixed(1)} KB`;
    const created = a.createdAt?.substring(0, 10) || '';
    const author = halLink(a, 'author');
    console.log(`📎  #${String(a.id).padEnd(8)}  ${a.fileName.padEnd(30)}  ${size.padStart(12)}  ${created}  ${author}`);
  }
  console.log(`\n${resp._embedded.elements.length} attachment(s)`);
}

async function cmdMeetingAttachmentAdd(options) {
  if (!options.id || !options.file) {
    console.error('ERROR: --id and --file are required');
    process.exit(1);
  }

  const filePath = resolve(safePath(options.file) || options.file);
  checkFileSize(filePath);

  const fileContent = readFileSync(filePath);
  const fileName = basename(filePath);

  const form = new FormData();
  form.append('file', new Blob([fileContent]), fileName);
  form.append('metadata', JSON.stringify({ fileName, description: { format: 'plain', raw: '' } }));

  const url = `${baseUrl()}/meetings/${options.id}/attachments`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Authorization': authHeader() },
    body: form,
  });

  if (!resp.ok) {
    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }
    const msg = json?.message || json?.errorIdentifier || body;
    console.error(`ERROR (${resp.status}): ${msg}`);
    process.exit(1);
  }

  const result = await resp.json();
  console.log(`✅ Attachment uploaded to meeting #${options.id}`);
  console.log(`   File: ${result.fileName}`);
  console.log(`   ID: ${result.id}`);
}

// ── Days commands ────────────────────────────────────────────────────────────

async function cmdDayRead(options) {
  if (!options.date) {
    console.error('ERROR: --date is required (YYYY-MM-DD)');
    process.exit(1);
  }

  const d = await opFetch(`/days/${options.date}`);

  const working = d.working ? '✅ Working day' : '❌ Non-working day';
  console.log(`📅 ${d.date}: ${working}`);
  if (d.name) console.log(`   Name: ${d.name}`);
}

async function cmdDaysList(options) {
  const from = options.from || new Date().toISOString().substring(0, 10);
  const to = options.to;

  let url = `/days?filters=[{"date":{"operator":">d","values":["${from}"`;
  if (to) url += `,"${to}"`;
  url += ']}}]&pageSize=31';

  const resp = await opFetch(url);

  if (!resp._embedded.elements.length) {
    console.log('No days found in range.');
    return;
  }

  for (const d of resp._embedded.elements) {
    const working = d.working ? '✅' : '❌';
    const name = d.name ? `  (${d.name})` : '';
    console.log(`  ${working}  ${d.date}${name}`);
  }
  console.log(`\n${resp._embedded.elements.length} day(s)`);
}

async function cmdNonWorkingDaysList() {
  const resp = await opFetch(`/days/non_working?pageSize=${CFG.maxResults}`);

  if (!resp._embedded.elements.length) {
    console.log('No non-working days configured.');
    return;
  }

  for (const d of resp._embedded.elements) {
    const name = d.name || '';
    console.log(`  🚫  ${d.date}  ${name}`);
  }
  console.log(`\n${resp._embedded.elements.length} non-working day(s)`);
}

async function cmdNonWorkingDayRead(options) {
  if (!options.date) {
    console.error('ERROR: --date is required (YYYY-MM-DD)');
    process.exit(1);
  }

  const d = await opFetch(`/days/non_working/${options.date}`);

  console.log(`🚫 Non-Working Day: ${d.date}`);
  if (d.name) console.log(`   Name: ${d.name}`);
}

async function cmdWeekDaysList() {
  const resp = await opFetch('/days/week');

  for (const d of resp._embedded.elements) {
    const working = d.working ? '✅' : '❌';
    const dayNames = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const name = dayNames[d.day] || `Day ${d.day}`;
    console.log(`  ${working}  ${name} (${d.day})`);
  }
}

async function cmdWeekDayRead(options) {
  if (!options.day) {
    console.error('ERROR: --day is required (1=Monday ... 7=Sunday)');
    process.exit(1);
  }

  const d = await opFetch(`/days/week/${options.day}`);

  const working = d.working ? '✅ Working day' : '❌ Non-working day';
  const dayNames = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const name = dayNames[d.day] || `Day ${d.day}`;
  console.log(`📅 ${name}: ${working}`);
}

// ── Configuration commands ───────────────────────────────────────────────────

async function cmdConfigRead() {
  const cfg = await opFetch('/configuration');

  console.log('⚙️ Instance Configuration');
  if (cfg.maximumAttachmentFileSize) console.log(`   Max attachment size: ${cfg.maximumAttachmentFileSize} bytes`);
  if (cfg.perPageOptions) console.log(`   Per-page options:   ${JSON.stringify(cfg.perPageOptions)}`);
  if (cfg.dateFormat) console.log(`   Date format:        ${cfg.dateFormat}`);
  if (cfg.timeFormat) console.log(`   Time format:        ${cfg.timeFormat}`);
  if (cfg.startOfWeek !== undefined) console.log(`   Start of week:      ${cfg.startOfWeek}`);
  if (cfg.activeFeatureFlags?.length) console.log(`   Feature flags:      ${cfg.activeFeatureFlags.join(', ')}`);

  // Print remaining keys
  const shown = ['_type', '_links', 'maximumAttachmentFileSize', 'perPageOptions', 'dateFormat', 'timeFormat', 'startOfWeek', 'activeFeatureFlags'];
  const remaining = Object.entries(cfg).filter(([k]) => !shown.includes(k));
  for (const [key, val] of remaining) {
    const display = typeof val === 'object' ? JSON.stringify(val) : val;
    console.log(`   ${key}: ${display}`);
  }
}

async function cmdProjectConfigRead(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set OP_DEFAULT_PROJECT)');
    process.exit(1);
  }

  const cfg = await opFetch(`/projects/${project}/configuration`);

  console.log(`⚙️ Project Configuration: ${project}`);
  const skip = ['_type', '_links'];
  for (const [key, val] of Object.entries(cfg)) {
    if (skip.includes(key)) continue;
    const display = typeof val === 'object' ? JSON.stringify(val) : val;
    console.log(`   ${key}: ${display}`);
  }
}

// ── OAuth commands ───────────────────────────────────────────────────────────

async function cmdOauthAppRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const app = await opFetch(`/oauth_applications/${options.id}`);

  console.log(`🔐 OAuth Application #${app.id}`);
  console.log(`   Name:            ${app.name || '?'}`);
  console.log(`   Client ID:       ${app.clientId || '?'}`);
  console.log(`   Confidential:    ${app.confidential ?? '?'}`);
  if (app.redirectUri) console.log(`   Redirect URI:    ${app.redirectUri}`);
  console.log(`   Created:         ${app.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:         ${app.updatedAt?.substring(0, 10) || '?'}`);
}

async function cmdOauthCredentialsRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const cred = await opFetch(`/oauth_client_credentials/${options.id}`);

  console.log(`🔑 OAuth Client Credentials #${cred.id}`);
  console.log(`   Client ID:       ${cred.clientId || '?'}`);
  console.log(`   Confidential:    ${cred.confidential ?? '?'}`);
  console.log(`   Created:         ${cred.createdAt?.substring(0, 10) || '?'}`);
}

// ── Help Text commands ───────────────────────────────────────────────────────

async function cmdHelpTextList() {
  const resp = await opFetch('/help_texts');

  if (!resp._embedded.elements.length) {
    console.log('No help texts found.');
    return;
  }

  for (const h of resp._embedded.elements) {
    const attr = h.attribute || '?';
    const text = h.helpText?.raw?.substring(0, 80) || '';
    console.log(`  ❓  ID: ${String(h.id).padEnd(6)}  ${attr.padEnd(25)}  ${text}${text.length >= 80 ? '...' : ''}`);
  }
  console.log(`\n${resp._embedded.elements.length} help text(s)`);
}

async function cmdHelpTextRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const h = await opFetch(`/help_texts/${options.id}`);

  console.log(`❓ Help Text #${h.id}`);
  console.log(`   Attribute:   ${h.attribute || '?'}`);
  console.log(`   Scope:       ${h.scope || '?'}`);

  if (h.helpText?.raw) {
    console.log(`\n📝 Text:\n${h.helpText.raw}`);
  }
}

// ── Custom Field commands ────────────────────────────────────────────────────

async function cmdCustomFieldItems(options) {
  if (!options.id) {
    console.error('ERROR: --id is required (custom field ID)');
    process.exit(1);
  }

  const resp = await opFetch(`/custom_fields/${options.id}/items`);

  if (!resp._embedded?.elements?.length) {
    console.log('No items found for this custom field.');
    return;
  }

  for (const item of resp._embedded.elements) {
    const indent = item._links?.parent?.href ? '  ' : '';
    console.log(`${indent}  🏷️  ID: ${String(item.id).padEnd(6)}  ${item.value || item.name || '?'}`);
  }
  console.log(`\n${resp._embedded.elements.length} item(s)`);
}

async function cmdCustomFieldItemRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required (custom field item ID)');
    process.exit(1);
  }

  const item = await opFetch(`/custom_field_items/${options.id}`);

  console.log(`🏷️ Custom Field Item #${item.id}`);
  console.log(`   Value:       ${item.value || item.name || '?'}`);
  if (item._links?.parent?.href) {
    const parentId = item._links.parent.href.split('/').pop();
    console.log(`   Parent:      #${parentId}`);
  }
}

async function cmdCustomFieldItemBranch(options) {
  if (!options.id) {
    console.error('ERROR: --id is required (custom field item ID)');
    process.exit(1);
  }

  const resp = await opFetch(`/custom_field_items/${options.id}/branch`);

  if (!resp._embedded?.elements?.length) {
    console.log('No branch items found.');
    return;
  }

  for (const item of resp._embedded.elements) {
    console.log(`  🏷️  ID: ${String(item.id).padEnd(6)}  ${item.value || item.name || '?'}`);
  }
  console.log(`\n${resp._embedded.elements.length} item(s) in branch`);
}

async function cmdCustomOptionRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const opt = await opFetch(`/custom_options/${options.id}`);

  console.log(`🔘 Custom Option #${opt.id}`);
  console.log(`   Value:       ${opt.value || '?'}`);
}

// ── Custom Action commands ───────────────────────────────────────────────────

async function cmdCustomActionRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const ca = await opFetch(`/custom_actions/${options.id}`);

  console.log(`⚡ Custom Action #${ca.id}: ${ca.name || '?'}`);
  if (ca.description) console.log(`   Description: ${ca.description}`);
}

async function cmdCustomActionExecute(options) {
  if (!options.id || !options.wpId) {
    console.error('ERROR: --id and --wp-id are required');
    process.exit(1);
  }

  // Get current work package for lockVersion
  const wp = await opFetch(`/work_packages/${options.wpId}`);

  await opFetch(`/custom_actions/${options.id}/execute`, {
    method: 'POST',
    body: JSON.stringify({
      lockVersion: wp.lockVersion,
      _links: {
        workPackage: { href: `/api/v3/work_packages/${options.wpId}` },
      },
    }),
  });

  console.log(`✅ Custom action #${options.id} executed on WP#${options.wpId}`);
}

// ── Group commands ───────────────────────────────────────────────────────────

async function cmdGroupList() {
  const resp = await opFetch(`/groups?pageSize=${CFG.maxResults}`);

  if (!resp._embedded.elements.length) {
    console.log('No groups found.');
    return;
  }

  for (const g of resp._embedded.elements) {
    const memberCount = g._embedded?.members?.length ?? '?';
    console.log(`  👥  ID: ${String(g.id).padEnd(6)}  ${g.name.padEnd(30)}  ${memberCount} member(s)`);
  }
  console.log(`\n${resp._embedded.elements.length} group(s)`);
}

async function cmdGroupRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const g = await opFetch(`/groups/${options.id}`);

  console.log(`👥 ${g.name}`);
  console.log(`   ID:          ${g.id}`);
  console.log(`   Created:     ${g.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${g.updatedAt?.substring(0, 10) || '?'}`);

  const members = g._embedded?.members || [];
  if (members.length) {
    console.log(`\n   Members (${members.length}):`);
    for (const m of members) {
      const login = m.login ? ` (${m.login})` : '';
      console.log(`     👤  ID: ${String(m.id).padEnd(6)}  ${m.name}${login}`);
    }
  } else {
    console.log('   Members:     none');
  }
}

async function cmdGroupCreate(options) {
  if (!options.name) {
    console.error('ERROR: --name is required');
    process.exit(1);
  }

  const payload = { name: options.name };

  if (options.members) {
    const ids = options.members.split(',').map(id => id.trim());
    payload._links = {
      members: ids.map(id => ({ href: `/api/v3/users/${id}` })),
    };
  }

  const result = await opFetch('/groups', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Group created: ${result.name}`);
  console.log(`   ID: ${result.id}`);
}

async function cmdGroupUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const payload = {};
  if (options.name) payload.name = options.name;

  if (options.members) {
    const ids = options.members.split(',').map(id => id.trim());
    payload._links = {
      members: ids.map(id => ({ href: `/api/v3/users/${id}` })),
    };
  }

  await opFetch(`/groups/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Group #${options.id} updated`);
}

async function cmdGroupDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }

  await opFetch(`/groups/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Group #${options.id} deleted`);
}

// ── News commands ────────────────────────────────────────────────────────────

async function cmdNewsList(options) {
  const resp = await opFetch(`/news?pageSize=${CFG.maxResults}&sortBy=[["createdAt","desc"]]`);

  if (!resp._embedded.elements.length) {
    console.log('No news found.');
    return;
  }

  for (const n of resp._embedded.elements) {
    const author = halLink(n, 'author');
    const project = halLink(n, 'project');
    const created = n.createdAt?.substring(0, 10) || '?';
    const summary = n.summary ? `  ${n.summary.substring(0, 60)}${n.summary.length > 60 ? '...' : ''}` : '';
    console.log(`📰  #${String(n.id).padEnd(6)}  ${project.padEnd(20)}  ${created}  ${author.padEnd(20)}  ${n.title}${summary}`);
  }
  console.log(`\n${resp._embedded.elements.length} of ${resp.total} news item(s)`);
}

async function cmdNewsRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const n = await opFetch(`/news/${options.id}`);

  console.log(`📰 #${n.id}: ${n.title}`);
  console.log(`   Project:     ${halLink(n, 'project')}`);
  console.log(`   Author:      ${halLink(n, 'author')}`);
  console.log(`   Created:     ${n.createdAt?.substring(0, 10) || '?'}`);
  if (n.summary) console.log(`   Summary:     ${n.summary}`);

  if (n.description?.raw) {
    console.log(`\n📝 Description:\n${n.description.raw}`);
  }
}

async function cmdNewsCreate(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set OP_DEFAULT_PROJECT)');
    process.exit(1);
  }
  if (!options.title) {
    console.error('ERROR: --title is required');
    process.exit(1);
  }

  // Resolve project to numeric ID
  const projResp = await opFetch(`/projects/${project}`);

  const payload = {
    title: options.title,
    _links: {
      project: { href: `/api/v3/projects/${projResp.id}` },
    },
  };

  if (options.summary) payload.summary = options.summary;
  if (options.description) payload.description = { format: 'markdown', raw: options.description };

  const result = await opFetch('/news', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  console.log(`✅ News created: #${result.id} — ${result.title}`);
}

async function cmdNewsUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const payload = {};
  if (options.title) payload.title = options.title;
  if (options.summary !== undefined) payload.summary = options.summary;
  if (options.description) payload.description = { format: 'markdown', raw: options.description };

  await opFetch(`/news/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ News #${options.id} updated`);
}

async function cmdNewsDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: openproject news-delete --id 5 --confirm');
    process.exit(1);
  }

  await opFetch(`/news/${options.id}`, { method: 'DELETE' });
  console.log(`✅ News #${options.id} deleted`);
}

// ── Watcher commands ─────────────────────────────────────────────────────────

async function cmdWatcherList(options) {
  if (!options.wpId) {
    console.error('ERROR: --wp-id is required');
    process.exit(1);
  }

  const resp = await opFetch(`/work_packages/${options.wpId}/watchers`);

  if (!resp._embedded.elements.length) {
    console.log('No watchers on this work package.');
    return;
  }

  for (const u of resp._embedded.elements) {
    const login = u.login ? ` (${u.login})` : '';
    const email = u.email ? `  ${u.email}` : '';
    console.log(`  👁️  ID: ${String(u.id).padEnd(6)}  ${u.name}${login}${email}`);
  }
  console.log(`\n${resp._embedded.elements.length} watcher(s)`);
}

async function cmdWatcherAdd(options) {
  if (!options.wpId || !options.userId) {
    console.error('ERROR: --wp-id and --user-id are required');
    process.exit(1);
  }

  await opFetch(`/work_packages/${options.wpId}/watchers`, {
    method: 'POST',
    body: JSON.stringify({
      user: { href: `/api/v3/users/${options.userId}` },
    }),
  });

  console.log(`✅ User #${options.userId} added as watcher on WP#${options.wpId}`);
}

async function cmdWatcherRemove(options) {
  if (!options.wpId || !options.userId) {
    console.error('ERROR: --wp-id and --user-id are required');
    process.exit(1);
  }

  await opFetch(`/work_packages/${options.wpId}/watchers/${options.userId}`, {
    method: 'DELETE',
  });

  console.log(`✅ User #${options.userId} removed as watcher from WP#${options.wpId}`);
}

async function cmdWatcherAvailable(options) {
  if (!options.wpId) {
    console.error('ERROR: --wp-id is required');
    process.exit(1);
  }

  const resp = await opFetch(`/work_packages/${options.wpId}/available_watchers`);

  if (!resp._embedded.elements.length) {
    console.log('No available watchers.');
    return;
  }

  for (const u of resp._embedded.elements) {
    const login = u.login ? ` (${u.login})` : '';
    console.log(`  👤  ID: ${String(u.id).padEnd(6)}  ${u.name}${login}`);
  }
  console.log(`\n${resp._embedded.elements.length} available watcher(s)`);
}

// ── Notification commands ────────────────────────────────────────────────────

function reasonEmoji(reason) {
  const map = {
    assigned: '👤', commented: '💬', created: '🆕', dateAlert: '📅',
    mentioned: '📣', prioritized: '⚡', processed: '⚙️', responsible: '🎯',
    subscribed: '🔔', scheduled: '🗓️', watched: '👁️',
  };
  return map[reason] || '🔔';
}

async function cmdNotificationList(options) {
  const filters = [];

  if (options.reason) {
    filters.push({ reason: { operator: '=', values: [options.reason] } });
  }
  if (options.project) {
    filters.push({ project: { operator: '=', values: [options.project] } });
  }
  if (options.unread) {
    filters.push({ readIAN: { operator: '=', values: ['f'] } });
  }
  if (options.wpId) {
    filters.push({ resourceId: { operator: '=', values: [options.wpId] } });
  }

  const filterParam = filters.length ? `&filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
  const resp = await opFetch(`/notifications?pageSize=${CFG.maxResults}${filterParam}&sortBy=[["createdAt","desc"]]`);

  if (!resp._embedded.elements.length) {
    console.log('No notifications found.');
    return;
  }

  for (const n of resp._embedded.elements) {
    const emoji = reasonEmoji(n.reason);
    const read = n.readIAN ? '  ' : '🔵';
    const actor = halLink(n, 'actor');
    const resource = halLink(n, 'resource');
    const project = halLink(n, 'project');
    const created = n.createdAt?.substring(0, 16).replace('T', ' ') || '?';
    console.log(`${read} ${emoji}  #${String(n.id).padEnd(8)}  ${n.reason.padEnd(12)}  ${actor.padEnd(20)}  ${resource.padEnd(30)}  ${project}  ${created}`);
  }

  const unreadCount = resp._embedded.elements.filter(n => !n.readIAN).length;
  console.log(`\n${resp._embedded.elements.length} of ${resp.total} notification(s)${unreadCount ? ` (${unreadCount} unread)` : ''}`);
}

async function cmdNotificationRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const n = await opFetch(`/notifications/${options.id}`);

  const emoji = reasonEmoji(n.reason);
  console.log(`${emoji} Notification #${n.id}`);
  console.log(`   Reason:      ${n.reason}`);
  console.log(`   Read:        ${n.readIAN ? 'Yes' : 'No'}`);
  console.log(`   Actor:       ${halLink(n, 'actor')}`);
  console.log(`   Resource:    ${halLink(n, 'resource')}`);
  console.log(`   Project:     ${halLink(n, 'project')}`);
  console.log(`   Created:     ${n.createdAt?.substring(0, 16).replace('T', ' ') || '?'}`);
  console.log(`   Updated:     ${n.updatedAt?.substring(0, 16).replace('T', ' ') || '?'}`);
}

async function cmdNotificationMarkRead(options) {
  if (options.all) {
    const filters = [];
    if (options.project) {
      filters.push({ project: { operator: '=', values: [options.project] } });
    }
    const filterParam = filters.length ? `?filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
    await opFetch(`/notifications/read_ian${filterParam}`, { method: 'POST' });
    console.log('✅ All matching notifications marked as read');
  } else if (options.id) {
    await opFetch(`/notifications/${options.id}/read_ian`, { method: 'POST' });
    console.log(`✅ Notification #${options.id} marked as read`);
  } else {
    console.error('ERROR: --id or --all is required');
    process.exit(1);
  }
}

async function cmdNotificationMarkUnread(options) {
  if (options.all) {
    const filters = [];
    if (options.project) {
      filters.push({ project: { operator: '=', values: [options.project] } });
    }
    const filterParam = filters.length ? `?filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
    await opFetch(`/notifications/unread_ian${filterParam}`, { method: 'POST' });
    console.log('✅ All matching notifications marked as unread');
  } else if (options.id) {
    await opFetch(`/notifications/${options.id}/unread_ian`, { method: 'POST' });
    console.log(`✅ Notification #${options.id} marked as unread`);
  } else {
    console.error('ERROR: --id or --all is required');
    process.exit(1);
  }
}

// ── User commands ────────────────────────────────────────────────────────────

async function cmdUserList(options) {
  const filters = [];

  if (options.status) {
    const statusMap = {
      active: '0', registered: '1', locked: '2', invited: '4',
    };
    const val = statusMap[options.status.toLowerCase()] || options.status;
    filters.push({ status: { operator: '=', values: [val] } });
  }
  if (options.name) {
    filters.push({ name: { operator: '~', values: [options.name] } });
  }
  if (options.group) {
    filters.push({ group: { operator: '=', values: [options.group] } });
  }

  const filterParam = filters.length ? `&filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
  const resp = await opFetch(`/users?pageSize=${CFG.maxResults}${filterParam}&sortBy=[["name","asc"]]`);

  if (!resp._embedded.elements.length) {
    console.log('No users found.');
    return;
  }

  for (const u of resp._embedded.elements) {
    const status = u.status || '?';
    const admin = u.admin ? ' 👑' : '';
    const email = u.email ? `  ${u.email}` : '';
    const login = u.login ? ` (${u.login})` : '';
    console.log(`  👤  ID: ${String(u.id).padEnd(6)}  ${u.name || `${u.firstName} ${u.lastName}`}${login}${admin}  [${status}]${email}`);
  }
  console.log(`\n${resp._embedded.elements.length} of ${resp.total} user(s)`);
}

async function cmdUserRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required (numeric user ID or "me")');
    process.exit(1);
  }

  const u = await opFetch(`/users/${options.id}`);

  console.log(`👤 ${u.name || `${u.firstName} ${u.lastName}`}`);
  console.log(`   ID:          ${u.id}`);
  if (u.login) console.log(`   Login:       ${u.login}`);
  if (u.email) console.log(`   Email:       ${u.email}`);
  console.log(`   Status:      ${u.status || '?'}`);
  console.log(`   Admin:       ${u.admin ? 'Yes' : 'No'}`);
  if (u.language) console.log(`   Language:    ${u.language}`);
  console.log(`   Created:     ${u.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${u.updatedAt?.substring(0, 10) || '?'}`);
  if (u.avatar) console.log(`   Avatar:      ${u.avatar}`);
}

async function cmdUserMe() {
  const u = await opFetch('/users/me');

  console.log(`👤 ${u.name || `${u.firstName} ${u.lastName}`}`);
  console.log(`   ID:          ${u.id}`);
  if (u.login) console.log(`   Login:       ${u.login}`);
  if (u.email) console.log(`   Email:       ${u.email}`);
  console.log(`   Status:      ${u.status || '?'}`);
  console.log(`   Admin:       ${u.admin ? 'Yes' : 'No'}`);
  if (u.language) console.log(`   Language:    ${u.language}`);
  console.log(`   Created:     ${u.createdAt?.substring(0, 10) || '?'}`);
  console.log(`   Updated:     ${u.updatedAt?.substring(0, 10) || '?'}`);
}

// ── Relation commands ────────────────────────────────────────────────────────

const RELATION_TYPES = [
  'relates', 'duplicates', 'duplicated', 'blocks', 'blocked',
  'precedes', 'follows', 'includes', 'partof', 'requires', 'required',
];

function relationEmoji(type) {
  const map = {
    relates: '🔗', duplicates: '♊', duplicated: '♊',
    blocks: '🚫', blocked: '🚫', precedes: '⏩', follows: '⏪',
    includes: '📦', partof: '🧩', requires: '⚙️', required: '⚙️',
  };
  return map[type] || '🔗';
}

async function cmdRelationList(options) {
  const filters = [];

  if (options.wpId) {
    filters.push({ involved: { operator: '=', values: [options.wpId] } });
  }
  if (options.type) {
    filters.push({ type: { operator: '=', values: [options.type] } });
  }

  const filterParam = filters.length ? `&filters=${encodeURIComponent(JSON.stringify(filters))}` : '';
  const resp = await opFetch(`/relations?pageSize=${CFG.maxResults}${filterParam}`);

  if (!resp._embedded.elements.length) {
    console.log('No relations found.');
    return;
  }

  for (const r of resp._embedded.elements) {
    const fromId = halId(r, 'from') || '?';
    const toId = halId(r, 'to') || '?';
    const emoji = relationEmoji(r.type);
    const desc = r.description ? `  "${r.description}"` : '';
    const lag = r.lag ? `  (lag: ${r.lag}d)` : '';
    console.log(`${emoji}  #${String(r.id).padEnd(6)}  WP#${fromId} → ${r.type} → WP#${toId}${lag}${desc}`);
  }
  console.log(`\n${resp._embedded.elements.length} relation(s)`);
}

async function cmdRelationRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const r = await opFetch(`/relations/${options.id}`);

  const fromId = halId(r, 'from') || '?';
  const toId = halId(r, 'to') || '?';
  const emoji = relationEmoji(r.type);

  console.log(`${emoji} Relation #${r.id}`);
  console.log(`   Type:        ${r.type}`);
  console.log(`   From:        WP#${fromId}`);
  console.log(`   To:          WP#${toId}`);
  if (r.lag != null) console.log(`   Lag:         ${r.lag} day(s)`);
  if (r.description) console.log(`   Description: ${r.description}`);
  if (r.reverseType) console.log(`   Reverse:     ${r.reverseType}`);
}

async function cmdRelationCreate(options) {
  if (!options.wpId || !options.toWpId || !options.type) {
    console.error('ERROR: --wp-id, --to-wp-id, and --type are required');
    process.exit(1);
  }

  const type = options.type.toLowerCase();
  if (!RELATION_TYPES.includes(type)) {
    console.error(`ERROR: Invalid type "${options.type}". Must be one of: ${RELATION_TYPES.join(', ')}`);
    process.exit(1);
  }

  const payload = {
    type,
    _links: {
      to: { href: `/api/v3/work_packages/${options.toWpId}` },
    },
  };

  if (options.description) payload.description = options.description;
  if (options.lag !== undefined) payload.lag = parseInt(options.lag, 10);

  const result = await opFetch(`/work_packages/${options.wpId}/relations`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Relation created: WP#${options.wpId} ${type} WP#${options.toWpId}`);
  console.log(`   ID: ${result.id}`);
}

async function cmdRelationUpdate(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }

  const payload = {};
  if (options.type) {
    const type = options.type.toLowerCase();
    if (!RELATION_TYPES.includes(type)) {
      console.error(`ERROR: Invalid type "${options.type}". Must be one of: ${RELATION_TYPES.join(', ')}`);
      process.exit(1);
    }
    payload.type = type;
  }
  if (options.description !== undefined) payload.description = options.description || null;
  if (options.lag !== undefined) payload.lag = parseInt(options.lag, 10);

  await opFetch(`/relations/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });

  console.log(`✅ Relation #${options.id} updated`);
}

async function cmdRelationDelete(options) {
  if (!options.id) {
    console.error('ERROR: --id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: openproject relation-delete --id 5 --confirm');
    process.exit(1);
  }

  await opFetch(`/relations/${options.id}`, { method: 'DELETE' });
  console.log(`✅ Relation #${options.id} deleted`);
}

// ── Wiki Page commands ──────────────────────────────────────────────────────

async function cmdWikiRead(options) {
  if (!options.id) {
    console.error('ERROR: --id is required (wiki page numeric ID)');
    process.exit(1);
  }

  const wp = await opFetch(`/wiki_pages/${options.id}`);

  console.log(`📖 Wiki Page #${wp.id}: ${wp.title}`);
  console.log(`   Project:     ${halLink(wp, 'project')}`);
  console.log(`   URL:         ${CFG.host}/wiki/${wp.id}`);

  if (wp._links?.attachments?.href) {
    console.log(`   Attachments: ${wp._links.attachments.href}`);
  }
}

async function cmdWikiAttachmentList(options) {
  if (!options.id) {
    console.error('ERROR: --id is required (wiki page numeric ID)');
    process.exit(1);
  }

  const resp = await opFetch(`/wiki_pages/${options.id}/attachments`);

  if (!resp._embedded.elements.length) {
    console.log('No attachments on this wiki page.');
    return;
  }

  for (const a of resp._embedded.elements) {
    const size = `${(a.fileSize / 1024).toFixed(1)} KB`;
    const created = a.createdAt?.substring(0, 10) || '';
    const author = halLink(a, 'author');
    console.log(`📎  #${String(a.id).padEnd(8)}  ${a.fileName.padEnd(30)}  ${size.padStart(12)}  ${created}  ${author}`);
  }
  console.log(`\n${resp._embedded.elements.length} attachment(s)`);
}

async function cmdWikiAttachmentAdd(options) {
  if (!options.id || !options.file) {
    console.error('ERROR: --id and --file are required');
    process.exit(1);
  }

  const filePath = resolve(safePath(options.file) || options.file);
  checkFileSize(filePath);

  const fileContent = readFileSync(filePath);
  const fileName = basename(filePath);

  const form = new FormData();
  form.append('file', new Blob([fileContent]), fileName);
  form.append('metadata', JSON.stringify({ fileName, description: { format: 'plain', raw: '' } }));

  const url = `${baseUrl()}/wiki_pages/${options.id}/attachments`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Authorization': authHeader() },
    body: form,
  });

  if (!resp.ok) {
    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }
    const msg = json?.message || json?.errorIdentifier || body;
    console.error(`ERROR (${resp.status}): ${msg}`);
    process.exit(1);
  }

  const result = await resp.json();
  console.log(`✅ Attachment uploaded to wiki page #${options.id}`);
  console.log(`   File: ${result.fileName}`);
  console.log(`   Size: ${(result.fileSize / 1024).toFixed(1)} KB`);
  console.log(`   ID: ${result.id}`);
}

// ── CLI ─────────────────────────────────────────────────────────────────────

const program = new Command();

program
  .name('openproject')
  .description('OpenClaw OpenProject Skill — project management via API v3')
  .version('2.0.0');

// Work Packages
program.command('wp-list').description('List work packages')
  .option('-p, --project <id>', 'Project identifier')
  .option('-s, --status <name>', 'Filter by status name')
  .option('-a, --assignee <user>', 'Filter by assignee ("me" or user ID)')
  .option('-t, --type <name>', 'Filter by type name')
  .action(wrap(cmdWpList));

program.command('wp-create').description('Create a work package')
  .option('-p, --project <id>', 'Project identifier')
  .requiredOption('-s, --subject <text>', 'Work package subject')
  .option('-d, --description <text>', 'Description (markdown)')
  .option('-t, --type <name>', 'Type (Task, Bug, Feature...)')
  .option('--priority <name>', 'Priority name')
  .action(wrap(cmdWpCreate));

program.command('wp-read').description('Read work package details')
  .requiredOption('--id <id>', 'Work package ID')
  .action(wrap(cmdWpRead));

program.command('wp-update').description('Update a work package')
  .requiredOption('--id <id>', 'Work package ID')
  .option('-s, --subject <text>', 'New subject')
  .option('-d, --description <text>', 'New description')
  .option('--status <name>', 'New status name')
  .option('--priority <name>', 'New priority name')
  .option('-t, --type <name>', 'New type name')
  .option('--percent-done <n>', 'Percentage done (0-100)')
  .action(wrap(cmdWpUpdate));

program.command('wp-delete').description('Delete a work package (requires --confirm)')
  .requiredOption('--id <id>', 'Work package ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdWpDelete));

// Projects
program.command('project-list').description('List projects')
  .action(wrap(cmdProjectList));

program.command('project-read').description('Read project details')
  .requiredOption('--id <id>', 'Project identifier or numeric ID')
  .action(wrap(cmdProjectRead));

program.command('project-create').description('Create a project')
  .requiredOption('-n, --name <name>', 'Project name')
  .option('-i, --identifier <id>', 'Project identifier (slug)')
  .option('-d, --description <text>', 'Description')
  .option('--public <bool>', 'Public project (true/false)')
  .action(wrap(cmdProjectCreate));

// Comments
program.command('comment-list').description('List comments on a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .action(wrap(cmdCommentList));

program.command('comment-add').description('Add a comment to a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .requiredOption('-b, --body <text>', 'Comment body (markdown)')
  .action(wrap(cmdCommentAdd));

// Attachments
program.command('attachment-list').description('List attachments on a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .action(wrap(cmdAttachmentList));

program.command('attachment-add').description('Upload an attachment to a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .requiredOption('-f, --file <path>', 'Local file path')
  .action(wrap(cmdAttachmentAdd));

program.command('attachment-delete').description('Delete an attachment (requires --confirm)')
  .requiredOption('--id <id>', 'Attachment ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdAttachmentDelete));

// Time Entries
program.command('time-list').description('List time entries')
  .option('-p, --project <id>', 'Project identifier')
  .option('--wp-id <id>', 'Work package ID')
  .action(wrap(cmdTimeList));

program.command('time-create').description('Log time on a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .requiredOption('--hours <n>', 'Hours spent (e.g. 2.5)')
  .option('-c, --comment <text>', 'Comment')
  .option('--date <YYYY-MM-DD>', 'Date spent (default: today)')
  .option('--activity-id <id>', 'Activity type ID')
  .action(wrap(cmdTimeCreate));

program.command('time-update').description('Update a time entry')
  .requiredOption('--id <id>', 'Time entry ID')
  .option('--hours <n>', 'New hours')
  .option('-c, --comment <text>', 'New comment')
  .option('--date <YYYY-MM-DD>', 'New date')
  .action(wrap(cmdTimeUpdate));

program.command('time-delete').description('Delete a time entry (requires --confirm)')
  .requiredOption('--id <id>', 'Time entry ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdTimeDelete));

// Reference Data
program.command('status-list').description('List all statuses').action(wrap(cmdStatusList));
program.command('type-list').description('List work package types').action(wrap(cmdTypeList));
program.command('priority-list').description('List priorities').action(wrap(cmdPriorityList));

program.command('member-list').description('List project members')
  .option('-p, --project <id>', 'Project identifier')
  .action(wrap(cmdMemberList));

program.command('version-list').description('List project versions/milestones')
  .option('-p, --project <id>', 'Project identifier')
  .action(wrap(cmdVersionList));

program.command('category-list').description('List project categories')
  .option('-p, --project <id>', 'Project identifier')
  .action(wrap(cmdCategoryList));

// Users
program.command('user-list').description('List users')
  .option('-s, --status <status>', 'Filter by status (active, registered, locked, invited)')
  .option('-n, --name <text>', 'Search by name (partial match)')
  .option('-g, --group <id>', 'Filter by group ID')
  .action(wrap(cmdUserList));

program.command('user-read').description('Read user details')
  .requiredOption('--id <id>', 'User numeric ID')
  .action(wrap(cmdUserRead));

program.command('user-me').description('Show current authenticated user')
  .action(wrap(cmdUserMe));

// Documents
program.command('document-list').description('List documents')
  .action(wrap(cmdDocumentList));
program.command('document-read').description('Read a document')
  .requiredOption('--id <id>', 'Document ID')
  .action(wrap(cmdDocumentRead));
program.command('document-update').description('Update a document')
  .requiredOption('--id <id>', 'Document ID')
  .option('--title <text>', 'New title')
  .option('-d, --description <text>', 'New description')
  .action(wrap(cmdDocumentUpdate));

// Revisions
program.command('revision-read').description('Read a revision')
  .requiredOption('--id <id>', 'Revision ID')
  .action(wrap(cmdRevisionRead));
program.command('revision-list-by-wp').description('List revisions for a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .action(wrap(cmdRevisionListByWp));

// Capabilities & Actions
program.command('capability-list').description('List capabilities')
  .option('--context <id>', 'Filter by context (project ID or "global")')
  .option('--action <id>', 'Filter by action')
  .option('--principal <id>', 'Filter by principal (user/group ID)')
  .action(wrap(cmdCapabilityList));
program.command('capability-global').description('List global capabilities')
  .action(wrap(cmdCapabilityGlobal));
program.command('action-list').description('List available actions')
  .action(wrap(cmdActionList));
program.command('action-read').description('Read an action')
  .requiredOption('--id <id>', 'Action ID')
  .action(wrap(cmdActionRead));

// My Preferences
program.command('my-preferences-read').description('View my preferences')
  .action(wrap(cmdMyPreferencesRead));
program.command('my-preferences-update').description('Update my preferences')
  .option('--time-zone <tz>', 'Time zone')
  .option('--auto-hide-popups <bool>', 'Auto-hide popups (true/false)')
  .option('--comment-order <order>', 'Comment order (asc/desc)')
  .option('--warn-on-leaving-unsaved <bool>', 'Warn on leaving unsaved (true/false)')
  .action(wrap(cmdMyPreferencesUpdate));

// Render
program.command('render-markdown').description('Render markdown to HTML')
  .requiredOption('--text <text>', 'Markdown text to render')
  .action(wrap(cmdRenderMarkdown));
program.command('render-plain').description('Render plain text to HTML')
  .requiredOption('--text <text>', 'Plain text to render')
  .action(wrap(cmdRenderPlain));

// Posts (Forum)
program.command('post-read').description('Read a forum post')
  .requiredOption('--id <id>', 'Post ID')
  .action(wrap(cmdPostRead));
program.command('post-attachment-list').description('List attachments on a forum post')
  .requiredOption('--id <id>', 'Post ID')
  .action(wrap(cmdPostAttachmentList));

// Reminders
program.command('reminder-list').description('List my reminders')
  .action(wrap(cmdReminderList));
program.command('reminder-create').description('Create a reminder for a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .requiredOption('--remind-at <ISO>', 'Reminder date-time (ISO 8601)')
  .option('--note <text>', 'Reminder note')
  .action(wrap(cmdReminderCreate));
program.command('reminder-update').description('Update a reminder')
  .requiredOption('--id <id>', 'Reminder ID')
  .option('--remind-at <ISO>', 'New reminder date-time')
  .option('--note <text>', 'New note')
  .action(wrap(cmdReminderUpdate));
program.command('reminder-delete').description('Delete a reminder (requires --confirm)')
  .requiredOption('--id <id>', 'Reminder ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdReminderDelete));

// Project Statuses
program.command('project-status-read').description('Read a project status')
  .requiredOption('--id <id>', 'Project status ID')
  .action(wrap(cmdProjectStatusRead));

// Project Phases (Enterprise)
program.command('project-phase-definition-list').description('List project phase definitions (Enterprise)')
  .action(wrap(cmdProjectPhaseDefinitionList));

program.command('project-phase-definition-read').description('Read a project phase definition (Enterprise)')
  .requiredOption('--id <id>', 'Phase definition ID')
  .action(wrap(cmdProjectPhaseDefinitionRead));

program.command('project-phase-read').description('Read a project phase (Enterprise)')
  .requiredOption('--id <id>', 'Project phase ID')
  .action(wrap(cmdProjectPhaseRead));

// Portfolios (Enterprise)
program.command('portfolio-list').description('List portfolios (Enterprise)')
  .action(wrap(cmdPortfolioList));

program.command('portfolio-read').description('Read a portfolio (Enterprise)')
  .requiredOption('--id <id>', 'Portfolio ID')
  .action(wrap(cmdPortfolioRead));

program.command('portfolio-update').description('Update a portfolio (Enterprise)')
  .requiredOption('--id <id>', 'Portfolio ID')
  .option('-n, --name <name>', 'New name')
  .option('-d, --description <text>', 'New description')
  .action(wrap(cmdPortfolioUpdate));

program.command('portfolio-delete').description('Delete a portfolio (Enterprise, requires --confirm)')
  .requiredOption('--id <id>', 'Portfolio ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdPortfolioDelete));

// Programs (Enterprise)
program.command('program-list').description('List programs (Enterprise)')
  .action(wrap(cmdProgramList));

program.command('program-read').description('Read a program (Enterprise)')
  .requiredOption('--id <id>', 'Program ID')
  .action(wrap(cmdProgramRead));

program.command('program-update').description('Update a program (Enterprise)')
  .requiredOption('--id <id>', 'Program ID')
  .option('-n, --name <name>', 'New name')
  .option('-d, --description <text>', 'New description')
  .action(wrap(cmdProgramUpdate));

program.command('program-delete').description('Delete a program (Enterprise, requires --confirm)')
  .requiredOption('--id <id>', 'Program ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdProgramDelete));

// Placeholder Users (Enterprise)
program.command('placeholder-user-list').description('List placeholder users (Enterprise)')
  .action(wrap(cmdPlaceholderUserList));

program.command('placeholder-user-read').description('Read a placeholder user (Enterprise)')
  .requiredOption('--id <id>', 'Placeholder user ID')
  .action(wrap(cmdPlaceholderUserRead));

program.command('placeholder-user-create').description('Create a placeholder user (Enterprise)')
  .requiredOption('-n, --name <name>', 'Placeholder name')
  .action(wrap(cmdPlaceholderUserCreate));

program.command('placeholder-user-update').description('Update a placeholder user (Enterprise)')
  .requiredOption('--id <id>', 'Placeholder user ID')
  .option('-n, --name <name>', 'New name')
  .action(wrap(cmdPlaceholderUserUpdate));

program.command('placeholder-user-delete').description('Delete a placeholder user (Enterprise, requires --confirm)')
  .requiredOption('--id <id>', 'Placeholder user ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdPlaceholderUserDelete));

// Budgets (Enterprise)
program.command('budget-read').description('Read a budget (Enterprise)')
  .requiredOption('--id <id>', 'Budget ID')
  .action(wrap(cmdBudgetRead));

program.command('budget-list').description('List project budgets (Enterprise)')
  .option('-p, --project <id>', 'Project identifier')
  .action(wrap(cmdBudgetList));

// Meetings (Enterprise)
program.command('meeting-read').description('Read a meeting (Enterprise)')
  .requiredOption('--id <id>', 'Meeting ID')
  .action(wrap(cmdMeetingRead));

program.command('meeting-attachment-list').description('List meeting attachments (Enterprise)')
  .requiredOption('--id <id>', 'Meeting ID')
  .action(wrap(cmdMeetingAttachmentList));

program.command('meeting-attachment-add').description('Upload attachment to meeting (Enterprise)')
  .requiredOption('--id <id>', 'Meeting ID')
  .requiredOption('-f, --file <path>', 'Local file path')
  .action(wrap(cmdMeetingAttachmentAdd));

// Days
program.command('day-read').description('Check if a date is a working day')
  .requiredOption('--date <YYYY-MM-DD>', 'Date to check')
  .action(wrap(cmdDayRead));

program.command('days-list').description('List days in a date range')
  .option('--from <YYYY-MM-DD>', 'Start date (default: today)')
  .option('--to <YYYY-MM-DD>', 'End date')
  .action(wrap(cmdDaysList));

program.command('non-working-days-list').description('List all non-working days')
  .action(wrap(cmdNonWorkingDaysList));

program.command('non-working-day-read').description('View a non-working day')
  .requiredOption('--date <YYYY-MM-DD>', 'Date')
  .action(wrap(cmdNonWorkingDayRead));

program.command('week-days-list').description('List week day configuration (working/non-working)')
  .action(wrap(cmdWeekDaysList));

program.command('week-day-read').description('View a week day configuration')
  .requiredOption('--day <1-7>', 'Day number (1=Monday, 7=Sunday)')
  .action(wrap(cmdWeekDayRead));

// Configuration
program.command('config-read').description('View instance configuration')
  .action(wrap(cmdConfigRead));

program.command('project-config-read').description('View project configuration')
  .option('-p, --project <id>', 'Project identifier')
  .action(wrap(cmdProjectConfigRead));

// OAuth
program.command('oauth-app-read').description('Read an OAuth application')
  .requiredOption('--id <id>', 'OAuth application ID')
  .action(wrap(cmdOauthAppRead));

program.command('oauth-credentials-read').description('Read OAuth client credentials')
  .requiredOption('--id <id>', 'OAuth client credentials ID')
  .action(wrap(cmdOauthCredentialsRead));

// Help Texts
program.command('help-text-list').description('List attribute help texts')
  .action(wrap(cmdHelpTextList));

program.command('help-text-read').description('Read a help text')
  .requiredOption('--id <id>', 'Help text ID')
  .action(wrap(cmdHelpTextRead));

// Custom Fields & Options
program.command('custom-field-items').description('List items for a hierarchical custom field')
  .requiredOption('--id <id>', 'Custom field ID')
  .action(wrap(cmdCustomFieldItems));

program.command('custom-field-item-read').description('Read a custom field item')
  .requiredOption('--id <id>', 'Custom field item ID')
  .action(wrap(cmdCustomFieldItemRead));

program.command('custom-field-item-branch').description('Get a custom field item branch (ancestors)')
  .requiredOption('--id <id>', 'Custom field item ID')
  .action(wrap(cmdCustomFieldItemBranch));

program.command('custom-option-read').description('Read a custom option value')
  .requiredOption('--id <id>', 'Custom option ID')
  .action(wrap(cmdCustomOptionRead));

// Custom Actions
program.command('custom-action-read').description('Read a custom action')
  .requiredOption('--id <id>', 'Custom action ID')
  .action(wrap(cmdCustomActionRead));

program.command('custom-action-execute').description('Execute a custom action on a work package')
  .requiredOption('--id <id>', 'Custom action ID')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .action(wrap(cmdCustomActionExecute));

// Groups
program.command('group-list').description('List groups')
  .action(wrap(cmdGroupList));

program.command('group-read').description('Read group details with members')
  .requiredOption('--id <id>', 'Group ID')
  .action(wrap(cmdGroupRead));

program.command('group-create').description('Create a group')
  .requiredOption('-n, --name <name>', 'Group name')
  .option('-m, --members <ids>', 'Comma-separated user IDs')
  .action(wrap(cmdGroupCreate));

program.command('group-update').description('Update a group')
  .requiredOption('--id <id>', 'Group ID')
  .option('-n, --name <name>', 'New group name')
  .option('-m, --members <ids>', 'New comma-separated user IDs (replaces all)')
  .action(wrap(cmdGroupUpdate));

program.command('group-delete').description('Delete a group (requires --confirm)')
  .requiredOption('--id <id>', 'Group ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdGroupDelete));

// News
program.command('news-list').description('List news')
  .action(wrap(cmdNewsList));

program.command('news-read').description('Read news details')
  .requiredOption('--id <id>', 'News ID')
  .action(wrap(cmdNewsRead));

program.command('news-create').description('Create a news item')
  .requiredOption('--title <text>', 'News headline')
  .option('-p, --project <id>', 'Project identifier')
  .option('-s, --summary <text>', 'Short summary')
  .option('-d, --description <text>', 'Full description (markdown)')
  .action(wrap(cmdNewsCreate));

program.command('news-update').description('Update a news item')
  .requiredOption('--id <id>', 'News ID')
  .option('--title <text>', 'New headline')
  .option('-s, --summary <text>', 'New summary')
  .option('-d, --description <text>', 'New description (markdown)')
  .action(wrap(cmdNewsUpdate));

program.command('news-delete').description('Delete a news item (requires --confirm)')
  .requiredOption('--id <id>', 'News ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdNewsDelete));

// Watchers
program.command('watcher-list').description('List watchers on a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .action(wrap(cmdWatcherList));

program.command('watcher-add').description('Add a watcher to a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .requiredOption('--user-id <id>', 'User ID to add as watcher')
  .action(wrap(cmdWatcherAdd));

program.command('watcher-remove').description('Remove a watcher from a work package')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .requiredOption('--user-id <id>', 'User ID to remove')
  .action(wrap(cmdWatcherRemove));

program.command('watcher-available').description('List users available as watchers')
  .requiredOption('--wp-id <id>', 'Work package ID')
  .action(wrap(cmdWatcherAvailable));

// Notifications
program.command('notification-list').description('List notifications')
  .option('--unread', 'Show only unread notifications')
  .option('--reason <reason>', 'Filter by reason (assigned, commented, mentioned, watched, ...)')
  .option('-p, --project <id>', 'Filter by project ID')
  .option('--wp-id <id>', 'Filter by work package ID')
  .action(wrap(cmdNotificationList));

program.command('notification-read').description('Read notification details')
  .requiredOption('--id <id>', 'Notification ID')
  .action(wrap(cmdNotificationRead));

program.command('notification-mark-read').description('Mark notification(s) as read')
  .option('--id <id>', 'Notification ID')
  .option('--all', 'Mark all notifications as read')
  .option('-p, --project <id>', 'Filter by project (with --all)')
  .action(wrap(cmdNotificationMarkRead));

program.command('notification-mark-unread').description('Mark notification(s) as unread')
  .option('--id <id>', 'Notification ID')
  .option('--all', 'Mark all notifications as unread')
  .option('-p, --project <id>', 'Filter by project (with --all)')
  .action(wrap(cmdNotificationMarkUnread));

// Relations
program.command('relation-list').description('List relations')
  .option('--wp-id <id>', 'Filter by work package ID (shows all relations involving this WP)')
  .option('-t, --type <type>', 'Filter by relation type (relates, blocks, follows, precedes, ...)')
  .action(wrap(cmdRelationList));

program.command('relation-read').description('Read relation details')
  .requiredOption('--id <id>', 'Relation ID')
  .action(wrap(cmdRelationRead));

program.command('relation-create').description('Create a relation between work packages')
  .requiredOption('--wp-id <id>', 'Source work package ID')
  .requiredOption('--to-wp-id <id>', 'Target work package ID')
  .requiredOption('-t, --type <type>', 'Relation type: relates, duplicates, blocks, precedes, follows, includes, partof, requires')
  .option('-d, --description <text>', 'Description')
  .option('--lag <days>', 'Lag in days (for precedes/follows)')
  .action(wrap(cmdRelationCreate));

program.command('relation-update').description('Update a relation')
  .requiredOption('--id <id>', 'Relation ID')
  .option('-t, --type <type>', 'New relation type')
  .option('-d, --description <text>', 'New description (empty string to clear)')
  .option('--lag <days>', 'New lag in days')
  .action(wrap(cmdRelationUpdate));

program.command('relation-delete').description('Delete a relation (requires --confirm)')
  .requiredOption('--id <id>', 'Relation ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdRelationDelete));

// Wiki Pages
program.command('wiki-read').description('Read a wiki page')
  .requiredOption('--id <id>', 'Wiki page numeric ID')
  .action(wrap(cmdWikiRead));

program.command('wiki-attachment-list').description('List attachments on a wiki page')
  .requiredOption('--id <id>', 'Wiki page numeric ID')
  .action(wrap(cmdWikiAttachmentList));

program.command('wiki-attachment-add').description('Upload an attachment to a wiki page')
  .requiredOption('--id <id>', 'Wiki page numeric ID')
  .requiredOption('-f, --file <path>', 'Local file path')
  .action(wrap(cmdWikiAttachmentAdd));

function wrap(fn) {
  return async (...args) => {
    try {
      await fn(...args);
    } catch (err) {
      if (err.statusCode) {
        console.error(`ERROR (${err.statusCode}): ${err.message}`);
      } else {
        console.error(`ERROR: ${err.message}`);
      }
      process.exit(1);
    }
  };
}

program.parse();
