#!/usr/bin/env node
'use strict';

const path = require('path');

const PRIVATE_FIELD_PATTERN = /(domain|hash|id|website|homepage|url|link)$/i;
const DEFAULT_BATCH_DIR = '/private/tmp/okki-go-batches';
const DEFAULT_OUTPUT_HARD_CAP = 100;
const DEFAULT_COMPANY_TARGET_COUNT = 30;
const DEFAULT_LOCALE = 'en-US';
const regionDisplayNamesByLocale = new Map();

function nowIso() {
  return new Date().toISOString();
}

function batchIdFromPath(filePath) {
  if (!filePath) return null;
  return path.basename(filePath).replace(/\.[^.]+$/, '');
}

function defaultRawPath(prefix) {
  const stamp = new Date().toISOString()
    .replace(/[-:]/g, '')
    .replace(/\..*$/, '')
    .replace('T', '-');
  return path.join(DEFAULT_BATCH_DIR, `${prefix}-${stamp}.json`);
}

function positiveIntegerOrNull(value) {
  if (value === null || value === undefined || value === '') return null;
  const number = Number(value);
  if (!Number.isInteger(number) || number < 0) return null;
  return number;
}

function resolveOutputBudget(options = {}) {
  const defaultCap = positiveIntegerOrNull(options.defaultCap);
  const hardCap = positiveIntegerOrNull(options.hardCap);
  const requestedLimit = positiveIntegerOrNull(options.requestedLimit);
  const resolvedDefaultCap = defaultCap === null ? 20 : defaultCap;
  const resolvedHardCap = hardCap === null ? DEFAULT_OUTPUT_HARD_CAP : hardCap;
  const requestedOrDefault = requestedLimit === null ? resolvedDefaultCap : requestedLimit;
  const appliedLimit = Math.min(requestedOrDefault, resolvedHardCap);
  const offset = Math.max(0, Number.isInteger(Number(options.offset)) ? Number(options.offset) : 0);

  return {
    defaultCap: resolvedDefaultCap,
    hardCap: resolvedHardCap,
    requestedLimit,
    appliedLimit,
    offset
  };
}

function outputBudgetMetadata(options = {}) {
  const budget = resolveOutputBudget(options);
  const returned = Math.max(0, Number.isInteger(Number(options.returned)) ? Number(options.returned) : 0);
  const availableFallback = budget.offset + returned;
  const available = Math.max(0, Number.isFinite(Number(options.available)) ? Number(options.available) : availableFallback);
  const nextOffset = budget.offset + returned;
  const truncated = nextOffset < available;

  return {
    returned,
    truncated,
    available,
    next_offset: truncated ? nextOffset : null,
    output_budget: {
      default_cap: budget.defaultCap,
      hard_cap: budget.hardCap,
      requested_limit: budget.requestedLimit,
      applied_limit: budget.appliedLimit,
      offset: budget.offset
    }
  };
}

function splitDebugMetadata(output, fields) {
  const normal = { ...output };
  const debug = {};
  for (const field of fields) {
    if (Object.prototype.hasOwnProperty.call(normal, field)) {
      debug[field] = normal[field];
      delete normal[field];
    }
  }
  return { normal, debug };
}

function applyDebugMetadata(output, fields, includeDebugMetadata) {
  const split = splitDebugMetadata(output, fields);
  if (includeDebugMetadata && Object.keys(split.debug).length > 0) {
    split.normal.debug_metadata = split.debug;
  }
  return split.normal;
}

function discoveryHealth(options = {}) {
  const targetCount = positiveIntegerOrNull(options.targetCount) || DEFAULT_COMPANY_TARGET_COUNT;
  const visibleUniqueCount = Math.max(0, Number.isFinite(Number(options.visibleUniqueCount))
    ? Number(options.visibleUniqueCount)
    : Number(options.returned) || 0);
  const usableCandidateCount = Math.max(0, Number.isFinite(Number(options.usableCandidateCount))
    ? Number(options.usableCandidateCount)
    : visibleUniqueCount);
  const available = Math.max(0, Number.isFinite(Number(options.available))
    ? Number(options.available)
    : usableCandidateCount);
  const nextOffset = positiveIntegerOrNull(options.nextOffset);
  const hasNextPage = Boolean(options.hasNextPage || (nextOffset !== null && nextOffset < available));
  const latestHealth = options.latestHealth && typeof options.latestHealth === 'object'
    ? options.latestHealth
    : null;
  const previousStreak = latestHealth && Number.isInteger(Number(latestHealth.low_yield_batch_streak))
    ? Number(latestHealth.low_yield_batch_streak)
    : 0;
  const lowYield = !hasNextPage && usableCandidateCount < targetCount;
  const lowYieldBatchStreak = lowYield ? previousStreak + 1 : 0;
  const status = hasNextPage ? 'page_available' : lowYield ? 'low_yield' : 'healthy';
  const recommendedMode = hasNextPage
    ? 'l0_pagination'
    : lowYield
      ? 'post_result_low_yield_diagnosis'
      : 'l0_default_search';
  const healthAction = hasNextPage
    ? 'fetch_next_page'
    : lowYieldBatchStreak >= 2
      ? 'offer_guided_strategy'
      : lowYield
        ? 'ask_refinement'
        : 'show_results';

  return {
    target_count: targetCount,
    visible_unique_count: visibleUniqueCount,
    usable_candidate_count: usableCandidateCount,
    has_next_page: hasNextPage,
    low_yield: lowYield,
    status,
    recommended_mode: recommendedMode,
    health_action: healthAction,
    low_yield_batch_streak: lowYieldBatchStreak,
    repeated_low_yield: lowYieldBatchStreak >= 2
  };
}

