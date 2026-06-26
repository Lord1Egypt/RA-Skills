#!/usr/bin/env node
/**
 * invoice-scan v1.7.1 — Full Test Suite
 * 
 * Tests all functionality:
 *   1. Schema (canonical.js)
 *   2. Validation — arithmetic (arithmetic.js)
 *   3. Validation — document rules (document-rules.js)
 *   4. Pre-export pipeline (prepare.js)
 *   5. Output — JSON (json.js)
 *   6. Output — CSV (csv.js)
 *   7. Output — Excel (excel.js)
 *   8. Output — formatOutput registry (output/index.js)
 *   9. Integration — agent-native mode (bare object → full pipeline)
 *  10. Integration — CLI mode (full canonical → no double-run)
 * 
 * Run: node test/run-tests.js
 */

const { createBlankInvoice, validateSchema, SCHEMA_VERSION } = require('../schema/canonical');
const { validateArithmetic, TOLERANCE } = require('../validation/arithmetic');
const { validateDocumentRules } = require('../validation/document-rules');
const { prepareForExport } = require('../output/prepare');
const { toJSON } = require('../output/json');
const { toCSV } = require('../output/csv');
const { toExcel } = require('../output/excel');
const { formatOutput, listFormats } = require('../output/index');

// ── Test Harness ──────────────────────────────────────────────

// --quiet flag: only show failures + summary
const QUIET = process.argv.includes('--quiet') || process.argv.includes('-q');

let totalTests = 0;
let passed = 0;
let failed = 0;
const failures = [];

function assert(condition, testName) {
  totalTests++;
  if (condition) {
    passed++;
    if (!QUIET) console.log(`  ✅ ${testName}`);
  } else {
    failed++;
    failures.push(testName);
    console.log(`  ❌ ${testName}`);
  }
}

function assertEq(actual, expected, testName) {
  assert(actual === expected, `${testName} (got: ${actual}, expected: ${expected})`);
}

function assertApprox(actual, expected, tolerance, testName) {
  assert(Math.abs(actual - expected) <= tolerance, `${testName} (got: ${actual}, expected: ~${expected})`);
}

function section(name) {
  if (!QUIET) console.log(`\n━━━ ${name} ━━━`);
}

// ── Helper: build test invoices ────────────────────────────────

function makeFullInvoice(overrides = {}) {
  const inv = createBlankInvoice();
  Object.assign(inv.header, {
    invoiceNumber: 'INV-001',
    invoiceDate: '2025-06-01',
    dueDate: '2025-07-01',
    currency: 'GBP',
    supplierName: 'Acme Ltd',
    supplierAddress: '123 Test Street',
    supplierVatNumber: 'GB123456789',
    buyerName: 'Buyer Corp',
    buyerAddress: '456 Client Road',
    buyerVatNumber: 'GB987654321',
    paymentTerms: 'Net 30',
    paymentReference: 'REF-001',
    bankDetails: { iban: 'GB12BANK12345612345678', bic: 'BANKGB2L', accountNumber: '12345678', sortCode: '12-34-56' },
  });
  inv.lineItems = [
    { description: 'Widget A', quantity: 10, unitOfMeasure: 'pcs', unitPrice: 5.00, lineTotal: 50.00, vatRate: 20, sku: 'WA-001', discount: null },
    { description: 'Widget B', quantity: 5, unitOfMeasure: 'pcs', unitPrice: 20.00, lineTotal: 100.00, vatRate: 20, sku: 'WB-002', discount: null },
  ];
  Object.assign(inv.totals, {
    netTotal: 150.00,
    vatBreakdown: [{ rate: 20, amount: 30.00 }],
    vatTotal: 30.00,
    grossTotal: 180.00,
    amountPaid: null,
    amountDue: 180.00,
  });
  Object.assign(inv.metadata, {
    confidence: 0.95,
    language: 'en',
    pageCount: 1,
    provider: 'anthropic',
    extractionTimestamp: '2025-06-01T12:00:00Z',
    documentType: 'invoice',
  });
  // Apply overrides
  for (const [key, val] of Object.entries(overrides)) {
    if (typeof val === 'object' && !Array.isArray(val) && val !== null && inv[key]) {
      Object.assign(inv[key], val);
    } else {
      inv[key] = val;
    }
  }
  return inv;
}

function makeAgentNativeInvoice() {
  // Simulates what an agent would produce — no metadata block, no validation run
  return {
    header: {
      invoiceNumber: 'AN-001',
      invoiceDate: '2025-03-15',
      dueDate: null,
      currency: 'USD',
      supplierName: 'Agent Supplier',
      supplierAddress: null,
      supplierVatNumber: null,
      buyerName: 'Agent Buyer',
      buyerAddress: null,
      buyerVatNumber: null,
      paymentTerms: null,
      paymentReference: null,
      bankDetails: {},
    },
    lineItems: [
      { description: 'Service', quantity: 1, unitOfMeasure: 'hr', unitPrice: 200, lineTotal: 200, vatRate: null, sku: null, discount: null },
    ],
    totals: { netTotal: 200, vatBreakdown: [], vatTotal: null, grossTotal: 200, amountPaid: -200, amountDue: 0 },
    documentType: 'invoice',
    language: 'en',
  };
}

