/**
 * Schema Completeness Checker
 * 
 * Walks the canonical invoice and reports field completeness.
 * Distinguishes between:
 *   - populated: field has a real value
 *   - not_on_document: agent explicitly confirmed field isn't on the document
 *   - missing: field is null/undefined (agent may have forgotten it)
 * 
 * The sentinel value "__NOT_ON_DOCUMENT__" signals explicit absence.
 */

const NOT_ON_DOCUMENT = '__NOT_ON_DOCUMENT__';

/**
 * Fields to check for completeness.
 * Grouped by importance:
 *   - critical: should always be present on a valid invoice
 *   - important: usually present, worth retrying
 *   - optional: nice to have, don't retry
 */
const FIELD_SPECS = {
  critical: [
    { path: 'header.invoiceNumber', label: 'Invoice Number' },
    { path: 'header.invoiceDate', label: 'Invoice Date' },
    { path: 'header.currency', label: 'Currency' },
    { path: 'header.supplierName', label: 'Supplier Name' },
    { path: 'metadata.documentType', label: 'Document Type' },
    { path: 'totals.grossTotal', label: 'Gross Total' },
  ],
  important: [
    { path: 'header.supplierAddress', label: 'Supplier Address' },
    { path: 'header.supplierVatNumber', label: 'Supplier VAT Number' },
    { path: 'header.buyerName', label: 'Buyer Name' },
    { path: 'header.buyerAddress', label: 'Buyer Address' },
    { path: 'header.buyerVatNumber', label: 'Buyer VAT Number' },
    { path: 'header.dueDate', label: 'Due Date' },
    { path: 'header.paymentTerms', label: 'Payment Terms' },
    { path: 'header.paymentReference', label: 'Payment Reference' },
    { path: 'header.bankDetails.iban', label: 'IBAN' },
    { path: 'header.bankDetails.bic', label: 'BIC/SWIFT' },
    { path: 'header.bankDetails.accountNumber', label: 'Account Number' },
    { path: 'header.bankDetails.sortCode', label: 'Sort Code' },
    { path: 'totals.netTotal', label: 'Net Total' },
    { path: 'totals.vatTotal', label: 'VAT Total' },
    { path: 'totals.amountDue', label: 'Amount Due' },
  ],
  optional: [
    { path: 'totals.amountPaid', label: 'Amount Paid' },
    { path: 'totals.discount', label: 'Discount Amount' },
    { path: 'totals.discountRate', label: 'Discount Rate' },
    { path: 'metadata.language', label: 'Language' },
    { path: 'metadata.paidDate', label: 'Paid Date' },
    { path: 'metadata.vatInclusive', label: 'VAT Inclusive Flag' },
    { path: 'remarks', label: 'Remarks' },
  ],
};

/**
 * Resolve a dot-path on an object.
 * @param {object} obj 
 * @param {string} path - e.g. "header.bankDetails.iban"
 * @returns {*} value at path, or undefined if path doesn't exist
 */
function getByPath(obj, path) {
  return path.split('.').reduce((o, k) => (o != null ? o[k] : undefined), obj);
}

/**
 * Classify a field's status.
 * @param {*} value 
 * @returns {'populated'|'not_on_document'|'missing'}
 */
function classifyField(value) {
  if (value === NOT_ON_DOCUMENT) return 'not_on_document';
  if (value === null || value === undefined) return 'missing';
  if (typeof value === 'string' && value.trim() === '') return 'missing';
  return 'populated';
}

/**
 * Check completeness of an invoice against the schema.
 * 
 * @param {object} invoice - Canonical invoice object
 * @param {object} options
 * @param {boolean} options.includeOptional - Include optional fields in report (default: false)
 * @returns {object} Completeness report
 */
