#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { outputBudgetMetadata } = require('./lib/compact-output');

const VERSION = '1.1';
const FILE_MODE = 0o600;
const VALID_SOURCES = new Set(['user_confirmed', 'user_provided', 'user_provided_current_turn', 'agent_inferred', 'imported']);
const DEFAULT_WINDOW_DAYS = 30;

const B_CLASS_FIELDS = [
  ['offerings', 'usps'],
  ['offerings', 'applications'],
  ['offerings', 'certifications'],
  ['target_baseline', 'regions_primary'],
  ['target_baseline', 'decision_roles'],
  ['exclusions', 'industries_blacklist']
];

function usage() {
  return [
    'Usage:',
    '  node scripts/okki-state.js profile read [--now ISO]',
    '  node scripts/okki-state.js profile redact [--now ISO]',
    '  node scripts/okki-state.js profile upsert --json JSON [--now ISO]',
    '  node scripts/okki-state.js profile update-history --json JSON [--now ISO]',
    '  node scripts/okki-state.js profile reset',
    '',
    '  node scripts/okki-state.js viewed classify (--results-json JSON | --results-file PATH | --results-file -) [--window-days N] [--now ISO]',
    '  node scripts/okki-state.js viewed classify (--results-json JSON | --results-file PATH | --results-file -) [--compact] [--debug-metadata] [--window-days N] [--now ISO]',
    '  node scripts/okki-state.js viewed mark-shown (--results-json JSON | --results-file PATH | --results-file -) [--brief-summary TEXT] [--compact] [--debug-metadata] [--now ISO]',
    '  node scripts/okki-state.js viewed mark-unlocked --domain DOMAIN [--country-code ISO] [--compact] [--debug-metadata] [--now ISO]',
    '  node scripts/okki-state.js viewed mark-unlocked-batch (--json JSON | --file PATH) [--now ISO]',
    '  node scripts/okki-state.js viewed reset',
    '',
    'State path:',
    '  ${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/profile.json',
    '  ${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/viewed.json'
  ].join('\n');
}

function main(argv) {
  const parsed = parseArgs(argv);
  if (parsed.help) {
    console.log(usage());
    return;
  }

  const now = parseNow(parsed.options.now);
  const [scope, command] = parsed.positionals;

  if (!scope || !command) {
    throw userError(usage(), 2);
  }

  if (scope === 'profile') {
    handleProfile(command, parsed.options, now);
    return;
  }

  if (scope === 'viewed') {
    handleViewed(command, parsed.options, now);
    return;
  }

  throw userError(`Unsupported scope: ${scope}\n\n${usage()}`, 2);
}

function parseArgs(argv) {
  const options = {};
  const positionals = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      return { help: true, options, positionals };
    }

    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      if (!key) {
        throw userError('Invalid empty option', 2);
      }
      if (key === 'compact') {
        options.compact = true;
        continue;
      }
      if (key === 'debug-metadata') {
        options.debugMetadata = true;
        continue;
      }
      if (i + 1 >= argv.length || argv[i + 1].startsWith('--')) {
        throw userError(`Missing value for ${arg}`, 2);
      }
      options[toCamelCase(key)] = argv[i + 1];
      i += 1;
      continue;
    }

    positionals.push(arg);
  }

  return { help: false, options, positionals };
}

function toCamelCase(value) {
  return value.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
}

function handleProfile(command, options, now) {
  if (command === 'read') {
    const loaded = loadState('profile', now);
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated,
      chmodded: loaded.chmodded,
      profile: loaded.state
    });
    return;
  }

  if (command === 'redact') {
    const loaded = loadState('profile', now);
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated,
      chmodded: loaded.chmodded,
      redacted: true,
      profile: redactProfile(loaded.state)
    });
    return;
  }

  if (command === 'upsert') {
    const patch = parseJsonOption(options.json, '--json');
    const loaded = loadState('profile', now);
    const merged = deepMerge(deepClone(loaded.state), patch);
    const normalized = normalizeProfile(merged, now, { touch: true });
    saveState('profile', normalized.state);
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated || normalized.changed,
      profile: normalized.state
    });
    return;
  }

  if (command === 'update-history') {
    const patch = parseJsonOption(options.json, '--json');
    const loaded = loadState('profile', now);
    const profile = deepClone(loaded.state);
    profile.history = isPlainObject(profile.history) ? profile.history : {};
    profile.history.last_used_axes = isPlainObject(profile.history.last_used_axes)
      ? profile.history.last_used_axes
      : {};

    const axesPatch = isPlainObject(patch.last_used_axes) ? patch.last_used_axes : patch;
    profile.history.last_used_axes = deepMerge(profile.history.last_used_axes, axesPatch);
    profile.history.search_count = toSafeInteger(profile.history.search_count) + 1;

    const normalized = normalizeProfile(profile, now, { touch: true });
    saveState('profile', normalized.state);
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated || normalized.changed,
      profile: normalized.state
    });
    return;
  }

  if (command === 'reset') {
    const file = statePath('profile');
    removeFileIfExists(file);
    writeJson({
      ok: true,
      path: file,
      reset: true,
      profile: zeroProfile()
    });
    return;
  }

  throw userError(`Unsupported profile command: ${command}`, 2);
}