// ══════════════════════════════════════════════════════════════
//  1. SCHEMA TESTS
// ══════════════════════════════════════════════════════════════

section('1. Schema — createBlankInvoice');

const blank = createBlankInvoice();
assert(blank.schemaVersion === SCHEMA_VERSION, 'schemaVersion set');
assert(blank.header !== undefined, 'header exists');
assert(blank.header.invoiceNumber === null, 'header fields default to null');
assert(Array.isArray(blank.lineItems), 'lineItems is array');
assert(blank.lineItems.length === 0, 'lineItems empty');
assert(blank.totals.netTotal === null, 'totals.netTotal defaults to null');
assert(blank.totals.amountPaid === null, 'totals.amountPaid exists (v1.5.0+)');
assert(blank.totals.amountDue === null, 'totals.amountDue exists (v1.5.0+)');
assert(Array.isArray(blank.totals.vatBreakdown), 'vatBreakdown is array');
assert(blank.metadata.documentType === null, 'metadata.documentType exists');
assert(blank.metadata.provider === null, 'metadata.provider exists');
assert(blank.metadata.language === null, 'metadata.language exists');
assert(blank.metadata.extractionTimestamp === null, 'metadata.extractionTimestamp exists');
assert(Array.isArray(blank.stamps), 'stamps[] exists (v1.6.0+)');
assert(blank.stamps.length === 0, 'stamps defaults empty');
assert(blank.remarks === null, 'remarks exists (v1.6.0+)');
assert(Array.isArray(blank.fields), 'fields[] exists');
assert(blank.validation.arithmeticValid === null, 'validation.arithmeticValid starts null');
assert(Array.isArray(blank.validation.errors), 'validation.errors is array');
assert(Array.isArray(blank.validation.warnings), 'validation.warnings is array');

section('1b. Schema — validateSchema');

const valid = makeFullInvoice();
const schemaResult = validateSchema(valid);
assert(schemaResult.valid === true, 'Full invoice passes schema validation');
assertEq(schemaResult.errors.length, 0, 'No schema errors');

const broken = { header: { invoiceNumber: 'X' }, lineItems: 'not-array' };
const brokenResult = validateSchema(broken);
assert(brokenResult.valid === false, 'Broken invoice fails schema validation');
assert(brokenResult.errors.length > 0, 'Schema errors reported');

// ══════════════════════════════════════════════════════════════
//  2. ARITHMETIC VALIDATION
// ══════════════════════════════════════════════════════════════

section('2. Arithmetic Validation');

// 2a. Perfect invoice — no errors
const arith1 = makeFullInvoice();
validateArithmetic(arith1);
assert(arith1.validation.arithmeticValid === true, 'Perfect invoice: arithmetic valid');
assertEq(arith1.validation.errors.length, 0, 'Perfect invoice: no errors');

// 2b. Line items don't sum to net
const arith2 = makeFullInvoice({ totals: { netTotal: 999 } });
validateArithmetic(arith2);
assert(arith2.validation.arithmeticValid === false, 'Wrong net total: arithmetic invalid');
assert(arith2.validation.errors.some(e => e.field === 'totals.netTotal'), 'Wrong net total: error on netTotal');

// 2c. qty × price ≠ lineTotal
const arith3 = makeFullInvoice();
arith3.lineItems[0].lineTotal = 999;
validateArithmetic(arith3);
assert(arith3.validation.errors.some(e => e.field.includes('lineItems[0]')), 'Bad line total: error on lineItem');

// 2d. VAT breakdown doesn't match vatTotal
const arith4 = makeFullInvoice({ totals: { vatTotal: 99.99 } });
validateArithmetic(arith4);
assert(arith4.validation.errors.some(e => e.field === 'totals.vatTotal'), 'VAT mismatch: error on vatTotal');

// 2e. Net + VAT ≠ Gross
const arith5 = makeFullInvoice({ totals: { grossTotal: 999 } });
validateArithmetic(arith5);
assert(arith5.validation.errors.some(e => e.field === 'totals.grossTotal'), 'Gross mismatch: error on grossTotal');

// 2f. Gross < net (warning)
const arith6 = makeFullInvoice({ totals: { grossTotal: 100, vatTotal: 0, vatBreakdown: [] } });
arith6.totals.netTotal = 150;
validateArithmetic(arith6);
assert(arith6.validation.warnings.some(w => w.message.includes('less than net')), 'Gross < net: warning generated');

