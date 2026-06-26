# Canonical Invoice Schema v1.0.0

Every scan produces this structure regardless of AI provider.

## Top-Level

```
{ schemaVersion, header, referencedDocuments[], lineItems[], totals, metadata, fields[], validation, exceptions }
```

## header

invoiceNumber, invoiceDate (YYYY-MM-DD), dueDate, currency (ISO 4217), supplierName, supplierAddress, supplierVatNumber, buyerName, buyerAddress, buyerVatNumber, paymentTerms, paymentReference, bankDetails: { iban, bic, accountNumber, sortCode }

## lineItems[]

description, quantity, unitOfMeasure, unitPrice, lineTotal, vatRate (percentage), sku, discount

## referencedDocuments[]

type (PO|contract|GRN|inspection|timesheet|project|proforma|invoice|credit-note|debit-note|other), reference

For credit/debit memos: ALWAYS include a referencedDocument with type "invoice" and the original invoice number as reference. This is the primary link back to the original document.

## totals

netTotal, vatBreakdown[]: { rate, amount, type (optional — tax regime label e.g. "CGST", "SGST", "USt", "НДС") }, vatTotal, grossTotal, amountPaid, amountDue, discount (invoice-level discount amount), discountRate (percentage e.g. 10 for 10%)

## charges[]

Surcharges and fees that appear outside the line items table (shipping, handling, etc.). Do NOT duplicate items already captured as line items.

type (shipping|handling|insurance|surcharge|discount|other), label (original text from document, e.g. "P&P", "Freight"), amount (net, before tax), vatRate (percentage or null), vatAmount (explicit tax amount or null)

## stamps[]

type (company|paid|approved|date|tax|other), text

## remarks

Freeform string — any comments, notes, or remarks printed on the document (null if none).

## metadata

confidence (0.0–1.0), language (ISO 639-1), pageCount, processingDurationMs, provider, extractionTimestamp (ISO 8601), documentType, paidDate (YYYY-MM-DD — date from PAID stamp if present), vatInclusive (true if line totals include VAT, false if net, null if unknown)

## fields[]

Per-field detail: name, value, confidence, boundingBox ({ x, y, width, height, page } or null), extractionMethod (ocr|icr|stamp|inferred), failureReason

## validation

arithmeticValid (boolean), errors[]: { field, message }, warnings[]: { field, message }, documentQuality: { score, presentFields, totalChecked, rating (good|partial|poor) }

## exceptions

overallStatus (success|partial|failed|rejected), failedFields[], processingAttempts, rejectionReason
