#!/usr/bin/env node
'use strict';

const fs = require('fs');
const http = require('http');
const https = require('https');
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
  parseFields,
  projectFields,
  responseList,
  responseTotal
} = require('./lib/compact-output');
const { authHeaders, writeJsonFile } = require('./lib/okki-api');
const {
  readLatestBatchPointer,
  writeSelectionHandle,
  writeLatestBatchPointer
} = require('./lib/batch-state');
const {
  KEYWORD_FIELDS,
  normalizeCompanySearchPayload,
  splitCompanySearchPayload
} = require('./lib/company-search-payloads');
const {
  addCompanySearchDisplayTable
} = require('./lib/company-search-display');

const BASE_URL = process.env.OKKIGO_BASE_URL || 'https://go.okki.ai';
const TRANSIENT_RETRY_DELAY_MS = 300;

function usage() {
  console.error([
    'Usage:',
    '  node scripts/search-companies.js --json \'<search-advanced payload>\'',
    '  node scripts/search-companies.js --file /path/to/payload.json',
    '  node scripts/search-companies.js --json \'<payload>\' --compact [--locale en-US] [--target-count 30] [--limit-output 50] [--fields company_name,country_name,email_count,fit] [--save-raw PATH] [--debug-metadata]',
    '',
    'Example:',
    '  node scripts/search-companies.js --json \'{"productKeywords":["auto glass"],"companyTypeKeywords":["importer","distributor"],"includeCountry":["DE"],"withEmails":0,"size":20}\' --compact --locale zh-CN'
  ].join('\n'));
}

function parseArgs(argv) {
  const args = {
    json: null,
    file: null,
    printPayload: false,
    compact: false,
    fields: null,
    limitOutput: null,
    saveRaw: null,
    locale: null,
    targetCount: null,
    debugMetadata: false
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--json') {
      args.json = argv[++i];
    } else if (arg === '--file') {
      args.file = argv[++i];
    } else if (arg === '--print-payload') {
      args.printPayload = true;
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--fields') {
      args.fields = argv[++i];
    } else if (arg === '--limit-output') {
      args.limitOutput = parsePositiveInteger(argv[++i], '--limit-output');
    } else if (arg === '--save-raw') {
      args.saveRaw = argv[++i];
    } else if (arg === '--locale') {
      args.locale = argv[++i];
    } else if (arg === '--target-count') {
      args.targetCount = parsePositiveInteger(argv[++i], '--target-count');
    } else if (arg === '--debug-metadata') {
      args.debugMetadata = true;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if ((args.json ? 1 : 0) + (args.file ? 1 : 0) !== 1) {
    throw new Error('Provide exactly one of --json or --file.');
  }
  return args;
}

function parsePositiveInteger(value, label) {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 1) {
    throw new Error(`${label} must be a positive integer.`);
  }
  return number;
}

function readPayload(args) {
  if (args.json) return parseJson(args.json, '--json');
  return parseJson(fs.readFileSync(args.file, 'utf8'), args.file);
}

function parseJson(source, label) {
  try {
    return JSON.parse(source);
  } catch (error) {
    throw new Error(`Invalid JSON in ${label}: ${error.message}`);
  }
}

function normalizePayload(input) {
  return normalizeCompanySearchPayload(input);
}

function postJson(urlString, headers, payload) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlString);
    const transport = url.protocol === 'http:' ? http : https;
    const body = JSON.stringify(payload);
    const request = transport.request({
      method: 'POST',
      hostname: url.hostname,
      port: url.port || (url.protocol === 'http:' ? 80 : 443),
      path: `${url.pathname}${url.search}`,
      headers: Object.assign({}, headers, {
        'Content-Length': Buffer.byteLength(body)
      })
    }, (response) => {
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        resolve({
          statusCode: response.statusCode || 0,
          body: Buffer.concat(chunks).toString('utf8')
        });
      });
    });
    request.on('error', reject);
    request.write(body);
    request.end();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isTransientCompanySearchResponse(response) {
  if (!response) return false;
  if ([429, 502, 503, 504].includes(Number(response.statusCode))) return true;
  return /系统繁忙|system busy|temporarily unavailable|timeout|timed out|rate[- ]?limit|too many requests/i
    .test(String(response.body || ''));
}