function checkCompleteness(invoice, options = {}) {
  const { includeOptional = false } = options;

  const levels = ['critical', 'important'];
  if (includeOptional) levels.push('optional');

  const report = {
    totalFields: 0,
    populated: 0,
    notOnDocument: 0,
    missing: 0,
    score: 0,           // 0.0 – 1.0 (populated / (populated + missing))
    missingFields: [],   // fields the agent may have forgotten
    confirmedAbsent: [], // fields confirmed not on document
    byLevel: {},
  };

  for (const level of levels) {
    const specs = FIELD_SPECS[level] || [];
    const levelReport = { total: 0, populated: 0, notOnDocument: 0, missing: 0, missingFields: [] };

    for (const spec of specs) {
      report.totalFields++;
      levelReport.total++;

      const value = getByPath(invoice, spec.path);
      const status = classifyField(value);

      switch (status) {
        case 'populated':
          report.populated++;
          levelReport.populated++;
          break;
        case 'not_on_document':
          report.notOnDocument++;
          levelReport.notOnDocument++;
          report.confirmedAbsent.push({ path: spec.path, label: spec.label, level });
          break;
        case 'missing':
          report.missing++;
          levelReport.missing++;
          report.missingFields.push({ path: spec.path, label: spec.label, level });
          levelReport.missingFields.push({ path: spec.path, label: spec.label });
          break;
      }
    }

    report.byLevel[level] = levelReport;
  }

  // Score: populated / (populated + missing). notOnDocument doesn't count against.
  const denominator = report.populated + report.missing;
  report.score = denominator > 0 ? Math.round((report.populated / denominator) * 100) / 100 : 1.0;

  // Line items completeness (separate — checked but not scored against header fields)
  if (Array.isArray(invoice.lineItems) && invoice.lineItems.length > 0) {
    report.lineItems = {
      count: invoice.lineItems.length,
      fieldsChecked: ['description', 'quantity', 'unitPrice', 'lineTotal'],
      itemsMissingFields: [],
    };

    invoice.lineItems.forEach((item, i) => {
      const missing = [];
      if (!item.description) missing.push('description');
      if (item.quantity == null) missing.push('quantity');
      if (item.unitPrice == null) missing.push('unitPrice');
      if (item.lineTotal == null) missing.push('lineTotal');
      if (missing.length > 0) {
        report.lineItems.itemsMissingFields.push({ index: i, missing });
      }
    });
  }

  return report;
}

/**
 * Get fields that should be retried (missing critical + important fields).
 * 
 * @param {object} invoice - Canonical invoice object
 * @returns {Array<{path: string, label: string, level: string}>} Fields to retry
 */
function getRetryFields(invoice) {
  const report = checkCompleteness(invoice);
  // Only retry critical and important fields
  return report.missingFields.filter(f => f.level === 'critical' || f.level === 'important');
}

/**
 * Build a focused retry prompt for missing fields.
 * 
 * @param {Array<{path: string, label: string}>} missingFields
 * @returns {string} Prompt text
 */
function buildRetryPrompt(missingFields) {
  const fieldList = missingFields.map(f => `- ${f.label} (${f.path})`).join('\n');

  return `You previously extracted data from this document but the following fields were returned as null:

${fieldList}

Please look at the document again carefully and for EACH field above, do ONE of:
1. Extract the value if it IS on the document
2. Return "__NOT_ON_DOCUMENT__" if it genuinely is NOT on the document, with a brief reason

Return ONLY valid JSON with this exact structure (no markdown, no explanation):

{
  "retryFields": [
    {
      "path": "the.field.path",
      "value": "extracted value OR __NOT_ON_DOCUMENT__",
      "reason": "brief explanation (required if __NOT_ON_DOCUMENT__)"
    }
  ]
}

Rules:
- Look MORE carefully than the first pass — these fields may be in headers, footers, stamps, or small print
- Numbers must be JSON numbers with dot decimal separator (e.g., 1234.56)
- Dates must be YYYY-MM-DD format
- If a field is genuinely not on the document, that's fine — just confirm it with "__NOT_ON_DOCUMENT__"
- Do NOT guess or hallucinate values. Only extract what you can actually see.`;
}

/**
 * Merge retry results back into the invoice.
 * 
 * @param {object} invoice - Canonical invoice object (mutated in place)
 * @param {Array<{path: string, value: any, reason: string}>} retryResults
 * @returns {object} Summary of what changed
 */
function mergeRetryResults(invoice, retryResults) {
  const summary = { recovered: [], confirmedAbsent: [], unchanged: [] };

  for (const result of retryResults) {
    const { path: fieldPath, value, reason } = result;

    if (value === NOT_ON_DOCUMENT) {
      summary.confirmedAbsent.push({ path: fieldPath, reason });
      // Leave as null — don't set the sentinel in the final output
      continue;
    }

    if (value === null || value === undefined) {
      summary.unchanged.push({ path: fieldPath });
      continue;
    }

    // Set the value on the invoice
    const parts = fieldPath.split('.');
    let target = invoice;
    for (let i = 0; i < parts.length - 1; i++) {
      if (target[parts[i]] == null) target[parts[i]] = {};
      target = target[parts[i]];
    }
    const lastKey = parts[parts.length - 1];
    target[lastKey] = value;
    summary.recovered.push({ path: fieldPath, value });
  }

  return summary;
}

module.exports = {
  NOT_ON_DOCUMENT,
  FIELD_SPECS,
  checkCompleteness,
  getRetryFields,
  buildRetryPrompt,
  mergeRetryResults,
};
