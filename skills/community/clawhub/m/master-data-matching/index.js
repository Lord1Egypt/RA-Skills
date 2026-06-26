/**
 * Master Data Intelligent Matching System
 * Production-ready skill for entity resolution across business domains
 *
 * Features:
 * - Business Domain Isolation (procurement/finance/sales/HR)
 * - OCR Field to Schema Visual Line Mapping (confidence colors)
 * - Dual-Path Entity Retrieval (exact + vector, thresholds 0.92/0.70)
 * - Field Value Verification (4 states)
 * - Human-in-the-Loop at every stage
 * - Active Learning from corrections
 */

// ─── Domain Schemas ─────────────────────────────────────────────────────────

export const DOMAIN_SCHEMAS = {
  procurement: {
    name: 'Procurement',
    fields: [
      { name: 'vendor_name', type: 'string', weight: 0.3, critical: true },
      { name: 'vendor_code', type: 'string', weight: 0.25, critical: true },
      { name: 'tax_id', type: 'string', weight: 0.2, critical: true },
      { name: 'contact_person', type: 'string', weight: 0.05, critical: false },
      { name: 'email', type: 'string', weight: 0.05, critical: false },
      { name: 'phone', type: 'string', weight: 0.05, critical: false },
      { name: 'address', type: 'string', weight: 0.05, critical: false },
      { name: 'bank_account', type: 'string', weight: 0.05, critical: false },
    ],
  },
  finance: {
    name: 'Finance',
    fields: [
      { name: 'company_name', type: 'string', weight: 0.3, critical: true },
      { name: 'registration_number', type: 'string', weight: 0.25, critical: true },
      { name: 'tax_id', type: 'string', weight: 0.2, critical: true },
      { name: 'fiscal_year_end', type: 'date', weight: 0.05, critical: false },
      { name: 'registered_capital', type: 'number', weight: 0.05, critical: false },
      { name: 'legal_representative', type: 'string', weight: 0.05, critical: false },
      { name: 'address', type: 'string', weight: 0.05, critical: false },
      { name: 'bank_account', type: 'string', weight: 0.05, critical: false },
    ],
  },
  sales: {
    name: 'Sales',
    fields: [
      { name: 'customer_name', type: 'string', weight: 0.3, critical: true },
      { name: 'customer_code', type: 'string', weight: 0.25, critical: true },
      { name: 'industry', type: 'string', weight: 0.1, critical: false },
      { name: 'contact_person', type: 'string', weight: 0.1, critical: false },
      { name: 'email', type: 'string', weight: 0.1, critical: false },
      { name: 'phone', type: 'string', weight: 0.05, critical: false },
      { name: 'address', type: 'string', weight: 0.05, critical: false },
      { name: 'credit_limit', type: 'number', weight: 0.05, critical: false },
    ],
  },
  hr: {
    name: 'HR',
    fields: [
      { name: 'employee_name', type: 'string', weight: 0.3, critical: true },
      { name: 'employee_id', type: 'string', weight: 0.25, critical: true },
      { name: 'id_number', type: 'string', weight: 0.2, critical: true },
      { name: 'department', type: 'string', weight: 0.05, critical: false },
      { name: 'position', type: 'string', weight: 0.05, critical: false },
      { name: 'email', type: 'string', weight: 0.05, critical: false },
      { name: 'phone', type: 'string', weight: 0.05, critical: false },
      { name: 'hire_date', type: 'date', weight: 0.05, critical: false },
    ],
  },
};

// ─── Confidence Colors ───────────────────────────────────────────────────────

export const CONFIDENCE_COLORS = {
  high: { color: '#22c55e', label: 'green', description: 'High confidence (>= 0.92)' },
  medium: { color: '#eab308', label: 'yellow', description: 'Medium confidence (0.70 - 0.92)' },
  low: { color: '#ef4444', label: 'red', description: 'Low confidence (< 0.70)' },
  dbOnly: { color: '#3b82f6', label: 'blue', description: 'Database only (no OCR data)' },
};

// ─── Field Value Verification States ─────────────────────────────────────────

export const VERIFICATION_STATES = {
  MATCH: 'match',
  MISMATCH: 'mismatch',
  NEW_INFO: 'new_info',
  DB_ONLY: 'db_only',
};

// ─── Matching Thresholds ──────────────────────────────────────────────────────

export const MATCHING_THRESHOLDS = {
  exactMatch: 0.92,
  vectorSemantic: 0.70,
};

// ─── Core Functions ──────────────────────────────────────────────────────────

