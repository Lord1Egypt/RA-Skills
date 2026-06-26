/**
 * Pre-export Pipeline
 * 
 * Normalises, validates, and fills defaults on an invoice object
 * before writing to any output format. Ensures consistent output
 * regardless of whether the invoice came from CLI mode or agent-native.
 * 
 * This is the single pipeline that both modes share.
 */

const { validateArithmetic } = require('../validation/arithmetic');
const { validateDocumentRules } = require('../validation/document-rules');
const { checkCompleteness } = require('../validation/completeness');

/**
 * Infer document type from available signals when the agent didn't set it.
 * Uses a weighted scoring system — not LLM discretion.
 * 
 * @param {object} invoice
 * @returns {string|null} inferred documentType or null if can't determine
 */
function inferDocumentType(invoice) {
  const h = invoice.header || {};
  const t = invoice.totals || {};
  const refs = invoice.referencedDocuments || [];
  const remarks = (invoice.remarks || '').toLowerCase();

  // Build searchable text from document CONTENT only — not JSON keys
  // This avoids false positives from field names like "invoiceNumber"
  const contentParts = [
    h.invoiceNumber, h.supplierName, h.buyerName,
    h.paymentTerms, h.paymentReference,
    remarks,
    ...(invoice.lineItems || []).map(li => li.description),
    ...(invoice.stamps || []).map(s => s.text),
    ...(invoice.charges || []).map(c => c.label),
  ].filter(Boolean);
  const allText = contentParts.join(' ').toLowerCase();

  // --- Signal scoring ---
  const scores = {
    'invoice': 0,
    'credit-note': 0,
    'debit-note': 0,
    'receipt': 0,
    'purchase-order': 0,
    'delivery-note': 0,
    'statement': 0,
    'other-financial': 0,
    'not-financial': 0,
  };

  // Credit note signals
  const creditSignals = ['credit note', 'credit memo', 'credit advice', 'gutschrift', 'avoir', 'nota de crédito', 'nota di credito', 'кредит'];
  if (creditSignals.some(s => allText.includes(s))) scores['credit-note'] += 5;
  if (refs.some(r => r.type === 'invoice')) scores['credit-note'] += 2; // references original invoice
  // Negative totals suggest credit
  if ((t.grossTotal != null && t.grossTotal < 0) || (t.netTotal != null && t.netTotal < 0)) scores['credit-note'] += 3;

  // Debit note signals
  const debitSignals = ['debit note', 'debit memo', 'lastschrift', 'nota de débito'];
  if (debitSignals.some(s => allText.includes(s))) scores['debit-note'] += 5;

  // Receipt signals
  const receiptSignals = ['receipt', 'thank you for your purchase', 'terminal id', 'auth code', 'cashier', 'till', 'change due', 'quittung', 'reçu', 'recibo'];
  const receiptHits = receiptSignals.filter(s => allText.includes(s)).length;
  scores['receipt'] += receiptHits * 2;

  // Purchase order signals
  const poSignals = ['purchase order', 'order confirmation', 'bestellung', 'bon de commande', 'orden de compra'];
  if (poSignals.some(s => allText.includes(s))) scores['purchase-order'] += 5;

  // Delivery note signals
  const dnSignals = ['delivery note', 'packing slip', 'lieferschein', 'bon de livraison', 'albarán'];
  if (dnSignals.some(s => allText.includes(s))) scores['delivery-note'] += 5;

  // Statement signals
  const stmtSignals = ['statement of account', 'account statement', 'kontoauszug'];
  if (stmtSignals.some(s => allText.includes(s))) scores['statement'] += 5;

  // Proforma → other-financial
  const proformaSignals = ['proforma', 'pro forma', 'pro-forma'];
  if (proformaSignals.some(s => allText.includes(s))) scores['other-financial'] += 5;

  // Invoice signals (positive indicators)
  const invoiceSignals = ['invoice', 'tax invoice', 'vat invoice', 'rechnung', 'facture', 'factura', 'fattura', 'faktura', 'фактура', 'счёт-фактура', '发票', 'fapiao'];
  const invHits = invoiceSignals.filter(s => allText.includes(s)).length;
  scores['invoice'] += invHits * 2;

  // Structural signals for invoice
  if (h.invoiceNumber) scores['invoice'] += 2;
  if (h.dueDate) scores['invoice'] += 1;
  if (h.supplierVatNumber || h.buyerVatNumber) scores['invoice'] += 1;
  if (h.bankDetails?.iban || h.bankDetails?.accountNumber) scores['invoice'] += 1;
  if (t.vatTotal != null && t.vatTotal > 0) scores['invoice'] += 1;

  // Find the highest-scoring type
  let best = null;
  let bestScore = 0;
  for (const [type, score] of Object.entries(scores)) {
    if (score > bestScore) {
      best = type;
      bestScore = score;
    }
  }

  // Only return if we have meaningful confidence (score >= 3)
  return bestScore >= 3 ? best : null;
}

/**
 * Prepare an invoice for export.
 * Mutates the invoice in place and returns it.
 * 
 * Steps:
 *   1. Ensure structural completeness (metadata, validation, stamps, etc.)
 *   2. Fill metadata defaults (provider, timestamp, documentType)
 *   3. Normalise field locations (top-level ↔ metadata.*)
 *   4. Run validators if not already run
 * 
 * @param {object} invoice - Invoice object (canonical or agent-native)
 * @returns {object} invoice - Same object, normalised and validated
 */
