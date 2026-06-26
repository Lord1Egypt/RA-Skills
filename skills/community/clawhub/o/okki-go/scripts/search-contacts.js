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
  defaultRawPath,
  nowIso,
  applyDebugMetadata,
  responseList,
  responseTotal
} = require('./lib/compact-output');

const DEFAULT_SIZE = 20;
const MAX_SIZE = 100;
const SUPPORTED_FIELDS = new Set([
  'name',
  'contact_match',
  'title',
  'title_type',
  'company_name',
  'working_company',
  'description',
  'primary_industry_name',
  'country_codes',
  'industry_codes',
  'has_email',
  'has_phone',
  'has_linkedin',
  'has_facebook',
  'has_company_name',
  'employees_min',
  'employees_max',
  'size',
  'page'
]);

function usage() {
  console.error([
    'Usage:',
    '  node scripts/search-contacts.js --json \'<contacts/search payload>\' --compact [--save-batch PATH] [--debug-metadata]',
    '  node scripts/search-contacts.js --file payload.json --compact [--debug-metadata]'
  ].join('\n'));
}

function parseArgs(argv) {
  const args = { json: null, file: null, compact: false, saveBatch: null, includePhone: false, limitOutput: null, debugMetadata: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--json') {
      args.json = argv[++i];
    } else if (arg === '--file') {
      args.file = argv[++i];
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--save-batch') {
      args.saveBatch = argv[++i];
    } else if (arg === '--include-phone') {
      args.includePhone = true;
    } else if (arg === '--limit-output') {
      args.limitOutput = positiveInt(argv[++i], '--limit-output');
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

function readPayload(args) {
  return args.file ? readJsonFile(args.file) : parseJson(args.json, '--json');
}

function normalizePayload(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    throw new Error('Payload must be a JSON object.');
  }
  const payload = {};
  for (const [key, value] of Object.entries(input)) {
    if (!SUPPORTED_FIELDS.has(key)) continue;
    if (value === null || value === undefined || value === '') continue;
    payload[key] = value;
  }
  payload.page = positiveInt(payload.page || 1, 'page');
  payload.size = positiveInt(payload.size || DEFAULT_SIZE, 'size');
  for (const key of ['has_email', 'has_phone', 'has_linkedin', 'has_facebook', 'has_company_name']) {
    if (key in payload) payload[key] = normalizeFlag(payload[key], key);
  }
  return payload;
}

function positiveInt(value, label) {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 1 || number > MAX_SIZE) {
    throw new Error(`${label} must be an integer between 1 and ${MAX_SIZE}.`);
  }
  return number;
}

function normalizeFlag(value, key) {
  if (value === true || value === 1 || value === '1' || String(value).toLowerCase() === 'true') return 1;
  if (value === false || value === 0 || value === '0' || String(value).toLowerCase() === 'false') return 0;
  throw new Error(`${key} must be 0 or 1.`);
}

function compactContact(record, row, options) {
  const item = {
    row,
    name: record.name || null,
    title: record.title || record.title_type || null,
    company: record.company || record.company_name || record.working_company || null,
    country: record.country || record.country_code || null,
    email: record.email || null,
    linkedin: record.linkedin ? 'available' : null
  };
  if (options.includePhone && record.phone) item.phone = record.phone;
  return item;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const payload = normalizePayload(readPayload(args));
  const response = await postJson('/api/v1/contacts/search', payload);
  const allContacts = responseList(response);
  const total = responseTotal(response, allContacts.length);
  const budgeted = budgetedItems(allContacts, {
    defaultCap: DEFAULT_SIZE,
    hardCap: MAX_SIZE,
    requestedLimit: args.limitOutput || payload.size,
    available: total
  });
  const contacts = budgeted.items;
  const saveBatch = args.saveBatch || defaultRawPath('contacts-search');
  writeJsonFile(saveBatch, {
    version: '1.0',
    created_at: nowIso(),
    request: payload,
    raw: response
  });

  const output = {
    charged: true,
    charge_type: 'credit_per_query',
    charge_summary: 'Contact search costs 1 credit per query; balance is not included in this wrapper response.',
    balance_available: false,
    total,
    batch_id: batchIdFromPath(saveBatch),
    contacts: contacts.map((record, index) => compactContact(record, index + 1, args)),
    raw_saved: true,
    raw_path: saveBatch,
    ...budgeted.metadata
  };

  if (args.compact) {
    process.stdout.write(`${JSON.stringify(contactNormalOutput(output, args.debugMetadata), null, 2)}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(response, null, 2)}\n`);
}

function contactNormalOutput(output, debugMetadata) {
  return applyDebugMetadata(output, [
    'batch_id',
    'raw_path',
    'output_budget'
  ], debugMetadata);
}

main().catch((error) => {
  console.error(error.message);
  usage();
  process.exit(2);
});