/**
 * Validate domain name
 * @param {string} domain
 * @returns {boolean}
 */
export function isValidDomain(domain) {
  return Object.hasOwn(DOMAIN_SCHEMAS, domain);
}

/**
 * Get schema for a domain
 * @param {string} domain
 * @returns {object|null}
 */
export function getDomainSchema(domain) {
  return DOMAIN_SCHEMAS[domain] || null;
}

/**
 * Get all supported domains
 * @returns {string[]}
 */
export function getSupportedDomains() {
  return Object.keys(DOMAIN_SCHEMAS);
}

/**
 * Normalize string for comparison (trim, lowercase, collapse whitespace)
 * @param {string} str
 * @returns {string}
 */
export function normalizeString(str) {
  if (!str || typeof str !== 'string') return '';
  return str.trim().toLowerCase().replace(/\s+/g, ' ');
}

/**
 * Compute Levenshtein distance between two strings
 * @param {string} a
 * @param {string} b
 * @returns {number}
 */
export function levenshteinDistance(a, b) {
  const m = a.length;
  const n = b.length;
  const dp = Array.from({ length: m + 1 }, (_, i) =>
    Array.from({ length: n + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0))
  );
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
      }
    }
  }
  return dp[m][n];
}

/**
 * Compute string similarity (Jaccard of character bigrams, normalized)
 * @param {string} a
 * @param {string} b
 * @returns {number} 0-1
 */
export function stringSimilarity(a, b) {
  if (!a && !b) return 1.0;
  if (!a || !b) return 0.0;
  const normalize = (s) => s.toLowerCase().replace(/\s+/g, '');
  a = normalize(a);
  b = normalize(b);
  if (a === b) return 1.0;
  const getBigrams = (s) => {
    const set = new Set();
    for (let i = 0; i < s.length - 1; i++) set.add(s.slice(i, i + 2));
    return set;
  };
  const bgA = getBigrams(a);
  const bgB = getBigrams(b);
  const intersection = new Set([...bgA].filter((x) => bgB.has(x)));
  const union = new Set([...bgA, ...bgB]);
  return union.size === 0 ? 0 : intersection.size / union.size;
}

/**
 * Compute field-level similarity based on field type
 * @param {object} field - field definition
 * @param {any} ocrValue
 * @param {any} dbValue
 * @returns {number} 0-1
 */
export function fieldSimilarity(field, ocrValue, dbValue) {
  if (ocrValue === null || ocrValue === undefined || ocrValue === '') {
    return dbValue === null || dbValue === undefined || dbValue === '' ? 1.0 : 0.0;
  }
  if (dbValue === null || dbValue === undefined || dbValue === '') return 0.0;
  if (ocrValue === dbValue) return 1.0;

  const strA = normalizeString(String(ocrValue));
  const strB = normalizeString(String(dbValue));
  if (strA === strB) return 1.0;

  switch (field.type) {
    case 'number':
      const numA = parseFloat(ocrValue);
      const numB = parseFloat(dbValue);
      if (isNaN(numA) || isNaN(numB)) return stringSimilarity(strA, strB);
      const max = Math.max(Math.abs(numA), Math.abs(numB));
      if (max === 0) return 1.0;
      return 1.0 - Math.min(1.0, Math.abs(numA - numB) / max);
    case 'date':
      return stringSimilarity(strA, strB);
    default:
      return stringSimilarity(strA, strB);
  }
}

/**
 * Get confidence color for a score
 * @param {number} score
 * @param {boolean} isDbOnly
 * @returns {object}
 */
export function getConfidenceColor(score, isDbOnly = false) {
  if (isDbOnly) return CONFIDENCE_COLORS.dbOnly;
  if (score >= MATCHING_THRESHOLDS.exactMatch) return CONFIDENCE_COLORS.high;
  if (score >= MATCHING_THRESHOLDS.vectorSemantic) return CONFIDENCE_COLORS.medium;
  return CONFIDENCE_COLORS.low;
}

/**
 * Build OCR field to schema line mapping
 * @param {object} ocrFields - { fieldName: value }
 * @param {string} domain
 * @returns {object[]} Array of { ocrField, schemaField, lineIndex, confidence }
 */