function handleViewed(command, options, now) {
  if (command === 'classify') {
    const results = parseResults(options);
    const windowDays = parseWindowDays(options.windowDays);
    const loaded = loadState('viewed', now);
    const classified = classifyResults(results, loaded.state, windowDays, now);
    if (options.compact) {
      writeJson({
        ok: true,
        path: loaded.path,
        recovered: loaded.recovered,
        migrated: loaded.migrated,
        chmodded: loaded.chmodded,
        window_days: windowDays,
        counts: {
          unlocked: classified.unlocked.length,
          seen: classified.seen.length,
          new: classified.new.length
        },
        ...stateDebugMetadata(compactStateBudget(results.length), options.debugMetadata)
      });
      return;
    }
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated,
      chmodded: loaded.chmodded,
      window_days: windowDays,
      counts: {
        unlocked: classified.unlocked.length,
        seen: classified.seen.length,
        new: classified.new.length
      },
      groups: classified
    });
    return;
  }

  if (command === 'mark-shown') {
    const results = parseResults(options);
    const loaded = loadState('viewed', now);
    const state = markShown(loaded.state, results, {
      now,
      briefSummary: options.briefSummary || ''
    });
    saveState('viewed', state.state);
    if (options.compact) {
      writeJson({
        ok: true,
        path: loaded.path,
        recovered: loaded.recovered,
        migrated: loaded.migrated || state.changed,
        updated: state.updated,
        total_items: state.state.items.length,
        ...stateDebugMetadata(compactStateBudget(state.state.items.length), options.debugMetadata)
      });
      return;
    }
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated || state.changed,
      updated: state.updated,
      viewed: state.state
    });
    return;
  }

  if (command === 'mark-unlocked') {
    const domain = normalizeDomain(options.domain);
    if (!domain) {
      throw userError('Missing or invalid --domain', 2);
    }
    const loaded = loadState('viewed', now);
    const state = markUnlocked(loaded.state, {
      domain,
      countryCode: normalizeCountryCode(options.countryCode),
      now
    });
    saveState('viewed', state.state);
    if (options.compact) {
      writeJson({
        ok: true,
        path: loaded.path,
        recovered: loaded.recovered,
        migrated: loaded.migrated || state.changed,
        updated: 1,
        total_items: state.state.items.length,
        ...stateDebugMetadata(compactStateBudget(state.state.items.length), options.debugMetadata)
      });
      return;
    }
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated || state.changed,
      viewed: state.state
    });
    return;
  }

  if (command === 'mark-unlocked-batch') {
    const rows = parseUnlockRows(options);
    const loaded = loadState('viewed', now);
    let state = loaded.state;
    let updated = 0;
    for (const row of rows) {
      const domain = normalizeDomain(row.domain || row.website || row.url || row.companyDomain || row.company_domain);
      if (!domain) continue;
      const result = markUnlocked(state, {
        domain,
        countryCode: normalizeCountryCode(row.country_code || row.countryCode),
        now
      });
      state = result.state;
      updated += 1;
    }
    saveState('viewed', state);
    writeJson({
      ok: true,
      path: loaded.path,
      recovered: loaded.recovered,
      migrated: loaded.migrated,
      updated,
      total_items: state.items.length,
      ...stateDebugMetadata(compactStateBudget(state.items.length), options.debugMetadata)
    });
    return;
  }

  if (command === 'reset') {
    const file = statePath('viewed');
    removeFileIfExists(file);
    writeJson({
      ok: true,
      path: file,
      reset: true,
      viewed: zeroViewed()
    });
    return;
  }

  throw userError(`Unsupported viewed command: ${command}`, 2);
}

