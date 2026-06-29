'use strict';

const KEYWORD_FIELDS = ['companyTypeKeywords', 'productKeywords', 'industryKeywords'];
const MAX_KEYWORDS_PER_FIELD = 5;
const MAX_COMPANY_TYPE_KEYWORDS_PER_REQUEST = 1;
const MAX_COMPANY_SEARCH_SIZE = 50;
const CJK_COMPANY_ROLE_TERMS = [
  '系统集成商',
  '集成商',
  '工程商',
  '工程公司',
  '承包商',
  '供应商',
  '服务商',
  '经销商',
  '分销商',
  '进口商',
  '代理商',
  '批发商',
  '零售商'
];
const ENGLISH_COMPANY_ROLE_TERMS = [
  'system integrator',
  'integrator',
  'engineering company',
  'contractor',
  'supplier',
  'service provider',
  'distributor',
  'importer',
  'agent',
  'wholesaler',
  'retailer'
];
const SUPPORTED_COMPANY_SEARCH_FIELDS = new Set([
  'companyTypeKeywords',
  'productKeywords',
  'industryKeywords',
  'includeCountry',
  'excludeCountry',
  'withEmails',
  'crossFieldOperator',
  'from',
  'size'
]);

function normalizeCompanySearchPayload(input, options = {}) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    throw new Error('Payload must be a JSON object.');
  }

  const normalized = {};
  const dropped = [];
  const supportedFields = options.supportedFields || SUPPORTED_COMPANY_SEARCH_FIELDS;

  for (const [key, value] of Object.entries(input)) {
    if (!supportedFields.has(key)) {
      dropped.push(key);
      continue;
    }
    if (value === undefined || value === null || value === '') continue;
    normalized[key] = value;
  }

  normalizeArrayField(normalized, 'companyTypeKeywords');
  normalizeArrayField(normalized, 'productKeywords');
  normalizeArrayField(normalized, 'industryKeywords');
  normalizeArrayField(normalized, 'includeCountry', true);
  normalizeArrayField(normalized, 'excludeCountry', true);
  validateCountryCodes(normalized, 'includeCountry');
  validateCountryCodes(normalized, 'excludeCountry');
  normalizeWithEmails(normalized);
  normalizeCrossFieldOperator(normalized);
  normalizePagination(normalized, options);
  ensureSearchable(normalized);
  validateCompanyTypeKeywords(normalized);

  return { payload: normalized, dropped, warnings: guardrailWarnings(normalized) };
}

function normalizeArrayField(payload, key, uppercase) {
  if (!(key in payload)) return;

  const values = Array.isArray(payload[key]) ? payload[key] : [payload[key]];
  const cleaned = values
    .filter((value) => typeof value === 'string' || typeof value === 'number')
    .map((value) => String(value).trim())
    .filter(Boolean)
    .map((value) => uppercase ? value.toUpperCase() : value);

  if (cleaned.length === 0) {
    delete payload[key];
  } else {
    payload[key] = Array.from(new Set(cleaned));
  }
}

function validateCountryCodes(payload, key) {
  if (!(key in payload)) return;

  const invalid = payload[key].filter((value) => !/^[A-Z]{2}$/.test(value));
  if (invalid.length > 0) {
    throw new Error(`${key} must contain ISO 3166-1 alpha-2 country codes. Invalid: ${invalid.join(', ')}`);
  }
}

function normalizeWithEmails(payload) {
  if (!('withEmails' in payload)) return;

  const value = payload.withEmails;
  if (value === true || value === 1 || value === '1' || String(value).toLowerCase() === 'true') {
    payload.withEmails = 1;
  } else if (value === false || value === 0 || value === '0' || String(value).toLowerCase() === 'false') {
    payload.withEmails = 0;
  } else {
    throw new Error('withEmails must be 0 or 1.');
  }
}

function normalizeCrossFieldOperator(payload) {
  if (!('crossFieldOperator' in payload)) return;

  const value = String(payload.crossFieldOperator).trim().toUpperCase();
  if (value !== 'AND' && value !== 'OR') {
    throw new Error('crossFieldOperator must be "AND" or "OR".');
  }
  payload.crossFieldOperator = value;
}

function normalizePagination(payload, options = {}) {
  const defaultSize = positiveIntegerOrDefault(options.defaultSize, 30);
  const from = payload.from === undefined ? 0 : Number(payload.from);
  const size = payload.size === undefined ? defaultSize : Number(payload.size);

  if (!Number.isInteger(from) || from < 0) {
    throw new Error('from must be a non-negative integer.');
  }
  if (!Number.isInteger(size) || size < 1) {
    throw new Error('size must be a positive integer.');
  }

  payload.from = from;
  payload.size = Math.min(size, MAX_COMPANY_SEARCH_SIZE);
}

function ensureSearchable(payload) {
  const hasKeywords = KEYWORD_FIELDS
    .some((key) => Array.isArray(payload[key]) && payload[key].length > 0);

  if (!hasKeywords) {
    throw new Error('Payload must include at least one of productKeywords, industryKeywords, or companyTypeKeywords.');
  }
}