// 2g. amountDue = gross - amountPaid (v1.6.0+) — wrong amountDue
const arith7 = makeFullInvoice({ totals: { amountPaid: -100, amountDue: 50, grossTotal: 180 } });
// Expected: 180 - 100 = 80, but amountDue says 50 → should warn
validateArithmetic(arith7);
assert(arith7.validation.arithmeticValid === true, 'amountDue check: arithmetic still valid (warning not error)');
assert(arith7.validation.warnings.some(w => w.field === 'totals.amountDue'), 'amountDue mismatch: warning generated');

// 2h. amountDue correct — no warning
const arith8 = makeFullInvoice({ totals: { amountPaid: -80, amountDue: 100, grossTotal: 180 } });
validateArithmetic(arith8);
assert(!arith8.validation.warnings.some(w => w.field === 'totals.amountDue'), 'amountDue correct: no warning');

// 2i. Overpayment warning (v1.6.0+)
const arith9 = makeFullInvoice({ totals: { amountPaid: -500, grossTotal: 180 } });
validateArithmetic(arith9);
assert(arith9.validation.warnings.some(w => w.field === 'totals.amountPaid' && w.message.includes('overpayment')), 'Overpayment: warning generated');

// 2j. Tolerance — within ±0.02 should pass
const arith10 = makeFullInvoice();
arith10.totals.netTotal = 150.01; // 0.01 off — within tolerance
validateArithmetic(arith10);
assert(arith10.validation.arithmeticValid === true, 'Within tolerance (0.01): passes');

// 2k. Tolerance — beyond ±0.02 but ≤1.00 should warn (not error)
const arith11 = makeFullInvoice();
arith11.totals.netTotal = 150.05; // 0.05 off — outside tolerance but within rounding threshold
validateArithmetic(arith11);
assert(arith11.validation.arithmeticValid === true, 'Beyond tolerance (0.05) but ≤1.00: warning not error');
assert(arith11.validation.warnings.some(w => w.message.includes('rounding')), 'Beyond tolerance (0.05): has rounding warning');

// 2k2. Beyond rounding threshold (>1.00) should error
const arith11b = makeFullInvoice();
arith11b.totals.netTotal = 152.00; // 2.00 off — beyond rounding threshold
validateArithmetic(arith11b);
assert(arith11b.validation.arithmeticValid === false, 'Beyond rounding threshold (2.00): fails');

// ══════════════════════════════════════════════════════════════
//  3. DOCUMENT RULES VALIDATION
// ══════════════════════════════════════════════════════════════

section('3. Document Rules Validation');

// 3a. Perfect invoice — minimal warnings
const doc1 = makeFullInvoice();
validateDocumentRules(doc1);
assert(doc1.validation.documentQuality !== undefined, 'Document quality computed');
assert(doc1.validation.documentQuality.rating === 'good', 'Full invoice: quality rating "good"');
assertEq(doc1.validation.documentQuality.score, 1, 'Full invoice: quality score 1.0');

// 3b. Missing invoice number
const doc2 = makeFullInvoice({ header: { invoiceNumber: null } });
validateDocumentRules(doc2);
assert(doc2.validation.warnings.some(w => w.field === 'header.invoiceNumber'), 'Missing invoice number: warning');

// 3c. Missing supplier
const doc3 = makeFullInvoice({ header: { supplierName: null } });
validateDocumentRules(doc3);
assert(doc3.validation.warnings.some(w => w.field === 'header.supplierName'), 'Missing supplier: warning');

// 3d. Missing buyer
const doc4 = makeFullInvoice({ header: { buyerName: null } });
validateDocumentRules(doc4);
assert(doc4.validation.warnings.some(w => w.field === 'header.buyerName'), 'Missing buyer: warning');

// 3e. No VAT info
const doc5 = makeFullInvoice({ totals: { vatTotal: null, vatBreakdown: [] } });
validateDocumentRules(doc5);
assert(doc5.validation.warnings.some(w => w.field === 'totals.vatTotal'), 'No VAT info: warning');

// 3f. No line items
const doc6 = makeFullInvoice();
doc6.lineItems = [];
validateDocumentRules(doc6);
assert(doc6.validation.warnings.some(w => w.field === 'lineItems'), 'No line items: warning');

// 3g. Very small amount
const doc7 = makeFullInvoice({ totals: { grossTotal: 5 } });
validateDocumentRules(doc7);
assert(doc7.validation.warnings.some(w => w.message.includes('Very small')), 'Small amount: warning');

// 3h. Invoice with no due date
const doc8 = makeFullInvoice({ header: { dueDate: null } });
doc8.metadata.documentType = 'invoice';
validateDocumentRules(doc8);
assert(doc8.validation.warnings.some(w => w.field === 'header.dueDate'), 'Invoice no due date: warning');

// 3i. debit-note with no due date (v1.7.1 fix)
const doc9 = makeFullInvoice({ header: { dueDate: null } });
doc9.metadata.documentType = 'debit-note';
validateDocumentRules(doc9);
assert(doc9.validation.warnings.some(w => w.field === 'header.dueDate'), 'Debit-note no due date: warning');

