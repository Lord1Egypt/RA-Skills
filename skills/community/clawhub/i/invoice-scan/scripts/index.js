/**
 * invoice-scan
 * 
 * AI-powered invoice scanning — extract structured data from any invoice document.
 * 
 * @example
 *   const { scanInvoice, formatOutput } = require('invoice-scan');
 *   const invoice = await scanInvoice('invoice.pdf', { apiKey: '...' });
 *   const csv = formatOutput(invoice, 'csv');
 */

const { scanInvoice } = require('./extraction/scanner');
const { formatOutput, listFormats } = require('./output/index');
const { getAdapter, listProviders } = require('./adapters/index');
const { validateArithmetic } = require('./validation/arithmetic');
const { validateDocumentRules } = require('./validation/document-rules');
const { createBlankInvoice, validateSchema, SCHEMA_VERSION } = require('./schema/canonical');
const { checkCompleteness, getRetryFields, buildRetryPrompt, mergeRetryResults } = require('./validation/completeness');

module.exports = {
  // Core
  scanInvoice,

  // Output
  formatOutput,
  listFormats,

  // Adapters
  getAdapter,
  listProviders,

  // Schema
  createBlankInvoice,
  validateSchema,
  SCHEMA_VERSION,

  // Validation
  validateArithmetic,
  validateDocumentRules,

  // Completeness
  checkCompleteness,
  getRetryFields,
  buildRetryPrompt,
  mergeRetryResults,
};
