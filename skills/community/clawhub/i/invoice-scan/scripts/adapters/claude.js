/**
 * Claude (Anthropic) Provider Adapter
 * 
 * Normalises Claude's vision API response to the canonical schema.
 * This is the primary adapter for Phase 1.
 */

const { BaseAdapter } = require('./base');
const { createBlankInvoice } = require('../schema/canonical');

class ClaudeAdapter extends BaseAdapter {
  constructor() {
    super('claude');
  }

  /**
   * Build the extraction prompt for Claude.
   * Returns a structured prompt that produces consistent JSON output.
   */
  buildPrompt() {
    return `You are an expert document classifier and invoice data extractor.

STEP 1: First, classify this document. Determine what type it is:
- "invoice" — a commercial invoice requesting payment
- "credit-note" — a credit note / credit memo
- "receipt" — a payment receipt or till receipt (proof of payment ALREADY made, not a request for payment)
- "purchase-order" — a purchase order
- "delivery-note" — a delivery note or packing slip
- "confirmation" — a booking confirmation, order confirmation, or reservation
- "statement" — a bank or account statement
- "other-financial" — another financial document (quote, estimate, proforma)
- "not-financial" — not a financial document at all (screenshot, photo, letter, etc.)

STEP 2: If the document is an "invoice" or "credit-note", extract ALL data.
If it is any other type, still extract whatever financial data you can see, but set the documentType accordingly.

Key differences to watch for:
- RECEIPT vs INVOICE: A receipt confirms payment was made. An invoice requests payment. Look for words like "RECEIPT", "PAID", "Thank you for your payment" (receipt) vs "INVOICE", "Payment due", "Please pay" (invoice).
- CONFIRMATION vs INVOICE: Confirmations confirm a booking/order but don't request payment.
- PROFORMA vs INVOICE: Proforma invoices are estimates, not payment demands. Classify as "other-financial".

Return ONLY valid JSON with this exact structure (no markdown, no explanation):

{
  "documentType": "invoice|credit-note|receipt|purchase-order|delivery-note|confirmation|statement|other-financial|not-financial",
  "documentTypeConfidence": "high|medium|low",
  "documentTypeReason": "brief explanation of why you classified it this way",
  "invoiceNumber": "string or null",
  "invoiceDate": "YYYY-MM-DD or null",
  "dueDate": "YYYY-MM-DD or null",
  "currency": "ISO 4217 code (e.g., GBP, USD, EUR) or null",
  "supplier": {
    "name": "string or null",
    "address": "full address string or null",
    "vatNumber": "string or null"
  },
  "buyer": {
    "name": "string or null",
    "address": "full address string or null",
    "vatNumber": "string or null"
  },
  "lineItems": [
    {
      "description": "string",
      "quantity": number,
      "unitOfMeasure": "string or null",
      "unitPrice": number,
      "lineTotal": number,
      "vatRate": number or null,
      "sku": "string or null",
      "discount": number or null
    }
  ],
  "totals": {
    "netTotal": number or null,
    "vatBreakdown": [{ "rate": number, "amount": number }],
    "vatTotal": number or null,
    "grossTotal": number or null,
    "amountPaid": number or null,
    "amountDue": number or null
  },
  "charges": [
    {
      "type": "shipping|handling|insurance|surcharge|discount|other",
      "label": "original label from document (e.g. Postage & Packing, Freight, Delivery Charge)",
      "amount": number or null,
      "vatRate": number or null,
      "vatAmount": number or null
    }
  ],
  "referencedDocuments": {
    "poNumber": "string or null",
    "contractNumber": "string or null",
    "deliveryNote": "string or null",
    "inspectionReport": "string or null",
    "timesheetRef": "string or null",
    "projectRef": "string or null",
    "proformaRef": "string or null",
    "invoiceRef": "original invoice number if this is a credit/debit memo, or null",
    "creditNoteRef": "related credit note number, or null",
    "debitNoteRef": "related debit note number, or null",
    "other": [{ "type": "string", "reference": "string" }]
  },
  "paymentTerms": "string or null",
  "paymentReference": "string or null",
  "bankDetails": "freeform string with IBAN/BIC/account details or null",
  "language": "ISO 639-1 code (e.g., en, de, fr)",
  "handwrittenNotes": "any handwritten text found, or null",
  "stamps": [{ "type": "company|paid|approved|date|tax|other", "text": "extracted text" }],
  "confidence": "high|medium|low"
}

Rules:
- Extract ALL line items, even if the table is complex or spans multiple pages
- For currencies: detect from symbols (£=GBP, €=EUR, $=USD) or context
- For dates: always output as YYYY-MM-DD
- For VAT rates: output as percentage number (e.g., 20 not 0.2)
- Include any handwritten text or stamp text you can read
- If a field is genuinely not present on the invoice, use null (a retry pass will verify missing fields)
- Numbers MUST be actual JSON numbers using dot as decimal separator (e.g., 1234.56)
- Convert ALL locale-specific number formats to standard JSON numbers:
  - European: 1.234,56 → 1234.56
  - French: 1 234,56 → 1234.56  
  - Russian: 1 234-56 or 1 234.56 → 1234.56
  - Indian: 1,23,456.78 → 123456.78
  - Never use spaces, commas as thousands separators, or hyphens as decimal points in output
- If a number on the invoice uses a locale-specific format, YOU must convert it to standard decimal notation
- CHARGES: Capture shipping, postage, delivery, freight, handling, insurance, eco-levies, surcharges, and similar fees that appear OUTSIDE the line items table. Use the "charges" array. Common labels include: Shipping, S&H, Postage, P&P, Delivery, Freight, Carriage, Dispatch, Handling, Insurance. If a charge IS already a line item, do NOT duplicate it in charges. If no separate charges exist, return an empty array.`;
  }