// 3j. debit-note NOT flagged as "not standard" (v1.7.1 fix)
const doc10 = makeFullInvoice();
doc10.metadata.documentType = 'debit-note';
validateDocumentRules(doc10);
assert(!doc10.validation.warnings.some(w => w.field === 'metadata.documentType'), 'Debit-note: NOT flagged as non-standard');

// 3k. receipt IS flagged as non-standard
const doc11 = makeFullInvoice();
doc11.metadata.documentType = 'receipt';
validateDocumentRules(doc11);
assert(doc11.validation.warnings.some(w => w.field === 'metadata.documentType' && w.message.includes('receipt')), 'Receipt: flagged as non-standard');

// 3l. credit-note NOT flagged as non-standard
const doc12 = makeFullInvoice();
doc12.metadata.documentType = 'credit-note';
validateDocumentRules(doc12);
assert(!doc12.validation.warnings.some(w => w.field === 'metadata.documentType'), 'Credit-note: NOT flagged as non-standard');

// 3m. Short invoice number
const doc13 = makeFullInvoice({ header: { invoiceNumber: 'A' } });
validateDocumentRules(doc13);
assert(doc13.validation.warnings.some(w => w.message.includes('suspiciously short')), 'Short invoice number: warning');

// 3n. POS-style invoice number
const doc14 = makeFullInvoice({ header: { invoiceNumber: 'TXN-12345' } });
validateDocumentRules(doc14);
assert(doc14.validation.warnings.some(w => w.message.includes('POS/terminal')), 'POS-style number: warning');

// 3o. No payment info warning
const doc15 = makeFullInvoice({ header: { paymentTerms: null, dueDate: null, bankDetails: {} } });
doc15.metadata.documentType = 'invoice';
validateDocumentRules(doc15);
assert(doc15.validation.warnings.some(w => w.field === 'header.paymentInfo'), 'No payment info: warning');

// 3p. Document quality — partial
const doc16 = makeFullInvoice({ header: { invoiceNumber: null, supplierVatNumber: null, buyerName: null } });
doc16.totals.vatTotal = null;
validateDocumentRules(doc16);
assert(doc16.validation.documentQuality.rating === 'partial', 'Missing fields: quality "partial"');

// ══════════════════════════════════════════════════════════════
//  4. PRE-EXPORT PIPELINE (prepare.js)
// ══════════════════════════════════════════════════════════════

section('4. Pre-export Pipeline');

// 4a. Agent-native object gets metadata filled
const prep1 = makeAgentNativeInvoice();
prepareForExport(prep1);
assertEq(prep1.metadata.provider, 'agent-native', 'Provider defaults to "agent-native"');
assert(prep1.metadata.extractionTimestamp !== null, 'Extraction timestamp auto-set');
assertEq(prep1.metadata.language, 'en', 'Language copied from top-level');
assertEq(prep1.metadata.documentType, 'invoice', 'documentType copied from top-level');

// 4b. Bidirectional sync — metadata → top-level
const prep2 = createBlankInvoice();
prep2.metadata.documentType = 'credit-note';
prep2.metadata.language = 'de';
prepareForExport(prep2);
assertEq(prep2.documentType, 'credit-note', 'metadata.documentType → top-level');
assertEq(prep2.language, 'de', 'metadata.language → top-level');

// 4c. Auto-run validators
const prep3 = makeAgentNativeInvoice();
assert(prep3.validation === undefined, 'Agent-native: no validation block before prepare');
prepareForExport(prep3);
assert(prep3.validation.arithmeticValid !== null, 'Arithmetic validator auto-ran');
assert(prep3.validation.documentQuality !== undefined, 'Document rules auto-ran');

// 4d. Doesn't double-run validators
const prep4 = makeFullInvoice();
validateArithmetic(prep4);
validateDocumentRules(prep4);
const warningsBefore = prep4.validation.warnings.length;
prepareForExport(prep4);
const warningsAfter = prep4.validation.warnings.length;
assertEq(warningsAfter, warningsBefore, 'Pre-validated: no double-run');

// 4e. Structural completeness — bare minimum object
const prep5 = { header: { invoiceNumber: 'BARE' } };
prepareForExport(prep5);
assert(Array.isArray(prep5.stamps), 'Bare object: stamps[] created');
assert(Array.isArray(prep5.lineItems), 'Bare object: lineItems[] created');
assert(prep5.metadata !== undefined, 'Bare object: metadata created');
assert(prep5.validation !== undefined, 'Bare object: validation created');
assert(Array.isArray(prep5.validation.errors), 'Bare object: validation.errors created');
assert(Array.isArray(prep5.validation.warnings), 'Bare object: validation.warnings created');

