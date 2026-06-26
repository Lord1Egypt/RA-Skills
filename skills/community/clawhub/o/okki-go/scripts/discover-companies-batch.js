#!/usr/bin/env node
'use strict';

const {
  parseJson,
  postJson,
  readJsonFile,
  writeJsonFile
} = require('./lib/okki-api');
const {
  batchIdFromPath,
  budgetedItems,
  compactCompanyRow,
  DEFAULT_COMPANY_TARGET_COUNT,
  defaultRawPath,
  discoveryHealth,
  applyDebugMetadata,
  nextActionFromDiscoveryHealth,
  normalizeDomain,
  normalizeName,
  nowIso,
  responseList,
  responseTotal
} = require('./lib/compact-output');
const {
  readLatestBatchPointer,
  writeSelectionHandle,
  writeLatestBatchPointer
} = require('./lib/batch-state');
const {
  normalizeCompanySearchPayload,
  splitCompanySearchPayload
} = require('./lib/company-search-payloads');
const {
  addCompanySearchDisplayTable
} = require('./lib/company-search-display');

const MAX_PAGE_SIZE = 50;
const DEFAULT_CONCURRENCY = 1;
const TRANSIENT_RETRY_DELAY_MS = 300;

function usage() {
  console.error([
    'Usage:',
    '  node scripts/discover-companies-batch.js --plan /path/plan.json --target-count N --save-batch /private/tmp/okki-go-batches/batch.json --compact [--locale en-US] [--debug-metadata]',
    '  node scripts/discover-companies-batch.js --json \'<plan>\' --compact [--locale en-US] [--debug-metadata]'
  ].join('\n'));
}

function parseArgs(argv) {
  const args = {
    plan: null,
    json: null,
    targetCount: null,
    saveBatch: null,
    compact: false,
    concurrency: DEFAULT_CONCURRENCY,
    locale: null,
    debugMetadata: false
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--plan') {
      args.plan = argv[++i];
    } else if (arg === '--json') {
      args.json = argv[++i];
    } else if (arg === '--target-count') {
      args.targetCount = positiveInt(argv[++i], '--target-count');
    } else if (arg === '--save-batch') {
      args.saveBatch = argv[++i];
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--locale') {
      args.locale = argv[++i];
    } else if (arg === '--concurrency') {
      args.concurrency = positiveInt(argv[++i], '--concurrency');
    } else if (arg === '--debug-metadata') {
      args.debugMetadata = true;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if ((args.plan ? 1 : 0) + (args.json ? 1 : 0) !== 1) {
    throw new Error('Provide exactly one of --plan or --json.');
  }
  return args;
}

function positiveInt(value, label) {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 1) throw new Error(`${label} must be a positive integer.`);
  return number;
}

function readPlan(args) {
  const plan = args.plan ? readJsonFile(args.plan) : parseJson(args.json, '--json');
  if (!plan || typeof plan !== 'object' || Array.isArray(plan)) {
    throw new Error('Plan must be a JSON object.');
  }
  if (!Array.isArray(plan.payloads) || plan.payloads.length === 0) {
    throw new Error('Plan must include payloads[].');
  }
  return plan;
}

function buildRequests(plan) {
  const requests = [];
  let splitQueryCount = 0;
  let originalQueryCount = 0;
  for (const payloadPlan of plan.payloads) {
    const pages = positiveInt(payloadPlan.pages || 1, 'payload.pages');
    const basePayload = { ...payloadPlan };
    delete basePayload.pages;
    const normalized = normalizeCompanySearchPayload(basePayload, { defaultSize: 50 }).payload;
    const size = Math.min(normalized.size || 50, MAX_PAGE_SIZE);
    const startFrom = normalized.from || 0;
    const splitSearch = splitCompanySearchPayload(normalized);
    originalQueryCount += pages;
    splitQueryCount += splitSearch.payloads.length * pages;
    for (const splitPayload of splitSearch.payloads) {
      for (let page = 0; page < pages; page += 1) {
        const payload = { ...splitPayload, size, from: startFrom + (page * size) };
        requests.push({ payload, page: page + 1 });
      }
    }
  }
  requests.splitQueryCount = splitQueryCount;
  requests.originalQueryCount = originalQueryCount;
  return requests;
}

async function runWithConcurrency(items, concurrency, worker) {
  const results = new Array(items.length);
  let next = 0;

  async function runOne() {
    while (next < items.length) {
      const index = next;
      next += 1;
      results[index] = await worker(items[index], index);
    }
  }

  const runners = Array.from(
    { length: Math.min(Math.max(1, concurrency), items.length) },
    () => runOne()
  );
  await Promise.all(runners);
  return results;
}