function parseUnlockRows(options) {
  const source = options.json
    ? parseJsonOption(options.json, '--json')
    : options.file
      ? parseJsonOption(fs.readFileSync(options.file, 'utf8'), '--file')
      : null;

  if (!source) {
    throw userError('mark-unlocked-batch requires --json or --file', 2);
  }
  if (Array.isArray(source)) return source;
  if (Array.isArray(source.rows)) return source.rows;
  throw userError('mark-unlocked-batch input must be an array or an object with rows[]', 2);
}

function loadState(kind, now) {
  const file = statePath(kind);
  const zero = kind === 'profile' ? zeroProfile() : zeroViewed();
  const result = {
    path: file,
    state: zero,
    recovered: false,
    migrated: false,
    chmodded: false,
    backup_path: null
  };

  if (!fs.existsSync(file)) {
    return result;
  }

  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    result.recovered = true;
    result.backup_path = backupCorruptFile(file, now);
    return result;
  }

  result.chmodded = ensureMode(file);

  const normalized = kind === 'profile'
    ? normalizeProfile(parsed, now, { touch: false })
    : normalizeViewed(parsed, now);

  result.state = normalized.state;
  result.migrated = normalized.changed || result.chmodded;

  if (normalized.changed) {
    saveState(kind, normalized.state);
  }

  return result;
}

function saveState(kind, state) {
  const file = statePath(kind);
  ensureStateDir();
  writeAtomicJson(file, state);
}

function statePath(kind) {
  return path.join(stateDir(), `${kind === 'profile' ? 'profile' : 'viewed'}.json`);
}

function stateDir() {
  return path.join(configHome(), 'okki-go');
}

function configHome() {
  if (process.env.XDG_CONFIG_HOME) {
    return process.env.XDG_CONFIG_HOME;
  }
  const home = process.env.HOME || os.homedir();
  return path.join(home, '.config');
}

function ensureStateDir() {
  fs.mkdirSync(stateDir(), { recursive: true });
}

function writeAtomicJson(file, value) {
  ensureStateDir();
  const temp = `${file}.tmp-${process.pid}-${Date.now()}`;
  const body = `${JSON.stringify(value, null, 2)}\n`;
  try {
    fs.writeFileSync(temp, body, { mode: FILE_MODE });
    fs.renameSync(temp, file);
    fs.chmodSync(file, FILE_MODE);
  } catch (error) {
    removeFileIfExists(temp);
    throw error;
  }
}

function backupCorruptFile(file, now) {
  const backup = `${file}.corrupt.${fileTimestamp(now)}`;
  fs.renameSync(file, backup);
  return backup;
}

function ensureMode(file) {
  const mode = fs.statSync(file).mode & 0o777;
  if (mode !== FILE_MODE) {
    fs.chmodSync(file, FILE_MODE);
    return true;
  }
  return false;
}

function zeroProfile() {
  return {
    version: VERSION,
    updated_at: null,
    completeness: 0,
    company: {},
    offerings: {},
    target_baseline: {},
    outreach_identity: {
      preferred_language: null
    },
    sales_context: {},
    exclusions: {},
    history: {
      last_used_axes: {},
      search_count: 0
    }
  };
}

function zeroViewed() {
  return {
    version: VERSION,
    items: []
  };
}