// 4f. Doesn't overwrite existing metadata
const prep6 = makeFullInvoice();
prep6.metadata.provider = 'anthropic';
prep6.metadata.extractionTimestamp = '2020-01-01T00:00:00Z';
prepareForExport(prep6);
assertEq(prep6.metadata.provider, 'anthropic', 'Existing provider preserved');
assertEq(prep6.metadata.extractionTimestamp, '2020-01-01T00:00:00Z', 'Existing timestamp preserved');

// ══════════════════════════════════════════════════════════════
//  5. JSON OUTPUT
// ══════════════════════════════════════════════════════════════

section('5. JSON Output');

const json1 = makeFullInvoice();
const jsonStr = toJSON(json1, true);
assert(typeof jsonStr === 'string', 'toJSON returns string');
const jsonParsed = JSON.parse(jsonStr);
assertEq(jsonParsed.header.invoiceNumber, 'INV-001', 'JSON contains invoice data');

const jsonCompact = toJSON(json1, false);
assert(!jsonCompact.includes('\n'), 'Compact JSON has no newlines');

// ══════════════════════════════════════════════════════════════
//  6. CSV OUTPUT
// ══════════════════════════════════════════════════════════════

section('6. CSV Output');

const csv1 = makeFullInvoice();
prepareForExport(csv1);
const csvStr = toCSV(csv1);
const csvLines = csvStr.split('\n');
assertEq(csvLines.length, 3, 'CSV: header + 2 line items = 3 lines');
assert(csvLines[0].includes('invoiceNumber'), 'CSV: header row has invoiceNumber');
assert(csvLines[1].includes('INV-001'), 'CSV: data row has invoice number');
assert(csvLines[1].includes('Widget A'), 'CSV: first line item present');
assert(csvLines[2].includes('Widget B'), 'CSV: second line item present');

// CSV with documentType
assert(csvLines[0].includes('documentType'), 'CSV: header has documentType column');
assert(csvLines[1].includes('invoice'), 'CSV: data has documentType value');

// CSV with no line items
const csv2 = makeFullInvoice();
csv2.lineItems = [];
prepareForExport(csv2);
const csvEmpty = toCSV(csv2);
assertEq(csvEmpty.split('\n').length, 2, 'CSV: no line items = header + 1 row');

// CSV escaping
const csv3 = makeFullInvoice();
csv3.header.supplierName = 'Acme, "The Best" Ltd';
prepareForExport(csv3);
const csvEscaped = toCSV(csv3);
assert(csvEscaped.includes('"Acme, ""The Best"" Ltd"'), 'CSV: special chars escaped');

// ══════════════════════════════════════════════════════════════
//  7. EXCEL OUTPUT
// ══════════════════════════════════════════════════════════════

section('7. Excel Output');

const xl1 = makeFullInvoice();
prepareForExport(xl1);
validateArithmetic(xl1);
validateDocumentRules(xl1);
const xlBuf = toExcel(xl1);
assert(Buffer.isBuffer(xlBuf), 'toExcel returns Buffer');
assert(xlBuf.length > 1000, 'Excel buffer has content');

// Verify Excel contents by reading back
const XLSX = require('xlsx');
const wb = XLSX.read(xlBuf, { type: 'buffer' });
assert(wb.SheetNames.includes('Header'), 'Excel: Header sheet exists');
assert(wb.SheetNames.includes('Line Items'), 'Excel: Line Items sheet exists');
assert(wb.SheetNames.includes('Validation'), 'Excel: Validation sheet exists');

// Check Header sheet values
const headerSheet = XLSX.utils.sheet_to_json(wb.Sheets['Header'], { header: 1 });
const headerMap = {};
headerSheet.forEach(row => { if (row[0]) headerMap[row[0]] = row[1]; });
assertEq(headerMap['Invoice Number'], 'INV-001', 'Excel Header: invoice number');
assertEq(headerMap['Currency'], 'GBP', 'Excel Header: currency');
assertEq(headerMap['Document Type'], 'invoice', 'Excel Header: documentType populated');
assertEq(headerMap['Language'], 'en', 'Excel Header: language populated');
assertEq(headerMap['Provider'], 'anthropic', 'Excel Header: provider populated');
assert(headerMap['Extracted At'] !== undefined && headerMap['Extracted At'] !== null, 'Excel Header: extractedAt populated');
assertEq(headerMap['Net Total'], 150, 'Excel Header: net total');
assertEq(headerMap['Gross Total'], 180, 'Excel Header: gross total');

// Check Line Items sheet
const lineSheet = XLSX.utils.sheet_to_json(wb.Sheets['Line Items']);
assertEq(lineSheet.length, 2, 'Excel Line Items: 2 rows');
assertEq(lineSheet[0]['Description'], 'Widget A', 'Excel Line Items: first item');
assertEq(lineSheet[1]['Description'], 'Widget B', 'Excel Line Items: second item');