function nextActionFromDiscoveryHealth(health) {
  if (!health || typeof health !== 'object') return 'ask_unlock_selection';
  if (health.health_action === 'fetch_next_page') return 'paginate_next';
  if (health.health_action === 'ask_refinement') return 'offer_refinement';
  if (health.health_action === 'offer_guided_strategy') return 'offer_guided_strategy';
  if (health.health_action === 'offer_expansion') return 'offer_expansion';
  return 'ask_unlock_selection';
}

function budgetedItems(items, options = {}) {
  const list = Array.isArray(items) ? items : [];
  const budget = resolveOutputBudget(options);
  const available = Number.isFinite(Number(options.available)) ? Number(options.available) : list.length;
  const visible = list.slice(budget.offset, budget.offset + budget.appliedLimit);
  return {
    items: visible,
    metadata: outputBudgetMetadata({
      ...options,
      returned: visible.length,
      available,
      offset: budget.offset
    })
  };
}

function asArray(value) {
  if (Array.isArray(value)) return value;
  if (value == null) return [];
  return [value];
}

function responseList(body) {
  if (!body || typeof body !== 'object') return [];
  return asArray(body.list || body.data || body.rows || body.results);
}

function responseTotal(body, fallback) {
  if (!body || typeof body !== 'object') return fallback;
  const total = body.total ?? body.totalCount ?? body.count;
  return Number.isFinite(Number(total)) ? Number(total) : fallback;
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (value === 0) return value;
    if (value !== null && value !== undefined && String(value).trim() !== '') {
      return value;
    }
  }
  return null;
}

function cleanString(value) {
  if (value === null || value === undefined) return '';
  return String(value).replace(/\s+/g, ' ').trim();
}

function truncateText(value, maxChars = 240) {
  const text = cleanString(value);
  if (text.length <= maxChars) return text;
  return `${text.slice(0, Math.max(0, maxChars - 1)).trim()}...`;
}

function normalizeDomain(value) {
  if (!value) return '';
  let text = String(value).trim().toLowerCase();
  if (!text) return '';
  try {
    if (/^https?:\/\//i.test(text)) {
      text = new URL(text).hostname;
    }
  } catch (_) {
    return '';
  }
  text = text.replace(/^www\./, '').replace(/\/.*$/, '');
  return /^[a-z0-9.-]+\.[a-z]{2,}$/i.test(text) ? text : '';
}

function normalizeName(value) {
  return cleanString(value).toLowerCase().replace(/[^a-z0-9]+/gi, ' ').trim();
}

function companyName(record) {
  return cleanString(firstNonEmpty(
    record.company_name,
    record.companyName,
    record.name,
    record.company
  ));
}

function countryCode(record) {
  const value = firstNonEmpty(record.country_code, record.countryCode, record.country, record.country_code_iso);
  return value ? String(value).trim().toUpperCase() : '';
}

function normalizeLocale(value) {
  const locale = cleanString(value || DEFAULT_LOCALE);
  try {
    return Intl.DisplayNames.supportedLocalesOf([locale])[0] || DEFAULT_LOCALE;
  } catch (_) {
    return DEFAULT_LOCALE;
  }
}

function regionDisplayNames(locale) {
  const normalized = normalizeLocale(locale);
  if (!regionDisplayNamesByLocale.has(normalized)) {
    regionDisplayNamesByLocale.set(normalized, new Intl.DisplayNames([normalized], { type: 'region' }));
  }
  return regionDisplayNamesByLocale.get(normalized);
}

function countryName(recordOrCode, locale) {
  const code = typeof recordOrCode === 'string' ? recordOrCode.trim().toUpperCase() : countryCode(recordOrCode);
  if (!/^[A-Z]{2}$/.test(code)) return '';
  try {
    return cleanString(regionDisplayNames(locale).of(code)) || code;
  } catch (_) {
    return code;
  }
}