function normalizeProfile(input, now, options) {
  const touch = Boolean(options && options.touch);
  const original = isPlainObject(input) ? deepClone(input) : {};
  const profile = deepMerge(zeroProfile(), original);
  let changed = !isPlainObject(input);

  if (profile.version !== VERSION) {
    profile.version = VERSION;
    changed = true;
  }

  for (const key of ['company', 'offerings', 'target_baseline', 'outreach_identity', 'sales_context', 'exclusions', 'history']) {
    if (!isPlainObject(profile[key])) {
      profile[key] = {};
      changed = true;
    }
  }

  if (!isPlainObject(profile.history.last_used_axes)) {
    profile.history.last_used_axes = {};
    changed = true;
  }
  const searchCount = toSafeInteger(profile.history.search_count);
  if (profile.history.search_count !== searchCount) {
    profile.history.search_count = searchCount;
    changed = true;
  }

  if (!Object.prototype.hasOwnProperty.call(profile.outreach_identity, 'preferred_language')) {
    profile.outreach_identity.preferred_language = null;
    changed = true;
  }

  for (const [parentKey, fieldKey] of B_CLASS_FIELDS) {
    const parent = profile[parentKey];
    if (!Object.prototype.hasOwnProperty.call(parent, fieldKey)) {
      continue;
    }
    const normalized = normalizeBClassArray(parent[fieldKey], now);
    parent[fieldKey] = normalized.value;
    if (normalized.changed) {
      changed = true;
    }
  }

  const completeness = computeCompleteness(profile);
  if (profile.completeness !== completeness) {
    profile.completeness = completeness;
    changed = true;
  }

  if (touch || !Object.prototype.hasOwnProperty.call(profile, 'updated_at')) {
    profile.updated_at = now.toISOString();
    changed = true;
  }

  return { state: profile, changed };
}

function normalizeBClassArray(value, now) {
  const array = Array.isArray(value) ? value : value == null ? [] : [value];
  let changed = !Array.isArray(value);
  const today = isoDate(now);
  const normalized = array.map((entry) => {
    if (isPlainObject(entry) && Object.prototype.hasOwnProperty.call(entry, 'value')) {
      const item = deepClone(entry);
      if (!VALID_SOURCES.has(item.source)) {
        item.source = 'agent_inferred';
        changed = true;
      }
      if (!item.updated_at) {
        item.updated_at = today;
        changed = true;
      }
      return item;
    }

    changed = true;
    return {
      value: isPlainObject(entry) ? deepClone(entry) : entry,
      source: 'agent_inferred',
      updated_at: today
    };
  });

  return { value: normalized, changed };
}

function computeCompleteness(profile) {
  const families = [
    hasCompanyIdentity(profile),
    hasOfferings(profile),
    hasTargetBaseline(profile),
    hasOutreachIdentity(profile),
    hasSalesContext(profile)
  ];
  const score = families.filter(Boolean).length / families.length;
  return Math.round(score * 100) / 100;
}

function hasCompanyIdentity(profile) {
  return Boolean(
    hasValue(profile.company.name) ||
    hasValue(profile.company.website) ||
    hasValue(profile.company.country) ||
    hasValue(profile.company.employee_range) ||
    hasValue(profile.company.founded_year) ||
    hasValue(profile.company.type)
  );
}

function hasOfferings(profile) {
  return Boolean(
    hasValue(profile.offerings.primary_products) ||
    hasValue(profile.offerings.product_keywords_zh) ||
    hasValue(profile.offerings.product_keywords_en) ||
    hasValue(profile.offerings.landing_page) ||
    hasTrustedBValues(profile.offerings.usps) ||
    hasTrustedBValues(profile.offerings.applications) ||
    hasTrustedBValues(profile.offerings.certifications)
  );
}

function hasTargetBaseline(profile) {
  return Boolean(
    hasValue(profile.target_baseline.company_types) ||
    hasValue(profile.target_baseline.employee_range) ||
    hasValue(profile.target_baseline.regions_excluded) ||
    hasTrustedBValues(profile.target_baseline.regions_primary) ||
    hasTrustedBValues(profile.target_baseline.decision_roles)
  );
}

function hasOutreachIdentity(profile) {
  return Boolean(
    hasValue(profile.outreach_identity.sender_name) ||
    hasValue(profile.outreach_identity.sender_email) ||
    hasValue(profile.outreach_identity.sender_title) ||
    hasValue(profile.outreach_identity.signature_block) ||
    hasValue(profile.outreach_identity.preferred_language)
  );
}

function hasSalesContext(profile) {
  const ctx = profile.sales_context;
  return Boolean(
    isPlainObject(ctx) &&
    (ctx.source === 'user_confirmed' || ctx.source === 'imported') &&
    (hasValue(ctx.goal) || hasValue(ctx.time_horizon) || hasValue(ctx.channel))
  );
}

function hasTrustedBValues(value) {
  return Array.isArray(value) && value.some((entry) => (
    isPlainObject(entry) &&
    hasValue(entry.value) &&
    (entry.source === 'user_confirmed' || entry.source === 'imported')
  ));
}