// Check Validation sheet
const valSheet = XLSX.utils.sheet_to_json(wb.Sheets['Validation'], { header: 1 });
const valText = JSON.stringify(valSheet);
assert(valText.includes('YES'), 'Excel Validation: arithmetic valid = YES');

// Agent-native Excel — documentType should flow through (v1.7.0 fix)
const xl2 = makeAgentNativeInvoice();
xl2.documentType = 'debit-note';
const xl2Buf = formatOutput(xl2, 'excel');
const wb2 = XLSX.read(xl2Buf, { type: 'buffer' });
const headerSheet2 = XLSX.utils.sheet_to_json(wb2.Sheets['Header'], { header: 1 });
const headerMap2 = {};
headerSheet2.forEach(row => { if (row[0]) headerMap2[row[0]] = row[1]; });
assertEq(headerMap2['Document Type'], 'debit-note', 'Agent-native Excel: documentType flows through');
assertEq(headerMap2['Provider'], 'agent-native', 'Agent-native Excel: provider defaults');
assert(headerMap2['Extracted At'] !== undefined, 'Agent-native Excel: timestamp auto-filled');

// ══════════════════════════════════════════════════════════════
//  8. FORMAT REGISTRY
// ══════════════════════════════════════════════════════════════

section('8. Format Registry');

const formats = listFormats();
assert(formats.includes('json'), 'listFormats includes json');
assert(formats.includes('csv'), 'listFormats includes csv');
assert(formats.includes('excel'), 'listFormats includes excel');

// formatOutput with each format
const reg1 = makeFullInvoice();
const regJson = formatOutput(reg1, 'json');
assert(typeof regJson === 'string', 'formatOutput json: returns string');
assert(JSON.parse(regJson).header.invoiceNumber === 'INV-001', 'formatOutput json: valid JSON');

const reg2 = makeFullInvoice();
const regCsv = formatOutput(reg2, 'csv');
assert(typeof regCsv === 'string', 'formatOutput csv: returns string');
assert(regCsv.includes('INV-001'), 'formatOutput csv: contains data');

const reg3 = makeFullInvoice();
const regXlsx = formatOutput(reg3, 'xlsx');
assert(Buffer.isBuffer(regXlsx), 'formatOutput xlsx: returns Buffer');

// Unknown format throws
let threw = false;
try { formatOutput(makeFullInvoice(), 'parquet'); } catch (e) { threw = true; }
assert(threw, 'Unknown format throws error');

// ══════════════════════════════════════════════════════════════
//  9. INTEGRATION — AGENT-NATIVE MODE
// ══════════════════════════════════════════════════════════════

section('9. Integration — Agent-native Mode');

// Full flow: bare object → formatOutput → complete Excel
const int1 = {
  header: {
    invoiceNumber: 'INT-001', invoiceDate: '2025-01-01', dueDate: null,
    currency: 'EUR', supplierName: 'Euro Corp', supplierAddress: null,
    supplierVatNumber: 'DE123456789', buyerName: 'Käufer GmbH',
    buyerAddress: null, buyerVatNumber: null, paymentTerms: null,
    paymentReference: null, bankDetails: {},
  },
  lineItems: [
    { description: 'Beratung', quantity: 8, unitOfMeasure: 'hrs', unitPrice: 150, lineTotal: 1200, vatRate: 19, sku: null, discount: null },
  ],
  totals: { netTotal: 1200, vatBreakdown: [{ rate: 19, amount: 228 }], vatTotal: 228, grossTotal: 1428, amountPaid: null, amountDue: 1428 },
  documentType: 'invoice',
  language: 'de',
  stamps: [{ type: 'company', text: 'Euro Corp GmbH' }],
  remarks: 'Payment within 14 days',
};

const int1Json = JSON.parse(formatOutput(int1, 'json'));
assertEq(int1Json.metadata.documentType, 'invoice', 'Agent-native integration: documentType in JSON');
assertEq(int1Json.metadata.provider, 'agent-native', 'Agent-native integration: provider in JSON');
assertEq(int1Json.metadata.language, 'de', 'Agent-native integration: language in JSON');
assert(int1Json.validation.arithmeticValid === true, 'Agent-native integration: arithmetic validated');
assert(int1Json.validation.documentQuality !== undefined, 'Agent-native integration: doc quality computed');
assertEq(int1Json.stamps.length, 1, 'Agent-native integration: stamps preserved');
assertEq(int1Json.remarks, 'Payment within 14 days', 'Agent-native integration: remarks preserved');

// ══════════════════════════════════════════════════════════════
//  10. INTEGRATION — CLI MODE (no double-run)
// ══════════════════════════════════════════════════════════════

section('10. Integration — CLI Mode (no double-run)');

const int2 = makeFullInvoice();
validateArithmetic(int2);
validateDocumentRules(int2);
const warnCount = int2.validation.warnings.length;
const errCount = int2.validation.errors.length;