async function postCompanySearchWithRetry(urlString, headers, payload) {
  const response = await postJson(urlString, headers, payload);
  if (!isTransientCompanySearchResponse(response)) return response;
  await sleep(TRANSIENT_RETRY_DELAY_MS);
  return postJson(urlString, headers, payload);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { payload, dropped, warnings } = normalizePayload(readPayload(args));
  const splitSearch = splitCompanySearchPayload(payload);
  const searchPayloads = splitSearch.payloads;

  if (args.printPayload) {
    console.error(JSON.stringify({ payload, payloads: searchPayloads, dropped, warnings }, null, 2));
    return;
  } else if (dropped.length > 0) {
    console.error(`Dropped unsupported fields: ${dropped.join(', ')}`);
  }
  for (const warning of warnings) {
    console.error(`Search guardrail warning: ${warning}`);
  }

  const headers = authHeaders();

  const responses = [];
  for (const searchPayload of searchPayloads) {
    const response = await postCompanySearchWithRetry(`${BASE_URL}/api/v1/companies/search-advanced`, headers, searchPayload);
    if (response.statusCode < 200 || response.statusCode >= 300) {
      console.error(response.body);
      process.exit(response.statusCode >= 400 && response.statusCode < 600 ? 1 : 2);
    }
    responses.push(response);
  }
  if (args.compact) {
    const body = mergeSearchBodies(responses.map((response, index) => (
      parseJson(response.body || '{}', `OKKI Go response ${index + 1}`)
    )));
    const rawPath = args.saveRaw || defaultRawPath('search-companies');
    const compact = compactSearchResponse(body, {
      payload,
      requestFrom: payload.from || 0,
      rawPath,
      fields: parseFields(args.fields),
      limitOutput: args.limitOutput || payload.size || DEFAULT_COMPANY_TARGET_COUNT,
      locale: args.locale,
      targetCount: args.targetCount || payload.size || DEFAULT_COMPANY_TARGET_COUNT,
      latestPointer: readLatestBatchPointer({ ignoreErrors: true }),
      splitQueryCount: splitSearch.splitQueryCount
    });
    writeJsonFile(rawPath, compact.raw);
    const selection = writeSelectionHandle({
      batchPath: rawPath,
      displayedRows: compact.output.returned,
      requestSummary: compact.raw.request_summary,
      discoveryHealth: compact.output.discovery_health
    });
    compact.output.selection_handle = selection.handle;
    writeLatestBatchPointer({
      batchPath: rawPath,
      displayedRows: compact.output.returned,
      requestSummary: compact.raw.request_summary,
      discoveryHealth: compact.output.discovery_health
    });
    process.stdout.write(`${JSON.stringify(companyNormalOutput(compact.output, {
      debugMetadata: args.debugMetadata,
      locale: args.locale
    }), null, 2)}\n`);
    return;
  }
  const outputBody = responses.length === 1
    ? responses[0].body
    : JSON.stringify(mergeSearchBodies(responses.map((response, index) => (
      parseJson(response.body || '{}', `OKKI Go response ${index + 1}`)
    ))), null, 2);
  process.stdout.write(outputBody);
  if (outputBody && !outputBody.endsWith('\n')) process.stdout.write('\n');
}

function mergeSearchBodies(bodies) {
  const rows = [];
  let total = 0;
  for (const body of bodies) {
    const list = responseList(body);
    rows.push(...list);
    total += responseTotal(body, list.length);
  }
  return {
    total,
    list: dedupeCompanyRecords(rows)
  };
}

function dedupeCompanyRecords(records) {
  const byKey = new Map();
  for (const record of records) {
    const domain = normalizeDomain(record.domain || record.companyDomain || record.company_domain);
    const name = normalizeName(record.company_name || record.companyName || record.name);
    const key = domain ? `domain:${domain}` : name ? `name:${name}` : `raw:${byKey.size}`;
    if (!byKey.has(key)) byKey.set(key, record);
  }
  return Array.from(byKey.values());
}

function companyNormalOutput(output, options = {}) {
  return addCompanySearchDisplayTable(applyDebugMetadata(output, [
    'batch_id',
    'private_mapping_saved',
    'raw_path',
    'output_budget'
  ], options.debugMetadata), { locale: options.locale });
}

function compactSearchResponse(body, options) {
  const list = responseList(body);
  const total = responseTotal(body, list.length);
  const budgeted = budgetedItems(list, {
    defaultCap: 50,
    hardCap: 100,
    requestedLimit: options.limitOutput,
    available: total
  });
  const absoluteNextOffset = (options.requestFrom || 0) + budgeted.metadata.returned;
  const absoluteTruncated = absoluteNextOffset < total;
  const fields = options.fields;
  const displayRows = budgeted.items.map((record, index) => (
    compactCompanyRow(record, index + 1, { locale: options.locale })
  ));
  const rows = displayRows.map((row) => projectFields(row, fields));
  const rawRows = list.map((record, index) => ({
    row: index + 1,
    domain: record.domain || record.companyDomain || record.company_domain || null,
    country_code: record.country_code || record.countryCode || null,
    company_name: record.company_name || record.companyName || record.name || null,
    id: record.id || record.companyHashId || record.company_hash_id || null,
    raw: record
  }));
  const output = {
    total,
    batch_id: batchIdFromPath(options.rawPath),
    display_rows: displayRows,
    rows,
    private_mapping_saved: true,
    raw_path: options.rawPath,
    ...budgeted.metadata,
    truncated: absoluteTruncated,
    next_offset: absoluteTruncated ? absoluteNextOffset : null
  };
  if (options.splitQueryCount > 1) output.split_query_count = options.splitQueryCount;
  output.discovery_health = discoveryHealth({
    targetCount: options.targetCount,
    visibleUniqueCount: rows.length,
    usableCandidateCount: rows.length,
    available: budgeted.metadata.available,
    nextOffset: output.next_offset,
    hasNextPage: output.truncated,
    latestHealth: options.latestPointer && options.latestPointer.discovery_health
  });
  output.next_action = nextActionFromDiscoveryHealth(output.discovery_health);
  return {
    output,
    raw: {
      version: '1.0',
      created_at: nowIso(),
      request_summary: summarizePayload(options.payload),
      rows: rawRows
    }
  };
}

function summarizePayload(payload) {
  const countries = Array.isArray(payload.includeCountry) ? payload.includeCountry.join(',') : '';
  const keywords = KEYWORD_FIELDS
    .flatMap((key) => Array.isArray(payload[key]) ? payload[key] : [])
    .slice(0, 8)
    .join(', ');
  return [countries, keywords].filter(Boolean).join(' ');
}

main().catch((error) => {
  console.error(error.message);
  usage();
  process.exit(2);
});