function hasValue(value) {
  if (Array.isArray(value)) {
    return value.length > 0;
  }
  if (isPlainObject(value)) {
    return Object.keys(value).length > 0;
  }
  return value !== null && value !== undefined && String(value).trim() !== '';
}

function redactProfile(profile) {
  const redacted = deepClone(profile);
  if (redacted.outreach_identity && hasValue(redacted.outreach_identity.sender_email)) {
    redacted.outreach_identity.sender_email = redactEmail(redacted.outreach_identity.sender_email);
  }
  if (redacted.outreach_identity && hasValue(redacted.outreach_identity.sender_name)) {
    redacted.outreach_identity.sender_name = redactName(redacted.outreach_identity.sender_name);
  }
  return redacted;
}

function redactEmail(value) {
  const email = String(value);
  const at = email.indexOf('@');
  if (at <= 0) {
    return redactName(email);
  }
  return `${email.slice(0, 1)}***${email.slice(at)}`;
}

function redactName(value) {
  const text = String(value);
  if (!text) {
    return '';
  }
  return `${text.slice(0, 1)}***`;
}

function normalizeViewed(input, now) {
  let sourceItems;
  let changed = false;

  if (Array.isArray(input)) {
    sourceItems = input;
    changed = true;
  } else if (isPlainObject(input) && Array.isArray(input.items)) {
    sourceItems = input.items;
  } else if (isPlainObject(input) && isPlainObject(input.domains)) {
    sourceItems = Object.keys(input.domains).map((domain) => {
      const item = input.domains[domain];
      return isPlainObject(item) ? Object.assign({ domain }, item) : { domain, shown_at: item };
    });
    changed = true;
  } else {
    sourceItems = [];
    changed = true;
  }

  const state = {
    version: VERSION,
    items: []
  };

  if (!isPlainObject(input) || input.version !== VERSION) {
    changed = true;
  }

  const byDomain = new Map();
  for (const rawItem of sourceItems) {
    const normalized = normalizeViewedItem(rawItem, now);
    if (!normalized.item.domain) {
      changed = true;
      continue;
    }
    if (normalized.changed) {
      changed = true;
    }
    const existing = byDomain.get(normalized.item.domain);
    byDomain.set(
      normalized.item.domain,
      existing ? mergeViewedItems(existing, normalized.item) : normalized.item
    );
    if (existing) {
      changed = true;
    }
  }

  state.items = Array.from(byDomain.values()).sort((a, b) => a.domain.localeCompare(b.domain));
  return { state, changed };
}

function normalizeViewedItem(rawItem, now) {
  const original = isPlainObject(rawItem) ? deepClone(rawItem) : { domain: rawItem };
  const item = {};
  let changed = !isPlainObject(rawItem);

  item.domain = normalizeDomain(original.domain || original.url || original.website || original.companyDomain || original.company_domain || original.companyWebsite || original.company_website);
  if (item.domain !== original.domain) {
    changed = true;
  }

  item.shown_at = validIsoOrNull(original.shown_at || original.viewed_at || original.last_seen_at);
  if ((original.shown_at || original.viewed_at || original.last_seen_at) && !item.shown_at) {
    changed = true;
  }

  item.brief_summary = hasValue(original.brief_summary) ? String(original.brief_summary) : '';
  item.country_code = normalizeCountryCode(original.country_code || original.countryCode);

  item.status = original.status === 'unlocked' ? 'unlocked' : 'viewed';
  if (item.status !== original.status) {
    changed = true;
  }

  item.unlocked_at = item.status === 'unlocked'
    ? validIsoOrNull(original.unlocked_at) || now.toISOString()
    : null;
  if (item.unlocked_at !== (original.unlocked_at || null)) {
    changed = true;
  }

  return { item, changed };
}

function mergeViewedItems(a, b) {
  const merged = deepClone(a);
  if (isAfter(b.shown_at, merged.shown_at)) {
    merged.shown_at = b.shown_at;
    merged.brief_summary = b.brief_summary || merged.brief_summary;
  }
  if (!merged.country_code && b.country_code) {
    merged.country_code = b.country_code;
  }
  if (b.status === 'unlocked' && isAfter(b.unlocked_at, merged.unlocked_at)) {
    merged.status = 'unlocked';
    merged.unlocked_at = b.unlocked_at;
  }
  return merged;
}