// formatOutput should not re-run validators
const int2Json = JSON.parse(formatOutput(int2, 'json'));
assertEq(int2Json.validation.warnings.length, warnCount, 'CLI mode: warnings unchanged after formatOutput');
assertEq(int2Json.validation.errors.length, errCount, 'CLI mode: errors unchanged after formatOutput');

// ══════════════════════════════════════════════════════════════
//  11. EDGE CASES
// ══════════════════════════════════════════════════════════════

section('11. Edge Cases');

// 11a. All 10 document types
const docTypes = ['invoice', 'credit-note', 'debit-note', 'receipt', 'purchase-order', 'delivery-note', 'confirmation', 'statement', 'other-financial', 'not-financial'];
for (const dt of docTypes) {
  const edge = makeFullInvoice();
  edge.metadata.documentType = dt;
  const result = formatOutput(edge, 'json');
  const parsed = JSON.parse(result);
  assertEq(parsed.metadata.documentType, dt, `Document type "${dt}" survives pipeline`);
}

// 11b. Stamps with different types
const edge2 = makeFullInvoice();
edge2.stamps = [
  { type: 'company', text: 'ACME' },
  { type: 'paid', text: 'PAID IN FULL' },
  { type: 'approved', text: 'APPROVED' },
  { type: 'date', text: '2025-06-01' },
  { type: 'tax', text: 'GST EXEMPT' },
  { type: 'other', text: 'Original for Buyer' },
];
const edge2Json = JSON.parse(formatOutput(edge2, 'json'));
assertEq(edge2Json.stamps.length, 6, 'All 6 stamp types preserved');

// 11c. Referenced documents
const edge3 = makeFullInvoice();
edge3.referencedDocuments = [
  { type: 'PO', reference: 'PO-12345' },
  { type: 'contract', reference: 'C-2025-001' },
];
const edge3Buf = formatOutput(edge3, 'excel');
const wb3 = XLSX.read(edge3Buf, { type: 'buffer' });
const hdr3 = XLSX.utils.sheet_to_json(wb3.Sheets['Header'], { header: 1 });
const hdr3Text = JSON.stringify(hdr3);
assert(hdr3Text.includes('PO-12345'), 'Excel: referenced documents in Header sheet');
assert(hdr3Text.includes('Purchase Order'), 'Excel: PO renders as "Purchase Order"');

// 11c-ii. Invoice/credit-note/debit-note references (credit memo support)
const edge3b = makeFullInvoice();
edge3b.referencedDocuments = [
  { type: 'invoice', reference: 'INV-2025-001' },
  { type: 'credit-note', reference: 'CN-100' },
  { type: 'debit-note', reference: 'DN-200' },
];
const edge3bBuf = formatOutput(edge3b, 'excel');
const wb3b = XLSX.read(edge3bBuf, { type: 'buffer' });
const hdr3b = XLSX.utils.sheet_to_json(wb3b.Sheets['Header'], { header: 1 });
const hdr3bText = JSON.stringify(hdr3b);
assert(hdr3bText.includes('Original Invoice'), 'Excel: invoice ref renders as "Original Invoice"');
assert(hdr3bText.includes('INV-2025-001'), 'Excel: invoice reference value present');
assert(hdr3bText.includes('CN-100'), 'Excel: credit-note reference present');
assert(hdr3bText.includes('DN-200'), 'Excel: debit-note reference present');

// CSV: originalInvoiceRef column
const edge3bCsv = formatOutput(edge3b, 'csv');
assert(edge3bCsv.includes('INV-2025-001'), 'CSV: originalInvoiceRef populated');
assert(edge3bCsv.includes('credit-note: CN-100'), 'CSV: referencedDocuments detail includes credit-note');

// 11d. Multi-rate VAT
const edge4 = makeFullInvoice();
edge4.totals.vatBreakdown = [{ rate: 20, amount: 20 }, { rate: 5, amount: 5 }];
edge4.totals.vatTotal = 25;
validateArithmetic(edge4);
assert(!edge4.validation.errors.some(e => e.field === 'totals.vatTotal'), 'Multi-rate VAT: breakdown sum matches total');

// 11e. Charges (shipping, handling, etc.) — v1.8.0
section('12. Charges');

// 12a. Schema includes charges[]
const ch1 = createBlankInvoice();
assert(Array.isArray(ch1.charges), 'Schema: charges[] exists');
assertEq(ch1.charges.length, 0, 'Schema: charges defaults empty');