function prepareForExport(invoice) {
  // --- 1. Structural completeness ---
  if (!invoice.metadata) {
    invoice.metadata = {};
  }
  if (!invoice.validation) {
    invoice.validation = { arithmeticValid: null, errors: [], warnings: [] };
  }
  if (!Array.isArray(invoice.validation.errors)) {
    invoice.validation.errors = [];
  }
  if (!Array.isArray(invoice.validation.warnings)) {
    invoice.validation.warnings = [];
  }
  if (!Array.isArray(invoice.charges)) {
    invoice.charges = [];
  }
  if (!Array.isArray(invoice.stamps)) {
    invoice.stamps = [];
  }
  if (!Array.isArray(invoice.lineItems)) {
    invoice.lineItems = [];
  }
  if (!invoice.totals) {
    invoice.totals = {};
  }
  if (!Array.isArray(invoice.totals.vatBreakdown)) {
    invoice.totals.vatBreakdown = [];
  }
  if (!invoice.header) {
    invoice.header = {};
  }
  if (!Array.isArray(invoice.referencedDocuments)) {
    invoice.referencedDocuments = [];
  }
  if (!Array.isArray(invoice.fields)) {
    invoice.fields = [];
  }

  // --- 2. Fill metadata defaults ---
  const m = invoice.metadata;

  // Provider
  if (!m.provider) {
    m.provider = invoice.provider || 'agent-native';
  }

  // Extraction timestamp
  if (!m.extractionTimestamp) {
    m.extractionTimestamp = invoice.extractedAt || new Date().toISOString();
  }

  // Language
  if (!m.language) {
    m.language = invoice.language || null;
  }

  // Document type
  if (!m.documentType) {
    m.documentType = invoice.documentType || null;
  }

  // Confidence
  if (m.confidence === null || m.confidence === undefined) {
    if (invoice.qualityScore?.score !== null && invoice.qualityScore?.score !== undefined) {
      // qualityScore is a fraction (e.g. 6/9) — normalise if > 1
      const raw = invoice.qualityScore.score;
      const total = invoice.qualityScore.total || 9;
      m.confidence = raw > 1 ? Math.round((raw / total) * 100) / 100 : raw;
    }
  }

  // --- 3. Normalise field locations (bidirectional sync) ---
  // Top-level → metadata (for formatters that read metadata.*)
  // Already done above

  // metadata → top-level (for formatters that read top-level)
  if (!invoice.documentType && m.documentType) {
    invoice.documentType = m.documentType;
  }
  if (!invoice.language && m.language) {
    invoice.language = m.language;
  }
  if (!invoice.provider && m.provider) {
    invoice.provider = m.provider;
  }
  if (!invoice.extractedAt && m.extractionTimestamp) {
    invoice.extractedAt = m.extractionTimestamp;
  }

  // --- 3b. Infer documentType if missing ---
  // Programmatic inference so we don't rely on the agent's discretion
  if (!m.documentType) {
    m.documentType = inferDocumentType(invoice);
  }
  // Sync to top-level after inference
  if (m.documentType && !invoice.documentType) {
    invoice.documentType = m.documentType;
  }

  // --- 3c. Required field warnings ---
  // Flag critical missing fields so they show up in Validation tab
  const requiredFieldChecks = [
    { field: 'metadata.documentType', value: m.documentType, msg: 'Document type not detected — could not classify document' },
    { field: 'totals.grossTotal', value: invoice.totals.grossTotal, msg: 'Gross total not extracted' },
  ];

  // amountDue: required for invoices and debit notes (not receipts, not-financial, etc.)
  const dtLower = (m.documentType || '').toLowerCase();
  if (['invoice', 'debit-note', 'credit-note'].includes(dtLower)) {
    requiredFieldChecks.push(
      { field: 'totals.amountDue', value: invoice.totals.amountDue, msg: 'Amount due not extracted — required for ' + m.documentType },
    );
  }

  for (const check of requiredFieldChecks) {
    if (check.value === null || check.value === undefined) {
      // Only add if not already flagged
      const alreadyFlagged = invoice.validation.warnings.some(w => w.field === check.field && w.message === check.msg);
      if (!alreadyFlagged) {
        invoice.validation.warnings.push({ field: check.field, message: check.msg });
      }
    }
  }

  // --- 4. Completeness check ---
  if (!m.completeness) {
    const completenessReport = checkCompleteness(invoice);
    m.completeness = {
      score: completenessReport.score,
      populated: completenessReport.populated,
      missing: completenessReport.missing,
      notOnDocument: completenessReport.notOnDocument,
      retried: false,
      retryRecovered: 0,
      retryConfirmedAbsent: 0,
    };

    // Add missing field warnings
    for (const field of completenessReport.missingFields) {
      const alreadyFlagged = invoice.validation.warnings.some(
        w => w.field === field.path && w.message.includes('not extracted')
      );
      if (!alreadyFlagged) {
        invoice.validation.warnings.push({
          field: field.path,
          message: `${field.label} not extracted (${field.level} field)`,
        });
      }
    }
  }

  // --- 5. Run validators if not already run ---
  // Arithmetic: run if never executed (arithmeticValid is still null)
  if (invoice.validation.arithmeticValid === null) {
    validateArithmetic(invoice);
  }

  // Document rules: run if documentQuality not yet computed
  if (!invoice.validation.documentQuality) {
    validateDocumentRules(invoice);
  }

  return invoice;
}

module.exports = { prepareForExport };