function markShown(viewed, results, options) {
  const state = normalizeViewed(viewed, options.now).state;
  const byDomain = new Map(state.items.map((item) => [item.domain, item]));
  let updated = 0;

  for (const result of results) {
    const domain = normalizeResultDomain(result);
    if (!domain) {
      continue;
    }
    const existing = byDomain.get(domain) || {
      domain,
      shown_at: null,
      brief_summary: '',
      status: 'viewed',
      unlocked_at: null,
      country_code: null
    };

    existing.shown_at = options.now.toISOString();
    existing.brief_summary = options.briefSummary || existing.brief_summary || '';
    existing.country_code = existing.country_code || resultCountryCode(result);
    if (existing.status !== 'unlocked') {
      existing.status = 'viewed';
      existing.unlocked_at = null;
    }

    byDomain.set(domain, existing);
    updated += 1;
  }

  return {
    state: {
      version: VERSION,
      items: Array.from(byDomain.values()).sort((a, b) => a.domain.localeCompare(b.domain))
    },
    updated,
    changed: updated > 0
  };
}

function markUnlocked(viewed, options) {
  const state = normalizeViewed(viewed, options.now).state;
  const byDomain = new Map(state.items.map((item) => [item.domain, item]));
  const existing = byDomain.get(options.domain) || {
    domain: options.domain,
    shown_at: options.now.toISOString(),
    brief_summary: '',
    status: 'viewed',
    unlocked_at: null,
    country_code: null
  };

  existing.status = 'unlocked';
  existing.unlocked_at = options.now.toISOString();
  existing.country_code = options.countryCode || existing.country_code || null;

  byDomain.set(options.domain, existing);
  return {
    state: {
      version: VERSION,
      items: Array.from(byDomain.values()).sort((a, b) => a.domain.localeCompare(b.domain))
    },
    changed: true
  };
}

function classifyResults(results, viewed, windowDays, now) {
  const byDomain = new Map(viewed.items.map((item) => [item.domain, item]));
  const groups = {
    unlocked: [],
    seen: [],
    new: []
  };

  for (const result of results) {
    const domain = normalizeResultDomain(result);
    const stateItem = domain ? byDomain.get(domain) : null;
    const entry = {
      domain,
      result,
      state: stateItem ? deepClone(stateItem) : null
    };

    if (stateItem && stateItem.status === 'unlocked' && isWithinWindow(stateItem.unlocked_at, windowDays, now)) {
      groups.unlocked.push(entry);
    } else if (stateItem && isWithinWindow(stateItem.shown_at, windowDays, now)) {
      groups.seen.push(entry);
    } else {
      groups.new.push(entry);
    }
  }

  return groups;
}

function normalizeResultDomain(result) {
  if (typeof result === 'string') {
    return normalizeDomain(result);
  }
  if (!isPlainObject(result)) {
    return null;
  }
  return normalizeDomain(
    result.domain ||
    result.website ||
    result.url ||
    result.companyDomain ||
    result.company_domain ||
    result.companyWebsite ||
    result.company_website ||
    result.homepage
  );
}

function resultCountryCode(result) {
  if (!isPlainObject(result)) {
    return null;
  }
  return normalizeCountryCode(result.country_code || result.countryCode || result.country);
}