export function buildOcrSchemaMapping(ocrFields, domain) {
  const schema = getDomainSchema(domain);
  if (!schema) throw new Error(`Unknown domain: ${domain}`);

  const mapping = [];
  const ocrKeys = Object.keys(ocrFields);
  const usedSchemaFields = new Set();

  // First pass: exact and near-exact field name matches
  for (const ocrKey of ocrKeys) {
    const normalizedOcr = normalizeString(ocrKey);
    let bestMatch = null;
    let bestScore = 0;

    for (const sf of schema.fields) {
      if (usedSchemaFields.has(sf.name)) continue;
      const normalizedSf = normalizeString(sf.name);
      if (normalizedOcr === normalizedSf) {
        bestMatch = sf;
        bestScore = 1.0;
        break;
      }
      const sim = stringSimilarity(normalizedOcr, normalizedSf);
      if (sim > bestScore) {
        bestScore = sim;
        bestMatch = sf;
      }
    }

    if (bestMatch && bestScore > 0.5) {
      usedSchemaFields.add(bestMatch.name);
      const color = getConfidenceColor(bestScore);
      mapping.push({
        ocrField: ocrKey,
        schemaField: bestMatch.name,
        lineIndex: mapping.length,
        confidence: bestScore,
        color: color.color,
        colorLabel: color.label,
        matched: true,
      });
    } else {
      mapping.push({
        ocrField: ocrKey,
        schemaField: null,
        lineIndex: mapping.length,
        confidence: bestScore,
        color: CONFIDENCE_COLORS.low.color,
        colorLabel: 'red',
        matched: false,
        note: 'No schema mapping found',
      });
    }
  }

  return mapping;
}

/**
 * Exact match retrieval - direct field equality lookup
 * @param {object} entity - entity to match { fieldName: value }
 * @param {string} domain
 * @param {object[]} databaseRecords - existing records in the database
 * @returns {object[]} Array of { record, score, matchedFields }
 */
export function exactMatchRetrieval(entity, domain, databaseRecords) {
  const schema = getDomainSchema(domain);
  if (!schema) throw new Error(`Unknown domain: ${domain}`);

  const criticalFields = schema.fields.filter((f) => f.critical);
  const results = [];

  for (const record of databaseRecords) {
    let matchedCritical = 0;
    const matchedFields = [];

    for (const cf of criticalFields) {
      const entityVal = normalizeString(entity[cf.name] || '');
      const recordVal = normalizeString(record[cf.name] || '');
      if (entityVal && recordVal && entityVal === recordVal) {
        matchedCritical++;
        matchedFields.push(cf.name);
      }
    }

    // Exact match requires ALL critical fields to match
    if (matchedCritical === criticalFields.length) {
      const score = matchedCritical / criticalFields.length;
      results.push({ record, score, matchedFields, method: 'exact' });
    }
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score);
  return results;
}

/**
 * Vector semantic search - similarity-based matching
 * @param {object} entity - entity to match { fieldName: value }
 * @param {string} domain
 * @param {object[]} databaseRecords - existing records in the database
 * @param {number} threshold - minimum similarity threshold (default 0.70)
 * @returns {object[]} Array of { record, score, matchedFields }
 */
