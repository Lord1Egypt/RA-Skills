/**
 * Output Format Registry
 * 
 * formatOutput() is the single entry point for all exports.
 * It runs the pre-export pipeline (normalise → validate → write)
 * regardless of whether the invoice came from CLI or agent-native mode.
 */

const { toJSON } = require('./json');
const { toCSV } = require('./csv');
const { toExcel } = require('./excel');
const { prepareForExport } = require('./prepare');

const formatters = {
  json: (invoice, opts) => toJSON(invoice, opts?.pretty !== false),
  csv: (invoice, opts) => toCSV(invoice, opts),
  excel: (invoice, opts) => toExcel(invoice, opts),
  xlsx: (invoice, opts) => toExcel(invoice, opts),
};

function formatOutput(invoice, format = 'json', options = {}) {
  const formatter = formatters[format];
  if (!formatter) {
    throw new Error(`Unknown format "${format}". Available: ${Object.keys(formatters).join(', ')}`);
  }

  // Run the pre-export pipeline: normalise → validate → then write
  prepareForExport(invoice);

  return formatter(invoice, options);
}

function listFormats() {
  return ['json', 'csv', 'excel'];
}

module.exports = { formatOutput, listFormats };