function normalizeDomain(value) {
  if (!hasValue(value)) {
    return null;
  }
  let text = String(value).trim().toLowerCase();
  text = text.replace(/^mailto:/, '');
  if (text.includes('@') && !text.includes('/')) {
    text = text.slice(text.indexOf('@') + 1);
  }
  text = text.replace(/^[a-z][a-z0-9+.-]*:\/\//, '');
  text = text.replace(/^\/\//, '');
  text = text.split('/')[0].split('?')[0].split('#')[0];
  text = text.replace(/:\d+$/, '');
  text = text.replace(/^www\./, '');
  text = text.replace(/\.$/, '');
  return text || null;
}

function normalizeCountryCode(value) {
  if (!hasValue(value)) {
    return null;
  }
  const text = String(value).trim().toUpperCase();
  return /^[A-Z]{2}$/.test(text) ? text : text;
}

function parseResults(options) {
  const hasInlineJson = options.resultsJson !== undefined;
  const hasFile = options.resultsFile !== undefined;

  if (hasInlineJson && hasFile) {
    throw userError('Use only one of --results-json or --results-file', 2);
  }

  const parsed = hasFile
    ? parseJsonText(readResultsFile(options.resultsFile), `--results-file ${options.resultsFile}`)
    : parseJsonOption(options.resultsJson, '--results-json');

  if (!Array.isArray(parsed)) {
    throw userError('Results input must be a JSON array', 2);
  }
  return parsed;
}

function readResultsFile(filePath) {
  if (filePath === undefined) {
    throw userError('Missing --results-json or --results-file', 2);
  }
  if (filePath === '-') {
    return fs.readFileSync(0, 'utf8');
  }
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    throw userError(`Cannot read --results-file ${filePath}: ${error.message}`, 2);
  }
}

function parseJsonOption(value, optionName) {
  if (value === undefined) {
    throw userError(`Missing ${optionName}`, 2);
  }
  return parseJsonText(value, optionName);
}

function parseJsonText(value, optionName) {
  try {
    return JSON.parse(value);
  } catch (error) {
    throw userError(`Invalid JSON for ${optionName}: ${error.message}`, 2);
  }
}

function parseWindowDays(value) {
  if (value === undefined) {
    return DEFAULT_WINDOW_DAYS;
  }
  const number = Number(value);
  if (!Number.isInteger(number) || number <= 0) {
    throw userError('--window-days must be a positive integer', 2);
  }
  return number;
}

function parseNow(value) {
  if (!value) {
    return new Date();
  }
  const now = new Date(value);
  if (Number.isNaN(now.getTime())) {
    throw userError('--now must be a valid ISO date/time', 2);
  }
  return now;
}

function validIsoOrNull(value) {
  if (!value) {
    return null;
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date.toISOString();
}

function isWithinWindow(value, windowDays, now) {
  const date = value ? new Date(value) : null;
  if (!date || Number.isNaN(date.getTime())) {
    return false;
  }
  const ageMs = now.getTime() - date.getTime();
  return ageMs >= 0 && ageMs <= windowDays * 24 * 60 * 60 * 1000;
}

function isAfter(candidate, current) {
  if (!candidate) {
    return false;
  }
  if (!current) {
    return true;
  }
  return new Date(candidate).getTime() > new Date(current).getTime();
}

function isoDate(now) {
  return now.toISOString().slice(0, 10);
}

function fileTimestamp(now) {
  return now.toISOString().replace(/[:.]/g, '-');
}

function toSafeInteger(value) {
  const number = Number(value);
  return Number.isSafeInteger(number) && number >= 0 ? number : 0;
}

function deepMerge(target, patch) {
  if (!isPlainObject(target) || !isPlainObject(patch)) {
    return deepClone(patch);
  }
  const result = deepClone(target);
  for (const key of Object.keys(patch)) {
    if (isPlainObject(result[key]) && isPlainObject(patch[key])) {
      result[key] = deepMerge(result[key], patch[key]);
    } else {
      result[key] = deepClone(patch[key]);
    }
  }
  return result;
}

function deepClone(value) {
  if (value === undefined) {
    return undefined;
  }
  return JSON.parse(JSON.stringify(value));
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function removeFileIfExists(file) {
  try {
    fs.unlinkSync(file);
  } catch (error) {
    if (error.code !== 'ENOENT') {
      throw error;
    }
  }
}

function writeJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function compactStateBudget(available) {
  return outputBudgetMetadata({
    defaultCap: 0,
    hardCap: 0,
    returned: 0,
    available
  });
}

function stateDebugMetadata(metadata, debugMetadata) {
  return applyDebugMetadataForState(metadata, debugMetadata);
}

function applyDebugMetadataForState(metadata, debugMetadata) {
  const output = { ...metadata };
  const debug = {};
  if (Object.prototype.hasOwnProperty.call(output, 'output_budget')) {
    debug.output_budget = output.output_budget;
    delete output.output_budget;
  }
  if (debugMetadata && Object.keys(debug).length > 0) {
    output.debug_metadata = debug;
  }
  return output;
}

function userError(message, code) {
  const error = new Error(message);
  error.exitCode = code;
  return error;
}

if (require.main === module) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exit(error.exitCode || 1);
  }
}

module.exports = {
  normalizeDomain,
  normalizeProfile,
  normalizeViewed,
  classifyResults,
  computeCompleteness,
  redactProfile
};
