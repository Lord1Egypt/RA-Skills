/**
 * CSV Output Formatter
 * 
 * Produces a flat CSV with one row per line item.
 * Header fields are repeated on each row.
 */

const DELIMITER = ',';

function escapeCSV(val) {
  if (val === null || val === undefined) return '';
  const str = String(val);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

/**
 * Convert canonical invoice to CSV string.
 * @param {object} invoice
 * @param {object} options
 * @param {string} options.delimiter - Column delimiter (default: comma)
 * @returns {string}
 */
function toCSV(invoice, options = {}) {
  const delim = options.delimiter || DELIMITER;

  const headers = [
    'invoiceNumber', 'invoiceDate', 'dueDate', 'currency',
    'supplierName', 'supplierAddress', 'supplierVatNumber',
    'buyerName', 'buyerAddress', 'buyerVatNumber',
    'paymentTerms', 'paymentReference',
    'lineDescription', 'lineQuantity', 'lineUnitOfMeasure',
    'lineUnitPrice', 'lineTotal', 'lineVatRate', 'lineSku', 'lineDiscount',
    'netTotal', 'chargesTotal', 'chargesDetail', 'vatTotal', 'grossTotal', 'amountPaid', 'amountDue',
    'originalInvoiceRef', 'referencedDocuments',
    'documentType', 'confidence', 'language', 'provider',
  ];

  const rows = [headers.join(delim)];

  const h = invoice.header;
  const t = invoice.totals;
  const m = invoice.metadata || {
    documentType: invoice.documentType,
    confidence: invoice.qualityScore?.score,
    language: invoice.language,
    provider: invoice.provider,
  };

  // Pre-compute charges summary
  const charges = invoice.charges || [];
  const chargesTotal = charges.reduce((sum, ch) => sum + (ch.amount || 0), 0) || null;
  const chargesDetail = charges.length > 0
    ? charges.map(ch => `${ch.label || ch.type}: ${ch.amount}`).join('; ')
    : null;

  // Pre-compute referenced documents
  const refDocs = invoice.referencedDocuments || [];
  const originalInvoiceRef = refDocs.find(rd => rd.type === 'invoice')?.reference || null;
  const refDocsDetail = refDocs.length > 0
    ? refDocs.map(rd => `${rd.type}: ${rd.reference}`).join('; ')
    : null;

  if (invoice.lineItems.length === 0) {
    // Single row with just header data
    const row = [
      h.invoiceNumber, h.invoiceDate, h.dueDate, h.currency,
      h.supplierName, h.supplierAddress, h.supplierVatNumber,
      h.buyerName, h.buyerAddress, h.buyerVatNumber,
      h.paymentTerms, h.paymentReference,
      '', '', '', '', '', '', '', '',
      t.netTotal, chargesTotal, chargesDetail, t.vatTotal, t.grossTotal, t.amountPaid, t.amountDue,
      originalInvoiceRef, refDocsDetail,
      m.documentType, m.confidence, m.language, m.provider,
    ].map(escapeCSV);
    rows.push(row.join(delim));
  } else {
    for (const li of invoice.lineItems) {
      const row = [
        h.invoiceNumber, h.invoiceDate, h.dueDate, h.currency,
        h.supplierName, h.supplierAddress, h.supplierVatNumber,
        h.buyerName, h.buyerAddress, h.buyerVatNumber,
        h.paymentTerms, h.paymentReference,
        li.description, li.quantity, li.unitOfMeasure,
        li.unitPrice, li.lineTotal, li.vatRate, li.sku, li.discount,
        t.netTotal, chargesTotal, chargesDetail, t.vatTotal, t.grossTotal, t.amountPaid, t.amountDue,
        originalInvoiceRef, refDocsDetail,
        m.documentType, m.confidence, m.language, m.provider,
      ].map(escapeCSV);
      rows.push(row.join(delim));
    }
  }

  return rows.join('\n');
}

module.exports = { toCSV };