// 12b. Charges survive pipeline
const ch2 = makeFullInvoice();
ch2.charges = [
  { type: 'shipping', label: 'Postage & Packing', amount: 5.99, vatRate: 20, vatAmount: 1.20 },
  { type: 'handling', label: 'Handling Fee', amount: 2.00, vatRate: 0, vatAmount: 0 },
];
const ch2Json = JSON.parse(formatOutput(ch2, 'json'));
assertEq(ch2Json.charges.length, 2, 'Charges: 2 charges preserved in JSON');
assertEq(ch2Json.charges[0].type, 'shipping', 'Charges: first type correct');
assertEq(ch2Json.charges[0].label, 'Postage & Packing', 'Charges: original label preserved');
assertEq(ch2Json.charges[0].amount, 5.99, 'Charges: amount correct');
assertEq(ch2Json.charges[0].vatRate, 20, 'Charges: vatRate correct');
assertEq(ch2Json.charges[0].vatAmount, 1.20, 'Charges: vatAmount correct (got: 1.2, expected: 1.2)');
assertEq(ch2Json.charges[1].type, 'handling', 'Charges: second type correct');

// 12c. Charges in Excel
const ch3 = makeFullInvoice();
ch3.charges = [
  { type: 'shipping', label: 'Freight', amount: 25.00, vatRate: null, vatAmount: null },
];
const ch3Buf = formatOutput(ch3, 'excel');
const wb4 = XLSX.read(ch3Buf, { type: 'buffer' });
const hdr4 = XLSX.utils.sheet_to_json(wb4.Sheets['Header'], { header: 1 });
const hdr4Text = JSON.stringify(hdr4);
assert(hdr4Text.includes('Freight'), 'Excel: charges label appears in Header sheet');
assert(hdr4Text.includes('25'), 'Excel: charges amount appears in Header sheet');

// 12d. Charges in CSV
const ch4 = makeFullInvoice();
ch4.charges = [
  { type: 'shipping', label: 'P&P', amount: 3.50, vatRate: 20, vatAmount: 0.70 },
  { type: 'insurance', label: 'Insurance', amount: 1.50, vatRate: 0, vatAmount: 0 },
];
const ch4Csv = formatOutput(ch4, 'csv');
const ch4Headers = ch4Csv.split('\n')[0];
assert(ch4Headers.includes('chargesTotal'), 'CSV: chargesTotal column exists');
assert(ch4Headers.includes('chargesDetail'), 'CSV: chargesDetail column exists');
const ch4Row = ch4Csv.split('\n')[1];
assert(ch4Row.includes('5'), 'CSV: chargesTotal sum present'); // 3.50 + 1.50 = 5
assert(ch4Row.includes('P&P'), 'CSV: charges detail includes label');

// 12e. Empty charges — no crash
const ch5 = makeFullInvoice();
ch5.charges = [];
const ch5Json = JSON.parse(formatOutput(ch5, 'json'));
assertEq(ch5Json.charges.length, 0, 'Empty charges: no crash');

// 12f. Bare object without charges — auto-created
const ch6 = { header: { invoiceNumber: 'BARE-CH' } };
prepareForExport(ch6);
assert(Array.isArray(ch6.charges), 'Bare object: charges[] auto-created');

// 12g. All charge types
const chargeTypes = ['shipping', 'handling', 'insurance', 'surcharge', 'discount', 'other'];
for (const ct of chargeTypes) {
  const chx = makeFullInvoice();
  chx.charges = [{ type: ct, label: `Test ${ct}`, amount: 10, vatRate: null, vatAmount: null }];
  const chxJson = JSON.parse(formatOutput(chx, 'json'));
  assertEq(chxJson.charges[0].type, ct, `Charge type "${ct}" survives pipeline`);
}

// 12h. Agent-native with charges
const ch8 = makeAgentNativeInvoice();
ch8.charges = [{ type: 'shipping', label: 'Delivery', amount: 7.99, vatRate: 20, vatAmount: 1.60 }];
const ch8Json = JSON.parse(formatOutput(ch8, 'json'));
assertEq(ch8Json.charges.length, 1, 'Agent-native: charges preserved');
assertEq(ch8Json.charges[0].label, 'Delivery', 'Agent-native: charge label correct');

// 11e. Negative amounts (credit notes)
const edge5 = makeFullInvoice();
edge5.totals.netTotal = -100;
edge5.totals.vatTotal = -20;
edge5.totals.grossTotal = -120;
edge5.totals.vatBreakdown = [{ rate: 20, amount: -20 }];
edge5.lineItems = [{ description: 'Refund', quantity: -1, unitOfMeasure: 'ea', unitPrice: 100, lineTotal: -100, vatRate: 20, sku: null, discount: null }];
edge5.metadata.documentType = 'credit-note';
const edge5Result = formatOutput(edge5, 'json');
assert(typeof edge5Result === 'string', 'Credit note with negative amounts: exports OK');

// ══════════════════════════════════════════════════════════════
//  RESULTS
// ══════════════════════════════════════════════════════════════

console.log('\n══════════════════════════════════════════════');
console.log(`  Total: ${totalTests} | ✅ Passed: ${passed} | ❌ Failed: ${failed}`);
console.log('══════════════════════════════════════════════');

if (failures.length > 0) {
  console.log('\nFailed tests:');
  failures.forEach(f => console.log(`  ❌ ${f}`));
}

process.exit(failed > 0 ? 1 : 0);