export function vectorSemanticSearch(entity, domain, databaseRecords, threshold = MATCHING_THRESHOLDS.vectorSemantic) {
  const schema = getDomainSchema(domain);
  if (!schema) throw new Error(`Unknown domain: ${domain}`);

  const results = [];

  for (const record of databaseRecords) {
    let weightedSum = 0;
    let totalWeight = 0;
    const matchedFields = [];

    for (const field of schema.fields) {
      const valA = entity[field.name];
      const valB = record[field.name];
      const sim = fieldSimilarity(field, valA, valB);
      if (sim > threshold) {
        matchedFields.push(field.name);
      }
      weightedSum += sim * field.weight;
      totalWeight += field.weight;
    }

    const score = totalWeight > 0 ? weightedSum / totalWeight : 0;
    if (score >= threshold) {
      results.push({ record, score, matchedFields, method: 'semantic' });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results;
}

/**
 * Dual-path entity retrieval - combines exact match and vector search
 * @param {object} entity - entity to match
 * @param {string} domain
 * @param {object[]} databaseRecords
 * @returns {object} { exactMatches, semanticMatches, bestMatch, overallConfidence, path }
 */
export function dualPathEntityRetrieval(entity, domain, databaseRecords) {
  const exactMatches = exactMatchRetrieval(entity, domain, databaseRecords);
  const semanticMatches = vectorSemanticSearch(entity, domain, databaseRecords);

  let bestMatch = null;
  let overallConfidence = 0;
  let path = null;

  if (exactMatches.length > 0) {
    bestMatch = exactMatches[0].record;
    overallConfidence = exactMatches[0].score;
    path = 'exact';
  } else if (semanticMatches.length > 0) {
    bestMatch = semanticMatches[0].record;
    overallConfidence = semanticMatches[0].score;
    path = 'semantic';
  }

  return {
    exactMatches,
    semanticMatches,
    bestMatch,
    overallConfidence,
    path,
    needsHumanReview: overallConfidence < MATCHING_THRESHOLDS.exactMatch || !bestMatch,
  };
}

/**
 * Verify field values between OCR data and database record
 * @param {object} ocrEntity - entity from OCR { fieldName: value }
 * @param {object} dbRecord - database record { fieldName: value }
 * @param {string} domain
 * @returns {object} { fields: { fieldName, ocrValue, dbValue, state, similarity } }
 */
export function verifyFieldValues(ocrEntity, dbRecord, domain) {
  const schema = getDomainSchema(domain);
  if (!schema) throw new Error(`Unknown domain: ${domain}`);

  const results = {};

  for (const field of schema.fields) {
    const ocrVal = ocrEntity[field.name];
    const dbVal = dbRecord[field.name];
    const sim = fieldSimilarity(field, ocrVal, dbVal);

    const ocrEmpty = ocrVal === null || ocrVal === undefined || ocrVal === '';
    const dbEmpty = dbVal === null || dbVal === undefined || dbVal === '';

    let state;
    if (ocrEmpty && dbEmpty) {
      state = VERIFICATION_STATES.MATCH; // both empty = consistent
    } else if (ocrEmpty) {
      state = VERIFICATION_STATES.DB_ONLY; // only in DB
    } else if (dbEmpty) {
      state = VERIFICATION_STATES.NEW_INFO; // new from OCR
    } else if (sim >= MATCHING_THRESHOLDS.exactMatch) {
      state = VERIFICATION_STATES.MATCH;
    } else {
      state = VERIFICATION_STATES.MISMATCH;
    }

    results[field.name] = {
      fieldName: field.name,
      ocrValue: ocrVal,
      dbValue: dbVal,
      state,
      similarity: sim,
      color: getStateColor(state),
    };
  }

  return results;
}

/**
 * Get color for verification state
 * @param {string} state
 * @returns {string} hex color
 */
export function getStateColor(state) {
  switch (state) {
    case VERIFICATION_STATES.MATCH: return '#22c55e';
    case VERIFICATION_STATES.MISMATCH: return '#ef4444';
    case VERIFICATION_STATES.NEW_INFO: return '#eab308';
    case VERIFICATION_STATES.DB_ONLY: return '#3b82f6';
    default: return '#6b7280';
  }
}

/**
 * Generate human-in-the-loop review request
 * @param {object} matchResult - result from dualPathEntityRetrieval
 * @param {object} verification - result from verifyFieldValues
 * @param {object} ocrEntity
 * @param {string} domain
 * @returns {object} review payload
 */
export function generateHitlReviewRequest(matchResult, verification, ocrEntity, domain) {
  const schema = getDomainSchema(domain);
  return {
    domain,
    timestamp: new Date().toISOString(),
    needsReview: matchResult.needsHumanReview,
    overallConfidence: matchResult.overallConfidence,
    matchPath: matchResult.path,
    ocrEntity,
    suggestedMatch: matchResult.bestMatch,
    fieldVerification: verification,
    schemaFields: schema.fields.map((f) => ({
      name: f.name,
      critical: f.critical,
      type: f.type,
    })),
    mismatchedFields: Object.values(verification)
      .filter((v) => v.state === VERIFICATION_STATES.MISMATCH)
      .map((v) => v.fieldName),
    newInfoFields: Object.values(verification)
      .filter((v) => v.state === VERIFICATION_STATES.NEW_INFO)
      .map((v) => v.fieldName),
    reviewActions: [
      { action: 'confirm_match', label: 'Confirm Match', enabled: !matchResult.needsHumanReview },
      { action: 'reject_match', label: 'Reject Match', enabled: true },
      { action: 'create_new', label: 'Create New Record', enabled: true },
      { action: 'update_fields', label: 'Update & Confirm', enabled: false },
    ],
  };
}

/**
 * Process human review decision
 * @param {object} decision - { action, correctedData?, selectedRecordId? }
 * @param {object} currentState - current match/verification state
 * @returns {object} { status, data, learningPayload }
 */
export function processHumanDecision(decision, currentState) {
  const { action, correctedData, selectedRecordId, notes } = decision;

  let status = 'pending';
  let data = null;
  let learningPayload = null;

  switch (action) {
    case 'confirm_match': {
      status = 'confirmed';
      data = {
        recordId: currentState.matchResult?.bestMatch?.id,
        action: 'match_confirmed',
        timestamp: new Date().toISOString(),
        notes,
      };
      learningPayload = {
        event: 'match_confirmed',
        domain: currentState.domain,
        ocrEntity: currentState.ocrEntity,
        matchedRecord: currentState.matchResult?.bestMatch,
        confidence: currentState.matchResult?.overallConfidence,
      };
      break;
    }
    case 'reject_match': {
      status = 'rejected';
      data = {
        action: 'match_rejected',
        timestamp: new Date().toISOString(),
        notes,
        reason: correctedData?.reason || 'human_rejected',
      };
      learningPayload = {
        event: 'match_rejected',
        domain: currentState.domain,
        ocrEntity: currentState.ocrEntity,
        rejectedRecord: currentState.matchResult?.bestMatch,
        reason: correctedData?.reason || 'human_rejected',
      };
      break;
    }
    case 'create_new': {
      status = 'new_record';
      data = {
        action: 'create_new_record',
        source: 'ocr',
        mergedData: { ...currentState.ocrEntity, ...(correctedData || {}) },
        timestamp: new Date().toISOString(),
        notes,
      };
      learningPayload = {
        event: 'new_record_created',
        domain: currentState.domain,
        ocrEntity: currentState.ocrEntity,
        correctedData,
      };
      break;
    }
    case 'update_fields': {
      status = 'updated';
      data = {
        recordId: selectedRecordId,
        action: 'fields_updated',
        updates: correctedData,
        timestamp: new Date().toISOString(),
        notes,
      };
      learningPayload = {
        event: 'fields_updated',
        domain: currentState.domain,
        recordId: selectedRecordId,
        ocrEntity: currentState.ocrEntity,
        correctedData,
      };
      break;
    }
    default:
      throw new Error(`Unknown action: ${action}`);
  }

  return { status, data, learningPayload };
}

/**
 * Active Learning - update thresholds or patterns based on corrections
 * @param {object[]} learningPayloads - array of payloads from human decisions
 * @param {object} currentStats - current learning stats
 * @returns {object} updated stats
 */
export function updateActiveLearning(learningPayloads, currentStats = {}) {
  const stats = { ...currentStats };
  stats.totalDecisions = (stats.totalDecisions || 0) + learningPayloads.length;
  stats.domainStats = stats.domainStats || {};
  stats.fieldErrorRates = stats.fieldErrorRates || {};

  for (const payload of learningPayloads) {
    const domain = payload.domain;
    stats.domainStats[domain] = stats.domainStats[domain] || { confirmed: 0, rejected: 0, newRecords: 0 };
    stats.domainStats[domain][payload.event.replace('match_', '').replace('record_', '')]++;

    // Track field-level errors
    if (payload.event === 'match_rejected' || payload.event === 'fields_updated') {
      const ocrEntity = payload.ocrEntity;
      const correctedData = payload.correctedData || {};
      const allFields = { ...ocrEntity, ...correctedData };
      for (const [field, value] of Object.entries(allFields)) {
        if (!stats.fieldErrorRates[field]) stats.fieldErrorRates[field] = { errors: 0, total: 0 };
        stats.fieldErrorRates[field].total++;
        if (payload.event === 'match_rejected') stats.fieldErrorRates[field].errors++;
      }
    }
  }

  // Compute adjusted thresholds based on error rates
  stats.adjustedThresholds = computeAdjustedThresholds(stats);

  return stats;
}

/**
 * Compute adjusted thresholds based on field error rates
 * @param {object} stats
 * @returns {object}
 */
export function computeAdjustedThresholds(stats) {
  const baseExact = MATCHING_THRESHOLDS.exactMatch;
  const baseSemantic = MATCHING_THRESHOLDS.vectorSemantic;

  // If a field has high error rate, increase its weight / threshold
  const adjusted = { exactMatch: baseExact, vectorSemantic: baseSemantic };

  if (stats.fieldErrorRates) {
    for (const [field, data] of Object.entries(stats.fieldErrorRates)) {
      if (data.total >= 5) {
        const errorRate = data.errors / data.total;
        if (errorRate > 0.3) {
          // Increase threshold slightly for problematic fields
          adjusted.exactMatch = Math.min(1.0, adjusted.exactMatch + 0.02);
          adjusted.vectorSemantic = Math.min(adjusted.exactMatch - 0.01, adjusted.vectorSemantic + 0.02);
        }
      }
    }
  }

  return adjusted;
}

/**
 * Main matching pipeline - orchestrates all steps
 * @param {object} ocrEntity - entity extracted from OCR
 * @param {string} domain
 * @param {object[]} databaseRecords
 * @param {object} options - { skipHitl: boolean }
 * @returns {object} pipeline result
 */
export function runMatchingPipeline(ocrEntity, domain, databaseRecords, options = {}) {
  const { skipHitl = false } = options;

  // Step 1: Build OCR to schema mapping
  const mapping = buildOcrSchemaMapping(ocrEntity, domain);

  // Step 2: Dual-path entity retrieval
  const matchResult = dualPathEntityRetrieval(ocrEntity, domain, databaseRecords);

  // Step 3: Field verification
  const verification = matchResult.bestMatch
    ? verifyFieldValues(ocrEntity, matchResult.bestMatch, domain)
    : null;

  // Step 4: Build result
  const result = {
    domain,
    timestamp: new Date().toISOString(),
    ocrEntity,
    schemaMapping: mapping,
    matchResult: {
      ...matchResult,
      confidenceColor: getConfidenceColor(matchResult.overallConfidence, !matchResult.bestMatch),
    },
    fieldVerification: verification,
    needsHumanReview: matchResult.needsHumanReview,
  };

  // Step 5: Generate HITL request if needed
  if (!skipHitl) {
    result.hitlRequest = verification
      ? generateHitlReviewRequest(matchResult, verification, ocrEntity, domain)
      : {
          domain,
          timestamp: new Date().toISOString(),
          needsReview: true,
          overallConfidence: 0,
          matchPath: null,
          ocrEntity,
          suggestedMatch: null,
          fieldVerification: null,
          reviewActions: [
            { action: 'create_new', label: 'Create New Record', enabled: true },
          ],
        };
  }

  return result;
}

/**
 * Format matching result as human-readable summary
 * @param {object} result - from runMatchingPipeline
 * @returns {string}
 */
export function formatMatchingSummary(result) {
  if (!result || !result.matchResult) {
    return 'No matching result available. Run matching pipeline first.';
  }
  const lines = [
    `=== Master Data Matching Result ===`,
    `Domain: ${result.domain || 'unknown'}`,
    `Time: ${result.timestamp || new Date().toISOString()}`,
    `Overall Confidence: ${result.matchResult.overallConfidence != null ? (result.matchResult.overallConfidence * 100).toFixed(1) + '%' : 'N/A'}`,
    `Match Path: ${result.matchResult.path || 'none'}`,
    `Color: ${result.matchResult.confidenceColor?.colorLabel || 'n/a'}`,
    `Needs Human Review: ${result.needsHumanReview ? 'YES ⚠️' : 'NO ✅'}`,
    '',
  ];

  if (result.matchResult.bestMatch) {
    lines.push(`Matched Record ID: ${result.matchResult.bestMatch.id || 'unknown'}`);
  }

  if (result.fieldVerification) {
    lines.push('', 'Field Verification:');
    for (const [field, v] of Object.entries(result.fieldVerification)) {
      lines.push(`  ${field}: [${v.state.toUpperCase()}] (${(v.similarity * 100).toFixed(0)}%)`);
    }
  }

  if (result.schemaMapping) {
    lines.push('', 'OCR Schema Mapping:');
    for (const m of result.schemaMapping) {
      lines.push(`  ${m.ocrField} → ${m.schemaField || 'UNMAPPED'} [${m.colorLabel}]`);
    }
  }

  return lines.join('\n');
}

// ─── Exports ─────────────────────────────────────────────────────────────────

export default {
  DOMAIN_SCHEMAS,
  CONFIDENCE_COLORS,
  VERIFICATION_STATES,
  MATCHING_THRESHOLDS,
  isValidDomain,
  getDomainSchema,
  getSupportedDomains,
  normalizeString,
  levenshteinDistance,
  stringSimilarity,
  fieldSimilarity,
  getConfidenceColor,
  buildOcrSchemaMapping,
  exactMatchRetrieval,
  vectorSemanticSearch,
  dualPathEntityRetrieval,
  verifyFieldValues,
  getStateColor,
  generateHitlReviewRequest,
  processHumanDecision,
  updateActiveLearning,
  computeAdjustedThresholds,
  runMatchingPipeline,
  formatMatchingSummary,
};
