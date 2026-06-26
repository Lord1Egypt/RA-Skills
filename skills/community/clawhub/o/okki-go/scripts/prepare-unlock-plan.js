#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const {
  batchIdFromPath,
  cleanString,
  countryCode,
  countryName,
  outputBudgetMetadata,
  applyDebugMetadata,
  selectedRows
} = require('./lib/compact-output');
const {
  readJsonFile
} = require('./lib/okki-api');
const {
  resolveBatchPath,
  resolveSelectionHandle,
  writeUnlockPlan
} = require('./lib/batch-state');

function usage() {
  console.error([
    'Usage:',
    '  node scripts/prepare-unlock-plan.js --selection-set-file target-set.json --compact [--locale en-US] [--debug-metadata]',
    '  node scripts/prepare-unlock-plan.js --selection-handle HANDLE --rows ROWS --compact [--locale en-US] [--debug-metadata]',
    '  node scripts/prepare-unlock-plan.js --batch batch.json --rows ROWS --compact [--locale en-US] [--debug-metadata]'
  ].join('\n'));
}

function parseArgs(argv) {
  const args = {
    selectionSetFile: null,
    selectionHandle: null,
    batch: null,
    rows: null,
    compact: false,
    now: null,
    locale: null,
    debugMetadata: false
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--selection-set-file') {
      args.selectionSetFile = argv[++i];
    } else if (arg === '--selection-handle') {
      args.selectionHandle = argv[++i];
    } else if (arg === '--batch') {
      args.batch = argv[++i];
    } else if (arg === '--rows') {
      args.rows = argv[++i];
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--now') {
      args.now = argv[++i];
    } else if (arg === '--locale') {
      args.locale = argv[++i];
    } else if (arg === '--debug-metadata') {
      args.debugMetadata = true;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if ((args.selectionSetFile ? 1 : 0) + (args.selectionHandle ? 1 : 0) + (args.batch ? 1 : 0) !== 1) {
    throw new Error('Provide exactly one of --selection-set-file, --selection-handle, or --batch.');
  }
  if (!args.selectionSetFile && !args.rows) throw new Error('Missing --rows');
  if (args.selectionSetFile && args.rows) throw new Error('--selection-set-file cannot be combined with --rows.');
  return args;
}

function resolveSource(args) {
  if (args.selectionHandle) {
    const resolved = resolveSelectionHandle(args.selectionHandle, { now: args.now });
    return {
      batchPath: resolved.batchPath,
      selectionHandle: args.selectionHandle,
      requestSummary: resolved.selection.request_summary || ''
    };
  }
  const resolved = resolveBatchPath(args.batch, { now: args.now });
  return {
    batchPath: resolved.batchPath,
    selectionHandle: null,
    requestSummary: ''
  };
}

function planRows(rows) {
  if (rows.length > 50) {
    throw new Error('Selected rows exceed compact unlock hard cap 50. Split the unlock into smaller confirmed batches.');
  }
  return rows.map((row) => {
    const code = countryCode(row);
    if (!row.domain) throw new Error(`Selected row ${row.row} is missing domain.`);
    if (!code) throw new Error(`Selected row ${row.row} is missing country_code.`);
    return {
      row: row.row,
      domain: row.domain,
      country_code: code,
      company_name: cleanString(row.company_name) || 'Unknown company',
      raw: row.raw && typeof row.raw === 'object' ? row.raw : undefined
    };
  });
}

function planRowsForSource(rows, source) {
  return planRows(rows).map((row) => ({
    ...row,
    target_sources: [{
      selection_handle: source.selectionHandle || null,
      batch_id: batchIdFromPath(source.batchPath),
      batch_path: source.batchPath,
      row: row.row,
      reason: source.reason || null
    }]
  }));
}

function mergeTargetRows(targetRows) {
  const byKey = new Map();
  for (const row of targetRows) {
    const key = `${cleanString(row.domain).toLowerCase()}|${cleanString(row.country_code).toUpperCase()}`;
    if (!byKey.has(key)) {
      byKey.set(key, row);
      continue;
    }
    const existing = byKey.get(key);
    existing.target_sources = [
      ...(Array.isArray(existing.target_sources) ? existing.target_sources : []),
      ...(Array.isArray(row.target_sources) ? row.target_sources : [])
    ];
  }
  return Array.from(byKey.values());
}

function targetSetFingerprint(rows) {
  const stableRows = rows.map((row) => ({
    domain: cleanString(row.domain).toLowerCase(),
    country_code: cleanString(row.country_code).toUpperCase(),
    row: row.row,
    company_name: row.company_name
  }));
  return crypto
    .createHash('sha256')
    .update(JSON.stringify(stableRows))
    .digest('hex')
    .slice(0, 16);
}

function readSelectionSet(filePath) {
  const data = readJsonFile(filePath);
  const selections = Array.isArray(data)
    ? data
    : Array.isArray(data && data.selections)
      ? data.selections
      : null;
  if (!selections || selections.length === 0) {
    throw new Error('Selection set must include selections[].');
  }
  return selections;
}

function resolveSelectionSet(args) {
  const selections = readSelectionSet(args.selectionSetFile);
  const targetRows = [];
  const sources = [];
  for (const [index, selection] of selections.entries()) {
    const selectionHandle = cleanString(selection.selection_handle || selection.selectionHandle);
    const rowsSelector = cleanString(selection.rows);
    if (!selectionHandle) throw new Error(`Selection set item ${index + 1} is missing selection_handle.`);
    if (!rowsSelector) throw new Error(`Selection set item ${index + 1} is missing rows.`);
    const resolved = resolveSelectionHandle(selectionHandle, { now: args.now });
    const batch = readJsonFile(resolved.batchPath);
    const rows = Array.isArray(batch.rows) ? batch.rows : [];
    const selected = selectedRows(rows, rowsSelector);
    const expectedRowNumbers = parseRowSelector(rowsSelector);
    if (selected.length !== expectedRowNumbers.length) {
      throw new Error(`One or more selected rows were not found for selection ${selectionHandle}.`);
    }
    const source = {
      selectionHandle,
      batchPath: resolved.batchPath,
      requestSummary: resolved.selection.request_summary || batch.request_summary || '',
      reason: cleanString(selection.reason) || null
    };
    sources.push({
      selection_handle: selectionHandle,
      batch_path: resolved.batchPath,
      batch_id: batchIdFromPath(resolved.batchPath),
      rows: rowsSelector,
      reason: source.reason
    });
    targetRows.push(...planRowsForSource(selected, source));
  }
  const rows = mergeTargetRows(targetRows);
  if (rows.length > 50) {
    throw new Error('Selected rows exceed compact unlock hard cap 50. Split the unlock into smaller confirmed batches.');
  }
  const fingerprint = targetSetFingerprint(rows);
  return {
    batchPath: null,
    selectionHandle: null,
    requestSummary: `target-set:${fingerprint}`,
    rows,
    targetSetFingerprint: fingerprint,
    source: {
      kind: 'target_set',
      target_set_fingerprint: fingerprint,
      selections: sources
    }
  };
}

function visibleRows(rows, locale) {
  return rows.map((row) => ({
    row: row.row,
    company_name: row.company_name,
    country_code: row.country_code,
    country_name: countryName(row.country_code, locale) || null
  }));
}

function parseRowSelector(selector) {
  const values = [];
  for (const part of String(selector || '').split(',')) {
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

function main() {
  const args = parseArgs(process.argv.slice(2));
  const source = args.selectionSetFile ? resolveSelectionSet(args) : resolveSource(args);
  let planInputRows;
  let batch = null;
  if (args.selectionSetFile) {
    planInputRows = source.rows;
  } else {
    batch = readJsonFile(source.batchPath);
    const rows = Array.isArray(batch.rows) ? batch.rows : [];
    const selected = selectedRows(rows, args.rows);
    const expectedRowNumbers = parseRowSelector(args.rows);
    if (selected.length !== expectedRowNumbers.length) {
      throw new Error('One or more selected rows were not found in the saved batch.');
    }
    planInputRows = planRows(selected);
  }
  const result = writeUnlockPlan({
    selectionHandle: source.selectionHandle,
    batchPath: source.batchPath,
    requestSummary: source.requestSummary || (batch && batch.request_summary) || '',
    rows: planInputRows,
    source: source.source,
    targetSetFingerprint: source.targetSetFingerprint,
    now: args.now
  });

  const output = {
    prepared: true,
    max_credit_cost: planInputRows.length,
    selected_companies: visibleRows(planInputRows, args.locale),
    paid_confirmation_required: true,
    confirmation_boundary: 'Ask the user to confirm the selected companies and maximum credit cost before unlocking.',
    unlock_plan_id: result.planId,
    batch_id: batchIdFromPath(source.batchPath),
    target_set_fingerprint: source.targetSetFingerprint,
    ...outputBudgetMetadata({
      defaultCap: 50,
      hardCap: 50,
      requestedLimit: planInputRows.length,
      returned: planInputRows.length,
      available: planInputRows.length
    })
  };

  process.stdout.write(`${JSON.stringify(planNormalOutput(output, args.debugMetadata), null, 2)}\n`);
}

function planNormalOutput(output, debugMetadata) {
  return applyDebugMetadata(output, [
    'unlock_plan_id',
    'batch_id',
    'target_set_fingerprint',
    'output_budget'
  ], debugMetadata);
}

try {
  main();
} catch (error) {
  console.error(error.message);
  usage();
  process.exit(2);
}