  /**
   * Normalise Claude's response to canonical schema.
   * @param {object} raw - Parsed JSON from Claude's response
   * @returns {object} Canonical invoice
   */
  normalise(raw) {
    const invoice = createBlankInvoice();
    const startTime = Date.now();

    // Header
    invoice.header.invoiceNumber = raw.invoiceNumber || null;
    invoice.header.invoiceDate = this.normaliseDate(raw.invoiceDate);
    invoice.header.dueDate = this.normaliseDate(raw.dueDate);
    invoice.header.currency = this.normaliseCurrency(raw.currency);
    invoice.header.supplierName = raw.supplier?.name || null;
    invoice.header.supplierAddress = raw.supplier?.address || null;
    invoice.header.supplierVatNumber = raw.supplier?.vatNumber || null;
    invoice.header.buyerName = raw.buyer?.name || null;
    invoice.header.buyerAddress = raw.buyer?.address || null;
    invoice.header.buyerVatNumber = raw.buyer?.vatNumber || null;
    invoice.header.paymentTerms = raw.paymentTerms || null;
    invoice.header.paymentReference = raw.paymentReference || null;

    // Bank details
    if (raw.bankDetails) {
      if (typeof raw.bankDetails === 'string') {
        const parsed = this.parseBankDetailsFromString(raw.bankDetails);
        invoice.header.bankDetails.iban = parsed.iban;
        invoice.header.bankDetails.bic = parsed.bic;
      } else if (typeof raw.bankDetails === 'object') {
        invoice.header.bankDetails.iban = raw.bankDetails.iban || null;
        invoice.header.bankDetails.bic = raw.bankDetails.bic || null;
        invoice.header.bankDetails.accountNumber = raw.bankDetails.accountNumber || null;
        invoice.header.bankDetails.sortCode = raw.bankDetails.sortCode || null;
      }
    }

    // Referenced documents
    if (raw.referencedDocuments) {
      const rd = raw.referencedDocuments;
      if (rd.poNumber) invoice.referencedDocuments.push({ type: 'PO', reference: rd.poNumber });
      if (rd.contractNumber) invoice.referencedDocuments.push({ type: 'contract', reference: rd.contractNumber });
      if (rd.deliveryNote) invoice.referencedDocuments.push({ type: 'GRN', reference: rd.deliveryNote });
      if (rd.inspectionReport) invoice.referencedDocuments.push({ type: 'inspection', reference: rd.inspectionReport });
      if (rd.timesheetRef) invoice.referencedDocuments.push({ type: 'timesheet', reference: rd.timesheetRef });
      if (rd.projectRef) invoice.referencedDocuments.push({ type: 'project', reference: rd.projectRef });
      if (rd.proformaRef) invoice.referencedDocuments.push({ type: 'proforma', reference: rd.proformaRef });
      if (rd.invoiceRef) invoice.referencedDocuments.push({ type: 'invoice', reference: rd.invoiceRef });
      if (rd.creditNoteRef) invoice.referencedDocuments.push({ type: 'credit-note', reference: rd.creditNoteRef });
      if (rd.debitNoteRef) invoice.referencedDocuments.push({ type: 'debit-note', reference: rd.debitNoteRef });
      if (rd.other && Array.isArray(rd.other)) {
        for (const o of rd.other) {
          invoice.referencedDocuments.push({ type: o.type || 'other', reference: o.reference });
        }
      }
    }

    // Line items
    if (Array.isArray(raw.lineItems)) {
      invoice.lineItems = raw.lineItems.map(li => ({
        description: li.description || null,
        quantity: this.parseLocaleNumber(li.quantity),
        unitOfMeasure: li.unitOfMeasure || li.unit || null,
        unitPrice: this.parseLocaleNumber(li.unitPrice),
        lineTotal: this.parseLocaleNumber(li.lineTotal),
        vatRate: this.normaliseVatRate(li.vatRate),
        sku: li.sku || null,
        discount: typeof li.discount === 'number' ? li.discount : null,
      }));
    }

    // Totals
    if (raw.totals) {
      invoice.totals.netTotal = this.parseLocaleNumber(raw.totals.netTotal);
      invoice.totals.vatTotal = this.parseLocaleNumber(raw.totals.vatTotal);
      invoice.totals.grossTotal = this.parseLocaleNumber(raw.totals.grossTotal);
      invoice.totals.amountPaid = this.parseLocaleNumber(raw.totals.amountPaid);
      invoice.totals.amountDue = this.parseLocaleNumber(raw.totals.amountDue);
      if (Array.isArray(raw.totals.vatBreakdown)) {
        invoice.totals.vatBreakdown = raw.totals.vatBreakdown.map(vb => ({
          rate: this.normaliseVatRate(vb.rate),
          amount: typeof vb.amount === 'number' ? vb.amount : parseFloat(vb.amount) || 0,
        }));
      }
    }

    // Charges (shipping, handling, etc.)
    if (Array.isArray(raw.charges)) {
      invoice.charges = raw.charges.map(ch => ({
        type: ch.type || 'other',
        label: ch.label || null,
        amount: this.parseLocaleNumber(ch.amount),
        vatRate: this.normaliseVatRate(ch.vatRate),
        vatAmount: typeof ch.vatAmount === 'number' ? ch.vatAmount : null,
      }));
    }

    // Metadata
    invoice.metadata.provider = 'claude';
    invoice.metadata.language = raw.language || null;
    invoice.metadata.extractionTimestamp = new Date().toISOString();
    invoice.metadata.documentType = raw.documentType || null;

    // Document classification
    if (raw.documentType && !['invoice', 'credit-note'].includes(raw.documentType)) {
      invoice.validation.warnings.push({
        field: 'documentType',
        message: `Document classified as "${raw.documentType}" (not an invoice). Reason: ${raw.documentTypeReason || 'unknown'}`,
      });
    }

    // Store classification detail in fields
    if (raw.documentType) {
      invoice.fields.push({
        name: 'documentType',
        value: raw.documentType,
        confidence: ({ high: 0.95, medium: 0.80, low: 0.60 })[raw.documentTypeConfidence] || 0.80,
        boundingBox: null,
        extractionMethod: 'inferred',
        failureReason: null,
      });
      if (raw.documentTypeReason) {
        invoice.fields.push({
          name: 'documentTypeReason',
          value: raw.documentTypeReason,
          confidence: 1.0,
          boundingBox: null,
          extractionMethod: 'inferred',
          failureReason: null,
        });
      }
    }

    // Map confidence string to number
    const confMap = { high: 0.95, medium: 0.80, low: 0.60 };
    invoice.metadata.confidence = confMap[raw.confidence] || 0.80;

    // Stamps (store in fields array as additional data)
    if (Array.isArray(raw.stamps)) {
      for (const stamp of raw.stamps) {
        invoice.fields.push({
          name: `stamp.${stamp.type}`,
          value: stamp.text,
          confidence: 0.75,
          boundingBox: null,
          extractionMethod: 'stamp',
          failureReason: null,
        });
      }
    }

    // Handwritten notes
    if (raw.handwrittenNotes) {
      invoice.fields.push({
        name: 'handwrittenNotes',
        value: raw.handwrittenNotes,
        confidence: 0.70,
        boundingBox: null,
        extractionMethod: 'icr',
        failureReason: null,
      });
    }

    return invoice;
  }
}

module.exports = { ClaudeAdapter };