function compilePatterns(values) {
  return (Array.isArray(values) ? values : [])
    .map((value) => String(value).trim())
    .filter(Boolean)
    .map((value) => new RegExp(value, 'i'));
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isTransientCompanySearchError(error) {
  const statusCode = Number(error && error.statusCode);
  if ([429, 502, 503, 504].includes(statusCode)) return true;

  const text = [
    error && error.message,
    error && typeof error.body === 'string' ? error.body : '',
    error && error.body && typeof error.body === 'object' ? JSON.stringify(error.body) : ''
  ].filter(Boolean).join(' ');

  return /系统繁忙|system busy|temporarily unavailable|timeout|timed out|rate[- ]?limit|too many requests/i.test(text);
}

async function postCompanySearchWithRetry(payload) {
  try {
    return await postJson('/api/v1/companies/search-advanced', payload);
  } catch (error) {
    if (!isTransientCompanySearchError(error)) throw error;
    await sleep(TRANSIENT_RETRY_DELAY_MS);
    return postJson('/api/v1/companies/search-advanced', payload);
  }
}

function searchableText(record) {
  return [
    record.company_name,
    record.companyName,
    record.name,
    record.company_type,
    record.companyType,
    record.industry,
    record.main_products,
    record.mainProducts,
    record.company_profile,
    record.description
  ].flatMap((value) => Array.isArray(value) ? value : [value])
    .filter((value) => value !== null && value !== undefined)
    .join(' ');
}

function shouldKeep(record, includePatterns, excludePatterns) {
  const text = searchableText(record);
  if (excludePatterns.some((pattern) => pattern.test(text))) return false;
  if (includePatterns.length === 0) return true;
  return includePatterns.some((pattern) => pattern.test(text));
}

function dedupe(records) {
  const byKey = new Map();
  for (const record of records) {
    const domain = normalizeDomain(record.domain || record.companyDomain || record.company_domain);
    const name = normalizeName(record.company_name || record.companyName || record.name);
    const key = domain ? `domain:${domain}` : name ? `name:${name}` : `raw:${byKey.size}`;
    if (!byKey.has(key)) byKey.set(key, record);
  }
  return Array.from(byKey.values());
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const plan = readPlan(args);
  const targetCount = Math.min(args.targetCount || plan.target_count || DEFAULT_COMPANY_TARGET_COUNT, 100);
  const saveBatch = args.saveBatch || defaultRawPath('discover-companies');
  const includePatterns = compilePatterns(plan.include);
  const excludePatterns = compilePatterns(plan.exclude);
  const requests = buildRequests(plan);
  const latestPointer = readLatestBatchPointer({ ignoreErrors: true });

  const pageResults = await runWithConcurrency(requests, args.concurrency, async (request) => {
    const body = await postCompanySearchWithRetry(request.payload);
    return {
      body,
      rows: responseList(body),
      total: responseTotal(body, responseList(body).length)
    };
  });

  const rawRecords = pageResults.flatMap((result) => result.rows);
  const filtered = rawRecords.filter((record) => shouldKeep(record, includePatterns, excludePatterns));
  const deduped = dedupe(filtered);
  const budgeted = budgetedItems(deduped, {
    defaultCap: targetCount,
    hardCap: 100,
    requestedLimit: targetCount,
    available: deduped.length
  });
  const selected = budgeted.items;
  const batchRows = selected.map((record, index) => ({
    row: index + 1,
    domain: record.domain || record.companyDomain || record.company_domain || null,
    country_code: record.country_code || record.countryCode || null,
    company_name: record.company_name || record.companyName || record.name || null,
    id: record.id || record.companyHashId || record.company_hash_id || null,
    raw: record
  }));

  const batch = {
    version: '1.0',
    created_at: nowIso(),
    request_summary: plan.request_summary || '',
    target_count: targetCount,
    rows: batchRows
  };
  const output = {
    batch_id: batchIdFromPath(saveBatch),
    scanned_pages: requests.length,
    raw_count: rawRecords.length,
    deduped_count: deduped.length,
    rows: selected.map((record, index) => compactCompanyRow(record, index + 1, {
      include: plan.include,
      locale: args.locale
    })),
    private_mapping_saved: true,
    raw_path: saveBatch,
    ...budgeted.metadata
  };
  if (requests.splitQueryCount > requests.originalQueryCount) {
    output.split_query_count = requests.splitQueryCount;
  }
  output.discovery_health = discoveryHealth({
    targetCount,
    visibleUniqueCount: selected.length,
    usableCandidateCount: deduped.length,
    available: deduped.length,
    nextOffset: budgeted.metadata.next_offset,
    hasNextPage: budgeted.metadata.truncated,
    latestHealth: latestPointer && latestPointer.discovery_health
  });
  output.next_action = nextActionFromDiscoveryHealth(output.discovery_health);
  writeJsonFile(saveBatch, batch);
  const selection = writeSelectionHandle({
    batchPath: saveBatch,
    displayedRows: selected.length,
    requestSummary: batch.request_summary,
    discoveryHealth: output.discovery_health
  });
  output.selection_handle = selection.handle;
  writeLatestBatchPointer({
    batchPath: saveBatch,
    displayedRows: selected.length,
    requestSummary: batch.request_summary,
    discoveryHealth: output.discovery_health
  });

  if (args.compact) {
    process.stdout.write(`${JSON.stringify(companyBatchNormalOutput(output, {
      debugMetadata: args.debugMetadata,
      locale: args.locale
    }), null, 2)}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(batch, null, 2)}\n`);
}

function companyBatchNormalOutput(output, options = {}) {
  return addCompanySearchDisplayTable(applyDebugMetadata(output, [
    'batch_id',
    'private_mapping_saved',
    'raw_path',
    'output_budget'
  ], options.debugMetadata), { locale: options.locale });
}

main().catch((error) => {
  console.error(error.message);
  usage();
  process.exit(2);
});