function validateCompanyTypeKeywords(payload) {
  const values = Array.isArray(payload.companyTypeKeywords) ? payload.companyTypeKeywords : [];
  const invalid = values.filter(isCompoundCompanyTypeKeyword);
  if (invalid.length === 0) return;

  throw new Error([
    `Invalid compound \`companyTypeKeywords\` term: ${invalid.join(', ')}.`,
    '`companyTypeKeywords` must contain pure buyer/company role terms such as 系统集成商, 工程商, or 进口商.',
    'Move product, industry, application, or project-scenario words into `productKeywords` or `industryKeywords`.',
    'Target-side first still applies: use target-buyer profile keywords, not copied seller product, SKU, model, or service-list terms.'
  ].join(' '));
}

function isCompoundCompanyTypeKeyword(value) {
  const term = String(value || '').trim();
  if (!term) return false;
  if (isCompoundCjkCompanyTypeKeyword(term)) return true;
  return isCompoundEnglishCompanyTypeKeyword(term);
}

function isCompoundCjkCompanyTypeKeyword(term) {
  if (CJK_COMPANY_ROLE_TERMS.includes(term)) return false;
  return CJK_COMPANY_ROLE_TERMS.some((role) => {
    return term.endsWith(role) && term.slice(0, -role.length).trim().length > 0;
  });
}

function isCompoundEnglishCompanyTypeKeyword(term) {
  const normalized = term.toLowerCase().replace(/[-_/]+/g, ' ').replace(/\s+/g, ' ').trim();
  if (ENGLISH_COMPANY_ROLE_TERMS.includes(normalized)) return false;
  return ENGLISH_COMPANY_ROLE_TERMS.some((role) => {
    return normalized.endsWith(` ${role}`);
  });
}

function guardrailWarnings(payload) {
  const warnings = [];
  const usedKeywordFields = KEYWORD_FIELDS
    .filter((key) => Array.isArray(payload[key]) && payload[key].length > 0);

  if (payload.withEmails === 1) {
    warnings.push('withEmails:1 narrows company discovery; use it only when the user asked for email-only leads.');
  }

  if (payload.crossFieldOperator === 'AND' && usedKeywordFields.length === KEYWORD_FIELDS.length) {
    warnings.push('AND with productKeywords + companyTypeKeywords + industryKeywords can over-narrow the first search.');
  }

  if (payload.crossFieldOperator === 'OR' && Array.isArray(payload.includeCountry) && payload.includeCountry.length > 0) {
    warnings.push('Global OR with includeCountry can be noisy; prefer changing target-side terms before using OR.');
  }

  return warnings;
}

function splitCompanySearchPayload(payload, options = {}) {
  const maxKeywords = positiveIntegerOrDefault(options.maxKeywordsPerField, MAX_KEYWORDS_PER_FIELD);
  const chunksByField = KEYWORD_FIELDS.map((field) => {
    const values = Array.isArray(payload[field]) ? payload[field] : [];
    const fieldMaxKeywords = field === 'companyTypeKeywords'
      ? positiveIntegerOrDefault(options.maxCompanyTypeKeywordsPerRequest, MAX_COMPANY_TYPE_KEYWORDS_PER_REQUEST)
      : maxKeywords;
    return {
      field,
      chunks: values.length > fieldMaxKeywords ? chunk(values, fieldMaxKeywords) : [values]
    };
  });

  const splitPayloads = [];
  for (const companyTypeKeywords of chunksByField[0].chunks) {
    for (const productKeywords of chunksByField[1].chunks) {
      for (const industryKeywords of chunksByField[2].chunks) {
        const next = { ...payload };
        applyKeywordChunk(next, 'companyTypeKeywords', companyTypeKeywords);
        applyKeywordChunk(next, 'productKeywords', productKeywords);
        applyKeywordChunk(next, 'industryKeywords', industryKeywords);
        splitPayloads.push(next);
      }
    }
  }

  return {
    payloads: splitPayloads,
    splitQueryCount: splitPayloads.length
  };
}

function applyKeywordChunk(payload, field, values) {
  if (!Array.isArray(values) || values.length === 0) {
    delete payload[field];
    return;
  }
  payload[field] = values;
}

function chunk(values, size) {
  const chunks = [];
  for (let index = 0; index < values.length; index += size) {
    chunks.push(values.slice(index, index + size));
  }
  return chunks.length > 0 ? chunks : [[]];
}

function positiveIntegerOrDefault(value, fallback) {
  const number = Number(value);
  return Number.isInteger(number) && number > 0 ? number : fallback;
}

module.exports = {
  KEYWORD_FIELDS,
  MAX_COMPANY_SEARCH_SIZE,
  MAX_COMPANY_TYPE_KEYWORDS_PER_REQUEST,
  MAX_KEYWORDS_PER_FIELD,
  normalizeCompanySearchPayload,
  SUPPORTED_COMPANY_SEARCH_FIELDS,
  isCompoundCompanyTypeKeyword,
  splitCompanySearchPayload
};
