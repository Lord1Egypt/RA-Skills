#!/usr/bin/env node

/**
 * OpenClaw HubSpot Skill — CLI for the full HubSpot platform.
 *
 * Covers CRM (contacts, companies, deals, tickets, owners, pipelines,
 * associations, properties, engagements), CMS (blog posts, pages, domains),
 * Marketing (email campaigns, forms, marketing emails, contact lists),
 * Conversations (inbox conversations, messages), and Automation (workflows).
 *
 * @author Abdelkrim BOUJRAF <abdelkrim@alt-f1.be>
 * @license MIT
 * @see https://github.com/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be
 */

// fs/path used for: reading package.json version, OAuth token cache file I/O
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
    console.error(`ERROR: Missing required env var ${key}. See .env.example`);
    process.exit(1);
  }
  return v;
}

// ── Auth: Private App token OR OAuth 2.0 ─────────────────────────────────────

const OAUTH_TOKEN_PATH = resolve(homedir(), '.cache', 'openclaw', 'hubspot-token.json');

let _cachedAccessToken = null;
let _tokenExpiresAt = 0;

function isOAuthMode() {
  return !!process.env.HUBSPOT_CLIENT_ID;
}

async function getAccessToken() {
  if (!isOAuthMode()) {
    return env('HUBSPOT_ACCESS_TOKEN');
  }

  // Check cached token
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
    } catch {
      // ignore corrupt cache
    }
  }

  // Refresh the token
  const clientId = env('HUBSPOT_CLIENT_ID');
  const clientSecret = env('HUBSPOT_CLIENT_SECRET');
  const refreshToken = env('HUBSPOT_REFRESH_TOKEN');

  const resp = await fetch('https://api.hubapi.com/oauth/v1/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      client_id: clientId,
      client_secret: clientSecret,
      refresh_token: refreshToken,
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    console.error(`ERROR: OAuth token refresh failed (${resp.status}): ${text}`);
    process.exit(1);
  }

  const data = await resp.json();
  _cachedAccessToken = data.access_token;
  _tokenExpiresAt = Date.now() + data.expires_in * 1000;

  // Cache to disk
  try {
    const cacheDir = dirname(OAUTH_TOKEN_PATH);
    if (!existsSync(cacheDir)) mkdirSync(cacheDir, { recursive: true });
    writeFileSync(OAUTH_TOKEN_PATH, JSON.stringify({
      access_token: _cachedAccessToken,
      expires_at: _tokenExpiresAt,
    }), 'utf8');
  } catch {
    // non-fatal — token still works in memory
  }

  return _cachedAccessToken;
}

// ── Config (lazy via Proxy) ──────────────────────────────────────────────────

let _cfg;
function getCfg() {
  if (!_cfg) {
    _cfg = {
      maxResults: parseInt(process.env.HUBSPOT_MAX_RESULTS || '100', 10),
    };
  }
  return _cfg;
}
const CFG = new Proxy({}, { get: (_, prop) => getCfg()[prop] });

// ── HTTP client with rate-limit retry ────────────────────────────────────────

const API_BASE = 'https://api.hubapi.com';

async function apiFetch(path, options = {}, retries = 3) {
  const token = await getAccessToken();
  const url = path.startsWith('http') ? path : `${API_BASE}${path}`;
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

    if (resp.status === 204) return null;

    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }

    if (!resp.ok) {
      const msg = json?.message || json?.errors?.[0]?.message || body || resp.statusText;
      const err = new Error(msg);
      err.statusCode = resp.status;
      throw err;
    }

    return json;
  }
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
  const clean = str.replace(/\n/g, ' ').trim();
  return clean.length > len ? clean.substring(0, len) + '...' : clean;
}

function fmtDate(d) {
  return d ? d.substring(0, 10) : '—';
}

function propsLine(props, keys) {
  return keys.map(k => {
    const val = props[k];
    return val ? `${k}: ${val}` : null;
  }).filter(Boolean).join(' | ');
}

// ═══════════════════════════════════════════════════════════════════════════════
// CRM — Generic CRUD helpers for CRM v3 objects
// ═══════════════════════════════════════════════════════════════════════════════

async function crmList(objectType, options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.after) params.set('after', options.after);
  if (options.properties) params.set('properties', options.properties);

  const resp = await apiFetch(`/crm/v3/objects/${objectType}?${params}`);
  return resp;
}

