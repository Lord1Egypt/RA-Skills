#!/usr/bin/env node

/**
 * OpenClaw Hivebrite Skill — CLI for the full Hivebrite Admin API.
 *
 * Covers users, companies, events, groups, donations, memberships, emailings,
 * mentoring, news, projects, media center, forums, admins, approvals, roles,
 * receipts, categories, comments, posts, audit logs, engagement scoring,
 * payment accounts, network settings, and more.
 *
 * @author Abdelkrim BOUJRAF <abdelkrim@alt-f1.be>
 * @license MIT
 * @see https://github.com/ALT-F1-OpenClaw/openclaw-skill-hivebrite-by-altf1be
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';
import { config } from 'dotenv';
import { Command } from 'commander';

// ── Load .env ────────────────────────────────────────────────────────────────

config();

// ── Read package.json version ────────────────────────────────────────────────

const __dirname = dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(readFileSync(resolve(__dirname, '..', 'package.json'), 'utf8'));

// ── Env helpers (explicit access — ClawHub scanner rule) ─────────────────────

function env(key) {
  const v = process.env[key];
  if (!v) {
    console.error(`ERROR: Missing required env var ${key}. See SKILL.md setup.`);
    process.exit(1);
  }
  return v;
}

// ── Auth: Bearer token OR OAuth 2.0 (password / refresh_token grant) ─────────

const OAUTH_TOKEN_PATH = resolve(homedir(), '.cache', 'openclaw', 'hivebrite-token.json');

let _cachedAccessToken = null;
let _tokenExpiresAt = 0;

function isOAuthMode() {
  return !!process.env.HIVEBRITE_CLIENT_ID;
}

async function getAccessToken() {
  if (!isOAuthMode()) {
    return env('HIVEBRITE_ACCESS_TOKEN');
  }

  // Check in-memory cache
  if (_cachedAccessToken && Date.now() < _tokenExpiresAt - 60000) {
    return _cachedAccessToken;
  }

  // Try reading from disk cache
  if (!_cachedAccessToken && existsSync(OAUTH_TOKEN_PATH)) {
    try {
      const cached = JSON.parse(readFileSync(OAUTH_TOKEN_PATH, 'utf8'));
      if (cached.access_token && cached.expires_at && Date.now() < cached.expires_at - 60000) {
        _cachedAccessToken = cached.access_token;
        _tokenExpiresAt = cached.expires_at;
        return _cachedAccessToken;
      }
      // If we have a refresh token from previous auth, use it
      if (cached.refresh_token) {
        process.env.HIVEBRITE_REFRESH_TOKEN = process.env.HIVEBRITE_REFRESH_TOKEN || cached.refresh_token;
      }
    } catch {
      // ignore corrupt cache
    }
  }

  const baseUrl = env('HIVEBRITE_BASE_URL');
  const clientId = env('HIVEBRITE_CLIENT_ID');
  const clientSecret = env('HIVEBRITE_CLIENT_SECRET');

  const body = {
    client_id: clientId,
    client_secret: clientSecret,
    scope: 'admin',
  };

  // Prefer refresh_token grant, fall back to password grant
  if (process.env.HIVEBRITE_REFRESH_TOKEN) {
    body.grant_type = 'refresh_token';
    body.refresh_token = process.env.HIVEBRITE_REFRESH_TOKEN;
  } else {
    body.grant_type = 'password';
    body.admin_email = env('HIVEBRITE_ADMIN_EMAIL');
    body.password = env('HIVEBRITE_ADMIN_PASSWORD');
  }

  const resp = await fetch(`${baseUrl.replace(/\/+$/, '')}/oauth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(body),
  });

  if (!resp.ok) {
    const text = await resp.text();
    console.error(`ERROR: OAuth token request failed (${resp.status}): ${text}`);
    process.exit(1);
  }

  const data = await resp.json();
  _cachedAccessToken = data.access_token;
  _tokenExpiresAt = Date.now() + (data.expires_in || 7200) * 1000;

  // Cache to disk (including refresh_token for future runs)
  try {
    const cacheDir = dirname(OAUTH_TOKEN_PATH);
    if (!existsSync(cacheDir)) mkdirSync(cacheDir, { recursive: true });
    writeFileSync(OAUTH_TOKEN_PATH, JSON.stringify({
      access_token: _cachedAccessToken,
      refresh_token: data.refresh_token || process.env.HIVEBRITE_REFRESH_TOKEN || null,
      expires_at: _tokenExpiresAt,
    }), 'utf8');
  } catch {
    // non-fatal
  }

  return _cachedAccessToken;
}

// ── Config (lazy via Proxy) ──────────────────────────────────────────────────

let _cfg;
function getCfg() {
  if (!_cfg) {
    _cfg = {
      maxResults: parseInt(process.env.HIVEBRITE_MAX_RESULTS || '25', 10),
    };
  }
  return _cfg;
}
const CFG = new Proxy({}, { get: (_, prop) => getCfg()[prop] });

// ── HTTP client with rate-limit retry ────────────────────────────────────────

function apiBase(version = 'v2') {
  return `${env('HIVEBRITE_BASE_URL').replace(/\/+$/, '')}/api/admin/${version}`;
}

async function apiFetch(path, options = {}, retries = 3) {
  const token = await getAccessToken();
  const url = path.startsWith('http') ? path : `${apiBase(options._apiVersion || 'v2')}${path}`;
  delete options._apiVersion;

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Accept': 'application/json',
    ...options.headers,
  };

  if (options.body && typeof options.body === 'string') {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  }

  for (let attempt = 1; attempt <= retries; attempt++) {
    const resp = await fetch(url, { ...options, headers });

    if (resp.status === 429) {
      const retryAfter = parseInt(resp.headers.get('retry-after') || '5', 10);
      const backoff = retryAfter * 1000 * attempt;
      if (attempt < retries) {
        console.error(`Rate limited — retrying in ${(backoff / 1000).toFixed(0)}s (attempt ${attempt}/${retries})`);
        await new Promise(r => setTimeout(r, backoff));
        continue;
      }
    }

    if (resp.status === 204) return { _headers: resp.headers, _status: 204 };

    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }

    if (!resp.ok) {
      const msg = json?.message || json?.error || json?.errors?.[0]?.message || body || resp.statusText;
      const err = new Error(msg);
      err.statusCode = resp.status;
      throw err;
    }

    // Attach pagination headers for list endpoints
    if (json && typeof json === 'object') {
      json._pagination = {
        total: resp.headers.get('x-total') ? parseInt(resp.headers.get('x-total'), 10) : null,
        page: resp.headers.get('x-page') ? parseInt(resp.headers.get('x-page'), 10) : null,
        perPage: resp.headers.get('x-per-page') ? parseInt(resp.headers.get('x-per-page'), 10) : null,
        link: resp.headers.get('link') || null,
      };
    }

    return json;
  }
}

// Helper for v1 endpoints
async function apiFetchV1(path, options = {}, retries = 3) {
  return apiFetch(path, { ...options, _apiVersion: 'v1' }, retries);
}

// Helper for v3 endpoints
async function apiFetchV3(path, options = {}, retries = 3) {
  return apiFetch(path, { ...options, _apiVersion: 'v3' }, retries);
}

// ── Error wrapper ────────────────────────────────────────────────────────────

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

// ── Formatting helpers ───────────────────────────────────────────────────────

function truncate(str, len = 80) {
  if (!str) return '';
  const clean = String(str).replace(/\n/g, ' ').trim();
  return clean.length > len ? clean.substring(0, len) + '...' : clean;
}

function fmtDate(d) {
  if (!d) return '—';
  return typeof d === 'string' ? d.substring(0, 10) : new Date(d).toISOString().substring(0, 10);
}

// ── Pagination display helper ────────────────────────────────────────────────

function showPagination(data) {
  const p = data?._pagination;
  if (!p || !p.total) return;
  const parts = [];
  if (p.page) parts.push(`page ${p.page}`);
  if (p.perPage) parts.push(`${p.perPage}/page`);
  if (p.total) parts.push(`${p.total} total`);
  if (parts.length) console.log(`\nPagination: ${parts.join(' | ')}`);
}

// ── List display helper ──────────────────────────────────────────────────────

function displayList(items, labelFn, data) {
  if (!items || !items.length) {
    console.log('No results found.');
    return;
  }
  for (const item of items) {
    console.log(labelFn(item));
  }
  console.log(`\n${items.length} result(s)`);
  showPagination(data);
}

// ── Query string builder ─────────────────────────────────────────────────────

function buildParams(options) {
  const params = new URLSearchParams();
  params.set('per_page', String(options.perPage || options.limit || CFG.maxResults));
  if (options.page) params.set('page', String(options.page));
  return params;
}

// ═══════════════════════════════════════════════════════════════════════════════
// 1. ME
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdMe() {
  const data = await apiFetch('/me');
  const u = data;
  console.log(`Current Admin`);
  console.log(`  ID:         ${u.id || '—'}`);
  console.log(`  Name:       ${[u.firstname, u.lastname].filter(Boolean).join(' ') || '—'}`);
  console.log(`  Email:      ${u.email || '—'}`);
  console.log(`  Role:       ${u.role || '—'}`);
  console.log(`  Created:    ${fmtDate(u.created_at)}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 2. SETTINGS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdSettingsCustomizableAttributes(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/settings/customizable_attributes?${params}`);
  const items = Array.isArray(data) ? data : data?.customizable_attributes || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.name || '').padEnd(30)} type: ${a.attribute_type || '—'}`, data);
}

async function cmdSettingsFieldsOfStudy(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/settings/fields_of_study?${params}`);
  const items = Array.isArray(data) ? data : data?.fields_of_study || [];
  displayList(items, f => `  ${String(f.id).padEnd(8)} ${f.name || '—'}`, data);
}

async function cmdSettingsIndustries(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/settings/industries?${params}`);
  const items = Array.isArray(data) ? data : data?.industries || [];
  displayList(items, i => `  ${String(i.id).padEnd(8)} ${i.name || '—'}`, data);
}

async function cmdSettingsJobFunctions(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/settings/job_functions?${params}`);
  const items = Array.isArray(data) ? data : data?.job_functions || [];
  displayList(items, j => `  ${String(j.id).padEnd(8)} ${j.name || '—'}`, data);
}

async function cmdSettingsCurrencies(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/settings/currencies?${params}`);
  const items = Array.isArray(data) ? data : data?.currencies || [];
  displayList(items, c => `  ${String(c.id || '').padEnd(8)} ${(c.code || '').padEnd(6)} ${c.name || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 3. NETWORK
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdNetworkInfo() {
  const data = await apiFetch('/network');
  const n = data?.network || data;
  console.log(`Network`);
  console.log(`  ID:         ${n.id || '—'}`);
  console.log(`  Name:       ${n.name || '—'}`);
  console.log(`  Subdomain:  ${n.subdomain || '—'}`);
  console.log(`  URL:        ${n.url || '—'}`);
  console.log(`  Locale:     ${n.locale || '—'}`);
  console.log(`  Created:    ${fmtDate(n.created_at)}`);
}

async function cmdNetworkSubNetworks(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/network/sub_networks?${params}`);
  const items = Array.isArray(data) ? data : data?.sub_networks || [];
  displayList(items, s => `  ${String(s.id).padEnd(8)} ${(s.name || '').padEnd(30)} ${s.subdomain || '—'}`, data);
}

async function cmdNetworkCitizenships(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/network/citizenships?${params}`);
  const items = Array.isArray(data) ? data : data?.citizenships || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${c.name || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 4. USERS
// ═══════════════════════════════════════════════════════════════════════════════

function userLabel(u) {
  const name = [u.firstname, u.lastname].filter(Boolean).join(' ') || '(no name)';
  return `#${String(u.id).padEnd(8)} ${name.padEnd(30)} ${(u.email || '').padEnd(30)} ${u.role || ''}`;
}

async function cmdUsersList(options) {
  const params = buildParams(options);
  if (options.query) params.set('q', options.query);
  const data = await apiFetch(`/admin/users?${params}`);
  const items = Array.isArray(data) ? data : data?.users || [];
  displayList(items, userLabel, data);
}

async function cmdUsersRead(options) {
  const u = await apiFetch(`/admin/users/${options.id}`);
  const user = u?.user || u;
  console.log(`User #${user.id}`);
  console.log(`  Name:       ${[user.firstname, user.lastname].filter(Boolean).join(' ') || '—'}`);
  console.log(`  Email:      ${user.email || '—'}`);
  console.log(`  Role:       ${user.role || '—'}`);
  console.log(`  Headline:   ${user.headline || '—'}`);
  console.log(`  Location:   ${user.location || '—'}`);
  console.log(`  Phone:      ${user.phone || '—'}`);
  console.log(`  Created:    ${fmtDate(user.created_at)}`);
  console.log(`  Updated:    ${fmtDate(user.updated_at)}`);
  console.log(`  Confirmed:  ${user.confirmed ? 'Yes' : 'No'}`);
}

async function cmdUsersCreate(options) {
  const body = {};
  if (options.email) body.email = options.email;
  if (options.firstname) body.firstname = options.firstname;
  if (options.lastname) body.lastname = options.lastname;
  if (options.phone) body.phone = options.phone;
  if (options.headline) body.headline = options.headline;
  if (options.location) body.location = options.location;

  if (!body.email) {
    console.error('ERROR: --email is required');
    process.exit(1);
  }

  const result = await apiFetch('/admin/users', {
    method: 'POST',
    body: JSON.stringify({ user: body }),
  });
  const u = result?.user || result;
  console.log(`Created user #${u.id}`);
}

async function cmdUsersUpdate(options) {
  const body = {};
  if (options.email) body.email = options.email;
  if (options.firstname) body.firstname = options.firstname;
  if (options.lastname) body.lastname = options.lastname;
  if (options.phone) body.phone = options.phone;
  if (options.headline) body.headline = options.headline;
  if (options.location) body.location = options.location;

  await apiFetch(`/admin/users/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ user: body }),
  });
  console.log(`Updated user #${options.id}`);
}

async function cmdUsersDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await apiFetch(`/admin/users/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted user #${options.id}`);
}

async function cmdUsersExperiences(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/admin/users/${options.userId}/experiences?${params}`);
  const items = Array.isArray(data) ? data : data?.experiences || [];
  displayList(items, e => `  ${String(e.id).padEnd(8)} ${(e.title || '').padEnd(25)} @ ${(e.organization_name || '').padEnd(20)} ${fmtDate(e.start_date)}–${fmtDate(e.end_date)}`, data);
}

async function cmdUsersEducations(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/admin/users/${options.userId}/educations?${params}`);
  const items = Array.isArray(data) ? data : data?.educations || [];
  displayList(items, e => `  ${String(e.id).padEnd(8)} ${(e.degree || '').padEnd(20)} @ ${(e.school_name || '').padEnd(25)} ${fmtDate(e.start_date)}–${fmtDate(e.end_date)}`, data);
}

async function cmdUsersNotificationSettings(options) {
  const data = await apiFetch(`/admin/users/${options.userId}/notification_settings`);
  const s = data?.notification_settings || data;
  console.log(`Notification settings for user #${options.userId}`);
  console.log(JSON.stringify(s, null, 2));
}

async function cmdUsersPostalAddresses(options) {
  const data = await apiFetch(`/admin/users/${options.userId}/postal_addresses`);
  const items = Array.isArray(data) ? data : data?.postal_addresses || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.address_1 || '').padEnd(30)} ${(a.city || '').padEnd(15)} ${a.country || '—'}`, data);
}

async function cmdUsersGroupMembership(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/admin/users/${options.userId}/groups?${params}`);
  const items = Array.isArray(data) ? data : data?.groups || [];
  displayList(items, g => `  ${String(g.id).padEnd(8)} ${g.name || '—'}`, data);
}

async function cmdUsersFindByField(options) {
  const params = new URLSearchParams();
  if (options.field) params.set('field', options.field);
  if (options.value) params.set('value', options.value);
  const data = await apiFetch(`/admin/users/find_by_field?${params}`);
  const u = data?.user || data;
  if (u?.id) {
    console.log(userLabel(u));
  } else {
    console.log('No user found.');
  }
}

async function cmdUsersNotify(options) {
  const body = {};
  if (options.subject) body.subject = options.subject;
  if (options.message) body.message = options.message;

  await apiFetch(`/admin/users/${options.id}/notify`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
  console.log(`Notification sent to user #${options.id}`);
}

async function cmdUsersActivate(options) {
  await apiFetch(`/admin/users/${options.id}/activate`, { method: 'PUT' });
  console.log(`Activated user #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 5. EXPERIENCES (standalone)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdExperiencesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/experiences?${params}`);
  const items = Array.isArray(data) ? data : data?.experiences || [];
  displayList(items, e => `  ${String(e.id).padEnd(8)} ${(e.title || '').padEnd(25)} @ ${(e.organization_name || '').padEnd(20)} user:${e.user_id || '—'}`, data);
}

async function cmdExperiencesRead(options) {
  const data = await apiFetch(`/experiences/${options.id}`);
  const e = data?.experience || data;
  console.log(`Experience #${e.id}`);
  console.log(`  Title:        ${e.title || '—'}`);
  console.log(`  Organization: ${e.organization_name || '—'}`);
  console.log(`  Location:     ${e.location || '—'}`);
  console.log(`  Start:        ${fmtDate(e.start_date)}`);
  console.log(`  End:          ${fmtDate(e.end_date)}`);
  console.log(`  Current:      ${e.current ? 'Yes' : 'No'}`);
  console.log(`  User ID:      ${e.user_id || '—'}`);
}

async function cmdExperiencesCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.title) body.title = options.title;
  if (options.organization) body.organization_name = options.organization;
  if (options.location) body.location = options.location;
  if (options.startDate) body.start_date = options.startDate;
  if (options.endDate) body.end_date = options.endDate;
  if (options.current) body.current = true;
  if (options.description) body.description = options.description;

  const result = await apiFetch('/experiences', {
    method: 'POST',
    body: JSON.stringify({ experience: body }),
  });
  const e = result?.experience || result;
  console.log(`Created experience #${e.id}`);
}

async function cmdExperiencesUpdate(options) {
  const body = {};
  if (options.title) body.title = options.title;
  if (options.organization) body.organization_name = options.organization;
  if (options.location) body.location = options.location;
  if (options.startDate) body.start_date = options.startDate;
  if (options.endDate) body.end_date = options.endDate;
  if (options.current) body.current = true;
  if (options.description) body.description = options.description;

  await apiFetch(`/experiences/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ experience: body }),
  });
  console.log(`Updated experience #${options.id}`);
}

async function cmdExperiencesDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await apiFetch(`/experiences/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted experience #${options.id}`);
}

async function cmdExperiencesCustomizableAttributes(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/experiences/customizable_attributes?${params}`);
  const items = Array.isArray(data) ? data : data?.customizable_attributes || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.name || '').padEnd(30)} type: ${a.attribute_type || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 6. EDUCATIONS (standalone)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdEducationsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/educations?${params}`);
  const items = Array.isArray(data) ? data : data?.educations || [];
  displayList(items, e => `  ${String(e.id).padEnd(8)} ${(e.degree || '').padEnd(20)} @ ${(e.school_name || '').padEnd(25)} user:${e.user_id || '—'}`, data);
}

async function cmdEducationsRead(options) {
  const data = await apiFetch(`/educations/${options.id}`);
  const e = data?.education || data;
  console.log(`Education #${e.id}`);
  console.log(`  Degree:     ${e.degree || '—'}`);
  console.log(`  School:     ${e.school_name || '—'}`);
  console.log(`  Field:      ${e.field_of_study || '—'}`);
  console.log(`  Start:      ${fmtDate(e.start_date)}`);
  console.log(`  End:        ${fmtDate(e.end_date)}`);
  console.log(`  User ID:    ${e.user_id || '—'}`);
}

async function cmdEducationsCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.degree) body.degree = options.degree;
  if (options.school) body.school_name = options.school;
  if (options.field) body.field_of_study = options.field;
  if (options.startDate) body.start_date = options.startDate;
  if (options.endDate) body.end_date = options.endDate;
  if (options.description) body.description = options.description;

  const result = await apiFetch('/educations', {
    method: 'POST',
    body: JSON.stringify({ education: body }),
  });
  const e = result?.education || result;
  console.log(`Created education #${e.id}`);
}

async function cmdEducationsUpdate(options) {
  const body = {};
  if (options.degree) body.degree = options.degree;
  if (options.school) body.school_name = options.school;
  if (options.field) body.field_of_study = options.field;
  if (options.startDate) body.start_date = options.startDate;
  if (options.endDate) body.end_date = options.endDate;
  if (options.description) body.description = options.description;

  await apiFetch(`/educations/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ education: body }),
  });
  console.log(`Updated education #${options.id}`);
}

async function cmdEducationsDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await apiFetch(`/educations/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted education #${options.id}`);
}

async function cmdEducationsCustomizableAttributes(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/educations/customizable_attributes?${params}`);
  const items = Array.isArray(data) ? data : data?.customizable_attributes || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.name || '').padEnd(30)} type: ${a.attribute_type || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 7. EMAILINGS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdEmailingCategoriesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/emailing/categories?${params}`);
  const items = Array.isArray(data) ? data : data?.categories || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${c.name || '—'}`, data);
}

async function cmdEmailingCategoriesRead(options) {
  const data = await apiFetch(`/emailing/categories/${options.id}`);
  const c = data?.category || data;
  console.log(`Emailing Category #${c.id}`);
  console.log(`  Name:       ${c.name || '—'}`);
  console.log(`  Created:    ${fmtDate(c.created_at)}`);
}

async function cmdEmailingCategoriesCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const result = await apiFetch('/emailing/categories', {
    method: 'POST',
    body: JSON.stringify({ category: { name: options.name } }),
  });
  const c = result?.category || result;
  console.log(`Created emailing category #${c.id}`);
}

async function cmdEmailingCategoriesUpdate(options) {
  await apiFetch(`/emailing/categories/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ category: { name: options.name } }),
  });
  console.log(`Updated emailing category #${options.id}`);
}

async function cmdEmailingCategoriesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/emailing/categories/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted emailing category #${options.id}`);
}

async function cmdEmailingCampaignsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/emailing/campaigns?${params}`);
  const items = Array.isArray(data) ? data : data?.campaigns || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${(c.subject || c.name || '').padEnd(40)} status: ${c.status || '—'}`, data);
}

async function cmdEmailingCampaignsRead(options) {
  const data = await apiFetch(`/emailing/campaigns/${options.id}`);
  const c = data?.campaign || data;
  console.log(`Emailing Campaign #${c.id}`);
  console.log(`  Subject:    ${c.subject || '—'}`);
  console.log(`  Name:       ${c.name || '—'}`);
  console.log(`  Status:     ${c.status || '—'}`);
  console.log(`  From:       ${c.from_name || '—'} <${c.from_email || '—'}>`);
  console.log(`  Created:    ${fmtDate(c.created_at)}`);
  console.log(`  Sent at:    ${fmtDate(c.sent_at)}`);
}

async function cmdEmailingCampaignsCreate(options) {
  const body = {};
  if (options.subject) body.subject = options.subject;
  if (options.name) body.name = options.name;
  if (options.fromName) body.from_name = options.fromName;
  if (options.fromEmail) body.from_email = options.fromEmail;
  if (options.categoryId) body.category_id = options.categoryId;
  if (options.body) body.body = options.body;

  if (!body.subject && !body.name) {
    console.error('ERROR: --subject or --name is required');
    process.exit(1);
  }

  const result = await apiFetch('/emailing/campaigns', {
    method: 'POST',
    body: JSON.stringify({ campaign: body }),
  });
  const c = result?.campaign || result;
  console.log(`Created emailing campaign #${c.id}`);
}

async function cmdEmailingCampaignsUpdate(options) {
  const body = {};
  if (options.subject) body.subject = options.subject;
  if (options.name) body.name = options.name;
  if (options.fromName) body.from_name = options.fromName;
  if (options.fromEmail) body.from_email = options.fromEmail;
  if (options.body) body.body = options.body;

  await apiFetch(`/emailing/campaigns/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ campaign: body }),
  });
  console.log(`Updated emailing campaign #${options.id}`);
}

async function cmdEmailingCampaignsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/emailing/campaigns/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted emailing campaign #${options.id}`);
}

async function cmdEmailingCampaignsSend(options) {
  await apiFetch(`/emailing/campaigns/${options.id}/send`, { method: 'POST' });
  console.log(`Sent emailing campaign #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 8. GROUPS
// ═══════════════════════════════════════════════════════════════════════════════

function groupLabel(g) {
  return `#${String(g.id).padEnd(8)} ${(g.name || '(unnamed)').padEnd(35)} members: ${g.users_count ?? '—'}`;
}

async function cmdGroupsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/groups?${params}`);
  const items = Array.isArray(data) ? data : data?.groups || [];
  displayList(items, groupLabel, data);
}

async function cmdGroupsRead(options) {
  const data = await apiFetch(`/groups/${options.id}`);
  const g = data?.group || data;
  console.log(`Group #${g.id}`);
  console.log(`  Name:       ${g.name || '—'}`);
  console.log(`  Slug:       ${g.slug || '—'}`);
  console.log(`  Members:    ${g.users_count ?? '—'}`);
  console.log(`  Visible:    ${g.visible ? 'Yes' : 'No'}`);
  console.log(`  Created:    ${fmtDate(g.created_at)}`);
  if (g.description) console.log(`  Desc:       ${truncate(g.description, 200)}`);
}

async function cmdGroupsCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.description) body.description = options.description;
  if (options.slug) body.slug = options.slug;

  const result = await apiFetch('/groups', {
    method: 'POST',
    body: JSON.stringify({ group: body }),
  });
  const g = result?.group || result;
  console.log(`Created group #${g.id}`);
}

async function cmdGroupsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.description) body.description = options.description;
  if (options.slug) body.slug = options.slug;

  await apiFetch(`/groups/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ group: body }),
  });
  console.log(`Updated group #${options.id}`);
}

async function cmdGroupsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/groups/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted group #${options.id}`);
}

async function cmdGroupUsersList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/groups/${options.groupId}/users?${params}`);
  const items = Array.isArray(data) ? data : data?.users || [];
  displayList(items, userLabel, data);
}

async function cmdGroupUsersAdd(options) {
  await apiFetch(`/groups/${options.groupId}/users`, {
    method: 'POST',
    body: JSON.stringify({ user_id: options.userId }),
  });
  console.log(`Added user #${options.userId} to group #${options.groupId}`);
}

async function cmdGroupUsersRemove(options) {
  if (!options.confirm) { console.error('ERROR: Remove requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/groups/${options.groupId}/users/${options.userId}`, { method: 'DELETE' });
  console.log(`Removed user #${options.userId} from group #${options.groupId}`);
}

async function cmdGroupTopicCategories(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/groups/${options.groupId}/topic_categories?${params}`);
  const items = Array.isArray(data) ? data : data?.topic_categories || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${c.name || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 9. COMPANIES
// ═══════════════════════════════════════════════════════════════════════════════

function companyLabel(c) {
  return `#${String(c.id).padEnd(8)} ${(c.name || '(unnamed)').padEnd(35)} ${(c.industry || '').padEnd(20)} ${c.city || ''}`;
}

async function cmdCompaniesList(options) {
  const params = buildParams(options);
  if (options.query) params.set('q', options.query);
  const data = await apiFetch(`/companies?${params}`);
  const items = Array.isArray(data) ? data : data?.companies || [];
  displayList(items, companyLabel, data);
}

async function cmdCompaniesRead(options) {
  const data = await apiFetch(`/companies/${options.id}`);
  const c = data?.company || data;
  console.log(`Company #${c.id}`);
  console.log(`  Name:       ${c.name || '—'}`);
  console.log(`  Industry:   ${c.industry || '—'}`);
  console.log(`  Website:    ${c.website || '—'}`);
  console.log(`  City:       ${c.city || '—'}`);
  console.log(`  Country:    ${c.country || '—'}`);
  console.log(`  Size:       ${c.size || '—'}`);
  console.log(`  Phone:      ${c.phone || '—'}`);
  console.log(`  Created:    ${fmtDate(c.created_at)}`);
}

async function cmdCompaniesCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.industry) body.industry = options.industry;
  if (options.website) body.website = options.website;
  if (options.city) body.city = options.city;
  if (options.country) body.country = options.country;
  if (options.phone) body.phone = options.phone;

  const result = await apiFetch('/companies', {
    method: 'POST',
    body: JSON.stringify({ company: body }),
  });
  const c = result?.company || result;
  console.log(`Created company #${c.id}`);
}

async function cmdCompaniesUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.industry) body.industry = options.industry;
  if (options.website) body.website = options.website;
  if (options.city) body.city = options.city;
  if (options.country) body.country = options.country;
  if (options.phone) body.phone = options.phone;

  await apiFetch(`/companies/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ company: body }),
  });
  console.log(`Updated company #${options.id}`);
}

async function cmdCompaniesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/companies/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted company #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 10. NEWS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdNewsCategoriesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/news/categories?${params}`);
  const items = Array.isArray(data) ? data : data?.categories || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${c.name || '—'}`, data);
}

async function cmdNewsCategoriesRead(options) {
  const data = await apiFetch(`/news/categories/${options.id}`);
  const c = data?.category || data;
  console.log(`News Category #${c.id}`);
  console.log(`  Name:       ${c.name || '—'}`);
  console.log(`  Created:    ${fmtDate(c.created_at)}`);
}

async function cmdNewsCategoriesCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const result = await apiFetch('/news/categories', {
    method: 'POST',
    body: JSON.stringify({ category: { name: options.name } }),
  });
  const c = result?.category || result;
  console.log(`Created news category #${c.id}`);
}

async function cmdNewsCategoriesUpdate(options) {
  await apiFetch(`/news/categories/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ category: { name: options.name } }),
  });
  console.log(`Updated news category #${options.id}`);
}

async function cmdNewsCategoriesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/news/categories/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted news category #${options.id}`);
}

async function cmdNewsPostsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/news?${params}`);
  const items = Array.isArray(data) ? data : data?.news || [];
  displayList(items, n => `  ${String(n.id).padEnd(8)} ${fmtDate(n.published_at).padEnd(12)} ${truncate(n.title, 50)}`, data);
}

async function cmdNewsPostsRead(options) {
  const data = await apiFetch(`/news/${options.id}`);
  const n = data?.news_item || data?.news || data;
  console.log(`News #${n.id}`);
  console.log(`  Title:      ${n.title || '—'}`);
  console.log(`  Status:     ${n.status || '—'}`);
  console.log(`  Published:  ${fmtDate(n.published_at)}`);
  console.log(`  Author:     ${n.author_name || '—'}`);
  console.log(`  Category:   ${n.category?.name || n.category_id || '—'}`);
  console.log(`  Created:    ${fmtDate(n.created_at)}`);
  if (n.body) console.log(`\n  Body:\n  ${truncate(n.body, 500)}`);
}

async function cmdNewsPostsCreate(options) {
  if (!options.title) { console.error('ERROR: --title is required'); process.exit(1); }
  const body = { title: options.title };
  if (options.body) body.body = options.body;
  if (options.categoryId) body.category_id = options.categoryId;
  if (options.status) body.status = options.status;

  const result = await apiFetch('/news', {
    method: 'POST',
    body: JSON.stringify({ news: body }),
  });
  const n = result?.news_item || result?.news || result;
  console.log(`Created news #${n.id}`);
}

async function cmdNewsPostsUpdate(options) {
  const body = {};
  if (options.title) body.title = options.title;
  if (options.body) body.body = options.body;
  if (options.categoryId) body.category_id = options.categoryId;
  if (options.status) body.status = options.status;

  await apiFetch(`/news/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ news: body }),
  });
  console.log(`Updated news #${options.id}`);
}

async function cmdNewsPostsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/news/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted news #${options.id}`);
}

async function cmdNewsPostsDuplicate(options) {
  const result = await apiFetch(`/news/${options.id}/duplicate`, { method: 'POST' });
  const n = result?.news_item || result?.news || result;
  console.log(`Duplicated news #${options.id} → new #${n.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 11. ROLES
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdRolesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/roles?${params}`);
  const items = Array.isArray(data) ? data : data?.roles || [];
  displayList(items, r => `  ${String(r.id).padEnd(8)} ${r.name || '—'}`, data);
}

async function cmdRolesRead(options) {
  const data = await apiFetch(`/roles/${options.id}`);
  const r = data?.role || data;
  console.log(`Role #${r.id}`);
  console.log(`  Name:       ${r.name || '—'}`);
  console.log(`  Created:    ${fmtDate(r.created_at)}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 12. BUSINESS OPPORTUNITIES
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdBusinessOpportunitiesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/business_opportunities?${params}`);
  const items = Array.isArray(data) ? data : data?.business_opportunities || [];
  displayList(items, b => `  ${String(b.id).padEnd(8)} ${(b.title || '').padEnd(35)} status: ${b.status || '—'}`, data);
}

async function cmdBusinessOpportunitiesRead(options) {
  const data = await apiFetch(`/business_opportunities/${options.id}`);
  const b = data?.business_opportunity || data;
  console.log(`Business Opportunity #${b.id}`);
  console.log(`  Title:      ${b.title || '—'}`);
  console.log(`  Status:     ${b.status || '—'}`);
  console.log(`  Type:       ${b.opportunity_type || '—'}`);
  console.log(`  Location:   ${b.location || '—'}`);
  console.log(`  Company:    ${b.company_name || '—'}`);
  console.log(`  Created:    ${fmtDate(b.created_at)}`);
  if (b.description) console.log(`\n  Desc:\n  ${truncate(b.description, 300)}`);
}

async function cmdBusinessOpportunitiesCreate(options) {
  if (!options.title) { console.error('ERROR: --title is required'); process.exit(1); }
  const body = { title: options.title };
  if (options.type) body.opportunity_type = options.type;
  if (options.location) body.location = options.location;
  if (options.company) body.company_name = options.company;
  if (options.description) body.description = options.description;
  if (options.status) body.status = options.status;

  const result = await apiFetch('/business_opportunities', {
    method: 'POST',
    body: JSON.stringify({ business_opportunity: body }),
  });
  const b = result?.business_opportunity || result;
  console.log(`Created business opportunity #${b.id}`);
}

async function cmdBusinessOpportunitiesUpdate(options) {
  const body = {};
  if (options.title) body.title = options.title;
  if (options.type) body.opportunity_type = options.type;
  if (options.location) body.location = options.location;
  if (options.company) body.company_name = options.company;
  if (options.description) body.description = options.description;
  if (options.status) body.status = options.status;

  await apiFetch(`/business_opportunities/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ business_opportunity: body }),
  });
  console.log(`Updated business opportunity #${options.id}`);
}

async function cmdBusinessOpportunitiesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/business_opportunities/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted business opportunity #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 13. RECEIPTS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdReceiptsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/receipts?${params}`);
  const items = Array.isArray(data) ? data : data?.receipts || [];
  displayList(items, r => `  ${String(r.id).padEnd(8)} ${(r.status || '').padEnd(12)} ${fmtDate(r.created_at).padEnd(12)} ${r.amount || '—'} ${r.currency || ''}`, data);
}

async function cmdReceiptsRead(options) {
  const data = await apiFetch(`/receipts/${options.id}`);
  const r = data?.receipt || data;
  console.log(`Receipt #${r.id}`);
  console.log(`  Status:     ${r.status || '—'}`);
  console.log(`  Amount:     ${r.amount || '—'} ${r.currency || ''}`);
  console.log(`  User ID:    ${r.user_id || '—'}`);
  console.log(`  Created:    ${fmtDate(r.created_at)}`);
  console.log(`  Updated:    ${fmtDate(r.updated_at)}`);
}

async function cmdReceiptsUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;

  await apiFetch(`/receipts/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ receipt: body }),
  });
  console.log(`Updated receipt #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 14. PAGES (Customizable)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdPagesCustomizableList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/pages?${params}`);
  const items = Array.isArray(data) ? data : data?.pages || [];
  displayList(items, p => `  ${String(p.id).padEnd(8)} ${(p.title || p.name || '').padEnd(40)} ${p.status || '—'}`, data);
}

async function cmdPagesCustomizableRead(options) {
  const data = await apiFetch(`/pages/${options.id}`);
  const p = data?.page || data;
  console.log(`Page #${p.id}`);
  console.log(`  Title:      ${p.title || p.name || '—'}`);
  console.log(`  Slug:       ${p.slug || '—'}`);
  console.log(`  Status:     ${p.status || '—'}`);
  console.log(`  Created:    ${fmtDate(p.created_at)}`);
}

async function cmdPagesCustomizableCreate(options) {
  if (!options.title) { console.error('ERROR: --title is required'); process.exit(1); }
  const body = { title: options.title };
  if (options.slug) body.slug = options.slug;
  if (options.body) body.body = options.body;

  const result = await apiFetch('/pages', {
    method: 'POST',
    body: JSON.stringify({ page: body }),
  });
  const p = result?.page || result;
  console.log(`Created page #${p.id}`);
}

async function cmdPagesCustomizableUpdate(options) {
  const body = {};
  if (options.title) body.title = options.title;
  if (options.slug) body.slug = options.slug;
  if (options.body) body.body = options.body;

  await apiFetch(`/pages/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ page: body }),
  });
  console.log(`Updated page #${options.id}`);
}

async function cmdPagesCustomizableDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/pages/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted page #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 15. APPROVALS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdApprovalsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/approvals?${params}`);
  const items = Array.isArray(data) ? data : data?.approvals || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.status || '').padEnd(12)} type: ${a.approvable_type || '—'}  user: ${a.user_id || '—'}`, data);
}

async function cmdApprovalsRead(options) {
  const data = await apiFetch(`/approvals/${options.id}`);
  const a = data?.approval || data;
  console.log(`Approval #${a.id}`);
  console.log(`  Status:     ${a.status || '—'}`);
  console.log(`  Type:       ${a.approvable_type || '—'}`);
  console.log(`  User ID:    ${a.user_id || '—'}`);
  console.log(`  Created:    ${fmtDate(a.created_at)}`);
}

async function cmdApprovalsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/approvals/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted approval #${options.id}`);
}

async function cmdApprovalsReject(options) {
  await apiFetch(`/approvals/${options.id}/reject`, { method: 'PUT' });
  console.log(`Rejected approval #${options.id}`);
}

async function cmdApprovalsApprove(options) {
  await apiFetch(`/approvals/${options.id}/approve`, { method: 'PUT' });
  console.log(`Approved approval #${options.id}`);
}

async function cmdApprovalsLinkToUser(options) {
  await apiFetch(`/approvals/${options.id}/link_to_user`, {
    method: 'PUT',
    body: JSON.stringify({ user_id: options.userId }),
  });
  console.log(`Linked approval #${options.id} to user #${options.userId}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 16. VERSIONS (deleted items)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdVersionsList(options) {
  const params = buildParams(options);
  if (options.itemType) params.set('item_type', options.itemType);
  const data = await apiFetch(`/versions?${params}`);
  const items = Array.isArray(data) ? data : data?.versions || [];
  displayList(items, v => `  ${String(v.id).padEnd(8)} ${(v.item_type || '').padEnd(20)} item_id: ${v.item_id || '—'}  ${fmtDate(v.created_at)}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 17. COMMENTS (v3)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdCommentsList(options) {
  const params = buildParams(options);
  if (options.commentableType) params.set('commentable_type', options.commentableType);
  if (options.commentableId) params.set('commentable_id', options.commentableId);
  const data = await apiFetchV3(`/comments?${params}`);
  const items = Array.isArray(data) ? data : data?.comments || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} user:${String(c.user_id || '').padEnd(6)} ${fmtDate(c.created_at).padEnd(12)} ${truncate(c.body, 60)}`, data);
}

async function cmdCommentsRead(options) {
  const data = await apiFetchV3(`/comments/${options.id}`);
  const c = data?.comment || data;
  console.log(`Comment #${c.id}`);
  console.log(`  User ID:    ${c.user_id || '—'}`);
  console.log(`  Type:       ${c.commentable_type || '—'}`);
  console.log(`  Target ID:  ${c.commentable_id || '—'}`);
  console.log(`  Created:    ${fmtDate(c.created_at)}`);
  if (c.body) console.log(`\n  Body:\n  ${truncate(c.body, 500)}`);
}

async function cmdCommentsCreate(options) {
  if (!options.body) { console.error('ERROR: --body is required'); process.exit(1); }
  const body = { body: options.body };
  if (options.commentableType) body.commentable_type = options.commentableType;
  if (options.commentableId) body.commentable_id = options.commentableId;

  const result = await apiFetchV3('/comments', {
    method: 'POST',
    body: JSON.stringify({ comment: body }),
  });
  const c = result?.comment || result;
  console.log(`Created comment #${c.id}`);
}

async function cmdCommentsUpdate(options) {
  const body = {};
  if (options.body) body.body = options.body;

  await apiFetchV3(`/comments/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ comment: body }),
  });
  console.log(`Updated comment #${options.id}`);
}

async function cmdCommentsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetchV3(`/comments/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted comment #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 18. POSTS (v3)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdPostsList(options) {
  const params = buildParams(options);
  const data = await apiFetchV3(`/posts?${params}`);
  const items = Array.isArray(data) ? data : data?.posts || [];
  displayList(items, p => `  ${String(p.id).padEnd(8)} user:${String(p.user_id || '').padEnd(6)} ${fmtDate(p.created_at).padEnd(12)} ${truncate(p.body || p.title, 50)}`, data);
}

async function cmdPostsRead(options) {
  const data = await apiFetchV3(`/posts/${options.id}`);
  const p = data?.post || data;
  console.log(`Post #${p.id}`);
  console.log(`  User ID:    ${p.user_id || '—'}`);
  console.log(`  Created:    ${fmtDate(p.created_at)}`);
  console.log(`  Updated:    ${fmtDate(p.updated_at)}`);
  if (p.title) console.log(`  Title:      ${p.title}`);
  if (p.body) console.log(`\n  Body:\n  ${truncate(p.body, 500)}`);
}

async function cmdPostsCreate(options) {
  if (!options.body) { console.error('ERROR: --body is required'); process.exit(1); }
  const body = { body: options.body };
  if (options.title) body.title = options.title;
  if (options.groupId) body.group_id = options.groupId;

  const result = await apiFetchV3('/posts', {
    method: 'POST',
    body: JSON.stringify({ post: body }),
  });
  const p = result?.post || result;
  console.log(`Created post #${p.id}`);
}

async function cmdPostsUpdate(options) {
  const body = {};
  if (options.body) body.body = options.body;
  if (options.title) body.title = options.title;

  await apiFetchV3(`/posts/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ post: body }),
  });
  console.log(`Updated post #${options.id}`);
}

async function cmdPostsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetchV3(`/posts/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted post #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 19. NETWORK EVENTS
// ═══════════════════════════════════════════════════════════════════════════════

function eventLabel(e) {
  return `#${String(e.id).padEnd(8)} ${fmtDate(e.starts_at).padEnd(12)} ${(e.name || e.title || '').padEnd(35)} ${e.status || ''}`;
}

async function cmdEventsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/events?${params}`);
  const items = Array.isArray(data) ? data : data?.events || [];
  displayList(items, eventLabel, data);
}

async function cmdEventsRead(options) {
  const data = await apiFetch(`/events/${options.id}`);
  const e = data?.event || data;
  console.log(`Event #${e.id}`);
  console.log(`  Name:       ${e.name || e.title || '—'}`);
  console.log(`  Status:     ${e.status || '—'}`);
  console.log(`  Starts:     ${fmtDate(e.starts_at)}`);
  console.log(`  Ends:       ${fmtDate(e.ends_at)}`);
  console.log(`  Location:   ${e.location || '—'}`);
  console.log(`  Capacity:   ${e.capacity ?? '—'}`);
  console.log(`  Created:    ${fmtDate(e.created_at)}`);
  if (e.description) console.log(`\n  Desc:\n  ${truncate(e.description, 400)}`);
}

async function cmdEventsCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.startsAt) body.starts_at = options.startsAt;
  if (options.endsAt) body.ends_at = options.endsAt;
  if (options.location) body.location = options.location;
  if (options.capacity) body.capacity = parseInt(options.capacity, 10);
  if (options.description) body.description = options.description;

  const result = await apiFetch('/events', {
    method: 'POST',
    body: JSON.stringify({ event: body }),
  });
  const e = result?.event || result;
  console.log(`Created event #${e.id}`);
}

async function cmdEventsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.startsAt) body.starts_at = options.startsAt;
  if (options.endsAt) body.ends_at = options.endsAt;
  if (options.location) body.location = options.location;
  if (options.capacity) body.capacity = parseInt(options.capacity, 10);
  if (options.description) body.description = options.description;

  await apiFetch(`/events/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ event: body }),
  });
  console.log(`Updated event #${options.id}`);
}

async function cmdEventsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/events/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted event #${options.id}`);
}

async function cmdEventsCancel(options) {
  await apiFetch(`/events/${options.id}/cancel`, { method: 'PUT' });
  console.log(`Cancelled event #${options.id}`);
}

async function cmdEventsDuplicate(options) {
  const result = await apiFetch(`/events/${options.id}/duplicate`, { method: 'POST' });
  const e = result?.event || result;
  console.log(`Duplicated event #${options.id} → new #${e.id}`);
}

async function cmdEventsCustomizableAttributes(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/events/customizable_attributes?${params}`);
  const items = Array.isArray(data) ? data : data?.customizable_attributes || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.name || '').padEnd(30)} type: ${a.attribute_type || '—'}`, data);
}

// Event Tickets
async function cmdEventTicketsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/events/${options.eventId}/tickets?${params}`);
  const items = Array.isArray(data) ? data : data?.tickets || [];
  displayList(items, t => `  ${String(t.id).padEnd(8)} ${(t.name || '').padEnd(25)} price: ${t.price ?? '—'} ${t.currency || ''}  capacity: ${t.capacity ?? '—'}`, data);
}

async function cmdEventTicketsRead(options) {
  const data = await apiFetch(`/events/${options.eventId}/tickets/${options.id}`);
  const t = data?.ticket || data;
  console.log(`Ticket #${t.id}`);
  console.log(`  Name:       ${t.name || '—'}`);
  console.log(`  Price:      ${t.price ?? '—'} ${t.currency || ''}`);
  console.log(`  Capacity:   ${t.capacity ?? '—'}`);
  console.log(`  Status:     ${t.status || '—'}`);
}

async function cmdEventTicketsCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.price) body.price = parseFloat(options.price);
  if (options.capacity) body.capacity = parseInt(options.capacity, 10);
  if (options.currency) body.currency = options.currency;

  const result = await apiFetch(`/events/${options.eventId}/tickets`, {
    method: 'POST',
    body: JSON.stringify({ ticket: body }),
  });
  const t = result?.ticket || result;
  console.log(`Created ticket #${t.id}`);
}

async function cmdEventTicketsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.price) body.price = parseFloat(options.price);
  if (options.capacity) body.capacity = parseInt(options.capacity, 10);

  await apiFetch(`/events/${options.eventId}/tickets/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ ticket: body }),
  });
  console.log(`Updated ticket #${options.id}`);
}

async function cmdEventTicketsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/events/${options.eventId}/tickets/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted ticket #${options.id}`);
}

// Event Bookings
async function cmdEventBookingsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/events/${options.eventId}/bookings?${params}`);
  const items = Array.isArray(data) ? data : data?.bookings || [];
  displayList(items, b => `  ${String(b.id).padEnd(8)} user:${String(b.user_id || '').padEnd(6)} ticket:${String(b.ticket_id || '').padEnd(6)} status: ${b.status || '—'}`, data);
}

async function cmdEventBookingsRead(options) {
  const data = await apiFetch(`/events/${options.eventId}/bookings/${options.id}`);
  const b = data?.booking || data;
  console.log(`Booking #${b.id}`);
  console.log(`  User ID:    ${b.user_id || '—'}`);
  console.log(`  Ticket ID:  ${b.ticket_id || '—'}`);
  console.log(`  Status:     ${b.status || '—'}`);
  console.log(`  Created:    ${fmtDate(b.created_at)}`);
}

async function cmdEventBookingsCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.ticketId) body.ticket_id = options.ticketId;

  const result = await apiFetch(`/events/${options.eventId}/bookings`, {
    method: 'POST',
    body: JSON.stringify({ booking: body }),
  });
  const b = result?.booking || result;
  console.log(`Created booking #${b.id}`);
}

async function cmdEventBookingsUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;

  await apiFetch(`/events/${options.eventId}/bookings/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ booking: body }),
  });
  console.log(`Updated booking #${options.id}`);
}

async function cmdEventBookingsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/events/${options.eventId}/bookings/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted booking #${options.id}`);
}

// Event Attendees
async function cmdEventAttendeesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/events/${options.eventId}/attendees?${params}`);
  const items = Array.isArray(data) ? data : data?.attendees || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${([a.firstname, a.lastname].filter(Boolean).join(' ') || '').padEnd(25)} ${a.email || '—'}`, data);
}

async function cmdEventAttendeesRead(options) {
  const data = await apiFetch(`/events/${options.eventId}/attendees/${options.id}`);
  const a = data?.attendee || data;
  console.log(`Attendee #${a.id}`);
  console.log(`  Name:       ${[a.firstname, a.lastname].filter(Boolean).join(' ') || '—'}`);
  console.log(`  Email:      ${a.email || '—'}`);
  console.log(`  Status:     ${a.status || '—'}`);
  console.log(`  Checked in: ${a.checked_in ? 'Yes' : 'No'}`);
}

async function cmdEventAttendeesCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.email) body.email = options.email;
  if (options.firstname) body.firstname = options.firstname;
  if (options.lastname) body.lastname = options.lastname;

  const result = await apiFetch(`/events/${options.eventId}/attendees`, {
    method: 'POST',
    body: JSON.stringify({ attendee: body }),
  });
  const a = result?.attendee || result;
  console.log(`Created attendee #${a.id}`);
}

async function cmdEventAttendeesUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;
  if (options.checkedIn !== undefined) body.checked_in = options.checkedIn === 'true';

  await apiFetch(`/events/${options.eventId}/attendees/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ attendee: body }),
  });
  console.log(`Updated attendee #${options.id}`);
}

async function cmdEventAttendeesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/events/${options.eventId}/attendees/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted attendee #${options.id}`);
}

// Event RSVPs
async function cmdEventRsvpsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/events/${options.eventId}/rsvps?${params}`);
  const items = Array.isArray(data) ? data : data?.rsvps || [];
  displayList(items, r => `  ${String(r.id).padEnd(8)} user:${String(r.user_id || '').padEnd(6)} status: ${r.status || '—'}`, data);
}

async function cmdEventRsvpsRead(options) {
  const data = await apiFetch(`/events/${options.eventId}/rsvps/${options.id}`);
  const r = data?.rsvp || data;
  console.log(`RSVP #${r.id}`);
  console.log(`  User ID:    ${r.user_id || '—'}`);
  console.log(`  Status:     ${r.status || '—'}`);
  console.log(`  Created:    ${fmtDate(r.created_at)}`);
}

async function cmdEventRsvpsCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.status) body.status = options.status;

  const result = await apiFetch(`/events/${options.eventId}/rsvps`, {
    method: 'POST',
    body: JSON.stringify({ rsvp: body }),
  });
  const r = result?.rsvp || result;
  console.log(`Created RSVP #${r.id}`);
}

async function cmdEventRsvpsUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;

  await apiFetch(`/events/${options.eventId}/rsvps/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ rsvp: body }),
  });
  console.log(`Updated RSVP #${options.id}`);
}

async function cmdEventRsvpsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/events/${options.eventId}/rsvps/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted RSVP #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 20. VENTURES / PROJECTS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdProjectsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/ventures?${params}`);
  const items = Array.isArray(data) ? data : data?.ventures || data?.projects || [];
  displayList(items, p => `  ${String(p.id).padEnd(8)} ${(p.name || p.title || '').padEnd(35)} status: ${p.status || '—'}`, data);
}

async function cmdProjectsRead(options) {
  const data = await apiFetch(`/ventures/${options.id}`);
  const p = data?.venture || data?.project || data;
  console.log(`Project #${p.id}`);
  console.log(`  Name:       ${p.name || p.title || '—'}`);
  console.log(`  Status:     ${p.status || '—'}`);
  console.log(`  Created:    ${fmtDate(p.created_at)}`);
  if (p.description) console.log(`\n  Desc:\n  ${truncate(p.description, 300)}`);
}

async function cmdProjectsCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.description) body.description = options.description;
  if (options.status) body.status = options.status;

  const result = await apiFetch('/ventures', {
    method: 'POST',
    body: JSON.stringify({ venture: body }),
  });
  const p = result?.venture || result?.project || result;
  console.log(`Created project #${p.id}`);
}

async function cmdProjectsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.description) body.description = options.description;
  if (options.status) body.status = options.status;

  await apiFetch(`/ventures/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ venture: body }),
  });
  console.log(`Updated project #${options.id}`);
}

async function cmdProjectsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/ventures/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted project #${options.id}`);
}

// Project Team Members
async function cmdProjectTeamMembersList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/ventures/${options.projectId}/team_members?${params}`);
  const items = Array.isArray(data) ? data : data?.team_members || [];
  displayList(items, m => `  ${String(m.id).padEnd(8)} user:${String(m.user_id || '').padEnd(6)} role: ${m.role || '—'}`, data);
}

async function cmdProjectTeamMembersAdd(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.role) body.role = options.role;

  const result = await apiFetch(`/ventures/${options.projectId}/team_members`, {
    method: 'POST',
    body: JSON.stringify({ team_member: body }),
  });
  const m = result?.team_member || result;
  console.log(`Added team member #${m.id}`);
}

async function cmdProjectTeamMembersUpdate(options) {
  const body = {};
  if (options.role) body.role = options.role;

  await apiFetch(`/ventures/${options.projectId}/team_members/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ team_member: body }),
  });
  console.log(`Updated team member #${options.id}`);
}

async function cmdProjectTeamMembersRemove(options) {
  if (!options.confirm) { console.error('ERROR: Remove requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/ventures/${options.projectId}/team_members/${options.id}`, { method: 'DELETE' });
  console.log(`Removed team member #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 21. MEMBERSHIPS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdMembershipTypesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/membership_types?${params}`);
  const items = Array.isArray(data) ? data : data?.membership_types || [];
  displayList(items, t => `  ${String(t.id).padEnd(8)} ${(t.name || '').padEnd(30)} price: ${t.price ?? '—'} ${t.currency || ''}`, data);
}

async function cmdMembershipTypesRead(options) {
  const data = await apiFetch(`/membership_types/${options.id}`);
  const t = data?.membership_type || data;
  console.log(`Membership Type #${t.id}`);
  console.log(`  Name:       ${t.name || '—'}`);
  console.log(`  Price:      ${t.price ?? '—'} ${t.currency || ''}`);
  console.log(`  Duration:   ${t.duration || '—'}`);
  console.log(`  Created:    ${fmtDate(t.created_at)}`);
}

async function cmdMembershipTypesCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.price) body.price = parseFloat(options.price);
  if (options.currency) body.currency = options.currency;
  if (options.duration) body.duration = options.duration;

  const result = await apiFetch('/membership_types', {
    method: 'POST',
    body: JSON.stringify({ membership_type: body }),
  });
  const t = result?.membership_type || result;
  console.log(`Created membership type #${t.id}`);
}

async function cmdMembershipTypesUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.price) body.price = parseFloat(options.price);
  if (options.currency) body.currency = options.currency;
  if (options.duration) body.duration = options.duration;

  await apiFetch(`/membership_types/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ membership_type: body }),
  });
  console.log(`Updated membership type #${options.id}`);
}

async function cmdMembershipTypesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/membership_types/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted membership type #${options.id}`);
}

async function cmdMembershipSubscriptionsList(options) {
  const params = buildParams(options);
  if (options.userId) params.set('user_id', options.userId);
  const data = await apiFetch(`/membership_subscriptions?${params}`);
  const items = Array.isArray(data) ? data : data?.membership_subscriptions || [];
  displayList(items, s => `  ${String(s.id).padEnd(8)} user:${String(s.user_id || '').padEnd(6)} type:${String(s.membership_type_id || '').padEnd(6)} status: ${s.status || '—'}`, data);
}

async function cmdMembershipSubscriptionsRead(options) {
  const data = await apiFetch(`/membership_subscriptions/${options.id}`);
  const s = data?.membership_subscription || data;
  console.log(`Subscription #${s.id}`);
  console.log(`  User ID:    ${s.user_id || '—'}`);
  console.log(`  Type ID:    ${s.membership_type_id || '—'}`);
  console.log(`  Status:     ${s.status || '—'}`);
  console.log(`  Starts:     ${fmtDate(s.starts_at)}`);
  console.log(`  Ends:       ${fmtDate(s.ends_at)}`);
  console.log(`  Created:    ${fmtDate(s.created_at)}`);
}

async function cmdMembershipSubscriptionsCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.typeId) body.membership_type_id = options.typeId;
  if (options.startsAt) body.starts_at = options.startsAt;
  if (options.endsAt) body.ends_at = options.endsAt;

  const result = await apiFetch('/membership_subscriptions', {
    method: 'POST',
    body: JSON.stringify({ membership_subscription: body }),
  });
  const s = result?.membership_subscription || result;
  console.log(`Created subscription #${s.id}`);
}

async function cmdMembershipSubscriptionsUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;
  if (options.startsAt) body.starts_at = options.startsAt;
  if (options.endsAt) body.ends_at = options.endsAt;

  await apiFetch(`/membership_subscriptions/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ membership_subscription: body }),
  });
  console.log(`Updated subscription #${options.id}`);
}

async function cmdMembershipSubscriptionsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/membership_subscriptions/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted subscription #${options.id}`);
}

async function cmdMembershipPaymentOptions(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/membership_types/${options.typeId}/payment_options?${params}`);
  const items = Array.isArray(data) ? data : data?.payment_options || [];
  displayList(items, o => `  ${String(o.id).padEnd(8)} ${(o.name || '').padEnd(25)} price: ${o.price ?? '—'} ${o.currency || ''}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 22. ENGAGEMENT SCORING
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdEngagementRankingsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/engagement_scoring/rankings?${params}`);
  const items = Array.isArray(data) ? data : data?.rankings || [];
  displayList(items, r => `  ${String(r.user_id || '').padEnd(8)} score: ${r.score ?? '—'}  rank: ${r.rank ?? '—'}`, data);
}

async function cmdEngagementUserRank(options) {
  const data = await apiFetch(`/engagement_scoring/rankings/${options.userId}`);
  const r = data?.ranking || data;
  console.log(`Engagement Rank for User #${options.userId}`);
  console.log(`  Score:      ${r.score ?? '—'}`);
  console.log(`  Rank:       ${r.rank ?? '—'}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 23. PAYMENT ACCOUNTS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdPaymentAccountsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/payment_accounts?${params}`);
  const items = Array.isArray(data) ? data : data?.payment_accounts || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.name || a.provider || '').padEnd(25)} ${a.currency || ''}`, data);
}

async function cmdPaymentAccountsRead(options) {
  const data = await apiFetch(`/payment_accounts/${options.id}`);
  const a = data?.payment_account || data;
  console.log(`Payment Account #${a.id}`);
  console.log(`  Name:       ${a.name || '—'}`);
  console.log(`  Provider:   ${a.provider || '—'}`);
  console.log(`  Currency:   ${a.currency || '—'}`);
  console.log(`  Created:    ${fmtDate(a.created_at)}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 24. CATEGORIES
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdCategoriesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/categories?${params}`);
  const items = Array.isArray(data) ? data : data?.categories || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${c.name || '—'}`, data);
}

async function cmdCategoriesRead(options) {
  const data = await apiFetch(`/categories/${options.id}`);
  const c = data?.category || data;
  console.log(`Category #${c.id}`);
  console.log(`  Name:       ${c.name || '—'}`);
  console.log(`  Created:    ${fmtDate(c.created_at)}`);
}

async function cmdCategoriesCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const result = await apiFetch('/categories', {
    method: 'POST',
    body: JSON.stringify({ category: { name: options.name } }),
  });
  const c = result?.category || result;
  console.log(`Created category #${c.id}`);
}

async function cmdCategoriesUpdate(options) {
  await apiFetch(`/categories/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ category: { name: options.name } }),
  });
  console.log(`Updated category #${options.id}`);
}

async function cmdCategoriesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/categories/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted category #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 25. CURRENT LOCATIONS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdCurrentLocationsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/current_locations?${params}`);
  const items = Array.isArray(data) ? data : data?.current_locations || [];
  displayList(items, l => `  ${String(l.id).padEnd(8)} ${(l.name || l.city || '').padEnd(30)} ${l.country || '—'}`, data);
}

async function cmdCurrentLocationsRead(options) {
  const data = await apiFetch(`/current_locations/${options.id}`);
  const l = data?.current_location || data;
  console.log(`Current Location #${l.id}`);
  console.log(`  Name:       ${l.name || '—'}`);
  console.log(`  City:       ${l.city || '—'}`);
  console.log(`  Country:    ${l.country || '—'}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 26. MEDIA CENTER
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdMediaFilesList(options) {
  const params = buildParams(options);
  if (options.folderId) params.set('folder_id', options.folderId);
  const data = await apiFetch(`/media_center/files?${params}`);
  const items = Array.isArray(data) ? data : data?.files || [];
  displayList(items, f => `  ${String(f.id).padEnd(8)} ${(f.name || f.filename || '').padEnd(35)} ${f.content_type || '—'}  size: ${f.size || '—'}`, data);
}

async function cmdMediaFilesRead(options) {
  const data = await apiFetch(`/media_center/files/${options.id}`);
  const f = data?.file || data;
  console.log(`File #${f.id}`);
  console.log(`  Name:       ${f.name || f.filename || '—'}`);
  console.log(`  Type:       ${f.content_type || '—'}`);
  console.log(`  Size:       ${f.size || '—'}`);
  console.log(`  Folder ID:  ${f.folder_id || '—'}`);
  console.log(`  URL:        ${f.url || '—'}`);
  console.log(`  Created:    ${fmtDate(f.created_at)}`);
}

async function cmdMediaFilesCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.folderId) body.folder_id = options.folderId;
  if (options.url) body.url = options.url;

  const result = await apiFetch('/media_center/files', {
    method: 'POST',
    body: JSON.stringify({ file: body }),
  });
  const f = result?.file || result;
  console.log(`Created file #${f.id}`);
}

async function cmdMediaFilesUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.folderId) body.folder_id = options.folderId;

  await apiFetch(`/media_center/files/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ file: body }),
  });
  console.log(`Updated file #${options.id}`);
}

async function cmdMediaFilesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/media_center/files/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted file #${options.id}`);
}

async function cmdMediaFilesMove(options) {
  await apiFetch(`/media_center/files/${options.id}/move`, {
    method: 'PUT',
    body: JSON.stringify({ folder_id: options.folderId }),
  });
  console.log(`Moved file #${options.id} to folder #${options.folderId}`);
}

async function cmdMediaFilesDownloadUrl(options) {
  const data = await apiFetch(`/media_center/files/${options.id}/download_url`);
  const url = data?.url || data?.download_url || JSON.stringify(data);
  console.log(`Download URL for file #${options.id}:`);
  console.log(`  ${url}`);
}

async function cmdMediaFoldersList(options) {
  const params = buildParams(options);
  if (options.parentId) params.set('parent_id', options.parentId);
  const data = await apiFetch(`/media_center/folders?${params}`);
  const items = Array.isArray(data) ? data : data?.folders || [];
  displayList(items, f => `  ${String(f.id).padEnd(8)} ${(f.name || '').padEnd(30)} parent: ${f.parent_id || 'root'}`, data);
}

async function cmdMediaFoldersRead(options) {
  const data = await apiFetch(`/media_center/folders/${options.id}`);
  const f = data?.folder || data;
  console.log(`Folder #${f.id}`);
  console.log(`  Name:       ${f.name || '—'}`);
  console.log(`  Parent ID:  ${f.parent_id || 'root'}`);
  console.log(`  Created:    ${fmtDate(f.created_at)}`);
}

async function cmdMediaFoldersCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.parentId) body.parent_id = options.parentId;

  const result = await apiFetch('/media_center/folders', {
    method: 'POST',
    body: JSON.stringify({ folder: body }),
  });
  const f = result?.folder || result;
  console.log(`Created folder #${f.id}`);
}

async function cmdMediaFoldersUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;

  await apiFetch(`/media_center/folders/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ folder: body }),
  });
  console.log(`Updated folder #${options.id}`);
}

async function cmdMediaFoldersDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/media_center/folders/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted folder #${options.id}`);
}

async function cmdMediaFoldersMove(options) {
  await apiFetch(`/media_center/folders/${options.id}/move`, {
    method: 'PUT',
    body: JSON.stringify({ parent_id: options.parentId }),
  });
  console.log(`Moved folder #${options.id} to parent #${options.parentId}`);
}

async function cmdMediaRootFolder() {
  const data = await apiFetch('/media_center/folders/root');
  const f = data?.folder || data;
  console.log(`Root Folder`);
  console.log(`  ID:         ${f.id || '—'}`);
  console.log(`  Name:       ${f.name || '—'}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 27. AUDIT LOGS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdAuditLogsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/audit_logs?${params}`);
  const items = Array.isArray(data) ? data : data?.audit_logs || [];
  displayList(items, l => `  ${String(l.id).padEnd(8)} ${fmtDate(l.created_at).padEnd(12)} ${(l.action || '').padEnd(15)} ${(l.admin_email || '').padEnd(25)} ${truncate(l.resource_type, 20)}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 28. ADMINS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdAdminsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/admins?${params}`);
  const items = Array.isArray(data) ? data : data?.admins || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${([a.firstname, a.lastname].filter(Boolean).join(' ') || '').padEnd(25)} ${(a.email || '').padEnd(30)} role: ${a.role || '—'}`, data);
}

async function cmdAdminsRead(options) {
  const data = await apiFetch(`/admins/${options.id}`);
  const a = data?.admin || data;
  console.log(`Admin #${a.id}`);
  console.log(`  Name:       ${[a.firstname, a.lastname].filter(Boolean).join(' ') || '—'}`);
  console.log(`  Email:      ${a.email || '—'}`);
  console.log(`  Role:       ${a.role || '—'}`);
  console.log(`  Created:    ${fmtDate(a.created_at)}`);
}

async function cmdAdminsCreate(options) {
  if (!options.email) { console.error('ERROR: --email is required'); process.exit(1); }
  const body = { email: options.email };
  if (options.firstname) body.firstname = options.firstname;
  if (options.lastname) body.lastname = options.lastname;
  if (options.role) body.role = options.role;

  const result = await apiFetch('/admins', {
    method: 'POST',
    body: JSON.stringify({ admin: body }),
  });
  const a = result?.admin || result;
  console.log(`Created admin #${a.id}`);
}

async function cmdAdminsUpdate(options) {
  const body = {};
  if (options.email) body.email = options.email;
  if (options.firstname) body.firstname = options.firstname;
  if (options.lastname) body.lastname = options.lastname;
  if (options.role) body.role = options.role;

  await apiFetch(`/admins/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ admin: body }),
  });
  console.log(`Updated admin #${options.id}`);
}

async function cmdAdminsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/admins/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted admin #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 29. MENTORING
// ═══════════════════════════════════════════════════════════════════════════════

// Mentee Profiles
async function cmdMentoringMenteesList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/mentoring/mentee_profiles?${params}`);
  const items = Array.isArray(data) ? data : data?.mentee_profiles || [];
  displayList(items, m => `  ${String(m.id).padEnd(8)} user:${String(m.user_id || '').padEnd(6)} status: ${m.status || '—'}`, data);
}

async function cmdMentoringMenteesRead(options) {
  const data = await apiFetch(`/mentoring/mentee_profiles/${options.id}`);
  const m = data?.mentee_profile || data;
  console.log(`Mentee Profile #${m.id}`);
  console.log(`  User ID:    ${m.user_id || '—'}`);
  console.log(`  Status:     ${m.status || '—'}`);
  console.log(`  Program ID: ${m.program_id || '—'}`);
  console.log(`  Created:    ${fmtDate(m.created_at)}`);
}

async function cmdMentoringMenteesCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.programId) body.program_id = options.programId;

  const result = await apiFetch('/mentoring/mentee_profiles', {
    method: 'POST',
    body: JSON.stringify({ mentee_profile: body }),
  });
  const m = result?.mentee_profile || result;
  console.log(`Created mentee profile #${m.id}`);
}

async function cmdMentoringMenteesUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;

  await apiFetch(`/mentoring/mentee_profiles/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ mentee_profile: body }),
  });
  console.log(`Updated mentee profile #${options.id}`);
}

async function cmdMentoringMenteesDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/mentoring/mentee_profiles/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted mentee profile #${options.id}`);
}

// Mentor Profiles
async function cmdMentoringMentorsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/mentoring/mentor_profiles?${params}`);
  const items = Array.isArray(data) ? data : data?.mentor_profiles || [];
  displayList(items, m => `  ${String(m.id).padEnd(8)} user:${String(m.user_id || '').padEnd(6)} status: ${m.status || '—'}`, data);
}

async function cmdMentoringMentorsRead(options) {
  const data = await apiFetch(`/mentoring/mentor_profiles/${options.id}`);
  const m = data?.mentor_profile || data;
  console.log(`Mentor Profile #${m.id}`);
  console.log(`  User ID:    ${m.user_id || '—'}`);
  console.log(`  Status:     ${m.status || '—'}`);
  console.log(`  Program ID: ${m.program_id || '—'}`);
  console.log(`  Created:    ${fmtDate(m.created_at)}`);
}

async function cmdMentoringMentorsCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.programId) body.program_id = options.programId;

  const result = await apiFetch('/mentoring/mentor_profiles', {
    method: 'POST',
    body: JSON.stringify({ mentor_profile: body }),
  });
  const m = result?.mentor_profile || result;
  console.log(`Created mentor profile #${m.id}`);
}

async function cmdMentoringMentorsUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;

  await apiFetch(`/mentoring/mentor_profiles/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ mentor_profile: body }),
  });
  console.log(`Updated mentor profile #${options.id}`);
}

async function cmdMentoringMentorsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/mentoring/mentor_profiles/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted mentor profile #${options.id}`);
}

// Mentoring Programs
async function cmdMentoringProgramsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/mentoring/programs?${params}`);
  const items = Array.isArray(data) ? data : data?.programs || [];
  displayList(items, p => `  ${String(p.id).padEnd(8)} ${(p.name || '').padEnd(30)} status: ${p.status || '—'}`, data);
}

async function cmdMentoringProgramsRead(options) {
  const data = await apiFetch(`/mentoring/programs/${options.id}`);
  const p = data?.program || data;
  console.log(`Mentoring Program #${p.id}`);
  console.log(`  Name:       ${p.name || '—'}`);
  console.log(`  Status:     ${p.status || '—'}`);
  console.log(`  Created:    ${fmtDate(p.created_at)}`);
  if (p.description) console.log(`\n  Desc:\n  ${truncate(p.description, 300)}`);
}

async function cmdMentoringProgramsCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.description) body.description = options.description;

  const result = await apiFetch('/mentoring/programs', {
    method: 'POST',
    body: JSON.stringify({ program: body }),
  });
  const p = result?.program || result;
  console.log(`Created mentoring program #${p.id}`);
}

async function cmdMentoringProgramsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.description) body.description = options.description;
  if (options.status) body.status = options.status;

  await apiFetch(`/mentoring/programs/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ program: body }),
  });
  console.log(`Updated mentoring program #${options.id}`);
}

async function cmdMentoringProgramsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/mentoring/programs/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted mentoring program #${options.id}`);
}

// Mentoring Relationships
async function cmdMentoringRelationshipsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/mentoring/relationships?${params}`);
  const items = Array.isArray(data) ? data : data?.relationships || [];
  displayList(items, r => `  ${String(r.id).padEnd(8)} mentor:${String(r.mentor_profile_id || '').padEnd(6)} mentee:${String(r.mentee_profile_id || '').padEnd(6)} status: ${r.status || '—'}`, data);
}

async function cmdMentoringRelationshipsRead(options) {
  const data = await apiFetch(`/mentoring/relationships/${options.id}`);
  const r = data?.relationship || data;
  console.log(`Mentoring Relationship #${r.id}`);
  console.log(`  Mentor:     ${r.mentor_profile_id || '—'}`);
  console.log(`  Mentee:     ${r.mentee_profile_id || '—'}`);
  console.log(`  Status:     ${r.status || '—'}`);
  console.log(`  Program ID: ${r.program_id || '—'}`);
  console.log(`  Created:    ${fmtDate(r.created_at)}`);
}

async function cmdMentoringRelationshipsCreate(options) {
  const body = {};
  if (options.mentorProfileId) body.mentor_profile_id = options.mentorProfileId;
  if (options.menteeProfileId) body.mentee_profile_id = options.menteeProfileId;
  if (options.programId) body.program_id = options.programId;

  const result = await apiFetch('/mentoring/relationships', {
    method: 'POST',
    body: JSON.stringify({ relationship: body }),
  });
  const r = result?.relationship || result;
  console.log(`Created mentoring relationship #${r.id}`);
}

async function cmdMentoringRelationshipsUpdate(options) {
  const body = {};
  if (options.status) body.status = options.status;

  await apiFetch(`/mentoring/relationships/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ relationship: body }),
  });
  console.log(`Updated mentoring relationship #${options.id}`);
}

async function cmdMentoringRelationshipsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/mentoring/relationships/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted mentoring relationship #${options.id}`);
}

async function cmdMentoringCustomizableAttributes(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/mentoring/customizable_attributes?${params}`);
  const items = Array.isArray(data) ? data : data?.customizable_attributes || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.name || '').padEnd(30)} type: ${a.attribute_type || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 30. ORDER MANAGEMENT (manual transactions)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdManualTransactionsCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.amount) body.amount = parseFloat(options.amount);
  if (options.currency) body.currency = options.currency;
  if (options.description) body.description = options.description;

  const result = await apiFetch('/order_management/manual_transactions', {
    method: 'POST',
    body: JSON.stringify({ manual_transaction: body }),
  });
  const t = result?.manual_transaction || result;
  console.log(`Created manual transaction #${t.id}`);
}

async function cmdManualTransactionsUpdate(options) {
  const body = {};
  if (options.amount) body.amount = parseFloat(options.amount);
  if (options.description) body.description = options.description;

  await apiFetch(`/order_management/manual_transactions/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ manual_transaction: body }),
  });
  console.log(`Updated manual transaction #${options.id}`);
}

async function cmdManualTransactionsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/order_management/manual_transactions/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted manual transaction #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 31. EMAIL ANALYTICS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdEmailAnalyticsDeliveries(options) {
  const params = buildParams(options);
  if (options.campaignId) params.set('campaign_id', options.campaignId);
  const data = await apiFetch(`/email_analytics/deliveries?${params}`);
  const items = Array.isArray(data) ? data : data?.deliveries || [];
  displayList(items, d => `  ${String(d.id || '').padEnd(8)} ${(d.email || '').padEnd(30)} status: ${d.status || '—'}  ${fmtDate(d.delivered_at)}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 32. FORUMS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdForumDiscussionsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/forums/discussions?${params}`);
  const items = Array.isArray(data) ? data : data?.discussions || [];
  displayList(items, d => `  ${String(d.id).padEnd(8)} ${(d.title || '').padEnd(40)} replies: ${d.replies_count ?? '—'}`, data);
}

async function cmdForumDiscussionsRead(options) {
  const data = await apiFetch(`/forums/discussions/${options.id}`);
  const d = data?.discussion || data;
  console.log(`Discussion #${d.id}`);
  console.log(`  Title:      ${d.title || '—'}`);
  console.log(`  Author:     ${d.author_name || d.user_id || '—'}`);
  console.log(`  Replies:    ${d.replies_count ?? '—'}`);
  console.log(`  Created:    ${fmtDate(d.created_at)}`);
  if (d.body) console.log(`\n  Body:\n  ${truncate(d.body, 400)}`);
}

async function cmdForumDiscussionsCreate(options) {
  if (!options.title) { console.error('ERROR: --title is required'); process.exit(1); }
  const body = { title: options.title };
  if (options.body) body.body = options.body;
  if (options.forumId) body.forum_id = options.forumId;

  const result = await apiFetch('/forums/discussions', {
    method: 'POST',
    body: JSON.stringify({ discussion: body }),
  });
  const d = result?.discussion || result;
  console.log(`Created discussion #${d.id}`);
}

async function cmdForumDiscussionsUpdate(options) {
  const body = {};
  if (options.title) body.title = options.title;
  if (options.body) body.body = options.body;

  await apiFetch(`/forums/discussions/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ discussion: body }),
  });
  console.log(`Updated discussion #${options.id}`);
}

async function cmdForumDiscussionsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/forums/discussions/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted discussion #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 33. NOTIFICATIONS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdNotificationsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/notifications?${params}`);
  const items = Array.isArray(data) ? data : data?.notifications || [];
  displayList(items, n => `  ${String(n.id).padEnd(8)} ${fmtDate(n.created_at).padEnd(12)} ${(n.notification_type || '').padEnd(20)} ${truncate(n.message || n.title, 40)}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 34. SUB-NETWORKS (clusters)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdSubNetworkClustersList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/sub_networks/clusters?${params}`);
  const items = Array.isArray(data) ? data : data?.clusters || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${(c.name || '').padEnd(30)} ${c.subdomain || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 35. USER DATA FIELDS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdUserDataFieldsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/user_data_fields?${params}`);
  const items = Array.isArray(data) ? data : data?.user_data_fields || [];
  displayList(items, f => `  ${String(f.id).padEnd(8)} ${(f.name || '').padEnd(25)} type: ${f.field_type || '—'}  required: ${f.required ? 'Yes' : 'No'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 36. DONATIONS
// ═══════════════════════════════════════════════════════════════════════════════

// Donation Funds
async function cmdDonationFundsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/donations/funds?${params}`);
  const items = Array.isArray(data) ? data : data?.funds || [];
  displayList(items, f => `  ${String(f.id).padEnd(8)} ${(f.name || '').padEnd(30)} goal: ${f.goal_amount ?? '—'} ${f.currency || ''}`, data);
}

async function cmdDonationFundsRead(options) {
  const data = await apiFetch(`/donations/funds/${options.id}`);
  const f = data?.fund || data;
  console.log(`Donation Fund #${f.id}`);
  console.log(`  Name:       ${f.name || '—'}`);
  console.log(`  Goal:       ${f.goal_amount ?? '—'} ${f.currency || ''}`);
  console.log(`  Status:     ${f.status || '—'}`);
  console.log(`  Created:    ${fmtDate(f.created_at)}`);
  if (f.description) console.log(`\n  Desc:\n  ${truncate(f.description, 300)}`);
}

async function cmdDonationFundsCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.goal) body.goal_amount = parseFloat(options.goal);
  if (options.currency) body.currency = options.currency;
  if (options.description) body.description = options.description;

  const result = await apiFetch('/donations/funds', {
    method: 'POST',
    body: JSON.stringify({ fund: body }),
  });
  const f = result?.fund || result;
  console.log(`Created donation fund #${f.id}`);
}

async function cmdDonationFundsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.goal) body.goal_amount = parseFloat(options.goal);
  if (options.currency) body.currency = options.currency;
  if (options.description) body.description = options.description;

  await apiFetch(`/donations/funds/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ fund: body }),
  });
  console.log(`Updated donation fund #${options.id}`);
}

async function cmdDonationFundsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/donations/funds/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted donation fund #${options.id}`);
}

// Donation Campaigns
async function cmdDonationCampaignsList(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/donations/campaigns?${params}`);
  const items = Array.isArray(data) ? data : data?.campaigns || [];
  displayList(items, c => `  ${String(c.id).padEnd(8)} ${(c.name || '').padEnd(30)} status: ${c.status || '—'}`, data);
}

async function cmdDonationCampaignsRead(options) {
  const data = await apiFetch(`/donations/campaigns/${options.id}`);
  const c = data?.campaign || data;
  console.log(`Donation Campaign #${c.id}`);
  console.log(`  Name:       ${c.name || '—'}`);
  console.log(`  Status:     ${c.status || '—'}`);
  console.log(`  Fund ID:    ${c.fund_id || '—'}`);
  console.log(`  Created:    ${fmtDate(c.created_at)}`);
}

async function cmdDonationCampaignsCreate(options) {
  if (!options.name) { console.error('ERROR: --name is required'); process.exit(1); }
  const body = { name: options.name };
  if (options.fundId) body.fund_id = options.fundId;
  if (options.description) body.description = options.description;

  const result = await apiFetch('/donations/campaigns', {
    method: 'POST',
    body: JSON.stringify({ campaign: body }),
  });
  const c = result?.campaign || result;
  console.log(`Created donation campaign #${c.id}`);
}

async function cmdDonationCampaignsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.description) body.description = options.description;

  await apiFetch(`/donations/campaigns/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ campaign: body }),
  });
  console.log(`Updated donation campaign #${options.id}`);
}

async function cmdDonationCampaignsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/donations/campaigns/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted donation campaign #${options.id}`);
}

// Donations
async function cmdDonationsList(options) {
  const params = buildParams(options);
  if (options.fundId) params.set('fund_id', options.fundId);
  const data = await apiFetch(`/donations?${params}`);
  const items = Array.isArray(data) ? data : data?.donations || [];
  displayList(items, d => `  ${String(d.id).padEnd(8)} user:${String(d.user_id || '').padEnd(6)} amount: ${d.amount ?? '—'} ${d.currency || ''}  ${fmtDate(d.created_at)}`, data);
}

async function cmdDonationsRead(options) {
  const data = await apiFetch(`/donations/${options.id}`);
  const d = data?.donation || data;
  console.log(`Donation #${d.id}`);
  console.log(`  User ID:    ${d.user_id || '—'}`);
  console.log(`  Amount:     ${d.amount ?? '—'} ${d.currency || ''}`);
  console.log(`  Fund ID:    ${d.fund_id || '—'}`);
  console.log(`  Campaign:   ${d.campaign_id || '—'}`);
  console.log(`  Status:     ${d.status || '—'}`);
  console.log(`  Created:    ${fmtDate(d.created_at)}`);
}

async function cmdDonationsCreate(options) {
  const body = {};
  if (options.userId) body.user_id = options.userId;
  if (options.amount) body.amount = parseFloat(options.amount);
  if (options.currency) body.currency = options.currency;
  if (options.fundId) body.fund_id = options.fundId;
  if (options.campaignId) body.campaign_id = options.campaignId;

  const result = await apiFetch('/donations', {
    method: 'POST',
    body: JSON.stringify({ donation: body }),
  });
  const d = result?.donation || result;
  console.log(`Created donation #${d.id}`);
}

async function cmdDonationsUpdate(options) {
  const body = {};
  if (options.amount) body.amount = parseFloat(options.amount);
  if (options.status) body.status = options.status;

  await apiFetch(`/donations/${options.id}`, {
    method: 'PUT',
    body: JSON.stringify({ donation: body }),
  });
  console.log(`Updated donation #${options.id}`);
}

async function cmdDonationsDelete(options) {
  if (!options.confirm) { console.error('ERROR: Delete requires --confirm flag for safety'); process.exit(1); }
  await apiFetch(`/donations/${options.id}`, { method: 'DELETE' });
  console.log(`Deleted donation #${options.id}`);
}

// Donation Gifts
async function cmdDonationGiftsRead(options) {
  const data = await apiFetch(`/donations/gifts/${options.id}`);
  const g = data?.gift || data;
  console.log(`Gift #${g.id}`);
  console.log(`  Donation:   ${g.donation_id || '—'}`);
  console.log(`  Amount:     ${g.amount ?? '—'} ${g.currency || ''}`);
  console.log(`  Status:     ${g.status || '—'}`);
  console.log(`  Created:    ${fmtDate(g.created_at)}`);
}

async function cmdDonationsCustomizableAttributes(options) {
  const params = buildParams(options);
  const data = await apiFetch(`/donations/customizable_attributes?${params}`);
  const items = Array.isArray(data) ? data : data?.customizable_attributes || [];
  displayList(items, a => `  ${String(a.id).padEnd(8)} ${(a.name || '').padEnd(30)} type: ${a.attribute_type || '—'}`, data);
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMMON OPTIONS
// ═══════════════════════════════════════════════════════════════════════════════

function addPaginationOpts(cmd) {
  return cmd
    .option('-l, --limit <n>', 'Results per page (max 100)')
    .option('--page <n>', 'Page number');
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLI DEFINITION
// ═══════════════════════════════════════════════════════════════════════════════

const program = new Command();

program
  .name('hivebrite')
  .description('OpenClaw Hivebrite Skill — full Hivebrite Admin API CLI')
  .version(pkg.version);

// ── 1. Me ────────────────────────────────────────────────────────────────────

program.command('me').description('Show current admin info')
  .action(wrap(cmdMe));

// ── 2. Settings ──────────────────────────────────────────────────────────────

const settings = program.command('settings').description('Network settings and reference data');

addPaginationOpts(settings.command('customizable-attributes').description('List customizable attributes'))
  .action(wrap(cmdSettingsCustomizableAttributes));

addPaginationOpts(settings.command('fields-of-study').description('List fields of study'))
  .action(wrap(cmdSettingsFieldsOfStudy));

addPaginationOpts(settings.command('industries').description('List industries'))
  .action(wrap(cmdSettingsIndustries));

addPaginationOpts(settings.command('job-functions').description('List job functions'))
  .action(wrap(cmdSettingsJobFunctions));

addPaginationOpts(settings.command('currencies').description('List currencies'))
  .action(wrap(cmdSettingsCurrencies));

// ── 3. Network ───────────────────────────────────────────────────────────────

const network = program.command('network').description('Network info and sub-networks');

network.command('info').description('Show network info')
  .action(wrap(cmdNetworkInfo));

addPaginationOpts(network.command('sub-networks').description('List sub-networks'))
  .action(wrap(cmdNetworkSubNetworks));

addPaginationOpts(network.command('citizenships').description('List citizenships'))
  .action(wrap(cmdNetworkCitizenships));

// ── 4. Users ─────────────────────────────────────────────────────────────────

const users = program.command('users').description('Manage users');

addPaginationOpts(users.command('list').description('List users'))
  .option('-q, --query <text>', 'Search query')
  .action(wrap(cmdUsersList));

users.command('read').description('Read user details')
  .requiredOption('--id <id>', 'User ID')
  .action(wrap(cmdUsersRead));

users.command('create').description('Create a user')
  .requiredOption('-e, --email <email>', 'Email address')
  .option('--firstname <name>', 'First name')
  .option('--lastname <name>', 'Last name')
  .option('--phone <phone>', 'Phone')
  .option('--headline <text>', 'Headline')
  .option('--location <text>', 'Location')
  .action(wrap(cmdUsersCreate));

users.command('update').description('Update a user')
  .requiredOption('--id <id>', 'User ID')
  .option('-e, --email <email>', 'Email')
  .option('--firstname <name>', 'First name')
  .option('--lastname <name>', 'Last name')
  .option('--phone <phone>', 'Phone')
  .option('--headline <text>', 'Headline')
  .option('--location <text>', 'Location')
  .action(wrap(cmdUsersUpdate));

users.command('delete').description('Delete a user (requires --confirm)')
  .requiredOption('--id <id>', 'User ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdUsersDelete));

addPaginationOpts(users.command('experiences').description('List user experiences'))
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdUsersExperiences));

addPaginationOpts(users.command('educations').description('List user educations'))
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdUsersEducations));

users.command('notification-settings').description('Show user notification settings')
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdUsersNotificationSettings));

users.command('postal-addresses').description('List user postal addresses')
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdUsersPostalAddresses));

addPaginationOpts(users.command('group-membership').description('List user group memberships'))
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdUsersGroupMembership));

users.command('find-by-field').description('Find user by field value')
  .requiredOption('--field <name>', 'Field name')
  .requiredOption('--value <val>', 'Field value')
  .action(wrap(cmdUsersFindByField));

users.command('notify').description('Send notification to user')
  .requiredOption('--id <id>', 'User ID')
  .option('--subject <text>', 'Notification subject')
  .option('--message <text>', 'Notification message')
  .action(wrap(cmdUsersNotify));

users.command('activate').description('Activate a user')
  .requiredOption('--id <id>', 'User ID')
  .action(wrap(cmdUsersActivate));

// ── 5. Experiences ───────────────────────────────────────────────────────────

const experiences = program.command('experiences').description('Manage experiences (standalone)');

addPaginationOpts(experiences.command('list').description('List experiences'))
  .action(wrap(cmdExperiencesList));

experiences.command('read').description('Read experience details')
  .requiredOption('--id <id>', 'Experience ID')
  .action(wrap(cmdExperiencesRead));

experiences.command('create').description('Create an experience')
  .option('--user-id <id>', 'User ID')
  .option('--title <text>', 'Job title')
  .option('--organization <name>', 'Organization name')
  .option('--location <text>', 'Location')
  .option('--start-date <date>', 'Start date (YYYY-MM-DD)')
  .option('--end-date <date>', 'End date (YYYY-MM-DD)')
  .option('--current', 'Current position')
  .option('--description <text>', 'Description')
  .action(wrap(cmdExperiencesCreate));

experiences.command('update').description('Update an experience')
  .requiredOption('--id <id>', 'Experience ID')
  .option('--title <text>', 'Job title')
  .option('--organization <name>', 'Organization name')
  .option('--location <text>', 'Location')
  .option('--start-date <date>', 'Start date')
  .option('--end-date <date>', 'End date')
  .option('--current', 'Current position')
  .option('--description <text>', 'Description')
  .action(wrap(cmdExperiencesUpdate));

experiences.command('delete').description('Delete an experience (requires --confirm)')
  .requiredOption('--id <id>', 'Experience ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdExperiencesDelete));

addPaginationOpts(experiences.command('customizable-attributes').description('List experience customizable attributes'))
  .action(wrap(cmdExperiencesCustomizableAttributes));

// ── 6. Educations ────────────────────────────────────────────────────────────

const educations = program.command('educations').description('Manage educations (standalone)');

addPaginationOpts(educations.command('list').description('List educations'))
  .action(wrap(cmdEducationsList));

educations.command('read').description('Read education details')
  .requiredOption('--id <id>', 'Education ID')
  .action(wrap(cmdEducationsRead));

educations.command('create').description('Create an education')
  .option('--user-id <id>', 'User ID')
  .option('--degree <text>', 'Degree')
  .option('--school <name>', 'School name')
  .option('--field <text>', 'Field of study')
  .option('--start-date <date>', 'Start date (YYYY-MM-DD)')
  .option('--end-date <date>', 'End date (YYYY-MM-DD)')
  .option('--description <text>', 'Description')
  .action(wrap(cmdEducationsCreate));

educations.command('update').description('Update an education')
  .requiredOption('--id <id>', 'Education ID')
  .option('--degree <text>', 'Degree')
  .option('--school <name>', 'School name')
  .option('--field <text>', 'Field of study')
  .option('--start-date <date>', 'Start date')
  .option('--end-date <date>', 'End date')
  .option('--description <text>', 'Description')
  .action(wrap(cmdEducationsUpdate));

educations.command('delete').description('Delete an education (requires --confirm)')
  .requiredOption('--id <id>', 'Education ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEducationsDelete));

addPaginationOpts(educations.command('customizable-attributes').description('List education customizable attributes'))
  .action(wrap(cmdEducationsCustomizableAttributes));

// ── 7. Emailings ─────────────────────────────────────────────────────────────

const emailings = program.command('emailings').description('Manage emailing categories and campaigns');

const emailCategories = emailings.command('categories').description('Emailing categories');

addPaginationOpts(emailCategories.command('list').description('List emailing categories'))
  .action(wrap(cmdEmailingCategoriesList));

emailCategories.command('read').description('Read emailing category')
  .requiredOption('--id <id>', 'Category ID')
  .action(wrap(cmdEmailingCategoriesRead));

emailCategories.command('create').description('Create emailing category')
  .requiredOption('-n, --name <name>', 'Category name')
  .action(wrap(cmdEmailingCategoriesCreate));

emailCategories.command('update').description('Update emailing category')
  .requiredOption('--id <id>', 'Category ID')
  .requiredOption('-n, --name <name>', 'Category name')
  .action(wrap(cmdEmailingCategoriesUpdate));

emailCategories.command('delete').description('Delete emailing category (requires --confirm)')
  .requiredOption('--id <id>', 'Category ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEmailingCategoriesDelete));

const emailCampaigns = emailings.command('campaigns').description('Emailing campaigns');

addPaginationOpts(emailCampaigns.command('list').description('List emailing campaigns'))
  .action(wrap(cmdEmailingCampaignsList));

emailCampaigns.command('read').description('Read emailing campaign')
  .requiredOption('--id <id>', 'Campaign ID')
  .action(wrap(cmdEmailingCampaignsRead));

emailCampaigns.command('create').description('Create emailing campaign')
  .option('--subject <text>', 'Email subject')
  .option('-n, --name <name>', 'Campaign name')
  .option('--from-name <name>', 'Sender name')
  .option('--from-email <email>', 'Sender email')
  .option('--category-id <id>', 'Category ID')
  .option('--body <html>', 'Email body HTML')
  .action(wrap(cmdEmailingCampaignsCreate));

emailCampaigns.command('update').description('Update emailing campaign')
  .requiredOption('--id <id>', 'Campaign ID')
  .option('--subject <text>', 'Email subject')
  .option('-n, --name <name>', 'Campaign name')
  .option('--from-name <name>', 'Sender name')
  .option('--from-email <email>', 'Sender email')
  .option('--body <html>', 'Email body HTML')
  .action(wrap(cmdEmailingCampaignsUpdate));

emailCampaigns.command('delete').description('Delete emailing campaign (requires --confirm)')
  .requiredOption('--id <id>', 'Campaign ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEmailingCampaignsDelete));

emailCampaigns.command('send').description('Send emailing campaign')
  .requiredOption('--id <id>', 'Campaign ID')
  .action(wrap(cmdEmailingCampaignsSend));

// ── 8. Groups ────────────────────────────────────────────────────────────────

const groups = program.command('groups').description('Manage groups');

addPaginationOpts(groups.command('list').description('List groups'))
  .action(wrap(cmdGroupsList));

groups.command('read').description('Read group details')
  .requiredOption('--id <id>', 'Group ID')
  .action(wrap(cmdGroupsRead));

groups.command('create').description('Create a group')
  .requiredOption('-n, --name <name>', 'Group name')
  .option('-d, --description <text>', 'Description')
  .option('--slug <slug>', 'URL slug')
  .action(wrap(cmdGroupsCreate));

groups.command('update').description('Update a group')
  .requiredOption('--id <id>', 'Group ID')
  .option('-n, --name <name>', 'Group name')
  .option('-d, --description <text>', 'Description')
  .option('--slug <slug>', 'URL slug')
  .action(wrap(cmdGroupsUpdate));

groups.command('delete').description('Delete a group (requires --confirm)')
  .requiredOption('--id <id>', 'Group ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdGroupsDelete));

const groupUsers = groups.command('users').description('Group user management');

addPaginationOpts(groupUsers.command('list').description('List users in a group'))
  .requiredOption('--group-id <id>', 'Group ID')
  .action(wrap(cmdGroupUsersList));

groupUsers.command('add').description('Add user to group')
  .requiredOption('--group-id <id>', 'Group ID')
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdGroupUsersAdd));

groupUsers.command('remove').description('Remove user from group (requires --confirm)')
  .requiredOption('--group-id <id>', 'Group ID')
  .requiredOption('--user-id <id>', 'User ID')
  .option('--confirm', 'Confirm removal')
  .action(wrap(cmdGroupUsersRemove));

addPaginationOpts(groups.command('topic-categories').description('List group topic categories'))
  .requiredOption('--group-id <id>', 'Group ID')
  .action(wrap(cmdGroupTopicCategories));

// ── 9. Companies ─────────────────────────────────────────────────────────────

const companies = program.command('companies').description('Manage companies');

addPaginationOpts(companies.command('list').description('List companies'))
  .option('-q, --query <text>', 'Search query')
  .action(wrap(cmdCompaniesList));

companies.command('read').description('Read company details')
  .requiredOption('--id <id>', 'Company ID')
  .action(wrap(cmdCompaniesRead));

companies.command('create').description('Create a company')
  .requiredOption('-n, --name <name>', 'Company name')
  .option('--industry <text>', 'Industry')
  .option('--website <url>', 'Website')
  .option('--city <city>', 'City')
  .option('--country <country>', 'Country')
  .option('--phone <phone>', 'Phone')
  .action(wrap(cmdCompaniesCreate));

companies.command('update').description('Update a company')
  .requiredOption('--id <id>', 'Company ID')
  .option('-n, --name <name>', 'Company name')
  .option('--industry <text>', 'Industry')
  .option('--website <url>', 'Website')
  .option('--city <city>', 'City')
  .option('--country <country>', 'Country')
  .option('--phone <phone>', 'Phone')
  .action(wrap(cmdCompaniesUpdate));

companies.command('delete').description('Delete a company (requires --confirm)')
  .requiredOption('--id <id>', 'Company ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdCompaniesDelete));

// ── 10. News ─────────────────────────────────────────────────────────────────

const news = program.command('news').description('Manage news categories and posts');

const newsCategories = news.command('categories').description('News categories');

addPaginationOpts(newsCategories.command('list').description('List news categories'))
  .action(wrap(cmdNewsCategoriesList));

newsCategories.command('read').description('Read news category')
  .requiredOption('--id <id>', 'Category ID')
  .action(wrap(cmdNewsCategoriesRead));

newsCategories.command('create').description('Create news category')
  .requiredOption('-n, --name <name>', 'Category name')
  .action(wrap(cmdNewsCategoriesCreate));

newsCategories.command('update').description('Update news category')
  .requiredOption('--id <id>', 'Category ID')
  .requiredOption('-n, --name <name>', 'Category name')
  .action(wrap(cmdNewsCategoriesUpdate));

newsCategories.command('delete').description('Delete news category (requires --confirm)')
  .requiredOption('--id <id>', 'Category ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdNewsCategoriesDelete));

const newsPosts = news.command('posts').description('News posts');

addPaginationOpts(newsPosts.command('list').description('List news posts'))
  .action(wrap(cmdNewsPostsList));

newsPosts.command('read').description('Read news post')
  .requiredOption('--id <id>', 'Post ID')
  .action(wrap(cmdNewsPostsRead));

newsPosts.command('create').description('Create news post')
  .requiredOption('--title <text>', 'Post title')
  .option('--body <html>', 'Post body')
  .option('--category-id <id>', 'Category ID')
  .option('--status <status>', 'Post status')
  .action(wrap(cmdNewsPostsCreate));

newsPosts.command('update').description('Update news post')
  .requiredOption('--id <id>', 'Post ID')
  .option('--title <text>', 'Post title')
  .option('--body <html>', 'Post body')
  .option('--category-id <id>', 'Category ID')
  .option('--status <status>', 'Post status')
  .action(wrap(cmdNewsPostsUpdate));

newsPosts.command('delete').description('Delete news post (requires --confirm)')
  .requiredOption('--id <id>', 'Post ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdNewsPostsDelete));

newsPosts.command('duplicate').description('Duplicate news post')
  .requiredOption('--id <id>', 'Post ID')
  .action(wrap(cmdNewsPostsDuplicate));

// ── 11. Roles ────────────────────────────────────────────────────────────────

const roles = program.command('roles').description('List and read roles');

addPaginationOpts(roles.command('list').description('List roles'))
  .action(wrap(cmdRolesList));

roles.command('read').description('Read role details')
  .requiredOption('--id <id>', 'Role ID')
  .action(wrap(cmdRolesRead));

// ── 12. Business Opportunities ───────────────────────────────────────────────

const bizOps = program.command('business-opportunities').description('Manage business opportunities');

addPaginationOpts(bizOps.command('list').description('List business opportunities'))
  .action(wrap(cmdBusinessOpportunitiesList));

bizOps.command('read').description('Read business opportunity')
  .requiredOption('--id <id>', 'Opportunity ID')
  .action(wrap(cmdBusinessOpportunitiesRead));

bizOps.command('create').description('Create business opportunity')
  .requiredOption('--title <text>', 'Title')
  .option('--type <type>', 'Opportunity type')
  .option('--location <text>', 'Location')
  .option('--company <name>', 'Company name')
  .option('--description <text>', 'Description')
  .option('--status <status>', 'Status')
  .action(wrap(cmdBusinessOpportunitiesCreate));

bizOps.command('update').description('Update business opportunity')
  .requiredOption('--id <id>', 'Opportunity ID')
  .option('--title <text>', 'Title')
  .option('--type <type>', 'Opportunity type')
  .option('--location <text>', 'Location')
  .option('--company <name>', 'Company name')
  .option('--description <text>', 'Description')
  .option('--status <status>', 'Status')
  .action(wrap(cmdBusinessOpportunitiesUpdate));

bizOps.command('delete').description('Delete business opportunity (requires --confirm)')
  .requiredOption('--id <id>', 'Opportunity ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdBusinessOpportunitiesDelete));

// ── 13. Receipts ─────────────────────────────────────────────────────────────

const receipts = program.command('receipts').description('Manage receipts');

addPaginationOpts(receipts.command('list').description('List receipts'))
  .action(wrap(cmdReceiptsList));

receipts.command('read').description('Read receipt details')
  .requiredOption('--id <id>', 'Receipt ID')
  .action(wrap(cmdReceiptsRead));

receipts.command('update').description('Update receipt')
  .requiredOption('--id <id>', 'Receipt ID')
  .option('--status <status>', 'Status')
  .action(wrap(cmdReceiptsUpdate));

// ── 14. Pages (customizable) ────────────────────────────────────────────────

const pages = program.command('pages').description('Manage customizable pages');

addPaginationOpts(pages.command('list').description('List pages'))
  .action(wrap(cmdPagesCustomizableList));

pages.command('read').description('Read page details')
  .requiredOption('--id <id>', 'Page ID')
  .action(wrap(cmdPagesCustomizableRead));

pages.command('create').description('Create a page')
  .requiredOption('--title <text>', 'Page title')
  .option('--slug <slug>', 'URL slug')
  .option('--body <html>', 'Page body')
  .action(wrap(cmdPagesCustomizableCreate));

pages.command('update').description('Update a page')
  .requiredOption('--id <id>', 'Page ID')
  .option('--title <text>', 'Page title')
  .option('--slug <slug>', 'URL slug')
  .option('--body <html>', 'Page body')
  .action(wrap(cmdPagesCustomizableUpdate));

pages.command('delete').description('Delete a page (requires --confirm)')
  .requiredOption('--id <id>', 'Page ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdPagesCustomizableDelete));

// ── 15. Approvals ────────────────────────────────────────────────────────────

const approvals = program.command('approvals').description('Manage approvals');

addPaginationOpts(approvals.command('list').description('List approvals'))
  .action(wrap(cmdApprovalsList));

approvals.command('read').description('Read approval details')
  .requiredOption('--id <id>', 'Approval ID')
  .action(wrap(cmdApprovalsRead));

approvals.command('delete').description('Delete approval (requires --confirm)')
  .requiredOption('--id <id>', 'Approval ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdApprovalsDelete));

approvals.command('reject').description('Reject an approval')
  .requiredOption('--id <id>', 'Approval ID')
  .action(wrap(cmdApprovalsReject));

approvals.command('approve').description('Approve an approval')
  .requiredOption('--id <id>', 'Approval ID')
  .action(wrap(cmdApprovalsApprove));

approvals.command('link-to-user').description('Link approval to a user')
  .requiredOption('--id <id>', 'Approval ID')
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdApprovalsLinkToUser));

// ── 16. Versions ─────────────────────────────────────────────────────────────

const versions = program.command('versions').description('List deleted items (versions)');

addPaginationOpts(versions.command('list').description('List deleted items'))
  .option('--item-type <type>', 'Filter by item type')
  .action(wrap(cmdVersionsList));

// ── 17. Comments (v3) ───────────────────────────────────────────────────────

const comments = program.command('comments').description('Manage comments (v3 API)');

addPaginationOpts(comments.command('list').description('List comments'))
  .option('--commentable-type <type>', 'Commentable type')
  .option('--commentable-id <id>', 'Commentable ID')
  .action(wrap(cmdCommentsList));

comments.command('read').description('Read comment')
  .requiredOption('--id <id>', 'Comment ID')
  .action(wrap(cmdCommentsRead));

comments.command('create').description('Create a comment')
  .requiredOption('--body <text>', 'Comment body')
  .option('--commentable-type <type>', 'Commentable type')
  .option('--commentable-id <id>', 'Commentable ID')
  .action(wrap(cmdCommentsCreate));

comments.command('update').description('Update a comment')
  .requiredOption('--id <id>', 'Comment ID')
  .option('--body <text>', 'Comment body')
  .action(wrap(cmdCommentsUpdate));

comments.command('delete').description('Delete a comment (requires --confirm)')
  .requiredOption('--id <id>', 'Comment ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdCommentsDelete));

// ── 18. Posts (v3) ──────────────────────────────────────────────────────────

const posts = program.command('posts').description('Manage posts (v3 API)');

addPaginationOpts(posts.command('list').description('List posts'))
  .action(wrap(cmdPostsList));

posts.command('read').description('Read post')
  .requiredOption('--id <id>', 'Post ID')
  .action(wrap(cmdPostsRead));

posts.command('create').description('Create a post')
  .requiredOption('--body <text>', 'Post body')
  .option('--title <text>', 'Post title')
  .option('--group-id <id>', 'Group ID')
  .action(wrap(cmdPostsCreate));

posts.command('update').description('Update a post')
  .requiredOption('--id <id>', 'Post ID')
  .option('--body <text>', 'Post body')
  .option('--title <text>', 'Post title')
  .action(wrap(cmdPostsUpdate));

posts.command('delete').description('Delete a post (requires --confirm)')
  .requiredOption('--id <id>', 'Post ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdPostsDelete));

// ── 19. Network Events ──────────────────────────────────────────────────────

const events = program.command('events').description('Manage network events');

addPaginationOpts(events.command('list').description('List events'))
  .action(wrap(cmdEventsList));

events.command('read').description('Read event details')
  .requiredOption('--id <id>', 'Event ID')
  .action(wrap(cmdEventsRead));

events.command('create').description('Create an event')
  .requiredOption('-n, --name <name>', 'Event name')
  .option('--starts-at <datetime>', 'Start date/time (ISO 8601)')
  .option('--ends-at <datetime>', 'End date/time (ISO 8601)')
  .option('--location <text>', 'Location')
  .option('--capacity <n>', 'Capacity')
  .option('--description <text>', 'Description')
  .action(wrap(cmdEventsCreate));

events.command('update').description('Update an event')
  .requiredOption('--id <id>', 'Event ID')
  .option('-n, --name <name>', 'Event name')
  .option('--starts-at <datetime>', 'Start date/time')
  .option('--ends-at <datetime>', 'End date/time')
  .option('--location <text>', 'Location')
  .option('--capacity <n>', 'Capacity')
  .option('--description <text>', 'Description')
  .action(wrap(cmdEventsUpdate));

events.command('delete').description('Delete an event (requires --confirm)')
  .requiredOption('--id <id>', 'Event ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEventsDelete));

events.command('cancel').description('Cancel an event')
  .requiredOption('--id <id>', 'Event ID')
  .action(wrap(cmdEventsCancel));

events.command('duplicate').description('Duplicate an event')
  .requiredOption('--id <id>', 'Event ID')
  .action(wrap(cmdEventsDuplicate));

addPaginationOpts(events.command('customizable-attributes').description('List event customizable attributes'))
  .action(wrap(cmdEventsCustomizableAttributes));

// Event Tickets
const eventTickets = events.command('tickets').description('Manage event tickets');

addPaginationOpts(eventTickets.command('list').description('List event tickets'))
  .requiredOption('--event-id <id>', 'Event ID')
  .action(wrap(cmdEventTicketsList));

eventTickets.command('read').description('Read event ticket')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Ticket ID')
  .action(wrap(cmdEventTicketsRead));

eventTickets.command('create').description('Create event ticket')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('-n, --name <name>', 'Ticket name')
  .option('--price <amount>', 'Price')
  .option('--capacity <n>', 'Capacity')
  .option('--currency <code>', 'Currency code')
  .action(wrap(cmdEventTicketsCreate));

eventTickets.command('update').description('Update event ticket')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Ticket ID')
  .option('-n, --name <name>', 'Ticket name')
  .option('--price <amount>', 'Price')
  .option('--capacity <n>', 'Capacity')
  .action(wrap(cmdEventTicketsUpdate));

eventTickets.command('delete').description('Delete event ticket (requires --confirm)')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Ticket ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEventTicketsDelete));

// Event Bookings
const eventBookings = events.command('bookings').description('Manage event bookings');

addPaginationOpts(eventBookings.command('list').description('List event bookings'))
  .requiredOption('--event-id <id>', 'Event ID')
  .action(wrap(cmdEventBookingsList));

eventBookings.command('read').description('Read event booking')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Booking ID')
  .action(wrap(cmdEventBookingsRead));

eventBookings.command('create').description('Create event booking')
  .requiredOption('--event-id <id>', 'Event ID')
  .option('--user-id <id>', 'User ID')
  .option('--ticket-id <id>', 'Ticket ID')
  .action(wrap(cmdEventBookingsCreate));

eventBookings.command('update').description('Update event booking')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Booking ID')
  .option('--status <status>', 'Status')
  .action(wrap(cmdEventBookingsUpdate));

eventBookings.command('delete').description('Delete event booking (requires --confirm)')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Booking ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEventBookingsDelete));

// Event Attendees
const eventAttendees = events.command('attendees').description('Manage event attendees');

addPaginationOpts(eventAttendees.command('list').description('List event attendees'))
  .requiredOption('--event-id <id>', 'Event ID')
  .action(wrap(cmdEventAttendeesList));

eventAttendees.command('read').description('Read event attendee')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Attendee ID')
  .action(wrap(cmdEventAttendeesRead));

eventAttendees.command('create').description('Create event attendee')
  .requiredOption('--event-id <id>', 'Event ID')
  .option('--user-id <id>', 'User ID')
  .option('-e, --email <email>', 'Email')
  .option('--firstname <name>', 'First name')
  .option('--lastname <name>', 'Last name')
  .action(wrap(cmdEventAttendeesCreate));

eventAttendees.command('update').description('Update event attendee')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Attendee ID')
  .option('--status <status>', 'Status')
  .option('--checked-in <bool>', 'Checked in (true/false)')
  .action(wrap(cmdEventAttendeesUpdate));

eventAttendees.command('delete').description('Delete event attendee (requires --confirm)')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'Attendee ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEventAttendeesDelete));

// Event RSVPs
const eventRsvps = events.command('rsvps').description('Manage event RSVPs');

addPaginationOpts(eventRsvps.command('list').description('List event RSVPs'))
  .requiredOption('--event-id <id>', 'Event ID')
  .action(wrap(cmdEventRsvpsList));

eventRsvps.command('read').description('Read event RSVP')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'RSVP ID')
  .action(wrap(cmdEventRsvpsRead));

eventRsvps.command('create').description('Create event RSVP')
  .requiredOption('--event-id <id>', 'Event ID')
  .option('--user-id <id>', 'User ID')
  .option('--status <status>', 'Status')
  .action(wrap(cmdEventRsvpsCreate));

eventRsvps.command('update').description('Update event RSVP')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'RSVP ID')
  .option('--status <status>', 'Status')
  .action(wrap(cmdEventRsvpsUpdate));

eventRsvps.command('delete').description('Delete event RSVP (requires --confirm)')
  .requiredOption('--event-id <id>', 'Event ID')
  .requiredOption('--id <id>', 'RSVP ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdEventRsvpsDelete));

// ── 20. Projects (Ventures) ─────────────────────────────────────────────────

const projects = program.command('projects').description('Manage projects/ventures');

addPaginationOpts(projects.command('list').description('List projects'))
  .action(wrap(cmdProjectsList));

projects.command('read').description('Read project details')
  .requiredOption('--id <id>', 'Project ID')
  .action(wrap(cmdProjectsRead));

projects.command('create').description('Create a project')
  .requiredOption('-n, --name <name>', 'Project name')
  .option('--description <text>', 'Description')
  .option('--status <status>', 'Status')
  .action(wrap(cmdProjectsCreate));

projects.command('update').description('Update a project')
  .requiredOption('--id <id>', 'Project ID')
  .option('-n, --name <name>', 'Project name')
  .option('--description <text>', 'Description')
  .option('--status <status>', 'Status')
  .action(wrap(cmdProjectsUpdate));

projects.command('delete').description('Delete a project (requires --confirm)')
  .requiredOption('--id <id>', 'Project ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdProjectsDelete));

const teamMembers = projects.command('team-members').description('Manage project team members');

addPaginationOpts(teamMembers.command('list').description('List team members'))
  .requiredOption('--project-id <id>', 'Project ID')
  .action(wrap(cmdProjectTeamMembersList));

teamMembers.command('add').description('Add team member')
  .requiredOption('--project-id <id>', 'Project ID')
  .requiredOption('--user-id <id>', 'User ID')
  .option('--role <role>', 'Role')
  .action(wrap(cmdProjectTeamMembersAdd));

teamMembers.command('update').description('Update team member')
  .requiredOption('--project-id <id>', 'Project ID')
  .requiredOption('--id <id>', 'Team member ID')
  .option('--role <role>', 'Role')
  .action(wrap(cmdProjectTeamMembersUpdate));

teamMembers.command('remove').description('Remove team member (requires --confirm)')
  .requiredOption('--project-id <id>', 'Project ID')
  .requiredOption('--id <id>', 'Team member ID')
  .option('--confirm', 'Confirm removal')
  .action(wrap(cmdProjectTeamMembersRemove));

// ── 21. Memberships ─────────────────────────────────────────────────────────

const memberships = program.command('memberships').description('Manage membership types, subscriptions, and payment options');

const memberTypes = memberships.command('types').description('Membership types');

addPaginationOpts(memberTypes.command('list').description('List membership types'))
  .action(wrap(cmdMembershipTypesList));

memberTypes.command('read').description('Read membership type')
  .requiredOption('--id <id>', 'Type ID')
  .action(wrap(cmdMembershipTypesRead));

memberTypes.command('create').description('Create membership type')
  .requiredOption('-n, --name <name>', 'Type name')
  .option('--price <amount>', 'Price')
  .option('--currency <code>', 'Currency')
  .option('--duration <text>', 'Duration')
  .action(wrap(cmdMembershipTypesCreate));

memberTypes.command('update').description('Update membership type')
  .requiredOption('--id <id>', 'Type ID')
  .option('-n, --name <name>', 'Type name')
  .option('--price <amount>', 'Price')
  .option('--currency <code>', 'Currency')
  .option('--duration <text>', 'Duration')
  .action(wrap(cmdMembershipTypesUpdate));

memberTypes.command('delete').description('Delete membership type (requires --confirm)')
  .requiredOption('--id <id>', 'Type ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMembershipTypesDelete));

const memberSubs = memberships.command('subscriptions').description('Membership subscriptions');

addPaginationOpts(memberSubs.command('list').description('List subscriptions'))
  .option('--user-id <id>', 'Filter by user ID')
  .action(wrap(cmdMembershipSubscriptionsList));

memberSubs.command('read').description('Read subscription')
  .requiredOption('--id <id>', 'Subscription ID')
  .action(wrap(cmdMembershipSubscriptionsRead));

memberSubs.command('create').description('Create subscription')
  .option('--user-id <id>', 'User ID')
  .option('--type-id <id>', 'Membership type ID')
  .option('--starts-at <date>', 'Start date')
  .option('--ends-at <date>', 'End date')
  .action(wrap(cmdMembershipSubscriptionsCreate));

memberSubs.command('update').description('Update subscription')
  .requiredOption('--id <id>', 'Subscription ID')
  .option('--status <status>', 'Status')
  .option('--starts-at <date>', 'Start date')
  .option('--ends-at <date>', 'End date')
  .action(wrap(cmdMembershipSubscriptionsUpdate));

memberSubs.command('delete').description('Delete subscription (requires --confirm)')
  .requiredOption('--id <id>', 'Subscription ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMembershipSubscriptionsDelete));

addPaginationOpts(memberships.command('payment-options').description('List payment options for membership type'))
  .requiredOption('--type-id <id>', 'Membership type ID')
  .action(wrap(cmdMembershipPaymentOptions));

// ── 22. Engagement Scoring ──────────────────────────────────────────────────

const engagement = program.command('engagement').description('Engagement scoring');

addPaginationOpts(engagement.command('rankings').description('List engagement rankings'))
  .action(wrap(cmdEngagementRankingsList));

engagement.command('user-rank').description('Get user engagement rank')
  .requiredOption('--user-id <id>', 'User ID')
  .action(wrap(cmdEngagementUserRank));

// ── 23. Payment Accounts ────────────────────────────────────────────────────

const paymentAccounts = program.command('payment-accounts').description('View payment accounts');

addPaginationOpts(paymentAccounts.command('list').description('List payment accounts'))
  .action(wrap(cmdPaymentAccountsList));

paymentAccounts.command('read').description('Read payment account')
  .requiredOption('--id <id>', 'Account ID')
  .action(wrap(cmdPaymentAccountsRead));

// ── 24. Categories ──────────────────────────────────────────────────────────

const categories = program.command('categories').description('Manage categories');

addPaginationOpts(categories.command('list').description('List categories'))
  .action(wrap(cmdCategoriesList));

categories.command('read').description('Read category')
  .requiredOption('--id <id>', 'Category ID')
  .action(wrap(cmdCategoriesRead));

categories.command('create').description('Create category')
  .requiredOption('-n, --name <name>', 'Category name')
  .action(wrap(cmdCategoriesCreate));

categories.command('update').description('Update category')
  .requiredOption('--id <id>', 'Category ID')
  .requiredOption('-n, --name <name>', 'Category name')
  .action(wrap(cmdCategoriesUpdate));

categories.command('delete').description('Delete category (requires --confirm)')
  .requiredOption('--id <id>', 'Category ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdCategoriesDelete));

// ── 25. Current Locations ───────────────────────────────────────────────────

const currentLocations = program.command('current-locations').description('View current locations');

addPaginationOpts(currentLocations.command('list').description('List current locations'))
  .action(wrap(cmdCurrentLocationsList));

currentLocations.command('read').description('Read current location')
  .requiredOption('--id <id>', 'Location ID')
  .action(wrap(cmdCurrentLocationsRead));

// ── 26. Media Center ────────────────────────────────────────────────────────

const media = program.command('media').description('Manage media center files and folders');

const mediaFiles = media.command('files').description('Media center files');

addPaginationOpts(mediaFiles.command('list').description('List files'))
  .option('--folder-id <id>', 'Filter by folder ID')
  .action(wrap(cmdMediaFilesList));

mediaFiles.command('read').description('Read file details')
  .requiredOption('--id <id>', 'File ID')
  .action(wrap(cmdMediaFilesRead));

mediaFiles.command('create').description('Create file record')
  .requiredOption('-n, --name <name>', 'File name')
  .option('--folder-id <id>', 'Folder ID')
  .option('--url <url>', 'File URL')
  .action(wrap(cmdMediaFilesCreate));

mediaFiles.command('update').description('Update file')
  .requiredOption('--id <id>', 'File ID')
  .option('-n, --name <name>', 'File name')
  .option('--folder-id <id>', 'Folder ID')
  .action(wrap(cmdMediaFilesUpdate));

mediaFiles.command('delete').description('Delete file (requires --confirm)')
  .requiredOption('--id <id>', 'File ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMediaFilesDelete));

mediaFiles.command('move').description('Move file to folder')
  .requiredOption('--id <id>', 'File ID')
  .requiredOption('--folder-id <id>', 'Target folder ID')
  .action(wrap(cmdMediaFilesMove));

mediaFiles.command('download-url').description('Get file download URL')
  .requiredOption('--id <id>', 'File ID')
  .action(wrap(cmdMediaFilesDownloadUrl));

const mediaFolders = media.command('folders').description('Media center folders');

addPaginationOpts(mediaFolders.command('list').description('List folders'))
  .option('--parent-id <id>', 'Filter by parent folder ID')
  .action(wrap(cmdMediaFoldersList));

mediaFolders.command('read').description('Read folder details')
  .requiredOption('--id <id>', 'Folder ID')
  .action(wrap(cmdMediaFoldersRead));

mediaFolders.command('create').description('Create folder')
  .requiredOption('-n, --name <name>', 'Folder name')
  .option('--parent-id <id>', 'Parent folder ID')
  .action(wrap(cmdMediaFoldersCreate));

mediaFolders.command('update').description('Update folder')
  .requiredOption('--id <id>', 'Folder ID')
  .option('-n, --name <name>', 'Folder name')
  .action(wrap(cmdMediaFoldersUpdate));

mediaFolders.command('delete').description('Delete folder (requires --confirm)')
  .requiredOption('--id <id>', 'Folder ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMediaFoldersDelete));

mediaFolders.command('move').description('Move folder')
  .requiredOption('--id <id>', 'Folder ID')
  .requiredOption('--parent-id <id>', 'New parent folder ID')
  .action(wrap(cmdMediaFoldersMove));

media.command('root-folder').description('Show root folder')
  .action(wrap(cmdMediaRootFolder));

// ── 27. Audit Logs ──────────────────────────────────────────────────────────

const auditLogs = program.command('audit-logs').description('View audit logs');

addPaginationOpts(auditLogs.command('list').description('List audit logs'))
  .action(wrap(cmdAuditLogsList));

// ── 28. Admins ──────────────────────────────────────────────────────────────

const admins = program.command('admins').description('Manage admins');

addPaginationOpts(admins.command('list').description('List admins'))
  .action(wrap(cmdAdminsList));

admins.command('read').description('Read admin details')
  .requiredOption('--id <id>', 'Admin ID')
  .action(wrap(cmdAdminsRead));

admins.command('create').description('Create admin')
  .requiredOption('-e, --email <email>', 'Email')
  .option('--firstname <name>', 'First name')
  .option('--lastname <name>', 'Last name')
  .option('--role <role>', 'Role')
  .action(wrap(cmdAdminsCreate));

admins.command('update').description('Update admin')
  .requiredOption('--id <id>', 'Admin ID')
  .option('-e, --email <email>', 'Email')
  .option('--firstname <name>', 'First name')
  .option('--lastname <name>', 'Last name')
  .option('--role <role>', 'Role')
  .action(wrap(cmdAdminsUpdate));

admins.command('delete').description('Delete admin (requires --confirm)')
  .requiredOption('--id <id>', 'Admin ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdAdminsDelete));

// ── 29. Mentoring ───────────────────────────────────────────────────────────

const mentoring = program.command('mentoring').description('Manage mentoring programs, profiles, and relationships');

// Mentee Profiles
const mentees = mentoring.command('mentees').description('Mentee profiles');

addPaginationOpts(mentees.command('list').description('List mentee profiles'))
  .action(wrap(cmdMentoringMenteesList));

mentees.command('read').description('Read mentee profile')
  .requiredOption('--id <id>', 'Profile ID')
  .action(wrap(cmdMentoringMenteesRead));

mentees.command('create').description('Create mentee profile')
  .option('--user-id <id>', 'User ID')
  .option('--program-id <id>', 'Program ID')
  .action(wrap(cmdMentoringMenteesCreate));

mentees.command('update').description('Update mentee profile')
  .requiredOption('--id <id>', 'Profile ID')
  .option('--status <status>', 'Status')
  .action(wrap(cmdMentoringMenteesUpdate));

mentees.command('delete').description('Delete mentee profile (requires --confirm)')
  .requiredOption('--id <id>', 'Profile ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMentoringMenteesDelete));

// Mentor Profiles
const mentors = mentoring.command('mentors').description('Mentor profiles');

addPaginationOpts(mentors.command('list').description('List mentor profiles'))
  .action(wrap(cmdMentoringMentorsList));

mentors.command('read').description('Read mentor profile')
  .requiredOption('--id <id>', 'Profile ID')
  .action(wrap(cmdMentoringMentorsRead));

mentors.command('create').description('Create mentor profile')
  .option('--user-id <id>', 'User ID')
  .option('--program-id <id>', 'Program ID')
  .action(wrap(cmdMentoringMentorsCreate));

mentors.command('update').description('Update mentor profile')
  .requiredOption('--id <id>', 'Profile ID')
  .option('--status <status>', 'Status')
  .action(wrap(cmdMentoringMentorsUpdate));

mentors.command('delete').description('Delete mentor profile (requires --confirm)')
  .requiredOption('--id <id>', 'Profile ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMentoringMentorsDelete));

// Programs
const programs = mentoring.command('programs').description('Mentoring programs');

addPaginationOpts(programs.command('list').description('List programs'))
  .action(wrap(cmdMentoringProgramsList));

programs.command('read').description('Read program details')
  .requiredOption('--id <id>', 'Program ID')
  .action(wrap(cmdMentoringProgramsRead));

programs.command('create').description('Create program')
  .requiredOption('-n, --name <name>', 'Program name')
  .option('--description <text>', 'Description')
  .action(wrap(cmdMentoringProgramsCreate));

programs.command('update').description('Update program')
  .requiredOption('--id <id>', 'Program ID')
  .option('-n, --name <name>', 'Program name')
  .option('--description <text>', 'Description')
  .option('--status <status>', 'Status')
  .action(wrap(cmdMentoringProgramsUpdate));

programs.command('delete').description('Delete program (requires --confirm)')
  .requiredOption('--id <id>', 'Program ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMentoringProgramsDelete));

// Relationships
const relationships = mentoring.command('relationships').description('Mentoring relationships');

addPaginationOpts(relationships.command('list').description('List relationships'))
  .action(wrap(cmdMentoringRelationshipsList));

relationships.command('read').description('Read relationship')
  .requiredOption('--id <id>', 'Relationship ID')
  .action(wrap(cmdMentoringRelationshipsRead));

relationships.command('create').description('Create relationship')
  .option('--mentor-profile-id <id>', 'Mentor profile ID')
  .option('--mentee-profile-id <id>', 'Mentee profile ID')
  .option('--program-id <id>', 'Program ID')
  .action(wrap(cmdMentoringRelationshipsCreate));

relationships.command('update').description('Update relationship')
  .requiredOption('--id <id>', 'Relationship ID')
  .option('--status <status>', 'Status')
  .action(wrap(cmdMentoringRelationshipsUpdate));

relationships.command('delete').description('Delete relationship (requires --confirm)')
  .requiredOption('--id <id>', 'Relationship ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdMentoringRelationshipsDelete));

addPaginationOpts(mentoring.command('customizable-attributes').description('List mentoring customizable attributes'))
  .action(wrap(cmdMentoringCustomizableAttributes));

// ── 30. Order Management ────────────────────────────────────────────────────

const orders = program.command('orders').description('Order management (manual transactions)');

orders.command('create').description('Create manual transaction')
  .option('--user-id <id>', 'User ID')
  .option('--amount <amount>', 'Amount')
  .option('--currency <code>', 'Currency')
  .option('--description <text>', 'Description')
  .action(wrap(cmdManualTransactionsCreate));

orders.command('update').description('Update manual transaction')
  .requiredOption('--id <id>', 'Transaction ID')
  .option('--amount <amount>', 'Amount')
  .option('--description <text>', 'Description')
  .action(wrap(cmdManualTransactionsUpdate));

orders.command('delete').description('Delete manual transaction (requires --confirm)')
  .requiredOption('--id <id>', 'Transaction ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdManualTransactionsDelete));

// ── 31. Email Analytics ─────────────────────────────────────────────────────

const emailAnalytics = program.command('email-analytics').description('Email analytics');

addPaginationOpts(emailAnalytics.command('deliveries').description('List email deliveries'))
  .option('--campaign-id <id>', 'Filter by campaign ID')
  .action(wrap(cmdEmailAnalyticsDeliveries));

// ── 32. Forums ──────────────────────────────────────────────────────────────

const forums = program.command('forums').description('Manage forum discussions');

addPaginationOpts(forums.command('list').description('List discussions'))
  .action(wrap(cmdForumDiscussionsList));

forums.command('read').description('Read discussion')
  .requiredOption('--id <id>', 'Discussion ID')
  .action(wrap(cmdForumDiscussionsRead));

forums.command('create').description('Create discussion')
  .requiredOption('--title <text>', 'Discussion title')
  .option('--body <text>', 'Discussion body')
  .option('--forum-id <id>', 'Forum ID')
  .action(wrap(cmdForumDiscussionsCreate));

forums.command('update').description('Update discussion')
  .requiredOption('--id <id>', 'Discussion ID')
  .option('--title <text>', 'Discussion title')
  .option('--body <text>', 'Discussion body')
  .action(wrap(cmdForumDiscussionsUpdate));

forums.command('delete').description('Delete discussion (requires --confirm)')
  .requiredOption('--id <id>', 'Discussion ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdForumDiscussionsDelete));

// ── 33. Notifications ───────────────────────────────────────────────────────

const notifications = program.command('notifications').description('View notifications');

addPaginationOpts(notifications.command('list').description('List notifications'))
  .action(wrap(cmdNotificationsList));

// ── 34. Sub-Networks (clusters) ─────────────────────────────────────────────

const subNetworks = program.command('sub-networks').description('Sub-network clusters');

addPaginationOpts(subNetworks.command('clusters').description('List clusters'))
  .action(wrap(cmdSubNetworkClustersList));

// ── 35. User Data Fields ────────────────────────────────────────────────────

const userDataFields = program.command('user-data-fields').description('View user data field definitions');

addPaginationOpts(userDataFields.command('list').description('List user data fields'))
  .action(wrap(cmdUserDataFieldsList));

// ── 36. Donations ───────────────────────────────────────────────────────────

const donations = program.command('donations').description('Manage donations, funds, campaigns, and gifts');

// Funds
const donationFunds = donations.command('funds').description('Donation funds');

addPaginationOpts(donationFunds.command('list').description('List funds'))
  .action(wrap(cmdDonationFundsList));

donationFunds.command('read').description('Read fund')
  .requiredOption('--id <id>', 'Fund ID')
  .action(wrap(cmdDonationFundsRead));

donationFunds.command('create').description('Create fund')
  .requiredOption('-n, --name <name>', 'Fund name')
  .option('--goal <amount>', 'Goal amount')
  .option('--currency <code>', 'Currency')
  .option('--description <text>', 'Description')
  .action(wrap(cmdDonationFundsCreate));

donationFunds.command('update').description('Update fund')
  .requiredOption('--id <id>', 'Fund ID')
  .option('-n, --name <name>', 'Fund name')
  .option('--goal <amount>', 'Goal amount')
  .option('--currency <code>', 'Currency')
  .option('--description <text>', 'Description')
  .action(wrap(cmdDonationFundsUpdate));

donationFunds.command('delete').description('Delete fund (requires --confirm)')
  .requiredOption('--id <id>', 'Fund ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdDonationFundsDelete));

// Donation Campaigns
const donationCampaigns = donations.command('campaigns').description('Donation campaigns');

addPaginationOpts(donationCampaigns.command('list').description('List campaigns'))
  .action(wrap(cmdDonationCampaignsList));

donationCampaigns.command('read').description('Read campaign')
  .requiredOption('--id <id>', 'Campaign ID')
  .action(wrap(cmdDonationCampaignsRead));

donationCampaigns.command('create').description('Create campaign')
  .requiredOption('-n, --name <name>', 'Campaign name')
  .option('--fund-id <id>', 'Fund ID')
  .option('--description <text>', 'Description')
  .action(wrap(cmdDonationCampaignsCreate));

donationCampaigns.command('update').description('Update campaign')
  .requiredOption('--id <id>', 'Campaign ID')
  .option('-n, --name <name>', 'Campaign name')
  .option('--description <text>', 'Description')
  .action(wrap(cmdDonationCampaignsUpdate));

donationCampaigns.command('delete').description('Delete campaign (requires --confirm)')
  .requiredOption('--id <id>', 'Campaign ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdDonationCampaignsDelete));

// Donations
const donationItems = donations.command('items').description('Individual donations');

addPaginationOpts(donationItems.command('list').description('List donations'))
  .option('--fund-id <id>', 'Filter by fund ID')
  .action(wrap(cmdDonationsList));

donationItems.command('read').description('Read donation')
  .requiredOption('--id <id>', 'Donation ID')
  .action(wrap(cmdDonationsRead));

donationItems.command('create').description('Create donation')
  .option('--user-id <id>', 'User ID')
  .option('--amount <amount>', 'Amount')
  .option('--currency <code>', 'Currency')
  .option('--fund-id <id>', 'Fund ID')
  .option('--campaign-id <id>', 'Campaign ID')
  .action(wrap(cmdDonationsCreate));

donationItems.command('update').description('Update donation')
  .requiredOption('--id <id>', 'Donation ID')
  .option('--amount <amount>', 'Amount')
  .option('--status <status>', 'Status')
  .action(wrap(cmdDonationsUpdate));

donationItems.command('delete').description('Delete donation (requires --confirm)')
  .requiredOption('--id <id>', 'Donation ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(cmdDonationsDelete));

// Gifts
donations.command('gift').description('Read donation gift')
  .requiredOption('--id <id>', 'Gift ID')
  .action(wrap(cmdDonationGiftsRead));

addPaginationOpts(donations.command('customizable-attributes').description('List donation customizable attributes'))
  .action(wrap(cmdDonationsCustomizableAttributes));

// ── Parse ────────────────────────────────────────────────────────────────────

program.parse();