/**
 * Excel (XLSX) Output Formatter
 * 
 * Produces a structured workbook with:
 * - Header sheet: invoice metadata
 * - Line Items sheet: line item details
 * - Validation sheet: confidence scores, flags, errors
 */

let XLSX;
try {
  XLSX = require('xlsx');
} catch (e) {
  XLSX = null;
}

/**
 * Convert canonical invoice to XLSX buffer.
 * @param {object} invoice
 * @returns {Buffer}
 */
function toExcel(invoice) {
  if (!XLSX) {
    throw new Error('xlsx package not installed. Run: npm install xlsx');
  }

  const wb = XLSX.utils.book_new();

  // --- Header Sheet ---
  const h = invoice.header;
  const headerData = [
    ['Field', 'Value'],
    ['Invoice Number', h.invoiceNumber],
    ['Invoice Date', h.invoiceDate],
    ['Due Date', h.dueDate],
    ['Currency', h.currency],
    ['Supplier Name', h.supplierName],
    ['Supplier Address', h.supplierAddress],
    ['Supplier VAT', h.supplierVatNumber],
    ['Buyer Name', h.buyerName],
    ['Buyer Address', h.buyerAddress],
    ['Buyer VAT', h.buyerVatNumber],
    ['Payment Terms', h.paymentTerms],
    ['Payment Reference', h.paymentReference],
    ['IBAN', h.bankDetails?.iban],
    ['BIC', h.bankDetails?.bic],
    ['Account Number', h.bankDetails?.accountNumber],
    ['Sort Code', h.bankDetails?.sortCode],
  ];

  // Referenced documents — shown early, especially important for credit/debit memos
  const refDocs = invoice.referencedDocuments || [];
  if (refDocs.length > 0) {
    headerData.push(['', '']);
    headerData.push(['── Related Documents ──', '']);
    for (const rd of refDocs) {
      const label = rd.type === 'invoice' ? 'Original Invoice'
        : rd.type === 'PO' ? 'Purchase Order'
        : rd.type;
      headerData.push([label, rd.reference]);
    }
  }

  // Metadata — paid date and VAT-inclusive flag
  if (invoice.metadata?.paidDate) {
    headerData.push(['Paid Date', invoice.metadata.paidDate]);
  }
  if (invoice.metadata?.vatInclusive !== null && invoice.metadata?.vatInclusive !== undefined) {
    headerData.push(['VAT Inclusive', invoice.metadata.vatInclusive ? 'YES' : 'NO']);
  }

  // Totals block
  headerData.push(
    ['', ''],
    ['── Totals ──', ''],
    ['Net Total', invoice.totals.netTotal],
  );

  // Insert charges between net and VAT (they affect the final total)
  const charges = invoice.charges || [];
  if (charges.length > 0) {
    for (const ch of charges) {
      const vatInfo = ch.vatRate != null ? ` (VAT ${ch.vatRate}%)` : '';
      headerData.push([`  + ${ch.label || ch.type}`, ch.amount != null ? ch.amount + vatInfo : '']);
    }
    const chargesNet = charges.reduce((sum, ch) => sum + (ch.amount || 0), 0);
    headerData.push(['  Charges Subtotal', chargesNet]);
  }

  // VAT breakdown with type labels
  const vatBkdn = invoice.totals.vatBreakdown || [];
  if (vatBkdn.length > 0) {
    for (const vb of vatBkdn) {
      const label = vb.type ? `  VAT: ${vb.type}` : `  VAT @ ${vb.rate != null ? vb.rate + '%' : '?'}`;
      headerData.push([label, vb.amount]);
    }
  }

  headerData.push(
    ['VAT Total', invoice.totals.vatTotal],
  );

  // Invoice-level discount
  if (invoice.totals.discount != null) {
    const discLabel = invoice.totals.discountRate != null
      ? `Discount (${invoice.totals.discountRate}%)`
      : 'Discount';
    headerData.push([discLabel, -Math.abs(invoice.totals.discount)]);
  }

  headerData.push(
    ['Gross Total', invoice.totals.grossTotal],
    ['Amount Paid', invoice.totals.amountPaid],
    ['Amount Due', invoice.totals.amountDue],
    ['', ''],
    ['Document Type', invoice.metadata?.documentType ?? invoice.documentType],
    ['Confidence', invoice.metadata?.confidence ?? invoice.qualityScore?.score],
    ['Language', invoice.metadata?.language ?? invoice.language],
    ['Provider', invoice.metadata?.provider ?? invoice.provider],
    ['Extracted At', invoice.metadata?.extractionTimestamp ?? invoice.extractedAt],
  );

  const headerSheet = XLSX.utils.aoa_to_sheet(headerData);
  headerSheet['!cols'] = [{ wch: 20 }, { wch: 50 }];
  XLSX.utils.book_append_sheet(wb, headerSheet, 'Header');

  // --- Line Items Sheet ---
  const lineItemHeaders = [
    'Description', 'Quantity', 'Unit', 'Unit Price',
    'Line Total', 'VAT Rate %', 'SKU', 'Discount',
  ];
  const lineItemRows = invoice.lineItems.map(li => [
    li.description, li.quantity, li.unitOfMeasure,
    li.unitPrice, li.lineTotal, li.vatRate, li.sku, li.discount,
  ]);
  const lineSheet = XLSX.utils.aoa_to_sheet([lineItemHeaders, ...lineItemRows]);
  lineSheet['!cols'] = [
    { wch: 40 }, { wch: 10 }, { wch: 10 }, { wch: 12 },
    { wch: 12 }, { wch: 12 }, { wch: 15 }, { wch: 12 },
  ];
  XLSX.utils.book_append_sheet(wb, lineSheet, 'Line Items');

  // --- Validation Sheet ---
  const valData = [
    ['Arithmetic Valid', invoice.validation.arithmeticValid ? 'YES' : 'NO'],
    ['', ''],
    ['Errors', ''],
  ];
  for (const err of invoice.validation.errors) {
    valData.push([err.field, err.message]);
  }
  if (invoice.validation.errors.length === 0) {
    valData.push(['(none)', '']);
  }
  valData.push(['', '']);
  valData.push(['Warnings', '']);
  for (const warn of invoice.validation.warnings) {
    valData.push([warn.field, warn.message]);
  }
  if (invoice.validation.warnings.length === 0) {
    valData.push(['(none)', '']);
  }

  // Add field confidence scores
  const fields = invoice.fields || invoice.validation?.fieldConfidence || [];
  if (fields.length > 0) {
    valData.push(['', '']);
    valData.push(['Field Confidence', '']);
    valData.push(['Field', 'Confidence', 'Method']);
    for (const f of fields) {
      valData.push([f.name ?? f.field, f.confidence, f.extractionMethod ?? f.method]);
    }
  }

  const valSheet = XLSX.utils.aoa_to_sheet(valData);
  valSheet['!cols'] = [{ wch: 30 }, { wch: 60 }, { wch: 15 }];
  XLSX.utils.book_append_sheet(wb, valSheet, 'Validation');

  return XLSX.write(wb, { type: 'buffer', bookType: 'xlsx' });
}

module.exports = { toExcel };