function compactCompanyRow(record, row, options = {}) {
  const code = countryCode(record);
  const type = compactList(firstNonEmpty(
    record.company_type,
    record.companyType,
    record.industry,
    record.primary_industry_name,
    record.primaryIndustryName
  ), 2);
  return {
    row,
    company_name: companyName(record) || 'Unknown company',
    country_code: code || null,
    country_name: countryName(code, options.locale) || null,
    company_type: type || '未知',
    has_email: positiveCount(firstNonEmpty(record.email_count, record.emailCount, record.emails_count)),
    has_whatsapp: positiveCount(firstNonEmpty(record.whatsapp_count, record.whatsappCount, record.whatsapps_count)),
    employees_count: firstNonEmpty(record.employees_count, record.employeeCount, record.employeesCount, record.employee_range) || '未知',
    founding_time: firstNonEmpty(record.founding_time, record.foundingTime, record.founded_year, record.foundedYear) || '',
    fit: fitText(record, options)
  };
}

function positiveCount(value) {
  if (value === null || value === undefined || value === '') return '未知';
  const number = Number(value);
  return Number.isFinite(number) ? number > 0 : '未知';
}

function compactList(value, maxItems = 4) {
  const items = Array.isArray(value) ? value : value == null ? [] : [value];
  return items
    .map(cleanString)
    .filter(Boolean)
    .slice(0, maxItems)
    .join(', ');
}

function fitText(record, options = {}) {
  const include = asArray(options.include).map((item) => String(item).toLowerCase()).filter(Boolean);
  const haystackValues = [
    record.company_type,
    record.companyType,
    record.industry,
    record.main_products,
    record.mainProducts,
    record.company_profile,
    record.description
  ];
  const haystack = haystackValues.flatMap((value) => Array.isArray(value) ? value : [value])
    .map(cleanString)
    .filter(Boolean);
  const text = haystack.join(' ').toLowerCase();
  const matched = include.filter((term) => text.includes(term)).slice(0, 4);
  if (matched.length > 0) return matched.join(', ');
  const productFit = compactList(firstNonEmpty(record.main_products, record.mainProducts, record.products), 4);
  if (productFit) return productFit;
  return truncateText(firstNonEmpty(record.company_profile, record.description, record.industry), 120);
}

function sanitizeForStdout(value) {
  if (Array.isArray(value)) return value.map(sanitizeForStdout);
  if (!value || typeof value !== 'object') return value;
  const cleaned = {};
  for (const [key, child] of Object.entries(value)) {
    if (PRIVATE_FIELD_PATTERN.test(key)) continue;
    cleaned[key] = sanitizeForStdout(child);
  }
  return cleaned;
}

function parseFields(value) {
  if (!value) return null;
  return String(value).split(',').map((field) => field.trim()).filter(Boolean);
}

function projectFields(row, fields) {
  if (!fields || fields.length === 0) return row;
  const projected = {};
  for (const field of fields) {
    if (Object.prototype.hasOwnProperty.call(row, field)) {
      projected[field] = row[field];
    }
  }
  return projected;
}

function selectedRows(rows, selector) {
  const indexes = parseRowSelector(selector);
  const byRow = new Map(rows.map((row) => [Number(row.row), row]));
  const selected = [];
  for (const rowNumber of indexes) {
    const row = byRow.get(rowNumber);
    if (row) selected.push(row);
  }
  return selected;
}

function parseRowSelector(selector) {
  if (!selector) throw new Error('Missing --rows');
  const values = [];
  for (const part of String(selector).split(',')) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    const range = trimmed.match(/^(\d+)-(\d+)$/);
    if (range) {
      const start = Number(range[1]);
      const end = Number(range[2]);
      if (start > end) throw new Error(`Invalid row range: ${trimmed}`);
      for (let value = start; value <= end; value += 1) values.push(value);
      continue;
    }
    if (!/^\d+$/.test(trimmed)) throw new Error(`Invalid row selector: ${trimmed}`);
    values.push(Number(trimmed));
  }
  if (values.length === 0) throw new Error('No rows selected.');
  return Array.from(new Set(values));
}

module.exports = {
  batchIdFromPath,
  budgetedItems,
  cleanString,
  compactCompanyRow,
  compactList,
  countryCode,
  countryName,
  DEFAULT_BATCH_DIR,
  DEFAULT_COMPANY_TARGET_COUNT,
  DEFAULT_LOCALE,
  DEFAULT_OUTPUT_HARD_CAP,
  defaultRawPath,
  discoveryHealth,
  normalizeLocale,
  normalizeDomain,
  normalizeName,
  nowIso,
  nextActionFromDiscoveryHealth,
  outputBudgetMetadata,
  parseFields,
  projectFields,
  resolveOutputBudget,
  responseList,
  responseTotal,
  sanitizeForStdout,
  selectedRows,
  applyDebugMetadata,
  splitDebugMetadata,
  truncateText
};