async function crmSearch(objectType, filters, options) {
  const body = {
    filterGroups: [{ filters }],
    limit: options.limit || CFG.maxResults,
  };
  if (options.properties) body.properties = options.properties.split(',');
  if (options.after) body.after = options.after;

  return apiFetch(`/crm/v3/objects/${objectType}/search`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

async function crmRead(objectType, id, properties) {
  const params = properties ? `?properties=${properties}` : '';
  return apiFetch(`/crm/v3/objects/${objectType}/${id}${params}`);
}

async function crmCreate(objectType, properties) {
  return apiFetch(`/crm/v3/objects/${objectType}`, {
    method: 'POST',
    body: JSON.stringify({ properties }),
  });
}

async function crmUpdate(objectType, id, properties) {
  return apiFetch(`/crm/v3/objects/${objectType}/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ properties }),
  });
}

async function crmDelete(objectType, id) {
  return apiFetch(`/crm/v3/objects/${objectType}/${id}`, { method: 'DELETE' });
}

// ── CRM display helpers ──────────────────────────────────────────────────────

function displayCrmResults(resp, labelFn) {
  const items = resp?.results || [];
  if (!items.length) {
    console.log('No results found.');
    return;
  }
  for (const item of items) {
    console.log(labelFn(item));
  }
  console.log(`\n${items.length} result(s)${resp.paging?.next?.after ? ` — next: --after ${resp.paging.next.after}` : ''}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONTACTS
// ═══════════════════════════════════════════════════════════════════════════════

const CONTACT_PROPS = 'firstname,lastname,email,phone,company,lifecyclestage';

function contactLabel(c) {
  const p = c.properties || {};
  const name = [p.firstname, p.lastname].filter(Boolean).join(' ') || '(no name)';
  return `#${String(c.id).padEnd(12)} ${name.padEnd(30)} ${(p.email || '').padEnd(30)} ${p.company || ''}`;
}

async function cmdContactsList(options) {
  const resp = await crmList('contacts', { ...options, properties: CONTACT_PROPS });
  displayCrmResults(resp, contactLabel);
}

async function cmdContactsSearch(options) {
  if (!options.query) { console.error('ERROR: --query is required'); process.exit(1); }
  const filters = [{ propertyName: 'email', operator: 'CONTAINS_TOKEN', value: `*${options.query}*` }];
  const resp = await crmSearch('contacts', filters, { ...options, properties: CONTACT_PROPS });
  displayCrmResults(resp, contactLabel);
}

async function cmdContactsRead(options) {
  const c = await crmRead('contacts', options.id, CONTACT_PROPS);
  const p = c.properties || {};
  console.log(`Contact #${c.id}`);
  console.log(`  Name:       ${[p.firstname, p.lastname].filter(Boolean).join(' ') || '—'}`);
  console.log(`  Email:      ${p.email || '—'}`);
  console.log(`  Phone:      ${p.phone || '—'}`);
  console.log(`  Company:    ${p.company || '—'}`);
  console.log(`  Lifecycle:  ${p.lifecyclestage || '—'}`);
  console.log(`  Created:    ${fmtDate(p.createdate)}`);
  console.log(`  Updated:    ${fmtDate(p.lastmodifieddate)}`);
}

async function cmdContactsCreate(options) {
  const props = {};
  if (options.email) props.email = options.email;
  if (options.firstname) props.firstname = options.firstname;
  if (options.lastname) props.lastname = options.lastname;
  if (options.phone) props.phone = options.phone;
  if (options.company) props.company = options.company;
  if (options.lifecycle) props.lifecyclestage = options.lifecycle;

  if (!props.email && !props.firstname) {
    console.error('ERROR: At least --email or --firstname is required');
    process.exit(1);
  }

  const result = await crmCreate('contacts', props);
  console.log(`Created contact #${result.id}`);
}

async function cmdContactsUpdate(options) {
  const props = {};
  if (options.email) props.email = options.email;
  if (options.firstname) props.firstname = options.firstname;
  if (options.lastname) props.lastname = options.lastname;
  if (options.phone) props.phone = options.phone;
  if (options.company) props.company = options.company;
  if (options.lifecycle) props.lifecyclestage = options.lifecycle;

  await crmUpdate('contacts', options.id, props);
  console.log(`Updated contact #${options.id}`);
}

async function cmdContactsDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await crmDelete('contacts', options.id);
  console.log(`Deleted contact #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPANIES
// ═══════════════════════════════════════════════════════════════════════════════

const COMPANY_PROPS = 'name,domain,industry,city,state,country,phone,numberofemployees';

function companyLabel(c) {
  const p = c.properties || {};
  return `#${String(c.id).padEnd(12)} ${(p.name || '(no name)').padEnd(30)} ${(p.domain || '').padEnd(25)} ${p.industry || ''}`;
}

async function cmdCompaniesList(options) {
  const resp = await crmList('companies', { ...options, properties: COMPANY_PROPS });
  displayCrmResults(resp, companyLabel);
}

async function cmdCompaniesSearch(options) {
  if (!options.query) { console.error('ERROR: --query is required'); process.exit(1); }
  const filters = [{ propertyName: 'name', operator: 'CONTAINS_TOKEN', value: `*${options.query}*` }];
  const resp = await crmSearch('companies', filters, { ...options, properties: COMPANY_PROPS });
  displayCrmResults(resp, companyLabel);
}

async function cmdCompaniesRead(options) {
  const c = await crmRead('companies', options.id, COMPANY_PROPS);
  const p = c.properties || {};
  console.log(`Company #${c.id}`);
  console.log(`  Name:       ${p.name || '—'}`);
  console.log(`  Domain:     ${p.domain || '—'}`);
  console.log(`  Industry:   ${p.industry || '—'}`);
  console.log(`  Location:   ${[p.city, p.state, p.country].filter(Boolean).join(', ') || '—'}`);
  console.log(`  Phone:      ${p.phone || '—'}`);
  console.log(`  Employees:  ${p.numberofemployees || '—'}`);
  console.log(`  Created:    ${fmtDate(p.createdate)}`);
}

async function cmdCompaniesCreate(options) {
  const props = {};
  if (options.name) props.name = options.name;
  if (options.domain) props.domain = options.domain;
  if (options.industry) props.industry = options.industry;
  if (options.phone) props.phone = options.phone;
  if (options.city) props.city = options.city;

  if (!props.name) {
    console.error('ERROR: --name is required');
    process.exit(1);
  }

  const result = await crmCreate('companies', props);
  console.log(`Created company #${result.id}`);
}

async function cmdCompaniesUpdate(options) {
  const props = {};
  if (options.name) props.name = options.name;
  if (options.domain) props.domain = options.domain;
  if (options.industry) props.industry = options.industry;
  if (options.phone) props.phone = options.phone;
  if (options.city) props.city = options.city;

  await crmUpdate('companies', options.id, props);
  console.log(`Updated company #${options.id}`);
}

async function cmdCompaniesDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await crmDelete('companies', options.id);
  console.log(`Deleted company #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// DEALS
// ═══════════════════════════════════════════════════════════════════════════════

const DEAL_PROPS = 'dealname,dealstage,pipeline,amount,closedate,hubspot_owner_id';

function dealLabel(c) {
  const p = c.properties || {};
  const amount = p.amount ? `$${Number(p.amount).toLocaleString()}` : '';
  return `#${String(c.id).padEnd(12)} ${(p.dealname || '(no name)').padEnd(35)} ${(p.dealstage || '').padEnd(20)} ${amount}`;
}

async function cmdDealsList(options) {
  const resp = await crmList('deals', { ...options, properties: DEAL_PROPS });
  displayCrmResults(resp, dealLabel);
}

async function cmdDealsSearch(options) {
  if (!options.query) { console.error('ERROR: --query is required'); process.exit(1); }
  const filters = [{ propertyName: 'dealname', operator: 'CONTAINS_TOKEN', value: `*${options.query}*` }];
  const resp = await crmSearch('deals', filters, { ...options, properties: DEAL_PROPS });
  displayCrmResults(resp, dealLabel);
}

async function cmdDealsRead(options) {
  const c = await crmRead('deals', options.id, DEAL_PROPS);
  const p = c.properties || {};
  console.log(`Deal #${c.id}`);
  console.log(`  Name:       ${p.dealname || '—'}`);
  console.log(`  Stage:      ${p.dealstage || '—'}`);
  console.log(`  Pipeline:   ${p.pipeline || '—'}`);
  console.log(`  Amount:     ${p.amount ? '$' + Number(p.amount).toLocaleString() : '—'}`);
  console.log(`  Close date: ${fmtDate(p.closedate)}`);
  console.log(`  Owner:      ${p.hubspot_owner_id || '—'}`);
  console.log(`  Created:    ${fmtDate(p.createdate)}`);
}

async function cmdDealsCreate(options) {
  const props = {};
  if (options.name) props.dealname = options.name;
  if (options.stage) props.dealstage = options.stage;
  if (options.pipeline) props.pipeline = options.pipeline;
  if (options.amount) props.amount = options.amount;
  if (options.closedate) props.closedate = options.closedate;
  if (options.owner) props.hubspot_owner_id = options.owner;

  if (!props.dealname) {
    console.error('ERROR: --name is required');
    process.exit(1);
  }

  const result = await crmCreate('deals', props);
  console.log(`Created deal #${result.id}`);
}

async function cmdDealsUpdate(options) {
  const props = {};
  if (options.name) props.dealname = options.name;
  if (options.stage) props.dealstage = options.stage;
  if (options.pipeline) props.pipeline = options.pipeline;
  if (options.amount) props.amount = options.amount;
  if (options.closedate) props.closedate = options.closedate;
  if (options.owner) props.hubspot_owner_id = options.owner;

  await crmUpdate('deals', options.id, props);
  console.log(`Updated deal #${options.id}`);
}

async function cmdDealsDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await crmDelete('deals', options.id);
  console.log(`Deleted deal #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// TICKETS
// ═══════════════════════════════════════════════════════════════════════════════

const TICKET_PROPS = 'subject,content,hs_pipeline,hs_pipeline_stage,hs_ticket_priority,createdate';

function ticketLabel(c) {
  const p = c.properties || {};
  return `#${String(c.id).padEnd(12)} ${(p.subject || '(no subject)').padEnd(40)} ${(p.hs_pipeline_stage || '').padEnd(15)} ${p.hs_ticket_priority || ''}`;
}

async function cmdTicketsList(options) {
  const resp = await crmList('tickets', { ...options, properties: TICKET_PROPS });
  displayCrmResults(resp, ticketLabel);
}

async function cmdTicketsSearch(options) {
  if (!options.query) { console.error('ERROR: --query is required'); process.exit(1); }
  const filters = [{ propertyName: 'subject', operator: 'CONTAINS_TOKEN', value: `*${options.query}*` }];
  const resp = await crmSearch('tickets', filters, { ...options, properties: TICKET_PROPS });
  displayCrmResults(resp, ticketLabel);
}

async function cmdTicketsRead(options) {
  const c = await crmRead('tickets', options.id, TICKET_PROPS);
  const p = c.properties || {};
  console.log(`Ticket #${c.id}`);
  console.log(`  Subject:    ${p.subject || '—'}`);
  console.log(`  Pipeline:   ${p.hs_pipeline || '—'}`);
  console.log(`  Stage:      ${p.hs_pipeline_stage || '—'}`);
  console.log(`  Priority:   ${p.hs_ticket_priority || '—'}`);
  console.log(`  Created:    ${fmtDate(p.createdate)}`);
  if (p.content) console.log(`\n  Content:\n  ${truncate(p.content, 500)}`);
}

async function cmdTicketsCreate(options) {
  const props = {};
  if (options.subject) props.subject = options.subject;
  if (options.content) props.content = options.content;
  if (options.pipeline) props.hs_pipeline = options.pipeline;
  if (options.stage) props.hs_pipeline_stage = options.stage;
  if (options.priority) props.hs_ticket_priority = options.priority;

  if (!props.subject) {
    console.error('ERROR: --subject is required');
    process.exit(1);
  }

  const result = await crmCreate('tickets', props);
  console.log(`Created ticket #${result.id}`);
}

async function cmdTicketsUpdate(options) {
  const props = {};
  if (options.subject) props.subject = options.subject;
  if (options.content) props.content = options.content;
  if (options.pipeline) props.hs_pipeline = options.pipeline;
  if (options.stage) props.hs_pipeline_stage = options.stage;
  if (options.priority) props.hs_ticket_priority = options.priority;

  await crmUpdate('tickets', options.id, props);
  console.log(`Updated ticket #${options.id}`);
}

async function cmdTicketsDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await crmDelete('tickets', options.id);
  console.log(`Deleted ticket #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// OWNERS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdOwnersList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.after) params.set('after', options.after);
  if (options.email) params.set('email', options.email);

  const resp = await apiFetch(`/crm/v3/owners/?${params}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No owners found.'); return; }
  for (const o of items) {
    console.log(`#${String(o.id).padEnd(12)} ${(`${o.firstName || ''} ${o.lastName || ''}`).trim().padEnd(25)} ${(o.email || '').padEnd(30)} ${o.teams?.map(t => t.name).join(', ') || ''}`);
  }
  console.log(`\n${items.length} owner(s)`);
}

async function cmdOwnersRead(options) {
  const o = await apiFetch(`/crm/v3/owners/${options.id}`);
  console.log(`Owner #${o.id}`);
  console.log(`  Name:    ${o.firstName || ''} ${o.lastName || ''}`);
  console.log(`  Email:   ${o.email || '—'}`);
  console.log(`  User ID: ${o.userId || '—'}`);
  console.log(`  Created: ${fmtDate(o.createdAt)}`);
  console.log(`  Updated: ${fmtDate(o.updatedAt)}`);
  if (o.teams?.length) {
    console.log(`  Teams:   ${o.teams.map(t => t.name).join(', ')}`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// PIPELINES
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdPipelinesList(options) {
  const objectType = options.objectType || 'deals';
  const resp = await apiFetch(`/crm/v3/pipelines/${objectType}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No pipelines found.'); return; }
  for (const p of items) {
    console.log(`\nPipeline: ${p.label} (id: ${p.id})`);
    if (p.stages?.length) {
      for (const s of p.stages) {
        console.log(`  Stage: ${s.label.padEnd(30)} id: ${s.id}  order: ${s.displayOrder}`);
      }
    }
  }
  console.log(`\n${items.length} pipeline(s)`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// ASSOCIATIONS (v4)
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdAssociationsList(options) {
  const resp = await apiFetch(`/crm/v4/objects/${options.fromType}/${options.fromId}/associations/${options.toType}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No associations found.'); return; }
  for (const a of items) {
    const types = a.associationTypes?.map(t => `${t.label || t.typeId} (${t.category})`).join(', ') || '';
    console.log(`  -> ${options.toType} #${a.toObjectId}  [${types}]`);
  }
  console.log(`\n${items.length} association(s)`);
}

async function cmdAssociationsCreate(options) {
  const body = [{
    associationSpec: {
      associationCategory: options.category || 'HUBSPOT_DEFINED',
      associationTypeId: parseInt(options.typeId, 10),
    },
    to: { id: options.toId },
  }];

  await apiFetch(`/crm/v4/objects/${options.fromType}/${options.fromId}/associations/${options.toType}`, {
    method: 'PUT',
    body: JSON.stringify(body),
  });
  console.log(`Created association: ${options.fromType} #${options.fromId} -> ${options.toType} #${options.toId}`);
}

async function cmdAssociationsDelete(options) {
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    process.exit(1);
  }
  await apiFetch(`/crm/v4/objects/${options.fromType}/${options.fromId}/associations/${options.toType}/${options.toId}`, {
    method: 'DELETE',
  });
  console.log(`Deleted association: ${options.fromType} #${options.fromId} -> ${options.toType} #${options.toId}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// PROPERTIES
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdPropertiesList(options) {
  const objectType = options.objectType || 'contacts';
  const resp = await apiFetch(`/crm/v3/properties/${objectType}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No properties found.'); return; }
  for (const p of items) {
    console.log(`  ${p.name.padEnd(35)} ${(p.type || '').padEnd(12)} ${(p.fieldType || '').padEnd(15)} ${p.label}`);
  }
  console.log(`\n${items.length} property(ies) for ${objectType}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// ENGAGEMENTS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdEngagementsList(engagementType, options) {
  const resp = await crmList(engagementType, { ...options, properties: options.properties || '' });
  const items = resp?.results || [];
  if (!items.length) { console.log(`No ${engagementType} found.`); return; }
  for (const item of items) {
    const p = item.properties || {};
    const title = p.hs_timestamp || p.hs_task_subject || p.hs_meeting_title || p.hs_email_subject || p.hs_note_body || '';
    console.log(`#${String(item.id).padEnd(12)} ${fmtDate(p.hs_timestamp || p.createdate).padEnd(12)} ${truncate(title, 60)}`);
  }
  console.log(`\n${items.length} ${engagementType}${resp.paging?.next?.after ? ` — next: --after ${resp.paging.next.after}` : ''}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CMS — Blog Posts
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdBlogPostsList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.after) params.set('after', options.after);
  if (options.state) params.set('state', options.state);

  const resp = await apiFetch(`/cms/v3/blogs/posts?${params}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No blog posts found.'); return; }
  for (const p of items) {
    console.log(`#${String(p.id).padEnd(12)} ${(p.state || '').padEnd(12)} ${fmtDate(p.publishDate).padEnd(12)} ${truncate(p.name || p.htmlTitle, 50)}`);
  }
  console.log(`\n${items.length} post(s)`);
}

async function cmdBlogPostsRead(options) {
  const p = await apiFetch(`/cms/v3/blogs/posts/${options.id}`);
  console.log(`Blog Post #${p.id}`);
  console.log(`  Title:      ${p.name || p.htmlTitle || '—'}`);
  console.log(`  Slug:       ${p.slug || '—'}`);
  console.log(`  State:      ${p.state || '—'}`);
  console.log(`  Published:  ${fmtDate(p.publishDate)}`);
  console.log(`  Author:     ${p.authorName || '—'}`);
  console.log(`  URL:        ${p.url || '—'}`);
}

async function cmdBlogPostsCreate(options) {
  const body = { name: options.name };
  if (options.slug) body.slug = options.slug;
  if (options.content) body.postBody = options.content;

  if (!body.name) {
    console.error('ERROR: --name is required');
    process.exit(1);
  }

  const result = await apiFetch('/cms/v3/blogs/posts', {
    method: 'POST',
    body: JSON.stringify(body),
  });
  console.log(`Created blog post #${result.id}`);
}

async function cmdBlogPostsUpdate(options) {
  const body = {};
  if (options.name) body.name = options.name;
  if (options.slug) body.slug = options.slug;
  if (options.content) body.postBody = options.content;

  await apiFetch(`/cms/v3/blogs/posts/${options.id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
  console.log(`Updated blog post #${options.id}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CMS — Pages
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdPagesList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.after) params.set('after', options.after);

  const resp = await apiFetch(`/cms/v3/pages/site-pages?${params}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No pages found.'); return; }
  for (const p of items) {
    console.log(`#${String(p.id).padEnd(12)} ${(p.state || '').padEnd(12)} ${truncate(p.name || p.htmlTitle, 50)}`);
  }
  console.log(`\n${items.length} page(s)`);
}

async function cmdPagesRead(options) {
  const p = await apiFetch(`/cms/v3/pages/site-pages/${options.id}`);
  console.log(`Page #${p.id}`);
  console.log(`  Title:      ${p.name || p.htmlTitle || '—'}`);
  console.log(`  Slug:       ${p.slug || '—'}`);
  console.log(`  State:      ${p.state || '—'}`);
  console.log(`  Published:  ${fmtDate(p.publishDate)}`);
  console.log(`  URL:        ${p.url || '—'}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CMS — Domains
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdDomainsList(options) {
  const resp = await apiFetch('/cms/v3/domains/');
  const items = resp?.results || [];
  if (!items.length) { console.log('No domains found.'); return; }
  for (const d of items) {
    const primary = d.isPrimaryBlogPost ? ' [primary-blog]' : '';
    const ssl = d.isSslEnabled ? ' [ssl]' : '';
    console.log(`#${String(d.id).padEnd(12)} ${(d.domain || '').padEnd(35)}${primary}${ssl}`);
  }
  console.log(`\n${items.length} domain(s)`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// MARKETING — Email Campaigns
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdEmailCampaignsList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.offset) params.set('offset', options.offset);

  const resp = await apiFetch(`/email/public/v1/campaigns?${params}`);
  const items = resp?.campaigns || [];
  if (!items.length) { console.log('No email campaigns found.'); return; }
  for (const c of items) {
    console.log(`#${String(c.id).padEnd(12)} ${(c.name || '(unnamed)').padEnd(40)} appId: ${c.appId || '—'}`);
  }
  console.log(`\n${items.length} campaign(s)`);
}

async function cmdEmailCampaignsRead(options) {
  const c = await apiFetch(`/email/public/v1/campaigns/${options.id}`);
  console.log(`Email Campaign #${c.id}`);
  console.log(`  Name:       ${c.name || '—'}`);
  console.log(`  Subject:    ${c.subject || '—'}`);
  console.log(`  Type:       ${c.type || '—'}`);
  console.log(`  App ID:     ${c.appId || '—'}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// MARKETING — Forms
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdFormsList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.after) params.set('after', options.after);

  const resp = await apiFetch(`/marketing/v3/forms/?${params}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No forms found.'); return; }
  for (const f of items) {
    console.log(`#${String(f.id).padEnd(38)} ${(f.name || '(unnamed)').padEnd(35)} ${f.formType || ''}`);
  }
  console.log(`\n${items.length} form(s)`);
}

async function cmdFormsRead(options) {
  const f = await apiFetch(`/marketing/v3/forms/${options.id}`);
  console.log(`Form #${f.id}`);
  console.log(`  Name:       ${f.name || '—'}`);
  console.log(`  Type:       ${f.formType || '—'}`);
  console.log(`  Created:    ${fmtDate(f.createdAt)}`);
  console.log(`  Updated:    ${fmtDate(f.updatedAt)}`);
  if (f.fieldGroups?.length) {
    console.log(`  Fields:`);
    for (const g of f.fieldGroups) {
      for (const field of (g.fields || [])) {
        console.log(`    - ${field.name} (${field.fieldType || field.type || ''})`);
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// MARKETING — Marketing Emails
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdMarketingEmailsList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.offset) params.set('offset', options.offset);

  const resp = await apiFetch(`/marketing-emails/v1/emails?${params}`);
  const items = resp?.objects || [];
  if (!items.length) { console.log('No marketing emails found.'); return; }
  for (const e of items) {
    console.log(`#${String(e.id).padEnd(12)} ${(e.state || '').padEnd(12)} ${(e.name || '(unnamed)').padEnd(40)} ${e.subject || ''}`);
  }
  console.log(`\n${items.length} email(s)`);
}

async function cmdMarketingEmailsRead(options) {
  const e = await apiFetch(`/marketing-emails/v1/emails/${options.id}`);
  console.log(`Marketing Email #${e.id}`);
  console.log(`  Name:       ${e.name || '—'}`);
  console.log(`  Subject:    ${e.subject || '—'}`);
  console.log(`  State:      ${e.state || '—'}`);
  console.log(`  Type:       ${e.emailType || '—'}`);
  console.log(`  Created:    ${fmtDate(e.created ? new Date(e.created).toISOString() : null)}`);
  console.log(`  Updated:    ${fmtDate(e.updated ? new Date(e.updated).toISOString() : null)}`);
}

async function cmdMarketingEmailsStats(options) {
  const e = await apiFetch(`/marketing-emails/v1/emails/${options.id}`);
  const stats = e.stats?.counters || {};
  console.log(`Marketing Email #${e.id} — ${e.name || '(unnamed)'}`);
  console.log(`  Sent:       ${stats.sent || 0}`);
  console.log(`  Delivered:  ${stats.delivered || 0}`);
  console.log(`  Opens:      ${stats.open || 0}`);
  console.log(`  Clicks:     ${stats.click || 0}`);
  console.log(`  Bounces:    ${stats.bounce || 0}`);
  console.log(`  Unsubs:     ${stats.unsubscribed || 0}`);
  console.log(`  Spam:       ${stats.spamreport || 0}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// MARKETING — Contact Lists
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdListsList(options) {
  const params = new URLSearchParams({ count: String(options.limit || CFG.maxResults) });
  if (options.offset) params.set('offset', options.offset);

  const resp = await apiFetch(`/contacts/v1/lists?${params}`);
  const items = resp?.lists || [];
  if (!items.length) { console.log('No contact lists found.'); return; }
  for (const l of items) {
    const dynamic = l.dynamic ? 'dynamic' : 'static';
    console.log(`#${String(l.listId).padEnd(10)} ${dynamic.padEnd(8)} ${(l.name || '(unnamed)').padEnd(35)} contacts: ${l.metaData?.size || 0}`);
  }
  console.log(`\n${items.length} list(s)`);
}

async function cmdListsRead(options) {
  const l = await apiFetch(`/contacts/v1/lists/${options.id}`);
  console.log(`Contact List #${l.listId}`);
  console.log(`  Name:       ${l.name || '—'}`);
  console.log(`  Type:       ${l.dynamic ? 'Dynamic (smart)' : 'Static'}`);
  console.log(`  Size:       ${l.metaData?.size || 0} contacts`);
  console.log(`  Created:    ${fmtDate(l.createdAt ? new Date(l.createdAt).toISOString() : null)}`);
  console.log(`  Updated:    ${fmtDate(l.updatedAt ? new Date(l.updatedAt).toISOString() : null)}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONVERSATIONS
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdConversationsList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.after) params.set('after', options.after);

  const resp = await apiFetch(`/conversations/v3/conversations/threads?${params}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No conversations found.'); return; }
  for (const c of items) {
    console.log(`#${String(c.id).padEnd(12)} ${(c.status || '').padEnd(10)} ${fmtDate(c.createdAt).padEnd(12)} ${truncate(c.latestMessagePreview || '', 50)}`);
  }
  console.log(`\n${items.length} conversation(s)`);
}

async function cmdConversationsRead(options) {
  const c = await apiFetch(`/conversations/v3/conversations/threads/${options.id}`);
  console.log(`Conversation #${c.id}`);
  console.log(`  Status:     ${c.status || '—'}`);
  console.log(`  Created:    ${fmtDate(c.createdAt)}`);
  console.log(`  Updated:    ${fmtDate(c.updatedAt)}`);
  console.log(`  Inbox:      ${c.inboxId || '—'}`);
  if (c.latestMessagePreview) {
    console.log(`\n  Latest message:\n  ${truncate(c.latestMessagePreview, 500)}`);
  }
}

async function cmdMessagesList(options) {
  const params = new URLSearchParams({ limit: String(options.limit || CFG.maxResults) });
  if (options.after) params.set('after', options.after);

  const resp = await apiFetch(`/conversations/v3/conversations/threads/${options.threadId}/messages?${params}`);
  const items = resp?.results || [];
  if (!items.length) { console.log('No messages found.'); return; }
  for (const m of items) {
    const sender = m.senders?.[0]?.name || m.senders?.[0]?.senderField || '(unknown)';
    console.log(`#${String(m.id).padEnd(12)} ${fmtDate(m.createdAt).padEnd(12)} ${sender.padEnd(25)} ${truncate(m.text || m.subject || '', 50)}`);
  }
  console.log(`\n${items.length} message(s)`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// AUTOMATION — Workflows
// ═══════════════════════════════════════════════════════════════════════════════

async function cmdWorkflowsList(options) {
  const resp = await apiFetch('/automation/v3/workflows');
  const items = resp?.workflows || [];
  if (!items.length) { console.log('No workflows found.'); return; }
  for (const w of items) {
    const enabled = w.enabled ? 'enabled' : 'disabled';
    console.log(`#${String(w.id).padEnd(10)} ${enabled.padEnd(10)} ${(w.type || '').padEnd(15)} ${w.name || '(unnamed)'}`);
  }
  console.log(`\n${items.length} workflow(s)`);
}

async function cmdWorkflowsRead(options) {
  const w = await apiFetch(`/automation/v3/workflows/${options.id}`);
  console.log(`Workflow #${w.id}`);
  console.log(`  Name:       ${w.name || '—'}`);
  console.log(`  Type:       ${w.type || '—'}`);
  console.log(`  Enabled:    ${w.enabled ? 'Yes' : 'No'}`);
  console.log(`  Created:    ${fmtDate(w.insertedAt ? new Date(w.insertedAt).toISOString() : null)}`);
  console.log(`  Updated:    ${fmtDate(w.updatedAt ? new Date(w.updatedAt).toISOString() : null)}`);
  if (w.actions?.length) {
    console.log(`  Actions:    ${w.actions.length} step(s)`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLI DEFINITION
// ═══════════════════════════════════════════════════════════════════════════════

const program = new Command();

program
  .name('hubspot')
  .description('OpenClaw HubSpot Skill — full HubSpot platform CLI')
  .version(pkg.version);

// ── Contacts ─────────────────────────────────────────────────────────────────

const contacts = program.command('contacts').description('Manage CRM contacts');

contacts.command('list').description('List contacts')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdContactsList));

contacts.command('search').description('Search contacts by email')
  .requiredOption('-q, --query <text>', 'Search query (email)')
  .option('-l, --limit <n>', 'Max results')
  .action(wrap(cmdContactsSearch));

contacts.command('read').description('Read contact details')
  .requiredOption('--id <id>', 'Contact ID')
  .action(wrap(cmdContactsRead));

contacts.command('create').description('Create a contact')
  .option('-e, --email <email>', 'Email address')
  .option('--firstname <name>', 'First name')
  .option('--lastname <name>', 'Last name')
  .option('--phone <phone>', 'Phone number')
  .option('--company <name>', 'Company name')
  .option('--lifecycle <stage>', 'Lifecycle stage')
  .action(wrap(cmdContactsCreate));

contacts.command('update').description('Update a contact')
  .requiredOption('--id <id>', 'Contact ID')
  .option('-e, --email <email>', 'Email address')
  .option('--firstname <name>', 'First name')
  .option('--lastname <name>', 'Last name')
  .option('--phone <phone>', 'Phone number')
  .option('--company <name>', 'Company name')
  .option('--lifecycle <stage>', 'Lifecycle stage')
  .action(wrap(cmdContactsUpdate));

contacts.command('delete').description('Delete a contact (requires --confirm)')
  .requiredOption('--id <id>', 'Contact ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdContactsDelete));

// ── Companies ────────────────────────────────────────────────────────────────

const companies = program.command('companies').description('Manage CRM companies');

companies.command('list').description('List companies')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdCompaniesList));

companies.command('search').description('Search companies by name')
  .requiredOption('-q, --query <text>', 'Search query (name)')
  .option('-l, --limit <n>', 'Max results')
  .action(wrap(cmdCompaniesSearch));

companies.command('read').description('Read company details')
  .requiredOption('--id <id>', 'Company ID')
  .action(wrap(cmdCompaniesRead));

companies.command('create').description('Create a company')
  .requiredOption('-n, --name <name>', 'Company name')
  .option('-d, --domain <domain>', 'Domain')
  .option('--industry <type>', 'Industry')
  .option('--phone <phone>', 'Phone number')
  .option('--city <city>', 'City')
  .action(wrap(cmdCompaniesCreate));

companies.command('update').description('Update a company')
  .requiredOption('--id <id>', 'Company ID')
  .option('-n, --name <name>', 'Company name')
  .option('-d, --domain <domain>', 'Domain')
  .option('--industry <type>', 'Industry')
  .option('--phone <phone>', 'Phone number')
  .option('--city <city>', 'City')
  .action(wrap(cmdCompaniesUpdate));

companies.command('delete').description('Delete a company (requires --confirm)')
  .requiredOption('--id <id>', 'Company ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdCompaniesDelete));

// ── Deals ────────────────────────────────────────────────────────────────────

const deals = program.command('deals').description('Manage CRM deals');

deals.command('list').description('List deals')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdDealsList));

deals.command('search').description('Search deals by name')
  .requiredOption('-q, --query <text>', 'Search query (deal name)')
  .option('-l, --limit <n>', 'Max results')
  .action(wrap(cmdDealsSearch));

deals.command('read').description('Read deal details')
  .requiredOption('--id <id>', 'Deal ID')
  .action(wrap(cmdDealsRead));

deals.command('create').description('Create a deal')
  .requiredOption('-n, --name <name>', 'Deal name')
  .option('-s, --stage <stage>', 'Deal stage')
  .option('-p, --pipeline <id>', 'Pipeline ID')
  .option('-a, --amount <amount>', 'Deal amount')
  .option('--closedate <date>', 'Close date (YYYY-MM-DD)')
  .option('--owner <id>', 'Owner ID')
  .action(wrap(cmdDealsCreate));

deals.command('update').description('Update a deal')
  .requiredOption('--id <id>', 'Deal ID')
  .option('-n, --name <name>', 'Deal name')
  .option('-s, --stage <stage>', 'Deal stage')
  .option('-p, --pipeline <id>', 'Pipeline ID')
  .option('-a, --amount <amount>', 'Deal amount')
  .option('--closedate <date>', 'Close date (YYYY-MM-DD)')
  .option('--owner <id>', 'Owner ID')
  .action(wrap(cmdDealsUpdate));

deals.command('delete').description('Delete a deal (requires --confirm)')
  .requiredOption('--id <id>', 'Deal ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdDealsDelete));

// ── Tickets ──────────────────────────────────────────────────────────────────

const tickets = program.command('tickets').description('Manage CRM tickets');

tickets.command('list').description('List tickets')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdTicketsList));

tickets.command('search').description('Search tickets by subject')
  .requiredOption('-q, --query <text>', 'Search query (subject)')
  .option('-l, --limit <n>', 'Max results')
  .action(wrap(cmdTicketsSearch));

tickets.command('read').description('Read ticket details')
  .requiredOption('--id <id>', 'Ticket ID')
  .action(wrap(cmdTicketsRead));

tickets.command('create').description('Create a ticket')
  .requiredOption('--subject <text>', 'Ticket subject')
  .option('--content <text>', 'Ticket content/description')
  .option('-p, --pipeline <id>', 'Pipeline ID')
  .option('-s, --stage <stage>', 'Pipeline stage')
  .option('--priority <level>', 'Priority (LOW, MEDIUM, HIGH)')
  .action(wrap(cmdTicketsCreate));

tickets.command('update').description('Update a ticket')
  .requiredOption('--id <id>', 'Ticket ID')
  .option('--subject <text>', 'Ticket subject')
  .option('--content <text>', 'Ticket content/description')
  .option('-p, --pipeline <id>', 'Pipeline ID')
  .option('-s, --stage <stage>', 'Pipeline stage')
  .option('--priority <level>', 'Priority (LOW, MEDIUM, HIGH)')
  .action(wrap(cmdTicketsUpdate));

tickets.command('delete').description('Delete a ticket (requires --confirm)')
  .requiredOption('--id <id>', 'Ticket ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdTicketsDelete));

// ── Owners ───────────────────────────────────────────────────────────────────

const owners = program.command('owners').description('List and read CRM owners');

owners.command('list').description('List owners')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .option('-e, --email <email>', 'Filter by email')
  .action(wrap(cmdOwnersList));

owners.command('read').description('Read owner details')
  .requiredOption('--id <id>', 'Owner ID')
  .action(wrap(cmdOwnersRead));

// ── Pipelines ────────────────────────────────────────────────────────────────

const pipelines = program.command('pipelines').description('List deal/ticket pipelines');

pipelines.command('list').description('List pipelines with stages')
  .option('-t, --object-type <type>', 'Object type: deals or tickets (default: deals)')
  .action(wrap(cmdPipelinesList));

// ── Associations (v4) ────────────────────────────────────────────────────────

const associations = program.command('associations').description('Manage CRM associations (v4)');

associations.command('list').description('List associations')
  .requiredOption('--from-type <type>', 'Source object type (e.g. contacts)')
  .requiredOption('--from-id <id>', 'Source object ID')
  .requiredOption('--to-type <type>', 'Target object type (e.g. companies)')
  .action(wrap(cmdAssociationsList));

associations.command('create').description('Create an association')
  .requiredOption('--from-type <type>', 'Source object type')
  .requiredOption('--from-id <id>', 'Source object ID')
  .requiredOption('--to-type <type>', 'Target object type')
  .requiredOption('--to-id <id>', 'Target object ID')
  .requiredOption('--type-id <typeId>', 'Association type ID')
  .option('--category <cat>', 'Category (default: HUBSPOT_DEFINED)')
  .action(wrap(cmdAssociationsCreate));

associations.command('delete').description('Delete an association (requires --confirm)')
  .requiredOption('--from-type <type>', 'Source object type')
  .requiredOption('--from-id <id>', 'Source object ID')
  .requiredOption('--to-type <type>', 'Target object type')
  .requiredOption('--to-id <id>', 'Target object ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdAssociationsDelete));

// ── Properties ───────────────────────────────────────────────────────────────

const properties = program.command('properties').description('List CRM object properties');

properties.command('list').description('List properties for an object type')
  .option('-t, --object-type <type>', 'Object type (default: contacts)')
  .action(wrap(cmdPropertiesList));

// ── Engagements ──────────────────────────────────────────────────────────────

const engagements = program.command('engagements').description('List CRM engagements');

engagements.command('notes').description('List notes')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .option('--properties <props>', 'Comma-separated properties')
  .action(wrap((opts) => cmdEngagementsList('notes', { ...opts, properties: opts.properties || 'hs_note_body,hs_timestamp' })));

engagements.command('emails').description('List emails')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .option('--properties <props>', 'Comma-separated properties')
  .action(wrap((opts) => cmdEngagementsList('emails', { ...opts, properties: opts.properties || 'hs_email_subject,hs_timestamp' })));

engagements.command('calls').description('List calls')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .option('--properties <props>', 'Comma-separated properties')
  .action(wrap((opts) => cmdEngagementsList('calls', { ...opts, properties: opts.properties || 'hs_call_title,hs_timestamp,hs_call_duration' })));

engagements.command('tasks').description('List tasks')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .option('--properties <props>', 'Comma-separated properties')
  .action(wrap((opts) => cmdEngagementsList('tasks', { ...opts, properties: opts.properties || 'hs_task_subject,hs_timestamp,hs_task_status' })));

engagements.command('meetings').description('List meetings')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .option('--properties <props>', 'Comma-separated properties')
  .action(wrap((opts) => cmdEngagementsList('meetings', { ...opts, properties: opts.properties || 'hs_meeting_title,hs_timestamp' })));

// ── CMS: Blog Posts ──────────────────────────────────────────────────────────

const blogPosts = program.command('blog-posts').description('Manage CMS blog posts');

blogPosts.command('list').description('List blog posts')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .option('-s, --state <state>', 'Filter by state (DRAFT, PUBLISHED, etc.)')
  .action(wrap(cmdBlogPostsList));

blogPosts.command('read').description('Read blog post details')
  .requiredOption('--id <id>', 'Blog post ID')
  .action(wrap(cmdBlogPostsRead));

blogPosts.command('create').description('Create a blog post')
  .requiredOption('-n, --name <title>', 'Post title')
  .option('--slug <slug>', 'URL slug')
  .option('--content <html>', 'Post body (HTML)')
  .action(wrap(cmdBlogPostsCreate));

blogPosts.command('update').description('Update a blog post')
  .requiredOption('--id <id>', 'Blog post ID')
  .option('-n, --name <title>', 'Post title')
  .option('--slug <slug>', 'URL slug')
  .option('--content <html>', 'Post body (HTML)')
  .action(wrap(cmdBlogPostsUpdate));

// ── CMS: Pages ───────────────────────────────────────────────────────────────

const pages = program.command('pages').description('Browse CMS site pages');

pages.command('list').description('List site pages')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdPagesList));

pages.command('read').description('Read page details')
  .requiredOption('--id <id>', 'Page ID')
  .action(wrap(cmdPagesRead));

// ── CMS: Domains ─────────────────────────────────────────────────────────────

const domains = program.command('domains').description('List CMS domains');

domains.command('list').description('List domains')
  .action(wrap(cmdDomainsList));

// ── Marketing: Email Campaigns ───────────────────────────────────────────────

const emailCampaigns = program.command('email-campaigns').description('Browse marketing email campaigns');

emailCampaigns.command('list').description('List email campaigns')
  .option('-l, --limit <n>', 'Max results')
  .option('--offset <n>', 'Pagination offset')
  .action(wrap(cmdEmailCampaignsList));

emailCampaigns.command('read').description('Read email campaign details')
  .requiredOption('--id <id>', 'Campaign ID')
  .action(wrap(cmdEmailCampaignsRead));

// ── Marketing: Forms ─────────────────────────────────────────────────────────

const forms = program.command('forms').description('Browse marketing forms');

forms.command('list').description('List forms')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdFormsList));

forms.command('read').description('Read form details')
  .requiredOption('--id <id>', 'Form ID')
  .action(wrap(cmdFormsRead));

// ── Marketing: Marketing Emails ──────────────────────────────────────────────

const marketingEmails = program.command('marketing-emails').description('Browse and analyze marketing emails');

marketingEmails.command('list').description('List marketing emails')
  .option('-l, --limit <n>', 'Max results')
  .option('--offset <n>', 'Pagination offset')
  .action(wrap(cmdMarketingEmailsList));

marketingEmails.command('read').description('Read marketing email details')
  .requiredOption('--id <id>', 'Email ID')
  .action(wrap(cmdMarketingEmailsRead));

marketingEmails.command('stats').description('Show marketing email statistics')
  .requiredOption('--id <id>', 'Email ID')
  .action(wrap(cmdMarketingEmailsStats));

// ── Marketing: Contact Lists ─────────────────────────────────────────────────

const lists = program.command('lists').description('Browse contact lists');

lists.command('list').description('List contact lists')
  .option('-l, --limit <n>', 'Max results')
  .option('--offset <n>', 'Pagination offset')
  .action(wrap(cmdListsList));

lists.command('read').description('Read contact list details')
  .requiredOption('--id <id>', 'List ID')
  .action(wrap(cmdListsRead));

// ── Conversations ────────────────────────────────────────────────────────────

const conversations = program.command('conversations').description('Browse inbox conversations');

conversations.command('list').description('List conversations')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdConversationsList));

conversations.command('read').description('Read conversation details')
  .requiredOption('--id <id>', 'Conversation/thread ID')
  .action(wrap(cmdConversationsRead));

// ── Messages ─────────────────────────────────────────────────────────────────

const messages = program.command('messages').description('List messages in a conversation');

messages.command('list').description('List messages in a conversation thread')
  .requiredOption('--thread-id <id>', 'Conversation thread ID')
  .option('-l, --limit <n>', 'Max results')
  .option('--after <cursor>', 'Pagination cursor')
  .action(wrap(cmdMessagesList));

// ── Automation: Workflows ────────────────────────────────────────────────────

const workflows = program.command('workflows').description('Browse automation workflows');

workflows.command('list').description('List workflows')
  .action(wrap(cmdWorkflowsList));

workflows.command('read').description('Read workflow details')
  .requiredOption('--id <id>', 'Workflow ID')
  .action(wrap(cmdWorkflowsRead));

// ── Parse ────────────────────────────────────────────────────────────────────

program.parse();
